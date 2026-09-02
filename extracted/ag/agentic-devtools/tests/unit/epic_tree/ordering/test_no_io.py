"""AST-based source inspection: no subprocess/requests imports and no open() calls."""

import ast
from pathlib import Path

from agentic_devtools.epic_tree import ordering


class TestNoIOInOrdering:
    """Verify ordering module has no subprocess/requests imports and no open() calls."""

    def test_no_disallowed_imports(self):
        """No imports of subprocess or requests modules."""
        source_path = Path(ordering.__file__)
        tree = ast.parse(source_path.read_text())
        disallowed = {"subprocess", "requests"}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name not in disallowed, f"Disallowed import: {alias.name}"
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.split(".")[0] in disallowed:
                    msg = f"Disallowed import from: {node.module}"
                    raise AssertionError(msg)

    def test_no_open_calls(self):
        """No open() builtin calls."""
        source_path = Path(ordering.__file__)
        tree = ast.parse(source_path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == "open":
                    msg = "Found open() call in ordering module"
                    raise AssertionError(msg)
