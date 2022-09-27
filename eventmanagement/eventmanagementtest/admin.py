from django.contrib import admin
from eventmanagementtest.models import OrderDetail, event_details, register
admin.site.register(register)
admin.site.register(event_details)
admin.site.register(OrderDetail)
# Register your models here.
