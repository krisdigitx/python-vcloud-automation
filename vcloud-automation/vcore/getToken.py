__author__ = 'krishnaa'
import urllib2
import base64
import sys


def getToken(url,login,passwd,method):
    handler = urllib2.HTTPSHandler()
    opener = urllib2.build_opener(handler)
    url = url + '/api/sessions'
    request = urllib2.Request(url)

    base64string = base64.encodestring('%s:%s' % (login, passwd))[:-1]
    authheader = "Basic %s" % base64string
    request.add_header("Authorization", authheader)
    request.add_header("Accept",'application/*+xml;version=5.5')

    request.get_method = lambda: method

    try:
        connection = opener.open(request)
    except urllib2.HTTPError,e:
        connection = e

    if connection.code == 200:
        data = connection.read()
        print "Session code "
        authtoken = connection.info().getheader('x-vcloud-authorization')
        #print "Data :", data
    else:
        print "Unauthorized..."
        print "ERROR", connection.code, connection.read()
        sys.exit(1)
    return authtoken
