"""WS-7 — the pure spec, verifier, and recipe primitives, unit-level."""

from __future__ import annotations

import pytest

from matrx_scraper.ai_browser.login import (
    AWS_IAM_CONSOLE_RECIPE,
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
        PageObservation(login_form_present=False, login_form_present_before=True),
        expect=ExpectSpec(),
    )
    assert v.outcome == "authenticated"
    assert v.confidence == pytest.approx(0.2)  # weak, not certain


def test_challenge_beats_success_and_rejection():
    v = verify(
        PageObservation(present_selectors=frozenset({"#mfacode", "#err", "#acct"})),
        expect=ExpectSpec(
            challenge_selector="#mfacode",
            failure_selector="#err",
            success_selector="#acct",
        ),
    )
    assert v.outcome == "challenged"


def test_contradiction_is_unknown_with_both_sets():
    v = verify(
        PageObservation(present_selectors=frozenset({"#acct", "#err"})),
        expect=ExpectSpec(success_selector="#acct", failure_selector="#err"),
    )
    assert v.outcome == "unknown"
    assert v.contradiction is True
    assert len([s for s in v.signals if s.observed]) == 2


def test_recipe_first_and_high_confidence():
    v = verify(
        PageObservation(
            url="https://console.aws.amazon.com/home",
            present_selectors=frozenset({"[data-testid='awsc-nav-account-menu-button']"}),
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
            text_content="Your authentication information is incorrect: SECRET_ECHO",
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
