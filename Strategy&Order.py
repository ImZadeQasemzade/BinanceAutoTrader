import math
import pandas as pd
import time
from binance.client import Client
from binance.enums import *
from guppy import hpy
from FilePrepANDTA import *
from TelegramANDGraph import *


def buy_spot(client, order_type, symbol, value, stop_limit_constant=1.1, limit_constant=0.9, stop_limit_price=None,
             limit_price=None, stop_limit_constatnt=10):
    info = client.get_symbol_info(symbol)
    last_price = float(client.get_ticker(symbol=symbol)['lastPrice'])
    minimum = float(info["filters"][3]['minNotional'])
    quantity_step_size = float(info["filters"][2]['minQty'])
    quantity_precision = len(info["filters"][2]['minQty']) - 2
    price_step_size = float(info["filters"][0]['minPrice'])
    price_precision = len(info["filters"][0]['minPrice']) - 2
    if (order_type == "OCO" or order_type == "STOPLIMIT") and stop_limit_price is None:
        quantity = sci_to_reg(
            math.floor((value / (last_price * stop_limit_constant) * 0.98) / quantity_step_size) * quantity_step_size,
            quantity_precision)
    elif stop_limit_price is not None:
        quantity = sci_to_reg(math.floor((value / stop_limit_price * 0.98) / quantity_step_size) * quantity_step_size,
                              quantity_precision)
    else:
        quantity = sci_to_reg(math.floor((value / last_price * 0.98) / quantity_step_size) * quantity_step_size,
                              quantity_precision)

    if value * 0.98 < minimum:
        print("Low value! Increase the value.")
        return None, None, None, None, quantity

    if order_type == "OCO":
        if limit_price is None:
            limit_price = sci_to_reg(math.floor(last_price * limit_constant / price_step_size) * price_step_size,
                                     price_precision)
        else:
            limit_price = sci_to_reg(math.floor(limit_price / price_step_size) * price_step_size, price_precision)
        if stop_limit_price is None:
            price = sci_to_reg(
                math.floor(
                    last_price * stop_limit_constant / price_step_size) * price_step_size + stop_limit_constatnt * price_step_size,
                price_precision)
            stopPrice = sci_to_reg(math.floor(last_price * stop_limit_constant / price_step_size) * price_step_size,
                                   price_precision)
        else:
            price = sci_to_reg(
                math.floor(
                    stop_limit_price / price_step_size) * price_step_size + stop_limit_constatnt * price_step_size,
                price_precision)
            stopPrice = sci_to_reg(math.floor(stop_limit_price / price_step_size) * price_step_size,
                                   price_precision)
        return client.create_oco_order(symbol=symbol, side=SIDE_BUY, stopLimitTimeInForce=TIME_IN_FORCE_GTC,
                                       quantity=quantity, price=limit_price, stopPrice=stopPrice,
                                       stopLimitPrice=price), limit_price, stopPrice, price, quantity

    elif order_type == "MARKET":
        return client.create_order(symbol=symbol, side=SIDE_BUY, type=ORDER_TYPE_MARKET,
                                   quantity=quantity), None, None, None, quantity

    elif order_type == "LIMIT":
        if limit_price is None:
            limit_price = sci_to_reg(math.floor(last_price * limit_constant / price_step_size) * price_step_size,
                                     price_precision)
        else:
            limit_price = sci_to_reg(math.floor(limit_price / price_step_size) * price_step_size, price_precision)
        return client.create_order(symbol=symbol, side=SIDE_BUY, type=ORDER_TYPE_LIMIT,
                                   timeInForce=TIME_IN_FORCE_GTC, quantity=quantity,
                                   price=limit_price), limit_price, None, None, quantity

    elif order_type == "STOPLIMIT":
        if stop_limit_price is None:
            price = sci_to_reg(
                math.floor(
                    last_price * stop_limit_constant / price_step_size) * price_step_size + stop_limit_constatnt * price_step_size,
                price_precision)
            stopPrice = sci_to_reg(math.floor(last_price * stop_limit_constant / price_step_size) * price_step_size,
                                   price_precision)
        else:
            price = sci_to_reg(
                math.floor(
                    stop_limit_price / price_step_size) * price_step_size + stop_limit_constatnt * price_step_size,
                price_precision)
            stopPrice = sci_to_reg(math.floor(stop_limit_price / price_step_size) * price_step_size,
                                   price_precision)
        return client.create_order(symbol=symbol, side=SIDE_BUY, type=ORDER_TYPE_STOP_LOSS_LIMIT,
                                   timeInForce=TIME_IN_FORCE_GTC, quantity=quantity, price=price,
                                   stopPrice=stopPrice), None, stopPrice, price, quantity


