#!/usr/bin/python2.7

import sys
sys.path.append('/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages')

from N2nd3rdDegree import app

import eventlet
from eventlet import wsgi

eventlet.monkey_patch()

wsgi.server(eventlet.listen(('localhost', 3030)), app)
