import streamlit as st
import numpy as np

class AgentTrader:
    def __init__(self, env): 
        self.env = env
        self.max_stock_market = env.max_stock_market
        self.portefeuille = st.session_state.portefeuille


    def can_trade(self, action, quantities, price_stock_market):
        if action == "Buy" and self.portefeuille["n_stock_market"] + quantities <= self.max_stock_market and \
            price_stock_market * quantities <= self.portefeuille["capital"]:
            return True
        elif action == "Sell" and self.portefeuille["n_stock_market"] - quantities >= 0:
            return True
        elif action == "Hold":
            return True
        return False
    

    def execute_trade(self, action, quantities, price_stock_market):
        if action == "Buy":
            self.portefeuille["capital"] -= price_stock_market * quantities
            self.portefeuille["n_stock_market"] +=  quantities
            self.in_position = True
    
        elif action == "Sell":
            self.portefeuille["capital"] += price_stock_market * quantities
            self.portefeuille["n_stock_market"] -=  quantities
        
        elif action == "Hold":
            quantities = 0