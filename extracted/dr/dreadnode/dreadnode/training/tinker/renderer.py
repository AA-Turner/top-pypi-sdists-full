"""Model-specific renderers for encoding OpenAI conversations into token sequences.

Each renderer knows how to format tool calls, thinking traces, and role headers
for a specific model family. The base class provides shared logic for
supervised-example construction (autoregressive shift + weight masking).

Renderers mirror the canonical chat_template from each model's
tokenizer_config.json so SFT sequences match the bytes the base model saw
during post-training. Sources are cited per renderer class.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import UTC, datetime
from enum import StrEnum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from dreadnode.training.etl.worlds import OpenAIMessage, ToolSchema


class TrainOnWhat(StrEnum):
    """Which assistant tokens to include in the loss."""

    ALL_ASSISTANT_MESSAGES = "all_assistant_messages"
    LAST_ASSISTANT_MESSAGE = "last_assistant_message"


class Renderer(ABC):
    """Base class for model-specific conversation renderers."""

    def __init__(self, tokenizer: Any) -> None:
        self._tokenizer = tokenizer

    @abstractmethod
    def encode_conversation(
        self,
        messages: list[OpenAIMessage],
        tools: list[ToolSchema] | None = None,
    ) -> tuple[list[int], list[float]]:
        """Encode a conversation into tokens and per-token weights.

        Returns:
            Tuple of (tokens, weights) where weights are 1.0 for assistant
            tokens and 0.0 for everything else.
        """
        ...

    def build_supervised_example(
        self,
        messages: list[OpenAIMessage],
        tools: list[ToolSchema] | None = None,
        train_on_what: TrainOnWhat = TrainOnWhat.ALL_ASSISTANT_MESSAGES,
    ) -> tuple[list[int], list[float]]:
        """Encode and apply train_on_what masking.

        Returns tokens and weights BEFORE autoregressive shift — the caller
        (datum builder) handles the shift.
        """
        tokens, weights = self.encode_conversation(messages, tools)

        if train_on_what == TrainOnWhat.LAST_ASSISTANT_MESSAGE:
            weights = _mask_all_but_last_assistant(messages, weights)

        return tokens, weights

    def _encode(self, text: str, *, add_special_tokens: bool = False) -> list[int]:
        return self._tokenizer.encode(text, add_special_tokens=add_special_tokens)

    def _append(
        self,
        tokens: list[int],
        weights: list[float],
        text: str,
        weight: float,
        *,
        add_special_tokens: bool = False,
    ) -> None:
        """Encode `text`, append its tokens to `tokens`, and extend `weights` with `weight`."""
        toks = self._encode(text, add_special_tokens=add_special_tokens)
        tokens.extend(toks)
        weights.extend([weight] * len(toks))


def _mask_all_but_last_assistant(
    messages: list[OpenAIMessage],
    weights: list[float],
) -> list[float]:
    """Zero out weights for all assistant segments except the last one."""
    if not any(msg.get("role") == "assistant" for msg in messages):
        return weights

    new_weights = [0.0] * len(weights)
    regions: list[tuple[int, int]] = []
    in_region = False
    start = 0
    for i, w in enumerate(weights):
        if w > 0 and not in_region:
            in_region = True
            start = i
        elif w == 0 and in_region:
            in_region = False
            regions.append((start, i))
    if in_region:
        regions.append((start, len(weights)))

    if regions:
        last_start, last_end = regions[-1]
        for i in range(last_start, last_end):
            new_weights[i] = weights[i]

    return new_weights


# ---------------------------------------------------------------------------
# Qwen3 Renderer
# ---------------------------------------------------------------------------


class Qwen3Renderer(Renderer):
    """Renderer for Qwen 3.x models.

    Mirrors the canonical chat template from Qwen/Qwen3-8B
    (``tokenizer_config.json``): ChatML framing with ``<|im_start|>`` /
    ``<|im_end|>``, ``<tools>...</tools>`` XML preamble for tool defs,
    ``<tool_call>``/``<tool_response>`` blocks for invocations and results,
    and ``user``-role coalescing of consecutive tool results.
    """

    def encode_conversation(
        self,
        messages: list[OpenAIMessage],
        tools: list[ToolSchema] | None = None,
    ) -> tuple[list[int], list[float]]:
        tokens: list[int] = []
        weights: list[float] = []

        # Identify the index of the final "real" user query so we know where
        # to enable <think>-block rendering (canonical: only assistant turns
        # after the last user query may surface reasoning content).
        last_query_index = len(messages) - 1
        for i in range(len(messages) - 1, -1, -1):
            msg = messages[i]
            if msg.get("role") != "user":
                continue
            content = msg.get("content") or ""
            if (
                isinstance(content, str)
                and content.startswith("<tool_response>")
                and content.endswith("</tool_response>")
            ):
                continue
            last_query_index = i
            break

        first_is_system = bool(messages) and messages[0].get("role") == "system"
        system_consumed_by_tools = False

        if tools:
            self._append(tokens, weights, "<|im_start|>system\n", 0.0)
            if first_is_system:
                self._append(
                    tokens,
                    weights,
                    (messages[0].get("content") or "") + "\n\n",
                    0.0,
                )
                system_consumed_by_tools = True
            self._append(tokens, weights, self._tool_preamble_body(tools), 0.0)
        elif first_is_system:
            content = messages[0].get("content") or ""
            self._append(tokens, weights, f"<|im_start|>system\n{content}<|im_end|>\n", 0.0)
            system_consumed_by_tools = True

        for i, msg in enumerate(messages):
            if i == 0 and first_is_system and system_consumed_by_tools:
                continue

            role = msg.get("role", "user")
            content = msg.get("content") or ""
            tool_calls = msg.get("tool_calls") or []

            if role in ("user", "system"):
                self._append(
                    tokens,
                    weights,
                    f"<|im_start|>{role}\n{content}<|im_end|>\n",
                    0.0,
                )

            elif role == "assistant":
                reasoning, display_content = _split_qwen_thinking(content)
                allow_think = i > last_query_index
                is_last = i == len(messages) - 1
                emit_think_block = allow_think and (is_last or bool(reasoning))

                if emit_think_block:
                    header = (
                        "<|im_start|>assistant\n"
                        f"<think>\n{reasoning}\n</think>\n\n"
                        f"{display_content.lstrip(chr(10))}"
                    )
                else:
                    header = f"<|im_start|>assistant\n{display_content}"

                # Header (<|im_start|>assistant\n) is prompt tokens (weight 0);
                # content and everything after is the model's target (weight 1).
                self._append(tokens, weights, "<|im_start|>assistant\n", 0.0)
                body = header[len("<|im_start|>assistant\n") :]
                if body:
                    self._append(tokens, weights, body, 1.0)

                for tc_idx, tc in enumerate(tool_calls):
                    func = tc.get("function", {})
                    name = func.get("name", "") or ""
                    args = func.get("arguments", "")
                    needs_newline = (tc_idx == 0 and bool(display_content)) or tc_idx > 0
                    lead = "\n" if needs_newline else ""
                    rendered_args = _serialize_tool_arguments(args)
                    self._append(
                        tokens,
                        weights,
                        (
                            f"{lead}<tool_call>\n"
                            f'{{"name": "{name}", "arguments": {rendered_args}}}\n'
                            f"</tool_call>"
                        ),
                        1.0,
                    )

                self._append(tokens, weights, "<|im_end|>\n", 1.0)

            elif role == "tool":
                prev_role = messages[i - 1].get("role") if i > 0 else None
                next_role = messages[i + 1].get("role") if i + 1 < len(messages) else None
                opens_block = prev_role != "tool"
                closes_block = next_role != "tool"

                if opens_block:
                    self._append(tokens, weights, "<|im_start|>user", 0.0)
                self._append(
                    tokens,
                    weights,
                    f"\n<tool_response>\n{content}\n</tool_response>",
                    0.0,
                )
                if closes_block:
                    self._append(tokens, weights, "<|im_end|>\n", 0.0)

        return tokens, weights

    @staticmethod
    def _tool_preamble_body(tools: list[ToolSchema]) -> str:
        """Render the ``# Tools`` body (inside the system block, closes with ``<|im_end|>\\n``)."""
        parts = [
            "# Tools\n\n",
            "You may call one or more functions to assist with the user query.\n\n",
            "You are provided with function signatures within <tools></tools> XML tags:\n",
            "<tools>",
        ]
        for tool in tools:
            parts.append("\n" + json.dumps(tool, ensure_ascii=False))
        parts.append(
            "\n</tools>\n\n"
            "For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:\n"
            '<tool_call>\n{"name": <function-name>, "arguments": <args-json-object>}\n</tool_call>'
            "<|im_end|>\n"
        )
        return "".join(parts)


