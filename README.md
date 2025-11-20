# Blackjack Simulator

This is a basic blackjack simulator built with Python.
It uses an sqlitedatabase to log game sessions and hands played and keep track of player balance accross games.

The game follows these rules:

- Dealer stands on 17
- Blackjack pays 3/2

## Next Steps

- The split logic is too complex with this code as it stands as it requires keeping track of multiple hands at once --> may need to iterate over an array containing active hands
- Build interactive UI instead of console (tkinter maybe?)
