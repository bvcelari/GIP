"""gip URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from gip import views
from gip import views_cliente
from gip import views_proveedor
from gip import cliente_urls
from gip import proveedor_urls
from django.contrib.auth.views import login, logout
from rest_framework.authtoken.views import obtain_auth_token





urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^cliente/', include(cliente_urls)),
    url(r'^proveedor/', include(proveedor_urls)),
    url(r'^login_redirect/', views.login_redirect, name='login_redirect'),
    #common urls
    url(r'^mylogin/$', login),
    url(r'^mylogout/$', logout),
#url('^accounts/', include('django.contrib.auth.urls')),
]
#this should be a folder in nginx
from django.conf.urls.static import static
from django.conf import settings

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [ url(r'^obtain-auth-token/$', obtain_auth_token) ]
