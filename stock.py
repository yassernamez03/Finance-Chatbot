import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import datetime
import plotly.offline as pyo
import plotly.graph_objects as go
import os


def GetCrypto():
    url = "https://twelve-data1.p.rapidapi.com/cryptocurrencies"
    querystring = {"format":"json"}
    headers = {
        "X-RapidAPI-Key": "01859bbbdbmsh5ef4be697540182p16dee3jsnd363a79130f7",
        "X-RapidAPI-Host": "twelve-data1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)

    L = []
    try:
        cryptos = json.loads(response.text)["data"]
    except:
        raise Exception("Requests/min Exceeded.")

    for crypto in cryptos:
        L.append(crypto["symbol"])
    return L

def GetStocks():
    url = "https://twelve-data1.p.rapidapi.com/stocks"

    querystring = {"exchange": 'NASDAQ', "format":"json"}

    headers = {
        "X-RapidAPI-Key": "01859bbbdbmsh5ef4be697540182p16dee3jsnd363a79130f7",
        "X-RapidAPI-Host": "twelve-data1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    try:
        data = json.loads(response.text)["data"]
    except:
        raise Exception("Requests/min Exceeded.")
    
    L = []
    for e in data:
        L.append(e["symbol"])
    
    return list(dict.fromkeys(L)) # Removing Duplicates

def GetForex():
    url = "https://twelve-data1.p.rapidapi.com/forex_pairs"
    querystring = {"format":"json"}
    headers = {
        "X-RapidAPI-Key": "01859bbbdbmsh5ef4be697540182p16dee3jsnd363a79130f7",
        "X-RapidAPI-Host": "twelve-data1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)

    L = []
    try:
        forex = json.loads(response.text)["data"]
    except:
        raise Exception("Requests/min Exceeded.")
        
    for stock in forex:
        L.append(stock["symbol"])
    return list(dict.fromkeys(L)) # Removing Duplicates


def GetStockData(symbol, interval, size=2*365):
        url = "https://twelve-data1.p.rapidapi.com/time_series"

        querystring = {"interval":interval, "symbol":symbol, "format":"json", "outputsize":size}

        headers = {
                "X-RapidAPI-Key": "01859bbbdbmsh5ef4be697540182p16dee3jsnd363a79130f7",
                "X-RapidAPI-Host": "twelve-data1.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        

        H, L, O, C, V, D = [], [], [], [], [], []
        try:
            data = json.loads(response.text)["values"]
        except:
            raise Exception("GETSTOCKDATA: Not Found / Cooldown !")

            
        # Setting Data
        for e in data:
            H.append(e["high"])
            D.append(e["datetime"])
            L.append(e["low"])
            O.append(e["open"])
            C.append(e["close"])
            try:
                V.append(e["volume"])
            except:
                V.append(0)
        
        # Defining Market Capitalization Value for Symbol
        #MC = GetMaretMarketCap(symbol)
                
        #Reversing Lists
        H.reverse()
        L.reverse()
        O.reverse()
        C.reverse()
        D.reverse()
        V.reverse()

        #Converting Data to float-Str
        H = np.array(H).astype(float)
        L = np.array(L).astype(float)
        O = np.array(O).astype(float)
        C = np.array(C).astype(float)
        V = np.array(V).astype(float)
        D = np.array(D).astype(str)
         
        return {"High": H, "Open": O, "Close": C, "Low": L, "Volume": V, "Date": D}

def LinePlot(symbol, D, C, *args):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=D, y=C,
                             line=dict(width=3)))
    for x in args:
        fig.add_trace(go.Scatter(x=D, y=x[0], name= x[1],
                                 line=dict(width=1, dash='dot')))

    fig.update_layout(xaxis_title="Days", yaxis_title="Stock Values", title=f"{symbol.upper()} Predictions")

    #Save Plot
    name = os.urandom(13).hex()
    fig.write_image(f'static/data/{name}.png', width=500, height=500, scale=5)
    
    return name
    

def CandleStick(symbol, H, O, C, L, V, D, *args):
    fig = go.Figure(data=[go.Candlestick(x=D,
                    open=O,
                    high=H,
                    low=L,
                    close=C)])
    fig.update_layout(xaxis_rangeslider_visible=False)
    
    for x in args:
        fig.add_trace(go.Scatter(x=D, y=x, name='Moving Average',
                                 line=dict(width=2)))

    fig.update_layout(xaxis_title="Time", yaxis_title="Stock Values", title=f"{symbol.upper()} Time Series")

    #Save Plot
    name = os.urandom(12).hex()
    fig.write_image(f'static/data/{name}.png', width=500, height=500, scale=5)
    
    return name



