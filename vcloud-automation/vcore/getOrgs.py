__author__ = 'krishnaa'
import urllib2
import base64
import sys
import xml.etree.ElementTree as ET

def getOrgs(url,authtoken,method):
    print authtoken
    handler = urllib2.HTTPSHandler()
    opener = urllib2.build_opener(handler)
    url = url + '/api/org'
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
        print "Data from ORG "
        #print "Data :", data
    else:
        print "ERROR", connection.code
        sys.exit(1)
    orgxml = ET.fromstring(data)
    print "printing org XML"

    dict = {}
    orgs = []
    print orgxml
    versioninfo = orgxml.find("ns:Org",namespaces={'ns':'http://www.vmware.com/vcloud/v1.5'})
    for key,value in versioninfo.attrib.items():
        print key , value
        dict[key] = value
    orgs.append(dict)
    print orgs
    return orgs