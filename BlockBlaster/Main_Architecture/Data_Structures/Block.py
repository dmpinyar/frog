from Data_Structures.Tile import Tile

class Block:
    def __init__(self, width, height, tileList):
        """
        initalizes Block object, either does it with a list of tiles or if not provided
        just initializes it all to false tiles. Kind of just leaving it open for implementation
        right now. Use setter method if we choose to build Blocks dynamically during execution
        """
        self.width = width
        self.height = height
        self.tileList = tileList

    def get_tile(self, idx):
        """ returns the Tile at (x, y) """
        return self.tiles[idx]

    def set_tile(self, idx, tile):
        """ replaces the Tile at (x, y) """
        if not isinstance(tile, Tile):
            raise TypeError("Expected a Tile object")
        self.tiles[idx]

    def get_tiles(self):
        """ returns the entire tilelist """
        return self.tileList

    def get_occupied(self, idx):
        """ returns isOccupied at (x, y) """
        return self.get_tile(idx).isOccupied

    def set_occupied(self, idx, isOccupied):
        """ updates isOccupied at (x, y) """
        self.get_tile(idx).isOccupied = isOccupied
