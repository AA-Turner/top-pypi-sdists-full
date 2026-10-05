"""The CLI writes an argument-only agent needs: driven end to end through `cli.main`.

Five doors, each one a write the dashboard assistant made through its own tool
layer and the CLI could not:

  * `notes append` / `notes edit` change a note with text passed as arguments,
    never a file. The server has had no append or span edit since 0.388.0.0, so
    both read the note, change the text here and replace it pinned to the
    version read -- these tests hold the refusals (no match, two matches, a
    note that moved) to "nothing was written". With `--team` they call the
    server-computed team-note writes instead (`/v1/team-note/apply/*`).
  * `views update` replaces a view's expression, optionally pinned to the
    `updated_at` the caller read.
  * `run set --status` corrects a status WITHOUT touching the run's clock.
  * `project set` / `experiment set` change fields and tags in ONE PATCH.
"""

from __future__ import annotations

import importlib
import json

import httpx
import pytest

from probe import cli, expr
from tests.conftest import make_client, open_run

cli_main = importlib.import_module("probe.cli.main")


@pytest.fixture
def wired(app, tmp_path, monkeypatch):
    def factory(**_kw):
        return make_client(app, tmp_spool=tmp_path / "spool")

    monkeypatch.setattr(cli, "Client", factory)
    assert cli.main(["project", "create", "--kind", "general", "p"]) == 0
    assert cli.main(["experiment", "create", "e", "--question", "h", "--project", "p"]) == 0
    return app


def _json_out(capsys) -> dict:
    return json.loads(capsys.readouterr().out)


def _project(app) -> dict:
    return next(row for row in app.projects.values() if row.get("slug") == "p")


def _experiment(app) -> dict:
    return next(row for row in app.experiments.values() if row.get("slug") == "e")


def _patches(app, path_fragment: str = "") -> list[dict]:
    return [
        json.loads(r.content or b"{}")
        for r in app.requests
        if r.method == "PATCH" and path_fragment in r.url.path
    ]


def _new_run(wired, tmp_path, name: str = "r1"):
    return open_run(make_client(wired, tmp_spool=tmp_path / "s"), experiment="e", name=name)


def _intercept(app, monkeypatch, respond):
    """Route every request through `respond(request)` first; None falls through."""
    real = app.handler

    def handler(request: httpx.Request) -> httpx.Response:
        answer = respond(request)
        if answer is not None:
            app.requests.append(request)
            return answer
        return real(request)

    monkeypatch.setattr(app, "handler", handler)


def _stale(version: int = 7) -> httpx.Response:
    """`app.core.notes.stale_replace`, byte for byte in shape."""
    return httpx.Response(
        409,
        json={
            "detail": {
                "message": (
                    "the document moved since you read it; re-read it and merge, "
                    "then replace again from the version you merged onto"
                ),
                "notes_version": version,
            }
        },
    )


# ---------------------------------------------------------------- notes append


def test_append_adds_a_paragraph_after_a_blank_line(wired, capsys):
    project = _project(wired)
    project["notes"] = "# Findings\n- lr 3e-4 is stable"

    rc = cli.main(["notes", "append", "--project", "p", "--text", "- warmup matters"])
    assert rc == 0
    out = _json_out(capsys)
    assert out["target"] == "project" and out["chars"] == len("- warmup matters")
    assert project["notes"] == "# Findings\n- lr 3e-4 is stable\n\n- warmup matters"
    # A replace pinned to the version it read: the `notes push` contract.
    (body,) = _patches(wired, "/v1/projects/")
    assert body["notes"] == project["notes"]
    assert "base_version" in body and "force" not in body


@pytest.mark.parametrize("flag", ["--experiment", "--run", "--group"])
def test_append_reaches_every_entity_note(wired, tmp_path, capsys, flag):
    if flag == "--experiment":
        ref, row = "e", _experiment(wired)
    elif flag == "--run":
        run = _new_run(wired, tmp_path)
        ref, row = run.id, wired.runs[run.id]
    else:
        client = make_client(wired, tmp_spool=tmp_path / "s")
        group = client.create_group(_experiment(wired)["id"], "sweep")
        ref, row = group["id"], wired.groups[group["id"]]

    assert cli.main(["notes", "append", flag, ref, "--text", "first"]) == 0
    assert cli.main(["notes", "append", flag, ref, "--text", "second"]) == 0
    capsys.readouterr()
    assert row["notes"] == "first\n\nsecond"


def test_append_to_a_sub_note(wired, capsys):
    assert cli.main(["notes", "create", "--experiment", "e", "--title", "Caveats"]) == 0
    capsys.readouterr()
    assert cli.main(
        ["notes", "append", "--experiment", "e", "--note", "Caveats", "--text", "eval leak"]
    ) == 0
    out = _json_out(capsys)
    assert out["note"] == "Caveats" and out["version"] == 1
    (sub,) = wired.sub_notes.values()
    assert sub["body"] == "eval leak"


def test_append_text_is_literal_never_a_file_or_stdin(wired, tmp_path, monkeypatch, capsys):
    """`--notes @path` reads a file elsewhere in this CLI; here it must not, or a
    command could copy any file it can name into a note."""
    secret = tmp_path / "secret.txt"
    secret.write_text("do not send")
    monkeypatch.setattr("sys.stdin", __import__("io").StringIO("from stdin"))
    project = _project(wired)

    assert cli.main(["notes", "append", "--project", "p", "--text", f"@{secret}"]) == 0
    assert cli.main(["notes", "append", "--project", "p", "--text", "-"]) == 0
    capsys.readouterr()
    assert project["notes"] == f"@{secret}\n\n-"
    assert "do not send" not in project["notes"] and "from stdin" not in project["notes"]


