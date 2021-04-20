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

st.write("# Ciara's crypto canine money maker!")

st.image("https://owngoal63.pythonanywhere.com/media/images/Blueboy.png", caption="Blueboy is keeping an eye on this rival!", width=100)


btime = st.slider("Move slider to decrease/increase data in periods of 10 days", min_value=1, max_value=20, value=10)

#cryptocurrency = 'DOGE'
#target_currency = 'GBP'

data = get_hist_data('DOGE', 'GBP', 'day', 10 * btime)
df_doge = data_to_dataframe(data)

data = get_hist_data('BTC', 'GBP', 'day', 10 * btime)
df_btc = data_to_dataframe(data)

#plot_data(df, cryptocurrency, target_currency)
st.image("https://cdn.vox-cdn.com/thumbor/lddh05MIQrPTx2QL93RLRGZHfEM=/21x0:539x345/920x613/filters:focal(21x0:539x345):format(webp)/cdn.vox-cdn.com/assets/3727699/Dogecoin_logo.png", width=100)



current_price = round(get_current_data('DOGE','GBP').get("GBP"),3)
no_of_coins = 1280
total_value = round(current_price * no_of_coins, 2)
profit = round(total_value - 50,2)
st.write("### Dogecoin: £" + str(current_price) + " Qty: " + str(no_of_coins) + " Balance: £" + str(total_value) + " Profit : £" + str(profit))

plt.style.use('seaborn-whitegrid')
plt.figure(figsize=(12.5, 4.5))

fig, ax = plt.subplots()
#ax.axhline(y=0.038, color='b', linestyle='-')
ax.axvline(pd.Timestamp('2021-02-22'),color='r', label="Purchase point £0.038")
ax.plot(df_doge.close, label='Close Price(GBP)', lw=1)
ax.legend(loc='upper left')
ax.xaxis.set_tick_params(rotation=45, labelsize=8)
ax.yaxis.set_tick_params(labelsize=8)
#ax.label.set_fontsize('x-small')
#ax.tick_params(axis='both', which='minor', labelsize=8)

st.pyplot(fig)

st.write("# vs Bitcon")

fig, ax = plt.subplots()
ax.plot(df_btc.close, label='Bitcoin', lw=1)
ax.legend(loc='upper left')
ax.xaxis.set_tick_params(rotation=45, labelsize=8)
ax.yaxis.set_tick_params(labelsize=8)

st.pyplot(fig)



#print(get_current_data('BTC','GBP'))