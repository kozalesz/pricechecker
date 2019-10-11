from psycopg2 import connect, OperationalError
from database_settings import *


def make_connection():
    try:
        cnx = connect(user=username, password=passwd, host=hostname,
                      database=db_name)
        cursor = cnx.cursor()
        print("Połączenie udane.")
    except OperationalError:
        print("Nieudane połączenie.")
    return cnx, cursor

def close_connection(cnx, cursor):
    cursor.close()
    cnx.close()

def send_data(cnx, cursor, sql):
    cursor.execute("""SELECT price_now, url
                       FROM runcolors
                       WHERE url = %s""",
                   (sql[-3],))
    result = cursor.fetchone()

    if result:
        if result[0] == sql[-4]:
            print("Cena nie uległa zmianie - {}".format(sql[-3]))
        else:
            print("Cena uległa zmianie - {}".format(sql[-3]))
            cursor.execute("""UPDATE runcolors SET price_now = %s WHERE url = %s
            """, (sql[-4], sql[-3]))
    else:
        cursor.execute("""
        INSERT INTO runcolors (brand, product_number, product_name, 
        price_regular, price_now, url, url_jpg, steal)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s)
        """, sql,)
        print("Rekord dodano! - {}".format(sql[-3]))

    cnx.commit()