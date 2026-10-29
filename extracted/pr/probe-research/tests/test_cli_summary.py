"""`probe summary checkout|push`, `probe visuals options|set` and the reminder
(plan writer-owns-summary §3.4, §3.5, §3.8; CONTRACT.md "CLI"), driven end to
end through the CLI against a fake of the server's summary and visuals routes
with production's status codes (200 / 409 / 422 / 503).
"""

from __future__ import annotations

import json
import os
import re
import uuid
from pathlib import Path

import httpx
import pytest

from probe import cli
from probe.cli import summary_cli
from tests.conftest import make_client

SID_A = "aaaaaaaa-1111-4111-8111-aaaaaaaaaaaa"
SID_B = "bbbbbbbb-2222-4222-8222-bbbbbbbbbbbb"
_ANCHOR = re.compile(r"(/v1/projects/[^/]+(?:/experiments/[^/]+)?)/(summary|visuals)(/.*)?")


class SummaryServer:
    """The summary and visuals routes of CONTRACT.md over a FakeApp: one page
    per anchor path, its version bumped by every write (summary or visuals)."""

    def __init__(self, app) -> None:
        self.pages: dict[str, dict] = {}
        self.mode = "recorder"
        #: What `.../visuals/options` says about the entity carrying tables and charts.
        self.eligible = True
        self.calls: list[tuple[str, str, dict]] = []
        inner = app.handler

        def handler(request: httpx.Request) -> httpx.Response:
            found = _ANCHOR.fullmatch(request.url.path)
            if found is None:
                return inner(request)
            body = json.loads(request.content) if request.content else {}
            self.calls.append((request.method, request.url.path, body))
            return self.serve(
                request.method, found.group(1), found.group(2), found.group(3) or "", body
            )

        app.handler = handler

    def page(self, anchor: str) -> dict:
        return self.pages.setdefault(
            anchor, {"markdown": "", "version": 0, "visuals": [], "erased_at": None}
        )

    def anchor_of(self, suffix: str) -> str:
        return next(a for a in self.pages if a.endswith(suffix))

    def write(self, anchor: str, markdown: str) -> None:
        """Another writer's push."""
        page = self.page(anchor)
        page["markdown"], page["version"] = markdown, page["version"] + 1

    @staticmethod
    def _detail(status: int, **detail) -> httpx.Response:
        return httpx.Response(status, json={"detail": detail})

    def serve(self, method: str, anchor: str, what: str, rest: str, body: dict) -> httpx.Response:
        page = self.page(anchor)
        if what == "summary" and method == "GET" and not rest:
            return httpx.Response(
                200,
                json={
                    "markdown": page["markdown"],
                    "version": page["version"],
                    "edited_at": None,
                    "edited_by": "Richard",
                    "via": "cli",
                    "session_title": None,
                    "you": "Richard",
                    "today": "2026-10-15",
                    "mode": self.mode,
                },
            )
        if method == "PUT" and self.mode == "lane":
            return self._detail(
                503, code="summary_writer_off", message="summaries are the lane's on this team"
            )
        expected = int(body.get("expected_version", -1))
        if what == "summary" and method == "PUT":
            if page["erased_at"] is not None and expected < page["erased_at"]:
                return self._detail(
                    409,
                    code="erased_since_checkout",
                    version=page["version"],
                    markdown=page["markdown"],
                )
            if expected != page["version"]:
                return self._detail(
                    409, code="version_moved", version=page["version"], markdown=page["markdown"]
                )
            if len(body["markdown"]) > 12_000:
                return self._detail(
                    422,
                    code="too_long",
                    message=f"{len(body['markdown']):,} characters of "
                    "summary text, over the 12,000 the server keeps",
                )
            page["markdown"], page["version"] = body["markdown"], page["version"] + 1
            return httpx.Response(
                200, json={"version": page["version"], "markdown": page["markdown"]}
            )
        if what == "visuals" and rest == "/options":
            return httpx.Response(
                200,
                json={
                    "scope": "experiment" if "/experiments/" in anchor else "project",
                    "eligible": self.eligible,
                    "reason": None,
                    "runs": [],
                    "runs_truncated": False,
                    "metrics": ["eval/acc"],
                    "configs": [],
                    "groups": [],
                    "caps": {"max_visuals": 8},
                    "current": page["visuals"],
                    "version": page["version"],
                },
            )
        if what == "visuals" and method == "PUT":
            if expected != page["version"]:
                return self._detail(
                    409, code="version_moved", version=page["version"], current=page["visuals"]
                )
            if any(not isinstance(v, dict) or "kind" not in v for v in body["visuals"]):
                return self._detail(
                    422, code="visuals_refused", message="visual 0: `kind` is required"
                )
            page["visuals"], page["version"] = body["visuals"], page["version"] + 1
            return httpx.Response(
                200,
                json={
                    "version": page["version"],
                    "visuals": [{"id": v.get("id"), "kind": v["kind"]} for v in body["visuals"]],
                },
            )
        return httpx.Response(404, json={"detail": "Not Found"})


