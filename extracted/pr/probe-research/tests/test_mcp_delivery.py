"""Consumer-facing MCP budget, reconstruction and cursor regression tests.

All sources are synthetic. The memory transport runs the same JSON-RPC handler
as stdio; HTTP tests additionally exercise actual FastMCP response serialization.
"""

from __future__ import annotations

import asyncio
import base64
import copy
import hashlib
import json
import sys
import zlib
from collections import Counter
from datetime import timedelta
from pathlib import Path

import httpx
import pytest
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.server.transport_security import TransportSecuritySettings
from mcp.shared.memory import create_connected_server_and_client_session

from probe.mcp import continuation
from probe.mcp.budget import Budget, count_tokens
from probe.mcp.server import create_server

_OPEN = TransportSecuritySettings(enable_dns_rebinding_protection=False)
_SMALL = {
    "data": {"ref": "run:synthetic", "status": "completed", "score": 0.75},
    "completeness": {"state": "complete", "missing": []},
    "next_cursor": None,
}
_TOOL_ARGUMENTS = {
    "search_knowledge": {"query": "synthetic"},
    "entity": {"refs": ["run:synthetic"], "view": "record"},
    "metrics": {"run_id": "synthetic", "mode": "coordinates"},
    "find_papers": {"mode": "search", "query": "synthetic"},
}


class _Service:
    def __init__(self, payload=None, error=None):
        self.payload = copy.deepcopy(_SMALL if payload is None else payload)
        self.error = error
        self.calls = []

    def __getattr__(self, name):
        def read(*args, **kwargs):
            self.calls.append((name, args, kwargs))
            if self.error is not None:
                raise self.error
            return copy.deepcopy(self.payload)

        return read


def _wire(service, tool, arguments, *, transport="http", register=None):
    async def run():
        mcp = create_server(service, transport_security=_OPEN)
        if register is not None:
            register(mcp)
        if transport == "memory":
            async with create_connected_server_and_client_session(mcp) as client:
                result = await client.call_tool(tool, arguments)
                return result.model_dump(mode="json", exclude_none=True)
        mcp.settings.streamable_http_path = "/mcp"
        app = mcp.streamable_http_app()
        async with app.router.lifespan_context(app):
            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(app=app), base_url="http://mcp.test"
            ) as client:
                response = await client.post(
                    "/mcp",
                    json={
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "tools/call",
                        "params": {"name": tool, "arguments": arguments},
                    },
                    headers={"Accept": "application/json, text/event-stream"},
                )
                assert response.status_code == 200, response.text
                return response.json()["result"]

    return asyncio.run(run())


def _bounded(result, limit=512, *, error=False):
    assert result.get("isError", False) is error, result
    assert "structuredContent" not in result, "a second full payload would bypass the cap"
    assert len(result["content"]) == 1
    block = result["content"][0]
    assert block["type"] == "text"
    text = block["text"]
    assert len(text.encode("utf-8")) <= 8 * limit
    assert count_tokens(text) <= limit
    return text if error else json.loads(text)


@pytest.mark.parametrize("transport", ["memory", "http"])
def test_small_status_answer_survives_the_real_mcp_boundary_in_one_read(transport):
    service = _Service()
    result = _wire(
        service, "entity", {"refs": ["run:synthetic"], "token_budget": 512}, transport=transport
    )
    # The service fake answers with the full envelope; delivery drops its defaults.
    assert _bounded(result) == {"data": _SMALL["data"]}
    assert len(service.calls) == 1


