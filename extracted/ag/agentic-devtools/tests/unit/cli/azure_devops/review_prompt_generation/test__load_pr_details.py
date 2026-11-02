"""Tests for _load_pr_details."""

import json
from typing import Any

import pytest

from agentic_devtools.cli.azure_devops.review_prompt_generation import _load_pr_details


def test_uses_supplied_details_without_reading_artifact(tmp_path) -> None:
    details: dict[str, Any] = {"files": []}
    assert _load_pr_details(tmp_path / "missing.json", details) is details


def test_reads_details_artifact_when_not_supplied(tmp_path) -> None:
    details_path = tmp_path / "details.json"
    details_path.write_text(json.dumps({"files": [{"path": "src/file.py"}]}), encoding="utf-8")

    assert _load_pr_details(details_path, None) == {"files": [{"path": "src/file.py"}]}


def test_raises_when_details_artifact_is_missing(tmp_path) -> None:
    with pytest.raises(FileNotFoundError, match="Run get_pull_request_details first"):
        _load_pr_details(tmp_path / "missing.json", None)
