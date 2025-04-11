import streamlit as st
from agent import *
from environment import *
from Dashborad import *
from train import *
import random
from tensorflow.keras.models import load_model

st.set_page_config(page_title="DQN Trading Bot", page_icon=":money_with_wings:", layout="wide")
st.title("DQN Trading Bot")

env = EnvTrading()
agent = AgentTrader(env=env)
trainer = Trainer(agent=agent, env=env)


sidebar_settings(agent, env)

episodes = st.sidebar.slider("Nombre d'épisodes", 1, 1000, 20)
epsilon = st.sidebar.slider("Epsilon", 0.0, 1.0, 0.3)

if st.sidebar.button("Start Trading"):

    for period in range(episodes):

        # Demarrage de l'agent du cycle de trading
        env.reset()

        price_stock_market = env.initialize_state()
        can_trade = True
        quantities = 1
        st.subheader(f"Portefeuille initial - {str(period)}ème période")
        
        if period == 0:
            try:model = load_model("./model.h5")
            except:model = trainer.create_model(input_shape=env.get_state().drop(["Next_Open"], axis=1).shape)
        
        for step in range(episodes):
            # Mise à jour de l'état de l'environnement
            env.portefeuille["current_step"] = step
            price_stock_market = env.update_state(can_trade)

            curent_state = env.portefeuille["current_states"].drop(["Next_Close"], axis=1).values
            curent_state = np.array([np.array(curent_state, dtype=np.float32)])

            # Action de l'agent

            if np.random.rand() <= epsilon: # Exploration
                id_action = np.random.randint(0, len(env.actions))
                action = env.actions[id_action]
                st.write(f"Action aléatoire: {action}, Quantité: {quantities}, Prix: {price_stock_market}, Capital: {env.portefeuille['capital']}, Total: {env.portefeuille['total']}")
            else:# Prédiction de l'action
                id_action = np.argmax(model.predict(curent_state, verbose=0)[0])
                action = env.actions[id_action]
                st.write(f"Action: {action}, Quantité: {quantities}, Prix: {price_stock_market}, Capital: {env.portefeuille['capital']}, Total: {env.portefeuille['total']}")

            # Exécution de l'action
            can_trade = agent.can_trade(action, quantities, price_stock_market)
            if can_trade:agent.execute_trade(action, quantities, price_stock_market)

            # Mise à jour du portefeuille
            env.update_portefeuille(action, quantities, price_stock_market)
            next_state = env.portefeuille["current_states"].drop(["Next_Close"], axis=1).values
            next_state = np.array([np.array(next_state, dtype=np.float32)])

            # Calcul de la récompense
            reward = agent.calculate_reward(can_trade, action)

            trainer.add_to_memory(curent_state, id_action, reward, next_state, can_trade)
            train_batch  = random.sample(trainer.memory ,  min(len(train_batch ), trainer.batch_size))

        # Entraînement du modèle
        for state, id_action, rewards, next_state, dones in train_batch : 
        
            target = model.predict(state, verbose=0)[0]
            target_next = model.predict(next_state, verbose=0)[0]

            target[id_action] = rewards + 0.5*np.amax(target_next)
            #print(target), print(target_next),print(rewards)
            model.fit(state, np.array([target], dtype=np.float32), epochs=1, verbose=1)

        model.save("model.h5")

        st.subheader("Portefeuille actuel")
        show_portefeuille(agent)
            
        # Affichage de l'historique des profits
        st.subheader("Historique des profits")
        st.line_chart(env.portefeuille["history_profit"])

        # Affichage de l'historique des récompenses
        st.subheader("Historique des récompenses")
        st.line_chart(env.portefeuille["history_reward"])
    