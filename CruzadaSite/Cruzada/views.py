#coding: utf8
import json
from django.http import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.core.urlresolvers import reverse
from Cruzada.models import *
from django.core.serializers.json import DjangoJSONEncoder
import stock_dal
import general_dal


# Create your views here.
def login_user(request):
    django_logout(request)
    if request.method == 'POST':
        if request.is_ajax:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                django_login(request, user)
                response_data = {}
                request.session["persona"] = Personas.objects.get_logged_persona(user.id) #"persona"
                if request.REQUEST.get('next'):
                    response_data['redirect'] = request.REQUEST.get('next')
                else:
                    response_data['redirect'] = reverse(home)
                return HttpResponse(json.dumps(response_data), content_type="application/json")
        return HttpResponseForbidden()  # catch invalid ajax and all non ajax
    return render(request, 'login.html')


@login_required(login_url='/login/')
def home(request):

    context = {
        'home': True
    }

    return render(request, 'home.html', context)


@login_required(login_url='/login/')
def articulos(request):

    result, lista_articulos, message = stock_dal.get_stock_sucursal(request.session["persona"]["uri_stock"])

    context = {
        'articulos': True,
        'b_lista_articulos': True,
        'message_title': 'Sistema Cruzada',
        'message_body': 'La app arrancó a seguir trabajando',
        'lista_articulos': lista_articulos
    }
    return render(request, 'articulos.html', context)


@login_required(login_url='/login/')
def pedido_detalle(request):
    return render(request, 'pedido_detalle.html')


@login_required(login_url='/login/')
@ensure_csrf_cookie
def venta(request):
    context = {
        'ventas': True,
        'nueva_venta': True,
        'transaccion_id': 0,
        'sub_total': 0,
        'cliente_id': 'null',
        'cliente_json': 'null',
        'forma_pago_id': 'null',
        'forma_pago_json': 'null'
    }
    return render(request, 'venta.html', context)


@login_required(login_url='/login/')
@ensure_csrf_cookie
def venta_editar(request, transaccion_id):
    read_only_path = reverse('venta_ver', kwargs={'transaccion_id': transaccion_id})
    if request.path == read_only_path:
        read_only = True
    else:
        read_only = False

    result, transaccion, message = general_dal.get_venta(transaccion_id, request.session["persona"]["sucursal_id"])
    if transaccion.__len__() > 0:
        transaccion = transaccion[0]

    result, renglones, message = general_dal.get_renglones(transaccion_id)
    sub_total = 0
    for renglon in renglones:
        sub_total += renglon["precio_unitario"] * renglon["cantidad"]

    result, cliente, message = general_dal.get_cliente(transaccion["cliente_id"])

    if cliente.__len__() > 0:
        cliente_id = cliente[0]["id"]
        if read_only:
            cliente_json = cliente[0]
        else:
            cliente_json = json.dumps(cliente[0], cls=DjangoJSONEncoder)
    else:
        cliente_id = "null"
        cliente_json = "null"

    result, forma_pago, message = general_dal.get_forma_pago(transaccion["forma_pago_id"])

    if forma_pago.__len__() > 0:
        forma_pago_id = forma_pago[0]["id"]
        if read_only:
            forma_pago_json = forma_pago[0]
        else:
            forma_pago_json = json.dumps(forma_pago[0], cls=DjangoJSONEncoder)
    else:
        forma_pago_id = "null"
        forma_pago_json = "null"

    context = {
        'ventas': True,
        'nueva_venta': True,
        'read_only': read_only,
        'transaccion': transaccion,
        'transaccion_id': transaccion_id,
        'renglones': renglones,
        'sub_total': sub_total,
        'cliente_id': cliente_id,
        'cliente_json': cliente_json,
        'forma_pago_id': forma_pago_id,
        'forma_pago_json': forma_pago_json
    }

    if read_only:
        recargo = forma_pago_json["recargo"]
        total_venta = sub_total + sub_total * recargo
        recargo = sub_total * recargo
        context["recargo"] = recargo
        context["ind_recargo"] = forma_pago_json["recargo"] * 100
        context["total_venta"] = total_venta

    return render(request, 'venta.html', context)


@login_required(login_url='/login/')
def ventas(request):
    result, lista_ventas, message = general_dal.get_lista_ventas(request.session["persona"]["uri_stock"])
    context = {
        'ventas': True,
        'b_lista_ventas': True,
        'lista_ventas': lista_ventas
    }
    return render(request, 'ventas.html', context)


