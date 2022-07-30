"""
date: 18apr22, author: hjltu, license: MIT
https://apilayer.com/marketplace/exchangerates_data-api?preview=true#documentation-tab
install:
   sudo apt install python3-venv python3-pip
   python3 -m venv venv
   venv/bin/pip install --upgrade pip
   venv/bin/pip install requests pytest
run:
   venv/bin/pytest -s get_curr.py
   venv/bin/pytest -rfP get_curr.py
   venv/bin/python get_curr.py
   venv/bin/python draw.py curr.db
"""


import os
import sys
import json
import time
import requests
from datetime import date, datetime, timedelta
from config import *
sys.path.append("..")
from data.exchanges_db import DB


MSG_ERR = f'{Style.LIGHT_RED}ERR: ' + 'code: {}, msg: {}' + f'{Style.RESET}'


def main():

    curr = Currency(SYMBOLS, BASE_SYMBOL, CURR_DATABASE)
    while True:
        timeseries = curr.get_timeseries()
        if timeseries:
            curr_time = time.strftime("%d%b%y_%H:%M")
            table = curr.prepare_data(timeseries)
            data = curr.print_table(table)
            curr.add_to_db(curr_time, data)
        try:
            time.sleep(LOOP_PAUSE)
        except KeyboardInterrupt:
            print(f'{Style.RESET}Interrupted')
            sys.exit(0)


def test_main():
    curr = Currency(TEST_SYMBOLS, TEST_BASE_SYMBOL, TEST_DATABASE)
    date = time.strftime("%d%b%y", time.strptime(TEST_TIMESERIES.get('end_date'),'%Y-%m-%d'))
    assert curr.prepare_data(TEST_TIMESERIES) == TEST_TABLE
    assert curr.print_table(TEST_TABLE) == TEST_DATA
    assert curr.add_to_db(date, TEST_DATA) == TEST_DATA


class Currency(object):

    def __init__(self, symbols, base, db_name):
        self.symbols = symbols
        self.base = base
        self.db = DB(db_name)


    def get_request(self, url, params):

        headers = {}
        code, response = None, None

        try:
            res = requests.get(url, headers=headers, params=params)
            code, response = res.status_code, json.loads(res.text)
        except Exception as e:
            print(MSG_ERR.format(code, e))

        if code == 200:
            return response

        print(MSG_ERR.format(code, response))


    def get_symbols(self):

        params = {}
        url = BASE_URL + '/symbols'

        return self.get_request(url, params)


    def get_current(self):

        """
            Input: symbols='' for all symbols
        """

        symbols = ','.join(self.symbols)
        params = {'base': self.base, 'symbols': symbols}
        url = BASE_URL + '/latest'

        return self.get_request(url, params)


    def get_timeseries(self):
        """
        url = "api.exchangerates.host/timeseries?start_date=2022-06-10&end_date=2022-06-28&base=RUB&symbols=EUR,GBP"
        headers = {}

        Output: config.TEST_TIMESERIES
        """

        # params
        today = date.today().strftime("%Y-%m-%d")
        past = (datetime.now() - timedelta(days=PERIOD_DAYS)).strftime("%Y-%m-%d")
        symbols = ','.join(self.symbols)
        params = {'start_date': past, 'end_date': today, 'base': self.base, 'symbols': symbols}
        url = BASE_URL + '/timeseries'

        res = self.get_request(url, params)

        if isinstance(res, type(None)):
            return None

        if res.get('success') == True:
            return res


    def prepare_data(self, timeseries: dict) -> list:

        """
            Output: config.TEST_TABLE
        """

        start_date = time.strftime("%d%b%y", time.strptime(timeseries.get('start_date'),'%Y-%m-%d'))
        end_date = time.strftime("%d%b%y", time.strptime(timeseries.get('end_date'),'%Y-%m-%d'))
        print(start_date, end_date)

        candles = self.get_candles(timeseries)
        table = self.get_table(candles)

        return table


    def get_table(self, candles: dict) -> list:

        table = []
        get_shift = lambda c, o: int((c-o)/(o/100))
        get_diff = lambda h, l, o: int((l-h)/(o/100))

        for name, candle in candles.items():

            shift = get_shift(1/candle.get('c'), 1/candle.get('o'))
            diff = get_diff(1/candle.get('h'), 1/candle.get('l'), 1/candle.get('o'))
            curr = {'name': name, 'shift': shift, 'diff': diff, **candle}
            table.append(curr)

        return table


    def get_candles(self, timeseries: dict) -> dict:

        candles = {s: {'h': 0, 'l': 0, 'o': 0, 'c': 0} for s in self.symbols}

        for symbol in self.symbols:
            for date, rates in timeseries.get('rates').items():

                # convert price to base's values
                #if symbol == 'BTC':
                #    timeseries.get('rates').get(date).update({symbol: 1/rates.get(symbol)})

                if date == timeseries.get('end_date'):
                    candles.get(symbol).update({'c': rates.get(symbol)})

                if date == timeseries.get('start_date'):
                    candles.get(symbol).update({'o': rates.get(symbol)})

                if candles.get(symbol).get('l') == 0:
                    candles.get(symbol).update({'l': rates.get(symbol) })

                candles.get(symbol).update({'l': min(candles.get(symbol).get('l'), rates.get(symbol)) })
                candles.get(symbol).update({'h': max(candles.get(symbol).get('h'), rates.get(symbol)) })

        return candles


    def print_table(self, table: list):

        """
        Output:
        """

        curr_time = time.strftime("%H:%M")
        curr_data = time.strftime("%d-%b")
        color = Style.YELLOW
        count = 0
        msg = ''
        data = []

        line = f'ticker\tprice\tperiod\t{curr_data}\tticker\tprice\tperiod\t{curr_time}\tticker\tprice\tperiod'
        print(f'{Style.BOLD}{line}{Style.RESET}')

        for curr in table:

            name = curr.get('name')
            if name == 'BTC':
                price = str(1/curr.get('c'))[:6]
            else:
                price = str(curr.get('c'))[:6]
            shift = self.set_color(curr.get('shift'), -25, 25, color, Style.LIGHT_BLUE, Style.LIGHT_GREEN)
            diff = self.set_color(curr.get('diff'), 40, 60, color, Style.BOLD, Style.LIGHT_RED)
            msg = f'{name}\t{price}\t{shift}%{diff}'

            if count % 3 == 0:
                line = msg
            else:
                line += f'\t\t{msg}'

            if count % 3 == 2:
                print(f'{color}{line}{Style.RESET}')

            count += 1
            color = Style.YELLOW if color is Style.WHITE else Style.WHITE
            data.append({'name': name, 'shift': curr.get('shift'), 'diff': curr.get('diff'), 'price': curr.get('c')})

        print(f'{Style.RESET}')

        return data


    def set_color(self, val, diff_min, diff_max, color, color_min, color_max):

        if val > diff_max:
            return f'{Style.BOLD}{color_max}{val}{Style.RESET}{color}'

        if diff_min < 0 and val < diff_min:
            return f'{Style.BOLD}{color_min}{val}{Style.RESET}{color}'
        if diff_min > 0 and val > diff_min:
            return f'{Style.RESET}{Style.BOLD}{val}{Style.RESET}{color}'

        return f'{val}'


    def add_to_db(self, date, data):

        #curr_time = time.strftime("%d%b%y_%H:%M")
        val = self.db.write(date, data)

        return val if val else None


if __name__ == "__main__":
    main()
