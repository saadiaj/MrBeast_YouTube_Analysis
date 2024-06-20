import matplotlib.pyplot as plt
import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Define the nodes for domains, data products, data sources, and consumers
domains = ["Patient Management", "Clinical Operations", "Billing", "Medical Research"]
data_products = ["Patient Records", "Clinical Reports", "Billing Information", "Research Data"]
data_sources = ["EHR System", "Lab System", "Billing System", "Research Database"]
consumers = ["Doctors", "Researchers", "Billing Departments"]

# Add nodes to the graph
G.add_nodes_from(domains, category="Domain")
G.add_nodes_from(data_products, category="Data Product")
G.add_nodes_from(data_sources, category="Data Source")
G.add_nodes_from(consumers, category="Consumer")

# Define edges (relationships)
edges = [
    # Domain to Data Product
    ("Patient Management", "Patient Records"),
    ("Clinical Operations", "Clinical Reports"),
    ("Billing", "Billing Information"),
    ("Medical Research", "Research Data"),

    # Data Product to Data Source
    ("Patient Records", "EHR System"),
    ("Clinical Reports", "Lab System"),
    ("Billing Information", "Billing System"),
    ("Research Data", "Research Database"),

    # Data Product to Consumer
    ("Patient Records", "Doctors"),
    ("Clinical Reports", "Doctors"),
    ("Research Data", "Researchers"),
    ("Billing Information", "Billing Departments")
]

# Add edges to the graph
G.add_edges_from(edges)

# Define colors for each node type
color_map = []
for node in G:
    if G.nodes[node]['category'] == 'Domain':
        color_map.append('lightblue')
    elif G.nodes[node]['category'] == 'Data Product':
        color_map.append('lightgreen')
    elif G.nodes[node]['category'] == 'Data Source':
        color_map.append('lightcoral')
    elif G.nodes[node]['category'] == 'Consumer':
        color_map.append('lightgoldenrodyellow')

# Define layout for the graph
pos = nx.spring_layout(G, seed=42)

# Draw the graph
plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=True, node_color=color_map, node_size=3000, font_size=10, font_weight='bold', edge_color='gray')
plt.title('Data Mesh for Hospital Systems')
plt.show()
