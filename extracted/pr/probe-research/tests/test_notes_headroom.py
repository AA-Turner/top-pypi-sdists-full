"""The forward signal: how full a notes document is, BEFORE the cap refuses a write.

The cap itself has been enforced correctly and loudly since 0.105.2 -- an append
to a full document raises, exits 1, and queues nothing (test_project_notes.py
covers that, and it is the one thing NOT retested here). What was missing is
anything ahead of it. `anthrogen/assignment-modeling` sat at 99,992 of its then
100,000-character cap and was still being appended to that same day: every write
was being refused and nobody saw it, because a refusal is only visible to whoever
reads the exit code of the command that hit it.

So these tests are about the two things that come before the wall: the numbers
the server publishes on every notes write, and what a client does with them.

THE CAPS ARE TOKENS (research-os P2): 30,000 o200k_base tokens for a document,
2,000 for a run note, each with a looser CHARACTER backstop (150,000 / 10,000)
the `*_chars` fields now measure. Every over-cap body here is built with
`token_text(n)`, whose count is pinned below: `"x" * 4001` is 501 tokens and
would pass every over-cap test silently.

WHAT NOT TO SUBSTITUTE. A backend too old to publish the token numbers must
produce NO warning rather than one computed against a cap the client made up --
or against its character pair, which measures a different limit on a current
server. That distinction has its own tests below and it is the point of the
whole design: a fullness the server never asserted is the same class of
confident wrong answer as "appended" for a write that was refused.
"""

from __future__ import annotations

import importlib
import io
import json
import re
import warnings
from pathlib import Path

import pytest

from probe import cli
from probe.sdk.notes import (
    COMPACT_ACTION,
    LIMIT_KEY,
    MOVE_UP_ACTION,
    NOTES_WARN_FRACTION,
    REMAINING_KEY,
    TOKENS_KEY,
    headroom_warning,
    notes_fullness,
    notes_limit,
    read_advisory,
    tokens_past_cap,
)
from tests.conftest import make_client, note_tokens, token_text

_AGENT_ROOT = Path(__file__).resolve().parents[1]


def _full(remaining: int, limit: int) -> dict:
    """A response's token headroom, as the server spells it."""
    return {REMAINING_KEY: remaining, LIMIT_KEY: limit, TOKENS_KEY: limit - remaining}


# -- the fixtures' own arithmetic ---------------------------------------------


def test_token_text_has_the_count_it_says() -> None:
    """Every over-cap body in the notes tests is built from this, so its count
    is asserted, not assumed -- and so is the trap it replaces."""
    for n in (1, 2, 95, 601, 2_000, 2_001, 2_500, 30_001):
        assert note_tokens(token_text(n)) == n
        assert len(token_text(n)) == 2 * n - 1
    assert note_tokens(token_text(0)) == 0
    assert note_tokens("x" * 4_001) == 501, "the old fixture is NOT 4,001 tokens"
    # The "5,000 characters, 1,000 tokens" run note the pre-send check must let through.
    assert (len(" word" * 1_000), note_tokens(" word" * 1_000)) == (5_000, 1_000)


def test_the_fakes_notes_numbers_have_the_servers_shapes(app, tmp_path):
    """The fake publishes the numbers every test here reads, so they are held
    to the server's own response models (`_generated/models.py`): each shape
    validates, and every fullness key the fake sends is a field the server
    declares. A fake key the server lacks would let a client read a number no
    real response carries."""
    from probe._generated import models

    c = make_client(app, tmp_spool=tmp_path / "spool")
    project = c.create_project("p", kind="general")
    experiment = c.create_experiment("e", project_id=project["id"], question="h")
    run = c.create_run(experiment["id"], "r", heartbeat=False)
    c._replace_notes("run", run.id, token_text(10), base_version=None, op_key="t")
    written = c._create_sub_note("experiment", experiment["id"], "Caveats", token_text(12))
    app.team_note["body"] = token_text(7)

    def fullness_keys(row: dict) -> set[str]:
        return {k for k in row if "tokens" in k or "chars" in k}

    shapes = [
        (models.SubNoteWriteOut, written),
        (models.SubNoteOut, c.get_sub_note(written["id"])),
        (models.SubNoteListItem, c.list_sub_notes("experiment", experiment["id"])["sub_notes"][0]),
        (models.TeamNoteOut, c.get_team_note()),
        (models.TeamNoteSyncOut, c.append_team_note("one more")),
        (models.NoteCatalogItem, c.list_notes(limit=100)["items"][0]),
    ]
    for model, row in shapes:
        model.model_validate(row)
        assert fullness_keys(row) <= set(model.model_fields), model.__name__
        assert {"tokens", "limit_tokens"} <= row.keys(), model.__name__
    for model, row in [
        (models.RunDetailOut, c.get_run(run.id)),
        (models.ProjectDetailOut, c.get_project(project["id"])),
    ]:
        assert fullness_keys(row) <= set(model.model_fields), model.__name__
        assert {"notes_tokens", "notes_limit_tokens", "notes_remaining_tokens"} <= row.keys()
    assert c.get_run(run.id)["notes_tokens"] == 10


