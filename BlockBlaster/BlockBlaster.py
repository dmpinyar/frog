import sys
import os
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Main_Architecture'))

from Sensors import Sensors
from Model import Model

# --- swap this line to compare configurations ---
# Model()                                                        full (MRV + LCV + FC)
# Model(useLcv=False, useForwardChecking=False)                  MRV only
# Model(useMrv=False, useLcv=False)                              backtracking + FC only
# Model(useMrv=False, useLcv=False, useForwardChecking=False)    plain backtracking
ACTIVE_MODEL = Model()


class BlockBlaster:
    def __init__(self):
        self.sensors = Sensors()
        self.model = ACTIVE_MODEL

    def run(self):
        rounds = 0
        while True:
            board = self.sensors.getBoard()
            blocks = self.sensors.readBlocks()

            actions = self.model.generateActions(board, blocks)
            if actions is None:
                print(f"Game over. Rounds survived: {rounds}")
                break

            for block_idx, x, y in actions:
                self.sensors.placeBlock(x, y, blocks[block_idx], block_idx)

            self.sensors.board = self.sensors.initializeStatespace()
            rounds += 1
            time.sleep(3)



if __name__ == "__main__":
    BlockBlaster().run()
