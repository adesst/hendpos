hendpos
=======

It is a simple NFC implementation of POS System using:

1. Flask

2. Gevent and Greenlet (websocket)

3. pyscard

4. RFIDIOt


### INSTALL:

#### using virtualenv  

$ mkdir hendpos

$ cd hendpos

$ virtualenv .

$ git clone git@github:adesst/hendpos .

$ source bin/activate

$ python setup.py install


#### no virtualenv

$ git clone git@github:adesst/hendpos hendpos

$ cd hendpos

$ python setup.py install


### REQUIREMENTS:

1. Browser that supports websocket (Firefox 12 or above)

2. PCSC module (linux: pcsc-lite along with cardiid)

3. MySQL (installed, and hendpos database must exists/created)

Have fun!
