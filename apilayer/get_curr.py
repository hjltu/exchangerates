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
        #table = curr.prepare_data(timeseries)
        #data = crypto.print_table(table)
        #crypto.add_to_db(data)
        try:
            time.sleep(LOOP_PAUSE)
        except KeyboardInterrupt:
            print(f'{Style.RESET}Interrupted')
            sys.exit(0)

def test_main():
    curr = Currency()
    print(json.dumps(TEST_TIMESERIES, indent=4))
    table = curr.prepare_data(TEST_TIMESERIES)


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


    def get_current(self, symbols=SYMBOLS):

        """
            Input: symbols='' for all symbols
        """

        params = {'base': BASE_SYMBOL, 'symbols': symbols}
        url = BASE_URL + 'latest'

        return self.get_request(url, params)


    def get_timeseries(self, days=33):
        """
        url = "api.apilayer.com/exchangerates_data/timeseries?start_date=2022-06-10&end_date=2022-06-28&base=RUB&symbols=EUR,GBP"
        headers = {apikey: }
        response = 

        Output:
        """

        # params
        today = date.today().strftime("%Y-%m-%d")
        past = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        params = {'start_date': past, 'end_date': today, 'base': BASE_SYMBOL, 'symbols': SYMBOLS}
        url = BASE_URL + 'timeseries'

        res = self.get_request(url, params)

        if res.get('success') == True:
            return res


    def prepare_data(self, timeseries):

        """
        Output:
        """

        table = []

        for rates in timeseries.get('rates').values():
            print(rates)
        return
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
                    o = float(data[len(data)-day].get('open'))
                    c = float(data[len(data)-1].get('close'))

                    proc = int((c-o)/(o/100))
                    diff = int((h-l)/(o/100))
                    period = {per: {'l': l, 'h': h, 'o': o, 'c': c, 'p': proc, 'd': diff}}
                    table[len(table)-1].update(period)
            else:
                table.append({'curr': curr.get('curr'), 'err': 'keine Daten'})

        #print(json.dumps(table, indent=4))
        return table


    def print_table(self, table):

        """
        Output:
            {'name': 'LTC', 'price': 62.16, 'BTC': 3, 'ETH': 0, 'LTC': 0}
        """
        curr_time = time.strftime("%d%b%y_%H:%M")
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


    def my_dist(self, x, y):
        if x < y:
            return max(x-y, y-x)
        if x > y:
            return min(x-y, y-x)
        else:
            return 0


    def add_to_db(self, data):

        curr_time = time.strftime("%d%b%y_%H:%M")
        val = self.db.add_to_db(curr_time, data)

        return val if val else None


if __name__ == "__main__":
    main()
