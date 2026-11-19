"""Self-Play Training - AI khud se khel ke seekhega."""

import torch
import torch.nn.functional as F
import numpy as np
import os
from game import ConnectFour
from network import ConnectFourNet, board_to_tensor, predict

def play_one_game(model):
    """Ek game khud se khelo, data jama karo."""
    g = ConnectFour()
    states = []  # har chaal pe board kaisa tha
    policies = []  # Network ne kya socha tha
    players = []  # us waqt kaun khel raha tha

    while g.winner is None:
        probs, _ = predict(model, g)
        # Thoda random bhi rakho, taaki AI naya try kare
        # 80% Network ki suno, 20% random
        if np.random.rand() < 0.2:
            move = np.random.choice(g.get_legal_moves())
            # Random wali chaal ka policy one-hot bana do
            probs = np.zeros(7)
            probs[move] = 1.0
        else:
            # Policy se ek chaal chuno
            legal = g.get_legal_moves()
            p = np.zeros(7)
            p[legal] = probs[legal]
            p = p / p.sum()
            move = np.random.choice(7, p=p)

        states.append(board_to_tensor(g)[0].numpy())
        policies.append(probs)
        players.append(g.current_player)
        g.play(move)

    # Winner ke hisaab se har chaal ka result
    # Jeetne wale ki chaal = +1, haarne wale ki = -1, Draw = 0
    values = []
    for p in players:
        if g.winner == 0:
            values.append(0.0)
        elif g.winner == p:
            values.append(1.0)
        else:
            values.append(-1.0)

    return states, policies, values, g.winner

def train(n_games=100):
    model = ConnectFourNet()
    opt = torch.optim.Adam(model.parameters(), lr=0.001)

    print(f"Training start - {n_games} self-play games...")

    for game_no in range(1, n_games + 1):
        states, policies, values, winner = play_one_game(model)

        # Ek game ka data se train karo
        x = torch.tensor(np.array(states))
        target_p = torch.tensor(np.array(policies), dtype=torch.float32)
        target_v = torch.tensor(np.array(values), dtype=torch.float32).unsqueeze(1)

        model.train()
        pred_p, pred_v = model(x)
        # Loss = Policy loss + Value loss
        loss_p = F.cross_entropy(pred_p, target_p)
        loss_v = F.mse_loss(pred_v, target_v)
        loss = loss_p + loss_v

        opt.zero_grad()
        loss.backward()
        opt.step()

        if game_no % 10 == 0:
            w = "Draw" if winner == 0 else f"Player {winner} jeeta"
            print(f"Game {game_no}/{n_games} - Loss: {loss.item():.4f} - Last: {w}")

    # Model save karo
    os.makedirs("../checkpoints", exist_ok=True)
    torch.save(model.state_dict(), "../checkpoints/best_model.pt")
    print("Training khatam! Model save ho gaya: checkpoints/best_model.pt")
    return model

if __name__ == "__main__":
    train(n_games=100)