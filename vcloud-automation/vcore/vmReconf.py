__author__ = 'krishnaa'

import urllib2
import base64
import sys
import xml.etree.ElementTree as ET

def vmReconf(vm_href,authtoken,method,vm_name,vm_ip,vm_network):
    handler = urllib2.HTTPSHandler()
    opener = urllib2.build_opener(handler)
    url = vm_href + '/action/reconfigureVm'
    request = urllib2.Request(url)
    request.add_header("Accept",'application/*+xml;version=5.5')
    request.add_header("x-vcloud-authorization",authtoken)
    request.add_header('Content-Type', 'application/vnd.vmware.vcloud.vm+xml')
    request.get_method = lambda: method
    root = ET.Element('Vm', attrib={
                                                                'xmlns':'http://www.vmware.com/vcloud/v1.5',
                                                                'xmlns:ovf':'http://schemas.dmtf.org/ovf/envelope/1',
                                                                'name': vm_name
                                                                })

    n = ET.SubElement(root, 'NetworkConnectionSection', attrib={'type':'application/vnd.vmware.vcloud.networkConnectionSection+xml',
                                                                'xmlns':'http://www.vmware.com/vcloud/v1.5',
                                                                'xmlns:ovf':'http://schemas.dmtf.org/ovf/envelope/1'
                                                             #   'ovf:required': 'false'
                                                                })
    n_ovf = ET.SubElement(n, 'ovf:Info')
    n_ovf.text = 'Specifies the available VM network connections'
    pnc = ET.SubElement(n, 'PrimaryNetworkConnectionIndex')
    pnc.text = '0'
    nc = ET.SubElement(n, 'NetworkConnection', attrib={'network':vm_network})
    nci = ET.SubElement(nc,'NetworkConnectionIndex')
    nci.text = '0'


    ip = ET.SubElement(nc,'IpAddress')
    ip.text = vm_ip


    ip_cn = ET.SubElement(nc,'IsConnected')
    ip_cn.text = 'true'

    """
    mac = ET.SubElement(nc, 'MACAddress')
    mac.text = '00:50:56:01:01:49'
    """

    ip_mode = ET.SubElement(nc,'IpAddressAllocationMode')
    ip_mode.text='MANUAL'


    g = ET.SubElement(root, 'GuestCustomizationSection', attrib= {'type':'application/vnd.vmware.vcloud.guestCustomizationSection+xml',
                                                                  'xmlns':'http://www.vmware.com/vcloud/v1.5',
                                                                  'xmlns:ovf':'http://schemas.dmtf.org/ovf/envelope/1',
                                                                  'ovf:required': 'false'})
    ovf = ET.SubElement(g, 'ovf:Info')
    ovf.text = 'Specifies Guest OS Customization Settings'
    c_vmname = ET.SubElement(g, 'ComputerName')
    c_vmname.text = 'MYSERVER'


    """
    s1 = ET.SubElement(root, 'SourcedItem')
    s1.attrib['sourceDelete'] = 'false'
    se1 = ET.SubElement(s1, 'Source')
    se1.attrib['href'] = template_url
    """
    #eu = ET.SubElement(root, 'AllEULAsAccepted')
    #eu.text = 'true'
    post_string =  ET.tostring(root)
    print post_string
    request.add_data(post_string)
    print "URL: ", url
    #print "Template URL: ", template_url

    try:
        connection = opener.open(request)
    except urllib2.HTTPError,e:
        connection = e

    if connection.code == 200 or connection.code == 201 or connection.code == 202:
        data = connection.read()
        #print "Data from Entity"
        print "Data :", data
    else:
        print "ERROR", connection.code
        print connection.read()
        sys.exit(1)

    vapp_output = ET.fromstring(data)
    print "data from elementtree"
    print vapp_output
    return vapp_output.attrib['href']

