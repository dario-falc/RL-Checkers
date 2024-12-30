from CheckersEnv import CheckersEnv
from QLearningAgent import QLearningAgent

env = CheckersEnv()
agent = QLearningAgent(env.action_space)

for episode in range(1000):  # Numero di episodi
    state = env.reset()  # Reset dell'ambiente
    done = False
    
    while not done:
        action = agent.choose_action(state)
        next_state, reward, done, _ = env.step(action)
        agent.learn(state, action, reward, next_state)
        state = next_state

    if episode % 100 == 0:
        print(f"Episode {episode} complete")
