"""The writer's summaries (writer-owns-summary ARTIFACT-PAGES P3), replacing the
§3.5 pin of one summary's whole text:

* before a writer run the worker checks out every project and experiment the
  session's writes landed on or created (the logbook, read by the CLI's own
  parse; at most `SUMMARY_DRAFTS_KEPT`, the most recently touched), with no
  model round, and never replaces a draft holding unpushed edits;
* the next message starts with an OUTLINE per entity -- never its text -- once
  per change (append-only), again after the outline changed;
* the writer changes a draft in place with `edit`: an exact find-and-replace,
  only under the note and summary draft folders, `old` found exactly once.

Same seams as test_daemon_conversation.py: Pydantic AI's FunctionModel, `probe`
commands answered by a replay, a real chat log.
"""

from __future__ import annotations

import asyncio
import json
import os
import time
from pathlib import Path

import pytest

pytest.importorskip("pydantic_ai")
pytest.importorskip("pydantic_ai_harness")

from pydantic_ai.models.function import FunctionModel  # noqa: E402

from probe.daemon import approvals as appr  # noqa: E402
from probe.daemon import folders, tools  # noqa: E402
from probe.daemon import model as model_mod  # noqa: E402
from probe.daemon.store import Store  # noqa: E402
from tests.test_daemon_conversation import (  # noqa: E402,F401 -- `_isolated` is an autouse fixture
    Replay,
    Script,
    _append_turn,
    _isolated,
    _live,
    _worker,
)

PAGE = (
    '<script type="application/json" data-probe-series>\n[]\n</script>\n'
    '<article class="ov-page"><p>Does a cosine decay beat a constant LR? Yes: B2decay 48.8 (sft-b2decay-3).</p>'
    "<h2>Where it stands</h2><p>Three seeds next.</p><h2>Oct 15 · Richard</h2><ul><li>ran it</li></ul>"
    "</article>\n"
)


def _drafts_root() -> Path:
    return folders.note_dirs()[1]


def _draft_for(kind: str, name: str, text: str) -> Path:
    path = _drafts_root() / kind / f"id-{name}" / "s.daemon.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    path.with_suffix(".base").write_text(text)
    return path


class CheckoutReplay(Replay):
    """`probe summary checkout` writes the draft and prints the checkout's JSON,
    as the CLI does; every other command answers `{"ok": true}`."""

    def __init__(self, text: str = PAGE, version: int = 3) -> None:
        super().__init__()
        self.text = text
        self.version = version

    async def run(self, argv, op_id):
        self.calls.append(list(argv))
        if argv[:2] == ["summary", "checkout"]:
            kind, ref = argv[2].lstrip("-"), argv[3]
            path = _draft_for(kind, ref, self.text)
            return 0, json.dumps({
                "target": kind, "label": ref, "path": str(path), "version": self.version,
                "you": "Richard", "today": "2026-10-17", "edited_by": "Ada",
                "edited_at": "2026-10-16T09:30:00Z", "mode": "recorder", "visuals": None,
                "format": "html", "html": self.text, "series": 0,
                "chartable_path": str(path.with_suffix(".chartable.json")),
                "chartable": {"runs": 0, "metric_keys": 0},
            })
        return 0, json.dumps({"ok": True})


@pytest.fixture
def lean(monkeypatch):
    monkeypatch.setattr(model_mod, "_PUSHED", {})
    monkeypatch.setenv(model_mod.ENV_WRITER_HISTORY, "lean")


def _log(store: Store, *argv: str, at: float | None = None) -> None:
    store.log_write(bite=None, op_id=f"op-{time.time()}", argv=["probe", *argv], head=" ".join(argv[:2]),
                    status="ran")
    if at is not None:
        store.db.execute("UPDATE writes SET at = ? WHERE id = (SELECT max(id) FROM writes)", (at,))


def _deps(tmp_path, replay) -> tools.Deps:
    work = tmp_path / "work"
    work.mkdir(parents=True, exist_ok=True)
    return tools.Deps(
        store=Store(tmp_path / "s.sqlite", clock=time.time), board=appr.Board(tmp_path / "appr"),
        session_id="s", cwd=work, workdirs=[work], home=tmp_path, write_dirs=folders.note_dirs(),
        probe_env={}, bypass=False, mode_known=True, bite_id=1, replay=replay,
    )


# ---------------------------------------------------------------------------
# What the session touched, and the checkout before a run.


