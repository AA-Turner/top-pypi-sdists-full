"""DeepSeek V4 / V4.1 renderer for chat template formatting.

DeepSeek V4 and V4.1 checkpoints (``deepseek-ai/DeepSeek-V4-Flash-0731``,
``deepseek-ai/DeepSeek-V4.1-Flash`` and their quantized twins) ship **no**
``chat_template.jinja`` — each release carries a reference Python encoder
instead — so ``tokenizer.apply_chat_template`` is unavailable and every
caller has to hand-roll the format. Hand-rolling it is
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

V4.1 (``v41=True``) keeps this structure and changes three things, mirroring
the checkpoint's ``encoding/encoding.py``: the DSML tag names carry a leading
space (``<｜DSML｜ calls>`` / `` invoke`` / `` parameter``) and tools may be
namespaced (``ns::name``); thinking mode opens the conversation with a
numeric effort prefix behind the ``<｜System｜>`` token; and a leading or
mid-conversation system message is framed by that token too. Like SGLang,
the empty tools-hosting system message is only inserted when tools are
present, because V4.1 renders even an empty one as a token.
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass
from typing import Any, cast

from river_client.images import Image
from river_client.renderers.base import (
    _ChunkBuilder,
    _truncate_chunks_to_length,
    ContentPart,
    ImageChunk,
    ImageFormat,
    ImagePart,
    Message,
    ParsedResponse,
    Renderer,
    SamplePrompt,
    TextPart,
    ThinkingPart,
    Tokenizer,
    ToolCall,
    ToolCallFunction,
    ToolSpec,
    TrainOnWhat,
    TrainingExample,
    UnparsedToolCall,
    image_part,
    image_part_size,
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
#: V4.1 only: frames the conversation opener (effort prefix and/or a leading
#: system message) and every mid-conversation system message.
_SYSTEM = "<｜System｜>"

_THINK_OPEN = "<think>"
_THINK_CLOSE = "</think>"

_TOOL_RESULT_OPEN = "<tool_result>"
_TOOL_RESULT_CLOSE = "</tool_result>"

#: V4.1's reference encoder replaces each structured image content block with
#: one placeholder. The serving image processor expands it to the model's full
#: image-token span after decoding the corresponding image bytes.
_IMAGE_PLACEHOLDER = "<｜deepseek_image｜>"

# Defaults from DeepSeek-V4.1-Flash's vision_config. The worker verifies the
# resulting expected_tokens against its own processor before using the sample.
_VISION_PATCH_SIZE = 14
_VISION_DOWNSAMPLE_RATIO = 3
_VISION_MAX_IMAGE_TOKENS = 1024
_VISION_MIN_PIXELS = 295936  # 544 x 544

_DSML = "｜DSML｜"

#: V4.1's `render_reasoning_effort`: the numeric budget prefix thinking mode
#: opens with, and the tier names it maps onto it. Default `high`, like the
#: encoder and SGLang's `SGLANG_DSV41_REASONING_EFFORT`.
_EFFORT_TEMPLATE = (
    "Reasoning Effort: {budget} "
    "(range 1-100, the higher the value, the more thorough the reasoning)\n\n"
)
_EFFORT_TIERS = {"low": 50, "high": 75, "max": 100}
_EFFORT_DEFAULT = "high"


@dataclass(frozen=True)
class DsmlDialect:
    """The DSML tag names of one DeepSeek encoder generation.

    V4 names the block, invoke and parameter tags ``tool_calls`` / ``invoke``
    / ``parameter``. V4.1's ``encoding/encoding.py`` renames them
    `` calls`` / `` invoke`` / `` parameter``, leading space included, and
    introduces tool namespaces, which qualify the rendered name as
    ``ns::name``. Both parsers on both sides accept either grammar; only the
    rendering side has to pick one.
    """

    calls: str
    invoke: str
    param: str
    namespaces: bool

    @property
    def calls_open(self) -> str:
        return f"<{_DSML}{self.calls}>"

    @property
    def calls_close(self) -> str:
        return f"</{_DSML}{self.calls}>"

    @property
    def invoke_open(self) -> str:
        return f"<{_DSML}{self.invoke}"

    @property
    def invoke_close(self) -> str:
        return f"</{_DSML}{self.invoke}>"

    @property
    def param_open(self) -> str:
        return f"<{_DSML}{self.param}"

    @property
    def param_close(self) -> str:
        return f"</{_DSML}{self.param}>"

    @property
    def close_markers(self) -> tuple[str, str, str]:
        """Every marker that terminates an enclosing DSML element. A
        parameter value containing any of them truncates the block at parse
        time."""
        return (self.param_close, self.invoke_close, self.calls_close)


DSML_V4 = DsmlDialect(
    calls="tool_calls", invoke="invoke", param="parameter", namespaces=False
)
DSML_V41 = DsmlDialect(
    calls=" calls", invoke=" invoke", param=" parameter", namespaces=True
)
_DIALECTS = (DSML_V4, DSML_V41)

# The tools instruction block, verbatim from the encoders' ``TOOLS_TEMPLATE``
# (format placeholders resolved per dialect). Model-family syntax the
# checkpoint was post-trained on — not prose we own, so it must not be
# paraphrased. river-serve renders the identical block from
# ``tokenizer.rs::render_tools_block``; the two must stay byte-identical or a
# client-rendered prompt and a `/v1/chat/completions` prompt disagree.
_TOOLS_TEMPLATE = """## Tools

