from django.db import models

class AccessLogfile(models.Model):
    name = models.CharField(max_length=128,null=False,default='')
    path = models.CharField(max_length=1024,null=False,default='')
    created_time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)
