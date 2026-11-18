
# Experiment 7: Travelling Salesman Problem Using A*
#
# INPUT FORMAT:
# Number of Cities: Any integer >= 2
# For each city, enter X and Y coordinates.
# City 0 is the starting and ending city.
#
# INPUT EXAMPLE:
# Number of Cities: 4
# City 0: X = 0,  Y = 0
# City 1: X = 0,  Y = 10
# City 2: X = 10, Y = 10
# City 3: X = 10, Y = 0
#
# EXPECTED OUTPUT:
# Optimal Tour: 0 -> 1 -> 2 -> 3 -> 0
# Total Distance: 40.00
#
# NOTE:
# The reverse tour is also optimal.
# A* finds an optimal tour when it completes.
# Large city counts can require significant time and memory.

import tkinter as tk
from tkinter import messagebox
import heapq
import math
import random
import threading
from functools import lru_cache

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def a_star_tsp(cities):
    n = len(cities)

    distances = [
        [
            math.hypot(
                cities[i][0] - cities[j][0],
                cities[i][1] - cities[j][1]
            )
            for j in range(n)
        ]
        for i in range(n)
    ]

    full_mask = (1 << n) - 1

    @lru_cache(maxsize=None)
    def mst_cost(mask):
        nodes = [
            i for i in range(n)
            if mask & (1 << i)
        ]

        if len(nodes) <= 1:
            return 0.0

        visited = {nodes[0]}
        total = 0.0

        while len(visited) < len(nodes):
            cost, next_city = min(
                (distances[i][j], j)
                for i in visited
                for j in nodes
                if j not in visited
            )

            total += cost
            visited.add(next_city)

        return total

    def heuristic(current, visited_mask):
        remaining = full_mask ^ visited_mask

        if remaining == 0:
            return distances[current][0]

        unvisited = [
            i for i in range(n)
            if remaining & (1 << i)
        ]

        return (
            mst_cost(remaining)
            + min(distances[current][i] for i in unvisited)
            + min(distances[0][i] for i in unvisited)
        )

    # Heap entry:
    # (f, tie_breaker, g, current, visited_mask, path)
    queue = [
        (heuristic(0, 1), 0, 0.0, 0, 1, (0,))
    ]

    best_g = {(0, 1): 0.0}
    counter = 0

    while queue:
        f, _, g, current, mask, path = heapq.heappop(queue)

        if g > best_g.get((current, mask), float("inf")):
            continue

        if mask == full_mask:
            total = g + distances[current][0]
            return list(path) + [0], total

        for next_city in range(1, n):
            bit = 1 << next_city

            if mask & bit:
                continue

            new_mask = mask | bit
            new_g = g + distances[current][next_city]
            state = (next_city, new_mask)

            if new_g < best_g.get(state, float("inf")):
                best_g[state] = new_g

                h = heuristic(next_city, new_mask)
                counter += 1

                heapq.heappush(
                    queue,
                    (
                        new_g + h,
                        counter,
                        new_g,
                        next_city,
                        new_mask,
                        path + (next_city,)
                    )
                )

    return None, None


