"""Tests for _file_imports_stem."""

from __future__ import annotations

from agentic_devtools.cli.checks.changed_files import _file_imports_stem


class TestFileImportsStem:
    """Tests for _file_imports_stem."""

    def test_from_import_with_stem_in_module_returns_true(self) -> None:
        text = "from tests.unit.adapters._contract_scenarios.helpers import util\n"
        assert _file_imports_stem(text, "_contract_scenarios") is True

    def test_from_import_with_stem_as_name_returns_true(self) -> None:
        text = "from tests.unit.adapters import _contract_scenarios\n"
        assert _file_imports_stem(text, "_contract_scenarios") is True

    def test_direct_import_with_stem_returns_true(self) -> None:
        text = "import _contract_scenarios\n"
        assert _file_imports_stem(text, "_contract_scenarios") is True

    def test_multiline_from_import_returns_true(self) -> None:
        text = "from tests.unit.adapters.issue_provider import (\n    _contract_scenarios,\n)\n"
        assert _file_imports_stem(text, "_contract_scenarios") is True

    def test_no_matching_import_returns_false(self) -> None:
        text = "import os\nfrom pathlib import Path\n"
        assert _file_imports_stem(text, "_contract_scenarios") is False

    def test_stem_in_comment_only_returns_false(self) -> None:
        text = "import os\n# _contract_scenarios is great\n"
        assert _file_imports_stem(text, "_contract_scenarios") is False

    def test_syntax_error_falls_back_to_line_heuristic_match(self) -> None:
        text = "import _contract_scenarios\n!invalid python!\n"
        assert _file_imports_stem(text, "_contract_scenarios") is True

    def test_syntax_error_falls_back_to_line_heuristic_no_match(self) -> None:
        text = "!invalid python!\n"
        assert _file_imports_stem(text, "_contract_scenarios") is False
