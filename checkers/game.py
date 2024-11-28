# Questo script contiene la rappresentazione astratta del gioco della dama e delle sue regole, indipendente
# da tutti gli altri files. Questo, teoricamente, permetterà anche ad un'intelligenza artificiale di giocare
import pygame
from .constants import BLACK, WHITE, BLUE, SQUARE_SIZE
from .board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
        
        
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
    
    
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = BLACK
        #self.turn_counter = 0
        self.valid_moves = {}
        
    
    def winner(self):
        return self.board.winner()
    
    
    def reset(self):
        self._init()
    
    
    def select(self, row, col):
        """Sulla base dell'oggetto selezionato e dello stato del gioco, fa qualcosa di diverso:
        - se self.selected non è vuoto, allora qualcosa è stato selezionato, quindi la selezione viene resettata in modo da poter selezionare qualcos'altro
        - se self.selected è vuoto, allora la selezione deve ancora avvenire, quindi, una volta selezionata una pedina, si aggiorna self.selected ed il dizionario delle mosse valide

        Args:
            row (Int): riga dell'oggetto selezionato
            col (Int): colonna dell'oggetto selezionato
        """
        
        # Se qualche oggetto è stato selezionato
        if self.selected:
            # Proviamo a muoverlo nella casella selezionata
            result = self._move(row, col)
            
            # Se non ci riusciamo, resettiamo la selezione e selezioniamo qualcos'altro chiamando nuovamente select() (ma questa volta, self.selected è uguale a None)
            if not result:
                self.selected = None
                self.select(row, col)
    
        # Altrimenti, selezioniamo un'altra casella
        piece = self.board.get_piece(row, col)
        
        # Se la casella contiene una pedina ed il suo colore è lo stesso del giocatore che deve muovere in questo turno, self.selected diventa quella stessa pedina
        # e il dizionario delle mosse valide in base alla selezione, viene aggiornato 
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True # selezione valida
    
        return False # selezione non valida


    def _move(self, row, col):
        """Sposta la pedina selezionata nella posizione desiderata

        Args:
            row (Inte): riga in cui spostare la pedina
            col (Int): colonna in cui spostare la pedina
        """

        # In questo momento, self.selected è la pedina da spostare, mentre piece sarebbe la casella in cui spostarla
        piece = self.board.get_piece(row, col)

        # Se la casella destinazione non contiene alcuna pedina e lo spostamento è effettivamente valido, allora sposta la pedina nella posizione desiderata        
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            
            if skipped:
                self.board.remove(skipped)

            self.change_turn()
        
        else:
            return False
        
        return True
    
    
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    
    
    def change_turn(self):
        # self.turn_counter += 1
        
        self.valid_moves = {}
        if self.turn == BLACK:
            self.turn == WHITE
        
        else:
            self.turn == BLACK