"""Tu (X) vs MCTS AI (O) - tu pehle khelega."""

from game import ConnectFour
from mcts import get_best_move

def main():
    g = ConnectFour()
    print("=== TU (X) vs AI (O) ===")
    print("Column 0-6 daalo. Tu X hai, AI O hai.")
    print("AI har chaal se pehle 500 baar sochta hai!")

    while g.winner is None:
        g.print_board()

        if g.current_player == 1:
            # Teri baari
            try:
                col = int(input("Teri chaal, column (0-6): "))
            except ValueError:
                print("Number daal bhi, 0-6 ke beech!")
                continue
            if col not in g.get_legal_moves():
                print("Ye column full hai / galat hai, dobara daal!")
                continue
            g.play(col)
        else:
            # AI ki baari
            print("AI soch raha hai...")
            col = get_best_move(g, n_simulations=500)
            print(f"AI ne chala: Column {col}")
            g.play(col)

    g.print_board()
    if g.winner == 1:
        print(">>> TU JEET GAYA! AI ko hara diya!")
    elif g.winner == -1:
        print(">>> AI JEET GAYA! Dobara try kar!")
    else:
        print(">>> DRAW! Dono barabar!")

if __name__ == "__main__":
    main()