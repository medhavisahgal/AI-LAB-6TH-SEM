import networkx as nx
import matplotlib.pyplot as plt

def bidirectional_dfs(graph, start, end):
    if start == end:
        return [start]
    
    stack_start = [(start, [start])]
    stack_end = [(end, [end])]
    visited_start = {start}
    visited_end = {end}
    
    while stack_start and stack_end:
        if stack_start:
            node, path = stack_start.pop()
            for neighbor in graph.neighbors(node):
                if neighbor not in visited_start:
                    new_path = path + [neighbor]
                    if neighbor in visited_end:
                        return new_path[:-1] + list(reversed([p for p, _ in stack_end if p == neighbor][0]))
                    visited_start.add(neighbor)
                    stack_start.append((neighbor, new_path))
        
        if stack_end:
            node, path = stack_end.pop()
            for neighbor in graph.neighbors(node):
                if neighbor not in visited_end:
                    new_path = path + [neighbor]
                    if neighbor in visited_start:
                        return list(reversed([p for p, _ in stack_start if p == neighbor][0])) + new_path[1:]
                    visited_end.add(neighbor)
                    stack_end.append((neighbor, new_path))
    
    return None

def visualize_graph(graph, path, title="Graph"):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(8, 6))
    nx.draw(graph, pos, with_labels=True, node_color="lightblue", edge_color="gray")
    if path:
        edges_in_path = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(graph, pos, edgelist=edges_in_path, edge_color="red", width=2)
    plt.title(title)
    plt.show()

# Create the graph
city_graph = nx.Graph()
city_graph.add_edges_from([
    ("A", "B"), ("A", "C"), ("B", "D"), ("C", "E"), 
    ("D", "E"), ("D", "F"), ("E", "F"), ("F", "G")
])

# Start and end nodes
start_node = "A"
end_node = "G"

# Run Bi-Directional DFS
bidirectional_dfs_path = bidirectional_dfs(city_graph, start_node, end_node)
print("Bi-Directional DFS Path:", bidirectional_dfs_path)

# Visualize Bi-Directional DFS result
visualize_graph(city_graph, bidirectional_dfs_path, title="Bi-Directional DFS Path")