@pytest.fixture
def server(app, tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    fake = SummaryServer(app)

    def factory(**_kw):
        return make_client(app, tmp_spool=tmp_path / "spool")

    monkeypatch.setattr(cli, "Client", factory)
    assert cli.main(["project", "create", "--kind", "general", "p"]) == 0
    assert (
        cli.main(["experiment", "create", "e", "--question", "does it work?", "--project", "p"])
        == 0
    )
    return fake


def _out(capsys) -> dict:
    return json.loads(capsys.readouterr().out)


def _session(monkeypatch, sid: str | None) -> None:
    if sid is None:
        monkeypatch.delenv("PROBE_DAEMON_SESSION", raising=False)
    else:
        monkeypatch.setenv("PROBE_DAEMON_SESSION", sid)


def _checkout(capsys, *flags: str) -> dict:
    capsys.readouterr()
    assert cli.main(["summary", "checkout", *flags]) == 0
    return _out(capsys)


def _push(capsys, *flags: str) -> tuple[int, dict, str]:
    capsys.readouterr()
    code = cli.main(["summary", "push", *flags])
    captured = capsys.readouterr()
    return code, json.loads(captured.out) if captured.out.strip() else {}, captured.err


# ---------------------------------------------------------------------------
# checkout and push
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "flags", [("--project", "p"), ("--experiment", "e"), ("--experiment", "e", "--project", "p")]
)
def test_checkout_writes_this_sessions_draft_and_prints_the_contract_json(
    server, capsys, monkeypatch, flags
):
    _session(monkeypatch, SID_A)
    out = _checkout(capsys, *flags)
    kind = "experiment" if "--experiment" in flags else "project"
    assert set(out) == {
        "target",
        "label",
        "path",
        "version",
        "markdown",
        "you",
        "today",
        "edited_by",
        "edited_at",
        "mode",
        "visuals",
    }
    assert out["visuals"] == {"eligible": True, "count": 0}
    assert (out["target"], out["version"], out["markdown"], out["you"], out["today"]) == (
        kind,
        0,
        "",
        "Richard",
        "2026-10-15",
    )
    path = Path(out["path"])
    assert path.name == f"{SID_A}.daemon.md" and path.parent.parent.name == kind
    assert path.parent.parent.parent == Path(os.environ["XDG_STATE_HOME"]) / "probe" / "summaries"
    for name in (f"{SID_A}.daemon.md", f"{SID_A}.daemon.base", f"{SID_A}.daemon.meta.json"):
        assert oct((path.parent / name).stat().st_mode)[-3:] == "600", name
    path.write_text("Does it work?\n\n**Where it stands (Oct 15):** yes.\n")
    code, pushed, _err = _push(capsys, *flags)
    assert code == 0 and pushed["pushed"] is True and pushed["version"] == 1
    method, route, body = server.calls[-1]
    assert (
        method == "PUT"
        and route.endswith("/summary")
        and ("/experiments/" in route) == (kind == "experiment")
    )
    assert body == {
        "markdown": path.read_text(),
        "expected_version": 0,
        "session_id": SID_A,
        "directed": False,
    }


def test_two_sessions_on_one_machine_never_lose_each_others_text(server, capsys, monkeypatch):
    """Per-session drafts (D13): both check out the same clean page; neither
    overwrites the other's file, and the second push merges onto the first."""
    _session(monkeypatch, SID_A)
    _checkout(capsys, "--project", "p")
    anchor = server.anchor_of("")
    server.write(anchor, "intro\n\nmiddle\n\nend\n")
    a = _checkout(capsys, "--project", "p")
    _session(monkeypatch, SID_B)
    b = _checkout(capsys, "--project", "p")
    assert a["path"] != b["path"]
    Path(a["path"]).write_text("intro A\n\nmiddle\n\nend\n")
    Path(b["path"]).write_text("intro\n\nmiddle\n\nend B\n")
    _session(monkeypatch, SID_A)
    assert _push(capsys, "--project", "p")[0] == 0
    _session(monkeypatch, SID_B)
    code, out, _ = _push(capsys, "--project", "p")
    assert code == 0 and out["merged"] is True and out["pushed"] is False
    assert [c[0] for c in server.calls[-2:]] == ["PUT", "PUT"], (
        "the 409 carried the head: no second read"
    )
    code, out, _ = _push(capsys, "--project", "p")
    assert code == 0 and out["pushed"] is True
    assert server.pages[anchor]["markdown"] == "intro A\n\nmiddle\n\nend B\n"


