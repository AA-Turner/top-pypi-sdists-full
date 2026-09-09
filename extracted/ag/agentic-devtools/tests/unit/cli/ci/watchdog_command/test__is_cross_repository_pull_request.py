"""Tests for _is_cross_repository_pull_request()."""

from agentic_devtools.cli.ci.watchdog_command import _is_cross_repository_pull_request


class TestIsCrossRepositoryPullRequest:
    """Cross-repository and malformed PR inventory detection."""

    def test_detects_cross_repository_edges(self) -> None:
        assert _is_cross_repository_pull_request({"base": {"repo": []}, "head": {"repo": {}}}, "o/r")
        assert _is_cross_repository_pull_request({"base": {"repo": {}}, "head": {"repo": {}}}, "o/r")
        assert _is_cross_repository_pull_request(
            {"base": {"repo": {"full_name": "o/r"}}, "head": {"repo": {"full_name": "o/fork"}}},
            "o/r",
        )
        assert not _is_cross_repository_pull_request(
            {"base": {"repo": {"full_name": "o/r"}}, "head": {"repo": {"full_name": "o/r"}}},
            "o/r",
        )

    def test_treats_missing_base_or_head_as_cross_repository(self) -> None:
        assert _is_cross_repository_pull_request({"base": None, "head": {"repo": {}}}, "o/r")
        assert _is_cross_repository_pull_request({"base": {"repo": {}}, "head": None}, "o/r")
