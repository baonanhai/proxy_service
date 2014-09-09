#!/bin/python
#-*- encoding: utf-8 -*-
import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger, Text
from sqlalchemy import create_engine

DB_PATH = 'mysql://root:654321@localhost:3306/proxy_service?charset=utf8'
Base = declarative_base()

class Proxy(Base):
	__tablename__ = 'proxy'
	id = Column(Integer, primary_key=True)
	ip = Column(String(20))
	port = Column(Integer)
	proxy_type = Column(String(10))
	anonymous_type = Column(String(10))
	is_in_china = Column(Integer)
	location = Column(String(20))
	delay_time = Column(Integer)
	created_time = Column(DateTime)
	check_time = Column(DateTime)

	def __init__(self):
		pass

	# def __init__(self, ip, port, delay_time, proxy_type, anonymous_type, is_in_china, location, created_time, check_time):
	#     self.ip = ip
	#     self.port = port
	#     self.delay_time = delay_time
	#     self.proxy_type = proxy_type
	#     self.anonymous_type = anonymous_type
	#     self.is_in_china = is_in_china
	#     self.location = location
	#     self.created_time = created_time
	#     self.check_time = check_time

	def __repr__(self):
		info = {}
		info['ip'] = self.ip
		info['port'] = self.port
		info['proxy_type'] = self.proxy_type
		info['anonymous_type'] = self.anonymous_type
		info['is_in_china'] = self.is_in_china
		info['location'] = self.location
		info['delay_time'] = self.delay_time
		info['created_time'] = str(self.created_time)
		info['check_time'] = str(self.check_time)
		return json.dumps(info)

def init_db(engine):
	Base.metadata.create_all(engine)

if __name__ == '__main__':
	engine = create_engine(DB_PATH, convert_unicode=True, pool_recycle=7200)
	init_db(engine)
