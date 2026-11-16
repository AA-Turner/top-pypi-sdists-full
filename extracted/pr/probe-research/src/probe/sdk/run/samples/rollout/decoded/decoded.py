"""Turns rebuilt from token ids and a loss mask (`turns_source=decoded`), for verl, SkyRL and Miles when no messages
were kept: split into model (mask 1) and other (mask 0) runs, decode each with special tokens kept, and let the chat
template's reader turn the text into messages (roles, tool calls, tool results, reasoning). Unknown template: each run
decoded with special tokens skipped, no tool parsing."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import Any

from ..messages import build_turns, to_message
from .chat_template import ChatTemplate
from .chat_templates import ChatML, Llama3

#: ``decode(ids, keep_special)``: token ids as text, the template's control tokens kept when ``keep_special``.
Decode = Callable[[list[int], bool], str]
#: The readers, tried in order on the decoded text (`get_chat_template`).
CHAT_TEMPLATES: tuple[ChatTemplate, ...] = (ChatML(), Llama3())


def make_decode(tokenizer: Any) -> Decode:
    """A Hugging Face tokenizer's `decode` as a `Decode`."""
    return lambda ids, keep_special: str(tokenizer.decode(list(ids), skip_special_tokens=not keep_special))


def get_chat_template(text: str) -> ChatTemplate | None:
    """The reader whose markers ``text`` holds; None for a template Probe has no reader for."""
    return next((template for template in CHAT_TEMPLATES if template.is_written_in(text)), None)


def build_decoded_turns(token_ids: Sequence[int], loss_mask: Sequence[Any] | None, decode: Decode | None, *,
                        prompt_ids: Sequence[int] = (), prompt_messages: Iterable[Mapping[str, Any]] = (),
                        other_role: str = "user") -> list[dict]:
    """The response's turns: ``prompt_messages`` (the dataset's chat messages) or ``prompt_ids`` (decoded like the
    response's other tokens) first, then each run of ``token_ids`` by ``loss_mask`` (None: all the model's), one turn
    per model reply (`messages.build_turns`). Tool calls with no id get `probe-<turn>-<i>` and their results link by
    order. A user message after the first model run is the environment's; ``other_role`` names an other run's text
    before any role marker (`tool` for a tool loop's replies)."""
    if decode is None or not token_ids:
        return []
    mask = list(loss_mask) if loss_mask is not None and len(loss_mask) == len(token_ids) else [1] * len(token_ids)
    runs = split_runs([*prompt_ids, *token_ids], [0] * len(prompt_ids) + mask)
    texts = [decode(ids, True) for _, ids in runs]
    template = get_chat_template("".join(texts))
    # Only messages `build_turns` keeps (a role), so each mark below lines up with its message.
    messages: list[dict] = [dict(message) for message in prompt_messages if to_message(message) is not None]
    marks: list[tuple[bool, bool]] = [(False, False)] * len(messages)
    has_seen_model = False
    for (is_model, ids), text in zip(runs, texts):
        role = "assistant" if is_model else other_role
        if template is None:
            found = [{"role": role, "content": decode(ids, False)}]
        else:
            found = template.read_messages(text, role=role)
            if is_model and not any(message["role"] == "assistant" for message in found):
                found.append({"role": "assistant", "content": ""})
            elif not is_model:
                found = [message for message in found if not _is_empty(message)]
        messages += found
        marks += [(is_model and message["role"] == "assistant", has_seen_model and message["role"] == "user")
                  for message in found]
        has_seen_model = has_seen_model or is_model
    turns = build_turns(messages, should_number_ids=True)
    for message, (is_trainable, is_observation) in zip((m for turn in turns for m in turn["messages"]), marks):
        if not is_trainable:
            message.pop("is_trainable", None)  # an assistant message in the prompt is not in the loss
        if is_observation:
            message["source"] = "environment"
    return turns


def split_runs(ids: Sequence[int], mask: Sequence[Any]) -> list[tuple[bool, list[int]]]:
    """The runs of equal mask bits: (is the model's, token ids), in order."""
    runs: list[tuple[bool, list[int]]] = []
    for token, bit in zip(ids, mask):
        if runs and runs[-1][0] == bool(bit):
            runs[-1][1].append(int(token))
        else:
            runs.append((bool(bit), [int(token)]))
    return runs


def _is_empty(message: Mapping[str, Any]) -> bool:
    return not str(message.get("content") or "").strip() and not message.get("tool_calls") and not message.get(
        "reasoning_content")