def _split_qwen_thinking(content: str) -> tuple[str, str]:
    """Extract a ``<think>...</think>`` block from assistant content (Qwen semantics).

    Returns (reasoning, remaining_content). If no block is present, reasoning is "".
    """
    if "</think>" not in content:
        return "", content
    pre, _, post = content.partition("</think>")
    reasoning = pre.split("<think>")[-1].lstrip("\n").rstrip("\n")
    return reasoning, post.lstrip("\n")


def _serialize_tool_arguments(args: Any) -> str:
    """Serialize tool-call arguments for emission as a JSON value.

    OpenAI's wire format types ``arguments`` as a JSON string. Qwen3's canonical
    template passes a string through untouched (the caller is expected to have
    already JSON-formatted it), and applies ``tojson`` otherwise. We parse
    JSON-string inputs and re-emit as compact JSON so that emitted bytes are
    stable regardless of caller formatting.
    """
    if isinstance(args, dict):
        return json.dumps(args, ensure_ascii=False)
    if isinstance(args, str):
        try:
            parsed = json.loads(args)
        except (json.JSONDecodeError, ValueError):
            return args
        return json.dumps(parsed, ensure_ascii=False)
    return json.dumps(args, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Nemotron3 Renderer
# ---------------------------------------------------------------------------


class Nemotron3Renderer(Renderer):
    """Renderer for Nemotron 3 models.

    Uses the same ``<|im_start|>`` / ``<|im_end|>`` framing as Qwen but
    renders tool declarations in XML format within the system message and
    tool calls as XML-structured parameters.
    """

    def encode_conversation(
        self,
        messages: list[OpenAIMessage],
        tools: list[ToolSchema] | None = None,
    ) -> tuple[list[int], list[float]]:
        tokens: list[int] = []
        weights: list[float] = []
        first = True

        if tools:
            tool_text = self._format_tools_xml(tools)
            header = "<|im_start|>system\n"
            footer = "<|im_end|>\n"
            h_toks = self._encode(header, add_special_tokens=first)
            first = False
            tokens.extend(h_toks)
            weights.extend([0.0] * len(h_toks))
            b_toks = self._encode(tool_text)
            tokens.extend(b_toks)
            weights.extend([0.0] * len(b_toks))
            f_toks = self._encode(footer)
            tokens.extend(f_toks)
            weights.extend([0.0] * len(f_toks))

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            tool_calls = msg.get("tool_calls")
            is_assistant = role == "assistant"

            header = f"<|im_start|>{role}\n"
            h_toks = self._encode(header, add_special_tokens=first)
            first = False
            tokens.extend(h_toks)
            weights.extend([0.0] * len(h_toks))

            body_parts: list[str] = []
            if content:
                body_parts.append(content)
            if tool_calls:
                for tc in tool_calls:
                    func = tc.get("function", {})
                    name = func.get("name", "")
                    args_str = func.get("arguments", "{}")
                    tc_text = (
                        "<tool_call>\n"
                        f"<name>{name}</name>\n"
                        f"<arguments>{args_str}</arguments>\n"
                        "</tool_call>"
                    )
                    body_parts.append(tc_text)
            if role == "tool":
                body_text = f"<tool_response>\n{content}\n</tool_response>" if content else ""
            else:
                body_text = "\n".join(body_parts)

            b_toks = self._encode(body_text or "")
            tokens.extend(b_toks)
            weights.extend([1.0 if is_assistant else 0.0] * len(b_toks))

            footer = "<|im_end|>\n"
            f_toks = self._encode(footer)
            tokens.extend(f_toks)
            weights.extend([1.0 if is_assistant else 0.0] * len(f_toks))

        return tokens, weights

    def _format_tools_xml(self, tools: list[ToolSchema]) -> str:
        lines = ["<tools>"]
        for tool in tools:
            func = tool.get("function", {})
            name = func.get("name", "")
            desc = func.get("description", "")
            params = json.dumps(func.get("parameters", {}), ensure_ascii=False)
            lines.append(
                f"<tool>\n<name>{name}</name>\n"
                f"<description>{desc}</description>\n"
                f"<parameters>{params}</parameters>\n</tool>"
            )
        lines.append("</tools>")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# GPT OSS Renderer
# ---------------------------------------------------------------------------


class GptOssRenderer(Renderer):
    """Renderer for gpt-oss (harmony) models.

    Mirrors the canonical ``chat_template.jinja`` from ``openai/gpt-oss-20b``.
    The harmony format is structured around ``<|start|>``/``<|end|>`` frames,
    explicit ``<|channel|>`` headers (``analysis``, ``commentary``, ``final``),
    and a dedicated ``developer`` role for instructions and tool definitions.

    Tool calls ride on the ``<|start|>`` header (``assistant to=functions.X``)
    and are terminated with ``<|call|>`` *in place of* ``<|end|>``. Tool
    results use a ``functions.X to=assistant`` header on the ``commentary``
    channel. The very last assistant turn in a training example closes with
    ``<|return|>``; earlier assistant turns close with ``<|end|>``.
    """

    DEFAULT_MODEL_IDENTITY = "You are ChatGPT, a large language model trained by OpenAI."
    DEFAULT_KNOWLEDGE_CUTOFF = "2024-06"
    DEFAULT_REASONING_EFFORT = "medium"

    def __init__(
        self,
        tokenizer: Any,
        *,
        model_identity: str | None = None,
        knowledge_cutoff: str | None = None,
        reasoning_effort: str | None = None,
        today_date: str | None = None,
    ) -> None:
        super().__init__(tokenizer)
        self._model_identity = model_identity or self.DEFAULT_MODEL_IDENTITY
        self._knowledge_cutoff = knowledge_cutoff or self.DEFAULT_KNOWLEDGE_CUTOFF
        self._reasoning_effort = reasoning_effort or self.DEFAULT_REASONING_EFFORT
        self._today_date = today_date or datetime.now(UTC).strftime("%Y-%m-%d")

    def encode_conversation(
        self,
        messages: list[OpenAIMessage],
        tools: list[ToolSchema] | None = None,
    ) -> tuple[list[int], list[float]]:
        tokens: list[int] = []
        weights: list[float] = []

        # Mandatory system block: identity / cutoff / date / reasoning /
        # channels spec. Always emitted, even for zero-turn examples.
        self._append(
            tokens,
            weights,
            f"<|start|>system<|message|>{self._build_system_body(tools)}<|end|>",
            0.0,
        )

        # Developer block: emitted if the caller passed a system/developer
        # message (pulled from messages[0]) OR tools are present.
        developer_message = ""
        loop_messages: list[OpenAIMessage] = list(messages)
        if loop_messages and loop_messages[0].get("role") in ("developer", "system"):
            developer_message = loop_messages[0].get("content") or ""
            loop_messages = loop_messages[1:]

        if developer_message or tools:
            parts = ["<|start|>developer<|message|>"]
            if developer_message:
                parts.append(f"# Instructions\n\n{developer_message}\n\n")
            if tools:
                parts.append("# Tools\n\n")
                parts.append(_render_typescript_namespace("functions", tools))
            parts.append("<|end|>")
            self._append(tokens, weights, "".join(parts), 0.0)

        last_tool_call_name: str | None = None
        for idx, msg in enumerate(loop_messages):
            role = msg.get("role")
            content = msg.get("content") or ""
            tool_calls = msg.get("tool_calls") or []
            is_last = idx == len(loop_messages) - 1

            if role == "user":
                self._append(
                    tokens,
                    weights,
                    f"<|start|>user<|message|>{content}<|end|>",
                    0.0,
                )

            elif role == "assistant":
                if tool_calls:
                    # Canonical logic: keep analysis CoT only if no future
                    # assistant final-answer message overrides it.
                    future_final = any(
                        future.get("role") == "assistant" and not (future.get("tool_calls") or [])
                        for future in loop_messages[idx + 1 :]
                    )
                    if content and not future_final:
                        self._append(
                            tokens, weights, "<|start|>assistant<|channel|>analysis<|message|>", 0.0
                        )
                        self._append(tokens, weights, f"{content}<|end|>", 1.0)

                    # Template assumes at most one tool call per message; we
                    # follow that invariant (ATIF → OpenAI conversion keeps
                    # them as separate assistant turns if the model emitted
                    # multiple). Emit only the first call.
                    tc = tool_calls[0]
                    func = tc.get("function", {})
                    name = func.get("name", "") or ""
                    args = func.get("arguments", "")
                    rendered_args = _serialize_tool_arguments(args)
                    self._append(
                        tokens,
                        weights,
                        f"<|start|>assistant to=functions.{name}<|channel|>commentary json<|message|>",
                        0.0,
                    )
                    self._append(tokens, weights, f"{rendered_args}<|call|>", 1.0)
                    last_tool_call_name = name
                else:
                    self._append(
                        tokens,
                        weights,
                        "<|start|>assistant<|channel|>final<|message|>",
                        0.0,
                    )
                    terminator = "<|return|>" if is_last else "<|end|>"
                    self._append(tokens, weights, f"{content}{terminator}", 1.0)
                    last_tool_call_name = None

            elif role == "tool":
                tool_name = last_tool_call_name or msg.get("tool_call_id") or "unknown"
                self._append(
                    tokens,
                    weights,
                    (
                        f"<|start|>functions.{tool_name} to=assistant<|channel|>commentary<|message|>"
                        f"{json.dumps(content, ensure_ascii=False)}<|end|>"
                    ),
                    0.0,
                )

        return tokens, weights

    def _build_system_body(self, tools: list[ToolSchema] | None) -> str:
        lines = [
            self._model_identity,
            f"Knowledge cutoff: {self._knowledge_cutoff}",
            f"Current date: {self._today_date}",
            "",
            f"Reasoning: {self._reasoning_effort}",
            "",
            "# Valid channels: analysis, commentary, final. Channel must be included for every message.",
        ]
        body = "\n".join(lines)
        if tools:
            body += "\nCalls to these tools must go to the commentary channel: 'functions'."
        return body


def _render_typescript_namespace(namespace: str, tools: list[ToolSchema]) -> str:
    """Render tool definitions as a TypeScript namespace (harmony format).

    Mirrors the ``render_tool_namespace`` macro in the canonical
    ``chat_template.jinja``. Produces blocks of the form::

        ## functions

        namespace functions {

        // description
        type name = (_: {
        // param description
        param?: string,
        }) => any;

        } // namespace functions
    """
    out = [f"## {namespace}\n\n", f"namespace {namespace} {{\n\n"]
    for tool in tools:
        func = tool.get("function", {})
        name = func.get("name", "") or ""
        description = func.get("description", "") or ""
        out.append(f"// {description}\n")
        out.append(f"type {name} = ")

        parameters = func.get("parameters", {}) or {}
        properties = parameters.get("properties") or {}
        required = set(parameters.get("required") or [])
        if properties:
            out.append("(_: {\n")
            for pname, pspec in properties.items():
                pdesc = (pspec or {}).get("description")
                if pdesc:
                    out.append(f"// {pdesc}\n")
                optional = "" if pname in required else "?"
                ts_type = _render_typescript_type(pspec or {})
                default_suffix = ""
                if "default" in (pspec or {}):
                    default = pspec["default"]
                    default_suffix = f", // default: {json.dumps(default, ensure_ascii=False)}"
                out.append(f"{pname}{optional}: {ts_type}{default_suffix},\n")
            out.append("}) => any;\n\n")
        else:
            out.append("() => any;\n\n")

    out.append(f"}} // namespace {namespace}")
    return "".join(out)


def _render_typescript_type(spec: Any) -> str:
    """Render a JSON-schema property as a TypeScript type (harmony-compatible).

    Implements the shape of the ``render_typescript_type`` macro in the
    canonical template. Coverage is pragmatic: strings (with enums), numbers,
    integers (as number), booleans, objects (nested or plain), and arrays.
    """
    if not isinstance(spec, dict):
        return "any"
    spec_type = spec.get("type")
    nullable_suffix = " | null" if spec.get("nullable") else ""

    if spec_type == "array":
        items = spec.get("items") or {}
        inner = items.get("type")
        if inner == "string":
            return "string[]" + nullable_suffix
        if inner in ("number", "integer"):
            return "number[]" + nullable_suffix
        if inner == "boolean":
            return "boolean[]" + nullable_suffix
        return "any[]" + nullable_suffix
    if spec_type == "string":
        enum = spec.get("enum")
        if enum:
            return '"' + '" | "'.join(enum) + '"'
        return "string" + nullable_suffix
    if spec_type in ("number", "integer"):
        return "number"
    if spec_type == "boolean":
        return "boolean"
    if spec_type == "object":
        properties = spec.get("properties") or {}
        if not properties:
            return "object"
        required = set(spec.get("required") or [])
        parts: list[str] = []
        for pname, pspec in properties.items():
            optional = "" if pname in required else "?"
            parts.append(f"{pname}{optional}: {_render_typescript_type(pspec or {})}")
        return "{\n" + ", ".join(parts) + "}"
    return "any"


# ---------------------------------------------------------------------------
# Llama 3.1 Renderer
# ---------------------------------------------------------------------------


class LlamaRenderer(Renderer):
    """Renderer for Llama 3.1 / 3.2 / 3.3 Instruct models.

    Base framing mirrors the minimal chat template shipped in
    ``meta-llama/Llama-3.1-8B-Instruct``'s ``tokenizer_config.json``
    (``<|begin_of_text|>`` BOS + ``<|start_header_id|>{role}<|end_header_id|>``
    headers + ``<|eot_id|>`` terminators + ``ipython`` role for tool results).

    When tools are provided, the system block is extended with the
    ``Environment: ipython`` / ``Cutting Knowledge Date`` / ``Today Date``
    preamble documented at https://www.llama.com/docs/model-cards-and-prompt-formats/llama3_1/
    followed by the custom JSON-tool instruction string and the tool schemas.
    Tool calls from the model are rendered as a raw JSON object
    ``{"name": ..., "parameters": {...}}`` (note: ``parameters``, not
    ``arguments``) as the assistant's content.
    """

    DEFAULT_KNOWLEDGE_CUTOFF = "December 2023"
    DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant"

    _TOOL_INSTRUCTION = (
        "You are a helpful assistant with tool calling capabilities. "
        "When you receive a tool call response, use the output to format an answer "
        "to the original user question. If you decide to invoke any of the function(s), "
        'you MUST put it in the format of {"name": function name, "parameters": dictionary of argument name and its value}. '
        "Do not use variables."
    )

    def __init__(
        self,
        tokenizer: Any,
        *,
        knowledge_cutoff: str | None = None,
        today_date: str | None = None,
        default_system_prompt: str | None = None,
    ) -> None:
        super().__init__(tokenizer)
        self._knowledge_cutoff = knowledge_cutoff or self.DEFAULT_KNOWLEDGE_CUTOFF
        self._today_date = today_date or datetime.now(UTC).strftime("%d %B %Y")
        self._default_system_prompt = default_system_prompt or self.DEFAULT_SYSTEM_PROMPT

    def encode_conversation(
        self,
        messages: list[OpenAIMessage],
        tools: list[ToolSchema] | None = None,
    ) -> tuple[list[int], list[float]]:
        tokens: list[int] = []
        weights: list[float] = []

        rendered = list(self._prepare_messages(messages, tools))

        self._append(tokens, weights, "<|begin_of_text|>", 0.0)
        for msg in rendered:
            role = msg.get("role") or "user"
            content = (msg.get("content") or "").strip()
            is_assistant = role == "assistant"

            self._append(
                tokens,
                weights,
                f"<|start_header_id|>{role}<|end_header_id|>\n\n",
                0.0,
            )
            self._append(
                tokens,
                weights,
                f"{content}<|eot_id|>",
                1.0 if is_assistant else 0.0,
            )

        return tokens, weights

    def _prepare_messages(
        self,
        messages: list[OpenAIMessage],
        tools: list[ToolSchema] | None,
    ) -> list[OpenAIMessage]:
        """Transform OpenAI-shaped messages into Llama-3.1 wire-shape.

        - ``tool`` role becomes ``ipython``.
        - Assistant messages with ``tool_calls`` have their content replaced
          by the JSON-tool-call object (``{"name": ..., "parameters": ...}``).
        - When ``tools`` is non-empty, the system message is augmented with
          the ``Environment: ipython`` preamble and the tool-schema block.
        """
        has_system = bool(messages) and messages[0].get("role") == "system"
        user_system_content = messages[0].get("content") if has_system else ""
        body_messages = messages[1:] if has_system else list(messages)

        out: list[OpenAIMessage] = []

        if tools or has_system or user_system_content:
            system_text = self._build_system_body(user_system_content or "", tools)
            out.append({"role": "system", "content": system_text})

        for msg in body_messages:
            role = msg.get("role")
            content = msg.get("content") or ""
            tool_calls = msg.get("tool_calls") or []

            if role == "tool":
                out.append({"role": "ipython", "content": content})  # type: ignore[typeddict-item]
                continue

            if role == "assistant" and tool_calls:
                tc = tool_calls[0]
                func = tc.get("function", {})
                name = func.get("name", "") or ""
                args = func.get("arguments", "")
                try:
                    parsed_args = json.loads(args) if isinstance(args, str) else args
                except (json.JSONDecodeError, ValueError):
                    parsed_args = args
                call_json = json.dumps(
                    {"name": name, "parameters": parsed_args},
                    ensure_ascii=False,
                )
                body = f"{content}\n\n{call_json}" if content else call_json
                out.append({"role": "assistant", "content": body})
                continue

            out.append({"role": role, "content": content})  # type: ignore[typeddict-item]

        return out

    def _build_system_body(self, user_system_content: str, tools: list[ToolSchema] | None) -> str:
        lines: list[str] = []
        if tools:
            lines.extend(
                [
                    "Environment: ipython",
                    f"Cutting Knowledge Date: {self._knowledge_cutoff}",
                    f"Today Date: {self._today_date}",
                    "",
                ]
            )

        lines.append(user_system_content.strip() or self._default_system_prompt)

        if tools:
            lines.append("")
            lines.append(self._TOOL_INSTRUCTION)
            for tool in tools:
                func = tool.get("function", {})
                schema = {
                    "name": func.get("name", ""),
                    "description": func.get("description", ""),
                    "parameters": func.get("parameters", {}),
                }
                lines.append("")
                lines.append(json.dumps(schema, ensure_ascii=False))

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# RoleColon Renderer (generic fallback)
# ---------------------------------------------------------------------------


class RoleColonRenderer(Renderer):
    """Generic fallback renderer using ``Role:\\ncontent\\n`` format.

    Equivalent to the existing ``convert_messages_to_datum`` logic. Does not
    have structured tool call support — tool calls are linearized to text.
    """

    def encode_conversation(
        self,
        messages: list[OpenAIMessage],
        tools: list[ToolSchema] | None = None,  # noqa: ARG002 — required by Renderer ABC; fallback does not use structured tool defs
    ) -> tuple[list[int], list[float]]:
        tokens: list[int] = []
        weights: list[float] = []
        first = True

        for msg in messages:
            role = _normalize_role(msg.get("role", "user"))
            content = msg.get("content", "") or ""
            tool_calls = msg.get("tool_calls")
            is_assistant = role == "assistant"

            # Linearize tool calls into content if present
            if tool_calls:
                tc_parts: list[str] = []
                for tc in tool_calls:
                    func = tc.get("function", {})
                    tc_parts.append(
                        f'<tool_call name="{func.get("name", "")}">'
                        f"{func.get('arguments', '')}</tool_call>"
                    )
                if content:
                    content = content + "\n\n" + "\n".join(tc_parts)
                else:
                    content = "\n".join(tc_parts)

            header = f"{role.capitalize()}:\n"
            h_toks = self._encode(header, add_special_tokens=first)
            first = False
            tokens.extend(h_toks)
            weights.extend([0.0] * len(h_toks))

            body = f"{content.strip()}\n" if content.strip() else "\n"
            b_toks = self._encode(body)
            tokens.extend(b_toks)
            weights.extend([1.0 if is_assistant else 0.0] * len(b_toks))

        return tokens, weights


def _normalize_role(role: str) -> str:
    mapping = {
        "user": "user",
        "human": "user",
        "assistant": "assistant",
        "ai": "assistant",
        "model": "assistant",
        "system": "system",
        "tool": "tool",
    }
    return mapping.get(role.strip().lower(), "user")


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------


def get_renderer(model_name: str, tokenizer: Any) -> Renderer:
    """Select a renderer based on model name pattern matching.

    Matched against ``model_name.lower()`` in priority order. ``gpt-oss`` is
    matched specifically (rather than ``gpt``) to avoid colliding with other
    GPT-family names that don't use the harmony format.
    """
    lower = model_name.lower()
    if "qwen" in lower:
        return Qwen3Renderer(tokenizer)
    if "llama" in lower:
        return LlamaRenderer(tokenizer)
    if "gpt-oss" in lower or "gpt_oss" in lower:
        return GptOssRenderer(tokenizer)
    if "nemotron" in lower:
        return Nemotron3Renderer(tokenizer)
    return RoleColonRenderer(tokenizer)


__all__ = [
    "GptOssRenderer",
    "LlamaRenderer",
    "Nemotron3Renderer",
    "Qwen3Renderer",
    "Renderer",
    "RoleColonRenderer",
    "TrainOnWhat",
    "get_renderer",
]
