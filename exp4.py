# Experiment 4 - BFS shortest path with Tkinter GUI
# INPUT (type in the window): Start Node = A, End Node = F  ->  ['A', 'C', 'F']
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
import tkinter as tk
from tkinter import messagebox

graph = {
    'A': ['B', 'C'], 'B': ['A', 'D', 'E'], 'C': ['A', 'F'],
    'D': ['B'], 'E': ['B', 'F'], 'F': ['C', 'E'],
}

def bfs_shortest_path(graph, start, end):
    queue, visited = deque([[start]]), {start}
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == end:
            return path
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    return None

def draw_graph(graph, shortest_path=None):
    G = nx.Graph(graph)
    pos = nx.spring_layout(G)
    fig, ax = plt.subplots(figsize=(6, 4))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray',
            node_size=2000, font_size=15, font_weight='bold', ax=ax)
    if shortest_path:
        edges = list(zip(shortest_path, shortest_path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='red',
                               width=2, style='dashed', ax=ax)
        nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_color='lightgreen', ax=ax)
    ax.set_title("Graph Visualization with Shortest Path Highlighted")
    return fig

def display_graph():
    start, end = start_entry.get().strip(), end_entry.get().strip()
    if start not in graph or end not in graph:
        messagebox.showerror("Error", "Invalid nodes.")
        return
    shortest_path = bfs_shortest_path(graph, start, end)
    result_label.config(
        text=f"Shortest path from {start} to {end}: {shortest_path if shortest_path else 'No path found.'}")
    fig = draw_graph(graph, shortest_path)
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=4, column=0, columnspan=3, pady=10)

if __name__ == "__main__":
    window = tk.Tk()
    window.title("BFS Shortest Path Finder")
    window.geometry("700x600")
    tk.Label(window, text="Start Node:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    start_entry = tk.Entry(window)
    start_entry.grid(row=0, column=1, padx=10, pady=10)
    tk.Label(window, text="End Node:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    end_entry = tk.Entry(window)
    end_entry.grid(row=1, column=1, padx=10, pady=10)
    tk.Button(window, text="Find Shortest Path", command=display_graph).grid(
        row=2, column=0, columnspan=3, pady=10)
    result_label = tk.Label(window, text="")
    result_label.grid(row=3, column=0, columnspan=3, pady=10)
    window.mainloop()
