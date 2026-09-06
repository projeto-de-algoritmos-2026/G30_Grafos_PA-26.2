"""Estrutura de grafo direcionado baseada em lista de adjacencia."""

from __future__ import annotations

from collections.abc import Iterable


class Graph:
    """Grafo direcionado simples com vertices identificados por inteiros.

    A lista de adjacencia guarda, para cada vertice, apenas os vertices alcancados
    por arestas de saida. Arestas paralelas nao sao inseridas mais de uma vez.
    """

    def __init__(self, edges: Iterable[tuple[int, int]] | None = None) -> None:
        self._adjacency: dict[int, list[int]] = {}
        self._edges: set[tuple[int, int]] = set()

        if edges is not None:
            for source, destination in edges:
                self.add_edge(source, destination)

    def add_vertex(self, vertex: int) -> bool:
        """Adiciona um vertice e informa se ele ainda nao existia."""
        if vertex in self._adjacency:
            return False

        self._adjacency[vertex] = []
        return True

    def add_edge(self, source: int, destination: int) -> bool:
        """Adiciona a aresta direcionada ``source -> destination``.

        Os dois vertices sao criados automaticamente quando necessario. O
        retorno e ``False`` caso a mesma aresta ja esteja presente.
        """
        self.add_vertex(source)
        self.add_vertex(destination)

        edge = (source, destination)
        if edge in self._edges:
            return False

        self._adjacency[source].append(destination)
        self._edges.add(edge)
        return True

    def get_neighbors(self, vertex: int) -> list[int]:
        """Devolve uma copia da lista de vizinhos de saida de ``vertex``."""
        if vertex not in self._adjacency:
            raise KeyError(f"Vertice inexistente: {vertex}")

        return self._adjacency[vertex].copy()

    def get_vertices(self) -> list[int]:
        """Devolve os vertices na ordem em que foram adicionados."""
        return list(self._adjacency)

    def vertex_count(self) -> int:
        """Devolve a quantidade de vertices do grafo."""
        return len(self._adjacency)

    def edge_count(self) -> int:
        """Devolve a quantidade de arestas direcionadas do grafo."""
        return len(self._edges)

    @property
    def num_vertices(self) -> int:
        """Quantidade de vertices, disponibilizada tambem como propriedade."""
        return self.vertex_count()

    @property
    def num_edges(self) -> int:
        """Quantidade de arestas, disponibilizada tambem como propriedade."""
        return self.edge_count()

    def __contains__(self, vertex: object) -> bool:
        return vertex in self._adjacency

    def __len__(self) -> int:
        return self.vertex_count()


DirectedGraph = Graph

