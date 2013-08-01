import sys
import os
from setuptools import setup
from setuptools.command.install import install

setup(
    name = 'hendpos',
    version = '1.0',
    install_requires = [
        'Mysql-python==1.2.3',
        'Flask-Babel==0.8',
        'Flask-sqlalchemy==0.16',
        'Flask-WTF==0.8.2',
        'FormAlchemy',
        'sqlalchemy==0.8',
        'Flask-WTF==0.8.2',
        'WTForms==1.0.3',
        'Flask==0.9',
        'gevent-websocket',
        'greenlet',
        'gevent',
        'pytz',
    ],
)

