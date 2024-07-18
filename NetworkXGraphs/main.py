import networkx as nx
import matplotlib.pyplot as plt

# Same g6 strings as Nauty
g6_strings = {
    "G?|v]{": 1,
    "G?Vdz{": 2,
    "GCNR~[": 1,
    "GCLm~{": 0
}

# dictionary to store NetworkX graphs
graphs = {}

# Convert g6 strings to NetworkX graphs and print canonical adjacency lists
for key, level in g6_strings.items():
    graph = nx.from_graph6_bytes(key.encode())
    canonical_graph = nx.convert_node_labels_to_integers(graph, label_attribute='original')
    graphs[key] = (canonical_graph, level)
    print(f"Graph: {key} (Level {level}) - Adjacency List (Canonical Form)")
    for line in nx.generate_adjlist(canonical_graph):
        print(line)
    print("\n")

plt.figure(figsize=(10, 10))

# Fix a layout for consistent node positioning and prevent overlapping lines
fixed_pos = {0: (0.3, 0.4), 1: (1, 0.1), 2: (1.7, 0.4),
             3: (0, 1.3), 4: (0.8, 1), 5: (2, 1.3),
             6: (0.3, 2), 7: (1, 2.3), 8: (1.7, 2)}

for i, (key, (graph, level)) in enumerate(graphs.items()):
    plt.subplot(2, 2, i + 1)
    nx.draw(graph, pos=fixed_pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
    plt.title(f"Graph: {key} (Level {level})")

plt.tight_layout()
plt.show()
