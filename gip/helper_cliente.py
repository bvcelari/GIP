from gip.models import Pedidos
from django.conf import settings

import ast

def list_grouper(query_pedidos):
  #TODO: add this tab definition to a Model or to settings
  def_tabs = settings.DEF_TABS
  #TODO: add this transitions to a Model or to settings 
  grouped_by = settings.GROUPED_BY
  ##this is the generated transitions tabs shortcut list
  working_scheme = {}
  for i in def_tabs:
    for k in grouped_by[def_tabs[i]]:
      working_scheme[str(k)] = i

  #bufff... if you have to modify this... you are allowed to do it from scratch
  sorted_pedidos = {}
  for t in grouped_by:
     #this is shit, cause dict.keys() do not work as expected with default dict
     sorted_pedidos[t] = []
  
  for t in query_pedidos:
    #sorted_pedidos[def_tabs[working_scheme[t['pedidostate']]]] = counted_tabs.get(def_tabs[working_scheme[t['pedidostate']]],0) + 1
    #TODO; if there is something unexpeted, like pediido_state = 101, will crash, FYI
    sorted_pedidos[def_tabs[working_scheme[t.pedidostate]]].append(t)
  #this is "slow", but.. will automate the way the tabs are counted and provided :)
  return sorted_pedidos, def_tabs


def generator_pedido_content(pedido):
  html = ''
  estado = [t[1] for t in pedido.STATE_CHOICES if t[0] == int(pedido.pedidostate)]
  print estado
  print pedido.pedidostate
  #TODO: do not use magic numbers
  #pedidos tha should show reformular actions
  acciones = build_botones_cliente(pedido,'modal')
  if int(pedido.pedidostate) in [10000,12200,12300]:
    html +=' <div class="modal" id="modaldemostrarpedido"> \
              <div class="modal-dialog modal-lg"> \
                  <div class="modal-content"> \
                      <div class="modal-header modal-header-info"> \
                          <button type="button" class="close" data-dismiss="modal" aria-hidden="true">X</button> \
                          <h4 class="modal-title">Pedido: {0} de {1}</h4> \
                      </div>\
                      <div class="modal-body">\
                       <table class="table">\
                    <thead>\
                      <tr>\
                        <th>Referencia</th>\
                        <th>Producto</th>\
                        <th>Cantidad</th>\
                        <th>Precio</th>\
                        <th>Reformular</th> \
                      </tr>\
                    </thead>\
                    <tbody>\
                     '.format(pedido.codigo, pedido.cliente.all()[0])
    print "WE HAVE PEDIOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
    print pedido.producto_serializado
    products = ast.literal_eval(pedido.producto_serializado)
    #pedido has 3 index, descripcion, orden, precio, cliente
    descripcion = 'descripcion'
    orden = 'orden' #contiene la cantidad que se ha pedido
    precio = 'precio' # precio al que se pidio
    active = 'active'
    for ele in products[descripcion]:
      strike = ''
      if products[active][ele] == 0:
        strike = '<strike>'
      html += '<tr data-toggle="collapse" data-target="#{0}_{1}" class="accordion-toggle"> \
               <td>{5}{1}</td> \
               <td>{5}{2}</td> \
               <td>{5}{3}</td> \
               <td>{5}{4}</td> \
                <td><a  href="#formularioreformular" class="btn btn-warning btn-sm" >Reformular Item</a></td>  \
      '.format(pedido.codigo, ele,products[descripcion][ele], products[orden][ele], products[precio][ele],strike)
      html += '<tr> \
                    <td colspan="12" class="hiddenRow"> \
                      <div class="accordian-body collapse" id="{0}_{1}"> \
                            <b>Sustituir por:</b> \
                      <div class="form-group form-inline"> \
                          <label class="sr-only" for="Referencia">Referencia</label> \
                          <input class="form-control" placeholder="Referencia"> \
                      </div> \
                      <div class="form-group">\
                        <label class="sr-only" for="Cantidad">cantidad</label> \
                        <input  class="form-control"  placeholder="Cantidad"> \
                      </div> \
                         <b> <p>Cuando pulse Guardar modificaciones los datos del pedido se modificarn</p> </b> \
                         <p>Compruebe que la referencia de su producto es la adecuada y no pertenece a otro producto.</p> \
                      </div> </td> \
                </tr>'.format(pedido.codigo, ele)
