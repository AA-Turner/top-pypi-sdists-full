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

from matrx_ai.config.context_trim import CHARS_PER_TOKEN_ESTIMATE

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
# ``prompt_preflight.context_window_trip_fraction`` (org-overridable,
# ``propagation = next_load``), seeded by aidream's
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


def estimate_prompt_tokens(config: Any) -> int:
    """Rough token count of everything this config puts on the wire.

    System instruction + messages + tool definitions, at
    ``CHARS_PER_TOKEN_ESTIMATE`` chars per token — the same divisor the trim
    gate uses, so the two systems never disagree about how big something is.
    """
    total = _chars(getattr(config, "system_instruction", None))
    messages = getattr(config, "messages", None)
    if messages is not None:
        try:
            for message in messages:
                total += _chars(message)
        except TypeError:  # not iterable — measure it whole
            total += _chars(messages)
    tools = getattr(config, "tools", None)
    if tools:
        total += _chars(tools)
    return int(total / CHARS_PER_TOKEN_ESTIMATE)


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
