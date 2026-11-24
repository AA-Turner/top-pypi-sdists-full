"""TEMPLATE THINKING — a saved thinking part rides only to the model that wrote it.

An agent's authored template may carry an assistant turn with a THINKING part saved from a real
run: Anthropic signed thinking, OpenAI reasoning (``encrypted_content`` + ``id``), Gemini thought
signatures — including the signature Gemini puts on a TEXT part
(``TextContent.metadata["google_thought_signature"]``). A signature is only valid for the model
that produced it, so:

* **At intake** (``stamp_produced_by``, called from ``UnifiedAIClient._stamp_offering_usage``, the
  one seam where the response meets its resolved call profile) every thinking part, and every
  Gemini text part carrying a thought signature, gets ``metadata["produced_by"]`` =
  ``{model, model_id, provider_model_id, provider, offering_id}``. Additive: an existing stamp is
  never overwritten. It persists with the part (``to_storage_dict``) and comes back through the one
  decoder (``reconstruct_content``), so a part copied into an agent's template keeps it.
* **At the send boundary** (``drop_foreign_template_thinking``, ONE step in
  ``config/send_boundary.prepare_for_send``) only messages carrying the ``cache_template`` mark
  (``config/cache_marks.py``) are read. Same model → the part goes verbatim (nothing changes, so
  turn 1 from the definition and turn 2 from the stored rows render the same bytes). A different
  model → the thinking part is REMOVED (never turned into visible text) and a signed text part
  loses only its signature. A stored Gemini text signature lives under a key no translator reads
  (``stored_google_thought_signature``) and is restored to the live key here, same model only — so
  live history keeps today's wire (no text signature on later turns). Every change lands on the WIRE copy only — the canonical config (what
  the chat stores) keeps the part, so switching back to the producing model sends it again.
* **No send profile** (no person turn): ``apply_template_thinking`` resolves the outgoing model
  from ``config.model``; still unknown → an unstamped part is dropped. **The step failing** drops
  every template thinking part and text signature (fail closed, for template thinking only).
* **No ``produced_by``** (a part saved before stamping existed): kept only when the outgoing wire
  is the part's own provider — exactly the parts today's ``ThinkingContent.to_<provider>`` would
  have sent verbatim — and dropped otherwise, where today's rule would have turned it into a TEXT
  block. Kept or dropped, it is noted.

Live conversation history (no ``cache_template`` mark) is never touched here.
"""

from __future__ import annotations

import logging
from copy import copy
from typing import Any

from matrx_utils import vcprint

logger = logging.getLogger(__name__)

#: Part metadata key: which model produced this thinking / signed text part.
PRODUCED_BY_KEY = "produced_by"
#: Gemini's thought signature on a TEXT part (``TextContent.from_google``) — the live key the Google
#: translator sends.
GOOGLE_TEXT_SIGNATURE_KEY = "google_thought_signature"
#: Where a stored text part keeps that signature (``TextContent.to_storage_dict``). NO translator reads
#: it, so a live conversation's later turns send exactly what they always did; only this module's
#: template step copies it back to the live key, for the model that produced it.
STORED_GOOGLE_TEXT_SIGNATURE_KEY = "stored_google_thought_signature"
#: The send-boundary step name, and the AppContext metadata key its notes land under.
STEP_NAME = "template_thinking"


def produced_by(profile: Any) -> dict[str, str] | None:
    """The ``produced_by`` stamp for a resolved call profile, or ``None`` without one."""
    if profile is None:
        return None
    stamp = {
        "model": getattr(profile, "model_name", None),
        "model_id": getattr(profile, "model_id", None),
        "provider_model_id": getattr(profile, "provider_model_id", None),
        "provider": getattr(profile, "vendor", None),
        "offering_id": getattr(profile, "offering_id", None),
    }
    out = {key: str(value) for key, value in stamp.items() if value}
    return out or None