#    for t in Pedidos.get_available_pedidostate_transitions(pedido):
#      for i in Pedidos.STATE_CHOICES:
#        if t.target in i:
#          if t.target == 12300:
#            botones += '<button type="button" class="btn btn-success" data-dismiss="modal">Validar</button>'
#            botones += '<button type="button" class="btn btn-success" data-dismiss="modal">Validar</button>'
#          elif t.target == 12200:
#            acciones += '<button type="button" class="btn btn-success" data-dismiss="modal">Validar</button>'

    
    html += '</tbody> \
                  </table>\
                  </form>\
                      </div>\
                      <div class="modal-footer">\
                      <center>TOTAL: {0} </center> \
                          {1}\
                      </div>\
                  </div>\
              </div>\
          </div>'.format(pedido.total,acciones)
  else:
    html +=' <div class="modal" id="modaldemostrarpedido"> \
              <div class="modal-dialog modal-lg"> \
                  <div class="modal-content"> \
                      <div class="modal-header modal-header-info"> \
                          <button type="button" class="close" data-dismiss="modal" aria-hidden="true">X</button> \
                          <h4 class="modal-title">Pedido: {0} de {1}</h4> \
                      </div>\
                      <div class="modal-body">\
                       <table class="table">\
                    <thead>\
                      <tr>\
                        <th>Referencia</th>\
                        <th>Producto</th>\
                        <th>Cantidad</th>\
                        <th>Precio</th>\
                      </tr>\
                    </thead>\
                    <tbody>\
                     '.format(pedido.codigo, pedido.cliente.all()[0])
    products = ast.literal_eval(pedido.producto_serializado)
    #pedido has 3 index, descripcion, orden, precio, cliente
    descripcion = 'descripcion'
    orden = 'orden' #contiene la cantidad que se ha pedido
    precio = 'precio' # precio al que se pidio
    active = 'active'
    for ele in products[descripcion]:
      strike = ''
      if products[active][ele] == 0:
        strike = '<strike>'
      html += '<tr data-toggle="collapse" data-target="#{0}_{1}" class="accordion-toggle"> \
               <td>{5}{1}</td> \
               <td>{5}{2}</td> \
               <td>{5}{3}</td> \
               <td>{5}{4}</td> \
      '.format(pedido.codigo, ele,products[descripcion][ele], products[orden][ele], products[precio][ele],strike)
    html += '</tbody> \
                  </table>\
                  </form>\
                      </div>\
                      <div class="modal-footer">\
                      <center>TOTAL: {0} </center> \
                      </div>\
                  </div>\
              </div>\
          </div>'.format(pedido.total)

  return html



def build_botones_cliente(pedido,source):
  pedido.pedidostate = int(pedido.pedidostate)
  acciones_tab = ''
  acciones_modal = ''
  for t in Pedidos.get_available_pedidostate_transitions(pedido):
    print "we are looking into "+str(pedido.codigo)+"with the id"+str(pedido.id)
    print "for current pedidostate:" +str(pedido.pedidostate)+ " transistion: "+str(t.name)+" is available"
    for i in Pedidos.STATE_CHOICES:
      #TODO: exclide the states that do not want to be seen be the proveedor using my_states
      if t.target in i:
        print "we have a target:"+str(t.target)+", and we identifi as  "+str(i)
        if t.target == 12200:
          acciones_tab += '<a href="#" onclick="show_pedido(\'{0}\')" class="btn btn-info btn-sm" data-toggle="modal">{1}</a> '.format(pedido.id,pedido.proveedor_id,i[1])
          acciones_modal +=  '<button type="submit" class="btn btn-warning btn-sm" onclick="submit_changes(\'{0}\',\'{1}\',\'{2}\')"> 1 Reformular </button>'.format(pedido.codigo,pedido.proveedor_id,t.name)
        elif t.target == 12300:
          acciones_tab += '<a href="#" onclick="show_pedido(\'{0}\')" class="btn btn-info btn-sm" data-toggle="modal">{1}</a> '.format(pedido.id,pedido.proveedor_id,i[1])
          acciones_modal +=  '<button type="submit" class="btn btn-warning btn-sm" onclick="send(\'{0}\',\'{1}\',\'{2}\')"> 2 Aceptar Pedido</button>'.format(pedido.codigo,pedido.proveedor_id,t.name)
        else:
          #acciones_tab += '<a href="#" onclick="send(\'{0}\',\'{1}\')" class="btn btn-info btn-sm" data-toggle="modal">{2}</a> '.format(pedido.id,t.name, i[1])
          #acciones_modal  += ' <button type="button" class="btn btn-warning" data-dismiss="modal" onclick="send(\'{0}\',\'{1}\')"> {2}</button> '.format(pedido.id,t.name, i[1])
          pass
  print "and we have acciones"
  #we will return accions modal or tab, depend on the source function is request from
  if source == 'tab':
    return acciones_tab
  else:
    return acciones_modal




