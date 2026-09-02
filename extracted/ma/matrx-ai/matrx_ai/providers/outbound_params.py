"""resolve_outbound_params — THE seam turning a ``UnifiedConfig`` into the
DB-resolved provider params for a chat request.

Every flipped chat translator calls this instead of shaping params off the
legacy ``api_class`` + ``ThinkingConfig``:

    params = resolve_outbound_params(config, profile.controls)

``canonical_settings_from_config`` extracts only the keys the caller set (one
provider-independent pass), then ``CompiledControlsMap.outbound`` applies the
per-api/per-offering control rules (ai.api.rules <- ai.offering.override:
rename / value_map / clamp / const / default / supported:false / processors)
and returns provider-vocabulary params — nested dicts already expanded from
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

Adjustments (drop/omit/map/clamp/const) are voiced with a yellow banner so a
user's request is never silently mutated — the same posture as the legacy
translators' CAPABILITY ADJUSTMENT warnings.
"""

from __future__ import annotations

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
    try:
        import asyncio

        from matrx_connect import get_app_context
        from matrx_connect.context.events import WarningPayload

        ctx = get_app_context()
        emitter = getattr(ctx, "emitter", None)
        if emitter is None:
            return
        keys = sorted({str(a.key) for a in lost})
        payload = WarningPayload(
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
        )
        asyncio.get_running_loop()
        from matrx_utils import detached_task

        detached_task(emitter.send_warning(payload), name="outbound_params_warning")
    except RuntimeError:
        return  # no running loop (sync/offline resolution) — the log still has it
    except Exception as exc:  # noqa: BLE001 — telling the user must never break the run
        vcprint(
            f"[outbound_params] could not emit the dropped-settings warning ({exc!r}); "
            "the adjustment detail is still in the log and on the Adjustment list.",
            color="yellow",
        )


def drop_foreign_canonical_keys(
    canonical: dict[str, Any],
    controls: CompiledControlsMap,
    *,
    model: Any = "?",
) -> list[str]:
    """THE DECLARED-KEYS GATE — the one canonical implementation, shared by the
    chat seam (``resolve_outbound_params``) and the media seam
    (``BaseMediaGeneration._outbound_params``).

    The canonicalizer extracts EVERY canonical cluster a config can carry
    (chat + media). The seeded rules of a DB api explicitly enumerate this
    api's full control surface (unsupported keys included, as supported:false)
    — so a canonical key with NO rule and NO processor ``consumes`` claim is
    foreign to this api (e.g. a chat key like ``verbosity`` riding on a config
    pointed at a media offering) and must never implicitly pass through to the
    provider via PASSTHROUGH_RULE. Passthrough profiles (rules == {}, the
    host-catalog client mode) keep the legacy behave-as-given semantics.

    Mutates ``canonical`` in place, voices every drop loudly, and returns the
    dropped keys (sorted).
    """
    if not controls.rules:
        return []
    declared = set(controls.rules)
    for rule in controls.rules.values():
        declared.update(rule.processor_config.get("consumes", []))
    foreign = sorted(
        key for key in canonical if not key.startswith("_") and key not in declared
    )
    if foreign:
        vcprint(
            f"[outbound_params] dropped foreign canonical key(s) not declared by "
            f"this api/offering's control rules: {foreign} (model={model})",
            color="yellow",
        )
        for key in foreign:
            canonical.pop(key)
    return foreign


def resolve_outbound_params(
    config: Any,
    controls: CompiledControlsMap,
    *,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    from matrx_ai.catalog.canonicalize import canonical_settings_from_config

    canonical = canonical_settings_from_config(config)
    for key in _STRUCTURAL_CANONICAL_KEYS:
        canonical.pop(key, None)

    drop_foreign_canonical_keys(canonical, controls, model=getattr(config, "model", "?"))

    params, adjustments = controls.outbound(canonical, context=context)
    for key in _STRUCTURAL_CANONICAL_KEYS:
        params.pop(key, None)
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


__all__ = [
    "drop_foreign_canonical_keys",
    "resolve_outbound_params",
    "warn_client_about_dropped_settings",
]