def _is_signed_text(part: Any) -> bool:
    from matrx_ai.config.unified_content import TextContent

    metadata = getattr(part, "metadata", None)
    return (
        isinstance(part, TextContent)
        and isinstance(metadata, dict)
        and (
            metadata.get(GOOGLE_TEXT_SIGNATURE_KEY) is not None
            or metadata.get(STORED_GOOGLE_TEXT_SIGNATURE_KEY) is not None
        )
    )


def stamp_produced_by(response: Any, profile: Any) -> int:
    """Stamp every thinking part and Gemini signed text part of ``response`` with the model that
    produced it. Returns how many parts were stamped. Never overwrites an existing stamp."""
    from matrx_ai.config.unified_content import ThinkingContent

    stamp = produced_by(profile)
    if stamp is None:
        return 0
    stamped = 0
    for message in getattr(response, "messages", None) or []:
        for part in getattr(message, "content", None) or []:
            if not (isinstance(part, ThinkingContent) or _is_signed_text(part)):
                continue
            metadata = getattr(part, "metadata", None)
            if not isinstance(metadata, dict):
                part.metadata = metadata = {}
            if PRODUCED_BY_KEY not in metadata:
                metadata[PRODUCED_BY_KEY] = dict(stamp)
                stamped += 1
    return stamped


def _wire_family(profile: Any) -> str | None:
    """The provider family the outgoing translator speaks (``anthropic_chat`` → ``anthropic``)."""
    wire_format = str(getattr(profile, "wire_format", "") or "")
    if wire_format.endswith("_chat"):
        return wire_format[: -len("_chat")]
    return str(getattr(profile, "vendor", "") or "") or None


def _outgoing_label(profile: Any, config: Any) -> str:
    return str(
        getattr(profile, "model_name", None)
        or getattr(config, "matrx_model_name", None)
        or getattr(config, "model", None)
        or "?"
    )


def _same_model(stamp: dict[str, Any], profile: Any, config: Any) -> bool:
    """Exact model identity when both sides have it; otherwise any shared name/id."""
    if profile is not None and stamp.get("model_id") and getattr(profile, "model_id", None):
        return str(stamp["model_id"]) == str(profile.model_id)
    if profile is not None:
        outgoing = {getattr(profile, "model_name", None), getattr(profile, "provider_model_id", None)}
    else:
        outgoing = {getattr(config, "model", None), getattr(config, "matrx_model_name", None)}
    stamped = {stamp.get("model"), stamp.get("model_id"), stamp.get("provider_model_id")}
    return bool({str(n) for n in outgoing if n} & {str(s) for s in stamped if s})


def _is_template(message: Any) -> bool:
    from matrx_ai.config.cache_marks import TEMPLATE_METADATA_KEY

    metadata = getattr(message, "metadata", None)
    return isinstance(metadata, dict) and bool(metadata.get(TEMPLATE_METADATA_KEY))


