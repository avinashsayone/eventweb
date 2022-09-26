from django.contrib import admin
from eventmanagementtest.models import event_details, register
admin.site.register(register)
admin.site.register(event_details)
# Register your models here.