# -- the numbers on the wire ---------------------------------------------------


def test_a_notes_write_hands_back_the_room_that_is_left(app, tmp_path):
    """The write response carries the headroom, so a writer never has to re-read
    the document to find out whether the next paragraph fits."""
    c = make_client(app, tmp_spool=tmp_path / "spool")
    project = c.create_project("p", kind="general")

    row = c._replace_notes("project", project["id"], token_text(900), base_version=None, op_key="t")

    assert row["notes_limit_tokens"] == app.document_notes_cap
    assert row["notes_tokens"] == 900
    assert row["notes_remaining_tokens"] == app.document_notes_cap - 900
    # The character pair still rides, measured against the backstop.
    assert row["notes_limit_chars"] == app.document_notes_backstop
    assert row["notes_remaining_chars"] == app.document_notes_backstop - len(token_text(900))


def test_the_caps_differ_by_carrier_and_the_response_says_which(app, tmp_path):
    """A run's notes is an annotation on a row and a project's is a document, so
    one number cannot serve both -- and a client that hardcoded either would be
    wrong about the other."""
    c = make_client(app, tmp_spool=tmp_path / "spool")
    project = c.create_project("p", kind="general")
    experiment = c.create_experiment("e", project_id=project["id"], question="h")
    run = c.create_run(experiment["id"], "r", heartbeat=False)

    project_row = c._replace_notes("project", project["id"], "note", base_version=None, op_key="t")
    run_row = c._replace_notes("run", run.id, "note", base_version=None, op_key="t")

    assert project_row["notes_limit_tokens"] == 30_000
    assert run_row["notes_limit_tokens"] == 2_000
    assert (project_row["notes_limit_chars"], run_row["notes_limit_chars"]) == (150_000, 10_000)


def test_an_edit_that_shrinks_a_document_gives_the_room_back(app, tmp_path):
    """Edit is the COMPACTION primitive, so its response is where a writer learns
    that compacting worked. A response that only ever reported growth would make
    the one action that fixes fullness invisible."""
    c = make_client(app, tmp_spool=tmp_path / "spool")
    project = c.create_project("p", kind="general")
    c._replace_notes("project", project["id"], token_text(5_000), base_version=None, op_key="t")

    # The span edit that used to compact a document is gone; a SHRINKING replace
    # is how a compaction lands now, and it must still report the room it gave
    # back. A response that only ever reported growth would make the one action
    # that fixes fullness invisible.
    row = c._replace_notes("project", project["id"], token_text(1_000), base_version=None, op_key="t2")

    assert row["notes_remaining_tokens"] == app.document_notes_cap - 1_000


def test_a_notes_write_no_longer_queues_even_under_async_writes(app, tmp_path):
    """The replace verb is sync=True, so it ALWAYS reaches a server or raises.

    This used to assert the opposite: an append journaled under `async_writes`
    and answered `None`, which was honest because no server had seen it. The
    file model cannot work that way -- a queued replace drains later against a
    `base_version` that has since moved, so it dead-letters after the caller was
    told it shipped. Every notes write is synchronous now, and a real headroom
    number coming back is the proof."""
    c = make_client(app, tmp_spool=tmp_path / "spool", async_writes=True)
    project = c.create_project("p", kind="general")

    row = c._replace_notes("project", project["id"], "queued", base_version=None, op_key="t")

    assert row is not None
    assert row["notes_remaining_tokens"] == app.document_notes_cap - note_tokens("queued")


# -- deciding whether to say something -----------------------------------------


def test_the_sdk_does_not_warn_because_it_no_longer_writes_notes(app, tmp_path):
    """Notes writing left the public SDK, so the SDK renders no message.

    It used to warn here, and under the SDK's ASYNC DEFAULT that warning never
    fired anyway: `Client.write` enqueues and returns None before any request,
    so an over-cap append was queued and dead-lettered rather than refused --
    the silent-success failure 0.105.2 was supposed to have ended. Closing the
    door beats warning from behind it. `probe notes write` is the writer, it
    is always synchronous, and it renders the message.

    Asserted rather than deleted: "the SDK is silent" is now a PROPERTY, and a
    future edit that reintroduces a warning here would be reintroducing a
    surface that cannot deliver one.
    """
    app.notes_cap = 100
    c = make_client(app, tmp_spool=tmp_path / "spool")
    project = c.create_project("p", kind="general")

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        row = c._replace_notes("project", project["id"], token_text(95), base_version=None, op_key="t")

    assert [str(w.message) for w in caught] == []
    # The NUMBERS still come back -- the CLI renders from them.
    assert row["notes_remaining_tokens"] == 5


