"""Tests for load_triage_config."""

from unittest.mock import patch

from agentic_devtools.cli.azure_devops.pr_review_triage import load_triage_config

_MODULE = "agentic_devtools.cli.azure_devops.pr_review_triage"


class TestLoadTriageConfig:
    def test_defaults_when_no_config(self):
        with patch(f"{_MODULE}.load_repo_config", return_value={}):
            config = load_triage_config(None)
        assert config["enabled"] is True
        assert config["defaultDepth"] == "deep"
        assert config["minDiffLinesForDeep"] == 20
        assert config["maxDeepModelCalls"] == 30

    def test_pull_request_review_not_dict(self):
        with patch(f"{_MODULE}.load_repo_config", return_value={"pullRequestReview": "x"}):
            config = load_triage_config("/repo")
        assert config["minDiffLinesForDeep"] == 20

    def test_triage_not_dict(self):
        with patch(f"{_MODULE}.load_repo_config", return_value={"pullRequestReview": {"triage": "x"}}):
            config = load_triage_config("/repo")
        assert config["maxDeepModelCalls"] == 30

    def test_valid_overrides_applied(self):
        repo_config = {
            "pullRequestReview": {
                "triage": {
                    "defaultDepth": "light",
                    "minDiffLinesForDeep": 50,
                    "deepGlobs": ["**/x/**"],
                    "enabled": False,
                }
            }
        }
        with patch(f"{_MODULE}.load_repo_config", return_value=repo_config):
            config = load_triage_config("/repo")
        assert config["defaultDepth"] == "light"
        assert config["minDiffLinesForDeep"] == 50
        assert config["deepGlobs"] == ["**/x/**"]
        assert config["enabled"] is False

    def test_invalid_type_override_ignored(self):
        repo_config = {"pullRequestReview": {"triage": {"minDiffLinesForDeep": "big"}}}
        with patch(f"{_MODULE}.load_repo_config", return_value=repo_config):
            config = load_triage_config("/repo")
        assert config["minDiffLinesForDeep"] == 20

    def test_invalid_default_depth_falls_back(self):
        repo_config = {"pullRequestReview": {"triage": {"defaultDepth": "medium"}}}
        with patch(f"{_MODULE}.load_repo_config", return_value=repo_config):
            config = load_triage_config("/repo")
        assert config["defaultDepth"] == "deep"

    def test_boolean_rejected_for_integer_threshold(self):
        # bool is a subclass of int — True/False must not silently coerce to 1/0.
        repo_config = {"pullRequestReview": {"triage": {"minDiffLinesForDeep": True, "maxDeepModelCalls": False}}}
        with patch(f"{_MODULE}.load_repo_config", return_value=repo_config):
            config = load_triage_config("/repo")
        assert config["minDiffLinesForDeep"] == 20
        assert config["maxDeepModelCalls"] == 30