def test_the_touched_entities_come_from_the_logbook_newest_first_and_at_most_six(tmp_path):
    deps = _deps(tmp_path, CheckoutReplay())
    _log(deps.store, "experiment", "create", "b2", "--project", "willow", "--question", "q?")
    for i in range(7):
        _log(deps.store, "experiment", "set", f"e{i}", "--conclusion", "yes")
    _log(deps.store, "project", "list")  # a read in the logbook names nothing
    touched = tools.touched_entities(deps.store)
    assert len(touched) == tools.SUMMARY_DRAFTS_KEPT == 6
    assert [(k, r) for k, r, _ in touched] == [("experiment", f"e{i}") for i in range(6, 0, -1)]
    everything = tools.touched_entities(deps.store, limit=20)
    assert ("experiment", "b2") in [(k, r) for k, r, _ in everything]
    assert ("project", "willow") in [(k, r) for k, r, _ in everything], "an experiment's creation touches its project"


def test_before_a_run_every_touched_entity_is_checked_out_with_no_model_round(tmp_path):
    replay = CheckoutReplay()
    deps = _deps(tmp_path, replay)
    _log(deps.store, "experiment", "create", "b2", "--project", "willow", "--question", "q?")
    done = asyncio.run(tools.autoload_summaries(deps))
    assert sorted(done) == ["experiment=b2", "project=willow"]
    assert sorted(c[:4] for c in replay.calls) == [
        ["summary", "checkout", "--experiment", "b2"], ["summary", "checkout", "--project", "willow"]]
    drafts = deps.store.fact(tools.SUMMARY_DRAFTS)
    assert drafts["experiment=b2"]["version"] == 3 and drafts["experiment=b2"]["format"] == "html"
    # The push the writer makes with the same flags finds the draft.
    assert deps.store.fact("checkouts")["summary checkout|experiment=b2"] == drafts["experiment=b2"]["path"]


def test_a_draft_with_unpushed_edits_is_never_replaced_and_its_outline_says_so(tmp_path):
    replay = CheckoutReplay()
    deps = _deps(tmp_path, replay)
    _log(deps.store, "experiment", "set", "b2", "--conclusion", "yes")
    asyncio.run(tools.autoload_summaries(deps))
    path = Path(deps.store.fact(tools.SUMMARY_DRAFTS)["experiment=b2"]["path"])
    path.write_text(PAGE.replace("Three seeds next.", "Five seeds next."))
    replay.calls.clear()
    replay.text = PAGE.replace("Three seeds", "someone else's")
    asyncio.run(tools.autoload_summaries(deps))
    assert replay.calls == [], "not checked out again"
    assert "Five seeds next." in path.read_text()
    assert tools.OUTLINE_DIRTY in tools.summary_outline(deps.store)


def test_nothing_is_checked_out_while_the_team_is_in_lane_mode(tmp_path):
    replay = CheckoutReplay()
    deps = _deps(tmp_path, replay)
    _log(deps.store, "experiment", "set", "b2", "--conclusion", "yes")
    tools._note_mode(deps, "lane")
    assert asyncio.run(tools.autoload_summaries(deps)) == [] and replay.calls == []


# ---------------------------------------------------------------------------
# The outline.


def test_the_outline_names_where_things_are_and_never_carries_the_text(tmp_path):
    deps = _deps(tmp_path, CheckoutReplay())
    _log(deps.store, "experiment", "create", "b2", "--project", "willow", "--question", "q?", at=1.0)
    asyncio.run(tools.autoload_summaries(deps))
    _log(deps.store, "experiment", "set", "b2", "--conclusion", "B2decay wins")
    _log(deps.store, "experiment", "create", "b3", "--project", "willow", "--question", "q?")
    _log(deps.store, "run", "start", "--experiment", "b2", "--name", "sft-3")
    _log(deps.store, "run", "start", "--experiment", "b2", "--name", "sft-4")
    _log(deps.store, "run", "start", "--experiment", "other", "--name", "elsewhere")
    _log(deps.store, "run", "end", "sft-3")
    _log(deps.store, "run", "end", "sft-4", "--status", "failed")
    _log(deps.store, "run", "end", "elsewhere")
    outline = tools.summary_outline(deps.store)
    path = deps.store.fact(tools.SUMMARY_DRAFTS)["experiment=b2"]["path"]
    expected_b2 = "\n".join([
        f"## Experiment b2 · v3 · {len(PAGE)} characters",
        f"- draft: {path} · push: probe summary push --experiment b2",
        "- last edited by Ada, 2026-10-16 09:30",
        "- headings: Where it stands · Oct 15 · Richard",
        "- opens: Does a cosine decay beat a constant LR? Yes: B2decay 48.8 (sft-b2decay-3).",
        "- since v3: conclusion set; run started ×2; run sft-3 completed; run sft-4 failed",
    ])
    assert expected_b2 in outline, outline
    assert "- since v3: new experiment b3" in outline, "the project sees its new experiment"
    assert "Three seeds next." not in outline and "ran it" not in outline, "an outline, never the page"
    header = tools.outline_header(outline)
    assert header.startswith("# Summaries you keep (outline ") and len(header) < 60


