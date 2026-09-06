"""Carregamento do dataset email-Eu-core.

O dataset possui dois arquivos de texto separados por espacos:

* ``email-Eu-core.txt``: uma aresta direcionada ``origem destino`` por linha;
* ``email-Eu-core-department-labels.txt``: ``pessoa departamento`` por linha.

Os identificadores sao mantidos como inteiros, tal como publicados pelo SNAP.
"""

from __future__ import annotations

from pathlib import Path
from typing import TypeAlias


Edge: TypeAlias = tuple[int, int]
DepartmentByPerson: TypeAlias = dict[int, int]

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
EMAIL_EDGES_PATH = DATA_DIR / "email-Eu-core.txt"
DEPARTMENT_LABELS_PATH = DATA_DIR / "email-Eu-core-department-labels.txt"


def _read_integer_pairs(file_path: str | Path, description: str) -> list[tuple[int, int]]:
    """Le pares de inteiros de um arquivo, preservando a ordem das linhas."""
    path = Path(file_path)
    pairs: list[tuple[int, int]] = []

    with path.open("r", encoding="utf-8") as file:
        for line_number, raw_line in enumerate(file, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            columns = line.split()
            if len(columns) != 2:
                raise ValueError(
                    f"Linha {line_number} invalida em {path}: esperado "
                    f"'{description}', encontrado {line!r}."
                )

            try:
                first, second = (int(value) for value in columns)
            except ValueError as error:
                raise ValueError(
                    f"Linha {line_number} invalida em {path}: os dois valores "
                    "devem ser inteiros."
                ) from error

            pairs.append((first, second))

    return pairs


def load_edges(file_path: str | Path = EMAIL_EDGES_PATH) -> list[Edge]:
    """Le as relacoes de e-mail como arestas direcionadas ``(origem, destino)``."""
    return _read_integer_pairs(file_path, "origem destino")


def load_department_labels(
    file_path: str | Path = DEPARTMENT_LABELS_PATH,
) -> DepartmentByPerson:
    """Le e devolve a associacao ``pessoa -> departamento``.

    Uma pessoa deve aparecer apenas uma vez no arquivo. A validacao evita que um
    rotulo anterior seja sobrescrito silenciosamente por uma linha duplicada.
    """
    labels: DepartmentByPerson = {}

    for person, department in _read_integer_pairs(file_path, "pessoa departamento"):
        if person in labels:
            raise ValueError(
                f"A pessoa {person} aparece mais de uma vez no arquivo de departamentos."
            )
        labels[person] = department

    return labels


def load_dataset(
    edges_path: str | Path = EMAIL_EDGES_PATH,
    department_labels_path: str | Path = DEPARTMENT_LABELS_PATH,
) -> tuple[list[Edge], DepartmentByPerson]:
    """Carrega a rede e seus departamentos, validando a associacao das pessoas.

    Returns:
        Um par ``(arestas, departamentos_por_pessoa)``.

    Raises:
        FileNotFoundError: se um dos arquivos nao existir.
        ValueError: se houver uma linha invalida, uma pessoa duplicada nos rotulos
            ou uma pessoa presente na rede sem departamento associado.
    """
    edges = load_edges(edges_path)
    departments = load_department_labels(department_labels_path)

    people_in_network = {person for edge in edges for person in edge}
    people_without_department = people_in_network.difference(departments)
    if people_without_department:
        preview = ", ".join(map(str, sorted(people_without_department)[:10]))
        suffix = "..." if len(people_without_department) > 10 else ""
        raise ValueError(
            "Pessoa(s) da rede sem departamento associado: "
            f"{preview}{suffix}."
        )

    return edges, departments


def load_email_eu_core(
    data_dir: str | Path = DATA_DIR,
) -> tuple[list[Edge], DepartmentByPerson]:
    """Carrega os dois arquivos oficiais a partir de um diretorio de dados."""
    directory = Path(data_dir)
    return load_dataset(
        directory / "email-Eu-core.txt",
        directory / "email-Eu-core-department-labels.txt",
    )

