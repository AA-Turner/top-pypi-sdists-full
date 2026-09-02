"""The login executor — resolve → capture-before → fill → submit → observe → verify
→ capture-after, in ONE indivisible call. The agent never receives a value.

This is the pure orchestration core (D-11 / D-12). Everything that touches a secret,
a real browser, or the DB is an injected protocol, so the whole flow is testable
against synthetic pages and a FakeWorker fill endpoint before any real worker exists.

The invariants this enforces, each with a test behind it:

* **Refusal-before-touch.** If the effective specification cannot be completed — a
  named ``field_key`` is unknown/sealed/inactive, or a step references an undeclared
  selector — the attempt is REFUSED before the first fill and before any capture.
  Nothing is typed. A half-filled page is a worse state than an untouched one.
* **Resolve-all-up-front.** Every secret the attempt needs is resolved in ONE call
  before any fill, so a mid-fill resolution failure can never leave a partial attempt.
* **One attempt.** The executor is single-shot by construction — it never retries and
  takes no ``force``/``retry`` argument. ``rejected`` ends the episode; a corrected
  credential is a NEW attempt at the host.
* **Values never surface.** Resolved values live in one local dict, are used for the
  fill, are never placed in a result, an exception, a log, or a capture, and the
  reference is dropped when the fills complete. Field NAMES travel in both directions.
* **State capture is core**, bracketing every attempt (before + after), for later
  learning when a verdict is wrong.
"""

from __future__ import annotations

from typing import Literal, Mapping, Protocol

from .recipe import LoginRecipe
from .results import CaptureRef, LoginAttemptResult, RecipeRef
from .spec import AttemptSpec, FieldSpec, SpecIncompleteError, SubmitSpec, WaitForSpec
from .verifier import PageObservation, verify

CapturePhase = Literal["before", "after"]


class FieldUnavailable(Exception):
    """A named ``field_key`` cannot be filled — it is not on the item, is inactive, or
    is sealed. Carries the field NAME and a reason; NEVER a value. Raised by the
    resolver so the executor can refuse the whole attempt before touching the page."""

    def __init__(self, field_key: str, reason: str) -> None:
        self.field_key = field_key
        self.reason = reason
        super().__init__(f"field {field_key!r} unavailable: {reason}")


class SecretResolver(Protocol):
    """Resolves the exact set of named secrets for one attempt, server-side. The host
    implementation wraps ``vault_browser_login_materialize`` (multi-field). It raises
    :class:`FieldUnavailable` for any key it cannot fill, and its return maps
    ``field_key -> value``. The value is never seen by the agent."""

    async def resolve(
        self, *, actor_id: str, credential_item_id: str, origin: str, field_keys: list[str]
    ) -> Mapping[str, str]: ...


class WorkerFill(Protocol):
    """The in-worker injection primitive (``RemoteBrowserClient.fill`` + submit/wait).
    ``fill`` returns only success — the ``FillResult.value`` echo is discarded here so
    a value can never ride a result outward."""

    async def fill(self, selector: str, value: str, *, clear_first: bool) -> bool: ...

    async def submit(self, *, kind: str, selector: str | None) -> None: ...

    async def wait_for(self, selector: str, *, timeout_ms: int) -> bool: ...


class PageObserver(Protocol):
    async def observe(self, *, login_form_present_before: bool) -> PageObservation: ...


class StateCapturer(Protocol):
    """Writes a redacted before/after state capture and returns its handle. Masking
    happens in the worker before the shutter; an unverifiable mask stores
    ``privacy_class='sensitive'`` and is never rendered in the product timeline."""

    async def capture(self, *, phase: CapturePhase) -> CaptureRef: ...


def _effective_plan(
    spec: AttemptSpec, recipe: LoginRecipe | None
) -> tuple[list[tuple[FieldSpec, SubmitSpec | None, WaitForSpec | None]], list[str], bool]:
    """Return (fill_plan, field_keys, recipe_overrode_agent_spec).

    Generic detection is the floor; a recipe is the ceiling. When an active recipe
    exists its selectors and field keys SUPERSEDE the agent's; the divergence is
    recorded (it is itself a Hindsight signal — an agent that keeps disagreeing with a
    recipe is telling you the site changed).
    """
    if recipe is None or not recipe.field_map:
        plan = spec.ordered_fill_plan()
        return plan, spec.field_keys, False

    # Build the plan from the recipe, grouped by step, submit riding each step's last
    # field. The recipe carries no submit control of its own per field, so a recipe-
    # driven attempt reuses the agent's submit as the step boundary action.
    rows = sorted(recipe.field_map, key=lambda r: (r.step, recipe.field_map.index(r)))
    submit = spec.submit or (spec.steps[-1].submit if spec.steps else SubmitSpec(kind="none"))
    plan: list[tuple[FieldSpec, SubmitSpec | None, WaitForSpec | None]] = []
    keys: list[str] = []
    for idx, row in enumerate(rows):
        fld = (
            FieldSpec(
                selector=row.selector,
                field_key=row.field_key,
                literal=None if row.field_key else "",  # literal_key resolution is host-side
                clear_first=row.clear_first,
            )
            if row.field_key
            else FieldSpec(selector=row.selector, literal="", clear_first=row.clear_first)
        )
        if row.field_key:
            keys.append(row.field_key)
        last = idx == len(rows) - 1
        plan.append((fld, submit if last else None, None))

    recipe_keys = sorted(set(keys))
    recipe_selectors = {r.selector for r in rows}
    spec_selectors = {f.selector for f in spec.fields}
    overrode = recipe_keys != spec.field_keys or recipe_selectors != spec_selectors
    return plan, recipe_keys, overrode