def sell_spot(client, order_type, symbol, value, stop_limit_constant=0.9, limit_constant=1.1, stop_limit_price=None,
              limit_price=None, stop_limit_constatnt=10):
    info = client.get_symbol_info(symbol)
    last_price = float(client.get_ticker(symbol=symbol)['lastPrice'])
    minimum = float(info["filters"][3]['minNotional'])
    quantity_step_size = float(info["filters"][2]['minQty'])
    quantity_precision = len(info["filters"][2]['minQty']) - 2
    price_step_size = float(info["filters"][0]['minPrice'])
    price_precision = len(info["filters"][0]['minPrice']) - 2
    quantity = sci_to_reg(math.floor(value / quantity_step_size) * quantity_step_size, quantity_precision)
    if value < minimum / last_price:
        print("Low value! Increase the value.")
        return None, None, None, None, quantity

    if order_type == "OCO":
        if limit_price is None:
            limit_price = sci_to_reg(math.floor(last_price * limit_constant / price_step_size) * price_step_size,
                                     price_precision)
        else:
            limit_price = sci_to_reg(math.floor(limit_price / price_step_size) * price_step_size, price_precision)
        if stop_limit_price is None:
            price = sci_to_reg(
                math.floor(
                    last_price * stop_limit_constant / price_step_size) * price_step_size - stop_limit_constatnt * price_step_size,
                price_precision)
            stopPrice = sci_to_reg(math.floor(last_price * stop_limit_constant / price_step_size) * price_step_size,
                                   price_precision)
        else:
            price = sci_to_reg(
                math.floor(
                    stop_limit_price / price_step_size) * price_step_size - stop_limit_constatnt * price_step_size,
                price_precision)
            stopPrice = sci_to_reg(math.floor(stop_limit_price / price_step_size) * price_step_size,
                                   price_precision)
        return client.create_oco_order(symbol=symbol, side=SIDE_SELL, stopLimitTimeInForce=TIME_IN_FORCE_GTC,
                                       quantity=quantity, price=limit_price, stopPrice=stopPrice,
                                       stopLimitPrice=price), limit_price, stopPrice, price, quantity

    elif order_type == "MARKET":
        return client.create_order(symbol=symbol, side=SIDE_SELL, type=ORDER_TYPE_MARKET,
                                   quantity=quantity), None, None, None, quantity

    elif order_type == "LIMIT":
        if limit_price is None:
            limit_price = sci_to_reg(math.floor(last_price * limit_constant / price_step_size) * price_step_size,
                                     price_precision)
        else:
            limit_price = sci_to_reg(math.floor(limit_price / price_step_size) * price_step_size, price_precision)
        return client.create_order(symbol=symbol, side=SIDE_SELL, type=ORDER_TYPE_LIMIT,
                                   timeInForce=TIME_IN_FORCE_GTC, quantity=quantity,
                                   price=limit_price), limit_price, None, None, quantity

    elif order_type == "STOPLIMIT":
        if stop_limit_price is None:
            price = sci_to_reg(
                math.floor(
                    last_price * stop_limit_constant / price_step_size) * price_step_size - stop_limit_constatnt * price_step_size,
                price_precision)
            stopPrice = sci_to_reg(math.floor(last_price * stop_limit_constant / price_step_size) * price_step_size,
                                   price_precision)
        else:
            price = sci_to_reg(
                math.floor(
                    stop_limit_price / price_step_size) * price_step_size - stop_limit_constatnt * price_step_size,
                price_precision)
            stopPrice = sci_to_reg(math.floor(stop_limit_price / price_step_size) * price_step_size,
                                   price_precision)
        return client.create_order(symbol=symbol, side=SIDE_SELL, type=ORDER_TYPE_STOP_LOSS_LIMIT,
                                   timeInForce=TIME_IN_FORCE_GTC, quantity=quantity, price=price,
                                   stopPrice=stopPrice), None, stopPrice, price, quantity


def cancel(client, symbol, orderId):
    return client.cancel_order(symbol=symbol, orderId=orderId)


