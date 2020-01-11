# enconding: utf-8
import json
from django.db import models
from .mysqlDB_CALL import MYSQL_DB
import ssl
from django.db import connection
import hashlib

class User(object):
  MYSQL_LOGIN_SQL = 'SELECT id,name,age,sex,tel,password FROM user2 where name=%s and password=%s'
  MYSQL_LIST_SQL = 'SELECT id,name,age,sex,tel FROM user2'
  MYSQL_COLUMN = ['id', 'name', 'age', 'sex', 'tel']
  SQL_GAT_USER_BY_ID = 'SELECT id ,name,age,sex,tel FROM user2 where id={0}'
  SQL_GAT_USER_BY_name = 'SELECT id ,name,age,sex,tel FROM user2 where name=%s '
  SQL_UPDATE_USER = 'update user2 set name=%s,age=%s,sex=%s,tel=%s where id=%s'
  MYSQL_DELETE_SQL = 'delete from user2 where id={0}'
  SQL_INSERT_USER = 'insert INTO user2(name,password,age,sex,tel) values(%s,%s,%s,%s,%s)'
  SQL_UPDATE_PASSORD='update user2 set password=%s where name=%s'

  def __init__(self, id='', name='', age='', sex='', tel='', password=''):
    self.id = id
    self.name = name
    self.age = age
    self.sex = sex
    self.tel = tel
    self.password = password
  

  @classmethod
  def password_hash(cls,password):
     h = hashlib.sha256()
     passwordstr = str(password)
     h.update(bytes(passwordstr, encoding='utf-8'))
     pawd_result = h.hexdigest()
     return  pawd_result

  @classmethod
  def valid_login(cls, name, password):
    mysql_data = MYSQL_DB.mysqlDB_Call(cls.MYSQL_LOGIN_SQL, (name, password), fetall=False, fetone=True)
    return User(id=mysql_data[0], name=mysql_data[1], age=mysql_data[2], sex=mysql_data[3], tel=mysql_data[4],
                password=mysql_data[5]) if mysql_data else None

  def as_dice(self):
    return {'id': self.id, 'name': self.name, 'age': self.age, 'sex': self.age, 'tel': self.tel}

  @classmethod
  def get_users(cls):
    mysql_data = MYSQL_DB.mysqlDB_Call(cls.MYSQL_LIST_SQL, fetall=True, fetone=False)
    return [{k: v for k, v in zip(cls.MYSQL_COLUMN, i)} for i in mysql_data]

  @classmethod
  def get_user_by_name(cls, name):
    mysql_data = MYSQL_DB.mysqlDB_Call(cls.SQL_GAT_USER_BY_name, (name,), fetall=False, fetone=True)
    return dict(zip(cls.MYSQL_COLUMN, mysql_data)) if mysql_data else None

  def valid_name_unique(name, id=None):
    user = User.get_user_by_name(name)
    if id is None:
      return not user
    else:
      if user is None:
        return None
      else:
        return str(user['id']) == str(id)

  @classmethod
  def get_user(cls, uid):
    mysql_cur = connection.cursor()
    mysql_cur.execute(cls.SQL_GAT_USER_BY_ID.format(uid))
    mysql_data = mysql_cur.fetchone()
    mysql_cur.close()
    return dict(zip(cls.MYSQL_COLUMN, mysql_data)) if mysql_data else None

  @classmethod
  def valid_update_user(cls, params):
    is_valid = True
    user = User()
    errors = {}
    user.id = params.get('id', '').strip()
    if User.get_user(user.id) is None:
      errors['uid'] = '用户不存在'
      is_valid = False
    user.name = params.get('name', '').strip()
    if User.valid_name_unique(user.name, user.id) is not None:
      errors['name'] = '用户名已经存在'
      is_valid = False
    user.age = params.get('age', '0').strip()
    if not user.age.isdigit():
      errors['age'] = '年龄格式错误'
      is_valid = False
    user.tel = params.get('tel', '0')
    user.sex = int(params.get('sex', '0'))

    return is_valid, user, errors

  @classmethod
  def update_user(cls, user):
    user_action = (user.name, user.age, user.sex, user.tel, user.id)
    MYSQL_DB.mysqlDB_Call(cls.SQL_UPDATE_USER, (user_action), fetall=False, fetone=False)
    return True
  @classmethod
  def delete_user(cls,uid):
    mysql_cur = connection.cursor()
    mysql_cur.execute(cls.MYSQL_DELETE_SQL.format(uid))
    connection.commit()
    mysql_cur.close()
    return True
  @classmethod
  def valid_insert_user(cls,params):
    data=params.copy() 
    data['password']=User.password_hash(data['password'])
    MYSQL_DB.mysqlDB_Call(cls.SQL_INSERT_USER,
                          (data['user_name'], data['password'], data['age'], data['sex'], data['tel']),
                          fetall=False, fetone=False)
    return True

  @classmethod
  def res_password(cls,name,password):
    print(name)
    print(password)
    MYSQL_DB.mysqlDB_Call(cls.SQL_UPDATE_PASSORD,(password,name),fetall=False,fetone=False)
    return True




















