import sys
import luno
import json
import pygsheets
import pusherclient
import sys

from pprint import pprint
from pygsheets.exceptions import RequestError
from googleapiclient.errors import HttpError

if sys.platform == "win32":
    credentials = "C:\\Users\\Wilhelm\\PycharmProjects\\arbitrage\\config\\service_creds.json"
else:
    credentials = "/home/guldenmw/PycharmProjects/arbitrage/config/service_creds.json"

sys.path.remove("/sunrise/projects/scripts/repository/release/modules")


class Arbitrage(object):
    def __init__(self):
        # Create your old_ticker variables for storing the previous ticker values.
        self.luno_old_ticker = None
        self.luno_new_ticker = None

        self.bitstamp_old_ticker = None
        self.bitstamp_new_ticker = None

        self.simple_gap = None

        self.gc = None
        self.lw = None
        self.pusher = None

    def callback(self, temp):
        # Callback function for Bitstamp pusher connection
        info = json.loads(temp)
        self.bitstamp_new_ticker = info['price']

    def connect_handler(self, data):
        # Function to handle Bitstamp websocket connection
        pprint(data)
        channel = self.pusher.subscribe('live_trades')
        channel.bind('trade', self.callback)

    def start(self):
        # Connect to Bitstamp websocket via pusher.
        appkey = 'de504dc5763aeef9ff52'
        self.pusher = pusherclient.Pusher(appkey)
        self.pusher.connection.bind('pusher:connection_established', self.connect_handler)
        self.pusher.connect()

        # Instantiate streaming object.
        self.lw = luno.classes.Stream()

        # Start the connection.
        self.lw.start()

        self.run()

    # def calculate_gap(self):

    def run(self):
        while True:
            # Get the latest ticker
            self.luno_new_ticker = self.lw.ticker()

            # If you only want to see changes in price, compare the new value to the previous value.
            if self.luno_new_ticker == self.luno_old_ticker and self.bitstamp_new_ticker == self.bitstamp_old_ticker:
                continue

            print("Luno: R%s" % self.luno_new_ticker)
            print("Bitstamp: $%s" % self.bitstamp_new_ticker)
            print("\n")
            print("-"*30)
            # if self.luno_new_ticker and self.bitstamp_new_ticker:
            #     self.simple_gap = ((self.luno_new_ticker-self.bitstamp_new_ticker)/self.bitstamp_new_ticker)
            #     print("{}%".format(round(self.simple_gap), 6))

            try:
                self.update_spreadsheet()

            except (RequestError, TypeError, HttpError):
                pass

            # Set your previous value at the end of the loop.
            self.luno_old_ticker = self.luno_new_ticker
            self.bitstamp_old_ticker = self.bitstamp_new_ticker

    def update_spreadsheet(self):
        luno_cell = "E4"
        bitstamp_cell = "D5"

        if not self.gc:
            self.gc = self.auth_sheets()

        doc = self.gc.open_by_key("1N1MDj7mXLbv_-LUj1peug53P9a2gh5jdD5BnPrOQVLU")
        pub_doc = self.gc.open_by_key("1ixwK7eoY2Txz490NtiKLCfbbaBX_Fu70oFi1ESkHFgQ")

        ex_sheet = doc.worksheet_by_title("Exchanges")
        pub_ex_sheet = pub_doc.worksheet_by_title("Exchanges")

        ex_sheet.update_cell(luno_cell, self.luno_new_ticker)
        ex_sheet.update_cell(bitstamp_cell, self.bitstamp_new_ticker)

        pub_ex_sheet.update_cell(luno_cell, self.luno_new_ticker)
        pub_ex_sheet.update_cell(bitstamp_cell, self.bitstamp_new_ticker)

        return True

    @staticmethod
    def auth_sheets():
        return pygsheets.authorize(service_file=credentials, no_cache=True)


class ArbitrageTable(object):
    def __init__(self):
        self.sheet_name = "ArbitrageTable"

    def get_sheet_name(self):
        return self.sheet_name



# if __name__ == '__main__':
new = Arbitrage()

new.start()

# new.run()