def test_the_notes_write_verbs_are_not_public_sdk_surface():
    """The removal itself, pinned. A caller reaching for `client.append_notes`
    gets an AttributeError rather than a queued write nothing delivers."""
    from probe.sdk.client import Client

    for verb in ("append_notes", "edit_notes", "append_project_notes", "set_project_notes"):
        assert not hasattr(Client, verb), f"{verb} is public again"
    # Reads stay: knowing what a note says was never the problem.
    assert hasattr(Client, "get_project_notes")
    assert hasattr(Client, "list_notes")


def test_the_advice_starts_with_room_left_to_act_in(app, tmp_path):
    """The message has to arrive while writes still succeed.

    Written against the FRACTION rather than a hardcoded percentage, so tuning
    `NOTES_WARN_FRACTION` moves this test with it -- what is asserted is "advises
    while the write still lands", not "advises at 60".
    """
    app.notes_cap = 1_000
    c = make_client(app, tmp_spool=tmp_path / "spool")
    project = c.create_project("p", kind="general")
    just_past_the_threshold = int(1_000 * (1 - NOTES_WARN_FRACTION)) + 1

    row = c._replace_notes(
        "project", project["id"], token_text(just_past_the_threshold), base_version=None, op_key="t"
    )

    assert row["notes_remaining_tokens"] > 0, "the write still succeeded"
    assert headroom_warning(row, kind="project") is not None


def test_a_backend_without_the_fields_says_nothing_at_all(app, tmp_path):
    """NOT a message computed against a client-side cap table.

    An old backend answers 200 with neither field. Substituting a cap here would
    let the client assert a fullness the server never published -- and it would
    be wrong the moment a cap changed, which is the drift the published limit
    exists to remove.
    """
    app.publishes_notes_headroom = False
    c = make_client(app, tmp_spool=tmp_path / "spool")
    project = c.create_project("p", kind="general")

    row = c._replace_notes("project", project["id"], token_text(29_000), base_version=None, op_key="t")

    assert notes_fullness(row) is None
    assert headroom_warning(row, kind="project") is None


def test_a_backend_before_token_caps_says_nothing_rather_than_counting_characters(app, tmp_path):
    """A server older than token caps publishes only `notes_*_chars` -- against
    the CAP it enforced then. On a current server the same two fields measure
    the character BACKSTOP. The client cannot tell which it is looking at, so a
    fullness read from them would be right on one server and wrong on the
    other: it says nothing instead, and does not fail."""
    app.publishes_note_tokens = False
    c = make_client(app, tmp_spool=tmp_path / "spool")
    project = c.create_project("p", kind="general")

    # 99% of the old 100,000-character cap: the old server WOULD warn here.
    row = c._replace_notes("project", project["id"], "y" * 99_000, base_version=None, op_key="t")

    assert row["notes_limit_chars"] == 100_000 and "notes_limit_tokens" not in row
    assert notes_fullness(row) is None
    assert notes_limit(row) is None
    assert headroom_warning(row, kind="project") is None
    assert read_advisory({**row, "notes": "y" * 99_000}) is None


def test_an_uncounted_note_has_a_cap_but_no_fullness(app, tmp_path):
    """A current server that has not counted a note (its backfill has not
    reached the row) publishes the cap with a null count. Fullness is UNKNOWN
    then -- not zero, not 100% -- while the cap is still known."""
    app.counts_note_tokens = False
    c = make_client(app, tmp_spool=tmp_path / "spool")
    project = c.create_project("p", kind="general")

    row = c._replace_notes("project", project["id"], token_text(29_000), base_version=None, op_key="t")

    assert row["notes_tokens"] is None and row["notes_remaining_tokens"] is None
    assert notes_limit(row) == app.document_notes_cap
    assert notes_fullness(row) is None
    assert headroom_warning(row, kind="project") is None


def test_the_advice_reads_tokens_never_the_character_backstop():
    """Both pairs ride a current response and they can disagree in either
    direction: dense text (code, CJK) fills the token cap long before the
    backstop, plain prose the other way round. Only the tokens refuse first."""
    tokens_full_chars_roomy = {
        **_full(remaining=100, limit=30_000),
        "notes_remaining_chars": 140_000,
        "notes_limit_chars": 150_000,
    }
    chars_full_tokens_roomy = {
        **_full(remaining=29_000, limit=30_000),
        "notes_remaining_chars": 10,
        "notes_limit_chars": 150_000,
    }

    message = headroom_warning(tokens_full_chars_roomy, kind="project")
    assert message is not None and "(29,900 of 30,000 tokens, 100 left)" in message
    assert headroom_warning(chars_full_tokens_roomy, kind="project") is None


