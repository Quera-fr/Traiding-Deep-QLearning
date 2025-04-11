import streamlit as st



def show_portefeuille(trader):
    a, b, c = st.columns(3)
    d, e, f = st.columns(3)

    a.metric("Sold en espèces", trader.portefeuille["capital"], "$2000", border=True)

    b.metric("Valeur des action", trader.portefeuille["n_stock_market"] * trader.portefeuille["price_stock_market"], "$2000", border=True, )
    c.metric("Titre au portefeuille", trader.portefeuille["n_stock_market"], "$1000", border=True)

    d.metric("Total", trader.portefeuille["total"], "$1000", border=True)
    e.metric("Profit/Perte", trader.portefeuille["profit"], "$2000", border=True)
    f.metric("Dernière valeur de l'action", trader.portefeuille["price_stock_market"], "$2000", border=True)


def sidebar_settings(agent, env):
    
    st.sidebar.subheader("Settings")

    if st.sidebar.checkbox("Show Portefeuille"):
        show_portefeuille(agent)
    
    if st.sidebar.checkbox("Manual Trading"):
        with st.form('action_form', border=True):
            col1, col2, col3 = st.columns(3)
            col4, col5 = st.columns(2)

            with col1 : action = st.selectbox("Achat ou vente", options=["Buy", "Sell", "Hold"])
            with col2 : quantities = st.slider("Nombre d'actions", 1, 50, 1)
            with col3 : price_stock_market = st.slider("Prix de l'action", 0.0, 1000.0, 18.5)
                
            if st.form_submit_button("Submit") and agent.can_trade(action, quantities, price_stock_market):
                agent.execute_trade(action, quantities, price_stock_market)
                env.update_portefeuille(action, quantities, price_stock_market)
                hiden_portefeuille = True
                show_portefeuille(agent)

    


    
    if st.sidebar.checkbox("Show settings"):
        st.sidebar.write("Set the parameters for the trading bot.")
        capital = st.sidebar.number_input("Capital initial", 0, 10000, 1000)
        n_stock_market = st.sidebar.number_input("Nombre d'actions initial", 0, 1000, 0)
        price_stock_market = st.sidebar.number_input("Cout initial de l'action", 0.0, 1000.0, 17.5)
        max_stock_market = st.sidebar.number_input("Nombre maximum d'actions", 0, 100, 10)
        loss_limit = st.sidebar.number_input("Limite de perte", 0, 10000, 500)
        profit_limit = st.sidebar.number_input("Limite de profit", 0, 10000, 5000)
        window_size = st.sidebar.number_input("Taille de la fenetre", 1, 100, 10)

        return {
            "capital": capital,
            "n_stock_market": n_stock_market,
            "price_stock_market": price_stock_market,
            "max_stock_market": max_stock_market,
            "loss_limit": loss_limit,
            "profit_limit": profit_limit,
            "window_size": window_size
        }
    
    st.sidebar.button("Reset", on_click=lambda: st.session_state.clear())
    if st.sidebar.button('Show Curent State'):
        st.write(env.portefeuille["current_states"])
    