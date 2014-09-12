#!/bin/python
#-*- encoding: utf-8 -*-
# Python imports
import os
import json
import time
import random

# Tornado imports
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
from tornado.web import url

# Sqlalchemy imports
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# App imports
import models
import proxy_manager

# Options
define("port", default=8012, help="run on the given port", type=int)
define("debug", default=True, type=bool)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			url(r'/proxy', ProxyHandler),
		]
		settings = dict(
			debug=options.debug,
			xsrf_cookies=False,
			cookie_secret="nzjxcjasduuqwheazmu293nsadhaslzkci9023nsadnua9sdads/Vo=",
		)
		tornado.web.Application.__init__(self, handlers, **settings)
		self.p_manager = proxy_manager.ProxyManager()
   
class BaseHandler(tornado.web.RequestHandler):
	def queue(self):
		return self.application.queue

class ProxyHandler(BaseHandler):
	def get(self):
		proxys = self.application.p_manager.get_proxy()
		self.write(str(proxys))
		self.flush()

	def post(self):
		pass

if __name__ == "__main__":
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
