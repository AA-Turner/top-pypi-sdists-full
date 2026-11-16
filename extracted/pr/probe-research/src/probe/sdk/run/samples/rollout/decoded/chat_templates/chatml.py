"""ChatML (Qwen 2.5 / 3 and most open models): `<|im_start|>role\\n...<|im_end|>` blocks, Hermes tool calls
(`<tool_call>{json}</tool_call>`), tool results inside a user block (`<tool_response>...</tool_response>`) or a `tool`
block, and reasoning in `<think>...</think>`."""

from __future__ import annotations

import re

from ..chat_template import ChatTemplate, to_hermes_call

START, END, END_OF_TEXT = "<|im_start|>", "<|im_end|>", "<|endoftext|>"
CALL_OPEN, CALL_CLOSE = "<tool_call>", "</tool_call>"
RESPONSE_OPEN, RESPONSE_CLOSE = "<tool_response>", "</tool_response>"
THINK_OPEN, THINK_CLOSE = "<think>", "</think>"
_CALLS = re.compile(re.escape(CALL_OPEN) + r"(.*?)" + re.escape(CALL_CLOSE), re.DOTALL)
_RESPONSES = re.compile(re.escape(RESPONSE_OPEN) + r"(.*?)" + re.escape(RESPONSE_CLOSE), re.DOTALL)


class ChatML(ChatTemplate):
    name = "chatml"
    control_tokens = (START, END, END_OF_TEXT, CALL_OPEN, CALL_CLOSE, RESPONSE_OPEN, RESPONSE_CLOSE, THINK_OPEN,
                      THINK_CLOSE)
    role_markers = (START, END)

    def read_messages(self, text: str, *, role: str) -> list[dict]:
        pieces = text.split(START)
        messages = self._read_block(role, pieces[0])
        for piece in pieces[1:]:
            name, _, body = piece.partition("\n")
            messages += self._read_block(name.strip() or "user", body)
        return messages

    def _read_block(self, role: str, body: str) -> list[dict]:
        body = body.split(END, 1)[0].replace(END_OF_TEXT, "")
        if role == "assistant":
            return [self._read_reply(body)]
        if role == "tool":
            return [{"role": "tool", "content": self._clean(_unwrap_response(body))}]
        if RESPONSE_OPEN in body:  # Qwen sends tool results as a user block of `<tool_response>`s
            results = [{"role": "tool", "content": self._clean(_strip_newline(found))}
                       for found in _RESPONSES.findall(body)]
            rest = self._clean(_RESPONSES.sub("", body)).strip()
            return results + ([{"role": role, "content": rest}] if rest else [])
        return [{"role": role, "content": self._clean(body).strip("\n")}]

    def _read_reply(self, body: str) -> dict:
        reasoning = None
        if THINK_CLOSE in body:
            before, _, body = body.partition(THINK_CLOSE)
            reasoning = before.split(THINK_OPEN, 1)[-1]
        elif body.lstrip().startswith(THINK_OPEN):  # cut off mid-thought
            reasoning, body = body.lstrip()[len(THINK_OPEN):], ""
        calls = []
        kept = []
        for found in _CALLS.findall(body):
            call = to_hermes_call(found.strip())
            if call is None:
                kept.append(found.strip())  # not a call the template's parser reads: kept as the model's text
            else:
                calls.append(call)
        content = "\n".join([_CALLS.sub("", body).strip(), *kept]).strip()
        message: dict = {"role": "assistant", "content": self._clean(content).strip()}
        if reasoning is not None and reasoning.strip():
            message["reasoning_content"] = self._clean(reasoning).strip()
        if calls:
            message["tool_calls"] = calls
        return message

    def _clean(self, text: str) -> str:
        return self.strip_control_tokens(text)


def _unwrap_response(body: str) -> str:
    found = _RESPONSES.findall(body)
    return "\n".join(_strip_newline(part) for part in found) if found else body.strip("\n")


def _strip_newline(text: str) -> str:
    """The template's own newline on each side of a tool result, and only that."""
    text = text[1:] if text.startswith("\n") else text
    return text[:-1] if text.endswith("\n") else text