@login_required(login_url='/login/')
def pedidos(request):
    lista_articulos = Articulos.objects.all()
    context = {
        'pedidos': True,
        'b_lista_pedidos': True,
        'lista_pedidos': lista_articulos
    }
    return render(request, 'pedidos.html', context)


""" AJAX VIEWS  """


def get_articulos_venta(request):
    if request.method == 'GET':
        if request.is_ajax:
            if 'keyword' in request.GET:
                keyword = request.GET["keyword"]
                result, articulos, message = stock_dal.get_stock_ajax(request.session["persona"]["uri_stock"], keyword)
                response = json.dumps({"articulos": articulos}, cls=DjangoJSONEncoder)
                return HttpResponse(response, content_type="application/json")
    return HttpResponseForbidden()


def get_clientes_venta(request):
    if request.method == 'GET':
        if request.is_ajax:
            if 'keyword' in request.GET:
                keyword = request.GET["keyword"]
                result, clientes, message = general_dal.get_cliente_ajax(keyword)
                response = json.dumps({"clientes": clientes}, cls=DjangoJSONEncoder)
                return HttpResponse(response, content_type="application/json")
    return HttpResponseForbidden()


def get_forma_pago_venta(request):
    if request.method == 'GET':
        if request.is_ajax:
            if 'keyword' in request.GET:
                keyword = request.GET["keyword"]
                result, formasPago, message = general_dal.get_forma_pago_ajax(keyword)
                response = json.dumps({"formasPago": formasPago}, cls=DjangoJSONEncoder)
                return HttpResponse(response, content_type="application/json")
    return HttpResponseForbidden()


def guardar_transaccion(request):
    # expect at least 1 article
    if request.method == 'POST':
        if request.is_ajax:
            # datos de transacción
            transaccion_id = request.POST["transaccion_id"]
            cliente_id = request.POST["cliente_id"]
            vendedor_id = request.POST["vendedor_id"]
            forma_pago_id = request.POST["forma_pago_id"]
            promocion_id = request.POST["promocion_id"]

            if transaccion_id == '0':
                transaccion_id = general_dal.nueva_transaccion(cliente_id, vendedor_id, forma_pago_id,
                                                               promocion_id, request.session["persona"]["sucursal_id"])
            else:
                general_dal.update_transaccion(request.session["persona"]["sucursal_id"], transaccion_id, cliente_id,
                                               vendedor_id, forma_pago_id, promocion_id)

            if transaccion_id is not None:
                # datos de renglón si los hay
                # if "articulo_id" in request.POST:
                #     articulo_id = request.POST["articulo_id"]
                #     result = stock_dal.update_stock(request.session["persona"]["uri_stock"], -1, articulo_id)
                #
                #     if result:
                #         # insert ren
                #         articulo = stock_dal.get_articulo(articulo_id)
                #         general_dal.nuevo_renglon(articulo_id, 1, articulo["precio"], transaccion_id)
                #
                return HttpResponse(json.dumps({"transaccion_id": transaccion_id}), content_type="application/json")

            return HttpResponseServerError()
    return HttpResponseForbidden()


def cancelar_transaccion(request):
    # expect at least 1 article
    if request.method == 'POST':
        if request.is_ajax:
            # datos de transacción
            transaccion_id = request.POST["transaccion_id"]

            if transaccion_id != '0':
                result, renglones, message = general_dal.get_renglones(transaccion_id)

                for renglon in renglones:
                    stock_dal.update_stock(request.session["persona"]["uri_stock"], renglon["cantidad"], renglon["articulo_id"])

                result = general_dal.cancel_transaccion(transaccion_id)

                return HttpResponse(json.dumps({"result": result}), content_type="application/json")

            return HttpResponseServerError()
    return HttpResponseForbidden()


def nuevo_cliente_ajax(request):
    if request.method == 'POST':
        if request.is_ajax:
            # datos del cliente
            nombre = request.POST["nombre"] if "nombre" in request.POST else ""
            apellido = request.POST["apellido"] if "nombre" in request.POST else ""
            email = request.POST["email"] if "nombre" in request.POST else ""
            direccion = request.POST["direccion"] if "nombre" in request.POST else ""
            dni = request.POST["dni"] if "nombre" in request.POST else 0
            cuil = request.POST["cuil"] if "nombre" in request.POST else ""

            id = general_dal.nuevo_cliente(nombre,apellido,email,direccion,dni,cuil)

            if id is not None:
                return HttpResponse(json.dumps({"result": True, "cliente_id": id}), content_type="application/json")
            return HttpResponseServerError()

    return HttpResponseForbidden()


