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
from asset.models import Host,Resource

class ResultCallback(CallbackBase):
  def __init__(self):
    super(ResultCallback, self).__init__()
    self._cache_host={}
  def v2_runner_on_ok(self, result, **kwargs):
      if result.task_name=='collect_host':
           facts = result._result.get('ansible_facts', {})
           ip = facts.get('ansible_default_ipv4',{}).get('address','')
           self._cache_host[result._host.name]= ip
      elif result.task_name=='copyfile':
        pass
      elif result.task_name=='collect_resource':
        ip = self._cache_host.get(result._host.name)
        resource=result._result.get('stdout_lines',[])
        Resource.create_system_litle(ip,resource[0],resource[1])


class Command(BaseCommand):

  def handle(self, *args, **options):
    Ansible_Options = namedtuple('Ansible_Options',
                                 ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user',
                                  'check', 'diff'])
    options = Ansible_Options(connection='smart', module_path=[], forks=10, become=None,
                              become_method=None, become_user=None, check=False, diff=False)
    loader = DataLoader()
    passwords = {}
    results_callback = ResultCallback()
    inventory = InventoryManager(loader=loader, sources=('/opt/sumscope/hosts'))
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    play_source = {
      'name': "cmdb",
      'hosts': 'all',
      'gather_facts': 'no',
      'tasks': [
        {
          'name': 'collect_host',
          'setup': ''
        },
        {
          'name':'copyfile',
          'copy':'src={0} dest={1}'.format('/opt/sumscope/python_script/resource.py','/opt/sumscope/python_script/resource.py')
          
        },
        {
          'name': 'collect_resource',
          'command': 'python3 {0}'.format( '/opt/sumscope/python_script/resource.py')
      
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