def test_append_refuses_empty_text(wired, capsys):
    assert cli.main(["notes", "append", "--project", "p", "--text", "  "]) == 2
    assert _patches(wired, "/v1/projects/") == []


def test_append_reapplies_on_the_new_text_when_the_note_moved(wired, monkeypatch, capsys):
    """A teammate writes between the read and the replace: the server refuses the
    stale version, and the append lands on THEIR text instead of erasing it."""
    project = _project(wired)
    project["notes"] = "start"
    raced = []

    def teammate(request):
        if request.method == "PATCH" and not raced:
            raced.append(True)
            project["notes"] = "start\n\na teammate's finding"
            return _stale()
        return None

    _intercept(wired, monkeypatch, teammate)
    assert cli.main(["notes", "append", "--project", "p", "--text", "mine"]) == 0
    capsys.readouterr()
    assert project["notes"] == "start\n\na teammate's finding\n\nmine"
    first, second = _patches(wired, "/v1/projects/")
    assert first["notes"] == "start\n\nmine"  # built on the stale read, refused
    assert second["notes"] == project["notes"]


def test_append_gives_up_on_a_note_that_never_stops_moving(wired, monkeypatch, capsys):
    project = _project(wired)
    project["notes"] = "start"
    _intercept(wired, monkeypatch, lambda r: _stale() if r.method == "PATCH" else None)

    assert cli.main(["notes", "append", "--project", "p", "--text", "mine"]) == 1
    captured = capsys.readouterr()
    assert "kept changing" in captured.err and "nothing was written" in captured.err
    assert captured.out == ""
    assert project["notes"] == "start"
    assert len(_patches(wired, "/v1/projects/")) == cli_main._NOTE_REWRITE_ATTEMPTS


def test_append_past_the_cap_is_refused_before_anything_is_sent(wired, tmp_path, capsys):
    run = _new_run(wired, tmp_path)
    wired.runs[run.id]["notes"] = "x" * 3_990  # a run note's cap is 4,000

    assert cli.main(["notes", "append", "--run", run.id, "--text", "one more line"]) == 1
    err = capsys.readouterr().err
    assert "4,000-character" in err and "FULL" in err
    assert _patches(wired, f"/v1/runs/{run.id}") == []


def test_a_refused_write_exits_non_zero_and_prints_no_result(wired, monkeypatch, capsys):
    _intercept(
        wired,
        monkeypatch,
        lambda r: httpx.Response(403, json={"detail": "write scope required"})
        if r.method == "PATCH"
        else None,
    )
    assert cli.main(["notes", "append", "--project", "p", "--text", "mine"]) == 1
    captured = capsys.readouterr()
    assert "write scope required" in captured.err
    assert captured.out == ""  # never a success line, never `null`


def test_an_unknown_target_writes_nothing(wired, capsys):
    assert cli.main(["notes", "append", "--project", "nope", "--text", "x"]) != 0
    assert cli.main(["notes", "append", "--experiment", "nope", "--text", "x"]) != 0
    assert cli.main(["notes", "edit", "--project", "nope", "--old", "a", "--new", "b"]) != 0
    capsys.readouterr()
    assert _patches(wired) == []


def test_two_targets_are_refused_rather_than_guessed(wired, capsys):
    rc = cli.main(["notes", "append", "--project", "p", "--experiment", "e", "--text", "x"])
    assert rc == 2
    assert _patches(wired) == []


def test_an_unknown_sub_note_title_writes_nothing(wired, capsys):
    rc = cli.main(["notes", "append", "--experiment", "e", "--note", "Nope", "--text", "x"])
    assert rc == 1
    assert "no sub-note titled 'Nope'" in capsys.readouterr().err
    assert _patches(wired) == []


# ---------------------------------------------------------------- notes edit


def test_edit_replaces_the_one_exact_match(wired, capsys):
    project = _project(wired)
    project["notes"] = "lr 3e-4 is stable\nwd 0.1 diverged"

    rc = cli.main(
        ["notes", "edit", "--project", "p", "--old", "wd 0.1 diverged", "--new", "wd 0.1 is fine"]
    )
    assert rc == 0
    out = _json_out(capsys)
    assert out["removed"] == len("wd 0.1 diverged") and out["added"] == len("wd 0.1 is fine")
    assert project["notes"] == "lr 3e-4 is stable\nwd 0.1 is fine"


def test_edit_with_an_empty_new_deletes_the_span(wired, capsys):
    project = _project(wired)
    project["notes"] = "keep\nDROP ME\nkeep too"
    assert cli.main(["notes", "edit", "--project", "p", "--old", "DROP ME\n", "--new", ""]) == 0
    capsys.readouterr()
    assert project["notes"] == "keep\nkeep too"


def test_edit_needs_new_spelled_out(wired, capsys):
    """Omitting --new must not silently mean "delete it"."""
    _project(wired)["notes"] = "a b"
    assert cli.main(["notes", "edit", "--project", "p", "--old", "a"]) == 2
    assert _project(wired)["notes"] == "a b"


@pytest.mark.parametrize(
    "document, old, says",
    [
        ("lr 3e-4 is stable", "wd 0.1", "matches nothing"),
        ("seed 1 diverged\nseed 2 diverged", "diverged", "matches 2 places"),
    ],
)
def test_edit_refuses_unless_old_matches_exactly_once(wired, capsys, document, old, says):
    project = _project(wired)
    project["notes"] = document

    assert cli.main(["notes", "edit", "--project", "p", "--old", old, "--new", "X"]) == 1
    captured = capsys.readouterr()
    assert says in captured.err and "nothing was written" in captured.err
    assert captured.out == ""
    assert project["notes"] == document
    assert _patches(wired, "/v1/projects/") == []


