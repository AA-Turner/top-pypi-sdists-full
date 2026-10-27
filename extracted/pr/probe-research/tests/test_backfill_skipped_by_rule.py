"""A folder imported before the skip rules, imported again: skipped, not absent.

CLI 0.328.0 started skipping hidden folders and nested git worktree copies
(`test_backfill_hidden_and_worktrees.py`). A folder an OLDER CLI imported keeps
those files in its coverage store, and the next census did not see them, so
they read as "previously observed files are absent" -- 65,491 of them for one
customer -- and `vanished` holds a project's reconstruction until its files
come back, which a skipped file never does.

The store here was written by RELEASED CLI 0.327.0, not by this tree
(`fixtures/coverage_0_327_0/make_store.py` says how): a real git repo with an
agent worktree under `.claude/worktrees/agent-x`, every file approved and
delivered except one the plan left undecided. The re-import is this tree's real
`execute` (`test_backfill_scoped_orchestration.make_harness`: only the server
and the model are substituted), over the folder rebuilt with real git.
"""

from __future__ import annotations

import json
import os
import shutil
import sqlite3
import subprocess
from dataclasses import asdict
from pathlib import Path

import pytest

from probe.cli import backfill as bf
from probe.cli import backfill_reconstruction as rec
from probe.cli import telemetry
from probe.cli import backfill_coverage as cov
from probe.cli.backfill_coverage import Coverage, SkipRule, Scope, WalkSkips, skipped_folders
from probe.cli.backfill_ledger import fingerprint

from test_backfill_scoped_orchestration import make_harness

pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="needs real git")

FIXTURE = Path(__file__).parent / "fixtures" / "coverage_0_327_0"
LAYOUT = json.loads((FIXTURE / "layout.json").read_text())
SOURCE_ID = (FIXTURE / "source_id").read_text().strip()
#: Saved before the harness swaps it out: one test runs the real thing.
REAL_RECONSTRUCTION = rec.complete_reconstruction

WORKTREE = LAYOUT["worktree"]
MAIN = sorted(LAYOUT["committed"])
WORKTREE_FILES = sorted(
    [f"{WORKTREE}/{rel}" for rel in (*LAYOUT["committed"], ".git")]
    + [rel for rel in LAYOUT["untracked"] if rel.startswith(WORKTREE + "/")]
)
HIDDEN_FILES = [".claude/settings.json"]
ENV = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
       "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid",
       "GIT_CONFIG_NOSYSTEM": "1"}


def _git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", "-c", "init.defaultBranch=main", *args], cwd=cwd, check=True,
                   capture_output=True, env=ENV)


def _write(root: Path, files: dict[str, str]) -> None:
    for rel, text in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text)


@pytest.fixture
def old_import(tmp_path, monkeypatch):
    """The folder and the 0.327.0 store, where the next import finds them."""
    h = make_harness(tmp_path, monkeypatch)
    for path in list(h.folder.iterdir()):
        path.unlink()
    _git(h.folder, "init", "-q")
    _write(h.folder, LAYOUT["committed"])
    _git(h.folder, "add", "-A")
    _git(h.folder, "commit", "-qm", "init")
    _git(h.folder, "worktree", "add", "-q", WORKTREE)
    _write(h.folder, LAYOUT["untracked"])
    h.projects.update({project["id"]: dict(project) for project in LAYOUT["projects"]})

    scope = Scope.resolve(h.client)
    assert asdict(scope) == LAYOUT["scope"]  # the store's identity, or it is refused
    base = tmp_path / "state" / "v2" / scope.key
    (base / SOURCE_ID).mkdir(parents=True)
    shutil.copyfile(FIXTURE / "coverage.sqlite3", base / SOURCE_ID / "coverage.sqlite3")
    (base / "sources.json").write_text(json.dumps({SOURCE_ID: {
        "paths": [str(h.folder.resolve())], "fingerprint": fingerprint(h.folder),
        "import_device_id": "device", "created_at": "2026-10-25T00:00:00Z"}}))
    return h


def _event(h, name):
    return [data for event, data in h.events if event == name][-1]


