# a4_game
"""
Hinger Game Core Gameplay Module
"""

import time
from a1_state import State
from a3_agent import Agent

def play(state, agentA=None, agentB=None, default_mode="alphabeta", turn_time_limit=None):
    """
    Simulate a Hinger game between two players (AI or human).
    
    Args:
        state (State): The initial game state.
        agentA (Agent or None): Player A agent, or None for human.
        agentB (Agent or None): Player B agent, or None for human.
        default_mode (str): The strategy mode to use for AI agents.
        turn_time_limit (float or None): Optional per-turn time limit in seconds.
        
    Returns:
        str or None: Name of the winner if there is one, else None for draw.
    """
    current_state = state.clone()
    players = [(agentA, "PlayerA"), (agentB, "PlayerB")]
    turn = 0
    move_count = 0
    move_history = []

    while True:
        agent, name = players[turn % 2]
        print(f"\n{name}'s turn (Move {move_count + 1}):")
        print(current_state)

        start_time = time.time()

        # Determine move
        if agent is None:
            # Human player
            try:
                r = int(input("Enter row: "))
                c = int(input("Enter column: "))
                move = (r, c)
            except ValueError:
                print(f"Invalid input! {name} loses.")
                return players[(turn + 1) % 2][1]
        else:
            # AI agent
            score_move = agent.move(current_state, default_mode)
            if score_move is None:
                print(f"No moves available for {name}. {players[(turn + 1) % 2][1]} wins!")
                return players[(turn + 1) % 2][1]
            _, move = score_move
            if not isinstance(move, tuple) or len(move) != 2:
                print(f"Invalid move format returned by {name}. {players[(turn + 1) % 2][1]} wins!")
                return players[(turn + 1) % 2][1]

        # Optional turn time limit
        if turn_time_limit is not None:
            elapsed = time.time() - start_time
            if elapsed > turn_time_limit:
                print(f"{name} exceeded turn time limit! {players[(turn + 1) % 2][1]} wins!")
                return players[(turn + 1) % 2][1]

        r, c = move

        # Check for illegal move
        if not (0 <= r < current_state.rows and 0 <= c < current_state.cols):
            print(f"Illegal move by {name}! {players[(turn + 1) % 2][1]} wins!")
            return players[(turn + 1) % 2][1]
        if current_state.grid[r][c] <= 0:
            print(f"Illegal move on empty cell by {name}! {players[(turn + 1) % 2][1]} wins!")
            return players[(turn + 1) % 2][1]

        # Apply move
        current_state.grid[r][c] -= 1
        move_count += 1
        move_history.append((name, (r, c)))

        # Check for hinger-triggered win
        if current_state.grid[r][c] == 0:
            regions_after = current_state.numRegions()
            if regions_after > 1:
                print(f"{name} triggered a hinger! {name} wins!")
                return name

        # Check for draw (all counters zero)
        if all(cell == 0 for row in current_state.grid for cell in row):
            print("All counters removed. Game is a draw!")
            return None

        # Next turn
        turn += 1

def tester():
    """
    Test the play() function by simulating a game between two AI agents.
    """
    initial_grid = [
        [1, 1, 0, 0],
        [0, 1, 0, 1],
        [1, 0, 1, 0],
        [0, 0, 0, 1]
    ]
    state = State(initial_grid)

    # Create two AI agents
    agentA = Agent(size=(4,4), name="AgentA")
    agentB = Agent(size=(4,4), name="AgentB")

    print("Starting Hinger game between AgentA and AgentB...")
    winner = play(state, agentA, agentB, default_mode="alphabeta", turn_time_limit=10)

    if winner is None:
        print("Game ended in a draw.")
    else:
        print(f"The winner is: {winner}")

if __name__ == "__main__":
    tester()
