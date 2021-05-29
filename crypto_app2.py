import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime
# pretty printing of pandas dataframe
pd.set_option('expand_frame_repr', False)  


import streamlit as st


# GET CURRENT PRICE DATA
def get_current_data(from_sym='BTC', to_sym='USD', exchange=''):
    url = 'https://min-api.cryptocompare.com/data/price'    
    
    parameters = {'fsym': from_sym,
                  'tsyms': to_sym }
    
    if exchange:
        print('exchange: ', exchange)
        parameters['e'] = exchange
        
    # response comes as json
    response = requests.get(url, params=parameters)   
    data = response.json()
    
    return data

def get_hist_data(from_sym='BTC', to_sym='USD', timeframe = 'day', limit=2000, aggregation=1, exchange=''):
    
    baseurl = 'https://min-api.cryptocompare.com/data/v2/histo'
    baseurl += timeframe
    
    parameters = {'fsym': from_sym,
                  'tsym': to_sym,
                  'limit': limit,
                  'aggregate': aggregation}
    if exchange:
        print('exchange: ', exchange)
        parameters['e'] = exchange    
    
    #print('baseurl: ', baseurl) 
    #print('timeframe: ', timeframe)
    #print('parameters: ', parameters)
    
    # response comes as json
    response = requests.get(baseurl, params=parameters)   
    
    data = response.json()['Data']['Data'] 
    
    return data


def data_to_dataframe(data):
    #data from json is in array of dictionaries
    df = pd.DataFrame.from_dict(data)
    
    # time is stored as an epoch, we need normal dates
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    #print(df.tail())
    
    return df

def plot_data(df, cryptocurrency, target_currency):
    # got his warning because combining matplotlib 
    # and time in pandas converted from epoch to normal date
    # To register the converters:
    # 	>>> from pandas.plotting import register_matplotlib_converters
    # 	>>> register_matplotlib_converters()
    #  warnings.warn(msg, FutureWarning)
    
    from pandas.plotting import register_matplotlib_converters
    register_matplotlib_converters()
    
    plt.figure(figsize=(15,5))
    plt.title('{} / {} price data'.format(cryptocurrency, target_currency))
    plt.plot(df.index, df.close)
    plt.legend()
    plt.show()
    
    return None

st.write("# Crypto Time")


btime = st.slider("Move slider to decrease/increase data by increments of 10 days", min_value=1, max_value=20, value=12)

#cryptocurrency = 'DOGE'
#target_currency = 'GBP'

data = get_hist_data('DOGE', 'GBP', 'day', 10 * btime)
df_doge = data_to_dataframe(data)

data = get_hist_data('BTC', 'GBP', 'day', 10 * btime)
df_btc = data_to_dataframe(data)

data = get_hist_data('ETH', 'GBP', 'day', 10 * btime)
df_eth = data_to_dataframe(data)

data = get_hist_data('DOT', 'GBP', 'day', 10 * btime)
df_dot = data_to_dataframe(data)

data = get_hist_data('CHZ', 'GBP', 'day', 10 * btime)
df_chz = data_to_dataframe(data)

data = get_hist_data('CAKE', 'GBP', 'day', 10 * btime)
df_cake = data_to_dataframe(data)

doge_current_price = round(get_current_data('DOGE','GBP').get("GBP"),3)

st.write("### Dogecoin DOGE: £" + str(doge_current_price))
st.image("https://www.coinopsy.com/media/img/quality_logo/Dogecoin.png", width=50)


# no_of_coins = 1280
# total_value = round(current_price * no_of_coins, 2)
# profit = round(total_value - 50,2)
# st.write("### Dogecoin: £" + str(current_price) + " Qty: " + str(no_of_coins) + " Balance: £" + str(total_value) + " Profit : £" + str(profit))

plt.style.use('seaborn-whitegrid')
plt.figure(figsize=(8.5, 3.0))

