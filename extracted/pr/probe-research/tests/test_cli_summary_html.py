"""`probe summary checkout|push` against a server with full pages
(writer-owns-summary ARTIFACT-PAGES P1) and the first write's own checkout
(P3), end to end through the CLI against a fake of the summary routes:

* checkout asks for `?format=html`; the draft is `<sid>.html` holding the
  chart declarations as one `data-probe-series` block ahead of the page, the
  base beside it, the closed set beside it (`<sid>.chartable.json`);
* push sends the draft by its extension (`html`), merges a moved page with the
  same merge3 as Markdown, and adopts the server's canonical text;
* a server that ignores `format` gets Markdown, as before;
* the first `probe` write of an agent's own session checks the summary out and
  prints the draft's path; without a server answer, or over unpushed edits,
  it prints the reminder instead and the write still succeeds.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import httpx
import pytest

from probe import cli
from probe.cli import summary_cli
from tests.conftest import make_client

SID = "aaaaaaaa-1111-4111-8111-aaaaaaaaaaaa"
RUN = "0b2f8e3c-1111-4111-8111-111111111111"
_ANCHOR = re.compile(r"(/v1/projects/[^/]+(?:/experiments/[^/]+)?)/(summary|visuals)(/.*)?")
_BLOCK = re.compile(r"<script\b[^>]*data-probe-series[^>]*>(.*?)</script>\n?", re.S)

PAGE = (
    '<article class="ov-page">\n<p>Does warmup help? Yes.</p>\n'
    '<div id="c" class="ov-chart"></div>\n'
    "<script>PROBE.lineChart('c', 'loss', {title: 'Loss'})</script>\n</article>"
)
SERIES = [{"id": "loss", "metric": "train/loss", "run_ids": [RUN]}]
CHARTABLE = {
    "format": "by_run",
    "columns": ["kind", "key", "point_count"],
    "by_run": [{"run_id": RUN, "name": "w-3", "series": [["train", "train/loss", 3], ["eval", "val/loss", 1]]}],
    "caps": {"charts_per_page": 6},
}


class HtmlSummaryServer:
    """The summary routes with full pages: GET `?format=html`, PUT `html`
    (the series block lifted out, as the server does)."""

    def __init__(self, app) -> None:
        self.pages: dict[str, dict] = {}
        self.html = True
        self.fail_reads = False
        self.calls: list[tuple[str, str, dict, dict]] = []
        inner = app.handler

        def handler(request: httpx.Request) -> httpx.Response:
            found = _ANCHOR.fullmatch(request.url.path)
            if found is None:
                return inner(request)
            body = json.loads(request.content) if request.content else {}
            params = dict(request.url.params)
            self.calls.append((request.method, request.url.path, body, params))
            if self.fail_reads and request.method == "GET":
                return httpx.Response(500, json={"detail": "down"})
            return self.serve(request.method, found.group(1), found.group(2), found.group(3) or "", body, params)

        app.handler = handler

    def page(self, anchor: str) -> dict:
        return self.pages.setdefault(anchor, {"html": "", "series": [], "markdown": "", "version": 0})

    def anchor_of(self, suffix: str) -> str:
        return next(a for a in self.pages if a.endswith(suffix))

    def write(self, anchor: str, html: str, series: list | None = None) -> None:
        page = self.page(anchor)
        page["html"], page["version"] = html, page["version"] + 1
        if series is not None:
            page["series"] = series

    def serve(self, method, anchor, what, rest, body, params) -> httpx.Response:
        page = self.page(anchor)
        if what == "visuals":
            return httpx.Response(200, json={"eligible": False, "current": [], "version": page["version"]})
        if method == "GET" and not rest:
            row = {
                "markdown": page["markdown"],
                "version": page["version"],
                "edited_at": None,
                "edited_by": "Richard",
                "via": "cli",
                "session_title": None,
                "you": "Richard",
                "today": "2026-10-17",
                "mode": "recorder",
            }
            if self.html and params.get("format") == "html":
                row.update(format="html", markdown="", html=page["html"], series=page["series"],
                           chartable=CHARTABLE)
            return httpx.Response(200, json=row)
        if method == "PUT":
            if int(body["expected_version"]) != page["version"]:
                head = {"html": page["html"], "series": page["series"]} if "html" in body else {
                    "markdown": page["markdown"]}
                return httpx.Response(409, json={"detail": {"code": "version_moved", "version": page["version"],
                                                            **head}})
            if "html" in body:
                text = body["html"]
                found = _BLOCK.search(text)
                series = json.loads(found.group(1)) if found else body.get("series") or []
                html = (text[: found.start()] + text[found.end():]) if found else text
                page["html"], page["series"], page["version"] = html.strip(), series, page["version"] + 1
                return httpx.Response(200, json={"version": page["version"], "markdown": "",
                                                 "html": page["html"], "series": page["series"]})
            page["markdown"], page["version"] = body["markdown"], page["version"] + 1
            return httpx.Response(200, json={"version": page["version"], "markdown": page["markdown"]})
        return httpx.Response(404, json={"detail": "Not Found"})


@pytest.fixture
def server(app, tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    fake = HtmlSummaryServer(app)
    monkeypatch.setattr(cli, "Client", lambda **_kw: make_client(app, tmp_spool=tmp_path / "spool"))
    assert cli.main(["project", "create", "--kind", "general", "p"]) == 0
    assert cli.main(["experiment", "create", "e", "--question", "does it work?", "--project", "p"]) == 0
    return fake


def _daemon(monkeypatch) -> None:
    monkeypatch.setenv(summary_cli.DAEMON_SESSION_ENV, SID)


def _checkout(capsys, *flags: str) -> dict:
    capsys.readouterr()
    assert cli.main(["summary", "checkout", *flags]) == 0
    return json.loads(capsys.readouterr().out)


def _push(capsys, *flags: str) -> tuple[int, dict, str]:
    capsys.readouterr()
    code = cli.main(["summary", "push", *flags])
    out = capsys.readouterr()
    return code, json.loads(out.out) if out.out.strip() else {}, out.err


def test_checkout_writes_one_html_draft_with_its_series_block_and_the_closed_set_beside_it(
    server, capsys, monkeypatch
):
    _daemon(monkeypatch)
    old = _checkout(capsys, "--experiment", "e")  # empty page: still an html draft
    anchor = server.anchor_of("")
    server.write(anchor, PAGE, SERIES)
    stale_md = Path(old["path"]).with_suffix(".md")
    stale_md.write_text("an old Markdown draft\n")
    capsys.readouterr()
    assert cli.main(["summary", "checkout", "--experiment", "e"]) == 2, "unpushed edits: not replaced"
    out = _checkout(capsys, "--experiment", "e", "--steal")
    assert ("GET", anchor + "/summary", {}, {"format": "html"}) in server.calls
    assert out["format"] == "html" and "markdown" not in out
    path = Path(out["path"])
    assert path.name == f"{SID}.daemon.html"
    assert out["html"] == path.read_text() == summary_cli.compose_draft(PAGE, SERIES)
    assert path.read_text().startswith('<script type="application/json" data-probe-series>\n[')
    assert path.read_text().endswith(PAGE + "\n")
    assert path.with_suffix(".base").read_text() == path.read_text()
    assert out["series"] == 1
    assert out["chartable"] == {"runs": 1, "metric_keys": 2}
    chartable = Path(out["chartable_path"])
    assert chartable.name == f"{SID}.daemon.chartable.json"
    assert json.loads(chartable.read_text())["by_run"][0]["name"] == "w-3"
    for f in (path, path.with_suffix(".base"), chartable):
        assert oct(f.stat().st_mode)[-3:] == "600", f
    assert not stale_md.exists(), "one stem holds one draft"


def test_push_sends_the_draft_as_html_and_adopts_the_canonical_page(server, capsys, monkeypatch):
    _daemon(monkeypatch)
    out = _checkout(capsys, "--experiment", "e")
    path = Path(out["path"])
    draft = summary_cli.compose_draft(PAGE, SERIES) + "\n"
    path.write_text(draft)
    code, pushed, _ = _push(capsys, "--experiment", "e")
    assert code == 0 and pushed["pushed"] is True and pushed["version"] == 1
    method, _route, body, _ = server.calls[-1]
    assert method == "PUT" and body["html"] == draft and "markdown" not in body
    assert body["expected_version"] == 0 and body["session_id"] == SID
    canonical = summary_cli.compose_draft(PAGE, SERIES)
    assert path.read_text() == canonical, "the server's canonical text replaced the unedited draft"
    assert path.with_suffix(".base").read_text() == canonical
    code, pushed, _ = _push(capsys, "--experiment", "e")
    assert pushed["pushed"] is False and pushed["detail"] == "no local edits"


def test_a_moved_page_merges_into_the_html_draft_with_the_same_merge3(server, capsys, monkeypatch):
    _daemon(monkeypatch)
    _checkout(capsys, "--project", "p")
    anchor = server.anchor_of("")
    server.write(anchor, PAGE, SERIES)
    out = _checkout(capsys, "--project", "p")
    path = Path(out["path"])
    path.write_text(path.read_text().replace("Does warmup help? Yes.", "Does warmup help? Yes, by 2.1."))
    server.write(anchor, PAGE.replace("</article>", "<p>Next: seeds.</p>\n</article>"), SERIES)
    code, pushed, _err = _push(capsys, "--project", "p")
    assert code == 0 and pushed["merged"] is True and pushed["pushed"] is False, (pushed, _err)
    merged = path.read_text()
    assert "Yes, by 2.1." in merged and "Next: seeds." in merged and "data-probe-series" in merged
    code, pushed, _ = _push(capsys, "--project", "p")
    assert code == 0 and pushed["pushed"] is True
    assert "Yes, by 2.1." in server.pages[anchor]["html"] and "Next: seeds." in server.pages[anchor]["html"]
    assert server.pages[anchor]["series"] == SERIES


def test_a_server_without_full_pages_gets_markdown_as_before(server, capsys, monkeypatch):
    _daemon(monkeypatch)
    server.html = False
    out = _checkout(capsys, "--project", "p")
    assert "format" not in out and out["markdown"] == ""
    assert Path(out["path"]).name == f"{SID}.daemon.md"
    Path(out["path"]).write_text("Does it work? Yes.\n")
    code, pushed, _ = _push(capsys, "--project", "p")
    assert code == 0 and pushed["pushed"] is True
    assert server.calls[-1][2]["markdown"] == "Does it work? Yes.\n"


# ---------------------------------------------------------------------------
# The first write's own checkout (P3, inline / agent profile).


def _agent_session(monkeypatch) -> None:
    monkeypatch.delenv(summary_cli.DAEMON_SESSION_ENV, raising=False)
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID)


def _summary_lines(err: str) -> list[str]:
    return [line for line in err.splitlines() if line.startswith("Summary of ")]


def test_the_first_write_checks_the_summary_out_and_prints_the_drafts_path(server, capsys, monkeypatch):
    _agent_session(monkeypatch)
    capsys.readouterr()
    assert cli.main(["experiment", "set", "e", "--question", "does it still work?"]) == 0
    (line,) = _summary_lines(capsys.readouterr().err)
    path = Path(line.split(": ", 1)[1].split(" - ", 1)[0])
    assert line == summary_cli.LOADED.format(label="e", kind="experiment", path=path, version=0)
    assert path.name == f"{SID}.html" and path.is_file()
    assert path.read_text() == summary_cli.compose_draft("", [])
    assert cli.main(["experiment", "set", "e", "--question", "and now?"]) == 0
    assert _summary_lines(capsys.readouterr().err) == [], "once per session per entity"


def test_without_a_server_answer_the_first_write_reminds_and_still_succeeds(server, capsys, monkeypatch):
    _agent_session(monkeypatch)
    capsys.readouterr()
    server.fail_reads = True
    assert cli.main(["project", "set", "p", "--name", "P"]) == 0
    assert _summary_lines(capsys.readouterr().err) == [summary_cli.REMINDER.format(label="p", kind="project")]


def test_the_first_write_never_replaces_a_draft_with_unpushed_edits(server, capsys, monkeypatch):
    _agent_session(monkeypatch)
    out = _checkout(capsys, "--project", "p")
    path = Path(out["path"])
    path.write_text(path.read_text() + "<p>unpushed</p>\n")
    # Forget the checkout, as a lost state file would.
    summary_cli._loaded_file(SID).unlink()
    capsys.readouterr()
    assert cli.main(["project", "set", "p", "--name", "P"]) == 0
    assert _summary_lines(capsys.readouterr().err) == [summary_cli.REMINDER.format(label="p", kind="project")]
    assert path.read_text().endswith("<p>unpushed</p>\n")


def test_under_the_daemon_the_first_write_keeps_the_reminder_line(server, capsys, monkeypatch):
    _daemon(monkeypatch)
    capsys.readouterr()
    assert cli.main(["project", "set", "p", "--name", "P"]) == 0
    assert _summary_lines(capsys.readouterr().err) == [summary_cli.REMINDER.format(label="p", kind="project")]
    assert not [c for c in server.calls if c[1].endswith("/summary")], "the daemon's worker loads it"


def test_without_a_session_a_dirty_markdown_draft_is_never_dropped_by_an_html_checkout(
    server, capsys, monkeypatch
):
    """The shared draft (no session id) is claimed whichever format it is in:
    an html checkout would replace the Markdown one, unpushed edits and all."""
    monkeypatch.delenv(summary_cli.DAEMON_SESSION_ENV, raising=False)
    server.html = False
    out = _checkout(capsys, "--project", "p")
    md = Path(out["path"])
    assert md.name == "note.md"
    md.write_text("unpushed words\n")
    server.html = True
    capsys.readouterr()
    assert cli.main(["summary", "checkout", "--project", "p"]) == 2
    assert md.read_text() == "unpushed words\n"
    out = _checkout(capsys, "--project", "p", "--steal")
    assert Path(out["path"]).name == "note.html" and not md.exists()



def test_a_checkout_never_replaces_unpushed_edits_without_steal(server, capsys, monkeypatch):
    """Review of #3034, finding 3: a session's checkout overwrote its own draft
    and base unconditionally (and deleted the other format's draft), so the
    daemon's automatic checkout could erase a writer's unpushed edits."""
    _daemon(monkeypatch)
    out = _checkout(capsys, "--project", "p")
    path = Path(out["path"])
    path.write_text(path.read_text() + "<p>unpushed</p>\n")
    server.write(server.anchor_of(""), PAGE, SERIES)
    capsys.readouterr()
    assert cli.main(["summary", "checkout", "--project", "p"]) == 2
    captured = capsys.readouterr()
    refused = json.loads(captured.out)
    assert refused == {"target": "project", "label": "p", "path": str(path), "version": 0, "format": "html",
                       "refused": "unpushed edits"}
    assert str(path) in captured.err and "--steal" in captured.err
    assert path.read_text().endswith("<p>unpushed</p>\n"), "the draft keeps its edits"
    assert not [c for c in server.calls if c[0] == "GET" and c[1].endswith("/summary")][1:], "nothing fetched"
    # A Markdown draft with edits guards an html checkout too.
    path.unlink()
    md = path.with_suffix(".md")
    md.write_text("unpushed markdown\n")
    assert cli.main(["summary", "checkout", "--project", "p"]) == 2
    assert md.read_text() == "unpushed markdown\n"
    out = _checkout(capsys, "--project", "p", "--steal")
    assert Path(out["path"]).read_text() == summary_cli.compose_draft(PAGE, SERIES) and not md.exists()


def test_the_first_writes_checkout_is_bounded_and_never_retried(server, capsys, monkeypatch):
    """Review of #3034, finding 6: one attempt, `FIRST_WRITE_LOAD_S` for all of it."""
    _agent_session(monkeypatch)
    seen = {}
    real = summary_cli.checkout_draft

    def spy(client, *args, **kwargs):
        from probe.sdk import transport as transport_mod

        seen["retries"] = client.transport.max_retries
        seen["timeout"] = client.transport.timeout
        seen["deadline"] = transport_mod._request_deadline.get()
        return real(client, *args, **kwargs)

    monkeypatch.setattr(summary_cli, "checkout_draft", spy)
    import time as time_mod

    before = time_mod.monotonic()
    assert cli.main(["project", "set", "p", "--name", "P"]) == 0
    assert seen["retries"] == 0 and seen["timeout"] <= summary_cli.FIRST_WRITE_LOAD_S
    assert before < seen["deadline"] <= time_mod.monotonic() + summary_cli.FIRST_WRITE_LOAD_S


# ---------------------------------------------------------------------------
# `probe summary edit|append`: one command, no draft (the dashboard assistant's
# door, whose commands each run in a temporary HOME). HTML only, pinned to the
# version read, a person's block refused here rather than silently restored.

KEPT = '<!-- kept: h1 --><p data-owner="human" data-strength="hard">My own words.</p><!-- /kept -->'
KEPT_PAGE = PAGE.replace("</article>", f"{KEPT}\n</article>")


def _one_shot(capsys, *args: str) -> tuple[int, dict, str]:
    capsys.readouterr()
    code = cli.main(["summary", *args])
    out = capsys.readouterr()
    return code, json.loads(out.out) if out.out.strip() else {}, out.err


def _seed(server, html: str = KEPT_PAGE) -> str:
    """The project's page at version 1; its anchor."""
    if not server.pages:  # a first read creates the project's page on the fake
        assert cli.main(["summary", "edit", "--project", "p", "--old", "@@none@@", "--new", "y"]) == 1
    anchor = server.anchor_of("")
    server.write(anchor, html, SERIES)
    server.calls.clear()
    return anchor


def _puts(server) -> list[dict]:
    return [body for method, _route, body, _ in server.calls if method == "PUT"]


def _gets(server) -> int:
    return sum(1 for method, route, _b, _p in server.calls if method == "GET" and route.endswith("/summary"))


def test_edit_replaces_one_exact_piece_and_writes_no_draft(server, capsys, tmp_path):
    anchor = _seed(server)
    code, out, err = _one_shot(capsys, "edit", "--project", "p", "--old", "Yes.", "--new", "Yes, by 2.1.")
    assert code == 0, err
    [body] = _puts(server)
    assert body["html"] == summary_cli.compose_draft(KEPT_PAGE.replace("Yes.", "Yes, by 2.1."), SERIES)
    assert body["expected_version"] == 1 and "markdown" not in body
    assert out == {"target": "project", "label": "p", "removed": 4, "added": 12, "changed": True, "version": 2}
    assert "Yes, by 2.1." in server.pages[anchor]["html"] and KEPT in server.pages[anchor]["html"]
    assert server.pages[anchor]["series"] == SERIES, "the chart declarations ride along unchanged"
    assert not [p for p in (tmp_path / "state").rglob("*") if p.suffix in (".html", ".md")], "no draft"


def test_edit_writes_nothing_when_old_matches_nothing_or_twice(server, capsys):
    _seed(server, KEPT_PAGE.replace("</article>", "<p>Yes.</p>\n</article>"))
    code, _out, err = _one_shot(capsys, "edit", "--project", "p", "--old", "**warmup**", "--new", "x")
    assert code == 1 and "matches nothing" in err and "not its Markdown" in err
    code, _out, err = _one_shot(capsys, "edit", "--project", "p", "--old", "Yes.", "--new", "x")
    assert code == 1 and "matches 2 places" in err
    assert _puts(server) == []


def test_edit_refuses_a_persons_block_rather_than_reporting_a_change_the_server_undoes(server, capsys):
    """The server puts a kept block's stored bytes back on every write, so an
    edit inside one would land as a new version with nothing changed."""
    _seed(server)
    for old in ("My own words.", "<!-- /kept -->"):  # the words, or only a marker
        code, _out, err = _one_shot(capsys, "edit", "--project", "p", "--old", old, "--new", "x")
        assert code == 1 and "only they can change it" in err, old
    assert _puts(server) == []


def test_a_moved_page_is_edited_again_from_the_head_the_409_carries(server, capsys):
    anchor = _seed(server)
    real = server.serve
    moved = []

    def serve(method, *rest):
        if method == "PUT" and not moved:
            moved.append(1)  # a teammate's push lands between this read and this write
            server.write(anchor, KEPT_PAGE.replace("</article>", "<p>Next: seeds.</p>\n</article>"))
        return real(method, *rest)

    server.serve = serve
    code, out, err = _one_shot(capsys, "edit", "--project", "p", "--old", "Yes.", "--new", "Yes, by 2.1.")
    assert code == 0, err
    assert [b["expected_version"] for b in _puts(server)] == [1, 2]
    assert _gets(server) == 1, "the 409 carried the head: no second read"
    html = server.pages[anchor]["html"]
    assert "Yes, by 2.1." in html and "Next: seeds." in html and out["version"] == 3


def test_an_old_the_moved_page_no_longer_has_is_refused(server, capsys):
    anchor = _seed(server)
    real = server.serve

    def serve(method, *rest):
        if method == "PUT" and server.pages[anchor]["version"] == 1:
            server.write(anchor, KEPT_PAGE.replace("Yes.", "No."))
        return real(method, *rest)

    server.serve = serve
    code, _out, err = _one_shot(capsys, "edit", "--project", "p", "--old", "Yes.", "--new", "x")
    assert code == 1 and "matches nothing" in err
    assert len(_puts(server)) == 1 and "No." in server.pages[anchor]["html"]


def test_an_erasure_mid_edit_stops_with_exit_2_and_never_writes_again(server, capsys):
    """The new text was written from a read the erasure has since changed:
    re-applying it could carry erased words back."""
    _seed(server)
    real = server.serve

    def serve(method, anchor, what, rest, body, params):
        if method == "PUT":
            return httpx.Response(409, json={"detail": {"code": "erased_since_checkout", "version": 3,
                                                        "html": PAGE, "series": SERIES}})
        return real(method, anchor, what, rest, body, params)

    server.serve = serve
    code, _out, err = _one_shot(capsys, "append", "--project", "p", "--html", "<p>Seeds next.</p>")
    assert code == 2 and "erasure" in err and "nothing was written" in err
    assert len(_puts(server)) == 1


@pytest.mark.parametrize("land", [True, False])
def test_a_lost_reply_is_settled_by_reading_and_never_sent_again(server, capsys, land):
    anchor = _seed(server)
    real = server.serve

    def serve(method, a, what, rest, body, params):
        if method == "PUT":
            if land:
                real(method, a, what, rest, body, params)
            raise httpx.ReadTimeout("the reply never came")
        return real(method, a, what, rest, body, params)

    server.serve = serve
    code, _out, err = _one_shot(capsys, "edit", "--project", "p", "--old", "Yes.", "--new", "Yes, by 2.1.")
    assert len(_puts(server)) == 1, "never sent twice"
    if land:
        assert code == 0 and "landed" in err
        assert "Yes, by 2.1." in server.pages[anchor]["html"]
    else:
        # A timeout can still land after this read: unchanged is NOT "nothing written".
        assert code == 1 and "may still" in err and "nothing was written" not in err


def test_a_server_without_full_pages_is_refused_rather_than_flattened(server, capsys):
    _seed(server)
    server.html = False
    code, _out, err = _one_shot(capsys, "append", "--project", "p", "--html", "<p>x</p>")
    assert code == 1 and "flattening" in err and _puts(server) == []


def test_the_credential_scrubber_never_rewrites_a_page_behind_the_writers_back(server, capsys):
    _seed(server, KEPT_PAGE.replace("Yes.", "Yes. control run: sk%2Dbaseline"))
    code, _out, err = _one_shot(capsys, "edit", "--project", "p", "--old", "warmup", "--new", "cooldown")
    assert code == 1 and "scrubber would rewrite" in err
    assert _puts(server) == []
    _seed(server)
    code, _out, err = _one_shot(capsys, "edit", "--project", "p", "--old", "Yes.", "--new", "sk%2Dbaseline")
    assert code == 1 and "credential" in err
    assert _puts(server) == []


def test_append_adds_before_the_articles_close(server, capsys):
    anchor = _seed(server)
    code, out, err = _one_shot(capsys, "append", "--project", "p", "--html", "<p>Seeds next.</p>\n")
    assert code == 0, err
    html = server.pages[anchor]["html"]
    assert html.endswith(f"{KEPT}\n<p>Seeds next.</p>\n</article>")
    assert out["added"] == len("<p>Seeds next.</p>") and out["version"] == 2


def test_append_refuses_an_empty_page_and_a_page_with_no_article(server, capsys):
    code, _out, err = _one_shot(capsys, "append", "--project", "p", "--html", "<p>x</p>")
    assert code == 1 and "no page yet" in err
    assert _puts(server) == []
    _seed(server, "<p>An older page.</p>")
    code, _out, err = _one_shot(capsys, "append", "--project", "p", "--html", "<p>x</p>")
    assert code == 1 and "summary edit" in err
    assert _puts(server) == []


def test_edit_and_append_are_the_summarys_own_commands_not_a_write_that_loads_it():
    for args in (["summary", "edit", "--project", "p", "--old", "a", "--new", "b"],
                 ["summary", "append", "--project", "p", "--html", "<p>b</p>"]):
        assert summary_cli.landing(args) is None, args


def _answer_puts(server, reply):
    """Every PUT answered by `reply(anchor)` (an httpx.Response), or by the fake."""
    real = server.serve

    def serve(method, a, what, rest, body, params):
        if method == "PUT":
            got = reply(a)
            if got is not None:
                return got
        return real(method, a, what, rest, body, params)

    server.serve = serve


def test_the_one_match_outside_a_persons_block_is_the_one_edited(server, capsys):
    anchor = _seed(server, KEPT_PAGE.replace("</article>", "<p>My own words.</p>\n</article>"))
    code, _out, err = _one_shot(capsys, "edit", "--project", "p", "--old", "My own words.", "--new", "Theirs.")
    assert code == 0, err
    html = server.pages[anchor]["html"]
    assert KEPT in html and "<p>Theirs.</p>" in html


def test_an_old_copied_across_a_persons_block_from_the_overview_read_is_refused_as_theirs(server, capsys):
    """The overview read shows the page without kept markers: text copied
    across a block's edge matches only once they are gone."""
    _seed(server)
    code, _out, err = _one_shot(capsys, "edit", "--project", "p", "--old", "</script>\n<p data-owner", "--new", "x")
    assert code == 1 and "only they can change it" in err and "matches nothing" not in err
    assert _puts(server) == []


def test_overlapping_matches_count_as_two(server, capsys):
    _seed(server, KEPT_PAGE.replace("Yes.", "a a a"))
    code, _out, err = _one_shot(capsys, "edit", "--project", "p", "--old", "a a", "--new", "b")
    assert code == 1 and "matches 2 places" in err and _puts(server) == []


def test_version_pins_the_first_write_and_a_move_since_is_edited_from_the_head(server, capsys):
    """`--version` is the page the caller's text came from: the first write is
    pinned to it (so the server's erasure check runs against it), a move since
    is applied again from the head the 409 carries."""
    anchor = _seed(server)
    server.write(anchor, KEPT_PAGE)  # v2 now
    code, out, err = _one_shot(capsys, "append", "--project", "p", "--version", "1", "--html", "<p>Seeds.</p>")
    assert code == 0, err
    assert [b["expected_version"] for b in _puts(server)] == [1, 2] and out["version"] == 3


def test_a_409_without_a_head_reads_again_and_gives_up_after_the_attempts(server, capsys):
    anchor = _seed(server)

    def moved(_a):
        server.write(anchor, server.pages[anchor]["html"])  # someone else's write, every time
        return httpx.Response(409, json={"detail": {"code": "version_moved"}})

    _answer_puts(server, moved)
    code, _out, err = _one_shot(capsys, "edit", "--project", "p", "--old", "Yes.", "--new", "Yes, by 2.1.")
    assert code == 1 and "kept changing" in err
    assert [b["expected_version"] for b in _puts(server)] == list(range(1, summary_cli.EDIT_ATTEMPTS + 1))
    assert _gets(server) == summary_cli.EDIT_ATTEMPTS


@pytest.mark.parametrize(("reply", "exit_code", "says"), [
    ({"code": "session_erased"}, 2, "erased"),
    ({"code": "something_else", "message": "refused for its own reason"}, 1, "own reason"),
])
def test_other_409s_stop_after_one_write(server, capsys, reply, exit_code, says):
    _seed(server)
    _answer_puts(server, lambda _a: httpx.Response(409, json={"detail": reply}))
    code, _out, err = _one_shot(capsys, "append", "--project", "p", "--html", "<p>x</p>")
    assert code == exit_code and says in err and len(_puts(server)) == 1


def test_a_closed_summary_door_says_so_instead_of_run_it_again(server, capsys):
    _seed(server)
    _answer_puts(server, lambda _a: httpx.Response(503, json={"detail": {
        "code": "summary_writer_off", "message": "this team's summaries are written by the overview lane"}}))
    code, _out, err = _one_shot(capsys, "append", "--project", "p", "--html", "<p>x</p>")
    assert code == 1 and summary_cli.LANE_MARK in err and "Run it again" not in err
    assert len(_puts(server)) == 1


def test_a_read_with_no_version_writes_nothing(server, capsys):
    _seed(server)
    real = server.serve

    def serve(method, a, what, rest, body, params):
        got = real(method, a, what, rest, body, params)
        if method == "GET" and what == "summary":
            row = json.loads(got.content)
            row.pop("version")
            return httpx.Response(200, json=row)
        return got

    server.serve = serve
    code, _out, err = _one_shot(capsys, "append", "--project", "p", "--html", "<p>x</p>")
    assert code == 1 and "which version" in err and _puts(server) == []


@pytest.mark.parametrize("reply", [
    lambda: httpx.Response(200, json={"html": "x"}),  # no version
    lambda: httpx.Response(200, content=b"<html>an ingress page</html>"),  # not JSON
])
def test_a_reply_that_does_not_confirm_the_write_is_settled_by_reading(server, capsys, reply):
    anchor = _seed(server)
    real = server.serve

    def serve(method, a, what, rest, body, params):
        if method == "PUT":
            real(method, a, what, rest, body, params)  # it landed
            return reply()
        return real(method, a, what, rest, body, params)

    server.serve = serve
    code, _out, err = _one_shot(capsys, "append", "--project", "p", "--html", "<p>Seeds.</p>")
    assert code == 0 and "landed" in err, err
    assert len(_puts(server)) == 1 and "<p>Seeds.</p>" in server.pages[anchor]["html"]


def test_append_lands_in_the_pages_own_article_whatever_else_says_article(server, capsys):
    page = (
        '<style>.ov-page::after{content:"</article>"}</style>\n<article class="ov-page">\n'
        '<p>Yes.</p>\n<article class="card"><p>A card.</p></article>\n</article>\n'
        "<script>PROBE.lineChart('c', 'loss', {title: '</article>'})</script>"
    )
    anchor = _seed(server, page)
    code, _out, err = _one_shot(capsys, "append", "--project", "p", "--html", "<p>Seeds.</p>")
    assert code == 0, err
    html = server.pages[anchor]["html"]
    assert "<p>A card.</p></article>\n<p>Seeds.</p>\n</article>\n<script>" in html
    assert html.startswith('<style>.ov-page::after{content:"</article>"}</style>')


def test_a_write_that_changes_nothing_says_so(server, capsys):
    _seed(server)
    _answer_puts(server, lambda _a: httpx.Response(200, json={"version": 1, "changed": False, "html": KEPT_PAGE}))
    code, out, err = _one_shot(capsys, "edit", "--project", "p", "--old", "Yes.", "--new", "Yes.")
    assert code == 0 and out["changed"] is False and "nothing changed" in err
