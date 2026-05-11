"""Item #15 — Trace-based code review (find untested functions)."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path

__all__ = ["UncoveredSymbol", "scan_for_uncovered"]


@dataclass
class UncoveredSymbol:
    file_path: str
    symbol: str
    line: int


def _extract_symbols(path: Path) -> list[tuple[str, int]]:
    """Return [(symbol_name, body_first_line), ...] for top-level Python defs."""
    try:
        text = path.read_text("utf-8", errors="replace")
        tree = ast.parse(text, filename=str(path))
    except (OSError, SyntaxError):
        return []
    out: list[tuple[str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            body_line = node.body[0].lineno if node.body else node.lineno
            out.append((node.name, body_line))
        elif isinstance(node, ast.ClassDef):
            body_line = node.body[0].lineno if node.body else node.lineno
            out.append((node.name, body_line))
    return out


def scan_for_uncovered(
    project_root: Path,
    coverage_data: dict[str, set[int]],
    *,
    recently_changed: list[str] | None = None,
) -> list[UncoveredSymbol]:
    """coverage_data: {filepath: set_of_lines_executed}.
    recently_changed: filter to these files."""
    targets = recently_changed or list(coverage_data.keys())
    results: list[UncoveredSymbol] = []
    for rel in targets:
        path = project_root / rel
        if not path.is_file():
            continue
        symbols = _extract_symbols(path)
        hit_lines = coverage_data.get(rel, set())
        for name, body_line in symbols:
            if body_line not in hit_lines:
                results.append(UncoveredSymbol(
                    file_path=rel, symbol=name, line=body_line,
                ))
    return results