def _decide(part: Any, profile: Any, config: Any) -> tuple[str, str | None]:
    """``(action, note)`` for one part of a template message.

    action: ``keep`` | ``drop`` (remove the thinking part) | ``unsign`` (copy of the text part
    without its Gemini signature) | ``restore`` (copy of the text part with its stored signature
    back on the live key — same model only)."""
    from matrx_ai.config.unified_content import ThinkingContent

    is_thinking = isinstance(part, ThinkingContent)
    if not (is_thinking or _is_signed_text(part)):
        return "keep", None
    what = "template thinking" if is_thinking else "template text signature"
    metadata = getattr(part, "metadata", None) or {}
    stamp = metadata.get(PRODUCED_BY_KEY) if isinstance(metadata, dict) else None
    outgoing = _outgoing_label(profile, config)
    if isinstance(stamp, dict) and stamp:
        if _same_model(stamp, profile, config):
            if not is_thinking and metadata.get(GOOGLE_TEXT_SIGNATURE_KEY) is None:
                return "restore", None
            return "keep", None
        source = stamp.get("model") or stamp.get("model_id") or "?"
        action = "drop" if is_thinking else "unsign"
        return action, (
            f"{what} from {source} dropped (model changed to {outgoing}); static seal break expected"
        )
    # No produced_by: a part saved before stamping existed.
    if not is_thinking:
        # Unstamped: today's behaviour stands (a live-key signature goes as before; a stored one
        # is never restored without knowing which model wrote it).
        return "keep", None
    if profile is None:
        # The outgoing model's provider is unknown (``apply_template_thinking`` could not resolve
        # it): fail closed — kept, a foreign part would reach ``to_<provider>`` and go as TEXT.
        return "drop", (
            f"{what} with no produced_by dropped (the outgoing model {outgoing} could not be "
            "resolved to a provider); static seal break expected"
        )
    family = _wire_family(profile)
    if family and getattr(part, "provider", None) == family:
        return "keep", f"{what} with no produced_by kept (same provider {family})"
    return "drop", (
        f"{what} with no produced_by from provider {getattr(part, 'provider', None) or '?'} dropped "
        f"(sending to {outgoing}); static seal break expected"
    )


def drop_foreign_template_thinking(prep: Any, config: Any, profile: Any) -> list[str]:
    """THE send-boundary step. Reads the wire copy when one exists, writes only a wire copy.

    Returns the notes recorded for this send (also on AppContext ``metadata["template_thinking"]``).
    """
    from matrx_ai.config.send_boundary import _wire_list

    source = prep.wire_config if prep.wire_config is not None else config
    messages = getattr(source, "messages", None)
    listed = list(messages or [])
    notes: list[str] = []
    out: list[Any] = []
    changed = False
    for message in listed:
        if not _is_template(message):
            out.append(message)
            continue
        kept: list[Any] = []
        touched = False
        for part in getattr(message, "content", None) or []:
            action, note = _decide(part, profile, config)
            if note:
                notes.append(note)
            if action == "drop":
                touched = True
                continue
            if action == "unsign":
                touched = True
                part = copy(part)
                part.metadata = {
                    k: v
                    for k, v in (part.metadata or {}).items()
                    if k not in (GOOGLE_TEXT_SIGNATURE_KEY, STORED_GOOGLE_TEXT_SIGNATURE_KEY)
                }
            elif action == "restore":
                touched = True
                part = copy(part)
                part.metadata = dict(part.metadata or {})
                part.metadata[GOOGLE_TEXT_SIGNATURE_KEY] = part.metadata[STORED_GOOGLE_TEXT_SIGNATURE_KEY]
            kept.append(part)
        if not touched:
            out.append(message)
            continue
        changed = True
        if not kept:
            notes.append(
                f"template {getattr(message, 'role', 'message')} turn held only foreign thinking and is "
                "left off this send"
            )
            continue
        replacement = copy(message)
        replacement.content = kept
        out.append(replacement)

    if changed:
        wire = prep.wire_config if prep.wire_config is not None else copy(config)
        wire.messages = _wire_list(messages, out)
        prep.wire_config = wire
        prep.steps.append(STEP_NAME)
    if notes:
        _record(prep, notes)
    return notes


def _has_template_thinking(prep: Any, config: Any) -> bool:
    from matrx_ai.config.unified_content import ThinkingContent

    source = prep.wire_config if prep.wire_config is not None else config
    return any(
        isinstance(part, ThinkingContent) or _is_signed_text(part)
        for message in list(getattr(source, "messages", None) or [])
        if _is_template(message)
        for part in getattr(message, "content", None) or []
    )


