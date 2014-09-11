#!/bin/python
#-*- encoding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from datetime import datetime
import threading

# app import
from html_getter import get_html
from xici_filter import filte
from proxy_manager import ProxyManager
from usefull_check import check_anonymous
from usefull_check import get_default_ip

BASE_URL = 'http://www.xici.net.co/'
CHINA_ANONYMOUS = 'nn/'    	#国内匿名
CHINA_NORMAL = 'nt/'		#国内普通
NO_CHINA_ANONYMOUS = 'wn/'	#国外匿名
NO_CHINA_NORMAL = 'wt/'		#国外普通

class XiciSpider(threading.Thread):
	"""docstring for XiciSpider"""
	def __init__(self):
		super(XiciSpider, self).__init__()
		self.urls = []
		self.urls.append(BASE_URL + CHINA_ANONYMOUS);
		self.urls.append(BASE_URL + CHINA_NORMAL);
		self.urls.append(BASE_URL + NO_CHINA_ANONYMOUS);
		self.urls.append(BASE_URL + NO_CHINA_NORMAL);

	def run(self):
		spider_start_time = str(datetime.now()).split('.')[0]
		print spider_start_time, 'time to spider start!'
		proxy_manager = ProxyManager()
		last_proxy = None
		for url in self.urls:
			page = get_html(url)
			page_count = self.get_page_count(page)
			page_count_time = str(datetime.now()).split('.')[0]
			print page_count_time, 'get page count:', page_count
			default_ip = get_default_ip()
			for i in xrange(1, page_count):
				page = get_html(url + str(i))
				proxy_list = filte(page)
				for proxy in proxy_list:
					if proxy.anonymous_type == '高匿':
						check_result = check_anonymous(proxy, default_ip)
						spider_time = str(datetime.now()).split('.')[0]
						if check_result[0]:
							proxy.delay_time = check_result[1]
							proxy.created_time = str(datetime.now()).split('.')[0]
							proxy.is_in_china = 0
							if url.endswith(CHINA_ANONYMOUS) or url.endswith(CHINA_NORMAL):
								proxy.is_in_china = 1
							proxy_manager.add_proxy(proxy, spider_time)
							last_proxy = proxy
						else:
							pass
							#print spider_time, proxy.ip, ':', proxy.port, " is not usefull."

	def get_page_count(self, content):
		page_count = 0
		soup = BeautifulSoup(content)
		for info in soup.findAll('a', attrs={'href':True}):
			try:
				page_count = int(info.text)
			except (UnicodeEncodeError, ValueError):
				pass
		return page_count

if __name__ == '__main__':
	xx = XiciSpider()
	xx.start();