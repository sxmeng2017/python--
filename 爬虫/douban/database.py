import pymysql

MYSQL_DB = 'douban'
MYSQL_USER = 'root'
MYSQL_PASS = '123456'
MYSQL_HOST = 'localhost'

connection = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER,
                             password=MYSQL_PASS, db=MYSQL_DB,
                             cursorclass=pymysql.cursors.DictCursor)