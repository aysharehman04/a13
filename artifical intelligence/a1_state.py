# a1_state
"""
Group ID: B1
Student IDs:
100464246


"""
"""
State class for the Hinger game
"""

from collections import deque
from copy import deepcopy
from itertools import count


class State:
    def __init__(self, grid):
        """
        Initialise a Hinger game state.
        Takes parameter grid which is a 2D list representing the number of counters in 
        each cell.
        """
        assert all(len(row) == len(grid[0]) for row in grid)
        self.grid = deepcopy(grid)
        self.rows = len(grid)
        self.cols = len(grid[0])
    
    def __str__(self):
        """
        Returns a readable string of the board.
        """
        return '\n'.join(' '.join(str(cell) for cell in row) for row in self.grid)
    
    def directions(self):
        """
        Returns all directions a player can move.
        """
        return [
            (-1,-1), #diagonal up-left
            (-1,0),  # above 
            (-1,1),  # diagonal up-right
            (0,-1),  # left
            (0,1),   # right
            (1,-1),  # diagonal down-left
            (1,0),   # down
            (1,1)    # diagonal down-right
        ]
    
    def numRegions(self):
        """
        Returns the number of active regions on the board.
        """
        visited = [[False]*self.cols for _ in range(self.rows)]
        regions = 0

        def bfs(sr, sc):
            queue = deque([(sr, sc)])
            visited[sr][sc] = True
            while queue:
                r, c = queue.popleft()
                for dr, dc in self.directions():
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        if self.grid[nr][nc] > 0 and not visited[nr][nc]:
                            visited[nr][nc] = True
                            queue.append((nr,nc))

        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] > 0 and not visited[r][c]:
                    bfs(r,c)
                    regions += 1
        return regions

       
    def numHingers(self):
        """
        Returns the number of hingers.
        A hinger is a special type of active cell: it has only one counter
        and when a move is made on a hinger (i.e., the last counter is removed from this cell), the
        cell becomes empty and the number of active regions on the board increases by one or
        more.
        """
        base_regions = self.numRegions()
        count = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 1:
                    new_state = self.clone()
                    new_state.grid[r][c] = 0
                    if new_state.numRegions() > base_regions:
                        count += 1
        return count

    
    def move_cost(self, r, c):
        """
        Returns the cost of a move at a cell (r, c)
        Cost is 1 + the number of active adjacent cells.
        Additional utility to support game play.
        """
        cost = 1
        for dr, dc in self.directions():
            nr, nc = r+dr, c+dc 
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.grid[nr][nc] > 0:
                    cost += 1
        return cost
    
    def moves(self):
        """
        This is a generator that yields all possible states after removing 1 counter from any 
        active cell.
        Each yeilded value is a truple (new_state, move_position, move_cost)
        """
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] > 0: # active cell
                    new_state = deepcopy(self)
                    new_state.grid[r][c] -= 1
                    yield (new_state, (r,c), self.move_cost(r, c))
    
    def clone(self):
        """
        Returns a deepcopy of the state.
        """
        return deepcopy(self)
    
    def is_binary(self):
        """
        Return True if all cells contain 0 or 1 counters
        """
        return all(cell in (0,1) for row in self.grid for cell in row)

def tester():
        """
        Tester for the Hinger state.
        """
        print("Hinger state tester:")

        sa_grid = [
            [2, 1, 0, 0, 0],
            [0, 1, 0, 1, 0],
            [1, 0, 2, 0, 1],
            [0, 0, 0, 1, 0]
        ]
        sa = State(sa_grid)

        print("\nState A:")
        print(sa)

        print("\nNumber of active regions:", sa.numRegions())
        print("Number of hinger cells:", sa.numHingers())

        print("\nPossible moves from State A:")
        for new_state, pos, cost in sa.moves():
            print(f"Move at {pos} (cost {cost}):")
            print(new_state)
            print("----")
    
if __name__ == "__main__":
     tester()





    

                       



    
