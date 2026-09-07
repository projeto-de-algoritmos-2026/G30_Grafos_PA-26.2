"""Analise da composicao departamental dos componentes da rede."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
from typing import TypedDict


class ComponentInfo(TypedDict):
    """Informacoes basicas de um componente fortemente conectado."""

    component_id: int
    vertices: list[int]
    size: int
    departments: list[int]
    department_counts: dict[int, int]
    predominant_department: int
    department_count: int
    purity: float
    predominant_department_percentage: float


class DepartmentInfo(TypedDict):
    """Resumo da distribuicao de um departamento entre os componentes."""

    department_id: int
    person_count: int
    component_ids: list[int]
    main_component_id: int | None
    main_component_person_count: int
    main_component_percentage: float


def analyze_components(
    components: Sequence[Sequence[int]],
    department_by_person: Mapping[int, int],
) -> list[ComponentInfo]:
    """Associa os departamentos aos componentes encontrados pelo Kosaraju.

    Os identificadores dos componentes seguem a ordem recebida e comecam em
    zero. A lista de departamentos e ordenada para oferecer uma saida estavel,
    enquanto a ordem dos vertices de cada componente e preservada.

    Args:
        components: Componentes representados por sequencias de vertices.
        department_by_person: Associacao ``pessoa -> departamento``.

    Returns:
        Uma lista com o ID, vertices, tamanho e composicao departamental de cada
        componente.

    Raises:
        ValueError: se algum vertice nao possuir departamento associado.
    """
    analyses: list[ComponentInfo] = []

    for component_id, component in enumerate(components):
        vertices = list(component)

        try:
            department_counts = Counter(
                department_by_person[vertex] for vertex in vertices
            )
        except KeyError as error:
            missing_vertex = error.args[0]
            raise ValueError(
                f"Vertice {missing_vertex} sem departamento associado."
            ) from error

        if not vertices:
            raise ValueError("Um componente fortemente conectado nao pode ser vazio.")

        predominant_count = max(department_counts.values())
        # Em caso de empate, o menor identificador torna o resultado deterministico.
        predominant_department = min(
            department
            for department, count in department_counts.items()
            if count == predominant_count
        )
        purity = predominant_count / len(vertices)

        analyses.append(
            {
                "component_id": component_id,
                "vertices": vertices,
                "size": len(vertices),
                "departments": sorted(department_counts),
                "department_counts": dict(department_counts),
                "predominant_department": predominant_department,
                "department_count": len(department_counts),
                "purity": purity,
                "predominant_department_percentage": purity * 100,
            }
        )

    return analyses


def analyze_department(
    department_id: int,
    components: Sequence[ComponentInfo],
) -> DepartmentInfo:
    """Analisa como um departamento esta distribuido entre os CFCs.

    O componente principal e aquele que possui a maior quantidade absoluta de
    pessoas do departamento. A porcentagem indica qual parcela de todas as
    pessoas do departamento esta nesse componente. Em caso de empate, e usado o
    componente com o menor ID.

    Departamentos ausentes produzem um resumo vazio, permitindo que a funcao
    tambem seja usada com filtros ou selecoes externas ao dataset carregado.
    """
    appearances: list[tuple[int, int]] = []

    for component in components:
        person_count = component["department_counts"].get(department_id, 0)
        if person_count > 0:
            appearances.append((component["component_id"], person_count))

    total_people = sum(person_count for _, person_count in appearances)
    if not appearances:
        return {
            "department_id": department_id,
            "person_count": 0,
            "component_ids": [],
            "main_component_id": None,
            "main_component_person_count": 0,
            "main_component_percentage": 0.0,
        }

    main_component_id, main_component_person_count = min(
        appearances,
        key=lambda appearance: (-appearance[1], appearance[0]),
    )

    return {
        "department_id": department_id,
        "person_count": total_people,
        "component_ids": [component_id for component_id, _ in appearances],
        "main_component_id": main_component_id,
        "main_component_person_count": main_component_person_count,
        "main_component_percentage": (
            main_component_person_count / total_people * 100
        ),
    }
