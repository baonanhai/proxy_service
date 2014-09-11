#!/bin/python
#-*- encoding: utf-8 -*-

import urllib2
import time
import sys
from datetime import datetime
from BeautifulSoup import BeautifulSoup
from models import Proxy
import re

reload(sys) 
sys.setdefaultencoding('utf-8')     

GOOGLE_CHECK_URL = 'https://www.google.com.hk/'
CHECK_URL = 'http://www.baidu.com'
ANONYMOUS_CHECK_URL = 'http://20140507.ip138.com/ic.asp'

def get_default_ip():
	while True:
		try:
			response = urllib2.urlopen(ANONYMOUS_CHECK_URL, timeout=3)
			body = BeautifulSoup(response).body.text
			pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
			rel_ip_info = re.search(pattern, body)
			if rel_ip_info:
				ip = rel_ip_info.group(0)
				return ip
		except:
			pass

def check(proxy_info):
	proxy_content = proxy_info.ip + ':' + str(proxy_info.port)
	proxy = urllib2.ProxyHandler({proxy_info.proxy_type : proxy_content})
	opener = urllib2.build_opener(proxy)
	urllib2.install_opener(opener)
	try:
		time1 = time.time()
		response = urllib2.urlopen(CHECK_URL, timeout=3)
		title = BeautifulSoup(response.read()).title.text
		if '百度一下，你就知道' == str(title):
			proxy_info.check_time = str(datetime.now()).split('.')[0]
			return (True, (time.time() - time1) * 1000)
		else:
			return (False, 0)
	except:
		return (False, 0)

def check_anonymous(proxy_info, default_ip):
	proxy_content = proxy_info.ip + ':' + str(proxy_info.port)
	proxy = urllib2.ProxyHandler({proxy_info.proxy_type : proxy_content})
	opener = urllib2.build_opener(proxy)
	urllib2.install_opener(opener)
	try:
		time1 = time.time()
		response = urllib2.urlopen(ANONYMOUS_CHECK_URL, timeout=5)
		body = BeautifulSoup(response).body.text
		pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
		rel_ip_info = re.search(pattern, body)
		if rel_ip_info:
			ip = rel_ip_info.group(0)
			print 'Now IP:', ip, 'default_ip:', default_ip
			if ip != default_ip:
				proxy_info.check_time = str(datetime.now()).split('.')[0]
				return (True, (time.time() - time1) * 1000)
		return (False, 0)
	except:
		return (False, 0)

def check_google(proxy_info):
	proxy_content = proxy_info.ip + ':' + str(proxy_info.port)
	proxy = urllib2.ProxyHandler({proxy_info.proxy_type : proxy_content})
	opener = urllib2.build_opener(proxy)
	urllib2.install_opener(opener)
	try:
		time1 = time.time()
		response = urllib2.urlopen(GOOGLE_CHECK_URL, timeout=3)
		title = BeautifulSoup(response.read()).title.text
		if 'Google' == str(title):
			proxy_info.check_time = str(datetime.now()).split('.')[0]
			return (True, (time.time() - time1) * 1000)
		else:
			return (False, 0)
	except:
		return (False, 0)

if __name__ == '__main__':
	proxy = Proxy()
	proxy.ip = '222.74.6.48'
	proxy.port = '8000'
	proxy.proxy_type = 'http'
	default_ip = get_default_ip()
	print check_anonymous(proxy, default_ip)
	
	