def asset_balance(client, asset):
    return float(client.get_asset_balance(asset=asset)["free"])


def status(client, symbol, orderId):
    return client.get_order(symbol=symbol, orderId=orderId)


def open_orders(client, symbol):
    return client.get_open_orders(symbol=symbol)


def last_price(client, symbol):
    return float(client.get_ticker(symbol=symbol)['lastPrice'])


def sell_price_stoplimit(client, symbol, orderId):
    order = status(client, orderId=839285929, symbol="AVAXUSDT")

    return float(client.get_ticker(symbol=symbol)['lastPrice'])


def higher_timeframe_change(client, symbol, interval):
    if interval == "1MINUTE":
        last_candle = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE)[-1]
        return float(last_candle[4]) / float(last_candle[1])
    if interval == "5MINUTE":
        last_candle = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_5MINUTE)[-1]
        return float(last_candle[4]) / float(last_candle[1])
    if interval == "15MINUTE":
        last_candle = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_15MINUTE)[-1]
        return float(last_candle[4]) / float(last_candle[1])
    if interval == "1HOUR":
        last_candle = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR)[-1]
        return float(last_candle[4]) / float(last_candle[1])
    if interval == "4HOUR":
        last_candle = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_4HOUR)[-1]
        return float(last_candle[4]) / float(last_candle[1])
    if interval == "1DAY":
        last_candle = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1DAY)[-1]
        return float(last_candle[4]) / float(last_candle[1])
    if interval == "1WEEK":
        last_candle = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1WEEK)[-1]
        return float(last_candle[4]) / float(last_candle[1])


def ram_monitor():
    h = hpy()
    print(str(h.heap())[38:67])


def channel_buy_oco(client, trading_symbol, value, order_address, train_address, higher_timeframe_interval="1HOUR", percent=2, number_of_candles=10):
    order_df = pd.read_csv(order_address, index_col=0)
    df = pd.read_csv(train_address, index_col=0)
    end_index = df.shape[0] - 1
    bolltrend = boll_trend(df["bollm"], number_of_candles=number_of_candles, percent=percent)
    print(bolltrend)

    if order_df["Open"][0] == 1 or order_df["Open"][0] == 4:
        open_order = open_orders(client, symbol=trading_symbol)
        if len(open_order) != 0:
            time.sleep(0.5)
            cancel(client, symbol=trading_symbol, orderId=open_order[0]["orderId"])
            order_df["Open"][0] = 0
    time.sleep(1)

    if order_df["Open"][0] == 0 and higher_timeframe_change(client, trading_symbol, higher_timeframe_interval) > 0.99:
        print("buy - ratio:", df["bollu"][end_index] / df["bolll"][end_index])
        if bolltrend == "Neutral" and df["bollu"][end_index] / df["bolll"][end_index] > 1.005:
            order_buy, limit_price, stopPrice, price, quantity = buy_spot(client, order_type="LIMIT",
                                                                          symbol=trading_symbol, value=value,
                                                                          limit_price=df["bolll"][end_index])
            print(order_buy)
            if len(order_buy["fills"]) > 0:
                Buy_price = order_buy["fills"][0]["price"]
            else:
                Buy_price = limit_price
            if order_buy is not None:
                order_df["Open"][0], order_df["Index"][0], order_df["Order_id_1"][0], order_df["Order_id_2"][0], order_df["Limit_price"][0], \
                order_df["Stop_price"][0], order_df["Price"][0], order_df["Quantity"][0], order_df["Buy_price"][0] = 1, end_index, order_buy[
                    'orderId'], 0, limit_price, stopPrice, price, quantity, Buy_price

        elif bolltrend == "Uptrend" and df["macd"][end_index] > df["macd"][end_index-1]:
            order_buy, limit_price, stopPrice, price, quantity = buy_spot(client, order_type="LIMIT",
                                                                          symbol=trading_symbol, value=value,
                                                                          limit_price=(3 * df["bollm"][end_index] + 2 *
                                                                                       df["bollu"][end_index]) / 5)
            print(order_buy)
            if len(order_buy["fills"]) > 0:
                Buy_price = order_buy["fills"][0]["price"]
            else:
                Buy_price = limit_price
            if order_buy is not None:
                order_df["Open"][0], order_df["Index"][0], order_df["Order_id_1"][0], order_df["Order_id_2"][0], order_df["Limit_price"][0], \
                order_df["Stop_price"][0], order_df["Price"][0], order_df["Quantity"][0], order_df["Buy_price"][0] = 4, end_index, order_buy[
                    'orderId'], 0, limit_price, stopPrice, price, quantity, Buy_price
    order_df.to_csv(order_address)
    df.to_csv(train_address)


