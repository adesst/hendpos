import sys
import os
from setuptools import setup
from setuptools.command.install import install

setup(
    name = 'hendpos',
    version = '1.0',
    install_requires = [
        'Mysql-python',
        'Flask==0.9',
        'pytz',
        'Flask-Babel',
        'Flask-sqlalchemy',
        'Flask-WTF==0.8.2',
        'FormAlchemy',
        'greenlet',
        'gevent',
    ],
)

