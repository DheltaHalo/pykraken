# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 13:27:11 2021

@author: DheltaHalo
"""
from datetime import datetime
import pandas as pd
import numpy as np
import requests
import json
from time import sleep
import openpyxl
import sys
from shutil import copyfile

import os

def par_mean(l: list, parity: int = 1):
    l_l = len(l)
    l: list = [parity*x for x in l if parity*x > 0]

    m = sum(l)/l_l
    
    return m

def remove(sheet):
  # iterate the sheet by rows
  for row in sheet.iter_rows():
  
    # all() return False if all of the row value is None
    if not all(cell.value for cell in row):
  
      # detele the empty row
      sheet.delete_rows(row[0].row, 1)
  
      # recursively call the remove() with modified sheet data
      remove(sheet)
  
      return
def kraken_download(symbol, timeframe):
    """
    Descarga los datos de kraken para un part específico y un timeframe
    específico y lo organiza en un diccionario

    Parameters
    ----------
    symbol: str, Par de criptomonedas
    
    timeframe: int, Timeframe que quieres ver 

    Returns
    -------
    crypto_data: dict, Diccionario con toda la información que se ha descargado

    """
    try:
        # Accedemos a los datos para un par en una franja de tiempo croncreta
        
        pair_split: list = symbol.split('/')
        symbol: str = pair_split[0] + pair_split[1]
    
        url: str = f'https://api.kraken.com/0/public/OHLC?pair={symbol}&interval={timeframe}'
        
        # Creamos un diccionario con todos los datos
        request = requests.get(url)    
        print(request)
        crypto_url: dict = json.loads(request.text)
    
        # Organizamos los datos como mejor nos conviene en un diccionario
            
        crypto_url_code: list = list(crypto_url["result"].keys())[0]
        crypto_data: dict = {"Date": [], "Open": [], "High": [], "Low": [], "Close": []}
        crypto_main: dict = crypto_url["result"][crypto_url_code]
    
        
        for i in crypto_data:
            crypto_data[i]: list = list(np.zeros(len(crypto_main)))
        
        for i in range(len(crypto_main)):
            time = datetime.utcfromtimestamp(crypto_main[i][0] + 3600*2).strftime('%Y-%m-%d %H:%M:%S')
            
            crypto_data["Date"][i]: str = time        
            crypto_data["Close"][i]: float = float(crypto_main[i][4])
    
        return crypto_data
    
    except KeyError:
        time = 10
        print("\nHa habido un problema al contactar con kraken, en " + \
              f"{time} segundos lo intentaré de nuevo")
        sleep(time)
        

def RSI(crypto_data: dict):
    # RSI calculo
    rsi_candle = 14
    close: list = crypto_data["Close"]
    

    gain_loss_list, avg_up, avg_down, rsi_list = list(np.zeros(len(close))), \
        list(np.zeros(len(close))), list(np.zeros(len(close))), list(np.zeros(len(close)))
    
    for i in range(1, len(close)):
        gain_loss_list[i] = close[i]-close[i-1]     
    
    for i in range(rsi_candle, len(close)):
        value = gain_loss_list[i]
        if i == rsi_candle:
            avg_up[i] = par_mean(gain_loss_list[1:rsi_candle + 1])
            avg_down[i] = par_mean(gain_loss_list[1: rsi_candle + 1], -1)

        else:
            if value > 0:
                avg_up[i] = (avg_up[i - 1] * (rsi_candle - 1) + value) / rsi_candle
                avg_down[i] = (avg_down[i - 1] * (rsi_candle - 1) + 0) / rsi_candle
            else:
                avg_down[i] = (avg_down[i - 1] * (rsi_candle - 1) - value) / rsi_candle
                avg_up[i] = (avg_up[i - 1] * (rsi_candle - 1) + 0) / rsi_candle
            
        try:
            rsi_list[i] = 100 - 100/(1 + avg_up[i]/avg_down[i])

        except ZeroDivisionError:
            rsi_list[i] = rsi_list[i - 1]
    
    return rsi_list[-1]

def main(par: str, path: str, exit_key: str):        
    par = par.split(",")
    pair = [x.replace(" ", "") for x in par]
    print()
                
    times = [1, 5, 15, 30, 60, 240]
    
    head = []
    rsi_a = {}
    
    for i in times:
        if i%60 == 0:
            if ((i%60)%24 == 0 and i/60 >= 24):
                head.append(str(int(i/60/24))+"d")
            else:
                head.append(str(int(i/60))+"h")
        else:
            head.append(str(int(i))+"m")

    refresh_time = 2

    while True:
        time_left = len(pair)*len(times)*refresh_time
        
        for i in range(len(pair)):
            rsi_a[pair[i]] = list(np.zeros(len(times)))
            for k in range(len(times)):
                try:
                    rsi_a[pair[i]][k] = RSI(kraken_download(pair[i], times[k]))

                except TypeError:
                    rsi_a[pair[i]][k] = 0

        df = pd.DataFrame(rsi_a, index = head)
        filename = '\data\\rsi_data.xlsx' 
        filename2 = '\data\\rsi_placeholder.xlsx' 

        src = path+filename
        dst = path+filename2

        df.T.to_excel (src, index = pair)
        
        copyfile(src, dst)
        
        if exit_key == "STOP":
            break
        
        sleep(60)




    
    

        


                                   
                                   