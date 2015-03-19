__author__ = 'emanuel'
import MySQLdb

config = {"host": "192.168.203.129",
         "user": "root",
         "passwd": "123456",
         "db": "cruzada",
         "charset": "utf8"}


def nueva_transaccion(cliente_id, vendedor_id, forma_pago_id, promocion_id, sucursal_id):

    # TODO: agregar la sucursal que realiza la transaccion

    cliente_id = 'null' if cliente_id == '' else cliente_id
    vendedor_id = 'null' if vendedor_id == '' else vendedor_id
    forma_pago_id = 'null' if forma_pago_id == '' else forma_pago_id
    promocion_id = 'null' if promocion_id == '' else promocion_id

    query = "INSERT INTO Transacciones (fecha,vendedor_id,forma_pago_id,cliente_id,promocion_id,tipo, sucursal_id) " \
            "VALUES (now(),{vendedor_id}, {forma_pago_id}, {cliente_id}, {promocion_id}, 'VENTA', {sucursal_id})".format(
        vendedor_id=vendedor_id,
        forma_pago_id=forma_pago_id,
        cliente_id=cliente_id,
        promocion_id=promocion_id,
        sucursal_id=sucursal_id)

    return _insert_query(query)


def update_transaccion(sucursal_id, transaccion_id, cliente_id, vendedor_id, forma_pago_id, promocion_id):

    cliente_id = 'null' if cliente_id == '' else cliente_id
    vendedor_id = 'null' if vendedor_id == '' else vendedor_id
    forma_pago_id = 'null' if forma_pago_id == '' else forma_pago_id
    promocion_id = 'null' if promocion_id == '' else promocion_id

    query = "UPDATE Transacciones " \
            "SET forma_pago_id = {forma_pago}, " \
            "cliente_id = {cliente_id}, " \
            "promocion_id = {promocion_id}, " \
            "vendedor_id = {vendedor_id} " \
            "WHERE id = {transaccion_id} " \
            "AND sucursal_id = {sucursal_id}".format(sucursal_id=sucursal_id,
                                                     transaccion_id=transaccion_id,
                                                     forma_pago=forma_pago_id,
                                                     cliente_id=cliente_id,
                                                     promocion_id=promocion_id,
                                                     vendedor_id=vendedor_id)

    return _update_query(query)


def cancel_transaccion(transaccion_id):
    query = "UPDATE Transacciones SET estado = 'CANCELADA' " \
            "WHERE id = {transaccion_id}".format(transaccion_id=transaccion_id)

    return _update_query(query)


def nuevo_renglon(articulo_id, cantidad, precio_unitario, cabecera_id):
    query = "INSERT INTO TransaccionesRen (articulo_id, cantidad, precio_unitario, cabecera_id) " \
            "VALUES ({articulo_id}, {cantidad}, {precio_unitario}, {cabecera_id})".format(
        articulo_id=articulo_id,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        cabecera_id=cabecera_id)

    _insert_query(query)


def update_renglon(articulo_id, cabecera_id):
    query = "UPDATE TransaccionesRen SET cantidad = cantidad + 1 " \
            "WHERE cabecera_id = {cabecera_id} AND articulo_id = {articulo_id}".format(
        articulo_id=articulo_id,
        cabecera_id=cabecera_id)

    return _update_query(query)


def delete_renglon(articulo_id, cabecera_id):
    query = "DELETE FROM TransaccionesRen " \
            "WHERE cabecera_id = {cabecera_id} AND articulo_id = {articulo_id}".format(
        articulo_id=articulo_id,
        cabecera_id=cabecera_id)

    return _update_query(query)


def nuevo_cliente(nombre,apellido,email,direccion,dni,cuil):
    query = "INSERT INTO Personas (nombre,apellido,email,direccion,dni,cuil,categoria_id,sucursal_id,rol_id,user_id) " \
            "VALUES ('{nombre}','{apellido}','{email}','{direccion}',{dni},'{cuil}',1,null,null,null) " \
            "".format(nombre=nombre, apellido=apellido, email=email, direccion=direccion, dni=dni, cuil=cuil)

    return _insert_query(query)


def get_cliente_ajax(_keyword):
    # split keyword by spaces
    keywords = _keyword.split(" ")
    condition = "(nombre LIKE '%{keyword}%' " \
            "OR apellido LIKE '%{keyword}%' " \
            "OR CAST(dni AS CHAR) = '%{keyword}%')"
    conditions = []
    for kwd in keywords:
        conditions.append(condition.format(keyword=kwd))

    query = "SELECT id, nombre, apellido, dni, email, cuil, direccion, " \
            "CONCAT(nombre, ' ', apellido, ' ', dni, ' ', email) AS name " \
            "FROM Personas " \
            "WHERE categoria_id = 1 AND {conditions} ".format(conditions=" AND ".join([x for x in conditions]))

    return _exec_query(query)


def get_forma_pago_ajax(_keyword):

    query = "SELECT a.id, a.descripcion, a.recargo, b.nombre, CONCAT(a.descripcion, ' - ', b.nombre) AS name " \
            "FROM MediosDePago AS a " \
            "INNER JOIN TipoMedioPago b " \
            "ON a.tipo_medio_id = b.id " \
            "WHERE descripcion LIKE '%{keyword}%' ".format(keyword=_keyword)

    return _exec_query(query)


