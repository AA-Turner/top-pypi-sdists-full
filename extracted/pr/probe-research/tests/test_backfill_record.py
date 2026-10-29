"""The record pass: an imported project recorded by the researcher's own skills.

What is pinned, each against the regression it exists for:

  * the prompt is the skills verbatim plus mechanics (an import's own writing
    rules made 1,032 hex-named, template-described runs, 2026-10-28);
  * the session's `probe` (`backfill_record_tool`, run as the agent's shell
    runs it) refuses links, uploads, creates and deletes, refuses an entity the
    import did not make with the nearest real names, refuses a field a person
    wrote, edits documents at once and stages every write to Probe;
  * the applier sends each op once (a rerun and a crash resume double
    nothing), merges a page that moved meanwhile, refuses a conflicting merge,
    masks credentials, and stops -- keeping its place -- when Probe is down;
  * a failed session never fails the import and is finished by the next run;
    an unchanged project is not recorded twice.

The fake client is checked against the real `Client`'s signatures, so a
keyword the fake accepts and production refuses fails here first.
"""

from __future__ import annotations

import inspect
import json
import os
import re
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from probe.cli import backfill as bf
from probe.cli import backfill_oplog as oplog
from probe.cli import backfill_prompts as prompts
from probe.cli import backfill_record as record
from probe.cli import backfill_record_tool as tool
from probe.cli import backfill_structure as structure
from probe.cli.backfill_ledger import is_import_agent_cwd
from probe.cli.import_agent_settings import Lane
from probe.cli.summary_cli import SERIES_ATTR, compose_draft
from probe.sdk import errors
from probe.sdk.client import Client
from probe.sdk.transport import Page

P = "11111111-1111-4111-8111-111111111111"
E = "22222222-2222-4222-8222-222222222222"
R1, R2, R3 = ("33333333-3333-4333-8333-33333333333" + str(n) for n in (1, 2, 3))

#: A credential shape the upload gate masks (the same family the redaction tests use).
TOKEN = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"


# -- a production-shaped fake Probe ---------------------------------------------


def _lift(text: str) -> tuple[str, list]:
    """What the server does with a pushed HTML draft: the series block out."""
    match = re.match(rf'<script type="application/json" {SERIES_ATTR}>\n(.*?)\n</script>\n',
                     text, re.S)
    if not match:
        return text, []
    return text[match.end():], json.loads(match.group(1).replace("<\\/", "</"))


