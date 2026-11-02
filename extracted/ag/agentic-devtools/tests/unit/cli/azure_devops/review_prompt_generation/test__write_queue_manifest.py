"""Tests for _write_queue_manifest."""

import json

from agentic_devtools.cli.azure_devops.review_prompt_generation import _write_queue_manifest


def test_writes_queue_metadata_and_pending_entries(tmp_path) -> None:
    pending = [{"path": "src/file.py", "status": "pending"}]
    _write_queue_manifest(tmp_path, 42, 1, pending)

    payload = json.loads((tmp_path / "queue.json").read_text(encoding="utf-8"))
    assert payload["pullRequestId"] == 42
    assert payload["total"] == 1
    assert payload["pending"] == pending
    assert payload["completed"] == []
    assert payload["generatedUtc"]
