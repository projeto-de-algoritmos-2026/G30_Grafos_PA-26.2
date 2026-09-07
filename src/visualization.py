import networkx as nx
import matplotlib.pyplot as plt

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
