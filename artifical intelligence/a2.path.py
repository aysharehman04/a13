# a2_path
"""
Group ID: B1
Student IDs:
100464246


"""

from a1_state import State
from copy import deepcopy
import heapq

"""

Helper functions

"""
def grid_to_key(grid):
    """Converts a 2D grid into a tuple-of-tuples for easy comparison."""
    return tuple(tuple(row) for row in grid)

def states_equal(s1, s2):
    """Returns True if two states have identical grids."""
    return s1.grid == s2.grid


def is_safe(state):
    """Returns True if a state is safe meaning it contains no hingers."""
    return state.numHingers() == 0


def move_cost_between(s1, s2):
    """Returns the cost of the move between s1 and s2."""
    for r in range(s1.rows):
        for c in range(s1.cols):
            if s1.grid[r][c] - s2.grid[r][c] == 1:
                return s1.move_cost(r, c)
    return 0


def path_cost(path):
    """Computes the total cost along a path along with a list of States."""
    total = 0
    for i in range(len(path) - 1):
        total += move_cost_between(path[i], path[i + 1])
    return total

"""
Breadth-First Search
Uses a queue to explore states level by level.
Stops when the end state is found.
"""
def path_BFS(start, end):
    if not is_safe(start) or not is_safe(end):
        return None
    if states_equal(start, end):
        return [start]

    frontier = [(start, [start])]
    visited = {grid_to_key(start.grid)}

    while frontier:
        current, path = frontier.pop(0)
        for next_state, pos, cost in current.moves():
            key = grid_to_key(next_state.grid)
            if key in visited or not is_safe(next_state):
                continue
            visited.add(key)
            new_path = path + [next_state]
            if states_equal(next_state, end):
                return new_path
            frontier.append((next_state, new_path))
    return None

"""
Depth-First Search
Uses a stack to explore states deeply before backtracking.
Uses a limit to avoid infinite loops.

"""
def path_DFS(start, end, limit=100):
    if not is_safe(start) or not is_safe(end):
        return None
    if states_equal(start, end):
        return [start]

    stack = [(start, [start])]
    visited = {grid_to_key(start.grid)}
    steps = 0

    while stack:
        current, path = stack.pop()
        steps += 1
        if steps > limit:
            return None
        for next_state, pos, cost in current.moves():
            key = grid_to_key(next_state.grid)
            if key in visited or not is_safe(next_state):
                continue
            visited.add(key)
            new_path = path + [next_state]
            if states_equal(next_state, end):
                return new_path
            stack.append((next_state, new_path))
    return None


# =====================================================
# Iterative Deepening DFS
# =====================================================
def _limited_dfs(current, end, depth, visited):
    if states_equal(current, end):
        return [current]
    if depth == 0:
        return None
    for next_state, pos, cost in current.moves():
        key = grid_to_key(next_state.grid)
        if key in visited or not is_safe(next_state):
            continue
        visited.add(key)
        result = _limited_dfs(next_state, end, depth - 1, visited)
        visited.remove(key)
        if result:
            return [current] + result
    return None


def path_IDDFS(start, end, max_depth=20):
    if not is_safe(start) or not is_safe(end):
        return None
    if states_equal(start, end):
        return [start]

    for depth in range(1, max_depth + 1):
        visited = {grid_to_key(start.grid)}
        result = _limited_dfs(start, end, depth, visited)
        if result:
            return result
    return None


# =====================================================
# A* Search
# =====================================================
def manhattan_heuristic(start, end):
    """
    Manhattan-style heuristic: sum of distances between active cells.
    Sorted in row-major order. Admissible but simple.
    """
    s1 = [(r, c) for r in range(start.rows) for c in range(start.cols) if start.grid[r][c] == 1]
    s2 = [(r, c) for r in range(end.rows) for c in range(end.cols) if end.grid[r][c] == 1]
    s1.sort()
    s2.sort()

    total = 0
    for p1, p2 in zip(s1, s2):
        total += abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    total += abs(len(s1) - len(s2))
    return total


def path_astar(start, end):
    if not is_safe(start) or not is_safe(end):
        return None
    if states_equal(start, end):
        return [start]

    open_heap = []
    start_key = grid_to_key(start.grid)
    heapq.heappush(open_heap, (manhattan_heuristic(start, end), start))
    came_from = {start_key: None}
    g_score = {start_key: 0}

    while open_heap:
        _, current = heapq.heappop(open_heap)
        current_key = grid_to_key(current.grid)

        if states_equal(current, end):
            path = []
            while current_key:
                prev_state = State([list(r) for r in current_key])
                path.insert(0, prev_state)
                current_key = came_from[current_key]
            return path

        for next_state, pos, cost in current.moves():
            if not is_safe(next_state):
                continue
            key = grid_to_key(next_state.grid)
            tentative_g = g_score[current_key] + cost
            if key not in g_score or tentative_g < g_score[key]:
                came_from[key] = current_key
                g_score[key] = tentative_g
                f_score = tentative_g + manhattan_heuristic(next_state, end)
                heapq.heappush(open_heap, (f_score, next_state))
    return None


# =====================================================
# Minimal Safe Path (returns list of moves)
# =====================================================
def min_safe(start, end):
    """
    Returns the minimal-cost safe path (list of (r,c) moves).
    Uses Dijkstra-like search, as it guarantees minimal move cost.
    """
    if not is_safe(start) or not is_safe(end):
        return None
    if states_equal(start, end):
        return []

    import heapq
    heap = [(0, start, [])]  # cost, state, moves
    visited = {}

    while heap:
        cost_so_far, current, moves = heapq.heappop(heap)
        key = grid_to_key(current.grid)
        if key in visited and visited[key] <= cost_so_far:
            continue
        visited[key] = cost_so_far

        if states_equal(current, end):
            return moves

        for next_state, pos, move_cost_val in current.moves():
            if not is_safe(next_state):
                continue
            heapq.heappush(heap, (cost_so_far + move_cost_val, next_state, moves + [pos]))
    return None


# =====================================================
# Compare all algorithms
# =====================================================
def compare(start, end):
    """Compare BFS, DFS, IDDFS, A*, min_safe on a pair of states."""
    algos = [
        ("BFS", path_BFS),
        ("DFS", path_DFS),
        ("IDDFS", path_IDDFS),
        ("A*", path_astar),
        ("min_safe", min_safe)
    ]
    print("\nComparison of search algorithms:")
    for name, func in algos:
        path = func(start, end)
        if path is None:
            print(f"{name:8} | Failed to find a path")
        else:
            if name == "min_safe":
                total = sum(start.move_cost(r, c) for r, c in path)
                print(f"{name:8} | Success | Moves: {len(path)} | Total cost: {total}")
            else:
                print(f"{name:8} | Success | Path length: {len(path)} | Total cost: {path_cost(path)}")


# =====================================================
# Tester
# =====================================================
def tester():
    """Tester for a2_path.py"""
    print("=== a2_path.py tester ===")
    start_grid = [
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    end_grid = [
        [0, 1, 1],
        [0, 0, 1],
        [0, 0, 0]
    ]
    start = State(start_grid)
    end = State(end_grid)

    print("\nStart State:")
    print(start)
    print("\nEnd State:")
    print(end)

    compare(start, end)


if __name__ == "__main__":
    tester()
