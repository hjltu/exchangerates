#!/usr/bin/env python3


"""
https://www.tutorialspoint.com/python-object-persistence-shelve
https://www.w3schools.com/python/matplotlib_plotting.asp

for rpi: sudo apt install python-dev libatlas-base-dev libopenjp2-7 libtiff5
python3 -m venv venv
venv/bin/pip install --upgrade pip
venv/bin/pip install matplotlib numpy

cp ../tbot-04may21/tbot.db tbot.db
venv/bin/python3 stat.py tbot.db
"""


import sys, time, shelve
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
from itertools import cycle

#import matplotlib
#for name, hex in matplotlib.colors.cnames.items():
#    print(name, hex)

GRAPH_NAME = 'plots/draw.png'


def main(dbfile):
    print('open',dbfile)
    with shelve.open(dbfile) as db:
        try:
            db.pop('token')
        except:
            pass
        #print(list(db))
        #coins_list = sorted(list(db.items()))
        coins_list = list(db.items())
        times = list(db.keys())
        times = sorted([datetime.strptime(tm,'%d%b%y') for tm in times])
        times = [tm.strftime('%d%b%y') for tm in times]

        coins = []
        for key in times:
            for val in coins_list:
                if val[0] == key:
                    coins.append(val[1])
    #print(times, '\t', coins)

    """
    times = ['25Jun22']
    coins = [[{'name': 'AAL', 'price': 13.89, 'proc': -16, 'diff': 37},]]
    """

    print('prepare table')

    table = []
    res = [table.append({'name': coin.get('name')}) for coin in coins[0]]
    #print('*** 1', table)

    for coin in table:
        for k, v in coins[0][0].items():
            coin if k == 'name' else coin.update({k: []})
    #print('*** 2', table)

    for time_beats in coins:
        for beat in time_beats:
            for coin in table:
                if coin.get('name') == beat.get('name'):
                    for k, v in beat.items():
                        coin if k == 'name' else coin[k].append(v)

    #print('*** 3', table)
    """
    table = [{'name': 'AAL', 'price': [13.89], 'proc': [-16], 'diff': [37]},]
    """

    print('drawing graph')
    fig = plt.figure(figsize=(30, 25), dpi=80)
    fig.patch.set_facecolor('tan')
    plt.rcParams['axes.facecolor'] = 'silver'
    plt.title('Procents by month')

    cycol = cycle(colors.cnames.keys())
    cycol = cycle(['blue','orange','green','red','brown','pink','olive','cyan','magenta','gold','beige','lime','violet','skyblue'])

    proc_min = 10
    proc_max = 10
    num = len(table)
    for n in range(num):
        coin = table[n]
        label = (coin.get('name'))
        t = coin.get('time')
        p = coin.get('proc')
        proc_min = min(p) if min(p) < proc_min else proc_min
        proc_max = max(p) if max(p) > proc_max else proc_max
        try:
            plt.plot(times, [0]*len(times), color='black', linewidth=3, linestyle='dotted')
            plt.plot(times, p, color=next(cycol), label=label, linewidth=3, marker='o', markevery=int(len(p)/9)+1)
        except:
            print(label, len(times), len(p), len(p_fix))

    if len(times) > 9:
        plt.xticks([times[i] for i in range(0, len(times), int(len(times)/5))])
    plt.yticks([p for p in range(proc_min, proc_max+1)])
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
    plt.tick_params(left=True, right=True)
    plt.tick_params(labelleft=True, labelright=True)
    plt.legend()

    plt.savefig(GRAPH_NAME)
    print('saved', GRAPH_NAME)


if __name__ == '__main__':
    main(sys.argv[1:][0])
