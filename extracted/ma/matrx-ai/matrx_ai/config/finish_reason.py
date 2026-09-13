from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from matrx_utils import vcprint


class FinishReason(StrEnum):
    """Unified finish reasons across all providers"""

    # Success cases
    STOP = "stop"
    MAX_TOKENS = "max_tokens"

    # Tool/function related
    TOOL_CALLS = "tool_calls"
    MALFORMED_FUNCTION_CALL = "malformed_function_call"
    UNEXPECTED_TOOL_CALL = "unexpected_tool_call"

    # Content filtering / Safety
    CONTENT_FILTER = "content_filter"
    SAFETY = "safety"
    RECITATION = "recitation"
    PROHIBITED_CONTENT = "prohibited_content"
    SPII = "spii"

    # Image generation specific
    IMAGE_SAFETY = "image_safety"
    IMAGE_PROHIBITED_CONTENT = "image_prohibited_content"
    NO_IMAGE = "no_image"
    IMAGE_RECITATION = "image_recitation"

    # Anthropic-specific
    REFUSAL = "refusal"
    MODEL_CONTEXT_WINDOW_EXCEEDED = "model_context_window_exceeded"

    # Other
    LANGUAGE = "language"
    BLOCKLIST = "blocklist"
    END_TURN = "end_turn"
    ERROR = "error"
    OTHER = "other"

    def is_success(self) -> bool:
        """Returns True if the model completed naturally with no truncation or errors."""
        return self in {
            self.STOP,
            self.TOOL_CALLS,
            self.END_TURN,
        }

    def is_truncated(self) -> bool:
        """Returns True if the response was cut short by a token limit.

        MAX_TOKENS means the model hit the output cap and stopped mid-response —
        this is NOT a success. The output is incomplete and the caller must be
        notified so the user isn't silently handed a truncated answer.
        """
        return self == self.MAX_TOKENS

    def is_retryable(self) -> bool:
        """Returns True if this error can be retried."""
        return self in {
            self.MALFORMED_FUNCTION_CALL,
            self.UNEXPECTED_TOOL_CALL,
        }

    def is_error(self) -> bool:
        """Returns True if this is a fatal error that should stop execution."""
        return self in {
            self.CONTENT_FILTER,
            self.SAFETY,
            self.RECITATION,
            self.PROHIBITED_CONTENT,
            self.SPII,
            self.IMAGE_SAFETY,
            self.IMAGE_PROHIBITED_CONTENT,
            self.NO_IMAGE,
            self.IMAGE_RECITATION,
            self.LANGUAGE,
            self.BLOCKLIST,
            self.ERROR,
            self.REFUSAL,
            self.MODEL_CONTEXT_WINDOW_EXCEEDED,
            # Retryable errors also count as errors (after retry exhaustion)
            self.MALFORMED_FUNCTION_CALL,
            self.UNEXPECTED_TOOL_CALL,
        }

    @classmethod
    def from_google(cls, google_reason: Any) -> "FinishReason":
        """Convert Google finish reason to unified format"""
        if not google_reason:
            return cls.STOP

        reason_str = str(google_reason).upper()
        if "." in reason_str:
            reason_str = reason_str.split(".")[-1]

        mapping = {
            "STOP": cls.STOP,
            "MAX_TOKENS": cls.MAX_TOKENS,
            "SAFETY": cls.SAFETY,
            "RECITATION": cls.RECITATION,
            "LANGUAGE": cls.LANGUAGE,
            "BLOCKLIST": cls.BLOCKLIST,
            "PROHIBITED_CONTENT": cls.PROHIBITED_CONTENT,
            "SPII": cls.SPII,
            "MALFORMED_FUNCTION_CALL": cls.MALFORMED_FUNCTION_CALL,
            "UNEXPECTED_TOOL_CALL": cls.UNEXPECTED_TOOL_CALL,
            "IMAGE_SAFETY": cls.IMAGE_SAFETY,
            "IMAGE_PROHIBITED_CONTENT": cls.IMAGE_PROHIBITED_CONTENT,
            "NO_IMAGE": cls.NO_IMAGE,
            "IMAGE_RECITATION": cls.IMAGE_RECITATION,
            "OTHER": cls.OTHER,
            "FINISH_REASON_UNSPECIFIED": cls.STOP,
        }
        return mapping.get(reason_str, cls.OTHER)

    @classmethod
    def from_anthropic(cls, stop_reason: str) -> "FinishReason":
        if stop_reason == "end_turn":
            return cls.STOP
        elif stop_reason == "max_tokens":
            return cls.MAX_TOKENS
        elif stop_reason == "tool_use":
            return cls.TOOL_CALLS
        elif stop_reason == "stop_sequence":
            return cls.STOP
        elif stop_reason == "refusal":
            return cls.REFUSAL
        elif stop_reason == "model_context_window_exceeded":
            return cls.MODEL_CONTEXT_WINDOW_EXCEEDED
        else:
            vcprint(stop_reason, "WARNING: Unknown Anthropic stop reason", color="yellow")
            return cls.OTHER

    @classmethod
    def to_anthropic(cls, finish_reason: "FinishReason") -> str:
        if finish_reason == cls.STOP:
            return "stop_sequence"
        elif finish_reason == cls.MAX_TOKENS:
            return "max_tokens"
        elif finish_reason == cls.TOOL_CALLS:
            return "tool_use"
        else:
            vcprint(
                finish_reason,
                "WARNING: Unknown Anthropic finish reason",
                color="yellow",
            )
            return "other_reason"


