import datetime
from binance.client import Client
import time
import os
from stockstats import *

api_key = "API Key"
secret_key = "Secret Key"
client = Client(api_key, secret_key)

#>>>>>>>>>>File prep<<<<<<<<<<
def sci_to_reg(number, precision):
    f_sci = "{:." + str(precision) + "f}"
    return f_sci.format(number)

def create_df(trading_symbol, interval="1DAY", start_date="1 jan, 2021"):
    train_address = "./data/" + trading_symbol + "_" + interval + ".csv"
    df = pd.DataFrame()

    if interval == "1MINUTE":
        klines = client.get_historical_klines(trading_symbol, Client.KLINE_INTERVAL_1MINUTE, start_str=start_date)
        for i in klines:
            row_date = datetime.datetime.fromtimestamp(i[0] / 1000)
            row_year = row_date.strftime("%Y")
            row_month = row_date.strftime("%m")
            row_day = row_date.strftime("%d")
            row_hour = row_date.strftime("%H")
            row_minute = row_date.strftime("%M")
            # row_second = row_date.strftime("%S")
            row_date = row_year + row_month + row_day + row_hour + row_minute
            row_open = i[1]
            row_high = i[2]
            row_low = i[3]
            row_close = i[4]
            row_volume = i[5]
            row = {"Date": row_date, "Open": row_open, "Close": row_close, "High": row_high, "Low": row_low,
                   "Volume": row_volume}
            df = df.append(row, ignore_index=True)

    if interval == "5MINUTE":
        klines = client.get_historical_klines(trading_symbol, Client.KLINE_INTERVAL_5MINUTE, start_str=start_date)
        for i in klines:
            row_date = datetime.datetime.fromtimestamp(i[0] / 1000)
            row_year = row_date.strftime("%Y")
            row_month = row_date.strftime("%m")
            row_day = row_date.strftime("%d")
            row_hour = row_date.strftime("%H")
            row_minute = row_date.strftime("%M")
            # row_second = row_date.strftime("%S")
            row_date = row_year + row_month + row_day + row_hour + row_minute
            row_open = i[1]
            row_high = i[2]
            row_low = i[3]
            row_close = i[4]
            row_volume = i[5]
            row = {"Date": row_date, "Open": row_open, "Close": row_close, "High": row_high, "Low": row_low,
                   "Volume": row_volume}
            df = df.append(row, ignore_index=True)

    if interval == "15MINUTE":
        klines = client.get_historical_klines(trading_symbol, Client.KLINE_INTERVAL_15MINUTE, start_str=start_date)
        for i in klines:
            row_date = datetime.datetime.fromtimestamp(i[0] / 1000)
            row_year = row_date.strftime("%Y")
            row_month = row_date.strftime("%m")
            row_day = row_date.strftime("%d")
            row_hour = row_date.strftime("%H")
            row_minute = row_date.strftime("%M")
            # row_second = row_date.strftime("%S")
            row_date = row_year + row_month + row_day + row_hour + row_minute
            row_open = i[1]
            row_high = i[2]
            row_low = i[3]
            row_close = i[4]
            row_volume = i[5]
            row = {"Date": row_date, "Open": row_open, "Close": row_close, "High": row_high, "Low": row_low,
                   "Volume": row_volume}
            df = df.append(row, ignore_index=True)

    if interval == "1HOUR":
        klines = client.get_historical_klines(trading_symbol, Client.KLINE_INTERVAL_1HOUR, start_str=start_date)
        for i in klines:
            row_date = datetime.datetime.fromtimestamp(i[0] / 1000)
            row_year = row_date.strftime("%Y")
            row_month = row_date.strftime("%m")
            row_day = row_date.strftime("%d")
            row_hour = row_date.strftime("%H")
            row_minute = row_date.strftime("%M")
            # row_second = row_date.strftime("%S")
            row_date = row_year + row_month + row_day + row_hour + row_minute
            row_open = i[1]
            row_high = i[2]
            row_low = i[3]
            row_close = i[4]
            row_volume = i[5]
            row = {"Date": row_date, "Open": row_open, "Close": row_close, "High": row_high, "Low": row_low,
                   "Volume": row_volume}
            df = df.append(row, ignore_index=True)

    if interval == "4HOUR":
        klines = client.get_historical_klines(trading_symbol, Client.KLINE_INTERVAL_4HOUR, start_str=start_date)
        for i in klines:
            row_date = datetime.datetime.fromtimestamp(i[0] / 1000)
            row_year = row_date.strftime("%Y")
            row_month = row_date.strftime("%m")
            row_day = row_date.strftime("%d")
            row_hour = row_date.strftime("%H")
            row_minute = row_date.strftime("%M")
            # row_second = row_date.strftime("%S")
            row_date = row_year + row_month + row_day + row_hour + row_minute
            row_open = i[1]
            row_high = i[2]
            row_low = i[3]
            row_close = i[4]
            row_volume = i[5]
            row = {"Date": row_date, "Open": row_open, "Close": row_close, "High": row_high, "Low": row_low,
                   "Volume": row_volume}
            df = df.append(row, ignore_index=True)

    if interval == "1DAY":
        klines = client.get_historical_klines(trading_symbol, Client.KLINE_INTERVAL_1DAY, start_str=start_date)
        for i in klines:
            row_date = datetime.datetime.fromtimestamp(i[0] / 1000)
            row_year = row_date.strftime("%Y")
            row_month = row_date.strftime("%m")
            row_day = row_date.strftime("%d")
            row_hour = row_date.strftime("%H")
            row_minute = row_date.strftime("%M")
            # row_second = row_date.strftime("%S")
            row_date = row_year + row_month + row_day + row_hour + row_minute
            row_open = i[1]
            row_high = i[2]
            row_low = i[3]
            row_close = i[4]
            row_volume = i[5]
            row = {"Date": row_date, "Open": row_open, "Close": row_close, "High": row_high, "Low": row_low,
                   "Volume": row_volume}
            df = df.append(row, ignore_index=True)

    time.sleep(1)
    df.to_csv(train_address)
    return

