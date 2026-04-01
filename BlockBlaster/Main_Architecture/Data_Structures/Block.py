class Block:
    def __init__(self, coordinateList):
        """
        initalizes Block object, either does it with a list of tiles or if not provided
        just initializes it all to false tiles. Kind of just leaving it open for implementation
        right now. Use setter method if we choose to build Blocks dynamically during execution
        """

        self.coordinateList = coordinateList
        maxX = 0
        maxY = 0
        for pair in coordinateList:
            if (maxX < pair[0]):
                maxX = pair[0]
            if (maxY < pair[1]):
                maxY = pair[1]

        self.width = maxX + 1
        self.height = maxY + 1

    def getTile(self, idx):
        """ returns the Tile at (x, y) """
        return self.coordinateList[idx]
    
    def getTiles(self):
        """ returns the entire tilelist """
        return self.coordinateList

    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height