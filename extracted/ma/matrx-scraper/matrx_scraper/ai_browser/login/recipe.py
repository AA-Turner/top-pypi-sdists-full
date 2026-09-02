"""Per-site login recipes — the ceiling for a known site.

D-11 named AWS as the first target. A recipe is the record that turns a fragile
generic guess into a reliable login: the exact fields, the exact selectors, and
**exactly what success, failure and challenge look like on that site.** Generic
detection (verifier.py) is the FLOOR for an unknown site; a recipe is the CEILING
for a known one (D-12).

This module is the pure, package-side shape and the reconciliation logic. The
durable record is S1's ``browser.login_recipe`` (system variant, versioned, never
edited in place, proposed by Hindsight and activated by a human) — persistence and
the Hindsight proposal path live in the aidream host. A recipe carries field KEYS,
selectors, and signal descriptors ONLY; it can never hold a value, and its signals
name selectors / URL prefixes / cookie NAMES, never contents.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# What a signal looks at on the page. Every one is structural — never a value.
SignalKind = Literal[
    "selector_present",  # a CSS selector is present on the page
    "selector_absent",  # a CSS selector is gone (e.g. the login form)
    "url_prefix",  # the current URL starts with this prefix
    "cookie_present",  # a cookie with this NAME exists (never its value)
    "text_present",  # a text fragment is visible (error copy, challenge copy)
]

# Which outcome a signal argues for.
SignalDirection = Literal["authenticated", "challenged", "rejected"]


class SignalDescriptor(BaseModel):
    """One thing to look for after submit, and which verdict it argues for."""

    model_config = ConfigDict(extra="forbid")

    kind: SignalKind
    value: str = Field(min_length=1)  # a selector, url prefix, cookie NAME, or text
    direction: SignalDirection
    weight: float = Field(default=0.5, ge=0.0, le=1.0)
    label: str | None = None


class RecipeFieldMap(BaseModel):
    """One field of the recipe's login form. ``field_key`` names a vault secret;
    ``literal_key`` names an agent/recipe-supplied non-secret (e.g. region)."""

    model_config = ConfigDict(extra="forbid")

    step: int = 0
    selector: str = Field(min_length=1)
    field_key: str | None = None
    literal_key: str | None = None
    clear_first: bool = True


class LoginRecipe(BaseModel):
    """The pure shape of ``browser.login_recipe``. ``recipe_version`` is the recipe's
    own monotonic revision (the base entity's optimistic-concurrency ``version`` is a
    separate concern the host owns)."""

    model_config = ConfigDict(extra="forbid")

    recipe_id: str | None = None
    normalized_origin: str = Field(min_length=1)
    match_pattern: str | None = None
    provider_key: str | None = None
    recipe_version: int = 1
    field_map: list[RecipeFieldMap] = Field(default_factory=list)
    submit: dict = Field(default_factory=dict)
    success_signals: list[SignalDescriptor] = Field(default_factory=list)
    failure_signals: list[SignalDescriptor] = Field(default_factory=list)
    challenge_signals: list[SignalDescriptor] = Field(default_factory=list)
    notes: str | None = None
    provenance: Literal["human", "hindsight_proposal", "imported"] = "human"
    source_finding_id: str | None = None
    status: Literal["proposed", "active", "retired"] = "proposed"
    confidence_floor: float | None = Field(default=None, ge=0.0, le=1.0)

    def all_signals(self) -> list[SignalDescriptor]:
        return [*self.challenge_signals, *self.failure_signals, *self.success_signals]


# ─────────────────────────────────────────────────────────────────────────────
# AWS — the first seeded recipe (D-7 / D-11). AWS root vs IAM sign-in are DIFFERENT
# forms; this recipe targets the IAM-user console sign-in. The root form is a
# separate recipe (different origin path + fields) and is deliberately not merged.
# All field_keys are names into the vault; no value appears anywhere here.
# ─────────────────────────────────────────────────────────────────────────────

AWS_IAM_CONSOLE_RECIPE = LoginRecipe(
    normalized_origin="https://signin.aws.amazon.com",
    match_pattern="/console",
    provider_key="aws_console",
    recipe_version=1,
    field_map=[
        RecipeFieldMap(step=0, selector="#resolving_input", field_key="account_id"),
        RecipeFieldMap(step=1, selector="#username", field_key="username"),
        RecipeFieldMap(step=1, selector="#password", field_key="password"),
    ],
    success_signals=[
        SignalDescriptor(
            kind="url_prefix",
            value="https://console.aws.amazon.com/",
            direction="authenticated",
            weight=0.6,
            label="landed on the AWS console",
        ),
        SignalDescriptor(
            kind="selector_present",
            value="[data-testid='awsc-nav-account-menu-button']",
            direction="authenticated",
            weight=0.6,
            label="account menu present",
        ),
        SignalDescriptor(
            kind="cookie_present",
            value="aws-userInfo",
            direction="authenticated",
            weight=0.4,
            label="AWS session cookie set",
        ),
    ],
    failure_signals=[
        SignalDescriptor(
            kind="selector_present",
            value="#error-message",
            direction="rejected",
            weight=0.7,
            label="AWS sign-in error shown",
        ),
        SignalDescriptor(
            kind="text_present",
            value="Your authentication information is incorrect",
            direction="rejected",
            weight=0.7,
        ),
    ],
    challenge_signals=[
        SignalDescriptor(
            kind="selector_present",
            value="#mfacode",
            direction="challenged",
            weight=0.8,
            label="AWS MFA code prompt",
        ),
        SignalDescriptor(
            kind="selector_present",
            value="#captchaGuess",
            direction="challenged",
            weight=0.8,
            label="AWS CAPTCHA",
        ),
    ],
    notes=(
        "AWS IAM-user console sign-in. Root-account sign-in is a DIFFERENT form "
        "(email field, different origin path) and gets its own recipe. AWS console "
        "sessions carry a hard expiry independent of activity (D-7)."
    ),
    provenance="imported",
    status="active",
    confidence_floor=0.5,
)

SEEDED_RECIPES: tuple[LoginRecipe, ...] = (AWS_IAM_CONSOLE_RECIPE,)


def match_seeded_recipe(normalized_origin: str, path: str = "") -> LoginRecipe | None:
    """Find the active seeded recipe for an origin (+ optional path narrowing). The
    host consults the DB first; this is the offline/standalone fallback and the seed
    source for the DB."""
    for recipe in SEEDED_RECIPES:
        if recipe.status != "active":
            continue
        if recipe.normalized_origin != normalized_origin:
            continue
        if recipe.match_pattern and not path.startswith(recipe.match_pattern):
            continue
        return recipe
    return None


__all__ = [
    "AWS_IAM_CONSOLE_RECIPE",
    "LoginRecipe",
    "RecipeFieldMap",
    "SEEDED_RECIPES",
    "SignalDescriptor",
    "SignalDirection",
    "SignalKind",
    "match_seeded_recipe",
]
