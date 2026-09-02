"""DeepSeek V4 renderer for chat template formatting.

DeepSeek V4 checkpoints (``deepseek-ai/DeepSeek-V4-Flash-0731`` and its
quantized twins) ship **no** ``chat_template.jinja`` — the release carries a
reference Python encoder instead — so ``tokenizer.apply_chat_template`` is
unavailable and every caller has to hand-roll the format. Hand-rolling it is
what this renderer exists to stop: the V4 generation prompt MUST end with a
thinking marker, and dropping it does not fail loudly, it silently produces
a model that decides per sample whether it is reasoning.

Format (this renderer and river-serve's built-in
``DEEPSEEK_V4_CHAT_TEMPLATE`` are two implementations of ONE authority, the
reference encoder — never of each other; see ``_schema_json``)::

    <｜begin▁of▁sentence｜>{system}
    <｜User｜>{question}
    <｜Assistant｜></think>{previous answer}<｜end▁of▁sentence｜>
    <｜User｜>{follow-up}
    <｜Assistant｜><think>

The generation prompt closes with ``<think>`` in thinking mode and
``</think>`` in chat mode — those two tokens ARE the mode switch. A prompt
that stops at the bare ``<｜Assistant｜>`` marker selects neither: the model
then opens a reasoning block on roughly half of samples and never closes it
on the rest, which burns the token budget without ever reaching an answer.

History assistant turns render with the reasoning dropped
(``<｜Assistant｜></think>``), matching the reference encoder's
``drop_thinking`` default — EXCEPT when the request carries tools, which
turns dropping off for the whole conversation, so every past assistant turn
keeps ``<think>{reasoning}</think>``. Reasoning comes from
``reasoning_content`` when present, else from a ``<think>`` block in the
content. Pass ``strip_thinking_from_history=False`` to keep it in the
tool-less case too.

Tool calls use the DSML dialect that river-serve parses with
``--tool-call-parser deepseek``.
"""

from __future__ import annotations

import json
import re
from typing import Any

from river_client.renderers.base import (
    ContentPart,
    Message,
    ParsedResponse,
    Renderer,
    TextPart,
    ThinkingPart,
    Tokenizer,
    ToolCall,
    ToolCallFunction,
    ToolSpec,
    TrainOnWhat,
    TrainingExample,
    UnparsedToolCall,
)

# ─── Constants ───────────────────────────────────────────────────────────

# DeepSeek's marker tokens are delimited by FULLWIDTH VERTICAL LINE (U+FF5C),
# not ASCII "|", and the word separators are LOWER ONE EIGHTH BLOCK (U+2581).
# They are single vocab entries; substituting the ASCII lookalikes tokenizes
# into unrelated pieces.
_BOS = "<｜begin▁of▁sentence｜>"
_EOS = "<｜end▁of▁sentence｜>"
_USER = "<｜User｜>"
_ASSISTANT = "<｜Assistant｜>"

_THINK_OPEN = "<think>"
_THINK_CLOSE = "</think>"

_TOOL_RESULT_OPEN = "<tool_result>"
_TOOL_RESULT_CLOSE = "</tool_result>"

_DSML_CALLS_OPEN = "<｜DSML｜tool_calls>"
_DSML_CALLS_CLOSE = "</｜DSML｜tool_calls>"
_DSML_INVOKE_OPEN = "<｜DSML｜invoke"
_DSML_INVOKE_CLOSE = "</｜DSML｜invoke>"
_DSML_PARAM_OPEN = "<｜DSML｜parameter"
_DSML_PARAM_CLOSE = "</｜DSML｜parameter>"

#: Every marker that terminates an enclosing DSML element. A parameter value
#: containing any of them truncates the block at parse time.
_DSML_CLOSE_MARKERS = (_DSML_PARAM_CLOSE, _DSML_INVOKE_CLOSE, _DSML_CALLS_CLOSE)