def test_the_advice_follows_the_carrier_not_the_size_of_its_cap(app, tmp_path):
    """A full project note should be COMPACTED; a full run note holds prose that
    belongs one level up. Telling a run to compact 2,000 tokens in place buys a
    few hundred and leaves the same problem next week."""
    full_document = _full(remaining=1, limit=30_000)
    full_annotation = _full(remaining=1, limit=2_000)

    assert "compact" in headroom_warning(full_document, kind="project")
    assert "move this prose up" in headroom_warning(full_annotation, kind="run")


def test_the_move_up_advice_names_the_order_that_cannot_lose_prose():
    """Moving prose up is TWO writes against TWO entities and nothing makes them
    atomic: append to the parent first and a failed second write duplicates, the
    other way round it is gone. The ORDER is the instruction, not a refinement.

    Pinned by EQUALITY, deliberately. Two earlier attempts asserted the property
    structurally and both were satisfiable by delete-first prose:

      * `"FIRST" in m` plus `m.index("append") < m.index("delete")` passes on
        "append/delete migration: FIRST delete it here, then append there";
      * the regex `append.*FIRST.*then delete` passes on "stop appending here --
        FIRST make sure you have the text, then delete it here, and append it to
        the project afterwards", because `append` matches inside `appending`.

    Substring order is not operation order, and no cheap pattern separates them.
    The clause is prose whose exact wording IS the safety property, so the test
    holds a copy: a reword fails here and the author has to re-read what the
    sentence carried before updating it. That is the point, not a nuisance.
    """
    assert MOVE_UP_ACTION == (
        "move this prose up into a project or experiment notes document: append "
        "there FIRST, then delete it here, so a failed second write duplicates it "
        "rather than losing it"
    )
    # And it is the clause a run-sized carrier actually receives.
    message = headroom_warning(_full(remaining=1, limit=2_000), kind="run")
    assert MOVE_UP_ACTION in message


def test_a_document_carrier_is_told_to_compact_in_place_with_no_ordering_caveat():
    """The two-write hazard is specific to moving BETWEEN entities. Compaction is
    one `edit` against one row, so an ordering clause would be noise there -- and
    noise in a warning is what teaches a reader to skim the next one.

    The absence check is case-INsensitive: `"FIRST" not in message` only rules
    out one spelling, and "delete the tail sections first, then re-add them
    condensed" would satisfy it while carrying exactly the ordering noise this
    test exists to keep out.
    """
    message = headroom_warning(_full(remaining=1, limit=30_000), kind="project")

    assert COMPACT_ACTION in message
    assert not re.search(r"\bfirst\b", message, re.I), (
        f"a document carrier must carry no ordering caveat; got: {message!r}"
    )


def test_a_document_that_still_accepts_a_write_is_never_reported_as_full(app):
    """Rounding printed "100% full" beside "8 left" for the real assignment-modeling
    numbers. A reader resolves that contradiction by believing the percentage."""
    almost = headroom_warning(_full(remaining=8, limit=30_000), kind="project")
    exactly = headroom_warning(_full(remaining=0, limit=30_000), kind="project")

    assert "99% full" in almost
    assert "(29,992 of 30,000 tokens, 8 left)" in almost
    # At the cap the state is different in KIND, not degree: the document is
    # closed until it is compacted, and a percentage would read as "nearly".
    assert "100% full" not in exactly
    assert "is FULL" in exactly
    assert "(30,000 of 30,000 tokens)" in exactly
    assert "Nothing further will be stored" in exactly


@pytest.mark.parametrize(
    "response",
    [
        None,
        {},
        {REMAINING_KEY: 5},
        {LIMIT_KEY: 2_000},
        {REMAINING_KEY: None, LIMIT_KEY: 2_000, TOKENS_KEY: None},
        {REMAINING_KEY: True, LIMIT_KEY: 2_000},
        {REMAINING_KEY: "5", LIMIT_KEY: 2_000},
        {REMAINING_KEY: 5, LIMIT_KEY: 0},
        {REMAINING_KEY: 5, LIMIT_KEY: True},
        # A server before token caps: its pair is in CHARACTERS and never read.
        {"notes_remaining_chars": 5, "notes_limit_chars": 4_000},
        # A sub-note's unprefixed spelling, not adapted by the caller.
        {"remaining_tokens": 5, "limit_tokens": 2_000},
    ],
)
def test_a_payload_that_cannot_be_trusted_reports_nothing(response):
    """Every unreadable shape reads the same as "no server said anything".

    `True` is in here on purpose: bool is an int in Python, so a JSON `true`
    slipping into either field would otherwise render as "1 tokens left" -- a
    plausible number from a malformed payload, which is worse than silence.
    """
    assert notes_fullness(response) is None
    assert headroom_warning(response, kind="run") is None
    assert read_advisory(response) is None


# -- counting before sending ---------------------------------------------------


