"""
date: 18apr22, author: hjltu, license: MIT
https://docs.coincap.io/
currency:
    https://www.tradingview.com/symbols/TRXUSD/
transacrions history:
    https://blockchair.com
install:
   sudo apt install python3-venv python3-pip
   python3 -m venv venv
   venv/bin/pip install --upgrade pip
   venv/bin/pip install requests tabulate pytest
run:
   venv/bin/pytest -s get_crypto_curr.py
   venv/bin/pytest -rfP get_crypto_curr.py
   venv/bin/python get_crypto_curr.py
"""


import sys
import json
import time
import requests
from tabulate import tabulate
from datetime import datetime, timedelta
from config import *
sys.path.append("..")
from data.exchanges_db import DB


MSG_ERR = f'{Style.LIGHT_RED}ERR: ' + 'code: {}, msg: {}' + f'{Style.RESET}'


def main():

    crypto = Crypto(SYMBOLS, BASE_SYMBOL, CRYPTO_DATABASE)
    while True:
        candles = crypto.get_candles()
        if candles:
            curr_time = time.strftime("%d%b%y_%H:%M")
            table = crypto.prepare_data(candles)
            data = crypto.print_table(table, SYMBOLS)
            crypto.add_to_db(curr_time, data)
        try:
            time.sleep(LOOP_PAUSE)
        except KeyboardInterrupt:
            print(f'{Style.RESET}Interrupted')
            sys.exit(0)


def test_main():
    crypto = Crypto(TEST_SYMBOLS, BASE_SYMBOL, TEST_DATABASE)
    date = datetime.fromtimestamp(TEST_CANDLES[0].get('timestamp')//1000).strftime("%d%b%y_%H:%M")
    assert crypto.prepare_data(TEST_CANDLES) == TEST_TABLE
    assert crypto.print_table(TEST_TABLE, TEST_SYMBOLS) == TEST_DATA
    assert crypto.add_to_db(date, TEST_DATA) == TEST_DATA


class Crypto(object):

    def __init__(self, symbols, base, db_name):
        self.symbols = symbols
        self.base = base
        self.db = DB(db_name)


    def get_candles(self):
        """
        url = "api.coincap.io/v2/candles?exchange=poloniex&interval=h8&baseId=ethereum&quoteId=bitcoin
        """

        candles = []
        # params
        today = int(datetime.now().timestamp() * 1000)
        diff = datetime.now() - timedelta(days=PERIOD_DAYS)
        past = int(diff.timestamp() * 1000)
        params = {'interval': CANDLE_INTERVAL, 'quoteId': self.base, 'start': past, 'end': today}

        for curr in self.symbols:
            params.update({'exchange': curr.get('exchange'), 'baseId': curr.get('id')})
            try:
                res = requests.get(API_URL, headers={}, data={}, params=params)
                code, response = res.status_code, json.loads(res.text)
                if code == 200:
                    response.update({'curr': curr.get('symbol')})
                    candles.append(response)
            except Exception as e:
                pass

        #print(json.dumps(candles, indent=4))
        return candles


    def prepare_data(self, candles):

        """
        """

        table = []

        for curr in candles:
            data = curr.get('data')
            periods = {'all': len(data), 'quart': 90, 'month': 30, 'week': 7}
            table.append({'curr': curr.get('curr')})

            if data:
                timestamp_min = data[0].get('period')/1000
                timestamp_max = data[len(data)-1].get('period')/1000
                date_from = datetime.fromtimestamp(timestamp_min).strftime('%d%b%y')
                date_to = datetime.fromtimestamp(timestamp_max).strftime('%d%b%y')
                table[len(table)-1].update({'curr': curr.get('curr'), 'from': date_from, 'to': date_to, 'num': len(data)})

                for per, day in periods.items():
                    l = min([float(l.get('low')) for l in data[len(data)-day:]])
                    h = max([float(m.get('high')) for m in data[len(data)-day:]])
                    o = float(data[len(data)-day].get('open')) if len(data) > day else float(data[0].get('open'))
                    c = float(data[len(data)-1].get('close'))

                    proc = int((c-o)/(o/100))
                    diff = int((h-l)/(o/100))
                    period = {per: {'l': l, 'h': h, 'o': o, 'c': c, 'p': proc, 'd': diff}}
                    table[len(table)-1].update(period)
            else:
                table.append({'curr': curr.get('curr'), 'err': 'keine Daten'})

        #print(json.dumps(table, indent=4))
        return table


    def print_table(self, table, symbols):

        """
        """
        curr_time = time.strftime("%d%b%y_%H:%M")
        currency_table=[]
        output_list = []
        color = Style.YELLOW
        cross = [c.get('symbol') for c in symbols]
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
                'name': curr.get('curr'), 'price': curr.get('all').get('c'),
                'shift': curr.get('week').get('p'), 'diff': curr.get('week').get('d')}
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


    def my_dist(self, x, y):
        if x < y:
            return max(x-y, y-x)
        if x > y:
            return min(x-y, y-x)
        else:
            return 0


    def add_to_db(self, date, data):

        val = self.db.write(date, data)

        return val if val else None


if __name__ == "__main__":
    main()
