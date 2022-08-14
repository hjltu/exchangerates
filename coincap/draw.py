
import sys, time, json, shelve
from datetime import datetime
import matplotlib.pyplot as plt
#from matplotlib.pyplot import figure
import numpy as np
from itertools import cycle
from config import *
sys.path.append("..")
from data.exchanges_db import DB


def main(db_file=CRYPTO_DATABASE, plt_file=PLOT):
    print('open',db_file)
    ctm = time.strftime("%b%y")

    times, times_sorted = prepare_data(db_file)
    table = prepare_table(times_sorted)
    #print_proc(times, table, plt_file)
    print_proc_price(times, table, plt_file)


def test_main(db_file=TEST_DATABASE, plt_file=TEST_PLOT):
    print('open',db_file)
    ctm = time.strftime("%b%y")

    times, times_sorted = prepare_data(db_file)
    table = prepare_table(times_sorted)
    #print_proc(times, table, plt_file)
    print_proc_price(times, table, plt_file)


def prepare_data(db_file):

    db = DB(db_file)
    coins_list = db.read()
    times = [ t[0] for t in coins_list ]
    times = sorted([datetime.strptime(tm,'%d%b%y_%H:%M') for tm in times])
    times = [tm.strftime('%d%b%y_%H:%M') for tm in times]
    #k = [tm for tm in k if ctm in tm]

    times_sorted = []
    for key in times:
        for val in coins_list:
            if val[0] == key:
                times_sorted.append(val[1])

    #print(coins_list, '\n',  times_sorted, '\n', times)
    return times, times_sorted



def prepare_table(times_sorted):
    """
    Output: table = [
        {'name': 'BTC', 'time': [], 'price': [], 'proc_week': [], 'BTC': [], 'ETH': []},
        {'name': 'ETC', 'time': [], 'price': [], 'proc_week': [], 'BTC': [], 'ETH': []}]
    """
    #table = [{'name': '', 'times': [], 'prices': []}] * len(times_sorted[0])
    table = []
    res = [table.append({'name': coin.get('name')}) for coin in times_sorted[0]]
    #print(table)
    for coin in table:
        for k, v in times_sorted[0][0].items():
            coin if k == 'name' else coin.update({k: []})

    #print(table)

    for moment_list in times_sorted:
        #print(len(moment_list),moment_list)
        for moment in moment_list:
            #print(moment)
            for coin in table:
                if coin.get('name') == moment.get('name'):
                    for k, v in moment.items():
                        coin if k == 'name' else coin[k].append(v)
    #print(json.dumps(table, indent=4))
    return table


def print_proc(times, table, plt_file):
    num = len(table)
    fig = plt.figure(figsize=(30, 15), dpi=80)
    fig.patch.set_facecolor('tan')
    plt.rcParams['axes.facecolor'] = 'silver'
    cycol = cycle(['blue','orange','green','red','brown','pink','olive','cyan','magenta','gold','beige','lime','violet','skyblue'])

    proc_min = 10
    proc_max = 10
    for n in range(num):
        coin = table[n]
        label = (coin.get('name'))
        t = times
        p = coin.get('shift')
        proc_min = min(p) if min(p) < proc_min else proc_min
        proc_max = max(p) if max(p) > proc_max else proc_max
        plt.plot(t, p, color=next(cycol), label=label, linewidth=3, marker='o', markevery=int(len(p)/9)+1)

    if len(t) > 9:
        plt.xticks([t[i] for i in range(0, len(t), int(len(t)/5))])
    plt.yticks([p for p in range(proc_min, proc_max+1)])
    plt.title('Procents by week')
    plt.ylabel('Procents by week')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
    plt.tick_params(left=True, right=True)
    plt.tick_params(labelleft=True, labelright=True)
    plt.legend()

    plt.savefig(plt_file)
    print('saved')


def print_proc_price(times, table, plt_file):
    num = len(table)
    fig = plt.figure(figsize=(30, num*15), dpi=80)
    fig.patch.set_facecolor('tan')
    plt.rcParams['axes.facecolor'] = 'silver'
    cycol = cycle(['blue','orange','green','red','brown','pink','olive','cyan','magenta','gold','beige','lime','violet','skyblue'])

    num = len(table)
    plt.subplot(num+1, 1, 1)

    proc_min = 10
    proc_max = 10
    for n in range(num):
        coin = table[n]
        label = (coin.get('name'))
        t = times
        p = coin.get('shift')
        proc_min = min(p) if min(p) < proc_min else proc_min
        proc_max = max(p) if max(p) > proc_max else proc_max
        plt.plot(t, p, color=next(cycol), label=label, linewidth=3, marker='o', markevery=int(len(p)/9)+1)

    if len(t) > 9:
        plt.xticks([t[i] for i in range(0, len(t), int(len(t)/5))])
    plt.yticks([p for p in range(proc_min, proc_max+1)])
    plt.title('Procents by week')
    plt.ylabel('Procents by week')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
    plt.tick_params(left=True, right=True)
    plt.tick_params(labelleft=True, labelright=True)
    plt.legend()

    for n in range(num):
        plt.subplot(num+1, 1, n+2)
        coin = table[n]
        t = times
        p = coin.get('price')
        plt.plot(t, p)
        plt.title(coin.get('name'))
        if len(t) > 9:
            plt.xticks([t[i] for i in range(0, len(t), int(len(t)/5))])
        #plt.yticks([p for p in range(proc_min, proc_max+1)])
        plt.grid(color = 'grey', linestyle = '--', linewidth = 0.5)

    plt.savefig(plt_file)
    print('saved')


if __name__ == '__main__':
    #main(sys.argv[1:][0])
    main()