def test_a_text_whose_bytes_fit_the_cap_is_never_tokenized(monkeypatch):
    """No token is shorter than a byte, so N bytes is at most N tokens: the
    common case answers without importing the MCP package or loading the
    vocabulary. Proven by a counter that fails if it is called."""
    import probe.mcp.budget as budget

    def no_count(_text: str) -> int:
        raise AssertionError("tokenized a text its byte size already cleared")

    monkeypatch.setattr(budget, "count_tokens", no_count)
    assert tokens_past_cap("x" * 2_000, 2_000) is None
    assert tokens_past_cap("é" * 1_000, 2_000) is None  # 2,000 bytes


def test_a_text_past_the_bytes_is_counted_exactly():
    # 9,999 bytes, 5,000 tokens: counted, and past a 2,000-token cap.
    assert tokens_past_cap(token_text(5_000), 2_000) == 5_000
    # 5,000 bytes and 1,000 tokens: counted, and under it.
    assert tokens_past_cap(" word" * 1_000, 2_000) is None
    # CJK runs dense in tokens per character; the count is the real one.
    cjk = "中文文本测试，包含标点符号。" * 300  # 4,200 characters, 12,600 bytes
    assert tokens_past_cap(cjk, 2_000) == 3_000 == note_tokens(cjk)


def test_a_text_this_machine_cannot_count_is_left_to_the_server(monkeypatch):
    """A missing tokenizer refuses nothing: the server's own check answers, and
    a client that guessed would refuse a write the server takes."""
    import probe.mcp.budget as budget

    def unavailable(_text: str) -> int:
        raise budget.TokenizerUnavailable("no vocabulary")

    monkeypatch.setattr(budget, "count_tokens", unavailable)
    assert tokens_past_cap(token_text(5_000), 2_000) is None
    # A lone surrogate cannot be encoded at all.
    assert tokens_past_cap("\ud800" * 3_000, 2_000) is None


# -- what the CLI does with them ----------------------------------------------


@pytest.fixture
def wired(app, tmp_path, monkeypatch):
    monkeypatch.setattr(
        cli, "Client", lambda **_kw: make_client(app, tmp_spool=tmp_path / "spool")
    )
    cli.main(["project", "create", "--kind", "general", "p"])
    return app


def _append(text: str, monkeypatch, *, target: str = "p") -> int:
    """Write a whole note through the CLI, the only way left to do it.

    Was `probe notes append`; that verb is gone with the span-edit model. `notes
    write` is the whole-document replace and carries the same headroom advisory,
    which is what every test below is actually about.
    """
    monkeypatch.setattr("sys.stdin", io.StringIO(text))
    return cli.main(["notes", "write", "--project", target, "-"])


def test_append_names_the_document_that_is_filling_up(wired, capsys, monkeypatch):
    """The SDK knows the kind; the CLI just resolved the slug and knows WHICH
    one. Only one message is printed, and it is the specific one."""
    wired.notes_cap = 100
    assert _append(token_text(95), monkeypatch) == 0

    err = capsys.readouterr().err
    assert "project notes (p) is 95% full (95 of 100 tokens, 5 left)" in err
    assert err.count("full") == 1, "the SDK's generic warning must not print too"


def test_append_puts_the_numbers_in_the_json_a_script_reads(wired, capsys, monkeypatch):
    """Tokens under their own keys; the keys a script already reads keep their
    CHARACTER meaning (the backstop now), the way the server kept `*_chars`."""
    wired.notes_cap = 1_000
    text = token_text(400)
    _append(text, monkeypatch)

    payload = json.loads(capsys.readouterr().out)
    assert payload["stored_tokens"] == 400
    assert payload["limit_tokens"] == 1_000
    assert payload["remaining_tokens"] == 600
    assert payload["stored_chars"] == len(text)
    assert payload["limit"] == wired.document_notes_backstop
    assert payload["remaining"] == wired.document_notes_backstop - len(text)


def test_a_backend_before_token_caps_gets_no_token_keys_and_no_warning(wired, capsys, monkeypatch):
    """Against an older server the JSON still carries the character keys it
    always did, no token keys, and stderr carries no fullness line at all --
    even at 99% of that server's own character cap."""
    wired.publishes_note_tokens = False
    assert _append("y" * 99_000, monkeypatch) == 0

    out = capsys.readouterr()
    payload = json.loads(out.out)
    assert payload["limit"] == 100_000 and payload["stored_chars"] == 99_000
    assert not {"stored_tokens", "limit_tokens", "remaining_tokens"} & payload.keys()
    assert "full" not in out.err


def test_an_uncounted_note_prints_its_cap_but_no_fullness(wired, capsys, monkeypatch):
    wired.counts_note_tokens = False
    assert _append(token_text(29_000), monkeypatch) == 0

    out = capsys.readouterr()
    payload = json.loads(out.out)
    assert payload["limit_tokens"] == wired.document_notes_cap
    assert "stored_tokens" not in payload and "remaining_tokens" not in payload
    assert "full" not in out.err


