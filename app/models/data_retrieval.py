import requests
import pandas as pd
import time

"""
Module that retrieves data from binance api into
a panda dataframe
"""
endpoint = 'https://api.binance.com/api/v3/klines'

symbol = 'BTCUSDT'
interval = '1d'

params = {
    'symbol': symbol,
    'interval': interval,
    'limit': 1000,  
    'startTime': 1672531200000,
    'endTime': int(time.time() * 1000),
}

def retrieve_data():
    """Sends an API request, convert the response
       to a pandas dataframe and convert the timestamp
    """
    response = requests.get(endpoint, params=params)
    data = response.json()

    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                     'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                     'taker_buy_quote_asset_volume', 'ignore'])

    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['close'] = df['close'].astype(float)

    return df

data_df = retrieve_data()
