import requests
import os
import re

def sendMail(target, subject, message): 
    url = "https://rapidprod-sendgrid-v1.p.rapidapi.com/mail/send"

    payload = {
        "personalizations": [
            {
                "to": [{"email": target}],
                "subject": subject
            }
        ],
        "from": {"email": "StockSensei@bot.ai"},
        "content": [
            {
                "type": "text/html",
                "value": message
            }
        ]
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "01859bbbdbmsh5ef4be697540182p16dee3jsnd363a79130f7",
        "X-RapidAPI-Host": "rapidprod-sendgrid-v1.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    
import yfinance as yf
import numpy as np
import datetime
import requests
import json


def extract_info(input_):
    search_sentences =  ["what's",'what is', 'tell me about', 'define','what can you say about',"meaning of",'is']

    search_sentences.sort(key=len, reverse=True)

    index = -1
    indexs = []
    for sentence in search_sentences:
        if sentence in input_:
            index = input_.find(sentence)+len(sentence)
            indexs.append(index)
            
    words = []
    if index != -1:
        for index in indexs:
            new_string = input_[index:]
            word = new_string.split()[0].strip()
            words.append(word)
    return words

def extract_item_predict(input_):
    sentences =  ["predict",'predictions about',"can you predict"]

    sentences.sort(key=len, reverse=True)
    if len(input_.split()) == 1:
        return input_.split()[0].strip() 
    else:
        index = -1
        for sentence in sentences:
            if sentence.lower() in input_:
                index = input_.find(sentence)+len(sentence) 
                
        if index != -1:
            new_string = input_[index:]
            word = new_string.split()[0]
            return word
        else:
            return None
        
def extract_item_plot(input_):
    sentences =  ["plot",'represent','show','draw']

    sentences.sort(key=len, reverse=True)
    if len(input_.split()) == 1:
        return input_.split()[0].strip() 
    else:
        index = -1
        for sentence in sentences:
            if sentence.lower() in input_:
                index = input_.find(sentence)+len(sentence) 
                
        if index != -1:
            new_string = input_[index:]
            word = new_string.split()[0]
            return word
        else:
            return None
        
def extract_item_analyze(input_):
    sentences =  ["analyze",'conclude','advise me about','analysis about',"conclusion of"]

    sentences.sort(key=len, reverse=True)
    if len(input_.split()) == 1:
        return input_.split()[0].strip() 
    else:
        index = -1
        for sentence in sentences:
            if sentence.lower() in input_:
                index = input_.find(sentence)+len(sentence) 
                
        if index != -1:
            new_string = input_[index:]
            word = new_string.split()[0]
            return word
        else:
            return None  


def extract_name(input_):
    
    sentences = ['my name is', 'this is', 'you can call me','It is','I am','my username is',"it's"]

    sentences.sort(key=len, reverse=True)
    if len(input_.split()) == 1:
        return input_.split()[0].strip() 
    else:
        index = -1
        for sentence in sentences:
            if sentence.lower() in input_:
                index = input_.find(sentence)+len(sentence) 
                
        if index != -1:
            new_string = input_[index:]
            word = ' '.join(new_string.split()[:1])
            return word
        else:
            return None
        

def GetCrypto():
    url = "https://twelve-data1.p.rapidapi.com/cryptocurrencies"
    querystring = {"format":"json"}
    headers = {
        "X-RapidAPI-Key": "01859bbbdbmsh5ef4be697540182p16dee3jsnd363a79130f7",
        "X-RapidAPI-Host": "twelve-data1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)

    L = []
    cryptos = json.loads(response.text)["data"]
    #print(cryptos)
    for crypto in cryptos:
        L.append(crypto["symbol"])
    return L

def GetForex():
    url = "https://twelve-data1.p.rapidapi.com/forex_pairs"
    querystring = {"format":"json"}
    headers = {
        "X-RapidAPI-Key": "01859bbbdbmsh5ef4be697540182p16dee3jsnd363a79130f7",
        "X-RapidAPI-Host": "twelve-data1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)

    L = []
    forex = json.loads(response.text)["data"]
    for stock in forex:
        L.append(stock["symbol"])
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

def Search(symbol):
    url = 'https://twelve-data1.p.rapidapi.com/symbol_search'
    querystring = {"outputsize":"30","symbol":symbol}
    headers = {
        "X-RapidAPI-Key": "01859bbbdbmsh5ef4be697540182p16dee3jsnd363a79130f7",
        "X-RapidAPI-Host": "twelve-data1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    state = False
    L = []
    try:
        data = json.loads(response.text)["data"]
    except:
        raise Exception("SEARCH: NOT FOUND")
    for e in data:
        L.append(e["symbol"])
    if len(L) == 0:
        return None
    else:
        return list(dict.fromkeys(L))[0]
    
def extract_days(message):
    return str(re.sub(r'day(s)?', '', message)).strip()