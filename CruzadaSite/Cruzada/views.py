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
        'nueva_venta': True
    }
    return render(request, 'venta.html', context)


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


def generar_transaccion(request):
    # expect at least 1 article
    if request.method == 'POST':
        if request.is_ajax:
            # datos de transacción
            cliente_id = request.POST["cliente_id"]
            vendedor_id = request.POST["vendedor_id"]
            forma_pago_id = request.POST["forma_pago_id"]
            promocion_id = request.POST["promocion_id"]

            transaccion_id = general_dal.nueva_transaccion(cliente_id, vendedor_id, forma_pago_id, promocion_id)

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
                return HttpResponse(json.dumps({"result": True}), content_type="application/json")
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
                    #result = stock_dal.update_stock(request.session["persona"]["uri_stock"], -1, articulo_id)

                    if result:
                        # update ren
                        result = general_dal.update_renglon(articulo_id, transaccion_id)

                        return HttpResponse(json.dumps({"result": result}), content_type="application/json")

            return HttpResponseServerError()

    return HttpResponseForbidden()


def removeRen_ajax(request):
    pass