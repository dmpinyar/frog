import sys
import os
import random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Main_Architecture'))

from Data_Structures.Board import Board
from Data_Structures.Block import Block
from Model import Model

W, H = 8, 8

# "Empty" model is all heuristics enabled as true is the default for all. 
# So if we want all off just say Model(useMrv=False, useLcv=False, useForwardChecking=False)
# ACTIVE_MODEL = Model()

# 'detailed' — shows board before placement, after placement, after line clears (per block)
# 'fast'    — skips per-block display, only shows final stats
# DISPLAY_MODE = 'detailed'

# Common Block Blast shapes — tiles use y=0 at bottom, y increases upward
SHAPES = [
    [[0,0]],                                          # 1x1
    [[0,0],[1,0]],                                    # 1x2 horizontal
    [[0,0],[0,1]],                                    # 1x2 vertical
    [[0,0],[1,0],[2,0]],                              # 1x3 horizontal
    [[0,0],[0,1],[0,2]],                              # 1x3 vertical
    [[0,0],[1,0],[2,0],[3,0]],                        # 1x4 horizontal
    [[0,0],[0,1],[0,2],[0,3]],                        # 1x4 vertical
    [[0,0],[1,0],[2,0],[3,0],[4,0]],                  # 1x5 horizontal
    [[0,0],[0,1],[0,2],[0,3],[0,4]],                  # 1x5 vertical
    [[0,0],[1,0],[0,1],[1,1]],                        # 2x2 square
    [[0,0],[1,0],[2,0],[0,1],[1,1],[2,1],[0,2],[1,2],[2,2]],  # 3x3 square
    [[0,0],[1,0],[0,1],[0,2]],                        # L shape
    [[0,0],[1,0],[1,1],[1,2]],                        # J shape
    [[0,0],[1,0],[2,0],[0,1]],                        # L rotated
    [[0,0],[1,0],[2,0],[2,1]],                        # J rotated
    [[0,1],[1,1],[2,1],[1,0]],                        # T shape
    [[0,0],[1,0],[1,1],[2,1]],                        # S shape
    [[1,0],[2,0],[0,1],[1,1]],                        # Z shape
    [[0,0],[1,0],[0,1],[1,1],[0,2],[1,2]],            # 2x3 rectangle
    [[0,0],[1,0],[2,0],[0,1],[1,1]],                  # 3x2 rectangle
    [[0,0],[0,1],[0,2],[1,2],[2,2]],                  # 3x3 L
    [[2,0],[2,1],[2,2],[1,2],[0,2]],                  # 3x3 J
    [[0,0],[1,0],[2,0],[0,1],[0,2]],                  # 3x3 L rotated
    [[0,0],[1,0],[2,0],[2,1],[2,2]],                  # 3x3 J rotated
]


def randomBlocks():
    return [Block(random.choice(SHAPES), (255,0,0)) for _ in range(3)]


def gridToBoard(grid):
    board = Board(W, H)
    for x in range(W):
        for y in range(H):
            if grid[x][y]:
                board.set_occupied(x, y)
    return board


def placeOnly(grid, block, x, y):
    '''
    places block on grid without clearing lines, returns new grid
    '''
    g = [col[:] for col in grid]
    for tx, ty in block.getTiles():
        g[x + tx][y + block.getHeight() - 1 - ty] = True
    return g


def clearLines(grid):
    '''
    clears full rows and columns, returns new_grid, lines_cleared
    '''
    g = [col[:] for col in grid]
    fullRows = [r for r in range(H) if all(g[c][r] for c in range(W))]
    fullCols = [c for c in range(W) if all(g[c][r] for r in range(H))]
    for r in fullRows:
        for c in range(W):
            g[c][r] = False
    for c in fullCols:
        for r in range(H):
            g[c][r] = False
    return g, len(fullRows) + len(fullCols)


def printBoard(grid):
    '''
    This prints the current board/grid with an outline. 
    '''
    print("+" + "-" * (W * 2 - 1) + "+")
    for y in range(H):
        row = [str(int(grid[x][y])) for x in range(W)]
        print("|" + " ".join(row) + "|")
    print("+" + "-" * (W * 2 - 1) + "+")


