from pathlib import Path

import pytest

from src.dataset_loader import (
    load_dataset,
    load_department_labels,
    load_edges,
    load_email_eu_core,
)


def _write(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path


def test_load_edges_reads_directed_relations(tmp_path: Path) -> None:
    edges_file = _write(tmp_path / "edges.txt", "0 1\n1 2\n2 0\n")

    assert load_edges(edges_file) == [(0, 1), (1, 2), (2, 0)]


def test_load_department_labels_associates_people(tmp_path: Path) -> None:
    labels_file = _write(tmp_path / "labels.txt", "0 4\n1 4\n2 9\n")

    assert load_department_labels(labels_file) == {0: 4, 1: 4, 2: 9}


def test_load_email_eu_core_uses_official_file_names(tmp_path: Path) -> None:
    _write(tmp_path / "email-Eu-core.txt", "0 1\n")
    _write(tmp_path / "email-Eu-core-department-labels.txt", "0 2\n1 3\n")

    assert load_email_eu_core(tmp_path) == ([(0, 1)], {0: 2, 1: 3})


def test_loader_ignores_blank_lines_and_comments(tmp_path: Path) -> None:
    edges_file = _write(tmp_path / "edges.txt", "# origem destino\n\n0  1\n")

    assert load_edges(edges_file) == [(0, 1)]


def test_load_dataset_rejects_person_without_department(tmp_path: Path) -> None:
    edges_file = _write(tmp_path / "edges.txt", "0 1\n")
    labels_file = _write(tmp_path / "labels.txt", "0 2\n")

    with pytest.raises(ValueError, match="sem departamento associado: 1"):
        load_dataset(edges_file, labels_file)


def test_invalid_line_reports_its_number(tmp_path: Path) -> None:
    edges_file = _write(tmp_path / "edges.txt", "0 1\nlinha invalida\n")

    with pytest.raises(ValueError, match="Linha 2 invalida"):
        load_edges(edges_file)


def test_duplicate_person_label_is_rejected(tmp_path: Path) -> None:
    labels_file = _write(tmp_path / "labels.txt", "0 2\n0 3\n")

    with pytest.raises(ValueError, match="pessoa 0 aparece mais de uma vez"):
        load_department_labels(labels_file)