# The tools instruction block, verbatim from the V4 encoder's
# ``TOOLS_TEMPLATE`` (format placeholders resolved). Model-family syntax the
# checkpoint was post-trained on — not prose we own, so it must not be
# paraphrased. river-serve renders the identical block from
# ``tokenizer.rs::dsml_tools_block``; the two must stay byte-identical or a
# client-rendered prompt and a `/v1/chat/completions` prompt disagree.
_TOOLS_TEMPLATE = """## Tools

You have access to a set of tools to help answer the user's question. \
You can invoke tools by writing a "<｜DSML｜tool_calls>" block like the following:

<｜DSML｜tool_calls>
<｜DSML｜invoke name="$TOOL_NAME">
<｜DSML｜parameter name="$PARAMETER_NAME" string="true|false">$PARAMETER_VALUE\
</｜DSML｜parameter>
...
</｜DSML｜invoke>
<｜DSML｜invoke name="$TOOL_NAME2">
...
</｜DSML｜invoke>
</｜DSML｜tool_calls>

String parameters should be specified as is and set `string="true"`. \
For all other types (numbers, booleans, arrays, objects), pass the value in \
JSON format and set `string="false"`.

If thinking_mode is enabled (triggered by <think>), you MUST output your \
complete reasoning inside <think>...</think> BEFORE any tool calls or final response.

Otherwise, output directly after </think> with tool calls or final response.

### Available Tool Schemas

{schemas}

You MUST strictly follow the above defined tool name and parameter schemas \
to invoke tool calls.
"""


def _schema_json(schema: object) -> str:
    """Serialize one tool schema the way the V4 REFERENCE encoder does.

    The encoder shipped with the checkpoint uses a plain
    ``json.dumps(t, ensure_ascii=False)`` — spaced separators, insertion
    order. That is the authority, and both river-serve and this renderer
    reproduce it.

    This used to emit ``separators=(",", ":"), sort_keys=True`` instead, to
    match river-serve's ``serde_json::to_string`` over a ``Value``. Matching
    the other River implementation rather than the reference is precisely
    how the two drifted together, away from what the model was trained on
    and away from what SGLang builds for the same request.
    """
    return json.dumps(schema, ensure_ascii=False)


def dsml_tools_block(tools: list[ToolSpec]) -> str:
    """Render the DSML tools instruction block for ``tools``.

    Each schema is emitted as one JSON line. OpenAI-wrapped entries
    (``{"type": "function", "function": {...}}``) are unwrapped to the bare
    function schema, matching river-serve's renderer.
    """
    schemas = "\n".join(
        _schema_json(tool.get("function", tool) if isinstance(tool, dict) else tool)
        for tool in tools
    )
    return _TOOLS_TEMPLATE.format(schemas=schemas)


# ─── Response parsing ────────────────────────────────────────────────────


def _reject_unrenderable_name(name: str, what: str) -> None:
    """Reject names DSML cannot represent.

    Attribute values are delimited by plain double quotes with no escape
    mechanism, so a ``"`` inside a name silently produces a block that the
    tolerant DSML parsers on both sides then mis-split — the call comes back
    as an ``UnparsedToolCall`` instead of erroring. Fail at render time,
    where the offending name is still in hand.
    """
    if '"' in name or ">" in name:
        raise ValueError(
            f"{what} {name!r} contains '\"' or '>', which DSML attribute "
            "values cannot encode."
        )


def _dsml_attrs(attrs: str) -> dict[str, str]:
    """Parse a ``k="v"`` attribute list, tolerating order and whitespace."""
    return {
        m.group(1): m.group(2) for m in re.finditer(r'(\w+)\s*=\s*"([^"]*)"', attrs)
    }


def _split_dsml_tag(segment: str) -> tuple[str, str] | None:
    """Split ``attrs...>body`` at the first ``>`` outside a quoted value."""
    in_quotes = False
    for i, ch in enumerate(segment):
        if ch == '"':
            in_quotes = not in_quotes
        elif ch == ">" and not in_quotes:
            return segment[:i], segment[i + 1 :]
    return None


