"""Turns rebuilt from token ids and a loss mask (`turns_source=decoded`), for verl, SkyRL and Miles when no messages
were kept: split into model (mask 1) and other (mask 0) runs, decode each with special tokens kept, and let the chat
template's reader turn the text into messages (roles, tool calls, tool results, reasoning). Unknown template: each run
decoded with special tokens skipped, no tool parsing. A reply's turn counts its own tokens (`Turn.usage`), each tool
result or observation its own (`Message.result_tokens`), and `add_reply_usage` gives replies' counts to turns kept as
sent from the same token stream."""

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
    before any role marker (`tool` for a tool loop's replies). A turn holding one model run's reply carries `usage`:
    that run's tokens, and with ``prompt_ids`` every token before it (one stream, so what the model read). A tool
    result or observation carries `result_tokens` where its span is exact (`_count_messages`)."""
    if decode is None or not token_ids:
        return []
    mask = list(loss_mask) if loss_mask is not None and len(loss_mask) == len(token_ids) else [1] * len(token_ids)
    runs = split_runs([*prompt_ids, *token_ids], [0] * len(prompt_ids) + mask)
    texts = [decode(ids, True) for _, ids in runs]
    template = get_chat_template("".join(texts))
    # Only messages `build_turns` keeps (a role), so each mark below lines up with its message.
    messages: list[dict] = [dict(message) for message in prompt_messages if to_message(message) is not None]
    marks: list[tuple[bool, bool]] = [(False, False)] * len(messages)
    #: Per message, the model run it came from (its index in `runs`), None for every other.
    origins: list[int | None] = [None] * len(messages)
    #: Per message, its own tokens when it follows a model run and its span is exact, else None.
    counts: list[int | None] = [None] * len(messages)
    names: dict[int, str] = {}  # token id -> its text alone, for `_count_messages`
    has_seen_model = False
    for place, ((is_model, ids), text) in enumerate(zip(runs, texts)):
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
        origins += [place if is_model else None] * len(found)
        if has_seen_model and not is_model:
            counts += _count_messages(template, ids, found, decode, role=role, names=names)
        else:
            counts += [None] * len(found)
        marks += [(is_model and message["role"] == "assistant", has_seen_model and message["role"] == "user")
                  for message in found]
        has_seen_model = has_seen_model or is_model
    turns = build_turns(messages, should_number_ids=True)
    for message, (is_trainable, is_observation), count in zip((m for turn in turns for m in turn["messages"]), marks,
                                                               counts):
        if not is_trainable:
            message.pop("is_trainable", None)  # an assistant message in the prompt is not in the loss
        if is_observation:
            message["source"] = "environment"
        if count is not None and (is_observation or message["role"] == "tool"):
            message["result_tokens"] = count
    _add_usage(turns, runs, origins, has_prompt=bool(prompt_ids))
    return turns


def _count_messages(template: ChatTemplate | None, ids: list[int], found: list[dict], decode: Decode, *, role: str,
                    names: dict[int, str]) -> list[int | None]:
    """Each of ``found`` (one non-model run's messages) its own tokens: the run cut before every token that is one of
    the template's `message_starts` alone, each piece read again; a piece read as one message is that message's
    span, its markers included. A piece that opens on a marker but reads as nothing (a block's role header before
    its first `<tool_response>`) joins the next piece, so a lone result counts its whole block in any wrapper; one
    that reads as nothing otherwise (the last reply's newline, the next reply's header) is no message's. All None
    with no template (nothing to cut at: the run may hold the next reply's header) or when the pieces read otherwise
    than the whole run: never a guess. ``names`` caches each token id's text across runs."""
    if template is None:
        return [None] * len(found)
    starts = []
    for place, token in enumerate(ids):
        if token not in names:
            names[token] = decode([token], True)
        if place and names[token] in template.message_starts:
            starts.append(place)
    counts: list[int | None] = []
    read: list[dict] = []
    carried = 0  # a header piece's tokens, for the message after it
    for begin, end in zip([0, *starts], [*starts, len(ids)]):
        pieces = [m for m in template.read_messages(decode(ids[begin:end], True), role=role) if not _is_empty(m)]
        read += pieces
        counts += [carried + end - begin if len(pieces) == 1 else None] * len(pieces)
        carried = carried + end - begin if not pieces and names[ids[begin]] in template.message_starts else 0
    return counts if read == found else [None] * len(found)


def _add_usage(turns: list[dict], runs: list[tuple[bool, list[int]]], origins: list[int | None], *,
               has_prompt: bool) -> None:
    """Each turn whose messages came from exactly one model run, that run in no other turn: its tokens (exact, not a
    split). The prompt count only when the prompt's ids were given (dataset messages have no count)."""
    places = iter(origins)
    by_turn = [{place for _ in turn["messages"] if (place := next(places, None)) is not None} for turn in turns]
    for turn, found in zip(turns, by_turn):
        if len(found) != 1:
            continue
        (place,) = found
        if sum(place in other for other in by_turn) != 1:
            continue
        usage = {"response_tokens": len(runs[place][1])}
        if has_prompt:
            usage["prompt_tokens"] = sum(len(ids) for _, ids in runs[:place])
        turn["usage"] = usage


def add_reply_usage(turns: list[dict], response_ids: Sequence[int], loss_mask: Sequence[Any] | None, *,
                    prompt_length: int | None = None) -> None:
    """Turns built from messages as sent (`build_turns`: one per model reply) given each reply's tokens from the
    response's token stream: the k-th model run (loss mask 1; None: the whole response) is the k-th reply, its turn's
    `usage` that run's length and, with ``prompt_length``, every token before it (one stream, so what that call
    read). Only when the runs and the replies are as many (a few-shot reply in the prompt, a reply masked in parts):
    otherwise no reply's run is known, and none is guessed."""
    mask = [1] * len(response_ids) if loss_mask is None else list(loss_mask)
    if not response_ids or len(mask) != len(response_ids):
        return
    replies = [turn for turn in turns if turn.get("messages") and turn["messages"][-1].get("role") == "assistant"]
    places: list[tuple[int, int]] = []  # (tokens before the run, its length) per model run
    offset = 0
    for is_model, ids in split_runs(response_ids, mask):
        if is_model:
            places.append((offset, len(ids)))
        offset += len(ids)
    if not replies or len(places) != len(replies):
        return
    for turn, (before, count) in zip(replies, places):
        usage = {"response_tokens": count}
        if prompt_length is not None:
            usage["prompt_tokens"] = prompt_length + before
        turn["usage"] = usage


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
