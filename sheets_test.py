import pygsheets

from pprint import pprint

credentials = "C:\\Users\\Wilhelm\\PycharmProjects\\arbitrage\\config\\service_creds.json"


def auth_sheets():
    return pygsheets.authorize(outh_file=credentials, no_cache=True)

gc = auth_sheets()
doc = gc.open_by_key("1N1MDj7mXLbv_-LUj1peug53P9a2gh5jdD5BnPrOQVLU")
ex_sheet = doc.worksheet_by_title("Exchanges")

pprint(ex_sheet)