"""The tool-argument stream hook: a registered tool hears each completed array element and
top-level scalar while Anthropic / OpenAI stream the call's arguments, and a close."""

from __future__ import annotations

import json
import random
from types import SimpleNamespace as NS
from typing import Any

import pytest

from matrx_ai.providers.anthropic.anthropic_api import AnthropicChat
from matrx_ai.providers.openai.openai_api import OpenAIChat
from matrx_ai.tools.partial_args import (
    PartialArgsSpec,
    PartialToolCall,
    _Scanner,
    register_partial_args,
    unregister_partial_args,
)

ARGS = {
    "action": "patch",
    "nodes_upsert": [{"id": "a", "data": {"x": [1, {"y": "}],\"q"}]}}, {"step": 3, "data": {}}],
    "meta": {"workflow_id": "decoy", "nodes_upsert": [9]},
    "nodes_remove": [7, 'b"c'],
    "workflow_id": "wf-1",
    "numbering": "n-abc",
}
SPEC = PartialArgsSpec(arrays=("nodes_upsert", "nodes_remove"), scalars=("workflow_id", "numbering"))


class _Emitter:
    async def send_chunk(self, text: str) -> None: ...
    async def send_reasoning_state(self, state: str) -> None: ...


class _Listener:
    def __init__(self, call: PartialToolCall) -> None:
        self.call = call
        self.heard: list[tuple[str, Any]] = []
        self.closed: list[bool] = []

    async def element(self, path: str, value: Any) -> None:
        self.heard.append((path, value))

    async def scalar(self, key: str, value: Any) -> None:
        self.heard.append((key, value))

    async def close(self, *, completed: bool) -> None:
        self.closed.append(completed)


@pytest.fixture
def listeners():
    made: list[_Listener] = []

    def factory(call: PartialToolCall) -> _Listener:
        made.append(_Listener(call))
        return made[-1]

    register_partial_args("workflow_author", SPEC, factory)
    yield made
    unregister_partial_args("workflow_author")


EXPECTED = [
    ("nodes_upsert[*]", ARGS["nodes_upsert"][0]),
    ("nodes_upsert[*]", ARGS["nodes_upsert"][1]),
    ("nodes_remove[*]", 7),
    ("nodes_remove[*]", 'b"c'),
    ("workflow_id", "wf-1"),
    ("numbering", "n-abc"),
]


def _pieces(text: str) -> list[str]:
    rnd = random.Random(7)
    out, i = [], 0
    while i < len(text):
        k = rnd.randint(1, 9)
        out.append(text[i : i + k])
        i += k
    return out


def test_scanner_reports_each_element_once_however_the_text_is_cut():
    for indent in (None, 2):
        text = json.dumps(ARGS, indent=indent)
        for seed in range(50):
            rnd = random.Random(seed)
            scanner, heard, i = _Scanner(SPEC), [], 0
            while i < len(text):
                k = rnd.randint(1, 7)
                heard += [(n, v) for _, n, v in scanner.feed(text[i : i + k])]
                i += k
            assert heard == EXPECTED


@pytest.mark.asyncio
async def test_anthropic_input_json_deltas_reach_the_listener(listeners):
    api, em = AnthropicChat(), _Emitter()
    await api._handle_event(
        NS(type="content_block_start", index=1, content_block=NS(type="tool_use", name="workflow_author", id="toolu_1")), em
    )
    for piece in _pieces(json.dumps(ARGS)):
        await api._handle_event(
            NS(type="content_block_delta", index=1, delta=NS(type="input_json_delta", partial_json=piece)), em
        )
    await api._handle_event(NS(type="content_block_stop", index=1), em)
    [heard] = listeners
    assert heard.call.call_id == "toolu_1"
    assert heard.heard == EXPECTED
    assert heard.closed == [True]


@pytest.mark.asyncio
async def test_anthropic_stream_that_stops_mid_call_closes_not_completed(listeners):
    api, em = AnthropicChat(), _Emitter()
    await api._handle_event(
        NS(type="content_block_start", index=0, content_block=NS(type="tool_use", name="workflow_author", id="t")), em
    )
    await api._handle_event(
        NS(type="content_block_delta", index=0, delta=NS(type="input_json_delta", partial_json='{"nodes_upsert": [{"id": "a"}, {"i')),
        em,
    )
    await api._handle_event(NS(type="message_stop"), em)
    assert listeners[0].heard == [("nodes_upsert[*]", {"id": "a"})]
    assert listeners[0].closed == [False]


