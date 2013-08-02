import sys
import traceback
import logging
import json
import app
import re
import ast
import subprocess
import datetime
from gevent import sleep

split_rule = re.compile('::')
error_pattern = re.compile('^Error')
PATH_RFIDIOT = sys.path[0] + "/RFIDIOt"

AUTH_BLOCK_4TH = 'FF8600000501000460'
AUTH_BLOCK = 'FF860000050100'
AUTH_KEY_NUMBER = '00'
AUTH_FAILED = '6300'
READ_BLOCK_4TH_16_BYTES = 'FFB0000410'
READ_BLOCK = 'FFB000'
WRITE_BLOCK = 'FFD600'
MIFARE_1K_AUTHKEY= '6000'
_16_BYTES = '10'
BLOCK_NO = (6,8,9,11,12)

def get_user(db, card):
    pass

def handle_websocket(ws):
    index = 1
    while True:
        message = ws.receive()
        if message is None:
            break
        else:
            d = {}
            try:
                d = ast.literal_eval(message)
            except Exception as E:
                # d has no value
                message = lazy_gettext('Error: D has no value')
                logging.error('%s %s' %(traceback.print_exc(), message))
                d = {'mode' : 'default'}

            str_reply = ''

            try:
                if 'check_uid' == d['mode'] :
                    res_call = subprocess.Popen(
                                    ["python",
                                    PATH_RFIDIOT + "/card_read_uid.py",
                                    " -uid "],
                                    stdout=subprocess.PIPE)
                    out, error = res_call.communicate()
                    str_reply = split_rule.split(out)[1]
                    if out == '':
                        str_reply = {'output' : 'Card holder: ', \
                            'data' : 100000 , \
                            'pict' : 'B004.png', }
                        ws.send(json.dumps(str_reply))
                    else:
                        str_reply = split_rule.split(out)[1]
                        str_reply = { \
                            'output' : 'Card holder: ', \
                            'data' : 100000 , \
                            'pict' : 'B004.png', \
                        }
                        ws.send(json.dumps(str_reply))
                elif 'get_card_id' == d['mode'] :
                    res_call = subprocess.Popen(
                                    ["python",
                                    PATH_RFIDIOT + "/card_read_id.py",
                                    " --uid"],
                                    stdout=subprocess.PIPE)
                    out, error = res_call.communicate()
                    if out == '':
                        str_reply = {'output' : 'XXXX'}
                        ws.send(json.dumps(str_reply))
                    else:
                        str_reply = split_rule.split(out)[1].rstrip("\n").rstrip("\r")
                        if error_pattern.match(str_reply) :
                            str_reply = {'output' : str_reply}
                        else:
                            str_reply = {'card' : str_reply}
                        ws.send(json.dumps(str_reply))
                elif 'sell' == d['mode'] :
                    ws.send(json.dumps({'output': 'Sell'}))
                elif 'top_up' == d['mode'] :
                    ws.send(json.dumps({'output': 'Top Up'}))
                elif 'new' == d['mode'] :
                    ws.send(json.dumps({'output': 'New'}))
                elif 'renew' == d['mode'] :
                    ws.send(json.dumps({'output': 'Renew'}))
                elif 'default' == d['mode'] :
                    pass # do nothing
                elif 'init' == d['mode']:
                    ws.send(json.dumps({"output" : "%s , System is up" %(datetime.datetime.now())}))
                else:
                    ws.send(json.dumps({'output': 'Error: Unknown Mode'}))
            except Exception as E:
                str_reply = json.dumps({'output': 'Error: App is not ready'})
                ws.send(str_reply)
                logging.error('%s %s %s' %(traceback.print_exc(), E, str_reply))
