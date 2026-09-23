"""Value-free receipt regressions for the one canonical login verdict engine."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from matrx_scraper.ai_browser.login import (
    EvaluatedObservation,
    ExpectSpec,
    LoginRecipe,
    PageObservation,
    SignalDescriptor,
    verify,
    verify_evaluated,
)


def _same_verdict(remote, evaluated, *, expect=None, recipe=None):
    raw = verify(remote, expect=expect, recipe=recipe)
    receipt = verify_evaluated(evaluated, expect=expect, recipe=recipe)
    assert receipt.model_dump() == raw.model_dump()


def test_evaluated_receipts_match_remote_for_generic_challenge_and_contradiction():
    expect = ExpectSpec(challenge_selector="#mfa", success_selector="#account", failure_selector="#error")
    _same_verdict(
        PageObservation(present_selectors=frozenset({"#mfa"}), selector_probe_known=True),
        EvaluatedObservation(challenge_selector=True),
        expect=expect,
    )
    _same_verdict(
        PageObservation(
            present_selectors=frozenset({"#account", "#error"}), selector_probe_known=True
        ),
        EvaluatedObservation(success_selector=True, failure_selector=True),
        expect=expect,
    )


def test_evaluated_receipt_matches_remote_for_unmet_expectation_and_recipe_precedence():
    expect = ExpectSpec(success_selector="#account")
    _same_verdict(
        PageObservation(
            password_field_present=False,
            otp_field_present=False,
            captcha_present=False,
            url_before="https://id.test/signin",
            url="https://app.test/home",
            url_probe_known=True,
            selector_probe_known=True,
        ),
        EvaluatedObservation(
            password_field_present_after=False,
            otp_field_present_after=False,
            captcha_present_after=False,
            url_relation="changed",
            url_flow="other",
        ),
        expect=expect,
    )

    recipe = LoginRecipe(
        normalized_origin="https://id.test",
        success_signals=[
            SignalDescriptor(
                kind="selector_present",
                value="#account",
                direction="authenticated",
                weight=0.6,
            )
        ],
    )
    _same_verdict(
        PageObservation(present_selectors=frozenset({"#account"}), selector_probe_known=True),
        EvaluatedObservation(recipe_matches=(True,)),
        recipe=recipe,
    )


def test_missing_structural_fact_cannot_turn_navigation_into_success():
    verdict = verify_evaluated(
        EvaluatedObservation(
            password_field_present_after=False,
            otp_field_present_after=None,
            captcha_present_after=False,
            url_relation="changed",
            url_flow="other",
        )
    )
    assert (verdict.outcome, verdict.confidence) == ("unknown", 0.0)


def test_unknown_url_never_implies_form_cleared_navigation_success():
    verdict = verify_evaluated(
        EvaluatedObservation(
            password_field_present_after=False,
            otp_field_present_after=False,
            captcha_present_after=False,
        )
    )
    assert verdict.outcome == "unknown"

    remote = verify(PageObservation(login_form_present=False, login_form_present_before=True))
    assert remote.outcome == "unknown"


def test_evaluated_receipt_rejects_extra_data_undeclared_hits_and_wrong_recipe_vector():
    with pytest.raises(ValidationError):
        EvaluatedObservation(password_field_present_after=False, raw_url="https://secret.test")

    with pytest.raises(ValueError, match="undeclared"):
        verify_evaluated(EvaluatedObservation(success_selector=True))

    recipe = LoginRecipe(
        normalized_origin="https://id.test",
        success_signals=[
            SignalDescriptor(
                kind="selector_absent",
                value="#login",
                direction="authenticated",
            )
        ],
    )
    with pytest.raises(ValueError, match="exactly match"):
        verify_evaluated(EvaluatedObservation(), recipe=recipe)


def test_unknown_recipe_match_generates_no_signal_for_selector_absent():
    recipe = LoginRecipe(
        normalized_origin="https://id.test",
        success_signals=[
            SignalDescriptor(
                kind="selector_absent",
                value="#login",
                direction="authenticated",
            )
        ],
    )
    verdict = verify_evaluated(EvaluatedObservation(recipe_matches=(None,)), recipe=recipe)
    assert (verdict.outcome, verdict.confidence) == ("unknown", 0.0)


def test_default_page_observation_cannot_make_selector_absent_recipe_authenticated():
    recipe = LoginRecipe(
        normalized_origin="https://portal.example.test",
        success_signals=[
            SignalDescriptor(
                kind="selector_absent",
                value="form#staff-login",
                direction="authenticated",
            )
        ],
    )
    assert verify(PageObservation(), recipe=recipe).outcome == "unknown"


def test_known_empty_page_observation_keeps_selector_absent_recipe_authenticated():
    recipe = LoginRecipe(
        normalized_origin="https://portal.example.test",
        success_signals=[
            SignalDescriptor(
                kind="selector_absent",
                value="form#staff-login",
                direction="authenticated",
            )
        ],
    )
    verdict = verify(PageObservation(selector_probe_known=True), recipe=recipe)
    assert verdict.outcome == "authenticated"


def test_unknown_raw_descriptor_channels_generate_no_recipe_signal():
    recipe = LoginRecipe(
        normalized_origin="https://portal.example.test",
        success_signals=[
            SignalDescriptor(
                kind="url_prefix",
                value="https://portal.example.test/home",
                direction="authenticated",
            ),
            SignalDescriptor(
                kind="cookie_present",
                value="session",
                direction="authenticated",
            ),
            SignalDescriptor(
                kind="text_present",
                value="Welcome back",
                direction="authenticated",
            ),
        ],
    )
    verdict = verify(
        PageObservation(
            url="https://portal.example.test/home",
            url_probe_known=False,
            cookie_names=frozenset({"session"}),
            cookie_probe_known=False,
            text_content="Welcome back",
            text_probe_known=False,
        ),
        recipe=recipe,
    )
    assert verdict.outcome == "unknown"


def test_timed_out_selector_probe_cannot_create_selector_absent_recipe_signal():
    recipe = LoginRecipe(
        normalized_origin="https://portal.example.test",
        success_signals=[
            SignalDescriptor(
                kind="selector_absent",
                value="form#staff-login",
                direction="authenticated",
            )
        ],
    )
    verdict = verify(
        PageObservation(
            url="https://portal.example.test/home",
            url_before="https://portal.example.test/signin",
            present_selectors=frozenset(),
            timed_out=True,
            password_field_present=False,
            otp_field_present=False,
            captcha_present=False,
        ),
        recipe=recipe,
    )
    assert verdict.outcome == "unknown"
