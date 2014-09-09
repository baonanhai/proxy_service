#!/bin/python
#-*- encoding: utf-8 -*-

import urllib2
import time
import sys
from datetime import datetime
from BeautifulSoup import BeautifulSoup
from models import Proxy

reload(sys) 
sys.setdefaultencoding('utf-8')     

CHECK_URL = 'http://www.baidu.com'

def check(proxy_info):
	proxy_content = proxy_info.ip + ':' + str(proxy_info.port)
	proxy = urllib2.ProxyHandler({proxy_info.proxy_type : proxy_content})
	opener = urllib2.build_opener(proxy)
	urllib2.install_opener(opener)
	try:
		time1 = time.time()
		response = urllib2.urlopen(CHECK_URL, timeout=3)
		title = BeautifulSoup(response.read()).title.text
		proxy_info.check_time = str(datetime.now()).split('.')[0]
		if '百度一下，你就知道' == str(title):
			return (True, (time.time() - time1) * 1000)
		else:
			return (False, 0)
	except:
		return (False, 0)

if __name__ == '__main__':
	proxy = Proxy()
	proxy.ip = '101.64.236.206'
	proxy.port = '18000'
	proxy.proxy_type = 'http'
	print check(proxy)