def test_real_stdio_process_enforces_caps_and_reconstructs_without_duplicate_content(tmp_path):
    code = """
from probe.mcp.server import create_server
class Source:
    def search_knowledge(self, query, **kwargs):
        if query == 'error':
            raise ValueError('synthetic upstream failure ' * 10000)
        return {'data': {'evidence': 'synthetic evidence 🌍 ' * 600}}
create_server(Source()).run(transport='stdio')
"""
    params = StdioServerParameters(
        command=sys.executable,
        args=["-c", code],
        cwd=tmp_path,
        env={
            "HOME": str(tmp_path),
            "PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src"),
            "PROBE_TELEMETRY": "off",
            "PYTHONDONTWRITEBYTECODE": "1",
        },
    )

    async def run():
        async with stdio_client(params) as (read, write):
            async with ClientSession(
                read, write, read_timeout_seconds=timedelta(seconds=15)
            ) as client:
                await client.initialize()
                cursor, pieces = None, []
                for _ in range(40):
                    result = await client.call_tool(
                        "search_knowledge",
                        {"query": "synthetic", "token_budget": 512, "cursor": cursor},
                    )
                    page = _bounded(result.model_dump(mode="json", exclude_none=True))
                    pieces.append(page["data"]["text"])
                    cursor = page.get("next_cursor")
                    if cursor is None:
                        break
                else:
                    pytest.fail("stdio walk failed to terminate")
                assert json.loads("".join(pieces)) == {
                    "data": {"evidence": "synthetic evidence 🌍 " * 600}
                }
                failed = await client.call_tool(
                    "search_knowledge", {"query": "error", "token_budget": 512}
                )
                assert _bounded(failed.model_dump(mode="json", exclude_none=True), error=True)

    asyncio.run(run())


@pytest.mark.parametrize("value", [True, False, 512.0, "512", None, 511, 8001, {}, []])
def test_raw_invalid_budget_is_rejected_before_fastmcp_can_coerce_it(value):
    service = _Service()
    result = _wire(service, "search_knowledge", {"query": "synthetic", "token_budget": value})
    assert "token_budget" in _bounded(result, error=True)
    assert service.calls == []


@pytest.mark.parametrize("refs", [[], ["run:synthetic"] * 21, ["run:" + "x" * 10000]])
def test_invalid_batch_size_or_oversized_reference_is_a_bounded_pre_read_error(refs):
    service = _Service()
    result = _wire(service, "entity", {"refs": refs, "token_budget": 512})
    assert _bounded(result, error=True)
    assert service.calls == []


def test_duplicate_references_preserve_each_requested_position():
    service = _Service()
    result = _wire(
        service, "entity", {"refs": ["run:synthetic", "run:synthetic"], "token_budget": 512}
    )
    page = _bounded(result)
    assert [row["ref"] for row in page["rows"]] == ["run:synthetic", "run:synthetic"]
    assert all(row == {"ref": "run:synthetic", "data": _SMALL["data"]} for row in page["rows"])
    assert "missing" not in page
    assert "next_cursor" not in page


def test_maximum_sized_batch_finishes_without_refetching_completed_positions():
    refs = [f"run:synthetic-{i:02}" for i in range(20)]
    done, seen = set(), []

    def read(args):
        ref = args["refs"][0]
        assert ref not in done
        return {"data": {"ref": ref, "evidence": "a measured synthetic finding " * 10}}

    cursor = None
    for _ in range(40):
        page = continuation.invoke(
            "entity", {"refs": refs, "token_budget": 512, "cursor": cursor}, read, "tenant-a"
        )
        assert Budget(512).fits(page)
        for row in page["rows"]:
            done.add(row["ref"])
            seen.append(row["ref"])
        cursor = page.get("next_cursor")
        if cursor is None:
            break
    else:
        pytest.fail("maximum accepted batch failed to finish")
    assert seen == refs


@pytest.mark.parametrize("transport", ["memory", "http"])
def test_new_unwrapped_tool_still_cannot_emit_an_oversized_or_duplicate_payload(transport):
    def register(mcp):
        @mcp.tool()
        def future_tool() -> dict[str, str]:
            return {"evidence": "long synthetic evidence " * 2000}

    result = _wire(
        _Service(), "future_tool", {"token_budget": 512}, transport=transport, register=register
    )
    assert _bounded(result, error=True)


def test_small_typed_future_tool_keeps_working_without_a_structured_duplicate():
    def register(mcp):
        @mcp.tool()
        def future_tool() -> dict[str, str]:
            return {"evidence": "small synthetic finding"}

    result = _wire(_Service(), "future_tool", {"token_budget": 512}, register=register)
    assert _bounded(result) == {"evidence": "small synthetic finding"}


def test_every_advertised_tool_has_a_delivery_fixture_or_the_separate_browse_suite():
    tools = asyncio.run(create_server(_Service()).list_tools())
    # `query_sql` is not paged: re-reading re-runs the query, so it answers in
    # ONE cut page and never a cursor. Its delivery is pinned in
    # test_mcp_query_sql.py, the way browse's is in its own suite.
    assert {tool.name for tool in tools} == {"browse", "query_sql", *_TOOL_ARGUMENTS}
    for tool in tools:
        assert "token_budget" in tool.inputSchema["properties"]


