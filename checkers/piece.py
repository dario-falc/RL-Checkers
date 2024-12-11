import pygame
from .constants import WHITE, BLACK, GREY, SQUARE_SIZE, CROWN

class Piece:
    # PADDING: distanza tra la pedina ed i bordi della casella in cui si trova
    PADDING = 15
    
    # OUTLINE: contorno della pedina per renderla visibile
    OUTLINE = 2
    
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        
        # Coordinate del centro della pedina
        self.x = 0
        self.y = 0
        self.calc_pos()
    
    
    def calc_pos(self):
        """
        Calcola le coordinate (x,y) nella finestra in base alla riga e alla colonna della scacchiera in cui la pedina si trova
        """
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE//2    # <- //2 per posizionare la pedina al centro della casella
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE//2
    
    
    def make_king(self):
        """
        Rende la pedina una dama
        """
        self.king = True
    
    
    def draw(self, win):
        """
        Disegna la pedina

        Args:
            win (Surface): finestra di gioco
        """
        
        # Raggio della pedina: dal centro al bordo della casella, meno il padding scelto
        radius = SQUARE_SIZE//2 - self.PADDING
        
        # Contorno della pedina
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        
        # Pedina
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        
        # Se la pedina è una dama, aggiungi a schermo una corona nella rispettiva posizione
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))
    
    
    def move(self, row, col):
        """
        Sposta la pedina

        Args:
            row (Int): riga in cui spostare la pedina
            col (Int): colonna in cui spostare la pedina
        """
        self.row = row
        self.col = col
        
        # Aggiornamento delle coordinate x e y della pedina
        self.calc_pos()
    
    
    def __repr__(self):
        return str(self.color)