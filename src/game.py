"""
Connect Four Game - Phase 1
Board: 6 rows x 7 cols, Player 1 = X (1), Player 2 = O (-1)
"""
import numpy as np

ROWS, COLS = 6, 7

class ConnectFour:
    def __init__(self):
        self.board = np.zeros((ROWS, COLS), dtype=int)
        self.current_player = 1
        self.winner = None  # 1, -1, 0 (draw), None (ongoing)
        self.moves = []

    def get_legal_moves(self):
        # Top row empty = column me jagah hai
        return [c for c in range(COLS) if self.board[0, c] == 0]

    def play(self, col):
        if col not in self.get_legal_moves():
            raise ValueError(f"Illegal move: column {col} full")
        # Sabse neeche wali khali row dhoondho
        for row in range(ROWS-1, -1, -1):
            if self.board[row, col] == 0:
                self.board[row, col] = self.current_player
                break
        self.moves.append(col)
        # Jeet check karo - is chaal ke baad
        if self._check_win(row, col):
            self.winner = self.current_player
        elif len(self.moves) == ROWS * COLS:
            self.winner = 0  # Draw
        else:
            self.current_player *= -1
        return self.winner

    def _check_win(self, row, col):
        p = self.board[row, col]
        # 4 directions: horizontal, vertical, diag \, diag /
        for dr, dc in [(0,1), (1,0), (1,1), (1,-1)]:
            count = 1
            for s in [1, -1]:
                r, c = row, col
                while True:
                    r += dr*s; c += dc*s
                    if 0 <= r < ROWS and 0 <= c < COLS and self.board[r, c] == p:
                        count += 1
                    else:
                        break
            if count >= 4:
                return True
        return False

    def copy(self):
        g = ConnectFour()
        g.board = self.board.copy()
        g.current_player = self.current_player
        g.winner = self.winner
        g.moves = self.moves.copy()
        return g

    def print_board(self):
        symbols = {0: '.', 1: 'X', -1: 'O'}
        print("\n  0 1 2 3 4 5 6")
        print("  -------------")
        for r in range(ROWS):
            print(f"| {' '.join(symbols[self.board[r, c]] for c in range(COLS))} |")
        print("  -------------")
        if self.winner == 1:
            print(">>> X (Player 1) WINS!")
        elif self.winner == -1:
            print(">>> O (Player 2) WINS!")
        elif self.winner == 0:
            print(">>> DRAW!")
        else:
            print(f"Turn: {'X' if self.current_player==1 else 'O'}")
