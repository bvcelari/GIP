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
from gip import views_cliente
from gip import views_proveedor

##All this urls are beyond /cliente/ :)
urlpatterns = [
    url(r'^$', views_cliente.index_cliente, name='index_cliente'),
    url(r'^productos/$', views_cliente.productos_cliente, name='productos_cliente'),
    url(r'^listas/$', views_cliente.listas_cliente, name='listas_cliente'),
    url(r'^listas/add/(?P<user_id>[0-9]+)$', views_cliente.listas_add_cliente, name='listas_add_cliente'),
    url(r'^listas/del/(?P<user_id>[0-9]+)$', views_cliente.listas_del_cliente, name='listas_del_cliente'),
    url(r'^listas/update/$', views_cliente.listas_update_cliente, name='listas_update_cliente'),
    url(r'^add_tolist/(?P<lista_id>[0-9]+)/(?P<producto_id>[0-9]+)$', views_cliente.add_tolist, name='add_tolist'),
    url(r'^del_fromlist/(?P<lista_id>[0-9]+)/(?P<elemento_id>[0-9]+)$', views_cliente.del_fromlist, name='del_fromlist'),
    url(r'^listas/add_custom/$', views_cliente.lista_add_custom, name='lista_add_custom'),
    url(r'^elemento/update/$', views_cliente.element_update_list, name='element_update_list'),
    url(r'^pedidos/$', views_cliente.pedidos , name='pedidos'),
    url(r'^make/pedido/$', views_cliente.make_pedido , name='make_pedido'),
    url(r'^historico/$', views_cliente.historico, name='historico'),
    url(r'^encurso/$', views_cliente.pedidos_en_curso, name='pedidos_en_curso'),
]
