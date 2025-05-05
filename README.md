# RL-Checkers

RL-Checkers è un progetto di dama (checkers) sviluppato in Python che integra una modalità di gioco umano vs. umano e una modalità in cui il giocatore può sfidare un agente AI basato su Q-learning. Il progetto è strutturato in maniera modulare per separare la logica del gioco dalla parte di intelligenza artificiale.

## Struttura del Progetto

/RL-Checkers │── assets/ # Immagini, icone e risorse grafiche (es. crown.png) │ ├── checkers/ # Modulo con la logica del gioco │ │── init.py │ │── board.py # Gestione della scacchiera, movimento e regole (incluse le catture obbligatorie) │ │── constants.py # Costanti di gioco (dimensioni, colori, immagini, ecc.) │ │── game.py # Gestione del flusso di gioco, turni e interazione con l'utente │ │── piece.py # Definizione delle pedine e loro comportamenti (movimento, promozione a dama, ecc.) │ ├── gym/ # Modulo per l’intelligenza artificiale e il reinforcement learning │ │── init.py │ │── CheckersEnv.py # Ambiente personalizzato per il gioco della dama (interfaccia tra il gioco e l'AI) │ │── QLearningAgent.py # Implementazione dell'agente Q-learning per prendere decisioni nel gioco │ │── train.py # Script per addestrare l'agente e salvare la Q-table │ │── main.py # Avvio del gioco in modalità umano vs. umano │── play_vs_agent.py # Modalità per giocare contro l'agente AI (con stampa in console del processo decisionale) │── q_table.pkl # File contenente la Q-table addestrata │── README.md # Questo file │── requirements.txt # Elenco delle dipendenze (es. pygame) │── .gitattributes

# Configurazioni per Git

## Caratteristiche Principali

- **Modalità di Gioco**:  
  - *Umano vs. Umano*: Avviabile tramite `main.py`.  
  - *Umano vs. AI*: Avviabile tramite `play_vs_agent.py`, dove l'agente utilizza Q-learning per decidere le mosse.

- **AI basata su Q-Learning**:  
  - L'agente apprende attraverso numerosi episodi di gioco, memorizzando i valori Q per ogni stato-azione.  
  - Il file `train.py` esegue il training dell'agente e salva la Q-table su `q_table.pkl`.

- **Logica di Gioco Avanzata**:  
  - Il file `board.py` implementa la logica delle mosse obbligatorie: se esiste una mossa di cattura, vengono considerate esclusivamente quelle.
  - Gestione delle pedine, promozione a dama e aggiornamento dello stato del gioco.

- **Visualizzazione e Interazione**:  
  - L'interfaccia grafica è realizzata con Pygame, con una finestra di gioco in cui vengono disegnate la scacchiera e le pedine.
  - In `play_vs_agent.py` l'agente mostra in console i Q-value per ciascuna mossa valida durante il suo turno.

## Come Iniziare

1. **Installazione delle dipendenze**:  
   Assicurati di avere Python installato. Poi esegui:
   ```bash
   pip install -r requirements.txt
Nota: Se non hai Pygame, installalo tramite pip install pygame.

2. Addestramento dell'Agente (facoltativo):
    Per addestrare l'agente AI, esegui:

    bash
    Copia
    Modifica
    python gym/train.py
    Questo genererà il file q_table.pkl con la Q-table addestrata.

3. Avvio del Gioco:

    Modalità Umano vs. Umano: python main.py

    Modalità Umano vs. AI: python play_vs_agent.py

