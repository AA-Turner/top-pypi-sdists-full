"""Tests for agentic_devtools.orchestration.nodes.commit._commit_result_field."""

from agentic_devtools.models.git_results import CommitResult
from agentic_devtools.orchestration.nodes import commit as commit_mod


class TestCommitResultField:
    def test_supports_dict_checkpoint_values(self):
        assert commit_mod._commit_result_field({"commit_sha": "abc"}, "commit_sha") == "abc"

    def test_supports_commitresult_attributes(self):
        result = CommitResult(commit_sha="abc123", push_succeeded=True)
        assert commit_mod._commit_result_field(result, "commit_sha") == "abc123"
