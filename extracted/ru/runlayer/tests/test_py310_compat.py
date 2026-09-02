"""Regression tests: CLI source must stay importable on Python 3.10.

`datetime.UTC` is Python 3.11+ (PEP 615). The CLI's `pyproject.toml` declares
`requires-python = ">=3.10"`, so any `from datetime import UTC` or
`datetime.UTC` reference crashes at import on 3.10 with
`ImportError: cannot import name 'UTC' from 'datetime'`.

CI only runs Python 3.13, so this class of bug slips through. This test
scans every `.py` under `runlayer_cli/` with `ast` so it catches the
regression on any Python version. Use `timezone.utc` instead.
"""

from __future__ import annotations

import ast
from pathlib import Path

CLI_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = CLI_ROOT / "runlayer_cli"
PYTHON_311_TYPING_EXPORTS = {"NotRequired", "Required"}


def _iter_source_files() -> list[Path]:
    return sorted(PACKAGE_ROOT.rglob("*.py"))


def _find_utc_usages(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(), filename=str(path))
    findings: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "datetime":
            for alias in node.names:
                if alias.name == "UTC":
                    findings.append(
                        f"{path}:{node.lineno} `from datetime import UTC` "
                        f"(Python 3.11+; use `timezone.utc`)"
                    )
        elif (
            isinstance(node, ast.Attribute)
            and node.attr == "UTC"
            and isinstance(node.value, ast.Name)
            and node.value.id == "datetime"
        ):
            findings.append(
                f"{path}:{node.lineno} `datetime.UTC` "
                f"(Python 3.11+; use `datetime.timezone.utc`)"
            )
    return findings


def _find_python_311_typing_imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(), filename=str(path))
    findings: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module == "typing":
            for alias in node.names:
                if alias.name in PYTHON_311_TYPING_EXPORTS:
                    findings.append(
                        f"{path}:{node.lineno} `typing.{alias.name}` is Python "
                        "3.11+; import it from `typing_extensions` on Python 3.10"
                    )
    return findings


def test_no_datetime_utc_usage():
    offenders: list[str] = []
    for path in _iter_source_files():
        offenders.extend(_find_utc_usages(path))
    assert not offenders, (
        "CLI must support Python 3.10 (`pyproject.toml` requires-python "
        ">=3.10), but `datetime.UTC` is Python 3.11+. Replace with "
        "`timezone.utc`:\n  " + "\n  ".join(offenders)
    )


def test_no_python_311_typing_imports():
    offenders: list[str] = []
    for path in _iter_source_files():
        offenders.extend(_find_python_311_typing_imports(path))
    assert not offenders, (
        "CLI must support Python 3.10 (`pyproject.toml` requires-python "
        ">=3.10), but these `typing` exports require Python 3.11:\n  "
        + "\n  ".join(offenders)
    )
