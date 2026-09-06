class KosarajuGraph:
    def __init__(self, vertices_list):
        self.vertices = vertices_list
        self.graph = {v: [] for v in vertices_list}

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def dfs(self, v, visited, stack=None, component=None):
        """
        Busca em profundidade (DFS)
        - Se 'stack' for fornecida, a função adiciona o vértice à pilha ao finalizar (1ª passada).
        - Se 'component' for fornecido, agrupa os vértices alcançados no componente atual (2ª passada).
        """
        visited.add(v)
        if component is not None:
            component.append(v)
            
        for neighbor in self.graph.get(v, []):
            if neighbor not in visited:
                self.dfs(neighbor, visited, stack, component)
                
        if stack is not None:
            stack.append(v)
