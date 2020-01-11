from django.urls import path
from user import views
app_name='user'
urlpatterns = [
    path('index/', views.index,name="index"),
    path('login/', views.login,name="login"),
    path('loginout/',views.loginout,name="loginout"),
    path('delete/',views.delete,name='delete'),
    path('view/',views.view,name='view'),
    path('update/',views.update,name='update'),
    path('insert/',views.insert,name='insert'),
    path('re_password',views.re_password,name='re_password'),
    path('create/ajax/',views.create_ajax,name='create_ajax'),
]


