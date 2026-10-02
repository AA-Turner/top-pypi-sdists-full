"""Byte accounting for hosted MCP tool responses.

The three things worth breaking on are all silent failures — each would ship an event
stream that looks fine and means nothing:

  * the tool name not surviving the worker-thread boundary (every event `tool: None`)
  * emission raising into the ASGI send path (a tool call fails to measure itself)
  * counting bodies we do not actually serve (initialize/tools-list inflating totals)
"""

from __future__ import annotations

import asyncio
import pathlib
import queue
import re
import threading

import anyio
import anyio.to_thread
import pytest

from probe.client_headers import CLIENT_KIND_HEADER, CLIENT_VERSION_HEADER
from probe.mcp import accounting


def _headers(**pairs: str) -> dict[bytes, bytes]:
    return {k.lower().encode(): v.encode() for k, v in pairs.items()}


# --- header parsing ---------------------------------------------------------


def test_a_captured_agent_and_valid_session_are_read() -> None:
    agent, session = accounting.agent_from_headers(
        _headers(**{"X-Probe-Agent": "claude_code", "X-Probe-Agent-Session": "a" * 12})
    )
    assert (agent, session) == ("claude_code", "a" * 12)


def test_absent_headers_yield_no_attribution() -> None:
    assert accounting.agent_from_headers({}) == (None, None)


def test_an_uncaptured_agent_is_refused() -> None:
    """Cursor is detectable but its transcripts never reach us, so a session id from it
    is a link nobody can follow. The plugin does not send one; the server does not
    trust that it did not."""
    agent, session = accounting.agent_from_headers(
        _headers(**{"X-Probe-Agent": "cursor", "X-Probe-Agent-Session": "a" * 12})
    )
    assert (agent, session) == (None, None)


def test_a_session_id_outside_the_charset_is_refused() -> None:
    agent, session = accounting.agent_from_headers(
        _headers(**{"X-Probe-Agent": "claude_code", "X-Probe-Agent-Session": "no spaces here"})
    )
    assert agent == "claude_code"
    assert session is None


def test_a_session_without_an_agent_is_refused() -> None:
    """Half a key resolves to nothing: the graph id is agent_session:{agent}:{id}."""
    agent, session = accounting.agent_from_headers(
        _headers(**{"X-Probe-Agent-Session": "a" * 12})
    )
    assert (agent, session) == (None, None)


def test_non_ascii_headers_do_not_raise() -> None:
    assert accounting.agent_from_headers({b"x-probe-agent": b"\xff\xfe"}) == (None, None)


# --- the holder -------------------------------------------------------------


def test_the_holder_carries_the_callers_client_not_ours() -> None:
    state = accounting.begin_request(
        "claude_code",
        "a" * 12,
        {CLIENT_KIND_HEADER: "plugin", CLIENT_VERSION_HEADER: "0.43.0"},
    )
    try:
        assert state["holder"]["client_kind"] == "plugin"
        assert state["holder"]["client_version"] == "0.43.0"
    finally:
        accounting.end_request(state)


def test_an_unreported_client_leaves_the_pair_empty() -> None:
    state = accounting.begin_request(None, None, {})
    try:
        assert state["holder"]["client_kind"] is None
        assert state["holder"]["client_version"] is None
    finally:
        accounting.end_request(state)


def test_note_tool_outside_a_request_is_a_no_op() -> None:
    """Stdio binds no holder. This must not raise — it runs on every tool call."""
    accounting.note_tool("browse")


# --- the thread boundary (the critical one) ---------------------------------


def test_the_tool_name_survives_the_worker_thread() -> None:
    """`_threaded_tool` runs tool bodies via anyio.to_thread.run_sync, which hands the
    worker a COPY of the context. Rebinding the ContextVar there would be invisible out
    here and every event would carry `tool: None`, with nothing failing to say so.

    This exercises the real anyio path rather than calling note_tool inline, because
    calling it inline is precisely the test that would pass while the product broke.
    """

    async def scenario() -> str | None:
        state = accounting.begin_request("claude_code", "a" * 12, {})
        try:

            def body() -> None:
                accounting.note_tool("search_knowledge")

            await anyio.to_thread.run_sync(body)
            return state["holder"]["tool"]
        finally:
            accounting.end_request(state)

    assert asyncio.run(scenario()) == "search_knowledge"


