
# Experiment 2: N Queens Using Backtracking
#
# INPUT FORMAT:
# Enter any positive integer N.
#
# INPUT EXAMPLES:
# N = 4
# N = 8
# N = 15
#
# EXPECTED OUTPUT:
# N = 4 -> [1, 3, 0, 2]
# N = 2 or 3 -> No solution exists
#
# NOTE:
# Larger N values may take longer to solve.

import tkinter as tk
from tkinter import messagebox


def solve_queens(n):
    board = [-1] * n
    columns = set()
    diagonal1 = set()
    diagonal2 = set()

    def place(row):
        if row == n:
            return True

        for col in range(n):
            d1 = row - col
            d2 = row + col

            if (col in columns or
                    d1 in diagonal1 or
                    d2 in diagonal2):
                continue

            board[row] = col
            columns.add(col)
            diagonal1.add(d1)
            diagonal2.add(d2)

            if place(row + 1):
                return True

            board[row] = -1
            columns.remove(col)
            diagonal1.remove(d1)
            diagonal2.remove(d2)

        return False

    if place(0):
        return board

    return None


class NQueensApp:
    def __init__(self, root):
        self.root = root
        root.title("Experiment 2 - N Queens")
        root.geometry("550x620")

        tk.Label(
            root,
            text="N Queens Using Backtracking",
            font=("Arial", 16, "bold")
        ).pack(pady=12)

        frame = tk.Frame(root)
        frame.pack(pady=8)

        tk.Label(frame, text="Enter N:").pack(side="left")

        self.n_entry = tk.Entry(frame, width=10)
        self.n_entry.pack(side="left", padx=6)

        tk.Button(
            frame, text="Solve", command=self.solve
        ).pack(side="left", padx=4)

        tk.Button(
            frame, text="Reset", command=self.reset
        ).pack(side="left", padx=4)

        tk.Button(
            frame, text="Exit", command=root.destroy
        ).pack(side="left", padx=4)

        self.canvas = tk.Canvas(
            root, width=450, height=450, bg="white"
        )
        self.canvas.pack(pady=12)

        self.result_label = tk.Label(
            root,
            text="Enter N and click Solve",
            font=("Arial", 11),
            wraplength=500
        )
        self.result_label.pack(pady=8)

    def reset(self):
        self.n_entry.delete(0, tk.END)
        self.canvas.delete("all")
        self.result_label.config(
            text="Enter N and click Solve"
        )

    def solve(self):
        try:
            n = int(self.n_entry.get())

            if n <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a positive integer."
            )
            return

        # No fixed maximum N
        # Backtracking may take longer for large N
        try:
            solution = solve_queens(n)
        except (RecursionError, MemoryError):
            messagebox.showerror(
                "Solver Error",
                "This N is too large for the current "
                "Python recursion or memory limits."
            )
            return

        self.canvas.delete("all")

        if solution is None:
            self.result_label.config(
                text=f"No solution exists for N = {n}"
            )
            return

        size = 450 / n

        for row in range(n):
            for col in range(n):
                color = (
                    "#f0d9b5"
                    if (row + col) % 2 == 0
                    else "#b58863"
                )

                self.canvas.create_rectangle(
                    col * size,
                    row * size,
                    (col + 1) * size,
                    (row + 1) * size,
                    fill=color,
                    outline=""
                )

            self.canvas.create_text(
                (solution[row] + 0.5) * size,
                (row + 0.5) * size,
                text="Q",
                font=(
                    "Arial",
                    max(1, int(size * 0.65)),
                    "bold"
                )
            )

        self.result_label.config(
            text=f"Solution for N = {n}: {solution}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = NQueensApp(root)
    root.mainloop()
