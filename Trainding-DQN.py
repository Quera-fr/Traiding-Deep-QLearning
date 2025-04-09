import streamlit as st

st.set_page_config(page_title="DQN Trading Bot", page_icon=":money_with_wings:", layout="wide")

st.title("DQN Trading Bot")
st.write("This is a simple DQN trading bot that uses reinforcement learning to trade stocks.")


with st.form('action_form', border=True):
    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns(2)

    with col1 : action = st.selectbox("Traiding Action", options=["Buy", "Sell", "Hold"])
    with col2 : quantities = st.slider("Quatities", 0, 50, 20)
    with col3 : stock_cost = st.slider("Stock Cost", 0, 1000, 100)
        
    if st.form_submit_button("Submit"):
        st.success("Action: %s, Quantities: %d" % (action, quantities))


default_capital = st.sidebar.number_input("Default Capital", 0, 10000, 10000)
default_stock = st.sidebar.number_input("Default R-value", 0, 1000, 1)
default_stock_cost = st.sidebar.number_input("Default Stock Cost", 0, 1000, 100)

a, b = st.columns(2)
c, d = st.columns(2)


a.metric("Sold", "$1000", "$2000", border=True)
b.metric("Bought", "$2000", "$1000", border=True)

c.metric("Profit", "$1000", "$2000", border=True)
d.metric("Loss", "$2000", "$1000", border=True)


