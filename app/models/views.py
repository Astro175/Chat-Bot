from flask import Blueprint, render_template, redirect

from .views import HomePageView, UpdateBinanceSymbolView, WalletView, UpdateWalletAssetView, UpdateCryptoBotSettingsView, ManageCoinAddView, ManageCoinDelView, CryptoDetailView, autocompleteAdd, autocompleteDel, SearchResults, GetOldOhlcvView, StartWebSocketView


app = Blueprint('app', __name__, template_folder='templates')


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/wallet.html')
def wallet():
    return render_template('wallet.html')


@app.route('/manage-coin.html')
def manage_coin():
    return render_template('manage-coin.html')


@app.route('/manage-coin.html/update-binance-list/')
def update_binance_list():
    return redirect(UpdateBinanceSymbolView.as_view())


@app.route('/manage-coin.html/delete-coin/')
def delete_coin():
    return redirect(ManageCoinDelView.as_view())


@app.route('/Wallet/Update_Asset/')
def update_wallet_asset():
    return redirect(UpdateWalletAssetView.as_view())


@app.route('/settings.html')
def settings():
    return render_template('settings.html')


@app.route('/autocompleteAdd')
def autocomplete_add():
    return autocompleteAdd()


@app.route('/autocompleteDel')
def autocomplete_del():
    return autocompleteDel()


@app.route('/dashboard/<slug:slug>/')
def crypto_details(slug):
    return render_template('crypto-details.html', slug=slug)


@app.route('/search/<str:search>/')
def search_results(search):
    return SearchResults(search)


@app.route('/dashboard/<str:asset>/get-old-ohlcv/')
def get_old_ohlcv(asset):
    return GetOldOhlcvView(asset)


@app.route('/dashboard/<str:asset>/start-websocket/')
def start_websocket(asset):
    return StartWebSocketView(asset)


if __name__ == '__main__':
    app.run(debug=True)