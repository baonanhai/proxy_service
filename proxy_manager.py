#!/bin/python
#-*- encoding: utf-8 -*-

import random
import time
from datetime import datetime

# Sqlalchemy imports
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import and_
from sqlalchemy.exc import DisconnectionError
from sqlalchemy import desc

#app import
from models import Proxy
from models import DB_PATH
import usefull_check

class ProxyManager(object):
	def __init__(self):
		super(ProxyManager, self).__init__()
		engine = create_engine(DB_PATH, convert_unicode=True, pool_recycle=5)
		engine.connect()
		self.db = scoped_session(sessionmaker(bind=engine))

	def has_in_db(self, ip, port):
		proxy = self.db.query(Proxy).filter(Proxy.ip == ip and Proxy.port == port).first()
		return proxy

	def add_proxy(self, proxy, spider_time):
		if self.has_in_db(proxy.ip, proxy.port):
			print spider_time, proxy.ip, ':', proxy.port, 'has in DB.'
		else:
			self.db.add(proxy)
			self.db.commit()
			print spider_time, proxy.ip, ':', proxy.port, "insert to DB."

	def del_proxy(self, del_ip, del_port):
		del_proxy = self.db.query(Proxy).filter(Proxy.ip == del_ip and Proxy.port == del_port).first()
		self.db.delete(del_proxy)
		self.db.commit()

	def get_proxy(self, is_anonymous = True, is_china = True):
		anonymous = '透明'
		if is_anonymous:
			anonymous = '高匿'

		country_flag = 0

		proxy_query = self.db.query(Proxy).filter(and_(Proxy.anonymous_type == anonymous, \
		  Proxy.is_in_china != country_flag, Proxy.proxy_type != 'socks4/5')\
		 ).order_by(desc(Proxy.check_time)).limit(10) 

		proxys = []
		for proxy in proxy_query:
			print proxy.check_time
			proxys.append(proxy)
		return proxys

	def check_all_proxy_usefull(self):
		check_start_time = str(datetime.now()).split('.')[0]
		print check_start_time, 'start check all proxy!'
		proxys = self.db.query(Proxy)
		for proxy in proxys:
			check_result = usefull_check.check(proxy)
			check_time = str(datetime.now()).split('.')[0]
			if not check_result[0]:
				self.del_proxy(proxy.ip, proxy.port)
				print check_time, proxy.ip, ':', proxy.port, ' is not usefull and delete it!'
			else:
				self.db.commit()
				print check_time, proxy.ip, ':', proxy.port, ' is usefull! update check time ', proxy.check_time
			
	def check_all_proxy_anonymous(self):
		default_ip = usefull_check.get_default_ip()
		check_start_time = str(datetime.now()).split('.')[0]
		print check_start_time, 'start check all proxy anonymous!'
		proxys = self.db.query(Proxy)
		for proxy in proxys:
			check_result = usefull_check.check_anonymous(proxy, default_ip)
			if not check_result[0]:
				self.del_proxy(proxy.ip, proxy.port)
				print proxy.ip, ':', proxy.port, ' is not anonymous and delete it!'
			else:
				print proxy.ip, ':', proxy.port, ' is anonymous!'


if __name__ == '__main__':
	proxy_manager = ProxyManager()
	proxy_manager.check_all_proxy_anonymous()
