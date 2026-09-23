"""WS-7 — the pure spec, verifier, and recipe primitives, unit-level."""

from __future__ import annotations

import pytest

from matrx_scraper.ai_browser.login import (
    AWS_IAM_CONSOLE_RECIPE,
    FIXED_VERDICT_REASONS,
    GENERIC_STRUCTURAL_SIGNALS,
    AttemptSpec,
    ExpectSpec,
    FieldSpec,
    HOW_TO_REPORT,
    LeakReport,
    PageObservation,
    SubmitSpec,
    match_seeded_recipe,
    verify,
)


# ── spec validation ─────────────────────────────────────────────────────────


def test_field_needs_exactly_one_source():
    with pytest.raises(ValueError):
        FieldSpec(selector="#u", field_key="username", literal="x")
    with pytest.raises(ValueError):
        FieldSpec(selector="#u")


def test_fields_xor_steps_and_submit_required():
    with pytest.raises(ValueError):
        # single-step with no submit
        AttemptSpec(fields=[FieldSpec(selector="#u", field_key="username")])
    with pytest.raises(ValueError):
        AttemptSpec()  # no fields, no steps


def test_field_keys_exclude_literals_and_sort():
    spec = AttemptSpec(
        fields=[
            FieldSpec(selector="#p", field_key="password"),
            FieldSpec(selector="#u", field_key="username"),
            FieldSpec(selector="#r", literal="us-west-1"),
        ],
        submit=SubmitSpec(kind="none"),
    )
    assert spec.field_keys == ["password", "username"]


def test_extra_keys_forbidden():
    with pytest.raises(ValueError):
        FieldSpec(selector="#u", field_key="username", nonsense=True)  # type: ignore[call-arg]


# ── verifier ────────────────────────────────────────────────────────────────


def test_no_signals_is_unknown_at_zero_never_authenticated():
    v = verify(PageObservation(login_form_present=True), expect=ExpectSpec())
    assert v.outcome == "unknown"
    assert v.confidence == 0.0


def test_lone_weak_signal_is_low_confidence_success():
    v = verify(
        PageObservation(
            login_form_present=False,
            login_form_present_before=True,
            url_before="https://id.test/signin",
            url="https://app.test/home",
            url_probe_known=True,
            selector_probe_known=True,
        ),
        expect=ExpectSpec(),
    )
    assert v.outcome == "authenticated"
    assert v.confidence == pytest.approx(0.2)  # weak, not certain


# ── the coarse "form gone" observation: weak success, never a silent unknown ──
# RED-then-GREEN against the shipped rule: with `_structural_signals` emitting the
# success signal only on a full settled probe, the first test below returns
# `unknown` and this block fails 1 of 4.


def _coarse(**overrides):
    """A page observed only coarsely: the form went present → absent and the url
    left the sign-in flow. No password/otp/captcha probe ever ran."""
    base = dict(
        login_form_present=False,
        login_form_present_before=True,
        url_before="https://id.test/signin",
        url="https://app.test/home",
        url_probe_known=True,
        selector_probe_known=True,
    )
    base.update(overrides)
    return PageObservation(**base)


def test_coarse_success_says_in_its_name_that_it_was_not_probed():
    v = verify(_coarse(), expect=ExpectSpec())
    assert v.outcome == "authenticated"
    assert v.reason == "form_cleared_left_sign_in_flow_unprobed"
    assert [s.signal for s in v.signals if s.observed] == [
        "form_cleared_left_sign_in_flow_unprobed"
    ]


def test_the_settled_probe_still_outranks_the_coarse_one_and_is_never_doubled():
    v = verify(
        _coarse(password_field_present=False, otp_field_present=False, captcha_present=False),
        expect=ExpectSpec(),
    )
    assert v.outcome == "authenticated"
    assert v.confidence == pytest.approx(0.75)
    assert [s.signal for s in v.signals if s.observed] == ["form_cleared_left_sign_in_flow"]


