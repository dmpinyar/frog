import pygetwindow as wn
import pyautogui as gui
import numpy as np
import mss
from collections import deque

from Data_Structures.Board import Board
from Data_Structures.Block import Block

### class constants ###
BOARD_WIDTH = 8
BOARD_HEIGHT = 8
WINDOW_WIDTH = 628
WINDOW_HEIGHT = 1020
TILE_WIDTH = 60
TILE_SPLIT = 24
BOARD_X_OFFSET = 145
BOARD_Y_OFFSET = 250

BLOCKS_Y_OFFSET = 841
BLOCKS_X_OFFSET_1 = 195
BLOCKS_X_DELTA = 159

BACKGROUND_TILE_OFFSET_Y = 90

MINI_BLOCK_WIDTH = 29

TOLERANCE = 10

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

        self.blocksLeft = window.left + BLOCKS_X_OFFSET_1
        self.blocksTop = window.top + BLOCKS_Y_OFFSET
        
        
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
        backgroundColors = self._getUniqueColorsInColumn(self.blocksLeft - 90, self.blocksTop + 150, self.blocksTop - 150)

        all_blocks = []

        for i in range(0, 3):
            # locate the center of a block within a pattern
            blockCenterX = self.blocksLeft + i * BLOCKS_X_DELTA
            blockCenterY = self.blocksTop

            color = gui.pixel(blockCenterX, blockCenterY)
            if (self._colorInColors(color, backgroundColors)):
                blockCenterY -= MINI_BLOCK_WIDTH
                color = gui.pixel(blockCenterX, blockCenterY)
            if (self._colorInColors(color, backgroundColors)):
                blockCenterY += 2 * MINI_BLOCK_WIDTH
                color = gui.pixel(blockCenterX, blockCenterY)
            
            commonColor = self._getMostCommonColor(blockCenterX, blockCenterY, MINI_BLOCK_WIDTH, MINI_BLOCK_WIDTH, backgroundColors)
            if (commonColor is None):
                continue

            tempX = blockCenterX
            tempY = blockCenterY
            
            offset = MINI_BLOCK_WIDTH // 2
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
                    (MINI_BLOCK_WIDTH, 0, 1, 0),
                    (-MINI_BLOCK_WIDTH, 0, -1, 0),
                    (0, MINI_BLOCK_WIDTH, 0, -1),
                    (0, -MINI_BLOCK_WIDTH, 0, 1),
                    (MINI_BLOCK_WIDTH, MINI_BLOCK_WIDTH, 1, -1),
                    (-MINI_BLOCK_WIDTH, -MINI_BLOCK_WIDTH, -1, 1),
                    (-MINI_BLOCK_WIDTH, MINI_BLOCK_WIDTH, -1, -1),
                    (MINI_BLOCK_WIDTH, -MINI_BLOCK_WIDTH, 1, 1)
                ]

                for dx, dy, rdx, rdy in directions:
                    nx, ny = px + dx, py + dy
                    nrx, nry = rx + rdx, ry + rdy
                    if (nx, ny) not in visited:
                        queue.append(((nx, ny), (nrx, nry)))

            all_blocks.append(tiles)

        if (len(all_blocks) == 0):
            raise Exception("no blocks detected")
        
        return all_blocks
    
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
        startingX += MINI_BLOCK_WIDTH // 6
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