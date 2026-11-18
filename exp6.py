
# Experiment 6: Means-End Analysis (MEA)
# Robot Navigation Using Python
#
# INPUT FORMAT:
# Grid Size: Positive integer
# Start X: Starting row (0-based)
# Start Y: Starting column (0-based)
# Goal X: Destination row (0-based)
# Goal Y: Destination column (0-based)
#
# INPUT EXAMPLE:
# Grid Size: 10
# Start X: 2
# Start Y: 3
# Goal X: 5
# Goal Y: 7
#
# EXPECTED OUTPUT:
# Path: (2,3) -> (3,3) -> (4,3) -> (5,3)
#       -> (5,4) -> (5,5) -> (5,6) -> (5,7)
# Total Moves: 7
#
# NOTE:
# MEA reduces the difference between the current
# position and goal position, one step at a time.
# This implementation moves along X first, then Y.

import tkinter as tk
from tkinter import messagebox


def means_end_analysis(start, goal):
    x, y = start
    gx, gy = goal

    path = [(x, y)]

    while (x, y) != (gx, gy):
        if x < gx:
            x += 1
        elif x > gx:
            x -= 1
        elif y < gy:
            y += 1
        elif y > gy:
            y -= 1

        path.append((x, y))

    return path


class MEAApp:
    def __init__(self, root):
        self.root = root
        root.title("Experiment 6 - Means-End Analysis")
        root.geometry("650x720")

        tk.Label(
            root,
            text="Robot Navigation Using MEA",
            font=("Arial", 16, "bold")
        ).pack(pady=12)

        input_frame = tk.Frame(root)
        input_frame.pack(pady=8)

        labels = [
            "Grid Size",
            "Start X",
            "Start Y",
            "Goal X",
            "Goal Y"
        ]

        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(
                input_frame,
                text=label + ":"
            ).grid(
                row=i, column=0,
                padx=8, pady=4, sticky="e"
            )

            entry = tk.Entry(input_frame, width=12)
            entry.grid(
                row=i, column=1,
                padx=8, pady=4
            )

            self.entries[label] = entry

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Solve",
            command=self.solve
        ).pack(side="left", padx=6)

        tk.Button(
            button_frame,
            text="Reset",
            command=self.reset
        ).pack(side="left", padx=6)

        tk.Button(
            button_frame,
            text="Exit",
            command=root.destroy
        ).pack(side="left", padx=6)

        self.canvas = tk.Canvas(
            root,
            width=450,
            height=450,
            bg="white"
        )
        self.canvas.pack(pady=10)

        self.result_label = tk.Label(
            root,
            text="Enter positions and click Solve",
            font=("Arial", 11),
            wraplength=600
        )
        self.result_label.pack(pady=5)

        self.step_label = tk.Label(
            root,
            text="",
            font=("Arial", 11)
        )
        self.step_label.pack()

        self.path = []
        self.step = 0
        self.grid_size = 10
        self.animation_id = None

    def reset(self):
        self.cancel_animation()

        for entry in self.entries.values():
            entry.delete(0, tk.END)

        self.canvas.delete("all")

        self.result_label.config(
            text="Enter positions and click Solve"
        )

        self.step_label.config(text="")

        self.path = []
        self.step = 0

    def cancel_animation(self):
        if self.animation_id is not None:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None

    def draw_grid(self, robot_position):
        self.canvas.delete("all")

        n = self.grid_size
        cell = 450 / n

        for row in range(n):
            for col in range(n):
                x1 = col * cell
                y1 = row * cell

                position = (row, col)

                if position == robot_position:
                    color = "#ffcc66"
                elif position == self.goal:
                    color = "#90ee90"
                else:
                    color = "white"

                self.canvas.create_rectangle(
                    x1, y1,
                    x1 + cell,
                    y1 + cell,
                    fill=color,
                    outline="gray"
                )

        row, col = robot_position

        self.canvas.create_text(
            (col + 0.5) * cell,
            (row + 0.5) * cell,
            text="R",
            font=(
                "Arial",
                max(1, int(cell * 0.5)),
                "bold"
            )
        )

        gr, gc = self.goal

        if robot_position != self.goal:
            self.canvas.create_text(
                (gc + 0.5) * cell,
                (gr + 0.5) * cell,
                text="G",
                font=(
                    "Arial",
                    max(1, int(cell * 0.5)),
                    "bold"
                )
            )

    def solve(self):
        self.cancel_animation()

        try:
            n = int(
                self.entries["Grid Size"].get()
            )

            sx = int(
                self.entries["Start X"].get()
            )

            sy = int(
                self.entries["Start Y"].get()
            )

            gx = int(
                self.entries["Goal X"].get()
            )

            gy = int(
                self.entries["Goal Y"].get()
            )

            if n <= 0:
                raise ValueError(
                    "Grid size must be positive."
                )

            for value in (sx, sy, gx, gy):
                if not 0 <= value < n:
                    raise ValueError(
                        f"Coordinates must be between 0 and {n - 1}."
                    )

        except ValueError as error:
            messagebox.showerror(
                "Invalid Input",
                str(error)
            )
            return

        self.grid_size = n
        self.goal = (gx, gy)

        self.path = means_end_analysis(
            (sx, sy),
            self.goal
        )

        self.step = 0

        path_text = " -> ".join(
            str(position) for position in self.path
        )

        self.result_label.config(
            text=f"Total Moves: {len(self.path) - 1}\n"
                 f"Path: {path_text}"
        )

        self.animate()

    def animate(self):
        self.animation_id = None

        if self.step >= len(self.path):
            return

        self.draw_grid(
            self.path[self.step]
        )

        self.step_label.config(
            text=f"Step {self.step} of {len(self.path) - 1}"
        )

        self.step += 1

        if self.step < len(self.path):
            self.animation_id = self.root.after(
                500,
                self.animate
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = MEAApp(root)
    root.mainloop()
