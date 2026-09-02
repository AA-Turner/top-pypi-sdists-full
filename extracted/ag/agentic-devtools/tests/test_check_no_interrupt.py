"""Tests for scripts/check_no_interrupt.py."""

from __future__ import annotations

import ast
import importlib.util
import textwrap
from pathlib import Path


def _load_module():
    """Load scripts/check_no_interrupt.py as a module."""
    repo_root = Path(__file__).resolve().parents[1]
    script_path = repo_root / "scripts" / "check_no_interrupt.py"
    spec = importlib.util.spec_from_file_location("check_no_interrupt", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load check_no_interrupt.py from {script_path!s}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checker = _load_module()


# ---------------------------------------------------------------------------
# _find_interrupt_aliases
# ---------------------------------------------------------------------------


class TestFindInterruptAliases:
    """Tests for _find_interrupt_aliases()."""

    def test_direct_import_returns_interrupt(self):

        src = "from langgraph.types import interrupt"
        tree = ast.parse(src)
        assert checker._find_interrupt_aliases(tree) == {"interrupt"}

    def test_aliased_import_returns_alias(self):

        src = "from langgraph.types import interrupt as intr"
        tree = ast.parse(src)
        assert checker._find_interrupt_aliases(tree) == {"intr"}

    def test_unrelated_import_returns_empty(self):

        src = "from langgraph.types import Command"
        tree = ast.parse(src)
        assert checker._find_interrupt_aliases(tree) == set()

    def test_no_imports_returns_empty(self):

        src = "x = 1"
        tree = ast.parse(src)
        assert checker._find_interrupt_aliases(tree) == set()


# ---------------------------------------------------------------------------
# _find_langgraph_types_aliases
# ---------------------------------------------------------------------------


class TestFindLanggraphTypesAliases:
    """Tests for _find_langgraph_types_aliases()."""

    def test_import_with_alias(self):

        src = "import langgraph.types as lg_types"
        tree = ast.parse(src)
        assert checker._find_langgraph_types_aliases(tree) == {"lg_types"}

    def test_import_without_alias_not_detected(self):
        """``import langgraph.types`` without an alias binds ``langgraph``, not ``types``."""

        src = "import langgraph.types"
        tree = ast.parse(src)
        # Without an asname Python binds the root name 'langgraph', not 'types'.
        # Our detector only catches explicit aliases; the full chain is caught by
        # _is_langgraph_types_interrupt instead.
        assert checker._find_langgraph_types_aliases(tree) == set()

    def test_from_langgraph_import_types(self):

        src = "from langgraph import types"
        tree = ast.parse(src)
        assert checker._find_langgraph_types_aliases(tree) == {"types"}

    def test_from_langgraph_import_types_with_alias(self):

        src = "from langgraph import types as t"
        tree = ast.parse(src)
        assert checker._find_langgraph_types_aliases(tree) == {"t"}

    def test_unrelated_import_returns_empty(self):

        src = "from langgraph import checkpoint"
        tree = ast.parse(src)
        assert checker._find_langgraph_types_aliases(tree) == set()

    def test_multiple_aliases_collected(self):

        src = textwrap.dedent("""\
            import langgraph.types as lg_types
            from langgraph import types as t
        """)
        tree = ast.parse(src)
        assert checker._find_langgraph_types_aliases(tree) == {"lg_types", "t"}


# ---------------------------------------------------------------------------
# _check_file (using tmp_path to write real files)
# ---------------------------------------------------------------------------


class TestCheckFile:
    """Tests for _check_file() covering all detection patterns."""

    def _write(self, tmp_path: Path, src: str) -> Path:
        p = tmp_path / "test_module.py"
        p.write_text(textwrap.dedent(src))
        return p

    def test_clean_file_produces_no_violations(self, tmp_path: Path):
        fp = self._write(tmp_path, "x = 1\n")
        assert checker._check_file(fp) == []

    # --- direct call ---

    def test_direct_interrupt_call_detected(self, tmp_path: Path):
        fp = self._write(
            tmp_path,
            """\
            def node(state):
                interrupt("waiting")
            """,
        )
        violations = checker._check_file(fp)
        assert len(violations) == 1
        assert "interrupt" in violations[0]

    # --- from langgraph.types import interrupt ---

    def test_aliased_interrupt_direct_call_detected(self, tmp_path: Path):
        fp = self._write(
            tmp_path,
            """\
            from langgraph.types import interrupt as intr
            def node(state):
                intr("waiting")
            """,
        )
        violations = checker._check_file(fp)
        assert len(violations) == 1
        assert "intr" in violations[0]

    # --- langgraph.types.interrupt(...) ---

    def test_full_chain_attribute_call_detected(self, tmp_path: Path):
        fp = self._write(
            tmp_path,
            """\
            import langgraph.types
            def node(state):
                langgraph.types.interrupt("waiting")
            """,
        )
        violations = checker._check_file(fp)
        assert len(violations) == 1
        assert "langgraph.types.interrupt" in violations[0]

    # --- import langgraph.types as X; X.interrupt(...) ---

    def test_module_alias_import_call_detected(self, tmp_path: Path):
        fp = self._write(
            tmp_path,
            """\
            import langgraph.types as lg_types
            def node(state):
                lg_types.interrupt("waiting")
            """,
        )
        violations = checker._check_file(fp)
        assert len(violations) == 1
        assert "lg_types.interrupt" in violations[0]

    # --- from langgraph import types; types.interrupt(...) ---

    def test_submodule_import_call_detected(self, tmp_path: Path):
        fp = self._write(
            tmp_path,
            """\
            from langgraph import types
            def node(state):
                types.interrupt("waiting")
            """,
        )
        violations = checker._check_file(fp)
        assert len(violations) == 1
        assert "types.interrupt" in violations[0]

    # --- from langgraph import types as t; t.interrupt(...) ---

    def test_submodule_aliased_import_call_detected(self, tmp_path: Path):
        fp = self._write(
            tmp_path,
            """\
            from langgraph import types as t
            def node(state):
                t.interrupt("waiting")
            """,
        )
        violations = checker._check_file(fp)
        assert len(violations) == 1
        assert "t.interrupt" in violations[0]

    def test_unrelated_interrupt_method_not_flagged(self, tmp_path: Path):
        """Calls like ``my_obj.interrupt()`` from unrelated modules must not trigger."""
        fp = self._write(
            tmp_path,
            """\
            class Event:
                def interrupt(self):
                    pass
            e = Event()
            e.interrupt()
            """,
        )
        violations = checker._check_file(fp)
        assert violations == []
