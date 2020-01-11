from django.urls import path
from . import views
app_name='asset'
urlpatterns = [
    path('index', views.index,name="index"),
    path('list/ajax',views.list_ajax,name="list_ajax"),
    path('delete/ajax',views.delete_ajax,name='delete_ajax'),
    path('resource/ajax',views.resource_ajax,name='resource_ajax')
]



