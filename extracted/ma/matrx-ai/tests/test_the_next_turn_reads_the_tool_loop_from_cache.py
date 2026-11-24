"""FORCING GUARD — the next turn reads the previous tool loop from the prompt cache.

Since every send of a turn carries the page block (``test_a_tool_loop_keeps_its_page_values.py``),
a tool-loop send places it before her words and the rolling cache mark on the newest tool result:
the prefix that send caches HOLDS the block. The block used to be dropped when the turn ended, so
the next turn replayed her old message without it. Its prefix diverged at that message (index 0
for a one-turn history) and the whole previous tool loop, tool results included, was written to
the cache again at 1.25x instead of read at 0.1x — every agent with any turn-context policy that
made a tool call (wave-1 review item 1a, repro ``xturn.py``, 2026-11-02).

The fix keeps that turn's block on her turn when the turn ends
(``send_boundary.keep_turn_context_for_next_turn``, called by the executor's
``_strip_ephemeral_for_storage``) and replays it in the same place on every later send
(``send_boundary._replay_kept_turn_context``). This guard runs the real boundary, the real end-of-turn
step, a storage round trip and the real Anthropic translator, and asserts the cached prefix of the
turn's last send is a byte-identical prefix of the next turn's first send, whose first new message
is the reply and the new person turn.
"""

from __future__ import annotations

import json
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.config import (
    MessageList,
    TextContent,
    ToolCallContent,
    ToolResultContent,
    UnifiedConfig,
    UnifiedMessage,
)
from matrx_ai.config.send_boundary import order_for_wire
from matrx_ai.orchestrator.executor import _strip_ephemeral_for_storage
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.testing.profile_factory import make_profile

SYSTEM = "You are a careful assistant. " * 40
PAGE_V1 = "<page>doc v1: Website Corrections Brief</page>"
PAGE_V2 = "<page>doc v2: Website Corrections Brief, slide 2 shortened</page>"


def _turn_one() -> list[UnifiedMessage]:
    return [
        UnifiedMessage(role="user", content=[TextContent(text="HER WORDS turn this doc into a deck")]),
        UnifiedMessage(role="assistant", content=[ToolCallContent(id="c0", name="deck", arguments={"a": 1})]),
        UnifiedMessage(
            role="tool",
            content=[ToolResultContent(tool_use_id="c0", name="deck", content="BIG_TOOL_RESULT " * 200)],
        ),
    ]


def _config(messages: list[UnifiedMessage], block: str) -> UnifiedConfig:
    config = UnifiedConfig(model="claude-x", messages=MessageList(_messages=messages))
    config.system_instruction = SYSTEM
    config.messages.attach_turn_context(block, slot="context_manifest")
    return config


def _request(config: UnifiedConfig, iteration: int) -> dict[str, Any]:
    profile = make_profile(model_name="claude-x", wire_format="anthropic_chat")
    prep = order_for_wire(config, profile, iteration=iteration)
    return AnthropicTranslator().build_request(prep.wire_config or config, profile)


def _cached_prefix(request: dict[str, Any]) -> list[dict[str, Any]]:
    """The messages through the rolling cache mark, with the marks removed."""
    messages = request["messages"]
    end = max(
        (i for i, m in enumerate(messages) for b in m["content"] if isinstance(b, dict) and "cache_control" in b),
        default=-1,
    )
    return _unmarked(messages[: end + 1])


