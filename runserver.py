#!/usr/bin/env python
# coding: utf-8
import logging
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

from app import my_app

if __name__ == '__main__':
    log = logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(msg)s", filename="log.txt")
    http_server = WSGIServer(('',5000), my_app, handler_class=WebSocketHandler, log=log)
    http_server.serve_forever()