def test_edit_matches_exactly_without_normalising(wired, capsys):
    project = _project(wired)
    project["notes"] = "Loss Diverged"
    assert cli.main(["notes", "edit", "--project", "p", "--old", "loss diverged", "--new", "x"]) == 1
    assert project["notes"] == "Loss Diverged"


def test_edit_rechecks_the_match_on_a_note_that_moved(wired, monkeypatch, capsys):
    """The stale-version retry re-reads and re-matches: when a teammate already
    changed the span, the edit is refused rather than forced through."""
    project = _project(wired)
    project["notes"] = "wd 0.1 diverged"
    raced = []

    def teammate(request):
        if request.method == "PATCH" and not raced:
            raced.append(True)
            project["notes"] = "wd 0.1 was a bad seed"
            return _stale()
        return None

    _intercept(wired, monkeypatch, teammate)
    rc = cli.main(
        ["notes", "edit", "--project", "p", "--old", "wd 0.1 diverged", "--new", "wd 0.1 fine"]
    )
    assert rc == 1
    assert "matches nothing" in capsys.readouterr().err
    assert project["notes"] == "wd 0.1 was a bad seed"


def test_edit_a_sub_note_by_id(wired, capsys):
    assert cli.main(
        ["notes", "create", "--experiment", "e", "--title", "Caveats"]
    ) == 0
    note_id = _json_out(capsys)["id"]
    assert cli.main(
        ["notes", "append", "--experiment", "e", "--note", "Caveats", "--text", "seed 3 leaked"]
    ) == 0
    capsys.readouterr()
    rc = cli.main(
        [
            "notes", "edit", "--experiment", "e", "--note", f"id:{note_id}",
            "--old", "leaked", "--new", "was clean",
        ]
    )
    assert rc == 0
    assert wired.sub_notes[note_id]["body"] == "seed 3 was clean"


def test_edit_refuses_an_empty_old(wired, capsys):
    assert cli.main(["notes", "edit", "--project", "p", "--old", "", "--new", "x"]) == 2


# ---------------------------------------------------------------- the team note


def _team_posts(app) -> list[tuple[str, dict]]:
    return [
        (r.url.path, json.loads(r.content or b"{}"))
        for r in app.requests
        if r.method == "POST" and r.url.path.startswith("/v1/team-note/")
    ]


def test_append_to_the_team_note_uses_the_server_computed_write(wired, capsys):
    wired.team_note["body"] = "# Cluster\n\nGPUs are oversubscribed.\n"

    assert cli.main(["notes", "append", "--team", "--text", "Cap vitest at 2 threads."]) == 0
    out = _json_out(capsys)
    assert out["target"] == "team" and out["version"] == 1
    assert out["remaining"] == 100_000 - len(wired.team_note["body"])
    assert wired.team_note["body"] == (
        "# Cluster\n\nGPUs are oversubscribed.\n\nCap vitest at 2 threads.\n"
    )
    # One write carrying no version: the server merges under its own lock. The
    # one read before it is what settles a reply that goes missing.
    assert _team_posts(wired) == [
        ("/v1/team-note/apply/paragraph", {"text": "Cap vitest at 2 threads."})
    ]
    reads = [r for r in wired.requests if r.url.path == "/v1/team-note"]
    assert [r.method for r in reads] == ["GET"]


def test_edit_the_team_note(wired, capsys):
    wired.team_note["body"] = "GPUs are oversubscribed.\n"
    rc = cli.main(
        ["notes", "edit", "--team", "--old", "oversubscribed", "--new", "free after 6pm"]
    )
    assert rc == 0
    out = _json_out(capsys)
    assert out["removed"] == len("oversubscribed") and out["added"] == len("free after 6pm")
    assert wired.team_note["body"] == "GPUs are free after 6pm.\n"
    assert _team_posts(wired) == [
        (
            "/v1/team-note/apply/span",
            {"old_text": "oversubscribed", "new_text": "free after 6pm"},
        )
    ]


@pytest.mark.parametrize(
    "document, old, says",
    [
        ("GPUs are oversubscribed.\n", "idle", "matches nothing"),
        ("seed 1 diverged\nseed 2 diverged\n", "diverged", "matches 2 places"),
    ],
)
def test_a_team_edit_refuses_unless_old_matches_exactly_once(wired, capsys, document, old, says):
    wired.team_note["body"] = document
    assert cli.main(["notes", "edit", "--team", "--old", old, "--new", "X"]) == 1
    captured = capsys.readouterr()
    assert says in captured.err and "team note" in captured.err
    assert "nothing was written" in captured.err and captured.out == ""
    assert wired.team_note["body"] == document and wired.team_note["version"] == 0


def test_a_team_write_retries_only_the_refusal_that_wrote_nothing(wired, monkeypatch, capsys):
    """`retryable: true` (another write landed at the same instant) is retried;
    the second attempt lands."""
    raced = []

    def collide(request):
        if request.url.path == "/v1/team-note/apply/paragraph" and not raced:
            raced.append(True)
            return httpx.Response(
                409,
                json={
                    "detail": {
                        "message": "another writer landed at the same moment; retry.",
                        "retryable": True,
                    }
                },
            )
        return None

    _intercept(wired, monkeypatch, collide)
    assert cli.main(["notes", "append", "--team", "--text", "mine"]) == 0
    capsys.readouterr()
    assert wired.team_note["body"] == "mine\n"
    assert len(_team_posts(wired)) == 2