class Probe:
    def __init__(self):
        self.project = {"id": P, "slug": "odyssey", "name": "Odyssey", "description": "d",
                        "notes": "", "notes_version": 0}
        self.experiments = {E: {"id": E, "slug": "lr-sweep", "name": "lr sweep",
                                "question": "Which lr?", "conclusion": None, "notes": "",
                                "notes_version": 0}}
        self.runs = {
            R1: {"id": R1, "slug": "brave-otter-1", "name": "run-a", "name_customized": True,
                 "description": "Tests a grader.", "description_customized": False,
                 "notes": "", "notes_version": 0, "status": "completed",
                 "summary_metrics": {"reward": 1}, "config": {"lr": 0.1}},
            R2: {"id": R2, "slug": "calm-fox-2", "name": "Pinned by Ana", "name_customized": True,
                 "description": None, "description_customized": False, "notes": "",
                 "notes_version": 0, "status": "untracked", "summary_metrics": {"reward": 0},
                 "config": {}},
        }
        self.pages = {(P, None): {"html": "<article><p>Old intro.</p></article>", "series": [],
                                  "version": 2},
                      (P, E): {"html": "", "series": [], "version": 0}}
        self.writes: list[tuple] = []
        self.fail_next: Exception | None = None

    def _maybe_fail(self):
        if self.fail_next is not None:
            exc, self.fail_next = self.fail_next, None
            raise exc

    def get_project(self, project_id):
        return dict(self.project)

    def get_experiment(self, experiment_id, *, project_id=None):
        return dict(self.experiments[experiment_id])

    def get_run(self, run_id):
        return dict(self.runs[run_id])

    def list_runs(self, *, experiment_id=None, project_id=None, direct=False, tags=None,
                  unfiled=False, **params):
        ids = sorted(self.runs)
        start = int(params.get("cursor") or 0)
        limit = 1  # one a page: paging is exercised
        page = ids[start:start + limit]
        nxt = str(start + limit) if start + limit < len(ids) else None
        return Page(items=[dict(self.runs[i], project_id=P) for i in page], next_cursor=nxt)

    def get_summary(self, *, project=None, experiment=None, format=None):
        page = self.pages[(project, experiment)]
        return {"format": "html", "html": page["html"], "series": page["series"],
                "version": page["version"]}

    def put_summary(self, markdown=None, *, expected_version, project=None, experiment=None,
                    session_id=None, directed=False, html=None, series=None):
        self._maybe_fail()
        page = self.pages[(project, experiment)]
        if expected_version != page["version"]:
            raise errors.ConflictError("moved", detail={"version": page["version"]})
        page["html"], page["series"] = _lift(html)
        page["version"] += 1
        self.writes.append(("page", project, experiment))
        return {"version": page["version"], "html": page["html"], "series": page["series"]}

    def _replace_notes(self, entity, entity_id, text, *, base_version, op_key):
        self._maybe_fail()
        row = {"project": self.project, "experiment": self.experiments.get(entity_id),
               "run": self.runs.get(entity_id)}[entity]
        if base_version is not None and base_version != row["notes_version"]:
            raise errors.ConflictError("moved", detail={"version": row["notes_version"]})
        row["notes"] = text
        row["notes_version"] += 1
        self.writes.append(("note", entity, entity_id))
        return {"notes_version": row["notes_version"]}

    def update_run(self, run_id, *, name=None, description=None, notes=None, status=None,
                   authored_by=None):
        self._maybe_fail()
        assert authored_by == "agent"
        row = self.runs[run_id]
        for key, value in (("name", name), ("description", description)):
            if value is not None:
                row[key] = value
        self.writes.append(("run", run_id, name, description))
        return dict(row)

    def set_project_metric(self, project_id, key, *, goal, reduce=None):
        self._maybe_fail()
        self.metric = {"project": project_id, "key": key, "goal": goal, "reduce": reduce}
        self.writes.append(("metric", project_id, key, goal))
        return dict(self.metric)

    def update_experiment(self, experiment_id, *, question=None, conclusion=None, name=None,
                          description=None, document=None, tags=None, metadata=None,
                          summary=None, authored_by=None, project_id=None):
        self._maybe_fail()
        row = self.experiments[experiment_id]
        for key, value in (("question", question), ("conclusion", conclusion), ("name", name)):
            if value is not None:
                row[key] = value
        self.writes.append(("experiment", experiment_id))
        return dict(row)


@pytest.mark.parametrize(("method", "sent"), [
    ("update_run", {"name", "description", "authored_by"}),
    ("update_experiment", {"question", "conclusion", "name", "authored_by", "project_id"}),
    ("put_summary", {"html", "expected_version", "project", "experiment"}),
    ("get_summary", {"project", "experiment", "format"}),
    ("_replace_notes", {"base_version", "op_key"}),
    ("list_runs", {"project_id"}),
    ("get_experiment", {"project_id"}),
    ("set_project_metric", {"goal", "reduce"}),
])
def test_the_fake_takes_only_what_the_real_client_takes(method, sent):
    """The record pass sends these keywords; the real Client must take each
    (a `**kwargs` fake accepts a wrong one silently)."""
    real = inspect.signature(getattr(Client, method)).parameters
    fake = inspect.signature(getattr(Probe, method)).parameters
    assert sent <= set(real) and sent <= set(fake), (method, sent - set(real))


class Coverage:
    """The coverage store's surface `listing_for` and `complete_record` read."""

    def __init__(self, directory: Path):
        self.directory = directory
        self._meta = {structure.META_KEY: {
            "experiments": {"sweep": {"id": E, "slug": "lr-sweep", "name": "lr sweep",
                                      "question": "Which lr?", "project_id": P}},
            "runs": {"sweep/run-a": {"id": R1, "project_id": P, "experiment": "sweep"},
                     "sweep/run-b": {"id": R2, "project_id": P, "experiment": "sweep"}},
        }}
        self.conn = None

    def meta(self, key, default=None):
        return json.loads(json.dumps(self._meta.get(key, default)))

    def put_meta(self, key, value):
        self._meta[key] = json.loads(json.dumps(value))

    def rows(self):
        note = json.dumps({"notes": f"the grader log, token {TOKEN}"})
        return [{"path": "sweep/run-a/log.txt", "project_id": P, "manifest": note},
                {"path": "README.md", "project_id": P}]

    def planned_placements(self):
        return [{"level": structure.Level.RUN.value, "folder": "sweep/run-a", "path": "x"}]


