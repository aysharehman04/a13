import tkinter as tk
from a1_state import State
from a3_agent import Agent

# Example grid to initialise the State
initial_grid = [
    [2, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [1, 0, 2, 0, 1],
    [0, 0, 0, 1, 0]
]

state = State(initial_grid)

def on_click(r, c):
    print(f"Button clicked at ({r}, {c})")

root = tk.Tk()
root.title("B1 Hinger Game")

for r in range(state.rows):
    for c in range(state.cols):
        btn = tk.Button(
            root, 
            width=4,
            height=2,
            text=str(state.grid[r][c]),
            command=lambda r=r ,c=c: on_click(r,c)
        )
        btn.grid(row=r, column=c)

root.mainloop()


