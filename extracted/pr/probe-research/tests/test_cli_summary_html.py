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
