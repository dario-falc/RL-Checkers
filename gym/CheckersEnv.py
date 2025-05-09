import numpy as np
from checkers.game import Game
from checkers.piece import Piece
from checkers.constants import BLACK, WHITE

class CheckersEnv:
    def __init__(self):
        self.game = Game(None)
        self.board = self.game.board
        self.done = False


    def reset(self):
        self.game.reset()
        self.board = self.game.board
        self.done = False
        return self.get_state()


    def step(self, action, capture_move_exists):
        # Decodifica l'azione in coordinate        
        from_row = action[0][0] # Riga di partenza
        from_col = action[0][1] # Colonna di partenza
        to_row = action[1][0] # Riga di arrivo
        to_col = action[1][1] # Colonna di arrivo
        
        # Muove la pedina
        self.game.select(from_row, from_col)  # Seleziona la pedina da muovere
        self.game.select(to_row, to_col) # Seleziona la casella di arrivo

        # Il reward è +100 per vittoria, -100 per sconfitta, +10 per mosse con catture, -1 per mossa senza catture, -0.5 se l'agente sta perdendo
        reward = 0

        if capture_move_exists:
            reward += 10            # +10 se l'agente cattura
        else:
            reward -= 1             # -1 se l'agente non cattura
        
        if self.game.board.black_left < self.game.board.white_left:
            reward -= 0.5           # -0.5 se l'agente sta perdendo
        
        if self.game.winner() == BLACK:
            reward += 100           # +100 se l'agente ha vinto
            self.done = True
        
        elif self.game.winner() == WHITE:
            reward -= 100
            self.done = True        # -100 se l'agente ha perso
        
        return self.get_state(), reward, self.done


    def board_to_state(self, board):
        state = []
        for row in board.board:
            for piece in row:
                if piece is None:
                    state.append(0)
                else:
                    try:
                        val = 1 if piece.color == BLACK else 2
                        if piece.king:
                            val += 2
                    except AttributeError:
                        # Se piece è già un int
                        val = piece
                    state.append(val)
        return state


    def get_state(self):
        state = self.board_to_state(self.board)
        return tuple(state)  # Converte la lista in tupla perché le tuple sono hashable e possono essere usate come chiavi in un dizionario


    def set_state(self, next_state):
        for i, val in enumerate(next_state):
            row = i // 8
            col = i % 8
            #print(f"i:{i}, val:{val}\n")
            if val == 0:
                self.board.board[row][col] = 0
            elif val == 1:
                self.board.board[row][col] = Piece(row, col, BLACK)
            elif val == 2:
                self.board.board[row][col] = Piece(row, col, WHITE)
            
            if val == 3:
                self.board.board[row][col] = Piece(row, col, BLACK)
                piece = self.board.get_piece(row, col)
                piece.make_king()
            
            elif val == 4:
                self.board.board[row][col] = Piece(row, col, WHITE)
                piece = self.board.get_piece(row, col)
                piece.make_king()
        
        #print(f"Stato scacchiera:")
        #for item in self.board.board:
        #    print(item)
        #print("\n")
    