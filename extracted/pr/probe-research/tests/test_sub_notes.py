"""Titled sub-notes (0146) through the SDK, the outbox, and the MCP view.

The load-bearing claims: the title travels IN the write (so a queued write
survives the outbox — review 13A), refusals raise instead of queueing (the
`_write_notes` rule applied to the new door), and the MCP notes view surfaces
sub-notes as bounded excerpts, never a context bomb.
"""

from __future__ import annotations

import pytest

from probe.sdk import errors
from conftest import make_client


def test_create_list_and_title_append_roundtrip(client, app):
    exp = app.seed_experiment("e")["id"]
    created = client._create_sub_note("experiment", exp, "Caveats", "first")
    assert created["title"] == "Caveats"
    assert "body" not in created  # write responses never carry the document

    client._replace_sub_note_by_title("experiment", exp, "Caveats", "second")
    page = client.list_sub_notes("experiment", exp)
    assert [row["title"] for row in page["sub_notes"]] == ["Caveats"]
    note_id = page["sub_notes"][0]["id"]
    # The gated GET is where the document lives — with the blank-line separator.
    # A replace REPLACES -- concatenation was the append's property.
    assert client.get_sub_note(note_id)["body"] == "second"


def test_a_title_write_is_sent_even_under_async_writes(app, tmp_path):
    """Inverted, and the inversion is the point.

    A title-addressed APPEND could be journaled: the title travelled in the write
    and the server resolved it at apply time, so a replayed write still landed on
    the right document. A REPLACE cannot work that way -- it carries a
    base_version that will have moved by the time a queue drains, so it would
    dead-letter after the caller was told it shipped. Every notes write is
    synchronous now.
    """
    queued = make_client(app, tmp_spool=tmp_path / "spool", async_writes=True)
    exp = app.seed_experiment("e")["id"]
    make_client(app)._create_sub_note("experiment", exp, "Caveats", "seeded")

    assert queued._replace_sub_note_by_title("experiment", exp, "Caveats", "later") is not None
    assert not queued.journal.pending()  # sync: on the server, never the outbox


def test_refusals_raise_and_never_queue(client, app, tmp_path):
    """A refusal replayed later is the same no — the `_write_notes` rule."""
    exp = app.seed_experiment("e")["id"]
    client._create_sub_note("experiment", exp, "Ideas", "x")
    client._create_sub_note("experiment", exp, "Ideas", "y")

    # Ambiguous title: 409, raised, nothing journaled.
    with pytest.raises(errors.RosError):
        client._replace_sub_note_by_title("experiment", exp, "Ideas", "which one?")
    # Missing title: 404 listing what exists, raised.
    with pytest.raises(errors.RosError):
        client._replace_sub_note_by_title("experiment", exp, "Cavets", "typo")
    # A STALE PRECONDITION: 409, raised. This replaces "an edit whose span is
    # absent" -- the span edit is gone, and a stale base_version is the refusal
    # a replace can actually hit.
    client._create_sub_note("experiment", exp, "Solo", "prose here")
    with pytest.raises(errors.RosError):
        client._replace_sub_note_by_title("experiment", exp, "Solo", "x", base_version=999)
    assert client.journal.pending() == []
    assert client.journal.failed() == []


def test_rename_and_delete_by_id(client, app):
    exp = app.seed_experiment("e")["id"]
    client._create_sub_note("experiment", exp, "old", "body")
    note_id = client.list_sub_notes("experiment", exp)["sub_notes"][0]["id"]

    client._rename_sub_note(note_id, "new")
    assert client.list_sub_notes("experiment", exp)["sub_notes"][0]["title"] == "new"

    client._delete_sub_note(note_id)
    assert client.list_sub_notes("experiment", exp)["sub_notes"] == []


# -- MCP ----------------------------------------------------------------------


def _service(client):
    from probe.mcp.service import ResearchReadService
    from probe.mcp.source import ResearchOSSource

    return ResearchReadService(ResearchOSSource(client))


def test_the_notes_view_carries_sub_note_excerpts(client, app):
    exp = app.seed_experiment("e")["id"]
    client._create_sub_note("experiment", exp, "Caveats", "the dataloader was stale")
    client._create_sub_note("experiment", exp, "Long", "x" * 2_000)

    view = _service(client).get_entity(f"experiment:{exp}", view="notes")

    section = view["data"]["sub_notes"]
    assert [item["title"] for item in section] == ["Caveats", "Long"]
    assert section[0]["excerpt"] == "the dataloader was stale"
    assert "truncated" not in section[0]
    # The long one is CLIPPED with a pointer, never shipped whole.
    assert section[1]["truncated"] is True
    assert len(section[1]["excerpt"]) < 2_000
    assert "read_all" in section[1]


def test_an_entity_without_sub_notes_has_no_sub_notes_key(client, app):
    """Absent, never empty: a `sub_notes` key with nothing in it reads as
    "this entity has sub-notes" — same rule as the card's notes excerpt."""
    exp = app.seed_experiment("e")["id"]
    view = _service(client).get_entity(f"experiment:{exp}", view="notes")
    assert "sub_notes" not in view["data"]


