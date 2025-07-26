from pyvis.network import Network
import networkx as nx

def build_graph(items, edges):
    G = nx.DiGraph()  # Directed graph

    # Add nodes (functions/classes)
    for item_type, name in items:
        G.add_node(name, label=name, title=item_type)

    # Add edges (relationships from call graph)
    for source, target in edges:
        G.add_edge(source, target)

    # Create PyVis network
    net = Network(height="600px", width="100%", directed=True)
    net.from_nx(G)
    net.save_graph("templates/code_graph.html")
    return net
