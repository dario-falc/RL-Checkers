import numpy as np
import pickle
import random

from checkers.constants import WHITE

class QLearningAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.99, epsilon=1.0, epsilon_decay=0.995, min_epsilon=0.1):
        self.q_table = {}  # Usa dizionario: (state, action) -> valore Q
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon


    # Prende il valore Q per un dato stato e azione
    def get_q(self, state, action):
        return self.q_table.get((state, action), 0.0)


    def learn(self, state, action, reward, next_state, env):
        """
        Aggiorna il valore Q usando il metodo standard del Q-learning.
        """
        
        old_value = self.get_q(state, action)
        
        # Passa al prossimo stato
        env.set_state(next_state)
        
        valid_next_actions, _ = self.get_valid_actions(env)
        
        # Se ci sono azioni valide nel prossimo stato, calcola il valore Q massimo tra di esse
        if valid_next_actions:
            next_max = max([self.get_q(next_state, a) for a in valid_next_actions])
        else:
            next_max = 0
    
        # Formula Q-learning
        new_value = (1 - self.learning_rate) * old_value + self.learning_rate * (reward + self.discount_factor * next_max)
        
        # Aggiorna la Q-table
        self.q_table[(state, action)] = new_value


    def choose_action(self, state, env):
        valid_actions, capture_move_exists = self.get_valid_actions(env)

        if not valid_actions:
            return None  # Nessuna azione valida, gioco finito o errore

        if random.random() < self.epsilon:
            # Esplorazione: azione casuale tra quelle valide
            return random.choice(valid_actions), capture_move_exists
        
        else:
            # Sfruttamento: azione con Q-value più alto
            # q_value contiene delle tuple (action, q_value)
            q_values = [(action, self.get_q(state, action)) for action in valid_actions]

            # max_q contiene il valore Q più alto tra le azioni valide
            # siccome q_values è una tupla ed il q_value è il secondo elemento, si usa una lambda function per estrarre il secondo elemento
            max_q = max(q_values, key=lambda x: x[1])[1]
            
            # best_actions contiene tutte le azioni con il valore Q più alto (se ce ne sono multiple con lo stesso q_value)
            best_actions = [a for a, q in q_values if q == max_q]
            
            return random.choice(best_actions), capture_move_exists


    #def save_q_table(self, filename):
    #    with open(filename, 'wb') as f:
    #        pickle.dump(self.q_table, f)


    def load_q_table(self, filename):
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)


    def get_valid_actions(self, env):
        """
        Ottiene tutte le azioni valide per lo stato corrente dell'ambiente.
        Un'azione è una tupla: ((start_row, start_col), (end_row, end_col))
        """
        player_moves, capture_move_exists = env.board.get_valid_moves_player(env.game.turn)
        actions = []
        for start_pos, moves in player_moves.items():
            for end_pos in moves.keys():
                actions.append((start_pos, end_pos))
        return actions, capture_move_exists