@pytest.fixture
def probe():
    return Probe()


@pytest.fixture
def listing(probe, tmp_path):
    return record.listing_for(probe, Coverage(tmp_path), P)


# -- what the import made, read from Probe ---------------------------------------


def test_the_listing_reads_every_page_of_runs_and_marks_what_a_person_wrote(listing):
    runs = {run["folder"]: run for run in listing["runs"]}
    assert set(runs) == {"sweep/run-a", "sweep/run-b"}
    # The import's own folder name is the import's to replace; a person's name is not.
    assert runs["sweep/run-a"]["locked"] == []
    assert runs["sweep/run-b"]["locked"] == ["name"]
    assert runs["sweep/run-a"]["experiment"] == "lr-sweep"
    # Unit notes ride beside their run, masked whole before the cut.
    (note,) = runs["sweep/run-a"]["import_notes"]
    assert note.startswith("log.txt: the grader log") and TOKEN not in note
    assert listing["project"]["page"]["version"] == 2
    assert listing["experiments"][0]["page"]["draft"].startswith('<script type="application/json"')


# -- the prompt --------------------------------------------------------------------


def _fake_agent(commands, calls, *, ok=True):
    """A `launch_agent` that runs the session's REAL `probe` launcher, as the
    agent's shell would, then reports `ok`."""
    def launch(folder, prompt, **kwargs):
        calls.append({"prompt": prompt, **kwargs})
        exe = Path(kwargs["path_prepend"]) / "probe"
        for argv, stdin in commands(kwargs):
            subprocess.run([str(exe), *argv], input=stdin or "", text=True, capture_output=True,
                           cwd=kwargs["workdir"], env={**os.environ}, check=False)
        return ok, "Recorded." if ok else "Error: the model stopped"
    return launch


def test_the_session_reads_the_skills_verbatim_and_runs_on_the_record_lane(
        listing, tmp_path, monkeypatch):
    from probe import skill_versions
    from probe.daemon.bite import SHARED_SKILLS, skills_text

    calls: list = []
    monkeypatch.setattr(bf, "launch_agent", _fake_agent(lambda kw: [], calls))
    record.run_sessions(listing, tmp_path / "folder", tmp_path / "root", agent=bf.Agent.CLAUDE)
    (call,) = calls
    assert skills_text(SHARED_SKILLS, reader=skill_versions.MAIN_AGENT) in call["prompt"]
    assert "sweep/run-a" in call["prompt"] and "a person wrote its name" in call["prompt"]
    assert call["tools"] == record.RECORD_TOOLS
    assert "settings" not in call  # no settings given: the lane's builtin launch


def test_only_the_record_session_may_run_probe_and_codex_keeps_no_network(
        listing, tmp_path, monkeypatch):
    """The classifier and unit agents still cannot run `probe` (2026-10-26: an
    agent that could uploaded 1,583 duplicates); Codex gets no allowlist and
    the same argv as every other lane (its sandbox, no network)."""
    assert "Bash(probe:" not in bf.AGENT_TOOLS
    assert "Bash(probe:*)" in record.RECORD_TOOLS
    calls: list = []
    monkeypatch.setattr(bf, "launch_agent", _fake_agent(lambda kw: [], calls))
    record.run_sessions(listing, tmp_path / "f", tmp_path / "root", agent=bf.Agent.CODEX)
    assert calls[0]["tools"] is None
    monkeypatch.setattr(bf, "supported_flags", lambda binary, agent: None)
    monkeypatch.setattr(bf, "codex_features", lambda binary: None)
    argv = bf.agent_argv(bf.Agent.CODEX, "/bin/codex", Path("/f"), workdir=Path("/w"))
    assert not any("network" in part for part in argv)


# -- the session's `probe` -----------------------------------------------------------


@pytest.fixture
def shim(listing, tmp_path):
    work = tmp_path / "work"
    work.mkdir()
    data = {**listing, "session": "s1", "folder": str(tmp_path),
            "writes": {"project": True, "experiments": True, "runs": True}}
    path = tmp_path / "listing.json"
    path.write_text(json.dumps(data))
    launcher = tmp_path / "probe"
    launcher.write_text(tool.launcher_script(path, work))
    launcher.chmod(0o700)

    def run(*argv, stdin=""):
        proc = subprocess.run([str(launcher), *argv], input=stdin, text=True, capture_output=True,
                              cwd=work, check=False)
        return proc.returncode, proc.stdout, proc.stderr

    run.work = work
    return run


