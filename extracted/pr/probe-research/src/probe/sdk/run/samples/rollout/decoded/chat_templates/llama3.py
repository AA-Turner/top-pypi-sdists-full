"""Llama 3: `<|start_header_id|>role<|end_header_id|>\\n\\n...<|eot_id|>` blocks; tool results in an `ipython` block;
a tool call as a JSON object (`{"name", "parameters"}`), optionally after `<|python_tag|>`."""

from __future__ import annotations

from ..chat_template import ChatTemplate, to_hermes_call

BEGIN, END_OF_TEXT = "<|begin_of_text|>", "<|end_of_text|>"
HEADER_OPEN, HEADER_CLOSE = "<|start_header_id|>", "<|end_header_id|>"
END_OF_TURN, END_OF_MESSAGE, PYTHON_TAG = "<|eot_id|>", "<|eom_id|>", "<|python_tag|>"
#: Llama's tool-result role.
TOOL_ROLES = {"ipython": "tool", "tool": "tool"}


class Llama3(ChatTemplate):
    name = "llama3"
    control_tokens = (BEGIN, END_OF_TEXT, HEADER_OPEN, HEADER_CLOSE, END_OF_TURN, END_OF_MESSAGE, PYTHON_TAG)
    role_markers = (HEADER_OPEN, END_OF_TURN, END_OF_MESSAGE)

    def read_messages(self, text: str, *, role: str) -> list[dict]:
        pieces = text.replace(BEGIN, "").split(HEADER_OPEN)
        messages = [self._read_block(role, pieces[0])]
        for piece in pieces[1:]:
            name, _, body = piece.partition(HEADER_CLOSE)
            messages.append(self._read_block(name.strip() or "user", body))
        return messages

    def _read_block(self, role: str, body: str) -> dict:
        for end in (END_OF_TURN, END_OF_MESSAGE):
            body = body.split(end, 1)[0]
        body = self.strip_control_tokens(body).strip()
        role = TOOL_ROLES.get(role, role)
        if role == "assistant":
            call = to_hermes_call(body) if body.startswith("{") else None
            if call is not None:
                return {"role": "assistant", "content": "", "tool_calls": [call]}
        return {"role": role, "content": body}
