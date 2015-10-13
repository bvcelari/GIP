from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

#import only the needed ones
from gip.models import *
from gip.utils import is_cliente

from django.db.models import Q

ELEMENTOS_POR_PAGINA = 8

@login_required(login_url='/mylogin/')
@user_passes_test(is_cliente)
def index_cliente(request):
    #we will retrieve Promo and show per Tarifa/User
    current_user = request.user
    username = str(current_user.username)
    current_page = "Inicio"
    promo_list = []
    #get user tarifa
    tarifas = Cliente.objects.filter(user_id=current_user.id).values('tarifa')
    for tarifa in tarifas:
      promo_to_add = Promo.objects.filter(tarifa=tarifa['tarifa'])
      if promo_to_add:
        for promo in promo_to_add:
         if promo.producto:
           promo_list.append(promo)
           #we should generate and add html of the product itself
         else:
           #we shoul send the html of the promo
           promo_list.append(promo) 
    #get tarifa:
    #Promo.objects.filter(tarifa=1)
    user_listas = Cliente.objects.get(id=current_user.id).listas.all()

    context = {'username': username, 
               'current_page': current_page,
               'user_listas': user_listas,
               'promo_list': promo_list}
    return render(request, 'cliente/index_cliente.html', context)

@login_required(login_url='/mylogin/')
@user_passes_test(is_cliente)
def productos_cliente(request):
    #we will retrieve Promo and show per Tarifa/User
    current_user = request.user
    username = str(current_user.username)
    current_page = "Productos"
    #get all the categories
    categorias_list = Categoria.objects.all()
    sub_categorias_list = []
    #TODO:filter using disable and filtering by tarifa my friend
    search_parameters = request.POST.copy()
    print search_parameters
    if search_parameters:
      #wipe out the csrf:
      search_parameters.pop('csrfmiddlewaretoken')
      #THE PAGINATION DO NOT WORK
      full_search = Q()
      if 'search' in search_parameters:
        #Miss split words and do it smart
        search_string=Q(nombre__icontains=search_parameters['search']) |  Q(descripcion__icontains=search_parameters['search'])# ' %(search_parameters['search'],search_parameters['search'])
        full_search = full_search & search_string
      if 'categoria' in search_parameters:
        cat_id = Categoria.objects.get(nombre=search_parameters['categoria']).id
        search_cat = Q(categoria__id=Categoria.objects.get(nombre=search_parameters['categoria']).id)
        full_search = full_search & search_cat
      if 'subcategoria' in search_parameters:
        #TODO:is not tested, Will be necessary look for the father first, or check in the models :/
        subcat_id = Categoria.objects.get(nombre=search_parameters['subcategoria']).id
        search_subcat = Q(categoria__id=Categoria.objects.get(nombre=search_parameters['categoria']).id)
        full_search = full_search & search_subcat
      all_product_list = Producto.objects.filter(full_search)
      paginator = Paginator(all_product_list, ELEMENTOS_POR_PAGINA)
      page = request.GET.get('page')
    else:
      all_product_list = Producto.objects.all()
      #this is he default search
      paginator = Paginator(all_product_list, ELEMENTOS_POR_PAGINA)
      page = request.GET.get('page')
    try:
        product_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        product_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        product_list = paginator.page(paginator.num_pages)
    #Get the listas 
    user_listas = Cliente.objects.get(id=current_user.id).listas.all()
    context = {'username': username,
               'current_page': current_page,
               'product_list': product_list,
               'categorias_list': categorias_list,
               'sub_categorias_list': sub_categorias_list,
               'user_listas': user_listas,
               'search_parameters': search_parameters
		}
               
    return render(request, 'cliente/productos_cliente.html', context)



@login_required(login_url='/mylogin/')
@user_passes_test(is_cliente)
def listas_cliente(request):
    current_user = request.user
    username = str(current_user.username)
    current_page = "Listas"
    user_listas = Cliente.objects.get(id=current_user.id).listas.all()
    form_parameters = request.POST.copy()
    print form_parameters
    if form_parameters:
      print "something comes up!"
    print user_listas
    ##TODO: decide if should be all the lists retrieved here or Ajax
    full_listas = {}
    for lista_i in user_listas:
      full_listas[lista_i]= Elemento.objects.filter(lista_id = lista_i.id)

      #retrieve listas here, you should check the query generated by ORM and check indexes 
    print type(full_listas)

    context = {'username': username,
               'current_user': current_user,
               'current_page': current_page,
               'user_listas': user_listas,
               'full_listas': full_listas,
                }

    return render(request, 'cliente/listas_cliente.html', context)

@login_required(login_url='/mylogin/')
@user_passes_test(is_cliente)
def listas_add_cliente(request,user_id):
  search_parameters = request.POST.copy()
  my_cli = Cliente.objects.get(id=user_id)
  lis = Lista(nombre=search_parameters['lista_to_add'])
  lis.save()
  my_cli.listas.add(lis.id)
  print lis.id
  # Always return an HttpResponseRedirect after successfully dealing
  # with POST data. This prevents data from being posted twice if a
  # user hits the Back button.
  return HttpResponseRedirect(reverse('listas_cliente'))

@login_required(login_url='/mylogin/')
@user_passes_test(is_cliente)
def elemento_add_cliente(request, lista_id):
  pass

@login_required(login_url='/mylogin/')
@user_passes_test(is_cliente)
def add_tolist(request):
  search_parameters = request.POST.copy()
  print search_parameters
  return HttpResponseRedirect(reverse('index_cliente'))


#    current_user = request.user
#    username = str(current_user.username)
#    current_page = "Listas"
#    user_listas = Cliente.objects.get(id=current_user.id).listas.all()
#    form_parameters = request.POST.copy()
#    print form_parameters
#    if form_parameters:
#      print "something comes up!"
#    print user_listas
#    ##TODO: decide if should be all the lists retrieved here or Ajax
#    full_listas = {}
#    for lista_i in user_listas:
#      full_listas[lista_i]= Elemento.objects.filter(lista_id = lista_i.id)
#
#      #retrieve listas here, you should check the query generated by ORM and check indexes 
#    print type(full_listas)
#
#    context = {'username': username,
#               'current_user': current_user,
#               'current_page': current_page,
#               'user_listas': user_listas,
#               'full_listas': full_listas,
#                }
#
#    return render(request, 'cliente/listas_cliente.html', context)

