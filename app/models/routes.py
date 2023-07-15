from flask import Blueprint, render_template, redirect

from models import HomePageView, UpdateBinanceSymbolView, WalletView, UpdateWalletAssetView, UpdateCryptoBotSettingsView, ManageCoinAddView, ManageCoinDelView, CryptoDetailView, autocompleteAdd, autocompleteDel, SearchResults, GetOldOhlcvView, StartWebSocketView
from forms import *
from wallets import *
import requests

app = Blueprint('app', __name__, template_folder='templates')


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route("/manage-coin/add", methods=["GET", "POST"])
def manage_coin_add():
    form = CoinListAddForm()
    coinlist = CoinList.objects.all()
    symbolist = BinanceSymbolList.objects.all()
    if requests.method == "POST":
        if form.validate_on_submit():
            form.save()
            show_text = True
        else:
            show_text = False
    else:
        show_text = False
    return render_template(
        "manage-coin.html",
        addform=form,
        coinlist=coinlist,
        show_text=show_text,
        symbolist=symbolist,
    )


@app.route("/manage-coin/delete", methods=["GET", "POST"])
def manage_coin_delete():
    form = CoinListDelForm()
    coinlist = CoinList.objects.all()
    symbolist = BinanceSymbolList.objects.all()
    if requests.method == "POST":
        if form.validate_on_submit():
            show_del_text = True
        else:
            show_del_text = False
    else:
        show_del_text = False
    return render_template(
        "manage-coin.html",
        delform=form,
        coinlist=coinlist,
        symbolist=symbolist,
        show_del_text=show_del_text,
    )


@app.route("/wallet")
def wallet_view():
    wallet_asset = WalletAssetList.objects.all()
    wallet_balance = WalletAssetBalance.objects.all()
    return render_template("wallet.html", wallet_asset=wallet_asset, wallet_balance=wallet_balance)


@app.route("/wallet/update-asset", methods=["POST"])
def update_wallet_asset():
    form = UpdateWalletAssetForm()
    if form.validate_on_submit():
        save_balance = get_binance_savings()
        btc_save = save_balance["totalAmountInBTC"]
        usdt_save = save_balance["totalAmountInUSDT"]
        locked_stake_usdt, locked_stake_btc = get_binance_locked_stacking()
        flex_defi_stake_usdt, flex_defi_stake_btc = get_binance_flex_defi_stacking()
        locked_defi_stake_usdt, locked_defi_stake_btc = get_binance_locked_defi_stacking()
        asset_list, spot_usdt, spot_btc = get_wallet_assets(info)
        for index, row in asset_list.iterrows():
            asset = row["asset"]
            free = row["free"]
            locked = row["locked"]
            ownusdt = row["ownusdt"]
            ownbtc = row["ownbtc"]
            WalletAssetList.objects.create(
                free=free, locked=locked, ownusdt=ownusdt, ownbtc=ownbtc, asset=asset
            )
        usdt_tot = float(usdt_save) + float(spot_usdt) + float(locked_stake_usdt)
        btc_tot = float(btc_save) + float(spot_btc) + float(locked_stake_btc)
        usdt_stake = locked_stake_usdt + flex_defi_stake_usdt + locked_defi_stake_usdt
        btc_stake = locked_stake_btc + flex_defi_stake_btc + locked_defi_stake_btc
        WalletAssetBalance.objects.create(
            usdtspot=spot_usdt,
            btcspot=spot_btc,
            usdtsav=usdt_save,
            btcsav=btc_save,
            usdtbal=usdt_tot,
            btcbal=btc_tot,
            usdtstake=usdt_stake,
            btcstake=btc_stake,
        )
    return redirect(url_for("wallet_view"))


@app.route("/manage-coin/update-symbol", methods=["GET", "POST"])
def update_binance_symbol():
    form = UpdateBnSymbol()
    coinlist = CoinList.objects.all()
    symbolist = BinanceSymbolList.objects.all()
    symbol_list = get_binance_symbol()
    symbol_list.sort()
    symbol = BinanceSymbolList.objects.values_list("symbol", flat=True)
    symbol = list(symbol)
    symbol.sort()
    if symbol_list == symbol:
        list_updated = True
    else:
        new = list(set(symbol_list) - set(symbol))
        BinanceSymbolList.objects.bulk_create([BinanceSymbolList(symbol=x) for x in new])
        show_list_text = True
    return render_template(
        "manage-coin.html",
        list_updated=list_updated,
        show_list_text=show_list_text,
        coinlist=coinlist,
        symbolist=symbolist,
    )


@app.route("/settings", methods=["GET", "POST"])
def update_crypto_bot_settings():
    form = UpdateCryptoBotSettings()
    if form.validate_on_submit():
        form.save()
        show_text = True
    else:
        show_text = False
    return render_template("settings.html", form=form, show_text=show_text)

if __name__ == '__main__':
    app.run(debug=True)
