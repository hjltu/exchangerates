
import sys, time, json, shelve
from datetime import datetime
import matplotlib.pyplot as plt
#from matplotlib.pyplot import figure
import numpy as np
from itertools import cycle
from config import CRYPTO_DATABASE


def main(dbfile):
    print('open',dbfile)
    ctm = time.strftime("%b%y")

    coins_list, times_sorted = prepare_data(dbfile)
    table = prepare_table(times_sorted)
    print_proc(table)
    #print_table(table)


def prepare_data(dbfile):
    with shelve.open(dbfile) as db:
        #coins_list = sorted(list(db.items()))
        coins_list = list(db.items())

        times = list(db.keys())
        times = sorted([datetime.strptime(tm,'%d%b%y_%H:%M') for tm in times])
        times = [tm.strftime('%d%b%y_%H:%M') for tm in times]
        #k = [tm for tm in k if ctm in tm]

    times_sorted = []
    for key in times:
        for val in coins_list:
            if val[0] == key:
                times_sorted.append(val[1])

    """
    coins_list = [
        ('04Jun22_13:27', [
            {'name': 'BTC', 'time': '04Jun22_13:27', 'price': 29656.9, 'proc_week': 2, 'BTC': 0, 'ETH': -3, 'LTC': -2},
            {'name': 'ETH', 'time': '04Jun22_13:27', 'price': 1763.7, 'proc_week': 2, 'BTC': 3, 'ETH': 0, 'LTC': 1},
            {'name': 'LTC', 'time': '04Jun22_13:27', 'price': 62.45, 'proc_week': 2, 'BTC': 2, 'ETH': -1, 'LTC': 0}]),
        ('04Jun22_13:32', [
            {'name': 'BTC', 'time': '04Jun22_13:32', 'price': 29656.9, 'proc_week': 2, 'BTC': 0, 'ETH': -3, 'LTC': -2},
            {'name': 'ETH', 'time': '04Jun22_13:32', 'price': 1763.7, 'proc_week': 2, 'BTC': 3, 'ETH': 0, 'LTC': 1},
            {'name': 'LTC', 'time': '04Jun22_13:32', 'price': 62.45, 'proc_week': 2, 'BTC': 2, 'ETH': -1, 'LTC': 0}])]

    times = ['31May22_06:22', '31May22_06:28']
    coins = [
        [
            {'name': 'BTC', 'time': '04Jun22_13:27', 'price': 29656.9, 'proc_week': 2, 'BTC': 0, 'ETH': -3, 'LTC': -2},
            {'name': 'ETH', 'time': '04Jun22_13:27', 'price': 1763.7, 'proc_week': 2, 'BTC': 3, 'ETH': 0, 'LTC': 1},
            {'name': 'LTC', 'time': '04Jun22_13:27', 'price': 62.45, 'proc_week': 2, 'BTC': 2, 'ETH': -1, 'LTC': 0}],
        [
            {'name': 'BTC', 'time': '04Jun22_13:32', 'price': 29656.9, 'proc_week': 2, 'BTC': 0, 'ETH': -3, 'LTC': -2},
            {'name': 'ETH', 'time': '04Jun22_13:32', 'price': 1763.7, 'proc_week': 2, 'BTC': 3, 'ETH': 0, 'LTC': 1},
            {'name': 'LTC', 'time': '04Jun22_13:32', 'price': 62.45, 'proc_week': 2, 'BTC': 2, 'ETH': -1, 'LTC': 0}]]
    """
    #print(coins_list, '\n',  times_sorted, '\n', times)
    return coins_list, times_sorted



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


def print_proc(table):
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
        t = coin.get('time')
        p = coin.get('proc_week')
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

    plt.savefig('plots/draw.png')
    print('saved')


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
    main(sys.argv[1:][0])
