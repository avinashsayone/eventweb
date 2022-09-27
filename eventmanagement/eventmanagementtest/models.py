import uuid
from django.db import models

# Create your models here.
# from __future__ import unicode_literals

from django.db import models
class register(models.Model):
    name=models.CharField(max_length=20)
    age=models.CharField(max_length=3)
    address=models.TextField()
    phonenumber=models.CharField(max_length=20)
    email=models.EmailField(max_length=50,blank=True,null=True)
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=20)
    def __str__(self):
        return (self.username )
    class Meta:
        db_table = 'register'
# Create your models here.
# class register_member(models.Model):
#     name=models.CharField(max_length=20)
#     age=models.CharField(max_length=3)
#     address=models.CharField(max_length=75)
#     phonenumber=models.CharField(max_length=20)
#     userid=models.CharField(max_length=20)
#     def __str__(self):
#         return (self.userid )
class event_details(models.Model):
    event_name=models.CharField(max_length=100)
    user=models.ForeignKey("register", on_delete=models.DO_NOTHING)
    description=models.TextField()
    date=models.DateField()
    time=models.TimeField()
    object_id=models.UUIDField(default=uuid.uuid4, editable=False)
    event_image = models.FileField(blank=True, upload_to="media")
    # def __str__(self):
    #     return(self.userids + '-' +self.bookname)



class OrderDetail(models.Model):

    id = models.BigAutoField(
        primary_key=True
    )

    # You can change as a Foreign Key to the user model
    customer_email = models.EmailField(
        verbose_name='Customer Email'
    )

    product = models.ForeignKey(
        to=event_details,
        verbose_name='Product',
        on_delete=models.CASCADE
    )

    amount = models.IntegerField(
        verbose_name='Amount'
    )

    stripe_payment_intent = models.CharField(
        max_length=200,null=True
    )

    # This field can be changed as status
    has_paid = models.BooleanField(
        default=False,
        verbose_name='Payment Status'
    )

    created_on = models.DateTimeField(
        auto_now_add=True
    )

    updated_on = models.DateTimeField(
        auto_now_add=True
    )