def test_a_refused_team_write_exits_non_zero(wired, monkeypatch, capsys):
    wired.team_note["body"] = "x" * 99_990
    assert cli.main(["notes", "append", "--team", "--text", "one more paragraph"]) == 1
    captured = capsys.readouterr()
    assert "team note limit" in captured.err and captured.out == ""
    assert wired.team_note["version"] == 0

    _intercept(
        wired,
        monkeypatch,
        lambda r: httpx.Response(403, json={"detail": "write scope required"})
        if r.url.path.startswith("/v1/team-note/apply/")
        else None,
    )
    assert cli.main(["notes", "edit", "--team", "--old", "x", "--new", "y"]) == 1
    captured = capsys.readouterr()
    assert "write scope required" in captured.err and captured.out == ""


def test_team_text_is_literal(wired, tmp_path, capsys):
    secret = tmp_path / "secret.txt"
    secret.write_text("do not send")
    assert cli.main(["notes", "append", "--team", "--text", f"@{secret}"]) == 0
    capsys.readouterr()
    assert wired.team_note["body"] == f"@{secret}\n"


def _lose_replies(app, monkeypatch, *, path: str, method: str, land: bool, then=None):
    """Make every `method` request to `path` lose its reply: the write lands on
    the fake first when `land`, and `then(app)` can play a teammate writing
    before the reply goes missing."""
    real = app.handler

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == method and request.url.path == path:
            if land:
                real(request)
            else:
                app.requests.append(request)
            if then is not None:
                then(app)
            raise httpx.ReadTimeout("the reply never came", request=request)
        return real(request)

    monkeypatch.setattr(app, "handler", handler)


# A credential-shaped token the scrubber turns the WHOLE value into `<redacted>`
# for, as it did to a real note (review of #2217).
_WIPES_THE_VALUE = "control run: sk%2Dbaseline"


def test_append_refuses_a_note_the_scrubber_would_rewrite(wired, capsys):
    """Text already in the note that the scrubber would rewrite (written before
    the server scrubbed, or matched by a newer rule) must not be rewritten by an
    append that never touched it: one append once turned a whole note into
    `<redacted>`."""
    project = _project(wired)
    project["notes"] = f"- lr 3e-4 is stable\n{_WIPES_THE_VALUE}"

    assert cli.main(["notes", "append", "--project", "p", "--text", "- warmup matters"]) == 1
    captured = capsys.readouterr()
    assert "scrubber" in captured.err and "notes checkout" in captured.err
    assert "nothing was written" in captured.err and captured.out == ""
    assert project["notes"] == f"- lr 3e-4 is stable\n{_WIPES_THE_VALUE}"
    assert _patches(wired, "/v1/projects/") == []


def test_edit_refuses_a_note_the_scrubber_would_rewrite(wired, capsys):
    project = _project(wired)
    project["notes"] = f"wd 0.1 diverged\n{_WIPES_THE_VALUE}"
    rc = cli.main(["notes", "edit", "--project", "p", "--old", "diverged", "--new", "is fine"])
    assert rc == 1
    assert "scrubber" in capsys.readouterr().err
    assert _patches(wired, "/v1/projects/") == []


def test_new_text_whose_scrub_would_rewrite_the_rest_of_the_note_is_refused(wired, capsys):
    """The caller's own text may be scrubbed, but some rules rewrite the WHOLE
    value: appending one of those would replace every line already there."""
    project = _project(wired)
    project["notes"] = "- lr 3e-4 is stable"
    assert cli.main(["notes", "append", "--project", "p", "--text", _WIPES_THE_VALUE]) == 1
    assert "scrubber" in capsys.readouterr().err
    assert project["notes"] == "- lr 3e-4 is stable"
    assert _patches(wired, "/v1/projects/") == []


def test_the_callers_own_text_is_still_scrubbed_as_before(wired, capsys):
    project = _project(wired)
    project["notes"] = "- lr 3e-4 is stable"
    token = "ghp_" + "a" * 36
    assert cli.main(["notes", "append", "--project", "p", "--text", f"key was {token}"]) == 0
    capsys.readouterr()
    assert project["notes"] == "- lr 3e-4 is stable\n\nkey was <redacted:github-token>"


@pytest.mark.parametrize(
    "argv",
    [
        ["notes", "edit", "--team", "--old", "sk-baseline", "--new", "X"],
        ["notes", "edit", "--project", "p", "--old", "sk-baseline", "--new", "X"],
    ],
)
def test_edit_refuses_an_old_the_scrubber_would_rewrite(wired, capsys, argv):
    """The server scrubs `old_text` before matching, so `--old sk-baseline` once
    matched an unrelated `<redacted>` placeholder and replaced it."""
    wired.team_note["body"] = "old key: <redacted>\nbaseline is fine\n"
    _project(wired)["notes"] = "old key: <redacted>\nbaseline is fine\n"

    assert cli.main(argv) == 1
    captured = capsys.readouterr()
    assert "scrubber" in captured.err and captured.out == ""
    assert wired.team_note["body"] == "old key: <redacted>\nbaseline is fine\n"
    assert _project(wired)["notes"] == "old key: <redacted>\nbaseline is fine\n"
    assert _team_posts(wired) == [] and _patches(wired) == []


def test_a_lost_reply_whose_write_landed_is_reported_once(wired, monkeypatch, capsys):
    """Re-sending would append the paragraph twice; the note is re-read instead
    and shows the write landed."""
    project = _project(wired)
    project["notes"] = "start"
    _lose_replies(wired, monkeypatch, path=f"/v1/projects/{project['id']}", method="PATCH", land=True)

    assert cli.main(["notes", "append", "--project", "p", "--text", "mine"]) == 0
    out = _json_out(capsys)
    assert out["version"] == 1
    assert project["notes"] == "start\n\nmine"
    assert len(_patches(wired, "/v1/projects/")) == 1


