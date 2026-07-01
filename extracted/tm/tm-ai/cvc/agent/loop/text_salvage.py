"""Text-mode tool-call salvage for the CVC agent loop.

The structural problem
---------------------
The CVC gateway's SSE chat loop (`cvc/gateway.py:6240-6500`) collects
LLM responses via a streaming iterator. The provider is supposed to
emit structured ``tool_call_start`` / ``tool_call_delta`` events that
the loop turns into `cvc.agent.llm.ToolCall(id, name, arguments)`
objects. The loop body at line 6485 only dispatches tools if
``tool_calls`` is non-empty — if it's empty, the loop assumes the
turn is a final text response and breaks.

In practice, several classes of model misbehaviour land in the empty
``tool_calls`` branch and get treated as "done":

1. **Provider text-mode fallback** — some providers (notably Copilot
   routes and the Anthropic Sonnet streaming path) degrade to
   returning ``<tool_call>``` blocks in the assistant text when the
   structured tool-call channel errors mid-stream. The text shows up
   verbatim to the user (the screenshot the user shared shows
   ``<minimax>[<invoke name="list_dir">]`` rendered as text), the
   ``tool_calls`` list is empty, and the loop terminates without
   doing anything.

2. **Tool-call deltas that never produce a finalised event** — the
   streaming layer sometimes receives ``tool_call_start`` +
   ``tool_call_delta`` events that are buffered but never flushed to
   the dispatch path because the provider's "done" event lands with
   the args buffer still incomplete. The model emitted the intent;
   we just didn't finalise it.

3. **Stop reason confusion** — the provider returns ``finish_reason
   = "tool_calls"`` but the structured event list is empty. The text
   body contains the call. Same outcome as (1).

The screenshot evidence
-----------------------
The dashboard log the user shared in the very first turn was dominated
by the failure mode: the model emitted ``grep``, ``read_file``,
``list_dir`` as raw text in successive turns, each turn "completed"
without dispatching anything, and the task went nowhere. This module
is the fallback path that catches the misbehaviour and turns the
text-mode calls back into real dispatches.

Design
------
* :func:`extract_synthetic_tool_calls` — scans a text blob for one or
  more ``<tool_call>``` blocks and returns a list of synthetic
  ``ToolCall(id, name, arguments)`` objects. Each block's JSON
  argument is passed through :func:`repair_tool_call_arguments` so a
  truncated / fence-wrapped / quote-escaped block still produces a
  usable args dict.
* :func:`apply_salvage` — drop-in call site the gateway uses. Returns
  ``(calls, leftover_text)``: the list of synthetic calls AND the
  assistant text with the raw ``<tool_call>``` blocks stripped out (so
  the user doesn't see the XML in the chat body).
* :func:`strip_provider_tags` — removes provider-specific wire-format
  tokens like ``<minimax>`` / ``<|$text>`` that the streaming layer
  sometimes leaks into the assistant text. Cheap regex pass; no
  parsing.

Failure handling
----------------
The function NEVER raises. A malformed ``<tool_call>``` block that
can't be parsed is dropped from the synthetic-call list AND left in
the output text (rather than silently deleted) so the user can see
the model tried something. Errors are logged at WARNING level so
the dashboard can correlate them with the failed turn.

Why this is a loop primitive, not a tool
----------------------------------------
Salvage happens *after* the streaming layer has produced an empty
``tool_calls`` list and *before* the loop decides to break. It is
loop plumbing, not something the LLM calls. Putting it in ``loop/``
matches the dependency direction: ``gateway.py`` calls
``text_salvage.apply_salvage``, the salvage module calls nothing
tool-specific.
"""
from __future__ import annotations

import json
import logging
import re
import uuid
from dataclasses import dataclass
from typing import List, Optional, Tuple

from .sanitize import repair_tool_call_arguments

logger = logging.getLogger("cvc.agent.loop.text_salvage")

__all__ = [
    "SyntheticToolCall",
    "extract_synthetic_tool_calls",
    "apply_salvage",
    "strip_provider_tags",
]


# ── Synthetic ToolCall ─────────────────────────────────────────────


@dataclass
class SyntheticToolCall:
    """A tool call recovered from text-mode assistant output.

    Mirrors the shape of :class:`cvc.agent.llm.ToolCall` (id, name,
    arguments) so the gateway can splice it into the existing
    ``tool_calls`` list and re-use the dispatch path unchanged.
    """

    id: str
    name: str
    arguments: dict


# ── Block extractor ───────────────────────────────────────────────