def test_a_conflict_is_written_into_the_file_and_exits_2(server, capsys, monkeypatch):
    _session(monkeypatch, SID_A)
    _checkout(capsys, "--experiment", "e")
    anchor = server.anchor_of("")
    server.write(anchor, "a line\n")
    path = Path(_checkout(capsys, "--experiment", "e")["path"])
    path.write_text("mine\n")
    server.write(anchor, "theirs\n")
    code, pushed, _ = _push(capsys, "--experiment", "e")
    assert code == 2 and pushed["conflicted"] is True
    assert "<<<<<<<" in path.read_text()
    code, _, err = _push(capsys, "--experiment", "e")
    assert code == 2 and "conflict markers" in err, "an unresolved file is never sent"


def test_erased_since_checkout_is_not_merged_and_asks_for_a_fresh_checkout(
    server, capsys, monkeypatch
):
    _session(monkeypatch, SID_A)
    out = _checkout(capsys, "--project", "p")
    anchor = server.anchor_of("")
    path = Path(out["path"])
    base = path.with_suffix(".base").read_text()
    path.write_text("my edit, grown from the erased text\n")
    server.write(anchor, "rolled back\n")
    server.pages[anchor]["erased_at"] = server.pages[anchor]["version"]
    gets_before = sum(1 for c in server.calls if c[0] == "GET")
    code, pushed, err = _push(capsys, "--project", "p")
    assert code == 2 and pushed["pushed"] is False and pushed["merged"] is False
    assert "check out again" in pushed["detail"] and "probe summary checkout --project p" in err
    assert path.read_text() == "my edit, grown from the erased text\n", "the file keeps its edits"
    assert path.with_suffix(".base").read_text() == base, "nothing was merged onto the erased page"
    assert sum(1 for c in server.calls if c[0] == "GET") == gets_before
    assert "--steal" in pushed["detail"]
    # The draft still holds those edits: a checkout replaces it only with
    # --steal (review of #3034, finding 3), then pushes.
    capsys.readouterr()
    assert cli.main(["summary", "checkout", "--project", "p"]) == 2
    assert path.read_text() == "my edit, grown from the erased text\n"
    out = _checkout(capsys, "--project", "p", "--steal")
    assert out["markdown"] == "rolled back\n"
    Path(out["path"]).write_text("rolled back\nand mine\n")
    assert _push(capsys, "--project", "p")[0] == 0


def test_the_lane_s_503_and_a_422_exit_1_with_the_servers_words(server, capsys, monkeypatch):
    _session(monkeypatch, SID_A)
    server.mode = "lane"
    out = _checkout(capsys, "--project", "p")
    assert out["mode"] == "lane"
    Path(out["path"]).write_text("hello\n")
    code, pushed, err = _push(capsys, "--project", "p")
    assert code == 1 and pushed["pushed"] is False and "lane's on this team" in err
    server.mode = "recorder"
    Path(out["path"]).write_text("x" * 12_001)
    code, pushed, err = _push(capsys, "--project", "p")
    assert code == 1 and "12,000" in pushed["detail"]


def test_without_a_session_the_shared_file_is_claimed_like_a_note(server, capsys, monkeypatch):
    _session(monkeypatch, None)
    out = _checkout(capsys, "--project", "p")
    path = Path(out["path"])
    assert path.name == "note.md"
    path.write_text("unpushed\n")
    capsys.readouterr()
    assert cli.main(["summary", "checkout", "--project", "p"]) == 2
    assert "--steal" in capsys.readouterr().err
    assert cli.main(["summary", "checkout", "--project", "p", "--steal"]) == 0


def test_push_without_a_checkout_says_so_and_exits_1(server, capsys, monkeypatch):
    _session(monkeypatch, SID_B)
    code, _, err = _push(capsys, "--project", "p")
    assert code == 1 and "probe summary checkout --project p" in err


def test_directed_reaches_the_server_from_anywhere_on_the_line(server, capsys, monkeypatch):
    _session(monkeypatch, SID_A)
    out = _checkout(capsys, "--project", "p")
    Path(out["path"]).write_text("asked for\n")
    capsys.readouterr()
    assert cli.main(["--directed", "summary", "push", "--project", "p"]) == 0
    assert server.calls[-1][2]["directed"] is True


def test_a_page_the_server_rewrites_becomes_the_base(server, capsys, monkeypatch):
    """What a fresh GET returns after the push (a person's block expanded, the
    renderer's spelling) is the next push's ancestor."""
    _session(monkeypatch, SID_A)
    out = _checkout(capsys, "--project", "p")
    anchor = server.anchor_of("")
    original = server.serve

    def normalizing(method, a, what, rest, body):
        answer = original(method, a, what, rest, body)
        if method == "PUT" and what == "summary" and answer.status_code == 200:
            server.pages[a]["markdown"] = body["markdown"].replace("*", "_")
            return httpx.Response(
                200,
                json={
                    "version": server.pages[a]["version"],
                    "markdown": server.pages[a]["markdown"],
                },
            )
        return answer

    server.serve = normalizing
    path = Path(out["path"])
    path.write_text("*Where it stands*\n")
    assert _push(capsys, "--project", "p")[0] == 0
    assert path.read_text() == "_Where it stands_\n" == path.with_suffix(".base").read_text()
    assert server.pages[anchor]["markdown"] == "_Where it stands_\n"


