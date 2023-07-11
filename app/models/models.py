#!/usr/bin/python3
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class CoinList(db.Model):
    """
       Creates a column of coin_list and adds
       to the database
    """
    coin = db.Column(db.String(15), primary_key=True)
    slug = db.Column(db.String(15), unique=True, nullable=True)

    def save(self):
        self.slug = slugify(self.coin).upper()
        self.coin = self.coin.upper()
        db.session.add(self)
        db.session.commit()

    def __str__(self):
        return self.coin


class BinanceSymbolList(db.Model):
    symbol = db.Column(db.String(15), primary_key=True)

    def save(self):
        self.symbol = self.symbol.upper()
        db.session.add(self)
        db.session.commit()

    def __str__(self):
        return self.symbol


class Wallet(db.Model):
    asset = db.Column(db.String(15), primary_key=True)
    spot_balance = db.Column(db.Numeric(precision=36, scale=18), default=0.0)

    def __str__(self):
        return self.asset
    
class WalletAssetList(db.Model):
    time = db.DateTimeField(auto_now=True, null=True)
    asset = db.CharField(max_length=15)
    free = db.DecimalField(max_digits=36, decimal_places=18, default=0.0)
    locked = db.DecimalField(max_digits=36, decimal_places=18, default=0.0)
    ownusdt = db.DecimalField(max_digits=19, decimal_places=8, default=0.0)
    ownbtc = db.DecimalField(max_digits=19, decimal_places=8, default=0.0)

    def __str__(self):
        return self.asset


class WalletAssetBalance(db.Model):
    time = db.DateTimeField(auto_now=True, null=True)
    usdtbal = db.DecimalField(max_digits=19, decimal_places=8, default=0.0)
    btcbal = db.DecimalField(max_digits=19, decimal_places=8, default=0.0)
    usdtspot = db.DecimalField(max_digits=19, decimal_places=8, default=0.0)
    btcspot = db.DecimalField(max_digits=19, decimal_places=8, default=0.0)
    usdtsav = db.DecimalField(max_digits=19, decimal_places=8, default=0.0)
    btcsav = db.DecimalField(max_digits=19, decimal_places=8, default=0.0)
    usdtstake = db.DecimalField(max_digits=19, decimal_places=8, default=0.0)
    btcstake = db.DecimalField(max_digits=19, decimal_places=8, default=0.0)
