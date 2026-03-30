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

BLOCKS_Y_OFFSET = 905
BLOCKS_X_OFFSET_1 = 255
BLOCKS_X_DELTA = 160

BACKGROUND_TILE_OFFSET_X = 415
BACKGROUND_TILE_OFFSET_Y = 785

MINI_BLOCK_WIDTH = 30

class Sensors:
    def __init__(self):
        """ initializes the sensors, sets board to current status"""
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

        self.blocksTop = window.top + BLOCKS_Y_OFFSET
        self.blocksLeft = window.left + BLOCKS_X_OFFSET_1
        
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
    
    def placeBlock(self, x, y, block):
        """
        updates the maintained board with the block we chose to place down 
        x would be the top left of the block I think
        """
        for tile in block.get_tiles():
            if (self.board[x + tile.x][y + tile.y].isOccupied()):
                raise Exception("Chose occupied location for block")
            self.board[x + tile.x][y + tile.y].setOccupied()
    
    def readBlocks(self):
        """ reads the three choice input blocks and returns a list for them """
        # gui.moveTo(BLOCKS_X_OFFSET_1 + 1 * BLOCKS_X_DELTA + MINI_BLOCK_WIDTH, BLOCKS_Y_OFFSET)
        backgroundColor = gui.pixel(BACKGROUND_TILE_OFFSET_X, BACKGROUND_TILE_OFFSET_Y)
        tileColor = None
        print(backgroundColor)

        for i in range(0, 3):
            color = gui.pixel(BLOCKS_X_OFFSET_1 + i * BLOCKS_X_DELTA, BLOCKS_Y_OFFSET)
            colorR = gui.pixel(BLOCKS_X_OFFSET_1 + i * BLOCKS_X_DELTA + (int) (MINI_BLOCK_WIDTH / 2), BLOCKS_Y_OFFSET)
            colorL = gui.pixel(BLOCKS_X_OFFSET_1 + i * BLOCKS_X_DELTA - (int) (MINI_BLOCK_WIDTH / 2), BLOCKS_Y_OFFSET)
            colorU = gui.pixel(BLOCKS_X_OFFSET_1 + i * BLOCKS_X_DELTA, BLOCKS_Y_OFFSET - (int) (MINI_BLOCK_WIDTH / 2))
            colorD = gui.pixel(BLOCKS_X_OFFSET_1 + i * BLOCKS_X_DELTA, BLOCKS_Y_OFFSET + (int) (MINI_BLOCK_WIDTH / 2))
            #print(f"color {}")

        return None
    
    def _readSingleBlock(backgroundColor, x, y):
        blockFound = False
        color = None

        # # check cardinal directions 
        # for i in range(0, MINI_BLOCK_WIDTH):
            
        # while (blockFound == False):
        #     color = gui.pixel(x, y)
            
        return None
    
    def printBoardRepresentation(self):
        """ prints board for testing purposes """
        board = self.board.get_tiles()
        for y in range(0, BOARD_HEIGHT): 
            for x in range(0, BOARD_WIDTH):
                if board[x][y].isOccupied:
                    print(1, end=" ")
                else:
                    print(0, end=" ")
            print()

test = Sensors()
test.readBlocks()
# test.printBoardRepresentation()

# while True:
#     x, y = gui.position()
#     positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4) + ' Color: ' + str(gui.pixel(x, y))
#     print(positionStr, end='')
#     print('\b' * len(positionStr), end='', flush=True)
