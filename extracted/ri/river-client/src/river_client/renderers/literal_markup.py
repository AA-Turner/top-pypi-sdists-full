"""Tokenize message text so the control markup it quotes stays text.

A chat template writes its own structure with the tokenizer's added tokens
(``<|user|>``, ``<tool_call>``, ``</think>`` ...). Encoding the rendered prompt
as one string also turns any copy of that markup inside a message into the
control token, so a tool result or file that merely mentions ``<tool_call>``
reaches the model as a real call marker. Hugging Face's
``split_special_tokens`` does not help: it covers only special tokens, and
GLM's call and reasoning markup are non-special added tokens.

Quoted text is every non-assistant message's content, the argument values of
assistant tool calls, and the tool definitions. This module renders the
template once more with each marker in quoted text swapped for a sentinel,
then swaps the markers back and remembers where they are. The prompt is
encoded as usual except that an added token inside one of those spans is not
matched: the text around it is encoded as if the tokenizer had no added
tokens. A prompt without such markup encodes exactly as before.

Assistant content and reasoning are left alone: the template reads inline
reasoning from assistant content, and a rejected call block written back into
it is markup the model produced.

River's server applies the same rule to GLM chat requests
(``rust/river-serve/python/src/tokenizer.rs``), so both produce the same ids.
"""

from __future__ import annotations

import bisect
import json
import re
from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass, replace
from typing import Any

# Sentinel delimiters come from Unicode plane 15's private use area, which
# real text almost never uses; one absent from the prompt is chosen per render.
_SENTINEL_FIRST = 0xF0000
_SENTINEL_LAST = 0xFFFFD


@dataclass(frozen=True)
class RenderedPrompt:
    """A rendered prompt and the character ranges of quoted markup in it."""

    text: str
    literal_spans: tuple[tuple[int, int], ...] = ()

    def removeprefix(self, prefix: str) -> RenderedPrompt:
        if not self.text.startswith(prefix):
            return self
        shift = len(prefix)
        return RenderedPrompt(
            self.text[shift:],
            tuple(
                (start - shift, end - shift)
                for start, end in self.literal_spans
                if start >= shift
            ),
        )

    def removesuffix(self, suffix: str) -> RenderedPrompt:
        if not suffix or not self.text.endswith(suffix):
            return self
        end = len(self.text) - len(suffix)
        return RenderedPrompt(
            self.text[:end],
            tuple(span for span in self.literal_spans if span[1] <= end),
        )

    def append(self, text: str) -> RenderedPrompt:
        return replace(self, text=self.text + text)


class LiteralMarkup:
    """The added-token markers of a fast tokenizer and the matching encoder."""

    def __init__(self, tokenizer: Any) -> None:
        from tokenizers import Tokenizer

        backend = tokenizer.backend_tokenizer
        self._tokenizer = tokenizer
        added = backend.get_added_tokens_decoder()
        self._added_ids = frozenset(added)
        contents: set[str] = {str(token.content) for token in added.values()}
        self.markers = tuple(sorted(contents, key=str.__len__, reverse=True))
        self._marker_index = {marker: i for i, marker in enumerate(self.markers)}
        # Python's alternation takes the first alternative that matches, so
        # longest-first ordering finds the longest marker at each position.
        self._pattern = (
            re.compile("|".join(re.escape(marker) for marker in self.markers))
            if self.markers
            else None
        )
        # Private copies without truncation or padding, which a caller may
        # have enabled on the shared backend: the offsets must cover the
        # whole prompt. ``_plain`` also drops the added vocabulary.
        config = json.loads(backend.to_str())
        config["truncation"] = None
        config["padding"] = None
        self._full = Tokenizer.from_str(json.dumps(config))
        config["added_tokens"] = []
        self._plain = Tokenizer.from_str(json.dumps(config))

    def render(
        self,
        render: Callable[[list[dict[str, Any]], Any], str],
        messages: list[dict[str, Any]],
        tools: Any = None,
    ) -> RenderedPrompt:
        """Render ``messages`` and locate the markup copied from their text.

        ``render(messages, tools)`` must be deterministic. If the template
        transforms quoted text in a way that loses a sentinel, the prompt is
        returned without spans and encodes as before.
        """
        original_messages = messages
        # Templates write a message's text parts back to back, so a marker
        # can span two of them; look for markers in the joined text.
        messages = [_join_text_parts(m) for m in messages]
        if not self._quotes_markup([_quoted(m) for m in messages] + [tools]):
            return RenderedPrompt(render(original_messages, tools))
        original = render(original_messages, tools)
        delimiter = _sentinel_delimiter(original)
        if delimiter is None:
            return RenderedPrompt(original)

        def substitute(text: str) -> str:
            assert self._pattern is not None
            return self._pattern.sub(
                lambda match: (
                    f"{delimiter}{self._marker_index[match.group()]}{delimiter}"
                ),
                text,
            )

        swapped = [_swap_quoted(m, substitute) for m in messages]
        rendered = render(swapped, _map_strings(tools, substitute))
        restored, spans = self._restore(rendered, delimiter)
        if restored != original:
            return RenderedPrompt(original)
        return RenderedPrompt(original, spans)

    def encode(self, prompt: RenderedPrompt) -> list[int]:
        """Encode ``prompt``, leaving added tokens in its literal spans as text."""
        if not prompt.literal_spans:
            return list(self._tokenizer.encode(prompt.text, add_special_tokens=False))
        encoding = self._full.encode(prompt.text, add_special_tokens=False)
        starts = [start for start, _ in prompt.literal_spans]
        ends = [end for _, end in prompt.literal_spans]

        def quoted(start: int, end: int) -> bool:
            index = bisect.bisect_right(starts, end - 1) - 1
            return index >= 0 and ends[index] > start

        out: list[int] = []
        pending: list[int] = []
        segment_start = 0
        rewrite = False

        def flush(end: int) -> None:
            nonlocal pending, rewrite
            if rewrite:
                text = prompt.text[segment_start:end]
                out.extend(self._plain.encode(text, add_special_tokens=False).ids)
            else:
                out.extend(pending)
            pending, rewrite = [], False

        for token_id, (start, end) in zip(encoding.ids, encoding.offsets, strict=True):
            if token_id not in self._added_ids:
                pending.append(token_id)
            elif quoted(start, end):
                rewrite = True
            else:
                flush(start)
                out.append(token_id)
                segment_start = end
        flush(len(prompt.text))
        return out

    def _quotes_markup(self, value: Any) -> bool:
        pattern = self._pattern
        return pattern is not None and any(
            pattern.search(text) for text in _strings(value)
        )

    def _restore(
        self, text: str, delimiter: str
    ) -> tuple[str, tuple[tuple[int, int], ...]]:
        pieces: list[str] = []
        spans: list[tuple[int, int]] = []
        length = 0
        position = 0
        sentinel = re.compile(f"{delimiter}([0-9]+){delimiter}")
        for match in sentinel.finditer(text):
            plain = text[position : match.start()]
            pieces.append(plain)
            length += len(plain)
            marker = self.markers[int(match.group(1))]
            pieces.append(marker)
            spans.append((length, length + len(marker)))
            length += len(marker)
            position = match.end()
        pieces.append(text[position:])
        return "".join(pieces), tuple(spans)


