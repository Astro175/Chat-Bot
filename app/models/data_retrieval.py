from typing import Any
from binance.client import Client
import pandas as pd
import datetime as dt
import config
from binance.exceptions import BinanceAPIException
from flask import current_app
from models import CoinList, BinanceSymbolList, Ohlcv
import os
from sqlalchemy import create_engine

api_key = os.getenv("api_key")
api_secret = os.getenv("api_secret")

# initialize
client = Client(api_key, api_secret)


# DB connection
user = config.DATABASES['default']['USER']
password = config.DATABASES['default']['PASSWORD']
database_name = config.DATABASES['default']['NAME']
host_name = config.DATABASES['default']['HOST']

database_url = 'mysql+mysqldb://{user}:{password}@{host_name}/{database_name}'.format(
    user=user,
    password=password,
    database_name=database_name,
    host_name = host_name,
)


engine = create_engine(database_url, echo=False)




# Get all Binance symbols
def get_binance_symbol():
    symbol_list = []
    exchange_info = client.get_exchange_info()
    for n in exchange_info['symbols']:
        symbol = n['symbol']
        symbol_list.append(symbol)
    return symbol_list    



    







def get_old_ohlcv(slug):
    # obj = CoinList.query.filter_by(coin=slug,price__isnull=True).first()
    # if obj:
    #     past_days = 5
    #     status = True
    # else:
    #     past_days = 1
    #     status = False  

    past_days = 20
    # client = Client()
    interval = '4h'
    start_str = str(
        (pd.to_datetime('today')-pd.Timedelta(str(past_days)+' days')).date())
    D = pd.DataFrame(client.get_historical_klines(
        symbol=slug, start_str=start_str, interval=interval))
    D.columns = ['open_time', 'open', 'high', 'low', 'close', 'volume',
                 'close_time', 'qav', 'num_trades', 'taker_base_vol',
                 'taker_quote_vol', 'is_best_match']
    D['date'] = [
        dt.datetime.fromtimestamp(x/1000) for x in D.open_time]
    dfohlcv = D[['date', 'open', 'high', 'low', 'close',
                 'volume', 'num_trades', 'taker_base_vol', 'taker_quote_vol']]
    D['coin_id'] = slug
    dfohlcv = D[['date', 'open', 'high', 'low', 'close',
                 'volume', 'num_trades', 'taker_base_vol', 'taker_quote_vol', 'coin_id']]
    print(dfohlcv)
   
    dfohlcv.to_sql(Ohlcv.__tablename__, con=engine, if_exists='append', index=False)

    # Ohlcv.query.update( \
    #             values={'free': free, 'locked': locked, \
    #             'ownusdt': ownusdt, 'ownbtc': ownbtc}, \
    #             synchronize_session=False )                       

    return True

