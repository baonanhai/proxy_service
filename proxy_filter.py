#!/bin/python
#-*- encoding: utf-8 -*-

import re
from BeautifulSoup import BeautifulSoup

from models import Proxy
		
def filte(content):
	soup = BeautifulSoup(content)
	proxy_list_tables = soup.findAll('table')
	table_index = 0
	pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
	proxy_list = []
	for table in proxy_list_tables:
		table_index += 1
		if table_index == 3:
			proxy_list_info = table.findAll('tr')
			for proxy in proxy_list_info:
				td_index = 0
				proxy_tds = proxy.findAll('td')
				proxy = Proxy();
				is_proxy = False
				for proxy_td in proxy_tds:
					td_index += 1
					if td_index == 2:
						rel_ip_info = re.search(pattern, proxy_td.text)
						if rel_ip_info:
							proxy.ip = rel_ip_info.group(0)
							is_proxy = True
					elif td_index == 3:
						if is_proxy:
							proxy.port = int(proxy_td.text)
					elif td_index == 4:
						if is_proxy:
							if '匿名代理' == proxy_td.text or '高度匿名' == proxy_td.text:
								proxy.anonymous_type = '高匿'
							else:
								proxy.anonymous_type = '透明'
					elif td_index == 5:
						if is_proxy:
							proxy.location = proxy_td.text
							proxy.proxy_type = 'http'
				if is_proxy:
					proxy_list.append(proxy)
	return proxy_list

if __name__ == '__main__':
	html = open('test.html', 'r')
	print filte(html)