def update_df(trading_symbol, address, interval="1HOUR", start_date="1 jan, 2020"):
    df = pd.read_csv(address, index_col=0)
    df["Date"] = df["Date"].astype("int64")
    last = df.shape[0]
    df = df.drop(last - 1)

    if interval == "1MINUTE":
        klines = client.get_historical_klines(trading_symbol, Client.KLINE_INTERVAL_1MINUTE, start_str=start_date)
        for i in klines:
            row_date = datetime.datetime.fromtimestamp(i[0] / 1000)
            row_year = row_date.strftime("%Y")
            row_month = row_date.strftime("%m")
            row_day = row_date.strftime("%d")
            row_hour = row_date.strftime("%H")
            row_minute = row_date.strftime("%M")
            # row_second = row_date.strftime("%S")
            row_date = row_year + row_month + row_day + row_hour + row_minute
            row_open = i[1]
            row_high = i[2]
            row_low = i[3]
            row_close = i[4]
            row_volume = i[5]
            row = {"Date": row_date, "Open": row_open, "Close": row_close, "High": row_high, "Low": row_low,
                   "Volume": row_volume}
            if not (int(row_date) in df["Date"].tolist()):
                df = df.append(row, ignore_index=True)

    if interval == "5MINUTE":
        klines = client.get_historical_klines(trading_symbol, Client.KLINE_INTERVAL_5MINUTE, start_str=start_date)
        for i in klines:
            row_date = datetime.datetime.fromtimestamp(i[0] / 1000)
            row_year = row_date.strftime("%Y")
            row_month = row_date.strftime("%m")
            row_day = row_date.strftime("%d")
            row_hour = row_date.strftime("%H")
            row_minute = row_date.strftime("%M")
            # row_second = row_date.strftime("%S")
            row_date = row_year + row_month + row_day + row_hour + row_minute
            row_open = i[1]
            row_high = i[2]
            row_low = i[3]
            row_close = i[4]
            row_volume = i[5]
            row = {"Date": row_date, "Open": row_open, "Close": row_close, "High": row_high, "Low": row_low,
                   "Volume": row_volume}
            if not (int(row_date) in df["Date"].tolist()):
                df = df.append(row, ignore_index=True)

    if interval == "15MINUTE":
        klines = client.get_historical_klines(trading_symbol, Client.KLINE_INTERVAL_15MINUTE, start_str=start_date)
        for i in klines:
            row_date = datetime.datetime.fromtimestamp(i[0] / 1000)
            row_year = row_date.strftime("%Y")
            row_month = row_date.strftime("%m")
            row_day = row_date.strftime("%d")
            row_hour = row_date.strftime("%H")
            row_minute = row_date.strftime("%M")
            # row_second = row_date.strftime("%S")
            row_date = row_year + row_month + row_day + row_hour + row_minute
            row_open = i[1]
            row_high = i[2]
            row_low = i[3]
            row_close = i[4]
            row_volume = i[5]
            row = {"Date": row_date, "Open": row_open, "Close": row_close, "High": row_high, "Low": row_low,
                   "Volume": row_volume}
            if not (int(row_date) in df["Date"].tolist()):
                df = df.append(row, ignore_index=True)

    if interval == "1HOUR":
        klines = client.get_historical_klines(trading_symbol, Client.KLINE_INTERVAL_1HOUR, start_str=start_date)
        for i in klines:
            row_date = datetime.datetime.fromtimestamp(i[0] / 1000)
            row_year = row_date.strftime("%Y")
            row_month = row_date.strftime("%m")
            row_day = row_date.strftime("%d")
            row_hour = row_date.strftime("%H")
            row_minute = row_date.strftime("%M")
            # row_second = row_date.strftime("%S")
            row_date = row_year + row_month + row_day + row_hour + row_minute
            row_open = i[1]
            row_high = i[2]
            row_low = i[3]
            row_close = i[4]
            row_volume = i[5]
            row = {"Date": row_date, "Open": row_open, "Close": row_close, "High": row_high, "Low": row_low,
                   "Volume": row_volume}
            if not (int(row_date) in df["Date"].tolist()):
                df = df.append(row, ignore_index=True)

    if interval == "4HOUR":
        klines = client.get_historical_klines(trading_symbol, Client.KLINE_INTERVAL_4HOUR, start_str=start_date)
        for i in klines:
            row_date = datetime.datetime.fromtimestamp(i[0] / 1000)
            row_year = row_date.strftime("%Y")
            row_month = row_date.strftime("%m")
            row_day = row_date.strftime("%d")
            row_hour = row_date.strftime("%H")
            row_minute = row_date.strftime("%M")
            # row_second = row_date.strftime("%S")
            row_date = row_year + row_month + row_day + row_hour + row_minute
            row_open = i[1]
            row_high = i[2]
            row_low = i[3]
            row_close = i[4]
            row_volume = i[5]
            row = {"Date": row_date, "Open": row_open, "Close": row_close, "High": row_high, "Low": row_low,
                   "Volume": row_volume}
            if not (int(row_date) in df["Date"].tolist()):
                df = df.append(row, ignore_index=True)

    if interval == "1DAY":
        klines = client.get_historical_klines(trading_symbol, Client.KLINE_INTERVAL_1DAY, start_str=start_date)
        for i in klines:
            row_date = datetime.datetime.fromtimestamp(i[0] / 1000)
            row_year = row_date.strftime("%Y")
            row_month = row_date.strftime("%m")
            row_day = row_date.strftime("%d")
            row_hour = row_date.strftime("%H")
            row_minute = row_date.strftime("%M")
            # row_second = row_date.strftime("%S")
            row_date = row_year + row_month + row_day + row_hour + row_minute
            row_open = i[1]
            row_high = i[2]
            row_low = i[3]
            row_close = i[4]
            row_volume = i[5]
            row = {"Date": row_date, "Open": row_open, "Close": row_close, "High": row_high, "Low": row_low,
                   "Volume": row_volume}
            if not (int(row_date) in df["Date"].tolist()):
                df = df.append(row, ignore_index=True)

    time.sleep(1)
    df.to_csv(address)
    return

