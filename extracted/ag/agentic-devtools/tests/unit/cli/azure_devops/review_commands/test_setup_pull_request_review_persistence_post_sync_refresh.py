"""Tests for the review_commands module and helper functions."""

import pytest

from ._persistence_test_helpers import PersistenceTestHelpers


class TestSetupPullRequestReviewPersistence(PersistenceTestHelpers):
    def test_post_sync_metadata_exits_when_refreshed_commit_never_matches_head(self, capsys):
        """Post-sync metadata must abort when refreshed API payload never reaches local HEAD."""
        old_commit = "abcdef1234567890abcdef1234567890abcdef12"
        new_commit = "1234567890abcdef1234567890abcdef12345678"
        pr_details = self._make_pr_details()
        pr_details["pullRequest"]["lastMergeSourceCommit"] = {"commitId": old_commit}

        with pytest.raises(SystemExit):
            self._run_setup_with_post_sync_head(
                pr_details,
                new_commit,
                fetch_side_effect=[pr_details, pr_details, pr_details, pr_details],
            )

        captured = capsys.readouterr()
        assert "did not match local HEAD" in captured.err
        assert "Could not load PR details for the post-sync HEAD commit" in captured.err

    def test_post_sync_metadata_exits_when_refreshed_pr_info_is_not_a_dict(self, capsys):
        """Post-sync metadata must abort when refreshed payload lacks a dict PR object."""

        class PullRequestLike:
            def __init__(self, values):
                self.values = values

            def get(self, key, default=None):
                return self.values.get(key, default)

        old_commit = "abcdef1234567890abcdef1234567890abcdef12"
        new_commit = "1234567890abcdef1234567890abcdef12345678"
        pr_details = {
            "pullRequest": PullRequestLike(
                {
                    "pullRequestId": 123,
                    "title": "Test PR",
                    "createdBy": {"displayName": "Test User"},
                    "sourceRefName": "refs/heads/feature/test",
                    "targetRefName": "refs/heads/main",
                    "lastMergeSourceCommit": {"commitId": old_commit},
                }
            ),
            "files": [],
            "threads": [],
        }

        with pytest.raises(SystemExit):
            self._run_setup_with_post_sync_head(
                pr_details,
                new_commit,
                fetch_side_effect=[pr_details, pr_details, pr_details, pr_details],
            )

        captured = capsys.readouterr()
        assert "did not match local HEAD" in captured.err
        assert "Could not load PR details for the post-sync HEAD commit" in captured.err

    def test_post_sync_metadata_exits_when_head_is_unavailable(self, capsys):
        """Post-sync metadata aborts when local HEAD cannot be read after a rewritten push."""
        old_commit = "abcdef1234567890abcdef1234567890abcdef12"
        pr_details = self._make_pr_details()
        pr_details["pullRequest"]["lastMergeSourceCommit"] = {"commitId": old_commit}

        with pytest.raises(SystemExit):
            self._run_setup_with_post_sync_head(pr_details, None)

        assert "Could not determine the post-sync HEAD commit" in capsys.readouterr().err

    def test_post_sync_metadata_skips_write_when_commit_is_unchanged(self):
        """Post-sync metadata does not rewrite details when synchronization keeps the same commit."""
        old_commit = "abcdef1234567890abcdef1234567890abcdef12"
        pr_details = self._make_pr_details()
        pr_details["pullRequest"]["lastMergeSourceCommit"] = {"commitId": old_commit}

        _, mock_json_dump = self._run_setup_with_post_sync_head(
            pr_details,
            old_commit,
            capture_json_dump=True,
        )
        mock_json_dump.assert_not_called()

    def test_post_sync_metadata_exits_when_refreshed_payload_type_is_unexpected(self, capsys):
        """Post-sync metadata aborts when a refresh returns a non-dict payload."""
        old_commit = "abcdef1234567890abcdef1234567890abcdef12"
        new_commit = "1234567890abcdef1234567890abcdef12345678"
        pr_details = self._make_pr_details()
        pr_details["pullRequest"]["lastMergeSourceCommit"] = {"commitId": old_commit}

        with pytest.raises(SystemExit):
            self._run_setup_with_post_sync_head(
                pr_details,
                new_commit,
                fetch_side_effect=[pr_details, [], [], []],
            )

        captured = capsys.readouterr()
        assert "Refreshed PR details had unexpected type" in captured.err
        assert "Could not load PR details for the post-sync HEAD commit" in captured.err

    def test_post_sync_metadata_exits_when_refresh_read_fails(self, capsys):
        """Post-sync metadata aborts when refreshed details cannot be parsed."""
        old_commit = "abcdef1234567890abcdef1234567890abcdef12"
        new_commit = "1234567890abcdef1234567890abcdef12345678"
        pr_details = self._make_pr_details()
        pr_details["pullRequest"]["lastMergeSourceCommit"] = {"commitId": old_commit}

        with pytest.raises(SystemExit):
            self._run_setup_with_post_sync_head(
                pr_details,
                new_commit,
                fetch_side_effect=[
                    pr_details,
                    ValueError("bad payload"),
                    ValueError("bad payload"),
                    ValueError("bad payload"),
                ],
            )

        captured = capsys.readouterr()
        assert "Could not refresh PR details after sync" in captured.err
        assert "Could not load PR details for the post-sync HEAD commit" in captured.err
