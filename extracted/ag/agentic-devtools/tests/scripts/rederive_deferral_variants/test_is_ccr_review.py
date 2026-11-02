"""Tests for is_ccr_review in rederive_deferral_variants."""

from __future__ import annotations

import pytest

from tests.scripts.rederive_deferral_variants import rederive


@pytest.mark.parametrize(
    "login",
    [
        "copilot-pull-request-reviewer[bot]",
        "Copilot-Pull-Request-Reviewer[bot]",
        "copilot-pull-request-reviewer",
    ],
)
def test_accepts_the_ccr_reviewer_login(login: str) -> None:
    """The CCR reviewer is matched exactly, case-insensitively, with or without [bot]."""
    assert rederive.is_ccr_review({"user": {"login": login}}) is True


@pytest.mark.parametrize(
    "login",
    [
        "copilot-swe-agent[bot]",
        "copilot",
        "Copilot",
        "some-copilot-fan",
        "a-human",
        "",
    ],
)
def test_rejects_non_ccr_authors(login: str) -> None:
    """The cloud coding agent and any other copilot-ish login are not CCR rounds."""
    assert rederive.is_ccr_review({"user": {"login": login}}) is False


def test_tolerates_a_missing_user() -> None:
    """A review with a null user (ghost author) is not a CCR round."""
    assert rederive.is_ccr_review({"user": None}) is False
    assert rederive.is_ccr_review({}) is False