# Match ``<tool_call>
#                  <name>...</name>
#                  <arguments>{...}</arguments>
#              </tool_call>`` blocks. Both attribute-style and
# element-style invocations are handled. The regex is intentionally
# non-greedy on the inner ``</tool_call>`` close so multiple blocks
# in one blob all match.
#
# Three shapes observed in the wild across the providers we ship:
#   1. ``<tool_call><invoke name="X">...</invoke></tool_call>``     (OpenAI / Anthropic standard)
#   2. ``<minimax>[<invoke name="X">]...[/invoke]</tool_call>``    (MiniMax wire-format token)
#   3. ``<invoke name="X">...</invoke>`` (no outer wrapper)        (some streaming degradation)
#
# We use a regex (not a parser) because:
#  * the wire format is loose — the model emits a wide variety of
#    shapes depending on provider, and a regex with two passes (name
#    + arguments) is more forgiving than an XML parser
#  * performance: regex runs in linear time, parser is O(n²) on
#    pathological inputs
#  * the assistant text is the LLM's output, not user input — it
#    can be slightly malformed and we want to be tolerant
#
# The matched group is the block INNER content — everything between
# the opening tag and the close (or, for shape 3, the inner content
# of the <invoke> block).
_TOOL_CALL_BLOCK_RE = re.compile(
    # Form 1: ``<tool_call>``` wrapper (OpenAI / Anthropic standard).
    r"<tool_call>\s*(.*?)\s*</tool_call>"
    # Form 2: <minimax>[<invoke name="X">...</invoke>]</minimax>
    # (MiniMax wire-format with per-line envelope). The denoiser
    # strips the <minimax> tags so we match the bare <invoke>.
    r"|<\s*invoke\b([^>]*)>(.*?)<\s*/\s*invoke\s*>"
    # Form 3: same as Form 2 but with closing `]` from the
    # <minimax>[...] envelope that the denoiser didn't strip (the
    # model sometimes drops the `]` on the inner content line).
    r"|<\s*invoke\b([^>]*)>(.*?)<\s*/\s*invoke\s*>\s*\]?",
    re.DOTALL | re.IGNORECASE,
)

# Match the function name. Two shapes observed in the wild:
#   <invoke name="read_file">        ← Anthropic / OpenAI shape
#   <tool name="read_file">          ← some older Anthropic models
#   read_file(...)                    ← CVC's own text-format
_FUNCTION_NAME_RE = re.compile(
    r"""(?:
        <\s*(?:invoke|tool|tool_call)\s+[^>]*?name\s*=\s*["']([^"']+)["']   # attribute form
        |
        <\s*(?:invoke|tool|tool_call)\s+[^>]*?["']name["']\s*:\s*["']([^"']+)["']  # JSON-ish attribute
        |
        ^\s*([A-Za-z_][A-Za-z0-9_.]*)\s*\(\s*$                                 # bare name then parens
    )""",
    re.VERBOSE | re.MULTILINE,
)

# Match the arguments. Four shapes:
#   <arguments>{"path": "x.py"}</arguments>
#   <parameter name="path">x.py</parameter>      ← Anthropic XML variant
#   <path>x.py</path>                           ← bare key element, Anthropic wire-format
#   { "path": "x.py" }                           ← bare JSON object
_ARGUMENTS_JSON_RE = re.compile(
    r"<\s*arguments?\s*>\s*(\{.*?\})\s*<\s*/\s*arguments?\s*>",
    re.DOTALL | re.IGNORECASE,
)
_ARGUMENTS_TAG_RE = re.compile(
    r"<\s*arguments?\s*/?>(.*?)<\s*/\s*arguments?\s*>",
    re.DOTALL | re.IGNORECASE,
)
_PARAMETER_PAIRS_RE = re.compile(
    r"<\s*parameter\s+name\s*=\s*[\"']([^\"']+)[\"']\s*>(.*?)<\s*/\s*parameter\s*>",
    re.DOTALL | re.IGNORECASE,
)
# Bare-key elements: <path>x.py</path> or <path>11-11-0</path>.
# The element name is the key. We match the COMMON CVC tool arg
# names here rather than all possible XML element names — the goal
# is targeted recovery, not XML parsing in general.
_BARE_KEY_ELEMENTS = (
    "path", "file", "filename", "old_string", "new_string",
    "content", "command", "pattern", "query", "name", "message",
    "text", "input", "data", "url", "key", "value", "args",
)
_BARE_KEY_RE = re.compile(
    r"<\s*(" + "|".join(_BARE_KEY_ELEMENTS) + r")\s*>(.*?)<\s*/\s*\1\s*>",
    re.DOTALL | re.IGNORECASE,
)
_BARE_JSON_OBJECT_RE = re.compile(r"(\{[^{}]*\})", re.DOTALL)