def _parse_dsml_params(body: str) -> dict[str, Any] | None:
    """Parse the ``<｜DSML｜parameter>`` elements inside one invoke body.

    ``None`` (malformed invoke) on stray inter-parameter text, a missing or
    unrecognized ``string`` flag, or a duplicate parameter name — the same
    rejections river-serve's parser makes, so client and server agree on
    which blocks are tool calls and which are just text.
    """
    params: dict[str, Any] = {}
    rest = body
    while (p := rest.find(_DSML_PARAM_OPEN)) != -1:
        if rest[:p].strip():
            return None
        split = _split_dsml_tag(rest[p + len(_DSML_PARAM_OPEN) :])
        if split is None:
            return None
        attrs, after_tag = split
        parsed = _dsml_attrs(attrs)
        key = parsed.get("name")
        flag = parsed.get("string")
        if key is None or flag not in ("true", "false"):
            return None
        val_end = after_tag.find(_DSML_PARAM_CLOSE)
        if val_end == -1:
            return None
        raw = after_tag[:val_end]
        if flag == "true":
            value: Any = raw
        else:
            # Non-string params carry JSON; unparseable values degrade to
            # strings rather than failing the whole invoke.
            try:
                value = json.loads(raw.strip())
            except (json.JSONDecodeError, ValueError):
                value = raw
        if key in params:
            return None  # duplicate parameter name (reference rejects too)
        params[key] = value
        rest = after_tag[val_end + len(_DSML_PARAM_CLOSE) :]
    return None if rest.strip() else params


def _parse_dsml_invoke(segment: str) -> ToolCall | UnparsedToolCall:
    """Parse one ``<｜DSML｜invoke ...>...</｜DSML｜invoke>`` segment."""
    inner = segment[len(_DSML_INVOKE_OPEN) : -len(_DSML_INVOKE_CLOSE)]
    split = _split_dsml_tag(inner)
    if split is None:
        return UnparsedToolCall(raw_text=segment, error="Malformed DSML invoke tag")
    attrs, body = split
    name = _dsml_attrs(attrs).get("name", "")
    if not name:
        return UnparsedToolCall(raw_text=segment, error="Missing invoke name")
    params = _parse_dsml_params(body)
    if params is None:
        return UnparsedToolCall(raw_text=segment, error="Malformed DSML parameters")
    return ToolCall(
        type="function",
        id=None,
        function=ToolCallFunction(
            name=name, arguments=json.dumps(params, ensure_ascii=False)
        ),
    )


def parse_deepseek_content_blocks(
    content: str,
) -> tuple[list[ContentPart], list[ToolCall | UnparsedToolCall]] | None:
    """Parse DeepSeek V4 ``<think>`` and DSML tool-call blocks.

    Returns ``None`` when the text carries neither, so callers can keep the
    plain-string content form. A trailing unclosed ``<think>`` block is
    treated as thinking: long generations truncate before ``</think>``.
    """
    # A think block is only recognized at the very start: V4 emits its
    # reasoning before anything else, and the generation prompt opens the
    # block, so that is the only position it can legitimately occupy. A
    # `<think>` appearing mid-text is the model quoting the tag, not
    # reasoning — return None there rather than handing back parts with raw
    # tags embedded in the TextPart, so the caller keeps the plain string.
    has_reasoning = content.startswith(_THINK_OPEN)
    if not has_reasoning and _DSML_CALLS_OPEN not in content:
        return None

    parts: list[ContentPart] = []
    tool_calls: list[ToolCall | UnparsedToolCall] = []

    # Reasoning first: the format puts the whole think block ahead of any
    # tool call or answer, so a single leading split is enough.
    remainder = content
    if has_reasoning:
        after_open = content[len(_THINK_OPEN) :]
        close = after_open.find(_THINK_CLOSE)
        if close == -1:
            thinking, remainder = after_open, ""
        else:
            thinking = after_open[:close]
            remainder = after_open[close + len(_THINK_CLOSE) :].lstrip("\n")
        if thinking.strip():
            parts.append(ThinkingPart(type="thinking", thinking=thinking.strip()))

    visible, calls = _extract_dsml_tool_calls(remainder)
    tool_calls.extend(calls)
    if visible:
        parts.append(TextPart(type="text", text=visible))
    return parts, tool_calls


