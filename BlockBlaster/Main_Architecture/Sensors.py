import pygetwindow as wn
import pyautogui as gui
import numpy as np
import mss
from collections import deque
import time

from Data_Structures.Board import Board
from Data_Structures.Block import Block

### class constants ###
BOARD_WIDTH = 8
BOARD_HEIGHT = 8
# WINDOW_WIDTH = 628
# WINDOW_HEIGHT = 1020
# TILE_WIDTH = 60
# TILE_SPLIT = 24
# BOARD_X_OFFSET = 145
# BOARD_Y_OFFSET = 250

# BLOCKS_Y_OFFSET = 841
# BLOCKS_X_OFFSET_1 = 195
# BLOCKS_X_DELTA = 159

# BACKGROUND_TILE_OFFSET_Y = 90

# MINI_BLOCK_WIDTH = 29

TOLERANCE = 10



BASE_WINDOW_WIDTH = 628
BASE_WINDOW_HEIGHT = 1020

# these ones are offset from board x and y offset (add them)
# MIN_MOUSE_CHECK_X = -50
# MAX_MOUSE_CHECK_X = 500
# MIN_MOUSE_CHECK_Y = 160
# MAX_MOUSE_CHECK_Y = 690


# MIN_MOUSE_CHECK_X = -100
# MAX_MOUSE_CHECK_X = 450
# MIN_MOUSE_CHECK_Y = 210
# MAX_MOUSE_CHECK_Y = 650
# MOUSE_STEP = 20