def _unmarked(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return json.loads(json.dumps(messages).replace(', "cache_control": {"type": "ephemeral"}', ""))


def _from_storage(message: UnifiedMessage, at: int) -> UnifiedMessage:
    """``message`` as the next turn reads it back from ``cx_message``."""
    stored = message.to_storage_dict()
    row = SimpleNamespace(
        id=f"row-{at}",
        role=stored["role"],
        content=stored["content"],
        user_content=stored.get("user_content"),
        created_at=None,
        status="active",
        is_visible_to_model=True,
        metadata=stored.get("metadata"),
        position=at,
        agent_id=None,
    )
    return UnifiedMessage.from_cx_message(row)


def _end_turn_one() -> tuple[dict[str, Any], list[UnifiedMessage]]:
    """Turn one's LAST send (newest message a tool result), then the executor's end-of-turn step."""
    config = _config(_turn_one(), PAGE_V1)
    last_send = _request(config, iteration=2)
    # The executor's real end-of-turn step (every exit of ``_finalize_and_persist`` runs it).
    _strip_ephemeral_for_storage(config)
    assert not config.messages.turn_context_blocks(), "the turn's context channel is cleared"
    return last_send, list(config.messages)


def _turn_two(history: list[UnifiedMessage]) -> dict[str, Any]:
    messages = [
        *history,
        UnifiedMessage(role="assistant", content=[TextContent(text="Done, deck built.")]),
        UnifiedMessage(role="user", content=[TextContent(text="SECOND WORDS now shorten slide 2")]),
    ]
    return _request(_config(messages, PAGE_V2), iteration=1)


@pytest.mark.parametrize("path", ["same_process", "reloaded_from_storage"])
def test_the_next_turn_reads_the_whole_previous_tool_loop_from_cache(path: str) -> None:
    last_send, history = _end_turn_one()
    if path == "reloaded_from_storage":
        history = [_from_storage(m, i) for i, m in enumerate(history)]
    cached = _cached_prefix(last_send)
    nxt = _unmarked(_turn_two(history)["messages"])

    first_diff = next((i for i, (a, b) in enumerate(zip(cached, nxt)) if a != b), min(len(cached), len(nxt)))
    assert first_diff == len(cached), (
        f"the next turn diverges from the cached prefix at message {first_diff} of {len(cached)}: the "
        "previous tool loop is re-written to the cache instead of read"
    )
    # The first new message is the reply, then the new person turn with ITS page values.
    assert nxt[len(cached)]["role"] == "assistant"
    last = nxt[-1]["content"]
    assert PAGE_V2 in json.dumps(last) and "SECOND WORDS" in last[-1]["text"]
    # The kept block of turn one rides before her old words, never after its tool result.
    first = nxt[0]["content"]
    assert PAGE_V1 in first[0]["text"] and "HER WORDS" in first[-1]["text"]


def test_the_kept_block_lives_on_her_turn_and_never_in_what_she_sees() -> None:
    from matrx_ai.config.typed_text_last import STORED_TURN_CONTEXT_KEY

    _last_send, history = _end_turn_one()
    her = history[0]
    assert PAGE_V1 in her.metadata[STORED_TURN_CONTEXT_KEY]
    assert [c.text for c in her.content] == ["HER WORDS turn this doc into a deck"]


def test_a_one_send_turn_keeps_nothing() -> None:
    """Its cache mark sat BEFORE the block, so the next turn already matches without it."""
    from matrx_ai.config.send_boundary import keep_turn_context_for_next_turn

    config = _config([UnifiedMessage(role="user", content=[TextContent(text="HER WORDS hello")])], PAGE_V1)
    request = _request(config, iteration=1)
    assert PAGE_V1 not in json.dumps(_cached_prefix(request))
    assert keep_turn_context_for_next_turn(config) is None


# --------------------------------------------------------------------------------------------- #
# With an attached file (REVIEW-C103 #2): the turn that homes a file runs a tool loop.            #
# --------------------------------------------------------------------------------------------- #

FILE_KEY = "resource_file_0b0b6c1e-3f0a-4a77-9d55-8a1f1b2c3d4e"
FILE_TEXT = "TRAILER LEDGER row 7 TR-40917 " * 400
FILE_ENTRY = [{"key": FILE_KEY, "file_id": FILE_KEY[14:], "file_name": "ledger.csv", "text": FILE_TEXT}]


def _file_request(config: UnifiedConfig, iteration: int) -> dict[str, Any]:
    """The boundary's real steps in order: wire clone, the attached-file step, the person-turn order."""
    from matrx_ai.config.attached_files import CONTEXT_FILE_BLOCKS_KEY
    from matrx_ai.config.send_boundary import (
        STAGE_LOOP,
        SendPrep,
        _build_wire,
        _place_attached_files,
    )

    config.metadata[CONTEXT_FILE_BLOCKS_KEY] = FILE_ENTRY
    profile = make_profile(model_name="claude-x", wire_format="anthropic_chat")
    prep = SendPrep(stage=STAGE_LOOP)
    _build_wire(prep, config)
    _place_attached_files(prep, config)
    prep = order_for_wire(config, profile, prep=prep, iteration=iteration)
    return AnthropicTranslator().build_request(prep.wire_config or config, profile)


@pytest.mark.parametrize("typed_mark", [True, False], ids=["typed_marked", "typed_unmarked"])
@pytest.mark.parametrize("path", ["same_process", "reloaded_from_storage"])
def test_a_tool_loop_that_brings_a_file_is_read_from_cache_next_turn(path: str, typed_mark: bool) -> None:
    """The first send led ``[file, block, words]``; the replay of the kept block must lead the same
    way, or block 0 differs and the whole loop plus the file is re-written (review probe_cache2)."""
    from matrx_ai.config.attached_files import FILE_BLOCK_HOMES_KEY
    from matrx_ai.config.template_substitution import mark_as_data

    words = TextContent(text="HER WORDS read the ledger")
    if typed_mark:
        mark_as_data(words)
    turn_one = _turn_one()
    turn_one[0] = UnifiedMessage(role="user", content=[words])
    turn_one[0].metadata[FILE_BLOCK_HOMES_KEY] = [FILE_KEY]
    config = _config(turn_one, PAGE_V1)
    last_send = _file_request(config, iteration=2)
    _strip_ephemeral_for_storage(config)
    history = list(config.messages)
    if path == "reloaded_from_storage":
        history = [_from_storage(m, i) for i, m in enumerate(history)]
    messages = [
        *history,
        UnifiedMessage(role="assistant", content=[TextContent(text="Done.")]),
        UnifiedMessage(role="user", content=[TextContent(text="SECOND WORDS which trailer?")]),
    ]
    nxt_request = _file_request(_config(messages, PAGE_V2), iteration=1)
    cached = _cached_prefix(last_send)
    nxt = _unmarked(nxt_request["messages"])
    first_diff = next((i for i, (a, b) in enumerate(zip(cached, nxt)) if a != b), min(len(cached), len(nxt)))
    assert first_diff == len(cached), (
        f"the next turn diverges from the cached prefix at message {first_diff}: "
        f"{json.dumps(cached[first_diff])[:300] if first_diff < len(cached) else ''} vs "
        f"{json.dumps(nxt[first_diff])[:300] if first_diff < len(nxt) else ''}"
    )
    assert json.dumps(nxt).count("TR-40917") == 400, "exactly one copy of the file per request"
    first = nxt[0]["content"]
    assert first[0]["text"].startswith("<attachment ") and PAGE_V1 in first[1]["text"]


@pytest.mark.parametrize("with_file", [False, True], ids=["no_file", "file"])
@pytest.mark.parametrize("path", ["same_process", "reloaded_from_storage"])
def test_a_templated_turn_with_typed_words_is_read_from_cache_next_turn(path: str, with_file: bool) -> None:
    """REVIEW-C110 minor 1: the agent's authored template with her typed words glued on as a data
    tail. The first send splits it ``[template] block [words]``; storage drops the typed marks, so
    the replay put the block before the whole turn and the next turn missed from message 0 (the
    loop, and the file, re-written at 1.25x). The kept layout makes the replay split it the same way."""
    from matrx_ai.config.attached_files import FILE_BLOCK_HOMES_KEY
    from matrx_ai.config.template_substitution import add_data_tail

    block = TextContent(text="TEMPLATE: analyse the ledger. HER WORDS which trailer?")
    add_data_tail(block, "HER WORDS which trailer?")
    turn_one = _turn_one()
    turn_one[0] = UnifiedMessage(role="user", content=[block])
    if with_file:
        turn_one[0].metadata[FILE_BLOCK_HOMES_KEY] = [FILE_KEY]
    send = _file_request if with_file else _request
    config = _config(turn_one, PAGE_V1)
    last_send = send(config, 2)
    _strip_ephemeral_for_storage(config)
    history = list(config.messages)
    if path == "reloaded_from_storage":
        history = [_from_storage(m, i) for i, m in enumerate(history)]
    messages = [
        *history,
        UnifiedMessage(role="assistant", content=[TextContent(text="Done.")]),
        UnifiedMessage(role="user", content=[TextContent(text="SECOND WORDS and the pallets?")]),
    ]
    cached = _cached_prefix(last_send)
    nxt = _unmarked(send(_config(messages, PAGE_V2), 1)["messages"])
    first_diff = next((i for i, (a, b) in enumerate(zip(cached, nxt)) if a != b), min(len(cached), len(nxt)))
    assert first_diff == len(cached), (
        f"the next turn diverges from the cached prefix at message {first_diff}: "
        f"{json.dumps(cached[first_diff])[:300] if first_diff < len(cached) else ''} vs "
        f"{json.dumps(nxt[first_diff])[:300] if first_diff < len(nxt) else ''}"
    )


@pytest.mark.parametrize("shape", ["typed_block", "template_with_typed_tail"])
def test_a_group_chat_turn_replays_her_layout_after_the_speaker_name(shape: str) -> None:
    """REVIEW-C110b I1: in a chat several people write in, ``_name_speakers`` puts a host-written
    ``"Alice:"`` block in front of her turn on the wire. The typed layout is recorded on the STORED
    message (no speaker block) and applied on the WIRE turn (with it): counted over all blocks, every
    index was off by one and the replay sent ``[HER WORDS] [BLOCK] [Alice:]`` — a cache miss, and her
    words lost their speaker. Counted over her own blocks, the replay is the first send."""
    from matrx_ai.config.message_config import HOST_AUTHORED_BY
    from matrx_ai.config.speakers import SPEAKER_NAME_REASON
    from matrx_ai.config.template_substitution import add_data_tail, mark_as_data
    from matrx_ai.config.typed_text_last import STORED_TYPED_LAYOUT_KEY, place_before_typed_text, typed_layout

    text = "HER WORDS which trailer?" if shape == "typed_block" else "TEMPLATE: analyse. HER WORDS which trailer?"

    def speaker() -> TextContent:
        return TextContent(text="Alice:", metadata={"authored_by": HOST_AUTHORED_BY, "authored_reason": SPEAKER_NAME_REASON})

    marked = TextContent(text=text)
    if shape == "typed_block":
        mark_as_data(marked)
    else:
        add_data_tail(marked, "HER WORDS which trailer?")
    stored = UnifiedMessage(role="user", content=[marked])
    layout = typed_layout(stored.content)  # what keep_turn_context_for_next_turn records

    def texts(messages: list[Any]) -> list[list[str]]:
        return [[getattr(c, "text", "") for c in m.content] for m in messages]

    first, _ = place_before_typed_text([UnifiedMessage(role="user", content=[speaker(), marked])], PAGE_V1)
    reloaded = UnifiedMessage(role="user", content=[speaker(), TextContent(text=text)])
    reloaded.metadata = {STORED_TYPED_LAYOUT_KEY: layout}
    replay, _ = place_before_typed_text([reloaded], PAGE_V1, replayed=True)
    assert texts(replay) == texts(first), (texts(first), texts(replay))
    assert texts(first)[0][0] == "Alice:" and texts(first)[-1][-1].endswith("which trailer?")