def test_a_lost_reply_after_another_write_may_have_landed(wired, monkeypatch, capsys):
    project = _project(wired)
    project["notes"] = "start"

    def teammate(app):
        project["notes"] = "start\n\nsomeone else"
        project["notes_version"] = (project.get("notes_version") or 0) + 1

    _lose_replies(
        wired, monkeypatch, path=f"/v1/projects/{project['id']}", method="PATCH",
        land=False, then=teammate,
    )
    assert cli.main(["notes", "append", "--project", "p", "--text", "mine"]) == 1
    captured = capsys.readouterr()
    assert "may have landed" in captured.err and captured.out == ""


def _hold_writes(app, monkeypatch, *, path: str, method: str):
    """Hold every `method` request to `path` WITHOUT applying it and lose its
    reply: the server is still working after the CLI gave up (it waits 30 s,
    the server up to 300 s). Returns `land()`, which applies what was held."""
    real = app.handler
    held: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == method and request.url.path == path:
            held.append(request)
            app.requests.append(request)
            raise httpx.ReadTimeout("the reply never came", request=request)
        return real(request)

    monkeypatch.setattr(app, "handler", handler)

    def land() -> None:
        for request in held:
            real(request)

    return land


def _never_says_run_it_again(err: str) -> None:
    assert "may still" in err and "Run it again" not in err
    assert "nothing was written" not in err


def test_a_lost_reply_with_the_note_unchanged_may_still_land(wired, monkeypatch, capsys):
    """Unchanged at the re-read is NOT "nothing was written" after a timeout:
    the server may still be applying it, and running it again would append the
    paragraph twice."""
    project = _project(wired)
    project["notes"] = "start"
    _lose_replies(wired, monkeypatch, path=f"/v1/projects/{project['id']}", method="PATCH", land=False)

    assert cli.main(["notes", "append", "--project", "p", "--text", "mine"]) == 1
    captured = capsys.readouterr()
    _never_says_run_it_again(captured.err)
    assert "probe notes show" in captured.err and captured.out == ""
    assert project["notes"] == "start"


def test_a_write_that_lands_after_the_cli_gave_up(wired, monkeypatch, capsys):
    """The real server's case (review of eca06e398): the run row is locked, the
    CLI times out and re-reads the old version, and the write lands later. The
    CLI must not have told the caller to run it again."""
    project = _project(wired)
    project["notes"] = "start"
    land = _hold_writes(wired, monkeypatch, path=f"/v1/projects/{project['id']}", method="PATCH")

    assert cli.main(["notes", "append", "--project", "p", "--text", "mine"]) == 1
    captured = capsys.readouterr()
    _never_says_run_it_again(captured.err)
    assert project["notes"] == "start"  # not there at the re-read...

    land()
    assert project["notes"] == "start\n\nmine"  # ...and there afterwards, once
    assert project["notes_version"] == 1


@pytest.mark.parametrize("status", [502, 504])
def test_a_gateway_timeout_may_still_land(wired, monkeypatch, capsys, status):
    project = _project(wired)
    project["notes"] = "start"
    _intercept(
        wired,
        monkeypatch,
        lambda r: httpx.Response(status, text="gateway") if r.method == "PATCH" else None,
    )
    assert cli.main(["notes", "append", "--project", "p", "--text", "mine"]) == 1
    _never_says_run_it_again(capsys.readouterr().err)


@pytest.mark.parametrize("status", [500, 503])
def test_a_5xx_the_app_answered_wrote_nothing(wired, monkeypatch, capsys, status):
    """The app answered, so its transaction is over: unchanged is nothing written."""
    project = _project(wired)
    project["notes"] = "start"
    _intercept(
        wired,
        monkeypatch,
        lambda r: httpx.Response(status, json={"detail": "boom"}) if r.method == "PATCH" else None,
    )
    assert cli.main(["notes", "append", "--project", "p", "--text", "mine"]) == 1
    assert "nothing was written" in capsys.readouterr().err


@pytest.mark.parametrize("land", [True, False])
def test_a_lost_team_reply_is_settled_by_reading_the_team_note(wired, monkeypatch, capsys, land):
    wired.team_note["body"] = "GPUs are oversubscribed.\n"
    _lose_replies(
        wired, monkeypatch, path="/v1/team-note/apply/paragraph", method="POST", land=land
    )
    rc = cli.main(["notes", "append", "--team", "--text", "Cap vitest at 2 threads."])
    captured = capsys.readouterr()
    if land:
        assert rc == 0 and json.loads(captured.out)["version"] == 1
        assert wired.team_note["body"].count("Cap vitest") == 1
    else:
        assert rc == 1 and captured.out == ""
        _never_says_run_it_again(captured.err)
        assert "probe notes team" in captured.err
        assert wired.team_note["version"] == 0


def test_a_team_write_that_lands_after_the_cli_gave_up(wired, monkeypatch, capsys):
    wired.team_note["body"] = "GPUs are oversubscribed.\n"
    land = _hold_writes(wired, monkeypatch, path="/v1/team-note/apply/paragraph", method="POST")
    assert cli.main(["notes", "append", "--team", "--text", "Cap vitest."]) == 1
    _never_says_run_it_again(capsys.readouterr().err)
    land()
    assert wired.team_note["body"].count("Cap vitest.") == 1


