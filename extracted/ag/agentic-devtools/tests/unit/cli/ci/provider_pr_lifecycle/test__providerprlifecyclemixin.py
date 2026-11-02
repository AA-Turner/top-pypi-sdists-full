"""Tests for the pr lifecycle provider capability."""

import pytest

from tests.unit.cli.ci.provider._fixtures import _ConcreteProvider


class TestProviderPrLifecycleMixin:
    """Tests for the pr lifecycle provider capability."""

    def test_approve_pr_returns_bool(self) -> None:
        provider = _ConcreteProvider()
        result = provider.approve_pr(1, "sha", "LGTM")
        assert result is True

    def test_merge_pr_returns_none(self) -> None:
        provider = _ConcreteProvider()
        provider.merge_pr(1, "sha", "squash")

    def test_list_pr_files_returns_list(self) -> None:
        provider = _ConcreteProvider()
        result = provider.list_pr_files(1)
        assert isinstance(result, list)
        assert all(isinstance(f, str) for f in result)

    def test_get_check_annotations_returns_list(self) -> None:
        provider = _ConcreteProvider()
        result = provider.get_check_annotations(1, 10)
        assert isinstance(result, list)
        assert all(isinstance(a, str) for a in result)

    def test_publish_pr_returns_none(self) -> None:
        provider = _ConcreteProvider()
        provider.publish_pr(1)

    def test_get_pr_body_default_returns_empty(self) -> None:
        assert _ConcreteProvider().get_pr_body(1) == ""

    def test_update_pr_title_default_is_unsupported(self) -> None:
        with pytest.raises(NotImplementedError, match="does not implement update_pr_title"):
            _ConcreteProvider().update_pr_title(1, "title")

    def test_list_closing_issues_default_returns_empty(self) -> None:
        assert _ConcreteProvider().list_closing_issues(1) == []

    def test_durable_claims_are_explicitly_unsupported_by_default(self) -> None:
        with pytest.raises(NotImplementedError, match="durable initial-delivery claims"):
            _ConcreteProvider()._get_initial_delivery_claims()