def channel_sell_oco(client, trading_symbol, order_address, train_address, stop_price_constant=0.99, min_limit_constant=1.003):
    order_df = pd.read_csv(order_address, index_col=0)
    df = pd.read_csv(train_address, index_col=0)
    end_index = df.shape[0] - 1

    # >>>uptrend<<<
    if order_df["Open"][0] == 4:
        order_status = status(client, symbol=trading_symbol, orderId=int(order_df["Order_id_1"][0]))
        if order_status['status'] == 'FILLED':
            print("Buy order (limit - uptrend): " + trading_symbol + "\n", order_df["Buy_price"][0])
            message("Buy order (limit - uptrend): " + trading_symbol + "\n" + str(order_df["Buy_price"][0]))
            order_df["Open"][0], order_df["Index"][0], order_df["Order_id_1"][0], order_df["Order_id_2"][0], order_df["Limit_price"][0], \
            order_df["Stop_price"][0], order_df["Price"][0], order_df["Quantity"][0], order_df["Buy_price"][0] = 5, end_index, 0, 0, order_df["Limit_price"][
                0], order_df["Stop_price"][0], order_df["Price"][0], order_df["Quantity"][0], order_df["Buy_price"][0]
        time.sleep(1)

    if order_df["Open"][0] == 6:
        order_status = status(client, symbol=trading_symbol, orderId=int(order_df["Order_id_1"][0]))
        if order_status['status'] == 'FILLED':
            sell_price = float(order_status['cummulativeQuoteQty']) / float(order_status['executedQty'])
            print("Sell order (stop limit - uptrend): " + trading_symbol + "\n",
                  sell_price / order_df["Buy_price"][0])
            graph(df, start_index=int(order_df["Index"][0]), end_index=end_index, buy_price=order_df["Buy_price"][0], sell_price=sell_price)
            image(address="./data/order.png", caption="Sell order (stop limit - uptrend): " + trading_symbol + "\n"+str(df["Date"][order_df["Index"][0]])+"\n"+str(df["Date"][end_index])+"\n"+str(sell_price / order_df["Buy_price"][0]))
            order_df["Open"][0], order_df["Index"][0], order_df["Order_id_1"][0], order_df["Order_id_2"][0], order_df["Limit_price"][0], \
            order_df["Stop_price"][0], order_df["Price"][0], order_df["Quantity"][0], order_df["Buy_price"][0] = 0, 0, 0, 0, 0, 0, 0, 0, 0
        else:
            time.sleep(0.5)
            cancel(client, symbol=trading_symbol, orderId=int(order_df['Order_id_1'][0]))
            order_df["Open"][0], order_df["Index"][0], order_df["Order_id_1"][0], order_df["Order_id_2"][0], order_df["Limit_price"][0], \
            order_df["Stop_price"][0], order_df["Price"][0], order_df["Quantity"][0], order_df["Buy_price"][0] = 5, order_df["Index"][0], 0, 0, order_df["Limit_price"][
                0], order_df["Stop_price"][0], order_df["Price"][0], order_df["Quantity"][0], order_df["Buy_price"][0]
        time.sleep(1)

    if order_df["Open"][0] == 5:
        print("Sell...STOPLIMIT:")
        if trading_symbol[-3:] == "BTC":
            value = asset_balance(client, trading_symbol[:-3])
        else:
            value = asset_balance(client, trading_symbol[:-4])
        time.sleep(1)
        print("value: ", value)
        lastPrice = last_price(client, trading_symbol)
        print("stop price: ", max(lastPrice * stop_price_constant, order_df["Stop_price"][0], order_df["Buy_price"][0] * stop_price_constant))
        order_sell, limit_price, stopPrice, price, quantity = sell_spot(client, order_type="STOPLIMIT",
                                                                        symbol=trading_symbol,
                                                                        value=value, stop_limit_price=max(
                lastPrice * stop_price_constant, order_df["Stop_price"][0], order_df["Buy_price"][
                    0] * stop_price_constant))
        print(order_sell)
        if order_sell is not None:
            order_df["Open"][0], order_df["Index"][0], order_df["Order_id_1"][0], order_df["Order_id_2"][0], order_df["Limit_price"][0], \
            order_df["Stop_price"][0], order_df["Price"][0], order_df["Quantity"][0], order_df["Buy_price"][0] = 6, order_df["Index"][0], order_sell[
                'orderId'], 0, limit_price, stopPrice, price, quantity, order_df["Buy_price"][0]
        time.sleep(1)

    # >>>neutral<<<
    if order_df["Open"][0] == 1:
        order_status = status(client, symbol=trading_symbol, orderId=int(order_df["Order_id_1"][0]))
        if order_status['status'] == 'FILLED':
            print("Buy order (limit - neutral): " + trading_symbol + "\n", order_df["Buy_price"][0])
            message("Buy order (limit - neutral): " + trading_symbol + "\n" + str(order_df["Buy_price"][0]))
            order_df["Open"][0], order_df["Index"][0], order_df["Order_id_1"][0], order_df["Order_id_2"][0], order_df["Limit_price"][0], \
            order_df["Stop_price"][0], order_df["Price"][0], order_df["Quantity"][0], order_df["Buy_price"][0] = 2, end_index, 0, 0, order_df["Limit_price"][
                0], order_df["Stop_price"][0], order_df["Price"][0], order_df["Quantity"][0], order_df["Buy_price"][0]
        time.sleep(1)

    if order_df["Open"][0] == 3:
        order_status1 = status(client, symbol=trading_symbol, orderId=int(order_df["Order_id_1"][0]))
        order_status2 = status(client, symbol=trading_symbol, orderId=int(order_df["Order_id_2"][0]))
        if order_status1['status'] == 'FILLED':
            sell_price = float(order_status1['cummulativeQuoteQty']) / float(order_status1['executedQty'])
            print("Sell order (oco - neutral): " + trading_symbol + "\n",
                  sell_price / order_df["Buy_price"][0])
            graph(df, start_index=int(order_df["Index"][0]), end_index=end_index, buy_price=order_df["Buy_price"][0], sell_price=float(order_status1['price']))
            image(address="./data/order.png", caption="Sell order (oco - neutral): " + trading_symbol + "\n" + str(df["Date"][order_df["Index"][0]])+"\n"+str(df["Date"][end_index])+"\n"+str(sell_price / order_df["Buy_price"][0]))
            order_df["Open"][0], order_df["Index"][0], order_df["Order_id_1"][0], order_df["Order_id_2"][0], order_df["Limit_price"][0], \
            order_df["Stop_price"][0], order_df["Price"][0], order_df["Quantity"][0], order_df["Buy_price"][0] = 0, 0, 0, 0, 0, 0, 0, 0, 0
        elif order_status2['status'] == 'FILLED':
            sell_price = float(order_status2['cummulativeQuoteQty']) / float(order_status2['executedQty'])
            print("Sell order (oco - neutral): " + trading_symbol + "\n",
                  sell_price / order_df["Buy_price"][0])
            graph(df, start_index=int(order_df["Index"][0]), end_index=end_index, buy_price=order_df["Buy_price"][0], sell_price=float(order_status2['price']))
            image(address="./data/order.png", caption="Sell order (oco - neutral): " + trading_symbol + "\n" +str(df["Date"][order_df["Index"][0]])+"\n"+str(df["Date"][end_index])+"\n"+str(sell_price / order_df["Buy_price"][0]))
            order_df["Open"][0], order_df["Index"][0], order_df["Order_id_1"][0], order_df["Order_id_2"][0], order_df["Limit_price"][0], \
            order_df["Stop_price"][0], order_df["Price"][0], order_df["Quantity"][0], order_df["Buy_price"][0] = 0, 0, 0, 0, 0, 0, 0, 0, 0
        else:
            time.sleep(0.5)
            cancel(client, symbol=trading_symbol, orderId=int(order_df['Order_id_1'][0]))
            order_df["Open"][0], order_df["Index"][0], order_df["Order_id_1"][0], order_df["Order_id_2"][0], order_df["Limit_price"][0], \
            order_df["Stop_price"][0], order_df["Price"][0], order_df["Quantity"][0], order_df["Buy_price"][0] = 2, order_df["Index"][0], 0, 0, order_df["Limit_price"][
                0], order_df["Stop_price"][0], order_df["Price"][0], order_df["Quantity"][0], order_df["Buy_price"][0]
        time.sleep(1)

    if order_df["Open"][0] == 2:
        print("Sell...OCO:")
        if trading_symbol[-3:] == "BTC":
            value = asset_balance(client, trading_symbol[:-3])
        else:
            value = asset_balance(client, trading_symbol[:-4])
        time.sleep(1)
        print("value: ", value)
        if df["bollu"][end_index] > last_price(client, trading_symbol) > max(df["bollm"][end_index], order_df["Buy_price"][0]*min_limit_constant):
            stopPrice = order_df["Buy_price"][0] * min_limit_constant
            print(1)
            print("STOPLIMIT change", trading_symbol, order_df["Buy_price"][0] * stop_price_constant, " => ", order_df["Buy_price"][0] * min_limit_constant)
            message("STOPLIMIT change " + trading_symbol + "\n" + str(order_df["Buy_price"][0] * stop_price_constant) + " => " + str(order_df["Buy_price"][0] * min_limit_constant))
        elif order_df["Stop_price"][0] == order_df["Buy_price"][0] * min_limit_constant: #after change
            print(2)
            stopPrice = order_df["Buy_price"][0] * min_limit_constant
            print("STOPLIMIT change", trading_symbol, order_df["Buy_price"][0] * stop_price_constant, " => ", order_df["Buy_price"][0] * min_limit_constant)
            message("STOPLIMIT change " + trading_symbol + "\n" + str(order_df["Buy_price"][0] * stop_price_constant) + " => " + str(order_df["Buy_price"][0] * min_limit_constant))
        else: #first time & so on
            print(3)
            stopPrice = order_df["Buy_price"][0] * stop_price_constant
        print("stop price: ", stopPrice, "limit price: ", max(df["bollu"][end_index], order_df["Buy_price"][0] * (min_limit_constant + 0.001)))
        order_sell, limit_price, stopPrice, price, quantity = sell_spot(client, order_type="OCO", symbol=trading_symbol,
                                                                        value=value,
                                                                        limit_price=max(df["bollu"][end_index],
                                                                                        order_df["Buy_price"][
                                                                                            0] * (min_limit_constant + 0.001)),
                                                                        stop_limit_price=stopPrice)
        print(order_sell)
        if order_sell is not None:
            order_df["Open"][0], order_df["Index"][0], order_df["Order_id_1"][0], order_df["Order_id_2"][0], order_df["Limit_price"][0], \
            order_df["Stop_price"][0], order_df["Price"][0], order_df["Quantity"][0], order_df["Buy_price"][0] = 3, order_df["Index"][0], order_sell['orders'][0][
                'orderId'], order_sell['orders'][1]['orderId'], limit_price, stopPrice, price, quantity, order_df["Buy_price"][0]
        time.sleep(1)

    order_df.to_csv(order_address)
    df.to_csv(train_address)


