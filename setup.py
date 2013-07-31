import sys
import os
from setuptools import setup
from setuptools.command.install import install

class PostTestInstall(install):
    def run(self):
        saved_path = os.getcwd()
        new_path = sys.path[0] + '/app/pyscard-1.6.12'
        os.chdir(new_path)
        install.run(self)
        from subprocess import call
        call(['python','setup.py','install'])
        os.chdir(saved_path)


class PostInstall(install):
    pass

setup(
    install_requires = [
        'Flask==0.9',
        'pytz',
        'Flask-Babel',
        'Flask-sqlalchemy',
        'Flask-Markdown',
        'Flask-WTF',
        'FormAlchemy',
        'greenlet',
        'gevent',
    ],
    cmdclass={'test' : PostTestInstall}
)

