"""resolve_outbound_params — THE seam turning a ``UnifiedConfig`` into the
DB-resolved provider params for a chat request.

Every flipped chat translator calls this instead of shaping params off the
legacy ``api_class`` + ``ThinkingConfig``:

    params = resolve_outbound_params(config, profile.controls)

``canonical_settings_from_config`` extracts only the keys the caller set (one
provider-independent pass), then ``CompiledControlsMap.outbound`` applies the
per-api/per-offering control rules (ai.api.rules <- ai.offering.override:
rename / value_map / clamp / const / default / processors) and returns
provider-vocabulary params — nested dicts already expanded from
dotted provider keys, ready to merge into the provider request.

Structural concerns stay in the translators: messages, tools, tool_choice,
stream, response_format schema enforcement, cache breakpoints. Two structural
keys are explicitly excluded here:

- ``response_format`` — canonicalize carries it for other consumers, but the
  translators own its per-provider schema conversion/sanitization; letting it
  ride through ``outbound`` would clobber that (or leak the raw unified shape
  on a passthrough host-catalog profile).
- ``stream`` — never enters the canonical dict; each provider client owns its
  streaming decision (e.g. Cerebras disables streaming when tools are present).

Before ``outbound``, the gate (``drop_foreign_canonical_keys`` ->
``CompiledControlsMap.translate_foreign``) converts every key the target does
not carry through its setting family (K7), or drops it as before C6 while the
family data is absent.

Adjustments (drop/omit/map/clamp/const) are voiced with a yellow banner so a
user's request is never silently mutated — the same posture as the legacy
translators' CAPABILITY ADJUSTMENT warnings.
"""

from __future__ import annotations

import contextlib
from contextvars import ContextVar
from typing import TYPE_CHECKING, Any

from matrx_utils import vcprint

if TYPE_CHECKING:  # circular-by-design: catalog.models imports providers.resolved_capabilities
    from matrx_ai.catalog.controls import CompiledControlsMap

# Keys the translators own STRUCTURALLY — they must never reach a provider
# through the scalar param seam, even when this seam produces them.
#
#   - ``response_format`` — the canonicalizer emits it, but each translator owns
#     its per-provider schema conversion/sanitization.
#   - ``tts_voice`` / ``audio_format`` — the canonicalizer does NOT emit these,
#     but a TTS offering's control rules declare them ``supported:true`` with a
#     ``default`` (see ai.offering.override.params for gemini-*-tts), so
#     ``controls.outbound`` INJECTS the defaults (``tts_voice="kore"``,
#     ``audio_format="wav"``) into the resolved params. The TTS-capable chat
#     translators consume both structurally off ``UnifiedConfig`` — ``tts_voice``
#     → ``speech_config`` (``TTSVoiceConfig.to_google()`` etc.), ``audio_format``
#     → output transcode — never as a scalar provider param. Merged blind into a
#     provider's config object they 400 it ("Extra inputs" for
#     ``GenerateContentConfig``); this seam strips them so that whole class of
#     TTS-build failure is extinct across every chat translator, not one.
_STRUCTURAL_CANONICAL_KEYS: tuple[str, ...] = (
    "response_format",
    "tts_voice",
    "audio_format",
    # Speech controls: every TTS translator places these itself
    # (matrx_ai.speech.compile) — Gemini as director prose, OpenAI as
    # `instructions`/`speed`, ElevenLabs as audio tags / voice_settings /
    # language_code. None is a GenerateContentConfig field.
    "performance_direction",
    "speech_speed",
    "turn_pause_ms",
    "language_code",
    "multi_speaker",
)


# Actions that mean "the caller's value did not make it onto the wire".
_DROP_ACTIONS = frozenset({"dropped", "omitted", "unsupported_value"})


