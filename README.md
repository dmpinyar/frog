# Block Blast AI

A CSP-based AI agent that plays Block Blast in the terminal. It uses backtracking with MRV, LCV, and Forward Checking heuristics, plus a Greedy baseline for comparison.

**Team Members:** Devin Pinyard, Kevin Alvarenga 


## How to Run

From the `BlockBlaster/` directory:

```
python simulate.py
```

No dependencies needed beyond the Python standard library.


## Configuration

# various flags can be given to program
by default all heuristics are on, so these all change the behavior of the program for testing purposes
can be chosen in any order

-nmrv   turn off minimum remaining values in the backtracking search
-nlcv   turn off least common values in the backtracking search
-nfc    turn off forward checking in the backtracking search
-g      swap it to greedy search
-np     simply turns off the board printing
-nd     turns off the detailed version of the board printing (both need to be chosen for just final output)
-i=x    whatever x is set to is the number of games it will play before halting

## Files

- `simulate.py` — main file, runs the terminal simulation
- `Main_Architecture/Model.py` — CSP model (MRV, LCV, Forward Checking, Greedy)
- `Main_Architecture/Data_Structures/Board.py` — 8x8 grid of Tiles
- `Main_Architecture/Data_Structures/Block.py` — block shape and dimensions
- `Main_Architecture/Data_Structures/Tile.py` — single cell with an occupied/empty state

`BlockBlaster.py` and `Sensors.py` were an earlier prototype that read the real game screen and controlled it with mouse input. It was scrapped due to portability issues and replaced by the terminal simulation.
