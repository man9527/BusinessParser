import urllib2
import httplib
import socket
import time

httplib.HTTPConnection._http_vsn = 10
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

socket.setdefaulttimeout(30)

def get(url):
    try:
        page_html_file = urllib2.urlopen(url)
        return page_html_file.read()
    except Exception, e:
        time.sleep(1)
        try:
            page_html_file = urllib2.urlopen(url)
            return page_html_file.read()
        except Exception, e:
            raise Exception(e)