# ---------------------------------------------------------------------------
# visuals
# ---------------------------------------------------------------------------


def test_visuals_options_writes_a_draft_and_set_sends_it(server, capsys, monkeypatch):
    _session(monkeypatch, SID_A)
    capsys.readouterr()
    assert cli.main(["visuals", "options", "--experiment", "e"]) == 0
    options = _out(capsys)
    assert options["scope"] == "experiment" and options["metrics"] == ["eval/acc"]
    draft = Path(options["path"])
    assert json.loads(draft.read_text()) == [] and oct(draft.stat().st_mode)[-3:] == "600"
    draft.write_text(json.dumps([{"id": "acc", "kind": "table", "title": "Accuracy"}]))
    assert cli.main(["visuals", "set", "--experiment", "e"]) == 0
    out = _out(capsys)
    assert out["set"] is True and out["visuals"] == [{"id": "acc", "kind": "table"}]
    method, route, body = server.calls[-1]
    assert method == "PUT" and route.endswith("/visuals") and body["expected_version"] == 0
    assert body["directed"] is False


def test_visuals_set_refusals(server, capsys, monkeypatch, tmp_path):
    _session(monkeypatch, SID_A)
    spec = tmp_path / "v.json"
    spec.write_text(json.dumps({"visuals": [{"id": "x"}]}))
    capsys.readouterr()
    assert cli.main(["visuals", "set", "--project", "p", "--file", str(spec)]) == 1
    assert "`kind` is required" in capsys.readouterr().err
    spec.write_text(json.dumps([{"id": "x", "kind": "table"}]))
    assert (
        cli.main(["visuals", "set", "--project", "p", "--file", str(spec), "--version", "7"]) == 2
    )
    captured = capsys.readouterr()
    assert json.loads(captured.out)["current"] == [] and "moved" in captured.err
    server.mode = "lane"
    assert cli.main(["visuals", "set", "--project", "p", "--file", str(spec)]) == 1


