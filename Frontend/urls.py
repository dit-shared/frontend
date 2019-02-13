from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [
	path('', views.redirect),
    path('admin/', admin.site.urls),
    path('auth/', include('Account.auth_urls')),
    path('account/', include('Account.account_urls')),
]