def prices_and_orders_csv(trading_symbol, interval, start_date, start_date_update, address, order_address, train_address):
    if os.path.isfile(address):
        update_df(trading_symbol, address=address, interval=interval, start_date=start_date_update)
    else:
        create_df(trading_symbol, interval=interval, start_date=start_date)

    if not os.path.isfile(order_address):
        order_df = pd.DataFrame()
        row = {"Open": 0, "Index":0, "Order_id_1": 0, "Order_id_2": 0, "Buy_price": 0, "Quantity": 0, "Stop_price": 0, "Price": 0, "Limit_price": 0}
        order_df = order_df.append(row, ignore_index=True)
        order_df.to_csv(order_address)

    df = pd.read_csv(address, index_col=0)
    stock = StockDataFrame.retype(pd.read_csv(address, index_col=0))
    stock[""] = range(0, stock.shape[0])
    stock = stock.set_index("")
    df.insert(6, "sma", stock['close_5_sma'])
    df.insert(6, "atr", stock['atr'])
    df.insert(6, "macd", stock['macdh'])
    df.insert(6, "kdjk", stock['kdjk'])
    df.insert(6, "kdjd", stock['kdjd'])
    df.insert(6, "kdjj", stock['kdjj'])
    df.insert(6, "rsi", stock['rsi_6'])
    df.insert(6, "bollm", stock['boll'])
    df.insert(6, "bollu", stock['boll_ub'])
    df.insert(6, "bolll", stock['boll_lb'])
    df.to_csv(train_address)
    print("Done updating list:" + trading_symbol)

