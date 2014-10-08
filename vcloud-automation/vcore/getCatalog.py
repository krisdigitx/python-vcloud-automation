__author__ = 'krishnaa'

import urllib2
import base64
import sys
import xml.etree.ElementTree as ET

def getCatalog(url,authtoken,method,vapp_name):
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
        #print "Data from Catalog "
        #print "Data :", data
    else:
        print "ERROR", connection.code
        sys.exit(1)
    catalog_xml = ET.fromstring(data)
    #print "catlog xml"
    catg = catalog_xml.findall("ns:CatalogItems/ns:CatalogItem",namespaces={'ns':'http://www.vmware.com/vcloud/v1.5'})
    for cat in catg:
        cat_dict = cat.attrib
        if vapp_name in cat_dict.values():
            vapp_dict = cat_dict
    return vapp_dict
