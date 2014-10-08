__author__ = 'krishnaa'

import urllib2
import base64
import sys
import xml.etree.ElementTree as ET

def checkVAPP(vapp_name,url,authtoken,method):
    handler = urllib2.HTTPSHandler()
    opener = urllib2.build_opener(handler)
    request = urllib2.Request(url)
    request.add_header("Accept",'application/*+xml;version=5.5')
    request.add_header("x-vcloud-authorization",authtoken)
    request.get_method = lambda: method
    try:
        connection = opener.open(request)
    except urllib2.HTTPError,e:
        connection = e

    if connection.code == 200:
        data = connection.read()
        #print "Data from Entity"
        print "Data :", data
    else:
        print "ERROR", connection.code
        sys.exit(1)

    vdc_xml = ET.fromstring(data)
    print "list VDC"
    vdc = vdc_xml.findall("ns:ResourceEntities/ns:ResourceEntity",namespaces={'ns':'http://www.vmware.com/vcloud/v1.5'})
    print vdc
    for c in vdc:
        if c.attrib['type'] == "application/vnd.vmware.vcloud.vApp+xml" and c.attrib['name'] == vapp_name:
            print c.attrib
            vapp_href = c.attrib['href']
            vapp_exist = True
            break
        else:
            vapp_href = "NULL"
            vapp_exist = False

    return (vapp_href,vapp_exist)