def test_an_old_server_says_it_predates_summaries(app, tmp_path, monkeypatch, capsys):
    """FastAPI's own 404 for a route the server does not have."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    inner = app.handler
    app.handler = lambda request: (
        httpx.Response(404, json={"detail": "Not Found"})
        if _ANCHOR.fullmatch(request.url.path)
        else inner(request)
    )
    monkeypatch.setattr(cli, "Client", lambda **_kw: make_client(app, tmp_spool=tmp_path / "spool"))
    assert cli.main(["project", "create", "--kind", "general", "p"]) == 0
    capsys.readouterr()
    assert cli.main(["summary", "checkout", "--project", "p"]) == 1
    assert "predates recorder summaries" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# the reminder (§3.5, D11)
# ---------------------------------------------------------------------------


def _reminders(err: str) -> list[str]:
    return [line for line in err.splitlines() if line.startswith("Summary of ")]


def test_the_reminder_is_the_approved_line():
    assert summary_cli.REMINDER.format(label="willow", kind="project") == (
        "Summary of willow not loaded this session - probe summary checkout --project willow"
    )


def test_the_first_write_to_an_entity_reminds_once_per_session(server, capsys, monkeypatch):
    _session(monkeypatch, SID_A)
    capsys.readouterr()
    assert cli.main(["experiment", "set", "e", "--question", "does it still work?"]) == 0
    first = _reminders(capsys.readouterr().err)
    # An experiment write names the experiment, not its project.
    assert first == ["Summary of e not loaded this session - probe summary checkout --experiment e"]
    assert cli.main(["experiment", "set", "e", "--question", "and now?"]) == 0
    assert _reminders(capsys.readouterr().err) == [], "once per session per entity"
    assert cli.main(["project", "set", "p", "--name", "P"]) == 0
    assert _reminders(capsys.readouterr().err) == [
        "Summary of p not loaded this session - probe summary checkout --project p"
    ]
    _session(monkeypatch, SID_B)  # another session is told again
    assert cli.main(["project", "set", "p", "--name", "P2"]) == 0
    assert len(_reminders(capsys.readouterr().err)) == 1


def test_no_reminder_after_a_checkout_or_for_an_unscoped_write(server, capsys, monkeypatch):
    _session(monkeypatch, SID_A)
    _checkout(capsys, "--experiment", "e")
    assert cli.main(["experiment", "set", "e", "--question", "q2"]) == 0
    assert _reminders(capsys.readouterr().err) == [], "loaded this session"
    # By any spelling the checkout resolved: its id too.
    eid = server.anchor_of("").rsplit("/", 1)[-1]
    assert summary_cli.landing(["experiment", "set", f"id:{eid}", "--question", "q"]) == (
        "experiment",
        f"id:{eid}",
    )
    assert cli.main(["experiment", "set", f"id:{eid}", "--question", "q3"]) == 0
    assert _reminders(capsys.readouterr().err) == []
    assert summary_cli.landing(["run", "tag", "r1", "x"]) is None, (
        "unscoped: names no project or experiment"
    )
    assert summary_cli.landing(["run", "move", "r1", "--to", "p"]) is None, (
        "could be either: names nothing"
    )
    assert summary_cli.landing(["project", "list"]) is None, "a read"
    assert summary_cli.landing(["summary", "push", "--project", "p"]) is None, "the summary itself"
    assert summary_cli.landing(
        ["experiment", "create", "x2", "--project", "p", "--question", "q"]
    ) == ("experiment", "x2")
    assert summary_cli.landing(["notes", "push", "--experiment", "e", "--project", "p"]) == (
        "experiment",
        "e",
    )


def test_no_reminder_without_a_session_inside_a_run_or_where_the_daemon_records(
    server, capsys, monkeypatch
):
    from probe.sdk import session_marker

    _session(monkeypatch, None)
    assert cli.main(["project", "set", "p", "--name", "P"]) == 0
    assert _reminders(capsys.readouterr().err) == []
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID_B)
    monkeypatch.setenv("PROBE_RUN_ID", str(uuid.uuid4()))
    assert cli.main(["project", "set", "p", "--name", "P3"]) == 0
    assert _reminders(capsys.readouterr().err) == [], "a run recording its own data"
    monkeypatch.delenv("PROBE_RUN_ID")
    session_marker.sessions_dir().mkdir(parents=True, exist_ok=True)
    (session_marker.sessions_dir() / f"{SID_B}.state").write_text(session_marker.STATE_DAEMON)
    monkeypatch.setattr(
        session_marker, "agent_writes_freely", lambda *_a: True
    )  # no live lease needed here
    assert cli.main(["--directed", "project", "set", "p", "--name", "P4"]) == 0
    assert _reminders(capsys.readouterr().err) == [], "the daemon keeps this session's summaries"
    (session_marker.sessions_dir() / f"{SID_B}.state").write_text(session_marker.STATE_FULL)
    assert cli.main(["project", "set", "p", "--name", "P5"]) == 0
    assert len(_reminders(capsys.readouterr().err)) == 1, "the agent records: it keeps them"



def _checkout_err(capsys, *flags: str) -> tuple[dict, str]:
    capsys.readouterr()
    assert cli.main(["summary", "checkout", *flags]) == 0
    captured = capsys.readouterr()
    return json.loads(captured.out), captured.err


def test_checkout_names_unset_tables_and_charts_and_stays_quiet_once_set(server, capsys, monkeypatch):
    """Plan 3.8: the hint rides the checkout, the moment the entity is handed over."""
    _session(monkeypatch, SID_A)
    out, err = _checkout_err(capsys, "--experiment", "e", "--project", "p")
    assert out["visuals"] == {"eligible": True, "count": 0}
    assert "Tables and charts for e: none set - read overview-visuals, then probe visuals options --experiment e" in err
    anchor = next(a for a in server.pages if "/experiments/" in a)
    server.pages[anchor]["visuals"] = [{"id": "acc", "kind": "table"}]
    out, err = _checkout_err(capsys, "--experiment", "e", "--project", "p")
    assert out["visuals"] == {"eligible": True, "count": 1}
    assert "Tables and charts" not in err


def test_checkout_in_lane_mode_asks_nothing_about_tables(server, capsys, monkeypatch):
    _session(monkeypatch, SID_A)
    server.mode = "lane"
    out, err = _checkout_err(capsys, "--project", "p")
    assert out["visuals"] is None and "Tables and charts" not in err
    assert not any(c[1].endswith("/visuals/options") for c in server.calls)
    # Since writer-owns-summary R2 no lane writes a `lane` team's summaries:
    # the note says the door is closed and who opens it, with the daemon's mark.
    assert "summary door is closed (summaries_by=lane) (mode lane)" in err
    assert "ask Probe (support@prbe.ai)" in err and "overview lane" not in err


# ---------------------------------------------------------------------------
# review (2026-10-16): drafts, erasure, versions, keys
# ---------------------------------------------------------------------------


def test_the_agents_own_checkout_never_replaces_the_daemons_draft(server, capsys, monkeypatch):
    """The daemon records the agent's session under the agent's own id: the
    daemon's draft is `<sid>.daemon.md`, so a checkout the agent makes in the
    same session never discards the daemon's unpushed edits."""
    _session(monkeypatch, SID_A)
    daemon = Path(_checkout(capsys, "--project", "p")["path"])
    daemon.write_text("the daemon's unpushed edit\n")
    _session(monkeypatch, None)
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID_A)
    agent = Path(_checkout(capsys, "--project", "p")["path"])
    assert agent.name == f"{SID_A}.md" and agent != daemon
    assert daemon.read_text() == "the daemon's unpushed edit\n"


