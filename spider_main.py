#!/bin/python
#-*- encoding: utf-8 -*-

import thread

from xici_spider import XiciSpider
from proxy_spider import ProxySpider

def start_xici():
	xici_spider = XiciSpider()
	xici_spider.start()

def start_proxy():
	proxy_spider = ProxySpider()
	proxy_spider.start()

if __name__ == '__main__':
	start_xici()
	start_proxy()