def test_the_opening_is_cut_and_a_credential_never_shows(tmp_path):
    long = "<p>" + "word " * 200 + "AKIAIOSFODNN7EXAMPLE</p>"
    deps = _deps(tmp_path, CheckoutReplay(text=f'<article class="ov-page">{long}</article>'))
    _log(deps.store, "experiment", "set", "b2", "--conclusion", "yes")
    asyncio.run(tools.autoload_summaries(deps))
    line = next(x for x in tools.summary_outline(deps.store).splitlines() if x.startswith("- opens: "))
    assert len(line) <= len("- opens: ") + tools.OUTLINE_OPENING_CHARS and line.endswith("…")
    deps.store.fact(tools.SUMMARY_DRAFTS)
    path = Path(deps.store.fact(tools.SUMMARY_DRAFTS)["experiment=b2"]["path"])
    path.write_text('<article class="ov-page"><p>key AKIAIOSFODNN7EXAMPLE here</p></article>')
    outline = tools.summary_outline(deps.store)
    assert "AKIAIOSFODNN7EXAMPLE" not in outline and "<redacted:" in outline


def test_at_most_six_entities_are_kept_and_outlined(tmp_path):
    deps = _deps(tmp_path, CheckoutReplay())
    for i in range(8):
        _log(deps.store, "experiment", "set", f"e{i}", "--conclusion", "yes", at=100.0 + i)
        asyncio.run(tools.autoload_summaries(deps))
    drafts = deps.store.fact(tools.SUMMARY_DRAFTS)
    assert sorted(drafts) == sorted(f"experiment=e{i}" for i in range(2, 8)), "the six touched last"
    assert tools.summary_outline(deps.store).count("\n## Experiment ") + 1 == 6


def test_a_markdown_draft_is_outlined_too(tmp_path):
    md = "What it is.\n\n**Where it stands:** fine.\n\n## Oct 15 · Ada\n\n- did it\n<!-- kept: h1 -->\n> # their heading\n<!-- /kept -->\n"
    deps = _deps(tmp_path, CheckoutReplay(text=md))
    _log(deps.store, "project", "set", "willow", "--name", "W")
    asyncio.run(tools.autoload_summaries(deps))
    entry = deps.store.fact(tools.SUMMARY_DRAFTS)["project=willow"]
    deps.store.set_fact(tools.SUMMARY_DRAFTS, {"project=willow": {**entry, "format": "markdown"}})
    outline = tools.summary_outline(deps.store)
    assert "- headings: Oct 15 · Ada" in outline and "- opens: What it is." in outline


def _next_message(w, prompt: str) -> str:
    _append_turn(w.session.transcript, prompt)
    script = Script([("done", "nothing new")])
    w._model = FunctionModel(script)
    w.read_new()
    assert asyncio.run(w.run_bite("prompt")) is True
    parts = [p.content for m in script.seen[0][0] for p in m.parts if isinstance(getattr(p, "content", None), str)]
    return parts[-1]


