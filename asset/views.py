from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Host,Resource
from datetime import timedelta
from django.utils import timezone
import functools


def index(request):
   return render(request,'asset/index.html')


def list_ajax(request):
    result=[]
    for host in Host.objects.all():
        result.append(host.as_dict())
    return JsonResponse({'code':200,'result': result})

def delete_ajax(request):
    _id = request.GET.get('id',0)
    print(_id)
    try:
       Host.objects.get(pk=_id).delete()
    except ObjectDoesNotExist as e:
        pass
    return JsonResponse({'code':200})
def resource_ajax(request):
     try:
        _id=request.GET.get('id',0)
        host = Host.objects.get(pk=_id)
        end_time = timezone.now()
        start_time = end_time - timedelta(days=1)
        resources = Resource.objects.filter(ip=host.ip,create_time__gte=start_time).order_by('create_time')
        tmp_datetime={}
        data_weekend=[]
        data_cpu=[]
        data_mem=[]
        for resource in resources:
              tmp_datetime[resource.create_time.strftime('%Y-%m-%d %H:%M')] = {'cpu':resource.cpu,'mem':resource.mem}
        while start_time <= end_time:
              key = start_time.strftime('%Y-%m-%d %H:%M')
              resource = tmp_datetime.get(key,{})
              data_weekend.append(start_time)
              data_cpu.append(resource.get('cpu',0))
              data_mem.append(resource.get('mem',0))
              start_time+=timedelta(minutes=1)


        return JsonResponse({'code':200,'result': {'data_weekend':data_weekend,'data_cpu':data_cpu,'data_mem':data_mem}})
     except:
           return JsonResponse({'code':400})