def test_files_an_older_cli_imported_from_a_worktree_or_hidden_folder_are_skipped_not_absent(
    old_import,
):
    h = old_import
    lines = h.run()
    report = h.report()
    assert report["vanished"] == []
    assert report["skipped"] == sorted(HIDDEN_FILES + WORKTREE_FILES)
    assert report["delivered"] == MAIN
    with h.coverage().writer() as coverage:
        rules = coverage.skipped_rules()
        assert coverage.source_id == SOURCE_ID  # the old store, not a new one
    assert rules == {**dict.fromkeys(HIDDEN_FILES, SkipRule.HIDDEN_FOLDER),
                     **dict.fromkeys(WORKTREE_FILES, SkipRule.WORKTREE_COPY)}
    text = "\n".join(lines)
    assert "absent" not in text
    assert (f"{len(HIDDEN_FILES + WORKTREE_FILES)} previously observed files are now skipped "
            "(hidden folders and worktree copies)") in text
    assert "Every observed file has a receipt" in text
    assert h.outcome == telemetry.BackfillOutcome.SUCCESS

    summary = _event(h, telemetry.EVENT_BACKFILL_SUMMARY)
    assert (summary["absent_files"], summary["skipped_by_rule_files"]) == (0, 8)
    scanned = _event(h, telemetry.EVENT_BACKFILL_SCANNED)
    assert (scanned["skipped_worktrees"], scanned["skipped_worktree_files"]) == (1, 7)
    assert (scanned["skipped_hidden_dirs"], scanned["skipped_hidden_files"]) == (1, 1)

    # The per-file report says it too, by rule.
    per_file = json.loads((h.coverage().directory / "coverage.json").read_text())
    assert per_file["files"]["skipped"] == report["skipped"]
    assert per_file["skipped"][HIDDEN_FILES[0]] == "hidden_folder"


def test_the_plan_json_carries_what_the_walk_skipped(old_import):
    """The files the old import delivered are organized on this import (#3488),
    so a plan is made, and its `plan.json` names the skips beside the counts:
    the desktop job record's fields (`Census.skipped_json`), added, not moved."""
    h = old_import
    h.run()
    plan = json.loads((h.coverage().directory / "plan.json").read_text())
    assert plan["schema"] == "probe.backfill.plan/1" and "totals" in plan
    assert plan["totals"]["already_imported"] == len(MAIN)
    skipped = plan["skipped"]
    assert skipped["worktrees"] == [{"path": WORKTREE, "files": 7}]
    assert (skipped["worktreeCount"], skipped["worktreeFiles"]) == (1, 7)
    assert skipped["hiddenFolders"] == [{"path": ".claude", "files": 1}]
    assert (skipped["hiddenFolderCount"], skipped["hiddenFiles"]) == (1, 1)
    assert skipped["includedHidden"] == []


class _Server:
    """What reconstruction reads: readable artifacts and a project document."""

    def __init__(self):
        self.transport = self

    def presign_download_batch(self, ids):
        return {"items": {ident: {"download_url": "https://r2.invalid/x"} for ident in ids}}

    def get_project(self, project_id):
        return {"id": project_id, "document": "", "metadata": {"summary": {}}}

    def me(self):
        return {"capabilities": [rec.CAPABILITY]}

    def get(self, path):
        from probe.sdk.errors import NotFoundError

        raise NotFoundError("no page", status=404)

    def post(self, path, body, **kwargs):
        return {"state": "generating"}


def _reconstruct(h, monkeypatch):
    drafted = []

    def generate(inputs, directory, *, agent, agents=None):
        drafted.append(inputs)
        return rec._render(json.dumps({"sections": [
            {"title": "Purpose", "claims": [{"text": "It trains once.", "sources": ["F001"]}]},
        ]}), inputs)

    monkeypatch.setattr(rec, "_generate", generate)
    with h.coverage().writer() as coverage:
        lines = REAL_RECONSTRUCTION(_Server(), h.folder, coverage, None, agent=bf.Agent.CLAUDE,
                                    interactive=False, yes=False)
    return lines, drafted