def _html_reply() -> httpx.Response:
    return httpx.Response(200, text="<html>sign in</html>", headers={"content-type": "text/html"})


def test_a_reread_that_is_not_json_may_have_landed(wired, monkeypatch, capsys):
    """The re-read itself answered by an ingress page: a clean "may have
    landed", never a JSONDecodeError traceback."""
    project = _project(wired)
    project["notes"] = "start"
    path = f"/v1/projects/{project['id']}"
    _lose_replies(wired, monkeypatch, path=path, method="PATCH", land=True)
    reads = []
    real = wired.handler

    def html_after_the_write(request):
        if request.method == "GET" and request.url.path == path and _patches(wired, path):
            reads.append(request)
            return _html_reply()
        return real(request)

    monkeypatch.setattr(wired, "handler", html_after_the_write)
    assert cli.main(["notes", "append", "--project", "p", "--text", "mine"]) == 1
    captured = capsys.readouterr()
    assert "could not be re-read" in captured.err and "may have landed" in captured.err
    assert reads, "the re-read was answered by the page"


def test_a_team_pre_read_that_is_not_json_still_writes(wired, monkeypatch, capsys):
    """The pre-read only settles a lost reply; an ingress page there must not
    crash the write, and a lost reply is then "may have landed"."""
    _intercept(
        wired,
        monkeypatch,
        lambda r: _html_reply() if r.method == "GET" and r.url.path == "/v1/team-note" else None,
    )
    assert cli.main(["notes", "append", "--team", "--text", "first"]) == 0
    capsys.readouterr()
    assert wired.team_note["body"] == "first\n"

    _lose_replies(wired, monkeypatch, path="/v1/team-note/apply/paragraph", method="POST", land=True)
    assert cli.main(["notes", "append", "--team", "--text", "second"]) == 1
    assert "may have landed" in capsys.readouterr().err


def test_a_team_write_by_a_credential_that_cannot_read_still_writes(wired, monkeypatch, capsys):
    """The team-note read is only there to settle a lost reply. A write-only
    credential still writes; a lost reply is then reported as possibly landed,
    never as written or as not written."""
    def write_only(request):
        if request.method == "GET" and request.url.path == "/v1/team-note":
            return httpx.Response(403, json={"detail": "read scope required"})
        return None

    _intercept(wired, monkeypatch, write_only)
    assert cli.main(["notes", "append", "--team", "--text", "first"]) == 0
    capsys.readouterr()
    assert wired.team_note["body"] == "first\n"

    _lose_replies(wired, monkeypatch, path="/v1/team-note/apply/paragraph", method="POST", land=True)
    assert cli.main(["notes", "append", "--team", "--text", "second"]) == 1
    captured = capsys.readouterr()
    assert "may have landed" in captured.err and captured.out == ""


def test_a_lost_team_edit_reply_whose_edit_landed(wired, monkeypatch, capsys):
    wired.team_note["body"] = "GPUs are oversubscribed.\n"
    _lose_replies(wired, monkeypatch, path="/v1/team-note/apply/span", method="POST", land=True)
    rc = cli.main(["notes", "edit", "--team", "--old", "oversubscribed", "--new", "free"])
    assert rc == 0
    assert wired.team_note["body"] == "GPUs are free.\n"


@pytest.mark.parametrize(
    "reply",
    [
        lambda: httpx.Response(200, text="<html>sign in</html>", headers={"content-type": "text/html"}),
        lambda: httpx.Response(307, headers={"location": "https://elsewhere.test/"}),
    ],
    ids=["html-200", "redirect"],
)
def test_a_reply_that_is_not_probes_is_not_success(wired, monkeypatch, capsys, reply):
    """A redirect or a non-JSON 200 hands back no version: nothing proves the
    note changed, so it is not reported as written."""
    project = _project(wired)
    project["notes"] = "start"
    _intercept(
        wired, monkeypatch,
        lambda r: reply() if r.method in ("PATCH", "POST") else None,
    )
    assert cli.main(["notes", "append", "--project", "p", "--text", "mine"]) == 1
    captured = capsys.readouterr()
    assert captured.out == "" and "appended" not in captured.err
    # The app (or something in front of it) answered, so unchanged IS nothing.
    assert "nothing was written" in captured.err
    assert cli.main(["notes", "append", "--team", "--text", "mine"]) == 1
    captured = capsys.readouterr()
    assert captured.out == "" and "appended" not in captured.err
    assert "nothing was written" in captured.err


def test_a_read_without_a_version_is_refused(wired, monkeypatch, capsys):
    """Without the version it read, the replace cannot be pinned, so a
    teammate's write in between would be overwritten."""
    project = _project(wired)
    project["notes"] = "start"

    def unversioned(request):
        if request.method == "GET" and request.url.path == f"/v1/projects/{project['id']}":
            row = {k: v for k, v in project.items() if k != "notes_version"}
            return httpx.Response(200, json=row)
        return None

    _intercept(wired, monkeypatch, unversioned)
    assert cli.main(["notes", "append", "--project", "p", "--text", "mine"]) == 1
    assert "version" in capsys.readouterr().err
    assert _patches(wired, "/v1/projects/") == []
    assert project["notes"] == "start"


def _seed_artifact(app, notes: str | None = None) -> dict:
    row = {"id": "art-00000000-0000-4000-8000-000000000001", "name": "eval.csv", "notes": notes}
    app.artifacts.setdefault("project:p", []).append(row)
    return row


