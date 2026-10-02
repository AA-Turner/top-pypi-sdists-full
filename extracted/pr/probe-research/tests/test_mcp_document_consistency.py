"""Document snapshots survive native pages, appends, edits and saved versions."""

from __future__ import annotations

import asyncio
import json
from copy import deepcopy
from types import SimpleNamespace

import pytest

from probe.mcp import delivery_context as delivery
from probe.mcp.delivery_context import current_delivery, delivery_context, pin_document
from probe.mcp.service import ResearchReadService
from probe.mcp.source import ResearchOSSource
from probe.sdk import errors
from tests.test_mcp_session_views import _SID, _seed


def _transcript_page(client, *, snapshot=None, cursor=None, filters=None):
    # Reconstruct state like another worker receiving a stateless cursor.
    hint = json.loads(json.dumps(snapshot)) if snapshot else None
    with delivery_context(hint) as context:
        result = ResearchReadService(ResearchOSSource(client)).get_entity(
            f"session:{_SID}",
            view="transcript",
            token_budget=600,
            cursor=cursor,
            filters=filters,
        )
    return result, context.snapshot


@pytest.mark.parametrize("grep", [False, True])
def test_native_transcript_walk_pins_original_end_across_every_page(client, app, grep):
    _seed(app, agent="codex", lines=400)
    doc = app.session_transcripts[(_SID, "codex")]
    original = doc["content"]
    filters = {"grep": "line", "context_lines": 0} if grep else None
    first, snapshot = _transcript_page(client, filters=filters)
    assert snapshot["end"] == len(original)
    assert snapshot["source"] == f"transcript:{_SID}:codex"
    assert len(json.dumps(snapshot)) < 250
    sections = list(first["data"]["sections"])
    cursor = first["next_cursor"]
    pages = 0
    while cursor:
        pages += 1
        assert pages < 100
        doc["content"] += f"\nline appended {pages}: must not join this read"
        doc["body_size_bytes"] = len(doc["content"].encode())
        page, observed = _transcript_page(
            client,
            snapshot=snapshot,
            cursor=cursor,
            filters=filters,
        )
        assert observed == snapshot
        assert page["data"]["total_lines"] == 400
        assert page["data"]["body_size_bytes"] == len(original.encode())
        sections.extend(page["data"]["sections"])
        cursor = page.get("next_cursor")
    assert pages > 1  # native pages, not just a fragmented first page
    assert "\n".join(row["text"] for row in sections) == original


@pytest.mark.parametrize("change", ["edit_seen", "edit_unseen", "truncate", "delete"])
def test_native_transcript_resume_rejects_edits_and_deletion(client, app, change):
    _seed(app, lines=400)
    first, snapshot = _transcript_page(client)
    assert first["next_cursor"]
    doc = app.session_transcripts[(_SID, "claude_code")]
    if change == "edit_seen":
        doc["content"] = doc["content"].replace("line 1:", "edit 1:", 1)
    elif change == "edit_unseen":
        doc["content"] = doc["content"].replace("line 400:", "edit 400:", 1)
    elif change == "truncate":
        doc["content"] = doc["content"][:-1]
    else:
        del app.session_transcripts[(_SID, "claude_code")]
    with pytest.raises(errors.ValidationError, match="source_changed") as exc:
        _transcript_page(client, snapshot=snapshot, cursor=first["next_cursor"])
    assert exc.value.status == 409


def test_transcript_resume_keeps_the_original_agent_when_work_metadata_changes(client, app):
    _seed(app, agent="codex", lines=400)
    first, snapshot = _transcript_page(client)
    app.session_work[_SID]["agent"] = "pi"
    app.session_transcripts[(_SID, "pi")] = {"agent": "pi", "content": "different document"}
    page, observed = _transcript_page(client, snapshot=snapshot, cursor=first["next_cursor"])
    assert page["data"]["agent"] == "codex"
    assert observed == snapshot
    del app.session_transcripts[(_SID, "codex")]
    with pytest.raises(errors.ValidationError, match="source_changed"):
        _transcript_page(client, snapshot=snapshot, cursor=first["next_cursor"])


def test_prefix_offsets_preserve_unicode_and_a_partial_last_line(client, app):
    _seed(app, lines=120)
    doc = app.session_transcripts[(_SID, "claude_code")]
    doc["content"] += "\n🙂\r\u2028partial"
    original = doc["content"]
    page, snapshot = _transcript_page(client)
    sections = list(page["data"]["sections"])
    doc["content"] += " continuation\nnew line"
    while page.get("next_cursor"):
        page, _ = _transcript_page(client, snapshot=snapshot, cursor=page["next_cursor"])
        sections.extend(page["data"]["sections"])
    assert "\n".join(row["text"] for row in sections) == original


