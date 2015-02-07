__author__ = 'emanuel'
import MySQLdb


def get_stock(stock_sucursal):
    query = "SELECT * from %s" % stock_sucursal
    return exec_query(query)


def exec_query(query):
    db = MySQLdb.connect(host="192.168.203.129",
                         user="root",
                         passwd="123456",
                         db="cruzada")

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