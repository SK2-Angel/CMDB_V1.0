#enconding: utf-8
import ssl
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import User
def index(request):
        if not request.session.get('user'):
                return redirect('user:login')
        return render(request,'user/index.html',{'users' :  User.get_users()})

def login(request):
        if 'GET' == request.method:
                return render(request,'user/login.html')
        else:
                name=request.POST.get('name')
                password=request.POST.get('password')
                retun_values=User.valid_login(name,User.password_hash(password))
                if retun_values:
                        request.session['user']=retun_values.as_dice()

                        return redirect('user:index')
                else:
                        return render(request,'user/login.html',{'name': name,'errors':{'filed':'用户名或密码错误'}})



def loginout(request):
        request.session.flush()
        return redirect('user:login')


def delete(request):
  if not request.session.get('user'):
    return redirect('user:login')
  uid = request.GET.get('uid', )
  if User.delete_user(uid, ):
    return redirect('user:index')


def view(request):
  if not request.session.get('user'):
    return redirect('user:login')
  uid = request.GET.get('uid', '')
  return render(request, 'user/view.html', {'user': User.get_user(uid)})


def update(request):
  if not request.session.get('user'):
    return redirect('user:login')
  is_valid, user, errors = User.valid_update_user(request.POST)
  if is_valid:
    User.update_user(user)
    return redirect('user:index')
  else:
    return render(request, 'user/view.html', {'user': user, 'errors': errors})


def insert(request):
  return render(request, 'user/insert.html', {'user': insert_data(request)})


def insert_data(request):
   if request.POST:
       is_valid = User.valid_insert_user(request.POST)
       return redirect('user:index')
   else:
        #return render(request,'user/insert.html',{'name':name,'errors':{'filde':'创建用户失败,请重新创建'}})
        return render(request,'user/insert.html')

def re_password(request):
   if 'GET' == request.method:
      return render(request,'user/re_password.html')
   else:
       name=request.POST.get('name')
       password_1=request.POST.get('password_1')
       password_2 = request.POST.get('password_2')
       if  User.get_user_by_name(name)  is  None :
          return render(request, 'user/re_password.html', {'name': name, 'errors': {'filed': '没有此用户，请重新输入'}})
       elif  password_1 != password_2:
             return render(request, 'user/re_password.html', {'name': name, 'errors': {'filed': '两次密码输入不一致，请重新输入'}})
       else:
          password=User.password_hash(password_1)
          User.res_password(name,password)
          return redirect('user:re_password')




def create_ajax(request):
  if not request.session.get('user'):
     return JsonResponse({'code':403})

  if request.POST:
       is_valid = User.valid_insert_user(request.POST)
       return JsonResponse({'code':200})
  else:
        #return render(request,'user/insert.html',{'name':name,'errors':{'filde':'创建用户失败,请重新创建'}})
        return JsonResponse({'code':400})