def _ops(work: Path) -> list[dict]:
    return oplog.read(work / tool.LOG_FILE)[0]


@pytest.mark.parametrize("argv", [
    ("edge", "add", "--source", "run:a", "--relation", "derived_from", "--target", "run:b"),
    ("experiment", "fork", "lr-sweep", "lr-sweep-2", "--question", "q"),
    ("checkpoint", "use", "checkpoint:x@step1", "--run", "sweep/run-a"),
    ("run", "fork", "sweep/run-a"),
    ("run", "child", "sweep/run-a"),
])
def test_an_import_makes_no_links(shim, argv):
    code, _, err = shim(*argv)
    assert code == 1 and "imports make no links" in err
    assert _ops(shim.work) == []


@pytest.mark.parametrize("argv", [
    ("artifact", "add", "sweep/run-a", "x.txt"),
    ("experiment", "create", "new-one", "--question", "q"),
    ("run", "delete", "sweep/run-a"),
    ("session", "track", "off"),
])
def test_uploads_creates_deletes_and_the_switch_are_refused(shim, argv):
    code, _, err = shim(*argv)
    assert code == 1 and err.startswith("refused:")
    assert _ops(shim.work) == []


def test_an_entity_this_import_did_not_make_is_refused_with_the_nearest_names(shim):
    code, _, err = shim("run", "set", "sweep/run-c", "--name", "x")
    assert code == 1 and "nearest: sweep/run-b, sweep/run-a" in err


def test_a_field_a_person_wrote_is_refused(shim):
    code, _, err = shim("run", "set", "sweep/run-b", "--name", "Better")
    assert code == 1 and "a person wrote this run's name" in err
    code, _, _ = shim("run", "set", "sweep/run-b", "--description", "Scores 0 of 1.")
    assert code == 0


def test_writes_to_probe_are_staged_with_ids_and_documents_change_at_once(shim):
    code, out, _ = shim("run", "set", "sweep/run-a", "--name", "Grader passes",
                        "--description", "Rewards the fix; reward 1.")
    assert code == 0 and json.loads(out)["staged"]
    shim("experiment", "set", "lr-sweep", "--conclusion", "lr 0.1 wins: 1 of 2 runs pass.")
    _, out, _ = shim("summary", "checkout", "--project", "odyssey")
    page = Path(json.loads(out)["path"])
    code, out, _ = shim("draft", "edit", str(page), stdin=(
        "<<<<<<< OLD\n<p>Old intro.</p>\n======= NEW\n<p>New intro.</p>\n>>>>>>> END\n"))
    assert code == 0 and "<p>New intro.</p>" in page.read_text()
    # An edit is local until it is pushed.
    assert [op["kind"] for op in _ops(shim.work)] == ["run_set", "experiment_set"]
    shim("summary", "push", "--project", "odyssey")
    shim("notes", "append", "--run", "sweep/run-a", "--text", "Rerun after the fix.")
    ops = _ops(shim.work)
    assert [op["kind"] for op in ops] == ["run_set", "experiment_set", "page", "note"]
    assert len({op["id"] for op in ops}) == 4 and [op["seq"] for op in ops] == [1, 2, 3, 4]
    assert ops[0]["target"] == {"kind": "run", "id": R1, "folder": "sweep/run-a",
                                "slug": "brave-otter-1", "under": None}
    assert ops[1]["target"]["slug"] == "lr-sweep" and ops[1]["target"]["under"] == "sweep"
    assert ops[2]["base_version"] == 2


def test_a_batch_runs_each_line_as_a_typed_command(shim):
    batch = shim.work / "b.jsonl"
    batch.write_text("\n".join(json.dumps(line) for line in [
        ["run", "set", "sweep/run-a", "--name", "A"],
        ["probe", "run", "set", "sweep/run-b", "--description", "B"],
        ["edge", "add", "--source", "run:a", "--relation", "derived_from", "--target", "run:b"],
    ]))
    code, out, err = shim("batch", "--from", str(batch))
    assert code == 1 and json.loads(out) == {"ran": 2, "refused": 1}
    assert "line 3" in err and "no links" in err
    assert len(_ops(shim.work)) == 2


def test_session_status_reads_on(shim):
    """The skill's first step: an `off` answer would make the agent write nothing."""
    code, out, _ = shim("session", "status")
    assert code == 0 and json.loads(out)["state"] == "on"


