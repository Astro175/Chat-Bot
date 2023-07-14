from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError
from .models import CoinList, BinanceSymbolList, WalletAssetList, WalletAssetBalance, CryptoBotSettings


class CoinListAddForm(FlaskForm):
    coin = StringField('Coin', render_kw={"placeholder": "ex. BTCUSDT"})
    submit = SubmitField('Add Coin')

    def validate_coin(self, field):
        data = field.data
        if data.islower() or (not data.islower() and not data.isupper()):
            data = data.upper()
        if not BinanceSymbolList.query.filter_by(symbol=data).first():
            raise ValidationError(f"Coin {data} not found")
        if CoinList.query.filter_by(coin=data).first():
            raise ValidationError(f"Coin {data} has already been added")


class CoinListDelForm(FlaskForm):
    coin = StringField('Coin', render_kw={"placeholder": "ex. ADAUSDT"})
    submit = SubmitField('Delete Coin')

    def validate_coin(self, field):
        data = field.data
        if data.islower() or (not data.islower() and not data.isupper()):
            data = data.upper()
            field.data = data
        if CoinList.query.filter_by(coin=data).first():
            CoinList.query.filter_by(coin=data).delete()
            db.session.commit()
        else:
            raise ValidationError(f"Cryptocurrency pair {field.data} not found")


class UpdateBnSymbolForm(FlaskForm):
    symbol = StringField('Symbol')
    submit = SubmitField('Update')


class UpdateWalletAssetForm(FlaskForm):
    asset = StringField('Asset')
    free = StringField('Free')
    locked = StringField('Locked')
    ownusdt = StringField('Own USDT')
    ownbtc = StringField('Own BTC')
    submit = SubmitField('Update')


class UpdateWalletBalanceForm(FlaskForm):
    usdtbal = StringField('USDT Balance')
    btcbal = StringField('BTC Balance')
    submit = SubmitField('Update')


class UpdateCryptoBotSettingsForm(FlaskForm):
    api_key = StringField('API Key')
    api_secret = StringField('API Secret')
    secret_key = StringField('Secret Key')
    submit = SubmitField('Update')

    def validate(self):
        if CryptoBotSettings.query.first():
            raise ValidationError('You cannot add more somethings.')
        return super(UpdateCryptoBotSettingsForm, self).validate()
