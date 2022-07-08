#!/usr/bin/env pyton3

"""
28jun22 hjltu
config for get_curr
"""


BASE_URL = "https://api.exchangerate.host"
BASE_SYMBOL = "USD"
LOOP_PAUSE = 9999
PERIOD_DAYS = 33
CURR_DATABASE='../data/curr.db'
PLOT = '../plots/curr.png'
SYMBOLS = [ 'BTC','RUB','EUR','GBP','JPY','CHF','CNY','HKD','TRY','KZT','BYN','AMD' ]

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

########## TEST ##########

TEST_DATABASE='../data/test_curr.db'
TEST_PLOT = '../plots/test_curr.png'
TEST_SYMBOLS = [ 'USD', 'EUR', 'GBP' ]
TEST_BASE_SYMBOL = "RUB"

TEST_TIMESERIES = {
'success': True, 'timeseries': True, 'start_date': '2022-06-29', 'end_date': '2022-07-02', 'base': 'RUB',
'rates': {
'2022-06-29': {
'USD': 0.019048, 'EUR': 0.018234, 'GBP': 0.015703},
'2022-06-30': {
'USD': 0.018223, 'EUR': 0.017393, 'GBP': 0.014986},
'2022-07-01': {
'USD': 0.017604, 'EUR': 0.016884, 'GBP': 0.014551},
'2022-07-02': {
'USD': 0.017604, 'EUR': 0.016884, 'GBP': 0.014551}}}

TEST_TABLE = [
{'name': 'USD', 'shift': 8, 'diff': 8, 'h': 56.8052715291979, 'l': 52.49895002099958, 'o': 52.49895002099958, 'c': 56.8052715291979},
{'name': 'EUR', 'shift': 7, 'diff': 7, 'h': 59.227671167969675, 'l': 54.842601733026214, 'o': 54.842601733026214, 'c': 59.227671167969675},
{'name': 'GBP', 'shift': 7, 'diff': 7, 'h': 68.72379905161158, 'l': 63.68209896198178, 'o': 63.68209896198178, 'c': 68.72379905161158}]

TEST_DATA = [
{'name': 'USD', 'shift': 8, 'diff': 8, 'price': 56.8052715291979},
{'name': 'EUR', 'shift': 7, 'diff': 7, 'price': 59.227671167969675},
{'name': 'GBP', 'shift': 7, 'diff': 7, 'price': 68.72379905161158}]

TEST_DATA_FROM_DB = [
('02Jul22', [
{'name': 'USD', 'shift': 8, 'diff': 8, 'price': 56.8052715291979},
{'name': 'EUR', 'shift': 7, 'diff': 7, 'price': 59.227671167969675},
{'name': 'GBP', 'shift': 7, 'diff': 7, 'price': 68.72379905161158}])]

TEST_DB_DATA = [
('03Jul21_03:04', [
{'name': 'USD', 'shift': -8, 'diff': 8, 'price': 56.8052715291979},
{'name': 'EUR', 'shift': 7, 'diff': 7, 'price': 59.227671167969675},
{'name': 'GBP', 'shift': 7, 'diff': 7, 'price': 68.72379905161158}]),
('02Jul22_04:03', [
{'name': 'USD', 'shift': 8, 'diff': 8, 'price': 56.8052715291979},
{'name': 'EUR', 'shift': -7, 'diff': 7, 'price': 59.227671167969675},
{'name': 'GBP', 'shift': 7, 'diff': 7, 'price': 68.72379905161158}])]

TEST_TABLE_TO_DRAW = [
{'name': 'USD', 'time': ['03Jul21_03:04', '02Jul22_04:03'], 'shift': [-8, 8]},
{'name': 'EUR', 'time': ['03Jul21_03:04', '02Jul22_04:03'], 'shift': [7, -7]},
{'name': 'GBP', 'time': ['03Jul21_03:04', '02Jul22_04:03'], 'shift': [7, 7]}]
