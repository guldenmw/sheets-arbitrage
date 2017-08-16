import os
import json
import bitstamp.bitstamp
import luno
from pprint import pprint

bs_config = "%s%s%s%s%s" % (os.path.abspath(os.path.dirname(__file__)), os.sep, "config", os.sep, "bs_creds.json")

bs = bitstamp.bitstamp.Bitstamp(bs_config)

luno = luno.classes.Stream(path_to_creds="config/luno.json")

luno.

# print(bs.ticker())
pprint(bs.balance())
