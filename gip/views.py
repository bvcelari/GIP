from django.shortcuts import render

#from gip.models import *
#from gip.views_cliente import *
from django.contrib.auth.decorators import login_required, user_passes_test
from gip.utils import is_cliente, is_proveedor
from django.shortcuts import resolve_url
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.models import User, Group
#from DRF
from rest_framework import viewsets
from serializers import UserSerializer, GroupSerializer










def index(request):
    my_test_string = 'Oh! Yeah!'
    context = {'my_test_string': my_test_string}
    return render(request, 'index.html', context)

@login_required(login_url='/mylogin/')
def login_redirect(request):
    redirect_to = resolve_url('/mylogout/')
    if User.objects.get(username=request.user).groups.filter(name='cliente').exists():
      redirect_to = resolve_url(settings.LOGIN_REDIRECT_CLIENTE) 
    elif User.objects.get(username=request.user).groups.filter(name='proveedor').exists():
      redirect_to = resolve_url(settings.LOGIN_REDIRECT_PROVEEDOR)
    else:
      print "someone is logged inand is not a client or a proveedor, Who?" +str(request.user)
    return HttpResponseRedirect(redirect_to)

    

#views for DRF

class UserViewVSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None):
        if pk == 'i':
            return Response(UserSerializer(request.user,
                context={'request':request}).data)
        return super(UserViewSet, self).retrieve(request, pk)

