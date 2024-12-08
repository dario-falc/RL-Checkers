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
            
            return True
    
        # Altrimenti, selezioniamo un'altra casella
        piece = self.board.get_piece(row, col)

        # Controlla se il giocatore ha mosse obbligatorie (catture)
        all_moves = self.board.get_all_valid_moves(self.turn)  # Usa il nuovo metodo
        capture_moves = {pos: moves for pos, moves in all_moves.items() if any(moves.values())}

        if piece != 0 and piece.color == self.turn:
            if capture_moves:  # Esistono mosse obbligatorie?
                if (row, col) in capture_moves:  # La pedina selezionata può fare una cattura
                    self.selected = piece
                    self.valid_moves = self.board.get_valid_moves(piece)
                    return True
                else:
                    return False  # La pedina selezionata non è tra quelle con catture obbligatorie
            else:
                self.selected = piece
                self.valid_moves = self.board.get_valid_moves(piece)
                return True
    
        return False # selezione non valida


    def _move(self, row, col):
        """Sposta la pedina selezionata nella posizione desiderata

        Args:
            row (Inte): riga in cui spostare la pedina
            col (Int): colonna in cui spostare la pedina
        """

        #self.selected è la pedina da spostare, mentre piece sarebbe la casella in cui spostarla
        piece = self.board.get_piece(row, col)

        # Se la casella destinazione non contiene alcuna pedina e lo spostamento è effettivamente valido, allora sposta la pedina nella posizione desiderata        
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            # Sposta la pedina nella nuova posizione
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]  # Pedine catturate
            
            if skipped:  # Se ci sono catture
                self.board.remove(skipped)
                
            self.change_turn()  # Cambia turno solo se non ci sono più catture
        
        else:
            return False
        
        return True
    
    # tale funzione prevede di disegnare all'interno della cella un punto blu per tutte le mosse che può compiere
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    
    
    def change_turn(self):
        # self.turn_counter += 1
        self.valid_moves = {}  # Azzeriamo le mosse valide
        self.selected = None  # Deselezioniamo qualsiasi pedina
        self.turn = WHITE if self.turn == BLACK else BLACK  # Cambiamo il turno