"""Tests for agentic_devtools.orchestration.nodes.commit._classify_push_failure."""

import pytest

from agentic_devtools.orchestration.nodes import commit as commit_mod


class TestClassifyPushFailure:
    @pytest.mark.parametrize(
        ("stderr", "category"),
        [
            ("remote: error: GH006: Protected branch update failed", "protection"),
            ("remote: error: GH013: Repository rule violations found", "protection"),
            ("pre-receive hook declined", "protection"),
            ("fatal: Authentication failed", "auth"),
            ("Permission denied (publickey)", "auth"),
            ("could not read Username", "auth"),
            ("remote: Repository not found.", "auth"),
            ("The requested URL returned error: 403", "auth"),
            ("! [rejected] main -> main (non-fast-forward)", "conflict"),
            ("error: some completely unknown git error", "transient"),
        ],
    )
    def test_classifies_stderr(self, stderr, category):
        assert commit_mod._classify_push_failure(stderr).category == category
