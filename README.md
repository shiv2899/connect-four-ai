# Connect Four AI - AlphaZero Style

AI that learns Connect Four only by playing against itself, using the same idea DeepMind used for AlphaZero.

## Demo

2-Player game - X ne Horizontal XXXX se jeeta:

![2-Player Win](results/connect_four_2player_win.png)

MCTS AI (O) ne Diagonal se jeeta:

![AI Wins](results/ai_wins_mcts.png)

Tu ne Trained AlphaZero AI ko Vertical XXXX se haraya:

![Beat Trained AI](results/trained_ai_loss.png)

## How it Works (5 Phases)
- **Phase 1:** Game - board, legal moves, win check
- **Phase 2:** MCTS - Monte Carlo Tree Search, no neural network
- **Phase 3:** Policy/Value Network - predicts best move + win probability
- **Phase 4:** Self-Play Training - MCTS + Network play each other, network trains on results
- **Phase 5:** Test vs perfect solver

## How to Run
```bash
pip install -r requirements.txt
cd src
python play.py      # 2-Player game
python test_game.py # Game tests
python play_vs_ai.py   # Tu (X) vs MCTS AI (O)
python train.py   # 100 self-play games se train karo
python play_vs_trained.py   # Tu vs Trained AI
```

## Files
- `src/game.py` - Connect Four board + win logic
- `src/mcts.py` - MCTS AI, 500 simulations soch ke chaal chalega
- `src/play_vs_ai.py` - Tu vs AI game
- `src/play.py` - 2-Player game
- `src/test_game.py` - Game tests
- `src/network.py` - Policy/Value Network, 58,519 parameters
- `src/train.py` - Self-Play Training, 100 games
- `src/play_vs_trained.py` - Tu vs Trained AI

## Results
- Phase 1: Game working, all tests pass
- Phase 2: MCTS AI working, AI ne Diagonal se jeet ke dikhaya
- Phase 3: AlphaZero Network + Self-Play Training working, 100 games, Tu ne Trained AI ko haraya
