import pymysql

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_DB = 'inventario_oficina'

def get_db_connection():
    return pymysql.connect(host=MYSQL_HOST,
                           user=MYSQL_USER,
                           password=MYSQL_PASSWORD,
                           database=MYSQL_DB)