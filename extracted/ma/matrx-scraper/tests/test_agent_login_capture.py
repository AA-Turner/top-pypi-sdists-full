"""P2-B — on-the-fly credential capture: the pure branch + proposal + no-value
guarantees, unit-level (no DB, no worker)."""

from __future__ import annotations

import asyncio
import json

import pytest

from matrx_scraper.ai_browser.login.capture import (
    CaptureFieldSpec,
    CredentialCaptureSpec,
    DocumentedRecipeSpec,
    build_proposed_recipe,
    resolve_capture_context,
)
from matrx_scraper.ai_browser.login.recipe import (
    AWS_IAM_CONSOLE_RECIPE,
    RecipeFieldMap,
    SignalDescriptor,
)


def _spec() -> CredentialCaptureSpec:
    return CredentialCaptureSpec(
        display_name="Acme Admin — personal",
        normalized_origin="https://admin.acme.test",
        login_url="https://admin.acme.test/login",
        description="Acme back office",
        fields=[
            CaptureFieldSpec(field_key="username", selector="#u", label="Email", secret=False),
            CaptureFieldSpec(field_key="password", selector="#p", label="Password", secret=True),
        ],
        submit_selector="#go",
    )


# ── the spec never carries a value ───────────────────────────────────────────


def test_capture_spec_has_no_value_field():
    spec = _spec()
    # extra=forbid on the models means a value key would raise; assert the field
    # set is names/selectors only.
    for f in spec.fields:
        assert set(f.model_dump().keys()) == {
            "field_key",
            "selector",
            "label",
            "secret",
            "step",
            "clear_first",
        }
    dumped = json.dumps(spec.model_dump())
    assert "value" not in dumped  # no value key anywhere in the agent-supplied spec


def test_field_specs_reject_a_value_key():
    with pytest.raises(Exception):
        CaptureFieldSpec(field_key="password", selector="#p", value="hunter2")  # type: ignore[call-arg]


def test_secret_and_nonsecret_keys():
    spec = _spec()
    assert spec.field_keys == ["username", "password"]
    assert spec.secret_field_keys == ["password"]


# ── the known/unknown branch ─────────────────────────────────────────────────


def test_unknown_branch_when_no_recipe():
    ctx = asyncio.run(resolve_capture_context("https://admin.acme.test", "/login", store=None))
    assert ctx.branch == "unknown"
    assert ctx.recipe is None
    assert "propose_recipe" in ctx.guidance or "document" in ctx.guidance.lower()


def test_known_branch_uses_seeded_recipe():
    origin = AWS_IAM_CONSOLE_RECIPE.normalized_origin
    ctx = asyncio.run(resolve_capture_context(origin, "/console", store=None))
    assert ctx.branch == "known"
    assert ctx.recipe is not None
    assert ctx.recipe.normalized_origin == origin
    # A recipe carries field KEYS + selectors, never a value.
    dumped = json.dumps(ctx.recipe.model_dump())
    assert "password" in dumped  # the KEY name is fine
    for fm in ctx.recipe.field_map:
        assert fm.field_key is not None
        assert not hasattr(fm, "value")


# ── proposed recipe is always proposed + human provenance, never a value ─────


def test_build_proposed_recipe_is_proposed_and_human():
    documented = DocumentedRecipeSpec(
        normalized_origin="https://admin.acme.test",
        provider_key="acme",
        field_map=[
            RecipeFieldMap(step=0, selector="#u", field_key="username"),
            RecipeFieldMap(step=0, selector="#p", field_key="password"),
        ],
        submit={"kind": "click", "selector": "#go"},
        success_signals=[
            SignalDescriptor(kind="selector_absent", value="#p", direction="authenticated")
        ],
        failure_signals=[
            SignalDescriptor(kind="selector_present", value=".error", direction="rejected")
        ],
        notes="single-step form",
    )
    recipe = build_proposed_recipe(documented)
    assert recipe.status == "proposed"  # never auto-active
    assert recipe.provenance == "human"  # the human typed the credential
    assert [m.field_key for m in recipe.field_map] == ["username", "password"]
    assert recipe.submit == {"kind": "click", "selector": "#go"}
    dumped = json.dumps(recipe.model_dump())
    for banned in ("hunter2", "secretvalue"):
        assert banned not in dumped