def test_rebinding_the_contextvar_in_the_worker_would_not_have_worked() -> None:
    """Pins WHY the holder is mutable, so a later refactor to a plain ContextVar value
    fails here with an explanation instead of silently emitting null tool names."""

    async def scenario() -> tuple[object, object]:
        state = accounting.begin_request(None, None, {})
        try:

            def body() -> None:
                accounting._request.set({"tool": "rebound"})

            await anyio.to_thread.run_sync(body)
            return (accounting._request.get(), state["holder"])
        finally:
            accounting.end_request(state)

    outer, holder = asyncio.run(scenario())
    assert outer is holder, "the worker's rebind must not be visible out here"
    assert holder["tool"] is None


# --- byte counting ----------------------------------------------------------


def _drain(state, messages):
    async def go():
        sent = []

        async def send(message):
            sent.append(message)

        wrapped = accounting.counting_send(state, send)
        for message in messages:
            await wrapped(message)
        return sent

    return asyncio.run(go())


def test_a_single_body_is_counted() -> None:
    state = accounting.begin_request(None, None, {})
    try:
        _drain(state, [{"type": "http.response.body", "body": b"0123456789"}])
        assert state["holder"]["response_bytes"] == 10
    finally:
        accounting.end_request(state)


def test_a_chunked_body_is_summed() -> None:
    state = accounting.begin_request(None, None, {})
    try:
        _drain(
            state,
            [
                {"type": "http.response.body", "body": b"abc", "more_body": True},
                {"type": "http.response.body", "body": b"defg", "more_body": True},
                {"type": "http.response.body", "body": b""},
            ],
        )
        assert state["holder"]["response_bytes"] == 7
    finally:
        accounting.end_request(state)


def test_response_start_contributes_nothing() -> None:
    state = accounting.begin_request(None, None, {})
    try:
        _drain(
            state,
            [
                {"type": "http.response.start", "status": 200, "headers": []},
                {"type": "http.response.body", "body": b"xy"},
            ],
        )
        assert state["holder"]["response_bytes"] == 2
    finally:
        accounting.end_request(state)


def test_every_message_still_reaches_the_real_send() -> None:
    """The wrapper is on the response path; dropping a message would hang the client."""
    state = accounting.begin_request(None, None, {})
    try:
        messages = [
            {"type": "http.response.start", "status": 200, "headers": []},
            {"type": "http.response.body", "body": b"xy"},
        ]
        assert _drain(state, messages) == messages
    finally:
        accounting.end_request(state)


def test_bytes_not_characters() -> None:
    """The unit is what ASGI hands us. A 3-byte character must count as 3, and the
    property name says bytes so nobody divides it as if it were characters."""
    state = accounting.begin_request(None, None, {})
    try:
        _drain(state, [{"type": "http.response.body", "body": "日本".encode()}])
        assert state["holder"]["response_bytes"] == 6
    finally:
        accounting.end_request(state)


# --- emission ---------------------------------------------------------------


@pytest.fixture
def captured(monkeypatch):
    # Opt IN to emission. `_telemetry_off` pins PROBE_TELEMETRY=off suite-wide and
    # `_telemetry_permitted()` fails closed on it, so without this every assertion
    # below would pass against an empty list -- the shape of green test that proves
    # nothing. Base URL must also satisfy the self-host egress gate.
    monkeypatch.setenv("PROBE_TELEMETRY", "on")
    monkeypatch.setenv(accounting.ANALYTICS_ENV, "1")
    sent: list[dict] = []
    sender = accounting._Sender()
    sender.put = sent.append  # type: ignore[method-assign]
    monkeypatch.setattr(accounting, "_ensure_sender", lambda: sender)
    return sent


_IDENTITY = {
    "distinct_id": "u-1",
    "customer_id": "acme",
    "workspace_id": None,
    "authenticated": True,
}