@pytest.mark.parametrize("name,args", list(_TOOL_ARGUMENTS.items()))
def test_non_browse_tools_enforce_a_cap_without_discarding_valid_oversized_data(name, args):
    service = _Service({"data": {"evidence": "measured synthetic evidence " * 1000}})
    result = _wire(service, name, {**args, "token_budget": 512})
    payload = _bounded(result)
    assert payload.get("next_cursor"), "a valid oversized source must remain reachable"
    assert len(service.calls) == 1


def test_http_full_json_walk_reconstructs_every_scientific_value_across_replicas():
    source = {
        "data": {
            "rows": [
                {"id": i, "score": i / 8, "notes": "证据 🌍 <|endoftext|> " * 30} for i in range(12)
            ],
            "configuration": {"lora_rank": 64, "seed": 7},
        },
        "completeness": {"state": "partial", "missing": ["upstream_metric_gap"]},
        "next_cursor": None,
    }
    service = _Service(source)
    cursor, fragments, expected_offset = None, [], 0
    for _ in range(100):
        # _wire creates a fresh server for each page, like another hosted replica.
        result = _wire(
            service,
            "entity",
            {"refs": ["run:synthetic"], "view": "record", "token_budget": 512, "cursor": cursor},
        )
        page = _bounded(result)
        fragment = page["data"]
        assert fragment["format"] == "json_fragment"
        assert fragment["offset"] == expected_offset
        assert fragment["text"]
        fragments.append(fragment["text"])
        expected_offset += len(fragment["text"])
        cursor = page.get("next_cursor")
        if cursor is None:
            assert fragment["complete"] is True
            assert page["completeness"] == source["completeness"]
            break
        assert fragment["complete"] is False
    else:
        pytest.fail("full walk did not finish within 100 bounded reads")
    reconstructed = "".join(fragments)
    # Every scientific value and the partial verdict survive; the null cursor is
    # a default, dropped exactly as a whole-fit answer drops it.
    assert json.loads(reconstructed) == continuation.omit_defaults(source)
    assert json.loads(reconstructed)["completeness"] == source["completeness"]
    assert hashlib.sha256(reconstructed.encode()).hexdigest() == fragment["sha256"]
    assert len(service.calls) == len(fragments)


def test_authored_text_walk_keeps_the_original_prefix_when_the_document_is_appended():
    original = "# Synthetic notes\n证据 🌍 <|endoftext|> trailing spaces  \n" * 100
    current = original
    args = {"refs": ["project:synthetic"], "view": "notes", "token_budget": 512}

    def read(_):
        return {
            "data": {"notes": current, "notes_version": len(current)},
            "as_of": len(current),
            "completeness": {"state": "complete", "missing": []},
        }

    cursor, chunks, offset = None, [], 0
    for _ in range(100):
        page = continuation.invoke("entity", {**args, "cursor": cursor}, read, "tenant-a")
        assert Budget(512).fits(page)
        item = page["data"]
        assert item["format"] == "text_fragment"
        assert item["offset"] == offset
        assert item["path"] == ["data", "notes"]
        chunks.append(item["text"])
        offset += len(item["text"])
        cursor = page.get("next_cursor")
        current += "new appended evidence\n"
        if cursor is None:
            break
    else:
        pytest.fail("append-only document failed to finish")
    assert "".join(chunks) == original


def test_first_fragment_keeps_an_upstream_gap_visible_without_finishing_the_walk():
    def read(_):
        return {
            "data": {"evidence": "synthetic finding " * 2000},
            "completeness": {"state": "partial", "missing": ["upstream_metric_gap"]},
        }

    page = continuation.invoke(
        "entity",
        {"refs": ["run:synthetic"], "view": "record", "token_budget": 512},
        read,
        "tenant-a",
    )
    assert Budget(512).fits(page)
    assert page["next_cursor"]
    assert "upstream_metric_gap" in page["completeness"]["missing"]


