"""Tests for _persist_filtered_pr_details."""

import json
from unittest.mock import patch

from agentic_devtools.cli.azure_devops.review_prompt_generation import _persist_filtered_pr_details


def test_atomically_replaces_details_artifact_with_filtered_files(tmp_path) -> None:
    details_path = tmp_path / "details.json"
    details_path.write_text("{}", encoding="utf-8")
    details = {"files": [{"path": "src/kept.py"}]}

    _persist_filtered_pr_details(details_path, details)

    assert json.loads(details_path.read_text(encoding="utf-8")) == details
    assert not details_path.with_name("details.json.tmp").exists()


def test_does_nothing_when_details_artifact_is_missing(tmp_path) -> None:
    with patch("agentic_devtools.cli.azure_devops.review_prompt_generation.os.replace") as replace:
        _persist_filtered_pr_details(tmp_path / "missing.json", {})

    replace.assert_not_called()
