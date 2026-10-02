"""Actual service/source reads through the bounded MCP transport, with mutations."""

from __future__ import annotations

import json
from copy import deepcopy

import pytest

from probe.mcp.service import ResearchReadService
from probe.mcp.source import ResearchOSSource
from tests.test_mcp_delivery import _bounded, _wire
from tests.test_mcp_document_consistency import NoteClient
from tests.test_mcp_entity_projection import EntitySource
from tests.test_mcp_session_views import _SID, _seed


def _walk(service, arguments, *, after_page=None, next_budget=None):
    cursor, pending, delivered, pages = None, "", [], []
    for index in range(100):
        limit = (
            arguments.get("token_budget", 512) if not index or next_budget is None else next_budget
        )
        page = _bounded(
            _wire(service, "entity", {**arguments, "cursor": cursor, "token_budget": limit}), limit
        )
        pages.append(page)
        data = page.get("data", {})
        if data.get("format") in {"json_fragment", "text_fragment"}:
            assert data["offset"] == len(pending)
            pending += data["text"]
            if data["complete"]:
                delivered.append(
                    json.loads(pending) if data["format"] == "json_fragment" else pending
                )
                pending = ""
        else:
            assert not pending
            delivered.append(page)
        if after_page:
            after_page(index, page)
        cursor = page.get("next_cursor")
        if not cursor:
            assert not pending
            return delivered, pages
    pytest.fail("source continuation did not terminate")


@pytest.mark.parametrize("changed_budget", [False, True])
def test_real_transcript_source_pins_snapshot_across_fragments_and_native_pages(
    client, app, changed_budget
):
    _seed(app, agent="codex", lines=120)
    doc = app.session_transcripts[(_SID, "codex")]
    original = doc["content"]

    def append(_, page):
        doc["content"] += "\nAn append outside the original read"
        doc["body_size_bytes"] = len(doc["content"].encode())

    delivered, pages = _walk(
        ResearchReadService(ResearchOSSource(client)),
        {"refs": [f"session:{_SID}"], "view": "transcript", "token_budget": 512},
        after_page=append,
        next_budget=8000 if changed_budget else None,
    )
    assert pages[0]["data"]["format"] == "json_fragment"
    assert len(delivered) >= 2  # crossing a native cursor, not just first-page fragments
    sections = [section for page in delivered for section in page["data"]["sections"]]
    assert "\n".join(section["text"] for section in sections) == original
    assert all(page["data"]["total_lines"] == 120 for page in delivered)
    assert "completeness" not in pages[-1]


def test_real_transcript_source_mutation_is_explicit_at_the_mcp_boundary(client, app):
    _seed(app, lines=120)
    service = ResearchReadService(ResearchOSSource(client))
    args = {"refs": [f"session:{_SID}"], "view": "transcript", "token_budget": 512}
    first = _bounded(_wire(service, "entity", args))
    app.session_transcripts[(_SID, "claude_code")]["content"] = "edited original prefix"
    result = _bounded(
        _wire(service, "entity", {**args, "cursor": first["next_cursor"]}), error=True
    )
    assert "source_changed" in result
    assert "next_cursor" not in result


def test_native_document_staleness_records_only_a_closed_telemetry_reason(client, app, monkeypatch):
    from probe.mcp import accounting

    measurements = []
    monkeypatch.setattr(accounting, "note_delivery", lambda **counts: measurements.append(counts))
    _seed(app, lines=3000)
    service = ResearchReadService(ResearchOSSource(client))
    args = {"refs": [f"session:{_SID}"], "view": "transcript", "token_budget": 8000}
    first = _bounded(_wire(service, "entity", args), 8000)
    # Finish any wire fragments of the first source page. Its final cursor
    # advances to a native page with no fragment hash left to detect the edit.
    for _ in range(10):
        if "format" not in first["data"] or first["data"]["complete"]:
            break
        first = _bounded(_wire(service, "entity", {**args, "cursor": first["next_cursor"]}), 8000)
    else:
        pytest.fail("the first native source page never finished")
    assert first["next_cursor"]
    assert measurements[-1]["stale_reason"] is None

    app.session_transcripts[(_SID, "claude_code")]["content"] = "edited original prefix"
    failed = _bounded(_wire(service, "entity", {**args, "cursor": first["next_cursor"]}), 8000)
    assert failed["rows"] == []
    assert failed["missing"][0]["reason"].startswith("ValidationError: source_changed:")
    assert measurements[-1]["stale_reason"] == "source_changed"
    assert measurements[-1]["has_continuation"] is False


