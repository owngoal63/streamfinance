import yfinance as yf
import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from datetime import datetime
from dateutil.relativedelta import relativedelta


def buy_sell_sma(data):
    sigPriceBuy = []
    sigPriceSell = []
    flag = -1
    latest_status = ""  # Initilise variable to hold the latest status ( Buy or Sell)

    for i in range(len(data)):
        if data['SMA30'][i] > data['SMA100'][i]:
            if flag != 1:
                sigPriceBuy.append(data['Daily Close'][i])
                latest_status = "BUY"
                date_latest_status = data.index[i]
                sigPriceSell.append(np.nan)
                flag = 1
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        elif data['SMA30'][i] < data['SMA100'][i]:
            if flag != 0:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(data['Daily Close'][i])
                latest_status = "SELL"
                date_latest_status = data.index[i]
                flag = 0
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        else:
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(np.nan)

    return (sigPriceBuy, sigPriceSell, latest_status, date_latest_status)


def buy_sell_MACD(signal):
    Buy = []
    Sell = []
    flag = -1
    latest_status = ""  # Initilise variable to hold the latest status ( Buy or Sell)

    for i in range(0, len(signal)):
        if signal['MACD'][i] > signal['Signal Line'][i]:
            Sell.append(np.nan)
            if flag != 1:
                Buy.append(signal['Close'][i])
                latest_status = "BUY"
                date_latest_status = data.index[i]
                flag = 1
            else:
                Buy.append(np.nan)
        elif signal['MACD'][i] < signal['Signal Line'][i]:
            Buy.append(np.nan)
            if flag != 0:
                Sell.append(signal['Close'][i])
                latest_status = "SELL"
                date_latest_status = data.index[i]
                flag = 0
            else:
                Sell.append(np.nan)
        else:
            Buy.append(np.nan)
            Sell.append(np.nan)

    return(Buy, Sell, latest_status, date_latest_status)

# Functions for calculating the Simple Moving Average (SMA) and the Exponential Moving Average (EMA)
# Typical time periods for moving averages are 15,20 & 30
#SMA
def SMA(data, period=30, column="Close"):
    return data[column].rolling(window=period).mean()
#EMA
def EMA(data, period=20, column="Close"):
    return data[column].ewm(span=period, adjust=False).mean()

# Function for Moving Average Convergance/Divergance MACD
def MACD(data, period_long=26, period_short=12, period_signal=9, column='Close'):
    ShortEMA = EMA(data, period=period_short, column=column)
    LongEMA = EMA(data, period=period_long, column=column)
    # Calculate and store the MACD inot the data frame
    data['MACD'] = ShortEMA - LongEMA
    # Calculate signal line and store to DF
    data['signal_Line'] = EMA(data, period=period_signal, column='MACD')
    return data

# Create a function for relative strength index (RSI)
def RSI(data, period=14, column='Close'):
    delta = data[column].diff(1)
    delta = delta.dropna()
    up = delta.copy()
    down = delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    data['up'] = up
    data['down'] = down
    AVG_Gain = SMA(data, period, column='up')
    AVG_Loss = abs(SMA(data, period, column='down'))
    RS = AVG_Gain / AVG_Loss
    RSI = 100.0 - (100.0 / (1.0 + RS))

    data['RSI'] = RSI
    return data


st.sidebar.header("NYSE Stock Tickers")
tickerSymbols = st.sidebar.multiselect(
    "Select ticker:",
    ["GME", "GOOGL", "JNJ", "AAPL" ,"MSFT", "AMZN", "FB", "TSLA", "BRK-A", "JPM", "XOM", "BAC", "JPM", "KO", "EBAY", "GILD"],["TSLA"]
)

st.write("""
    # Stock Price App with SMA, MACD Tracking and Movement Predictor Model
    """)

x = st.slider("Move slider to decrease/increase data period in years", min_value=1, max_value=10, value=5) 
start_date = datetime.strftime(datetime.now() - relativedelta(years=x), '%Y-%m-%d')
st.write(x, 'years of data. Start date is ', start_date, '. End date is today. ')

#Chart setup
plt.style.use('fivethirtyeight')
plt.figure(figsize=(12.5, 4.5))
plt.ylabel("Close Price ($)")
#plt.xticks(rotation=45)


