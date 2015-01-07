#coding: utf8
from django.db import models


# Create your models here.
class Categoria(models.Model):

    class Meta:
        db_table = 'Categoria'

    descripcion = models.CharField(max_length=100)

    def __unicode__(self):
        return self.descripcion

class PedidosEstados(models.Model):

    class Meta:
        db_table = 'PedidosEstados'

    descripcion = models.CharField(max_length=100)

    def __unicode__(self):
        return self.descripcion

class TipoMedioPago(models.Model):

    class Meta:
        db_table = 'TipoMedioPago'

    nombre = models.CharField(max_length=50)

    def __unicode__(self):
        return self.nombre


class Rol(models.Model):

    class Meta:
        db_table = 'Rol'

    descripcion = models.CharField(max_length=100)

    def __unicode__(self):
        return self.descripcion


class Sucursal(models.Model):

    class Meta:
        db_table = 'Sucursal'

    descripcion = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    nro_interno = models.IntegerField(max_length=10)


class Personas(models.Model):

    class Meta:
        db_table = 'Personas'

    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.CharField(max_length=255, null=True)
    direccion = models.CharField(max_length=255, null=True)
    dni = models.IntegerField()
    cuil = models.CharField(max_length=13)
    categoria = models.ForeignKey(Categoria)
    sucursal = models.ForeignKey(Sucursal)
    rol = models.ForeignKey(Rol)


class MediosDePago(models.Model):

    class Meta:
        db_table = 'MediosDePago'

    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    recargo = models.DecimalField(decimal_places=2, max_digits=3)
    tipo_medio = models.ForeignKey(TipoMedioPago)


class Promociones(models.Model):

    class Meta:
        db_table = 'Promociones'

    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    vigencia_desde = models.DateTimeField()
    vigencia_hasta = models.DateField()
    descuento = models.DecimalField(max_digits=2,decimal_places=2)


class ServicioAlmacen(models.Model):

    class Meta:
        db_table = 'ServicioAlmacen'

    descripcion = models.CharField(max_length=100)

    def __unicode__(self):
        return self.descripcion


class Almacenes(models.Model):

    class Meta:
        db_table = 'Almacenes'

    sucursal = models.OneToOneField(Sucursal, primary_key=True)
    servicio = models.ForeignKey(ServicioAlmacen)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_baja = models.DateTimeField()
    uri_stock = models.CharField(max_length=255)


class Talle(models.Model):

    class Meta:
        db_table = 'Talle'

    descripcion = models.CharField(max_length=100)

    def __unicode__(self):
        return self.descripcion

class Colores(models.Model):

    class Meta:
        db_table = 'Colores'

    descripcion = models.CharField(max_length=100)

    def __unicode__(self):
        return self.descripcion


class Articulos(models.Model):

    class Meta:
        db_table = 'Articulos'

    descripcion = models.CharField(max_length=100)
    codigo = models.CharField(max_length=45)
    talle = models.ForeignKey(Talle)
    color = models.ForeignKey(Colores)
    precio = models.DecimalField(max_digits=10, decimal_places=2)


class Pedidos(models.Model):

    class Meta:
        db_table = 'Pedidos'

    nro_pedido = models.CharField(max_length=45, unique=True)
    suc_origen = models.ForeignKey(Sucursal, related_name='suc_origen')
    suc_destino = models.ForeignKey(Sucursal, related_name='suc_destino')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    fecha_proceso = models.DateTimeField()
    fecha_entrega = models.DateTimeField()
    fecha_recepcion = models.DateTimeField()
    observaciones = models.TextField()
    estado = models.ForeignKey(PedidosEstados)
    uri_detalle = models.CharField(max_length=255)


class Transacciones(models.Model):

    class Meta:
        db_table = 'Transacciones'

    # numero = models.AutoField(unique=True)
    fecha = models.DateTimeField(auto_now_add=True)
    vendedor = models.ForeignKey(Personas, related_name='vendedor')
    forma_pago = models.ForeignKey(MediosDePago)
    cliente = models.ForeignKey(Personas, related_name='cliente')
    promocion = models.ForeignKey(Promociones)
    tipo = models.CharField(max_length=45)


class TransaccionesRen(models.Model):

    class Meta:
        db_table = 'TransaccionesRen'

    articulo = models.ForeignKey(Articulos)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    accion = models.CharField(max_length=45)
    cabecera = models.ForeignKey(Transacciones)



#Categoria Listo
#Personas Listo
#Sucursal Listo
#PedidosEstados Listo
#MediosdePago Listo
#TipoMedioPago Listo
#Rol Listo
#Pedidos Listo
#Almacenes Listo
#ServicioAlmacen Listo
#Transacciones Listo
#TransaccionRen Listo
#Promociones Listo
#Talle Listo
#Artículos Listo
#Colores Listo