def test_cards_stay_untouched(client, app):
    """No titles line on cards — that would be an N+1 on the cheapest read."""
    exp = app.seed_experiment("e")["id"]
    client._create_sub_note("experiment", exp, "Caveats", "text")
    card = _service(client).get_entity(f"experiment:{exp}")
    assert "sub_notes" not in card["data"]

def test_create_refusals_raise_and_never_queue(client, app):
    """The cap 422 and the blank-title 422 are answers, not retryable events."""
    exp = app.seed_experiment("e")["id"]
    for i in range(20):
        client._create_sub_note("experiment", exp, f"tab {i}")

    with pytest.raises(errors.RosError, match="delete one before creating another"):
        client._create_sub_note("experiment", exp, "one more")
    with pytest.raises(errors.RosError, match="must not be blank"):
        client._create_sub_note("experiment", exp, "   ")
    assert client.journal.pending() == []
    assert client.journal.failed() == []
    assert len(client.list_sub_notes("experiment", exp)["sub_notes"]) == 20


def test_a_transient_failure_on_create_raises_instead_of_queueing(app, tmp_path, monkeypatch):
    """STRICT by design: titles are non-unique, so a create whose response was
    lost and then replayed is a SECOND tab that makes every title-addressed
    write ambiguous — the opposite of a retry."""
    c = make_client(app, tmp_spool=tmp_path / "spool")
    exp = app.seed_experiment("e")["id"]

    def unreachable(*_a, **_kw):
        raise errors.TransportError("POST: connection refused")

    monkeypatch.setattr(c.transport, "request", unreachable)
    with pytest.raises(errors.TransportError):
        c._create_sub_note("experiment", exp, "Caveats", "seeded")
    assert c.journal.pending() == []


def test_a_strict_replace_lands_and_bumps_the_version(client, app):
    exp = app.seed_experiment("e")["id"]
    client._create_sub_note("experiment", exp, "Solo", "alpha HEAD beta")

    client._replace_sub_note_by_title("experiment", exp, "Solo", "TAIL")

    row = client.list_sub_notes("experiment", exp)["sub_notes"][0]
    # A replace REPLACES the whole body.
    assert client.get_sub_note(row["id"])["body"] == "TAIL"
    assert row["notes_version"] == 2


def test_by_id_writes_reach_exactly_one_duplicate(client, app):
    """The duplicated-title escape hatch: `id:` addressing works where every
    title-addressed write is refused as ambiguous."""
    exp = app.seed_experiment("e")["id"]
    client._create_sub_note("experiment", exp, "Ideas", "first doc")
    client._create_sub_note("experiment", exp, "Ideas", "second doc")
    first_id = client.list_sub_notes("experiment", exp)["sub_notes"][0]["id"]

    client._replace_sub_note(first_id, "more", base_version=None, op_key="t")
    client._replace_sub_note(first_id, "1st", base_version=None, op_key="t")

    bodies = [
        client.get_sub_note(r["id"])["body"]
        for r in client.list_sub_notes("experiment", exp)["sub_notes"]
    ]
    # The by-id door still reaches exactly ONE of two duplicate titles;
    # what changed is that it replaces rather than appends.
    assert bodies == ["1st", "second doc"]


def _notes_entity(kind: str, client, app) -> str:
    if kind == "experiment":
        return app.seed_experiment("e")["id"]
    if kind == "project":
        return client.create_project("p1", kind="general")["id"]
    if kind == "group":
        exp = app.seed_experiment("e")
        return client.create_group(exp["id"], "g")["id"]
    project_id = client.create_project("p1", kind="general")["id"]
    app.seed_experiment("e", project_id=project_id)
    return client.run(project="p1", experiment="e", name="r1").id


@pytest.mark.parametrize("kind", ["project", "experiment", "run", "group"])
def test_every_notes_view_kind_carries_sub_note_excerpts(kind, client, app):
    """All four per-kind notes views route through the shared implementation —
    pinned per kind, because a typo'd kind string in any one of them would
    render as 'no sub-notes' and stay green."""
    entity_id = _notes_entity(kind, client, app)
    client._create_sub_note(kind, entity_id, "Caveats", "the dataloader was stale")

    view = _service(client).get_entity(f"{kind}:{entity_id}", view="notes")

    section = view["data"]["sub_notes"]
    assert [item["title"] for item in section] == ["Caveats"]
    assert section[0]["excerpt"] == "the dataloader was stale"


def test_a_failed_body_read_says_unavailable_not_empty(client, app, monkeypatch):
    """An outage on one document read must not render as 'this tab is blank' —
    that is a conclusion, and only the body can draw it."""
    exp = app.seed_experiment("e")["id"]
    client._create_sub_note("experiment", exp, "Caveats", "real content")

    def broken(_sub_note_id):
        raise errors.RosError("boom")

    monkeypatch.setattr(client, "get_sub_note", broken)
    view = _service(client).get_entity(f"experiment:{exp}", view="notes")

    (item,) = view["data"]["sub_notes"]
    assert item["unavailable"] is True
    assert "excerpt" not in item


# The transient-failure QUEUE tests that stood here are gone by design. They
# pinned that a failed sub-note write is journaled and replayed; a replace
# carries a `base_version` that will have moved by the time a queue drains, so
# replaying it would dead-letter after the caller was told it shipped. Every
# notes write is synchronous now and a failure RAISES -- see
# `probe notes push`, which keeps the file and its base on disk so the retry is
# the same command again.