def test_a_request_that_ran_no_tool_emits_nothing(captured) -> None:
    """initialize and tools/list share this path. Schema traffic is out of scope by
    decision — the ~37.7KB of instructions plus schemas is tracked in TODOS.md."""
    state = accounting.begin_request("claude_code", "a" * 12, {})
    accounting.emit(state, _IDENTITY)
    accounting.end_request(state)
    assert captured == []


def test_a_served_tool_emits_one_event_with_its_bytes(captured) -> None:
    state = accounting.begin_request("claude_code", "a" * 12, {})
    state["holder"]["tool"] = "browse"
    state["holder"]["response_bytes"] = 4096
    accounting.emit(state, _IDENTITY)
    accounting.end_request(state)

    assert len(captured) == 1
    entry = captured[0]
    assert entry["event"] == accounting.EVENT_TOOL_SERVED
    assert entry["distinct_id"] == "u-1"
    props = entry["properties"]
    assert props["tool"] == "browse"
    assert props["response_bytes"] == 4096
    assert props["agent"] == "claude_code"
    assert props["agent_session_id"] == "a" * 12
    assert props["team"] == "acme"


def test_legacy_emission_does_not_invent_a_token_estimate(captured) -> None:
    """An ASGI byte count alone is not an exact final-text reference token count."""
    state = accounting.begin_request("claude_code", "a" * 12, {})
    state["holder"]["tool"] = "browse"
    state["holder"]["response_bytes"] = 4096
    accounting.emit(state, _IDENTITY)
    accounting.end_request(state)

    props = captured[0]["properties"]
    assert not any("token" in key.lower() for key in props)
    assert 1024 not in props.values(), "4096/4 must not appear anywhere"


_DELIVERY = {
    "reference_tokens": 123,
    "response_text_bytes": 678,
    "token_budget": 2000,
    "has_continuation": True,
}


def test_delivery_counts_survive_worker_and_remain_distinct_from_asgi_bytes(captured) -> None:
    async def scenario():
        state = accounting.begin_request("claude_code", "a" * 12, {})
        try:
            accounting.note_tool("entity")
            await anyio.to_thread.run_sync(lambda: accounting.note_delivery(**_DELIVERY))
            state["holder"]["response_bytes"] = 901
            accounting.emit(state, _IDENTITY)
        finally:
            accounting.end_request(state)

    asyncio.run(scenario())
    assert len(captured) == 1
    props = captured[0]["properties"]
    assert all(props[key] == value for key, value in _DELIVERY.items())
    assert props["reference_encoding"] == "o200k_base_frozen_v1"
    assert props["response_bytes"] == 901
    assert "stale_reason" not in props
    assert not any("billed" in key for key in props)


def test_delivery_without_hosted_holder_does_not_start_a_sender(monkeypatch) -> None:
    def unexpected():
        pytest.fail("stdio must not start an analytics sender")

    monkeypatch.setattr(accounting, "_ensure_sender", unexpected)
    assert accounting._request.get() is None
    accounting.note_delivery(**_DELIVERY)
    assert accounting._request.get() is None


@pytest.mark.parametrize(
    "change",
    [
        {"reference_tokens": "private query text"},
        {"reference_tokens": -1},
        {"reference_tokens": True},
        {"response_text_bytes": {"raw_cursor": "private"}},
        {"response_text_bytes": -1},
        {"response_text_bytes": 4.5},
        {"token_budget": False},
        {"token_budget": 511},
        {"token_budget": 8001},
        {"has_continuation": "private cursor"},
    ],
)
def test_invalid_delivery_scalars_are_dropped_without_changing_legacy_event(captured, change):
    state = accounting.begin_request(None, None, {})
    try:
        accounting.note_tool("browse")
        accounting.note_delivery(**{**_DELIVERY, **change})
        accounting.emit(state, _IDENTITY)
    finally:
        accounting.end_request(state)
    props = captured[0]["properties"]
    assert not (set(props) & accounting._DELIVERY_PROPERTIES)
    assert "private" not in str(props)
    assert props["tool"] == "browse"


