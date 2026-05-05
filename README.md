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

Open `simulate.py` and edit these two lines at the top:

```python
# Choose your model
ACTIVE_MODEL = Model()                                                       # all heuristics on (default)
ACTIVE_MODEL = Model(useMrv=False, useLcv=False, useForwardChecking=False)  # backtracking, no heuristics
ACTIVE_MODEL = Model(useGreedy=True)                                         # greedy baseline

# Choose display mode
DISPLAY_MODE = 'detailed'   # shows board before/after each block placement
DISPLAY_MODE = 'fast'       # shows round-level summary only
```


## Files

- `simulate.py` — main file, runs the terminal simulation
- `Main_Architecture/Model.py` — CSP model (MRV, LCV, Forward Checking, Greedy)
- `Main_Architecture/Data_Structures/Board.py` — 8x8 grid of Tiles
- `Main_Architecture/Data_Structures/Block.py` — block shape and dimensions
- `Main_Architecture/Data_Structures/Tile.py` — single cell with an occupied/empty state

`BlockBlaster.py` and `Sensors.py` were an earlier prototype that read the real game screen and controlled it with mouse input. It was scrapped due to portability issues and replaced by the terminal simulation.
