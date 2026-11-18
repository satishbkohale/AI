# Experiment 3 - DFS (all simple paths explored, shortest kept)
# INPUT: graph below, start_node = 'A', end_node = 'F'
# Expected: path ['A', 'C', 'F'], length 3
import networkx as nx
import matplotlib.pyplot as plt

def dfs_shortest_path(graph, start, end, path=None):
    if path is None:
        path = []
    path = path + [start]
    print(f"Exploring node: {start}, Current path: {path}")
    if start == end:
        print(f"Reached the end node: {end}, Path: {path}")
        return path
    shortest = None
    for node in graph[start]:
        if node not in path:
            print(f"Going to node: {node} from node: {start}")
            newpath = dfs_shortest_path(graph, node, end, path)
            if newpath:
                if shortest is None or len(newpath) < len(shortest):
                    shortest = newpath
    if shortest:
        print(f"Backtracking to node: {start}, Shortest path found: {shortest}")
        print(f"Length of the path: {len(shortest)}")
    else:
        print(f"Backtracking to node: {start}, No path found.")
    return shortest

def draw_graph(graph, shortest_path=None):
    G = nx.Graph()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 7))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray',
            node_size=2000, font_size=15, font_weight='bold')
    if shortest_path:
        path_edges = list(zip(shortest_path, shortest_path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red',
                               width=2, style='dashed')
        nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_color='lightgreen')
    plt.title("Graph Visualization with Shortest Path Highlighted")
    plt.show()

if __name__ == "__main__":
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E'],
    }
    print("The graph is:")
    for node, neighbors in graph.items():
        print(f"{node}: {', '.join(neighbors)}")

    start_node = 'A'
    end_node = 'F'
    print(f"\nFinding shortest path from {start_node} to {end_node}...\n")
    shortest_path = dfs_shortest_path(graph, start_node, end_node)
    if shortest_path:
        print(f"Shortest path from {start_node} to {end_node}: {shortest_path}")
        print(f"Length of the shortest path: {len(shortest_path)}")
    else:
        print(f"No path found from {start_node} to {end_node}.")
    draw_graph(graph, shortest_path)
