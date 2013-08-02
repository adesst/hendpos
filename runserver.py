#!/usr/bin/env python
# coding: utf-8
import os
import logging
import traceback
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

from app import my_app

class XWSGIServer(WSGIServer):

    def __init__(self, listener, application=None, backlog=None, spawn='default', log='default', handler_class=None,
                 environ=None, **ssl_args):
        super(XWSGIServer, self).__init__(listener, application, backlog, spawn, log, handler_class, environ, **ssl_args)

    def log_error(self, msg, *args):
        try:
            message = msg % args
        except Exception:
            traceback.print_exc()
            message = '%r %r' % (msg, args)
            logging.error('%s %s' % ( traceback.print_exc, message))
        try:
            message = '%s: %s' % (self.socket, message)
        except Exception:
            pass
        try:
            sys.stderr.write(message + '\n')
            logging.error('%s ' % ( message))
        except Exception:
            traceback.print_exc()
            logging.error('%s ' % ( traceback.print_exc))

if __name__ == '__main__':
    print 'Initializing...'
    if os.name == 'nt':
        print 'To Close this application just close this window.'

    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(msg)s", filename="log.txt")

    class SimpleLog():
        def __init__(self):
            pass
        def write(self,msg, *args, **kwargs):
            logging.info(msg.rsplit("\n"))

    try:
        http_server = XWSGIServer(('',5000), my_app, handler_class=WebSocketHandler, log=SimpleLog())
        print 'You can access the application using Firefox (recommended)'
        print 'And type the url to http://localhost:5000/'
        print 'Show time :D'
        http_server.serve_forever()
    except Exception as e:
        print e
        logging.error('%s %s' %(traceback.print_exc(), e))