def _extract_name(block_attrs: str, block_body: str) -> Optional[str]:
    """Pull the function name from a ``<tool_call>``` block's attrs/body.

    *block_attrs* is the attribute string of the opening tag
    (e.g. ``' name="list_dir"'``). *block_body* is the content
    between the open and close tags. We check the attrs first
    (the common case) and then the body (in case the name is
    somewhere unexpected).
    """
    # Look for name="X" or name='X' in the attrs string.
    m = re.search(r'name\s*=\s*["\']([^"\']+)["\']', block_attrs or "")
    if m:
        return m.group(1)
    # Fallback: look in the body for the same shape.
    m = re.search(
        r'name\s*=\s*["\']([^"\']+)["\']',
        block_body or "",
    )
    if m:
        return m.group(1)
    return None


def _extract_arguments(block_body: str) -> dict:
    """Pull the args dict out of a ``<tool_call>``` block's body.

    Tries the structured forms first (XML parameter, XML arguments
    tag, bare JSON object), then falls back to the JSON repair
    utility so a truncated / fence-wrapped / quote-broken payload
    still yields a usable dict.
    """
    # Form 1: <arguments>{...}</arguments>
    m = _ARGUMENTS_JSON_RE.search(block_body)
    if m:
        return repair_tool_call_arguments(m.group(1))

    # Form 2: bare JSON object somewhere in the block.
    m = _BARE_JSON_OBJECT_RE.search(block_body)
    if m:
        return repair_tool_call_arguments(m.group(1))

    # Form 3: <parameter name="k">v</parameter> pairs.
    pairs = _PARAMETER_PAIRS_RE.findall(block_body)
    if pairs:
        return {k: v.strip() for k, v in pairs}

    # Form 3b: bare key elements <path>x</path>, <content>y</content>.
    # This is the shape the screenshot showed — Anthropic wire format
    # with the model wrapping each arg in its own element rather than
    # collecting them under <parameter> tags.
    bare_pairs = _BARE_KEY_RE.findall(block_body)
    if bare_pairs:
        return {k: v.strip() for k, v in bare_pairs}

    # Form 4: <arguments>...</arguments> with the JSON broken —
    # hand the raw content to the repair utility.
    m = _ARGUMENTS_TAG_RE.search(block_body)
    if m:
        return repair_tool_call_arguments(m.group(1))

    return {}


def _denoise_text(text: str) -> str:
    """Strip provider wire-format ENVELOPE tokens from *text* so the
    downstream block-extraction regex can work against a clean
    payload.

    Some streaming layers wrap EVERY line of a tool_call block in
    its own ``<minimax>[...]`` envelope (we saw this in production
    on 2026-06-22). The standard ``<invoke>...</invoke>`` regex
    can't match across envelopes. By pre-stripping the envelope
    noise we collapse the wire format back into the well-formed
    ``<invoke name="X">...</invoke>`` shape the standard extractor
    expects.

    This is the conservative inner-tag-PRESERVING variant. The
    public :func:`strip_provider_tags` is the aggressive
    inner-tag-STRIPPING variant used for visible chat-text
    cleanup. Two separate functions, two separate regexes, one
    shared philosophy: targeted recovery.
    """
    return _DENOISE_ENVELOPE_RE.sub("", text)


def extract_synthetic_tool_calls(text: str) -> List[SyntheticToolCall]:
    """Find all ``<tool_call>``` blocks in *text* and parse them.

    Returns one :class:`SyntheticToolCall` per successfully parsed
    block. Malformed blocks are silently dropped (with a WARNING
    log) — we never raise, because this is on the hot path of the
    streaming loop and any exception here would block the user
    from getting their final text response.

    The implementation first runs :func:`_denoise_text` to collapse
    per-line ``<minimax>[...]`` envelopes back into a clean
    ``<invoke>...</invoke>`` shape, then matches the standard
    block regexes against the cleaned payload.
    """
    if not text:
        return []
    if "<tool_call>" not in text and "<invoke" not in text:
        return []
    cleaned = _denoise_text(text) if "<" in text else text

    calls: List[SyntheticToolCall] = []
    for match in _TOOL_CALL_BLOCK_RE.finditer(cleaned):
        # The regex has three alternations:
        #   group 1 → form 1's body (inside ``)
        #   group 2 → form 2's attrs (`<invoke ...>` attributes)
        #   group 3 → form 2's body
        #   group 4 → form 3's attrs
        #   group 5 → form 3's body
        # At most one of these is non-None per match. We pick the
        # first non-None attrs+body pair.
        groups = match.groups()
        if groups[0] is not None:
            # Form 1: `` — no separate attrs, name is in the body.
            block_attrs = ""
            block_body = groups[0]
        elif groups[1] is not None and groups[2] is not None:
            block_attrs, block_body = groups[1], groups[2]
        elif groups[3] is not None and groups[4] is not None:
            block_attrs, block_body = groups[3], groups[4]
        else:
            continue
        name = _extract_name(block_attrs, block_body)
        if not name:
            logger.warning(
                "text_salvage: tool_call block missing name; block=%r",
                block_body[:200],
            )
            continue
        arguments = _extract_arguments(block_body)
        # id is synthesized — the original block doesn't carry one.
        # We use a uuid4 so the gateway's per-tool_call_id correlation
        # stays unique within the turn (multiple blocks at the same
        # iter would otherwise collide).
        calls.append(SyntheticToolCall(
            id=f"salvage-{uuid.uuid4().hex[:12]}",
            name=name,
            arguments=arguments,
        ))
    return calls


