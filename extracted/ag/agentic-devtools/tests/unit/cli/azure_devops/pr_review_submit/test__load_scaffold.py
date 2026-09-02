"""Tests for _load_scaffold."""

import json

import pytest

from agentic_devtools.cli.azure_devops.pr_review_submit import _load_scaffold


class TestLoadScaffold:
    def test_missing_returns_none(self, tmp_path):
        assert _load_scaffold(tmp_path, "k") is None

    def test_valid_object(self, tmp_path):
        (tmp_path / "k.answer.json").write_text(json.dumps({"fileKey": "k"}), encoding="utf-8")
        assert _load_scaffold(tmp_path, "k") == {"fileKey": "k"}

    def test_malformed_json_returns_none(self, tmp_path):
        (tmp_path / "k.answer.json").write_text("{not json", encoding="utf-8")
        assert _load_scaffold(tmp_path, "k") is None

    def test_non_object_returns_none(self, tmp_path):
        (tmp_path / "k.answer.json").write_text("[1, 2]", encoding="utf-8")
        assert _load_scaffold(tmp_path, "k") is None

    @pytest.mark.parametrize("file_key", ["../escape", "..\\escape", "/tmp/escape", "../../escape"])
    def test_unsafe_file_key_returns_none(self, tmp_path, file_key):
        assert _load_scaffold(tmp_path, file_key) is None
