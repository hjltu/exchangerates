#!/usr/bin/env pyton3

"""
20jun22 hjltu
config for get_crypto
"""



API_URL = "https://api.coincap.io/v2/candles"
CANDLE_INTERVAL = "d1"
PERIOD_DAYS = 222
BASE_SYMBOL = "tether"
EXCHANGE = "binance"
LOOP_PAUSE = 9999
CRYPTO_DATABASE='../data/crypto.db'
PLOT = '../plots/crypto.png'

SYMBOLS = [
    {'exchange': EXCHANGE, 'id': 'bitcoin',     'symbol': 'BTC'},
    {'exchange': EXCHANGE, 'id': 'ethereum',    'symbol': 'ETH'},
    {'exchange': EXCHANGE, 'id': 'litecoin',    'symbol': 'LTC'},
    {'exchange': EXCHANGE, 'id': 'tron',        'symbol': 'TRX'},
    {'exchange': EXCHANGE, 'id': 'xrp',         'symbol': 'XRP'},
    {'exchange': EXCHANGE, 'id': 'monero',      'symbol': 'XMR'},
    {'exchange': EXCHANGE, 'id': 'zcash',       'symbol': 'ZEC'},
    {'exchange': EXCHANGE, 'id': 'polkadot',    'symbol': 'DOT'},
    {'exchange': EXCHANGE, 'id': 'avalanche',   'symbol': 'AVAX'},
    {'exchange': EXCHANGE, 'id': 'cosmos',      'symbol': 'ATOM'},
    {'exchange': EXCHANGE, 'id': 'solana',      'symbol': 'SOL'},
    {'exchange': EXCHANGE, 'id': 'cardano',     'symbol': 'ADA'},
]

NOTES = """
guarda:
    - SOL, XMR, ZEC, AVAX
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

### TEST CONFIG ###

TEST_DATABASE='../data/test_crypto.db'
TEST_PLOT = '../plots/test_crypto.png'
TEST_SYMBOLS = [
    {'exchange': EXCHANGE, 'id': 'bitcoin',     'symbol': 'BTC'},
    {'exchange': EXCHANGE, 'id': 'ethereum',    'symbol': 'ETH'}
]

TEST_CANDLES = [{
    "data": [{
        "open": "23845.2500000000000000",
        "high": "24442.6600000000000000",
        "low": "23414.0300000000000000",
        "close": "23773.7400000000000000",
        "volume": "181181.1391200000000000",
        "period": 1659052800000},{
        "open": "23777.2800000000000000",
        "high": "24668.0000000000000000",
        "low": "23502.2500000000000000",
        "close": "23643.5100000000000000",
        "volume": "147040.5368600000000000",
        "period": 1659139200000}],
    "timestamp": 1659263725591,
    "curr": "BTC"},{
    "data": [{
        "open": "1724.5200000000000000",
        "high": "1765.9900000000000000",
        "low": "1655.0200000000000000",
        "close": "1721.6800000000000000",
        "volume": "1075910.0060000000000000",
        "period": 1659052800000},{
        "open": "1721.6800000000000000",
        "high": "1744.8500000000000000",
        "low": "1673.0100000000000000",
        "close": "1697.0000000000000000",
        "volume": "715882.6519000000000000",
        "period": 1659139200000}],
    "timestamp": 1659263726437,
    "curr": "ETH"}]

TEST_TABLE = [
    {'curr': 'BTC', 'from': '29Jul22', 'to': '30Jul22', 'num': 2,
        'all': {'l': 23414.03, 'h': 24668.0, 'o': 23845.25, 'c': 23643.51, 'p': 0, 'd': 5},
        'quart': {'l': 23414.03, 'h': 24668.0, 'o': 23845.25, 'c': 23643.51, 'p': 0, 'd': 5},
        'month': {'l': 23414.03, 'h': 24668.0, 'o': 23845.25, 'c': 23643.51, 'p': 0, 'd': 5},
        'week': {'l': 23414.03, 'h': 24668.0, 'o': 23845.25, 'c': 23643.51, 'p': 0, 'd': 5}},
    {'curr': 'ETH', 'from': '29Jul22', 'to': '30Jul22', 'num': 2,
        'all': {'l': 1655.02, 'h': 1765.99, 'o': 1724.52, 'c': 1697.0, 'p': -1, 'd': 6},
        'quart': {'l': 1655.02, 'h': 1765.99, 'o': 1724.52, 'c': 1697.0, 'p': -1, 'd': 6},
        'month': {'l': 1655.02, 'h': 1765.99, 'o': 1724.52, 'c': 1697.0, 'p': -1, 'd': 6},
        'week': {'l': 1655.02, 'h': 1765.99, 'o': 1724.52, 'c': 1697.0, 'p': -1, 'd': 6}}]

TEST_DATA = [{'name': 'BTC', 'price': 23643.51, 'shift': 0, 'diff': 5},
    {'name': 'ETH', 'price': 1697.0, 'shift': -1, 'diff': 6}]
