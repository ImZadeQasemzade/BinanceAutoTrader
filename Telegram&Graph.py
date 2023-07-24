import telegram
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

TELEGRAM_BOT_TOKEN = 'Telegram Bot Token'
TELEGRAM_CHAT_ID = 'Telegram Chat ID'
def message(text):
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)

def image(address, caption):
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=open(address, 'rb'), caption=caption)

def graph(prices, start_index, end_index, buy_price, sell_price):
    # Plot settings
    fig, ax = plt.subplots()
    plt.figure(figsize=(10, 8))

    # Candlesticks
    indices, heights, bottoms, colors, widths = [], [], [], [], []

    for i in range(start_index, end_index + 1):
        indices.append(i)
        widths.append(0.3)
        heights.append(prices.loc[i, 'High'] - prices.loc[i, 'Low'])
        bottoms.append(prices.loc[i, 'Low'])
        if prices.loc[i, 'Open'] < prices.loc[i, 'Close']:
            colors.append('green')
        else:
            colors.append('red')

        indices.append(i)
        widths.append(1)
        if prices.loc[i, 'Open'] < prices.loc[i, 'Close']:
            colors.append('green')
            heights.append(prices.loc[i, 'Close'] - prices.loc[i, 'Open'])
            bottoms.append(prices.loc[i, 'Open'])
        else:
            colors.append('red')
            heights.append(prices.loc[i, 'Open'] - prices.loc[i, 'Close'])
            bottoms.append(prices.loc[i, 'Close'])

    ax.plot([start_index, end_index], [buy_price, sell_price], "*")
    ax.bar(indices, heights, bottom=bottoms, width=widths, color=colors)

    bollu, bollm, bolll = {}, {}, {}
    for i in range(start_index, end_index+1):
        bollu[i] = prices["bollu"][i]
        bollm[i] = prices["bollm"][i]
        bolll[i] = prices["bolll"][i]
    bollu_plot = pd.Series(data=bollu)
    bollm_plot = pd.Series(data=bollm)
    bolll_plot = pd.Series(data=bolll)
    ax.plot(bollu_plot, color='yellow')
    ax.plot(bollm_plot, color='pink')
    ax.plot(bolll_plot, color='purple')

    fig.savefig('./data/order.png')
    plt.close(fig)
