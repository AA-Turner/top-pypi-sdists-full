"""Kimi K3 XTML text, reasoning, tool and supervised-training rendering.

Unlike K2, K3 uses separate message/think/response/tools elements. Response
parsing requires those special tokens to be preserved when decoding samples.
Images are not supported by the current K3 serving path and are rejected.
"""

from __future__ import annotations

import html
import json
import re
import unicodedata
from typing import Any

from river_client.renderers.tool_arguments import (
    decode_json_marked,
    find_outside_json_strings,
    standard_json,
)
from river_client.renderers.base import (
    append_visible_text,
    rejected_call_text,
    ContentPart,
    Message,
    ParsedResponse,
    Renderer,
    SamplePrompt,
    Tokenizer,
    ToolCall,
    ToolSpec,
    TrainOnWhat,
    TrainingExample,
    UnparsedToolCall,
)

END_OF_MESSAGE = "<|end_of_msg|>"
_ATTR = re.compile(r'([\w-]+)="([^"]*)"')
_SEP = "<|sep|>"


def _attr(value: str) -> str:
    return value.replace("&", "&amp;").replace('"', "&quot;")


def _open(element: str, **attributes: str) -> str:
    attrs = "".join(f' {key}="{_attr(value)}"' for key, value in attributes.items())
    return f"<|open|>{element}{attrs}<|sep|>"


def _close(element: str) -> str:
    return f"<|close|>{element}<|sep|>"


def _trim_incomplete_tag(text: str, *tags: str) -> str:
    """Remove only a trailing prefix of an expected structural tag."""
    start = max(text.rfind("<|open|>"), text.rfind("<|close|>"))
    if start >= 0:
        suffix = text[start:]
        if any(tag.startswith(suffix) and tag != suffix for tag in tags):
            return text[:start]
    return text


def _json(value: Any, *, compact: bool = False) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        allow_nan=False,
        **({"separators": (",", ":")} if compact else {}),
    )


def _value_type(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, (int, float)):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, list):
        return "array"
    raise ValueError(
        f"K3 tool arguments must contain JSON values, got {type(value).__name__}"
    )


def _content(message: Message) -> tuple[str, str]:
    content = message.get("content") or ""
    reasoning = message.get("reasoning_content") or message.get("reasoning") or ""
    if isinstance(content, str):
        return content, reasoning
    texts, thoughts = [], []
    for part in content:
        if part["type"] == "text":
            texts.append(part["text"])
        elif part["type"] == "thinking" and message["role"] == "assistant":
            thoughts.append(part["thinking"])
        else:
            raise ValueError(
                f"Kimi K3 does not support {part['type']!r} content in {message['role']} messages"
            )
    return "".join(texts), reasoning or "".join(thoughts)


def _normalize_messages(messages: list[Message]) -> list[Message]:
    """Order tool results by the preceding call IDs, as the reference does."""
    result = []
    calls = {}
    index = 0
    while index < len(messages):
        message = messages[index]
        if message["role"] == "assistant":
            calls = {}
            for position, call in enumerate(message.get("tool_calls") or []):
                if call.get("id") is not None and call["id"] not in calls:
                    calls[call["id"]] = (position, call["function"]["name"])
        if message["role"] != "tool":
            result.append(message)
            index += 1
            continue
        end = index
        while end < len(messages) and messages[end]["role"] == "tool":
            end += 1
        batch = messages[index:end]
        if all(message.get("tool_call_id") in calls for message in batch):
            for message in sorted(
                batch, key=lambda item: calls[item["tool_call_id"]][0]
            ):
                name = calls[message["tool_call_id"]][1]
                result.append({**message, "name": name, "tool": name})
        else:
            result.extend(batch)
        index = end
    return result


def _nonzero(digit: str) -> bool:
    return unicodedata.decimal(digit) != 0


def _typed_form_holds(arguments: dict[str, Any]) -> bool:
    """Whether typed ``argument`` elements can carry ``arguments`` losslessly.

    A key's attribute ends at the first ``<|sep|>``, and a string value is raw
    text that ends at its element's own close tag; neither has an escape.
    """
    return not any(
        _SEP in key or (isinstance(value, str) and _close("argument") in value)
        for key, value in arguments.items()
    )


