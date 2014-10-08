__author__ = 'krishnaa'

import urllib2
import base64
import sys
import xml.etree.ElementTree as ET

def deployVapp(vapp_name,vapp_desc,vapp_poweron,vapp_deploy,url,authtoken,method,template_url):
    handler = urllib2.HTTPSHandler()
    opener = urllib2.build_opener(handler)
    url = url + '/action/instantiateVAppTemplate'
    request = urllib2.Request(url)
    request.add_header("Accept",'application/*+xml;version=5.5')
    request.add_header("x-vcloud-authorization",authtoken)
    request.add_header('Content-Type', 'application/vnd.vmware.vcloud.instantiateVAppTemplateParams+xml')
    request.get_method = lambda: method
    root = ET.Element('InstantiateVAppTemplateParams', attrib={
                                                                'xmlns':'http://www.vmware.com/vcloud/v1.5',
                                                                'xmlns:ovf':'http://schemas.dmtf.org/ovf/envelope/1',
                                                                'name':vapp_name,
                                                                'deploy':vapp_deploy,
                                                                'powerOn':vapp_poweron
                                                                })
    d = ET.SubElement(root, 'Description')
    s = ET.SubElement(root, 'Source')

    d.text = vapp_desc
    s.attrib['href'] = template_url
    post_string =  ET.tostring(root)
    request.add_data(post_string)
    print "URL: ", url
    print "Template URL: ", template_url

    try:
        connection = opener.open(request)
    except urllib2.HTTPError,e:
        connection = e

    if connection.code == 200 or connection.code == 201:
        data = connection.read()
        #print "Data from Entity"
        print "Data :", data
    else:
        print "ERROR", connection.code
        sys.exit(1)

    vapp_output = ET.fromstring(data)
    print "data from elementtree"
    return vapp_output.attrib['href']