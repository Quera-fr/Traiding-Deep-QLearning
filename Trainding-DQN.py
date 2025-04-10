import streamlit as st
from agent import *
from environment import *
from Dashborad import *


st.set_page_config(page_title="DQN Trading Bot", page_icon=":money_with_wings:", layout="wide")
st.title("DQN Trading Bot")


env = EnvTrading()
trader = AgentTrader(env=env)

sidebar_settings()
if not st.sidebar.checkbox("Show Portefeuille"):
    show_portefeuille(trader)
st.sidebar.button("Reset", on_click=lambda: st.session_state.clear())



with st.form('action_form', border=True):
    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns(2)

    with col1 : action = st.selectbox("Achat ou vente", options=["Buy", "Sell", "Hold"])
    with col2 : quantities = st.slider("Nombre d'actions", 1, 50, 1)
    with col3 : price_stock_market = st.slider("Prix de l'action", 0.0, 1000.0, 18.5)
        
    if st.form_submit_button("Submit") and trader.can_trade(action, quantities, price_stock_market):
        trader.execute_trade(action, quantities, price_stock_market)
        env.update_portefeuille(action, quantities, price_stock_market)
        hiden_portefeuille = True
        show_portefeuille(trader)



if st.button("Start Trading"):
    # Demarrage de l'agent du cycle de trading
    env.get_state()
    
    for step in range(10):
        env.portefeuille["current_step"] = step
        price_stock_market = env.portefeuille["current_states"]['Next_Close'].iloc[step]
        action = env.actions[np.random.randint(0, 3)]
        quantities = 1

        
        can_trade = trader.can_trade(action, quantities, price_stock_market)
        if can_trade:
            trader.execute_trade(action, quantities, price_stock_market)
            st.success("Action: %s, Quantities: %d" % (action, quantities))
        else:
            st.error("Action impossible. Veuillez vérifier les paramètres.")

        env.update_portefeuille(action, quantities, price_stock_market)
        env.update_state(can_trade)
    show_portefeuille(trader)



if st.button('Show Curent State'):
    st.write(env.portefeuille["current_states"])