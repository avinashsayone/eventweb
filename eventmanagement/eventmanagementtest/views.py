from pathlib import Path
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from eventmanagementtest.models import OrderDetail, register,event_details
from eventmanagementtest.form import Register,Addevent
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.base import TemplateView
from django.conf import settings # new
from django.http.response import JsonResponse,HttpResponse # new
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.shortcuts import get_object_or_404
import stripe
import json
from django.core.files.storage import FileSystemStorage
import os
BASE_DIR = Path(__file__).resolve().parent.parent

def index(request):
    data_obj= event_details.objects.get_queryset().order_by('-date')
    p = Paginator(data_obj, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    if 'user_id' not in request.session:
        user_obj=None
        return render(request, "index.html", {'user_obj': user_obj, 'permission': False,'data':page_obj})
    else:
        user_obj = register.objects.filter(username=request.session['user_id']).values('pk', 'name', 'age', 'address', 'username', 'phonenumber')
        
        return render(request, "index.html", {'user_obj': user_obj, 'permission': True,'data':page_obj})


def registerform(request):
    user='none'
    name='none'
    age='none'
    password='none'
    address='none'
    phonenumber='none'
    s=[]
    if request.method=='POST':

        log=Register(request.POST)
        if log.is_valid():

            user=log.cleaned_data['username']

            name=log.cleaned_data['name']

            age=log.cleaned_data['age']

            password=log.cleaned_data['password']

            address=log.cleaned_data['address']

            phonenumber=log.cleaned_data['phonenumber']

            a=register(username=user,name=name,age=age,password=password,address=address,phonenumber=phonenumber)
            a.save()
        s=(user,name,age,password,address,phonenumber)
    return HttpResponseRedirect('/login')

def login(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            check_exist = register.objects.filter(username=username).exists()
            if check_exist == False:
                messages.success(request, 'User not Exist')
                return HttpResponseRedirect('/login')
            else:
                
                messages.success(request, 'success')
            login_obj = register.objects.filter(username=username).values('pk','name','username','password')
            request.session['pk']=login_obj[0]['pk']
            request.session['user_id'] = login_obj[0]['username']
            if login_obj[0]['password'] == password:
                return HttpResponseRedirect('/')
            else:
                return redirect('login')
                return HttpResponseRedirect('/index')
            messages.success(request, 'Wrong password')
        else:
            return render(request, "login.html")
    except Exception as e:
        print(e)

def Logout(request):

    try:
        if request.session.has_key('user_id'):
            # del request.session['user_id']
            request.session.flush()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')
    except Exception as e:
        return HttpResponse(e)

def addevent(request):
    event_name='none'
    description='none'
    date='none'
    time='none'
    s=[]

    if request.method=='POST':
        log=Addevent(request.POST)
        if log.is_valid():

            event_name=log.cleaned_data['event_name']

            description=log.cleaned_data['description']

            date=log.cleaned_data['date']

            time=log.cleaned_data['time']
            event_pic = request.FILES.get('propic')
            if event_pic:
                fs = FileSystemStorage()
                name = fs.save(event_pic.name, event_pic)
                name = 'media/' + name
                path = os.path.join(BASE_DIR, name)
            user=register.objects.get(username=request.session.get('user_id'))
            events=event_details(event_name=event_name,description=description,date=date,time=time,user=user,event_image=event_pic)
            events.save()
        s=(event_name,description,date,time)
    return HttpResponseRedirect('/create-checkout-session')

class HomePageView(TemplateView):
    template_name = 'payment.html'

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request):
    product=event_details.objects.filter(user=request.session['pk']).order_by('-id')
    # request_data = json.loads(request.body)
    # product = get_object_or_404(event_details, object_id=id)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        # Customer Email is optional,
        # It is not safe to accept email directly from the client side
        customer_email = product[0].user.username,
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                    'name': product[0].event_name,
                    },
                    'unit_amount': int(20 * 100),
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('success')
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('cancelled')),
    )

    # OrderDetail.objects.create(
    #     customer_email=email,
    #     product=product, ......
    # )
    order = OrderDetail()
    order.customer_email = product[0].user.username
    order.product = product[0]
    order.stripe_payment_intent = checkout_session['payment_intent']
    order.amount = int(20 * 100)
    order.has_paid = True
    order.save()

    # return JsonResponse({'data': checkout_session})
    # return JsonResponse({'sessionId': checkout_session.id})
    return HttpResponseRedirect(checkout_session['url'])

def SuccessView(request):
    return HttpResponseRedirect('/')
def CancelledView(request):
    return HttpResponseRedirect('/addevent')



@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        # TODO: run some custom code here

    return HttpResponse(status=200)


def Delete_data(request,id):
    try:
        event=event_details.objects.get(id=id)
        event.delete()

        return HttpResponseRedirect('/')
    
    except Exception as e:
        print(e)   