def apply_salvage(
    text: str,
) -> Tuple[List[SyntheticToolCall], str]:
    """Drop-in call site for the gateway chat loop.

    Returns ``(calls, leftover_text)`` where:

    * ``calls`` — synthetic ``ToolCall`` objects ready to splice
      into the existing ``tool_calls`` list. Empty if the model
      emitted no raw ``<tool_call>``` blocks (the common case).
    * ``leftover_text`` — the original text with the parsed blocks
      removed AND provider wire-format tokens stripped. The user
      does NOT see the raw XML in the chat body. If a block was
      unparseable, it is left in the leftover so the user can see
      what the model tried to do (rather than us silently
      swallowing it).

    This is the function the gateway's ``# No tool calls → final
    text response, break loop`` branch calls before deciding to
    break. If ``calls`` is non-empty, the gateway continues the
    loop with the synthetic calls dispatched as if they had come
    from the streaming layer.
    """
    if not text:
        return [], text
    if "<tool_call>" not in text and "<invoke" not in text:
        # No salvage candidates — but we may still want to clean
        # provider tags from the text.
        return [], strip_provider_tags(text)
    cleaned = _denoise_text(text) if "<" in text else text

    calls: List[SyntheticToolCall] = []
    leftover_parts: List[str] = []
    cursor = 0
    for match in _TOOL_CALL_BLOCK_RE.finditer(cleaned):
        # Emit the text BEFORE this block, unchanged.
        leftover_parts.append(cleaned[cursor:match.start()])
        groups = match.groups()
        if groups[0] is not None:
            block_attrs = ""
            block_body = groups[0]
        elif groups[1] is not None and groups[2] is not None:
            block_attrs, block_body = groups[1], groups[2]
        elif groups[3] is not None and groups[4] is not None:
            block_attrs, block_body = groups[3], groups[4]
        else:
            continue
        name = _extract_name(block_attrs, block_body)
        if name:
            arguments = _extract_arguments(block_body)
            calls.append(SyntheticToolCall(
                id=f"salvage-{uuid.uuid4().hex[:12]}",
                name=name,
                arguments=arguments,
            ))
            # The block was parseable — drop it from the visible text.
            # We replace it with a single space so the surrounding text
            # doesn't get squished together if the model wrote "I will
            # now do X" immediately followed by the tool_call block.
            leftover_parts.append(" ")
        else:
            # Unparseable — leave the raw block visible so the user
            # can see what the model tried. This is the same
            # observability affordance the dud-nudge gives in the
            # structured path.
            logger.warning(
                "text_salvage: unparseable tool_call block, leaving in text: %r",
                cleaned[match.start():match.end()][:200],
            )
            leftover_parts.append(match.group(0))
        cursor = match.end()
    leftover_parts.append(cleaned[cursor:])

    leftover = "".join(leftover_parts)
    # Collapse runs of whitespace that the removed blocks would have
    # left behind. Trim leading/trailing whitespace.
    leftover = re.sub(r"[ \t]+", " ", leftover).strip()
    return calls, leftover


# ── Provider-tag stripper ──────────────────────────────────────────


