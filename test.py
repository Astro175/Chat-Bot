#!/usr/bin/python3

import os
from binance import Client
import pandas as pd

binance_api = os.getenv('binance_api')
binance_key = os.getenv('binance_secret')

client = Client(binance_api, binance_key)
tickers = client.get_historical_klines('BTCUSDT', '5m', '30m ago UTC')
data = pd.DataFrame(tickers)
print(data)