@pytest.mark.asyncio
async def test_an_unregistered_tool_costs_nothing(listeners):
    api, em = AnthropicChat(), _Emitter()
    await api._handle_event(
        NS(type="content_block_start", index=0, content_block=NS(type="tool_use", name="other_tool", id="t")), em
    )
    await api._handle_event(
        NS(type="content_block_delta", index=0, delta=NS(type="input_json_delta", partial_json='{"nodes_upsert": [1]}')), em
    )
    assert listeners == []


@pytest.mark.asyncio
async def test_openai_function_call_argument_deltas_reach_the_listener(listeners):
    api, em = OpenAIChat(), _Emitter()
    await api._handle_event(
        NS(type="response.output_item.added", output_index=2, item=NS(type="function_call", name="workflow_author", call_id="call_9")),
        em,
    )
    for piece in _pieces(json.dumps(ARGS)):
        await api._handle_event(NS(type="response.function_call_arguments.delta", output_index=2, delta=piece), em)
    await api._handle_event(NS(type="response.function_call_arguments.done", output_index=2), em)
    [heard] = listeners
    assert heard.call.call_id == "call_9"
    assert heard.heard == EXPECTED
    assert heard.closed == [True]


@pytest.mark.asyncio
async def test_a_failing_listener_never_breaks_the_stream():
    class _Boom(_Listener):
        async def element(self, path: str, value: Any) -> None:
            raise RuntimeError("listener bug")

    made: list[_Listener] = []
    register_partial_args("workflow_author", SPEC, lambda call: made.append(_Boom(call)) or made[-1])
    try:
        api, em = AnthropicChat(), _Emitter()
        await api._handle_event(
            NS(type="content_block_start", index=0, content_block=NS(type="tool_use", name="workflow_author", id="t")), em
        )
        for piece in _pieces(json.dumps(ARGS)):
            await api._handle_event(
                NS(type="content_block_delta", index=0, delta=NS(type="input_json_delta", partial_json=piece)), em
            )
        await api._handle_event(NS(type="content_block_stop", index=0), em)
    finally:
        unregister_partial_args("workflow_author")


NESTED = {
    "action": "update",
    "definition": {
        "nodes": [{"id": "a", "data": {"nodes": [1], "x": "}]"}}, {"id": "b", "type": "t"}],
        "meta": {"nodes": ["decoy"]},
        "edges": [{"id": "e", "source": "a", "target": "b"}],
        "version": "1",
    },
    "nodes": [{"id": "top-level decoy"}],
    "workflow_id": "wf-2",
    "expected_version": 3,
}
NESTED_SPEC = PartialArgsSpec(arrays=("definition.nodes", "definition.edges"), scalars=("action", "workflow_id", "definition.version"))


def test_scanner_reports_nested_paths_through_objects_however_the_text_is_cut():
    """``definition.nodes`` (a whole-definition ``update``) is watched by its dotted path; the same
    key at any other place (``definition.meta.nodes``, top-level ``nodes``) is not."""
    expected = [
        ("action", "update"),
        ("definition.nodes[*]", NESTED["definition"]["nodes"][0]),
        ("definition.nodes[*]", NESTED["definition"]["nodes"][1]),
        ("definition.edges[*]", NESTED["definition"]["edges"][0]),
        ("definition.version", "1"),
        ("workflow_id", "wf-2"),
    ]
    for indent in (None, 2):
        text = json.dumps(NESTED, indent=indent)
        for seed in range(30):
            rnd = random.Random(seed)
            scanner, heard, i = _Scanner(NESTED_SPEC), [], 0
            while i < len(text):
                k = rnd.randint(1, 7)
                heard += [(n, v) for _, n, v in scanner.feed(text[i : i + k])]
                i += k
            assert heard == expected


@pytest.mark.asyncio
async def test_arguments_cut_off_before_they_close_are_heard_as_unfinished(listeners):
    """A call whose block stopped mid-object (the output limit) never runs: its listener must hear
    ``completed=False`` so whatever it showed is rolled back now, not on a timer."""
    api, em = AnthropicChat(), _Emitter()
    text = json.dumps(ARGS)
    for call_id, written in (("toolu_cut", text[: text.index('"nodes_remove"')]), ("toolu_whole", text)):
        await api._handle_event(
            NS(type="content_block_start", index=1, content_block=NS(type="tool_use", name="workflow_author", id=call_id)), em
        )
        await api._handle_event(NS(type="content_block_delta", index=1, delta=NS(type="input_json_delta", partial_json=written)), em)
        await api._handle_event(NS(type="content_block_stop", index=1), em)
    assert [listener.closed for listener in listeners] == [[False], [True]]
