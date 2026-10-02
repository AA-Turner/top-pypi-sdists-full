"""Run.snapshot() writes the launch block and lockfile identity."""

from __future__ import annotations

import sys

import pytest

from tests.conftest import open_run

# Storage-agnostic: every case here runs under both snapshot storages.
pytestmark = pytest.mark.usefixtures("code_storage")


def test_snapshot_writes_launch_block(client, tmp_path):
    (tmp_path / "train.py").write_text("print('hi')\n")
    (tmp_path / "uv.lock").write_text("[lock]\n")
    run = open_run(client, experiment="exp-launch")
    run.snapshot(
        cwd=str(tmp_path),
        include_env=False,
        include_gpu=False,
        argv=["python", "train.py", "--seed", "9"],
    )
    row = client.run_bundle(run.id)["run"]
    launch = (row.get("metadata") or {}).get("launch")
    assert launch["schema"] == "probe.launch/1"
    assert launch["process"]["argv"] == ["python", "train.py", "--seed", "9"]
    seeds = {s["name"]: s for s in launch["determinism"]["seeds"]}
    assert seeds["seed"]["value"] == "9"
    assert row.get("env_ref")


def test_snapshot_merges_metadata_not_clobbers(client, tmp_path):
    (tmp_path / "a.py").write_text("a\n")
    run = open_run(client, experiment="exp-meta", metadata={"owner": "mahit"})
    run.snapshot(cwd=str(tmp_path), include_env=False, include_gpu=False)
    row = client.run_bundle(run.id)["run"]
    assert row["metadata"]["owner"] == "mahit"
    assert "launch" in row["metadata"]


def test_snapshot_deps_include_lockfile_hashes(client, tmp_path):
    (tmp_path / "uv.lock").write_text("[lock]\nversion = 1\n")
    run = open_run(client, experiment="exp-lock")
    snap = run.snapshot(cwd=str(tmp_path), include_env=False, include_gpu=False)
    locks = snap["deps"].get("lockfiles")
    assert locks and locks[0]["path"] == "uv.lock" and locks[0]["sha256"]


def test_same_tree_same_execution_record(client, tmp_path):
    """Identity is the code MANIFEST (design doc D1); git provenance -- a
    per-snapshot commit sha + run-id ref -- must NOT be hashed into the
    execution record, or two runs over an identical (non-git) tree would
    mint distinct execution records and never dedupe."""
    (tmp_path / "a.py").write_text("a\n")
    run1 = open_run(client, experiment="exp-dedupe-1")
    run2 = open_run(client, experiment="exp-dedupe-2")
    h1 = run1.snapshot(cwd=str(tmp_path), include_env=False, include_gpu=False)["content_hash"]
    h2 = run2.snapshot(cwd=str(tmp_path), include_env=False, include_gpu=False)["content_hash"]
    assert h1 == h2