def warn_client_about_dropped_settings(adjustments: list[Any], *, model: Any = "?") -> None:
    """THE EQUIVALENCE LAW's client half: an UNEXPECTED drop reaches the user.

    Arman, 2026-08-17: *"a conversion does not need to be reported to the
    client, but an unexpected drop definitely needs to be communicated to the
    client as a warning, not as an error."*

    So this is deliberately narrow:
      * conversions (mapped / clamped / a reconciled unsupported value) are the
        system working as designed — SILENT to the client;
      * a DECLARED capability gap (``supported: false``, a value_map entry
        pointing at null) is expected — also silent;
      * an UNEXPECTED drop — the caller set something this offering silently
        would not carry — is a WARNING. Never an error: the response is still
        valid and, per ``send_warning``, a warning decorates a response rather
        than invalidating it.

    One event per request, not one per key: a switch between distant providers
    can drop several settings at once and N toasts is noise, not information.

    Fire-and-forget by design — telling the user must never delay or break the
    request that is already running. The full detail is on the Adjustment list
    and in the server log regardless.
    """
    lost = [a for a in adjustments if a.action in _DROP_ACTIONS and not a.expected]
    if not lost:
        return
    from matrx_connect.context.events import WarningPayload

    keys = sorted({str(a.key) for a in lost})
    send_client_warning(
        WarningPayload(
            code="setting_not_supported",
            system_message=(
                f"{len(lost)} setting(s) could not be applied to {model}: "
                + "; ".join(a.reason for a in lost)
            ),
            user_message=(
                "This model does not support "
                + ", ".join(keys)
                + ". Everything else was applied and your request ran normally."
            ),
            level="low",
            recoverable=True,
            metadata={
                "model": str(model),
                "dropped": [
                    {"key": str(a.key), "requested": a.canonical_value} for a in lost
                ],
            },
        ),
        name="outbound_params_warning",
    )


def send_client_warning(payload: Any, *, name: str) -> None:
    """THE one door for "the server changed what the caller asked for" (law 4).

    Every server-side step that drops or rewrites a setting the request carried
    — an unsupported key here, a ceiling the send boundary raises — tells the
    CALLER through the stream as a ``warning`` event, not only the server log.
    Fire-and-forget: telling the user must never delay or break the run; with no
    emitter or no running loop the server log (written by the caller) still has it.
    """
    try:
        import asyncio

        from matrx_connect import get_app_context

        ctx = get_app_context()
        emitter = getattr(ctx, "emitter", None)
        if emitter is None:
            return
        asyncio.get_running_loop()
        from matrx_utils import detached_task

        detached_task(emitter.send_warning(payload), name=name)
    except RuntimeError:
        return  # no running loop / no context (sync/offline) — the log still has it
    except Exception as exc:  # noqa: BLE001 — telling the user must never break the run
        vcprint(
            f"[outbound_params] could not emit client warning {name!r} ({exc!r}); "
            "the detail is still in the server log.",
            color="yellow",
        )


def drop_foreign_canonical_keys(
    canonical: dict[str, Any],
    controls: CompiledControlsMap,
    *,
    model: Any = "?",
    adjustments: list[Any] | None = None,
) -> list[str]:
    """THE GATE before ``outbound`` — the one implementation shared by the chat
    seam (``resolve_outbound_params``) and the media seam
    (``BaseMediaGeneration._outbound_params``). It is
    ``CompiledControlsMap.translate_foreign`` (target-aware):

    * setting families loaded (K7, settings-translation C6): a canonical key the
      target does not natively carry — no rule and no processor claim, or a rule
      that says ``supported: false`` — CONVERTS to a sibling in its family that
      the target carries (reasoning_effort=max at an image model becomes its top
      resolution). Only a family with no member that can carry it drops, as an
      UNEXPECTED Adjustment (``expected=False`` -> the one client warning).
    * families absent (today's live catalog): exactly the pre-C6 declared-keys
      gate — a key with no rule and no ``consumes`` claim is dropped loudly
      (``expected=True``, silent to the client); ``supported: false`` is left to
      ``outbound``.

    Mutates ``canonical`` in place and returns the keys removed from it (dropped
    or converted into a sibling), sorted. K9: every outcome is appended to
    ``adjustments`` when given. Passthrough profiles (rules == {}) are untouched.
    """
    translated, gate_adjustments, removed = controls.translate_foreign(canonical, model=model)
    if translated is not canonical:
        canonical.clear()
        canonical.update(translated)
    if adjustments is not None:
        adjustments.extend(gate_adjustments)
    return sorted(removed)


# The Adjustments of the most recent outbound pass in this context, for the
# K10 rejection record (``setting_rejection.build_record``): a provider that
# refuses a wire key is traced back to the canonical key + value that produced
# it — including a value CONVERTED from a sibling, which the request's own
# config never carried. Set by both seams; read only on the failure path.
_LAST_OUTBOUND: ContextVar[tuple[str, tuple[Any, ...]] | None] = ContextVar(
    "matrx_ai_last_outbound_adjustments", default=None
)


def remember_outbound_adjustments(model: Any, adjustments: list[Any]) -> None:
    try:
        _LAST_OUTBOUND.set((str(model), tuple(adjustments)))
    except Exception:  # noqa: BLE001 — bookkeeping must never break a request
        pass