You have access to a set of tools to help answer the user's question. \
You can invoke tools by writing a "<｜DSML｜{calls}>" block like the following:

<｜DSML｜{calls}>
<｜DSML｜{invoke} name="$TOOL_NAME">
<｜DSML｜{param} name="$PARAMETER_NAME" string="true|false">$PARAMETER_VALUE\
</｜DSML｜{param}>
...
</｜DSML｜{invoke}>
<｜DSML｜{invoke} name="$TOOL_NAME2">
...
</｜DSML｜{invoke}>
</｜DSML｜{calls}>

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


def qualified_tool_name(name: str, namespace: str | None = None) -> str:
    """The V4.1 encoder's ``_tool_name_for_encoding``.

    A namespace, given separately or as the ``ns::`` prefix of the name
    itself, qualifies the rendered name. The two spellings must agree, and
    neither side may itself contain ``::`` — the encoder asserts on both.
    """
    prefix, separator, bare = name.partition("::")
    if separator:
        if namespace not in (None, prefix):
            raise ValueError(f"Conflicting tool namespaces: {namespace} != {prefix}")
        namespace, name = prefix, bare
    if "::" in name:
        raise ValueError(f"Tool name must not contain '::': {name}")
    if namespace is not None and "::" in namespace:
        raise ValueError(f"Tool namespace must not contain '::': {namespace}")
    return name if namespace is None else f"{namespace}::{name}"


def _v41_function_schema(tool: Any, function: dict[str, Any]) -> dict[str, Any]:
    """The V4.1 encoder's ``tools_from_openai_format`` for one schema.

    A tool-level ``namespace`` (a string, or ``{name, description}``) moves
    onto the function, the rendered ``name`` becomes ``ns::name``, the
    namespace's description is prepended to the function's, and the
    ``namespace`` key itself is not rendered. Every other key keeps the
    caller's order.
    """
    function = dict(function)
    if (
        isinstance(tool, dict)
        and "function" in tool
        and tool.get("namespace") is not None
    ):
        function["namespace"] = tool["namespace"]
    namespace: Any = function.pop("namespace", None)
    ns_name: str | None = (
        namespace["name"] if isinstance(namespace, dict) else namespace
    )
    function["name"] = qualified_tool_name(function["name"], ns_name)
    if isinstance(namespace, dict) and namespace.get("description"):
        function["description"] = (
            namespace["description"] + "\n" + (function.get("description") or "")
        )
    return function


