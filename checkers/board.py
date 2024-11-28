import pygame
from .constants import DUSK_DARK, DUSK_LIGHT, WHITE, BLACK, SQUARE_SIZE, ROWS, COLS
from .piece import Piece


class Board:
    """
    Si occupa del movimento delle pedine, la loro rimozione, la creazione della scacchiera sullo schermo ecc.
    """
    def __init__(self):
        # self.board: lista bidimensionale 8x8 che conterrà lo stato delle pedine sulla scacchiera
        self.board = []
        
        # self.black_left: pedine nere rimanenti
        # self.white_left: pedine bianche rimanenti
        self.black_left = self.white_left = 12

        # self.black_kings: dame nere presenti
        # self.white_kings: dame bianche presenti
        self.black_kings = self.white_kings = 0
        
        # Rappresentazione interna della scacchiera
        self.create_board()
    
    
    def draw_squares(self, win):
        """Disegna le caselle della scacchiera

        Args:
            win (Surface): finestra in cui disegnare la scacchiera
        """

        # Background (caselle scure)
        win.fill(DUSK_DARK)
        
        # Caselle chiare
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                # Disegna la casella nella finestra win:
                # - usa il colore DUSK_LIGHT
                # - row*SQUARE_SIZE e col*SQUARE_SIZE sono le coordinate del vertice in alto a sinistra della casella da disegnare
                # - la dimensione delle caselle è  SQUARE_SIZExSQUARE_SIZE 
                pygame.draw.rect(win, DUSK_LIGHT, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


    def move(self, piece, row, col):
        """Sposta la pedina selezionato nella posizione desiderata

        Args:
            piece (Piece): pedina da spostare
            row (Int): riga in cui spostare la pedina
            col (Int): colonna in cui spostare la pedina
        """
        
        # Invertiamo la posizione della pedina che vogliamo muovere e di ciò che si trova nella casella IN CUI vogliamo muoverla
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        
        # Se la casella si trova nella prima o nell'ultima riga, diventa una dama
        if row == 0 or row == ROWS-1:
            piece.make_kings()
            
            # Aggionrna i contatori di dame in base al colore della pedina
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.black_kings += 1
    
    
    def get_piece(self, row, col):
        """Prende in input le coordinate della casella e restituisce l'oggetto che si trova in quella posizione

        Args:
            row (Int): riga dell'oggetto da restituire
            col (Int): colonna dell'oggetto da restituire
        """

        return self.board[row][col]


    def create_board(self):
        """Crea la rappresentazione interna della scacchiera e aggiunge le pedine
        """
        for row in range(ROWS):
            # Una lista per ogni riga
            self.board.append([])
            for col in range(COLS):
                # Sostanzialmente:
                # - sulle righe di indice pari, la pedina viene disegnata nelle colonne di indice dispari
                # - sulle righe di indice dispari, la pedina viene disegnata nelle colonne di indice pari
                if col % 2 == ((row + 1) % 2):
                    # Nelle prime tre righe vengono disegnate le pedine bianche
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    
                    # Nelle ultime tre righe, vengono disegnate le pedine nere
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BLACK))
                    
                    # Nelle righe centrali, non disegniamo pedine ma aggiungiamo uno 0 nella rappresentazione interna della scacchiera
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
    
    
    def draw(self, win):
        """Crea sia le caselle che le pedine

        Args:
            win (Surface): finsetra di gioco
        """
        self.draw_squares(win)
        
        for row in range(ROWS):
            for col in range(COLS):
                
                # Itera sulla rappresentazione interna della scacchiera e disenga le pedine nelle rispettive posizioni
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)


    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == BLACK:
                    self.black_left -= 1
                else:
                    self.white_left -= 1


    def winner(self):
        if self.black_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return BLACK
        
        return None 



    def get_valid_moves(self, piece):
        # Dizionario contenente le mosse ammissibili:
        # - chiave: tupla di coordinate casella in cui ci si muove
        # - valore: lista di pedine (o caselle vuote) da scavalcare (e rimuovere) per arrivare nella casella indicata dalla chiave
        moves = {}
        
        # Coordinate delle mosse
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        
        # Queste condizioni controllano il movimento
        # Se la pedina è nera o è una dama, può muoversi verso l'alto
        # - start: row-1 permette di salire sulla scacchiera
        # - stop: quanto "lontano" cercare è max(row-3, -1) (il -1 serve per non andare oltre il limite superiore della scacchiera.
        #   Dato che partiamo da row-1, stiamo guardando due caselle in avanti, in cui possiamo:
        #       - trovare una casella vuota nella prima casella disponibile
        #       - trovare una pedina nella prima casella disponibile. Se è una pedina avversaria, bisogna cosa c'è in quella ancora dopo, in modo da capire se è possibile mangiare o meno
        # - step: -1 per muoversi in alto
        #  
        if piece.color == BLACK or piece.king:
            moves.update(self._traverse_left(row-1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row-1, max(row-3, -1), -1, piece.color, right))
        
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row+1, max(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row+1, max(row+3, ROWS), 1, piece.color, right))
        
        
        return moves

    
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        """Controlla le mosse disponibili nella diagonale sinistra della pedina

        Args:
            start (int): prima riga a partire dalla quale cercare le mosse disponibili
            stop (int): quanto "lontano" cercare le mosse
            step (int): di quanto muoversi
            color (Tuple): colore della pedina
            left (int): indice della colonna a sinistra della pedina
            skipped (list, optional): insieme di pedine incontrate (e da rimuovere) nel percorso di quella mossa. Defaults to [].
        """
        
        moves = {}
        last = []
        
        for r in range(start, stop, step):
            if left < 0:
                break
    
            current = self.board[r][left]
            
            # Se è stata trovata una casella vuota
            if current == 0:
                
                # Se abbiamo saltato qualcosa, abbiamo trovato una casella vuota ma non abbiamo altro da saltare, non possiamo muoverci lì RIVEDERE SEZIONE CENTRALE VIDEO PARTE 3
                if skipped and not last:
                    break
                
                # Altrimenti, ci sono pedine che sono state saltate quindi stiamo creando una sorta di coda di pedine avversarie da mangiare e da rimuovere dal gioco
                elif skipped:
                    moves[(r, left)] = last + skipped
                
                # Altrimenti, l'ultima mossa individuata è valida quindi viene aggiunta al dizionario
                else:
                    moves[(r, left)] = last
                
                
                # Chiamata ricorsiva
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
            
                    moves.update(self._traverse_left(r+step, row, step, color, left-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1, skipped=last))
                break
            
            # Altrimenti, se la casella non è vuota ma contiene una pedina dello stesso colore di quella che si sta muovendo,
            # non lo si può muovere quindi non si aggiunge quella alla lista delle possibili mosse
            elif current.color == color:
                break
            
            # Altrimenti, la pedina trovata è del colore opposto quindi ci si può muovere ASSUMENDO che la casella successiva è vuota
            else:
                last = [current]

            left -= 1
    
        return moves
    
    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        """Controlla le mosse disponibili nella diagonale sinistra della pedina

        Args:
            start (int): prima riga a partire dalla quale cercare le mosse disponibili
            stop (int): quanto "lontano" cercare le mosse
            step (int): di quanto muoversi
            color (Tuple): colore della pedina
            right (int): indice della colonna a sinistra della pedina
            skipped (list, optional): insieme di pedine incontrate (e da rimuovere) nel percorso di quella mossa. Defaults to [].
        """
        
        moves = {}
        last = []
        
        for r in range(start, stop, step):
            if right >= COLS:
                break
    
            current = self.board[r][right]
            
            # Se è stata trovata una casella vuota
            if current == 0:
                
                # Se abbiamo saltato qualcosa, abbiamo trovato una casella vuota ma non abbiamo altro da saltare, non possiamo muoverci lì RIVEDERE SEZIONE CENTRALE VIDEO PARTE 3
                if skipped and not last:
                    break
                
                # Altrimenti, ci sono pedine che sono state saltate quindi stiamo creando una sorta di coda di pedine avversarie da mangiare e da rimuovere dal gioco
                elif skipped:
                    moves[(r, right)] = last + skipped
                
                # Altrimenti, l'ultima mossa individuata è valida quindi viene aggiunta al dizionario
                else:
                    moves[(r, right)] = last
                
                
                # Chiamata ricorsiva
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
            
                    moves.update(self._traverse_left(r+step, row, step, color, right-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1, skipped=last))
                break
            
            # Altrimenti, se la casella non è vuota ma contiene una pedina dello stesso colore di quella che si sta muovendo,
            # non lo si può muovere quindi non si aggiunge quella alla lista delle possibili mosse
            elif current.color == color:
                break
            
            # Altrimenti, la pedina trovata è del colore opposto quindi ci si può muovere ASSUMENDO che la casella successiva è vuota
            else:
                last = [current]

            right += 1
    
        return moves    