# The provider params of the most recent outbound pass in this context — what
# the translator merges into the request for the SETTINGS. The K10 record reads
# ``sent_value`` from here when no captured wire body exists (a probe or a bare
# dispatch outside an orchestrated turn). Read only on the failure path.
_LAST_OUTBOUND_PARAMS: ContextVar[tuple[str, dict[str, Any]] | None] = ContextVar(
    "matrx_ai_last_outbound_params", default=None
)


def remember_outbound_params(model: Any, params: dict[str, Any]) -> None:
    try:
        _LAST_OUTBOUND_PARAMS.set((str(model), dict(params)))
    except Exception:  # noqa: BLE001 — bookkeeping must never break a request
        pass


def last_outbound_params(model: Any = None) -> dict[str, Any] | None:
    """The last outbound pass's provider params in this context (for ``model``
    when given), or None."""
    current = _LAST_OUTBOUND_PARAMS.get()
    if current is None:
        return None
    if model is not None and current[0] != str(model):
        return None
    return dict(current[1])


def last_outbound_adjustments(model: Any = None) -> list[Any] | None:
    """The last outbound pass's Adjustments in this context (for ``model`` when
    given), or None."""
    current = _LAST_OUTBOUND.get()
    if current is None:
        return None
    if model is not None and current[0] != str(model):
        return None
    return list(current[1])


# Speech controls ride UnifiedConfig, never the canonical dict: the TTS
# translators place them structurally. On a target that declares none of them
# (a text model) they would vanish without a word — with setting families
# loaded (K7) they go through the gate for its verdict, so a voice sent to a
# text model is an UNEXPECTED drop the caller is warned about. Accounting only:
# nothing here reaches the wire.
_SPEECH_KEYS: tuple[str, ...] = (
    "tts_voice",
    "performance_direction",
    "speech_speed",
    "turn_pause_ms",
)


def _undeclared_speech_drops(config: Any, controls: CompiledControlsMap) -> list[Any]:
    if controls.families is None or not controls.rules:
        return []
    speech = {
        key: value
        for key in _SPEECH_KEYS
        if (value := getattr(config, key, None)) is not None and not controls._declares(key)
    }
    if not speech:
        return []
    _, verdict, _ = controls.translate_foreign(speech, model=getattr(config, "model", "?"))
    return [a for a in verdict if a.action == "dropped"]


# Settings-translation R3: a CANDIDATE correction of one or more translation
# cells, replayed on the real send step BEFORE it is written (the rejection
# fixer's proof). Inside ``candidate_cell_rules`` every outbound pass in this
# context substitutes the candidate rules WHOLE for their keys — the same
# whole-cell substitution ``wire_validity.validate_cell`` makes — and stands
# each candidate in as the OFFERING-layer ``proposed`` cell it would be written
# as (``cell_id = "candidate:<key>"``), so layer-sensitive engine passes read it
# exactly as they will after the write (an offering cell's ``clamp.max`` on the
# output ceiling outranks the model maximum — controls ``_output_ceiling``) and
# no Adjustment claims the cell it is replacing.
# Never set on a person's request: only the fixer's replay (one provider call)
# runs inside it.
_CANDIDATE_RULES: ContextVar[dict[str, Any] | None] = ContextVar(
    "matrx_ai_candidate_cell_rules", default=None
)


@contextlib.contextmanager
def candidate_cell_rules(rules: dict[str, Any]):
    """Replay with these ``{setting_key: ControlRule}`` in place of the compiled ones."""
    from matrx_ai.catalog.models import ControlRule

    parsed = {
        key: rule if isinstance(rule, ControlRule) else ControlRule.model_validate(rule)
        for key, rule in rules.items()
    }
    token = _CANDIDATE_RULES.set(parsed)
    try:
        yield parsed
    finally:
        _CANDIDATE_RULES.reset(token)


def with_candidate_rules(controls: CompiledControlsMap) -> CompiledControlsMap:
    """``controls`` with the active candidate rules substituted (unchanged outside a block)."""
    candidates = _CANDIDATE_RULES.get()
    if not candidates:
        return controls
    from matrx_ai.catalog.models import CellRef

    cells = dict(getattr(controls, "cells", None) or {})
    for key in candidates:
        cells[key] = CellRef(cell_id=f"candidate:{key}", layer="offering", state="proposed")
    return controls.model_copy(update={"rules": {**controls.rules, **candidates}, "cells": cells})


