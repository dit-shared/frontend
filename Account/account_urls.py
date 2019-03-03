from django.urls import path
from . import views

urlpatterns = [
    path('', views.account, name='account'),
    path('upload', views.upload, name='upload'),
    path('predict', views.predict, name='predict'),
    path('view', views.view, name='view'),

    # temporary handlers
    path('encpass', views.encPasswd, name='encPasswd'),
]