def _tool_calls(tool_calls: list[ToolCall], rejected: str = "") -> str:
    """The tools channel: each call written so the parser reads it back.

    Calls use the reference's typed ``argument`` elements, except that a call
    those elements cannot hold losslessly goes as one ``json`` element, where
    quoted marker text is content. Both are forms the model emits.
    """
    parts = [_open("tools")]
    for index, call in enumerate(tool_calls, start=1):
        function = call["function"]
        parts.append(_open("call", tool=function["name"], index=str(index)))
        arguments = function.get("arguments")
        if isinstance(arguments, str):
            if arguments.strip():
                try:
                    arguments = json.loads(arguments)
                except json.JSONDecodeError:
                    parts.append(
                        _open("json", type="object") + arguments + _close("json")
                    )
                    arguments = None
                else:
                    if not isinstance(arguments, dict):
                        raise ValueError(
                            "Kimi K3 tool call arguments must be a JSON object"
                        )
            else:
                arguments = None
        if arguments is not None:
            if not isinstance(arguments, dict):
                raise ValueError("Kimi K3 tool call arguments must be a JSON object")
            if not _typed_form_holds(arguments):
                parts.append(
                    _open("json", type="object") + _json(arguments) + _close("json")
                )
                arguments = {}
            for key, value in sorted(arguments.items()):
                parts.append(
                    _open("argument", key=key, type=_value_type(value))
                    + (value if isinstance(value, str) else _json(value))
                    + _close("argument")
                )
        parts.append(_close("call"))
    return "".join(parts) + rejected + _close("tools")


_CALL_OPEN = "<|open|>call"
_ELEMENTS = ("argument", "json")


def _parse_tool_calls(
    text: str,
) -> tuple[list[ToolCall], list[UnparsedToolCall], list[str]]:
    """Parse a tools-channel body: (calls, rejected blocks, stray text).

    Each call element becomes a call or a rejected block, including one the
    output ends inside. Text between them is not a block: it stays visible,
    as River Serve keeps it, and renders in the response channel, where no
    markup is read as a call.
    """
    calls, errors, stray = [], [], []
    position = 0
    while position < len(text):
        at = text.find(_CALL_OPEN, position)
        if at == -1:
            at = len(text)
        if text[position:at].strip():
            stray.append(text[position:at].strip())
        if at == len(text):
            break
        position, result = _scan_call(text, at)
        (calls if "function" in result else errors).append(result)
    return calls, errors, stray


