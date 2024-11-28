import pygame

# Alcune costanti
WIDTH, HEIGHT = 800, 800        # dimensioni in pixels della finestra del gioco
ROWS, COLS = 8, 8               # dimensioni della scacchiera
SQUARE_SIZE = WIDTH//COLS       # dimensiioni delle singole caselle

# Colori in rgb
#RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Pedine
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)

# Scacchiera
DUSK_DARK = (112, 102, 119)
DUSK_LIGHT = (204, 183, 174)

# Icona dama, riscalata
CROWN = pygame.transform.scale(pygame.image.load("assets/crown.png"), (45, 25))
