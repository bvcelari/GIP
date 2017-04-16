##FROM BASH :  export DJANGO_SETTINGS_MODULE=gip.settings
##FROM BASH :  cd /home/adminuser/GIP/

import django
import random
import datetime
import time
django.setup()


from django.conf import settings

import rlcompleter, readline
readline.parse_and_bind('tab:complete')
from django.db import models
from gip.models import Tarifas
from gip.models import Destinos
from gip.models import Proveedor
from gip.models import Producto
from gip.models import Pedidos
from gip.models import Cliente
from gip.models import Carrito
      
from gip.models import Categoria
from gip.models import Lista
from gip.models import Elemento
from gip.helper_pedidos import send_order
from gip.helper_proveedor import list_grouper, generator_pedidos_tabs, generator_pedido_content


from django_fsm import FSMField, transition
from django.contrib.auth.models import User, Group

##FFS add all this in one file settings??
ELEMENTOS_POR_PAGINA_PROVEEDOR = 20
ELEMENTOS_POR_PAGINA_CLIENTE = 5
PROVEEDOR_ATTRIBUTE = 'proveedor'
CLIENTE_ATTRIBUTE = 'cliente'
##END FFS add all this in one file settings??

#Roles definition
grupocliente = Group.objects.create(name='cliente')
grupocliente.save()
grupoproveedor = Group.objects.create(name='proveedor')
grupoproveedor.save()




#I want ot create 20K products, 25 providers and 10K clients.
MAX_DESTINOS = 25
MAX_TARIFAS = 4
MAX_PROVEEDORES = 3
MAX_PRODUCTOS = 7000
MAX_PRODUCTOS = 1000
MAX_PRODUCTOS = 100
MAX_PRODUCTOS = 10 #just for the demo
MAX_CLIENTES = 2000
MAX_CLIENTES = 200
MAX_CLIENTES = 20
MAX_LISTAS= 5
MAX_CATEGORIAS = 8
MAX_ELEMENTOS = 25
#2.5K codigos postales
print "Current time " + time.strftime("%X")
print "creating destions... "
#for i in range(1,2500):
for i in range(1,MAX_DESTINOS):
  b = Destinos(codigo=i, nombre='CP - '+str(i))
  b.save()
  #time.sleep(0.01)

print "Current time " + time.strftime("%X")
#only 25 providers
print "creating providers... "
for i in range(1,MAX_PROVEEDORES):
  user = User.objects.create_user('PROVEEDOR'+str(i), 'p@p.com', 'password')
  grupo = Group.objects.create(name='Empresa Proveedor'+str(i))
  user.groups.add(grupo)
  user.groups.add(grupoproveedor)
  user.save()
  c = Proveedor(user=user, nombre='Proveedor'+str(i), descripcion='Descripcion'+str(i))
  c.save()
  #a provider can work in 350 CP
  for k in range(1,MAX_DESTINOS-1):
    c.destinos_reparto.add(random.randint(1,MAX_DESTINOS-1))
  c.save()
  ##and has 5 rates
  #for i in range(1,5):
  #  c.tipos_tarifas.add(random.randint(1,25))
  #c.save()
  
print "Current time " + time.strftime("%X")
  
#to do that, i need Tarifas 125 tarifas and 2.5K CP
print "creating tarifas... "
for i in range(1,MAX_TARIFAS):
  for j in Group.objects.all().filter(name__icontains='proveedor').exclude(name='proveedor'):
    a = Tarifas(nombre='tarifa'+str(i), descripcion='descripcion'+str(i), elproveedor_id=j.id)
    a.save()
  #time.sleep(0.01)

print "Current time " + time.strftime("%X")

print "Creating categorias..."
for i in range(1,MAX_CATEGORIAS):
  cat = Categoria(nombre='categoria'+str(i),short_url='categoria-'+str(i))
  cat.save()