@pytest.mark.parametrize("reason", [None, "source_changed", "private error or cursor", {"query": 1}])
def test_stale_reason_is_a_closed_dimension(captured, reason):
    state = accounting.begin_request(None, None, {})
    try:
        accounting.note_tool("entity")
        accounting.note_delivery(**_DELIVERY, stale_reason=reason)
        accounting.emit(state, _IDENTITY)
    finally:
        accounting.end_request(state)
    props = captured[0]["properties"]
    assert props["reference_tokens"] == 123
    assert props.get("stale_reason") == ("source_changed" if reason == "source_changed" else None)
    assert "private" not in str(props) and "query" not in str(props)


def test_final_delivery_replaces_earlier_measurement_and_preserves_a_cap_breach(captured):
    state = accounting.begin_request(None, None, {})
    try:
        accounting.note_tool("entity")
        accounting.note_delivery(**_DELIVERY, stale_reason="source_changed")
        accounting.note_delivery(
            reference_tokens=2001,
            response_text_bytes=16001,
            token_budget=2000,
            has_continuation=False,
        )
        accounting.emit(state, _IDENTITY)
    finally:
        accounting.end_request(state)
    props = captured[0]["properties"]
    assert props["reference_tokens"] == 2001 and props["response_text_bytes"] == 16001
    assert props["has_continuation"] is False and "stale_reason" not in props


def test_invalid_final_measurement_cannot_leave_an_earlier_count(captured):
    state = accounting.begin_request(None, None, {})
    try:
        accounting.note_tool("entity")
        accounting.note_delivery(**_DELIVERY)
        accounting.note_delivery(**{**_DELIVERY, "reference_tokens": None})
        accounting.emit(state, _IDENTITY)
    finally:
        accounting.end_request(state)
    assert not (set(captured[0]["properties"]) & accounting._DELIVERY_PROPERTIES)


def test_no_payload_content_reaches_the_event(captured) -> None:
    state = accounting.begin_request("claude_code", "a" * 12, {})
    state["holder"]["tool"] = "browse"
    state["holder"]["response_bytes"] = 12
    accounting.emit(state, _IDENTITY)
    accounting.end_request(state)

    assert set(captured[0]["properties"]) <= {
        "tool",
        "view",
        "response_bytes",
        "agent",
        "agent_session_id",
        "client_kind",
        "client_version",
        "team",
        "authenticated",
        "machine_id",
        "workspace_id",
        "$groups",
        "$lib",
        "$lib_version",
        "$process_person_profile",
        "cli_version",
    }


def test_email_is_not_forwarded_onto_the_person(captured) -> None:
    """build_batch would $set it onto the PostHog person. The distinct_id already
    merges with the dashboard's identify, so carrying email adds an identifiable field
    for no analytical gain — on the surface where account deletion is a known gap."""
    state = accounting.begin_request("claude_code", "a" * 12, {})
    state["holder"]["tool"] = "browse"
    accounting.emit(state, {**_IDENTITY, "email": "someone@example.com"})
    accounting.end_request(state)

    entry = captured[0]
    assert "$set" not in entry["properties"]
    assert "example.com" not in str(entry)


def test_an_unidentified_caller_still_emits_unattributed(captured) -> None:
    state = accounting.begin_request(None, None, {})
    state["holder"]["tool"] = "browse"
    accounting.emit(state, None)
    accounting.end_request(state)

    assert len(captured) == 1
    assert captured[0]["properties"]["authenticated"] is False


def test_emission_never_raises(monkeypatch) -> None:
    """It runs in the ASGI wrapper's finally. Raising there would turn a measurement
    problem into a failed tool call."""

    def boom():
        raise RuntimeError("sender is down")

    monkeypatch.setattr(accounting, "_ensure_sender", boom)
    state = accounting.begin_request("claude_code", "a" * 12, {})
    state["holder"]["tool"] = "browse"
    accounting.emit(state, _IDENTITY)  # must not raise
    accounting.end_request(state)


def test_a_malformed_state_never_raises() -> None:
    accounting.emit({}, None)
    accounting.emit({"holder": None}, None)


# --- the sender -------------------------------------------------------------


def test_a_full_queue_drops_rather_than_blocks() -> None:
    sender = accounting._Sender()
    sender.q = queue.Queue(maxsize=1)
    sender.put({"event": "one"})
    sender.put({"event": "two"})  # must not block or raise
    assert sender.q.qsize() == 1


