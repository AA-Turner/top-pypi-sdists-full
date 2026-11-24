"""A password form still up with its submit control DISABLED is a pending submit, never a refusal.

Namecheap 2026-10-30 (feedback 06d68845, fb062f51): after submit the visible form stayed up with
submit disabled and no provider error; the verifier answered credentials_rejected
(password_form_still_visible), telling the agent a saved credential was wrong when the site had
simply not answered yet. A re-enabled submit with the form still up is still a refusal.
"""

from __future__ import annotations

from matrx_scraper.ai_browser.login.verifier import (
    AMBIGUOUS_STRUCTURAL_REASONS,
    FIXED_VERDICT_REASONS,
    PageObservation,
    verify,
)


def _form_still_up(*, submit_disabled: bool | None) -> PageObservation:
    return PageObservation(
        url="https://www.namecheap.com/myaccount/login/",
        url_before="https://www.namecheap.com/myaccount/login/",
        url_probe_known=True,
        selector_probe_known=True,
        login_form_present=True,
        login_form_present_before=True,
        password_field_present=True,
        otp_field_present=False,
        captcha_present=False,
        submit_disabled_after_submit=submit_disabled,
    )


def test_a_disabled_submit_is_unknown_never_rejected() -> None:
    verdict = verify(_form_still_up(submit_disabled=True))
    assert verdict.outcome == "unknown"
    assert verdict.reason == "submit_still_pending"
    assert "submit_still_pending" in AMBIGUOUS_STRUCTURAL_REASONS
    assert "submit_still_pending" in FIXED_VERDICT_REASONS


def test_an_enabled_submit_with_the_form_up_is_still_a_refusal() -> None:
    for probed in (False, None):
        verdict = verify(_form_still_up(submit_disabled=probed))
        assert verdict.outcome == "rejected"
        assert verdict.reason == "password_form_still_visible"