def test_oversized_notes_do_not_drop_authored_sub_note_caveats_from_the_complete_walk():
    # Matches service._notes_with_sub_notes: the titled caveat is independent
    # authored evidence, not the static rendering/help prose we intend to omit.
    def read(_):
        return {
            "data": {
                "notes": "main notes evidence " * 1000,
                "notes_version": 7,
                "sub_notes": [
                    {"title": "Scorer caveat", "chars": 24, "excerpt": "Use corrected scorer v2"}
                ],
            }
        }

    cursor, delivered = None, []
    for _ in range(100):
        page = continuation.invoke(
            "entity",
            {"refs": ["run:synthetic"], "view": "notes", "token_budget": 512, "cursor": cursor},
            read,
            "tenant-a",
        )
        assert Budget(512).fits(page)
        delivered.append(page)
        cursor = page.get("next_cursor")
        if cursor is None:
            break
    else:
        pytest.fail("notes and companion caveats failed to finish")
    evidence = json.dumps(delivered, ensure_ascii=False)
    assert "Scorer caveat" in evidence
    assert "Use corrected scorer v2" in evidence


@pytest.mark.parametrize("edit", ["replace", "delete"])
def test_authored_text_edits_require_restart_instead_of_splicing_versions(edit):
    current = "original evidence 🌍 " * 1000
    args = {"refs": ["run:synthetic"], "view": "notes", "token_budget": 512}

    def read(_):
        return {"data": {"notes": current}}

    first = continuation.invoke("entity", args, read, "tenant-a")
    current = current[10:] if edit == "delete" else "X" + current[1:]
    with pytest.raises(continuation.ContinuationError, match="source_changed"):
        continuation.invoke("entity", {**args, "cursor": first["next_cursor"]}, read, "tenant-a")


def test_json_reordering_and_timestamp_refresh_survive_but_scientific_edits_do_not():
    value = {"data": {"notes": "evidence " * 2000, "score": 0.5}, "as_of": "first"}
    args = {"refs": ["run:synthetic"], "view": "record", "token_budget": 512}

    def read(_):
        return value

    first = continuation.invoke("entity", args, read, "tenant-a")
    value = {"as_of": "second", "data": {"score": 0.5, "notes": "evidence " * 2000}}
    continuation.invoke("entity", {**args, "cursor": first["next_cursor"]}, read, "tenant-a")
    value["data"]["score"] = 0.75
    with pytest.raises(continuation.ContinuationError, match="source_changed"):
        continuation.invoke("entity", {**args, "cursor": first["next_cursor"]}, read, "tenant-a")


def test_a_fragment_walk_finishes_its_source_page_before_advancing_the_native_cursor():
    first_source = {
        "data": {"evidence": "first source page evidence 🌍 " * 1000},
        "next_cursor": "native-page-two",
    }
    last_source = {"data": {"evidence": "second source page"}, "next_cursor": None}
    seen, fragments = [], []

    def read(args):
        seen.append(args["cursor"])
        assert args["cursor"] in (None, "native-page-two")
        return first_source if args["cursor"] is None else last_source

    args = {"query": "synthetic", "token_budget": 512}
    cursor, finished_first = None, False
    for _ in range(100):
        page = continuation.invoke("search_knowledge", {**args, "cursor": cursor}, read, "tenant-a")
        assert Budget(512).fits(page)
        if page["data"].get("format") == "json_fragment":
            assert not finished_first
            assert seen[-1] is None
            fragments.append(page["data"]["text"])
            finished_first = page["data"]["complete"]
        else:
            assert finished_first
            assert page == {"data": last_source["data"]}  # null next_cursor omitted
        cursor = page.get("next_cursor")
        if cursor is None:
            break
    else:
        pytest.fail("native-page continuation did not finish")
    assert json.loads("".join(fragments)) == first_source
    assert seen.count("native-page-two") == 1


def test_budget_can_change_mid_walk_without_restarting_or_skipping_content():
    source = {"data": {"evidence": "a synthetic finding 🌍 " * 2000}}
    args = {"refs": ["run:synthetic"], "view": "record"}

    def read(_):
        return source

    first = continuation.invoke("entity", {**args, "token_budget": 512}, read, "tenant-a")
    text, cursor = first["data"]["text"], first["next_cursor"]
    for _ in range(10):
        page = continuation.invoke(
            "entity", {**args, "token_budget": 8000, "cursor": cursor}, read, "tenant-a"
        )
        assert page["data"]["offset"] == len(text)
        assert Budget(8000).fits(page)
        text += page["data"]["text"]
        cursor = page.get("next_cursor")
        if cursor is None:
            break
    else:
        pytest.fail("larger budget did not finish the original walk")
    assert json.loads(text) == source