def generate_modales_encurso(pedido):
  html = ''
  estado = [t[1] for t in pedido.STATE_CHOICES if t[0] == int(pedido.pedidostate)]
  print estado
  print pedido.pedidostate
  #TODO: do not use magic numbers
  #pedidos tha should show reformular actions
  acciones = build_botones_cliente(pedido,'modal')
  if int(pedido.pedidostate) in [100,10000,12100]:
    reformular = True
    if pedido.pedidostate in [100,10000]:
      reformular = False     
    html +=' <div class="modal" id="modaldemostrarpedido_{0}"> \
              <div class="modal-dialog modal-lg"> \
                  <div class="modal-content"> \
                      <div class="modal-header modal-header-info"> \
                          <button type="button" class="close" data-dismiss="modal" aria-hidden="true">X</button> \
                          <h4 class="modal-title">Pedido: {0} de {1}</h4> \
                      </div>\
                      <div class="modal-body">\
                       <table class="table">\
                    <thead>\
                      <tr>\
                        <th>Referencia</th>\
                        <th>Producto</th>\
                        <th>Cantidad</th>\
                        <th>Precio</th>'.format(pedido.codigo, pedido.cliente.all()[0])
    if reformular: 
      html+='             <th>Reformular</th>  '
    html+='            </tr>\
                    </thead>\
                    <tbody>'
    print "WE HAVE PEDIOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
    print pedido.producto_serializado
    products = ast.literal_eval(pedido.producto_serializado)
    #pedido has 3 index, descripcion, orden, precio, cliente
    descripcion = 'descripcion'
    orden = 'orden' #contiene la cantidad que se ha pedido
    precio = 'precio' # precio al que se pidio
    active = 'active'
    for ele in products[descripcion]:
      strike = ''
      if products[active][ele] == 0:
        strike = '<strike>'
      html += '<tr data-toggle="collapse" data-target="#{0}_{1}" class="accordion-toggle"> \
               <td>{5}{1}</td> \
               <td>{5}{2}</td> \
               <td>{5}{3}</td> \
               <td>{5}{4}</td>'.format(pedido.codigo, ele,products[descripcion][ele].encode("utf-8"), products[orden][ele], products[precio][ele],strike)
      if reformular:
        html += '<td><a  href="#formularioreformular" class="btn btn-warning btn-sm" >Reformular Item</a></td>'
        html += '<tr> \
                      <td colspan="12" class="hiddenRow"> \
                        <div class="accordian-body collapse" id="{0}_{1}"> \
                              <b>Sustituir por:</b> \
                        <div class="form-group form-inline"> \
                            <label class="sr-only" for="Referencia">Referencia</label> \
                            <input class="form-control" placeholder="Referencia"> \
                        </div> \
                        <div class="form-group">\
                          <label class="sr-only" for="Cantidad">cantidad</label> \
                          <input  class="form-control"  placeholder="Cantidad"> \
                        </div> \
                           <b> <p>Cuando pulse Guardar modificaciones los datos del pedido se modificarn</p> </b> \
                           <p>Compruebe que la referencia de su producto es la adecuada y no pertenece a otro producto.</p> \
                        </div> </td> \
                  </tr>'.format(pedido.codigo, ele)
#    for t in Pedidos.get_available_pedidostate_transitions(pedido):
#      for i in Pedidos.STATE_CHOICES:
#        if t.target in i:
#          if t.target == 12300:
#            botones += '<button type="button" class="btn btn-success" data-dismiss="modal">Validar</button>'
#            botones += '<button type="button" class="btn btn-success" data-dismiss="modal">Validar</button>'
#          elif t.target == 12200:
#            acciones += '<button type="button" class="btn btn-success" data-dismiss="modal">Validar</button>'


    html += '</tbody> \
                  </table>\
                  </form>\
                      </div>\
                      <div class="modal-footer">\
                      <center>TOTAL: {0} </center> \
                          {1}\
                      </div>\
                  </div>\
              </div>\
          </div>'.format(pedido.total,acciones)
  else:
    html +=' <div class="modal" id="modaldemostrarpedido"> \
              <div class="modal-dialog modal-lg"> \
                  <div class="modal-content"> \
                      <div class="modal-header modal-header-info"> \
                          <button type="button" class="close" data-dismiss="modal" aria-hidden="true">X</button> \
                          <h4 class="modal-title">Pedido: {0} de {1}</h4> \
                      </div>\
                      <div class="modal-body">\
                       <table class="table">\
                    <thead>\
                      <tr>\
                        <th>Referencia</th>\
                        <th>Producto</th>\
                        <th>Cantidad</th>\
                        <th>Precio</th>\
                      </tr>\
                    </thead>\
                    <tbody>\
                     '.format(pedido.codigo, pedido.cliente.all()[0])
    products = ast.literal_eval(pedido.producto_serializado)
    #pedido has 3 index, descripcion, orden, precio, cliente
    descripcion = 'descripcion'
    orden = 'orden' #contiene la cantidad que se ha pedido
    precio = 'precio' # precio al que se pidio
    active = 'active'
    for ele in products[descripcion]:
      strike = ''
      if products[active][ele] == 0:
        strike = '<strike>'
      html += '<tr data-toggle="collapse" data-target="#{0}_{1}" class="accordion-toggle"> \
               <td>{5}{1}</td> \
               <td>{5}{2}</td> \
               <td>{5}{3}</td> \
               <td>{5}{4}</td> \
      '.format(pedido.codigo, ele,products[descripcion][ele].encode("utf-8"), products[orden][ele], products[precio][ele],strike)
    html += '</tbody> \
                  </table>\
                  </form>\
                      </div>\
                      <div class="modal-footer">\
                      <center>TOTAL: {0} </center> \
                      </div>\
                  </div>\
              </div>\
          </div>'.format(pedido.total)

  return html

