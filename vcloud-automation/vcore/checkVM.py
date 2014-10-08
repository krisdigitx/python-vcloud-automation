__author__ = 'krishnaa'

from getvAPPDetails import getvAPPDetails

def checkVM(vm_name,url,authtoken,method):
    print "checking if VM exists inside the VAPP"
    deploy_vapp_status = getvAPPDetails(url,authtoken,method)
    """
    while True:
        deploy_vapp_status = getvAPPDetails(url,authtoken,method)
        if deploy_vapp_status.attrib['deployed'] != 'true':
            print "Rechecking status in 10secs..."
            time.sleep(10)
        elif deploy_vapp_status.attrib['deployed'] == 'true':
            break
        else:
            print "unknown error"
    """
    for i in deploy_vapp_status:
        print i
    vm_status = deploy_vapp_status.findall("ns:Children/ns:Vm",namespaces={'ns':'http://www.vmware.com/vcloud/v1.5'})
    print len(vm_status)
    if len(vm_status) == 0:
        vm_exist = False
    for i in vm_status:
        print i.attrib
        print "attrib name: ",i.attrib['name']
        print vm_name
        if i.attrib['name'] == vm_name:
            vm_exist = True
            print "VM exists..."
            break
        else:
            print "cannot find the new VM..."
            vm_exist = False

    print "VM Exist: ",vm_exist
    return (vm_exist)