def test_execute_auto_snapshots(client, tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_AUTO_SNAPSHOT", "1")
    (tmp_path / "job.py").write_text("print('ok')\n")
    run = open_run(client, experiment="exp-exec")
    run.execute([sys.executable, "job.py"], cwd=str(tmp_path))
    row = client.run_bundle(run.id)["run"]
    launch = (row.get("metadata") or {}).get("launch")
    assert launch is not None
    assert launch["process"]["argv"] == [sys.executable, "job.py"]


def test_execute_auto_snapshot_opt_out(client, tmp_path):
    run = open_run(client, experiment="exp-exec-off")
    run.execute([sys.executable, "-c", "pass"], cwd=str(tmp_path))
    row = client.run_bundle(run.id)["run"]
    assert "launch" not in (row.get("metadata") or {})


def test_execute_survives_snapshot_failure(client, tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_AUTO_SNAPSHOT", "1")
    run = open_run(client, experiment="exp-boom")
    monkeypatch.setattr(
        type(run),
        "snapshot",
        lambda self, **kw: (_ for _ in ()).throw(RuntimeError("capture exploded")),
    )
    with pytest.warns(UserWarning, match="auto-snapshot failed"):
        result = run.execute([sys.executable, "-c", "pass"], cwd=str(tmp_path))
    assert result.returncode == 0  # block claims, never runs


def test_client_run_auto_snapshots(client, monkeypatch, tmp_path):
    # chdir into a plain tmp dir: the open-time snapshot must not depend on the
    # HOST checkout (it would capture the whole repo under test).
    (tmp_path / "a.py").write_text("a\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("PROBE_AUTO_SNAPSHOT", "1")
    run = client.run(
        project="proj-auto",
        experiment="exp-auto-open",
        question="auto-snapshot opens",
    )
    row = client.run_bundle(run.id)["run"]
    assert "launch" in (row.get("metadata") or {})


def test_client_run_snapshot_param_overrides(client, monkeypatch):
    monkeypatch.setenv("PROBE_AUTO_SNAPSHOT", "1")
    run = client.run(
        project="proj-auto2",
        experiment="exp-no-snap",
        question="param wins",
        snapshot=False,
    )
    row = client.run_bundle(run.id)["run"]
    assert "launch" not in (row.get("metadata") or {})


def test_execute_span_attributes_are_scrubbed(client, tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_AUTO_SNAPSHOT", "1")
    run = open_run(client, experiment="exp-span-scrub")
    run.execute([sys.executable, "-c", "pass", "--api-key", "sk-live12345678"], cwd=str(tmp_path))
    spans = client.transport.get(f"/v1/runs/{run.id}/spans")
    process_spans = [s for s in spans if s.get("span_type") == "process"]
    assert process_spans
    for span in process_spans:
        assert "sk-live12345678" not in str(span.get("attributes"))


# --- plan 2.6: capture never depends on being able to write git ----------------
#
# Each of these used to abort the WHOLE capture: the shadow `commit-tree` needed
# an identity and a writable object store, and `read-tree HEAD` needed a born
# branch -- so a bare pod recorded no code, no deps and no argv at all.

import os  # noqa: E402
import stat  # noqa: E402
import subprocess  # noqa: E402

ARGV = ["python", "train.py", "--seed", "7"]


def _git(cwd, *args, env=None):
    subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True,
        env={**os.environ, **(env or {})},
    )


def _refs(repo):
    return subprocess.run(
        ["git", "for-each-ref", "--format=%(refname)"], cwd=repo, capture_output=True, text=True
    ).stdout.split()


def _captured(client, run, cwd):
    snap = run.snapshot(cwd=str(cwd), include_env=False, include_gpu=False, argv=ARGV)
    row = client.run_bundle(run.id)["run"]
    assert row["metadata"]["launch"]["process"]["argv"] == ARGV, "argv captured"
    assert row.get("env_ref") and row["env_ref"] == snap["content_hash"], "env_ref pinned"
    meta = next(
        a["meta"] for a in client.run_bundle(run.id)["artifacts"] if a.get("kind") == "code_snapshot"
    )
    assert "train.py" in meta["paths_text"].split("\n"), "the code itself captured"
    return snap, meta


def _repo_with_commit(root, *, identity=True):
    root.mkdir()
    _git(root, "init", "-q")
    (root / "train.py").write_text("print('train')\n")
    _git(root, "add", "-A")
    _git(
        root, "commit", "-q", "-m", "init",
        env={"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@e.com",
             "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@e.com"},
    )
    (root / "train.py").write_text("print('train, edited')\n")
    return root


def test_no_git_identity_still_captures(client, tmp_path, monkeypatch):
    """A bare pod: no user.name/email anywhere, and auto-detection off -- exactly
    what made the shadow `commit-tree` fail ("Author identity unknown")."""
    repo = _repo_with_commit(tmp_path / "repo")
    _git(repo, "config", "user.useConfigOnly", "true")
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    for var in ("GIT_AUTHOR_NAME", "GIT_AUTHOR_EMAIL", "GIT_COMMITTER_NAME",
                "GIT_COMMITTER_EMAIL", "EMAIL"):
        monkeypatch.delenv(var, raising=False)
    run = open_run(client, experiment="exp-noid")
    snap, meta = _captured(client, run, repo)
    assert meta["vcs"] == "git" and meta["dirty"] is True and not meta.get("git_error")
    assert not [r for r in _refs(repo) if r.startswith("refs/probe/")]


def test_an_unborn_head_still_captures(client, tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    (repo / "train.py").write_text("print('train')\n")
    run = open_run(client, experiment="exp-unborn")
    snap, meta = _captured(client, run, repo)
    assert meta["vcs"] == "git" and meta["dirty"] is True
    assert meta["head"] is None and meta["branch"], "an unborn branch still has a name"
    assert _refs(repo) == []


@pytest.mark.skipif(hasattr(os, "geteuid") and os.geteuid() == 0, reason="root ignores modes")
def test_a_read_only_git_dir_still_captures(client, tmp_path):
    repo = _repo_with_commit(tmp_path / "repo")
    gitdir = repo / ".git"
    modes = {}
    for dirpath, dirnames, filenames in os.walk(gitdir):
        for name in [*dirnames, *filenames]:
            p = os.path.join(dirpath, name)
            modes[p] = os.stat(p).st_mode
        modes[dirpath] = os.stat(dirpath).st_mode
    for p, mode in modes.items():
        os.chmod(p, mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
    try:
        run = open_run(client, experiment="exp-rogit")
        snap, meta = _captured(client, run, repo)
        assert meta["vcs"] == "git" and meta["dirty"] is True and not meta.get("git_error")
    finally:
        for p, mode in sorted(modes.items(), key=lambda kv: len(kv[0])):
            os.chmod(p, mode)


def test_no_git_binary_captures_a_plain_directory_and_says_why(client, tmp_path, monkeypatch):
    repo = _repo_with_commit(tmp_path / "repo")
    empty = tmp_path / "empty-bin"
    empty.mkdir()
    monkeypatch.setenv("PATH", str(empty))
    run = open_run(client, experiment="exp-nogit")
    snap, meta = _captured(client, run, repo)
    # Without git nothing can say whether the tree is dirty: recorded as
    # unknown, never guessed, and the reason is on the row.
    assert meta["vcs"] is None and meta["dirty"] is None
    assert "git is not runnable" in meta["git_error"]
    assert snap["git"] is None and snap["git_error"] == meta["git_error"]


def test_a_git_repo_records_what_was_stored_not_a_shadow_ref(client, app, tmp_path):
    repo = _repo_with_commit(tmp_path / "repo")
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True
    ).stdout.strip()
    run = open_run(client, experiment="exp-uri")
    snap, meta = _captured(client, run, repo)
    row = next(a for a in app.artifacts[run.id] if a.get("kind") == "code_snapshot")
    assert row["uri"].startswith(("probe-manifest:", "probe-artifact:")), row["uri"]
    assert meta["head"] == head and meta["dirty"] is True
    assert _refs(repo) == ["refs/heads/" + meta["branch"]]


def _sha(repo, rev="HEAD"):
    return subprocess.run(
        ["git", "rev-parse", rev], cwd=repo, capture_output=True, text=True, check=True
    ).stdout.strip()


def _notice_count(err: str) -> int:
    return err.count("snapshot-prune-refs --dry-run")


def test_old_refs_are_reported_once_and_never_deleted(client, tmp_path, capfd):
    import warnings

    from probe.sdk import snapshot as snap_mod

    repo = _repo_with_commit(tmp_path / "repo")
    _git(repo, "update-ref", "refs/probe/snapshots/old-run", "HEAD")
    run = open_run(client, experiment="exp-notice")
    # Training scripts often run with warnings ignored. A notice that went
    # through `warnings` was marked shown and never seen; it goes to stderr now.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        run.snapshot(cwd=str(repo), include_env=False, include_gpu=False)
    err = capfd.readouterr().err
    assert _notice_count(err) == 1 and "holds 1 old code-snapshot ref" in err

    snap_mod._NOTICED.clear()  # a new process: the marker file says "shown for 1"
    run.snapshot(cwd=str(repo), include_env=False, include_gpu=False)
    assert _notice_count(capfd.readouterr().err) == 0, "shown once"
    assert "refs/probe/snapshots/old-run" in _refs(repo), "D10: never auto-deleted"

    # More refs than last time (an old Probe on another checkout of this repo
    # still writing them) is news, so it is said again, once.
    _git(repo, "update-ref", "refs/probe/snapshots/newer-run", "HEAD")
    snap_mod._NOTICED.clear()
    run.snapshot(cwd=str(repo), include_env=False, include_gpu=False)
    assert "holds 2 old code-snapshot ref" in capfd.readouterr().err
    snap_mod._NOTICED.clear()
    run.snapshot(cwd=str(repo), include_env=False, include_gpu=False)
    assert _notice_count(capfd.readouterr().err) == 0


def test_the_notice_marker_is_written_only_after_the_notice(client, tmp_path, monkeypatch, capfd):
    from probe.sdk import snapshot as snap_mod

    repo = _repo_with_commit(tmp_path / "repo")
    _git(repo, "update-ref", "refs/probe/snapshots/old-run", "HEAD")
    real_print = print

    def failing_print(*args, **kwargs):
        # The notice could not be written (a closed stderr, say): it was not
        # seen, so it may not be marked as seen.
        if "snapshot-prune-refs" in " ".join(map(str, args)):
            raise OSError("stderr is closed")
        real_print(*args, **kwargs)

    monkeypatch.setattr("builtins.print", failing_print)
    run = open_run(client, experiment="exp-notice-order")
    run.snapshot(cwd=str(repo), include_env=False, include_gpu=False)
    monkeypatch.setattr("builtins.print", real_print)
    common = snap_mod._common_dir(str(repo))
    assert not os.path.exists(snap_mod._notice_marker(common)), "not seen, so not marked"
    snap_mod._NOTICED.clear()
    run.snapshot(cwd=str(repo), include_env=False, include_gpu=False)
    assert _notice_count(capfd.readouterr().err) == 1, "shown on the next capture instead"
    assert os.path.exists(snap_mod._notice_marker(common))


def test_a_corrupt_index_keeps_head_and_branch(client, tmp_path):
    repo = _repo_with_commit(tmp_path / "repo")
    head = _sha(repo)
    (repo / ".git" / "index").write_bytes(b"DIRC-not-really-an-index")
    run = open_run(client, experiment="exp-badindex")
    snap, meta = _captured(client, run, repo)
    # `status` needs the index and HEAD does not: only dirty is unknown.
    assert meta["vcs"] == "git" and meta["head"] == head and meta["branch"]
    assert meta["dirty"] is None
    assert "index" in meta["git_error"], meta["git_error"]
    assert snap["git"]["head"] == head and snap["git_error"] == meta["git_error"]


def _cli_on(app, tmp_path, monkeypatch):
    import importlib

    from tests.conftest import make_client

    cli_main = importlib.import_module("probe.cli.main")
    monkeypatch.setattr(cli_main, "_client", lambda: make_client(app, tmp_spool=tmp_path / "cli"))


def test_prune_dry_run_prints_every_ref_and_sha(tmp_path, capsys):
    from probe import cli

    repo = _repo_with_commit(tmp_path / "repo")
    _git(repo, "update-ref", "refs/probe/snapshots/a", "HEAD")
    assert cli.main(["snapshot-prune-refs", "--cwd", str(repo), "--dry-run", "--force"]) == 0
    out = capsys.readouterr().out
    assert f"would delete refs/probe/snapshots/a {_sha(repo)}" in out and "dry run" in out
    assert "refs/probe/snapshots/a" in _refs(repo), "a dry run changes nothing"


def test_prune_force_removes_loose_and_packed_refs_only(tmp_path, capsys):
    from probe import cli

    repo = _repo_with_commit(tmp_path / "repo")
    for name in ("a", "b"):
        _git(repo, "update-ref", f"refs/probe/snapshots/{name}", "HEAD")
    _git(repo, "pack-refs", "--all")
    _git(repo, "update-ref", "refs/probe/snapshots/c", "HEAD")  # loose
    _git(repo, "update-ref", "refs/probe/other", "HEAD")  # not ours to touch
    assert "refs/probe/snapshots/a" in (repo / ".git" / "packed-refs").read_text()
    sha = _sha(repo)

    assert cli.main(["snapshot-prune-refs", "--cwd", str(repo), "--force"]) == 0
    out = capsys.readouterr().out
    for name in ("a", "b", "c"):
        # Each delete is printed with its sha, so `git update-ref` can undo it.
        assert f"deleted refs/probe/snapshots/{name} {sha}" in out
    assert "deleted 3 ref(s)" in out and "git update-ref <ref> <sha>" in out
    assert "--prune=now" not in out, "never suggest destroying the objects at once"
    left = _refs(repo)
    assert not [r for r in left if r.startswith("refs/probe/snapshots/")]
    assert "refs/probe/other" in left and any(r.startswith("refs/heads/") for r in left)
    assert "refs/probe/snapshots/" not in (repo / ".git" / "packed-refs").read_text()

    assert cli.main(["snapshot-prune-refs", "--cwd", str(repo)]) == 0
    assert "no refs/probe/snapshots" in capsys.readouterr().out


def test_prune_keeps_refs_whose_code_may_exist_nowhere_else(app, client, tmp_path, monkeypatch, capsys):
    """D10: a shadow commit may be the only copy of a dirty tree whose upload
    failed. Without --force or --bundle, only a run whose code-snapshot record
    says every file was stored loses its ref."""
    import uuid

    from probe import cli

    repo = _repo_with_commit(tmp_path / "repo")
    stored, unstored, legacy = (open_run(client, experiment=f"exp-prune-{i}") for i in range(3))
    unknown = str(uuid.uuid4())  # a run this account cannot see
    rows = {stored.id: {"n_pending_upload": 0}, unstored.id: {"n_pending_upload": 2}, legacy.id: {}}
    for rid, meta in rows.items():
        app.artifacts.setdefault(rid, []).append(
            {"id": str(uuid.uuid4()), "kind": "code_snapshot", "name": "code", "meta": meta}
        )
    nothing = open_run(client, experiment="exp-prune-none")  # no code-snapshot row at all
    for rid in (stored.id, unstored.id, legacy.id, nothing.id, unknown, "not-a-run"):
        _git(repo, "update-ref", f"refs/probe/snapshots/{rid}", "HEAD")
    _cli_on(app, tmp_path, monkeypatch)
    sha = _sha(repo)

    assert cli.main(["snapshot-prune-refs", "--cwd", str(repo)]) == 1, "kept refs exit non-zero"
    out = capsys.readouterr().out
    assert f"deleted refs/probe/snapshots/{stored.id} {sha}" in out
    left = set(_refs(repo))
    assert f"refs/probe/snapshots/{stored.id}" not in left
    for rid, why in (
        (unstored.id, "2 file(s) of its code never reached Probe"),
        (legacy.id, "predates upload accounting"),
        (nothing.id, "no code-snapshot record"),
        (unknown, "cannot be checked"),
        ("not-a-run", "not a run id"),
    ):
        assert f"refs/probe/snapshots/{rid}" in left, rid
        assert f"kept refs/probe/snapshots/{rid} {sha}  (" in out and why in out, rid
    assert "--bundle FILE" in out and "--force" in out


def test_prune_bundle_backs_every_ref_up_then_deletes_it(tmp_path, capsys):
    from probe import cli

    repo = _repo_with_commit(tmp_path / "repo")
    _git(repo, "update-ref", "refs/probe/snapshots/a", "HEAD")
    _git(repo, "update-ref", "refs/probe/snapshots/b", "HEAD")
    sha = _sha(repo)

    inside = repo / "backup.bundle"  # code capture would upload it
    assert cli.main(["snapshot-prune-refs", "--cwd", str(repo), "--bundle", str(inside)]) == 1
    assert "inside the working tree" in capsys.readouterr().err
    assert not inside.exists() and "refs/probe/snapshots/a" in _refs(repo), "nothing deleted"

    bundle = tmp_path / "backup.bundle"
    assert cli.main(["snapshot-prune-refs", "--cwd", str(repo), "--bundle", str(bundle)]) == 0
    out = capsys.readouterr().out
    assert f"backed up 2 ref(s) to {bundle}" in out and f"deleted refs/probe/snapshots/b {sha}" in out
    assert not [r for r in _refs(repo) if r.startswith("refs/probe/snapshots/")]

    # The bundle restores them, even after gc has dropped the objects.
    _git(repo, "reflog", "expire", "--expire=now", "--all")
    _git(repo, "gc", "-q", "--prune=now")
    _git(repo, "fetch", "-q", str(bundle), "refs/probe/snapshots/*:refs/probe/snapshots/*")
    assert {"refs/probe/snapshots/a", "refs/probe/snapshots/b"} <= set(_refs(repo))

    assert cli.main(["snapshot-prune-refs", "--cwd", str(repo), "--bundle", str(bundle)]) == 1
    assert "already exists" in capsys.readouterr().err, "never overwrites a backup"


def test_prune_refuses_a_ref_that_moved_after_it_was_listed(tmp_path):
    from probe.sdk import snapshot as snap_mod

    repo = _repo_with_commit(tmp_path / "repo")
    _git(repo, "update-ref", "refs/probe/snapshots/a", "HEAD")
    listed = snap_mod.old_snapshot_refs(str(repo))
    _git(repo, "commit", "-q", "-am", "moved",
         env={"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@e.com",
              "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@e.com"})
    _git(repo, "update-ref", "refs/probe/snapshots/a", "HEAD")
    with pytest.raises(snap_mod.SnapshotError):
        snap_mod.prune_snapshot_refs(str(repo), listed)
    assert "refs/probe/snapshots/a" in _refs(repo), "a commit nobody saw is not deleted"


def test_prune_resets_the_notice(client, tmp_path, capfd):
    from probe import cli
    from probe.sdk import snapshot as snap_mod

    repo = _repo_with_commit(tmp_path / "repo")
    for name in ("a", "b", "c"):
        _git(repo, "update-ref", f"refs/probe/snapshots/{name}", "HEAD")
    run = open_run(client, experiment="exp-notice-reset")
    run.snapshot(cwd=str(repo), include_env=False, include_gpu=False)
    assert _notice_count(capfd.readouterr().err) == 1
    assert cli.main(["snapshot-prune-refs", "--cwd", str(repo), "--force"]) == 0
    capfd.readouterr()
    _git(repo, "update-ref", "refs/probe/snapshots/d", "HEAD")  # fewer than before
    snap_mod._NOTICED.clear()
    run.snapshot(cwd=str(repo), include_env=False, include_gpu=False)
    assert "holds 1 old code-snapshot ref" in capfd.readouterr().err


def test_prune_says_why_git_cannot_read_the_repo(tmp_path, monkeypatch, capsys):
    from probe import cli

    repo = _repo_with_commit(tmp_path / "repo")
    empty = tmp_path / "empty-bin"
    empty.mkdir()
    monkeypatch.setenv("PATH", str(empty))
    assert cli.main(["snapshot-prune-refs", "--cwd", str(repo)]) == 1
    err = capsys.readouterr().err
    assert "git is not runnable" in err and "not inside a git repository" not in err


def test_doctor_reports_old_snapshot_refs(tmp_path, monkeypatch):
    from probe.cli import doctor

    repo = _repo_with_commit(tmp_path / "repo")
    assert "none in this repo" in doctor._snapshot_ref_rows(str(repo))[1]
    _git(repo, "update-ref", "refs/probe/snapshots/a", "HEAD")
    _git(repo, "update-ref", "refs/probe/snapshots/b", "HEAD")
    rows = doctor._snapshot_ref_rows(str(repo))
    assert rows[0] == "Code capture" and "2 in this repo" in rows[1]
    assert "snapshot-prune-refs --dry-run" in rows[1]
    assert doctor._snapshot_ref_rows(str(tmp_path)) == [], "nothing outside a repo"
    monkeypatch.chdir(repo)
    assert "2 in this repo" in doctor.render(doctor.Capabilities())
