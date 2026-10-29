"""A cursor carries the arguments of the call that returned it.

The incident: a transcript read with `view_options={"grep": "bench/"}` came
back with a cursor, the agent sent page two WITHOUT `view_options`, the cursor's
hash no longer matched, and the refusal told it to "repeat the original read
without cursor" -- so it started over and spent its steps again. Every test
here goes through the REAL `entity`/`search` tool entry point (FastMCP's
argument validation, its default filling, `_tool`, `continuation`), with only
the read service faked.
"""

from __future__ import annotations

import asyncio
import base64
import json
import random
import secrets
import string
import zlib

import pytest
from mcp.shared.memory import create_connected_server_and_client_session

from probe.mcp import continuation
from probe.mcp._generated.views import View
from probe.mcp.contract import ToolCorpus
from probe.mcp.server import create_server

_REF = "session:claude_code/0b9d2f7e-5c1a-4b8e-9f3d-2a6c8e1b7d40"
_GREP = {"grep": "bench/"}


class _Transcripts:
    """A read service with two native pages per ref; it records what it was asked."""

    def __init__(self):
        self.calls: list[dict] = []

    def get_entity(self, ref, view, token_budget, cursor, view_options, *, verbose=False):
        self.calls.append(
            {
                "ref": ref,
                "view": view,
                "cursor": cursor,
                "view_options": view_options,
                "verbose": verbose,
            }
        )
        if cursor is None:
            return {"data": {"ref": ref, "lines": ["page one"]}, "next_cursor": "native-2"}
        assert cursor == "native-2", cursor
        return {"data": {"ref": ref, "lines": ["page two"]}, "next_cursor": None}

    def search(self, query, **kwargs):
        self.calls.append({"query": query, **kwargs})
        if kwargs.get("cursor") is None:
            return {"data": {"hits": ["first"]}, "next_cursor": "native-2"}
        return {"data": {"hits": ["second"]}, "next_cursor": None}


def _call(service, tool: str, arguments: dict) -> tuple[bool, object]:
    async def run():
        mcp = create_server(service)
        async with create_connected_server_and_client_session(mcp) as client:
            return await client.call_tool(tool, arguments)

    result = asyncio.run(run())
    text = result.content[0].text
    return bool(result.isError), (text if result.isError else json.loads(text))


def _first_page(service, **extra) -> str:
    error, page = _call(
        service, "entity", {"refs": [_REF], "view": "transcript", "view_options": _GREP, **extra}
    )
    assert not error, page
    assert page["data"]["lines"] == ["page one"]
    return page["next_cursor"]


def _cursor_json(cursor: str) -> dict:
    raw = cursor[len(continuation.PREFIX) :]
    return json.loads(zlib.decompress(base64.urlsafe_b64decode(raw + "=" * (-len(raw) % 4))))


@pytest.mark.parametrize(
    "dropped",
    [
        pytest.param({"refs": [_REF], "view": "transcript"}, id="view_options-omitted"),
        pytest.param(
            {"refs": [_REF], "view": "transcript", "view_options": None}, id="explicit-null"
        ),
        pytest.param({"refs": [_REF]}, id="view-and-view_options-omitted"),
        pytest.param({"refs": [_REF], "view": "card"}, id="view-at-its-default"),
    ],
)
def test_page_two_without_the_original_view_options_reads_page_two(dropped):
    service = _Transcripts()
    cursor = _first_page(service)
    error, page = _call(service, "entity", {**dropped, "cursor": cursor})
    assert not error, page
    assert page["data"]["lines"] == ["page two"]
    second = service.calls[-1]
    assert second["cursor"] == "native-2"
    assert second["view_options"] == _GREP
    # Re-validated through the tool's own schema: the source gets the enum
    # FastMCP would have built, not the cursor's JSON string.
    assert second["view"] is View.TRANSCRIPT


def test_page_two_with_every_argument_repeated_still_reads_page_two():
    service = _Transcripts()
    cursor = _first_page(service)
    error, page = _call(
        service,
        "entity",
        {"refs": [_REF], "view": "transcript", "view_options": _GREP, "cursor": cursor},
    )
    assert not error, page
    assert page["data"]["lines"] == ["page two"]


@pytest.mark.parametrize(
    "changed,name",
    [
        ({"view_options": {"grep": "other/"}}, "view_options"),
        ({"view": "record"}, "view"),
        # The first call left `verbose` at its default, so the cursor carries
        # none; a continuation that turns it on is a different read.
        ({"verbose": True}, "verbose"),
    ],
)
def test_a_changed_argument_is_refused_by_name_before_any_read(changed, name):
    service = _Transcripts()
    cursor = _first_page(service)
    reads = len(service.calls)
    arguments = {"refs": [_REF], "view": "transcript", "view_options": _GREP, "cursor": cursor}
    error, text = _call(service, "entity", {**arguments, **changed})
    assert error
    assert f"`{name}` differs" in text
    assert "send the same arguments as the call that returned this cursor" in text
    assert "without cursor" not in text
    assert len(service.calls) == reads