def test_the_outline_starts_a_message_once_per_change(tmp_path, monkeypatch, lean):
    replay = CheckoutReplay()
    script = Script([("shell", "probe experiment set b2 --conclusion yes"), ("done", "set it")])
    w = _worker(tmp_path, model=FunctionModel(script), replay=replay, mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    nxt = _next_message(w, "NEXT: run three seeds of B2decay")
    assert ["summary", "checkout", "--experiment", "b2"] in [c[:4] for c in replay.calls], "loaded before the run"
    assert nxt.startswith("# Summaries you keep (outline "), nxt[:200]
    assert "## Experiment b2 · v3" in nxt and "Three seeds next." not in nxt
    assert "NEXT: run three seeds" in nxt
    again = _next_message(w, "THIRD: compare them")
    assert "# Summaries you keep" not in again, "the same outline is not shown twice"
    _log(w.store, "run", "start", "--experiment", "b2", "--name", "sft-3")
    changed = _next_message(w, "FOURTH: a run started")
    assert changed.startswith("# Summaries you keep (outline ") and "run started" in changed


def test_a_fresh_start_carries_the_outline_in_its_first_message(tmp_path, monkeypatch, lean):
    replay = CheckoutReplay()
    script = Script([("shell", "probe experiment set b2 --conclusion yes"), ("done", "set it")])
    w = _worker(tmp_path, model=FunctionModel(script), replay=replay, mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    asyncio.run(w._autoload_summaries(None))
    w.store.end_conversation(_live(w)["id"], "test: start fresh")
    _append_turn(w.session.transcript, "after the fresh start")
    w.read_new()
    _, history, built = w._next_in_conversation("prompt", None)
    assert history is None and built.prompt.startswith("# Summaries you keep (outline ")


def test_the_page_skills_ride_in_once(tmp_path, monkeypatch, lean):
    """The writer read artifact-design in 2 of 53 sessions that pushed a page
    when the page skills were a `read` away: they are in the conversation
    whole, once."""
    replay = CheckoutReplay()
    script = Script([("shell", "probe experiment set b2 --conclusion yes"), ("done", "set it")])
    w = _worker(tmp_path, model=FunctionModel(script), replay=replay, mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    first = "\n".join(p.content for m in script.seen[0][0] for p in m.parts if isinstance(getattr(p, "content", None), str))
    assert "# Page skills (shown here whole, no need to read their files; " in first
    for name in ("overview-page", "overview-contract", "overview-charts", "artifact-design", "artifact-diagramming"):
        assert f"# Skill: {name}" in first, name
    nxt = _next_message(w, "NEXT: run three seeds of B2decay")
    assert "# Page skills" not in nxt, "shown once per conversation"
    assert nxt.startswith("# Summaries you keep (outline "), "the outline still leads the message"


def test_the_first_page_of_a_new_experiment_is_written_with_the_page_skills(tmp_path, monkeypatch, lean):
    """A run that creates an experiment writes its first page in that run,
    before any draft exists: the skills are in its first message anyway."""
    w = _worker(tmp_path, model=FunctionModel(Script([("done", "x")])), replay=CheckoutReplay(),
                mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    _, _, built = w._next_in_conversation("prompt", None)
    assert "# Page skills (shown here whole" in built.prompt


def test_no_summary_no_outline(tmp_path, monkeypatch, lean):
    w = _worker(tmp_path, model=FunctionModel(Script([("done", "x")])), replay=CheckoutReplay(),
                mode="conversation", monkeypatch=monkeypatch)
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    assert "# Summaries you keep" not in _next_message(w, "NEXT")


# ---------------------------------------------------------------------------
# The edit tool.


def test_edit_replaces_the_one_match_and_answers_with_the_changed_lines(tmp_path):
    deps = _deps(tmp_path, CheckoutReplay())
    path = _draft_for("experiment", "b2", "line 1\nline 2\nline 3\nline 4\nline 5\nline 6\nline 7\nline 8\n")
    os.chmod(path, 0o600)
    out = asyncio.run(tools.edit_file(deps, str(path), "line 5\n", "line five\nand a new line\n"))
    assert path.read_text() == "line 1\nline 2\nline 3\nline 4\nline five\nand a new line\nline 6\nline 7\nline 8\n"
    assert out.startswith(f"edited {path} (lines 5-6):")
    assert "     5\tline five" in out and "     2\tline 2" in out and "     9\tline 8" in out
    assert "     1\tline 1" not in out, "a few lines of context, not the file"
    assert oct(path.stat().st_mode)[-3:] == "600"
    assert "edit" in tools.WRITE_TOOLS


@pytest.mark.parametrize(
    ("old", "words"),
    [("", "`old` is empty"), ("nowhere", "is not in"), ("twice", "appears 2 times")],
)
def test_edit_needs_old_exactly_once(tmp_path, old, words):
    deps = _deps(tmp_path, CheckoutReplay())
    path = _draft_for("project", "willow", "twice and twice\n")
    out = asyncio.run(tools.edit_file(deps, str(path), old, "x"))
    assert out.startswith("not edited:") and words in out
    assert path.read_text() == "twice and twice\n"


def test_edit_refuses_any_path_but_a_draft(tmp_path):
    deps = _deps(tmp_path, CheckoutReplay())
    elsewhere = tmp_path / "work" / "notes.md"
    elsewhere.write_text("hello\n")
    assert asyncio.run(tools.edit_file(deps, str(elsewhere), "hello", "bye")).startswith("not edited: `edit`")
    assert elsewhere.read_text() == "hello\n"
    team = folders.note_dirs()[-1] / "note.md"
    team.parent.mkdir(parents=True, exist_ok=True)
    team.write_text("team\n")
    assert asyncio.run(tools.edit_file(deps, str(team), "team", "x")).startswith("not edited: `edit`"), (
        "the team note's changes go to the researcher first"
    )
    draft = _draft_for("project", "willow", "body\n")
    base = draft.with_suffix(".base")
    assert "Probe's own record" in asyncio.run(tools.edit_file(deps, str(base), "body", "x"))
    link = draft.parent / "escape.html"
    link.symlink_to(elsewhere)
    assert asyncio.run(tools.edit_file(deps, str(link), "hello", "bye")).startswith("not edited: `edit`")
    assert elsewhere.read_text() == "hello\n"
    outside = asyncio.run(tools.edit_file(deps, str(_drafts_root() / ".." / "summaries-x" / "f.md"), "a", "b"))
    assert outside.startswith("not edited:")


def test_the_writer_has_the_edit_tool_and_it_runs_alone(monkeypatch):
    from tests.test_daemon_prompts import _tools_seen

    monkeypatch.setenv("PROBE_DAEMON_MCP", "0")
    seen, _ = _tools_seen()
    assert set(seen["edit"].parameters_json_schema["properties"]) == {"path", "old", "new"}
    assert "edit" in tools.WRITE_TOOLS, "a write: it runs alone, in the order the model called it"


def test_the_outline_names_the_push_with_the_checkouts_own_flags(tmp_path):
    """A writer's checkout with both flags keys its draft by both: the push the
    outline names repeats them, or the daemon would not find the draft."""
    replay = CheckoutReplay()
    deps = _deps(tmp_path, replay)
    from probe.daemon import precheck

    argv = ["summary", "checkout", "--experiment", "b2", "--project", "willow"]
    _code, out = asyncio.run(replay.run(argv[:4], "op"))
    tools._remember_note(deps, precheck.parse(argv), out)
    outline = tools.summary_outline(deps.store)
    assert "## Experiment b2 · v3" in outline
    assert "push: probe summary push --project willow --experiment b2" in outline


# ---------------------------------------------------------------------------
# Review of #3034 (head e2396b733): what an automatic load costs.


class HeadReplay(CheckoutReplay):
    """The server's summary version for each entity (`summary_head`), and a
    CLI that refuses a dirty draft the way the real one does."""

    def __init__(self, versions: dict[str, int] | None = None, *, delay: float = 0.0) -> None:
        super().__init__()
        self.versions = versions or {}
        self.heads: list[tuple[str, str]] = []
        self.delay = delay
        self.refuse: dict[str, str] = {}

    async def summary_head(self, kind, ref):
        self.heads.append((kind, ref))
        await asyncio.sleep(self.delay)
        version = self.versions.get(ref)
        return None if version is None else {"version": version, "mode": "recorder"}

    async def run(self, argv, op_id):
        if argv[:2] == ["summary", "checkout"] and argv[3] in self.refuse:
            self.calls.append(list(argv))
            return 2, self.refuse[argv[3]]
        return await super().run(argv, op_id)


def test_a_clean_draft_at_the_servers_version_is_not_checked_out_again(tmp_path):
    replay = HeadReplay({"b2": 3})
    deps = _deps(tmp_path, replay)
    _log(deps.store, "experiment", "set", "b2", "--conclusion", "yes")
    assert asyncio.run(tools.autoload_summaries(deps)) == ["experiment=b2"]
    assert replay.heads == [], "no draft yet: checked out without asking"
    assert replay.calls[-1] == ["summary", "checkout", "--experiment", "b2", "--no-visuals"]
    replay.calls.clear()
    assert asyncio.run(tools.autoload_summaries(deps)) == []
    assert replay.heads == [("experiment", "b2")] and replay.calls == [], "one plain read, no checkout"
    replay.versions["b2"] = 4  # someone else pushed
    assert asyncio.run(tools.autoload_summaries(deps)) == ["experiment=b2"]
    replay.calls.clear()
    replay.versions.pop("b2")  # the read fails: the draft on disk stands
    assert asyncio.run(tools.autoload_summaries(deps)) == [] and replay.calls == []


def test_a_missing_draft_is_checked_out_again(tmp_path):
    replay = HeadReplay({"b2": 3})
    deps = _deps(tmp_path, replay)
    _log(deps.store, "experiment", "set", "b2", "--conclusion", "yes")
    asyncio.run(tools.autoload_summaries(deps))
    Path(deps.store.fact(tools.SUMMARY_DRAFTS)["experiment=b2"]["path"]).unlink()
    replay.calls.clear()
    assert asyncio.run(tools.autoload_summaries(deps)) == ["experiment=b2"]


def test_loading_is_bounded_in_time(tmp_path, monkeypatch):
    monkeypatch.setattr(tools, "AUTOLOAD_TIMEOUT_S", 0.3)
    replay = HeadReplay({"b2": 9}, delay=30.0)
    deps = _deps(tmp_path, replay)
    _log(deps.store, "experiment", "set", "b2", "--conclusion", "yes")
    asyncio.run(tools.autoload_summaries(deps))
    started = time.monotonic()
    assert asyncio.run(tools.autoload_summaries(deps)) == []
    assert time.monotonic() - started < 5, "a hung server costs the bound, not the run"


def test_a_checkout_the_cli_refuses_for_unpushed_edits_is_outlined_as_such(tmp_path):
    """The CLI refuses (exit 2) to replace a draft with unpushed edits the
    daemon never recorded (`summary_cli.DraftDirty`): the outline names it."""
    replay = HeadReplay()
    path = _draft_for("experiment", "b2", PAGE)
    path.write_text(PAGE + "<p>unpushed</p>\n")
    replay.refuse["b2"] = json.dumps({"target": "experiment", "label": "b2", "path": str(path), "version": 3,
                                      "format": "html", "refused": "unpushed edits"})
    deps = _deps(tmp_path, replay)
    _log(deps.store, "experiment", "set", "b2", "--conclusion", "yes")
    assert asyncio.run(tools.autoload_summaries(deps)) == []
    outline = tools.summary_outline(deps.store)
    assert "## Experiment b2 · v3" in outline and tools.OUTLINE_DIRTY in outline
    assert path.read_text().endswith("<p>unpushed</p>\n")


def test_the_daemons_checkout_flags_parse():
    from probe.daemon import precheck

    parsed = precheck.parse(["summary", "checkout", "--experiment", "b2", "--no-visuals"])
    assert parsed.path == "summary checkout" and tools._anchor_key(parsed) == "experiment=b2"


def test_the_html_outline_never_quotes_a_persons_block_as_the_opening(tmp_path):
    """Review finding 7: a person's kept text is theirs, not the page's opening."""
    person = '<p data-owner="human" data-strength="hard">Ada wrote this first.</p>'
    text = ('<article class="ov-page"><!-- kept: h1 -->' + person + "<!-- /kept -->"
            "<h2>Their heading</h2><p>The writer's own opening.</p></article>")
    deps = _deps(tmp_path, CheckoutReplay(text=text))
    _log(deps.store, "experiment", "set", "b2", "--conclusion", "yes")
    asyncio.run(tools.autoload_summaries(deps))
    outline = tools.summary_outline(deps.store)
    assert "- opens: The writer's own opening." in outline and "Ada wrote this" not in outline


def test_the_edit_guard_compares_paths_without_case_on_macos(tmp_path, monkeypatch):
    """Review finding 7: macOS file names ignore case, and `realpath` keeps the
    spelling given; on Linux a differently cased folder is another folder."""
    deps = _deps(tmp_path, CheckoutReplay())
    path = _draft_for("project", "willow", "body\n")
    # The same draft as macOS would name it with other case (here a folder of its own).
    upper = Path(str(path).replace("/summaries/", "/SUMMARIES/"))
    upper.parent.mkdir(parents=True, exist_ok=True)
    upper.write_text("body\n")
    monkeypatch.setattr(tools.sys, "platform", "linux")
    assert asyncio.run(tools.edit_file(deps, str(upper), "body", "x")).startswith("not edited:")
    monkeypatch.setattr(tools.sys, "platform", "darwin")
    assert asyncio.run(tools.edit_file(deps, str(upper), "body", "x")).startswith("edited ")
    assert upper.read_text() == "x\n"


def test_a_mark_outside_markers_is_skipped_and_what_follows_is_read():
    text = ('<article class="ov-page"><p data-owner="human" data-strength="soft">theirs</p>'
            "<h2>After</h2><p>The writer's opening.</p></article>")
    assert tools._shape(text, "html") == (["After"], "The writer's opening.")
