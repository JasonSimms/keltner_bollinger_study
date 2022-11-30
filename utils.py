# This is a study on billinger bands and Kelter Channels. 
#  We are looking for potential upcoming squeeze when a Bollinger Band contracts inside the KC causing a volatility squeeze
# The demo uses a 2x BB and a 1.5 Keltner Channel **Keltner channel uses an ema so there are alot of tuning possible on periods....

from datetime import datetime
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt

def get_today():
    return datetime.today().strftime('%Y-%m-%d')


def chart_it():

    def get_sma(prices, rate):
        return prices.rolling(rate).mean()

    def get_bollinger_bands(prices, rate=20):
        sma = get_sma(prices, 20)
        std = prices.rolling(rate).std()
        bollinger_up = sma + std * 2
        bollinger_down = sma - std * 2
        return bollinger_up , bollinger_down

    def get_atr(data):
        high_low = data['High'] - data['Low']
        high_close = np.abs(data['High']- data['Close'].shift())
        low_close = np.abs(data['Low']-data['Close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis = 1)
        true_range = np.max(ranges, axis=1)
        atr = true_range.rolling(14).sum()/14
        return atr


    def get_keltner(ema , atr):
        keltner_up = ema + (1.5*atr)
        keltner_down = ema - (1.5*atr)
        return keltner_up , keltner_down



    today = get_today()
    df = pdr.DataReader("HD", 'yahoo', '2021-07-01', '2022-01-01')
    # df.index = np.arange(df.shape[0])
    # df.head()
    df["SMA"] = get_sma(df['Adj Close'],20)
    df["Bollinger Up"] , df["Bollinger Down"] = get_bollinger_bands(df['Adj Close'])
    df['ATR'] = get_atr(df)
    df['EMA'] = df['Adj Close'].ewm(com=0.4).mean()
    df['Keltner Up'] , df['Keltner Down'] = get_keltner(df['EMA'], df['ATR'])
    # print(df)
    # closing_prices = df['Close']

    # # sma = get_sma(closing_prices, 20)
    # bollinger_up , bollinger_down = get_bollinger_bands(closing_prices)
    

    plt.title('AAPL' + ' Bollinger Bands')
    plt.xlabel('Days')
    plt.ylabel('Closing Prices')
    plt.plot(df['Adj Close'], label='Closing Prices', c='black')
    plt.plot(df['Bollinger Up'], label='Bollinger Up', c='r')
    plt.plot(df['Bollinger Down'], label='Bollinger Down', c='r')
    plt.plot(df['Keltner Up'], label='Keltner Up', c='b')
    plt.plot(df['Keltner Down'], label='Keltner Down', c='b')
    plt.legend()
    plt.show()