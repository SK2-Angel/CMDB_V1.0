#enconding: utf-8
import traceback
from django.db import connection


class MYSQL_DB(object):
  @classmethod
  def mysqlDB_Call(cls,SQL,data='',fetall=True,fetone=False):
    try:
      mysql_cur = connection.cursor()
      mysql_cur.execute(SQL,data)
      connection.commit()
      if fetall:
        mysql_data = mysql_cur.fetchall()
        return mysql_data
      elif fetone:
        mysql_data=mysql_cur.fetchone()
        return mysql_data
    except:
      print('数据库调用错误')
      print(traceback.format_exc())
    finally:
      mysql_cur.close()