@pytest.mark.parametrize("change", ["scope", "tool", "view", "refs", "filter"])
def test_continuations_are_bound_before_a_cross_scope_or_changed_read(change):
    args = {
        "refs": ["run:one"],
        "view": "record",
        "filters": {"status": "completed"},
        "token_budget": 512,
    }

    def source(_):
        return {"data": {"notes": "synthetic evidence " * 2000}}

    first = continuation.invoke("entity", args, source, "tenant-a")
    changed, tool, scope = dict(args), "entity", "tenant-a"
    if change == "scope":
        scope = "tenant-b"
    elif change == "tool":
        tool = "search_knowledge"
    elif change == "view":
        changed["view"] = "notes"
    elif change == "refs":
        changed["refs"] = ["run:two"]
    else:
        changed["filters"] = {"status": "running"}

    def must_not_read(_):
        pytest.fail("mismatched cursor reached the source")

    with pytest.raises(continuation.ContinuationError):
        continuation.invoke(tool, {**changed, "cursor": first["next_cursor"]}, must_not_read, scope)


def test_mixed_batch_preserves_success_failure_and_never_refetches_completed_refs():
    refs = ["run:small", "run:large", "run:missing", "run:last"]
    large = {"data": {"notes": "synthetic long run evidence 🌍 " * 1000}}
    calls, done, seen = Counter(), set(), []

    def read(args):
        ref = args["refs"][0]
        assert ref not in done, "completed batch entry was fetched again"
        calls[ref] += 1
        if ref == "run:large":
            return large
        if ref == "run:missing":
            return {"rows": [], "missing": [{"ref": ref, "reason": "not_found"}]}
        return {"data": {"ref": ref, "status": "completed"}}

    cursor, chunks = None, []
    for _ in range(100):
        page = continuation.invoke(
            "entity",
            {"refs": refs, "view": "record", "token_budget": 512, "cursor": cursor},
            read,
            "tenant-a",
        )
        assert Budget(512).fits(page)
        for row in page["rows"]:
            ref = row["ref"]
            if ref == "run:large":
                # A row's verdict and cursor sit on the row; the cursor is the batch's.
                assert row.get("next_cursor") in (None, page.get("next_cursor"))
                fragment = row["data"]
                if not fragment["complete"]:
                    assert row["completeness"]["state"] == "partial"
                    assert "truncated_by_token_budget" in row["completeness"]["missing"]
                assert fragment["format"] == "json_fragment"
                chunks.append(fragment["text"])
                if fragment["complete"]:
                    done.add(ref)
                    seen.append(ref)
            else:
                done.add(ref)
                seen.append(ref)
        for missing in page.get("missing", []):
            assert missing == {"ref": "run:missing", "reason": "not_found"}
            done.add(missing["ref"])
            seen.append(missing["ref"])
        cursor = page.get("next_cursor")
        if cursor is None:
            break
    else:
        pytest.fail("mixed batch did not finish")
    assert Counter(seen) == Counter(refs)
    assert [ref for ref in seen if ref != "run:missing"] == [
        ref for ref in refs if ref != "run:missing"
    ]
    assert json.loads("".join(chunks)) == large
    assert calls["run:small"] == 1


def test_oversized_per_item_error_stays_a_failure_and_all_batch_refs_remain_reachable():
    class MixedService(_Service):
        def get_entity(self, ref, *args, **kwargs):
            self.calls.append(ref)
            if ref == "run:missing":
                raise ValueError("source unavailable " * 10000)
            return {"data": {"ref": ref, "status": "completed"}}

    service = MixedService()
    result = _wire(service, "entity", {"refs": ["run:missing", "run:ok"], "token_budget": 512})
    first = _bounded(result)
    assert first["missing"] and first["missing"][0]["ref"] == "run:missing"
    assert all(row["ref"] != "run:missing" for row in first["rows"])
    if not any(row["ref"] == "run:ok" for row in first["rows"]):
        assert first["next_cursor"], "remaining success became unreachable behind an error"
        following = _wire(
            service,
            "entity",
            {
                "refs": ["run:missing", "run:ok"],
                "token_budget": 512,
                "cursor": first["next_cursor"],
            },
        )
        next_page = _bounded(following)
        assert [row["ref"] for row in next_page["rows"]] == ["run:ok"]
        assert "next_cursor" not in next_page
    assert service.calls.count("run:missing") == 1


