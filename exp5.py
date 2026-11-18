# Experiment 5 - 8-puzzle with Best-First Search, Misplaced Tiles vs Manhattan
# INPUT: initial state [[1,2,3],[4,8,0],[7,6,5]], goal [[1,2,3],[4,5,6],[7,8,0]]
# Console mode (default) compares both heuristics; "python exp5_8puzzle.py gui" opens the GUI.
import heapq, copy, sys, time

GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
INITIAL_STATE = [[1, 2, 3], [4, 8, 0], [7, 6, 5]]

def misplaced_tiles(state):                     # h1
    return sum(1 for i in range(3) for j in range(3)
               if state[i][j] != 0 and state[i][j] != GOAL_STATE[i][j])

def manhattan_distance(state):                  # h2
    d = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                gx, gy = divmod(state[i][j] - 1, 3)
                d += abs(i - gx) + abs(j - gy)
    return d

def get_blank_pos(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def generate_successors(state):
    successors = []
    x, y = get_blank_pos(state)
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx_, ny_ = x + dx, y + dy
        if 0 <= nx_ < 3 and 0 <= ny_ < 3:
            s = copy.deepcopy(state)
            s[x][y], s[nx_][ny_] = s[nx_][ny_], s[x][y]
            successors.append(s)
    return successors

def key(state):
    return tuple(tuple(r) for r in state)

def best_first_search(initial_state, heuristic, timeout=10):
    """Returns (solution_path, nodes_expanded)."""
    start = time.time()
    counter = 0                                  # tie-breaker so lists are never compared
    frontier = [(heuristic(initial_state), counter, initial_state)]
    parent = {key(initial_state): None}
    expanded = 0
    while frontier:
        if time.time() - start > timeout:
            print("Search timed out.")
            return None, expanded
        _, _, current = heapq.heappop(frontier)
        expanded += 1
        if current == GOAL_STATE:
            path, k = [], key(current)
            while k is not None:                 # rebuild the real solution path
                path.append([list(r) for r in k])
                k = parent[k]
            return path[::-1], expanded
        for s in generate_successors(current):
            k = key(s)
            if k not in parent:
                parent[k] = key(current)
                counter += 1
                heapq.heappush(frontier, (heuristic(s), counter, s))
    return None, expanded

def run_console():
    for name, h in [("Misplaced Tiles", misplaced_tiles), ("Manhattan Distance", manhattan_distance)]:
        path, n = best_first_search(INITIAL_STATE, h)
        print(f"{name:20s} nodes expanded = {n:4d}, solution moves = {len(path)-1 if path else 'none'}")
        if name == "Manhattan Distance" and path:
            for st in path:
                print(*st, sep="\n"); print()

def run_gui():
    import tkinter as tk
    class PuzzleApp:
        def __init__(self, root):
            self.root = root
            root.title("8-Puzzle Solver")
            self.initial_state = copy.deepcopy(INITIAL_STATE)
            self.buttons = []
            for i in range(3):
                row = []
                for j in range(3):
                    b = tk.Button(root, width=5, height=2, font=("Helvetica", 18))
                    b.grid(row=i, column=j, padx=5, pady=5)
                    row.append(b)
                self.buttons.append(row)
            self.update_buttons(self.initial_state)
            tk.Button(root, text="Solve", command=self.solve).grid(row=3, column=0, columnspan=3)
        def update_buttons(self, state):
            for i in range(3):
                for j in range(3):
                    v = state[i][j]
                    bg = "skyblue" if v == 0 else ("lightgreen" if v == GOAL_STATE[i][j] else "lightcoral")
                    self.buttons[i][j].config(text="" if v == 0 else str(v), bg=bg, fg="black",
                                              relief="sunken" if v == 0 else "raised")
        def solve(self):
            path, n = best_first_search(self.initial_state, manhattan_distance)
            if path:
                for st in path:
                    self.update_buttons(st); self.root.update(); self.root.after(500)
            print("Nodes expanded:", n)
    root = tk.Tk(); PuzzleApp(root); root.mainloop()

if __name__ == "__main__":
    run_gui() if len(sys.argv) > 1 and sys.argv[1] == "gui" else run_console()