"""
[
  [
    1499040000000,      // Open time
    "0.01634790",       // Open
    "0.80000000",       // High
    "0.01575800",       // Low
    "0.01577100",       // Close
    "148976.11427815",  // Volume
    1499644799999,      // Close time
    "2434.19055334",    // Quote asset volume
    308,                // Number of trades
    "1756.87402397",    // Taker buy base asset volume
    "28.46694368",      // Taker buy quote asset volume
    "17928899.62484339" // Ignore.
  ]
]
"""

#>>>>>>>>>>TA<<<<<<<<<<
def trend(prices, start, end, start_index, end_index):
    indices = []
    for i in range(start, end + 1):
        if i != start_index and i != end_index and prices.loc[i, 'High'] > prices.loc[i - 1, 'High'] and prices.loc[i, 'High'] > prices.loc[i + 1, 'High']:
            indices.append((i, "High", prices.loc[i, 'High']))
        elif i == start_index and prices.loc[i, 'High'] > prices.loc[i + 1, 'High']:
            indices.append((i, "High", prices.loc[i, 'High']))
        elif i == end_index and prices.loc[i, 'High'] > prices.loc[i - 1, 'High']:
            indices.append((i, "High", prices.loc[i, 'High']))

        if i != start_index and i != end_index and prices.loc[i, 'Low'] < prices.loc[i - 1, 'Low'] and prices.loc[i, 'Low'] < prices.loc[i + 1, 'Low']:
            indices.append((i, "Low", prices.loc[i, 'Low']))
        elif i == start_index and prices.loc[i, 'Low'] < prices.loc[i + 1, 'Low']:
            indices.append((i, "Low", prices.loc[i, 'Low']))
        elif i == end_index and prices.loc[i, 'Low'] < prices.loc[i - 1, 'Low']:
            indices.append((i, "Low", prices.loc[i, 'Low']))

    for j in [0, 1]:
        Removing_indices_list = []
        for i in range(len(indices) - 1):
            if indices[i][1] == "High" and indices[i + 1][1] == "High" and indices[i][2] > indices[i + 1][2]:
                Removing_indices_list.append(indices[i + 1])
            elif indices[i][1] == "High" and indices[i + 1][1] == "High" and indices[i][2] <= indices[i + 1][2]:
                Removing_indices_list.append(indices[i])
            elif indices[i][1] == "Low" and indices[i + 1][1] == "Low" and indices[i][2] < indices[i + 1][2]:
                Removing_indices_list.append(indices[i + 1])
            elif indices[i][1] == "Low" and indices[i + 1][1] == "Low" and indices[i][2] >= indices[i + 1][2]:
                Removing_indices_list.append(indices[i])
            elif indices[i][0] == indices[i + 1][0]:
                Removing_indices_list.append(indices[i])
                Removing_indices_list.append(indices[i + 1])
        Removing_indices_list = list(dict.fromkeys(Removing_indices_list))
        for i in Removing_indices_list:
            indices.remove(i)

    Total = [(i[0], i[1]) for i in indices]
    return Total