# ---------------------------------------------------------------------------
# Truncation — saying it out loud
#
# THE DEFECT THIS CLOSES (live, 2026-09-11, the Masterwork Conductor): a turn
# that was writing a large tool call hit the output ceiling at exactly its
# max_output_tokens. The provider returned stop_reason=max_tokens with an
# INCOMPLETE tool_use block, which the parser dropped — so the turn persisted
# as thinking + text with zero tool calls, the save never happened, and the
# person watching saw "Using tool workflow_author" and then nothing at all.
#
# Nothing fails silently. A turn that ran out of room says so IN the
# conversation, names the tool whose call died with it, and says plainly that
# nothing was saved — and the stored message carries a marker so the UI can
# badge it without re-deriving any of this.
# ---------------------------------------------------------------------------

#: Assistant-message metadata key stamped on a turn cut off by the output cap.
#: Value shape: {"reason": "max_tokens", "model": str, "max_output_tokens":
#: int | None, "interrupted_tool_calls": list[str]}.
TRUNCATION_METADATA_KEY = "truncation"

#: Request-metadata key a caller sets to ``False`` when there is NOWHERE to
#: continue — a workflow step, a batch job, any call with no conversation a
#: person can prompt again. Absent means ``True`` (a conversation), which is
#: every historical caller, so the default behaviour is unchanged.
#:
#: THE DEFECT THIS CLOSES (live 2026-09-12, workflow run
#: 2cf711eb-1a15-49ed-baf7-ddb166dba129, step "Montessori asks"): a prose step
#: was cut at 1,200 tokens and the platform honestly said so — then offered
#: *"Ask me to continue and I'll pick up where it cut off"* to a parent sitting
#: inside a workflow run, where there is no me to ask and no way to ask it. A
#: remedy nobody can perform is not honesty; it is a dead control wearing a
#: helpful sentence (root CLAUDE.md: *a screen never lies*).
CONTINUABLE_METADATA_KEY = "continuable"


def interrupted_tool_names(raw_response: Any = None, messages: Any = None) -> list[str]:
    """Names of tool calls that were in flight when the turn was cut off.

    Looks at BOTH the parsed messages and the provider's raw content blocks on
    purpose: a tool call truncated mid-arguments is exactly the one the parser
    throws away, so the raw blocks are the only place it still exists. Names
    are de-duplicated, order preserved. Never raises — a diagnostic that
    crashes the turn it is describing would be worse than the silence.
    """
    found: list[str] = []

    def _add(name: Any) -> None:
        if isinstance(name, str) and name.strip() and name not in found:
            found.append(name)

    try:
        items = messages if isinstance(messages, list) else ([messages] if messages else [])
        for message in items:
            for block in getattr(message, "content", None) or []:
                if getattr(block, "type", None) in ("tool_call", "function_call"):
                    _add(getattr(block, "name", None))
    except Exception:  # noqa: BLE001 — best effort by contract
        pass

    try:
        blocks: Any = None
        if isinstance(raw_response, dict):
            blocks = raw_response.get("content")
            if blocks is None and isinstance(raw_response.get("message"), dict):
                blocks = raw_response["message"].get("content")
        for block in blocks or []:
            if not isinstance(block, dict):
                continue
            # Anthropic `tool_use`, OpenAI `function_call`/`tool_call`.
            if block.get("type") in ("tool_use", "tool_call", "function_call"):
                _add(block.get("name") or (block.get("function") or {}).get("name"))
    except Exception:  # noqa: BLE001
        pass

    return found


