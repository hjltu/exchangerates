#!/usr/bin/env pyton3

"""
20jun22 hjltu
config for get_crypto
"""



API_URL = "https://api.coincap.io/v2/candles"
CANDLE_INTERVAL = "d1"
PERIOD_DAYS = 33
BASE_SYMBOL = "tether"
LOOP_PAUSE = 9999
CRYPTO_DATABASE='../data/crypto.db'
PLOT = '../plots/crypto.png'

SYMBOLS = [
    ('binance', 'bitcoin', 'BTC'),
    ('binance', 'ethereum', 'ETH'),
    ('binance', 'litecoin', 'LTC'),
    ('binance', 'tron', 'TRX'),
    ('binance', 'xrp', 'XRP'),
    ('binance', 'monero', 'XMR'),
    ('binance', 'zcash', 'ZEC'),
    ('binance', 'polkadot', 'DOT'),
    ('binance', 'avalanche', 'AVAX'),
    ('binance', 'cosmos', 'ATOM'),
    ('binance', 'solana', 'SOL'),
    ('binance', 'cardano', 'ADA'),
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