def dsml_tools_block(tools: list[ToolSpec], dialect: DsmlDialect = DSML_V4) -> str:
    """Render the DSML tools instruction block for ``tools``.

    Each schema is emitted as one JSON line. OpenAI-wrapped entries
    (``{"type": "function", "function": {...}}``) are unwrapped to the bare
    function schema, matching river-serve's renderer. The V4.1 dialect also
    resolves tool namespaces into the rendered name.
    """
    schemas = []
    for tool in tools:
        spec: Any = tool
        function: Any = spec.get("function", spec) if isinstance(spec, dict) else spec
        if dialect.namespaces and isinstance(function, dict):
            function = _v41_function_schema(spec, function)
        schemas.append(_schema_json(function))
    return _TOOLS_TEMPLATE.format(
        calls=dialect.calls,
        invoke=dialect.invoke,
        param=dialect.param,
        schemas="\n".join(schemas),
    )


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


def _parse_dsml_params(body: str, dialect: DsmlDialect) -> dict[str, Any] | None:
    """Parse the ``<｜DSML｜parameter>`` elements inside one invoke body.

    ``None`` (malformed invoke) on stray inter-parameter text, a missing or
    unrecognized ``string`` flag, or a duplicate parameter name — the same
    rejections river-serve's parser makes, so client and server agree on
    which blocks are tool calls and which are just text.
    """
    params: dict[str, Any] = {}
    rest = body
    while (p := rest.find(dialect.param_open)) != -1:
        if rest[:p].strip():
            return None
        split = _split_dsml_tag(rest[p + len(dialect.param_open) :])
        if split is None:
            return None
        attrs, after_tag = split
        parsed = _dsml_attrs(attrs)
        key = parsed.get("name")
        flag = parsed.get("string")
        if key is None or flag not in ("true", "false"):
            return None
        val_end = after_tag.find(dialect.param_close)
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
        rest = after_tag[val_end + len(dialect.param_close) :]
    return None if rest.strip() else params


def _parse_dsml_invoke(
    segment: str, dialect: DsmlDialect
) -> ToolCall | UnparsedToolCall:
    """Parse one ``<｜DSML｜invoke ...>...</｜DSML｜invoke>`` segment.

    A V4.1 namespace stays in the name as ``ns::name``: that is how the
    encoder renders it back, so a parsed call round-trips into a prompt
    unchanged.
    """
    inner = segment[len(dialect.invoke_open) : -len(dialect.invoke_close)]
    split = _split_dsml_tag(inner)
    if split is None:
        return UnparsedToolCall(raw_text=segment, error="Malformed DSML invoke tag")
    attrs, body = split
    name = _dsml_attrs(attrs).get("name", "")
    if not name:
        return UnparsedToolCall(raw_text=segment, error="Missing invoke name")
    params = _parse_dsml_params(body, dialect)
    if params is None:
        return UnparsedToolCall(raw_text=segment, error="Malformed DSML parameters")
    return ToolCall(
        type="function",
        id=None,
        function=ToolCallFunction(
            name=name, arguments=json.dumps(params, ensure_ascii=False)
        ),
    )


def _dialect_of(text: str) -> DsmlDialect | None:
    """The dialect of the calls block in ``text``, if any.

    A dialect whose block is CLOSED wins over one whose opener merely
    appears (text quoting the other grammar's tag, say); among closed
    blocks the earliest opener wins, matching the parsers on both sides,
    which take the first well-formed block as the one that ends the turn.
    """
    closed = []
    opened = []
    for d in _DIALECTS:
        pos = text.find(d.calls_open)
        if pos == -1:
            continue
        opened.append((pos, d))
        if text.find(d.calls_close, pos + len(d.calls_open)) != -1:
            closed.append((pos, d))
    ranked = closed or opened
    return min(ranked, key=lambda item: item[0])[1] if ranked else None


def parse_deepseek_content_blocks(
    content: str,
) -> tuple[list[ContentPart], list[ToolCall | UnparsedToolCall]] | None:
    """Parse DeepSeek ``<think>`` and DSML tool-call blocks (V4 or V4.1 tags).

    Returns ``None`` when the text carries neither, so callers can keep the
    plain-string content form. A trailing unclosed ``<think>`` block is
    treated as thinking: long generations truncate before ``</think>``.
    """
    # A think block is only recognized at the very start: the model emits
    # its reasoning before anything else, and the generation prompt opens
    # the block, so that is the only position it can legitimately occupy. A
    # `<think>` appearing mid-text is the model quoting the tag, not
    # reasoning — return None there rather than handing back parts with raw
    # tags embedded in the TextPart, so the caller keeps the plain string.
    has_reasoning = content.startswith(_THINK_OPEN)
    if not has_reasoning and _dialect_of(content) is None:
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

    # The dialect is read from what is LEFT after the reasoning: reasoning
    # that quotes the other grammar's tag must not pin the parser to it.
    visible, calls = _extract_dsml_tool_calls(remainder)
    tool_calls.extend(calls)
    if visible:
        parts.append(TextPart(type="text", text=visible))
    return parts, tool_calls