def test_session_erased_is_refused_without_a_merge(server, capsys, monkeypatch):
    _session(monkeypatch, SID_A)
    path = Path(_checkout(capsys, "--project", "p")["path"])
    base = path.with_suffix(".base").read_text()
    path.write_text("edit\n")
    original = server.serve

    def erased(method, anchor, what, rest, body):
        if (method, what) == ("PUT", "summary"):
            return server._detail(409, code="session_erased", version=1, markdown="x")
        return original(method, anchor, what, rest, body)

    server.serve = erased
    code, pushed, err = _push(capsys, "--project", "p")
    assert code == 2 and pushed["merged"] is False and "this session was erased" in err
    assert path.with_suffix(".base").read_text() == base and path.read_text() == "edit\n"


def test_a_409_without_the_head_merges_from_a_read(server, capsys, monkeypatch):
    _session(monkeypatch, SID_A)
    path = Path(_checkout(capsys, "--project", "p")["path"])
    anchor = server.anchor_of("")
    server.write(anchor, "theirs\n\nshared\n")
    path.write_text("mine\n")
    original = server.serve

    def bare(method, a, what, rest, body):
        answer = original(method, a, what, rest, body)
        if answer.status_code == 409:
            return server._detail(409, code="version_moved", version=server.pages[a]["version"])
        return answer

    server.serve = bare
    code, pushed, _ = _push(capsys, "--project", "p")
    assert pushed["pushed"] is False and (pushed["merged"] or pushed["conflicted"])
    assert [c[0] for c in server.calls[-2:]] == ["PUT", "GET"], "the head came from a read"


def test_a_draft_from_another_server_is_never_pushed(server, capsys, monkeypatch):
    _session(monkeypatch, SID_A)
    path = Path(_checkout(capsys, "--project", "p")["path"])
    path.write_text("production prose\n")
    path.with_suffix(".owner").write_text("https://other-probe.example")
    puts = sum(1 for c in server.calls if c[0] == "PUT")
    code, _, err = _push(capsys, "--project", "p")
    assert code == 1 and "another Probe server or key" in err
    assert sum(1 for c in server.calls if c[0] == "PUT") == puts


def test_a_refused_key_reaches_main_in_the_daemons_words(server, capsys, monkeypatch):
    from probe.sdk.key_refusal import KEY_REFUSED_LINE

    _session(monkeypatch, SID_A)
    path = Path(_checkout(capsys, "--project", "p")["path"])
    path.write_text("edit\n")
    original = server.serve
    server.serve = lambda m, a, w, r, b: (
        httpx.Response(401, json={"detail": "invalid API key"}) if m == "PUT" else original(m, a, w, r, b)
    )
    code, _, err = _push(capsys, "--project", "p")
    assert code == 1 and KEY_REFUSED_LINE in err.splitlines()
    spec = Path(os.environ["XDG_STATE_HOME"]) / "v.json"
    spec.write_text(json.dumps([{"id": "x", "kind": "table"}]))
    capsys.readouterr()
    assert cli.main(["visuals", "set", "--project", "p", "--file", str(spec)]) == 1
    assert KEY_REFUSED_LINE in capsys.readouterr().err.splitlines()


def test_visuals_set_sends_the_version_options_read(server, capsys, monkeypatch):
    """Both reviews: `set` without `--version` used to read the page's version
    just before the PUT, so a list someone set after `options` was overwritten."""
    _session(monkeypatch, SID_A)
    capsys.readouterr()
    assert cli.main(["visuals", "options", "--experiment", "e"]) == 0
    draft = Path(_out(capsys)["path"])
    exp_anchor = next(a for a in server.pages if "/experiments/" in a)
    server.pages[exp_anchor]["visuals"] = [{"id": "theirs", "kind": "table"}]
    server.pages[exp_anchor]["version"] += 1
    draft.write_text(json.dumps([{"id": "mine", "kind": "table"}]))
    assert cli.main(["visuals", "set", "--experiment", "e"]) == 2
    captured = capsys.readouterr()
    assert json.loads(captured.out)["current"] == [{"id": "theirs", "kind": "table"}]
    assert server.pages[exp_anchor]["visuals"] == [{"id": "theirs", "kind": "table"}], "nothing overwritten"
    assert cli.main(["visuals", "options", "--experiment", "e"]) == 0
    capsys.readouterr()
    draft.write_text(json.dumps([{"id": "mine", "kind": "table"}]))
    assert cli.main(["visuals", "set", "--experiment", "e"]) == 0
    capsys.readouterr()
    assert cli.main(["visuals", "set", "--experiment", "e"]) == 0, "a set remembers the version it made"


