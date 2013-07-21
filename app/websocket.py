import json
import app
import re
import ast
import subprocess
import datetime
from gevent import sleep

error_pattern = re.compile('::Error')

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
        print '%s %s' %(message, type(message))
        if message is None:
            break
        else:
            d = {}
            try:
                d = ast.literal_eval(message)
            except Exception as E:
                # d has no value
                print 'Error: D has no value'
                d = {'mode' : 'default'}
            print d
            try:
                if 'check_uid' == d['mode'] :
                    res_call = subprocess.Popen(
                                    ["python",
                                    "/opt/flask/flask-websocket/app/RFIDIOt/card_read_uid.py",
                                    " -uid "],
                                    stdout=subprocess.PIPE)
                    out, error = res_call.communicate()
                    if out == '':
                        result = {'output' : 'Card holder: ', \
                            'data' : 100000 , \
                            'pict' : 'B004.png', }
                        #ws.send(json.dumps({'output': 'Error: Reader is not READY'}))
                        ws.send(json.dumps(result))
                    else:
                        result = { \
                            'output' : 'Card holder: ', \
                            'data' : 100000 , \
                            'pict' : 'B004.png', \
                        }
                        ws.send(json.dumps(result))
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
                print E
                ws.send(json.dumps({'output': 'Error: App is not ready'}))
            #try:
            #    card = rfidiot.card
            #    r = card.pcsc_send_apdu('%s%s' %( AUTH_BLOCK_4TH, AUTH_KEY_NUMBER ) )
            #    if  card.errorcode == AUTH_FAILED  :
            #        ws.send(json.dumps({'output': 'Error: Card Auth Failed'}))
            #        break
            #    else:
            #        pass # Continue
            #    r = card.pcsc_send_apdu('%s' %( READ_BLOCK_4TH_16_BYTES ) )
            #    if  card.errorcode == AUTH_FAILED  :
            #        ws.send(json.dumps({'output': 'Error: Card Read Failed'}))
            #        break
            #    else:
            #        pass # Continue
            #    username = card.data
            #    user = app.db.session.query(app.User). \
            #                filter( app.User.username == username )
            #    if user.count() > 1 :
            #        ws.send(json.dumps({'output': 'Error: Card ID duplicate'}))
            #        break
            #    elif user.count() == 1 :
            #        pass # continue
            #    else:
            #        ws.send(json.dumps({'output': 'Error: Card ID not registered or bad read'}))
            #        break
            #    # read the last_auth
            #    max_cardstate = app.db.session.query(app.func.max(app.CardState.id)). \
            #                        filter(app.CardState.user_id == user[0].id). \
            #                        subquery()
            #    cardstate = app.db.session.query(app.CardState). \
            #                    filter(app.CardState.id == max_cardstate ). \
            #                    first()
            #    if cardstate.no not in BLOCK_NO:
            #        ws.send(json.dumps({'output': 'Error: Card ID sequence number is null or damaged'}))
            #        break
            #    r = card.pcsc_send_apdu('%s%02d%s' %( AUTH_BLOCK, cardstate.block_no, MIFARE_1K_AUTHKEY ) )
            #    if card.data == AUTH_FAILED:
            #        ws.send(json.dumps({'output': 'Error: Balance Auth Failed'}))
            #        break
            #    else:
            #        pass # continue
            #    r = card.pcsc_send_apdu('%s%02d%s' %( READ_BLOCK, cardstate.block_no, _16_BYTES ) )
            #    last_auth = card.data
            #    if last_auth != cardstate.last_auth :
            #        ws.send(json.dumps({'output': 'Error: Inconsistent AuthKey'}))
            #        break
            #    else:
            #        pass # continue
            #    # read and return the remaining
            #    balance = app.db.session.query(app.Balance). \
            #                    filter(app.Balance.card_state_id == cardstate.id ). \
            #                    first()
            #    try:
            #        ws.send(json.dumps({'output': 'Balance: %s' %(balance.remain), 'balance' : balance.remain }))
            #    except:
            #        ws.send(json.dumps({'output': 'Error: Inconsistent balance '}))
            #except Exception as E:
            #    ws.send(json.dumps({'output': 'Error: Card is NOT ready'}))
            #    print E
            #message = json.loads(message)
            #index += 1
