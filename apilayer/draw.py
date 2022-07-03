#!/usr/bin/env python3

"""
02Jul22 hjltu
install:
   sudo apt install python3-venv python3-pip
   python3 -m venv venv
   venv/bin/pip install --upgrade pip
   venv/bin/pip install matplotlib pytest
run:
    ../venv/bin/pytest -rfP draw.py
    ../venv/bin/python draw.py
"""


import sys, time, json, shelve
import matplotlib.pyplot as plt
from datetime import datetime
from itertools import cycle
from config import *
sys.path.append("..")
from data.exchanges_db import DB


def main(db_file=CURR_DATABASE, plt_file=PLOT):
    db = DB(db_file)
    data = db.read()
    table = prepare_table(data)
    draw_plot(table, plt_file)


def test_main(db_file=TEST_DATABASE, plt_file=TEST_PLOT):
    db = DB(db_file)
    assert db.read() == TEST_DATA_FROM_DB
    assert prepare_table(TEST_DB_DATA) == TEST_TABLE_TO_DRAW
    assert draw_plot(TEST_TABLE_TO_DRAW, plt_file) is True


def prepare_table(data):

    times = [t[0] for t in data]
    times = sorted([datetime.strptime(tm,'%d%b%y') for tm in times])
    times = [tm.strftime('%d%b%y') for tm in times]

    table = []
    table = [{'name': d.get('name'), 'time': times, 'shift': []} for d in data[0][1]]
    for time in times:
        for prices in data:
            if time == prices[0]:
                add_to_table(table, prices[1])

    return table


def add_to_table(table, prices):

    for t in table:
        for p in prices:
            if t.get('name') == p.get('name'):
                t.get('shift').append(p.get('shift'))
    return


def draw_plot(table, plt_file):
    num = len(table)
    fig = plt.figure(figsize=(30, 15), dpi=80)
    #fig = plt.figure(figsize=(30, num*3), dpi=80)
    fig.patch.set_facecolor('tan')
    plt.rcParams['axes.facecolor'] = 'silver'
    cycol = cycle(['blue','orange','green','red','brown','pink','olive','cyan','magenta','gold','beige','lime','violet','skyblue'])

    shift_min = 10
    shift_max = 10
    for n in range(num):
        coin = table[n]
        label = (coin.get('name'))
        time = coin.get('time')
        shift = coin.get('shift')
        shift_min = min(shift) if min(shift) < shift_min else shift_min
        shift_max = max(shift) if max(shift) > shift_max else shift_max
        plt.plot(time, shift, color=next(cycol), label=label, linewidth=3, marker='o', markevery=int(len(shift)/9)+1)

    if len(time) > 9:
        plt.xticks([time[i] for i in range(0, len(time), int(len(time)/5))])
    plt.yticks([shift for shift in range(shift_min, shift_max+1)])
    plt.title(f'Base current is {BASE_SYMBOL}')
    plt.ylabel(f'Procent by {PERIOD_DAYS} days' )
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
    plt.tick_params(left=True, right=True)
    plt.tick_params(labelleft=True, labelright=True)
    plt.legend()

    plt.savefig(plt_file)
    print('saved')

    return True


def print_table(table):

    num = len(table)
    #fig = plt.figure(figsize=(30, 15), dpi=80)
    fig = plt.figure(figsize=(25, num*7), dpi=80)
    fig.patch.set_facecolor('tan')
    plt.rcParams['axes.facecolor'] = 'silver'

    for n in range(num):
        coin = table[n]
        plt.subplot(num, 1, n+1)
        plt.ylabel(coin.get('name'))
        t = coin.get('time')
        p = coin.get('price')

        #cycol = cycle('bgrcmyk')
        cycol = cycle(['blue','orange','green','red','brown','pink','olive','cyan','magenta','gold','beige','lime','violet','skyblue'])
        for k, v in coin.items():
            if k == 'name' or k == 'time' or k == 'price':
                continue
            if sum(v) is not 0:
                c = [p[i] + (p[i]/100)*v[i] for i in range(len(v))]
                if len(t) > len(c):
                    #print('t,c,v =', len(t),len(c), len(v))
                    c.insert(0, c[0])
                    v.insert(0, v[0])
                plt.plot(t, c, color=next(cycol), label=k, linewidth=4)

        plt.plot(t, p, color='black', label='price', linewidth=4, marker='o', markevery=int(len(p)/9)+1)
        #plt.ylim(min(p), max(p))
        #plt.yticks(np.arange(min(p), max(p), 1))

        if len(t) > 9:
            plt.xticks([t[i] for i in range(0, len(t), int(len(t)/5))])
        plt.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
        plt.tick_params(left=True, right=True)
        plt.tick_params(labelleft=True, labelright=True)
        plt.legend()

    plt.savefig('plots/draw.png')
    print('saved')


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args) if args else main()
