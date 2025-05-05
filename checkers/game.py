# Questo script contiene la rappresentazione astratta del gioco della dama e delle sue regole, indipendente
# da tutti gli altri files. Questo, teoricamente, permetterà anche ad un'intelligenza artificiale di giocare
import pygame
from .constants import BLACK, WHITE, BLUE, SQUARE_SIZE
from .board import Board

class Game:
    def __init__(self, win=None):
        self._init()
        self.window = win
        
        
    def update(self):
        """
        Aggiorna la scacchiera e la sua rappresentazione interna e la disegna a schermo
        """
        if self.window is None:
            return
    
        self.board.draw(self.window)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
    
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        #self.turn_counter = 0
        self.valid_moves = {}
        
    
    def winner(self):
        return self.board.winner()
    
    
    def reset(self):
        self._init()
    
    
    def select(self, row, col):
        """
        Sulla base dell'oggetto selezionato e dello stato del gioco, fa qualcosa di diverso.

        Args:
            row (Int): riga della casella selezionata
            col (Int): colonna della casella selezionata
        """
        
        # Se una pedina risulta precedentemente selezionata
        if self.selected:
            # Si prova a muoverla nella casella appena selezionata
            result = self._move(row, col)
            
            # Se questo non è possibile, la selezione viene resettata e la funzione viene chiamata nuovamente (con la differenza che questa volta, self.selected è uguale a None)
            if not result:
                self.selected = None
                self.select(row, col)
    
        # Altrimenti, salviamo il contenuto della casella appena cliccata
        piece = self.board.get_piece(row, col)

        # Calcolo di tutte le mosse disponibili per il giocatore
        player_moves, _ = self.board.get_valid_moves_player(self.turn)

        # Filtra tutte le mosse che prevedono catture
        capture_moves = {pos: moves for pos, moves in player_moves.items() if any(moves.values())}

        if piece != 0 and piece.color == self.turn:
            # Se esistono catture obbligatorie
            if capture_moves:
                # E se la pedina selezionata è una delle pedine che catturano, allora è l'unica a cui è concesso muoversi
                if (row, col) in capture_moves.keys():
                    self.selected = piece
                    self.valid_moves = self.board.get_valid_moves_piece(piece)
                    return True
                else:
                    return False
            # Altrimenti, non esistono catture obbligatorie, quindi il giocatore può scegliere liberamente quale mossa giocare
            else:
                # Quindi si vanno a ricalcolare le mosse per la pedina selezionata
                self.selected = piece
                self.valid_moves = self.board.get_valid_moves_piece(piece)
                return True
    
        return False


    def _move(self, row, col):
        """
        Sposta la pedina selezionata nella posizione desiderata

        Args:
            row (Int): riga in cui spostare la pedina
            col (Int): colonna in cui spostare la pedina
        """

        #self.selected è la pedina da spostare, mentre piece sarebbe la casella in cui spostarla
        piece = self.board.get_piece(row, col)

        # Se la casella destinazione è vuota e lo spostamento è effettivamente valido
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            # Allora sposta la pedina nella nuova posizione
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            
            # Se ci sono pedine catturate, le pedine vengono rimosse dal gioco
            if skipped:
                self.board.remove(skipped)
            
            # Il turno passa all'altro giocatore
            self.change_turn()
        
        else:
            return False
        
        return True
    
    
    def draw_valid_moves(self, moves):
        """
        Disegna un marcatore per tutte le mosse ammissibili

        Args:
            moves (Dict): dizionario di mosse disponibili in cui la chiave è una tupla contenente le coordinate (row, col) della casella destinazione,
            mentre il valore è una lista delle eventuali pedine mangiate sul percorso
        """
        for move in moves:
            row, col = move
            pygame.draw.circle(self.window, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    
    
    def change_turn(self):
        """
        Passa il turno all'altro giocatore, svuotando il dizionario di mosse possibili e resettando le selezioni
        """
        self.valid_moves = {}
        self.selected = None
        self.turn = WHITE if self.turn == BLACK else BLACK