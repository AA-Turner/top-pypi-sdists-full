"""Tests for matching moved paths to workflow source contracts."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.checks.changed_files import find_workflow_contract_tests


@pytest.mark.parametrize(
    "reference",
    [
        "agentic_devtools/old.py",
        "agentic_devtools/new.py",
        r"agentic_devtools\new.py",
        "agentic_devtools.new",
        "agentic_devtools.new.get_new",
    ],
)
def test_matches_either_path_and_module_notation(tmp_path, reference):
    root = tmp_path / "tests/workflows"
    root.mkdir(parents=True)
    (root / "test_contract.py").write_text(f"SOURCE = {reference!r}\n", encoding="utf-8")
    (root / "test_unrelated.py").write_text("SOURCE = 'agentic_devtools/other.py'\n", encoding="utf-8")
    assert find_workflow_contract_tests([("agentic_devtools/old.py", "agentic_devtools/new.py")], cwd=tmp_path) == [
        "tests/workflows/test_contract.py"
    ]


def test_does_not_match_longer_dotted_module_identifier(tmp_path):
    root = tmp_path / "tests/workflows"
    root.mkdir(parents=True)
    (root / "test_contract.py").write_text(
        "PATCH_TARGET = 'agentic_devtools.new_module.get_new'\n",
        encoding="utf-8",
    )
    assert find_workflow_contract_tests([("agentic_devtools.old", "agentic_devtools.new")], cwd=tmp_path) == []


def test_no_moves_or_workflow_tree(tmp_path):
    assert find_workflow_contract_tests([], cwd=tmp_path) == []
    assert find_workflow_contract_tests([("old.py", "new.py")], cwd=tmp_path) == []


@pytest.mark.parametrize("error", [OSError(), UnicodeDecodeError("utf-8", b"x", 0, 1, "invalid")])
def test_unreadable_contract_is_skipped(tmp_path, error):
    root = tmp_path / "tests/workflows"
    root.mkdir(parents=True)
    (root / "test_contract.py").touch()
    with patch("pathlib.Path.read_text", side_effect=error):
        assert find_workflow_contract_tests([("old.py", "new.py")], cwd=tmp_path) == []
