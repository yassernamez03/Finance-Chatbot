from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error 
from sklearn.linear_model import LinearRegression
import stock
import numpy as np
import pandas as pd
import json

#Using short Term Moving Average
def moving_average_analysis(dff, short_term=50):
    # Calculate the short-term moving averages
    dff['Short_MA'] = dff['Close'].rolling(short_term).mean()
    dff['Long_MA'] = dff['Close'].rolling(200).mean()
        
     # Determine the trend direction based on the moving averages
    dff['Trend'] = 'Sideways'
    dff.loc[dff['Short_MA'] > dff['Long_MA'], 'Trend'] = 'Up'
    dff.loc[dff['Short_MA'] < dff['Long_MA'], 'Trend'] = 'Down'
    
    # Get last Trend Volume
    LastTrendCount = 0
    LastTrendVolume = 0
    LastTrendLabel = dff.iloc[-1]['Trend']
    for i in range(len(dff)-1, -1, -1):
        if dff.iloc[i]['Trend']==LastTrendLabel:
            LastTrendVolume+=dff.iloc[i]['Volume']
            LastTrendCount+=1
        else:
            break
            
    LastTrendVolumeMean = LastTrendVolume/LastTrendCount
    
    LatestVolumeMean = dff['Volume'].iloc[len(dff)-LastTrendCount-30:len(dff)-LastTrendCount].mean()
    
    VolumeFactor = "IS Likely to continue" if LatestVolumeMean<LastTrendVolumeMean else "ISN'T Likely to continue"
    
    return (("UPTREND" if dff['Close'].iloc[-1]>dff['Short_MA'].iloc[-1] else "DOWNTREND"), VolumeFactor)

def calculate_rsi(dff, window):
    # Calculate the price change for each day
    delta = dff['Close'].diff()

    # Define the up and down days
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)

    # Calculate the average gain and loss over the specified window
    avg_gain = up.rolling(window=window).mean()
    avg_loss = down.rolling(window=window).mean()

    # Calculate the relative strength
    rs = avg_gain / avg_loss

    # Calculate the RSI
    rsi = 100 - (100 / (1 + rs))
        
    return 1 if rsi.iloc[-1]<=30 else (-1 if rsi.iloc[-1]>=70 else 0)

def calculate_bollinger_bands(dff, window_size=20, num_std=2):
    """
    Calculate the upper and lower Bollinger Bands for the given data.
    Returns the upper and lower bands as Pandas Series.
    """
    # Calculate rolling mean and standard deviation
    rolling_mean = dff['Close'].rolling(window=window_size).mean()
    rolling_std = dff['Close'].rolling(window=window_size).std()

    # Calculate upper and lower bands
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)

    # Determine trend direction based on current price
    current_price = dff['Close'].iloc[-1]
    
    #print(current_price, upper_band.iloc[-1], lower_band.iloc[-1])
    
    if current_price > upper_band.iloc[-1]:
        trend_direction = 1
    elif current_price < lower_band.iloc[-1]:
        trend_direction = -1
    else:
        trend_direction = 0

    return trend_direction

#Used by macd_signal()
def calculate_macd(dff, fast_period=12, slow_period=26, signal_period=9):
    exp1 = dff['Close'].ewm(span=fast_period, adjust=False).mean()
    exp2 = dff['Close'].ewm(span=slow_period, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    histogram = macd - signal
    return pd.DataFrame({'MACD': macd, 'Signal': signal, 'Histogram': histogram})

def macd_signal(stock_price, fast_period=12, slow_period=26, signal_period=9):
    macd_data = calculate_macd(stock_price, fast_period, slow_period, signal_period)
    last_macd = macd_data['MACD'].iloc[-1]
    last_signal = macd_data['Signal'].iloc[-1]
    prev_macd = macd_data['MACD'].iloc[-2]
    prev_signal = macd_data['Signal'].iloc[-2]
    
    if last_macd > last_signal and prev_macd <= prev_signal:
        return 1
    elif last_macd < last_signal and prev_macd >= prev_signal:
        return -1
    else:
        return 0

def candlestick_with_moving_averages(stock_data, short_term=50, long_term=200):
    # Calculate the short-term and long-term moving averages
    stock_data['Short_MA'] = stock_data['Close'].rolling(short_term).mean()
    stock_data['Long_MA'] = stock_data['Close'].rolling(long_term).mean()

    # Determine the trend direction based on the moving averages
    stock_data['Trend'] = 'Sideways'
    stock_data.loc[stock_data['Short_MA'] > stock_data['Long_MA'], 'Trend'] = 'Up'
    stock_data.loc[stock_data['Short_MA'] < stock_data['Long_MA'], 'Trend'] = 'Down'

    CandleStick(H, O, C, L, V, D, stock_data['Short_MA'], stock_data['Long_MA'], df['Close'])

    return stock_data

def PredictionSVR(symbol, days):
    #Getting Stock Data from API
    df = pd.DataFrame(stock.GetStockData(symbol, "1day"))
    H, O, C, L, V, D = df["High"], df["Open"], df["Close"], df["Low"], df["Volume"], df["Date"]
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date_delta'] = (df['Date'] - df['Date'].min())  / np.timedelta64(1,'D') #TIME=>DELTA TIME
    #Training/Test Sets
    train_features, test_features, train_labels, test_labels = train_test_split(df['Date_delta'].values.reshape(-1, 1), df['Close'].values, test_size=0.33, random_state=42)
    #Adjusting Sets
    scaler = StandardScaler()
    train_features = scaler.fit_transform(train_features)
    test_features = scaler.transform(test_features)
    #Defining SVR Algorithm
    svr = SVR(kernel='rbf', C=1e3, gamma=.1, epsilon=.1)
    svr.fit(train_features, train_labels)
    #Predicting
    predictions = svr.predict(test_features)
    test_features = [[float(df['Date_delta'].iloc[-1]+i)] for i in range(days+1)]
    test_features = scaler.transform(test_features)
    pred = svr.predict(test_features)
    #Loss Function & Accuracy
    loss = mean_absolute_error(test_labels, predictions)
    rmse = np.sqrt(mean_squared_error(test_labels, predictions))
    #Plotting
    #stock.LinePlot(df['Date_delta'],np.arange(len(test_features)), (pred, 'Predictions'))
    # Create dictionary with function outputs
    output_dict = {'predictions': pred.tolist(),
                   'test_features': np.arange(len(test_features)).tolist(),
                   'loss': loss,
                   'rmse': rmse}

    # Convert dictionary to BSON document
    json_doc = json.dumps(output_dict)
    
    return [np.arange(len(test_features)), pred, loss, rmse]

def factor(*args):
    print(args)