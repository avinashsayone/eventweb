from django.urls import path
from . import views
from django.views.generic import TemplateView , ListView
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', TemplateView.as_view(template_name='index.html'), name='home'),
    path('register/', views.registerform, name='registers'),

]