def test_a_push_does_not_stale_the_tables_this_session_read(server, capsys, monkeypatch):
    """Bench 10-16: every `visuals set` after the same session's `summary push`
    was refused for the push's own bump (21 of 42 visuals commands a session)."""
    _session(monkeypatch, SID_A)
    capsys.readouterr()
    assert cli.main(["visuals", "options", "--experiment", "e"]) == 0
    draft = Path(_out(capsys)["path"])
    where = Path(_checkout(capsys, "--experiment", "e")["path"])
    where.write_text("Result: 0.91 accuracy.\n")
    code, out, _ = _push(capsys, "--experiment", "e")
    assert code == 0 and out["pushed"] and out["version"] == 1
    draft.write_text(json.dumps([{"id": "acc", "kind": "table"}]))
    assert cli.main(["visuals", "set", "--experiment", "e"]) == 0
    assert server.calls[-1][2]["expected_version"] == 1


def test_a_tables_set_does_not_make_the_next_push_merge(server, capsys, monkeypatch):
    _session(monkeypatch, SID_A)
    where = Path(_checkout(capsys, "--experiment", "e")["path"])
    capsys.readouterr()
    assert cli.main(["visuals", "options", "--experiment", "e"]) == 0
    Path(_out(capsys)["path"]).write_text(json.dumps([{"id": "acc", "kind": "table"}]))
    assert cli.main(["visuals", "set", "--experiment", "e"]) == 0
    where.write_text("Result: 0.91 accuracy.\n")
    puts = sum(1 for m, r, _ in server.calls if m == "PUT" and r.endswith("/summary"))
    code, out, _ = _push(capsys, "--experiment", "e")
    assert code == 0 and out["pushed"] and not out["merged"] and out["version"] == 2
    assert sum(1 for m, r, _ in server.calls if m == "PUT" and r.endswith("/summary")) == puts + 1


def test_a_set_never_moves_the_remembered_tables_version_backwards(server, capsys, monkeypatch):
    """Review of #2964: a `summary push` of this session's landing while a `set`
    waits on its PUT moves the remembered version past the set's; the set's own
    write after it must not put the older one back."""
    _session(monkeypatch, SID_A)
    capsys.readouterr()
    assert cli.main(["visuals", "options", "--experiment", "e"]) == 0
    draft = Path(_out(capsys)["path"])
    meta = draft.with_name(f"{draft.stem}.meta.json")
    original = server.serve

    def push_lands_meanwhile(m, a, w, r, b):
        if w == "visuals" and m == "PUT":
            meta.write_text(json.dumps({"version": 5}))
        return original(m, a, w, r, b)

    server.serve = push_lands_meanwhile
    draft.write_text(json.dumps([{"id": "acc", "kind": "table"}]))
    assert cli.main(["visuals", "set", "--experiment", "e"]) == 0
    assert json.loads(meta.read_text())["version"] == 5


def test_a_push_follow_rechecks_the_tables_version_under_the_lock(server, capsys, monkeypatch):
    """The push's follow writes only if the version it saw is still remembered
    once it holds the lock: a set that moved it in between is not undone."""
    from probe.cli import summary_cli

    _session(monkeypatch, SID_A)
    capsys.readouterr()
    assert cli.main(["visuals", "options", "--experiment", "e"]) == 0
    draft = Path(_out(capsys)["path"])
    meta = draft.with_name(f"{draft.stem}.meta.json")
    seen = iter([0, 4])  # outside the lock: still v0; inside: a set has moved it to v4
    real = summary_cli._remembered_visuals_version
    monkeypatch.setattr(summary_cli, "_remembered_visuals_version", lambda d: next(seen, None) if d == draft else real(d))
    monkeypatch.setattr(summary_cli, "_visuals_draft", lambda target, sid: draft)
    meta.write_text(json.dumps({"version": 4}))
    summary_cli._visuals_follow_push(None, SID_A, 0, 1)
    assert json.loads(meta.read_text())["version"] == 4


def test_another_writers_bump_still_stales_both_halves(server, capsys, monkeypatch):
    _session(monkeypatch, SID_A)
    capsys.readouterr()
    assert cli.main(["visuals", "options", "--experiment", "e"]) == 0
    draft = Path(_out(capsys)["path"])
    server.write(next(a for a in server.pages if "/experiments/" in a), "theirs\n")
    where = Path(_checkout(capsys, "--experiment", "e")["path"])
    where.write_text("theirs\nmine\n")
    code, out, _ = _push(capsys, "--experiment", "e")
    assert code == 0 and out["pushed"] and out["version"] == 2
    draft.write_text(json.dumps([{"id": "acc", "kind": "table"}]))
    assert cli.main(["visuals", "set", "--experiment", "e"]) == 2, "options read v0; v1 was not this session's"