def test_append_and_edit_reach_an_artifact_note(wired, capsys):
    artifact = _seed_artifact(wired)
    ref = artifact["id"]
    assert cli.main(["notes", "append", "--artifact", ref, "--text", "held-out split v2"]) == 0
    assert cli.main(["notes", "append", "--artifact", ref, "--text", "rows 10-20 dropped"]) == 0
    assert cli.main(
        ["notes", "edit", "--artifact", ref, "--old", "10-20", "--new", "10-12"]
    ) == 0
    out = [json.loads(line) for line in capsys.readouterr().out.splitlines()]
    assert [o["version"] for o in out] == [1, 2, 3]
    assert artifact["notes"] == "held-out split v2\n\nrows 10-12 dropped"


@pytest.mark.parametrize(
    "argv",
    [
        ["notes", "append", "--team", "--project", "p", "--text", "x"],
        ["notes", "append", "--team", "--note", "Caveats", "--text", "x"],
        ["notes", "edit", "--team", "--run", "r1", "--old", "a", "--new", "b"],
        ["notes", "append", "--team", "--text", " "],
        ["notes", "edit", "--team", "--old", "", "--new", "b"],
    ],
)
def test_team_refuses_a_second_target_and_empty_text(wired, capsys, argv):
    assert cli.main(argv) == 2
    assert _team_posts(wired) == [] and _patches(wired) == []


# ---------------------------------------------------------------- views update


def _view(wired, tmp_path):
    run = open_run(make_client(wired, tmp_spool=tmp_path / "s"), experiment="cli-views")
    return run, run.create_view("ratio", expr.series("a") / expr.series("b"))


def test_views_update_replaces_the_spec_and_keeps_the_name(wired, tmp_path, capsys):
    run, view = _view(wired, tmp_path)
    spec = json.dumps(expr.spec(expr.series("a") * 2))

    assert cli.main(["views", "update", view["id"], "--spec", spec]) == 0
    out = _json_out(capsys)
    assert out["name"] == "ratio"
    assert out["spec"]["expression"]["fn"] == "mul"
    (body,) = _patches(wired, "/v1/views/")
    assert set(body) == {"spec"}


def test_views_update_can_rename_and_respec_in_one_write(wired, tmp_path, capsys):
    _run, view = _view(wired, tmp_path)
    spec = json.dumps(expr.spec(expr.series("a") - expr.series("b")))
    rc = cli.main(["views", "update", view["id"], "--name", "gap", "--spec", spec])
    assert rc == 0
    out = _json_out(capsys)
    assert out["name"] == "gap" and out["spec"]["expression"]["fn"] == "sub"
    assert len(_patches(wired, "/v1/views/")) == 1


def test_views_update_pinned_to_what_was_read(wired, tmp_path, capsys):
    _run, view = _view(wired, tmp_path)
    read_at = view["updated_at"]
    spec = json.dumps(expr.spec(expr.series("a") * 2))

    rc = cli.main(
        ["views", "update", view["id"], "--spec", spec, "--expected-updated-at", read_at]
    )
    assert rc == 0
    capsys.readouterr()
    # The view has moved since `read_at`: the same precondition is now stale.
    rc = cli.main(
        ["views", "update", view["id"], "--name", "late", "--expected-updated-at", read_at]
    )
    assert rc == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "view changed since it was loaded" in captured.err
    current = json.loads(captured.err.split("current: ", 1)[1])
    assert current["name"] == "ratio" and current["spec"]["expression"]["fn"] == "mul"


def test_views_update_needs_something_to_change(wired, capsys):
    assert cli.main(["views", "update", "v1"]) == 2
    assert cli.main(["views", "update", "v1", "--expected-updated-at", "2026-01-01T00:00:00Z"]) == 2
    assert _patches(wired) == []


def test_views_update_of_an_unknown_view_exits_non_zero(wired, capsys):
    assert cli.main(["views", "update", "no-such-view", "--name", "x"]) == 1
    captured = capsys.readouterr()
    assert "view not found" in captured.err and captured.out == ""


def test_views_update_refuses_a_bad_spec_before_sending(wired, capsys):
    rc = cli.main(["views", "update", "v1", "--spec", '{"op": "series", "key": "k"}'])
    assert rc == 2
    assert "invalid expression spec" in capsys.readouterr().err
    assert _patches(wired) == []


# ---------------------------------------------------------------- run set --status


def test_run_set_status_sends_the_status_and_no_timestamps(wired, tmp_path, capsys):
    run = _new_run(wired, tmp_path)
    row = wired.runs[run.id]
    row.update(
        status="completed",
        started_at="2026-09-01T00:00:00Z",
        ended_at="2026-09-01T06:00:00Z",
    )

    assert cli.main(["run", "set", run.id, "--status", "failed"]) == 0
    out = _json_out(capsys)
    assert out["status"] == "failed"
    (body,) = _patches(wired, f"/v1/runs/{run.id}")
    assert body["status"] == "failed"
    for clock in ("ended_at", "started_at", "write_epoch"):
        assert clock not in body, clock
    assert row["started_at"] == "2026-09-01T00:00:00Z"
    assert row["ended_at"] == "2026-09-01T06:00:00Z"


@pytest.mark.parametrize("status", ["completed", "failed", "crashed", "canceled"])
def test_run_set_takes_every_finished_status(wired, tmp_path, capsys, status):
    run = _new_run(wired, tmp_path)
    assert cli.main(["run", "set", run.id, "--status", status]) == 0
    assert wired.runs[run.id]["status"] == status


@pytest.mark.parametrize("status", ["created", "running", "untracked", "done"])
def test_run_set_refuses_anything_but_a_finished_status(wired, tmp_path, capsys, status):
    """`created`/`running` on a finished run skip the reopen guard, and the
    reaper later marks it crashed and emails the launcher; `untracked` is the
    reaper's own verdict. None of them is a correction."""
    run = _new_run(wired, tmp_path)
    assert cli.main(["run", "set", run.id, "--status", status]) == 2
    assert _patches(wired, f"/v1/runs/{run.id}") == []


