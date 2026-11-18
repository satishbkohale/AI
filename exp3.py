
# Experiment 3: Depth First Search (DFS)
#
# INPUT FORMAT:
# Nodes: Comma-separated node names
# Edges: Comma-separated connections using "-"
# Start: Starting node
# End: Destination node
#
# INPUT EXAMPLE:
# Nodes: A,B,C,D,E,F
# Edges: A-B,A-C,B-D,B-E,C-F,E-F
# Start: A
# End: F
#
# EXPECTED OUTPUT:
# Shortest Path: A -> C -> F
# Number of Edges: 2
#
# NOTE:
# This program uses DFS with backtracking to find
# the shortest path among all explored simple paths.
# Large graphs may take longer to process.

import tkinter as tk
from tkinter import messagebox
import networkx as nx
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def dfs_shortest_path(graph, start, end, path=None):
    if path is None:
        path = []

    path = path + [start]

    if start == end:
        return path

    shortest = None

    for node in graph[start]:
        if node not in path:
            new_path = dfs_shortest_path(
                graph, node, end, path
            )

            if new_path:
                if shortest is None or len(new_path) < len(shortest):
                    shortest = new_path

    return shortest


class DFSApp:
    def __init__(self, root):
        self.root = root
        root.title("Experiment 3 - DFS")
        root.geometry("760x650")

        tk.Label(
            root,
            text="Depth First Search (DFS)",
            font=("Arial", 16, "bold")
        ).pack(pady=12)

        tk.Label(root, text="Enter Nodes:").pack()
        self.nodes_entry = tk.Entry(root, width=55)
        self.nodes_entry.pack(pady=5)

        tk.Label(root, text="Enter Edges:").pack()
        self.edges_entry = tk.Entry(root, width=55)
        self.edges_entry.pack(pady=5)

        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Start:").pack(side="left")
        self.start_entry = tk.Entry(frame, width=8)
        self.start_entry.pack(side="left", padx=5)

        tk.Label(frame, text="End:").pack(side="left")
        self.end_entry = tk.Entry(frame, width=8)
        self.end_entry.pack(side="left", padx=5)

        tk.Button(
            frame, text="Run DFS", command=self.run
        ).pack(side="left", padx=5)

        tk.Button(
            frame, text="Reset", command=self.reset
        ).pack(side="left", padx=5)

        tk.Button(
            frame, text="Exit", command=root.destroy
        ).pack(side="left", padx=5)

        self.result_label = tk.Label(
            root,
            text="Enter graph details and click Run DFS",
            font=("Arial", 11)
        )
        self.result_label.pack(pady=8)

        self.figure = Figure(figsize=(7, 4))
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(
            self.figure, master=root
        )
        self.canvas.get_tk_widget().pack(
            fill="both", expand=True
        )

    def reset(self):
        self.nodes_entry.delete(0, tk.END)
        self.edges_entry.delete(0, tk.END)
        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)

        self.ax.clear()
        self.canvas.draw()

        self.result_label.config(
            text="Enter graph details and click Run DFS"
        )

    def run(self):
        try:
            nodes = [
                x.strip()
                for x in self.nodes_entry.get().split(",")
                if x.strip()
            ]

            if len(nodes) < 2 or len(nodes) != len(set(nodes)):
                raise ValueError(
                    "Enter at least two unique nodes."
                )

            graph = {node: [] for node in nodes}

            edges = self.edges_entry.get().split(",")

            for edge in edges:
                edge = edge.strip()

                if not edge:
                    continue

                pair = [
                    x.strip() for x in edge.split("-")
                ]

                if len(pair) != 2:
                    raise ValueError(
                        "Invalid edge format: " + edge
                    )

                a, b = pair

                if a not in graph or b not in graph:
                    raise ValueError(
                        "Edge contains an unknown node."
                    )

                if b not in graph[a]:
                    graph[a].append(b)

                if a not in graph[b]:
                    graph[b].append(a)

            start = self.start_entry.get().strip()
            end = self.end_entry.get().strip()

            if start not in graph or end not in graph:
                raise ValueError(
                    "Start and End must be valid nodes."
                )

            path = dfs_shortest_path(
                graph, start, end
            )

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return

        self.ax.clear()

        G = nx.Graph()
        G.add_nodes_from(nodes)

        for a in graph:
            for b in graph[a]:
                G.add_edge(a, b)

        pos = nx.spring_layout(G, seed=42)

        nx.draw(
            G, pos, ax=self.ax,
            with_labels=True,
            node_color="lightblue",
            node_size=950,
            font_weight="bold"
        )

        if path:
            self.result_label.config(
                text="Shortest Path: "
                + " -> ".join(path)
                + f" | Edges: {len(path) - 1}"
            )

            nx.draw_networkx_edges(
                G, pos, ax=self.ax,
                edgelist=list(zip(path, path[1:])),
                edge_color="red",
                width=3
            )

            nx.draw_networkx_nodes(
                G, pos, ax=self.ax,
                nodelist=path,
                node_color="lightgreen",
                node_size=950
            )

            nx.draw_networkx_labels(
                G, pos, ax=self.ax,
                font_weight="bold"
            )

        else:
            self.result_label.config(
                text="No path found"
            )

        self.ax.set_title("DFS Graph Visualization")
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = DFSApp(root)
    root.mainloop()
