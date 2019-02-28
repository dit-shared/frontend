from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='account'),
    path('encpass', views.encPasswd, name='encPasswd'),
]