def stoploss_price_update(client, updating_symbols, update_constant):
    removing_symbols = []
    for updating_symbol in updating_symbols:
        open_order = open_orders(client, symbol=updating_symbol)
        if len(open_order) == 0:
            print("Order is executed (stop limit): " + updating_symbol + "\n")
            message("Order is executed (stop limit): " + updating_symbol + "\n")
            removing_symbols.append(updating_symbol)
            continue
        lastPrice = last_price(client, symbol=updating_symbol)
        time.sleep(0.5)
        if float(status(client, symbol=updating_symbol, orderId=int(open_order[0]["orderId"]))[
                     'stopPrice']) < lastPrice * update_constant:
            cancel(client, symbol=updating_symbol, orderId=open_order[0]["orderId"])
            time.sleep(1)

            if updating_symbol[-3:] == "BTC":
                value = asset_balance(client, updating_symbol[:-3])
            else:
                value = asset_balance(client, updating_symbol[:-4])
            time.sleep(0.5)
            order_sell, limit_price, stopPrice, price, quantity = sell_spot(client, order_type="STOPLIMIT",
                                                                            symbol=updating_symbol, value=value,
                                                                            stop_limit_constant=update_constant,
                                                                            limit_constant=1.1)
            print("Price is updated (stop limit): " + updating_symbol + ":", stopPrice)
            message("Price is updated (stop limit): " + updating_symbol + ":" + str(stopPrice))
        time.sleep(1)
    for removing_symbol in removing_symbols:
        updating_symbols.remove(removing_symbol)
        print(removing_symbol + " is removed")
        message(removing_symbol + " is removed")