class NoteClient:
    def __init__(self, *, version=True):
        self.entity = {"id": "p1", "name": "Pinned notes", "notes": "Original caveat.\n" * 100}
        if version:
            self.entity["notes_version"] = 7
        self.saved = {7: self.entity["notes"]}
        self.reads = []
        self.transport = SimpleNamespace(get=self.read_version)

    def _unexpected_read(self, *_):
        pytest.fail("unrelated entity lookup")

    get_run = get_experiment = get_group = get_trial = _unexpected_read

    def get_project(self, ref):
        self.reads.append(("project", ref))
        return deepcopy(self.entity)

    def list_sub_notes(self, *_):
        self.reads.append(("sub_notes",))
        return {"sub_notes": []}

    def me(self):
        return {"customer_id": "synthetic"}

    def read_version(self, path):
        self.reads.append(("version", path))
        assert path == "/v1/projects/p1/notes/versions/7"
        if 7 not in self.saved:
            raise errors.NotFoundError("version not found")
        return {"version": 7, "body": self.saved[7]}


def _notes_page(client, snapshot=None, *, view="notes"):
    with delivery_context(snapshot) as context:
        result = ResearchReadService(ResearchOSSource(client)).get_entity("project:p1", view=view)
    return result, context.snapshot


def test_saved_notes_version_is_reused_after_the_head_is_rewritten():
    client = NoteClient()
    first, snapshot = _notes_page(client)
    assert snapshot["version"] == 7
    assert not any(read[0] == "version" for read in client.reads)
    client.entity.update(notes="A completely rewritten head", notes_version=8)
    second, observed = _notes_page(client, snapshot)
    assert second["data"]["notes"] == first["data"]["notes"]
    assert second["data"]["notes_version"] == 7
    assert observed == snapshot
    assert [read for read in client.reads if read[0] == "version"] == [
        ("version", "/v1/projects/p1/notes/versions/7")
    ]
    client.saved.clear()
    with pytest.raises(errors.ValidationError, match="source_changed"):
        _notes_page(client, snapshot)


def test_notes_without_a_known_version_pin_the_prefix_without_history_calls():
    client = NoteClient(version=False)
    first, snapshot = _notes_page(client)
    assert "version" not in snapshot
    client.entity["notes"] += "An append after the first page"
    second, observed = _notes_page(client, snapshot)
    assert second["data"]["notes"] == first["data"]["notes"]
    assert observed == snapshot
    assert not any(read[0] == "version" for read in client.reads)
    client.entity["notes"] = "An edit at the beginning"
    with pytest.raises(errors.ValidationError, match="source_changed"):
        _notes_page(client, snapshot)


def test_normal_card_does_not_read_history_or_hash_notes(monkeypatch):
    client = NoteClient()
    monkeypatch.setattr(delivery.hashlib, "sha256", lambda *_: pytest.fail("card hashed notes"))
    card, snapshot = _notes_page(client, view="card")
    assert card["data"]["entity"]["name"] == "Pinned notes"
    assert snapshot is None
    assert client.reads == [("project", "p1")]


def test_team_note_resume_reads_the_saved_version_and_pruning_is_explicit(client, app):
    original = "Team briefing.\n" * 100
    app.team_note.update(body=original, version=4)
    app.team_note_versions.append({"body": original, "version": 4})
    service = ResearchReadService(ResearchOSSource(client))
    with delivery_context() as first:
        service.get_entity("team-note")
    app.team_note.update(body="Rewritten shared note", version=5)
    with delivery_context(first.snapshot) as second:
        page = service.get_entity("team-note:")
    assert page["data"]["entity"]["body"] == original
    assert page["data"]["entity"]["version"] == 4
    assert first.snapshot == second.snapshot
    app.team_note_versions.clear()
    with (
        delivery_context(first.snapshot),
        pytest.raises(errors.ValidationError, match="source_changed"),
    ):
        service.get_entity("team-note")


def test_context_disabled_does_not_hash_and_resets_after_exception(monkeypatch):
    monkeypatch.setattr(delivery.hashlib, "sha256", lambda *_: pytest.fail("hash outside MCP"))
    assert pin_document("outside", "one") == "outside"
    with pytest.raises(RuntimeError):
        with delivery_context():
            assert current_delivery() is not None
            raise RuntimeError("stop")
    assert current_delivery() is None


def test_concurrent_delivery_contexts_do_not_share_snapshot():
    async def one(name):
        with delivery_context() as state:
            pin_document(name, name)
            await asyncio.sleep(0)
            assert current_delivery() is state
            assert state.snapshot["source"] == name
        assert current_delivery() is None

    async def run():
        await asyncio.gather(one("a"), one("b"))

    asyncio.run(run())


@pytest.mark.parametrize(
    "change", [{"end": True}, {"version": "../7"}, {"sha256": "bad"}, {"private": "data"}]
)
def test_context_rejects_malformed_snapshot_before_source_reads(change):
    with delivery_context() as first:
        pin_document("body", "notes:project:p1")
    with pytest.raises(errors.ValidationError, match="Invalid document continuation"):
        with delivery_context({**first.snapshot, **change}):
            pytest.fail("invalid context entered")