def get_lista_ventas(stock_sucursal):
    query = "SELECT t.id, t.fecha, IFNULL(mp.descripcion, '') AS forma_pago, " \
            "IFNULL(CONCAT(p.apellido, ', ', p.nombre),'') AS cliente, " \
            "t.estado, IFNULL(sum(tr.cantidad),0) as articulos " \
            "FROM Transacciones AS t " \
            "LEFT JOIN Personas p " \
            "ON t.cliente_id = p.id " \
            "LEFT JOIN MediosDePago mp " \
            "ON t.forma_pago_id = mp.id " \
            "LEFT JOIN TransaccionesRen tr " \
            "ON t.id = tr.cabecera_id " \
            "INNER JOIN Almacenes a " \
            "ON t.sucursal_id =  a.sucursal_id " \
            "AND a.uri_stock = '{stock_sucursal}' " \
            "GROUP BY 1,2,3,4,5 " \
            "ORDER BY t.id DESC".format(stock_sucursal=stock_sucursal)

    return _exec_query(query)


def get_venta(transaccion_id, sucursal_id):
    query = "SELECT * FROM Transacciones " \
            "WHERE id = {transaccion_id} AND sucursal_id = {sucursal_id} ".format(transaccion_id=transaccion_id,
                                                                                  sucursal_id=sucursal_id)

    return _exec_query(query)


def get_renglones(transaccion_id):
    query = "SELECT b.*, c.descripcion AS 'color', t.descripcion AS 'talle', " \
            "a.id as renglon_id, a.cantidad, a.precio_unitario, a.articulo_id " \
            "FROM TransaccionesRen AS a " \
            "INNER JOIN Articulos AS b " \
            "ON a.articulo_id = b.id " \
            "INNER JOIN Colores AS c " \
            "ON b.color_id = c.id " \
            "INNER JOIN Talle AS t " \
            "ON b.talle_id = t.id " \
            "WHERE a.cabecera_id = {transaccion_id}".format(transaccion_id=transaccion_id)

    return _exec_query(query)


def count_renglones(transaccion_id):
    query = "SELECT count(*) cant FROM TransaccionesRen " \
            "WHERE cabecera_id = {transaccion_id}".format(transaccion_id=transaccion_id)

    return _exec_query(query)


def get_cliente(cliente_id):
    query = "SELECT id, nombre, apellido, direccion, email, dni, cuil " \
            "FROM Personas " \
            "WHERE categoria_id = 1 AND id = {cliente_id}".format(cliente_id=cliente_id)

    return _exec_query(query)


def get_forma_pago(forma_pago_id):
    query = "SELECT a.id, a.descripcion, a.recargo, CONCAT(a.descripcion, ' - ', b.nombre) AS name, b.nombre " \
            "FROM MediosDePago a " \
            "INNER JOIN TipoMedioPago b " \
            "ON a.tipo_medio_id = b.id " \
            "WHERE a.id = {forma_pago_id}".format(forma_pago_id=forma_pago_id)

    return _exec_query(query)


def finalizar_venta(transaccion_id, sucursal_id):
    query = "UPDATE Transacciones SET estado = 'FINALIZADA' " \
            "WHERE id = {transaccion_id} AND sucursal_id = {sucursal_id} ".format(transaccion_id=transaccion_id,
                                                                                  sucursal_id=sucursal_id)

    return _exec_query(query)


def nuevo_pedido(sucursal_origen, sucursal_destino, usuario_pedido):
    query = "INSERT INTO Pedidos (suc_origen_id, suc_destino_id, estado_id, usuario_pedido) " \
            "VALUES ({sucursal_origen}, {sucursal_destino}, " \
            "2, {usuario_pedido})".format(sucursal_origen=sucursal_origen,
                                          sucursal_destino=sucursal_destino,
                                          usuario_pedido=usuario_pedido)
    return True#_insert_query(query)


def _insert_query(query):
    db = MySQLdb.connect(**config)

    cursor = db.cursor()
    id = None

    try:
        cursor.execute(query)
        id = cursor.lastrowid
        cursor.close()
        db.commit()
    except Exception as e:
        pass

    db.close()

    return id


def _update_query(query):
    db = MySQLdb.connect(**config)

    cursor = db.cursor()

    try:
        cursor.execute(query)
        cursor.close()
        db.commit()
        result = True
    except Exception as e:
        db.rollback()
        result = False

    db.close()

    return result

def _exec_query(query):
    db = MySQLdb.connect(**config)

    rows_list = []
    cursor = db.cursor()
    message = ""
    result = True
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        col_names = [i[0] for i in cursor.description]
        for row in rows:
            rows_list.append(dict(zip(col_names, row)))
        if rows_list.__len__() == 0:
            result = False
            message = "No records found"
        cursor.close()
    except Exception as e:
        message = "Error while running query: " + str(e)
        result = False

    db.close()

    return result, rows_list, message