def test_a_changed_required_argument_is_still_refused_before_any_read():
    # `refs` is in every call, so it is never carried; the binding refuses it.
    service = _Transcripts()
    cursor = _first_page(service)
    reads = len(service.calls)
    error, text = _call(
        service, "entity", {"refs": ["session:claude_code/another"], "cursor": cursor}
    )
    assert error
    assert "send the same arguments as the call that returned this cursor" in text
    assert len(service.calls) == reads


def test_several_changed_arguments_are_all_named():
    service = _Transcripts()
    cursor = _first_page(service)
    error, text = _call(
        service,
        "entity",
        {"refs": [_REF], "view": "record", "view_options": {"grep": "x"}, "cursor": cursor},
    )
    assert error
    assert "`view`, `view_options` differ" in text


def test_the_delivery_budget_may_change_on_a_continuation():
    service = _Transcripts()
    cursor = _first_page(service, token_budget=512)
    error, page = _call(service, "entity", {"refs": [_REF], "cursor": cursor, "token_budget": 4000})
    assert not error, page
    assert page["data"]["lines"] == ["page two"]
    assert service.calls[-1]["view_options"] == _GREP


def test_the_cursor_carries_only_optional_non_default_arguments():
    cursor = _first_page(_Transcripts())
    assert _cursor_json(cursor)["a"] == {"view": "transcript", "view_options": _GREP}


def _packed_length(value: dict) -> int:
    # The cursor codec, spelled out: canonical JSON, zlib, unpadded urlsafe base64.
    text = json.dumps(value, separators=(",", ":"), sort_keys=True).encode()
    return len(continuation.PREFIX) + len(
        base64.urlsafe_b64encode(zlib.compress(text)).decode().rstrip("=")
    )


def test_a_cursor_that_would_pass_the_size_cap_with_its_arguments_goes_hash_only():
    # Arguments within the carry cap, but a state already near the 4,096-char
    # cursor cap: the cursor drops the arguments rather than refusing to exist.
    rng = random.Random(0)
    alphabet = string.ascii_letters + string.digits

    def noise(n: int) -> str:
        return "".join(rng.choice(alphabet) for _ in range(n))

    request = continuation.Request(id="0" * 32, arguments={"view_options": {"grep": noise(120)}})
    for size in range(3600, 4200, 8):
        native = noise(size)
        bare = _packed_length({"b": request.id, "s": {"native": native}})
        carrying = _packed_length(
            {"a": request.arguments, "b": request.id, "s": {"native": native}}
        )
        if bare <= 4096 < carrying:
            break
    else:
        pytest.fail("no fixture straddles the 4,096-char cap")
    cursor = continuation.encode({"native": native}, request)
    assert cursor == continuation.encode({"native": native}, request.id)
    assert "a" not in _cursor_json(cursor)
    assert continuation.decode(cursor, request) == {"native": native}


@pytest.mark.parametrize(
    "size",
    [
        pytest.param(200, id="past-the-carry-cap"),
        # Incompressible, so the arguments alone would pass the 4,096-char cap.
        pytest.param(4000, id="past-the-cursor-cap"),
    ],
)
def test_arguments_too_big_to_carry_fall_back_to_a_hash_only_cursor(size):
    huge = {"grep": secrets.token_urlsafe(size)}
    service = _Transcripts()
    error, page = _call(
        service, "entity", {"refs": [_REF], "view": "transcript", "view_options": huge}
    )
    assert not error, page
    cursor = page["next_cursor"]
    assert len(cursor) <= 4096
    assert "a" not in _cursor_json(cursor)
    # Hash-only, as every cursor was before: it pages when the call repeats
    # its arguments ...
    repeat = {"refs": [_REF], "view": "transcript", "view_options": huge, "cursor": cursor}
    error, page = _call(service, "entity", repeat)
    assert not error, page
    assert page["data"]["lines"] == ["page two"]
    # ... and cannot fill one that is left out.
    error, text = _call(service, "entity", {"refs": [_REF], "view": "transcript", "cursor": cursor})
    assert error
    assert "send the same arguments as the call that returned this cursor" in text


def test_a_hash_only_cursor_from_before_this_change_still_continues():
    # Exactly what the tool layer emitted before cursors carried arguments: the
    # binding over every argument FastMCP passed (defaults included), no "a".
    service = _Transcripts()
    bound = continuation.binding(
        "entity",
        {
            "refs": [_REF],
            "view": "transcript",
            "view_options": _GREP,
            "verbose": False,
            "filters": None,
        },
        "stdio",
    )
    legacy = continuation.encode({"native": "native-2", "source_budget": 2000}, bound)
    assert "a" not in _cursor_json(legacy)
    error, page = _call(
        service,
        "entity",
        {"refs": [_REF], "view": "transcript", "view_options": _GREP, "cursor": legacy},
    )
    assert not error, page
    assert page["data"]["lines"] == ["page two"]
    error, text = _call(service, "entity", {"refs": [_REF], "view": "transcript", "cursor": legacy})
    assert error
    assert "changed request/scope" in text


