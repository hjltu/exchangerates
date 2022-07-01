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
   venv/bin/python get_curr.py
   venv/bin/python draw.py curr.db
"""


import os
import sys
import json
import time
print (os.getcwd())
import requests
from datetime import date, datetime, timedelta
from config import *

sys.path.append("..")
from data.exchanges_db import DB



MSG_ERR = f'{Style.LIGHT_RED}ERR: ' + 'code: {}, msg: {}' + f'{Style.RESET}'

def main():

    curr = Currency()
    while True:
        #symbols = curr.get_symbols()
        #prices = curr.get_current()
        timeseries = curr.get_timeseries()
        if timeseries:
            table = curr.prepare_data(timeseries)
            data = curr.print_table(table)
            #curr.add_to_db(data)
        try:
            time.sleep(LOOP_PAUSE)
        except KeyboardInterrupt:
            print(f'{Style.RESET}Interrupted')
            sys.exit(0)


def test_main():
    curr = Currency()
    #print('timeseries:', json.dumps(TEST_TIMESERIES, indent=4))
    assert curr.prepare_data(TEST_TIMESERIES) == TEST_TABLE
    data = curr.print_table(TEST_TABLE)


class Currency(object):

    def __init__(self):
        self.db = DB(CURR_DATABASE)


    def get_request(self, url, params):

        headers = {'apikey': API_KEY}

        try:
            res = requests.get(url, headers=headers, params=params)
            code, response = res.status_code, json.loads(res.text)
            #print(code, response)
        except Exception as e:
            print(MSG_ERR.format(code, e))

        if code == 200:
            return response

        print(MSG_ERR.format(code, response))


    def get_symbols(self):

        params = {}
        url = BASE_URL + 'symbols'

        return self.get_request(url, params)


    def get_current(self):

        """
            Input: symbols='' for all symbols
        """

        symbols = ''.join(SYMBOLS)
        params = {'base': BASE_SYMBOL, 'symbols': symbols}
        url = BASE_URL + 'latest'

        return self.get_request(url, params)


    def get_timeseries(self):
        """
        url = "api.apilayer.com/exchangerates_data/timeseries?start_date=2022-06-10&end_date=2022-06-28&base=RUB&symbols=EUR,GBP"
        headers = {apikey: }

        Output: config.TEST_TIMESERIES
        """

        # params
        today = date.today().strftime("%Y-%m-%d")
        past = (datetime.now() - timedelta(days=PERIOD_DAYS)).strftime("%Y-%m-%d")
        symbols = ','.join(SYMBOLS)
        params = {'start_date': past, 'end_date': today, 'base': BASE_SYMBOL, 'symbols': symbols}
        url = BASE_URL + 'timeseries'

        res = self.get_request(url, params)

        if res.get('success') == True:
            return res


    def prepare_data(self, timeseries: dict) -> list:

        """
            Output: config.TEST_TABLE
        """

        #print('timeseries:\n', timeseries)
        start_date = time.strftime("%d%b%y", time.strptime(timeseries.get('start_date'),'%Y-%m-%d'))
        end_date = time.strftime("%d%b%y", time.strptime(timeseries.get('end_date'),'%Y-%m-%d'))
        print(start_date, end_date)

        candles = self.get_candles(timeseries)
        #print('candles:\n', candles)

        table = self.get_table(candles)
        #print('table:\n', table)

        return table


    def get_table(self, candles: dict) -> list:

        table = []
        get_shift = lambda c, o: int((c-o)/(o/100))
        get_diff = lambda h, l, o: int((h-l)/(o/100))

        for name, candle in candles.items():

            shift = get_shift(candle.get('c'), candle.get('o'))
            diff = get_diff(candle.get('h'), candle.get('l'), candle.get('o'))
            curr = {'name': name, 'shift': shift, 'diff': diff, **candle}
            table.append(curr)

        return table


    def get_candles(self, timeseries: dict) -> dict:

        candles = {s: {'h': 0, 'l': 0, 'o': 0, 'c': 0} for s in SYMBOLS}

        for symbol in SYMBOLS:
            for date, rates in timeseries.get('rates').items():

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

        curr_time = time.strftime("%d%b%y_%H:%M")
        curr_data = time.strftime("%d%b%y")
        color = Style.YELLOW
        count = 0
        msg = ''

        line = f'ticker\tprice\tperiod\t{BASE_SYMBOL}\tticker\tprice\tperiod\t{curr_data}\tticker\tprice\tperiod'
        print(f'{Style.BOLD}{line}{Style.RESET}')

        for curr in table:

            name = curr.get('name')
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

        #line = line + f'{Style.RESET}'
        print(f'{Style.RESET}')
        return
        currency_table=[]
        output_list = []
        color = Style.YELLOW
        cross = [c[2] for c in CURR]
        line = Style.BOLD + 'name\t ' + '\t '.join(cross) + Style.RESET
        currency_table.append(line.split(sep='\t'))
        #print(NOTES, line)

        for per in ('all', 'quart', 'month', 'week'):
            line = f"{color}{per}"

            for curr in table:
                if curr.get('err'):
                    line += f"\t{curr.get('err')}"
                else:
                    proc = self.set_color(curr.get(per).get('p'), -25, 25, color, Style.LIGHT_BLUE, Style.LIGHT_GREEN)
                    diff = self.set_color(curr.get(per).get('d'), 40, 60, color, Style.BOLD, Style.LIGHT_RED)
                    line += f"\t{proc}%{diff}"

            #print(line + f'{Style.RESET}')
            currency_table.append(line.split(sep='\t'))
            color = Style.YELLOW if color is Style.WHITE else Style.WHITE

        line_close = '$price'
        for curr in table:
            line_close += f"\t{curr.get('all').get('c')}"[:7]
            output_data = {
                'name': curr.get('curr'), 'time': curr_time, 'price': curr.get('all').get('c'),
                'proc_week': curr.get('week').get('p')}
            line = f"{color}{curr.get('curr')}{curr.get('num')}"

            if curr.get('err'):
                line += f"\t{curr.get('err')}"
            else:
                for cross in table:
                    dist_a = self.my_dist(curr.get('all').get('p'), cross.get('all').get('p'))
                    dist_q = self.my_dist(curr.get('quart').get('p'), cross.get('quart').get('p'))
                    dist_m = self.my_dist(curr.get('month').get('p'), cross.get('month').get('p'))
                    dist_w = self.my_dist(curr.get('week').get('p'), cross.get('week').get('p'))
                    dist = int((dist_a+dist_q+dist_m+dist_w)/4)
                    output_data.update({cross.get('curr'): dist_w})
                    if dist == 0 and dist_w == 0:
                        line += f"\t{Style.RESET}{Style.BOLD}{curr.get('curr')}{Style.RESET}{color}"
                    else:
                        dist = self.set_color(dist, -33, 33, color, Style.LIGHT_BLUE, Style.LIGHT_GREEN)
                        dist_w = self.set_color(dist_w, -33, 33, color, Style.LIGHT_BLUE, Style.LIGHT_GREEN)
                        line += f"\t{dist}%{dist_w}"
            line = line + f'{Style.RESET}'
            currency_table.append(line.split(sep='\t'))
            output_list.append(output_data)

            #print(line)
            color = Style.YELLOW if color is Style.WHITE else Style.WHITE

        currency_table.append(line_close.split(sep='\t'))
        #print(line_close)
        print(tabulate(currency_table))

        return output_list


    def set_color(self, val, diff_min, diff_max, color, color_min, color_max):

        if val > diff_max:
            return f'{Style.BOLD}{color_max}{val}{Style.RESET}{color}'

        if diff_min < 0 and val < diff_min:
            return f'{Style.BOLD}{color_min}{val}{Style.RESET}{color}'
        if diff_min > 0 and val > diff_min:
            return f'{Style.RESET}{Style.BOLD}{val}{Style.RESET}{color}'

        return f'{val}'


    def add_to_db(self, data):

        curr_time = time.strftime("%d%b%y_%H:%M")
        val = self.db.add_to_db(curr_time, data)

        return val if val else None


if __name__ == "__main__":
    main()
