#!/bin/python
#-*- encoding: utf-8 -*-

from BeautifulSoup import BeautifulSoup

from models import Proxy
		
def filte(content):
	soup = BeautifulSoup(content)
	proxy_list_info = soup.findAll('tr')
	proxy_list = []
	for proxy in proxy_list_info:
		td_index = 0
		proxy_tds = proxy.findAll('td')
		has_get = False 
		proxy = Proxy();
		for proxy_td in proxy_tds:
			td_index += 1
			if td_index == 2:
				has_get = True
				proxy.ip = proxy_td.text
			elif td_index == 3:
				proxy.port = proxy_td.text
			elif td_index == 4:
				if not proxy_td.a == None:
					proxy.location = proxy_td.a.text
			elif td_index == 5:
				proxy.anonymous_type = proxy_td.text
			elif td_index == 6:
				proxy.proxy_type = proxy_td.text

		if has_get:
			proxy_list.append(proxy)
	return proxy_list

if __name__ == '__main__':
	html = open('test.html', 'r')
	proxy_filter = ProxyFilter(None)
	print proxy_filter.filte(html)