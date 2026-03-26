class Sensors:
    def __init__(self):
        """ initializes the sensors, sets board to null but if app is open we could also just call initializeStateSpace """
        self.board = None

    def initializeStatespace(self):
        """ generates the actions the model should take based on the board state and given blocks """
        self._configureAppBoot()
        return None
    
    def _configureAppBoot(self):
        """ if we want the program to open the app we would do it in this method """
        return None
    
    def getBoard(self):
        """ returns the board state maintained in this object """
        return self.board
    
    def placeBlock(self):
        """ updates the maintained board with the block we chose to place down """
        return None
    
    def readBlocks(self):
        """ reads the three choice input blocks and returns a list for them """
        return None
