"""Tests for _parse_imports function."""

from __future__ import annotations

import ast
from unittest.mock import patch

from agentic_devtools.orchestration.review.import_resolver import _parse_imports


class TestParseImports:
    """Tests for AST import parsing."""

    def test_parses_import_statement(self) -> None:
        code = "import agentic_devtools.state"
        imports = _parse_imports(code)
        assert len(imports) == 1
        assert imports[0]["module"] == "agentic_devtools.state"
        assert imports[0]["names"] == ["agentic_devtools"]

    def test_parses_from_import(self) -> None:
        code = "from agentic_devtools.cli.git.core import get_current_branch"
        imports = _parse_imports(code)
        assert len(imports) == 1
        assert imports[0]["module"] == "agentic_devtools.cli.git.core"
        assert "get_current_branch" in imports[0]["names"]

    def test_parses_from_import_alias_name(self) -> None:
        """from-import aliases are tracked by bound alias name."""
        code = "from agentic_devtools.state import get_value as gv"
        imports = _parse_imports(code)
        assert len(imports) == 1
        assert imports[0]["names"] == ["gv"]

    def test_syntax_error_returns_empty(self) -> None:
        """Invalid syntax returns empty list (no exception)."""
        code = "def broken("
        imports = _parse_imports(code)
        assert imports == []

    def test_from_import_no_module_included_as_sibling(self) -> None:
        """from . import X (module-less relative) is included: each name treated as sibling module."""
        code = "from . import something\n"
        imports = _parse_imports(code)
        assert len(imports) == 1
        assert imports[0]["module"] == "something"
        assert imports[0]["level"] == 1
        assert "something" in imports[0]["names"]

    def test_relative_import_with_module_includes_level(self) -> None:
        """from .config import X is parsed and includes the level field."""
        code = "from .config import SomeClass\n"
        imports = _parse_imports(code)
        assert len(imports) == 1
        assert imports[0]["module"] == "config"
        assert imports[0]["level"] == 1
        assert "SomeClass" in imports[0]["names"]

    def test_relative_import_two_levels_includes_level(self) -> None:
        """from ..state import X is parsed with level=2."""
        code = "from ..state import get_value\n"
        imports = _parse_imports(code)
        assert len(imports) == 1
        assert imports[0]["module"] == "state"
        assert imports[0]["level"] == 2

    def test_import_from_node_with_no_module_and_level_zero_is_skipped(self) -> None:
        """An ImportFrom node with no module and level=0 is skipped (unreachable in valid Python)."""
        # Construct a synthetic ImportFrom node that has module=None and level=0.
        # This branch is unreachable via valid Python source but must be covered.
        synthetic = ast.ImportFrom(
            module=None,
            names=[ast.alias(name="something", asname=None)],
            level=0,
        )
        synthetic.lineno = 1
        tree = ast.Module(body=[synthetic], type_ignores=[])
        with patch(
            "agentic_devtools.orchestration.review.import_resolver.ast.parse",
            return_value=tree,
        ):
            imports = _parse_imports("placeholder")
        assert imports == []
