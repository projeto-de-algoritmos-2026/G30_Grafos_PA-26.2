import pytest

from src.analysis import analyze_components


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
        },
        {
            "component_id": 1,
            "vertices": [3, 4],
            "size": 2,
            "departments": [30],
            "department_counts": {30: 2},
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
        }
    ]


def test_returns_empty_analysis_when_there_are_no_components() -> None:
    assert analyze_components([], {}) == []


def test_rejects_vertex_without_department() -> None:
    with pytest.raises(ValueError, match="Vertice 2 sem departamento associado"):
        analyze_components([[0, 1, 2]], {0: 10, 1: 10})