def _extract_dsml_tool_calls(
    text: str, dialect: DsmlDialect | None = None
) -> tuple[str, list[ToolCall | UnparsedToolCall]]:
    """Split ``text`` into (visible text, tool calls).

    The reference format emits at most ONE calls block and it terminates the
    turn; text before and after it stays visible. An unterminated block is
    left visible in full — the model was cut off mid-call and there is
    nothing well-formed to report.
    """
    dialect = dialect or _dialect_of(text)
    if dialect is None:
        return text, []
    open_at = text.find(dialect.calls_open)
    if open_at == -1:
        return text, []
    body_start = open_at + len(dialect.calls_open)
    close_rel = text[body_start:].find(dialect.calls_close)
    if close_rel == -1:
        return text, []

    calls: list[ToolCall | UnparsedToolCall] = []
    leftover: list[str] = []
    rest = text[body_start : body_start + close_rel]
    while (inv := rest.find(dialect.invoke_open)) != -1:
        leftover.append(rest[:inv])
        end_rel = rest[inv:].find(dialect.invoke_close)
        if end_rel == -1:
            leftover.append(rest[inv:])
            rest = ""
            break
        seg_end = inv + end_rel + len(dialect.invoke_close)
        calls.append(_parse_dsml_invoke(rest[inv:seg_end], dialect))
        rest = rest[seg_end:]
    leftover.append(rest)

    if not calls:
        return text, []
    fragments = [
        text[:open_at].rstrip("\n"),
        "".join(leftover).strip(),
        text[body_start + close_rel + len(dialect.calls_close) :].lstrip("\n"),
    ]
    return "\n".join(f for f in fragments if f), calls


def strip_deepseek_thinking_from_text(text: str) -> str:
    """Remove DeepSeek reasoning blocks (closed or trailing) from text."""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = re.sub(r"<think>.*$", "", text, flags=re.DOTALL)
    return text.lstrip()


