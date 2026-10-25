"""PROMPT PRE-FLIGHT — measure the prompt against the model's window BEFORE the call.

The hole this closes (live, 2026-09-12, workflow run ``cdde033d``): a For-Each
ran four ledger agents over four documents, a Gather collected them, and a
merge step was handed the WHOLE per-document AI results — each carrying its
``messages`` history (the documents themselves), usage and metadata, several
times over. Nothing between the graph and Anthropic measured that prompt. The
first thing that noticed was the provider, six steps in::

    prompt is too long: 1,019,616 tokens > 1,000,000 maximum

— a refusal with no step name, no field name and no remedy, after the run had
already spent four agents' worth of output tokens.

So the send boundary measures first. This is a REFUSAL, never a trim: nothing
here shortens a prompt (``trim_messages_context`` stays the one trimmer, called
from the one place). A prompt that cannot fit is an authoring defect upstream —
almost always an edge mapping carrying whole results where it should carry a
field — and the error says exactly that, names the step, and costs nothing.

Unmeasurable is announced, never assumed: a model whose catalog row declares no
``context_window`` is reported once (yellow) and passed through. A guessed
ceiling would be the worse failure — it would refuse calls the provider would
have served.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any

from matrx_utils import vcprint

from matrx_ai.config.context_trim import estimate_budget_tokens

logger = logging.getLogger(__name__)

# THE KNOB (agent-set starting value, Claude 2026-09-12; review 2026-12-12).
#
# The estimate is chars/4 — deliberately rough, and rough in BOTH directions
# per tokenizer and language. ``trip_fraction`` is the tolerance: the pre-flight
# refuses only when the estimate exceeds this multiple of the declared window.
# 1.0 with a chars/4 estimator that runs ~5-10% low in practice means a prompt
# has to be genuinely, obviously over the ceiling before a call is refused —
# an over-window prompt the provider WOULD have refused anyway. Raise it if a
# legitimate near-window prompt is ever refused here; lower it (0.9) to refuse
# earlier, before the provider's own hard edge.
#
# It is a ROW, not a constant: ``platform.feature_knob``
# ``prompt_preflight.context_window_trip_fraction`` (PLATFORM-LOCKED —
# ``overridable_by = '{}'``; this comment said "org-overridable" until
# 2026-09-20 and that was never achievable, because the value below is
# process-global state shared by every tenant in the process, so the last
# injection wins for everybody, ``propagation = next_load``), seeded by aidream's
# ``db/migrations/0644_prompt_preflight_trip_fraction_knob.sql`` and injected at
# boot through ``configure_context_preflight``
# (``aidream/startup/preflight_knob.py``). The package cannot read our database,
# so these values are what applies until the host injects — never a second
# opinion about the limit.
DEFAULT_TRIP_FRACTION = 1.0
DEFAULT_ENABLED = True


@dataclass
class PreflightPolicy:
    enabled: bool = DEFAULT_ENABLED
    trip_fraction: float = DEFAULT_TRIP_FRACTION


_POLICY = PreflightPolicy()
_UNMEASURABLE_ANNOUNCED: set[str] = set()


def configure_context_preflight(
    *, enabled: bool | None = None, trip_fraction: float | None = None
) -> None:
    """Host seam for the knob — injection, never an env read inside the package."""
    if enabled is not None:
        _POLICY.enabled = bool(enabled)
    if trip_fraction is not None and trip_fraction > 0:
        _POLICY.trip_fraction = float(trip_fraction)


def current_policy() -> PreflightPolicy:
    return PreflightPolicy(enabled=_POLICY.enabled, trip_fraction=_POLICY.trip_fraction)


class PromptTooLargeError(ValueError):
    """The prompt cannot fit the model's context window. Raised BEFORE the call.

    Carries the numbers so a caller (a workflow step's failure record, a chat
    error surface) can render them without re-parsing the message.
    """

    def __init__(
        self,
        *,
        step: str,
        model: str,
        estimated_tokens: int,
        context_window: int,
        remedy: str,
    ) -> None:
        self.step = step
        self.model = model
        self.estimated_tokens = estimated_tokens
        self.context_window = context_window
        self.remedy = remedy
        super().__init__(
            f"Prompt pre-flight REFUSED this call before the provider: step "
            f"{step!r} would send an estimated {estimated_tokens:,} tokens to "
            f"'{model}', whose context window is {context_window:,}. Nothing was "
            f"sent and nothing was spent. {remedy}"
        )


REMEDY = (
    "Remedy: a mapping is passing whole results — select the field. Point the "
    "edge at the field the next step needs (e.g. "
    "'structured_output.entries', or a Gather's 'structured_outputs' / "
    "'final_texts' instead of its raw 'values'), or split the input across "
    "steps so each call carries one document's worth."
)


def _chars(value: Any) -> int:
    """Serialized size of any prompt part — strings as-is, structures as JSON."""
    if value is None:
        return 0
    if isinstance(value, str):
        return len(value)
    if isinstance(value, (int, float, bool)):
        return len(str(value))
    dump = getattr(value, "model_dump_json", None)
    if callable(dump):
        try:
            return len(dump())
        except Exception:  # noqa: BLE001 — fall through to the generic path
            pass
    try:
        return len(json.dumps(value, default=str))
    except Exception:  # noqa: BLE001 — an unserializable part is not measurable
        return len(str(value))


#: Storage keys that carry bytes the model never reads as prompt text: a thinking block's
#: provider signature and inline media bytes (an image is billed by its pixels, not its base64).
_OPAQUE_KEYS = frozenset({"signature", "signature_encoding", "base64_data"})


def _block_chars(block: Any) -> int:
    """One content block as the model reads it: its storage form (the JSON the wire carries),
    never its ``repr`` — ``TextContent.__repr__`` cuts the text to 70 characters."""
    to_storage = getattr(block, "to_storage_dict", None)
    if callable(to_storage):
        try:
            stored = to_storage()
        except Exception:  # noqa: BLE001 — fall back to measuring the block whole
            stored = None
        if isinstance(stored, dict):
            return _chars({k: v for k, v in stored.items() if k not in _OPAQUE_KEYS})
    return _chars(block)


def _message_chars(message: Any) -> int:
    """A message the model is shown: its role and every content block. A message hidden from
    the model (``is_visible_to_model=False``) is never sent, so it counts nothing."""
    if getattr(message, "is_visible_to_model", True) is False:
        return 0
    content = getattr(message, "content", None)
    if not isinstance(content, list) or not hasattr(message, "role"):
        return _chars(message)  # a plain dict / str message — measured as given
    role = getattr(message, "role", "")
    return len(str(getattr(role, "value", role))) + sum(_block_chars(block) for block in content)


def _context_channel_chars(messages: Any) -> int:
    """The per-turn and tail context blocks a ``MessageList`` renders onto the wire at send."""
    total = 0
    for render in ("render_turn_context", "render_tail_context"):
        fn = getattr(messages, render, None)
        if callable(fn):
            try:
                total += _chars(fn())
            except Exception:  # noqa: BLE001 — a context block that cannot render is not sent
                pass
    return total


#: Model refs (and reasons) already announced, so a send path says each once per process.
_TOOL_MEASURE_ANNOUNCED: set[str] = set()
#: The declaration format used when the catalog cannot name this request's wire. Announced.
UNKNOWN_WIRE_TOOL_FORMAT = "anthropic"


def _announce_once(key: str, message: str) -> None:
    if key in _TOOL_MEASURE_ANNOUNCED:
        return
    _TOOL_MEASURE_ANNOUNCED.add(key)
    logger.warning(message)
    vcprint(message, color="yellow")


def _wire_tool_format(config: Any) -> str:
    """The declaration format this request's wire sends: the catalog's wire format for the model
    (its offering's ``ai.api.translator_key``) through the wire's own map. Announced, never silent,
    when the catalog cannot say."""
    from matrx_ai.providers.base_translator import tool_format_for_wire_format

    model_ref = str(getattr(config, "matrx_model_name", None) or getattr(config, "model", "") or "")
    # A device route sets its own format: llama-server always speaks OpenAI chat-completions,
    # and a person's own model file has no catalog offering to read one from (L5).
    if getattr(config, "served_via", None) is not None:
        return tool_format_for_wire_format("device_chat") or UNKNOWN_WIRE_TOOL_FORMAT
    wire_format = None
    try:
        from matrx_ai.catalog.manager import ai_catalog_manager

        wire_format = ai_catalog_manager.wire_format_for(
            model_ref, getattr(config, "routing_offering_id", None)
        )
    except Exception as exc:  # noqa: BLE001 — the catalog must never break a send
        logger.debug("prompt estimate could not read the catalog: %r", exc)
    tool_format = tool_format_for_wire_format(wire_format)
    if tool_format is None:
        _announce_once(
            f"format:{model_ref}:{wire_format}",
            f"[prompt estimate] the catalog names no tool-declaration format for model "
            f"{model_ref!r} (wire format {wire_format!r}); its tools are measured in the "
            f"{UNKNOWN_WIRE_TOOL_FORMAT!r} shape. Add the wire format to "
            "providers/base_translator.TOOL_FORMAT_BY_WIRE_FORMAT or fix the model's offering.",
        )
        tool_format = UNKNOWN_WIRE_TOOL_FORMAT
    return tool_format


def _tool_declarations_chars(config: Any) -> int:
    """Every tool declaration the request carries, as the provider receives it: registered names
    expanded through the registry (a request's projected agent tool first, as at dispatch), then
    inline tools, deduped across BOTH buckets by the wire's own rule (``first_declaration_per_name``
    — ``BaseTranslator.build_provider_tools``), in the format this request's wire sends. Measuring
    the names counted ~30,000 tokens of declarations as ~200. A name the registry cannot render is
    measured as the name, and that is announced."""
    names = list(getattr(config, "tools", None) or [])
    inline = list(getattr(config, "custom_tools", None) or [])
    if not names and not inline:
        return 0
    from matrx_ai.providers.base_translator import first_declaration_per_name

    tool_format = _wire_tool_format(config)
    registry = None
    lookup_projected = None
    try:
        from matrx_ai.tools.agent_projection import lookup_projected_tool
        from matrx_ai.tools.registry import ToolRegistry

        registry = ToolRegistry.get_instance()
        lookup_projected = lookup_projected_tool
    except Exception as exc:  # noqa: BLE001 — measuring must never break a send
        _announce_once(
            "registry:unreachable",
            f"[prompt estimate] the tool registry could not be reached ({exc!r}); registered "
            "tools are measured as their NAMES, so this estimate is low by their declarations.",
        )
    declarations: list[Any] = []
    unrendered: list[str] = []
    for name in names:
        if not isinstance(name, str):
            declarations.append(name)  # a declaration given as data is measured as given
            continue
        known = None
        try:
            known = (lookup_projected(name) if lookup_projected else None) or (
                registry.get(name) if registry is not None else None
            )
            if known is not None:
                declarations.append(known.get_provider_format(tool_format))
                continue
        except Exception as exc:  # noqa: BLE001 — unrenderable declaration: count the name
            logger.debug("prompt estimate could not render tool %r: %r", name, exc)
        unrendered.append(name)
        declarations.append({"name": name})
    for tool in inline:
        render = getattr(tool, "get_provider_format", None)
        try:
            declarations.append(render(tool_format) if callable(render) else tool)
        except Exception:  # noqa: BLE001
            declarations.append(tool)
    if unrendered and registry is not None:
        _announce_once(
            f"unrendered:{','.join(sorted(unrendered))[:200]}",
            f"[prompt estimate] {len(unrendered)} registered tool(s) could not be rendered from "
            f"the registry (loaded={getattr(registry, 'loaded', '?')}): {sorted(unrendered)[:10]}; "
            "they are measured as their NAMES, so this estimate is low by their declarations.",
        )
    kept, _dropped = first_declaration_per_name(declarations)
    return sum(_chars(decl) for decl in kept)


def estimate_prompt_tokens(config: Any) -> int:
    """Rough token count of everything this config puts on the wire.

    System instruction + every model-visible message (its content blocks in their storage form)
    + the context channel as prose; every tool declaration — registered names expanded through
    the registry, inline tools rendered — as structured payload. Through the ONE estimator
    (``estimate_budget_tokens``, the measured ratios the client and the Source input use). An
    under-count here promises a fit the provider then refuses, and tells the condense decision a
    conversation past its trigger is far below it, so the textbook 4 chars/token is never used,
    and nothing is measured through a debug ``repr``.
    """
    prose = _chars(getattr(config, "system_instruction", None))
    # The conversation's own instructions ride the wire after the system prompt (send_boundary).
    instructions = getattr(config, "conversation_instructions", None)
    if isinstance(instructions, str):
        prose += len(instructions)
    messages = getattr(config, "messages", None)
    if messages is not None:
        try:
            for message in messages:
                prose += _message_chars(message)
        except TypeError:  # not iterable — measure it whole
            prose += _chars(messages)
        prose += _context_channel_chars(messages)
    structured = _tool_declarations_chars(config)
    return estimate_budget_tokens(prose, "prose") + estimate_budget_tokens(structured, "structured")


def _declared_window(model_ref: str) -> int | None:
    try:
        from matrx_ai.catalog.manager import ai_catalog_manager

        return ai_catalog_manager.context_window(model_ref)
    except Exception as exc:  # noqa: BLE001 — the catalog must never break a send
        logger.debug("context pre-flight could not read the catalog: %r", exc)
        return None


def check_prompt_fits(config: Any, *, step: str) -> dict[str, Any] | None:
    """Refuse an over-window prompt before the provider sees it.

    Returns the measurement (for the audit) when the prompt fits or cannot be
    measured; raises :class:`PromptTooLargeError` when it provably does not.
    """
    if not _POLICY.enabled:
        return None
    model_ref = str(getattr(config, "matrx_model_name", None) or getattr(config, "model", "") or "")
    window = _declared_window(model_ref)
    if window is None:
        if model_ref and model_ref not in _UNMEASURABLE_ANNOUNCED:
            _UNMEASURABLE_ANNOUNCED.add(model_ref)
            vcprint(
                f"[send_boundary/preflight] '{model_ref}' declares no context_window "
                "in the catalog — this prompt was NOT measured against a window. "
                "Set ai.model_definition.context_window for it so an over-long "
                "prompt is refused here instead of by the provider.",
                color="yellow",
            )
        return None

    estimated = estimate_prompt_tokens(config)
    ceiling = int(window * _POLICY.trip_fraction)
    measurement = {
        "estimated_tokens": estimated,
        "context_window": window,
        "trip_fraction": _POLICY.trip_fraction,
        "model": model_ref,
        "step": step,
    }
    if estimated > ceiling:
        raise PromptTooLargeError(
            step=step,
            model=model_ref,
            estimated_tokens=estimated,
            context_window=window,
            remedy=REMEDY,
        )
    return measurement
