#!/usr/bin/env python3

"""
python3 -m venv venv
source venv/bin/activate
git clone https://github.com/Awethon/open-api-python-client.git
cd open-api-python-client
python3 setup.py install

check_prices.py hjltu@ya.ru 11aug20
Usage:
    ./check_prices.py
    ./check_prices.py 1 day
    ./check_prices.py 7 week
    ./check_prices.py 14 week
    ./check_prices.py 30 month
"""

#import os
#os.environ['tabs'] = '4'

import os, sys
from time import sleep
from orders import Orders
from datetime import datetime, timedelta
from pytz import timezone
from config import TOKEN, TICKERS, DB, LOOP_INTERVAL, Style

#sys.exit()

# grouped tickers by abc in 3 columns
sp = int(len(TICKERS)/3)
T1=TICKERS[:sp]; T2=TICKERS[sp:sp*2]; T3=TICKERS[sp*2:]
TICKERS=[]
for i in range(len(T1)):
    TICKERS+=([T1[i]]+[T2[i]]+[T3[i]])


def my_client():
    client = Orders(db=DB, token=TOKEN, account_id='')
    stocks = client.get_market('stocks')
    stocks = client.get_instruments_by_tickers(TICKERS, stocks)
    return client, stocks


def get_price(candles_num=33, candles_period='day'):
    """
    {'week':
        {'figi': 'BBG000BNGBW9', 'ticker': 'NOK', 'isin': 'US6549022043',
        'minPriceIncrement': 0.01, 'lot': 1, 'currency': 'USD', 'name': 'Nokia', 'type': 'Stock',
        'candles': [
            {'o': 5.4, 'c': 5.35, 'h': 5.45, 'l': 5.35, 'v': 1552309,
                'time': '2022-04-08T04:00:00Z', 'interval': 'day', 'figi': 'BBG000BNGBW9'},
            {'o': 5.36, 'c': 5.29, 'h': 5.36, 'l': 5.28, 'v': 1790711,
                'time': '2022-04-11T04:00:00Z', 'interval': 'day', 'figi': 'BBG000BNGBW9'}]},
    'month':
        {'figi': 'BBG000BNGBW9', 'ticker': 'NOK', 'isin': 'US6549022043',
        'minPriceIncrement': 0.01, 'lot': 1, 'currency': 'USD', 'name': 'Nokia', 'type': 'Stock',
        'candles': [
            {'o': 5.4, 'c': 5.35, 'h': 5.45, 'l': 5.35, 'v': 1552309,
                'time': '2022-04-08T04:00:00Z', 'interval': 'day', 'figi': 'BBG000BNGBW9'},
            {'o': 5.36, 'c': 5.29, 'h': 5.36, 'l': 5.28, 'v': 1790711,
                'time': '2022-04-11T04:00:00Z', 'interval': 'day', 'figi': 'BBG000BNGBW9'}]}}
    """

    tickers={}
    try:
        #print(week[0])
        month = client.get_candles(stocks, candles_num, candles_period)
    except Exception as e:
        print('ERR: ',e)
    for ticker in TICKERS:
        try:
            candles = [m.get('candles') for m in month if m.get('ticker') == ticker][0]
            tickers.update({ticker: candles})
        except Exception as e:
            print('ERR: ',e)
            tickers.update({ticker: []})
    print('t',len(TICKERS), len(month),len(tickers))
    #sys.exit(0)
    return tickers


def print_table(tickers, diff):
    now=datetime.utcnow().strftime("%d%b%y")
    msg, line, count, amount = '', '', 0, 0

    time_beat = []

    color = Style.YELLOW
    print(Style.BOLD + f'name\tclose\tmonth\t\tname\tclose\tmonth\t\tname\tclose\tmonth\tsum' + Style.RESET)
    for ticker in tickers.keys():
        name = ticker
        month = tickers.get(ticker)

        try:
            month_open = month[0].get('o')
            month_close = month[len(month)-1].get('c')
            month_high = max(w.get('h') for w in month)
            month_low = min(w.get('l') for w in month)
            month_proc = int((month_close - month_open)/(month_open/100))
            month_diff = int((month_high - month_low)/(month_open/100))

            amount += month_close
            time_beat.append({'name': name, 'price': month_close, 'proc': month_proc, 'diff': month_diff})

            if month_proc < -diff:
                month_proc = f'{Style.LIGHT_BLUE}{month_proc}{Style.RESET}{color}'
            elif month_proc > diff:
                month_proc = f'{Style.LIGHT_GREEN}{month_proc}{Style.RESET}{color}'

            if month_diff > diff*4:
                month_diff = f'{Style.LIGHT_RED}{month_diff}{Style.RESET}{color}'
            elif month_diff > diff*2:
                month_diff = f'{Style.RESET}{Style.BOLD}{month_diff}{Style.RESET}{color}'

            line = f'{name}\t{month_close}\t{month_proc}%{month_diff}'

        except:
            time_beat.append({'name': name, 'price': None, 'proc': None, 'diff': None})
            line = f'{name}\t- keine Daten -'

        if count%3 == 0:
            msg = f'{line}'
        else:
            msg += f'\t\t{line}'

        if count%3 == 2:
            print(f'{color}{msg}{Style.RESET}{color}\t{amount:.0f}')
            color = Style.YELLOW if color is Style.WHITE else Style.WHITE

        count +=1

    print(f'{Style.RESET}', end = '')

    client._add_to_db(now, time_beat)


def main(diff=15):

    """
    Input:
        config file,
        diff for colors
    """

    while True:
        tickers = get_price()
        print_table(tickers, diff)
        try:
            sleep(LOOP_INTERVAL)
        except KeyboardInterrupt:
            print('Interrupted')
            sys.exit(0)


if __name__=="__main__":
    client, stocks = my_client()
    arg = sys.argv[1:]
    main(arg[0]) if len(arg) > 0 else main()
