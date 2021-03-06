#! /usr/bin/env python
"""
Sample script to send 2 APDU

__author__ = "Ludovic Rousseau"

Copyright 2009
Author: Ludovic Rousseau, mailto:ludovic.rousseau@free.fr

This file is part of pyscard.

pyscard is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 2.1 of the License, or
(at your option) any later version.

pyscard is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with pyscard; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

import sys
import binascii
from smartcard.System import readers

# define the APDUs used in this script
SELECT_APPLET = [0x00, 0xA4, 0x04, 0x00, 0x06, 0xA0, 0x00, 0x00, 0x00,
        0x18, 0xFF]
GET_TIME = [0x80, 0x38, 0x00, 0xA0]
GET_UID = [0xFF, 0xCA, 0x00, 0x00 ,0x04]
GET_UIX = [0xFF, 0xCB, 0x00, 0x00 ,0x04]

try:
    # get all the available readers
    r = readers()
    print "Available readers: ", r

    # by default we use the first reader
    i = 0
    if len(sys.argv) > 1:
        i = int(sys.argv[1])
    print "Using: %s" % r[i]

    connection = r[i].createConnection()
    connection.connect()

    data, sw1, sw2 = connection.transmit(SELECT_APPLET)
    print "Select Applet: %02X %02X" % (sw1, sw2)

    data, sw1, sw2 = connection.transmit(GET_TIME)
    print "Get Time: %02X %02X" % (sw1, sw2)

    data, sw1, sw2 = connection.transmit(GET_UIX)
    print "Get UID: %02X %02X" % (sw1, sw2)
    x = ''
    for i in data : x = x + '%x' %i + ' '
    print x

except:
    print sys.exc_info()[1]
