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

from pydantic import BaseModel, ConfigDict, Field, StrictBool

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
    url_probe_known: bool = False
    title: str | None = None
    present_selectors: frozenset[str] = Field(default_factory=frozenset)
    # ``present_selectors`` is an empty *known* set only when its acquisition
    # succeeded. A failed/unsupported selector command must set this false so a
    # selector_absent descriptor cannot turn transport failure into a success.
    selector_probe_known: bool = False
    cookie_names: frozenset[str] = Field(default_factory=frozenset)
    cookie_probe_known: bool = False
    login_form_present: bool = True
    login_form_present_before: bool = True
    text_content: str | None = None
    text_probe_known: bool = False
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

    def signal_match(self, descriptor: SignalDescriptor) -> bool | None:
        """Return a descriptor match, or None when its acquisition failed."""
        kind = descriptor.kind
        val = descriptor.value
        if kind == "selector_present":
            return val in self.present_selectors if self.selector_probe_known and not self.timed_out else None
        if kind == "selector_absent":
            return val not in self.present_selectors if self.selector_probe_known and not self.timed_out else None
        if kind == "url_prefix":
            return self.url.startswith(val) if self.url_probe_known and self.url is not None else None
        if kind == "cookie_present":
            return val in self.cookie_names if self.cookie_probe_known and not self.timed_out else None
        if kind == "text_present":
            return (
                val in self.text_content
                if self.text_probe_known and self.text_content is not None and not self.timed_out
                else None
            )
        return None

    def signal_observed(self, descriptor: SignalDescriptor) -> bool:
        """Compatibility projection for legacy direct raw-observation callers."""
        return self.signal_match(descriptor) is True


UrlRelation = Literal["unchanged", "changed", "unknown"]
UrlFlow = Literal["challenge", "sign_in", "other", "unknown"]


