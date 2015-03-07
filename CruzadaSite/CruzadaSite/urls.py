from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CruzadaSite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'Cruzada.views.login_user'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'Cruzada.views.login_user', name='login'),
    url(r'^home/$', 'Cruzada.views.home', name='home'),
    url(r'^pedido_detalle/$', 'Cruzada.views.pedido_detalle', name='pedido_detalle'),
    url(r'^nueva_venta/$', 'Cruzada.views.venta', name='venta'),
    url(r'^ventas/$', 'Cruzada.views.ventas', name='ventas'),
    url(r'^lista_articulos/$', 'Cruzada.views.articulos', name='lista_articulos'),
    url(r'^lista_pedidos/$', 'Cruzada.views.pedidos', name='lista_pedidos'),

    ### AJAX URLs ###
    url(r'^venta_articulos_ajax/$', 'Cruzada.views.get_articulos_venta', name='venta_articulos_ajax'),
    url(r'^generar_transaccion_ajax/$', 'Cruzada.views.generar_transaccion', name='generar_transaccion_ajax'),
    url(r'^nuevo_cliente_ajax/$', 'Cruzada.views.nuevo_cliente_ajax', name='nuevo_cliente_ajax'),
    url(r'^venta_clientes_ajax/$', 'Cruzada.views.get_clientes_venta', name='venta_clientes_ajax'),
    url(r'^venta_fp_ajax/$', 'Cruzada.views.get_forma_pago_venta', name='venta_fp_ajax'),
    url(r'^venta_update_ren_ajax/$', 'Cruzada.views.updateRen_ajax', name='updateRen_ajax'),
    url(r'^venta_add_ren_ajax/$', 'Cruzada.views.addRen_ajax', name='addRen_ajax'),
    url(r'^venta_del_ren_ajax/$', 'Cruzada.views.deleteRen_ajax', name='delRen_ajax'),
)
