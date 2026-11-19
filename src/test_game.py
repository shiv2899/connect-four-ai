"""Game ke test - sab pass hone chahiye. Run: python test_game.py"""
from game import ConnectFour

# Test 1: Horizontal win
g = ConnectFour()
for c in [0,0,1,1,2,2,3]: g.play(c)
assert g.winner == 1, "Horizontal win fail"
print("Test 1 PASS - Horizontal win")

# Test 2: Vertical win
g = ConnectFour()
for c in [0,1,0,1,0,1,0]: g.play(c)
assert g.winner == 1, "Vertical win fail"
print("Test 2 PASS - Vertical win")

# Test 3: Illegal move - full column
g = ConnectFour()
for _ in range(6): g.play(0) if g.winner is None else None
# column 0 full hai, ab legal me nahi hona chahiye
assert 0 not in g.get_legal_moves()
print("Test 3 PASS - Full column blocked")

# Test 4: Board copy alag hona chahiye
g = ConnectFour(); g.play(3)
g2 = g.copy(); g2.play(4)
assert g.board[5,4] == 0 and g2.board[5,4] == -1
print("Test 4 PASS - Copy independent")

print("\nSab test PASS - Game sahi hai!")