for tickerSymbol in tickerSymbols:
    st.write("""---""")

    company_name = yf.Ticker(tickerSymbol).info['longName']
    st.write("### Stock closing prices and volume of " + company_name  )

    tickerData = yf.Ticker(tickerSymbol)
    #tickerDf = tickerData.history(period='1d', start=start_date, end='2021-1-29')
    tickerDf = tickerData.history(period='1d', start=start_date, end=datetime.strftime(datetime.now(), '%Y-%m-%d'))
    
    # Show the dataframe
    st.dataframe(tickerDf)

    # Create the simple moving average with a 30 day window
    SMA30 = pd.DataFrame()
    SMA30['Close'] = tickerDf['Close'].rolling(window=30).mean()
    #st.dataframe(SMA30)

    # Create the simple moving average with a 30 day window
    SMA100 = pd.DataFrame()
    SMA100['Close'] = tickerDf['Close'].rolling(window=100).mean()
    #st.dataframe(SMA100)

    # Plot the data
    fig, ax = plt.subplots()
    #ax.ticklabel_format(useOffset=False, style='plain')
    ax.plot(tickerDf['Close'], label='Close Price($)')
    ax.plot(SMA30['Close'], label = 'SMA30')
    ax.plot(SMA100['Close'], label = 'SMA100')
    ax.legend(loc='upper left')
    ax.xaxis.set_tick_params(rotation=45)

    #st.pyplot(fig)

    # Create new data frame to store all the data
    data = pd.DataFrame()
    data['Daily Close'] = tickerDf['Close']
    data['SMA30'] = SMA30['Close']
    data['SMA100'] = SMA100['Close']
    buy_sell_data = buy_sell_sma(data)
    data['Buy Signal Price'] = buy_sell_data[0]
    data['Sell Signal Price'] = buy_sell_data[1]
    latest_status = buy_sell_data[2]
    date_latest_status = buy_sell_data[3]
    date_latest_status_days_ago = datetime.now() - date_latest_status
    #print(date_latest_status_days_ago)
    # Show the consolidated Dataframe
    #st.dataframe(data)  

    # Visualise the data and the strategy
    fig, ax = plt.subplots()
    ax.plot(data['Daily Close'], label='Daily Close Price ($)', alpha = 0.35)
    ax.plot(data['SMA30'], label='SMA30', alpha = 0.35)
    ax.plot(data['SMA100'], label='SMA100', alpha = 0.35)
    ax.scatter(data.index, data['Buy Signal Price'], label = "Buy", marker='^', color='green')
    ax.scatter(data.index, data['Sell Signal Price'], label = "Sell", marker='v', color='red')
    ax.legend(loc='upper left')
    
    st.pyplot(fig)

    #print(date_latest_status)

    st.write("""Current status of SMA for """ + company_name + """ is """ +
    latest_status + """ set on """ + datetime.strftime(date_latest_status, '%Y-%m-%d')  +
     """ """ + str(date_latest_status_days_ago.days) + """ days ago.""" )

    # Calculate the MACD and signal line indicators
    # Calculate the short term expnential moving average (EMA)
    ShortEMA = tickerDf['Close'].ewm(span=12, adjust=False).mean()
    # Calculate the short term expnential moving average (EMA)
    LongEMA = tickerDf['Close'].ewm(span=26, adjust=False).mean()
    # Calculate the MACD line
    MACD = ShortEMA - LongEMA
    # Calculate the signal line
    signal = MACD.ewm(span=9, adjust=False).mean()
    # Create new columns
    tickerDf['MACD'] = MACD
    tickerDf['Signal Line'] = signal
    # Create the buy and sell columns
    a = buy_sell_MACD(tickerDf)
    tickerDf['Buy_Signal_Price'] = a[0]
    tickerDf['Sell_Signal_Price'] = a[1]
    latest_status = a[2]
    date_latest_status = a[3]
    date_latest_status_days_ago = datetime.now() - date_latest_status
    #st.dataframe(tickerDf)

    # Plot the chart
    fig, ax = plt.subplots()
    ax.plot(tickerDf['Close'], label='Close', color='blue', alpha=0.35)
    ax.scatter(tickerDf.index, tickerDf['Buy_Signal_Price'], label='Buy', color='green', marker='^')
    ax.scatter(tickerDf.index, tickerDf['Sell_Signal_Price'], label='Sell', color='red', marker='v')
    ax.legend(loc='upper left')
    st.pyplot(fig)

    st.write("""Current status of MACD for """ + company_name + """ is """ +
    latest_status + """ set on """ + datetime.strftime(date_latest_status, '%Y-%m-%d')  +
     """ """ + str(date_latest_status_days_ago.days) + """ days ago.""" )

    # ------------------------------------------------------------------------
    #MACD(tickerDf)
    RSI(tickerDf)
    tickerDf['SMA'] = SMA(tickerDf)
    tickerDf['EMA'] = EMA(tickerDf)

    # Create target column ( Is tomorrows price great than todays price?)
    tickerDf['Target'] = np.where(tickerDf['Close'].shift(-1) > tickerDf['Close'], 1, 0)

    # Remove first 29 days of data to get rid of null values
    tickerDf = tickerDf[29:]

    #st.dataframe(tickerDf)

    # Split the data set into a feature or independent data set (X) and a Target or dependent data set (Y)
    keep_columns = ['Close', 'MACD', 'Signal Line', 'RSI', 'SMA', 'EMA']
    X = tickerDf[keep_columns].values
    Y = tickerDf['Target'].values

    # Split the data again into 80% training and 20% testing data sets
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state = 2)

    # Create and traing the decision tree classifier model
    tree = DecisionTreeClassifier().fit(X_train, Y_train)
    # Check how well the model did on the training data set
    #print(company_name + " training accuracy: " + str(tree.score(X_train, Y_train)))
    # Check how well the model did on the test data set
    #print(company_name + " test accuracy: " + str(tree.score(X_test, Y_test)))

    # Show the model tree prediction
    tree_predictions = tree.predict(X_test)
    #print(tree_predictions)
    #print(Y_test)

    # Get the models metrics
    from sklearn.metrics import classification_report
    print(classification_report(Y_test, tree_predictions))

    st.dataframe(tickerDf)

    st.write(company_name + " prediction model accuracy score")
    st.write(" Accuracy Score: " + str(tree.score(X_test, Y_test)))











      