def truncation_notice(
    *,
    model: str | None = None,
    max_output_tokens: int | None = None,
    interrupted_tool_calls: list[str] | None = None,
    continuable: bool = True,
) -> str:
    """The honest sentence a person reads when a turn ran out of room.

    Plain language, no codes, no paths — it is addressed to the person in the
    conversation, and it always says what happened to the work.

    ``continuable`` is whether the reader can actually do the thing the remedy
    names. In a conversation they can: "ask me to continue" is a real control.
    In a workflow run there is no conversation and no next turn, so offering it
    is a lie — the honest remedy there names the step's limit and who can raise
    it. See ``CONTINUABLE_METADATA_KEY``.
    """
    tools = [t for t in (interrupted_tool_calls or []) if t]
    if tools:
        named = tools[0] if len(tools) == 1 else ", ".join(tools)
        retry = (
            "Nothing on your side is broken — I just need to do it in smaller pieces. "
            "Let me try again with a smaller change."
            if continuable
            else "Nothing on your side is broken, and this step cannot retry itself — "
            "whoever built this workflow needs to raise the step's output limit."
        )
        return (
            f"My reply ran out of room before I finished calling `{named}`, so that "
            f"call never went through and nothing was saved. {retry}"
        )
    limit = f" (the limit is {max_output_tokens:,} tokens)" if max_output_tokens else ""
    if not continuable:
        return (
            f"This step's reply was cut off at its output limit{limit} and stopped "
            "part-way, so what you see above is incomplete. There is no way to ask it "
            "to continue from inside a workflow run — whoever built this workflow "
            "needs to raise this step's output limit."
        )
    return (
        f"My reply ran out of room{limit} and stopped part-way, so what you see above "
        "is incomplete. Ask me to continue and I'll pick up where it cut off."
    )


def truncation_marker(
    *,
    model: str | None = None,
    max_output_tokens: int | None = None,
    interrupted_tool_calls: list[str] | None = None,
) -> dict[str, Any]:
    """The metadata a truncated assistant message carries, so the UI can badge
    it without re-deriving anything."""
    return {
        "reason": str(FinishReason.MAX_TOKENS),
        "model": model or "unknown model",
        "max_output_tokens": max_output_tokens,
        "interrupted_tool_calls": [t for t in (interrupted_tool_calls or []) if t],
    }


# ---------------------------------------------------------------------------
# THE OUTPUT-CEILING CLASSIFIER — one place that answers "was this cut off?"
#
# THE DEFECT THIS CLOSES (live, 2026-09-12, workflow run
# 23e72bf5-8b41-496e-a475-428f880d219f, step "The evidence ledger"): a saved
# agent with a declared structured output hit exactly 32,000 output tokens
# (claude-sonnet-5, finish_reason=max_tokens). The JSON was therefore
# incomplete, and the workflow node reported
# ``structured_output_invalid: "AI completed, but its declared structured
# output could not be parsed and validated."`` — a sentence that names the
# wrong cause and offers no remedy. Same masking class as night-1 walls W9
# ("the model returned no output text") and W17 (a provider parameter
# rejection reported as "no output"): the node had the truth in hand and
# reported something else.
#
# So: every post-call parse/validate failure asks THIS first. If the
# completion ran out of room, the failure is a truncation with the ceiling and
# the token count in it; the parse-failure wording is kept for genuinely
# malformed output.
# ---------------------------------------------------------------------------

#: Every spelling of "the model ran out of output room" across providers.
TRUNCATION_FINISH_REASONS: frozenset[str] = frozenset(
    {"max_tokens", "length", "max_completion_tokens", "model_max_tokens"}
)


@dataclass(frozen=True)
class OutputCeiling:
    """The facts about a reply cut short at its output limit."""

    finish_reason: str
    model: str | None = None
    max_output_tokens: int | None = None
    output_tokens: int | None = None
    interrupted_tool_calls: tuple[str, ...] = ()

    def as_details(self) -> dict[str, Any]:
        """The structured half a node failure carries in ``details``."""
        return {
            "finish_reason": self.finish_reason,
            "model": self.model or "",
            "max_output_tokens": self.max_output_tokens,
            "output_tokens": self.output_tokens,
            "interrupted_tool_calls": list(self.interrupted_tool_calls),
        }


def _is_truncation_reason(value: Any) -> bool:
    if value is None:
        return False
    text = str(value).strip().lower()
    if not text:
        return False
    if "." in text:  # FinishReason.MAX_TOKENS / enum reprs
        text = text.rsplit(".", 1)[-1]
    return text in TRUNCATION_FINISH_REASONS


