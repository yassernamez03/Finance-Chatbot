import numpy as np
from functions import *
from stock import *
from keras.models import load_model
import prediction
import pandas as pd
from coinmarketcapapi import CoinMarketCapAPI
from datetime import datetime
cmc = CoinMarketCapAPI(api_key='acfb8bea-4917-4cac-85ee-44e8a5d94754')

def Greeting(res,message,user_name):
    user_name = extract_name(message)
    if user_name is not None:
        resp = res.replace("HUMAN",user_name)
        return "{}".format(resp),user_name
    else:
        resp = res.replace("HUMAN","My Friend")
        return "{}".format(resp),None
    
def CurrentHumanQuery(res,user_name):
    if user_name is not None:
        resp = res.replace("HUMAN",user_name)
        return "{}".format(resp)
    else:
        resp = res.replace("HUMAN","My friend")
        return "{}".format(resp)
    
def TimeQuery():
    time = datetime.now().strftime("%H:%M:%S")
    return " It's {} AM".format(time)

def DateQuery():
    time = datetime.now().strftime("%Y-%m-%d")
    return " Today is {}".format(time)

def Definitions(message):
    defn = extract_info(message)[0]
    error = ''  
    item = Search(defn)         
    try:
        rep = cmc.cryptocurrency_info(symbol=item.upper())
        description = rep.data[item.upper()][0]['description']
    except :
        error = 'Unvalid search please give me the correct crypto symbol'
    if error != '':
        return '{}'.format(error)
    else: 
        reply  =  "Ok! here is the Definition of {} 🔍: <br/>".format(item)
        return reply + ("          {}".format(' '.join(description.split()[:-7])))
        
def stock_LIST(res,tag):
    if tag == "STOCK LIST":
        lit = GetStocks()
        return res.replace('list',' 🔸 '.join(lit))

    elif tag == "FOREX LIST":
        lit = GetForex()
        return res.replace('list',' 🔸 '.join(lit))

    elif tag == "CRYPTO LIST":
        lit = GetCrypto()
        return res.replace('list',' 🔸 '.join(lit))

def analyze(message):
    defn = extract_item_analyze(message)
    symbol = Search(defn) 
    
    if not(symbol):
            return "Are you sure this stock name exist?"
    else:
        output = f"🔍 {symbol.upper()} ANALYSIS:<br/>"
        res = pd.DataFrame(GetStockData(Search(symbol.upper()), '1day'))
        MACD = "UPTREND" if prediction.macd_signal(res)==1 else ("UNSURE" if prediction.macd_signal(res)==0 else "DOWNTREND")
        output += (f"1️ MACD (Moving average convergence/divergence) Indicates that {symbol.upper()} is in a {MACD} position.<br/>")
        BB = "UPTREND" if prediction.calculate_bollinger_bands(res)==1 else ("UNSURE" if prediction.calculate_bollinger_bands(res)==0 else "DOWNTREND")
        output += (f"2️ BB (Bollinger Bands) Indicates that {symbol.upper()} is in a {BB} position.<br/>")
        RSI = "OVERBOUGHT, it's likely to have a downstream" if prediction.calculate_rsi(res, 14)==-1 else ("UNSURE" if prediction.calculate_rsi(res, 14)==0 else "OVERSOLD, it's likely to have an upstream🚀")
        output += (f"3️ RSI (Relative strength index) Indicates that {symbol.upper()} is {RSI}.<br/>")
        if symbol not in GetCrypto():
            MAV = "BULLISH position and you may consider buying or holding📈" if prediction.moving_average_analysis(res)==1 else "BEARISH position and you may consider selling or holding📉" 
            output += (f"4️ Moving Averages and Volume Analysis Indicates that {symbol.upper()} is in a {MAV}.")

        return output

def ploting(message):
    defn = extract_item_plot(message)
    symbol = Search(defn) 
    if not(symbol):
        return "Are you sure this stock name exist?"
    else:
        data = pd.DataFrame(GetStockData(Search(symbol), '1day'))

        # Create dictionary with function outputs
        output_dict = {'High': data["High"].tolist(),
                    'Open': data["Open"].tolist(),
                    'Close': data["Close"].tolist(),
                    'Low': data["Low"].tolist(),
                    'Volume': data["Volume"].tolist(),
                    'Date': data["Date"].tolist()}

        # Convert dictionary to BSON document
        json_doc = json.dumps(output_dict)
        
        img = CandleStick(symbol, data["High"], data["Open"], data["Close"], data["Low"], data["Volume"], data["Date"])
        return img