async def _resolve_profile(config: Any) -> Any:
    """The outgoing model's call profile from ``config.model`` (the catalog's one resolver, as
    ``send_boundary._send_profile`` does), or ``None`` when it cannot be resolved."""
    from matrx_ai.catalog.resolve import resolve_call_profile
    from matrx_ai.config.served_via import served_via_kwargs

    try:
        return await resolve_call_profile(
            str(getattr(config, "model", "") or ""),
            offering_id=getattr(config, "routing_offering_id", None),
            **served_via_kwargs(config),
        )
    except Exception as exc:  # noqa: BLE001 — unresolved = unknown provider: the step fails closed
        logger.warning("template_thinking: the outgoing model %r did not resolve: %r", getattr(config, "model", None), exc)
        return None


def _fail_closed(prep: Any, config: Any) -> list[str]:
    """The step itself failed: no template thinking part and no template text signature goes out
    (a foreign one would otherwise reach ``to_<provider>`` and go as visible TEXT). Wire copy only."""
    from matrx_ai.config.send_boundary import _wire_list
    from matrx_ai.config.unified_content import ThinkingContent

    source = prep.wire_config if prep.wire_config is not None else config
    messages = getattr(source, "messages", None)
    out: list[Any] = []
    removed = 0
    for message in list(messages or []):
        if not _is_template(message):
            out.append(message)
            continue
        kept: list[Any] = []
        for part in getattr(message, "content", None) or []:
            if isinstance(part, ThinkingContent):
                removed += 1
                continue
            if _is_signed_text(part):
                removed += 1
                part = copy(part)
                part.metadata = {
                    k: v
                    for k, v in (part.metadata or {}).items()
                    if k not in (GOOGLE_TEXT_SIGNATURE_KEY, STORED_GOOGLE_TEXT_SIGNATURE_KEY)
                }
            kept.append(part)
        if kept:
            replacement = copy(message)
            replacement.content = kept
            out.append(replacement)
    if not removed:
        return []
    wire = prep.wire_config if prep.wire_config is not None else copy(config)
    wire.messages = _wire_list(messages, out)
    prep.wire_config = wire
    prep.steps.append(f"{STEP_NAME}:fail_closed")
    return [f"template thinking step failed; {removed} template thinking/signature part(s) left off this send (fail closed); static seal break expected"]


async def apply_template_thinking(prep: Any, config: Any, profile: Any) -> list[str]:
    """THE send-boundary entry. Resolves the outgoing profile when the boundary has none, runs
    ``drop_foreign_template_thinking``, and FAILS CLOSED: if the step raises, every template
    thinking part and text signature is left off this send (never passed through as text)."""
    try:
        if profile is None and _has_template_thinking(prep, config):
            profile = await _resolve_profile(config)
        return drop_foreign_template_thinking(prep, config, profile)
    except Exception as exc:  # noqa: BLE001 — fail closed for template thinking, never the send
        logger.error("send_boundary %s failed: %s: %s", STEP_NAME, type(exc).__name__, exc, exc_info=True)
        try:
            notes = _fail_closed(prep, config)
        except Exception as closed_exc:  # noqa: BLE001 — never breaking a send outranks the rare leak
            logger.critical("send_boundary %s fail-closed path failed too", STEP_NAME, exc_info=True)
            prep.steps.append(f"{STEP_NAME}:failed_open")
            notes = [
                f"template thinking step and its fail-closed path both failed ({type(exc).__name__}, "
                f"{type(closed_exc).__name__}); this send goes out as before the step existed"
            ]
        if notes:
            _record(prep, notes)
        return notes


def _record(prep: Any, notes: list[str]) -> None:
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if ctx is not None:
        ctx.metadata[STEP_NAME] = list(notes)
    for note in notes:
        vcprint(f"[send_boundary/{getattr(prep, 'stage', '?')}] {note}", color="yellow")
        logger.info("send_boundary %s: %s", STEP_NAME, note)


__all__ = [
    "GOOGLE_TEXT_SIGNATURE_KEY",
    "apply_template_thinking",
    "PRODUCED_BY_KEY",
    "STEP_NAME",
    "STORED_GOOGLE_TEXT_SIGNATURE_KEY",
    "drop_foreign_template_thinking",
    "produced_by",
    "stamp_produced_by",
]
