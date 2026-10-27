"""Hidden folders are skipped unless admitted; worktree copies are skipped; both are counted.

A customer's folder import uploaded 78,628 files, 65,491 of them from seven
Claude Code agent worktrees under `.claude/worktrees/agent-*/` -- copies of the
one repo the import was already carrying. Two rules fix it, and both are
tested here against a REAL filesystem and REAL git (`git worktree add`,
`git submodule add`), never a fake of either: the whole failure was a shape
of `.git` nobody's model of the tree had.

* Hidden FOLDERS are skipped unless allowlisted (`.hydra`, `.dvc`, `.aim`,
  `.neptune`) or named with `--include-hidden`; credential stores never.
* A nested git worktree whose main checkout is also under the root is a copy.

Neither may shrink the denominator silently: what is skipped is counted and
said, in the plan, in the desktop's job record and in `backfill.scanned`.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import asdict
from pathlib import Path

import pytest

from probe.cli import backfill as bf
from probe.cli import backfill_evidence as ev
from probe.cli import backfill_run as runner
from probe.cli import telemetry as tm

pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="needs real git")

GIT_ENV = {
    "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
    "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid",
    "GIT_CONFIG_NOSYSTEM": "1",
}


def _git(cwd: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "init.defaultBranch=main", "-c", "protocol.file.allow=always", *args],
        cwd=cwd, check=True, capture_output=True, env={**os.environ, **GIT_ENV},
    )


def _repo(path: Path, files: dict[str, str]) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    _git(path, "init", "-q")
    for rel, text in files.items():
        (path / rel).parent.mkdir(parents=True, exist_ok=True)
        (path / rel).write_text(text)
    _git(path, "add", "-A")
    _git(path, "commit", "-qm", "init")
    return path


def _write(root: Path, rel: str, text: str = "x\n") -> None:
    (root / rel).parent.mkdir(parents=True, exist_ok=True)
    (root / rel).write_text(text)


def _walk(root: Path, include=()):
    warn = ev.WalkWarnings()
    found = sorted(
        str(Path(f.path).relative_to(root.resolve()))
        for f in ev.walk(root, warn, include_hidden=include)
    )
    return found, warn


def _census(root: Path, include=()) -> bf.Census:
    census, _records, _warn, _index, _previous = runner._index(
        root, runner.Report(), include_hidden=include
    )
    return census


@pytest.fixture
def state(tmp_path, monkeypatch):
    # `_index` writes the folder's index under the backfill state dir.
    monkeypatch.setenv("PROBE_BACKFILL_STATE_DIR", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "xdg-state"))


@pytest.fixture
def repo(tmp_path):
    """A research repo with two worktree copies: one Claude Code agent worktree
    under `.claude/`, one ordinary non-dot `trees/` worktree."""
    root = _repo(tmp_path / "research", {"train.py": "print(1)\n", "runs/r1/log.txt": "loss 1\n"})
    _git(root, "worktree", "add", "-q", ".claude/worktrees/agent-x")
    _git(root, "worktree", "add", "-q", "trees/wt2")
    return root


# -- worktree copies ----------------------------------------------------------


def test_worktree_copies_are_skipped_counted_and_listed(repo, state):
    found, warn = _walk(repo)
    assert found == ["runs/r1/log.txt", "train.py"], "only the main checkout is imported"
    assert [f.pair() for f in warn.skipped_worktrees] == [
        # The `.git` FILE plus the two tracked files, in each copy.
        (".claude/worktrees/agent-x", 3),
        ("trees/wt2", 3),
    ]
    # The agent worktree is named as the copy it is, not folded into `.claude`,
    # and `.claude` -- nothing of its own but the worktrees -- is not listed.
    assert warn.skipped_hidden == []

    lines = runner.skipped_lines(_census(repo))
    assert ("Skipped 2 git worktrees (6 files): checkouts of a repo this import already "
            "carries.") in lines
    assert "  .claude/worktrees/agent-x (3 files)" in lines
    assert "  trees/wt2 (3 files)" in lines


def test_a_hidden_folder_beside_a_worktree_is_still_listed_as_hidden(repo, state):
    _write(repo, ".claude/settings.json", "{}\n")
    _found, warn = _walk(repo)
    assert [f.pair() for f in warn.skipped_hidden] == [(".claude", 1)]
    assert [f.path for f in warn.skipped_worktrees] == [".claude/worktrees/agent-x", "trees/wt2"]


def test_a_relative_gitdir_and_a_symlinked_root_are_resolved_before_comparing(repo, tmp_path, state):
    marker = repo / "trees" / "wt2" / ".git"
    marker.write_text("gitdir: ../../.git/worktrees/wt2\n")
    link = tmp_path / "via-link"
    link.symlink_to(repo, target_is_directory=True)
    found, warn = _walk(link)
    assert found == ["runs/r1/log.txt", "train.py"]
    assert [f.path for f in warn.skipped_worktrees] == [".claude/worktrees/agent-x", "trees/wt2"]


def test_a_worktree_named_like_a_hidden_folder_counts_as_a_worktree(repo, state):
    _git(repo, "worktree", "add", "-q", "-b", "dot-wt", ".wt")
    _found, warn = _walk(repo)
    assert ".wt" in [f.path for f in warn.skipped_worktrees]
    assert ".wt" not in [f.path for f in warn.skipped_hidden]


def test_a_submodule_is_not_a_copy(tmp_path, state):
    upstream = _repo(tmp_path / "upstream", {"lib.py": "x = 1\n"})
    root = _repo(tmp_path / "research", {"train.py": "print(1)\n"})
    _git(root, "submodule", "add", "-q", str(upstream), "vendor/lib")
    assert (root / "vendor" / "lib" / ".git").is_file(), "a submodule's .git is a file too"
    found, warn = _walk(root)
    assert "vendor/lib/lib.py" in found
    assert warn.skipped_worktrees == []


def test_a_worktree_of_a_repo_outside_the_root_is_the_only_copy_and_is_imported(tmp_path, state):
    elsewhere = _repo(tmp_path / "elsewhere", {"model.py": "w = 1\n"})
    root = tmp_path / "research"
    _write(root, "notes.md", "hi\n")
    _git(elsewhere, "worktree", "add", "-q", str(root / "checkout"))
    found, warn = _walk(root)
    assert "checkout/model.py" in found
    assert warn.skipped_worktrees == []


def test_a_bare_repos_worktrees_are_the_only_checkouts_and_are_imported(tmp_path, state):
    """`git clone --bare url proj/.git` puts a bare repo where a main checkout's
    `.git` would be: `proj` then LOOKS like the main working tree but holds
    nothing, and every worktree is a checkout nobody else carries."""
    upstream = _repo(tmp_path / "upstream", {"model.py": "w = 1\n"})
    root = tmp_path / "proj"
    _git(tmp_path, "clone", "-q", "--bare", str(upstream), str(root / ".git"))
    _git(root / ".git", "worktree", "add", "-q", str(root / "main"))
    _write(root, "main/only-here.csv", "a,b\n")
    found, warn = _walk(root)
    assert "main/model.py" in found and "main/only-here.csv" in found
    assert warn.skipped_worktrees == []


def test_a_worktree_is_kept_when_its_main_checkout_is_itself_skipped(tmp_path, state):
    """No checkout of the repo would be imported: the worktree is not a copy of
    anything this import carries. `--include-hidden` that admits the main
    checkout makes the worktree a copy again."""
    root = tmp_path / "research"
    main = _repo(root / ".repos" / "x", {"train.py": "print(1)\n"})
    _git(main, "worktree", "add", "-q", str(root / "x-feat"))
    _write(root, "x-feat/outputs/metrics.json", "{}\n")
    found, warn = _walk(root)
    assert "x-feat/outputs/metrics.json" in found and "x-feat/train.py" in found
    assert [f.path for f in warn.skipped_hidden] == [".repos"]
    assert warn.skipped_worktrees == []
    found, warn = _walk(root, include=(".repos",))
    assert ".repos/x/train.py" in found and "x-feat/train.py" not in found
    assert [f.path for f in warn.skipped_worktrees] == ["x-feat"]


def test_dvc_cache_and_tmp_are_copies_but_dvc_config_is_imported(tmp_path, state):
    for rel in (".dvc/config", ".dvc/cache/files/md5/ab/cdef", ".dvc/tmp/lock", "data/x.csv"):
        _write(tmp_path, rel)
    found, warn = _walk(tmp_path)
    assert found == [".dvc/config", "data/x.csv"]
    assert [f.pair() for f in warn.skipped_hidden] == [(".dvc/cache", 1), (".dvc/tmp", 1)]


def test_a_census_an_older_cli_saved_re_walks_by_the_older_rules(repo, state):
    """A queued job a previous CLI approved re-walks by ITS rules at the end;
    otherwise the hidden and worktree files it approved read as deleted and the
    job reports them unfinished on every resume."""
    _write(repo, ".claude/settings.json", "{}\n")
    legacy = bf.Census(**{"files": 1, "bytes": 1, "linked_dirs": [], "unreadable_dirs": []})
    assert legacy.walk_rules == 0 and _census(repo).walk_rules == bf.WALK_RULES
    warn = ev.WalkWarnings()
    found = {str(Path(f.path).relative_to(repo)) for f in ev.walk(repo, warn, legacy=True)}
    assert {".claude/settings.json", "trees/wt2/train.py"} <= found
    assert warn.skipped_hidden == [] and warn.skipped_worktrees == []


def test_the_import_root_is_never_skipped_even_when_it_is_a_worktree(repo, state):
    found, warn = _walk(repo / "trees" / "wt2")
    assert "train.py" in found and warn.skipped_worktrees == []


# -- hidden folders ------------------------------------------------------------


def test_research_dot_folders_are_imported_and_other_hidden_folders_are_skipped(tmp_path, state):
    for rel in (".hydra/config.yaml", ".dvc/config", ".aim/run.json", ".neptune/run.json",
                ".claude/settings.json", ".codex/x", ".somethingnew/y", ".somethingnew/z",
                "train.py", ".gitignore"):
        _write(tmp_path, rel)
    found, warn = _walk(tmp_path)
    assert found == [".aim/run.json", ".dvc/config", ".gitignore", ".hydra/config.yaml",
                     ".neptune/run.json", "train.py"]
    assert [f.pair() for f in warn.skipped_hidden] == [
        (".claude", 1), (".codex", 1), (".somethingnew", 2),
    ]
    lines = runner.skipped_lines(_census(tmp_path))
    assert ("Skipped hidden folders: .somethingnew (2 files), .claude (1 file), "
            ".codex (1 file).") in lines


def test_a_nested_hidden_folder_is_skipped_and_named_by_its_path(tmp_path, state):
    _write(tmp_path, "proj/.cursor/rules.md")
    _write(tmp_path, "proj/train.py")
    found, warn = _walk(tmp_path)
    assert found == ["proj/train.py"]
    assert [f.pair() for f in warn.skipped_hidden] == [("proj/.cursor", 1)]


def test_include_hidden_admits_a_skipped_folder(tmp_path, state):
    _write(tmp_path, ".somethingnew/y")
    _write(tmp_path, "train.py")
    found, warn = _walk(tmp_path, include=(".somethingnew",))
    assert found == [".somethingnew/y", "train.py"] and warn.skipped_hidden == []


def test_include_hidden_never_admits_a_credential_store(tmp_path, state):
    _write(tmp_path, ".ssh/id_rsa", "SECRET")
    _write(tmp_path, ".aws/credentials", "SECRET")
    _write(tmp_path, "train.py")
    found, warn = _walk(tmp_path, include=(".ssh", ".aws"))
    assert found == ["train.py"]
    # Pruned outright, like `.git`: never walked, so never listed either.
    assert warn.skipped_hidden == []
    assert runner.refused_includes((".ssh", ".aws", ".somethingnew")) == [
        "Not included: .ssh, .aws — credential stores are never imported."
    ]
    census = _census(tmp_path, include=(".ssh", ".somethingnew"))
    assert census.include_hidden == (".somethingnew",), "a refused name is not carried forward"


def test_credential_stores_stay_refused_whatever_the_allowlist_says(tmp_path, state, monkeypatch):
    """Named apart from the allowlist so a future edit to it cannot admit one."""
    assert bf.CREDENTIAL_DIRS == {
        ".ssh", ".aws", ".gnupg", ".kube", ".docker", ".azure", ".gcloud", ".config",
    }
    assert bf.CREDENTIAL_DIRS <= bf.SKIP_DIRS
    assert bf.CREDENTIAL_DIRS.isdisjoint(bf.RESEARCH_DOT_DIRS)
    monkeypatch.setattr(bf, "RESEARCH_DOT_DIRS", bf.RESEARCH_DOT_DIRS | bf.CREDENTIAL_DIRS)
    for name in bf.CREDENTIAL_DIRS:
        assert not bf.hidden_admitted(name, include=(name,)), name
        _write(tmp_path, f"{name}/secret", "SECRET")
    _write(tmp_path, "train.py")
    found, _warn = _walk(tmp_path, include=tuple(bf.CREDENTIAL_DIRS))
    assert found == ["train.py"]


def test_include_hidden_takes_names_not_paths():
    assert bf.hidden_includes([".claude", "codex", ".claude/", ".claude"]) == (".claude", ".codex")
    for bad in ("a/.b", "", ".", ".."):
        with pytest.raises(ValueError):
            bf.hidden_includes([bad])


# -- the denominator -----------------------------------------------------------


def test_the_census_still_counts_what_it_skips(repo, state):
    _write(repo, ".claude/settings.json", "{}\n")
    _write(repo, ".codex/x")
    census = _census(repo)
    assert census.files == 2, "the import's own denominator: what it places"
    assert census.skipped_worktrees == ((".claude/worktrees/agent-x", 3), ("trees/wt2", 3))
    assert census.skipped_hidden == ((".claude", 1), (".codex", 1))
    assert census.on_disk == 2 + 6 + 2
    assert not census.incomplete, "a skip by rule is said, not reported as a partial import"
    assert "(8 more skipped" in census.describe()


def test_the_skips_survive_a_queued_job_round_trip(repo, state):
    """The census travels in a background job's saved payload (JSON); the
    closing re-walk reads `include_hidden` back from it."""
    _write(repo, ".somethingnew/y")
    census = _census(repo, include=(".somethingnew",))
    back = bf.Census(**json.loads(json.dumps(asdict(census))))
    assert back.skipped_json() == census.skipped_json()
    assert list(back.include_hidden) == [".somethingnew"]
    found, _warn = _walk(repo, include=back.include_hidden)
    assert ".somethingnew/y" in found


def test_skipped_json_is_bounded_and_carries_every_count(tmp_path):
    census = bf.Census(
        files=1, bytes=1,
        skipped_hidden=tuple((f".h{i}", i) for i in range(bf.SKIPPED_LISTED + 5)),
        skipped_worktrees=(("trees/a", 7),),
    )
    data = census.skipped_json()
    assert len(data["hiddenFolders"]) == bf.SKIPPED_LISTED
    assert data["hiddenFolders"][0] == {"path": f".h{bf.SKIPPED_LISTED + 4}", "files": bf.SKIPPED_LISTED + 4}
    assert data["hiddenFolderCount"] == bf.SKIPPED_LISTED + 5
    assert data["hiddenFiles"] == sum(range(bf.SKIPPED_LISTED + 5))
    assert data["worktrees"] == [{"path": "trees/a", "files": 7}]
    assert (data["worktreeCount"], data["worktreeFiles"]) == (1, 7)


def test_the_desktop_job_record_carries_the_skips(tmp_path, monkeypatch):
    from probe.cli import desktop, import_jobs

    census = bf.Census(files=1, bytes=1, skipped_hidden=((".claude", 4),),
                       skipped_worktrees=((".claude/worktrees/agent-x", 9),))
    job = {"id": "j", "kind": "folder", "label": "Folder · x", "state": "running",
           "created_at": "t", "updated_at": "t", "progress": {}, "report": [],
           "skipped": census.skipped_json()}
    shown = desktop._public_job(job)
    assert shown["skipped"]["worktrees"] == [{"path": ".claude/worktrees/agent-x", "files": 9}]
    assert shown["skipped"]["hiddenFolders"] == [{"path": ".claude", "files": 4}]
    assert (shown["skipped"]["worktreeFiles"], shown["skipped"]["hiddenFiles"]) == (9, 4)
    assert "skipped" not in desktop._public_job(job, summary=True), "list rows stay light"
    del job["skipped"]
    assert "skipped" not in desktop._public_job(job), "additive: absent when not recorded"
    # No active worker: a foreground import records nothing anywhere.
    monkeypatch.setattr(import_jobs, "_active_job", None)
    import_jobs.remember_skipped(census.skipped_json())


# -- the whole import ----------------------------------------------------------


@pytest.fixture
def harness(tmp_path, monkeypatch):
    from test_backfill_scoped_orchestration import make_harness

    return make_harness(tmp_path, monkeypatch)


def test_an_import_uploads_the_main_checkout_only_and_reports_what_it_skipped(harness):
    h = harness
    _git(h.folder, "init", "-q")
    _git(h.folder, "add", "-A")
    _git(h.folder, "commit", "-qm", "init")
    _git(h.folder, "worktree", "add", "-q", ".claude/worktrees/agent-x")
    _git(h.folder, "worktree", "add", "-q", "trees/wt2")
    _write(h.folder, ".claude/settings.json", "{}\n")
    _write(h.folder, ".somethingnew/y", "kept = True\n")
    _write(h.folder, ".hydra/config.yaml", "experiment: x\n")
    lines = h.run(include_hidden=(".somethingnew",))
    assert h.classified == [[".hydra/config.yaml", ".somethingnew/y", "a.py"]]
    assert ("Skipped 2 git worktrees (4 files): checkouts of a repo this import already "
            "carries.") in lines
    assert any(line.startswith("Skipped hidden folders: .claude (1 file)") for line in lines)
    scanned = next(data for event, data in h.events if event == tm.EVENT_BACKFILL_SCANNED)
    assert scanned["files"] == 3
    assert (scanned["skipped_hidden_dirs"], scanned["skipped_hidden_files"]) == (1, 1)
    assert (scanned["skipped_worktrees"], scanned["skipped_worktree_files"]) == (2, 4)
    assert h.report()["queued"] == [".hydra/config.yaml", ".somethingnew/y", "a.py"]
    h.drain()
    uploaded = sorted(call[1] for call in h.remote.calls)
    assert uploaded == [".hydra/config.yaml", ".somethingnew/y", "a.py"]
    # The closing re-walk admits the same folder, so nothing reads as deleted
    # and the re-run confirms every receipt.
    lines = h.run(include_hidden=(".somethingnew",))
    assert h.report()["delivered"] == [".hydra/config.yaml", ".somethingnew/y", "a.py"]
    assert any("Every observed file has a receipt" in line for line in lines)


def test_probe_backfill_hands_include_hidden_to_the_import(monkeypatch, tmp_path):
    import sys

    import probe.cli.main  # noqa: F401 -- `probe.cli.main` the attribute is the entry FUNCTION

    main_mod = sys.modules["probe.cli.main"]
    seen = {}
    monkeypatch.setattr(bf, "run", lambda **kwargs: seen.update(kwargs) or [])
    monkeypatch.setattr("probe.cli.bootstrap.ensure_persistent_install",
                        lambda: type("Boot", (), {"message": ""})())
    monkeypatch.setattr(tm.TelemetryContext, "emit", lambda self, *a, **kw: None)
    main_mod.backfill(
        folder=str(tmp_path), agent="claude", project=None, source_id=None,
        import_changed=False, import_unverified=False, retry_dead=False, review_excluded=False,
        transcripts=False, transcripts_only=False, transcripts_budget_mb=None,
        include_hidden=["claude", ".somethingnew"],
    )
    assert seen["include_hidden"] == (".claude", ".somethingnew")


def test_scanned_counts_are_numbers_only():
    from probe.cli import backfill_import

    counts = backfill_import._skip_counts(
        bf.Census(files=0, bytes=0, skipped_hidden=((".claude", 2),),
                  skipped_worktrees=(("t/a", 5), ("t/b", 5)))
    )
    assert counts == {"skipped_hidden_dirs": 1, "skipped_hidden_files": 2,
                      "skipped_worktrees": 2, "skipped_worktree_files": 10}


def test_an_empty_import_still_emits_the_scanned_counts(harness):
    h = harness
    (h.folder / "a.py").unlink()
    _write(h.folder, ".codex/x")
    lines = h.run()
    assert any("no files to import" in line for line in lines)
    scanned = next(data for event, data in h.events if event == tm.EVENT_BACKFILL_SCANNED)
    assert scanned["files"] == 0 and scanned["skipped_hidden_files"] == 1
    assert any(line.startswith("Skipped hidden folders: .codex (1 file)") for line in lines)
