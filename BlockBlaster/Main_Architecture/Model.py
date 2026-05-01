boardWidth, boardHeight = 8, 8


class Model:
    def __init__(self, useMrv=True, useLcv=True, useForwardChecking=True):
        '''
        True if you want to use a specific variable constraint heuristic,
        False if you want it off.
        '''
        self.useMrv = useMrv
        self.useLcv = useLcv
        self.useForwardChecking = useForwardChecking

    def generateActions(self, board, blocks):
        '''
        Returns the best actions to take depending on the heuristics enabled.
        Should return as a list (block index, x, y) as the elements.
        '''
        grid = [[board.get_tile(x, y).isOccupied for y in range(boardHeight)] for x in range(boardWidth)]
        best = {'actions': None, 'score': float('-inf')}
        self._solve(grid, blocks, list(range(len(blocks))), [], best)
        return best['actions']

    def _solve(self, grid, blocks, unplaced, actions, best):
        '''
        Backtracking is the baseline. It checks to see if the heuristics are
        on, if they are then it uses them to get the best actions.
        '''
        if not unplaced:
            score = sum(not grid[x][y] for x in range(boardWidth) for y in range(boardHeight))
            if score > best['score']:
                best['score'] = score
                best['actions'] = list(actions)
            return

        # MRV: picking the block that has the least number of valid placements.
        if self.useMrv:
            idx = min(unplaced, key=lambda i: len(self._placements(grid, blocks[i])))
        else:
            idx = unplaced[0]
        block = blocks[idx]
        remaining = [i for i in unplaced if i != idx]

        candidates = self._placements(grid, block)

        # LCV: look for placements that leaves the most options for the remaining blocks.
        if self.useLcv and remaining:
            candidates = sorted(
                candidates,
                key=lambda p: sum(len(self._placements(self._place(grid, block, p[0], p[1]), blocks[i])) for i in remaining),
                reverse=True
            )

        for x, y in candidates:
            newGrid = self._place(grid, block, x, y)

            # Forward checking: skip if any remaining block has no valid placement
            if self.useForwardChecking and any(not self._placements(newGrid, blocks[i]) for i in remaining):
                continue

            actions.append((idx, x, y))
            self._solve(newGrid, blocks, remaining, actions, best)
            actions.pop()

    def _placements(self, grid, block):
        '''
        For any given block, this should return all the valid placements,
        depending on the current board.
        '''
        validPlacements = []

        for x in range(boardWidth - block.getWidth() + 1):
            for y in range(boardHeight - block.getHeight() + 1):
                valid = True

                for tx, ty in block.getTiles():
                    if grid[x + tx][y + block.getHeight() - 1 - ty]:
                        valid = False
                        break

                if valid:
                    validPlacements.append((x, y))

        return validPlacements

    def _place(self, grid, block, x, y):
        '''
        This returns a new grid with the block placed at x,y.
        '''
        g = [col[:] for col in grid]

        for tx, ty in block.getTiles():
            g[x + tx][y + block.getHeight() - 1 - ty] = True

        # getting all full rows
        fullRows = set()
        for r in range(boardHeight):
            if all(g[c][r] for c in range(boardWidth)):
                fullRows.add(r)
        
        #same thing just for columns
        fullCols = set()
        for c in range(boardWidth):
            if all(g[c][r] for r in range(boardHeight)):
                fullCols.add(c)

        # since they're full, need to reset them to empty
        for r in fullRows:
            for c in range(boardWidth):
                g[c][r] = False

        for c in fullCols:
            for r in range(boardHeight):
                g[c][r] = False

        return g