def test_a_document_edited_and_never_pushed_is_staged_at_the_end(shim, listing, tmp_path):
    _, out, _ = shim("notes", "checkout", "--project", "odyssey")
    Path(json.loads(out)["path"]).write_text("What this is: the lr sweep.\n")
    assert _ops(shim.work) == []
    data = json.loads((tmp_path / "listing.json").read_text())
    assert tool.finish(tool.Listing(data, shim.work)) == 1
    (op,) = _ops(shim.work)
    assert op["kind"] == "note" and op["fields"]["text"] == "What this is: the lr sweep.\n"
    assert tool.finish(tool.Listing(data, shim.work)) == 0


# -- applying the log -----------------------------------------------------------------


def _staged(shim):
    shim("run", "set", "sweep/run-a", "--name", "Grader passes", "--description", "Reward 1.")
    shim("experiment", "set", "lr-sweep", "--conclusion", "lr 0.1: 1 of 2 runs pass.")
    shim("notes", "append", "--run", "sweep/run-a", "--text", "Rerun after the fix.")
    _, out, _ = shim("summary", "checkout", "--project", "odyssey")
    page = Path(json.loads(out)["path"])
    page.write_text(page.read_text().replace("<p>Old intro.</p>", "<p>New intro.</p>"))
    shim("summary", "push", "--project", "odyssey")
    return shim.work / tool.LOG_FILE


def test_the_log_is_applied_in_order_and_a_rerun_sends_nothing(shim, probe, listing):
    log = _staged(shim)
    result = record.apply_log(probe, log, listing)
    assert [w[0] for w in probe.writes] == ["run", "experiment", "note", "page"]
    assert probe.runs[R1]["name"] == "Grader passes"
    assert probe.experiments[E]["conclusion"] == "lr 0.1: 1 of 2 runs pass."
    assert probe.runs[R1]["notes"] == "Rerun after the fix."
    assert "<p>New intro.</p>" in probe.pages[(P, None)]["html"]
    assert SERIES_ATTR not in probe.pages[(P, None)]["html"]
    assert result["values"]["run:sweep/run-a"] == {"name": "Grader passes", "description": "Reward 1."}
    probe.writes.clear()
    record.apply_log(probe, log, listing)
    assert probe.writes == []


def test_a_crash_after_a_note_landed_does_not_double_it(shim, probe, listing):
    """The response to a note was lost: Probe has it, the applied log does not.
    The resume finds the head moved, merges, and sends nothing twice."""
    log = _staged(shim)
    record.apply_log(probe, log, listing)
    done = oplog.applied_path(log)
    lines = done.read_text().splitlines()
    done.write_text("\n".join(line for line in lines if '"seq": 3' not in line) + "\n")
    # ... and the crash took the local base copy with it.
    import shutil

    shutil.rmtree(log.parent.parent / "apply")
    probe.writes.clear()
    fresh = record.listing_for(probe, Coverage(log.parent.parent), P)
    record.apply_log(probe, log, {**fresh, "runs": [{**fresh["runs"][0], "notes": "",
                                                    "notes_version": 0}, fresh["runs"][1]]})
    assert probe.runs[R1]["notes"] == "Rerun after the fix."
    assert ("note", "run", R1) not in probe.writes


def test_a_page_that_moved_meanwhile_is_merged_once_and_sent(shim, probe, listing):
    log = _staged(shim)
    # A live session added a paragraph after the import checked the page out.
    probe.pages[(P, None)] = {"html": "<article><p>Old intro.</p></article>\n<p>Live note.</p>",
                              "series": [], "version": 3}
    record.apply_log(probe, log, listing)
    html = probe.pages[(P, None)]["html"]
    assert "<p>New intro.</p>" in html and "<p>Live note.</p>" in html
    assert probe.pages[(P, None)]["version"] == 4


def test_a_conflicting_merge_is_refused_never_forced(shim, probe, listing):
    log = _staged(shim)
    probe.pages[(P, None)] = {"html": "<article><p>A person rewrote the intro.</p></article>",
                              "series": [], "version": 3}
    result = record.apply_log(probe, log, listing)
    assert result["counts"]["page:refused"] == 1
    assert probe.pages[(P, None)]["html"] == "<article><p>A person rewrote the intro.</p></article>"


def test_a_credential_in_staged_text_never_reaches_probe(shim, probe, listing):
    shim("run", "set", "sweep/run-a", "--description", f"Used token {TOKEN}.")
    record.apply_log(probe, shim.work / tool.LOG_FILE, listing)
    assert TOKEN not in json.dumps(probe.runs[R1])


