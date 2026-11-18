# Experiment 7 - TSP using A* (f = g + h, h = MST-based admissible heuristic)
# INPUT (in the window): number of cities = 12 -> click "Generate Cities" -> "Solve TSP"
# (Cities are random in 0..100 x 0..100. Allowed range: 2 to MAX_CITIES = 12.)
import heapq, math, random
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def mst_cost(cities, nodes):
    """Prim's MST over the given node indices."""
    nodes = list(nodes)
    if len(nodes) <= 1:
        return 0.0
    in_tree, total = {nodes[0]}, 0.0
    edges = [(dist(cities[nodes[0]], cities[n]), n) for n in nodes[1:]]
    heapq.heapify(edges)
    while edges and len(in_tree) < len(nodes):
        c, n = heapq.heappop(edges)
        if n in in_tree:
            continue
        in_tree.add(n); total += c
        for m in nodes:
            if m not in in_tree:
                heapq.heappush(edges, (dist(cities[n], cities[m]), m))
    return total

def heuristic(cities, current, unvisited):
    """MST(unvisited) + cheapest link from current + cheapest link back to start (admissible)."""
    if not unvisited:
        return dist(cities[current], cities[0])
    return (mst_cost(cities, unvisited)
            + min(dist(cities[current], cities[u]) for u in unvisited)
            + min(dist(cities[0], cities[u]) for u in unvisited))

MAX_CITIES = 12   # A* over (city, visited-set) states grows like n * 2^n; see README note below

def a_star_tsp(cities):
    """Optimal TSP tour by A*. Returns (tour, length).

    A node is either a partial tour (f = g + h) or a COMPLETED tour, i.e. every city visited
    AND the closing edge back to city 0 already added (f = g = true tour length).
    A tour is returned only when a completed-tour node is popped, so every other node
    still queued has f >= its cost. With an admissible h that guarantees optimality.
    """
    n = len(cities)
    if n < 2:
        raise ValueError("Need at least 2 cities.")
    if n > MAX_CITIES:
        raise ValueError(f"A* TSP is limited to {MAX_CITIES} cities (got {n}).")

    counter = 0                                   # tie-breaker for the heap
    best_g = {(0, frozenset([0])): 0.0}
    # entry: (f, tie, g, city, path, is_complete)
    open_list = [(heuristic(cities, 0, set(range(1, n))), counter, 0.0, 0, [0], False)]
    while open_list:
        f, _, g, cur, path, complete = heapq.heappop(open_list)
        if complete:                              # goal test: a finished, closed tour
            return path, g
        visited = frozenset(path)
        if g > best_g.get((cur, visited), float("inf")):
            continue                              # stale entry
        unvisited = set(range(n)) - visited
        if not unvisited:                         # all cities visited -> close the tour
            total = g + dist(cities[cur], cities[0])
            counter += 1
            heapq.heappush(open_list, (total, counter, total, 0, path + [0], True))
            continue
        for nxt in unvisited:
            ng = g + dist(cities[cur], cities[nxt])
            state = (nxt, visited | {nxt})
            if ng < best_g.get(state, float("inf")):
                best_g[state] = ng
                rest = unvisited - {nxt}
                h = heuristic(cities, nxt, rest)  # rest empty -> distance back to start
                counter += 1
                heapq.heappush(open_list, (ng + h, counter, ng, nxt, path + [nxt], False))
    return None, None

def plot_path(cities, path, total_cost):
    x, y = zip(*cities)
    plt.figure()
    plt.plot(x, y, 'o', color='blue')
    for i in range(len(path) - 1):
        a, b = cities[path[i]], cities[path[i + 1]]
        plt.plot([a[0], b[0]], [a[1], b[1]], 'r-')
    plt.title(f'TSP Solution - Total Distance: {total_cost:.2f}')
    plt.xlabel("X Coordinates"); plt.ylabel("Y Coordinates")
    plt.show()

def generate_cities():
    try:
        n = int(city_count_entry.get())
        if n < 2 or n > MAX_CITIES:
            raise ValueError(f"Please enter a number from 2 to {MAX_CITIES}.")
        cities.clear()
        cities.extend((random.randint(0, 100), random.randint(0, 100)) for _ in range(n))
        messagebox.showinfo("Success", f"{n} cities generated.")
    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))

def solve_tsp():
    if len(cities) < 2:
        messagebox.showerror("Error", "Generate cities first!")
        return
    path, total = a_star_tsp(cities)
    if path:
        print("Tour:", path, "Distance:", round(total, 2))
        plot_path(cities, path, total)
    else:
        messagebox.showerror("Error", "No solution found.")

cities = []
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Traveling Salesman Problem Solver")
    tk.Label(root, text="Enter number of cities:").pack()
    city_count_entry = tk.Entry(root)
    city_count_entry.pack()
    tk.Button(root, text="Generate Cities", command=generate_cities).pack()
    tk.Button(root, text="Solve TSP", command=solve_tsp).pack()
    root.mainloop()