def test_atomic_record_finishes_complete_after_exact_fragment_reconstruction():
    entity = {"id": "one", "config": {"rank": 16, "large": "配置\n" * 1200}}
    service = ResearchReadService(EntitySource("run", entity))
    raw = service.get_entity("run:one", view="record", token_budget=512)
    assert "token_budget_exceeded" in raw["completeness"]["missing"]
    delivered, pages = _walk(service, {"refs": ["run:one"], "view": "record", "token_budget": 512})
    assert len(pages) > 1 and len(delivered) == 1
    assert delivered[0]["data"]["record"] == entity
    # Rejoined, it is the same answer a whole fit sends: complete, so no block.
    assert "completeness" not in delivered[0]
    assert "completeness" not in pages[-1]
    assert "token_budget_exceeded" not in json.dumps(pages)


def test_whole_fitting_batch_items_clear_legacy_atomic_overflow_marker():
    # Repeated ASCII has fewer reference tokens than the old chars/4 estimate.
    # The real service marks this atomic record oversized, but it fits on wire.
    entity = {"id": "one", "metadata": {"text": "x" * 2200}}
    service = ResearchReadService(EntitySource("run", entity))
    raw = service.get_entity("run:one", view="record", token_budget=512)
    assert "token_budget_exceeded" in raw["completeness"]["missing"]
    page = _bounded(
        _wire(
            service,
            "entity",
            {"refs": ["run:one", "run:two"], "view": "record", "token_budget": 512},
        )
    )
    assert page["rows"] and "format" not in page["rows"][0]["data"]
    assert "token_budget_exceeded" not in json.dumps(page)
    # _source_state cleared the only marker, so the row is complete: nothing to say.
    assert "completeness" not in page["rows"][0]


@pytest.mark.parametrize("long_first", [False, True])
def test_batch_changes_entity_without_reusing_the_previous_document_snapshot(long_first):
    class PairClient(NoteClient):
        def get_project(self, ref):
            self.reads.append(("project", ref))
            body = ("A" if ref == "one" else "B") * (2500 if (ref == "one") == long_first else 8)
            return {"id": ref, "name": ref, "notes": body}

    service = ResearchReadService(ResearchOSSource(PairClient(version=False)))
    cursor, pending, records = None, "", {}
    for _ in range(80):
        page = _bounded(
            _wire(
                service,
                "entity",
                {
                    "refs": ["project:one", "project:two"],
                    "view": "notes",
                    "token_budget": 512,
                    "cursor": cursor,
                },
            )
        )
        assert "missing" not in page
        for row in page["rows"]:
            data = row["data"]
            if data.get("format") == "text_fragment":
                assert data["offset"] == len(pending)
                pending += data["text"]
                if data["complete"]:
                    records[row["ref"]] = pending
                    pending = ""
            else:
                assert not pending
                records[row["ref"]] = data["notes"]
        cursor = page.get("next_cursor")
        if not cursor:
            break
    else:
        pytest.fail("batch did not terminate")
    assert records == {
        "project:one": "A" * (2500 if long_first else 8),
        "project:two": "B" * (8 if long_first else 2500),
    }


def test_metrics_native_points_cursor_advances_the_real_service_source():
    source = EntitySource("run", {"id": "one"})
    calls = []

    def points(run_id, *, after_id=None, **kwargs):
        calls.append(after_id)
        rows = [{"id": i, "step": i, "value": float(i)} for i in range(1, 4)]
        return iter(deepcopy([row for row in rows if after_id is None or row["id"] > after_id]))

    source.export_points = points
    service = ResearchReadService(source)
    arguments = {"run_id": "one", "mode": "points", "limit": 1, "token_budget": 512}
    first = _bounded(_wire(service, "metrics", arguments))
    assert first["data"]["points"][0]["id"] == 1 and first["next_cursor"]
    second = _bounded(_wire(service, "metrics", {**arguments, "cursor": first["next_cursor"]}))
    assert second["data"]["points"][0]["id"] == 2
    assert calls == [None, 1]
