"""Tests for load_pull_request_review_config."""

from unittest.mock import patch

from agentic_devtools.cli.config.pull_request_review_config import (
    PullRequestReviewConfig,
    load_pull_request_review_config,
)

_LOAD = "agentic_devtools.cli.config.pull_request_review_config.load_project_config"


class TestLoadPullRequestReviewConfig:
    """Tests for load_pull_request_review_config."""

    def test_returns_defaults_when_key_missing(self):
        """Absent 'pullRequestReview' key yields a fully-defaulted config."""
        with patch(_LOAD, return_value={}):
            assert load_pull_request_review_config() == PullRequestReviewConfig()

    def test_returns_defaults_when_block_not_a_dict(self):
        """A non-dict 'pullRequestReview' value yields defaults (tolerant)."""
        with patch(_LOAD, return_value={"pullRequestReview": "oops"}):
            assert load_pull_request_review_config() == PullRequestReviewConfig()

    def test_parses_present_block(self):
        """A present block is parsed via from_dict."""
        with patch(
            _LOAD,
            return_value={"pullRequestReview": {"subagentMaxRetries": 9}},
        ):
            config = load_pull_request_review_config()
        assert config.subagentMaxRetries == 9

    def test_passes_git_root_through(self):
        """The git_root argument is forwarded to load_project_config."""
        with patch(_LOAD, return_value={}) as mock_load:
            load_pull_request_review_config(git_root=None)
        mock_load.assert_called_once_with(git_root=None)

    def test_defaults_round_trip_through_save_and_load(self, tmp_path):
        """Defaults written to project.json reload as an equal config (real I/O)."""
        from agentic_devtools.cli.config.project_config import save_project_config

        default = PullRequestReviewConfig()
        save_project_config({"pullRequestReview": default.to_dict()}, git_root=tmp_path)
        loaded = load_pull_request_review_config(git_root=tmp_path)
        assert loaded == default