fig, ax = plt.subplots()
#ax.axhline(y=0.038, color='b', linestyle='-')
ax.axvline(pd.Timestamp('2021-02-22'),color='r', label="Purchase point £0.038")
ax.axvline(pd.Timestamp('2021-05-12'),color='g', label="Purchase point £0.3237")
ax.plot(df_doge.close, label='Close Price(GBP)', lw=1)
ax.legend(loc='upper left')
ax.xaxis.set_tick_params(rotation=45, labelsize=8)
ax.yaxis.set_tick_params(labelsize=8)
#ax.label.set_fontsize('x-small')
#ax.tick_params(axis='both', which='minor', labelsize=8)

st.pyplot(fig)

btc_current_price = round(get_current_data('BTC','GBP').get("GBP"),2)

st.write("### Bitcoin BTC: £" + str(btc_current_price))

st.image("https://www.coinopsy.com/media/img/quality_logo/bitcoin-btc.png", width=50)

fig, ax = plt.subplots()
ax.axvline(pd.Timestamp('2021-04-18'),color='r', label="Purchase point £40,403")
ax.axvline(pd.Timestamp('2021-05-25'),color='y', label="Purchase point £27,090")
ax.plot(df_btc.close, label='Bitcoin', lw=1)
ax.legend(loc='upper left')
ax.xaxis.set_tick_params(rotation=45, labelsize=8)
ax.yaxis.set_tick_params(labelsize=8)

st.pyplot(fig)

eth_current_price = round(get_current_data('ETH','GBP').get("GBP"),2)

st.write("### Ethereum ETH: £" + str(eth_current_price))

st.image("https://www.coinopsy.com/media/img/quality_logo/ethereum-eth.png", width=50)

fig, ax = plt.subplots()
ax.axvline(pd.Timestamp('2021-05-12'),color='g', label="Purchase point £2888")
ax.plot(df_eth.close, label='Ethereum', lw=1)
ax.legend(loc='upper left')
ax.xaxis.set_tick_params(rotation=45, labelsize=8)
ax.yaxis.set_tick_params(labelsize=8)

st.pyplot(fig)

dot_current_price = round(get_current_data('DOT','GBP').get("GBP"),2)

st.write("### Polkadot DOT: £" + str(dot_current_price))

st.image("https://www.coinopsy.com/media/img/quality_logo/Polkadot.png", width=50)

fig, ax = plt.subplots()
ax.axvline(pd.Timestamp('2021-05-13'),color='g', label="Purchase point £32.36")
ax.plot(df_dot.close, label='Polkadot', lw=1)
ax.legend(loc='upper left')
ax.xaxis.set_tick_params(rotation=45, labelsize=8)
ax.yaxis.set_tick_params(labelsize=8)

st.pyplot(fig)

chz_current_price = round(get_current_data('CHZ','GBP').get("GBP"),2)

st.write("### Chiliz CHZ: £" + str(chz_current_price))
st.image("https://www.coinopsy.com/media/img/quality_logo/Chiliz.png", width=50)

fig, ax = plt.subplots()
ax.axvline(pd.Timestamp('2021-05-16'),color='r', label="Purchase point £0.33")
ax.axvline(pd.Timestamp('2021-05-15'),color='g', label="Purchase point £0.31")
ax.plot(df_chz.close, label='Chiliz', lw=1)
ax.legend(loc='upper left')
ax.xaxis.set_tick_params(rotation=45, labelsize=8)
ax.yaxis.set_tick_params(labelsize=8)

st.pyplot(fig)

cake_current_price = round(get_current_data('CAKE','GBP').get("GBP"),2)

st.write("### PancakeSwap CAKE: £" + str(cake_current_price))
st.image("https://dynamic-assets.coinbase.com/799c4f94ca16f05804c5856a242a2b105e4170090494c95326ef8178ab7fd716e3558031ede24d056d232e5e953873cbd7776430160960b124d277f6c7a0403c/asset_icons/7125e866d37d0835231d548349e2a8b5e60395f66509edbd84210f2ca1a1b775.png", width=50)

fig, ax = plt.subplots()
ax.axvline(pd.Timestamp('2021-05-15'),color='g', label="Purchase point £22.13")
ax.plot(df_cake.close, label='Pancake Swap', lw=1)
ax.legend(loc='upper left')
ax.xaxis.set_tick_params(rotation=45, labelsize=8)
ax.yaxis.set_tick_params(labelsize=8)

st.pyplot(fig)



#print(get_current_data('BTC','GBP'))