__author__ = 'krishnaa'

import time

from getvAPPDetails import getvAPPDetails

def getVAPP(url,authtoken,method):

    while True:
        deploy_vapp_status = getvAPPDetails(url,authtoken,method)
        if deploy_vapp_status.attrib['deployed'] != 'true':
            print "Rechecking status in 10secs..."
            time.sleep(10)
        elif deploy_vapp_status.attrib['deployed'] == 'true':
            break
        else:
            print "unknown error"

    for i in deploy_vapp_status:
        print i
    vm_status = deploy_vapp_status.findall("ns:Children/ns:Vm",namespaces={'ns':'http://www.vmware.com/vcloud/v1.5'})
    print len(vm_status)
    for i in vm_status:
        print i.attrib
        if i.attrib['name'] == "New Base VM":
            vm_href = i.attrib['href']
            vm_name = i.attrib['name']
            break
        else:
            print "cannot find the new VM..."
            vm_href = "NULL"
            vm_name = "NULL"

    return (vm_href,vm_name)
