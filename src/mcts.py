"""MCTS - Monte Carlo Tree Search, tere game.py ke hisaab se."""

import math
import random
from game import ConnectFour

class Node:
    def __init__(self, game, parent=None, move=None):
        self.game = game
        self.parent = parent
        self.move = move
        self.children = {}
        self.visits = 0
        self.wins = 0.0

    def is_fully_expanded(self):
        return len(self.children) == len(self.game.get_legal_moves())

class MCTS:
    def __init__(self, n_simulations=500):
        self.n_simulations = n_simulations

    def search(self, game):
        root = Node(game.copy())
        # root pe khelne wala player hi hamara player hai
        root_player = game.current_player

        for _ in range(self.n_simulations):
            node = root
            # 1. SELECTION - UCB se neeche jao
            while node.is_fully_expanded() and node.children and node.game.winner is None:
                best_score = -1
                best_node = None
                for child in node.children.values():
                    if child.visits == 0:
                        best_node = child
                        break
                    exploit = child.wins / child.visits
                    explore = 1.41 * math.sqrt(math.log(node.visits) / child.visits)
                    score = exploit + explore
                    if score > best_score:
                        best_score = score
                        best_node = child
                node = best_node

            # 2. EXPANSION - ek nayi chaal try karo
            if node.game.winner is None:
                tried = set(node.children.keys())
                untried = [m for m in node.game.get_legal_moves() if m not in tried]
                if untried:
                    move = random.choice(untried)
                    new_game = node.game.copy()
                    new_game.play(move)
                    child = Node(new_game, parent=node, move=move)
                    node.children[move] = child
                    node = child

            # 3. SIMULATION - random khel ke end tak jao
            sim_game = node.game.copy()
            while sim_game.winner is None and sim_game.get_legal_moves():
                sim_game.play(random.choice(sim_game.get_legal_moves()))
            winner = sim_game.winner

            # 4. BACKPROPAGATION - root_player ke nazariye se
            while node is not None:
                node.visits += 1
                if winner == root_player:
                    node.wins += 1
                elif winner == 0:
                    node.wins += 0.5
                node = node.parent

        best_move = max(root.children.items(), key=lambda x: x[1].visits)[0]
        return best_move

def get_best_move(game, n_simulations=500):
    return MCTS(n_simulations=n_simulations).search(game)

if __name__ == "__main__":
    g = ConnectFour()
    move = get_best_move(g, n_simulations=200)
    print(f"AI ne chaal chali: Column {move}")
    print("MCTS sahi chal raha hai!")