class Sensors:
    def __init__(self):
        """ initializes the sensors, sets board to current status"""
        matchingWindows = wn.getWindowsWithTitle("Block Blast!")
        if not matchingWindows:
            raise Exception("Block Blast not found. Confirm app is open")
        window = matchingWindows[0]

        # Actual window size
        self.window_width = window.width
        self.window_height = window.height

        # Scale factors
        self.scale_x = self.window_width / BASE_WINDOW_WIDTH
        self.scale_y = self.window_height / BASE_WINDOW_HEIGHT

        # if window.width != WINDOW_WIDTH:
        #     raise Exception(f"Window size error. Window width is {window.width} but should be {WINDOW_WIDTH}")
        # if window.height != WINDOW_HEIGHT:
        #     raise Exception(f"Window size error. Window height is {window.height} but should be {WINDOW_HEIGHT}")

        # Board
        self.TILE_WIDTH = int(60 * self.scale_x)
        self.TILE_SPLIT = int(24 * self.scale_y)
        self.BOARD_X_OFFSET = int(145 * self.scale_x)
        self.BOARD_Y_OFFSET = int(250 * self.scale_y)
        self.BLOCKS_Y_OFFSET = int(841 * self.scale_y)
        self.BLOCKS_X_OFFSET_1 = int(195 * self.scale_x)
        self.BLOCKS_X_DELTA = int(159 * self.scale_x)
        self.BACKGROUND_TILE_OFFSET_Y = int(90 * self.scale_y)
        self.MINI_BLOCK_WIDTH = int(29 * self.scale_x)
        self.MIN_MOUSE_CHECK_X = int(-100 * self.scale_x)
        self.MAX_MOUSE_CHECK_X = int(450 * self.scale_x)
        self.MIN_MOUSE_CHECK_Y = int(210 * self.scale_y)
        self.MAX_MOUSE_CHECK_Y = int(650 * self.scale_y)

        self.MOUSE_STEP = max(1, int(20 * min(self.scale_x, self.scale_y)))



        self.boardLeft = window.left + self.BOARD_X_OFFSET
        self.boardTop = window.top + self.BOARD_Y_OFFSET

        self.blocksLeft = window.left + self.BLOCKS_X_OFFSET_1
        self.blocksTop = window.top + self.BLOCKS_Y_OFFSET
        
        
        self.board = self.initializeStatespace()


    def initializeStatespace(self):
        """ generates the actions the model should take based on the board state and given blocks """
        print("initializing statespace...")
        board = Board(BOARD_WIDTH, BOARD_HEIGHT)

        for x in range(0, BOARD_WIDTH):
            for y in range(0, BOARD_HEIGHT):
                checkBaseX = self.boardLeft + x * self.TILE_WIDTH
                checkBaseY = self.boardTop + y * self.TILE_WIDTH

                color1 = gui.pixel(checkBaseX, checkBaseY)
                color2 = gui.pixel(checkBaseX, checkBaseY - self.TILE_SPLIT)

                if color1 != color2:
                    board.set_occupied(x, y)

        return board
    
    def getBoard(self):
        """ returns the board state maintained in this object """
        return self.board
    
    def _getBackgroundColor(self):
        for x in range(0, BOARD_WIDTH):
            for y in range(0, BOARD_HEIGHT):
                checkBaseX = self.boardLeft + x * self.TILE_WIDTH
                checkBaseY = self.boardTop + y * self.TILE_WIDTH

                color1 = gui.pixel(checkBaseX, checkBaseY)
                color2 = gui.pixel(checkBaseX, checkBaseY - self.TILE_SPLIT)

                if color1 == color2:
                    return color1

        return None
    
    def placeBlock(self, x, y, block, choice, backgroundColor=None):
        """
        updates the maintained board with the block we chose to place down 
        x would be the top left of the block I think. Further it actually 
        places a block down from the given choices (probably an integer for 0, 1, or 2) and the 
        (x, y) of where it is supposed to go on the board from the bottom left of the block. The bottom
        left of the block is without regard to the tile space, so there may not be anything there (at tile (0,0)), 
        but it still exists as a pivot point within the block. Takes the block just for help encapsulating data
        """

        for tile in block.getTiles():
            boardX = tile[0] + x
            boardY = block.getHeight() - 1 - tile[1] + y
            
            if (self.board.get_tile(boardX, boardY).isOccupied):
                raise Exception("Chose occupied location for block")
            self.board.set_occupied(boardX, boardY)
            
        ## this needs to be fixed but I don't want to figure out the coordinate logic right now

        # places the block using some exhaustion search something or other
        try:
            blockCenterX = self.blocksLeft + choice * self.BLOCKS_X_DELTA
            blockCenterY = self.blocksTop
            backgroundColor = self._getBackgroundColor()
            
            gui.moveTo(blockCenterX, blockCenterY)
            gui.mouseDown()
            
            for boardY in range(self.boardTop + self.MIN_MOUSE_CHECK_Y, self.boardTop + self.MAX_MOUSE_CHECK_Y, self.MOUSE_STEP):
                for boardX in range(self.boardLeft + self.MIN_MOUSE_CHECK_X, self.boardLeft + self.MAX_MOUSE_CHECK_X, self.MOUSE_STEP):
                    # for every mouse position check that the tile colors match and place if so
                    gui.moveTo(boardX, boardY)

                    found = True
                    tiles = block.getTiles()
                    for tile in tiles:
                        checkBaseX = self.boardLeft + (tile[0] + x) * self.TILE_WIDTH
                        checkBaseY = self.boardTop + (block.getHeight() - 1 - tile[1] + y) * self.TILE_WIDTH
                        color = gui.pixel(checkBaseX, checkBaseY)
                        if color == backgroundColor:
                            found = False
                            break
                    
                    if found == True:
                        gui.mouseUp()
                        return True

        finally:
            gui.mouseUp()

        return False

    
    def readBlocks(self):
        """ reads the three choice input blocks and returns a list for them """
        backgroundColors = self._getUniqueColorsInColumn(self.blocksLeft - 90, self.blocksTop + 150, self.blocksTop - 150)

        all_blocks = []
        block_colors = []

        for i in range(0, 3):
            # locate the center of a block within a pattern
            blockCenterX = self.blocksLeft + i * self.BLOCKS_X_DELTA
            blockCenterY = self.blocksTop

            color = gui.pixel(blockCenterX, blockCenterY)
            if (self._colorInColors(color, backgroundColors)):
                blockCenterY -= self.MINI_BLOCK_WIDTH
                color = gui.pixel(blockCenterX, blockCenterY)
            if (self._colorInColors(color, backgroundColors)):
                blockCenterY += 2 * self.MINI_BLOCK_WIDTH
                color = gui.pixel(blockCenterX, blockCenterY)
            
            commonColor = self._getMostCommonColor(blockCenterX, blockCenterY, self.MINI_BLOCK_WIDTH, self.MINI_BLOCK_WIDTH, backgroundColors)
            if (commonColor is None):
                continue

            tempX = blockCenterX
            tempY = blockCenterY
            
            offset = self.MINI_BLOCK_WIDTH // 2
            colorC = gui.pixel(blockCenterX, blockCenterY)
            colorR = gui.pixel(blockCenterX + offset, blockCenterY)
            colorU = gui.pixel(blockCenterX, blockCenterY - offset)
            colorL = gui.pixel(blockCenterX - offset, blockCenterY)
            colorD = gui.pixel(blockCenterX, blockCenterY + offset)

            if not self._colorsClose(commonColor, colorC):
                if (self._colorsClose(commonColor, colorR)):
                    blockCenterX += offset
                elif (self._colorsClose(commonColor, colorL)):
                    blockCenterX -= offset
                if (self._colorsClose(commonColor, colorU)):
                    blockCenterY -= offset
                elif (self._colorsClose(commonColor, colorD)):
                    blockCenterY += offset
                
                # check for those stupid 2x2 things
                if (tempX == blockCenterX and tempY == blockCenterY):
                    colorNE = gui.pixel(blockCenterX + offset, blockCenterY - offset)
                    colorNW = gui.pixel(blockCenterX - offset, blockCenterY - offset)
                    colorSE = gui.pixel(blockCenterX + offset, blockCenterY + offset)

                    if (self._colorsClose(commonColor, colorNE)):
                        blockCenterX += offset
                        blockCenterY -= offset
                    elif (self._colorsClose(commonColor, colorNW)):
                        blockCenterX -= offset
                        blockCenterY -= offset
                    elif (self._colorsClose(commonColor, colorSE)):
                        blockCenterX += offset
                        blockCenterY += offset
                    else:
                        blockCenterX -= offset
                        blockCenterY += offset


            # now breadth first search all ordinal directions for more
            visited = set()
            queue = deque()
            pivot = (blockCenterX, blockCenterY)
            queue.append((pivot, (0, 0)))
            tiles = []

            while queue:
                (px, py), (rx, ry) = queue.popleft()
                if (px, py) in visited:
                    continue
                visited.add((px, py))

                try:
                    current_color = gui.pixel(px, py)
                except:
                    continue
                if not self._colorsClose(current_color, commonColor):
                    continue

                tiles.append((rx, ry))

                directions = [
                    (self.MINI_BLOCK_WIDTH, 0, 1, 0),
                    (-self.MINI_BLOCK_WIDTH, 0, -1, 0),
                    (0, self.MINI_BLOCK_WIDTH, 0, -1),
                    (0, -self.MINI_BLOCK_WIDTH, 0, 1),
                    (self.MINI_BLOCK_WIDTH, self.MINI_BLOCK_WIDTH, 1, -1),
                    (-self.MINI_BLOCK_WIDTH, -self.MINI_BLOCK_WIDTH, -1, 1),
                    (-self.MINI_BLOCK_WIDTH, self.MINI_BLOCK_WIDTH, -1, -1),
                    (self.MINI_BLOCK_WIDTH, -self.MINI_BLOCK_WIDTH, 1, 1)
                ]

                for dx, dy, rdx, rdy in directions:
                    nx, ny = px + dx, py + dy
                    nrx, nry = rx + rdx, ry + rdy
                    if (nx, ny) not in visited:
                        queue.append(((nx, ny), (nrx, nry)))

            all_blocks.append(tiles)
            block_colors.append(commonColor)

        if (len(all_blocks) == 0):
            raise Exception("no blocks detected")
        
        return self._convertAllPairsToBlocks(all_blocks, block_colors)
    
    def _getMostCommonColor(self, x, y, width, height, backgroundColors, tolerance=TOLERANCE):
        left = int(x - width // 2)
        top = int(y - height // 2)

        region = {
            "top": top,
            "left": left,
            "width": int(width),
            "height": int(height)
        }

        with mss.mss() as sct:
            screenshot = sct.grab(region)
            img = np.array(screenshot)[:, :, :3].astype(np.int16)
            pixels = img.reshape(-1, 3)

            bg = np.array([c[::-1] for c in backgroundColors], dtype=np.int16)
            diff = np.abs(pixels[:, None, :] - bg[None, :, :])

            is_background = np.any(np.all(diff <= tolerance, axis=2), axis=1)
            filtered_pixels = pixels[~is_background]

            if len(filtered_pixels) == 0:
                return None
            fp = filtered_pixels.astype(np.uint32)
            pixels_1d = (
                (fp[:, 0] << 16) |
                (fp[:, 1] << 8)  |
                (fp[:, 2])
            )

            colors, counts = np.unique(pixels_1d, return_counts=True)
            most_common = int(colors[np.argmax(counts)])

            r = (most_common >> 16) & 255
            g = (most_common >> 8) & 255
            b = most_common & 255

            return (b, g, r)

    
    def _getShadowColor(self, backgroundColor, startingX, startingY):
        color = None
        startingX += self.MINI_BLOCK_WIDTH // 6
        startingY -= 5
        while True:
            currentColor = gui.pixel(startingX, startingY)
            if (currentColor == backgroundColor and color != None):
                return color
            startingY += 5
            color = currentColor

    def _getUniqueColorsInColumn(self, x, startY, endY):
        """
        Returns a list of unique (R, G, B) tuples along a vertical line.
        """

        top = int(min(startY, endY))
        height = int(abs(endY - startY))

        region = {
            "top": top,
            "left": int(x),
            "width": 1,
            "height": height
        }

        with mss.mss() as sct:
            screenshot = sct.grab(region)

            img = np.array(screenshot)[:, :, :3]

            pixels = img.reshape(-1, 3)
            unique_pixels = np.unique(pixels, axis=0)
            result = [
                (int(p[2]), int(p[1]), int(p[0]))
                for p in unique_pixels
            ]

            return result
        
    def _colorInColors(self, color, colors, tolerance=TOLERANCE):
        return any(self._colorsClose(color, bg, tolerance) for bg in colors)

    def _colorsClose(self, c1, c2, tolerance=TOLERANCE):
        return all(abs(int(a) - int(b)) <= tolerance for a, b in zip(c1, c2))
    
    def _convertAllPairsToBlocks(self, fullCoordinateSet, colorList):
        converted = []

        for i in range(0, len(fullCoordinateSet)):
            converted.append(self._convertSetToBlock(fullCoordinateSet[i], colorList[i]))

        return converted

    def _convertSetToBlock(self, coordinateSet, color):
        # standardize values
        min_x = min(coord[0] for coord in coordinateSet)
        min_y = min(coord[1] for coord in coordinateSet)

        normalized = []
        for x, y in coordinateSet:
            normalized.append([x - min_x, y - min_y])

        return Block(normalized, color)

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

# test = Sensors()
# test.printBoardRepresentation()
# blockList = test.readBlocks()
# for block in blockList:
#     print(block.getTiles())
#     print(block.getWidth())
#     print(block.getHeight())
#     print(block.getTileColor())
# test.placeBlock(2, 0, blockList[0], 1) # 0 indexed x and y
# x and y inputs are where you want to place on the board where 0,0
# is the uppermost left tile . Places from the pivot of the bottom leftmost point
# might also pivot from top left Im not quite sure yet
# it does pivot from top left of the block

# test.placeBlock(3, 3, blockList[1], 1)
# test.placeBlock(3, 0, blockList[1], 1)
# test.placeBlock(6, 1, blockList[2], 2)
# test.placeBlock(7, 7, blockList[1], 1)
# test.placeBlock(0, 7, blockList[2], 2)


# while True:
#     x, y = gui.position()
#     positionStr = 'X: ' + str(x  - test.boardLeft).rjust(4) + ' Y: ' + str(y  - test.boardTop ).rjust(4) + ' Color: ' + str(gui.pixel(x, y))
#     print(positionStr, end='')
#     print('\b' * len(positionStr), end='', flush=True)