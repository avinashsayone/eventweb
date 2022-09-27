"""eventmanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView , ListView
from django.conf import settings
from django.conf.urls.static import static

from eventmanagementtest import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('event-management/', include('eventmanagementtest.urls')),
    path('', views.index, name='home'),
    # path('home/', TemplateView.as_view(template_name='index.html'), name='home'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),
    path('register-user/', views.registerform, name='registers'),
    path('login/', views.login, name='login'),
    path('logout/', views.Logout,name='logout'),
    path('addevents/', views.addevent, name='addevents'),
    path('addevent/', TemplateView.as_view(template_name='addevent.html'), name='addevent'),
    path('payment/', views.HomePageView.as_view(), name='payment'),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    path('success/', views.SuccessView,name='success'), # new
    path('cancelled/', views.CancelledView,name='cancelled'),
    path('webhook/', views.stripe_webhook),
    path('delete/<int:id>', views.Delete_data,name='deleted'),
    
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL,
                                                                         document_root=settings.MEDIA_ROOT)