def test_a_hand_written_op_is_checked_like_any_other(shim, probe, listing):
    """The log sits in the agent's work dir: evidence, never authority."""
    log = shim.work / tool.LOG_FILE
    for seq, (target, fields) in enumerate([
        (oplog.target("run", folder="sweep/run-b"), {"name": "Overwritten"}),
        (oplog.target("run", folder="elsewhere/run"), {"name": "Not ours"}),
    ], 1):
        oplog.append(log, oplog.make(oplog.Kind.RUN_SET, target, fields, session="x", seq=seq))
    result = record.apply_log(probe, log, listing)
    assert result["counts"]["run_set:refused"] == 2
    assert probe.runs[R2]["name"] == "Pinned by Ana" and probe.writes == []


def test_a_name_a_person_gave_during_the_session_is_never_written_over(shim, probe, listing):
    """A run's PATCH replaces a person's words even when an agent sends it (only
    the claim flag is monotonic), so the applier re-reads the run first: a name
    a person set after the listing was read stays."""
    shim("run", "set", "sweep/run-a", "--name", "Grader passes", "--description", "Reward 1.")
    probe.runs[R1].update(name="Ana's name", name_customized=True)
    result = record.apply_log(probe, shim.work / tool.LOG_FILE, listing)
    assert result["counts"] == {"dropped": 0, "run_set:refused": 1}
    assert probe.runs[R1]["name"] == "Ana's name" and probe.writes == []


def test_a_placeholder_name_reads_as_no_name_in_the_listing(listing):
    """A run the import created unnamed carries the server's petname: the session
    must see that it has no name yet, or it leaves it so (smoke 2026-10-27: 3 of
    4 runs kept petnames and no description)."""
    runs = {run["folder"]: run for run in listing["runs"]}
    runs["sweep/run-a"].update(name=runs["sweep/run-a"]["slug"], description=None)
    text = record.render_listing(listing)
    line_a = next(line for line in text.splitlines() if "sweep/run-a" in line)
    line_b = next(line for line in text.splitlines() if "sweep/run-b" in line)
    assert "no name yet, no description" in line_a
    assert "name 'Pinned by Ana'" in line_b and "a person wrote its name" in line_b


def test_the_headline_metric_is_staged_from_what_the_runs_logged(shim, probe, listing):
    code, _, err = shim("project", "set", "odyssey", "--metric", "rewrd", "--goal", "max")
    assert code == 1 and "nearest: reward" in err
    code, _, err = shim("project", "set", "odyssey", "--metric", "reward")
    assert code == 1 and "--goal is max or min" in err
    code, _, err = shim("project", "set", "odyssey", "--best", "lr-sweep", "--reason", "x")
    assert code == 1 and "only the headline metric" in err
    code, _, _ = shim("project", "set", "odyssey", "--metric", "reward", "--goal", "max")
    assert code == 0
    (op,) = _ops(shim.work)
    assert op["kind"] == "project_metric" and op["fields"] == {"key": "reward", "goal": "max"}
    record.apply_log(probe, shim.work / tool.LOG_FILE, listing)
    assert probe.metric == {"project": P, "key": "reward", "goal": "max", "reduce": None}


def test_a_symlinked_document_is_never_read_or_staged(shim, listing, tmp_path):
    """A document swapped for a symlink would carry another file's text to Probe."""
    secret = tmp_path / "private.txt"
    secret.write_text("not for Probe")
    _, out, _ = shim("notes", "checkout", "--project", "odyssey")
    note = Path(json.loads(out)["path"])
    note.unlink()
    note.symlink_to(secret)
    code, _, err = shim("notes", "push", "--project", "odyssey")
    assert code == 1 and "not a plain file" in err
    data = json.loads((tmp_path / "listing.json").read_text())
    assert tool.finish(tool.Listing(data, shim.work)) == 0
    assert _ops(shim.work) == []


def test_a_forged_base_version_cannot_write_over_a_newer_page(shim, probe, listing):
    """The log is the agent's: a page op naming the head's version must still be
    pushed from the version the listing saw, so a person's newer text is merged
    or refused, never replaced."""
    log = _staged(shim)
    probe.pages[(P, None)] = {"html": "<article><p>A person rewrote the intro.</p></article>",
                              "series": [], "version": 3}
    ops = [json.loads(line) for line in log.read_text().splitlines()]
    for op in ops:
        if op["kind"] == "page":
            op["base_version"] = 3
    log.write_text("".join(json.dumps(op) + "\n" for op in ops))
    record.apply_log(probe, log, listing)
    assert probe.pages[(P, None)]["html"] == "<article><p>A person rewrote the intro.</p></article>"