def test_a_notes_write_reports_numbers_because_it_can_no_longer_queue(app, tmp_path, monkeypatch, capsys):
    """This used to assert the opposite, and the inversion is the point.

    An append could be JOURNALED under `async_writes`, so the CLI omitted the
    headroom keys entirely -- a key that is absent cannot be misread as a number,
    where `"remaining": null` invites a `jq` reader to treat it as zero. The
    replace verb is `sync=True`, so a notes write now always reaches a server or
    raises. The honest output is therefore real numbers, and the absent-key case
    is unreachable rather than merely untested."""
    monkeypatch.setattr(
        cli, "Client", lambda **_kw: make_client(app, tmp_spool=tmp_path / "spool")
    )
    cli.main(["project", "create", "--kind", "general", "p"])
    capsys.readouterr()
    monkeypatch.setattr(
        cli,
        "Client",
        lambda **_kw: make_client(app, tmp_spool=tmp_path / "spool", async_writes=True),
    )

    monkeypatch.setattr("sys.stdin", io.StringIO("queued"))
    cli.main(["notes", "write", "--project", "p", "-"])

    payload = json.loads(capsys.readouterr().out)
    assert payload["remaining_tokens"] == app.document_notes_cap - note_tokens("queued")
    assert payload["limit_tokens"] == app.document_notes_cap
    assert payload["remaining"] == app.document_notes_backstop - len("queued")


def test_compacting_stops_the_warning(wired, capsys, monkeypatch):
    """The signal has to be able to go away, or it is noise rather than a state."""
    wired.notes_cap = 100
    _append(token_text(95), monkeypatch)
    assert "full" in capsys.readouterr().err

    cli.main(["notes", "edit", "--project", "p", "--old", token_text(90), "--new", ""])

    assert "full" not in capsys.readouterr().err


def test_the_read_advisory_of_notes_show_is_in_tokens(wired, capsys, monkeypatch):
    """`notes show` prints the document on stdout and its fullness beside it."""
    _append(token_text(28_270), monkeypatch)
    capsys.readouterr()

    assert cli.main(["notes", "show", "--project", "p"]) == 0
    err = capsys.readouterr().err
    assert "94% full (28,270 of 30,000 tokens)" in err


def test_notes_find_prints_only_the_paragraphs_that_mention_the_words(wired, capsys, monkeypatch):
    """Daemon cost round 7, S1: the paragraph an edit changes, verbatim, without
    the whole note; nothing found says so."""
    note = "# P\n\n## Where it stands\n\nThe lr sweep is done.\n\n## Decisions\n\nWe chose lr 3e-4.\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(note))
    cli.main(["notes", "write", "--project", "p", "-"])
    capsys.readouterr()

    assert cli.main(["notes", "find", "--project", "p", "3e-4"]) == 0
    out = capsys.readouterr().out
    assert "1 of " in out and "[Decisions · line 9]\nWe chose lr 3e-4." in out
    assert "The lr sweep is done." not in out
    assert cli.main(["notes", "find", "--project", "p", "tokenizer"]) == 0
    assert 'no paragraph mentions "tokenizer"' in capsys.readouterr().out


# -- the sweep ----------------------------------------------------------------
#
# The piece that makes "which documents are near full?" answerable at all. It was
# one API fetch per entity before the catalog row carried a length -- 52 requests
# to size a tenant, which is why nobody ever did it.


def test_status_ranks_every_document_fullest_first(wired, capsys, monkeypatch):
    """One request, every carrier, ordered by the thing you are looking for."""
    wired.projects[next(iter(wired.projects))]["notes"] = token_text(20_000)
    monkeypatch.setattr("sys.stdin", io.StringIO("short"))
    cli.main(["notes", "write", "--project", "p", "-"])
    capsys.readouterr()

    assert cli.main(["notes", "status"]) == 0
    payload = json.loads(capsys.readouterr().out)

    percents = [d["percent"] for d in payload["documents"]]
    assert percents == sorted(percents, reverse=True)
    assert payload["scanned"] == len(payload["documents"])


def test_status_compares_carriers_with_different_caps_on_one_scale(wired, capsys):
    """A 1,940-token run note is fuller than a 15,000-token project note, and
    only a per-row cap can say so. This is the comparison the sweep exists for,
    and the one a client-side cap table gets wrong first."""
    project_id = next(iter(wired.projects))
    wired.projects[project_id]["notes"] = token_text(15_000)
    wired.runs["r-1"] = {"id": "r-1", "name": "tunneling-sambar-254", "notes": token_text(1_940)}

    cli.main(["notes", "status"])
    out = capsys.readouterr()
    payload = json.loads(out.out)

    fullest = payload["documents"][0]
    assert fullest["kind"] == "run"
    assert fullest["percent"] == 97
    assert (fullest["tokens"], fullest["limit_tokens"]) == (1_940, 2_000)
    assert [d["kind"] for d in payload["documents"]] == ["run", "project"]
    assert "1,940/2,000  tokens" in out.err