def completion_truncation(source: Any) -> OutputCeiling | None:
    """Was this completion cut off at the model's output ceiling?

    Accepts anything that carries the facts — a ``CompletedRequest`` (the
    orchestrator's own return), a normalized ``AiExecutionResult``, or a bare
    response object — and reads them defensively, by attribute, in the same
    spirit as ``graph_nodes.shared``: a classifier that raises while
    describing a failure would be worse than the silence it replaces.

    Returns ``None`` when the turn was NOT truncated (including when nothing
    in the object says either way — absence of evidence is never a truncation
    claim).
    """
    try:
        meta = getattr(source, "metadata", None)
        meta = dict(meta) if isinstance(meta, dict) else {}
        marker = meta.get(TRUNCATION_METADATA_KEY)
        marker = marker if isinstance(marker, dict) else {}

        final_response = getattr(source, "final_response", None)
        finish_candidates = [
            getattr(source, "finish_reason", None),
            getattr(final_response, "finish_reason", None) if final_response is not None else None,
            meta.get("finish_reason"),
            marker.get("reason"),
        ]
        finish = next((c for c in finish_candidates if _is_truncation_reason(c)), None)
        status_says = str(meta.get("status") or "").lower() == "truncated"
        type_says = str(meta.get("error_type") or "").lower() == "truncated_response"

        # THE SECOND, INDEPENDENT LAYER (PRINCIPLES.md: a class is not dead
        # until two layers each stop it alone). Every leg above believes the
        # provider's own finish_reason. When NOTHING says either way — the
        # provider was silent, or the reason was lost crossing a seam —
        # ARITHMETIC still knows: a completion that produced exactly (or more
        # than) the tokens it was permitted did not stop because it was
        # finished. Live 2026-09-12, run 2cf711eb…, step `read_case`:
        # output_tokens 2500, max_output_tokens 2500, reported to a parent as
        # "its declared structured output could not be parsed" — the wrong
        # cause, with no remedy in it.
        #
        # IT NEVER OVERRULES A PROVIDER THAT SPOKE. A model asked for 32,000
        # tokens may legitimately finish on its own at exactly 32,000, and a
        # declared `stop` / `end_turn` / `tool_calls` says so; calling that
        # truncated would invent a failure, which is the mirror of the defect
        # this closes. So the leg fires ONLY when no finish reason was declared
        # at all.
        declared_finish = next((c for c in finish_candidates if c not in (None, "")), None)
        request = getattr(source, "request", None)
        config = getattr(request, "config", None) if request is not None else None
        permitted = marker.get("max_output_tokens")
        if permitted is None:
            permitted = getattr(config, "max_output_tokens", None)
        produced = _output_tokens_of(source)
        spent_it_all = (
            declared_finish is None
            and isinstance(permitted, int | float)
            and isinstance(produced, int | float)
            and permitted > 0
            and produced >= permitted
        )

        if finish is None and not (status_says or type_says or marker or spent_it_all):
            return None
        finish_text = str(finish or marker.get("reason") or FinishReason.MAX_TOKENS)
        if "." in finish_text:
            finish_text = finish_text.rsplit(".", 1)[-1]

        model = marker.get("model") or getattr(config, "model", None) or meta.get("model")
        ceiling = permitted

        tools = marker.get("interrupted_tool_calls")
        tools = tuple(t for t in tools if isinstance(t, str) and t) if isinstance(tools, list) else ()

        return OutputCeiling(
            finish_reason=finish_text.lower(),
            model=str(model) if model else None,
            max_output_tokens=int(ceiling) if isinstance(ceiling, int | float) else None,
            output_tokens=_output_tokens_of(source),
            interrupted_tool_calls=tools,
        )
    except Exception:  # noqa: BLE001 — by contract: never fail the failure
        return None


def _output_tokens_of(source: Any) -> int | None:
    """Billed output tokens, from either usage shape (aggregate or normalized)."""
    for holder in (
        getattr(source, "total_usage", None),
        getattr(source, "usage", None),
    ):
        if holder is None:
            continue
        total = getattr(holder, "total", None)
        for candidate in (total, holder):
            value = getattr(candidate, "output_tokens", None) if candidate is not None else None
            if isinstance(value, int | float) and value:
                return int(value)
        if isinstance(holder, dict) and isinstance(holder.get("output_tokens"), int | float):
            return int(holder["output_tokens"])
    return None


def output_ceiling_message(ceiling: OutputCeiling, *, what: str = "the answer") -> str:
    """The sentence a person reads, with the remedy in it.

    Names the limit when we know it, the tokens actually produced when we
    don't, and always says what to do next — this is the half the masked
    parse-failure wording never had.
    """
    if ceiling.max_output_tokens:
        limit = f" ({ceiling.max_output_tokens:,} tokens)"
    elif ceiling.output_tokens:
        limit = f" (it produced {ceiling.output_tokens:,} tokens)"
    else:
        limit = ""
    tools = ", ".join(ceiling.interrupted_tool_calls)
    dropped = f" The in-flight call to {tools} was dropped and never ran." if tools else ""
    return (
        f"The AI's reply was cut off at its output limit{limit} before it finished "
        f"{what}.{dropped} Split the input into smaller pieces or raise the step's "
        "output limit."
    )
