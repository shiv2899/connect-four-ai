"""Tu (X) vs Trained AlphaZero AI (O) - jo 100 game seekh ke aaya hai."""

import torch
from game import ConnectFour
from network import ConnectFourNet, predict

def main():
    model = ConnectFourNet()
    model.load_state_dict(torch.load("../checkpoints/best_model.pt"))
    model.eval()
    print("Trained model load ho gaya - checkpoints/best_model.pt")

    g = ConnectFour()
    print("=== TU (X) vs TRAINED AI (O) ===")
    print("Tu X hai, AI O hai. AI ab seekh ke aaya hai!")

    while g.winner is None:
        g.print_board()

        if g.current_player == 1:
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
            probs, value = predict(model, g)
            col = int(probs.argmax())
            # Agar best chaal full hai to legal me se best lo
            if col not in g.get_legal_moves():
                legal = g.get_legal_moves()
                col = max(legal, key=lambda m: probs[m])
            print(f"AI ne chala: Column {col} (Value: {value:.2f})")
            g.play(col)

    g.print_board()
    if g.winner == 1:
        print(">>> TU JEET GAYA! Trained AI ko hara diya!")
    elif g.winner == -1:
        print(">>> TRAINED AI JEET GAYA!")
    else:
        print(">>> DRAW!")

if __name__ == "__main__":
    main()