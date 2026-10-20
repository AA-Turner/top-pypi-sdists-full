"""The shared keyword market row keeps the vendor payload and source exactly as returned.

Owner ruling R-F3: white-label is a display rule, never a storage rewrite. The 2026-10-17 G4 N8
change wrote ``raw = None`` and ``source_provider = "matrx"`` on every refresh, which also undid
the data restore (migration 20261019830000) row by row. This guard reads the writer's source:
any dict that writes both ``raw`` and ``source_provider`` must take them from the run, never
from a literal or a module constant. It fails on the G4 N8 code.
"""

from __future__ import annotations

import ast
from pathlib import Path

WRITERS = [
    Path(__file__).resolve().parents[1] / "matrx_seo" / "orm_repository.py",
    Path(__file__).resolve().parents[1] / "matrx_seo" / "repository.py",
]


def _row_dicts(tree: ast.AST) -> list[ast.Dict]:
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            keys = {
                k.value
                for k in node.keys
                if isinstance(k, ast.Constant) and isinstance(k.value, str)
            }
            if {"raw", "source_provider"} <= keys:
                found.append(node)
    return found


def _value(node: ast.Dict, key: str) -> ast.AST:
    for k, v in zip(node.keys, node.values):
        if isinstance(k, ast.Constant) and k.value == key:
            return v
    raise KeyError(key)


def _is_fixed(value: ast.AST) -> bool:
    """A literal (None, "matrx") or a CAPS module constant is a rewrite, not the run's value."""
    if isinstance(value, ast.Constant):
        return True
    return isinstance(value, ast.Name) and value.id.isupper()


def test_keyword_market_writers_store_raw_and_source_as_returned() -> None:
    checked = 0
    for path in WRITERS:
        tree = ast.parse(path.read_text())
        for row in _row_dicts(tree):
            for key in ("raw", "source_provider"):
                value = _value(row, key)
                assert not _is_fixed(value), (
                    f"{path.name}:{value.lineno} writes {key} = {ast.unparse(value)}: the stored "
                    "row must keep what the vendor returned (R-F3); scrub where a screen draws it"
                )
            checked += 1
    assert checked >= 2, "expected the ORM and in-memory keyword market writers"


def test_guard_catches_the_g4_n8_shape() -> None:
    old = ast.parse('row = {"raw": None, "source_provider": MEMBER_VISIBLE_SOURCE}')
    (row,) = _row_dicts(old)
    assert _is_fixed(_value(row, "raw")) and _is_fixed(_value(row, "source_provider"))


def _difficulty_source_stored(value: ast.AST) -> ast.AST:
    """The stored expression when a winner exists (body of ``X if winner else None``)."""
    return value.body if isinstance(value, ast.IfExp) else value


def test_keyword_market_writers_store_the_full_difficulty_source() -> None:
    """The G4 N8 writer cut it to its last word with ``str(operation).rsplit(".", 1)[-1]``."""
    checked = 0
    for path in WRITERS:
        for row in _row_dicts(ast.parse(path.read_text())):
            try:
                stored = _difficulty_source_stored(_value(row, "difficulty_source"))
            except KeyError:
                continue
            shortened = [
                n
                for n in ast.walk(stored)
                if isinstance(n, ast.Subscript)
                or (
                    isinstance(n, ast.Call)
                    and isinstance(n.func, ast.Attribute)
                    and n.func.attr
                    in {"rsplit", "split", "rpartition", "partition", "removeprefix"}
                )
            ]
            assert not shortened, (
                f"{path.name}:{stored.lineno} stores difficulty_source = {ast.unparse(stored)}: "
                "keep the full operation as returned (R-F3), never a shortened tail"
            )
            if ast.unparse(stored).startswith("_difficulty_guarded("):
                checked += 1  # conflict-update clause: keeps the stored column
                continue
            assert ast.unparse(stored) == "run.request.operation", (
                f"{path.name}:{stored.lineno} difficulty_source must be run.request.operation, "
                f"got {ast.unparse(stored)}"
            )
            checked += 1
    assert checked >= 1, "expected the ORM writer to set difficulty_source"


def test_difficulty_guard_catches_the_rsplit_shape() -> None:
    old = ast.parse(
        'row = {"raw": 1, "source_provider": 2, "difficulty_source": '
        '(str(run.request.operation).rsplit(".", 1)[-1] if w is not None else None)}'
    )
    (row,) = _row_dicts(old)
    stored = _difficulty_source_stored(_value(row, "difficulty_source"))
    assert isinstance(stored, ast.Subscript)
    assert ast.unparse(stored) != "run.request.operation"
