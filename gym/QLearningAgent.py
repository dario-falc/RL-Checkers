import numpy as np
import random

class QLearningAgent:
    def __init__(self, action_space, learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
        self.action_space = action_space
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.q_table = np.zeros((8, 8, 8, 8, action_space.n))  # Una tabella Q per ogni possibile configurazione della scacchiera
        
    def choose_action(self, state):
        """
        Sceglie un'azione usando epsilon-greedy.
        """
        if random.uniform(0, 1) < self.epsilon:
            return self.action_space.sample()  # Azione casuale (esplorazione)
        else:
            return np.argmax(self.q_table[state])  # Azione migliore (sfruttamento)
        
    def learn(self, state, action, reward, next_state):
        """
        Aggiorna la Q-table con l'algoritmo Q-learning.
        """
        best_next_action = np.argmax(self.q_table[next_state])
        self.q_table[state, action] = (1 - self.learning_rate) * self.q_table[state, action] + \
                                       self.learning_rate * (reward + self.discount_factor * self.q_table[next_state, best_next_action])
