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
    url(r'^venta/$', 'Cruzada.views.venta', name='venta'),
    url(r'^lista_articulos/$', 'Cruzada.views.articulos', name='lista_articulos'),
)
