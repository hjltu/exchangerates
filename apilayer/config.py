#!/usr/bin/env pyton3

"""
28jun22 hjltu
config for get_curr
"""


API_KEY = 'apilayer key'
BASE_URL = "https://api.apilayer.com/exchangerates_data/"
BASE_SYMBOL = "RUB"
LOOP_PAUSE = 9999
PERIOD_DAYS = 22
CURR_DATABASE='../data/test_curr.db'

SYMBOLS = [ 'USD', 'EUR', 'GBP', 'JPY', 'CNY', 'HKD', 'TRY', 'KZT', 'BYN' ]

NOTES = """
"""

class Style():
    BOLD = '\033[1m'
    ORANGE = '\033[33m'
    LIGHT_RED = '\033[91m'
    LIGHT_GREEN = '\033[92m'
    LIGHT_BLUE = '\033[94m'
    YELLOW = '\033[33m'
    WHITE = '\033[37m'
    SELECT = '\033[7m'
    RESET = '\033[0m'


TEST_TIMESERIES = {
'success': True, 'timeseries': True, 'start_date': '2022-06-29', 'end_date': '2022-07-02', 'base': 'RUB',
'rates': {
'2022-06-29': {
'USD': 0.019048, 'EUR': 0.018234, 'GBP': 0.015703, 'JPY': 2.601704, 'CNY': 0.127634, 'HKD': 0.14945, 'TRY': 0.316822, 'KZT': 8.913745, 'BYN': 0.064278},
'2022-06-30': {
'USD': 0.018223, 'EUR': 0.017393, 'GBP': 0.014986, 'JPY': 2.474523, 'CNY': 0.122081, 'HKD': 0.143004, 'TRY': 0.304271, 'KZT': 8.569494, 'BYN': 0.061519},
'2022-07-01': {
'USD': 0.017604, 'EUR': 0.016884, 'GBP': 0.014551, 'JPY': 2.379731, 'CNY': 0.117968, 'HKD': 0.138137, 'TRY': 0.295155, 'KZT': 8.172316, 'BYN': 0.059426},
'2022-07-02': {
'USD': 0.017604, 'EUR': 0.016884, 'GBP': 0.014551, 'JPY': 2.379731, 'CNY': 0.117968, 'HKD': 0.138137, 'TRY': 0.295155, 'KZT': 8.172316, 'BYN': 0.059426}}}

TEST_TABLE = [
{'name': 'USD', 'shift': -7, 'diff': 7, 'h': 0.019048, 'l': 0.017604, 'o': 0.019048, 'c': 0.017604},
{'name': 'EUR', 'shift': -7, 'diff': 7, 'h': 0.018234, 'l': 0.016884, 'o': 0.018234, 'c': 0.016884},
{'name': 'GBP', 'shift': -7, 'diff': 7, 'h': 0.015703, 'l': 0.014551, 'o': 0.015703, 'c': 0.014551},
{'name': 'JPY', 'shift': -8, 'diff': 8, 'h': 2.601704, 'l': 2.379731, 'o': 2.601704, 'c': 2.379731},
{'name': 'CNY', 'shift': -7, 'diff': 7, 'h': 0.127634, 'l': 0.117968, 'o': 0.127634, 'c': 0.117968},
{'name': 'HKD', 'shift': -7, 'diff': 7, 'h': 0.14945, 'l': 0.138137, 'o': 0.14945, 'c': 0.138137},
{'name': 'TRY', 'shift': -6, 'diff': 6, 'h': 0.316822, 'l': 0.295155, 'o': 0.316822, 'c': 0.295155},
{'name': 'KZT', 'shift': -8, 'diff': 8, 'h': 8.913745, 'l': 8.172316, 'o': 8.913745, 'c': 8.172316},
{'name': 'BYN', 'shift': -7, 'diff': 7, 'h': 0.064278, 'l': 0.059426, 'o': 0.064278, 'c': 0.059426}]
