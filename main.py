from binance.client import Client
from binance.enums import *
from TelegramANDGraph import *
from StrategyANDOrder import *
from FilePrepANDTA import *


now = datetime.datetime.now()
message("Start date: " + now.strftime("%Y-%m-%d %H:%M:%S"))

api_key = "wKDIRmfCf5h3bxqCTj9Hk1oSNCQJXjih2G65ntdcd58VjUp4aobqrOKAVL0gtjN7"
secret_key = "BECkHgtFwFlhIKFckqq1BhgRlDMbD5TJcVaIOkrQBj4KqsEPDCA9m39iK4N2zAcI"
client = Client(api_key, secret_key)

#>>>>>>>channel strategy<<<<<<<<
#Conditions: higher timeframe change > 0.99 - trend = neutral, uptrend - neutral bollu/bolll > 1.005, uptrend - neutral buy bolll, uptrend buy bollm - neutral sell bollu, uptrend sell follow 0.99
trading_symbols = ["DOTUSDT", "TOMOUSDT", "CAKEUSDT", "TRXUSDT", "AVAXUSDT", "ATOMUSDT", "DYDXUSDT"]
interval = "5MINUTE"
higher_timeframe_interval = "1HOUR"
start_date = "9 nov, 2021"
start_date_update = "10 nov, 2021"

valueBTC, numBTC = asset_balance(client, "BTC"), 0
valueUSDT, numUSDT = asset_balance(client, "USDT"), 0
for trading_symbol in trading_symbols:
    if trading_symbol[-3:] == "BTC":
        numBTC += 1
    else:
        numUSDT += 1
if valueBTC != 0 and numBTC != 0:
    BTCperCOIN = valueBTC/numBTC
if valueUSDT != 0 and numUSDT != 0:
    USDTperCOIN = valueUSDT/numUSDT
"""
updating_symbols = ["FTMUSDT"]
update_constant = 0.93
"""

while True:
    for trading_symbol in trading_symbols:
        address = "./data/" + trading_symbol + "_" + interval + ".csv"
        train_address = "./data/TRAIN_" + trading_symbol + "_" + interval + ".csv"
        order_address = "./data/ORDER_" + trading_symbol + "_" + interval + ".csv"
        if trading_symbol[-3:] == "BTC":
            value = BTCperCOIN
        else:
            value = USDTperCOIN
        prices_and_orders_csv(trading_symbol, interval, start_date, start_date_update, address, order_address, train_address)
        channel_buy_oco(client, trading_symbol, value=value, percent=2, number_of_candles=10, order_address=order_address, train_address=train_address, higher_timeframe_interval=higher_timeframe_interval)
        channel_sell_oco(client, trading_symbol, stop_price_constant=0.99, order_address=order_address, train_address=train_address)
        print("\n")
    """
    for updating_symbol in updating_symbols:
        stoploss_price_update(client, updating_symbol, update_constant)
    
    for tiny_symbol in tiny_symbols:
        tiny_buy_oco()
        tiny_sell_oco()
    """
    time.sleep(5)
