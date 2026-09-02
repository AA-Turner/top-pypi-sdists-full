"""Tests for find_consumer_test_paths."""

from __future__ import annotations

from agentic_devtools.cli.checks.changed_files import find_consumer_test_paths


class TestFindConsumerTestPaths:
    """Tests for find_consumer_test_paths."""

    def test_conftest_maps_to_containing_directory(self, tmp_path):
        result = find_consumer_test_paths("tests/unit/adapters/conftest.py", cwd=tmp_path)
        assert result == ["tests/unit/adapters"]

    def test_top_level_conftest_maps_to_tests(self, tmp_path):
        result = find_consumer_test_paths("conftest.py", cwd=tmp_path)
        assert result == ["tests"]

    def test_underscore_helper_maps_to_importing_test_files(self, tmp_path):
        tests_root = tmp_path / "tests" / "unit" / "adapters"
        consumer_dir = tests_root / "github_provider"
        consumer_dir.mkdir(parents=True)
        # An importing consumer suite.
        importer = consumer_dir / "test_githubprovider.py"
        importer.write_text(
            "from tests.unit.adapters.issue_provider import _contract_scenarios as c\n",
            encoding="utf-8",
        )
        # A test file that does not import the helper.
        (consumer_dir / "test_other.py").write_text("x = 1\n", encoding="utf-8")
        result = find_consumer_test_paths("tests/unit/adapters/issue_provider/_contract_scenarios.py", cwd=tmp_path)
        assert result == ["tests/unit/adapters/github_provider/test_githubprovider.py"]

    def test_underscore_helper_no_consumers_returns_empty(self, tmp_path):
        (tmp_path / "tests").mkdir()
        result = find_consumer_test_paths("tests/unit/adapters/issue_provider/_contract_scenarios.py", cwd=tmp_path)
        assert result == []

    def test_missing_tests_dir_returns_empty(self, tmp_path):
        result = find_consumer_test_paths("tests/unit/adapters/issue_provider/_contract_scenarios.py", cwd=tmp_path)
        assert result == []

    def test_unreadable_test_file_is_skipped(self, tmp_path):
        tests_root = tmp_path / "tests" / "unit"
        tests_root.mkdir(parents=True)
        # Invalid UTF-8 bytes make read_text raise UnicodeDecodeError; skipped gracefully.
        (tests_root / "test_binary.py").write_bytes(b"\xff\xfe import _contract_scenarios")
        result = find_consumer_test_paths("tests/unit/adapters/issue_provider/_contract_scenarios.py", cwd=tmp_path)
        assert result == []

    def test_import_line_without_stem_is_ignored(self, tmp_path):
        tests_root = tmp_path / "tests" / "unit"
        tests_root.mkdir(parents=True)
        # Mentions the stem but not on an import line, and imports something else.
        (tests_root / "test_foo.py").write_text(
            "import os\n# mentions _contract_scenarios in a comment only\n",
            encoding="utf-8",
        )
        result = find_consumer_test_paths("tests/unit/adapters/issue_provider/_contract_scenarios.py", cwd=tmp_path)
        assert result == []
