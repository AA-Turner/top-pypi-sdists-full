"""A CLOUD-BROWSER SELECTOR THAT MATCHES NOTHING IS TOOL FEEDBACK, NEVER A PLATFORM ERROR (2026-11-19).

Live (guided-setup, 2026-11-16): two ``tool_execution_failed`` rows "cloud_browser
(browser_action_failed): Nothing on this page matches button:has-text("Google")." The readiness
pre-gate every element-aimed action runs (matrx_scraper ai_browser/actions.py
``_refuse_unusable_target``, verdict ``absent``) positively determined the model aimed at an element
that is not on the page, and said so in one fixed sentence; the model reads it and picks another
selector. Only that sentence from ``cloud_browser`` is spared: any other browser action failure (a
dead worker, a navigation error, a hidden element Playwright timed out on) is still filed, and the
same sentence from another tool is still filed.

SUT: the executor's real ``_is_expected_domain_failure``.
"""

from __future__ import annotations

from matrx_ai.tools.executor import _is_expected_domain_failure


def test_a_selector_that_matches_nothing_is_tool_feedback() -> None:
    assert _is_expected_domain_failure(
        tool_name="cloud_browser",
        error_type="browser_action_failed",
        message='Nothing on this page matches button:has-text("Google").',
    )


def test_any_other_browser_action_failure_is_still_filed() -> None:
    assert not _is_expected_domain_failure(
        tool_name="cloud_browser",
        error_type="browser_action_failed",
        message="Target page, context or browser has been closed",
    )


def test_the_same_sentence_from_another_tool_is_still_filed() -> None:
    assert not _is_expected_domain_failure(
        tool_name="web_search", error_type="browser_action_failed", message="Nothing on this page matches x."
    )
