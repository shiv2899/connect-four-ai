"""Policy/Value Network - AlphaZero ka dimaag."""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from game import ConnectFour

class ConnectFourNet(nn.Module):
    def __init__(self):
        super().__init__()
        # Input: 3 channel - [Meri gota, Dushman ki gota, Khali]
        # Board: 6 row x 7 col
        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.conv3 = nn.Conv2d(64, 64, 3, padding=1)

        # Policy Head - 7 column me se kaunsi chaal?
        self.policy_conv = nn.Conv2d(64, 2, 1)
        self.policy_fc = nn.Linear(2 * 6 * 7, 7)

        # Value Head - jeetunga ya haarunga? -1 se +1
        self.value_conv = nn.Conv2d(64, 1, 1)
        self.value_fc1 = nn.Linear(1 * 6 * 7, 32)
        self.value_fc2 = nn.Linear(32, 1)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))

        # Policy
        p = F.relu(self.policy_conv(x))
        p = p.view(-1, 2 * 6 * 7)
        policy = self.policy_fc(p)  # 7 number, har column ke liye

        # Value
        v = F.relu(self.value_conv(x))
        v = v.view(-1, 1 * 6 * 7)
        v = F.relu(self.value_fc1(v))
        value = torch.tanh(self.value_fc2(v))  # -1 to +1

        return policy, value

def board_to_tensor(game):
    """Game ke board ko Network ke samajhne wale format me badlo."""
    board = game.board  # 6x7, 1 = X, -1 = O, 0 = khali
    me = (board == game.current_player).astype(np.float32)
    opp = (board == -game.current_player).astype(np.float32)
    empty = (board == 0).astype(np.float32)
    # Shape: (1, 3, 6, 7) - batch, channel, row, col
    arr = np.stack([me, opp, empty], axis=0)
    return torch.tensor(arr).unsqueeze(0)

def predict(model, game):
    """Ek board pe Network kya sochta hai, wo batao."""
    model.eval()
    with torch.no_grad():
        x = board_to_tensor(game)
        policy_logits, value = model(x)
        # Legal chaal ke alawa sabko -inf kar do
        mask = torch.ones(7) * -1e9
        for m in game.get_legal_moves():
            mask[m] = 0
        policy_logits = policy_logits[0] + mask
        probs = F.softmax(policy_logits, dim=0).numpy()
        return probs, float(value[0][0])

if __name__ == "__main__":
    net = ConnectFourNet()
    g = ConnectFour()
    probs, value = predict(net, g)
    print(f"Khali board pe Policy: {np.round(probs, 3)}")
    print(f"Khali board pe Value: {value:.3f} (0 = barabar)")
    print(f"Total Parameters: {sum(p.numel() for p in net.parameters())}")
    print("Network sahi chal raha hai!")