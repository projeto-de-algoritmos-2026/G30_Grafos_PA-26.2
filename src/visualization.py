import networkx as nx
import matplotlib.pyplot as plt

from src.graph import Graph

def draw_component(component_nodes, edges, departments, highlight_node=None):
    """
    Desenha um Componente Fortemente Conectado (CFC).
    
    Args:
        component_nodes (list): Lista de vértices do componente.
        edges (list): Lista de arestas do grafo inteiro (serão filtradas).
        departments (dict): Dicionário mapeando vértice -> departamento.
        highlight_node: Opcional, nó a ser destacado.
        
    Returns:
        fig: A figura matplotlib gerada.
    """
    G = nx.DiGraph()
    
    # Adicionar os nós e arestas correspondentes ao componente
    nodes_set = set(component_nodes)
    G.add_nodes_from(component_nodes)
    
    component_edges = [(u, v) for (u, v) in edges if u in nodes_set and v in nodes_set]
    G.add_edges_from(component_edges)
    
    # Definir cores baseadas nos departamentos
    # Uma paleta de cores simples
    cmap = plt.get_cmap('tab20')
    node_colors = []
    
    for node in G.nodes():
        dept = departments.get(node, 0)
        # Usa o ID do departamento para selecionar a cor
        node_colors.append(cmap(dept % 20))
        
    # Desenhar
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Posicionamento (layout com mola funciona bem para componentes pequenos/médios)
    pos = nx.spring_layout(G, seed=42)
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=300, ax=ax)
    nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=15, ax=ax, edge_color='gray', alpha=0.7)
    
    # Desenhar os rótulos apenas se o componente não for gigante, ou se quisermos
    if len(G.nodes()) <= 50:
        nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)
        
    ax.set_title(f"Visualização do CFC ({len(component_nodes)} nós)")
    ax.axis('off')
    
    return fig


def draw_condensation_graph(
    condensation: Graph,
    component_sizes: dict[int, int],
):
    """Desenha o grafo no qual cada vertice representa um CFC."""
    graph = nx.DiGraph()
    component_ids = condensation.get_vertices()
    graph.add_nodes_from(component_ids)
    graph.add_edges_from(
        (source, destination)
        for source in component_ids
        for destination in condensation.get_neighbors(source)
    )

    fig, ax = plt.subplots(figsize=(12, 8))
    positions = nx.spring_layout(graph, seed=42)
    sizes = [component_sizes[component_id] for component_id in component_ids]
    node_sizes = [min(2_500, 250 + size * 3) for size in sizes]

    nx.draw_networkx_nodes(
        graph,
        positions,
        node_color=sizes,
        node_size=node_sizes,
        cmap="viridis",
        ax=ax,
    )
    nx.draw_networkx_edges(
        graph,
        positions,
        arrowstyle="-|>",
        arrowsize=12,
        edge_color="gray",
        alpha=0.6,
        ax=ax,
    )

    labeled_components = (
        component_ids
        if len(component_ids) <= 50
        else sorted(
            component_ids,
            key=lambda component_id: component_sizes[component_id],
            reverse=True,
        )[:15]
    )
    if labeled_components:
        labels = {
            component_id: f"CFC {component_id}\n({component_sizes[component_id]})"
            for component_id in labeled_components
        }
        nx.draw_networkx_labels(graph, positions, labels=labels, font_size=8, ax=ax)

    ax.set_title(
        "Grafo de condensação "
        f"({condensation.vertex_count()} CFCs, "
        f"{condensation.edge_count()} relações)"
    )
    ax.axis("off")
    return fig