def test_a_resume_after_a_merge_sends_the_merged_draft(shim, probe, listing):
    """A merge with a person's paragraph, then Probe goes down before the send:
    the resume sends the merge, not the op's own text over the moved head."""
    log = _staged(shim)
    probe.pages[(P, None)] = {"html": "<article><p>Old intro.</p></article>\n<p>Live note.</p>",
                              "series": [], "version": 3}
    real = probe.put_summary
    calls = {"n": 0}

    def flaky(*args, **kwargs):
        calls["n"] += 1
        if calls["n"] == 2:  # the merged resend
            raise errors.TransportError("connection reset")
        return real(*args, **kwargs)

    probe.put_summary = flaky
    with pytest.raises(record.ApplyStopped):
        record.apply_log(probe, log, listing)
    probe.put_summary = real
    record.apply_log(probe, log, listing)
    html = probe.pages[(P, None)]["html"]
    assert "<p>New intro.</p>" in html and "<p>Live note.</p>" in html


def test_parallel_probe_calls_lose_no_op(listing, tmp_path, monkeypatch):
    """Agents run shell calls side by side: every staged write keeps its own id.
    Two stagers that read the same next sequence would make one id, and the
    reader drops the second as a duplicate."""
    import threading

    real_next = oplog.next_seq
    barrier = threading.Barrier(8, timeout=2)

    def slow_next(path):
        seq = real_next(path)
        try:
            barrier.wait()  # every stager has read the log before any appends
        except threading.BrokenBarrierError:
            pass
        return seq

    monkeypatch.setattr(oplog, "next_seq", slow_next)
    work = tmp_path / "work"
    work.mkdir()
    view = tool.Listing({**listing, "session": "s1"}, work)
    run = view.runs[0]
    threads = [threading.Thread(target=view.stage, args=(oplog.Kind.RUN_SET, "run", run,
                                                         {"description": f"Take {i}."}))
               for i in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    ops = oplog.read(work / tool.LOG_FILE)[0]
    assert len(ops) == 8 and len({op["id"] for op in ops}) == 8


def test_a_malformed_op_line_is_dropped_not_fatal(shim, probe, listing):
    log = _staged(shim)
    bad = oplog.make(oplog.Kind.PAGE, oplog.target("experiment", slug="lr-sweep"), {"html": "x"},
                     session="x", seq=99)
    bad["target"]["under"] = []
    with open(log, "a") as handle:
        handle.write(json.dumps(bad) + "\n")
    result = record.apply_log(probe, log, listing)
    assert result["counts"]["dropped"] == 1
    assert probe.runs[R1]["name"] == "Grader passes"


def test_the_applied_record_sits_outside_the_agents_work_dir(shim):
    log = shim.work / tool.LOG_FILE
    assert oplog.applied_path(log).parent == shim.work.parent


def test_two_entities_never_share_a_document(listing, tmp_path):
    view = tool.Listing(listing, tmp_path)
    a = view.doc_path("run", {"id": R1, "slug": "x" * 85 + "a"}, ".note.md")
    b = view.doc_path("run", {"id": R2, "slug": "x" * 85 + "b"}, ".note.md")
    assert a != b


def test_probe_unreachable_stops_the_applier_and_the_next_run_resumes(shim, probe, listing):
    log = _staged(shim)
    probe.fail_next = errors.TransportError("connection refused")
    with pytest.raises(record.ApplyStopped):
        record.apply_log(probe, log, listing)
    assert probe.writes == []
    record.apply_log(probe, log, listing)
    assert [w[0] for w in probe.writes] == ["run", "experiment", "note", "page"]


# -- the import's step -----------------------------------------------------------------


@pytest.fixture
def importing(probe, tmp_path, monkeypatch):
    monkeypatch.setattr(record, "excerpts", lambda coverage, folder, project_id: ([], []))
    coverage = Coverage(tmp_path / "state")
    (tmp_path / "folder").mkdir()
    return SimpleNamespace(coverage=coverage, folder=tmp_path / "folder", probe=probe)


def _name_runs(kwargs):
    return [(["run", "set", "sweep/run-a", "--name", "Grader passes"], "")]


def test_a_failed_session_never_fails_the_import_and_the_next_run_finishes(importing, monkeypatch):
    calls: list = []
    monkeypatch.setattr(bf, "launch_agent", _fake_agent(_name_runs, calls, ok=False))
    lines = record.complete_record(importing.probe, importing.folder, importing.coverage,
                                   agent=bf.Agent.CLAUDE)
    assert any("did not finish" in line and "the next import finishes it" in line for line in lines)
    assert importing.coverage.meta(record.META_PREFIX + P)["state"] == "partial"
    # What the failed session staged is still applied: each write was checked.
    assert importing.probe.runs[R1]["name"] == "Grader passes"
    monkeypatch.setattr(bf, "launch_agent", _fake_agent(lambda kw: [], calls, ok=True))
    lines = record.complete_record(importing.probe, importing.folder, importing.coverage,
                                   agent=bf.Agent.CLAUDE)
    assert len(calls) == 2
    assert importing.coverage.meta(record.META_PREFIX + P)["state"] == "recorded"
    assert lines and lines[0].startswith("odyssey: recorded by your skills")


def test_an_unchanged_project_is_not_recorded_twice_and_a_new_prompt_records_it_again(
        importing, monkeypatch):
    calls: list = []
    monkeypatch.setattr(bf, "launch_agent", _fake_agent(_name_runs, calls))
    for _ in range(2):
        record.complete_record(importing.probe, importing.folder, importing.coverage,
                               agent=bf.Agent.CLAUDE)
    assert len(calls) == 1
    monkeypatch.setattr(prompts, "RECORD_PROMPT_VERSION", "backfill-record/next")
    record.complete_record(importing.probe, importing.folder, importing.coverage,
                           agent=bf.Agent.CLAUDE)
    assert len(calls) == 2
    # The second pass may change the name the first pass wrote: it is the import's own.
    listing = record.listing_for(importing.probe, importing.coverage, P,
                                 applied=importing.coverage.meta(record.META_PREFIX + P)["applied"])
    assert {r["folder"]: r["locked"] for r in listing["runs"]}["sweep/run-a"] == []


def test_a_project_that_cannot_be_read_is_reported_not_raised(importing, monkeypatch):
    def broken(*args, **kwargs):
        raise OSError("disk")
    monkeypatch.setattr(record, "listing_for", broken)
    lines = record.complete_record(importing.probe, importing.folder, importing.coverage,
                                   agent=bf.Agent.CLAUDE)
    assert lines == [f"{P}: not recorded yet (OSError); the next import retries."]


# -- splitting a large project ------------------------------------------------------------


def test_a_large_project_is_recorded_in_groups_then_one_project_session(monkeypatch):
    monkeypatch.setattr(record, "RUNS_PER_SESSION", 3)
    listing = {"project": {"id": P, "slug": "big"},
               "experiments": [{"slug": f"e{i}", "under": f"e{i}"} for i in range(3)],
               "runs": ([{"folder": f"e0/r{i}", "experiment": "e0"} for i in range(2)]
                        + [{"folder": f"e1/r{i}", "experiment": "e1"} for i in range(2)]
                        + [{"folder": f"e2/r{i}", "experiment": "e2"} for i in range(1)]
                        + [{"folder": f"d{i}", "experiment": None} for i in range(4)])}
    sessions = record.sessions_for(listing)
    groups = [[e["slug"] for e in s["experiments"]] for s in sessions]
    assert groups == [["e0"], ["e1", "e2"], [], [], ["e0", "e1", "e2"]]
    assert [len(s["runs"]) for s in sessions] == [2, 3, 3, 1, 0]
    assert sessions[-1]["writes"] == {"project": True, "experiments": False, "runs": False}
    assert all(not s["writes"]["project"] for s in sessions[:-1])
    assert "2 runs" in sessions[-1]["summaries"]["e0"]


# -- the record sessions are the import's own automation ----------------------------------


def test_a_record_sessions_transcript_is_never_imported_as_the_researchers_work():
    """Sessions an import starts are Probe's own; the past-sessions import skips
    them by their scratch-dir layout (45 junk sessions on 2026-10-25)."""
    cwd = (f"/s/v2/{'a' * 16}/{P}/record/{P}/{'b' * 32}/s1/work")
    assert is_import_agent_cwd(cwd)
    assert not is_import_agent_cwd(f"/s/v2/{'a' * 16}/{P}/record/{P}/{'b' * 32}/s1")
