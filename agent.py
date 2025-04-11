import streamlit as st
import numpy as np

class AgentTrader:
    def __init__(self, env): 
        self.env = env
        self.max_stock_market = env.max_stock_market
        self.portefeuille = st.session_state.portefeuille


    def can_trade(self, action, quantities, price_stock_market):
        if action == "Buy" and self.portefeuille["n_stock_market"] + self.portefeuille["n_stock_market"] <= self.max_stock_market and \
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

    def calculate_reward(self, can_trade, action):
        # Gain immédiat du portefeuille
        reward = self.portefeuille["history_total"][-1] - self.env.portefeuille["history_total"][-2]
        self.portefeuille["history_gain"].append(reward)

        if reward > 0:
            # Capital supérieur à la limite de perte
            if self.portefeuille["total"] > self.env.profit_limit:reward += 50
            else:reward += 5
        elif reward < 0:
            if self.portefeuille["total"] < self.env.loss_limit:reward -= 50
            else:reward -= 0.5

        else:reward -= 1
        if not can_trade:reward -= 5
        if action =="Hold" and self.portefeuille["history_action"][-1] == "Hold":
            reward -= abs(self.portefeuille["history_reward"][-1])*0.5
            print("Hold action : ", reward)
                
        self.portefeuille["history_action"].append(action)
        self.portefeuille["history_reward"].append(reward)

        return reward