class TSPApp:
    def __init__(self, root):
        self.root = root
        root.title("Experiment 7 - TSP Using A*")
        root.geometry("850x720")

        self.fields = []
        self.busy = False
        self.job_id = 0

        tk.Label(
            root,
            text="Travelling Salesman Problem Using A*",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        controls = tk.Frame(root)
        controls.pack(pady=8)

        tk.Label(
            controls, text="Number of Cities:"
        ).pack(side="left")

        self.count_entry = tk.Entry(controls, width=6)
        self.count_entry.insert(0, "4")
        self.count_entry.pack(side="left", padx=5)

        self.create_button = tk.Button(
            controls,
            text="Create Fields",
            command=self.create_fields
        )
        self.create_button.pack(side="left", padx=4)

        self.random_button = tk.Button(
            controls,
            text="Random Cities",
            command=self.random_cities
        )
        self.random_button.pack(side="left", padx=4)

        self.solve_button = tk.Button(
            controls,
            text="Solve TSP",
            command=self.solve
        )
        self.solve_button.pack(side="left", padx=4)

        tk.Button(
            controls,
            text="Reset",
            command=self.reset
        ).pack(side="left", padx=4)

        tk.Button(
            controls,
            text="Exit",
            command=root.destroy
        ).pack(side="left", padx=4)

        # Scrollable input area for larger city counts
        input_box = tk.Frame(root)
        input_box.pack(fill="x", padx=15, pady=5)

        self.input_canvas = tk.Canvas(
            input_box, height=140
        )
        scrollbar = tk.Scrollbar(
            input_box,
            orient="vertical",
            command=self.input_canvas.yview
        )

        self.input_canvas.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(side="right", fill="y")
        self.input_canvas.pack(
            side="left", fill="both", expand=True
        )

        self.field_frame = tk.Frame(self.input_canvas)

        self.input_canvas.create_window(
            (0, 0),
            window=self.field_frame,
            anchor="nw"
        )

        self.field_frame.bind(
            "<Configure>",
            lambda event: self.input_canvas.configure(
                scrollregion=self.input_canvas.bbox("all")
            )
        )

        self.result_label = tk.Label(
            root,
            text="Enter city coordinates and click Solve TSP",
            font=("Arial", 11),
            wraplength=800
        )
        self.result_label.pack(pady=8)

        self.figure = Figure(figsize=(7, 4.5))
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(
            self.figure, master=root
        )
        self.canvas.get_tk_widget().pack(
            fill="both", expand=True, padx=10, pady=5
        )

        self.create_fields()

    def get_count(self):
        try:
            n = int(self.count_entry.get())
        except ValueError:
            raise ValueError(
                "Enter a valid whole number of cities."
            )

        if n < 2:
            raise ValueError(
                "Number of cities must be at least 2."
            )

        return n

    def create_fields(self):
        if self.busy:
            return

        try:
            n = self.get_count()
        except ValueError as error:
            messagebox.showerror("Input Error", str(error))
            return

        for widget in self.field_frame.winfo_children():
            widget.destroy()

        self.fields = []

        for i in range(n):
            row = tk.Frame(self.field_frame)
            row.pack(pady=2)

            tk.Label(
                row, text=f"City {i}:", width=10
            ).pack(side="left")

            tk.Label(row, text="X:").pack(side="left")
            x = tk.Entry(row, width=10)
            x.pack(side="left", padx=5)

            tk.Label(row, text="Y:").pack(side="left")
            y = tk.Entry(row, width=10)
            y.pack(side="left", padx=5)

            self.fields.append((x, y))

        self.ax.clear()
        self.canvas.draw()

    def random_cities(self):
        if self.busy:
            return

        self.create_fields()

        for x, y in self.fields:
            x.insert(0, str(random.randint(0, 100)))
            y.insert(0, str(random.randint(0, 100)))

    def read_cities(self):
        n = self.get_count()

        if len(self.fields) != n:
            raise ValueError(
                "Click Create Fields after changing city count."
            )

        cities = []

        for i, (x, y) in enumerate(self.fields):
            try:
                px = float(x.get())
                py = float(y.get())
            except ValueError:
                raise ValueError(
                    f"Enter valid coordinates for City {i}."
                )

            if not math.isfinite(px) or not math.isfinite(py):
                raise ValueError(
                    "Coordinates must be finite numbers."
                )

            cities.append((px, py))

        return cities

    def solve(self):
        if self.busy:
            return

        try:
            cities = self.read_cities()
        except ValueError as error:
            messagebox.showerror("Input Error", str(error))
            return

        self.busy = True
        self.solve_button.config(state="disabled")
        self.create_button.config(state="disabled")
        self.random_button.config(state="disabled")

        self.result_label.config(
            text="Solving TSP using A*... Please wait."
        )

        self.job_id += 1
        job = self.job_id

        # Run the search outside Tkinter's main thread.
        # The worker does not directly modify GUI widgets.
        result = {}

        def worker():
            try:
                result["value"] = a_star_tsp(cities)
            except Exception as error:
                result["error"] = str(error)
            finally:
                result["done"] = True

        threading.Thread(
            target=worker,
            daemon=True
        ).start()

        def check_result():
            if job != self.job_id:
                return

            if not result.get("done"):
                self.root.after(100, check_result)
                return

            self.busy = False
            self.solve_button.config(state="normal")
            self.create_button.config(state="normal")
            self.random_button.config(state="normal")

            if "error" in result:
                messagebox.showerror(
                    "Solver Error", result["error"]
                )
                return

            tour, distance = result["value"]

            if tour is None:
                self.result_label.config(
                    text="No solution found."
                )
                return

            self.result_label.config(
                text=(
                    "Optimal Tour: "
                    + " -> ".join(map(str, tour))
                    + f"\nTotal Distance: {distance:.2f}"
                )
            )

            self.draw_graph(cities, tour)

        self.root.after(100, check_result)

    def draw_graph(self, cities, tour):
        self.ax.clear()

        x = [point[0] for point in cities]
        y = [point[1] for point in cities]

        self.ax.scatter(
            x, y, color="blue", s=90, zorder=3
        )

        for i, (px, py) in enumerate(cities):
            self.ax.annotate(
                str(i),
                (px, py),
                xytext=(5, 5),
                textcoords="offset points"
            )

        route_x = [cities[i][0] for i in tour]
        route_y = [cities[i][1] for i in tour]

        self.ax.plot(
            route_x, route_y,
            color="red",
            linewidth=2
        )

        self.ax.set_title("Optimal TSP Tour Using A*")
        self.ax.set_xlabel("X Coordinate")
        self.ax.set_ylabel("Y Coordinate")
        self.ax.grid(True, alpha=0.3)

        self.canvas.draw()

    def reset(self):
        if self.busy:
            messagebox.showinfo(
                "Solver Running",
                "Wait for the current search to finish."
            )
            return

        self.count_entry.delete(0, tk.END)
        self.count_entry.insert(0, "4")

        self.create_fields()

        self.result_label.config(
            text="Enter city coordinates and click Solve TSP"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = TSPApp(root)
    root.mainloop()