def test_status_ranks_by_tokens_not_by_characters(wired, capsys):
    """Characters and tokens disagree, and the characters measure the backstop:
    a short note of dense text can be near its token cap while far from its
    character limit. The sweep ranks by the cap that refuses."""
    project_id = next(iter(wired.projects))
    # 37,800 characters (25% of its backstop) and 27,000 tokens (90% of its cap).
    dense = "中文文本测试，包含标点符号。" * 2_700
    wired.projects[project_id]["notes"] = dense
    # 6,000 characters (60% of its backstop) and 1,500 tokens (75% of its cap).
    wired.runs["r-1"] = {"id": "r-1", "name": "roomy", "notes": "r" * 6_000}

    cli.main(["notes", "status"])
    payload = json.loads(capsys.readouterr().out)

    by_kind = {d["kind"]: d for d in payload["documents"]}
    assert (by_kind["project"]["tokens"], by_kind["project"]["percent"]) == (27_000, 90)
    assert (by_kind["run"]["tokens"], by_kind["run"]["percent"]) == (1_500, 75)
    assert [d["kind"] for d in payload["documents"]] == ["project", "run"]
    # The character numbers still ride, under the keys they always had.
    assert by_kind["project"]["chars"] == len(dense)
    assert by_kind["project"]["limit"] == 150_000


def test_status_counts_what_is_past_the_warning_line(wired, capsys):
    project_id = next(iter(wired.projects))
    wired.projects[project_id]["notes"] = token_text(29_996)
    wired.runs["r-1"] = {"id": "r-1", "name": "roomy", "notes": token_text(100)}

    cli.main(["notes", "status"])
    payload = json.loads(capsys.readouterr().out)

    assert payload["near_full"] == 1
    assert payload["warn_at_percent"] == 100 * (1 - NOTES_WARN_FRACTION)


def test_status_can_report_only_the_documents_worth_acting_on(wired, capsys):
    project_id = next(iter(wired.projects))
    wired.projects[project_id]["notes"] = token_text(28_500)
    wired.runs["r-1"] = {"id": "r-1", "name": "roomy", "notes": token_text(100)}

    cli.main(["notes", "status", "--above", "80"])
    payload = json.loads(capsys.readouterr().out)

    assert [d["kind"] for d in payload["documents"]] == ["project"]
    # `scanned` still counts everything read: a filter narrows the REPORT, and a
    # report that also narrowed its own denominator would say "1 of 1 documents"
    # for a tenant with fifty.
    assert payload["scanned"] == 2


def test_status_does_not_rank_rows_it_has_no_token_count_for(wired, capsys):
    """A row with no token count cannot be ranked by fullness: the server has
    not counted it yet, or predates token caps. Not ranked rather than defaulted
    to zero, which would sort an unknown-size document to the BOTTOM of a report
    whose whole job is finding the full ones -- and never ranked by its
    characters, which measure a different limit. The report SAYS it skipped
    them, so "nothing is near full" is never a claim about unread documents."""
    project_id = next(iter(wired.projects))
    wired.projects[project_id]["notes"] = "p" * 100
    original = wired._notes_catalog

    def uncounted(include_sub_notes: bool = False) -> dict:
        page = original()
        for item in page["items"]:
            item["tokens"] = None
        return page

    wired._notes_catalog = uncounted
    cli.main(["notes", "status"])
    out = capsys.readouterr()
    payload = json.loads(out.out)

    assert payload["documents"] == []
    assert payload["scanned"] == 0
    assert payload["unmeasured"] == 1
    assert "1 not counted in tokens yet" in out.err


def test_status_against_a_backend_before_token_caps_ranks_nothing(wired, capsys):
    project_id = next(iter(wired.projects))
    wired.projects[project_id]["notes"] = "p" * 99_000
    wired.publishes_note_tokens = False

    assert cli.main(["notes", "status"]) == 0
    payload = json.loads(capsys.readouterr().out)

    assert (payload["scanned"], payload["unmeasured"], payload["near_full"]) == (0, 1, 0)