def addRen_ajax(request):
    if request.method == 'POST':
        if request.is_ajax:

            if "transaccion_id" in request.POST:

                transaccion_id = request.POST["transaccion_id"]

                if "articulo_id" in request.POST:

                    articulo_id = request.POST["articulo_id"]
                    result = stock_dal.update_stock(request.session["persona"]["uri_stock"], -1, articulo_id)

                    if result:
                        # insert ren
                        articulo = stock_dal.get_articulo(articulo_id)
                        general_dal.nuevo_renglon(articulo_id, 1, articulo["precio"], transaccion_id)

                return HttpResponse(json.dumps({"transaccion_id": transaccion_id}), content_type="application/json")

            return HttpResponseServerError()
    return HttpResponseForbidden()


def updateRen_ajax(request):
    if request.method == 'POST':
        if request.is_ajax:

            transaccion_id = request.POST["transaccion_id"]

            if transaccion_id is not None:
                # datos de renglón si los hay
                if "articulo_id" in request.POST:
                    articulo_id = request.POST["articulo_id"]
                    result = True
                    result = stock_dal.update_stock(request.session["persona"]["uri_stock"], -1, articulo_id)

                    if result:
                        # update ren
                        result = general_dal.update_renglon(articulo_id, transaccion_id)

                        return HttpResponse(json.dumps({"result": result}), content_type="application/json")

            return HttpResponseServerError()

    return HttpResponseForbidden()


def deleteRen_ajax(request):
    if request.method == 'POST':
        if request.is_ajax:

            transaccion_id = request.POST["transaccion_id"]

            if transaccion_id is not None:
                # datos de renglón si los hay
                if "articulo_id" in request.POST:
                    articulo_id = request.POST["articulo_id"]
                    cantidad = request.POST["cantidad"]

                    result = True
                    result = stock_dal.update_stock(request.session["persona"]["uri_stock"], cantidad, articulo_id)

                    if result:
                        # delete ren
                        result = general_dal.delete_renglon(articulo_id, transaccion_id)

                        return HttpResponse(json.dumps({"result": result}), content_type="application/json")

            return HttpResponseServerError()

    return HttpResponseForbidden()


def check_fin_transaccion_ajax(request):
    if request.method == 'GET':
        if request.is_ajax:
            transaccion_id = request.GET["transaccion_id"]
            if transaccion_id is not None:
                result, transaccion, message = general_dal.get_venta(transaccion_id, request.session["persona"]["sucursal_id"])

                if transaccion.__len__() > 0:
                    transaccion = transaccion[0]

                result, renglones, message = general_dal.count_renglones(transaccion_id)

                if transaccion["cliente_id"] is not None \
                    and transaccion["forma_pago_id"] is not None \
                    and renglones[0]["cant"] > 0:
                    result = True
                else:
                    result = False

                return HttpResponse(json.dumps({"result": result}), content_type="application/json")
    return HttpResponseForbidden()


def finalizar_transaccion_ajax(request):
    if request.method == 'POST':
        if request.is_ajax:

            transaccion_id = request.POST["transaccion_id"]

            if transaccion_id is not None:
                result = general_dal.finalizar_venta(transaccion_id, request.session["persona"]["sucursal_id"])
                return HttpResponse(json.dumps({"result": result}), content_type="application/json")

            return HttpResponseServerError()

    return HttpResponseForbidden()


def check_articulo_online_ajax(request):
    if request.method == 'GET':
        if request.is_ajax:
            articulo_id = request.GET["articulo_id"]
            result = stock_dal.check_articulo_online(articulo_id, request.session["persona"]["uri_stock"])
            return HttpResponse(json.dumps({"almacenes": result}), content_type="application/json")

#            return HttpResponseServerError()

    return HttpResponseForbidden()


def pedir_articulo_ajax(request):
    if request.method == 'POST':
        if request.is_ajax:

            articulo = request.POST["id"]
            sucursal_destino = request.POST["sucursal_destino"]


            id = general_dal.upsert_pedido(request.session["persona"]["sucursal_id"], sucursal_destino, 1)

            # insertar el renglón del pedido
            result = general_dal.upsert_renglon_pedido(id, articulo)
            result = True
            return HttpResponse(json.dumps({"result": result}), content_type="application/json")

            #return HttpResponseServerError()

    return HttpResponseForbidden()