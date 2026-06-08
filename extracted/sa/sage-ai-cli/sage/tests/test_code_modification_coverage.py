"""Full-branch tests for sage.core.code_modification.{CodeModification,SelfModificationSystem}.

Distinct from the deprecated test_code_modification_comprehensive.py (which
targeted an older API of ~30 dataclasses). This file tests the CURRENT
small public surface.
"""

from __future__ import annotations

import textwrap

import pytest

from sage.core.code_modification import (
    CodeModification,
    SelfModificationSystem,
)


@pytest.fixture
def sandbox(tmp_path):
    """A throwaway sage_root with one tiny module to modify."""
    (tmp_path / "sample.py").write_text(textwrap.dedent("""
        def add(a, b):
            return a + b

        class Counter:
            def __init__(self):
                self.value = 0
            def increment(self):
                self.value += 1
        # TODO: add multiply
    """).lstrip())
    return SelfModificationSystem(str(tmp_path))


class TestAnalyzeOwnCode:

    def test_returns_function_and_class_metadata(self, sandbox):
        analysis = sandbox.analyze_own_code("sample.py")
        assert analysis["file"] == "sample.py"
        assert any(f["name"] == "add" for f in analysis["functions"])
        assert any(c["name"] == "Counter" for c in analysis["classes"])
        # The Counter class has __init__ + increment = 2 methods
        counter = next(c for c in analysis["classes"] if c["name"] == "Counter")
        assert counter["methods"] == 2

    def test_picks_up_todos(self, sandbox):
        analysis = sandbox.analyze_own_code("sample.py")
        assert analysis["todos"]
        assert any("TODO" in todo["content"] for todo in analysis["todos"])

    def test_missing_file_raises(self, sandbox):
        with pytest.raises(FileNotFoundError):
            sandbox.analyze_own_code("nope.py")

    def test_syntax_error_is_reported_not_raised(self, sandbox, tmp_path):
        (tmp_path / "broken.py").write_text("def x(\n")
        analysis = sandbox.analyze_own_code("broken.py")
        assert any("Syntax error" in i for i in analysis["issues"])


class TestProposeModification:

    def test_marks_safe_by_default(self, sandbox):
        mod = sandbox.propose_modification(
            "sample.py", "old", "new", description="trivial",
        )
        assert mod.is_safe is True
        assert mod.modification_type == "replace"

    def test_flags_dangerous_added_subprocess_call(self, sandbox):
        mod = sandbox.propose_modification(
            "sample.py",
            "def add(a, b): return a + b",
            "import subprocess\nsubprocess.call(['rm', '-rf', '/'])",
            description="exfiltrate",
        )
        assert mod.is_safe is False

    def test_dangerous_already_present_in_original_is_ok(self, sandbox):
        """If the dangerous pattern was already in the original, modifying it
        further doesn't add new risk — we don't flag those."""
        mod = sandbox.propose_modification(
            "sample.py",
            "subprocess.call(['ls'])",
            "subprocess.call(['ls', '-la'])",
            description="add a flag to an existing subprocess.call",
        )
        assert mod.is_safe is True

    def test_modifications_are_tracked(self, sandbox):
        sandbox.propose_modification("sample.py", "a", "b", description="m1")
        sandbox.propose_modification("sample.py", "c", "d", description="m2")
        assert len(sandbox._modifications) == 2


class TestApplyModification:

    def test_applies_safe_modification(self, sandbox, tmp_path):
        mod = sandbox.propose_modification(
            "sample.py", "return a + b", "return a + b + 1",
            description="off-by-one",
        )
        assert sandbox.apply_modification(mod) is True
        assert "return a + b + 1" in (tmp_path / "sample.py").read_text()

    def test_unsafe_modification_rejected(self, sandbox):
        mod = CodeModification(
            file_path="sample.py",
            original_code="x",
            modified_code="y",
            modification_type="replace",
            line_start=0, line_end=0,
            description="bad",
            is_safe=False,
        )
        with pytest.raises(ValueError):
            sandbox.apply_modification(mod)

    def test_missing_file_raises(self, sandbox):
        mod = CodeModification(
            file_path="nope.py",
            original_code="x", modified_code="y",
            modification_type="replace",
            line_start=0, line_end=0,
            description="x",
        )
        with pytest.raises(FileNotFoundError):
            sandbox.apply_modification(mod)

    def test_falls_back_to_line_based_replace(self, sandbox, tmp_path):
        """If exact str.replace doesn't match, the line-by-line fallback runs."""
        # Original code has trailing whitespace that str.replace won't see
        # because the proposed `original_code` has different surrounding text.
        original = "def add(a, b):\n    return a + b"
        modified = "def add(a, b):\n    return a + b  # bumped"
        mod = sandbox.propose_modification(
            "sample.py", original, modified, description="add comment",
        )
        assert sandbox.apply_modification(mod) is True
        assert "# bumped" in (tmp_path / "sample.py").read_text()


def test_code_modification_dataclass_defaults():
    m = CodeModification(
        file_path="x.py", original_code="a", modified_code="b",
        modification_type="replace", line_start=0, line_end=0,
        description="x",
    )
    # Default values for is_safe + requires_tests
    assert m.is_safe is True
    assert m.requires_tests is True
