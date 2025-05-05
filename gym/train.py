import pickle
from checkers.constants import BLACK, WHITE
from tqdm import tqdm
from gym.CheckersEnv import CheckersEnv
from gym.QLearningAgent import QLearningAgent

# Ambiente e agente
env = CheckersEnv()
agent = QLearningAgent()

## Parametri
# Numero di episodi di addestramento
num_episodes = 10000
# Numero massimo di mosse per episodio
max_moves = 100

# Loop di training con barra di avanzamento
for episode in tqdm(range(num_episodes), desc="Training episodes"):
    state = env.reset()
    done = False

    for _ in range(max_moves):
        if done:
            break
        
        res = agent.choose_action(state, env)
        if res:
            action, capture_move_exists = res
            #print(f"state:{state}")
            #print(f"action:{action}")
        else:
            break # Nessuna azione valida
        
        # Esegui l'azione e ottieni il nuovo stato, la ricompensa e se il gioco è finito
        next_state, reward, done = env.step(action, capture_move_exists)
        
        # Aggiorna la Q-table solo se la mossa dell'agente è andata a buon fine e quindi il turno è stato passato al giocatore
        agent.learn(state, action, reward, next_state, env) if env.game.turn != BLACK else None
        state = next_state


# Salva la Q-table
with open("q_table.pkl", "wb") as f:
    pickle.dump(agent.q_table, f)

print("Addestramento completato. Q-table salvata.")
