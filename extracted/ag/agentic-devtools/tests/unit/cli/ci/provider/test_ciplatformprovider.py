"""Tests for CIPlatformProvider ABC."""

import pytest

from agentic_devtools.cli.ci.provider import CIPlatformProvider
from tests.unit.cli.ci.provider._fixtures import _ConcreteProvider


class TestCIPlatformProvider:
    """Tests for the CIPlatformProvider abstract base class."""

    def test_cannot_instantiate_abc(self) -> None:
        with pytest.raises(TypeError, match="abstract method"):
            CIPlatformProvider()  # type: ignore[abstract]

    def test_concrete_provider_instantiates(self) -> None:
        provider = _ConcreteProvider()
        assert isinstance(provider, CIPlatformProvider)

    def test_abstract_methods_list(self) -> None:
        """Verify all expected abstract methods are defined."""
        expected_methods = {
            "parse_event",
            "get_pr_metadata",
            "list_check_runs",
            "list_reviews",
            "post_comment",
            "update_comment",
            "find_comment",
            "approve_pr",
            "merge_pr",
            "delete_branch",
            "publish_pr",
            "squash_before_publish",
            "request_reviewer",
            "count_unresolved_review_threads",
            "list_pr_files",
            "get_check_annotations",
            "dispatch_repair",
            "list_review_comments",
            "list_issue_comments",
            "finalize_post_repair",
            "squash_post_repair",
            "list_pr_issue_events",
        }
        actual_abstracts = CIPlatformProvider.__abstractmethods__
        assert actual_abstracts == expected_methods
