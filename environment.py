# Projet Boursier CAC40
import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf


class EnvTrading:
    def __init__(self, 
                 name_stock="GLE.PA", 
                 capital=1000,
                 max_stock_market=10,
                 loss_limit=500, 
                 profit_limit=5000, 
                 window_size=10,
                 n_stock_market=0, 
                 price_stock_market=17.5
                 ):

        if "portefeuille" not in st.session_state:
            st.session_state.portefeuille = {
                "capital": capital,
                "capital_initial": capital,
                "n_stock_market": n_stock_market,
                "price_stock_market": price_stock_market,
                "history": [],
                "total": capital + n_stock_market * price_stock_market,
                "profit": 0,
                "in_position": False,
                "current_step": 0,
            }
        
        self.portefeuille = st.session_state.portefeuille
        
        self.actions = {0: 'Hold',1: 'Buy',2: 'Sell'}
        self.loss_limit = loss_limit
        self.profit_limit = profit_limit
        self.max_stock_market = max_stock_market
        self.data_preparation(name_stock, window_size)


    def data_preparation(self, name_stock, window_size):
        df = yf.Ticker(name_stock).history(period="max")[['Open', 'High', 'Low', 'Close', 'Volume']]
        df['Var'] = df['Open'].shift(-1) # Next day open price
        df['Var'] = ((df['Var'] - df['Close']) / df['Close'] )* 100
        df['Next_Close'] = df['Close'].shift(-1) # Next day close price
        df[['capital', 'total', 'profit',  'n_stock_market', 'can_trade']] = 0
        states = [df.iloc[i-window_size:i] for i in range(window_size, len(df))]
        self.states = states
        self.df = df[window_size:]


    def show_data(self):
        st.write(self.df)

    def show_state(self):
         st.write(pd.DataFrame(self.states[self.portefeuille["current_step"]]))

    def get_state(self):
        self.portefeuille["current_perdiod"] = np.random.randint(0, len(self.df)-1)
        state = self.states[self.portefeuille["current_perdiod"]]
        self.portefeuille["current_states"] =  pd.DataFrame(state)
        return self.portefeuille["current_states"]
         

    def update_portefeuille(self, action, quantities, price_stock_market):
        self.portefeuille["current_step"] += 1
        self.portefeuille["total"] = self.portefeuille["capital"] + self.portefeuille["n_stock_market"] * price_stock_market
        self.portefeuille["profit"] = self.portefeuille["total"] - self.portefeuille["capital_initial"]
        self.portefeuille["history"].append({"action": action, "quantities": quantities, "price_stock_market": price_stock_market})
        self.portefeuille["price_stock_market"] = price_stock_market
        if self.portefeuille["n_stock_market"] == 0:
                self.portefeuille["in_position"] = False
        else:
            self.portefeuille["in_position"] = True

    def update_state(self, can_trade):
        step = self.portefeuille["current_step"]
        self.portefeuille["current_states"]["capital"].iloc[step] = self.portefeuille["capital"]
        self.portefeuille["current_states"]["total"].iloc[step] = self.portefeuille["total"]
        self.portefeuille["current_states"]["profit"].iloc[step] = self.portefeuille["profit"]
        self.portefeuille["current_states"]["n_stock_market"].iloc[step] = self.portefeuille["n_stock_market"]
        self.portefeuille["current_states"]["can_trade"].iloc[step] = can_trade
