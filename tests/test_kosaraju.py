from src.kosaraju import KosarajuGraph


def _as_sets(components: list[list[int]]) -> set[frozenset[int]]:
    """Normaliza os CFCs para que a ordem da DFS nao afete as comparacoes."""
    return {frozenset(component) for component in components}


def test_finds_two_known_strongly_connected_components() -> None:
    """Valida os ciclos 0 -> 1 -> 2 -> 0 e 3 <-> 4."""
    graph = KosarajuGraph([0, 1, 2, 3, 4])
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 0)
    graph.add_edge(3, 4)
    graph.add_edge(4, 3)

    assert _as_sets(graph.get_sccs()) == {
        frozenset({0, 1, 2}),
        frozenset({3, 4}),
    }


def test_keeps_isolated_vertex_as_its_own_component() -> None:
    graph = KosarajuGraph([0, 1, 2, 3])
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 0)

    assert _as_sets(graph.get_sccs()) == {
        frozenset({0, 1, 2}),
        frozenset({3}),
    }


def test_finds_a_graph_formed_by_one_component() -> None:
    graph = KosarajuGraph([0, 1, 2, 3])
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 0)

    assert _as_sets(graph.get_sccs()) == {frozenset({0, 1, 2, 3})}


def test_finds_components_with_different_sizes() -> None:
    graph = KosarajuGraph([0, 1, 2, 3, 4, 5])
    graph.add_edge(0, 1)
    graph.add_edge(1, 0)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(4, 2)
    graph.add_edge(4, 5)

    assert _as_sets(graph.get_sccs()) == {
        frozenset({0, 1}),
        frozenset({2, 3, 4}),
        frozenset({5}),
    }
