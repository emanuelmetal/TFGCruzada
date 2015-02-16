import keyword

__author__ = 'emanuel'
import MySQLdb
config = {"host": "192.168.203.129",
         "user": "root",
         "passwd": "123456",
         "db": "cruzada"}


def get_stock_sucursal(stock_sucursal):
    query = "SELECT b.*, c.descripcion AS color, t.descripcion AS talle, a.cantidad AS stock " \
            "FROM %s AS a " \
            "INNER JOIN Articulos AS b " \
            "ON a.articulo = b.id " \
            "INNER JOIN Colores AS c " \
            "ON b.color_id = c.id " \
            "INNER JOIN Talle AS t " \
            "ON b.talle_id = t.id" % stock_sucursal

    return _exec_query(query)


def get_stock_ajax(stock_sucursal, _keyword):
    # split keyword by spaces
    keywords = _keyword.split(" ")
    condition = "(b.codigo LIKE '%{keyword}%' " \
            "OR b.descripcion LIKE '%{keyword}%' " \
            "OR c.descripcion LIKE '%{keyword}%' " \
            "OR t.descripcion LIKE  '%{keyword}%')"
    conditions = []
    for kwd in keywords:
        conditions.append(condition.format(keyword=kwd))

    query = "SELECT b.*, c.descripcion AS color, t.descripcion AS talle, a.cantidad, " \
            "CONCAT(b.descripcion,' ', c.descripcion, ' ', t.descripcion) AS name " \
            "FROM {table_name} AS a " \
            "INNER JOIN Articulos AS b " \
            "ON a.articulo = b.id " \
            "INNER JOIN Colores AS c " \
            "ON b.color_id = c.id " \
            "INNER JOIN Talle AS t " \
            "ON b.talle_id = t.id " \
            "WHERE {conditions} ".format(conditions=" AND ".join([x for x in conditions]),
                                         table_name=stock_sucursal)

    return _exec_query(query)


def update_stock(table_name, cantidad, articulo_id):
    query = "UPDATE {table_name} SET cantidad = cantidad + {cantidad} " \
            "WHERE articulo = {articulo_id}".format(table_name=table_name,
                                                    cantidad=cantidad,
                                                    articulo_id=articulo_id)

    return _update_query(query)


def get_articulo(articulo_id):
    query = "SELECT b.*, c.descripcion AS color, t.descripcion AS talle " \
            "FROM Articulos AS b " \
            "INNER JOIN Colores AS c " \
            "ON b.color_id = c.id " \
            "INNER JOIN Talle AS t " \
            "ON b.talle_id = t.id " \
            "WHERE b.id = {articulo_id}".format(articulo_id=articulo_id)

    result, rows_list, message = _exec_query(query)
    return rows_list[0]


def _update_query(query):
    db = MySQLdb.connect(**config)

    cursor = db.cursor()
    result = True
    try:
        cursor.execute(query)
        db.commit()

    except Exception as e:
        message = "Error while running query: " + str(e)
        result = False

    cursor.close()
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