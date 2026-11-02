"""Tests for _promote_findings."""

from agentic_devtools.cli.ci.models import ReviewInfo
from agentic_devtools.cli.ci.pipeline.snapshot_builder import _promote_findings
from tests.unit.cli.ci.pipeline._snapshot_fixtures import _PromotionProvider


def test_disabled_promotion_is_a_noop() -> None:
    """Disabled promotion does not call the provider."""
    provider = _PromotionProvider()

    assert _promote_findings(provider, 7, "head", "base", [], False) == ""
    assert provider.__dict__.get("promotion_calls", []) == []


def test_supported_promotion_receives_snapshot_provenance() -> None:
    """The provider receives the PR, both SHAs, and the review inventory."""
    provider = _PromotionProvider()
    reviews = [ReviewInfo(id=1, user="Copilot", state="COMMENTED")]

    assert _promote_findings(provider, 7, "head", "base", reviews, True) == ""
    assert provider.promotion_calls == [{"pr_number": 7, "commit_sha": "head", "base_sha": "base", "reviews": reviews}]


def test_promotion_error_is_returned_for_fail_closed_gate() -> None:
    """Ordinary promotion errors are summarized for the gate caller."""
    provider = _PromotionProvider()
    provider.promotion_error = "promotion unavailable"

    result = _promote_findings(provider, 7, "head", "base", [], True)

    assert result == "promotion unavailable"
