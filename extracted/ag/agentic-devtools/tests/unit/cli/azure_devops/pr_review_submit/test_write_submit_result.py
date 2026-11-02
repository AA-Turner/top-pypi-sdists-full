"""Tests for write_submit_result."""

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.azure_devops.pr_review_submit import (
    SUBMIT_RESULT_FILENAME,
    write_submit_result,
)

_MODULE = "agentic_devtools.cli.azure_devops.pr_review_submit"


class TestWriteSubmitResult:
    def test_writes_json_and_returns_path(self, tmp_path):
        answers_dir = tmp_path / "answers"
        path = write_submit_result(answers_dir, {"counts": {"accepted": 1}})
        assert path == answers_dir / SUBMIT_RESULT_FILENAME
        assert json.loads(path.read_text(encoding="utf-8"))["counts"]["accepted"] == 1

    def test_os_error_cleans_temp_and_reraises(self, tmp_path):
        answers_dir = tmp_path / "answers"
        with patch(f"{_MODULE}.os.replace", side_effect=OSError("nope")):
            with pytest.raises(OSError):
                write_submit_result(answers_dir, {"x": 1})
        # No temp files left behind.
        assert not list(answers_dir.glob("*.tmp"))