def _extract_dsml_tool_calls(
    text: str,
) -> tuple[str, list[ToolCall | UnparsedToolCall]]:
    """Split ``text`` into (visible text, tool calls).

    The reference format emits at most ONE ``tool_calls`` block and it
    terminates the turn; text before and after it stays visible. An
    unterminated block is left visible in full — the model was cut off
    mid-call and there is nothing well-formed to report.
    """
    open_at = text.find(_DSML_CALLS_OPEN)
    if open_at == -1:
        return text, []
    body_start = open_at + len(_DSML_CALLS_OPEN)
    close_rel = text[body_start:].find(_DSML_CALLS_CLOSE)
    if close_rel == -1:
        return text, []

    calls: list[ToolCall | UnparsedToolCall] = []
    leftover: list[str] = []
    rest = text[body_start : body_start + close_rel]
    while (inv := rest.find(_DSML_INVOKE_OPEN)) != -1:
        leftover.append(rest[:inv])
        end_rel = rest[inv:].find(_DSML_INVOKE_CLOSE)
        if end_rel == -1:
            leftover.append(rest[inv:])
            rest = ""
            break
        seg_end = inv + end_rel + len(_DSML_INVOKE_CLOSE)
        calls.append(_parse_dsml_invoke(rest[inv:seg_end]))
        rest = rest[seg_end:]
    leftover.append(rest)

    if not calls:
        return text, []
    fragments = [
        text[:open_at].rstrip("\n"),
        "".join(leftover).strip(),
        text[body_start + close_rel + len(_DSML_CALLS_CLOSE) :].lstrip("\n"),
    ]
    return "\n".join(f for f in fragments if f), calls


def strip_deepseek_thinking_from_text(text: str) -> str:
    """Remove DeepSeek reasoning blocks (closed or trailing) from text."""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = re.sub(r"<think>.*$", "", text, flags=re.DOTALL)
    return text.lstrip()


# ─── Renderer ────────────────────────────────────────────────────────────


