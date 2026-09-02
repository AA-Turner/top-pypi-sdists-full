"""Tests for derive_commit_hash_short function."""

import json
from unittest.mock import patch

from agentic_devtools.cli.azure_devops import review_state as rs_module
from agentic_devtools.cli.azure_devops.review_state import derive_commit_hash_short


def _minimal_state_data(pr_id: int = 25365) -> dict:
    return {
        "prId": pr_id,
        "repoId": "repo-guid",
        "repoName": "example-repo-name",
        "project": "ExampleProject",
        "organization": "https://dev.azure.com/example-org",
        "latestIterationId": 5,
        "scaffoldedUtc": "2026-02-25T10:00:00Z",
        "overallSummary": {"threadId": 161000, "commentId": 1771800000, "status": "unreviewed"},
        "folders": {},
        "files": {},
        "commitHash": "abc1234def567890",
    }


class TestDeriveCommitHashShort:
    """Tests for derive_commit_hash_short."""

    def test_returns_short_hash_when_review_state_exists(self, tmp_path):
        """Derives the first 12 characters of commitHash from review-state.json."""
        pr_id = 25553
        data = _minimal_state_data(pr_id)
        data["commitHash"] = "2fea8cdf46c8abcdef0123456789"
        state_dir = tmp_path / "reviews"
        state_dir.mkdir(parents=True)
        (state_dir / "review-state.json").write_text(json.dumps(data), encoding="utf-8")

        with patch.object(rs_module, "get_state_dir", return_value=tmp_path):
            result = derive_commit_hash_short(pr_id)

        assert result == "2fea8cdf46c8"

    def test_returns_empty_when_review_state_missing(self, tmp_path):
        """Returns empty string when review-state.json does not exist (FileNotFoundError)."""
        with patch.object(rs_module, "get_state_dir", return_value=tmp_path):
            result = derive_commit_hash_short(99999)

        assert result == ""

    def test_returns_empty_when_pr_id_mismatch(self, tmp_path):
        """Returns empty string when the local file belongs to a different PR."""
        stored_pr_id = 1
        requested_pr_id = 2
        data = _minimal_state_data(stored_pr_id)
        state_dir = tmp_path / "reviews"
        state_dir.mkdir(parents=True)
        (state_dir / "review-state.json").write_text(json.dumps(data), encoding="utf-8")

        with patch.object(rs_module, "get_state_dir", return_value=tmp_path):
            result = derive_commit_hash_short(requested_pr_id)

        assert result == ""

    def test_returns_empty_when_pr_id_is_boolean(self, tmp_path):
        """Boolean prId in JSON must not be treated as numeric PR ownership."""
        requested_pr_id = 1
        data = _minimal_state_data(requested_pr_id)
        data["prId"] = True
        state_dir = tmp_path / "reviews"
        state_dir.mkdir(parents=True)
        (state_dir / "review-state.json").write_text(json.dumps(data), encoding="utf-8")

        with patch.object(rs_module, "get_state_dir", return_value=tmp_path):
            result = derive_commit_hash_short(requested_pr_id)

        assert result == ""

    def test_returns_empty_when_pr_id_is_float(self, tmp_path):
        """Float prId in JSON must not be treated as numeric PR ownership."""
        requested_pr_id = 7
        data = _minimal_state_data(requested_pr_id)
        data["prId"] = 7.0
        state_dir = tmp_path / "reviews"
        state_dir.mkdir(parents=True)
        (state_dir / "review-state.json").write_text(json.dumps(data), encoding="utf-8")

        with patch.object(rs_module, "get_state_dir", return_value=tmp_path):
            result = derive_commit_hash_short(requested_pr_id)

        assert result == ""

    def test_returns_empty_when_commit_hash_absent(self, tmp_path):
        """Returns empty string when the stored review state has no commitHash."""
        pr_id = 5
        data = _minimal_state_data(pr_id)
        del data["commitHash"]
        state_dir = tmp_path / "reviews"
        state_dir.mkdir(parents=True)
        (state_dir / "review-state.json").write_text(json.dumps(data), encoding="utf-8")

        with patch.object(rs_module, "get_state_dir", return_value=tmp_path):
            result = derive_commit_hash_short(pr_id)

        assert result == ""

    def test_returns_empty_when_commit_hash_is_empty_string(self, tmp_path):
        """An empty (but present) commitHash yields an empty short hash rather than raising."""
        pr_id = 6
        data = _minimal_state_data(pr_id)
        data["commitHash"] = ""
        state_dir = tmp_path / "reviews"
        state_dir.mkdir(parents=True)
        (state_dir / "review-state.json").write_text(json.dumps(data), encoding="utf-8")

        with patch.object(rs_module, "get_state_dir", return_value=tmp_path):
            result = derive_commit_hash_short(pr_id)

        assert result == ""

    def test_returns_empty_when_derived_segment_unsafe(self, tmp_path):
        """Returns empty string when the derived segment would be an unsafe path segment."""
        pr_id = 7
        data = _minimal_state_data(pr_id)
        data["commitHash"] = "../evil12345678"
        state_dir = tmp_path / "reviews"
        state_dir.mkdir(parents=True)
        (state_dir / "review-state.json").write_text(json.dumps(data), encoding="utf-8")

        with patch.object(rs_module, "get_state_dir", return_value=tmp_path):
            result = derive_commit_hash_short(pr_id)

        assert result == ""

    def test_returns_empty_when_state_file_malformed_json(self, tmp_path):
        """Returns empty string (rather than raising) when review-state.json is not valid JSON."""
        pr_id = 8
        state_dir = tmp_path / "reviews"
        state_dir.mkdir(parents=True)
        (state_dir / "review-state.json").write_text("not json", encoding="utf-8")

        with patch.object(rs_module, "get_state_dir", return_value=tmp_path):
            result = derive_commit_hash_short(pr_id)

        assert result == ""

    def test_returns_empty_when_state_file_contains_non_dict_json(self, tmp_path):
        """Returns empty string when review-state.json contains valid JSON that is not a dict."""
        pr_id = 8
        state_dir = tmp_path / "reviews"
        state_dir.mkdir(parents=True)
        (state_dir / "review-state.json").write_text("[1, 2, 3]", encoding="utf-8")

        with patch.object(rs_module, "get_state_dir", return_value=tmp_path):
            result = derive_commit_hash_short(pr_id)

        assert result == ""

    def test_returns_empty_when_commit_hash_is_non_string(self, tmp_path):
        """Returns empty string (not AttributeError) when commitHash is a non-string JSON value."""
        pr_id = 9
        data = _minimal_state_data(pr_id)
        data["commitHash"] = 123
        state_dir = tmp_path / "reviews"
        state_dir.mkdir(parents=True)
        (state_dir / "review-state.json").write_text(json.dumps(data), encoding="utf-8")

        with patch.object(rs_module, "get_state_dir", return_value=tmp_path):
            result = derive_commit_hash_short(pr_id)

        assert result == ""

    def test_returns_empty_when_commit_hash_prefix_is_not_hex(self, tmp_path):
        """Returns empty string when the derived prefix is path-safe but not a commit hash."""
        pr_id = 10
        data = _minimal_state_data(pr_id)
        data["commitHash"] = "not-a-hash-value"
        state_dir = tmp_path / "reviews"
        state_dir.mkdir(parents=True)
        (state_dir / "review-state.json").write_text(json.dumps(data), encoding="utf-8")

        with patch.object(rs_module, "get_state_dir", return_value=tmp_path):
            result = derive_commit_hash_short(pr_id)

        assert result == ""

    def test_returns_hash_despite_malformed_overall_summary(self, tmp_path):
        """Derives commit hash even when overallSummary has an unexpected shape.

        The new implementation reads commitHash directly from JSON without
        deserialising the full ReviewState object, so sibling field anomalies
        do not affect the result.
        """
        pr_id = 11
        data = _minimal_state_data(pr_id)
        data["overallSummary"] = None
        state_dir = tmp_path / "reviews"
        state_dir.mkdir(parents=True)
        (state_dir / "review-state.json").write_text(json.dumps(data), encoding="utf-8")

        with patch.object(rs_module, "get_state_dir", return_value=tmp_path):
            result = derive_commit_hash_short(pr_id)

        assert result == "abc1234def56"

    def test_returns_hash_despite_malformed_folders(self, tmp_path):
        """Derives commit hash even when the folders field has an unexpected shape.

        The new implementation reads commitHash directly from JSON without
        deserialising the full ReviewState object, so sibling field anomalies
        do not affect the result.
        """
        pr_id = 12
        data = _minimal_state_data(pr_id)
        data["folders"] = {"src": {"files": [123]}}
        state_dir = tmp_path / "reviews"
        state_dir.mkdir(parents=True)
        (state_dir / "review-state.json").write_text(json.dumps(data), encoding="utf-8")

        with patch.object(rs_module, "get_state_dir", return_value=tmp_path):
            result = derive_commit_hash_short(pr_id)

        assert result == "abc1234def56"

    def test_does_not_fall_back_to_branch(self, tmp_path):
        """Never attempts the -agdt branch fallback (stays a fast, local-only read)."""
        with (
            patch.object(rs_module, "get_state_dir", return_value=tmp_path),
            patch.object(rs_module, "_load_from_branch") as mock_branch,
        ):
            result = derive_commit_hash_short(123)

        mock_branch.assert_not_called()
        assert result == ""
