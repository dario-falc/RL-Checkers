import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random
from checkers.game import Game
from checkers.constants import BLACK, WHITE, SQUARE_SIZE

class CheckersEnv(gym.Env):
    def __init__(self):
        super(CheckersEnv, self).__init__()
        self.game = Game(None)  # Inizializza il gioco senza una finestra grafica
        self.turn = BLACK  # Inizia il gioco con il giocatore nero
        
        # Spazi di azione
        self.action_space = spaces.Discrete(64 * 64)  # Ogni mossa è una coppia di caselle (da_row, da_col, a_row, a_col)
        
        # Spazio di osservazione (rappresentazione della scacchiera)
        self.observation_space = spaces.Box(low=0, high=2, shape=(8, 8), dtype=np.int32)
    
    def reset(self):
        """
        Reset del gioco: la scacchiera e gli stati vengono riportati al valore iniziale.
        """
        self.game.reset()
        self.turn = BLACK
        return self.get_observation()
    
    def step(self, action):
        """
        Esegui un'azione (sposta un pezzo da una casella all'altra) e restituisci lo stato successivo.
        
        Args:
            action (int): Azione rappresentata da un numero che indica il movimento.
        """
        # Decodifica dell'azione
        from_row = (action // 64)  # Calcola la riga di partenza
        from_col = action % 64  # Calcola la colonna di partenza
        
        # Trova la mossa corrispondente (row, col) -> (row_dest, col_dest)
        valid_moves = self.game.board.get_valid_moves_player(self.turn)
        possible_moves = valid_moves.get((from_row, from_col), {})

        if not possible_moves:
            return self.get_observation(), -1, True, {}  # Mossa non valida, l'agente perde

        # Scegli una mossa casuale valida
        move = random.choice(list(possible_moves.keys()))
        row_dest, col_dest = move
        
        # Esegui la mossa
        valid = self.game.select(from_row, from_col)
        if valid:
            self.game._move(row_dest, col_dest)

        # Calcola la ricompensa
        reward = self.calculate_reward()

        # Verifica se il gioco è finito
        done = self.is_done()

        # Passa il turno all'altro giocatore
        self.game.change_turn()

        return self.get_observation(), reward, done, {}

    def render(self):
        """
        Visualizza lo stato attuale del gioco (se necessario).
        """
        pass  # Poiché non abbiamo una finestra grafica, non è necessario renderizzare

    def get_observation(self):
        """
        Restituisce la rappresentazione della scacchiera come una matrice 8x8.
        """
        board = np.zeros((8, 8), dtype=np.int32)
        
        for row in range(8):
            for col in range(8):
                piece = self.game.board.get_piece(row, col)
                if piece != 0:
                    board[row, col] = 1 if piece.color == WHITE else 2  # Rappresentazione dei pezzi bianchi (1) e neri (2)
        
        return board
    
    def calculate_reward(self):
        """
        Calcola la ricompensa per l'agente, basata sullo stato attuale del gioco.
        """
        winner = self.game.winner()
        if winner == BLACK:
            return 1  # Ricompensa per vincere
        elif winner == WHITE:
            return -1  # Penalità per perdere
        else:
            return 0  # Ricompensa neutra in caso di pareggio o partita in corso
    
    def is_done(self):
        """
        Controlla se il gioco è finito.
        """
        return self.game.winner() is not None
