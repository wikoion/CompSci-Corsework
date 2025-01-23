import matplotlib.pyplot as plt
import networkx as nx

edges = [
    ('A', 'B', 1), ('A', 'G', 10), ('A', 'C', 5),
    ('B', 'D', 3), ('D', 'F', 1), ('D', 'C', 8),
    ('C', 'E', 6), ('C', 'Z', 9), ('E', 'Z', 1),
    ('G', 'E', 3), ('F', 'Z', 6)
]

def draw_graph(edges, title):
    G = nx.Graph()
    G.add_weighted_edges_from(edges)

    pos = {
        'A': (0, 1), 'B': (1, 2), 'C': (1, 0), 'D': (2, 2),
        'E': (2, 0), 'F': (3, 2), 'G': (0, -1), 'Z': (3, 0)
    }

    plt.figure(figsize=(10, 7))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1000, font_size=15, edge_color='purple')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d for u, v, d in edges}, font_size=12, font_color='black')
    plt.title(title)
    plt.show()

def kruskal_with_visualization(edges):
    edges = sorted(edges, key=lambda x: x[2])
    parent = {}

    def find(node):
        while parent[node] != node:
            node = parent[node]
        return node

    def union(node1, node2):
        root1 = find(node1)
        root2 = find(node2)
        if root1 != root2:
            parent[root2] = root1

    for u, v, _ in edges:
        parent[u] = u
        parent[v] = v

    mst = []

    print("Step-by-step MST creation:")
    draw_graph(edges, "Original Graph")

    for i, (u, v, weight) in enumerate(edges):
        if find(u) != find(v):
            union(u, v)
            mst.append((u, v, weight))
            print(f"Step {i + 1}: Added edge ({u}, {v}) with weight {weight}")
            draw_graph(mst, f"MST after Step {i + 1}") 

    return mst

mst = kruskal_with_visualization(edges)

print("\nFinal Minimum Spanning Tree (MST):")
for edge in mst:
    print(edge)

draw_graph(mst, "Final Minimum Spanning Tree (MST)")