def resolve_reasoning_effort(effort: int | str | None) -> int:
    """The V4.1 encoder's effort validation: a tier name or an integer budget
    in ``[1, 100]``; ``None`` is the encoder default (``high`` = 75)."""
    if effort is None:
        effort = _EFFORT_DEFAULT
    if isinstance(effort, str):
        if effort not in _EFFORT_TIERS:
            raise ValueError(
                f"Invalid reasoning effort for deepseek_v41: {effort!r}, should "
                f"be int within [1,100] or {list(_EFFORT_TIERS)}"
            )
        return _EFFORT_TIERS[effort]
    if (
        isinstance(effort, bool)
        or not isinstance(effort, int)
        or not 1 <= effort <= 100
    ):
        raise ValueError(
            f"Invalid reasoning effort for deepseek_v41: {effort!r}, should "
            f"be int within [1,100] or {list(_EFFORT_TIERS)}"
        )
    return effort


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

    ``v41`` selects the V4.1 encoder's format (see the module docstring);
    ``reasoning_effort`` is its numeric thinking budget — ``low`` / ``high``
    / ``max`` or an integer in ``[1, 100]``, default ``high`` — and is only
    meaningful there. V4.1 image parts are supported for sampling and RL
    continuation prompts; V4 remains text-only.
    """

    def __init__(
        self,
        tokenizer: Tokenizer,
        *,
        thinking: bool = True,
        strip_thinking_from_history: bool = True,
        v41: bool = False,
        reasoning_effort: int | str | None = None,
        vision_patch_size: int = _VISION_PATCH_SIZE,
        vision_downsample_ratio: int = _VISION_DOWNSAMPLE_RATIO,
        vision_max_image_tokens: int = _VISION_MAX_IMAGE_TOKENS,
        vision_min_pixels: int = _VISION_MIN_PIXELS,
        vision_max_wh_ratio: int | None = None,
    ) -> None:
        super().__init__(tokenizer)
        self.thinking = thinking
        self.strip_thinking_from_history = strip_thinking_from_history
        self.v41 = v41
        self.dialect = DSML_V41 if v41 else DSML_V4
        if not v41 and reasoning_effort is not None:
            raise ValueError(
                "reasoning_effort is a DeepSeek V4.1 control; the V4 encoder "
                "has no numeric budget, so it would be silently dropped."
            )
        self.reasoning_effort = (
            resolve_reasoning_effort(reasoning_effort) if v41 else None
        )
        self.vision_patch_size = vision_patch_size
        self.vision_downsample_ratio = vision_downsample_ratio
        self.vision_max_image_tokens = vision_max_image_tokens
        self.vision_min_pixels = vision_min_pixels
        self.vision_max_wh_ratio = vision_max_wh_ratio

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

    def build_sample_prompt(
        self,
        messages: list[Message],
        *,
        tools: list[ToolSpec] | None = None,
    ) -> SamplePrompt:
        """Render a V4.1 prompt and collect its images in placeholder order.

        The prompt contains one unexpanded ``<｜deepseek_image｜>`` per
        :class:`ImagePart`. River Serve performs the model-specific resize and
        expands each placeholder to its complete image-token span.
        """
        prompt = self.build_prompt_str(messages, tools=tools)
        image_parts = self._image_parts(messages)
        return SamplePrompt(
            prompt=prompt,
            images=[part["image"] for part in image_parts],
            image_formats=[part["format"] for part in image_parts],
        )

    def image_token_count(self, height: int, width: int) -> int:
        """Return the expanded V4.1 image span length for these dimensions."""
        if not self.v41:
            raise ValueError("DeepSeek V4 has no vision tower; use a V4.1 renderer")
        if height <= 0 or width <= 0:
            raise ValueError("image height and width must be positive")

        patch = self.vision_patch_size
        ratio = self.vision_downsample_ratio
        max_tokens = self.vision_max_image_tokens
        min_pixels = self.vision_min_pixels
        if min(patch, ratio, max_tokens, min_pixels) <= 0:
            raise ValueError("DeepSeek V4.1 vision configuration must be positive")

        resized_height, resized_width = height, width
        if (
            self.vision_max_wh_ratio is not None
            and resized_width > resized_height * self.vision_max_wh_ratio
        ):
            resized_width = resized_height * self.vision_max_wh_ratio
        pixels = resized_height * resized_width
        if pixels < min_pixels:
            scale = math.sqrt(min_pixels / pixels)
            resized_height = int(resized_height * scale)
            resized_width = int(resized_width * scale)

        best_height = math.ceil(resized_height / patch) * patch
        best_width = math.ceil(resized_width / patch) * patch

        def grid_size(h: int, w: int) -> tuple[int, int]:
            return (
                math.ceil((h // patch) / ratio),
                math.ceil((w // patch) / ratio),
            )

        def token_count(h: int, w: int) -> int:
            grid_h, grid_w = grid_size(h, w)
            return grid_h * (grid_w + 1) + 2

        if token_count(best_height, best_width) <= max_tokens:
            return token_count(best_height, best_width)

        aspect_ratio = resized_height / resized_width
        max_width = math.sqrt((max_tokens - 2) / aspect_ratio + 0.25) - 0.5
        max_height = max_width * aspect_ratio
        cell = patch * ratio
        if max_width < 1.0:
            best_height, best_width = (max_tokens - 2) // 2 * cell, cell
        elif max_height < 1.0:
            best_height, best_width = cell, (max_tokens - 3) * cell
        else:
            scale = min(
                math.floor(max_width) * cell / resized_width,
                math.floor(max_height) * cell / resized_height,
            )
            best_height = math.floor(resized_height * scale / patch) * patch
            best_width = math.floor(resized_width * scale / patch) * patch
        count = token_count(best_height, best_width)
        if count > max_tokens:
            raise ValueError(
                f"DeepSeek V4.1 image resize produced {count} tokens, above "
                f"the configured maximum of {max_tokens}"
            )
        return count

    def image_chunk(
        self,
        data: Image,
        *,
        format: str = "png",
        height: int | None = None,
        width: int | None = None,
    ) -> ImageChunk:
        """Build a V4.1 image chunk with the expected expanded span length."""
        if height is None or width is None:
            height, width = image_part_size(
                image_part(data, format=cast("ImageFormat", format))
            )
        return ImageChunk(
            type="image",
            data=data,
            format=cast("ImageFormat", format),
            expected_tokens=self.image_token_count(height, width),
        )

    def build_continuation_prompt(self, messages, *, last_stop):
        if any(m["role"] not in ("user", "tool") for m in messages):
            raise ValueError("DeepSeek continuations require user or tool observations")
        prefix = "" if last_stop == _EOS else _EOS
        rendered = self._render_all(messages, None)
        image_parts = self._image_parts(messages)
        return SamplePrompt(
            prefix
            + "".join(header + body for header, body in rendered)
            + self._generation_prompt(),
            [part["image"] for part in image_parts],
            [part["format"] for part in image_parts],
        )

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
        """BOS, the V4.1 opener, and a standalone tools block when there is
        no system turn.

        The V4 encoder always inserts an EMPTY system message (it renders to
        nothing) and joins it to the tools block with "\n\n", so the
        separator is there even with nothing in front of it. V4.1 frames the
        conversation with ``<｜System｜>`` whenever thinking mode opens it
        with the effort prefix OR there is a system message — and SGLang
        inserts the empty host only when tools need it, so a tool-less
        chat-mode request starts straight at the user marker.
        """
        prefix = _BOS
        has_system = bool(messages) and messages[0]["role"] == "system"
        if self.v41:
            if self.thinking:
                prefix += _SYSTEM + _EFFORT_TEMPLATE.format(
                    budget=self.reasoning_effort
                )
            elif has_system or tools:
                prefix += _SYSTEM
        if tools and not has_system:
            prefix += "\n\n" + dsml_tools_block(tools, self.dialect)
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
                content += "\n\n" + dsml_tools_block(tools, self.dialect)
            # V4.1 frames a mid-conversation system message with the system
            # token (the leading one is framed by `_prefix`); it also counts
            # as a user turn for the assistant header that follows, which
            # the assistant branch emits itself.
            header = _SYSTEM if self.v41 and idx > 0 else ""
            return header, content

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

    def parse_response(
        self, text: str, *, tools: list[ToolSpec] | None = None
    ) -> ParsedResponse:
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
        if self._contains_images(messages):
            if not self.v41:
                raise ValueError(
                    "DeepSeek V4 has no vision tower; use a V4.1 renderer for "
                    "image-bearing prompts"
                )
            return self._build_image_training_example(
                messages,
                train_on=train_on,
                train_on_eos=train_on_eos,
                max_length=max_length,
                tools=tools,
            )
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

    def _build_image_training_example(
        self,
        messages: list[Message],
        *,
        train_on: TrainOnWhat,
        train_on_eos: bool,
        max_length: int | None,
        tools: list[ToolSpec] | None,
    ) -> TrainingExample:
        """Build V4.1 chunks while keeping image bytes in document order."""
        placeholder_id = self.tokenizer.convert_tokens_to_ids(_IMAGE_PLACEHOLDER)
        if placeholder_id is None or placeholder_id == getattr(
            self.tokenizer, "unk_token_id", None
        ):
            raise ValueError(
                f"Tokenizer does not recognize {_IMAGE_PLACEHOLDER!r}; "
                "DeepSeek V4.1 image training requires the vision tokenizer."
            )

        builder = _ChunkBuilder()

        def emit(text: str, weight: float) -> None:
            if text:
                builder.add_text(
                    self.tokenizer.encode(text, add_special_tokens=False), weight
                )

        def emit_with_images(
            text: str, image_parts: list[ImagePart], weight: float
        ) -> None:
            pieces = text.split(_IMAGE_PLACEHOLDER)
            if len(pieces) != len(image_parts) + 1:
                raise ValueError(
                    "DeepSeek V4.1 rendered image placeholders do not match "
                    f"image parts ({len(pieces) - 1} placeholders, "
                    f"{len(image_parts)} images)"
                )
            emit(pieces[0], weight)
            for part, suffix in zip(image_parts, pieces[1:], strict=True):
                height, width = image_part_size(part)
                builder.add_image(
                    data=part["image"],
                    format=part["format"],
                    expected_tokens=self.image_token_count(height, width),
                    placeholder_id=int(placeholder_id),
                )
                emit(suffix, weight)

        emit(self._prefix(messages, tools), 0.0)

        last_assistant = max(
            (idx for idx, msg in enumerate(messages) if msg["role"] == "assistant"),
            default=-1,
        )
        if self.thinking and train_on == TrainOnWhat.ALL_ASSISTANT:
            assistants = sum(1 for msg in messages if msg["role"] == "assistant")
            if assistants > 1:
                raise ValueError(
                    "train_on=ALL_ASSISTANT cannot be represented in thinking "
                    "mode: the DeepSeek V4 template drops reasoning from every "
                    "history assistant turn, so only the final one can carry "
                    "the target layout. Train one turn per example "
                    "(LAST_ASSISTANT over progressively longer prefixes), or "
                    "use thinking=False, where history and generation share "
                    "the same </think> prefill."
                )

        rendered = self._render_all(
            messages,
            tools,
            generated_turn=last_assistant if last_assistant >= 0 else None,
        )
        for idx, (header, content) in enumerate(rendered):
            is_assistant = messages[idx]["role"] == "assistant"
            if train_on == TrainOnWhat.LAST_ASSISTANT:
                trainable = is_assistant and idx == last_assistant
            elif train_on == TrainOnWhat.ALL_ASSISTANT:
                trainable = is_assistant
            else:
                trainable = False

            emit(header, 0.0)
            message_images = self._image_parts([messages[idx]])
            if trainable and not train_on_eos and content.endswith(_EOS):
                emit_with_images(content[: -len(_EOS)], message_images, 1.0)
                emit(_EOS, 0.0)
            else:
                emit_with_images(content, message_images, 1.0 if trainable else 0.0)

        builder.finish()
        input_ids = builder.flat_ids
        weights = builder.weights
        model_input = builder.chunks
        if max_length is not None and len(input_ids) > max_length:
            model_input, expanded_length = _truncate_chunks_to_length(
                model_input, max_length
            )
            input_ids = input_ids[:expanded_length]
            weights = weights[:expanded_length]
        return TrainingExample(
            input_ids=input_ids,
            weights=weights,
            model_input=model_input,
        )

    # ── Tool support ─────────────────────────────────────────────────

    def build_system_message_with_tools(
        self, tools: list[ToolSpec], system_prompt: str = ""
    ) -> Message:
        """Bake the DSML tools block into a system message.

        Produces exactly what passing ``tools=`` to :meth:`build_prompt_str`
        renders, so pre-baking and inline rendering are interchangeable —
        but do BOTH and the block lands in the prompt twice.
        """
        block = dsml_tools_block(tools, self.dialect) if tools else ""
        if system_prompt and block:
            return Message(role="system", content=system_prompt + "\n\n" + block)
        return Message(role="system", content=block or system_prompt)

    def _format_tool_calls(self, tool_calls: list[ToolCall]) -> str:
        """Format tool calls as one DSML ``tool_calls`` block.

        Values carry an explicit ``string`` flag: ``true`` means the element
        text IS the string value, ``false`` means it is JSON. That flag is
        how the model (and both parsers) tell ``"3"`` from ``3``.
        """
        d = self.dialect
        invokes: list[str] = []
        for call in tool_calls:
            name = call["function"]["name"]
            if d.namespaces:
                # `tool_calls_from_openai_format`: the call-level namespace
                # wins over the function-level one; `::` in the name is the
                # same information spelled inline.
                fields: Any = call
                namespace = fields.get("namespace") or fields["function"].get(
                    "namespace"
                )
                if namespace is not None and not isinstance(namespace, str):
                    raise ValueError(
                        f"tool call namespace must be a string, got {namespace!r}"
                    )
                name = qualified_tool_name(name, namespace)
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
                for marker in d.close_markers:
                    if marker in text:
                        raise ValueError(
                            f"tool {name!r} parameter {key!r} contains "
                            f"{marker!r}, which would terminate the enclosing "
                            "DSML element early; DSML has no escape for it."
                        )
                params.append(
                    f'{d.param_open} name="{key}" '
                    f'string="{"true" if is_str else "false"}">'
                    f"{text}{d.param_close}"
                )
            # The encoder builds the body as "\n".join(params) and wraps it
            # in "\n...\n", so a zero-parameter invoke carries TWO newlines,
            # not one. Joining with a trailing newline per param collapses
            # that to one and diverges on every argument-less call.
            body = "\n".join(params)
            invokes.append(
                f'{d.invoke_open} name="{name}">\n{body}\n{d.invoke_close}\n'
            )
        return f"\n\n{d.calls_open}\n{''.join(invokes)}{d.calls_close}"

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
            self._reject_literal_image_placeholder(explicit)
            return explicit, self._text_of(message)
        content = message["content"]
        if isinstance(content, str):
            self._reject_literal_image_placeholder(content)
            if _THINK_CLOSE in content:
                head, _, tail = content.partition(_THINK_CLOSE)
                reasoning = head.rstrip("\n").split(_THINK_OPEN)[-1]
                return reasoning.strip(), tail.lstrip("\n")
            return "", content
        reasoning = "".join(p["thinking"] for p in content if p["type"] == "thinking")
        self._reject_literal_image_placeholder(reasoning)
        text = self._text_of(message)
        return reasoning.strip(), text

    def _text_of(self, message: Message) -> str:
        """Rendered text/placeholder content of one message."""
        content = message["content"]
        if isinstance(content, str):
            self._reject_literal_image_placeholder(content)
            return content
        if not self.v41:
            self._reject_non_text_parts(content)
            return "".join(p["text"] for p in content if p["type"] == "text")

        rendered: list[str] = []
        for part in content:
            if part["type"] == "text":
                text = cast(TextPart, part)["text"]
                self._reject_literal_image_placeholder(text)
                rendered.append(text)
            elif part["type"] == "image":
                rendered.append(_IMAGE_PLACEHOLDER)
            elif part["type"] != "thinking":
                raise ValueError(f"Unsupported content part type: {part['type']!r}")
        # V4.1's process_image_messages + render_message pair joins structured
        # content blocks with blank lines, including adjacent text blocks.
        return "\n\n".join(rendered)

    def _image_parts(self, messages: list[Message]) -> list[ImagePart]:
        """Return validated V4.1 images in prompt/document order."""
        parts: list[ImagePart] = []
        for message in messages:
            content = message["content"]
            if isinstance(content, str):
                continue
            for part in content:
                if part["type"] != "image":
                    continue
                if not self.v41:
                    self._reject_non_text_parts(content)
                image = cast(ImagePart, part)
                # Validate inline bytes (or explicit ImageHandle dimensions)
                # before the request reaches the server-side processor.
                _ = image_part_size(image)
                parts.append(image)
        return parts

    @staticmethod
    def _contains_images(messages: list[Message]) -> bool:
        return any(
            not isinstance(message["content"], str)
            and any(part["type"] == "image" for part in message["content"])
            for message in messages
        )

    def _reject_literal_image_placeholder(self, text: str) -> None:
        if self.v41 and _IMAGE_PLACEHOLDER in text:
            raise ValueError(
                f"Message text contains image placeholder {_IMAGE_PLACEHOLDER!r}; "
                "provide images as image_part(...) content blocks instead."
            )

    def _reject_non_text_parts(self, parts: list[ContentPart]) -> None:
        """Fail loudly on content this text-only renderer cannot express.

        DeepSeek V4 Flash has no vision tower. Silently dropping image parts
        would produce a corrupt prompt rather than an obvious error.
        """
        for p in parts:
            if p["type"] not in ("text", "thinking"):
                raise ValueError(
                    f"{type(self).__name__} cannot render {p['type']!r} content "
                    "parts; this renderer is text-only."
                )