class EvaluatedObservation(BaseModel):
    """Value-free facts evaluated against the authoritative expect and recipe.

    This is deliberately a receipt shape, not a second recipe format.  It can
    contain only booleans (or an honest ``None``) and the canonical URL classes;
    selectors, URLs, cookie names, text, labels, weights, and verdicts remain in
    the server-owned ``ExpectSpec`` and ``LoginRecipe`` passed to
    :func:`verify_evaluated`.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    password_field_present_before: StrictBool | None = None
    password_field_present_after: StrictBool | None = None
    otp_field_present_before: StrictBool | None = None
    otp_field_present_after: StrictBool | None = None
    captcha_present_before: StrictBool | None = None
    captcha_present_after: StrictBool | None = None
    login_form_present_before: StrictBool | None = None
    login_form_present_after: StrictBool | None = None
    url_relation: UrlRelation = "unknown"
    url_flow: UrlFlow = "unknown"

    # Each value aligns with the same-named authoritative ExpectSpec field.
    # Undeclared expectations MUST remain None; a caller cannot smuggle a hit.
    success_url_prefix: StrictBool | None = None
    success_selector: StrictBool | None = None
    failure_selector: StrictBool | None = None
    challenge_selector: StrictBool | None = None

    # Ordered against recipe.all_signals(), exactly once per descriptor.
    recipe_matches: tuple[StrictBool | None, ...] = ()

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


def _recipe_signals(
    recipe: LoginRecipe, matches: tuple[StrictBool | None, ...]
) -> list[VerdictSignal]:
    out: list[VerdictSignal] = []
    for idx, d in enumerate(recipe.all_signals()):
        out.append(
            VerdictSignal(
                signal=d.label or f"recipe:{d.kind}:{idx}",
                observed=matches[idx] is True,
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


def _url_flow(url: str | None) -> UrlFlow:
    """Project a raw URL into the only URL vocabulary receipts may carry."""
    if url is None:
        return "unknown"
    segments = url_segments(url)
    if segments & CHALLENGE_URL_SEGMENTS:
        return "challenge"
    if segments & AUTH_FLOW_URL_SEGMENTS:
        return "sign_in"
    return "other"


def _evaluate_page_observation(
    observation: PageObservation, *, expect: ExpectSpec, recipe: LoginRecipe | None
) -> EvaluatedObservation:
    """Remote adapter: evaluate rich, local-only page facts once at the edge."""
    def expect_match(value: str | None, matched: bool | None) -> StrictBool | None:
        return matched if value is not None else None

    relation: UrlRelation = "unknown"
    if observation.url_probe_known and observation.url is not None and observation.url_before is not None:
        relation = "unchanged" if observation.url == observation.url_before else "changed"

    return EvaluatedObservation(
        password_field_present_after=(
            observation.password_field_present
            if observation.selector_probe_known and not observation.timed_out
            else None
        ),
        otp_field_present_after=(
            observation.otp_field_present if observation.selector_probe_known and not observation.timed_out else None
        ),
        captcha_present_after=(
            observation.captcha_present
            if observation.selector_probe_known and not observation.timed_out
            else None
        ),
        login_form_present_before=observation.login_form_present_before,
        login_form_present_after=(
            observation.login_form_present
            if observation.selector_probe_known and not observation.timed_out
            else None
        ),
        url_relation=relation,
        url_flow=_url_flow(observation.url) if observation.url_probe_known else "unknown",
        success_url_prefix=expect_match(
            expect.success_url_prefix,
            observation.url.startswith(expect.success_url_prefix)
            if observation.url_probe_known
            and observation.url is not None
            and expect.success_url_prefix is not None
            else None,
        ),
        success_selector=expect_match(
            expect.success_selector,
            observation.signal_match(SignalDescriptor(
                kind="selector_present",
                value=expect.success_selector,
                direction="authenticated",
            ))
            if expect.success_selector is not None
            else None,
        ),
        failure_selector=expect_match(
            expect.failure_selector,
            observation.signal_match(SignalDescriptor(
                kind="selector_present",
                value=expect.failure_selector,
                direction="rejected",
            ))
            if expect.failure_selector is not None
            else None,
        ),
        challenge_selector=expect_match(
            expect.challenge_selector,
            observation.signal_match(SignalDescriptor(
                kind="selector_present",
                value=expect.challenge_selector,
                direction="challenged",
            ))
            if expect.challenge_selector is not None
            else None,
        ),
        recipe_matches=(
            tuple(observation.signal_match(d) for d in recipe.all_signals())
            if recipe is not None
            else ()
        ),
    )


#: The ambiguity markers — an observation that is real, is worth recording, and
#: is deliberately NOT evidence for any outcome. Their whole job is to stop a
#: success being claimed from the mere absence of a form.
AMBIGUOUS_STRUCTURAL_REASONS = (
    "password_form_on_new_page",
    "still_on_sign_in_flow",
    "form_cleared_url_unchanged",
)

#: EVERY generic structural signal this engine can emit, with its direction and
#: its weight — the ONE place the vocabulary is declared. `_structural_signals`
#: reads its weights from here, so a name cannot carry two weights, and hosts
#: bind their own tables to it instead of restating it:
#: `aidream/api/mcp/agent_service/browser_tools.py` (which reasons are safe to
#: hand an agent) and `aidream/services/cloud_browser/local_commands.py` (the
#: size bound a login completion must fit in). Adding a signal here therefore
#: reaches both; restating one there is how a new signal escapes unannounced.
GENERIC_STRUCTURAL_SIGNALS: tuple[tuple[str, str, float], ...] = (
    ("anti_bot_challenge_detected", "challenged", 0.85),
    ("verification_code_field_visible", "challenged", 0.85),
    ("password_form_still_visible", "rejected", 0.8),
    ("challenge_url_detected", "challenged", 0.8),
    ("form_cleared_left_sign_in_flow", "authenticated", 0.75),
    ("form_cleared_left_sign_in_flow_unprobed", "authenticated", 0.2),
)

#: The signals `_generic_signals` derives from a caller's ExpectSpec.
EXPECT_SIGNALS: tuple[tuple[str, str, float], ...] = (
    ("expected_challenge_present", "challenged", 0.9),
    ("expected_error_present", "rejected", 0.9),
    ("navigated_to_expected", "authenticated", 0.9),
    ("expected_marker_present", "authenticated", 0.9),
)

#: Every value `Verdict.reason` can hold that is NOT a user-authored recipe
#: label — a fixed, machine-safe vocabulary.
FIXED_VERDICT_REASONS: frozenset[str] = frozenset(
    {name for name, _d, _w in GENERIC_STRUCTURAL_SIGNALS}
    | {name for name, _d, _w in EXPECT_SIGNALS}
    | set(AMBIGUOUS_STRUCTURAL_REASONS)
    | {
        "explicit_expectation_not_met",
        "no_signals_observed",
        "signals_contradict",
        "recipe_signals_contradict",
    }
)

_STRUCTURAL_SIGNAL_SPEC = {name: (direction, weight) for name, direction, weight in GENERIC_STRUCTURAL_SIGNALS}


def _structural_signals(obs: EvaluatedObservation) -> tuple[list[VerdictSignal], str | None]:
    """The settled-page structural evidence, in D-12 precedence order.

    Returns ``(signals, ambiguity_reason)``. Exactly one directional signal can
    be observed, because the underlying facts are mutually exclusive by
    construction; when none is, ``ambiguity_reason`` names WHY the page could not
    be read — which is an honest ``unknown``, never a success.

    🚨 This is the knowledge the production Cloud Browser path had learned and
    kept in its own private classifier. It lives here now so there is exactly ONE
    implementation of the login decision.
    """
    def sig(name: str) -> VerdictSignal:
        direction, weight = _STRUCTURAL_SIGNAL_SPEC[name]
        return VerdictSignal(
            signal=name,
            observed=True,
            source="generic",
            direction=direction,  # type: ignore[arg-type]
            weight=weight,
        )

    # A positive challenge fact is decisive on its own.  Negative facts are
    # different: they need the full settled probe before they may support success.
    if obs.captcha_present_after is True:
        return [sig("anti_bot_challenge_detected")], None
    if obs.otp_field_present_after is True:
        return [sig("verification_code_field_visible")], None
    if obs.password_field_present_after is True:
        if obs.url_relation == "unchanged":
            return [sig("password_form_still_visible")], None
        # A password box on a DIFFERENT page is not a refusal and not a success
        # (a re-auth step, a second account chooser). Say so, decide nothing.
        return [], "password_form_on_new_page"
    if obs.url_flow == "challenge":
        return [sig("challenge_url_detected")], None
    if obs.url_flow == "sign_in":
        return [], "still_on_sign_in_flow"
    if obs.url_relation == "unchanged":
        return [], "form_cleared_url_unchanged"

    # Everything below here describes the SAME page shape: the sign-in form is
    # gone AND the browser left the sign-in flow for an ordinary url. How much
    # that is worth depends on HOW WELL it was observed, and the difference is
    # confidence, not outcome — which is exactly what `confidence` is for.
    if not (obs.url_relation == "changed" and obs.url_flow == "other"):
        return [], None

    settled_probe_saw_no_control = (
        obs.password_field_present_after is False
        and obs.otp_field_present_after is False
        and obs.captcha_present_after is False
    )
    if settled_probe_saw_no_control:
        # Precise: every control was probed and none is there. Strong evidence.
        return [sig("form_cleared_left_sign_in_flow")], None
    if obs.login_form_present_before is True and obs.login_form_present_after is False:
        # Coarse: the precise probe never ran (or ran partially), but the one
        # fact we DO have is a real before/after transition — the form was
        # there, it is not any more, and the browser is off the sign-in flow.
        # That is weak positive evidence, and dropping it is how a real success
        # gets written down as "I could not read the page" (Lane AK). It is a
        # weight-0.2 success: believable, never on its own sufficient, and it
        # says in its own name that it was not probed.
        return [sig("form_cleared_left_sign_in_flow_unprobed")], None
    return [], None


def _generic_signals(expect: ExpectSpec, obs: EvaluatedObservation) -> list[VerdictSignal]:
    out: list[VerdictSignal] = []
    if expect.challenge_selector:
        out.append(
            VerdictSignal(
                signal="expected_challenge_present",
                observed=obs.challenge_selector is True,
                source="expect",
                direction="challenged",
                weight=0.9,
            )
        )
    if expect.failure_selector:
        out.append(
            VerdictSignal(
                signal="expected_error_present",
                observed=obs.failure_selector is True,
                source="expect",
                direction="rejected",
                weight=0.9,
            )
        )
    if expect.success_url_prefix:
        out.append(
            VerdictSignal(
                signal="navigated_to_expected",
                observed=obs.success_url_prefix is True,
                source="expect",
                direction="authenticated",
                weight=0.9,
            )
        )
    if expect.success_selector:
        out.append(
            VerdictSignal(
                signal="expected_marker_present",
                observed=obs.success_selector is True,
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


def _validate_evaluated_observation(
    observation: EvaluatedObservation, *, expect: ExpectSpec, recipe: LoginRecipe | None
) -> None:
    """Reject facts that do not correspond to the frozen authoritative inputs."""
    for field in (
        "success_url_prefix",
        "success_selector",
        "failure_selector",
        "challenge_selector",
    ):
        if getattr(expect, field) is None and getattr(observation, field) is not None:
            raise ValueError(f"evaluated observation includes hit for undeclared {field}")
    expected_count = len(recipe.all_signals()) if recipe is not None else 0
    if len(observation.recipe_matches) != expected_count:
        raise ValueError(
            "evaluated observation recipe_matches must exactly match the frozen recipe descriptor count"
        )


def verify_evaluated(
    observation: EvaluatedObservation,
    *,
    expect: ExpectSpec | None = None,
    recipe: LoginRecipe | None = None,
) -> Verdict:
    """Decide a strict, value-free login receipt using the canonical algorithm.

    ``expect`` and ``recipe`` are authoritative server-side definitions.  An
    evaluated caller supplies only their resulting match booleans, never a
    descriptor, weight, or direction.
    """
    expect = expect or ExpectSpec()
    _validate_evaluated_observation(observation, expect=expect, recipe=recipe)

    if recipe is not None:
        recipe_signals = _recipe_signals(recipe, observation.recipe_matches)
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


def verify(
    observation: PageObservation,
    *,
    expect: ExpectSpec | None = None,
    recipe: LoginRecipe | None = None,
) -> Verdict:
    """Adapt the established rich remote observation into the canonical receipt.

    This remains the public API for existing Cloud Browser callers.  New local
    receipt paths call :func:`verify_evaluated` directly, so both paths share
    the one decision implementation above.
    """
    expect = expect or ExpectSpec()
    return verify_evaluated(
        _evaluate_page_observation(observation, expect=expect, recipe=recipe),
        expect=expect,
        recipe=recipe,
    )


__all__ = [
    "AMBIGUOUS_STRUCTURAL_REASONS",
    "AUTH_FLOW_URL_SEGMENTS",
    "CHALLENGE_URL_SEGMENTS",
    "EXPECT_SIGNALS",
    "FIXED_VERDICT_REASONS",
    "GENERIC_STRUCTURAL_SIGNALS",
    "EvaluatedObservation",
    "Outcome",
    "PageObservation",
    "Verdict",
    "VerdictSignal",
    "url_segments",
    "verify",
    "verify_evaluated",
]