print "Current time " + time.strftime("%X")
print "Creating listas"
for i in range(1,MAX_LISTAS*MAX_CLIENTES):
  #the client_id is uniq, the list is random sample
  lis = Lista(nombre='lista'+str(i))
  lis.save()

#here comes... 25K products
#for i in range(1,25000):
###Should not be needed, we are usinng "real" data
##print "Current time " + time.strftime("%X")
##print "creating provducts... "
##for i in range(1,MAX_PRODUCTOS):
## Not tested!!!
##  p = grupo[len(grupo)-1]
##  d = Producto(nombre='Producto'+str(i), descripcion='Descripcion'+str(i), formato='Formato'+str(i), caducidad_precio = datetime.datetime.now() + datetime.timedelta(days=1), proveedor=p,tarifa_id=random.randint(1,MAX_TARIFAS -1 ), categoria_id=random.randint(1,MAX_CATEGORIAS-1 ) )
##  d.save()
##
##print "Current time " + time.strftime("%X")



##here comes... 25K products
##for i in range(1,25000):
#print "Current time " + time.strftime("%X")
#print "creating provducts... "
#print "we are loading from a json"
##0: Nombre
##3: Producto ID
##4: Formato
##5: Descripcion
##7: Imagen
import json
from pprint import pprint

with open('./small_data_set.json') as data_file:
    data = json.load(data_file)


for i in data:
  ##Not tested, p may fail!!
  ##Not tested, p may fail!!
  for j in Group.objects.all().filter(name__icontains='proveedor').exclude(name='proveedor'):
    tarifas_availables = Tarifas.objects.filter(elproveedor=j.id)
    for t in tarifas_availables:
    #May crash due to fechacreacion o fechaupdate... they has default, shoudl not happen
      d = Producto(nombre = data[i][0].encode('utf-8'), descripcion = data[i][5].encode('utf-8'), formato = data[i][4].encode('utf-8'), caducidad_precio = datetime.datetime.now() + datetime.timedelta(days=1), proveedor_id=j.id,tarifa_id=t.id , categoria_id=random.randint(1,MAX_CATEGORIAS-1 ),image_url= data[i][7].encode('utf-8'), product_ref=data[i][3].encode('utf-8'), precio = random.randint(1,100) )
      d.save()
#
#print "Current time " + time.strftime("%X")



#and now, the clients, 2K
#for i in range(1,2001):
print "Current time " + time.strftime("%X")
print "creating clients... "
for i in range(1,MAX_CLIENTES):
  ##HERE, redo this, Will only work with one proveedor
  proveedor = Group.objects.all().exclude(name=CLIENTE_ATTRIBUTE)[0]
  user = User.objects.create_user('CLIENTE'+str(i), 'p@p.com', 'password')
  user.groups.add(grupocliente)
  user.save()
  grupo_cliente = Group.objects.get(name='cliente')
  grupo_proveedor = Group.objects.get(id=proveedor.id)
  user.groups.add(grupo_cliente)
  user.groups.add(grupo_proveedor)
  user.save()
  cliente = Cliente(user=user, nombre='Cliente'+str(i), descripcion='Descripcion'+str(i), cif='NIFNIFNIF'+str(i), direccion='calle direccion' ,ciudad='ciudadXX', telefono='telefono 123', contacto_nombre='Contact'+str(i) )
  #a client can has more than one CP
  cliente.save()
  for k in range(1,random.randint(2,5)):
    for j in Group.objects.all().filter(name__icontains='proveedor').exclude(name='proveedor'):
      #TODO: it does not work, only a tarif per client-provider pair
      tarifas_availables = Tarifas.objects.filter(elproveedor=j.id)
      tarif_per_proveedor = tarifas_availables[random.randint(0,len(tarifas_availables)-1)]
      cliente.tarifa.add(tarif_per_proveedor.id)
  for k in range(1,random.randint(2,5)):
    #probably there is something wrong here with listas and products per client...
    cliente.listas.add(random.randint(1,MAX_CATEGORIAS-1))
  for k in range(1,random.randint(2,5)):
    cliente.destino_reparto.add(random.randint(1,MAX_DESTINOS-1))
  cliente.save()

