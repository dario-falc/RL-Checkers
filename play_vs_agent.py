import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, BLACK
from checkers.game import Game
from gym.CheckersEnv import CheckersEnv
from gym.QLearningAgent import QLearningAgent

FPS = 60


def get_valid_actions(game):
    """
    Estrae le mosse valide dall'oggetto game. Poiché la logica delle
    mosse obbligatorie è gestita in board.py tramite il metodo
    get_valid_moves_player, qui vengono semplicemente codificate le mosse.
    
    Restituisce un dizionario:
      - chiave: azione, tupla ((from_row, from_col), (to_row, to_col))
      - valore: dizionario con le coordinate 'from', 'to' e la lista 'skipped'
    """
    
    valid_actions = {}
    # Ottiene le mosse valide per il giocatore corrente (già filtrate per eventuali catture obbligatorie)
    moves_player, _ = game.board.get_valid_moves_player(game.turn)
    for (from_row, from_col), moves in moves_player.items():
        for (to_row, to_col), skipped in moves.items():
            action = ((from_row, from_col), (to_row, to_col))
            valid_actions[action] = {
                "from": (from_row, from_col),
                "to": (to_row, to_col),
                "skipped": skipped
            }
    
    return valid_actions


def main():
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Play vs Agent')
    clock = pygame.time.Clock()

    game = Game(WIN)
    env = CheckersEnv()
    env.game = game  # Sincronizza l'ambiente con il gioco corrente

    agent = QLearningAgent()
    agent.load_q_table("q_table.pkl")  # Carica la Q-table prodotta dall'addestramento

    run = True
    while run:
        clock.tick(FPS)

        # Turno dell'agente (assumiamo che l'agente giochi con i pezzi neri)
        if game.turn == BLACK:
            state = env.get_state()
            valid_actions = get_valid_actions(game)
            if not valid_actions:
                print("Nessuna mossa valida per l'agente, vincitore: WHITE!")
                run = False
                continue

            # Visualizza in console il processo decisionale
            print("\n[AGENT DECISION] Q-values per le mosse valide:")
            for action, info in valid_actions.items():
                q_value = agent.get_q(state, action)
                print(f"Azione da {info['from']} a {info['to']}, cattura: {info['skipped']}, Q-value: {q_value:.4f}")

            # L'agente sceglie la mossa con il Q-value massimo
            best_action = max(valid_actions, key=lambda a: agent.get_q(state, a))
            best_info = valid_actions[best_action]
            print(f"[AGENT CHOICE]: da {best_info['from']} a {best_info['to']}\n")

            # Esegue la mossa scelta
            from_row, from_col = best_info["from"]
            to_row, to_col = best_info["to"]
            game.select(from_row, from_col)
            game._move(to_row, to_col)
            continue

        # Turno del giocatore umano (assumiamo che giochi con i pezzi bianchi)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if game.turn == WHITE and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
                game.select(row, col)
            
            if game.board.white_left == 0:
                print("Nessuna mossa valida per il giocatore, vincitore: BLACK!")
                run = False
                continue
        game.update()

    pygame.quit()


if __name__ == '__main__':
    main()
