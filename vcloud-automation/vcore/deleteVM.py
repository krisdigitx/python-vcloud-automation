__author__ = 'krishnaa'

import urllib2
import base64
import sys
import xml.etree.ElementTree as ET

def deleteVM(vapp_name,vapp_href,vm_href,authtoken,method):
    handler = urllib2.HTTPSHandler()
    opener = urllib2.build_opener(handler)
    url = vapp_href + '/action/recomposeVApp'
    request = urllib2.Request(url)
    request.add_header("Accept",'application/*+xml;version=5.5')
    request.add_header("x-vcloud-authorization",authtoken)
    request.add_header('Content-Type', 'application/vnd.vmware.vcloud.recomposeVAppParams+xml')
    request.get_method = lambda: method
    root = ET.Element('RecomposeVAppParams', attrib={
                                                                'xmlns':'http://www.vmware.com/vcloud/v1.5',
                                                                'xmlns:ovf':'http://schemas.dmtf.org/ovf/envelope/1',
                                                                'name':vapp_name
                                                                })
    #d = ET.SubElement(root, 'Description')
    s = ET.SubElement(root, 'DeleteItem')

    #d.text = vapp_desc
    s.attrib['href'] = vm_href
    post_string =  ET.tostring(root)
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