def test_run_set_status_help_says_failed_emails_the_launcher():
    import typer

    command = typer.main.get_command(cli_main.app).commands["run"].commands["set"]
    (status,) = [p for p in command.params if p.name == "status"]
    assert "failed" in status.help and "emails" in status.help


def test_run_set_status_refused_by_the_server_exits_non_zero(wired, tmp_path, monkeypatch, capsys):
    run = _new_run(wired, tmp_path)
    _intercept(
        wired,
        monkeypatch,
        lambda r: httpx.Response(409, json={"detail": "stale write_epoch"})
        if r.method == "PATCH"
        else None,
    )
    assert cli.main(["run", "set", run.id, "--status", "failed"]) == 1
    captured = capsys.readouterr()
    assert "stale write_epoch" in captured.err and captured.out == ""


# ------------------------------------------------- tags in project / experiment set


def test_project_set_changes_fields_and_tags_in_one_patch(wired, capsys):
    project = _project(wired)
    project["tags"] = ["baseline", "old"]

    rc = cli.main(
        [
            "project", "set", "p", "--name", "Renamed",
            "--add-tag", "Ablation", "--remove-tag", "old",
        ]
    )
    assert rc == 0
    capsys.readouterr()
    (body,) = _patches(wired, "/v1/projects/")
    assert body["name"] == "Renamed"
    assert body["tags"] == ["baseline", "ablation"]
    assert project["tags"] == ["baseline", "ablation"] and project["name"] == "Renamed"


def test_project_set_tags_alone_replace_and_clear(wired, capsys):
    project = _project(wired)
    project["tags"] = ["a", "b"]
    assert cli.main(["project", "set", "p", "--set-tags", "x", "--set-tags", "y"]) == 0
    assert project["tags"] == ["x", "y"]
    assert cli.main(["project", "set", "p", "--set-tags", ""]) == 0
    capsys.readouterr()
    assert project["tags"] == []


def test_project_set_with_tags_already_so_writes_nothing(wired, capsys):
    _project(wired)["tags"] = ["a"]
    assert cli.main(["project", "set", "p", "--add-tag", "a", "--remove-tag", "zzz"]) == 0
    assert _json_out(capsys)["tags"] == ["a"]
    assert _patches(wired, "/v1/projects/") == []


def test_project_set_sends_unchanged_tags_beside_a_field_change(wired, capsys):
    """Changed or not, the list rides with the other fields: a retried command
    then sends the body it sent the first time (Idempotency-Key replay)."""
    _project(wired)["tags"] = ["a"]
    assert cli.main(["project", "set", "p", "--name", "N", "--add-tag", "a"]) == 0
    capsys.readouterr()
    (body,) = _patches(wired, "/v1/projects/")
    assert body["tags"] == ["a"] and body["name"] == "N"


@pytest.mark.parametrize(
    "argv",
    [
        ["project", "set", "p", "--set-tags", "x", "--add-tag", "y"],
        ["project", "set", "p", "--set-tags", "x", "--remove-tag", "y"],
        ["project", "set", "p", "--add-tag", "x", "--remove-tag", "X"],
        ["project", "set", "p"],
        ["experiment", "set", "e"],
        ["experiment", "set", "e", "--set-tags", "x", "--add-tag", "y"],
    ],
)
def test_set_refuses_contradictions_and_empty_edits(wired, capsys, argv):
    assert cli.main(argv) == 2
    assert _patches(wired) == []


def test_experiment_set_edits_through_the_experiment_route(wired, capsys):
    """Light experiments R4: the question and name go to
    `PATCH /v1/projects/{P}/experiments/{E}`, never the project address."""
    experiment = _experiment(wired)
    rc = cli.main(["experiment", "set", "e", "--question", "does warmup help?", "--name", "Warmup"])
    assert rc == 0
    capsys.readouterr()
    (body,) = _patches(wired, f"/experiments/{experiment['id']}")
    assert body["question"] == "does warmup help?" and body["name"] == "Warmup"
    assert _patches(wired, f"/v1/projects/{experiment['id']}") == []
    assert experiment["question"] == "does warmup help?"


def test_experiment_tag_flags_are_refused_and_write_nothing(wired, capsys):
    """An experiment's tags are read-only since it moved to its own record (the
    server refuses tag writes on one since R3), so every tag flag says so."""
    experiment = _experiment(wired)
    experiment["tags"] = ["sweep"]
    assert cli.main(["experiment", "set", "e", "--question", "q?", "--add-tag", "warmup"]) != 0
    assert cli.main(["experiment", "tag", "e", "warmup"]) != 0
    assert cli.main(["experiment", "list", "--tag", "warmup"]) != 0
    assert "read-only" in capsys.readouterr().err
    assert _patches(wired) == []
    assert experiment["tags"] == ["sweep"]


def test_a_refused_set_with_tags_writes_neither_half(wired, monkeypatch, capsys):
    project = _project(wired)
    project["tags"] = ["a"]
    _intercept(
        wired,
        monkeypatch,
        lambda r: httpx.Response(422, json={"detail": "name too long"})
        if r.method == "PATCH"
        else None,
    )
    assert cli.main(["project", "set", "p", "--name", "N", "--add-tag", "b"]) == 1
    captured = capsys.readouterr()
    assert "name too long" in captured.err and captured.out == ""
    assert project["tags"] == ["a"] and project.get("name") != "N"