def test_a_tables_set_after_another_writers_push_leaves_the_summary_base_alone(server, capsys, monkeypatch):
    """Review: the summary half of the guard. A set landing v1 -> v2 says nothing
    about v0 -> v1 (another writer's text), so the next push still merges it in."""
    _session(monkeypatch, SID_A)
    where = Path(_checkout(capsys, "--experiment", "e")["path"])
    anchor = next(a for a in server.pages if "/experiments/" in a)
    server.write(anchor, "theirs\n")
    capsys.readouterr()
    assert cli.main(["visuals", "options", "--experiment", "e"]) == 0
    Path(_out(capsys)["path"]).write_text(json.dumps([{"id": "acc", "kind": "table"}]))
    assert cli.main(["visuals", "set", "--experiment", "e"]) == 0
    where.write_text("mine\n")
    code, out, _ = _push(capsys, "--experiment", "e")
    assert not out["pushed"] and (out["merged"] or out["conflicted"])
    assert server.pages[anchor]["markdown"] == "theirs\n", "their text was not overwritten"


def test_adopting_the_servers_text_leaves_a_draft_edited_after_the_send(tmp_path, monkeypatch):
    from probe.cli import notes_file

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    settings = type("Settings", (), {"base_url": "https://probe.example"})()
    where = notes_file.paths_for(settings, "project", "pid", root="summaries", draft="sid")
    notes_file.checkout(where, body="a\n", version=1)
    where.document.write_text("typed after the send\n")
    summary_cli._adopt_canonical(where, "a\n", "b\n", 2)
    assert where.document.read_text() == "typed after the send\n" and where.base.read_text() == "b\n"


def test_a_checkout_writes_the_document_before_its_version(tmp_path, monkeypatch):
    """Codex review: a checkout killed after the meta but before the document
    left the old text beside the new version, past the server's erasure check."""
    from probe.cli import note_sync, notes_file

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    settings = type("Settings", (), {"base_url": "https://probe.example"})()
    where = notes_file.paths_for(settings, "project", "pid", root="summaries", draft="sid")
    order: list[str] = []
    real = note_sync.write_text_atomic
    monkeypatch.setattr(note_sync, "write_text_atomic",
                        lambda path, text, **kw: (order.append(Path(path).name), real(path, text, **kw)))
    notes_file.checkout(where, body="page\n", version=3)
    assert order.index("sid.md") < order.index("sid.meta.json")


def test_visuals_set_never_guesses_the_drafts_version(server, capsys, monkeypatch, tmp_path):
    """Codex re-review: a draft whose recorded version is missing (an `options`
    killed between its two writes) is refused, never sent against the page's
    current version; a set from another file leaves the draft's version alone."""
    _session(monkeypatch, SID_A)
    capsys.readouterr()
    assert cli.main(["visuals", "options", "--experiment", "e"]) == 0
    draft = Path(_out(capsys)["path"])
    summary_cli._visuals_version_file(draft).unlink()
    draft.write_text(json.dumps([{"id": "a", "kind": "table"}]))
    assert cli.main(["visuals", "set", "--experiment", "e"]) == 1
    assert "`probe visuals options --experiment e` first" in capsys.readouterr().err
    assert cli.main(["visuals", "options", "--experiment", "e"]) == 0
    capsys.readouterr()
    other = tmp_path / "b.json"
    other.write_text(json.dumps([{"id": "b", "kind": "table"}]))
    assert cli.main(["visuals", "set", "--experiment", "e", "--file", str(other)]) == 0
    capsys.readouterr()
    assert cli.main(["visuals", "set", "--experiment", "e"]) == 2, "the draft still holds the list before b"


def test_no_reminder_while_the_team_was_last_seen_in_lane_mode(server, capsys, monkeypatch):
    """A lane team's summaries are refused: the reminder would only send every
    agent to a checkout that says so. One checkout per day per machine learns it."""
    _session(monkeypatch, None)
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID_A)
    server.mode = "lane"
    _checkout(capsys, "--project", "p")
    capsys.readouterr()
    assert cli.main(["experiment", "create", "lanex", "--question", "q?", "--project", "p"]) == 0
    assert _reminders(capsys.readouterr().err) == []
    server.mode = "recorder"
    _checkout(capsys, "--project", "p")
    capsys.readouterr()
    assert cli.main(["experiment", "create", "recx", "--question", "q?", "--project", "p"]) == 0
    # The agent's own session (no daemon): its first write checks the summary
    # out itself and names the draft (ARTIFACT-PAGES P3), in the reminder's place.
    (line,) = _reminders(capsys.readouterr().err)
    assert line.startswith("Summary of recx checked out for this session (v0): "), line
    assert Path(line.split(": ", 1)[1].split(" - ", 1)[0]).is_file()


def test_the_lane_memory_names_the_server_it_saw(server, capsys, monkeypatch):
    """Smoke, 2026-10-16: without `--base-url` the mode file said `"server": ""`,
    so a lane seen on one server quieted the reminder on every other."""
    _session(monkeypatch, None)
    server.mode = "lane"
    _checkout(capsys, "--project", "p")
    seen = json.loads(summary_cli._mode_file().read_text())
    assert seen["mode"] == "lane" and seen["server"] == summary_cli._settings().base_url != ""