def test_huge_exception_and_validation_errors_are_bounded_on_the_actual_wire():
    result = _wire(
        _Service(error=ValueError("upstream unavailable 🌍 " * 10000)),
        "search_knowledge",
        {"query": "synthetic", "token_budget": 512},
    )
    assert _bounded(result, error=True)
    result = _wire(
        _Service(),
        "search_knowledge",
        {"query": "synthetic", "search_in": ["invalid " * 10000], "token_budget": 512},
    )
    assert _bounded(result, error=True)


def test_oversized_or_malformed_cursor_is_rejected_without_a_source_read():
    args = {"refs": ["run:synthetic"], "view": "record", "token_budget": 512}
    bomb = continuation.PREFIX + base64.urlsafe_b64encode(zlib.compress(b"x" * 20000)).decode()

    def must_not_read(_):
        pytest.fail("invalid continuation reached the source")

    for cursor in (continuation.PREFIX + "x" * 5000, bomb, continuation.PREFIX + "!invalid"):
        with pytest.raises(continuation.ContinuationError):
            continuation.invoke("entity", {**args, "cursor": cursor}, must_not_read, "tenant-a")


def test_health_reports_an_unavailable_reference_tokenizer(monkeypatch):
    import probe.mcp.server as server_module
    from probe.mcp.budget import TokenizerUnavailable

    def unavailable(_):
        raise TokenizerUnavailable("broken assets")

    async def inner(*_):
        pytest.fail("health must not enter the MCP/auth path")

    async def check():
        app = server_module.with_auth_and_health(inner)
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://mcp.test"
        ) as client:
            healthy = await client.get("/healthz")
            assert healthy.status_code == 200
            monkeypatch.setattr(server_module, "count_tokens", unavailable)
            failed = await client.get("/healthz")
            assert failed.status_code == 503
            assert failed.json() == {"error": "mcp_tokenizer_unavailable"}

    asyncio.run(check())


@pytest.mark.parametrize("failure", [False, True])
def test_delivery_measurements_match_actual_text_and_never_capture_it(monkeypatch, failure):
    from probe.mcp import accounting

    measurements = []
    monkeypatch.setattr(accounting, "note_delivery", lambda **counts: measurements.append(counts))
    service = _Service(
        {"data": {"evidence": "synthetic measurement " * 1000}},
        error=ValueError("synthetic upstream error " * 1000) if failure else None,
    )
    result = _wire(service, "search_knowledge", {"query": "synthetic", "token_budget": 512})
    _bounded(result, error=failure)
    text = result["content"][0]["text"]
    assert measurements[-1]["reference_tokens"] == count_tokens(text)
    assert measurements[-1]["response_text_bytes"] == len(text.encode("utf-8"))
    assert measurements[-1]["token_budget"] == 512
    assert measurements[-1]["has_continuation"] is not failure
    assert not any(isinstance(value, str) and text in value for value in measurements[-1].values())


@pytest.mark.parametrize("payload", [
    {"data": {"notes": "source_changed: is an example, not an error"}},
    {"missing": [{"reason": "User content says source_changed: restart"}]},
    {"data": {"missing": [{"reason": "source_changed: arbitrary record content"}]}},
])
def test_content_cannot_impersonate_a_stale_read_measurement(monkeypatch, payload):
    from probe.mcp import accounting

    measurements = []
    monkeypatch.setattr(accounting, "note_delivery", lambda **counts: measurements.append(counts))
    _bounded(_wire(_Service(payload), "entity", {"refs": ["run:one"], "token_budget": 512}))
    assert measurements[-1]["stale_reason"] is None


def test_a_complete_batch_carries_no_default_valued_bookkeeping_on_the_wire():
    """Every row of an entity batch used to repeat `completeness: complete/[]`
    and `next_cursor: null`, and the batch added `missing: []` -- ~30 tokens per
    row that only said "this is all of it". Absence says that for free."""
    result = _wire(_Service(), "entity", {"refs": ["run:a", "run:b"], "token_budget": 512})
    assert _bounded(result) == {
        "rows": [
            {"ref": "run:a", "data": _SMALL["data"]},
            {"ref": "run:b", "data": _SMALL["data"]},
        ]
    }