def _scan_call(text: str, at: int) -> tuple[int, ToolCall | UnparsedToolCall]:
    """Parse the call element opening at ``at``: where it ends, and the result.

    A value that carries JSON (a ``json`` element, or an argument whose type
    is not ``string``) runs to the first close tag outside a JSON string, so
    quoted marker text is content: it can neither end the call early nor
    start another one. A ``string`` argument is raw text, so its own close
    tag ends it.
    """
    header_end = text.find(_SEP, at + len(_CALL_OPEN))
    if header_end == -1:
        return len(text), {"raw_text": text[at:], "error": "Incomplete K3 tool call"}
    header = text[at + len(_CALL_OPEN) : header_end]
    arguments: dict[str, Any] = {}
    error = None
    elements = json_seen = False
    position = header_end + len(_SEP)
    while not text.startswith(_close("call"), position):
        element = next(
            (e for e in _ELEMENTS if text.startswith(f"<|open|>{e}", position)), None
        )
        if element is None:
            # Stray text: resume at the next element so its JSON values
            # still read as content, never as markup.
            found = [
                found_at
                for marker in (*(f"<|open|>{e}" for e in _ELEMENTS), _close("call"))
                if (found_at := text.find(marker, position)) != -1
            ]
            if not found:
                return len(text), {
                    "raw_text": text[at:],
                    "error": "Incomplete K3 tool call",
                }
            error = error or "Invalid K3 argument framing"
            position = min(found)
            continue
        attributes_end = text.find(_SEP, position + len(f"<|open|>{element}"))
        if attributes_end == -1:
            return len(text), {
                "raw_text": text[at:],
                "error": "Incomplete K3 tool call",
            }
        attributes = text[position + len(f"<|open|>{element}") : attributes_end]
        value_at = attributes_end + len(_SEP)
        expected = {"type"} if element == "json" else {"key", "type"}
        try:
            metadata = _attributes(attributes, expected)
        except ValueError as exc:
            metadata, error = None, error or str(exc)
        close_tag = _close(element)
        if element == "json" or metadata is None or metadata["type"] != "string":
            close_at, marker = find_outside_json_strings(text, (close_tag,), value_at)
            close_at = close_at if marker is not None else -1
        else:
            close_at = text.find(close_tag, value_at)
        if close_at == -1:
            return len(text), {
                "raw_text": text[at:],
                "error": "Incomplete K3 tool call",
            }
        value = text[value_at:close_at]
        position = close_at + len(close_tag)
        first, json_seen = not elements, json_seen or element == "json"
        elements = True
        if metadata is None or error is not None:
            continue
        if element == "json":
            # The whole arguments object; anything else is not a call.
            try:
                decoded = standard_json(value)
            except ValueError:
                decoded = None
            if not first or not isinstance(decoded, dict):
                error = "K3 JSON arguments must be one object"
            else:
                arguments = decoded
        elif json_seen:
            error = "K3 JSON arguments must be one object"
        elif metadata["key"] in arguments:
            error = "Duplicate K3 argument key"
        else:
            # The declared type marks a string or JSON; the tool validates
            # the value against its own schema.
            arguments[metadata["key"]] = (
                value if metadata["type"] == "string" else decode_json_marked(value)
            )
    end = position + len(_close("call"))
    raw_text = text[at:end]
    if error is None:
        try:
            attrs = _attributes(header, {"tool", "index"})
        except ValueError as exc:
            error = str(exc)
        else:
            name, index = attrs["tool"], attrs["index"]
            # Positive without int(): an index too long to convert must
            # reject the block, not raise.
            if not name or not index.isdecimal() or not any(map(_nonzero, index)):
                error = "K3 calls require a tool name and positive index"
    if error is not None:
        return end, {"raw_text": raw_text, "error": error}
    return end, {
        "type": "function",
        "id": f"functions.{name}:{index}",
        "function": {"name": name, "arguments": _json(arguments)},
    }


def _attributes(header: str, expected: set[str]) -> dict[str, str]:
    attributes = {}
    position = 0
    for match in _ATTR.finditer(header):
        if header[position : match.start()].strip() or match[1] in attributes:
            raise ValueError("Malformed or duplicate K3 attributes")
        attributes[match[1]] = html.unescape(match[2])
        position = match.end()
    if header[position:].strip() or attributes.keys() != expected:
        raise ValueError("Unexpected or missing K3 attributes")
    return attributes


def _controls(tool_choice, response_format, response_schema) -> str:
    parts = []

    def add(kind: str, content: str):
        parts.append(
            _open("message", role="system", type=kind)
            + content
            + _close("message")
            + END_OF_MESSAGE
        )

    if tool_choice not in (None, "auto", "required", "none"):
        raise ValueError("K3 tool_choice must be auto, required or none")
    if tool_choice in ("required", "none"):
        instruction = (
            "You MUST call tools"
            if tool_choice == "required"
            else "You MUST NOT call any tools"
        )
        add(
            "tool-choice",
            f"The system is invoked with `tool_choice={tool_choice}`.\n{instruction} in the next message.",
        )
    kind = (
        response_format.get("type")
        if isinstance(response_format, dict)
        else response_format
    )
    if kind not in (None, "text", "json_object", "json_schema"):
        raise ValueError("Unsupported K3 response_format")
    if kind in ("json_object", "json_schema"):
        content = f"The system is invoked with `response_format={kind}`.\nYour response must be raw JSON data without markdown code blocks (```json) or any additional formatting."
        if kind == "json_schema":
            schema = response_schema
            if schema is None and isinstance(response_format, dict):
                schema = response_format.get("json_schema")
                if isinstance(schema, dict):
                    schema = schema.get("schema", schema.get("json_schema", schema))
            content += (
                "\nThe JSON data must match the following schema:\n```json\n"
                + _json(schema, compact=True)
                + "\n```"
            )
        add("response-format", content)
    return "".join(parts)


