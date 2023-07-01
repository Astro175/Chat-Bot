import requests
import pandas as pd
import time

# Binance API endpoint for klines (historical data)
endpoint = 'https://api.binance.com/api/v3/klines'

# Cryptocurrency symbol and timeframe
symbol = 'BTCUSDT'  # Example: Bitcoin (BTC) against Tether (USDT)
interval = '1d'  # Daily timeframe

# Parameters for the API request
params = {
    'symbol': symbol,
    'interval': interval,
    'limit': 1000,  # Maximum number of data points to retrieve
    'startTime': 1672531200000,  # January 1, 2023 (timestamp in milliseconds)
    'endTime': int(time.time() * 1000),
}

# Send the API request
response = requests.get(endpoint, params=params)
data = response.json()

# Convert the response to a pandas DataFrame
df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume',
                                 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume',
                                 'ignore'])

# Data preprocessing
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # Convert timestamp to datetime format
df['close'] = df['close'].astype(float)  # Convert close price to float

# Display the data
print(df.head())