async def run_login_attempt(
    *,
    actor_id: str,
    credential_item_id: str,
    origin: str,
    spec: AttemptSpec,
    resolver: SecretResolver,
    worker: WorkerFill,
    observer: PageObserver,
    capturer: StateCapturer,
    recipe: LoginRecipe | None = None,
    low_confidence_threshold: float = 0.5,
) -> LoginAttemptResult:
    """Execute one login attempt. Single-shot; never retries."""
    recipe_ref = RecipeRef(
        recipe_id=recipe.recipe_id if recipe else None,
        recipe_version=recipe.recipe_version if recipe else None,
    )

    # ── REFUSAL-BEFORE-TOUCH ────────────────────────────────────────────────
    # (1) The plan itself must be well-formed (undeclared step selectors refuse here).
    try:
        plan, field_keys, overrode = _effective_plan(spec, recipe)
    except SpecIncompleteError as exc:
        return LoginAttemptResult(
            status="spec_incomplete",
            field_keys=spec.field_keys,
            recipe=recipe_ref,
            missing_fields=exc.missing_fields,
            refusal_detail=exc.detail,
        )
    recipe_ref.recipe_overrode_agent_spec = overrode

    # (2) Resolve EVERY named secret up front. Any unavailable key refuses the WHOLE
    # attempt — before the page is touched, before any capture. Nothing is typed.
    resolved: Mapping[str, str] = {}
    if field_keys:
        try:
            resolved = await resolver.resolve(
                actor_id=actor_id,
                credential_item_id=credential_item_id,
                origin=origin,
                field_keys=field_keys,
            )
        except FieldUnavailable as exc:
            return LoginAttemptResult(
                status="spec_incomplete",
                field_keys=field_keys,
                recipe=recipe_ref,
                missing_fields=[exc.field_key],
                refusal_detail=(
                    f"cannot complete the attempt: field {exc.field_key!r} is "
                    f"{exc.reason}. Nothing was typed."
                ),
            )
        missing = [k for k in field_keys if k not in resolved]
        if missing:
            return LoginAttemptResult(
                status="spec_incomplete",
                field_keys=field_keys,
                recipe=recipe_ref,
                missing_fields=missing,
                refusal_detail=(
                    "cannot complete the attempt: the vault did not return "
                    f"{', '.join(missing)}. Nothing was typed."
                ),
            )

    # ── CAPTURE BEFORE ──────────────────────────────────────────────────────
    before = await capturer.capture(phase="before")
    baseline = await observer.observe(login_form_present_before=True)
    form_present_before = baseline.login_form_present

    # ── FILL + SUBMIT (values live only in this scope) ──────────────────────
    try:
        for field, submit, wait in plan:
            if field.is_secret and field.field_key:
                value = resolved[field.field_key]
            else:
                # A literal the agent legitimately knows. A recipe literal_key is
                # resolved host-side and arrives via the spec's literal; a bare "" is
                # a recipe placeholder the host fills before calling.
                value = field.literal or ""
            await worker.fill(field.selector, value, clear_first=field.clear_first)
            if submit is not None and submit.kind != "none":
                await worker.submit(kind=submit.kind, selector=submit.selector)
            if wait is not None:
                await worker.wait_for(wait.selector, timeout_ms=wait.timeout_ms)
    finally:
        # Drop the reference to the values as soon as the fills complete.
        resolved = {}

    # ── OBSERVE + VERIFY ────────────────────────────────────────────────────
    observation = await observer.observe(login_form_present_before=form_present_before)
    observation = observation.model_copy(update={"login_form_present_before": form_present_before})
    verdict = verify(observation, expect=spec.expect, recipe=recipe)

    # ── CAPTURE AFTER ───────────────────────────────────────────────────────
    after = await capturer.capture(phase="after")

    floor = (
        recipe.confidence_floor
        if recipe and recipe.confidence_floor is not None
        else low_confidence_threshold
    )
    low_confidence = verdict.outcome == "authenticated" and verdict.confidence < floor

    return LoginAttemptResult(
        status="ok",
        outcome=verdict.outcome,
        confidence=verdict.confidence,
        low_confidence=low_confidence,
        signals=verdict.signals,
        challenge_class=verdict.challenge_class,
        contradiction=verdict.contradiction,
        field_keys=field_keys,
        recipe=recipe_ref,
        before_capture=before,
        after_capture=after,
        url=observation.url,
        title=observation.title,
    )


__all__ = [
    "CapturePhase",
    "FieldUnavailable",
    "PageObserver",
    "SecretResolver",
    "StateCapturer",
    "WorkerFill",
    "run_login_attempt",
]
