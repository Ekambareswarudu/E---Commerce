import pymysql
def DBConnection():
    con=pymysql.connect(host='localhost', user='root', password='root', database='e_commerce', charset='utf8')
    return con
