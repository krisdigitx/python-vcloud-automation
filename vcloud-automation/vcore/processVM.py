__author__ = 'krishnaa'

import time

from addVM import addVM
from taskStatus import taskStatus
from getVAPP import getVAPP
from vmReconf import vmReconf


def processVM(vapp_name,vapp_desc,vapp_href,vdc_href,authtoken,new_vm_name,vm_ip,vm_network):

    task_href = addVM(vapp_name,vapp_desc,vapp_href,vdc_href,authtoken,'POST')

    while True:
        task_status = taskStatus(task_href,authtoken,'GET')
        if task_status != 'success':
            print "Rechecking task status in 10secs..."
            time.sleep(10)
        else:
            break

    print 'add vm: ',task_status

    vm_href,vm_name = getVAPP(vapp_href,authtoken,'GET')
    if vm_name == 'New Base VM':
        print "Correct VM Identified..."
        print vm_name
        print vm_href
        print "Reconfiguring VM..."
        vm_reconf_href = vmReconf(vm_href,authtoken,'POST',new_vm_name,vm_ip,vm_network)
        print "VM rename task URL ", vm_reconf_href
        while True:
            task_status = taskStatus(vm_reconf_href,authtoken,'GET')
            if task_status != 'success':
                print "Rechecking task status in 10secs..."
                time.sleep(10)

            else:
                break
    else:
        print "Cannot find the new VM in the VAPP"