def test_reconstruction_drafts_from_the_imported_files_and_waits_for_no_skipped_one(
    old_import, monkeypatch,
):
    """Before the fix the undecided worktree file read as absent with no project,
    and `complete_reconstruction` returned "waiting for reviewed file placement"
    for every project, on every run."""
    h = old_import
    h.run()
    lines, drafted = _reconstruct(h, monkeypatch)
    assert not any("waiting" in line for line in lines), lines
    (inputs,) = drafted  # project-a; project-b held only worktree copies
    assert inputs["project_id"] == "project-a" and inputs["inventory_count"] == len(MAIN)
    assert sorted(source["path"] for source in inputs["sources"].values()) == MAIN
    assert any(line.startswith("project-a: ") or "Draft saved" in line for line in lines)
    assert ("1 project(s) hold only files now skipped (hidden folders and worktree copies); "
            "they are not drafted from this folder: project-b.") in lines


def test_a_file_deleted_from_disk_is_still_absent_even_inside_a_skipped_folder(
    old_import, monkeypatch,
):
    h = old_import
    (h.folder / "notes" / "gone.md").unlink()
    (h.folder / WORKTREE / "old.py").unlink()
    lines = h.run()
    report = h.report()
    gone = sorted(["notes/gone.md", f"{WORKTREE}/old.py"])
    assert report["vanished"] == gone
    assert set(gone).isdisjoint(report["skipped"])
    assert ("2 previously observed files are absent (1 of them in hidden folders or worktree "
            "copies the import skips, so nothing waits for them)") in "\n".join(lines)
    summary = _event(h, telemetry.EVENT_BACKFILL_SUMMARY)
    assert (summary["absent_files"], summary["absent_skipped_files"],
            summary["skipped_by_rule_files"]) == (2, 1, 7)
    with h.coverage().writer() as coverage:  # the worktree file keeps its rule
        assert coverage.skipped_rules(on_disk=False) == {f"{WORKTREE}/old.py": "worktree_copy"}
    # A real absence of an imported file still holds its project, as before.
    lines, drafted = _reconstruct(h, monkeypatch)
    assert not drafted
    assert "project-a: reconstruction waiting for file delivery" in "\n".join(lines)


def test_a_skipped_file_deleted_before_the_next_import_becomes_absent(old_import, monkeypatch):
    """Across two imports: skipped while on disk, absent once deleted -- and,
    still out of the import by its rule, it holds no draft."""
    h = old_import
    h.run()
    assert f"{WORKTREE}/old.py" in h.report()["skipped"]
    (h.folder / WORKTREE / "old.py").unlink()
    h.run()
    report = h.report()
    assert report["vanished"] == [f"{WORKTREE}/old.py"]
    assert f"{WORKTREE}/old.py" not in report["skipped"]
    lines, drafted = _reconstruct(h, monkeypatch)
    assert not any("waiting" in line for line in lines), lines
    assert [inputs["project_id"] for inputs in drafted] == ["project-a"]


@pytest.mark.parametrize("first_reimport", [True, False], ids=["after", "before"])
def test_removing_the_agent_worktree_does_not_stall_reconstruction_again(
    old_import, monkeypatch, first_reimport,
):
    """A finished agent's worktree is removed (`git worktree remove`), and the
    walk no longer lists it. Removed after a re-import, its files keep the rule
    recorded then; removed before any (an older import, then the cleanup), the
    path alone places them under `.claude`, which the walk skips. Either way
    they are absent -- they are gone -- and hold nothing: before, the undecided
    `wip.py` held every project's draft."""
    h = old_import
    if first_reimport:
        h.run()
    _git(h.folder, "worktree", "remove", "--force", WORKTREE)
    lines = h.run()
    report = h.report()
    assert report["vanished"] == WORKTREE_FILES
    assert report["skipped"] == HIDDEN_FILES
    assert (f"{len(WORKTREE_FILES)} previously observed files are absent ({len(WORKTREE_FILES)} "
            "of them in hidden folders or worktree copies") in "\n".join(lines)
    summary = _event(h, telemetry.EVENT_BACKFILL_SUMMARY)
    assert (summary["absent_files"], summary["absent_skipped_files"]) == (7, 7)
    with h.coverage().writer() as coverage:
        rule = SkipRule.WORKTREE_COPY if first_reimport else SkipRule.HIDDEN_FOLDER
        assert coverage.skipped_rules(on_disk=False) == dict.fromkeys(WORKTREE_FILES, rule)
    lines, drafted = _reconstruct(h, monkeypatch)
    assert not any("waiting" in line for line in lines), lines
    assert [inputs["project_id"] for inputs in drafted] == ["project-a"]