def test_a_partial_answer_keeps_its_completeness_and_cursor_on_the_wire():
    partial = {
        "data": {"ref": "run:synthetic"},
        "completeness": {"state": "partial", "missing": ["semantic_search"]},
        "next_cursor": "native-page-two",
    }
    page = _bounded(_wire(_Service(partial), "search_knowledge", {"query": "q"}))
    assert page["data"] == partial["data"]
    assert page["completeness"] == partial["completeness"]
    assert page["next_cursor"]  # a delivery cursor wrapping the native one


def test_verbose_batch_keeps_every_default_valued_key_on_the_wire():
    result = _wire(
        _Service(), "entity", {"refs": ["run:a", "run:b"], "token_budget": 512, "verbose": True}
    )
    page = _bounded(result)
    assert page["missing"] == [] and page["next_cursor"] is None
    # Verbose keeps each row's whole envelope ON the row, null cursor included.
    assert [row["ref"] for row in page["rows"]] == ["run:a", "run:b"]
    assert all({k: v for k, v in row.items() if k != "ref"} == _SMALL for row in page["rows"])


@pytest.mark.parametrize(
    "envelope, kept",
    [
        ({"data": 1, "completeness": {"state": "complete", "missing": []}, "next_cursor": None}, {"data"}),
        ({"data": 1, "completeness": {"state": "no_match", "missing": []}}, {"data", "completeness"}),
        ({"data": 1, "completeness": {"state": "complete", "missing": ["m"]}}, {"data", "completeness"}),
        # A block with more than state/missing (a reproduce-style rollup) is not the default.
        ({"data": 1, "completeness": {"state": "complete", "missing": [], "advisories": ["a"]}}, {"data", "completeness"}),
        ({"rows": [], "missing": [{"ref": "r", "reason": "x"}], "next_cursor": "c"}, {"rows", "missing", "next_cursor"}),
        ({"rows": [], "missing": [], "next_cursor": None}, {"rows"}),
        ({"data": 1, "evidence": [], "next_cursor": ""}, {"data"}),
    ],
)
def test_omit_defaults_drops_only_default_valued_envelope_keys(envelope, kept):
    assert set(continuation.omit_defaults(envelope)) == kept


def test_omit_defaults_never_reaches_inside_data():
    inner = {"completeness": {"state": "complete", "missing": []}, "next_cursor": None}
    assert continuation.omit_defaults({"data": inner})["data"] == inner


def test_a_batch_row_sits_beside_its_ref_with_its_own_verdict():
    """The answer is `rows[i].data`, never `rows[i].data.data`; a partial row says
    so on the row. Partial for a DATA GAP is not "cut here": such a row keeps its
    cursor, the only thing saying the top-level cursor continues it, not the next ref."""
    partial = {"state": "partial", "missing": ["upstream_metric_gap"]}

    class PartialService(_Service):
        def get_entity(self, ref, view, token_budget, cursor, *args, **kwargs):
            self.calls.append((ref, cursor))
            if ref == "run:b" and cursor is None:
                return {"data": {"ref": ref}, "completeness": partial, "next_cursor": "native-2"}
            return {"data": {"ref": ref, "page": cursor}}

    service = PartialService()
    args = {"refs": ["run:a", "run:b"], "token_budget": 512}
    page = _bounded(_wire(service, "entity", args))
    assert page["rows"][0] == {"ref": "run:a", "data": {"ref": "run:a", "page": None}}
    row = page["rows"][1]
    assert row["data"] == {"ref": "run:b"} and row["completeness"] == partial
    assert row["next_cursor"] == page["next_cursor"]
    verbose = _bounded(_wire(service, "entity", {**args, "verbose": True}))
    assert verbose["rows"][1]["next_cursor"] == verbose["next_cursor"]
    # The one cursor resumes run:b at its own next page and never re-reads run:a.
    service.calls.clear()
    following = _bounded(_wire(service, "entity", {**args, "cursor": page["next_cursor"]}))
    assert service.calls == [("run:b", "native-2")]
    assert following == {"rows": [{"ref": "run:b", "data": {"ref": "run:b", "page": "native-2"}}]}


