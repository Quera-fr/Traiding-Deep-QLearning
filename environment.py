# Projet Boursier CAC40
import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf
from sklearn.preprocessing import StandardScaler


class EnvTrading:
    def __init__(self, 
                 name_stock="GLE.PA", 
                 capital=500,
                 max_stock_market=15,
                 loss_limit=450, 
                 profit_limit=550, 
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
                "total": capital + n_stock_market * price_stock_market,
                "profit": 0,
                "in_position": False,
                "current_step": 0,
                "current_states" : None,
                "current_perdiod": 0,
                "history": [],
                "history_profit": [],
                "history_reward": [],
                "history_total": [capital + n_stock_market * price_stock_market],
                "history_gain": [],
            }
        
        self.portefeuille = st.session_state.portefeuille
        self.window_size = window_size
        self.n_stock_market = n_stock_market
        self.price_stock_market = price_stock_market
        
        self.actions = {0: 'Hold',1: 'Buy',2: 'Sell'}
        self.capital_initial = capital
        self.loss_limit = loss_limit
        self.profit_limit = profit_limit
        self.max_stock_market = max_stock_market
        self.data_preparation(name_stock, window_size)

    def reset(self):
        self.portefeuille["capital"] = self.capital_initial
        self.portefeuille["n_stock_market"] = 0
        self.portefeuille["price_stock_market"] = 0
        self.portefeuille["total"] = self.capital_initial
        self.portefeuille["profit"] = 0
        self.portefeuille["in_position"] = False
        self.portefeuille["current_step"] = 0
        self.portefeuille["current_states"] = None
        self.portefeuille["current_perdiod"] = 0
        self.portefeuille["history"] = []
        self.portefeuille["history_profit"] = []
        self.portefeuille["history_reward"] = []
        self.portefeuille["history_total"] = [self.capital_initial]
        self.portefeuille["history_action"] = [None]

    def show_data(self):
        st.write(self.df)

    def show_state(self):
         st.write(pd.DataFrame(self.states[self.portefeuille["current_step"]]))

    def data_preparation(self, name_stock, window_size):
        df = yf.Ticker(name_stock).history(period="max")[['Open', 'High', 'Low', 'Close', 'Volume']]
        df['Next_Open'] = df['Open'].shift(-1) # Next day open price
        df['Var'] = ((df['Next_Open'] - df['Close']) / df['Close'] )* 100
        df['Next_Close'] = df['Close'].shift(-1) # Next day close price
        df[['capital', 'total', 'profit',  'n_stock_market', 'can_trade']] = 0
        sc = StandardScaler()
        df[['Open', 'High', 'Low', 'Close', 'Volume']] = sc.fit_transform(df[['Open', 'High', 'Low', 'Close', 'Volume']])
        
        states = [df.iloc[i-window_size:i] for i in range(window_size, len(df))]
        self.states = states
        self.df = df[window_size:]


    def update_portefeuille(self, action, quantities, price_stock_market):
        self.portefeuille["total"] = self.portefeuille["capital"] + self.portefeuille["n_stock_market"] * price_stock_market
        self.portefeuille['history_total'].append(self.portefeuille["total"])
        self.portefeuille["profit"] = self.portefeuille["total"] - self.portefeuille["capital_initial"]
        self.portefeuille["history"].append({"action": action, "quantities": quantities, "price_stock_market": price_stock_market})
        self.portefeuille["price_stock_market"] = price_stock_market
        if self.portefeuille["n_stock_market"] == 0:
                self.portefeuille["in_position"] = False
        else:
            self.portefeuille["in_position"] = True



    def initialize_state(self):
        self.portefeuille["current_perdiod"] = np.random.randint(0, len(self.df)-1)
        self.curent_state = pd.DataFrame(self.states[self.portefeuille["current_perdiod"]])
        self.portefeuille["price_stock_market"] = self.curent_state["Next_Open"].iloc[-1]
        return self.portefeuille["price_stock_market"]

    def get_state(self):
        state = self.states[self.portefeuille["current_perdiod"] + self.portefeuille["current_step"]]
        state = pd.DataFrame(state)
        self.portefeuille["price_stock_market"] = state["Next_Open"].iloc[-1]
        return state


    def update_state(self, can_trade):
        state = self.get_state()

        state["capital"] = self.portefeuille["capital"]
        state["total"] = self.portefeuille["total"]
        state["profit"] = self.portefeuille["profit"]
        state["n_stock_market"] = self.portefeuille["n_stock_market"]
        state["can_trade"] = can_trade
        self.portefeuille["current_states"] = state

        self.portefeuille["history_profit"].append(self.portefeuille["profit"])

        return self.portefeuille["price_stock_market"]
