from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, ValidationError
from .models import CoinList, BinanceSymbolList, WalletAssetList, WalletAssetBalance, CryptoBotSettings

class CoinListAddForm(FlaskForm):
    coin = StringField("Coin", validators=[InputRequired()], render_kw={"placeholder": "ex. BTCUSDT"})

    def validate_coin(self, field):
        data = field.data
        if data.islower() or (not data.islower() and not data.isupper()):
            data = data.upper()
        if not BinanceSymbolList.query.filter_by(symbol=data).first():
            raise ValidationError(f"Coin {data} not found")
        if CoinList.query.filter_by(coin=data).first():
            raise ValidationError(f"Coin {data} has already been added")

class CoinListDelForm(FlaskForm):
    coin = StringField("Coin", validators=[InputRequired()], render_kw={"placeholder": "ex. ADAUSDT"})

    def validate_coin(self, field):
        data = field.data
        if data.islower() or (not data.islower() and not data.isupper()):
            data = data.upper()
            field.data = data
        if CoinList.query.filter_by(coin=data).first():
            CoinList.query.filter_by(coin=data).delete()
        else:
            raise ValidationError(f"Cryptocurrency pair {field.data} not found")

class UpdateBnSymbolForm(FlaskForm):
    symbol = StringField("Symbol")

class UpdateWalletAssetForm(FlaskForm):
    asset = StringField("Asset")
    free = IntegerField("Free")
    locked = IntegerField("Locked")
    ownusdt = IntegerField("Ownusdt")
    ownbtc = IntegerField("Ownbtc")

class UpdateWalletBalanceForm(FlaskForm):
    usdtbal = IntegerField("Usdtbal")
    btcbal = IntegerField("Btcbal")

class UpdateCryptoBotSettingsForm(FlaskForm):
    api_key = StringField("API Key")
    api_secret = StringField("API Secret")
    SECRET_KEY = StringField("Secret Key")

    def validate(self):
        if CryptoBotSettings.query.first():
            raise ValidationError("You cannot add more somethings.")
        return super().validate()
