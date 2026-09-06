import pytest

from src.graph import DirectedGraph, Graph


def test_add_vertex() -> None:
    graph = Graph()

    assert graph.add_vertex(10) is True
    assert graph.add_vertex(10) is False
    assert graph.vertex_count() == 1
    assert graph.get_neighbors(10) == []


def test_add_directed_edge_and_access_neighbors() -> None:
    graph = Graph()

    assert graph.add_edge(1, 2) is True

    assert graph.get_neighbors(1) == [2]
    assert graph.get_neighbors(2) == []
    assert graph.vertex_count() == 2
    assert graph.edge_count() == 1


def test_add_edge_creates_its_vertices() -> None:
    graph = Graph()

    graph.add_edge(3, 4)

    assert graph.get_vertices() == [3, 4]


def test_duplicate_edge_is_not_counted_twice() -> None:
    graph = Graph()

    graph.add_edge(1, 2)
    assert graph.add_edge(1, 2) is False

    assert graph.get_neighbors(1) == [2]
    assert graph.edge_count() == 1


def test_neighbors_are_returned_as_a_copy() -> None:
    graph = Graph([(1, 2)])

    graph.get_neighbors(1).append(3)

    assert graph.get_neighbors(1) == [2]
    assert graph.edge_count() == 1


def test_unknown_vertex_has_no_adjacency_list() -> None:
    graph = Graph()

    with pytest.raises(KeyError, match="Vertice inexistente: 99"):
        graph.get_neighbors(99)


def test_counts_are_also_available_as_properties() -> None:
    graph = DirectedGraph([(0, 1), (1, 0)])

    assert graph.num_vertices == 2
    assert graph.num_edges == 2
    assert len(graph) == 2
    assert 0 in graph
