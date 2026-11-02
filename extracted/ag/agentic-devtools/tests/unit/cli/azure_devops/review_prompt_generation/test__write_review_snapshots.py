"""Tests for _write_review_snapshots."""

import json
from unittest.mock import patch

from agentic_devtools.cli.azure_devops.review_prompt_generation import _write_review_snapshots


def test_writes_pr_thread_and_empty_jira_snapshots(tmp_path) -> None:
    with patch("agentic_devtools.cli.azure_devops.review_prompt_generation.get_state_dir", return_value=tmp_path):
        _write_review_snapshots(tmp_path, [{"path": "src/file.py"}], [{"id": 1}])

    assert json.loads((tmp_path / "pull-request-files.json").read_text(encoding="utf-8")) == {
        "files": [{"path": "src/file.py"}]
    }
    assert json.loads((tmp_path / "pull-request-threads.json").read_text(encoding="utf-8")) == {"threads": [{"id": 1}]}
    assert (tmp_path / "pull-request-jira-issue.json").read_text(encoding="utf-8") == "{}"
