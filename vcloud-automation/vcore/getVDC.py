__author__ = 'krishnaa'

import urllib2
import base64
import sys
import xml.etree.ElementTree as ET

def getVDC(url,authtoken,vdc_lookup,catalog):
    method = 'GET'
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
        #print "Data from ORG "
        #print "Data :", data
    else:
        print "ERROR", connection.code
        sys.exit(1)
    orgxml = ET.fromstring(data)
    #print "orging xml"
    orgxml = ET.fromstring(data)
    vdc = orgxml.findall("ns:Link",namespaces={'ns':'http://www.vmware.com/vcloud/v1.5'})
    #print len(vdc)
    orgc = []
    for i in vdc:
        dict = i.attrib
        if "application/vnd.vmware.vcloud.vdc+xml" and vdc_lookup in dict.values():
            if vdc_lookup in dict.values():
                vdc_dict = dict
        if "application/vnd.vmware.vcloud.catalog+xml" and catalog in dict.values():
            if catalog in dict.values():
                catalog_dict = dict


    return (vdc_dict,catalog_dict)