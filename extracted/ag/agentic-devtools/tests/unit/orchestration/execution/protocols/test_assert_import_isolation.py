"""Tests for assert_import_isolation sentinel check."""

from agentic_devtools.orchestration.execution.protocols import assert_import_isolation


class TestAssertImportIsolation:
    def test_no_forbidden_imports(self) -> None:
        """SC-005: execution package imports no LLM provider libraries."""
        # Should NOT raise
        assert_import_isolation()
