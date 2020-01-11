#encoding: utf-8

import os
import json
import shutil
from django.core.management import BaseCommand
from django.conf import settings
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
import ansible.constants as C
from asset.models import Host 

class ResultCallback(CallbackBase):
  def v2_runner_on_ok(self, result, **kwargs):
      if result.task_name=='collect_host':
         self.collect_host(result._result)
  def collect_host(self,result):
      facts = result.get('ansible_facts',{})
      ip=facts.get('ansible_default_ipv4',{}).get('address','')
      name=facts.get('ansible_nodename','')
      mac=facts.get('ansible_default_ipv4',{}).get('macaddress','')
      os=facts.get('ansible_lsb',{}).get('description','')
      arch=facts.get('ansible_machine','')
      mem=facts.get('ansible_memory_mb',{}).get('real',{}).get('total','')
      cpu=facts.get('ansible_processor_vcpus','')
      def select_disk():
            disk_name=[]
            disk_size=[]
            for i in facts.get('ansible_mounts',[]):
                 disk_name.append(i.get('device'))
                 disk_size.append(round((i.get('size_total') /1024 /1024 /1024),2))
            return dict(zip(disk_name,disk_size))
      disk=select_disk()
      Host.create_or_replace(ip,name,mac,os,arch,mem,cpu,json.dumps(disk))



class Command(BaseCommand):


     def handle(self,*args,**options):
         Ansible_Options = namedtuple('Ansible_Options',
                              ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check','diff'])
         options = Ansible_Options(connection='smart', module_path=[], forks=10, become=None,
                           become_method=None, become_user=None, check=False, diff=False)
         loader = DataLoader()
         passwords = {}
         results_callback = ResultCallback()
         inventory = InventoryManager(loader=loader, sources=('/opt/sumscope/hosts'))
         variable_manager = VariableManager(loader=loader,inventory=inventory)
         play_source = {
           'name': "cmdb",
           'hosts': 'all',
           'gather_facts': 'no',
           'tasks': [
             {
               'name': 'collect_host',
               'setup': ''
             }
           ]
         }

         play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

         tqm = None
         try:
           tqm = TaskQueueManager(
             inventory=inventory,
             variable_manager=variable_manager,
             loader=loader,
             options=options,
             passwords=passwords,
             stdout_callback=results_callback,
           )
           result = tqm.run(play)
         finally:
           if tqm is not None:
             tqm.cleanup()

           shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)



