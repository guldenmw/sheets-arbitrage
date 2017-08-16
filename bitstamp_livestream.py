import pprint
import time
import json
import pusherclient


def callback(temp):
    info = json.loads(temp)
    pprint.pprint(info)


def connect_handler(data):
    pprint.pprint(data)
    channel = pusher.subscribe('live_trades')
    channel.bind('trade', callback)


appkey = 'de504dc5763aeef9ff52'
pusher = pusherclient.Pusher(appkey)
pusher.connection.bind('pusher:connection_established', connect_handler)
pusher.connect()

while True:
    time.sleep(1)
