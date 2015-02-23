__author__ = 'emanuel'
import MySQLdb

config = {"host": "192.168.203.129",
         "user": "root",
         "passwd": "123456",
         "db": "cruzada",
         "charset": "utf8"}


def nueva_transaccion(cliente_id, vendedor_id, forma_pago_id, promocion_id):
    cliente_id = 'null' if cliente_id == '' else cliente_id
    vendedor_id = 'null' if vendedor_id == '' else vendedor_id
    forma_pago_id = 'null' if forma_pago_id == '' else forma_pago_id
    promocion_id = 'null' if promocion_id == '' else promocion_id

    query = "INSERT INTO Transacciones (fecha,vendedor_id,forma_pago_id,cliente_id,promocion_id,tipo) " \
            "VALUES (now(),{vendedor_id}, {forma_pago_id}, {cliente_id}, {promocion_id}, 'VENTA')".format(
        vendedor_id=vendedor_id,
        forma_pago_id=forma_pago_id,
        cliente_id=cliente_id,
        promocion_id=promocion_id)

    return _insert_query(query)


def nuevo_renglon(articulo_id, cantidad, precio_unitario, cabecera_id):
    query = "INSERT INTO TransaccionesRen (articulo_id, cantidad, precio_unitario, cabecera_id) " \
            "VALUES ({articulo_id}, {cantidad}, {precio_unitario}, {cabecera_id})".format(
        articulo_id=articulo_id,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        cabecera_id=cabecera_id)

    _insert_query(query)


def nuevo_cliente(nombre,apellido,email,direccion,dni,cuil):
    query = "INSERT INTO Personas (nombre,apellido,email,direccion,dni,cuil,categoria_id,sucursal_id,rol_id,user_id) " \
            "VALUES ('{nombre}','{apellido}','{email}','{direccion}',{dni},'{cuil}',1,null,null,null) " \
            "".format(nombre=nombre, apellido=apellido, email=email, direccion=direccion, dni=dni, cuil=cuil)

    return _insert_query(query)


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


def get_cliente_ajax(_keyword):
    # split keyword by spaces
    keywords = _keyword.split(" ")
    condition = "(nombre LIKE '%{keyword}%' " \
            "OR apellido LIKE '%{keyword}%' " \
            "OR CAST(dni AS CHAR) = '%{keyword}%')"
    conditions = []
    for kwd in keywords:
        conditions.append(condition.format(keyword=kwd))

    query = "SELECT nombre, apellido, dni, email, cuil, direccion, " \
            "CONCAT(nombre, ' ', apellido, ' ', dni, ' ', email) AS name " \
            "FROM Personas " \
            "WHERE categoria_id = 1 AND {conditions} ".format(conditions=" AND ".join([x for x in conditions]))

    return _exec_query(query)


def get_forma_pago_ajax(_keyword):

    query = "SELECT a.descripcion, a.recargo, b.nombre, CONCAT(a.descripcion, ' - ', b.nombre) AS name " \
            "FROM MediosDePago AS a " \
            "INNER JOIN TipoMedioPago b " \
            "ON a.tipo_medio_id = b.id " \
            "WHERE descripcion LIKE '%{keyword}%' ".format(keyword=_keyword)

    return _exec_query(query)


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