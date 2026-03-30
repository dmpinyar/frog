from Tile import Tile

class Board:
    def __init__(self, width, height):
        """
        Creates a 2D grid of Tile objects
        """
        self.width = width
        self.height = height
        self.tiles = [
            [Tile(x, y, False) for y in range(height)]
            for x in range(width)
        ]

    def get_tile(self, x, y):
        """ Returns the Tile at (x, y) """
        self._validate_coordinates(x, y)
        return self.tiles[x][y]

    def set_tile(self, x, y, tile):
        """ Sets a Tile at (x, y) """
        self._validate_coordinates(x, y)
        if not isinstance(tile, Tile):
            raise TypeError("Expected a Tile object")
        self.tiles[x][y] = tile

    def get_tiles(self):
        """ Returns the entire 2D tile grid """
        return self.tiles

    def set_occupied(self, x, y):
        """ Marks the Tile at (x, y) as occupied """
        self._validate_coordinates(x, y)
        self.tiles[x][y].isOccupied = True

    def _validate_coordinates(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError(f"Coordinates ({x}, {y}) out of bounds")