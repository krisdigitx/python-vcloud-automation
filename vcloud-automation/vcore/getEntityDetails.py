__author__ = 'krishnaa'

import urllib2
import base64
import sys
import xml.etree.ElementTree as ET

def getEntityDetails(url,authtoken,method):
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
        #print "Data :", data
    else:
        print "ERROR", connection.code
        sys.exit(1)
    """
    catalogItem_xml = ET.fromstring(data)
    print "catlog item xml"
    cati = catalogItem_xml.findall("ns:Entity",namespaces={'ns':'http://www.vmware.com/vcloud/v1.5'})
    for c in cati:
        cati_dict = c.attrib

    return cati_dict
    """