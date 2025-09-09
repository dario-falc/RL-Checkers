import pygame
import sys
import os
from checkers.constants import WHITE, BLACK, WIDTH, HEIGHT, SQUARE_SIZE
from checkers.game import Game
from rl_agent.dqn_agent import DQNAgent
from rl_agent.environment import CheckersEnvironment

FPS = 60

class HumanVsAgentGame:
    """
    Classe per giocare contro l'agente DQN addestrato
    """
    
    def __init__(self, model_path, human_color=WHITE):
        """
        Inizializza il gioco umano vs agente
        
        Args:
            model_path: percorso del modello addestrato
            human_color: colore del giocatore umano (WHITE o BLACK)
        """
        # Inizializza pygame
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Checkers vs AI")
        
        # Inizializza gioco e environment
        self.game = Game(self.win)
        self.env = CheckersEnvironment()
        self.env.game = self.game  # Condivide la stessa istanza di gioco
        
        # Colori
        self.human_color = human_color
        self.agent_color = BLACK if human_color == WHITE else WHITE
        
        # Carica l'agente
        self.agent = DQNAgent(self.env.state_size, self.env.action_size)
        
        if not self.agent.load(model_path):
            print(f"Errore nel caricamento del modello da {model_path}")
            sys.exit(1)
        
        # Modalità evaluation (no exploration)
        self.agent.set_training_mode(False)
        
        print(f"Gioco inizializzato!")
        print(f"Tu giochi con le pedine {'BIANCHE' if human_color == WHITE else 'NERE'}")
        print(f"IA gioca con le pedine {'NERE' if self.agent_color == BLACK else 'BIANCHE'}")
        
    def get_row_col_from_mouse(self, pos):
        """Converte posizione mouse in coordinate scacchiera"""
        x, y = pos
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        return row, col
    
    def agent_move(self):
        """Esegue una mossa dell'agente"""
        current_state = self.env.get_state()
        valid_actions = self.env.get_valid_actions(self.agent_color)
        
        if len(valid_actions) == 0:
            print("L'agente non ha mosse valide!")
            return False
        
        # Ottieni azione dall'agente (senza exploration)
        action = self.agent.get_action(current_state, valid_actions, training=False)
        
        if action is None:
            print("L'agente ha restituito azione None!")
            return False
        
        # Decodifica l'azione
        from_row, from_col, to_row, to_col = self.env.decode_action(action)
        
        print(f"IA muove da ({from_row}, {from_col}) a ({to_row}, {to_col})")
        
        # Esegui la mossa nel gioco
        piece = self.game.board.get_piece(from_row, from_col)
        if piece == 0 or piece.color != self.agent_color:
            print(f"Errore: pezzo non valido in posizione ({from_row}, {from_col})")
            return False
        
        # Seleziona e muovi
        success1 = self.game.select(from_row, from_col)
        if not success1:
            print(f"Errore nella selezione del pezzo in ({from_row}, {from_col})")
            return False
        
        success2 = self.game.select(to_row, to_col)
        if not success2:
            print(f"Errore nel movimento verso ({to_row}, {to_col})")
            return False
        
        return True
    
    def display_game_info(self):
        """Mostra informazioni sullo stato del gioco"""
        current_player = "TU" if self.game.turn == self.human_color else "IA"
        pieces_white = self.game.board.white_left
        pieces_black = self.game.board.black_left
        kings_white = self.game.board.white_kings
        kings_black = self.game.board.black_kings
        
        print(f"\n--- Stato del gioco ---")
        print(f"Turno: {current_player}")
        print(f"Pedine bianche: {pieces_white} (Dame: {kings_white})")
        print(f"Pedine nere: {pieces_black} (Dame: {kings_black})")
        print(f"Epsilon agente: {self.agent.epsilon:.3f}")
        
    def run(self):
        """Esegue il game loop principale"""
        clock = pygame.time.Clock()
        running = True
        
        print("\n🎮 Gioco iniziato! Clicca su una pedina per selezionarla, poi sulla casella di destinazione.")
        self.display_game_info()
        
        while running:
            clock.tick(FPS)
            
            # Controlla se c'è un vincitore
            winner = self.game.winner()
            if winner is not None:
                winner_name = "TU" if winner == self.human_color else "IA"
                print(f"\n🎉 {winner_name} hai vinto!")
                print("Premi ESC per uscire o SPAZIO per una nuova partita")
                
                # Aspetta input per nuova partita o uscita
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            waiting = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                running = False
                                waiting = False
                            elif event.key == pygame.K_SPACE:
                                # Nuova partita
                                self.game.reset()
                                print("\n🔄 Nuova partita iniziata!")
                                self.display_game_info()
                                waiting = False
                    
                    # Aggiorna display anche durante l'attesa
                    self.game.update()
                
                continue
            
            # Turno dell'agente
            if self.game.turn == self.agent_color:
                if not self.agent_move():
                    print("Errore nella mossa dell'agente!")
                    break
                self.display_game_info()
            
            # Gestione eventi
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        # Reset partita
                        self.game.reset()
                        print("\n🔄 Partita resettata!")
                        self.display_game_info()
                
                elif event.type == pygame.MOUSEBUTTONDOWN and self.game.turn == self.human_color:
                    # Turno del giocatore umano
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_row_col_from_mouse(pos)
                    
                    old_turn = self.game.turn
                    self.game.select(row, col)
                    
                    # Se il turno è cambiato, il giocatore ha fatto una mossa valida
                    if old_turn != self.game.turn:
                        self.display_game_info()
            
            # Aggiorna display
            self.game.update()
        
        pygame.quit()


def main():
    """Funzione principale"""
    print("🏁 Checkers vs AI")
    print("=" * 50)
    
    # Percorso del modello
    model_path = input("Inserisci il percorso del modello (o premi ENTER per il modello di default): ").strip()
    
    if not model_path:
        model_path = "models/trained_models/dqn_checkers_final.pth"
    
    if not os.path.exists(model_path):
        print(f"❌ Modello non trovato: {model_path}")
        print("\nModelli disponibili:")
        models_dir = "models/trained_models/"
        if os.path.exists(models_dir):
            for file in os.listdir(models_dir):
                if file.endswith('.pth'):
                    print(f"  - {os.path.join(models_dir, file)}")
        else:
            print("  Nessun modello trovato. Esegui prima train_agent.py")
        return
    
    # Scelta del colore
    print("\nScegli il tuo colore:")
    print("1. Bianco (muovi per primo)")
    print("2. Nero (muovi per secondo)")
    
    choice = input("Scelta (1-2, default=1): ").strip()
    human_color = WHITE if choice != "2" else BLACK
    
    print("\n🎯 Controlli:")
    print("- Clicca per selezionare/muovere le pedine")
    print("- R: Reset partita")
    print("- ESC: Esci")
    print("- SPAZIO: Nuova partita (dopo la fine)")
    
    try:
        game = HumanVsAgentGame(model_path, human_color)
        game.run()
    except Exception as e:
        print(f"❌ Errore durante l'esecuzione del gioco: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()