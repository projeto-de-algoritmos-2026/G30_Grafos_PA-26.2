import pytest

from src.analysis import (
    analyze_components,
    analyze_department,
    build_condensation_graph,
)


def test_integrates_departments_into_components() -> None:
    components = [[0, 1, 2], [3, 4]]
    department_by_person = {
        0: 10,
        1: 10,
        2: 20,
        3: 30,
        4: 30,
    }

    assert analyze_components(components, department_by_person) == [
        {
            "component_id": 0,
            "vertices": [0, 1, 2],
            "size": 3,
            "departments": [10, 20],
            "department_counts": {10: 2, 20: 1},
            "predominant_department": 10,
            "department_count": 2,
            "purity": 2 / 3,
            "predominant_department_percentage": (2 / 3) * 100,
        },
        {
            "component_id": 1,
            "vertices": [3, 4],
            "size": 2,
            "departments": [30],
            "department_counts": {30: 2},
            "predominant_department": 30,
            "department_count": 1,
            "purity": 1.0,
            "predominant_department_percentage": 100.0,
        },
    ]


def test_handles_isolated_vertex_component() -> None:
    assert analyze_components([[7]], {7: 4}) == [
        {
            "component_id": 0,
            "vertices": [7],
            "size": 1,
            "departments": [4],
            "department_counts": {4: 1},
            "predominant_department": 4,
            "department_count": 1,
            "purity": 1.0,
            "predominant_department_percentage": 100.0,
        }
    ]


def test_returns_empty_analysis_when_there_are_no_components() -> None:
    assert analyze_components([], {}) == []


def test_rejects_vertex_without_department() -> None:
    with pytest.raises(ValueError, match="Vertice 2 sem departamento associado"):
        analyze_components([[0, 1, 2]], {0: 10, 1: 10})


def test_uses_smallest_department_as_tie_breaker() -> None:
    analysis = analyze_components(
        [[0, 1, 2, 3]],
        {0: 20, 1: 10, 2: 20, 3: 10},
    )

    assert analysis[0]["predominant_department"] == 10
    assert analysis[0]["department_count"] == 2
    assert analysis[0]["purity"] == 0.5
    assert analysis[0]["predominant_department_percentage"] == 50.0


def test_rejects_empty_component() -> None:
    with pytest.raises(ValueError, match="nao pode ser vazio"):
        analyze_components([[]], {})


def test_analyzes_department_distribution_between_components() -> None:
    components = analyze_components(
        [[0, 1, 2], [3, 4], [5]],
        {0: 10, 1: 10, 2: 20, 3: 10, 4: 20, 5: 30},
    )

    assert analyze_department(10, components) == {
        "department_id": 10,
        "person_count": 3,
        "component_ids": [0, 1],
        "main_component_id": 0,
        "main_component_person_count": 2,
        "main_component_percentage": (2 / 3) * 100,
    }


def test_department_analysis_uses_component_id_as_tie_breaker() -> None:
    components = analyze_components(
        [[0, 1, 2], [3, 4]],
        {0: 10, 1: 10, 2: 20, 3: 20, 4: 30},
    )

    assert analyze_department(20, components) == {
        "department_id": 20,
        "person_count": 2,
        "component_ids": [0, 1],
        "main_component_id": 0,
        "main_component_person_count": 1,
        "main_component_percentage": 50.0,
    }


def test_returns_empty_summary_for_unknown_department() -> None:
    components = analyze_components([[0, 1]], {0: 10, 1: 10})

    assert analyze_department(99, components) == {
        "department_id": 99,
        "person_count": 0,
        "component_ids": [],
        "main_component_id": None,
        "main_component_person_count": 0,
        "main_component_percentage": 0.0,
    }


def test_builds_condensation_graph_with_relations_between_components() -> None:
    components = [[0, 1], [2, 3], [4], [5]]
    edges = [
        (0, 1),
        (1, 0),
        (2, 3),
        (3, 2),
        (1, 2),
        (0, 3),
        (3, 4),
        (4, 4),
    ]

    condensation = build_condensation_graph(components, edges)

    assert condensation.get_vertices() == [0, 1, 2, 3]
    assert condensation.get_neighbors(0) == [1]
    assert condensation.get_neighbors(1) == [2]
    assert condensation.get_neighbors(2) == []
    assert condensation.get_neighbors(3) == []
    assert condensation.vertex_count() == 4
    assert condensation.edge_count() == 2


def test_condensation_rejects_vertex_in_multiple_components() -> None:
    with pytest.raises(ValueError, match="Vertice 1 pertence aos componentes 0 e 1"):
        build_condensation_graph([[0, 1], [1, 2]], [])


def test_condensation_rejects_edge_vertex_outside_components() -> None:
    with pytest.raises(ValueError, match="Vertice 2.*nao pertence a nenhum CFC"):
        build_condensation_graph([[0], [1]], [(0, 2)])