def test_status_says_so_when_it_stopped_early(wired, capsys, monkeypatch):
    """A truncated sweep that read as complete would be worse than no sweep:
    "nothing is near full" about pages it never opened."""
    # `probe.cli.main` is a MODULE shadowed by the `main` FUNCTION that
    # `probe.cli` re-exports, so it has to be imported by name.
    cli_main = importlib.import_module("probe.cli.main")
    monkeypatch.setattr(cli_main, "_NOTES_STATUS_MAX_PAGES", 1)
    original = wired._notes_catalog

    def always_more(include_sub_notes: bool = False) -> dict:
        page = original(include_sub_notes)
        page["next_cursor"] = "more"
        return page

    wired._notes_catalog = always_more
    project_id = next(iter(wired.projects))
    wired.projects[project_id]["notes"] = "p" * 100

    cli.main(["notes", "status"])
    out = capsys.readouterr()

    assert json.loads(out.out)["truncated"] is True
    assert "STOPPED" in out.err


# -- version skew --------------------------------------------------------------
#
# The one lever that reaches an install too old to have the fix. A <=0.105.1 CLI
# swallows the 422 a full document answers, prints "appended to <kind> notes",
# and exits 0 -- and no server change can make it print anything else, because
# the swallowing happens on the client. The manifest floor is what tells its
# human to upgrade.


def test_the_manifest_floors_the_cli_at_the_release_that_stopped_losing_notes():
    """`min` is a COMPATIBILITY floor, and a client that silently discards a
    write is the case it exists for.

    Asserted as ">= the fix" rather than "== 0.105.2" so a later floor raised for
    some other reason still passes -- what must never happen is the floor
    dropping back BELOW the release that stopped the loss.
    """
    manifest = json.loads((_AGENT_ROOT / "client-version.json").read_text())
    floor = tuple(int(part) for part in manifest["cli"]["min"].split("."))

    assert floor >= (0, 105, 2), (
        "a CLI below 0.105.2 reports refused notes writes as successful; the "
        "manifest floor is the only thing that reaches one"
    )


def test_the_floor_is_a_nudge_and_not_a_gate():
    """Worth stating because raising a floor is only safe while it stays one.

    `min` drives the SessionStart hook's "below the minimum supported version"
    message and the dashboard's REQUIRED banner. Neither blocks a command, which
    is why flooring at a compatibility bug costs an old install a louder nudge
    rather than its ability to work at all.
    """
    hook = (
        _AGENT_ROOT / "plugins" / "probe-research" / "hooks" / "version_check.py"
    ).read_text()

    assert "below the minimum supported version" in hook
    assert '_final({"continue": True})' in hook


# --- the READ advisory: the line that travels with the document -------------


def test_the_advisory_names_the_version_and_the_fullness() -> None:
    line = read_advisory({REMAINING_KEY: 1_730, LIMIT_KEY: 30_000}, version=41)
    assert "v41" in line
    assert "94% full" in line
    assert "28,270 of 30,000 tokens" in line
    assert "tighten what you can verify" in line
    assert "re-read the full document before editing" in line


def test_a_roomy_note_still_gets_the_correction_reminder() -> None:
    """The nudge is not a fullness warning. Correcting a claim you disproved is
    the job on EVERY read; tightening is the extra that a full note earns."""
    line = read_advisory({REMAINING_KEY: 29_700, LIMIT_KEY: 30_000}, version=3)
    assert "correct what your evidence contradicts" in line
    assert "tighten" not in line


def test_no_headroom_means_no_advisory_rather_than_a_guess() -> None:
    """Same rule as `notes_fullness`: absent means the response did not carry
    the document. An excerpt must not be described as if it were the whole."""
    assert read_advisory({"notes_version": 1}) is None
    assert read_advisory(None) is None
    assert read_advisory({REMAINING_KEY: True, LIMIT_KEY: 100}) is None
    # The character pair alone (a server before token caps) is not headroom.
    assert read_advisory({"notes_remaining_chars": 10, "notes_limit_chars": 100}) is None


def test_the_version_is_optional() -> None:
    line = read_advisory({REMAINING_KEY: 10, LIMIT_KEY: 100})
    assert line.startswith("notes ·")


def test_a_sub_notes_unprefixed_headroom_still_produces_an_advisory() -> None:
    """`SubNoteOut` publishes `remaining_tokens`/`limit_tokens`; the entity
    shapes publish the same numbers `notes_`-prefixed. The reader is written
    against the entity shape, so without the alias at the call site a sub-note
    read is silently advisory-free -- which is how it shipped for one smoke run.
    """
    cli_main = importlib.import_module("probe.cli.main")
    sub = {
        "remaining_tokens": 12_000,
        "limit_tokens": 30_000,
        "tokens": 18_000,
        "remaining_chars": 100_000,
        "limit_chars": 150_000,
        "notes_version": 2,
    }
    assert read_advisory(sub, version=sub["notes_version"]) is None

    aliased = cli_main._sub_note_row_for_headroom(sub)
    assert (aliased[REMAINING_KEY], aliased[LIMIT_KEY], aliased[TOKENS_KEY]) == (12_000, 30_000, 18_000)
    line = read_advisory(aliased, version=aliased["notes_version"])
    assert line is not None and "v2" in line and "60% full" in line
