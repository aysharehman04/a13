#a3_agent
"""
Group ID: B1
Student ID: 
100464246

Agent class for the Hinger Game
Integrates multiple strategies: minimax, alphabeta, and MCTS.
"""

import random
import math
from a1_state import State
import timeit

class Agent:
    def __init__(self, size, name='B1'):
        self.size = size
        self.name = name
        self.modes = ['minimax', 'alphabeta', 'mcts']

    def __str__(self):
        return f"Agent name: {self.name}, Board size: {self.size}, Modes: {self.modes}"

   
    def move(self, state, mode='mcts'):
        if self.is_terminal(state):
            return None
        if mode == 'mcts':
            return self.monte_carlo_tree_search(state, iterations=500)
        elif mode == 'minimax':
            _, move = self.minimax_move(state)
            return move
        elif mode == 'alphabeta':
            _, move = self.alphabeta_move(state, float('-inf'), float('inf'))
            return move
        else:
            raise ValueError(f"Unknown mode: {mode}")

    def is_terminal(self, state):
        if self.win():
            print("This state is in a winning position for the player whose turn is to move")
            return True
        for row in state.grid:
            for cell in row:
                if cell > 0: # found a move
                    return False
        return True # no moves found

    def win(self, state):
        return state.numHingers() > 0

    def evaluate(self,state):
        total_move_cost = sum(state.move_cost(r, c)
                              for r in range(state.rows)
                              for c in range(state.cols)
                              if state.grid[r][c] > 0)
        hinger_score = -state.numHingers() # fewer hingers is better
        region_score = state.numRegions() # fewer regions is better
        score = total_move_cost + 2 * region_score + 3 * hinger_score # weighted sum
        return score

   
    def minimax_move(self, state, depth=3, max_player=True):
        if depth == 0 or self.is_terminal(state):
            return self.evaluate(state), None

        if max_player:
            best_score = float('-inf')
            best_move = None
            for new_state, move, cost in state.moves():
                score, _ = self.minimax_move(new_state, depth-1, False)
                if score > best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move
        else:
            best_score = float('inf')
            best_move = None
            for new_state, move, cost in state.moves():
                score, _ = self.minimax_move(new_state, depth-1, True)
                if score < best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move

    
    def alphabeta_move(self, state,alpha=float("-inf"), beta=float("inf"), depth=3, max_player=True):
        #base case:
        if depth == 0 or self.is_terminal(state):
            return self.evaluate(state), None

        if max_player:
            max_score = float('-inf')
            best_move = None
            for new_state, move, cost in state.moves():
                score, _ = self.alphabeta_move(new_state, alpha, beta, depth-1, False)
                if score > max_score:
                    max_score = score
                    best_move = move
                alpha = max(alpha, max_score)
                if alpha >= beta:
                    break  # β cutoff → prune
            return max_score, best_move
        else:
            min_score = float('inf')
            best_move = None
            for new_state, move, cost in state.moves():
                score, _ = self.alphabeta_move(new_state, alpha, beta, depth-1, True)
                if score < min_score:
                    min_score = score
                    best_move = move
                beta = min(beta, min_score)
                if beta <= alpha:
                    break  # α cutoff → prune
            return min_score, best_move

    #  Monte Carlo Tree Search (MCTS)
   
    class Node:
        def __init__(self, state, parent=None, move=None):
            self.state = state
            self.parent = parent
            self.children = []
            self.visits = 0
            self.wins = 0
            self.untried_moves = [move for _, move, _ in state.moves()]
            self.move = move

    def monte_carlo_tree_search(self, state, iterations=500):
        root = self.Node(state)

        for _ in range(iterations):
            node = self.select(root)
            child = self.expand(node)
            result = self.simulate(child.state)
            self.backpropagate(child, result)

        if not root.children:
            return None
        best_child = max(root.children, key=lambda n: n.visits)
        return best_child.move

    def select(self, node):
        while node.untried_moves == [] and node.children:
            node = max(node.children, key=self.uct)
        return node

    def expand(self, node):
        if not node.untried_moves:
            return node
        move = random.choice(node.untried_moves)
        node.untried_moves.remove(move)
        new_state = self.apply_move(node.state, move)
        child_node = self.Node(new_state, parent=node, move=move)
        node.children.append(child_node)
        return child_node

    def simulate(self, state):
        current_state = state.clone()
        while not self.is_terminal(current_state):
            moves = [move for _, move, _ in current_state.moves()]
            if not moves:
                break
            move = random.choice(moves)
            current_state = self.apply_move(current_state, move)
        return 1 if self.win(current_state) else 0

    def backpropagate(self, node, result):
        while node:
            node.visits += 1
            node.wins += result
            node = node.parent

    def uct(self, node):
        if node.visits == 0:
            return float('inf')
        parent_visits = node.parent.visits
        return (node.wins / node.visits) + math.sqrt(2 * math.log(parent_visits) / node.visits)

    def apply_move(self, state, move):
        new_state = state.clone()
        r, c = move
        if new_state.grid[r][c] > 0:
            new_state.grid[r][c] -= 1
        return new_state


def tester():
    print("Agent state tester:")
    agent = Agent((4,5))
    print(agent)

    sa_grid = [
        [1, 1, 0, 0, 1],
        [1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1],
        [0, 0, 0, 1, 1]
    ]
    sa = State(sa_grid)
    print("Is terminal?",agent.is_terminal(sa))
    print("\n")


    print("Testing Minimax:")
    def run_minimax():
        score, move = agent.minimax_move(sa)
        # print(score, move)
        print("\n")

    avg_time = timeit.timeit(run_minimax, number=10) / 10
    print(f"Average Minimax time over 10 runs: {avg_time:.6f} seconds")

    print("Testing Alphabeta:")
    def run_alphabeta():
        score, move = agent.alphabeta_move(sa)
        # print(score, move)
        print("\n")

    avg_time = timeit.timeit(run_alphabeta, number=10) / 10
    print(f"Average alphabeta time over 10 runs: {avg_time:.6f} seconds")


    

    print("\nAgent selects a move using MCTS:")
    move = agent.move(sa, 'mcts')
    print("Selected move:", move)

    print("\nAgent selects a move using Minimax:")
    move = agent.move(sa, 'minimax')
    print("Selected move:", move)

    print("\nAgent selects a move using Alpha-Beta pruning:")
    move = agent.move(sa, 'alphabeta')
    print("Selected move:", move)

if __name__ == "__main__":
    tester()