print "Current time " + time.strftime("%X")



print "Current time " + time.strftime("%X")
print "Creating Elementos"
for i in range(1,MAX_LISTAS*MAX_ELEMENTOS*MAX_CLIENTES):
  #the client_id is uniq, the list is random sample
  p = random.randint(1,MAX_PRODUCTOS- 1 )
  #TODO: p can be empty, 
  l = random.randint(1,MAX_LISTAS*MAX_CLIENTES- 1 )
  c = random.randint(1,20)
  ele = Elemento(nombre='elem'+str(i),cantidad= c, lista_id= l )
  ele.save()
  #we saved a custom element
  p = Producto.objects.get(id= p )
  e = Elemento(nombre=p.nombre , cantidad= c, producto_id = p.id, lista_id= l )
  e.save()
  #we saved a product in a list

print "Current time " + time.strftime("%X")


#Updateing user passowrds..
print "Current time " + time.strftime("%X")
print "Updating passwords"
for i in User.objects.all().exclude(username='root'):
  i.set_password('1')
  i.save()

print "Current time " + time.strftime("%X")

##HERE, redo this, You are missing the grupo de proveedor that belongs to each user....
##Need to spend some time adding Pedidos, and Pedidos status... 

#Lets do some pedidos...
print "Current time " + time.strftime("%X")
print "an order per user, at least"
for user in User.objects.filter(username__contains='CLIENTE'):
  user_listas = Cliente.objects.get(user_id=user.id).listas.all()
  cliente = Cliente.objects.filter(user_id = user.id)
  proveedor = cliente[0].user.groups.exclude(name=CLIENTE_ATTRIBUTE)[0]
  pedido = {}
  cliente_values = cliente.values()[0]
  orden = {}
  descripcion = {}
  precio = {}
  active = {}
  c_pedido, c_nombre, c_cantidad, c_lista, c_stock_optimo, c_existencias = {}, {}, {}, {}, {}, {}
  for lista_i in user_listas:
    current_list = Elemento.objects.filter(lista_id = lista_i.id, producto_id__isnull = False)
    for ele in current_list:
      descripcion[ele.producto.product_ref] = ele.producto.nombre
      precio[ele.producto.product_ref] = float(ele.producto.precio)
      active[ele.producto.product_ref] = 1
      if ele.producto.product_ref in orden:
        orden[ele.producto.product_ref] += ele.cantidad
      else:
        orden[ele.producto.product_ref] = ele.cantidad
    pedido['cliente'] = cliente_values
    pedido['orden'] = orden
    #we can send the price of the elements right now... not sure if is right
    pedido['precio'] = precio
    pedido['descripcion'] = descripcion
    pedido['active'] = active
    print "Add logic to send order here"
    for c_ele in current_custom_list:
     c_nombre[c_ele.id]= c_ele.nombre
      c_cantidad[c_ele.id]= c_ele.cantidad
      c_lista[c_ele.id]= c_ele.lista.id
      c_stock_optimo[c_ele.id]= c_ele.stock_optimo
    c_pedido['c_nombre'], c_pedido['c_cantitdad'], c_pedido['c_lista'], c_pedido['c_stock_optimo'] = c_nombre, c_cantidad, c_lista, c_stock_optimo

    send_order(pedido,proveedor,c_pedido)
  print "Done"

print "Current time " + time.strftime("%X")


#lets put in different status the pedidos
print "Current time " + time.strftime("%X")
print "set random status"
for t in Pedidos.objects.all():
  t.pedidostate = str(Pedidos.STATE_CHOICES[random.randrange(0,len(Pedidos.STATE_CHOICES))][0])
  t.save()

print "Current time " + time.strftime("%X")