def test_a_folder_left_with_only_skipped_files_reports_them_skipped(old_import):
    """The empty-folder exit observes too, and no later re-walk corrects it."""
    h = old_import
    for rel in MAIN:
        (h.folder / rel).unlink()
    h.run()
    report = h.report()
    assert report["vanished"] == MAIN
    assert report["skipped"] == sorted(HIDDEN_FILES + WORKTREE_FILES)
    summary = _event(h, telemetry.EVENT_BACKFILL_SUMMARY)
    assert (summary["absent_files"], summary["skipped_by_rule_files"]) == (len(MAIN), 8)


def test_every_census_of_a_reimport_is_given_the_walks_skips(old_import, monkeypatch):
    calls = []
    real = cov.Coverage.observe

    def spy(self, root, paths, **kwargs):
        calls.append(kwargs.get("skipped"))
        return real(self, root, paths, **kwargs)

    monkeypatch.setattr(cov.Coverage, "observe", spy)
    old_import.run()
    assert len(calls) >= 2
    assert all(isinstance(c, WalkSkips) and c.worktrees == (WORKTREE,) for c in calls), calls


def test_admitting_the_hidden_folder_again_brings_its_file_back_and_the_worktree_stays_skipped(
    old_import,
):
    """`skipped` is recomputed by every census, both ways."""
    h = old_import
    h.run()
    assert HIDDEN_FILES[0] in h.report()["skipped"]
    h.run(include_hidden=(".claude",))
    report = h.report()
    assert HIDDEN_FILES[0] in report["delivered"]  # same bytes, same receipt
    assert report["skipped"] == WORKTREE_FILES and report["vanished"] == []
    with h.coverage().writer() as coverage:
        assert set(coverage.skipped_rules().values()) == {SkipRule.WORKTREE_COPY}


def test_the_old_store_is_migrated_in_place_keeping_its_identity_and_receipts(old_import):
    """Two additive columns. The identity and its schema are unchanged, which is
    what lets the release that wrote the store open it again (checked against
    released 0.327.0 on a migrated real store, outside CI); every approval and
    receipt it made survives."""
    h = old_import
    h.run()
    path = h.coverage().path
    with sqlite3.connect(path) as conn:
        columns = [row[1] for row in conn.execute("PRAGMA table_info(files)")]
        identity = json.loads(conn.execute(
            "SELECT value FROM meta WHERE key='identity'").fetchone()[0])
        receipts = conn.execute("SELECT count(*) FROM versions WHERE receipt IS NOT NULL").fetchone()
    assert columns[-2:] == ["skipped", "skipped_on_disk"]
    assert identity["schema"] == "probe.backfill.coverage/3"
    assert receipts == (11,)
    with sqlite3.connect(FIXTURE / "coverage.sqlite3") as conn:  # the fixture is untouched
        assert "skipped" not in [row[1] for row in conn.execute("PRAGMA table_info(files)")]


