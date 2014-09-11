#!/bin/python
#-*- encoding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from datetime import datetime
import threading

# app import
from html_getter import get_html
from proxy_filter import filte
from proxy_manager import ProxyManager
from usefull_check import check_anonymous
from usefull_check import get_default_ip

import re

BASE_URL = 'http://proxy.com.ru'
URL_HEADER = 'http://proxy.com.ru/list_'
URL_END = '.html'

class ProxySpider(threading.Thread):
	"""docstring for ProxySpider"""
	def __init__(self):
		super(ProxySpider, self).__init__()

	def run(self):
		spider_start_time = str(datetime.now()).split('.')[0]
		print spider_start_time, 'time to spider start!'
		proxy_manager = ProxyManager()
		page = get_html(BASE_URL)
		page = unicode(page,'GBK').encode('UTF-8')
		page_count = self.get_page_count(page)
		page_count_time = str(datetime.now()).split('.')[0]
		print page_count_time, 'get page count:', page_count
		default_ip = get_default_ip()
		if page_count != 0:
			last_proxy = None
			for i in xrange(1, page_count):
				page = get_html(URL_HEADER + str(i) + URL_END, last_proxy)
				proxy_list = filte(page)
				for proxy in proxy_list:
					if proxy.anonymous_type == '高匿':
						check_result = check_anonymous(proxy, default_ip)
						spider_time = str(datetime.now()).split('.')[0]
						if check_result[0]:
							proxy.delay_time = check_result[1]
							proxy.created_time = str(datetime.now()).split('.')[0]
							proxy.is_in_china = 2
							proxy_manager.add_proxy(proxy, spider_time)
							last_proxy = proxy
						else:
							pass
							#print spider_time, proxy.ip, ':', proxy.port, " is not usefull."

	def get_page_count(self, content):
		page_count = 0
		pattern = re.compile(r'共\d{1,3}页')
		page_count_info = re.search(pattern, content)
		if page_count_info:
			page_count = page_count_info.group(0)
			count = int(page_count[3 : len(page_count) - 3])
			return count
		return 0

if __name__ == '__main__':
	xx = ProxySpider()
	xx.start();