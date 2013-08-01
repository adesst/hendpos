import sys
import os
from setuptools import setup
from setuptools.command.install import install

setup(
    name = 'hendpos',
    version = '1.0',
    install_requires = [
        'Mysql-python==1.2.3',
        'Flask==0.9',
        'pytz',
        'Flask-Babel==0.8',
        'Flask-sqlalchemy==0.16',
        'sqlalchemy==0.8',
        'Flask-WTF==0.8.2',
        'WTForms==1.0.3',
        'FormAlchemy',
        'greenlet',
        'gevent',
        'gevent-websocket',
    ],
)