def test_a_queued_jobs_census_names_its_skips_after_the_json_round_trip():
    """A background job carries its census as JSON (`_background_payload`): the
    skipped folders come back as lists, and still name the same folders."""
    census = bf.Census(files=1, bytes=1, skipped_hidden=((".claude", 1),),
                       skipped_worktrees=((WORKTREE, 7),), include_hidden=(".neptune2",),
                       walk_rules=bf.WALK_RULES)
    again = bf.Census(**json.loads(json.dumps(asdict(census))))
    for skips in (skipped_folders(census), skipped_folders(again)):
        assert (skips.worktrees, skips.hidden, skips.legacy) == ((WORKTREE,), (".claude",), False)
        assert skips.hidden_rule((".claude", "worktrees")) and not skips.hidden_rule(("src",))
        assert not skips.hidden_rule((".neptune2",))  # admitted by --include-hidden
        assert skips.hidden_rule((".dvc", "cache")) and not skips.hidden_rule((".dvc",))
    # An older CLI's census walked by the rules before the skips: none apply.
    assert skipped_folders(bf.Census(files=1, bytes=1)) == WalkSkips(legacy=True)


def _store(tmp_path, files):
    root = tmp_path / "folder"
    for rel, text in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text)
    scope = Scope("https://example.test", "tenant-a", "workspace-a")
    return root, Coverage.for_folder(root, scope, directory=tmp_path / "state")


def test_a_broken_symlink_in_a_skipped_folder_is_skipped_like_the_walk_counts_it(tmp_path):
    root, store = _store(tmp_path, {"a.md": "a", ".claude/settings.json": "{}"})
    (root / ".claude" / "latest.log").symlink_to(root / "nowhere.log")
    with store.writer() as coverage:
        coverage.observe(root, ["a.md", ".claude/settings.json", ".claude/latest.log"])
        coverage.observe(root, ["a.md"], skipped=WalkSkips(hidden=(".claude",)))
        report = coverage.report()
    assert report["skipped"] == [".claude/latest.log", ".claude/settings.json"]
    assert report["vanished"] == []


def test_rules_stand_without_skips_or_under_a_legacy_walk(tmp_path):
    """A census given no skips keeps the rules recorded before (forgetting to
    pass them cannot turn skipped files back into absent ones), and so does a
    queued job resumed under the rules before the skips, which say nothing
    about them; neither adds one."""
    root, store = _store(tmp_path, {"a.md": "a", ".claude/settings.json": "{}", ".x/y.md": "y"})
    with store.writer() as coverage:
        coverage.observe(root, ["a.md", ".claude/settings.json", ".x/y.md"])
        coverage.observe(root, ["a.md", ".x/y.md"], skipped=WalkSkips(hidden=(".claude",)))
        for skips in (None, WalkSkips(legacy=True)):
            coverage.observe(root, ["a.md"], skipped=skips)
            assert coverage.report()["skipped"] == [".claude/settings.json"]
            assert coverage.report()["vanished"] == [".x/y.md"]  # none added


def test_a_recorded_worktree_rule_lapses_once_its_folder_is_walked_again(tmp_path):
    """Its main checkout moved out of the import, `wt/` is no worktree copy any
    more: the walk carries it, and a file deleted from it is a real absence."""
    root, store = _store(tmp_path, {"main.py": "m", "wt/a.csv": "a", "wt/b.csv": "b"})
    no_hidden = lambda parts: False  # noqa: E731
    with store.writer() as coverage:
        coverage.observe(root, ["main.py", "wt/a.csv", "wt/b.csv"])
        coverage.observe(root, ["main.py"], skipped=WalkSkips(worktrees=("wt",), hidden_rule=no_hidden))
        assert coverage.report()["skipped"] == ["wt/a.csv", "wt/b.csv"]
        (root / "wt" / "a.csv").unlink()
        coverage.observe(root, ["main.py", "wt/b.csv"], skipped=WalkSkips(hidden_rule=no_hidden))
        assert coverage.report()["vanished"] == ["wt/a.csv"]
        assert coverage.skipped_rules(on_disk=None) == {}


def test_the_hidden_rule_matches_the_walk_for_a_dvc_root():
    from probe.cli.backfill_evidence import skipped_by_hidden_rule

    assert skipped_by_hidden_rule(("cache",), root_name=".dvc")
    assert not skipped_by_hidden_rule(("cache",), root_name="project")
    assert skipped_by_hidden_rule(("a", ".claude", "worktrees"))
    assert not skipped_by_hidden_rule(("a", ".hydra"))  # a research dot-folder is walked
