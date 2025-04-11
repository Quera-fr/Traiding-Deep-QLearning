from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM


class Trainer:
    def __init__(self, agent, env, buffer_size=1000, batch_size=32, epochs=10):
        self.buffer_size = buffer_size
        self.batch_size = batch_size
        self.epochs = epochs
        self.memory = []

    def add_to_memory(self, state, action, reward, next_state, done):
        if len(self.memory) > self.buffer_size:
            self.memory.pop(0)
        self.memory.append((state, action, reward, next_state, done))


    def create_model(self, input_shape):
        model = Sequential()
        model.add(LSTM(15, activation='relu', input_shape=input_shape, return_sequences=True))
        model.add(LSTM(15, activation='relu'))
        model.add(Dense(3))
        model.compile(optimizer='adam', loss='mse')
        return model
    