# Provider wire-format ENVELOPE tokens. These are the tags the
# streaming layer WRAPS the actual content in. We strip the
# envelope and keep whatever the model wrote between (or, for
# self-closing envelopes, just remove the tag).
#
# Deliberately separate from the inner-tag stripper in
# strip_provider_tags: that one is for visible chat-text cleanup
# (where removing `<invoke>` is fine). This one is for
# block-extraction preprocessing where `<invoke>...</invoke>` is
# the structure we want to MATCH against, not remove.
_DENOISE_ENVELOPE_RE = re.compile(
    # Pipe-bracketed envelope: <|name|>, <|/name|>, <|name|/>
    # The name may include $-signs (LLM debug tokens like <|$text|>)
    # and underscores. Digits NOT allowed at the start of the name
    # so we don't match things like `<|0xFF|>` (which look like
    # bit-width designators in code).
    r"<\s*\|[A-Za-z_$][A-Za-z0-9_$]*\|(?:\s*/)?>"
    r"|<\s*/\s*\|[A-Za-z_$][A-Za-z0-9_$]*\|>"
    # Standard envelope: <name>, </name>, <name/>
    r"|<\s*(?:minimax|antml)\s*/?>"
    r"|<\s*/\s*(?:minimax|antml)\s*>",
    re.IGNORECASE,
)


# Provider wire-format tokens. The aggressive variant — used for
# visible chat-text cleanup. Strips BOTH the outer envelope AND
# the inner structural tags (`<invoke>`, `</invoke>`, `<arguments>`,
# `</arguments>`) so the user never sees ANY provider tokens in
# the chat body.
#
# The set is intentionally narrow: we don't try to scrub every
# possible provider marker. If a new one shows up in production logs
# the safe fix is to add a regex here, not to add a heavier filter.
#
# Shapes observed in the wild:
#   <minimax>...</minimax>     (MiniMax open/close)
#   <minimax/>                 (MiniMax self-close)
#   <|$text|>...</|$text|>     (pipe-bracketed tokens, leaked)
#   <antml>...</antml>         (Anthropic streaming tokens)
#   <invoke ...>...</invoke>   (Anthropic tool call wire-format)
#   <arguments>...</arguments> (Anthropic tool call args container)
#   <parameter name="k">v</parameter>  (Anthropic tool call param)
_PROVIDER_TAG_RE = re.compile(
    # Pipe-bracketed form: <|name|>, <|/name|>, <|name|/>
    r"<\s*\|[A-Za-z_$][A-Za-z0-9_$]*\|(?:\s*/)?>"
    r"|<\s*/\s*\|[A-Za-z_$][A-Za-z0-9_$]*\|>"
    # Standard form: <name>, </name>, <name/>, with optional
    # surrounding whitespace.
    r"|<\s*(?:minimax|antml|tool_call|tool|invoke|param|parameters|arguments)\s*/?>"
    r"|<\s*/\s*(?:minimax|antml|tool_call|tool|invoke|param|parameters|arguments)\s*>",
    re.IGNORECASE,
)


def _denoise_text(text: str) -> str:
    """Strip provider wire-format ENVELOPE tokens from *text*.

    Differs from :func:`strip_provider_tags` in scope: the public
    stripper removes anything that looks like a provider token
    (including the inner ``<invoke>...</invoke>`` markers). The
    denoiser is more conservative — it strips only the OUTER
    envelope (e.g. ``<minimax>...</minimax>``, ``<|$text|>...``)
    and leaves the inner XML structure intact so the block
    extractor can match against it.

    Why two functions exist: the user-visible chat text benefits
    from removing ALL provider tokens (the user shouldn't see
    ANY of them). The pre-extraction text needs to preserve
    ``<invoke>`` etc. so the regex can find the block.
    """
    return _DENOISE_ENVELOPE_RE.sub("", text)


def strip_provider_tags(text: str) -> str:
    """Remove provider wire-format tokens from the assistant text.

    Cheap regex pass. Returns the input unchanged if no tag is
    present. Used by the gateway to clean the ``response_text``
    stream before it reaches the dashboard so the user doesn't see
    ``<minimax>`` or ``<|$text>`` tokens leaking into the chat.
    """
    if not text or "<" not in text:
        return text
    return _PROVIDER_TAG_RE.sub("", text)


# ── Combined convenience ──────────────────────────────────────────


def salvage_and_clean(text: str) -> Tuple[List[SyntheticToolCall], str]:
    """One call: extract synthetic tool calls AND strip provider tags.

    Convenience wrapper for the gateway. Equivalent to::

        calls, leftover = apply_salvage(text)
        leftover = strip_provider_tags(leftover)
        return calls, leftover

    Kept as a separate function so the gateway can wire it in one
    line and so we have a single integration point to test against.
    """
    calls, leftover = apply_salvage(text)
    leftover = strip_provider_tags(leftover)
    return calls, leftover
