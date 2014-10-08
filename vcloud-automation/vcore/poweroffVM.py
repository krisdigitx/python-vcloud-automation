__author__ = 'krishnaa'

import urllib2
import base64
import sys
import xml.etree.ElementTree as ET

def poweroffVM(vm_href,authtoken,method):
    handler = urllib2.HTTPSHandler()
    opener = urllib2.build_opener(handler)
    url = vm_href + '/action/undeploy'
    request = urllib2.Request(url)
    request.add_header("Accept",'application/*+xml;version=5.5')
    request.add_header("x-vcloud-authorization",authtoken)
    request.get_method = lambda: method

    request.add_header('Content-Type', 'application/vnd.vmware.vcloud.undeployVAppParams+xml')
    request.get_method = lambda: method
    root = ET.Element('UndeployVAppParams', attrib={
                                                                'xmlns':'http://www.vmware.com/vcloud/v1.5'
                                                                })
    d = ET.SubElement(root, 'UndeployPowerAction')
    d.text = 'powerOff'
    post_string =  ET.tostring(root)
    request.add_data(post_string)
    print "URL: ", url

    print url
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

    vmpoweroff_output = ET.fromstring(data)
    print "data from poweroff"
    return (vmpoweroff_output.attrib['status'],vmpoweroff_output.attrib['href'])