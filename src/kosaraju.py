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

    def get_transpose(self):
        """
        Retorna o grafo transposto (reverso),
        onde todas as arestas u -> v são convertidas em v -> u.
        """
        g_transposed = KosarajuGraph(self.vertices)
        for u in self.vertices:
            for v in self.graph.get(u, []):
                g_transposed.add_edge(v, u)
        return g_transposed

    def get_sccs(self):
        """
        Executa o algoritmo de Kosaraju para encontrar
        os Componentes Fortemente Conectados (CFCs).
        """
        stack = []
        visited = set()
        
        # 1. Primeira DFS para preencher a pilha com a ordem de término
        for i in self.vertices:
            if i not in visited:
                self.dfs(i, visited, stack=stack)
                
        # 2 e 3. Obter o grafo transposto (reverso)
        g_transposed = self.get_transpose()
        
        # Preparação para a segunda DFS
        visited.clear()
        sccs = []
        
        # 4. Segunda DFS no grafo transposto processando na ordem de término (desempilhando)
        while stack:
            v = stack.pop()
            if v not in visited:
                component = []
                g_transposed.dfs(v, visited, component=component)
                # 5. Identificação e armazenamento do CFC
                sccs.append(component)
                
        return sccs
