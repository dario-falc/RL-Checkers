import pygame
from .constants import DUSK_DARK, DUSK_LIGHT, WHITE, BLACK, SQUARE_SIZE, ROWS, COLS
from .piece import Piece


class Board:
    """
    Si occupa del movimento delle pedine, del calcolo delle mosse, della loro rimozione, della creazione della scacchiera sullo schermo ecc.
    """
    def __init__(self):
        # self.board: lista bidimensionale 8x8 che conterrà la rappresentazione dello stato del gioco
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
        """
        Disegna le caselle della scacchiera

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
                # - la dimensione delle caselle è SQUARE_SIZExSQUARE_SIZE
                pygame.draw.rect(win, DUSK_LIGHT, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


    def move(self, piece, row, col):
        """
        Sposta la pedina selezionato nella posizione desiderata

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
            piece.make_king()
            
            # Aggionrna i contatori di dame in base al colore della pedina
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.black_kings += 1
    
    
    def get_piece(self, row, col):
        """
        Prende in input le coordinate della casella e restituisce l'oggetto che si trova in quella posizione

        Args:
            row (Int): riga dell'oggetto da restituire
            col (Int): colonna dell'oggetto da restituire
        """

        return self.board[row][col]


    def create_board(self):
        """
        Crea la rappresentazione interna della scacchiera e aggiunge le pedine
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
        """
        Crea sia le caselle che le pedine

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
        """
        Rimuove dal gioco le pedine nella lista ricevuta in input ed aggiorna i contatori in base al loro colore

        Args:
            pieces (List): Lista di pedine di rimuovare dal gioco
        """
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == BLACK:
                    self.black_left -= 1
                else:
                    self.white_left -= 1


    def winner(self):
        """
        Se le pedine di un giocatore finiscono, la partita termina
        """
        if self.black_left <= 0:
            return "Winner: WHITE"
        elif self.white_left <= 0:
            return "Winner: BLACK"
        
        return None 

    
    def get_valid_moves_player(self, color):
        """
        Calcola tutte le mosse valide per tutte le pedine di un determinato colore.
        
        Args:
            color (Tuple): Il colore delle pedine per cui calcolare le mosse valide.
        
        Returns:
            Dict: dizionario di mosse disponibili in cui la chiave è una tupla contenente le coordinate (row, col) della casella in cui si trova la pedina da muvoere,
            mentre il valore è a sua volta un dizionario contenente le mosse disponibili per quella pedina (vedi get_valid_moves_piece())
        """
        
        # Dizionario di mosse valide per il giocatore di turno
        player_moves = {}

        # Calcolo delle mosse
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if piece != 0 and piece.color == color:
                    # Se la pedina è del colore desiderato, aggiunge tutte le mosse di quella pedina al dizionario di mosse di quel giocatore
                    moves = self.get_valid_moves_piece(piece)
                    if moves:
                        player_moves[(row, col)] = moves

        #print(player_moves)
        return player_moves
    

    def get_valid_moves_piece(self, piece):
        """
        Calcola tutte le mosse valide per la pedina ricevuta in input

        Args:
            piece (Piece): pedina di cui calcolare le mosse

        Returns:
            Dict: dizionario di mosse disponibili in cui la chiave è una tupla contenente le coordinate (row, col) della casella destinazione
            ed il valore è una lista contenente eventuali pedine mangiate con quella mossa
        """

        moves = {}
        
        
        # Coordinate a partire dalle quali cercare delle mosse
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        # A seconda del colore della pedina oppure se è una dama, si cercano le mosse disponibili  
        if piece.color == BLACK or piece.king:
            left_moves_dict = self._traverse_left(row-1, max(row-3, -1), -1, piece.color, left)
            right_moves_dict = self._traverse_right(row-1, max(row-3, -1), -1, piece.color, right)
            
            moves.update(self._get_valid_moves(left_moves_dict, right_moves_dict))
            
        
        if piece.color == WHITE or piece.king:
            left_moves_dict = self._traverse_left(row+1, min(row+3, ROWS), 1, piece.color, left)
            right_moves_dict = self._traverse_right(row+1, min(row+3, ROWS), 1, piece.color, right)
            
            moves.update(self._get_valid_moves(left_moves_dict, right_moves_dict))

        return moves
    
    
    def _get_valid_moves(self, left_moves_dict, right_moves_dict):
        """
        Prende in input i dizionari delle mosse disponibili nelle diagonali destra e sinsitra e le filtra opportunamente

        Args:
            left_moves_dict (Dict): mosse nella diagonale sinistra
            right_moves_dict (Dict): mosse nella diagonale destra

        Returns:
            Dict: dizionario di mosse disponibili in cui la chiave è una tupla contenente le coordinate (row, col) della casella destinazione,
            mentre il valore è una lista delle eventuali pedine mangiate sul percorso
        """
        moves = {}
        to_return = {}
        
        # max_length_capture: tiene traccia della cattura più lunga, in modo che se c'è una cattura multipla, la rende obbligatoria e impedisce di non catturare tutte le pedine
        max_length_capture = None
        
        # Controlla la diagonale sinistra.
        for move in left_moves_dict.values():
            # Se ci sono catture, vengono aggiunte alla lista di mosse
            if move:
                moves.update(left_moves_dict)
                if max_length_capture == None or max_length_capture < len(move):
                    max_length_capture = len(move)
        
        # Controlla la diagonale destra.
        for move in right_moves_dict.values():
            # Se ci sono catture, vengono aggiunte alla lista di mosse
            if move:
                moves.update(right_moves_dict)
                if max_length_capture == None or max_length_capture < len(move):
                    max_length_capture = len(move)
        
        # Se non ci sono catture possibili, tutte le altre mosse sono ammesse
        if not moves:
            moves.update(left_moves_dict)
            moves.update(right_moves_dict)
        
        to_return = moves.copy()
        
        # Se ci sono catture e se sono di lunghezze diverse, scarta tutte ad eccezione delle più lunghe
        for key, move in moves.items():
            if max_length_capture and len(move) < max_length_capture:
                to_return.pop(key)
                
        return to_return
        
    

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        """
        Controlla le mosse disponibili nella diagonale sinistra della pedina

        Args:
            start (Int): prima riga a partire dalla quale cercare le mosse disponibili
            stop (Int): quanto "lontano" cercare le mosse
            step (Int): di quanto muoversi (positivo per le pedine bianche, negativo per le nere)
            color (Tuple): colore della pedina
            left (Int): indice della colonna a sinistra della pedina
            skipped (List, optional): insieme di pedine incontrate (e da rimuovere) nel percorso di quella mossa. Defaults to [].
        """
        
        moves = {}
        last = []
        
        for r in range(start, stop, step):
            # Se la colonna a sinistra è il bordo, non è possibile andare oltre
            if left < 0:
                break
    
            current = self.board[r][left]
            
            # Se è stata trovata una casella vuota
            if current == 0:
                
                # Se abbiamo mangiato qualcosa ma la casella successiva è vuota, non c'è altro da mangiare in quella direzione
                if skipped and not last:
                    break
                
                # Altrimenti, ci sono pedine che sono state mangiate quindi aggiungiamo la pedina alla lista di pedine da mangiare e da rimuovere dal gioco
                elif skipped:
                    moves[(r, left)] = last + skipped
                
                # Altrimenti, non ci sono pedine da mangiare quindi l'ultima mossa individuata è valida quindi viene aggiunta al dizionario
                else:
                    moves[(r, left)] = last
                
                
                # Se è possibile mangiare una pedina, effettua una chiamata ricorsiva per vedere se è possibile effettuare mangiate multiple
                if last:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS)
            
                    moves.update(self._traverse_left(r+step, row, step, color, left-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1, skipped=last))
            
                break
            
            # Altrimenti, se la casella non è vuota ma contiene una pedina dello stesso colore di quella che si sta muovendo,
            # non lo si può muovere quindi non si aggiunge quella alla lista delle possibili mosse
            elif current.color == color:
                break
            
            # Altrimenti, la pedina trovata è del colore opposto quindi viene salvata e alla prossima iterazione si andrà a controllare
            # se la casella che la segue è vuota in modo da capire se è possibile catturarla
            else:
                last = [current]
            
            
            # Oltre a controllare la riga successiva, bisogna cambiare anche colonna, quindi si va ulteriormente verso sinistra
            left -= 1
    
        return moves
    
    
    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        """
        Controlla le mosse disponibili nella diagonale destra della pedina

        Args:
            start (Int): prima riga a partire dalla quale cercare le mosse disponibili
            stop (Int): quanto "lontano" cercare le mosse
            step (Int): di quanto muoversi (positivo per le pedine bianche, negativo per le nere)
            color (Tuple): colore della pedina
            right (Int): indice della colonna a destra della pedina
            skipped (List, optional): insieme di pedine incontrate (e da rimuovere) nel percorso di quella mossa. Defaults to [].
        """
        
        moves = {}
        last = []
        
        for r in range(start, stop, step):
            if right >= COLS:
                break
    
            current = self.board[r][right]
            
            # Se è stata trovata una casella vuota
            if current == 0:
                
                # Se abbiamo mangiato qualcosa ma la casella successiva è vuota, non c'è altro da mangiare in quella direzione
                if skipped and not last:
                    break
                
                # Altrimenti, ci sono pedine che sono state mangiate quindi aggiungiamo la pedina alla lista di pedine da mangiare e da rimuovere dal gioco
                elif skipped:
                    moves[(r, right)] = last + skipped
                
                # Altrimenti, non ci sono pedine da mangiare quindi l'ultima mossa individuata è valida quindi viene aggiunta al dizionario
                else:
                    moves[(r, right)] = last
                
                
                # Se è possibile mangiare una pedina, effettua una chiamata ricorsiva per vedere se è possibile effettuare mangiate multiple
                if last:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS)

                    moves.update(self._traverse_left(r+step, row, step, color, right-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1, skipped=last))
                    
                break
            
            # Altrimenti, se la casella non è vuota ma contiene una pedina dello stesso colore di quella che si sta muovendo,
            # non lo si può muovere quindi non si aggiunge quella alla lista delle possibili mosse
            elif current.color == color:
                break
            
            # Altrimenti, la pedina trovata è del colore opposto quindi viene salvata e alla prossima iterazione si andrà a controllare se la casella che la segue è vuota
            # in modo da capire se è possibile catturarla
            else:
                last = [current]

            # Oltre a controllare la riga successiva, bisogna cambiare anche colonna, quindi si va ulteriormente verso destra
            right += 1
    
        return moves
    

