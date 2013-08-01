import sys
import os
from setuptools import setup
from setuptools.command.install import install

setup(
    name = 'hendpos',
    install_requires = [
        'Mysql-python',
        'Flask==0.9',
        'pytz',
        'Flask-Babel',
        'Flask-sqlalchemy',
        'Flask-WTF',
        'FormAlchemy',
        'greenlet',
        'gevent',
    ],
)

