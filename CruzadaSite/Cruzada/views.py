#coding: utf8
import json
from django.http import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.core.urlresolvers import reverse
from Cruzada.models import *


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
                persona = Personas.objects.filter(user=user.id).values('nombre', 'apellido', 'sucursal', 'rol')[0]
                request.session["persona"] = persona #"persona"
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
    lista_articulos = Articulos.objects.all()

    for articulo in lista_articulos:
        pass


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