def test_a_raw_source_cursor_still_passes_through_untouched():
    service = _Transcripts()
    error, page = _call(
        service,
        "entity",
        {"refs": [_REF], "view": "transcript", "view_options": _GREP, "cursor": "native-2"},
    )
    assert not error, page
    assert page["data"]["lines"] == ["page two"]
    assert service.calls[-1]["cursor"] == "native-2"


def test_a_hand_made_cursor_cannot_carry_a_value_the_schema_refuses():
    forged = continuation.encode(
        {"native": "native-2"},
        continuation.Request(id="0" * 32, arguments={"refs": [_REF], "view": "no-such-view"}),
    )
    service = _Transcripts()
    error, text = _call(service, "entity", {"refs": [_REF], "cursor": forged})
    assert error
    assert "Invalid continuation; restart the read." in text
    assert service.calls == []


def test_a_batch_cursor_carries_its_arguments_too():
    service = _Transcripts()
    other = "session:claude_code/another"
    arguments = {"refs": [_REF, other], "view": "transcript", "view_options": _GREP}
    error, page = _call(service, "entity", arguments)
    assert not error, page
    assert page["rows"][0]["data"]["lines"] == ["page one"]
    error, page = _call(service, "entity", {"refs": [_REF, other], "cursor": page["next_cursor"]})
    assert not error, page
    assert page["rows"][0]["data"]["lines"] == ["page two"]
    assert service.calls[-1]["view_options"] == _GREP


def test_search_shares_the_path():
    service = _Transcripts()
    error, page = _call(service, "search", {"query": "bench", "search_in": ["notes"], "top_k": 3})
    assert not error, page
    error, page = _call(service, "search", {"query": "bench", "cursor": page["next_cursor"]})
    assert not error, page
    assert page["data"]["hits"] == ["second"]
    second = service.calls[-1]
    assert second["search_in"] == [ToolCorpus.NOTES]
    assert second["top_k"] == 3


def test_a_mixed_docs_search_carries_docs_on_page_one_only(client, app):
    """Through the real `search` entry and the real read service: page two,
    sent with the cursor alone, gets `search_in` back from the cursor -- docs
    included -- and still carries no docs list. A cursor page continues the
    team's channels; the docs were answered on page one."""
    from probe.mcp.service import ResearchReadService
    from probe.mcp.source import ResearchOSSource
    from tests.conftest import search_response

    def experiment(eid):
        return {"entity_type": "experiment", "id": eid, "name": eid, "slug": eid,
                "workspace_id": None, "project_id": "p-1", "experiment_id": None,
                "run_id": None, "score": 0.9}

    app.search_responses = [
        search_response(exact=[experiment("e-1"), experiment("e-2")], exact_cursor="ex-2"),
        search_response(exact=[experiment("e-3")]),
    ]
    app.docs_response = {"state": "ok", "sections": [{
        "page": "Install", "heading": "Codex", "path": "install#codex",
        "url": "https://docs.prbe.ai/install#codex", "text": "Run `probe setup codex`.", "rank": 0,
    }]}
    service = ResearchReadService(ResearchOSSource(client))
    error, page = _call(
        service, "search", {"query": "codex", "search_in": ["docs", "experiments"], "top_k": 2}
    )
    assert not error, page
    assert [hit["card"]["title"] for hit in page["data"]["docs"]] == ["Install — Codex"]
    assert [r["id"] for r in page["data"]["results"]] == ["e-1", "e-2"]
    error, page = _call(service, "search", {"query": "codex", "cursor": page["next_cursor"]})
    assert not error, page
    assert [r["id"] for r in page["data"]["results"]] == ["e-3"]
    assert "docs" not in page["data"] and "docs_note" not in page["data"]
    assert app.search_requests[-1]["exact_cursor"] == "ex-2"
    assert len(app.docs_requests) == 1


def test_a_mis_copied_cursor_is_named_as_one_not_as_changed_arguments():
    # strand-ai 2026-10-17: the writer copied a 371-character cursor with one
    # character changed and two added, was told its request had changed, sent
    # the same arguments and the same broken cursor twice more, and the bite failed.
    service = _Transcripts()
    cursor = _first_page(service)
    body = cursor[len(continuation.PREFIX):]
    i = len(body) // 2
    miscopied = continuation.PREFIX + body[:i] + ("A" if body[i] != "A" else "B") + body[i + 1:]
    error, text = _call(
        service,
        "entity",
        {"refs": [_REF], "view": "transcript", "view_options": _GREP, "cursor": miscopied},
    )
    assert error
    assert "not copied exactly" in text and "changed request/scope" not in text
    assert len(service.calls) == 1, "nothing read on a cursor no result returned"
