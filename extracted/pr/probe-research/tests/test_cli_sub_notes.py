"""The `probe notes` sub-note commands, driven end-to-end through the CLI.

The SDK tests prove the wire protocol; these prove the WIRING — argument
parsing, the `id:` escape hatch, the printed JSON a script pipes into `jq`,
and every exit-1 path whose message is the only UI the refusal has.
"""

from __future__ import annotations

import pathlib
import json

import pytest
import typer

from probe import cli
from tests.conftest import make_client, token_text


@pytest.fixture
def wired(app, tmp_path, monkeypatch):
    def factory(**_kw):
        return make_client(app, tmp_spool=tmp_path / "spool")

    monkeypatch.setattr(cli, "Client", factory)
    cli.main(["project", "create", "--kind", "general", "p"])
    cli.main(["experiment", "create", "e", "--question", "h", "--project", "p"])
    return app


def _json_out(capsys) -> dict:
    return json.loads(capsys.readouterr().out)


def test_create_and_list_roundtrip(wired, capsys):
    rc = cli.main(["notes", "create", "--experiment", "e", "--title", "Caveats"])
    assert rc == 0
    created = _json_out(capsys)
    assert created["title"] == "Caveats"
    assert created["id"]  # the escape-hatch address, printed at birth

    assert cli.main(["notes", "list", "--experiment", "e"]) == 0
    page = _json_out(capsys)
    assert [row["title"] for row in page["sub_notes"]] == ["Caveats"]
    row = page["sub_notes"][0]
    assert row["stored_chars"] == 0
    assert row["limit"] == 150_000  # the character backstop
    assert row["stored_tokens"] == 0
    assert row["limit_tokens"] == 30_000  # the cap
    assert page["limit_count"] == 20


def test_checkout_edit_push_show_and_the_headroom_json(wired, capsys, monkeypatch):
    """The file round trip on a sub-note, and the headroom on the WRITE.

    Was `test_append_show_and_the_headroom_json`. `checkout` only reads, so the
    fullness it reports is of the document as it stands; `push` is the write, and
    it is the one that has to price what was stored.
    """
    cli.main(["notes", "create", "--experiment", "e", "--title", "Caveats"])
    note_id = _json_out(capsys)["id"]

    assert cli.main(["notes", "checkout", "--experiment", "e", "--note", "Caveats"]) == 0
    out = _json_out(capsys)
    assert out["note"] == "Caveats"
    path = pathlib.Path(out["path"])

    path.write_text("first paragraph")
    assert cli.main(["notes", "push", "--experiment", "e", "--note", "Caveats"]) == 0
    pushed = _json_out(capsys)
    assert pushed["pushed"] is True

    assert cli.main(["notes", "show", "--experiment", "e", "--note", "Caveats"]) == 0
    assert capsys.readouterr().out == "first paragraph\n"
    # The same document through the id: door.
    assert cli.main(["notes", "show", "--experiment", "e", "--note", f"id:{note_id}"]) == 0
    assert capsys.readouterr().out == "first paragraph\n"


def test_a_near_full_sub_note_warns_on_stderr(wired, capsys, monkeypatch):
    cli.main(["run", "start", "--experiment", "e", "--name", "r1"])
    run_id = capsys.readouterr().out.strip()
    cli.main(["notes", "create", "--run", run_id, "--title", "Caveats"])
    capsys.readouterr()

    assert cli.main(["notes", "checkout", "--run", run_id, "--note", "Caveats"]) == 0
    path = pathlib.Path(_json_out(capsys)["path"])
    path.write_text(token_text(1_300))
    assert cli.main(["notes", "push", "--run", run_id, "--note", "Caveats"]) == 0
    capsys.readouterr()

    # Check it out again: the advisory rides the READ, which is the only point
    # it can change what you do.
    assert cli.main(["notes", "checkout", "--run", run_id, "--note", "Caveats", "--steal"]) == 0
    err = capsys.readouterr().err
    # 1,300 of 2,000 tokens: the budget is visibly coming down.
    assert "warning:" in err and "(1,300 of 2,000 tokens, 700 left)" in err


def test_a_duplicated_title_refuses_and_the_id_door_still_works(wired, capsys):
    cli.main(["notes", "create", "--experiment", "e", "--title", "Ideas"])
    first_id = _json_out(capsys)["id"]
    cli.main(["notes", "create", "--experiment", "e", "--title", "Ideas"])
    capsys.readouterr()

    rc = cli.main(["notes", "rename", "--experiment", "e", "--note", "Ideas", "--to", "x"])
    assert rc == 1
    err = capsys.readouterr().err
    assert first_id in err  # the refusal hands over the addresses...
    assert "id:" in err  # ...and names the door they open

    rc = cli.main(
        ["notes", "rename", "--experiment", "e", "--note", f"id:{first_id}", "--to", "Kept"]
    )
    assert rc == 0
    capsys.readouterr()
    cli.main(["notes", "list", "--experiment", "e"])
    titles = [r["title"] for r in _json_out(capsys)["sub_notes"]]
    assert titles == ["Kept", "Ideas"]