class KimiK3Renderer(Renderer):
    """Text-only K3 renderer with retained reasoning by default, like serving."""

    def __init__(
        self,
        tokenizer: Tokenizer,
        *,
        thinking: bool = True,
        strip_thinking_from_history: bool = False,
        reasoning_effort: str = "max",
    ) -> None:
        super().__init__(tokenizer)
        if reasoning_effort not in {"low", "high", "max"}:
            raise ValueError("K3 reasoning_effort must be low, high or max")
        self.thinking = thinking
        self.strip_thinking_from_history = strip_thinking_from_history
        self.reasoning_effort = reasoning_effort

    def _generation_prompt(self) -> str:
        return _open("message", role="assistant") + _open(
            "think" if self.thinking else "response"
        )

    def _prefix(self, tools: list[ToolSpec] | None) -> str:
        parts = []
        if tools:
            declared = [
                tool if "function" in tool else {"type": "function", "function": tool}
                for tool in tools
            ]
            parts.append(
                _open("message", role="system", type="tool-declare")
                + "# Tools\nHere are the available tools, described in JSONSchema.\n\n```json\n"
                + _json(declared, compact=True)
                + "\n```"
                + _close("message")
                + END_OF_MESSAGE
            )
        if self.thinking:
            parts.append(
                _open("message", role="system", type="thinking-effort")
                + "`thinking_effort` guides on how much to think in your thinking channel (not including the response channel), supported values include `low`, `medium`, `high`, and `max`.\n"
                + f"Now the system is invoked with `thinking_effort={self.reasoning_effort}`."
                + _close("message")
                + END_OF_MESSAGE
            )
        return "".join(parts)

    def _render(self, messages: list[Message], *, generated_turn: int | None = None):
        messages = _normalize_messages(messages)
        # Training must use the selected target's inference context, not a
        # trailing user turn that has not happened when that target is sampled.
        last_user = max(
            (
                index
                for index, message in enumerate(messages[:generated_turn])
                if message["role"] == "user"
            ),
            default=-1,
        )
        calls, tool_index = [], 0
        for index, message in enumerate(messages):
            role = message["role"]
            if role not in {"system", "user", "assistant", "tool"}:
                raise ValueError(f"Kimi K3 cannot render role {role!r}")
            attributes = {"role": role}
            if message.get("name") and role != "tool":
                attributes["name"] = message["name"]
            if role == "tool":
                tool_index += 1
                name = message.get("tool") or message.get("name")
                if not name and tool_index <= len(calls):
                    name = calls[tool_index - 1]["function"]["name"]
                if not name:
                    raise ValueError(
                        "Kimi K3 tool messages need a name or preceding tool call"
                    )
                attributes.update(tool=name, index=str(tool_index))
            header = _open("message", **attributes)
            body, reasoning = _content(message)
            if role == "system" and message.get("tools"):
                header = _open("message", role="system", type="tool-declare")
                body = (
                    "## New Tools Available\nThe system dynamically extends the toolset via lazy-loading.\nYou have access to all existing and extended tools.\nHere are the specs for the extended tools.\n\n```json\n"
                    + _json(message["tools"], compact=True)
                    + "\n```"
                )
            if role == "assistant":
                calls, tool_index = message.get("tool_calls") or [], 0
                if self.thinking:
                    header += _open("think")
                    keep = not self.strip_thinking_from_history or index > last_user
                    body = (
                        (reasoning if keep and reasoning.strip() else "")
                        + _close("think")
                        + _open("response")
                        + body
                    )
                else:
                    header += _open("response")
                body += _close("response")
                rejected = rejected_call_text(message)
                if calls or rejected:
                    body += _tool_calls(calls, rejected)
            yield role, header, body + _close("message")

    def build_prompt_str(
        self,
        messages: list[Message],
        *,
        tools: list[ToolSpec] | None = None,
        tool_choice: str | None = None,
        response_format: str | dict | None = None,
        response_schema: dict | None = None,
    ) -> str:
        return (
            self._prefix(tools)
            + "".join(
                item[1] + item[2] + END_OF_MESSAGE for item in self._render(messages)
            )
            + _controls(tool_choice, response_format, response_schema)
            + self._generation_prompt()
        )

    def build_sample_prompt(
        self,
        messages: list[Message],
        *,
        tools: list[ToolSpec] | None = None,
        tool_choice: str | None = None,
        response_format: str | dict | None = None,
        response_schema: dict | None = None,
    ) -> SamplePrompt:
        return SamplePrompt(
            prompt=self.build_prompt_str(
                messages,
                tools=tools,
                tool_choice=tool_choice,
                response_format=response_format,
                response_schema=response_schema,
            )
        )

    def get_stop_strings(self) -> list[str]:
        return [END_OF_MESSAGE]

    def parse_response(
        self, text: str, *, tools: list[ToolSpec] | None = None
    ) -> ParsedResponse:
        """Accept the shared tools contract; XTML carries its own argument types."""
        stop_found = text.endswith(END_OF_MESSAGE)
        if stop_found:
            text = text[: -len(END_OF_MESSAGE)]
        text = text.removeprefix(self._generation_prompt())
        parts: list[ContentPart] = []
        if self.thinking:
            text = text.removeprefix(_open("think"))
            if not stop_found:
                text = _trim_incomplete_tag(text, _close("think"))
            reasoning, separator, text = text.partition(_close("think"))
            if reasoning:
                parts.append({"type": "thinking", "thinking": reasoning})
            if not separator:
                return ParsedResponse(
                    message={"role": "assistant", "content": parts},
                    stop_found=stop_found,
                )
        if not stop_found:
            text = _trim_incomplete_tag(text, _open("response"), _close("response"))
        text = text.removeprefix(_open("response"))
        response, separator, tail = text.partition(_close("response"))
        append_visible_text(parts, response)
        message: Message = {"role": "assistant", "content": parts}
        if separator:
            tail = tail.removesuffix(_close("message"))
            if not stop_found:
                tail = _trim_incomplete_tag(tail, _close("message"), _open("tools"))
            before, opened, tool_text = tail.partition(_open("tools"))
            # Not channel markup: visible text, as River Serve keeps it.
            append_visible_text(parts, before)
            if opened:
                if not stop_found:
                    tool_text = _trim_incomplete_tag(tool_text, _close("tools"))
                calls, errors, stray = _parse_tool_calls(
                    tool_text.removesuffix(_close("tools"))
                )
                for piece in stray:
                    append_visible_text(parts, piece)
                if calls:
                    message["tool_calls"] = calls
                if errors:
                    message["unparsed_tool_calls"] = errors
        return ParsedResponse(message=message, stop_found=stop_found)

    def build_training_example(
        self,
        messages: list[Message],
        *,
        train_on: TrainOnWhat = TrainOnWhat.LAST_ASSISTANT,
        train_on_eos: bool = True,
        max_length: int | None = None,
        tools: list[ToolSpec] | None = None,
        tool_choice: str | None = None,
        response_format: str | dict | None = None,
        response_schema: dict | None = None,
    ) -> TrainingExample:
        if train_on not in (TrainOnWhat.LAST_ASSISTANT, TrainOnWhat.ALL_ASSISTANT):
            raise ValueError(f"Unsupported train_on={train_on!r}")
        if max_length is not None and max_length < 1:
            raise ValueError("max_length must be positive")
        last = max(
            (
                index
                for index, message in enumerate(messages)
                if message["role"] == "assistant"
            ),
            default=-1,
        )
        rendered = list(self._render(messages, generated_turn=last))
        controls = _controls(tool_choice, response_format, response_schema)
        if (
            train_on == TrainOnWhat.ALL_ASSISTANT
            and sum(item[0] == "assistant" for item in rendered) > 1
            and (controls or (self.thinking and self.strip_thinking_from_history))
        ):
            raise ValueError(
                "Train one assistant turn per example when using K3 request controls or stripping history reasoning"
            )
        ids, weights = [], []

        def emit(text: str, weight: float):
            tokens = self.tokenizer.encode(text, add_special_tokens=False)
            ids.extend(tokens)
            weights.extend([weight] * len(tokens))

        emit(self._prefix(tools), 0.0)
        for index, (role, header, body) in enumerate(rendered):
            trainable = role == "assistant" and (
                train_on == TrainOnWhat.ALL_ASSISTANT or index == last
            )
            if index == last:
                emit(controls, 0.0)
            emit(header, 0.0)
            emit(body, float(trainable))
            emit(END_OF_MESSAGE, float(trainable and train_on_eos))
        return TrainingExample(input_ids=ids[:max_length], weights=weights[:max_length])
