# Esegui solo la prima volta per installare la libreria nell'environment
# pip3 install pygame

import pygame
from checkers.constants import BLACK, WIDTH, HEIGHT, SQUARE_SIZE
from checkers.board import Board
from checkers.game import Game

FPS = 60

# Finestra di gioco
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome della finestra
pygame.display.set_caption("Checkers")


def get_row_col_from_mouse(pos):
    """In base alla posizione attuale del puntatore, restituisce le coordinate (row,col) della casella corrispondente

    Args:
        pos (Tuple[int, int]): tupla contenente le coordinate x e y del puntatore
    """
    
    x, y = pos
    
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE

    return row, col


# Funzione principale per l'esecuzione del gioco
def main():
    """Funzione principale per l'esecuzione del gioco
    """
    run = True
    
    # clock: controlla la velocità dell'event loop (per evitare, ad esempio, che venga eseguito troppo velocemente)
    clock = pygame.time.Clock()
    
    # Istanziazione della partita
    game = Game(WIN)
    
    
    while run:
        clock.tick(FPS)
        
        # Se c'è un vincitore, la partita finisce
        if game.winner() != None:
            print(game.winner())
            run = False
        
        # Event loop: viene eseguito x volte al secondo e controlla eventuali input, aggiorna il display ecc.
        for event in pygame.event.get(): # <- lista di eventi eseguiti dall'ultimo controllo
            
            # Se viene chiusa la finestra, il programma viene fermato            
            if event.type == pygame.QUIT:
                run = False
            
            # Se viene premuto un pulsante del mouse, prendi le coordinate della casella cliccata e verifica il suo contenuto
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                
                game.select(row, col)
                
        
        # Aggiornamento della scacchiera
        game.update()
        
    pygame.quit()



main()