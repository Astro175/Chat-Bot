#!/usr/bin/python3
"""Module for user"""

import requests
import pandas as pd
import time

class User:
    """
       Balance: Available balance a user has
       User class that does portfolio management
    """
    def __init__(self, balance):
        self.balance = balance
        self.position = None
        self.asset = self.retrieve_data()
    
    def retrieve_data(self):
        """Sends an API request, convert the response
           to a pandas dataframe and convert the timestamp
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

        response = requests.get(endpoint, params=params)
        data = response.json()
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 
                                     'close', 'volume', 'close_time',
                                     'quote_asset_volume', 'number_of_trades',
                                     'taker_buy_base_asset_volume',
                                     'taker_buy_quote_asset_volume', 'ignore'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['close'] = df['close'].astype(float)

        return df
 
    def perform_technical_analysis(self, data):
        """ Perform your technical analysis operations here
            You can access the user's balance using self.balance
            You can access the data for analysis using the data parameter
        """
        
        # Example: Calculate RSI
        self.asset['rsi_14'] = (self.asset['close'], 14)
        print(self.asset)
        
        # Example: Make trading decisions based on RSI and user's balance
        if rsi > 70:
            # Sell some assets
            self.balance += 100
        elif rsi < 30:
            # Buy some assets
            self.balance -= 100
        else:
            pass
            # Hold
        
        # Return any relevant results or update the state of the class as needed
    
    def calculate_rsi(self, close, lookback):
        """Calculates the rsi of a given crypto asset"""
        diff = close.diff()
        average_up = []
        average_down = []

        for i in range(len(diff)):
            if diff[i] < 0:
                average_up.append(0)
                average_down.append(ret[i])
            else:
               average_up.append(ret[i])
               average_down.append(0)

        up_series = pd.Series(up)
        down_series = pd.Series(down).abs()
        up_ewm = up_series.ewm(com = lookback - 1, adjust = False).mean()
        down_ewm = down_series.ewm(com = lookback - 1, adjust = False).mean()
        rs = up_ewm/down_ewm
        rsi = 100 - (100 / (1 + rs))
        rsi_df = pd.DataFrame(rsi).rename(columns = {0:'rsi'}).set_index(close.index)
        rsi_df = rsi_df.dropna()
        return rsi_df[3:]