class DeepSeekV4Renderer(Renderer):
    """Renderer for the DeepSeek V4 family.

    ``thinking`` selects the generation-prompt marker: ``<think>`` (reason,
    then close the block and answer) or ``</think>`` (answer directly). This
    is the model's actual mode switch, so it also decides how the last
    assistant turn is laid out for SFT — training on a turn shaped
    differently from what inference prefills would fit the adapter against a
    prompt prefix the served model never sees.

    ``strip_thinking_from_history`` drops ``<think>`` blocks from assistant
    turns before the last user message, matching the reference encoder's
    ``drop_thinking`` default.
    """

    def __init__(
        self,
        tokenizer: Tokenizer,
        *,
        thinking: bool = True,
        strip_thinking_from_history: bool = True,
    ) -> None:
        super().__init__(tokenizer)
        self.thinking = thinking
        self.strip_thinking_from_history = strip_thinking_from_history

    # ── Prompt building ──────────────────────────────────────────────

    def build_prompt_str(
        self,
        messages: list[Message],
        *,
        tools: list[ToolSpec] | None = None,
    ) -> str:
        pieces = [self._prefix(messages, tools)]
        for header, content in self._render_all(messages, tools):
            pieces.append(header + content)
        pieces.append(self._generation_prompt())
        return "".join(pieces)

    def get_stop_strings(self) -> list[str]:
        return [_EOS]

    def _generation_prompt(self) -> str:
        """The generation prompt — and the model's thinking-mode switch.

        ``<think>`` opens a reasoning block the model closes itself before
        answering; ``</think>`` presents an already-closed block so it
        answers directly. Ending at the bare marker instead selects neither
        and leaves the mode to chance.
        """
        return _ASSISTANT + (_THINK_OPEN if self.thinking else _THINK_CLOSE)

    def _prefix(self, messages: list[Message], tools: list[ToolSpec] | None) -> str:
        """BOS, plus a standalone tools block when there is no system turn."""
        prefix = _BOS
        if tools and (not messages or messages[0]["role"] != "system"):
            # The encoder inserts an EMPTY system message and joins it to the
            # block with "\n\n", so the separator is there even with nothing
            # in front of it.
            prefix += "\n\n" + dsml_tools_block(tools)
        return prefix

    def _render_all(
        self,
        messages: list[Message],
        tools: list[ToolSpec] | None,
        *,
        generated_turn: int | None = None,
    ) -> list[tuple[str, str]]:
        """Render every message to ``(header, content)`` pairs.

        The split is the training seam: headers are prompt scaffolding the
        model never emits (weight 0), contents are what it generates.

        ``generated_turn`` is the index of the one assistant turn the model
        is producing *right now* — the only turn laid out like the
        generation prompt (``<｜Assistant｜><think>`` + reasoning + close).
        Every other assistant turn is history and renders the way the server
        template renders history, i.e. reasoning dropped behind a bare
        ``</think>``. ``None`` (prompt building) means every turn is
        history.
        """
        return [
            self._render_message_text(
                messages,
                idx,
                is_generated_turn=(idx == generated_turn),
                tools=tools,
            )
            for idx in range(len(messages))
        ]

    def _render_message_text(
        self,
        messages: list[Message],
        idx: int,
        *,
        is_generated_turn: bool,
        tools: list[ToolSpec] | None,
    ) -> tuple[str, str]:
        message = messages[idx]
        role = message["role"]

        if role == "system":
            content = self._text_of(message)
            if tools and idx == 0:
                content += "\n\n" + dsml_tools_block(tools)
            return "", content

        if role in ("user", "tool"):
            # `merge_tool_messages` folds a run of consecutive user AND tool
            # messages into ONE user turn, its parts joined by "\n\n" — not
            # just a run of tool results. The `[assistant(calls), tool…,
            # user]` shape every agentic loop produces hits this on the very
            # next request: the follow-up question belongs to the same turn
            # as the tool results before it, with no second `<｜User｜>`.
            prev = messages[idx - 1]["role"] if idx else None
            header = _USER if prev not in ("user", "tool") else "\n\n"
            text = self._text_of(message)
            if role == "tool":
                text = f"{_TOOL_RESULT_OPEN}{text}{_TOOL_RESULT_CLOSE}"
            return header, text

        if role == "assistant":
            # Only the turn being generated mirrors the prefill. For history
            # turns the encoder resolves `drop_thinking`, and its one
            # non-obvious rule is that ANY message carrying tools turns
            # dropping OFF for the whole conversation:
            #
            #     effective_drop_thinking = drop_thinking
            #     if any(m.get("tools") for m in full_messages):
            #         effective_drop_thinking = False
            #
            # so a tool trajectory keeps `<think>{reasoning}</think>` on
            # every past assistant turn. Rendering them all closed — which
            # this did, to match river-serve — feeds the model a transcript
            # where it made each tool call with no reasoning at all, and the
            # damage compounds per hop. Reasoning is never emitted in chat
            # mode, where the encoder writes no think markers into history.
            emit_reasoning = (
                self.thinking
                if is_generated_turn
                else self.thinking
                and (bool(tools) or not self.strip_thinking_from_history)
            )
            reasoning, text = self._split_reasoning(message)
            header = _ASSISTANT + (_THINK_OPEN if emit_reasoning else _THINK_CLOSE)
            body = f"{reasoning}{_THINK_CLOSE}" if emit_reasoning else ""
            body += text
            if message.get("tool_calls"):
                body += self._format_tool_calls(message["tool_calls"])
            return header, body + _EOS

        raise ValueError(f"{type(self).__name__} cannot render role {role!r}")

    # ── Response parsing ─────────────────────────────────────────────

    def parse_response(self, text: str) -> ParsedResponse:
        stop_found = text.endswith(_EOS)
        if stop_found:
            text = text[: -len(_EOS)]

        # In thinking mode the generation prompt prefills the opening
        # ``<think>``, so sampled text starts INSIDE the block and carries
        # only the closing tag. Restore the opener so it parses as thinking
        # instead of being mistaken for the answer.
        #
        # Gated on the mode, and NOT on the close tag being present: in
        # thinking mode sampling always starts inside the block, so every
        # reply is reasoning-first whether or not it got far enough to close
        # it. Requiring ``</think>`` here meant a `finish_reason=length`
        # generation — which never contains either tag — fell through as
        # plain content, and `get_text_content` handed back the whole
        # unfinished chain of thought as if it were the answer.
        #
        # In chat mode the prompt already ends with ``</think>`` and the
        # model is answering directly, so a bare ``</think>`` in the reply is
        # ordinary text. Restoring an opener there would reclassify
        # everything before it as reasoning and truncate the answer — and the
        # tools block this renderer emits literally instructs "output
        # directly after </think>", so an echo is not hypothetical.
        if self.thinking and _THINK_OPEN not in text:
            text = _THINK_OPEN + text

        message: Message = {"role": "assistant", "content": text}
        result = parse_deepseek_content_blocks(text)
        if result is not None:
            parts, tool_results = result
            message["content"] = parts
            calls = [t for t in tool_results if "function" in t]
            unparsed = [t for t in tool_results if "error" in t]
            if calls:
                message["tool_calls"] = calls  # type: ignore[assignment]
            if unparsed:
                message["unparsed_tool_calls"] = unparsed  # type: ignore[assignment]
        return ParsedResponse(message=message, stop_found=stop_found)

    # ── SFT training ─────────────────────────────────────────────────

    def build_training_example(
        self,
        messages: list[Message],
        *,
        train_on: TrainOnWhat = TrainOnWhat.LAST_ASSISTANT,
        train_on_eos: bool = True,
        max_length: int | None = None,
        tools: list[ToolSpec] | None = None,
    ) -> TrainingExample:
        encode = self.tokenizer.encode
        ids: list[int] = []
        weights: list[float] = []

        def emit(text: str, weight: float) -> None:
            if not text:
                return
            tokens = encode(text, add_special_tokens=False)
            ids.extend(tokens)
            weights.extend([weight] * len(tokens))

        emit(self._prefix(messages, tools), 0.0)

        last_assistant = -1
        for idx, msg in enumerate(messages):
            if msg["role"] == "assistant":
                last_assistant = idx

        # The turn being TRAINED is the one the model generates, so it — and
        # only it — is laid out like the generation prompt; anything before
        # it is history. Keyed off the trained turn rather than the trailing
        # message: with an agentic `[user, assistant(tool_calls), tool]`
        # example the target is the assistant turn even though a tool result
        # follows it, and rendering that as history would train the adapter
        # to answer after a `</think>` prefix thinking-mode inference never
        # presents, with the reasoning dropped from the target entirely.
        #
        # Anything after the trained turn is inert context (weight 0, and
        # causally after every weighted position), so laying the target out
        # for generation costs nothing there.
        if self.thinking and train_on == TrainOnWhat.ALL_ASSISTANT:
            assistants = sum(1 for m in messages if m["role"] == "assistant")
            if assistants > 1:
                raise ValueError(
                    "train_on=ALL_ASSISTANT cannot be represented in thinking "
                    "mode: the DeepSeek V4 template drops reasoning from every "
                    "history assistant turn, so only the final one can carry "
                    "the target layout. Train one turn per example "
                    "(LAST_ASSISTANT over progressively longer prefixes), or "
                    "use thinking=False, where history and generation share "
                    "the same `</think>` prefill."
                )
        generated_turn = last_assistant if last_assistant >= 0 else None
        rendered = self._render_all(messages, tools, generated_turn=generated_turn)
        for idx, (header, content) in enumerate(rendered):
            is_assistant = messages[idx]["role"] == "assistant"
            if train_on == TrainOnWhat.LAST_ASSISTANT:
                trainable = is_assistant and idx == last_assistant
            elif train_on == TrainOnWhat.ALL_ASSISTANT:
                trainable = is_assistant
            else:
                trainable = False

            emit(header, 0.0)
            if trainable and not train_on_eos and content.endswith(_EOS):
                emit(content[: -len(_EOS)], 1.0)
                emit(_EOS, 0.0)
            else:
                emit(content, 1.0 if trainable else 0.0)

        if max_length is not None and len(ids) > max_length:
            ids = ids[:max_length]
            weights = weights[:max_length]
        return TrainingExample(input_ids=ids, weights=weights)

    # ── Tool support ─────────────────────────────────────────────────

    def build_system_message_with_tools(
        self, tools: list[ToolSpec], system_prompt: str = ""
    ) -> Message:
        """Bake the DSML tools block into a system message.

        Produces exactly what passing ``tools=`` to :meth:`build_prompt_str`
        renders, so pre-baking and inline rendering are interchangeable —
        but do BOTH and the block lands in the prompt twice.
        """
        block = dsml_tools_block(tools) if tools else ""
        if system_prompt and block:
            return Message(role="system", content=system_prompt + "\n\n" + block)
        return Message(role="system", content=block or system_prompt)

    def _format_tool_calls(self, tool_calls: list[ToolCall]) -> str:
        """Format tool calls as one DSML ``tool_calls`` block.

        Values carry an explicit ``string`` flag: ``true`` means the element
        text IS the string value, ``false`` means it is JSON. That flag is
        how the model (and both parsers) tell ``"3"`` from ``3``.
        """
        invokes: list[str] = []
        for call in tool_calls:
            name = call["function"]["name"]
            raw_args = call["function"].get("arguments") or {}
            if isinstance(raw_args, str):
                try:
                    args = json.loads(raw_args)
                except (json.JSONDecodeError, ValueError):
                    args = None
            else:
                args = raw_args
            if not isinstance(args, dict):
                # Anything that is not a JSON object becomes ONE `arguments`
                # parameter carrying the raw text — the encoder's own
                # fallback, and what river-serve's `dsml_tool_calls_block`
                # does. Dropping them instead lost what the model asked for,
                # silently and only on this side.
                args = {"arguments": raw_args if isinstance(raw_args, str) else ""}

            _reject_unrenderable_name(name, "tool name")
            params = []
            for key, value in args.items():
                _reject_unrenderable_name(key, "parameter name")
                is_str = isinstance(value, str)
                text = value if is_str else json.dumps(value, ensure_ascii=False)
                # Every close marker, not just the parameter's own: the
                # parsers scan for the tool_calls close before they look at
                # invokes at all, and split invokes at the first invoke
                # close, so a value carrying either one truncates the
                # enclosing element and the call round-trips as an
                # UnparsedToolCall — the outcome this check exists to stop.
                for marker in _DSML_CLOSE_MARKERS:
                    if marker in text:
                        raise ValueError(
                            f"tool {name!r} parameter {key!r} contains "
                            f"{marker!r}, which would terminate the enclosing "
                            "DSML element early; DSML has no escape for it."
                        )
                params.append(
                    f'{_DSML_PARAM_OPEN} name="{key}" '
                    f'string="{"true" if is_str else "false"}">'
                    f"{text}{_DSML_PARAM_CLOSE}"
                )
            # The encoder builds the body as "\n".join(params) and wraps it
            # in "\n...\n", so a zero-parameter invoke carries TWO newlines,
            # not one. Joining with a trailing newline per param collapses
            # that to one and diverges on every argument-less call.
            body = "\n".join(params)
            invokes.append(
                f'{_DSML_INVOKE_OPEN} name="{name}">\n{body}\n{_DSML_INVOKE_CLOSE}\n'
            )
        return f"\n\n{_DSML_CALLS_OPEN}\n{''.join(invokes)}{_DSML_CALLS_CLOSE}"

    # ── Internal helpers ─────────────────────────────────────────────

    def _split_reasoning(self, message: Message) -> tuple[str, str]:
        """Split assistant content into ``(reasoning, answer_text)``.

        ``reasoning_content`` — the OpenAI-shaped field both this client and
        `/v1/chat/completions` return reasoning in — wins when present, so a
        caller replaying a response it just received gets that reasoning back
        into the prompt. Without this, a tool trajectory round-tripped
        through the API loses its reasoning on every hop.

        It is passed through VERBATIM. The encoder interpolates it with
        ``thinking_template.format(reasoning_content=rc)`` and never strips,
        so a streamed reply whose reasoning carries leading or trailing
        newlines has to render with them — river-serve emits
        ``{{ message.reasoning_content }}`` unchanged for the same reason.
        Stripping here made the two sides disagree on exactly that input.
        """
        explicit = message.get("reasoning_content")
        if isinstance(explicit, str):
            return explicit, self._text_of(message)
        content = message["content"]
        if isinstance(content, str):
            if _THINK_CLOSE in content:
                head, _, tail = content.partition(_THINK_CLOSE)
                reasoning = head.rstrip("\n").split(_THINK_OPEN)[-1]
                return reasoning.strip(), tail.lstrip("\n")
            return "", content
        self._reject_non_text_parts(content)
        reasoning = "".join(p["thinking"] for p in content if p["type"] == "thinking")
        text = "".join(p["text"] for p in content if p["type"] == "text")
        return reasoning.strip(), text

    def _text_of(self, message: Message) -> str:
        """Plain text of a non-assistant message."""
        content = message["content"]
        if isinstance(content, str):
            return content
        self._reject_non_text_parts(content)
        return "".join(p["text"] for p in content if p["type"] == "text")

    def _reject_non_text_parts(self, parts: list[ContentPart]) -> None:
        """Fail loudly on content this text-only renderer cannot express.

        DeepSeek V4 Flash has no vision tower; silently dropping image parts
        would produce corrupt training data rather than an obvious error.
        """
        for p in parts:
            if p["type"] not in ("text", "thinking"):
                raise ValueError(
                    f"{type(self).__name__} cannot render {p['type']!r} content "
                    "parts; DeepSeek V4 is text-only."
                )
