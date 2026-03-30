import pygetwindow as wn
import pyautogui as gui

from Data_Structures.Board import Board
from Data_Structures.Block import Block

### class constants ###
BOARD_WIDTH = 8
BOARD_HEIGHT = 8
WINDOW_WIDTH = 628
WINDOW_HEIGHT = 1020
TILE_WIDTH = 60
TILE_SPLIT = 20
BOARD_X_OFFSET = 140
BOARD_Y_OFFSET = 245

class Sensors:
    def __init__(self):
        """ initializes the sensors, sets board to null but if app is open we could also just call initializeStateSpace """
        matchingWindows = wn.getWindowsWithTitle("Block Blast!")
        if not matchingWindows:
            raise Exception("Block Blast not found. Confirm app is open")
        window = matchingWindows[0]
        if window.width != WINDOW_WIDTH:
            raise Exception(f"Window size error. Window width is {window.width} but should be {WINDOW_WIDTH}")
        if window.height != WINDOW_HEIGHT:
            raise Exception(f"Window size error. Window height is {window.height} but should be {WINDOW_HEIGHT}")

        self.boardLeft = window.left + BOARD_X_OFFSET
        self.boardTop = window.top + BOARD_Y_OFFSET
        
        self.board = self.initializeStatespace()


    def initializeStatespace(self):
        """ generates the actions the model should take based on the board state and given blocks """
        print("initializing statespace...")
        board = Board(BOARD_WIDTH, BOARD_HEIGHT)

        for x in range(0, BOARD_WIDTH):
            for y in range(0, BOARD_HEIGHT):
                checkBaseX = self.boardLeft + x * TILE_WIDTH
                checkBaseY = self.boardTop + y * TILE_WIDTH

                color1 = gui.pixel(checkBaseX, checkBaseY)
                color2 = gui.pixel(checkBaseX, checkBaseY - TILE_SPLIT)

                if color1 != color2:
                    board.set_occupied(x, y)

        return board
    
    def getBoard(self):
        """ returns the board state maintained in this object """
        return self.board
    
    def placeBlock(self):
        """ updates the maintained board with the block we chose to place down """
        return None
    
    def readBlocks(self):
        """ reads the three choice input blocks and returns a list for them """
        return None

# test = Sensors()
# board = test.getBoard().get_tiles()
# for y in range(0, 8):  # start from highest y
#     for x in range(8):
#         if board[x][y].isOccupied:  # example condition
#             print(1, end=" ")
#         else:
#             print(0, end=" ")
#     print()


# while True:
#         x, y = gui.position()
#         positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
#         print(positionStr, end='')
#         print('\b' * len(positionStr), end='', flush=True)
