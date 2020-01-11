#encoding: utf8 

import os
import json
import time
from django.conf import settings
from django.core.management import BaseCommand
import  MySQLdb
MYSQL_HOST='192.168.63.136'
MYSQL_PORT=3306
MYSQL_USER='artogrid'
MYSQL_PASSWORD='123456'
MYSQL_DB='cmdb_kk'
MYSQL_charset='utf8'
mounths={'Jan2':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
dates_format='{0}-{1}-{2} {3}:{4}:{5}'
MYSQL_INSERT_SQL='INSERT INTO web_user(IP_URL,datetime,status_request) values(%s,%s,%s) '


class Command(BaseCommand):
    def handle(self,*args,**options):
       path=os.path.join(settings.BASE_DIR,'media','notices')
       while True:
           lists = os.listdir(path)
           for filename in lists:
               notice = None
               path_notice = os.path.join(path,filename)
               self.parse(path_notice)
               os.unlink(path_notice)
           time.sleep(5)
    def parse(self,notice):
        filend=open(notice,'r')
        date_ss=filend.readline()
        date_ee=json.loads(date_ss)
        file_source=date_ee['path']
        fh = open(file_source,'r')

        while True:
            date_s=fh.readline()
            
            if not date_s:
               break
            lines = date_s.split()
            lines_ip = lines[0]
            lines_date_old = lines[3]
            lines_request = lines[6]
            lines_sqplit = lines_date_old.split('/')
            day = lines_sqplit[0].strip('[')
            mounth_old = lines_sqplit[1]
            mounth = mounths.get(mounth_old)
            dates = lines_sqplit[2]
            dates_split = dates.split(':')
            yeser = dates_split[0]
            houres = dates_split[1]
            minuth = dates_split[2]
            second = dates_split[3]
            datess = dates_format.format(yeser, mounth, day, houres, minuth, second)

            mysql_conne = MySQLdb.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DB,charset=MYSQL_charset)
            mysql_cur = mysql_conne.cursor()
            mysql_cur.execute(MYSQL_INSERT_SQL,(lines_ip,datess,lines_request))
            mysql_conne.commit()
            mysql_cur.close()
            mysql_conne.close()

        filend.close()
       