def trend_range(prices, start_index, end_index):
    indices = []
    for i in range(start_index, end_index + 1):
        if i != start_index and i != end_index and prices.loc[i, 'High'] > prices.loc[i - 1, 'High'] and prices.loc[i, 'High'] > prices.loc[i + 1, 'High']:
            indices.append((i, "High", prices.loc[i, 'High']))
        elif i == start_index and prices.loc[i, 'High'] > prices.loc[i + 1, 'High']:
            indices.append((i, "High", prices.loc[i, 'High']))
        elif i == end_index and prices.loc[i, 'High'] > prices.loc[i - 1, 'High']:
            indices.append((i, "High", prices.loc[i, 'High']))

        if i != start_index and i != end_index and prices.loc[i, 'Low'] < prices.loc[i - 1, 'Low'] and prices.loc[i, 'Low'] < prices.loc[i + 1, 'Low']:
            indices.append((i, "Low", prices.loc[i, 'Low']))
        elif i == start_index and prices.loc[i, 'Low'] < prices.loc[i + 1, 'Low']:
            indices.append((i, "Low", prices.loc[i, 'Low']))
        elif i == end_index and prices.loc[i, 'Low'] < prices.loc[i - 1, 'Low']:
            indices.append((i, "Low", prices.loc[i, 'Low']))

    for j in [0, 1]:
        Removing_indices_list = []
        for i in range(len(indices) - 1):
            if indices[i][1] == "High" and indices[i + 1][1] == "High" and indices[i][2] > indices[i+1][2]:
                Removing_indices_list.append(indices[i+1])
            elif indices[i][1] == "High" and indices[i + 1][1] == "High" and indices[i][2] <= indices[i + 1][2]:
                Removing_indices_list.append(indices[i])
            elif indices[i][1] == "Low" and indices[i + 1][1] == "Low" and indices[i][2] < indices[i+1][2]:
                Removing_indices_list.append(indices[i+1])
            elif indices[i][1] == "Low" and indices[i + 1][1] == "Low" and indices[i][2] > indices[i+1][2]:
                Removing_indices_list.append(indices[i])
            elif indices[i][0] == indices[i+1][0]:
                Removing_indices_list.append(indices[i])
                Removing_indices_list.append(indices[i+1])
        Removing_indices_list = list(dict.fromkeys(Removing_indices_list))
        for i in Removing_indices_list:
            indices.remove(i)

    High, Low, Trend, indices_list = 0, 0, "", []
    for i in range(0, len(indices)):
        if indices[i][1] == "Low":
            if Low == 0:
                Low = indices[i][2]
                Trend = "NA"
            if Low < indices[i][2]:
                Trend = "Uptrend"
            elif Low > indices[i][2]:
                Trend = "Downtrend"
            Low = indices[i][2]
        else:
            if High == 0:
                High = indices[i][2]
                Trend = "NA"
            if High < indices[i][2]:
                Trend = "Uptrend"
            elif High > indices[i][2]:
                Trend = "Downtrend"
            High = indices[i][2]
        indices_list.append([indices[i][0], Trend, indices[i][1], indices[i][2]])

    indices_list[0][1] = indices_list[2][1]
    indices_list[1][1] = indices_list[3][1]

    ranges = []
    last = indices_list[0][0]
    for i in range(1, len(indices_list)):
        if indices_list[i][1] != indices_list[i-1][1]:
            ranges.append((last, indices_list[i-1][0], indices_list[i-1][1]))
            last = indices_list[i-1][0]
        elif i == (len(indices_list)-1):
            ranges.append((last, indices_list[i][0], indices_list[i][1]))

    return ranges

def boll_trend(bollm, number_of_candles=10, percent=2):
    end_index = bollm.shape[0]-1
    tot = 0
    for i in range(end_index - number_of_candles, end_index+1):
        tot += (1 - bollm.loc[i]/bollm.loc[end_index])
    if tot > percent/100:
        return "Uptrend"
    elif tot < -percent/100:
        return "Downtrend"
    else:
        return "Neutral"
