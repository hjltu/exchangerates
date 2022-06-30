#!/usr/bin/env pyton3

"""
20jun22 hjltu
config for get_crypto
"""



API_URL = "https://api.coincap.io/v2/candles"
CANDLE_INTERVAL = "d1"
QUOTE_ID = "tether"
LOOP_PAUSE = 9999
CRYPTO_DATABASE='data/cross.db'

CURR = [
    ('bibox', 'bitcoin', 'BTC'),
    ('bibox', 'ethereum', 'ETH'),
    ('bibox', 'litecoin', 'LTC'),
    ('bibox', 'tron', 'TRX'),
    ('binance', 'xrp', 'XRP'),
    ('binance', 'monero', 'XMR'),
    ('bibox', 'zcash', 'ZEC'),
    ('binance', 'polkadot', 'DOT'),
    ('binance', 'avalanche', 'AVAX'),
    ('binance', 'cosmos', 'ATOM'),
    ('binance', 'solana', 'SOL'),
    ('binance', 'cardano', 'ADA'),
#    ('binance', 'kusama', 'KSM'),
#    ('binance', 'dogecoin', 'DOGE'),
#    ('binance', 'terra-luna', 'LUNA'),

#    ('binance', 'polygon', 'MATIC'),
#    ('binance', 'near-protocol', 'NEAR'),
#    ('binance', 'chainlink', 'LINK'),
#    ('binance', 'uniswap', 'UNI'),
#    ('binance', 'stellar', 'XLM'),
]
NOTES = """
guarda:
    - SOL, XMR, ZEC, AVAX
goals to buy:
    BTC: 30K
    ETH: 2K-1K
    LTC: 80-60
    TRX: 0.055
    XRP: 0.4-0.3
    XMR: 150-100
    ZEC: 100-50
    LUNA: 10-5
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
