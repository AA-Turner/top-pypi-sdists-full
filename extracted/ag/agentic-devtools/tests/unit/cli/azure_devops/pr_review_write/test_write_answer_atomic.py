"""Tests for write_answer_atomic."""

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.azure_devops.pr_review_write import write_answer_atomic


class TestWriteAnswerAtomic:
    def test_writes_json_and_creates_dir(self, tmp_path):
        target = tmp_path / "answers" / "k.answer.json"
        write_answer_atomic(target, {"fileKey": "k", "status": "complete"})
        assert target.exists()
        assert json.loads(target.read_text(encoding="utf-8"))["fileKey"] == "k"

    def test_overwrites_existing(self, tmp_path):
        target = tmp_path / "k.answer.json"
        target.write_text('{"old": true}', encoding="utf-8")
        write_answer_atomic(target, {"new": True})
        assert json.loads(target.read_text(encoding="utf-8")) == {"new": True}

    def test_no_temp_left_behind(self, tmp_path):
        target = tmp_path / "k.answer.json"
        write_answer_atomic(target, {"x": 1})
        assert list(tmp_path.glob("*.tmp")) == []

    def test_cleans_up_temp_when_replace_fails(self, tmp_path):
        target = tmp_path / "k.answer.json"
        with (
            patch(
                "agentic_devtools.cli.azure_devops.pr_review_write.os.replace",
                side_effect=OSError("disk full"),
            ),
            pytest.raises(OSError),
        ):
            write_answer_atomic(target, {"x": 1})
        assert list(tmp_path.glob("*.tmp")) == []