def test_a_cleared_form_at_the_same_url_is_still_unknown_not_a_coarse_success():
    """The SPA shape Lane AK closed: no url change is positive evidence of nothing,
    and the coarse signal must not smuggle a success in behind it."""
    v = verify(
        _coarse(url_before="https://app.test/gateway", url="https://app.test/gateway"),
        expect=ExpectSpec(),
    )
    assert v.outcome == "unknown"
    assert v.reason == "form_cleared_url_unchanged"


def test_an_unreadable_probe_is_never_a_coarse_success():
    """selector_probe_known=False is transport failure, not an absent form."""
    v = verify(_coarse(selector_probe_known=False), expect=ExpectSpec())
    assert v.outcome == "unknown"
    assert v.confidence == 0.0


def test_a_form_that_was_never_there_is_not_a_transition():
    v = verify(_coarse(login_form_present_before=False), expect=ExpectSpec())
    assert v.outcome == "unknown"


def test_every_structural_signal_weight_is_declared_exactly_once():
    """The vocabulary hosts bind to cannot carry a name twice or drift in weight."""
    names = [name for name, _d, _w in GENERIC_STRUCTURAL_SIGNALS]
    assert len(names) == len(set(names))
    assert set(names) <= FIXED_VERDICT_REASONS


def test_challenge_beats_success_and_rejection():
    v = verify(
        PageObservation(
            present_selectors=frozenset({"#mfacode", "#err", "#acct"}),
            selector_probe_known=True,
        ),
        expect=ExpectSpec(
            challenge_selector="#mfacode",
            failure_selector="#err",
            success_selector="#acct",
        ),
    )
    assert v.outcome == "challenged"


def test_contradiction_is_unknown_with_both_sets():
    v = verify(
        PageObservation(present_selectors=frozenset({"#acct", "#err"}), selector_probe_known=True),
        expect=ExpectSpec(success_selector="#acct", failure_selector="#err"),
    )
    assert v.outcome == "unknown"
    assert v.contradiction is True
    assert len([s for s in v.signals if s.observed]) == 2


def test_recipe_first_and_high_confidence():
    v = verify(
        PageObservation(
            url="https://console.aws.amazon.com/home",
            url_probe_known=True,
            present_selectors=frozenset({"[data-testid='awsc-nav-account-menu-button']"}),
            selector_probe_known=True,
        ),
        recipe=AWS_IAM_CONSOLE_RECIPE,
    )
    assert v.outcome == "authenticated"
    assert v.source == "recipe"
    assert v.confidence >= 0.5


def test_verdict_signals_carry_no_page_text():
    v = verify(
        PageObservation(
            present_selectors=frozenset({"#error-message"}),
            selector_probe_known=True,
            text_content="Your authentication information is incorrect: SECRET_ECHO",
            text_probe_known=True,
        ),
        recipe=AWS_IAM_CONSOLE_RECIPE,
    )
    for s in v.signals:
        assert "SECRET_ECHO" not in s.model_dump_json()


# ── recipe ──────────────────────────────────────────────────────────────────


def test_aws_recipe_matches_by_origin_and_path():
    assert match_seeded_recipe("https://signin.aws.amazon.com", "/console/home") is not None
    assert match_seeded_recipe("https://signin.aws.amazon.com", "/other") is None
    assert match_seeded_recipe("https://evil.example.com", "/console") is None


def test_recipe_field_map_is_names_only():
    for row in AWS_IAM_CONSOLE_RECIPE.field_map:
        assert row.field_key  # a name, never a value


# ── leak report ─────────────────────────────────────────────────────────────


def test_how_to_report_present_and_names_no_value():
    r = LeakReport(kind="secret_exposed", where="after-screenshot", description="unmasked")
    assert "action:'report'" in HOW_TO_REPORT
    assert r.kind == "secret_exposed"
