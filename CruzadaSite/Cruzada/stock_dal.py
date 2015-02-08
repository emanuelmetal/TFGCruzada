import keyword

__author__ = 'emanuel'
import MySQLdb


def get_stock_sucursal(stock_sucursal):
    query = "SELECT b.*, c.descripcion AS color, t.descripcion AS talle, a.cantidad AS stock " \
            "FROM %s AS a " \
            "INNER JOIN Articulos AS b " \
            "ON a.articulo = b.id " \
            "INNER JOIN Colores AS c " \
            "ON b.color_id = c.id " \
            "INNER JOIN Talle AS t " \
            "ON b.talle_id = t.id" % stock_sucursal

    return exec_query(query)


def get_stock_ajax(stock_sucursal, _keyword):
    query = "SELECT b.*, c.descripcion AS color, t.descripcion AS talle, a.cantidad, " \
            "CONCAT(b.descripcion,' ', c.descripcion, ' ', t.descripcion) AS name " \
            "FROM {table_name} AS a " \
            "INNER JOIN Articulos AS b " \
            "ON a.articulo = b.id " \
            "INNER JOIN Colores AS c " \
            "ON b.color_id = c.id " \
            "INNER JOIN Talle AS t " \
            "ON b.talle_id = t.id " \
            "WHERE b.codigo LIKE '%{keyword}%' " \
            "OR b.descripcion LIKE '%{keyword}%' " \
            "OR c.descripcion LIKE '%{keyword}%' " \
            "OR t.descripcion LIKE  '%{keyword}%' ".format(keyword=_keyword, table_name=stock_sucursal)

    return exec_query(query)


def exec_query(query):
    db = MySQLdb.connect(host="192.168.203.129",
                         user="root",
                         passwd="123456",
                         db="cruzada",
                         charset='utf8')

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