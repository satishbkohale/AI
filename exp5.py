
# Experiment 5: 8-Puzzle Using Greedy Best-First Search
#
# INPUT FORMAT:
# Enter 9 numbers from 0 to 8, separated by spaces.
# 0 represents the empty tile.
#
# INPUT EXAMPLE:
# Initial State: 1 2 3 4 8 0 7 6 5
# Goal State:    1 2 3 4 5 6 7 8 0
# Heuristic: Manhattan Distance
#
# EXPECTED OUTPUT:
# Puzzle solved in 5 moves.
#
# NOTE:
# Greedy Best-First Search uses only h(n).
# It does not guarantee the shortest solution.

import tkinter as tk
from tkinter import messagebox
import heapq
from itertools import count


def heuristic(state, goal, method):
    if method == "Misplaced Tiles":
        return sum(
            1 for i in range(9)
            if state[i] != 0 and state[i] != goal[i]
        )

    distance = 0

    for i in range(9):
        tile = state[i]

        if tile != 0:
            j = goal.index(tile)

            distance += (
                abs(i // 3 - j // 3)
                + abs(i % 3 - j % 3)
            )

    return distance


def get_neighbors(state):
    neighbors = []
    zero = state.index(0)

    row, col = divmod(zero, 3)

    moves = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    for dr, dc in moves:
        nr, nc = row + dr, col + dc

        if 0 <= nr < 3 and 0 <= nc < 3:
            new_state = list(state)
            new_pos = nr * 3 + nc

            new_state[zero], new_state[new_pos] = (
                new_state[new_pos], new_state[zero]
            )

            neighbors.append(tuple(new_state))

    return neighbors


def is_solvable(start, goal):
    def inversions(state):
        values = [x for x in state if x != 0]

        return sum(
            values[i] > values[j]
            for i in range(len(values))
            for j in range(i + 1, len(values))
        )

    return inversions(start) % 2 == inversions(goal) % 2


def greedy_best_first(start, goal, method):
    counter = count()

    queue = [
        (heuristic(start, goal, method),
         next(counter), start)
    ]

    visited = set()
    parent = {start: None}

    while queue:
        _, _, current = heapq.heappop(queue)

        if current in visited:
            continue

        visited.add(current)

        if current == goal:
            path = []

            while current is not None:
                path.append(current)
                current = parent[current]

            return path[::-1]

        for neighbor in get_neighbors(current):
            if neighbor not in visited and neighbor not in parent:
                parent[neighbor] = current

                heapq.heappush(
                    queue,
                    (
                        heuristic(neighbor, goal, method),
                        next(counter),
                        neighbor
                    )
                )

    return None


class PuzzleApp:
    def __init__(self, root):
        self.root = root
        root.title("Experiment 5 - 8 Puzzle")
        root.geometry("550x630")

        tk.Label(
            root,
            text="8-Puzzle Using Greedy Best-First Search",
            font=("Arial", 15, "bold")
        ).pack(pady=12)

        tk.Label(root, text="Initial State:").pack()

        self.initial_entry = tk.Entry(
            root, width=35, justify="center"
        )
        self.initial_entry.pack(pady=5)

        tk.Label(root, text="Goal State:").pack()

        self.goal_entry = tk.Entry(
            root, width=35, justify="center"
        )
        self.goal_entry.pack(pady=5)

        tk.Label(root, text="Select Heuristic:").pack()

        self.method = tk.StringVar(
            value="Manhattan Distance"
        )

        tk.OptionMenu(
            root,
            self.method,
            "Manhattan Distance",
            "Misplaced Tiles"
        ).pack(pady=5)

        frame = tk.Frame(root)
        frame.pack(pady=12)

        tk.Button(
            frame, text="Solve", command=self.solve
        ).pack(side="left", padx=5)

        tk.Button(
            frame, text="Reset", command=self.reset
        ).pack(side="left", padx=5)

        tk.Button(
            frame, text="Exit", command=root.destroy
        ).pack(side="left", padx=5)

        self.canvas = tk.Canvas(
            root, width=300, height=300, bg="white"
        )
        self.canvas.pack(pady=10)

        self.result_label = tk.Label(
            root,
            text="Enter puzzle states and click Solve",
            font=("Arial", 11)
        )
        self.result_label.pack(pady=8)

        self.step_label = tk.Label(
            root, text="", font=("Arial", 11)
        )
        self.step_label.pack()

        self.path = []
        self.step = 0
        self.animation_id = None

    def parse_state(self, text):
        try:
            numbers = tuple(map(int, text.split()))
        except ValueError:
            raise ValueError(
                "Enter numbers separated by spaces."
            )

        if len(numbers) != 9 or set(numbers) != set(range(9)):
            raise ValueError(
                "Enter each number from 0 to 8 exactly once."
            )

        return numbers

    def draw_board(self, state):
        self.canvas.delete("all")

        size = 100

        for i, value in enumerate(state):
            row, col = divmod(i, 3)

            x1 = col * size
            y1 = row * size

            color = "#ffffff" if value == 0 else "#add8e6"

            self.canvas.create_rectangle(
                x1, y1,
                x1 + size, y1 + size,
                fill=color,
                outline="black",
                width=2
            )

            if value != 0:
                self.canvas.create_text(
                    x1 + size / 2,
                    y1 + size / 2,
                    text=str(value),
                    font=("Arial", 26, "bold")
                )

    def cancel_animation(self):
        if self.animation_id is not None:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None

    def reset(self):
        self.cancel_animation()

        self.initial_entry.delete(0, tk.END)
        self.goal_entry.delete(0, tk.END)

        self.method.set("Manhattan Distance")

        self.canvas.delete("all")

        self.result_label.config(
            text="Enter puzzle states and click Solve"
        )

        self.step_label.config(text="")

        self.path = []
        self.step = 0

    def solve(self):
        self.cancel_animation()

        try:
            start = self.parse_state(
                self.initial_entry.get()
            )

            goal = self.parse_state(
                self.goal_entry.get()
            )

        except ValueError as error:
            messagebox.showerror(
                "Invalid Input", str(error)
            )
            return

        if not is_solvable(start, goal):
            messagebox.showerror(
                "Unsolvable Puzzle",
                "The initial state cannot reach the goal state."
            )
            return

        self.path = greedy_best_first(
            start, goal, self.method.get()
        )

        if self.path is None:
            self.result_label.config(
                text="No solution found."
            )
            return

        self.result_label.config(
            text=f"Puzzle Solved in {len(self.path) - 1} Moves"
        )

        self.step = 0
        self.animate()

    def animate(self):
        self.animation_id = None

        if self.step >= len(self.path):
            return

        self.draw_board(self.path[self.step])

        self.step_label.config(
            text=f"Step {self.step} of {len(self.path) - 1}"
        )

        self.step += 1

        if self.step < len(self.path):
            self.animation_id = self.root.after(
                700, self.animate
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleApp(root)
    root.mainloop()
