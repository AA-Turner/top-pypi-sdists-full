"""Tests for load_queue_entries."""

import json

from agentic_devtools.cli.azure_devops.pr_review_manifest import load_queue_entries


class TestLoadQueueEntries:
    def test_missing_file(self, tmp_path):
        assert load_queue_entries(tmp_path) == []

    def test_bad_json(self, tmp_path):
        (tmp_path / "queue.json").write_text("{ not json", encoding="utf-8")
        assert load_queue_entries(tmp_path) == []

    def test_os_error_when_queue_is_directory(self, tmp_path):
        (tmp_path / "queue.json").mkdir()
        assert load_queue_entries(tmp_path) == []

    def test_pending_not_list(self, tmp_path):
        (tmp_path / "queue.json").write_text(json.dumps({"pending": {}}), encoding="utf-8")
        assert load_queue_entries(tmp_path) == []

    def test_pending_list(self, tmp_path):
        (tmp_path / "queue.json").write_text(json.dumps({"pending": [{"path": "/a"}]}), encoding="utf-8")
        assert load_queue_entries(tmp_path) == [{"path": "/a"}]