def literal_markup(tokenizer: Any) -> LiteralMarkup | None:
    """The literal-markup encoder for ``tokenizer``, or None without a fast backend."""
    if getattr(tokenizer, "backend_tokenizer", None) is None:
        return None
    return LiteralMarkup(tokenizer)


def _quoted(message: dict[str, Any]) -> Any:
    """The fields of ``message`` that hold quoted text rather than markup."""
    if message.get("role") != "assistant":
        return message.get("content")
    arguments = [
        call.get("function", {}).get("arguments")
        for call in message.get("tool_calls") or []
    ]
    return [value for value in arguments if isinstance(value, dict)]


def _swap_quoted(message: dict[str, Any], fn: Callable[[str], str]) -> dict[str, Any]:
    if message.get("role") != "assistant":
        if "content" not in message:
            return message
        return {**message, "content": _map_strings(message["content"], fn)}
    if not message.get("tool_calls"):
        return message
    calls = []
    for call in message["tool_calls"]:
        function = call.get("function")
        if isinstance(function, dict) and "arguments" in function:
            arguments = function["arguments"]
            # A JSON-string form is parsed by the template's caller; only a
            # mapping's values are inlined as text.
            if isinstance(arguments, dict):
                function = {**function, "arguments": _map_strings(arguments, fn)}
            call = {**call, "function": function}
        calls.append(call)
    return {**message, "tool_calls": calls}


def _map_strings(value: Any, fn: Callable[[str], str]) -> Any:
    if isinstance(value, str):
        return fn(value)
    if isinstance(value, dict):
        return {
            _map_strings(key, fn): _map_strings(item, fn) for key, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [_map_strings(item, fn) for item in value]
    return value


def _join_text_parts(message: dict[str, Any]) -> dict[str, Any]:
    """``message`` with adjacent text parts of quoted content joined."""
    content = message.get("content")
    if message.get("role") == "assistant" or not isinstance(content, list):
        return message
    joined: list[Any] = []
    for part in content:
        if _text_part(part) and joined and _text_part(joined[-1]):
            joined[-1] = {"type": "text", "text": joined[-1]["text"] + part["text"]}
        else:
            joined.append(part)
    return {**message, "content": joined}


def _text_part(part: Any) -> bool:
    return (
        isinstance(part, dict)
        and part.get("type") == "text"
        and isinstance(part.get("text"), str)
    )


def _strings(value: Any) -> Iterator[str]:
    """Every string in ``value``, keys included: serialized JSON writes them."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from _strings(key)
            yield from _strings(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _strings(item)


def _sentinel_delimiter(text: str) -> str | None:
    for code in range(_SENTINEL_FIRST, _SENTINEL_LAST + 1):
        delimiter = chr(code)
        if delimiter not in text:
            return delimiter
    return None


__all__: Sequence[str] = ["LiteralMarkup", "RenderedPrompt", "literal_markup"]