def test_a_dead_transport_costs_the_caller_nothing() -> None:
    """PostHog being down must not kill the drain thread: the next tool call still
    needs somewhere to put its count."""
    sender = accounting._Sender()
    attempted = threading.Event()

    def explode(batch):
        attempted.set()
        raise RuntimeError("posthog is down")

    sender.transport = explode
    sender.start()
    sender.put({"event": "one"})
    assert attempted.wait(timeout=5), "the drain thread never attempted a send"

    # Still alive and still draining after the failure.
    attempted.clear()
    sender.put({"event": "two"})
    assert attempted.wait(timeout=5), "the thread died on the first failure"
    assert sender._thread is not None and sender._thread.is_alive()


# --- the gate, and what it is for -------------------------------------------


def test_the_killswitch_silences_the_hosted_emitter(monkeypatch) -> None:
    """PROBE_TELEMETRY=off must stop this surface too. It owns its own sender, so the
    gate every other sender applies had to be applied here explicitly."""
    from probe.mcp import accounting as acc

    sent: list[dict] = []
    sender = acc._Sender()
    sender.put = sent.append  # type: ignore[method-assign]
    monkeypatch.setattr(acc, "_ensure_sender", lambda: sender)
    monkeypatch.setenv(acc.ANALYTICS_ENV, "1")
    monkeypatch.setenv("PROBE_TELEMETRY", "off")

    state = acc.begin_request("claude_code", "a" * 12, {})
    try:
        state["holder"]["tool"] = "browse"
        acc.note_delivery(**_DELIVERY)
        acc.emit(state, _IDENTITY)
    finally:
        acc.end_request(state)
    assert sent == []


def test_a_self_hoster_emits_nothing(monkeypatch) -> None:
    """`probe-research-mcp-http` is a published console script, so anyone can run this
    server. tests/selfhost/test_egress.py promises we never call the vendor from a
    self-hosted deployment; without this gate a self-hoster would ship THEIR users'
    ids, tools and session ids to OUR PostHog with the embedded capture key.

    Fail-CLOSED: the opt-in is simply absent, which is what a self-hoster who
    configured nothing looks like."""
    from probe.mcp import accounting as acc

    sent: list[dict] = []
    sender = acc._Sender()
    sender.put = sent.append  # type: ignore[method-assign]
    monkeypatch.setattr(acc, "_ensure_sender", lambda: sender)
    monkeypatch.setenv("PROBE_TELEMETRY", "on")
    monkeypatch.delenv(acc.ANALYTICS_ENV, raising=False)

    state = acc.begin_request("claude_code", "a" * 12, {})
    try:
        state["holder"]["tool"] = "browse"
        acc.note_delivery(**_DELIVERY)
        acc.emit(state, _IDENTITY)
    finally:
        acc.end_request(state)
    assert sent == []


def test_the_servers_own_environment_never_labels_a_callers_event(captured, monkeypatch) -> None:
    """The bug this guards is the one the release fixes clientside, reintroduced on the
    server: build_batch's `agent` default detects from THIS process, which on a pod is
    the pod. A caller who sent no header must come out unattributed, not labelled with
    whatever the deployment happens to look like."""
    monkeypatch.setenv("PROBE_AGENT", "claude_code")  # as a stray pod env var would be
    monkeypatch.setenv("CLAUDECODE", "1")

    state = accounting.begin_request(None, None, {})
    try:
        state["holder"]["tool"] = "browse"
        accounting.emit(state, _IDENTITY)
    finally:
        accounting.end_request(state)

    assert "agent" not in captured[0]["properties"], (
        "the server labelled a caller it knows nothing about"
    )


def test_a_non_bytes_body_neither_raises_nor_breaks_the_response() -> None:
    """A different ASGI server could hand us a str or memoryview. The response must
    still go out; only the count is allowed to be wrong."""
    state = accounting.begin_request(None, None, {})
    try:
        messages = [{"type": "http.response.body", "body": "not bytes"}]
        assert _drain(state, messages) == messages
        # A str has a len() too. Counting its CHARACTERS into a field named
        # response_bytes is the silent wrongness this module exists to avoid.
        assert state["holder"]["response_bytes"] == 0
    finally:
        accounting.end_request(state)


