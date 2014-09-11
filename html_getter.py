#!/bin/python
#-*- encoding: utf-8 -*-

import urllib2
import socket

user_agents = [
    'Mozilla/6.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/6.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/6.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/6.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
        ]
        
def get_html(url, proxy_info = None):
	if proxy_info:
		proxy_content = proxy_info.ip + ':' + str(proxy_info.port)
		proxy = urllib2.ProxyHandler({proxy_info.proxy_type : proxy_content})
		opener = urllib2.build_opener(proxy)
		urllib2.install_opener(opener)
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agents)
	try:
		response = urllib2.urlopen(req)
		content = response.read()
		print url,' is finished'
		return content
	except socket.error:
		print url,' is failed'
		return ''
	except urllib2.HTTPError:
   		print url+' is forbidden'
		return ''
	except urllib2.URLError:
		print url+' No such file or directory'
		return ''
	except ValueError:
		print url+' unknown url type'
		return ''
	except:
		print 'error when get html' 
		return ''   


if __name__ == '__main__':
	print get_html('http://www.xici.net.co/nt/', None)
	
