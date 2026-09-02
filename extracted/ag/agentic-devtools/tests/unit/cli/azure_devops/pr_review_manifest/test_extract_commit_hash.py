"""Tests for extract_commit_hash."""

from agentic_devtools.cli.azure_devops.pr_review_manifest import extract_commit_hash


class TestExtractCommitHash:
    def test_from_pull_request_subkey(self):
        details = {"pullRequest": {"lastMergeSourceCommit": {"commitId": "  abc123  "}}}
        assert extract_commit_hash(details) == "abc123"

    def test_from_flat_details(self):
        details = {"lastMergeSourceCommit": {"commitId": "def456"}}
        assert extract_commit_hash(details) == "def456"

    def test_last_merge_not_dict(self):
        assert extract_commit_hash({"lastMergeSourceCommit": None}) == ""

    def test_commit_id_non_string(self):
        assert extract_commit_hash({"lastMergeSourceCommit": {"commitId": 123}}) == ""

    def test_missing(self):
        assert extract_commit_hash({}) == ""