def test_a_missing_title_lists_what_exists(wired, capsys):
    cli.main(["notes", "create", "--experiment", "e", "--title", "Caveats"])
    capsys.readouterr()

    rc = cli.main(["notes", "show", "--experiment", "e", "--note", "Cavets"])
    assert rc == 1
    err = capsys.readouterr().err
    assert "no sub-note titled 'Cavets'" in err
    assert "Caveats" in err  # the typo's fix is on screen


def test_delete_needs_confirmation_and_yes_bypasses_it(wired, capsys):
    cli.main(["notes", "create", "--experiment", "e", "--title", "Doomed"])
    capsys.readouterr()

    # No --yes and no tty: the confirm aborts, the sub-note survives.
    rc = cli.main(["notes", "delete", "--experiment", "e", "--note", "Doomed"])
    assert rc == 1
    assert len(wired.sub_notes) == 1

    rc = cli.main(["notes", "delete", "--experiment", "e", "--note", "Doomed", "--yes"])
    assert rc == 0
    assert wired.sub_notes == {}


def test_delete_reverifies_the_title_after_the_prompt(wired, capsys, monkeypatch):
    """A confirm given for title X must not destroy a document that was renamed
    to Y while the prompt sat open."""
    cli.main(["notes", "create", "--experiment", "e", "--title", "Doomed"])
    note_id = _json_out(capsys)["id"]

    def rename_then_confirm(*_a, **_kw):
        wired.sub_notes[note_id]["title"] = "Reprieved"
        return True

    monkeypatch.setattr(typer, "confirm", rename_then_confirm)
    rc = cli.main(["notes", "delete", "--experiment", "e", "--note", "Doomed"])
    assert rc == 1
    assert "Reprieved" in capsys.readouterr().err
    assert note_id in wired.sub_notes


def test_a_pre_0146_server_gets_the_upgrade_message(wired, capsys):
    cli.main(["run", "start", "--experiment", "e", "--name", "r1"])
    run_id = capsys.readouterr().out.strip()
    wired.sub_notes_route_absent = True
    rc = cli.main(["notes", "list", "--run", run_id])
    assert rc == 1
    err = capsys.readouterr().err
    assert "0.231.0.0" in err  # the version that shipped the routes
    assert "bare 404" in err
    # An experiment's sub-notes are on the experiment API since X21, so a
    # server without them predates THAT, and says so.
    rc = cli.main(["notes", "list", "--experiment", "e"])
    assert rc == 1
    assert "#2282" in capsys.readouterr().err


def test_an_entity_miss_is_not_mislabeled_as_an_old_server(wired, capsys, monkeypatch):
    """`run not found` must pass through as itself — the upgrade mapping keys
    on the ROUTE-shaped bare `Not Found` only. (A run deleted between its
    resolve and the sub-notes read is the miss left to hit: every carrier now
    resolves before the read.)"""
    from probe.sdk import errors
    from probe.sdk.client import Client

    cli.main(["run", "start", "--experiment", "e", "--name", "r1"])
    run_id = capsys.readouterr().out.strip()

    def gone(self, kind, entity_id):
        raise errors.NotFoundError("run not found", status=404, detail="run not found")

    monkeypatch.setattr(Client, "list_sub_notes", gone)
    rc = cli.main(["notes", "list", "--run", run_id])
    assert rc == 1
    err = capsys.readouterr().err
    assert "run not found" in err
    assert "0.231.0.0" not in err


@pytest.mark.parametrize("flag", ["--group", "--artifact"])
def test_files_and_sweep_groups_are_no_longer_note_targets(wired, capsys, flag):
    """Files and sweep groups stopped carrying notes, so no `notes` command
    takes a flag for them any more."""
    for argv in (
        ["notes", "list"],
        ["notes", "show"],
        ["notes", "checkout"],
        ["notes", "push"],
        ["notes", "create", "--title", "T"],
        ["notes", "append", "--text", "x"],
        ["notes", "edit", "--old", "a", "--new", "b"],
        ["notes", "rename", "--note", "T", "--to", "U"],
        ["notes", "delete", "--note", "T", "--yes"],
    ):
        assert cli.main([*argv, flag, "00000000-0000-0000-0000-000000000000"]) == 2, argv
        assert "No such option" in capsys.readouterr().err


def test_the_fullness_sweep_sees_sub_notes(wired, capsys, monkeypatch):
    """A sub-note can refuse writes at ITS cap while every main note has room —
    a sweep blind to them reports 'nothing is near full' about the exact
    documents losing writes."""
    cli.main(["run", "start", "--experiment", "e", "--name", "r1"])
    run_id = capsys.readouterr().out.strip()
    cli.main(["notes", "create", "--run", run_id, "--title", "Caveats"])
    capsys.readouterr()
    # Fill it through the file round trip -- `checkout` only READS, so a sweep
    # test has to actually push something for there to be fullness to see.
    cli.main(["notes", "checkout", "--run", run_id, "--note", "Caveats"])
    path = pathlib.Path(_json_out(capsys)["path"])
    path.write_text(token_text(1_950))
    cli.main(["notes", "push", "--run", run_id, "--note", "Caveats"])
    capsys.readouterr()

    rc = cli.main(["notes", "status"])
    assert rc == 0
    err = capsys.readouterr().err
    assert "sub_note" in err
    assert "Caveats" in err
