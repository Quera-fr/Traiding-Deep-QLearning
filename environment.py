# Projet Boursier CAC40
import yfinance as yf
import pandas as pd


GLE = yf.Ticker("GLE.PA")
df = GLE.history(period="max")
df

states = [df.iloc[i-10:i][['Open', 'High', 'Low', 'Close', 'Volume']].values.flatten() for i in range(10, len(df))]



class TradingEnv:
    def __init__(self, df, states, soldes=1000):
        self.soldes = soldes
        self.current_step = 0
        self.state = states
        self.done = False
        self.actions = {
            0: 'Hold',
            1: 'Buy',
            2: 'Sell'
        }
        self.capital = 0
        self.in_position = False
        self.buy_price = 0

    def get_states(self):
        return self.state[self.current_step]
    
    def step(self, action):
        # action = 0: Hold, 1: Buy, 2: Sell
        if action == 1 and self.soldes > 0:
            self.soldes -= self.state[self.current_step][3]
            self.in_position = True
            self.buy_price = self.state[self.current_step][3]
            self.capital += self.state[self.current_step][3]
        elif action == 2 and self.in_position:
            price_sell = self.state[self.current_step][3]  # close price
            profit = price_sell - self.buy_price
            reward = profit / self.buy_price  # reward is the profit percentage
        else:
            reward = 0

        self.current_step += 1
        if self.current_step >= len(self.state) - 1:
            self.done = True
        return self.state[self.current_step], self.done, {}
    
    def reset(self):
        self.soldes = 1000
        self.current_step = 0
        self.done = False
        return self.state[self.current_step]
    

    def render(self, action):
        print(f"Step: {self.current_step}, Soldes: {self.soldes}, Action: {self.actions[action]}")
        if self.done:
            print("Fin de l'épisode")
        else:
            print(f"Prochain état: {self.state[self.current_step]}")

    def close(self):
        print("Environnement fermé")

    def get_soldes(self):
        return self.soldes
    
    