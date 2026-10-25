"""No matrx-ai test imports the host (``aidream`` or its ``db`` models).

A matrx-* package never imports aidream (docs/packages/PACKAGE_BOUNDARIES.md), and that holds for
its tests too: ``scripts/check_package_boundaries.py`` scans package code, not tests, so eight tests
here failed with ``ModuleNotFoundError`` on every package-only run and two more sat behind skips
that always fired. A test that needs the host lives in the host's own ``aidream/**/tests`` tree.
"""

from __future__ import annotations

import ast
from pathlib import Path

TESTS = Path(__file__).resolve().parent
HOST_ROOTS = frozenset({"aidream", "db"})


def host_imports(root: Path) -> list[str]:
    hits: list[str] = []
    for path in sorted(root.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            names: list[str] = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                names = [node.module]
            elif (
                isinstance(node, ast.Call)
                and getattr(node.func, "attr", getattr(node.func, "id", ""))
                in {"importorskip", "import_module"}
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)
            ):
                names = [node.args[0].value]
            for name in names:
                if name.split(".", 1)[0] in HOST_ROOTS:
                    hits.append(f"{path.relative_to(root)}:{node.lineno}: {name}")
    return hits


def test_no_package_test_imports_the_host() -> None:
    assert host_imports(TESTS) == []


def test_the_guard_sees_every_way_a_test_reaches_the_host(tmp_path: Path) -> None:
    (tmp_path / "test_x.py").write_text(
        "import aidream.kinds\n"
        "from db.models.chat import Message\n"
        "def t():\n"
        "    from aidream.api.routers import cancel\n"
        "    pytest.importorskip('aidream')\n"
        "    importlib.import_module('db.models')\n"
        "from dbt import x\n"
        "from .db import y\n"
    )
    assert len(host_imports(tmp_path)) == 5
