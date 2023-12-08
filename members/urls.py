from django.urls import path
from . import views


urlpatterns = [
    path(' ', views.sflogin, name='sflogin'),
    path('sflogout', views.sflogout, name='sflogout'),

]