def renderBlock(block):
    '''
    This should returns a list of strings that
    is the block.
    '''
    w, h = block.getWidth(), block.getHeight()
    canvas = [['.' for _ in range(w)] for _ in range(h)]
    for tx, ty in block.getTiles():
        canvas[h - 1 - ty][tx] = 'X'
    return [''.join(row) for row in canvas]


def printBlocks(blocks):
    '''
    This prints the three blocks side by side 
    so we can see block 0, 1, 2 together. 
    '''
    rendered = [renderBlock(b) for b in blocks]
    maxH = max(len(r) for r in rendered)
    padded = []
    for i, r in enumerate(rendered):
        w = blocks[i].getWidth()
        top_pad = [' ' * w] * (maxH - len(r))
        padded.append(top_pad + r)
    labels = [f"Block {i}".ljust(14) for i in range(len(blocks))]
    print("  ".join(labels))
    for row in range(maxH):
        line = "  ".join(padded[i][row].ljust(14) for i in range(len(blocks)))
        print(line)


def run(doPrint=True, DISPLAY_MODE='detailed', useMrv=True, useLcv=True, useForwardChecking=True, useGreedy=False):
    '''
    This is the main function that simulates the game
    '''
    grid = [[False] * H for _ in range(W)]
    model = Model(useMrv=useMrv, useLcv=useLcv, useForwardChecking=useForwardChecking, useGreedy=useGreedy)
    rounds = 0
    totalScore = 0
    totalLines = 0

    print("   Block Blast Simulation    \n")

    while True:
        blocks = randomBlocks()
        board = gridToBoard(grid)

        if doPrint:
            print(f"Round {rounds + 1}")
            print("Board:")
            printBoard(grid)
            print("\nBlocks to place:")
            printBlocks(blocks)
            print()

        actions = model.generateActions(board, blocks)

        if actions is None:
            print("No more available actions! We lost! :(")
            break

        roundScore = 0
        roundLines = 0

        for block_idx, x, y in actions:
            block = blocks[block_idx]
            tileScore = len(block.getTiles())

            if DISPLAY_MODE == 'detailed' and doPrint:
                # For detailed mode, we show the board before placement. 
                print(f"  Placing block {block_idx} at ({x}, {y}):")
                print("  Before:")
                printBoard(grid)

            grid = placeOnly(grid, block, x, y)

            if DISPLAY_MODE == 'detailed' and doPrint:
                # for detailed mode, we show the board after placing the block
                # before any line clears, just for visual. 
                print("  After placement:")
                printBoard(grid)

            grid, linesCleared = clearLines(grid)

            if DISPLAY_MODE == 'detailed' and linesCleared > 0 and doPrint:
                # if needed, we show the board after any line clears. 
                print(f"  {linesCleared} line(s) cleared!")
                printBoard(grid)

            lineScore = linesCleared * 10
            roundScore += tileScore + lineScore
            roundLines += linesCleared

            if DISPLAY_MODE == 'detailed' and doPrint:
                print(f"  Placed block {block_idx} at ({x}, {y}):  +{tileScore} tile pts, +{lineScore} line pts")

        totalScore += roundScore
        totalLines += roundLines
        rounds += 1

        if doPrint:
            print(f"\nBoard after round {rounds}:")
            printBoard(grid)
            print(f"Round score: {roundScore} | Lines cleared: {roundLines}\n")

    print("End of game stats:")
    print(f"Rounds survived : {rounds}")
    print(f"Lines cleared   : {totalLines}")
    print(f"Total score     : {totalScore}")



if __name__ == "__main__":
    useMrv = True
    useLcv = True
    useForwardChecking = True
    useGreedy = False
    doPrint = True
    display_mode = 'detailed'

    for arg in sys.argv:
        if (arg == "-nmrv"):
            useMrv = False
        if (arg == "-nlcv"):
            useLcv = False
        if (arg == "-nfc"):
            useForwardChecking = False
        if (arg == "-g"):
            useGreedy = True
        if (arg == "-np"):
            doPrint = False
        if (arg == "-nd"):
            display_mode = ''

    run(doPrint=doPrint, DISPLAY_MODE=display_mode, useMrv=useMrv, useLcv=useLcv, useForwardChecking=useForwardChecking, useGreedy=useGreedy)
