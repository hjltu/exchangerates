#!/usr/bin/env pyton3

"""
28jun22 hjltu
config for get_curr
"""


API_KEY = 'apilayer key'
BASE_URL = "https://api.apilayer.com/exchangerates_data/"
BASE_SYMBOL = "RUB"
LOOP_PAUSE = 9999
CURR_DATABASE='../data/test_curr.db'

SYMBOLS = [ 'USD', 'EUR', 'GBP', 'JPY' ]

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
    'success': True,
    'timeseries': True,
    'start_date': '2022-06-28',
    'end_date': '2022-07-01',
    'base': 'RUB',
    'rates': {
        '2022-06-28': {'USD': 0.018605, 'EUR': 0.01768, 'GBP': 0.015263, 'JPY': 2.531148},
        '2022-06-29': {'USD': 0.019048, 'EUR': 0.018234, 'GBP': 0.015703, 'JPY': 2.601704},
        '2022-06-30': {'USD': 0.018519, 'EUR': 0.017677, 'GBP': 0.015209, 'JPY': 2.510319},
        '2022-07-01': {'USD': 0.018519, 'EUR': 0.017677, 'GBP': 0.015209, 'JPY': 2.510319}}}

