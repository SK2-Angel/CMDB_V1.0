import os
import time
import json
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from .models import AccessLogfile

def index(request):
    return render(request,'webanalysis/index.html')



def upload(request):
    log = request.FILES.get('log',None)
    if log:
         path_uploads = os.path.join(settings.BASE_DIR,'media','uploads',str(time.time()))
         fh = open(path_uploads,"wb")
         for chunk in log.chunks():
             fh.write(chunk)
         fh.close()
         obj = AccessLogfile(name=log.name,path=path_uploads)
         obj.save()
         path_notices = os.path.join(settings.BASE_DIR,'media','notices',str(time.time()))
         with open(path_notices,'w') as fh:
              fh.write(json.dumps({'id': obj.id,'path':obj.path}))
    return HttpResponse("upload")