def test_a_row_that_ends_at_its_window_still_says_it_has_more():
    """`complete` + a cursor (the view hit its fetch window, not the budget): the
    compact envelope drops the complete block, so the row's cursor is its only
    sign of being a slice -- it must survive on the row."""

    class WindowService(_Service):
        def get_entity(self, ref, view, token_budget, cursor, *args, **kwargs):
            self.calls.append((ref, cursor))
            if ref == "run:b" and cursor is None:
                return {"data": {"spans": [0, 1, 2]}, "next_cursor": "native-2"}
            return {"data": {"spans": [3, 4] if ref == "run:b" else []}}

    page = _bounded(_wire(WindowService(), "entity", {"refs": ["run:a", "run:b"], "token_budget": 512}))
    last = page["rows"][-1]
    assert last["ref"] == "run:b" and "completeness" not in last
    assert last["next_cursor"] and last["next_cursor"] == page["next_cursor"]


@pytest.mark.parametrize("verbose", [False, True])
def test_a_two_ref_notes_batch_reads_at_the_minimum_budget(verbose):
    """At token_budget=512 a batch fragment page carried its ~200-token cursor twice
    (row + top level) beside the first page's context, which left no room for one
    character of the note: "Request metadata exceeds this budget". A row cut for
    size no longer repeats the batch's cursor. Payload sized like a live notes read."""
    ids = {
        "project:one": "9e016e67-3bf7-4671-8cbf-a0b710716fb4",
        "project:two": "f7d1e12f-0363-4586-aaf2-07f4a77b417f",
    }
    notes = {ref: f"{ref} " + "word " * 620 for ref in ids}
    _walk_pinned_notes_batch(ids, notes, verbose=verbose)


@pytest.mark.parametrize("first_words", [150, 200, 240, 280, 320, 360])
def test_a_short_note_then_a_long_one_starts_at_the_minimum_budget(first_words):
    """When the second ref does not fit beside the first, the page sent must be the
    one MEASURED. It used to be rebuilt with the unread ref's snapshot in its
    cursor (~160 tokens, not ~40): 514-630 tokens against a 512 cap, refused at
    the boundary, and the same page again on every retry."""
    ids = {
        "project:one": "9e016e67-3bf7-4671-8cbf-a0b710716fb4",
        "project:two": "f7d1e12f-0363-4586-aaf2-07f4a77b417f",
    }
    notes = {"project:one": "word " * first_words, "project:two": "word " * 620}
    _walk_pinned_notes_batch(ids, notes, verbose=False)


def _walk_pinned_notes_batch(ids, notes, *, verbose):
    from probe.mcp.delivery_context import pin_document

    class NotesService(_Service):
        def get_entity(self, ref, *args, **kwargs):
            self.calls.append(ref)
            # Pinned like the real notes view: the snapshot rides in the cursor,
            # which is what made the cursor long enough to matter.
            body = pin_document(notes[ref], f"notes:project:{ids[ref]}", version=5)
            return {
                "data": {
                    "entity_type": "project",
                    "entity": {"id": ids[ref], "slug": "s" * 19, "name": "n" * 40, "kind": "training"},
                    "view": "notes",
                    "notes": body,
                    "notes_version": 5,
                    "notes_advisory": "a" * 124,
                },
                "completeness": {"state": "partial", "missing": ["token_budget_exceeded"]},
            }

    args = {"refs": list(notes), "view": "notes", "token_budget": 512, "verbose": verbose}
    service, cursor, joined = NotesService(), None, {}
    for _ in range(100):
        page = _bounded(_wire(service, "entity", {**args, "cursor": cursor}))
        for row in page["rows"]:
            if "truncated_by_token_budget" in row.get("completeness", {}).get("missing", []):
                assert "next_cursor" not in row  # the batch's cursor is the one
            data = row["data"]
            if data.get("format") == "text_fragment":
                joined[row["ref"]] = joined.get(row["ref"], "") + data["text"]
            else:
                joined[row["ref"]] = data["notes"]
        cursor = page.get("next_cursor")
        if cursor is None:
            break
    else:
        pytest.fail("batch did not finish")
    assert joined == notes
