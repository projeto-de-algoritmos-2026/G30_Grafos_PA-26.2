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