def resolve_outbound_params(
    config: Any,
    controls: CompiledControlsMap,
    *,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    from matrx_ai.catalog.canonicalize import canonical_settings_from_config

    controls = with_candidate_rules(controls)
    canonical = canonical_settings_from_config(config)
    for key in _STRUCTURAL_CANONICAL_KEYS:
        canonical.pop(key, None)

    foreign_adjustments: list[Any] = []
    drop_foreign_canonical_keys(
        canonical,
        controls,
        model=getattr(config, "model", "?"),
        adjustments=foreign_adjustments,
    )

    params, adjustments = controls.outbound(canonical, context=context)
    adjustments = foreign_adjustments + _undeclared_speech_drops(config, controls) + adjustments
    remember_outbound_adjustments(getattr(config, "model", "?"), adjustments)
    for key in _STRUCTURAL_CANONICAL_KEYS:
        params.pop(key, None)
    remember_outbound_params(getattr(config, "model", "?"), params)
    if adjustments:
        vcprint(
            data=[
                {
                    "key": adj.key,
                    "action": adj.action,
                    "requested": adj.canonical_value,
                    "sent": adj.sent_value,
                    "reason": adj.reason,
                }
                for adj in adjustments
            ],
            title=(
                f"⚠️  CAPABILITY ADJUSTMENT [{getattr(config, 'model', '?')}]: "
                f"{len(adjustments)} request param(s) adjusted by the api/offering "
                "control rules — the request proceeds with the adjusted values."
            ),
            color="yellow",
            verbose=True,
        )
    warn_client_about_dropped_settings(adjustments, model=getattr(config, "model", "?"))
    return params


def resolve_structural_setting(
    value: Any,
    key: str,
    controls: CompiledControlsMap,
    *,
    model: Any = "?",
) -> Any:
    """Apply the api/offering control rule for ONE translator-owned (structural) key.

    Structural keys (``tool_choice`` today) never ride the scalar param seam:
    each translator converts the canonical value into its own wire shape
    (Anthropic ``{"type": "any"}``, Google ``FunctionCallingConfig(mode="ANY")``).
    Before this helper that meant the rule a catalog row declared for such a key
    was UI-only: ``ai.model_config`` narrowed the dropdown, but a stored preset or
    raw API caller still reached the hardcoded switch — e.g. ``tool_choice=
    "required"`` became ``{"type": "any"}`` and 400'd on Claude Opus 5.5 / Fable
    5.1, which reject forced tool use.

    Now the translator asks the rule first. The rule is applied through the SAME
    ``CompiledControlsMap.outbound`` pass as every scalar key — a one-rule copy of
    the map, so ``supported`` / ``value_map`` / ``on_unmapped`` (incl. "nearest"
    via the canonical value order) / ``clamp`` / ``const`` behave identically and
    no processor or other key's default fires. Adjustments are voiced exactly like
    ``resolve_outbound_params``: server banner always, client warning on an
    UNEXPECTED drop (THE EQUIVALENCE LAW).

    Returns the canonical-vocabulary value the translator should shape, or
    ``None`` when the rule eliminated it (the translator then sends nothing and
    the provider default applies). A key with NO rule is returned unchanged —
    offerings that declare nothing behave exactly as before.
    """
    if value is None or key not in controls.rules:
        return value
    rule = controls.rules[key]
    single = controls.model_copy(update={"rules": {key: rule}})
    params, adjustments = single.outbound({key: value})
    if adjustments:
        vcprint(
            data=[
                {
                    "key": adj.key,
                    "action": adj.action,
                    "requested": adj.canonical_value,
                    "sent": adj.sent_value,
                    "reason": adj.reason,
                }
                for adj in adjustments
            ],
            title=(
                f"⚠️  CAPABILITY ADJUSTMENT [{model}]: structural '{key}' adjusted by "
                "the api/offering control rules — the request proceeds with the "
                "adjusted value."
            ),
            color="yellow",
            verbose=True,
        )
        warn_client_about_dropped_settings(adjustments, model=model)
    from matrx_ai.catalog.controls import flatten_dotted  # local: circular-by-design

    flat = flatten_dotted(params)
    return flat.get(rule.provider_key or key)


__all__ = [
    "drop_foreign_canonical_keys",
    "last_outbound_adjustments",
    "remember_outbound_adjustments",
    "resolve_outbound_params",
    "resolve_structural_setting",
    "send_client_warning",
    "warn_client_about_dropped_settings",
]