def test_end_request_survives_being_called_twice() -> None:
    state = accounting.begin_request(None, None, {})
    accounting.end_request(state)
    accounting.end_request(state)  # must not raise
    assert accounting._request.get() is None


def test_the_production_manifest_actually_turns_this_on() -> None:
    """The gate and the Deployment must agree, and only reading the manifest proves it.

    This exists because the first version of the gate keyed off `PROBE_BASE_URL`, which
    the hosted pod sets to the in-cluster Service (`http://research-os...:8080`) to dodge
    a load-balancer hairpin. That is neither https nor a prbe.ai host, so the gate said
    "self-hosted" about our own production fleet and the feature emitted nothing -- while
    every other test in this file stayed green, because none of them set that variable.

    A unit test cannot catch a gate that disagrees with a manifest. So read the manifest.
    """
    manifest = (
        pathlib.Path(__file__).resolve().parent.parent / "deploy" / "mcp" / "k8s.yaml"
    ).read_text()
    assert f"name: {accounting.ANALYTICS_ENV}" in manifest, (
        "the hosted Deployment does not set the opt-in, so production emits nothing"
    )
    env = dict(re.findall(r'name: (PROBE_[A-Z_]+), value: "([^"]*)"', manifest))
    assert env.get(accounting.ANALYTICS_ENV) == "1"
    # And prove the gate agrees, with the manifest's own values in the environment.
    import os

    restore = dict(os.environ)
    try:
        os.environ.update(env)
        os.environ.pop("PROBE_TELEMETRY", None)
        assert accounting._telemetry_permitted() is True
    finally:
        os.environ.clear()
        os.environ.update(restore)


# --- view: the dimension that splits get_entity's two cost shapes -----------


def test_a_known_view_is_recorded() -> None:
    state = accounting.begin_request(None, None, {})
    try:
        accounting.note_view("reproduce")
        assert state["holder"]["view"] == "reproduce"
    finally:
        accounting.end_request(state)


def test_an_unknown_view_is_dropped_not_recorded() -> None:
    """Validated against contract.View, not merely length-bounded. The argument comes
    from the caller, and an open string would make this a cardinality hazard on a
    property whose whole purpose is to be a closed dimension."""
    state = accounting.begin_request(None, None, {})
    try:
        accounting.note_view("card")
        accounting.note_view("../../etc/passwd")
        accounting.note_view("x" * 5000)
        accounting.note_view(None)
        accounting.note_view(12)
        assert state["holder"]["view"] == "card", "a bogus view overwrote a real one"
    finally:
        accounting.end_request(state)


def test_note_view_outside_a_request_is_a_no_op() -> None:
    accounting.note_view("card")  # stdio binds no holder; must not raise


def test_a_tool_with_no_view_argument_records_none(captured) -> None:
    state = accounting.begin_request("claude_code", "a" * 12, {})
    try:
        state["holder"]["tool"] = "search_knowledge"
        accounting.emit(state, _IDENTITY)
    finally:
        accounting.end_request(state)
    assert "view" not in captured[0]["properties"]


def test_the_view_rides_the_event(captured) -> None:
    state = accounting.begin_request("claude_code", "a" * 12, {})
    try:
        state["holder"]["tool"] = "entity"
        state["holder"]["view"] = "trajectory"
        state["holder"]["response_bytes"] = 4096
        accounting.emit(state, _IDENTITY)
    finally:
        accounting.end_request(state)
    props = captured[0]["properties"]
    assert props["tool"] == "entity"
    assert props["view"] == "trajectory"


def test_every_view_the_service_serves_is_recordable() -> None:
    """Guard against the enum growing a member this cannot express. If a new view
    lands and is not accepted here, its traffic silently files as no-view."""
    from probe.mcp.contract import View

    for member in View:
        state = accounting.begin_request(None, None, {})
        try:
            accounting.note_view(member.value)
            assert state["holder"]["view"] == member.value, member
        finally:
            accounting.end_request(state)
