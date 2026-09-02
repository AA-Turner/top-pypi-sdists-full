"""The D-12 verification engine — three outcomes plus explicit unknown, weighted
signals, a confidence value, and the signals that produced it.

> **Never a single signal, and never a binary.**

Deterministic. **No model call is in this path.** The order is exactly D-12 §7.3:

1. **Recipe first.** If a recipe supplies signals for the origin and ANY of them is
   observed, the verdict comes from the recipe signals alone, at high confidence.
2. **Generic signals otherwise.** Each observed signal contributes its weight to its
   outcome. Challenge evidence is weighed before rejection, rejection before success.
3. **Confidence** = the winning outcome's accumulated weight over the total observed
   weight, clamped to [0,1]. No signals at all → ``unknown`` at confidence 0.
4. **Contradiction is not resolved by picking the bigger number.** Success and
   rejection evidence appearing together yields ``unknown`` with BOTH signal sets
   attached — a recipe-shaped gap, exactly what Hindsight should read.

🚨 A verdict signal records the descriptor, whether it was observed, its source and
its weight — **never page content and never a value.** ``PageObservation.text_content``
is used only for substring membership of KNOWN fragments and never travels into a
verdict signal.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from .recipe import LoginRecipe, SignalDescriptor
from .spec import ExpectSpec

Outcome = Literal["authenticated", "challenged", "rejected", "unknown"]


class PageObservation(BaseModel):
    """The structural facts the verifier reads after submit. Collected by the worker
    observer — selectors present, cookie NAMES set, the current url, whether a login
    form is still on the page. ``text_content`` is a sanitized haystack used ONLY for
    membership checks of known fragments; it never enters a verdict."""

    model_config = ConfigDict(extra="forbid")

    url: str | None = None
    url_before: str | None = None
    title: str | None = None
    present_selectors: frozenset[str] = Field(default_factory=frozenset)
    cookie_names: frozenset[str] = Field(default_factory=frozenset)
    login_form_present: bool = True
    login_form_present_before: bool = True
    text_content: str | None = None
    timed_out: bool = False

    # ── The SETTLED structural probe (the strongest generic evidence we have) ──
    # ``None`` means "not probed"; a bool means the settled observation ran and
    # saw (or did not see) that control. When these are present they REPLACE the
    # coarse ``login_form_present`` signal — they are the same observation, taken
    # precisely, and counting both would double-weight one fact.
    password_field_present: bool | None = None
    otp_field_present: bool | None = None
    captcha_present: bool | None = None

    @property
    def structurally_probed(self) -> bool:
        return self.password_field_present is not None

    def signal_observed(self, descriptor: SignalDescriptor) -> bool:
        kind = descriptor.kind
        val = descriptor.value
        if kind == "selector_present":
            return val in self.present_selectors
        if kind == "selector_absent":
            return val not in self.present_selectors
        if kind == "url_prefix":
            return bool(self.url) and self.url.startswith(val)
        if kind == "cookie_present":
            return val in self.cookie_names
        if kind == "text_present":
            return bool(self.text_content) and val in self.text_content
        return False


class VerdictSignal(BaseModel):
    """One evaluated signal on the verdict — sanitized, never a value or page text."""

    model_config = ConfigDict(extra="forbid")

    signal: str  # a stable machine name, e.g. 'expected_marker_present'
    observed: bool
    source: Literal["recipe", "generic", "expect"]
    direction: Literal["authenticated", "challenged", "rejected"]
    weight: float


class Verdict(BaseModel):
    model_config = ConfigDict(extra="forbid")

    outcome: Outcome
    confidence: float = Field(ge=0.0, le=1.0)
    signals: list[VerdictSignal]
    challenge_class: str | None = None
    contradiction: bool = False
    source: Literal["recipe", "generic", "none"] = "none"
    #: The single machine name that best explains this verdict — the winning
    #: observed signal, or the ambiguity marker that stopped a decision. Stable
    #: vocabulary; safe to log, to key a recipe gap on, and to hand an agent.
    reason: str = "no_signals_observed"


def _decide(observed: list[VerdictSignal]) -> tuple[Outcome, float, bool]:
    """Combine observed signals into (outcome, confidence, contradiction).

    Precedence, per §7.3: challenge → contradiction check → rejected → authenticated.
    Confidence is the winning direction's weight over the total observed weight.
    """
    hits = [s for s in observed if s.observed]
    if not hits:
        return "unknown", 0.0, False
    by_dir: dict[str, float] = {"authenticated": 0.0, "challenged": 0.0, "rejected": 0.0}
    for s in hits:
        by_dir[s.direction] += s.weight

    # 🚨 Confidence is the WINNING direction's accumulated weight, clamped to [0,1] —
    # the ABSOLUTE strength of the evidence, NOT its share of total observed weight.
    # The share reading (§7.3's literal "over total observed weight") makes a single
    # weak signal read as certainty (0.2/0.2 = 1.0), which defeats the low-confidence
    # detection D-12 requires and D-16 item 4 depends on: a lone weight-0.2 "form gone"
    # signal is a *low*-confidence success and must present as one. Absolute winning
    # weight gives exactly that (0.2), while strong or corroborated evidence still
    # saturates toward 1.0. (Reconcile-not-contradict interpretation, recorded in the
    # WS-7 report.)

    # Challenge wins outright — a challenge page routinely removes the form and can
    # otherwise read as a partial success/failure. Conflating it is how a loop is built.
    if by_dir["challenged"] > 0:
        return "challenged", min(by_dir["challenged"], 1.0), False

    # Contradiction: success AND rejection evidence together → unknown, not the bigger.
    if by_dir["authenticated"] > 0 and by_dir["rejected"] > 0:
        return "unknown", min(by_dir["authenticated"] + by_dir["rejected"], 1.0), True

    if by_dir["rejected"] > 0:
        return "rejected", min(by_dir["rejected"], 1.0), False
    if by_dir["authenticated"] > 0:
        return "authenticated", min(by_dir["authenticated"], 1.0), False
    return "unknown", 0.0, False


def _recipe_signals(recipe: LoginRecipe, obs: PageObservation) -> list[VerdictSignal]:
    out: list[VerdictSignal] = []
    for idx, d in enumerate(recipe.all_signals()):
        out.append(
            VerdictSignal(
                signal=d.label or f"recipe:{d.kind}:{idx}",
                observed=obs.signal_observed(d),
                source="recipe",
                direction=d.direction,
                weight=d.weight,
            )
        )
    return out


# URL vocabulary for the settled structural verdict. Segments come from the
# normalized origin+path split on non-alphanumerics, so "signin" matches
# /v3/signin/ but never "designing". Lives HERE, in the one verification engine,
# because every surface that decides a login verdict needs the same vocabulary.
CHALLENGE_URL_SEGMENTS = frozenset(
    {
        "challenge",
        "mfa",
        "2fa",
        "2sv",
        "totp",
        "otp",
        "twostep",
        "2step",
        "verification",
        "verify",
        "twofactor",
        "authenticator",
        "onetimecode",
    }
)
AUTH_FLOW_URL_SEGMENTS = frozenset(
    {
        "signin",
        "login",
        "logon",
        "signon",
        "auth",
        "authorize",
        "authenticate",
        "oauth",
        "sso",
        "idp",
        "session",
        "sessions",
        "accounts",
        "identifier",
        "identity",
        "credentials",
    }
)


def url_segments(url: str | None) -> frozenset[str]:
    """Split a url into alphanumeric segments for vocabulary membership."""
    if not url:
        return frozenset()
    out: set[str] = set()
    token: list[str] = []
    for ch in url.lower():
        if ch.isalnum():
            token.append(ch)
        elif token:
            out.add("".join(token))
            token = []
    if token:
        out.add("".join(token))
    return frozenset(out)


#: The ambiguity markers — an observation that is real, is worth recording, and
#: is deliberately NOT evidence for any outcome. Their whole job is to stop a
#: success being claimed from the mere absence of a form.
AMBIGUOUS_STRUCTURAL_REASONS = (
    "password_form_on_new_page",
    "still_on_sign_in_flow",
    "form_cleared_url_unchanged",
)


def _structural_signals(obs: PageObservation) -> tuple[list[VerdictSignal], str | None]:
    """The settled-page structural evidence, in D-12 precedence order.

    Returns ``(signals, ambiguity_reason)``. Exactly one directional signal can
    be observed, because the underlying facts are mutually exclusive by
    construction; when none is, ``ambiguity_reason`` names WHY the page could not
    be read — which is an honest ``unknown``, never a success.

    🚨 This is the knowledge the production Cloud Browser path had learned and
    kept in its own private classifier. It lives here now so there is exactly ONE
    implementation of the login decision.
    """
    if not obs.structurally_probed:
        return [], None

    password = bool(obs.password_field_present)
    otp = bool(obs.otp_field_present)
    captcha = bool(obs.captcha_present)
    segments = url_segments(obs.url)
    url_unchanged = obs.url is not None and obs.url == obs.url_before

    def sig(name: str, direction: str, weight: float) -> VerdictSignal:
        return VerdictSignal(
            signal=name,
            observed=True,
            source="generic",
            direction=direction,  # type: ignore[arg-type]
            weight=weight,
        )

    if captcha:
        return [sig("anti_bot_challenge_detected", "challenged", 0.85)], None
    if otp:
        return [sig("verification_code_field_visible", "challenged", 0.85)], None
    if password:
        if url_unchanged:
            return [sig("password_form_still_visible", "rejected", 0.8)], None
        # A password box on a DIFFERENT page is not a refusal and not a success
        # (a re-auth step, a second account chooser). Say so, decide nothing.
        return [], "password_form_on_new_page"
    if segments & CHALLENGE_URL_SEGMENTS:
        return [sig("challenge_url_detected", "challenged", 0.8)], None
    if segments & AUTH_FLOW_URL_SEGMENTS:
        return [], "still_on_sign_in_flow"
    if url_unchanged:
        return [], "form_cleared_url_unchanged"
    return [sig("form_cleared_left_sign_in_flow", "authenticated", 0.75)], None


def _generic_signals(expect: ExpectSpec, obs: PageObservation) -> list[VerdictSignal]:
    out: list[VerdictSignal] = []
    # The login form is gone — weak alone (a site can swap the form for a challenge).
    # Skipped entirely once the settled structural probe ran: that probe measures
    # the same fact precisely, and counting both double-weights one observation.
    if obs.login_form_present_before and not obs.structurally_probed:
        out.append(
            VerdictSignal(
                signal="login_form_absent",
                observed=not obs.login_form_present,
                source="generic",
                direction="authenticated",
                weight=0.2,
            )
        )
    if expect.challenge_selector:
        out.append(
            VerdictSignal(
                signal="expected_challenge_present",
                observed=expect.challenge_selector in obs.present_selectors,
                source="expect",
                direction="challenged",
                weight=0.9,
            )
        )
    if expect.failure_selector:
        out.append(
            VerdictSignal(
                signal="expected_error_present",
                observed=expect.failure_selector in obs.present_selectors,
                source="expect",
                direction="rejected",
                weight=0.9,
            )
        )
    if expect.success_url_prefix:
        out.append(
            VerdictSignal(
                signal="navigated_to_expected",
                observed=bool(obs.url) and obs.url.startswith(expect.success_url_prefix),
                source="expect",
                direction="authenticated",
                weight=0.9,
            )
        )
    if expect.success_selector:
        out.append(
            VerdictSignal(
                signal="expected_marker_present",
                observed=expect.success_selector in obs.present_selectors,
                source="expect",
                direction="authenticated",
                weight=0.9,
            )
        )
    return out


#: Structural signal name → challenge class. A CAPTCHA and an MFA prompt are both
#: `challenged`, but the agent's next move differs completely (ask the human vs.
#: generate a code), so the class must survive the verdict.
_STRUCTURAL_CHALLENGE_CLASS = {
    "anti_bot_challenge_detected": "captcha",
    "verification_code_field_visible": "mfa",
    "challenge_url_detected": "mfa",
}


def _challenge_class(signals: list[VerdictSignal], recipe: LoginRecipe | None) -> str | None:
    for s in signals:
        if s.direction == "challenged" and s.observed:
            known = _STRUCTURAL_CHALLENGE_CLASS.get(s.signal)
            if known:
                return known
            label = (s.signal or "").lower()
            if "captcha" in label or "bot" in label:
                return "captcha"
            if "mfa" in label or "totp" in label or "code" in label:
                return "mfa"
            if "device" in label or "approval" in label:
                return "device_confirm"
            return "challenge"
    return None


def _winning_reason(signals: list[VerdictSignal], outcome: Outcome) -> str | None:
    """The heaviest OBSERVED signal pointing at the decided outcome."""
    hits = [x for x in signals if x.observed and x.direction == outcome]
    if not hits:
        return None
    return max(hits, key=lambda x: x.weight).signal


def verify(
    observation: PageObservation,
    *,
    expect: ExpectSpec | None = None,
    recipe: LoginRecipe | None = None,
) -> Verdict:
    """Produce the D-12 verdict for one login attempt.

    🚨 THE ONE DECISION. Every surface that must answer "did that login work?"
    calls this — the Cloud Browser server executor, the local-Chrome executor,
    and anything built next. A second classifier beside it is a defect: the
    two drift, and the documented confidence model stops describing reality.
    """
    expect = expect or ExpectSpec()

    if recipe is not None:
        recipe_signals = _recipe_signals(recipe, observation)
        if any(s.observed for s in recipe_signals):
            outcome, confidence, contradiction = _decide(recipe_signals)
            return Verdict(
                outcome=outcome,
                confidence=confidence,
                signals=recipe_signals,
                challenge_class=_challenge_class(recipe_signals, recipe),
                contradiction=contradiction,
                source="recipe",
                reason=_winning_reason(recipe_signals, outcome) or "recipe_signals_contradict",
            )

    structural, ambiguity = _structural_signals(observation)
    generic = structural + _generic_signals(expect, observation)
    outcome, confidence, contradiction = _decide(generic)

    # The caller declared what success/failure looks like here and NONE of it was
    # observed. A generic heuristic success cannot overrule that silence — the
    # agent knows this page better than the vocabulary does.
    declared = any(
        (
            expect.success_url_prefix,
            expect.success_selector,
            expect.failure_selector,
            expect.challenge_selector,
        )
    )
    expectation_hit = any(s.observed and s.source == "expect" for s in generic)
    if declared and not expectation_hit and outcome == "authenticated":
        outcome, confidence, contradiction = "unknown", 0.0, False
        ambiguity = "explicit_expectation_not_met"

    if outcome == "unknown":
        reason = "signals_contradict" if contradiction else (ambiguity or "no_signals_observed")
    else:
        reason = _winning_reason(generic, outcome) or "no_signals_observed"

    # An attempt that produced nothing observable is unknown — never authenticated
    # just because nothing went wrong.
    return Verdict(
        outcome=outcome,
        confidence=confidence,
        signals=generic,
        challenge_class=_challenge_class(generic, None),
        contradiction=contradiction,
        source="generic" if generic else "none",
        reason=reason,
    )


__all__ = [
    "AMBIGUOUS_STRUCTURAL_REASONS",
    "AUTH_FLOW_URL_SEGMENTS",
    "CHALLENGE_URL_SEGMENTS",
    "Outcome",
    "PageObservation",
    "Verdict",
    "VerdictSignal",
    "url_segments",
    "verify",
]
