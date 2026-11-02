"""Tests for _collect_extra_test_targets."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.checks.changed_files import DiffUnavailableError
from agentic_devtools.cli.checks.commands import _collect_extra_test_targets
from agentic_devtools.cli.checks.tests import _find_test_path

MODULE = "agentic_devtools.cli.checks.commands"


@pytest.fixture(autouse=True)
def no_module_moves():
    """Keep existing selection tests independent of repository history."""
    with patch(f"{MODULE}.get_python_module_moves", return_value=[]):
        yield


class TestCollectExtraTestTargets:
    """Tests for _collect_extra_test_targets."""

    @patch(f"{MODULE}.get_changed_files", return_value=[])
    @patch(f"{MODULE}._find_test_path", return_value=None)
    def test_uncovered_changed_test_returned(self, _ftp, _gcf, tmp_path):
        result = _collect_extra_test_targets(["tests/unit/other/test_bar.py"], [], tmp_path)
        assert result == ["tests/unit/other/test_bar.py"]

    @patch(f"{MODULE}.get_changed_files", return_value=[])
    def test_covered_by_test_file_excluded(self, _gcf, tmp_path):
        covered = "tests/unit/foo/test_foo.py"
        with patch(f"{MODULE}._find_test_path", return_value=str(tmp_path / covered)):
            result = _collect_extra_test_targets([covered], ["agentic_devtools/foo.py"], tmp_path)
        assert result == []

    @patch(f"{MODULE}.get_changed_files", return_value=[])
    def test_covered_by_directory_excluded(self, _gcf, tmp_path):
        covered_dir = tmp_path / "tests" / "unit" / "foo"
        with patch(f"{MODULE}._find_test_path", return_value=str(covered_dir)):
            result = _collect_extra_test_targets(["tests/unit/foo/test_bar.py"], ["agentic_devtools/foo.py"], tmp_path)
        assert result == []

    @patch(f"{MODULE}.get_changed_files", return_value=[])
    def test_covered_directory_equal_candidate_excluded(self, _gcf, tmp_path):
        covered_dir = tmp_path / "tests" / "unit" / "foo"
        with patch(f"{MODULE}._find_test_path", return_value=str(covered_dir)):
            result = _collect_extra_test_targets(["tests/unit/foo"], ["agentic_devtools/foo.py"], tmp_path)
        assert result == []

    @patch(f"{MODULE}.find_consumer_test_paths", return_value=["tests/unit/adapters/github_provider/test_x.py"])
    @patch(f"{MODULE}.get_changed_files", return_value=["tests/unit/adapters/issue_provider/_c.py"])
    @patch(f"{MODULE}._find_test_path", return_value=None)
    def test_support_file_consumer_added(self, _ftp, _gcf, _fctp, tmp_path):
        result = _collect_extra_test_targets([], [], tmp_path)
        assert result == ["tests/unit/adapters/github_provider/test_x.py"]

    @pytest.mark.parametrize("consumer", ["tests/unit/other/test_bar.py", "tests/unit/other"])
    @patch(f"{MODULE}.find_consumer_test_paths")
    @patch(f"{MODULE}.get_changed_files", return_value=["tests/conftest.py"])
    @patch(f"{MODULE}._find_test_path", return_value=None)
    def test_support_consumer_not_duplicated(self, _ftp, _gcf, _fctp, tmp_path, consumer):
        _fctp.return_value = [consumer]
        result = _collect_extra_test_targets([consumer], [], tmp_path)
        assert result == [consumer]

    @patch(f"{MODULE}.find_consumer_test_paths", return_value=["tests/unit/foo/test_bar.py"])
    @patch(f"{MODULE}.get_changed_files", return_value=["tests/conftest.py"])
    def test_support_consumer_already_covered_excluded(self, _gcf, _fctp, tmp_path):
        covered_dir = tmp_path / "tests" / "unit" / "foo"
        with patch(f"{MODULE}._find_test_path", return_value=str(covered_dir)):
            result = _collect_extra_test_targets([], ["agentic_devtools/foo.py"], tmp_path)
        assert result == []

    @patch(f"{MODULE}.find_consumer_test_paths")
    @patch(f"{MODULE}.get_changed_files", side_effect=DiffUnavailableError("no git"))
    @patch(f"{MODULE}._find_test_path", return_value=None)
    def test_diff_unavailable_skips_support_mapping(self, _ftp, _gcf, mock_fctp, tmp_path):
        result = _collect_extra_test_targets(["tests/unit/other/test_bar.py"], [], tmp_path)
        assert result == ["tests/unit/other/test_bar.py"]
        mock_fctp.assert_not_called()

    @pytest.mark.parametrize("moved", [True, False])
    @patch(f"{MODULE}.get_changed_files", return_value=[])
    def test_agent_task_extraction_retains_narrow_tests(self, _gcf, tmp_path, moved):
        """Model the source transition present at e151e09a in PR #4486."""
        old = "agentic_devtools/cli/ci/pipeline/session_detector.py"
        new = "agentic_devtools/cli/ci/agent_task_inventory.py"
        unit = "tests/unit/cli/ci/agent_task_inventory/test_load_agent_task_inventory.py"
        contract = "tests/workflows/test_github_read_token_pool_workflow_contracts.py"
        unit_path = tmp_path / unit
        unit_path.parent.mkdir(parents=True)
        unit_path.touch()
        contract_path = tmp_path / contract
        contract_path.parent.mkdir(parents=True)
        contract_path.write_text(
            f"def test_python_readonly_gh_calls_use_the_shared_pooled_runner():\n    paths = ({old!r}, {new!r})\n",
            encoding="utf-8",
        )
        (contract_path.parent / "test_unrelated.py").write_text("SOURCE = 'unrelated.py'\n", encoding="utf-8")
        with patch(f"{MODULE}.get_python_module_moves", return_value=[(old, new)] if moved else []):
            extra = _collect_extra_test_targets([unit], [new], tmp_path)
            duplicate = _collect_extra_test_targets([unit, contract], [new], tmp_path)
        # Per-file coverage owns the narrow suite; extras must not run it twice.
        assert extra == ([contract] if moved else [])
        assert duplicate == [contract]
        coverage_target = _find_test_path(new, tmp_path)
        assert coverage_target is not None
        selected = [path.relative_to(tmp_path).as_posix() for path in Path(coverage_target).glob("test_*.py")]
        selected.extend(extra)
        assert selected == ([unit, contract] if moved else [unit])

    @patch(f"{MODULE}.get_changed_files", return_value=[])
    def test_reverse_dependent_test_is_selected(self, _gcf, tmp_path):
        source = tmp_path / "agentic_devtools" / "app.py"
        source.parent.mkdir(parents=True)
        source.write_text("VALUE = 1\n", encoding="utf-8")
        test = tmp_path / "tests" / "unit" / "other" / "test_app.py"
        test.parent.mkdir(parents=True)
        test.write_text("from agentic_devtools.app import VALUE\n", encoding="utf-8")

        assert _collect_extra_test_targets([], ["agentic_devtools/app.py"], tmp_path) == [
            "tests/unit/other/test_app.py"
        ]

    @patch(f"{MODULE}.get_changed_files", return_value=[])
    def test_initializer_only_change_seeds_reverse_dependency_discovery(self, _gcf, tmp_path):
        initializer = tmp_path / "agentic_devtools" / "feature" / "__init__.py"
        initializer.parent.mkdir(parents=True)
        initializer.write_text("from agentic_devtools.core import Core\n", encoding="utf-8")
        (tmp_path / "agentic_devtools" / "core.py").write_text("class Core: ...\n", encoding="utf-8")
        worker = initializer.parent / "worker.py"
        worker.write_text("class Worker: ...\n", encoding="utf-8")
        test = tmp_path / "tests" / "unit" / "other" / "test_worker.py"
        test.parent.mkdir(parents=True)
        test.write_text("from agentic_devtools.feature.worker import Worker\n", encoding="utf-8")

        assert _collect_extra_test_targets(
            [],
            [],
            tmp_path,
            changed_source_for_discovery=["agentic_devtools/feature/__init__.py"],
        ) == ["tests/unit/other/test_worker.py"]

    @patch(f"{MODULE}.get_changed_files", return_value=[])
    def test_reverse_dependency_miss_adds_no_unrelated_targets(self, _gcf, tmp_path):
        source = tmp_path / "agentic_devtools" / "app.py"
        source.parent.mkdir(parents=True)
        source.write_text("VALUE = 1\n", encoding="utf-8")
        test = tmp_path / "tests" / "unit" / "test_unrelated.py"
        test.parent.mkdir(parents=True)
        test.write_text("import json\n", encoding="utf-8")

        assert _collect_extra_test_targets([], ["agentic_devtools/app.py"], tmp_path) == []

    @patch(f"{MODULE}.get_changed_files", return_value=["tests/unit/_support.py"])
    def test_reverse_changed_test_and_support_routes_are_deduplicated(self, _gcf, tmp_path):
        source = tmp_path / "agentic_devtools" / "app.py"
        source.parent.mkdir(parents=True)
        source.write_text("VALUE = 1\n", encoding="utf-8")
        support = tmp_path / "tests" / "unit" / "_support.py"
        support.parent.mkdir(parents=True)
        support.write_text("FIXTURE = True\n", encoding="utf-8")
        test = tmp_path / "tests" / "unit" / "test_app.py"
        test.write_text(
            "from agentic_devtools.app import VALUE\nfrom tests.unit import _support\n",
            encoding="utf-8",
        )

        assert _collect_extra_test_targets(["tests/unit/test_app.py"], ["agentic_devtools/app.py"], tmp_path) == [
            "tests/unit/test_app.py"
        ]

    @patch(f"{MODULE}.get_changed_files", return_value=["tests/unit/other/conftest.py"])
    def test_shared_support_directory_covers_reverse_dependent_test(self, _gcf, tmp_path):
        source = tmp_path / "agentic_devtools" / "app.py"
        source.parent.mkdir(parents=True)
        source.write_text("VALUE = 1\n", encoding="utf-8")
        support = tmp_path / "tests" / "unit" / "other" / "conftest.py"
        support.parent.mkdir(parents=True)
        support.write_text("FIXTURE = True\n", encoding="utf-8")
        test = support.parent / "test_app.py"
        test.write_text("from agentic_devtools.app import VALUE\n", encoding="utf-8")

        assert _collect_extra_test_targets([], ["agentic_devtools/app.py"], tmp_path) == ["tests/unit/other"]

    @patch(f"{MODULE}.get_changed_files", return_value=[])
    def test_real_repository_session_detector_selects_provider_test(self, _gcf):
        source = "agentic_devtools/cli/ci/pipeline/session_detector.py"
        provider_test = "tests/unit/cli/ci/github_provider/test_list_pr_agent_task_lifecycles.py"

        selected = _collect_extra_test_targets([], [source], Path(__file__).parents[5])

        selected_target_count = len(selected)
        assert isinstance(selected_target_count, int) and selected_target_count > 0
        assert provider_test in selected
        print(f"Reverse-dependent selected targets: {selected_target_count}")
