"""
Phase 1: 2-Player game - Tu aur tera dost / Tu khud dono side se
Run: python play.py
"""
from game import ConnectFour

def main():
    game = ConnectFour()
    print("=== CONNECT FOUR - 2 Player ===")
    print("Column number 0-6 daalo. X = Player 1, O = Player 2")
    while game.winner is None:
        game.print_board()
        try:
            col = int(input(f"Player {'X' if game.current_player==1 else 'O'}, column (0-6): "))
        except ValueError:
            print("Number daal bhi!"); continue
        if col not in game.get_legal_moves():
            print("Ye column full hai ya galat hai, dobara try kar"); continue
        game.play(col)
    game.print_board()
    print("Game khatam!")

if __name__ == "__main__":
    main()
