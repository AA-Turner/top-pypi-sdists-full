"""Ruling 19: before a Cloud Computer stops, unsaved git work is pushed to a safety branch.

Real git, real repositories, a real (bare, local) remote — nothing faked but the network.
Breaks these tests name:
* uncommitted or untracked work, or commits no remote has, stays on the machine only;
* the snapshot touches the person's working tree, index or branches;
* a same-day safety branch is overwritten (an earlier snapshot lost);
* a repository that could not be saved is not named, with its reason.
"""

from __future__ import annotations

import asyncio
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import pytest

from matrx_scraper.cloud_browser.worker.http_app import MACHINE_CAPABILITIES
from matrx_scraper.cloud_browser.worker.machine_git_safety import push_safety_branches

pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="needs git")

NOW = datetime(2026, 11, 2, 18, 30, 5, tzinfo=UTC)


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-c", "user.name=T", "-c", "user.email=t@example.com", "-c", "init.defaultBranch=main", *args],
        cwd=cwd, check=True, capture_output=True, text=True,
    ).stdout.strip()


def repo_with_remote(home: Path, name: str, remotes: Path) -> tuple[Path, Path]:
    bare = remotes / f"{name}.git"
    bare.mkdir(parents=True)
    git(bare, "init", "--bare", "-q")
    work = home / "repos" / name
    work.mkdir(parents=True)
    git(work, "init", "-q")
    (work / "README.md").write_text("hello\n")
    git(work, "add", "README.md")
    git(work, "commit", "-q", "-m", "first")
    git(work, "remote", "add", "origin", str(bare))
    git(work, "push", "-q", "origin", "HEAD:refs/heads/main")
    git(work, "fetch", "-q", "origin")
    return work, bare


def save(home: Path, now: datetime = NOW) -> dict:
    import os

    return asyncio.run(push_safety_branches(home, machine_id="m-123", base_env=os.environ,
                                            git_timeout_seconds=30, token_file="/nonexistent", now=now))


def test_uncommitted_and_untracked_work_reaches_a_safety_branch_without_touching_the_tree(tmp_path: Path) -> None:
    home, remotes = tmp_path / "home", tmp_path / "remotes"
    work, bare = repo_with_remote(home, "app", remotes)
    (work / "README.md").write_text("hello\nedited, not committed\n")
    (work / "new_idea.py").write_text("print('not yet tracked')\n")
    git(work, "add", "README.md")  # half staged: the index must stay exactly as it is
    status_before = git(work, "status", "--porcelain")

    answer = save(home)

    [repo] = answer["safety_branches"]
    assert repo["repo"] == "repos/app" and repo["pushed"] is True
    assert repo["branch"].startswith("safety/m-123-20261102-")
    files = git(bare, "ls-tree", "-r", "--name-only", repo["branch"]).split()
    assert sorted(files) == ["README.md", "new_idea.py"]
    assert "edited, not committed" in git(bare, "show", f"{repo['branch']}:README.md")
    assert git(work, "status", "--porcelain") == status_before
    assert git(work, "rev-parse", "--abbrev-ref", "HEAD") == "main"


def test_a_clean_pushed_repo_is_not_listed_and_unpushed_commits_are_saved(tmp_path: Path) -> None:
    home, remotes = tmp_path / "home", tmp_path / "remotes"
    repo_with_remote(home, "clean", remotes)
    work, bare = repo_with_remote(home, "ahead", remotes)
    (work / "b.txt").write_text("b\n")
    git(work, "add", "b.txt")
    git(work, "commit", "-q", "-m", "local only")
    head = git(work, "rev-parse", "HEAD")

    answer = save(home)

    assert answer["repos_checked"] == 2
    [repo] = answer["safety_branches"]
    assert repo["repo"] == "repos/ahead" and repo["pushed"] is True
    assert git(bare, "rev-parse", repo["branch"]) == head  # exactly the person's commit


def test_a_second_stop_the_same_day_never_overwrites_the_first_snapshot(tmp_path: Path) -> None:
    home, remotes = tmp_path / "home", tmp_path / "remotes"
    work, bare = repo_with_remote(home, "app", remotes)
    (work / "a.txt").write_text("first\n")
    first = save(home)["safety_branches"][0]
    (work / "a.txt").write_text("second\n")
    git(work, "commit", "-q", "--allow-empty", "-m", "moved on")
    second = save(home, NOW.replace(hour=20))["safety_branches"][0]
    assert first["branch"] != second["branch"] and second["pushed"] is True
    assert git(bare, "show", f"{first['branch']}:a.txt") == "first"
    assert git(bare, "show", f"{second['branch']}:a.txt") == "second"


def test_a_repo_that_cannot_be_saved_is_named_with_its_reason(tmp_path: Path) -> None:
    home = tmp_path / "home"
    work = home / "scratch"
    work.mkdir(parents=True)
    git(work, "init", "-q")
    (work / "notes.txt").write_text("only here\n")
    [repo] = save(home)["safety_branches"]
    assert repo["pushed"] is False and "no remote" in repo["reason"]


def test_the_worker_advertises_what_the_save_path_may_ask_for() -> None:
    assert {"cloud_files_flush", "git_safety_branches", "cloud_files_sync_feed"} <= set(MACHINE_CAPABILITIES)


def test_health_carries_the_capabilities_a_plain_browser_worker_has_none() -> None:
    from fastapi.testclient import TestClient

    from matrx_scraper.cloud_browser.worker.http_app import create_worker_app
    from matrx_scraper.cloud_browser.worker.runtime import BrowserWorker

    app = create_worker_app(BrowserWorker(worker_id="w-caps"))
    body = TestClient(app).get("/health").json()
    assert body["capabilities"] == []
    app.state.capabilities = MACHINE_CAPABILITIES
    assert TestClient(app).get("/health").json()["capabilities"] == sorted(MACHINE_CAPABILITIES)


# ── review 2026-11-02: hooks, clones of one remote, SSH remotes, the person's index ──────────


from matrx_scraper.cloud_browser.worker.machine_git_safety import is_ssh_remote  # noqa: E402


def _g(cwd: Path, *a: str) -> str:
    return subprocess.run(["git", "-c", "user.name=T", "-c", "user.email=t@e.com", "-c", "init.defaultBranch=main", *a],
                          cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def _bare(tmp_path: Path) -> Path:
    bare = tmp_path / "r.git"
    bare.mkdir()
    _g(bare, "init", "--bare", "-q")
    return bare


def _clone(home: Path, rel: str, bare: Path) -> Path:
    w = home / rel
    w.parent.mkdir(parents=True, exist_ok=True)
    _g(w.parent, "clone", "-q", str(bare), w.name)
    return w


def _seeded(tmp_path: Path) -> tuple[Path, Path]:
    bare = _bare(tmp_path)
    seed = tmp_path / "seed"
    seed.mkdir()
    _g(seed, "init", "-q")
    (seed / "a.txt").write_text("v1")
    _g(seed, "add", ".")
    _g(seed, "commit", "-qm", "i")
    _g(seed, "push", "-q", str(bare), "main")
    return bare, tmp_path / "home"


def test_three_clones_of_one_remote_each_get_their_own_branch(tmp_path: Path) -> None:
    bare, home = _seeded(tmp_path)
    clones = [_clone(home, rel, bare) for rel in ("repos/app", "work/app", "old/app")]
    for i, w in enumerate(clones):
        (w / "a.txt").write_text(f"clone {i}")
    out = save(home)
    assert len(out["safety_branches"]) == 3 and all(r["pushed"] for r in out["safety_branches"]), out
    branches = {r["branch"] for r in out["safety_branches"]}
    assert len(branches) == 3 and all(b.startswith("safety/m-123-20261102-app-") for b in branches)
    assert sorted(_g(bare, "show", f"{b}:a.txt") for b in branches) == ["clone 0", "clone 1", "clone 2"]


def test_a_failing_pre_push_hook_never_blocks_the_safety_push_and_the_index_is_untouched(tmp_path: Path) -> None:
    bare, home = _seeded(tmp_path)
    w = _clone(home, "app", bare)
    (w / "a.txt").write_text("staged")
    _g(w, "add", "a.txt")
    (w / "a.txt").write_text("staged+unstaged")
    hook = w / ".git/hooks/pre-push"
    hook.write_text("#!/bin/sh\nexit 1\n")
    hook.chmod(0o755)
    index_before = (w / ".git/index").read_bytes()
    before = _g(w, "diff", "--cached"), _g(w, "status", "--porcelain")
    [repo] = save(home)["safety_branches"]
    assert repo["pushed"], repo
    assert _g(bare, "show", f"{repo['branch']}:a.txt") == "staged+unstaged"
    assert (w / ".git/index").read_bytes() == index_before  # never written, not even refreshed
    assert (_g(w, "diff", "--cached"), _g(w, "status", "--porcelain")) == before


def test_an_ssh_remote_is_answered_at_once(tmp_path: Path) -> None:
    home = tmp_path / "home"
    w = home / "app"
    w.mkdir(parents=True)
    _g(w, "init", "-q")
    (w / "a.txt").write_text("x")
    _g(w, "remote", "add", "origin", "git@github.com:someone/app.git")
    [repo] = save(home)["safety_branches"]
    assert repo["pushed"] is False and repo["reason"].startswith("not pushed: ssh remote")
    assert is_ssh_remote("ssh://git@github.com/a/b.git") and not is_ssh_remote("https://github.com/a/b.git")


def test_the_snapshot_starts_from_the_persons_index_not_a_re_read_of_every_file(tmp_path: Path) -> None:
    """The throwaway index is a COPY of the person's (stat cache included), so ``add -A`` hashes
    only files whose stat changed — a 65k-file checkout on the network home is not re-read.
    Proof: a file whose bytes changed with its stat kept (size, mtime; ctime not trusted by this
    repository) keeps the index's blob; a snapshot rebuilt from HEAD would re-hash it."""
    import os

    bare, home = _seeded(tmp_path)
    w = _clone(home, "app", bare)
    _g(w, "config", "core.trustctime", "false")
    old = 1_600_000_000
    (w / "a.txt").write_text("v2")
    os.utime(w / "a.txt", (old, old))
    _g(w, "add", "a.txt")
    (w / "a.txt").write_text("v3")  # same size
    os.utime(w / "a.txt", (old, old))
    (w / "c.txt").write_text("untracked")
    [repo] = save(home)["safety_branches"]
    assert _g(bare, "show", f"{repo['branch']}:a.txt") == "v2"
    assert "c.txt" in _g(bare, "ls-tree", "-r", "--name-only", repo["branch"]).split()


def test_a_walk_that_times_out_cold_is_retried_once_and_names_its_real_verb(tmp_path: Path, monkeypatch) -> None:
    from matrx_scraper.cloud_browser.worker import machine_git_safety as mgs

    real = mgs._git
    calls: list[str] = []

    async def flaky(repo, *args, env, check=True, timeout_factor=1.0):
        if "add" in args:
            calls.append("add")
            if len(calls) == 1:
                verb = next(a for a in args if not a.startswith("-"))
                raise mgs.GitFailed(f"git {verb} timed out after 60s")
        return await real(repo, *args, env=env, check=check, timeout_factor=timeout_factor)

    monkeypatch.setattr(mgs, "_git", flaky)
    repo = tmp_path / "r"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    out = asyncio.run(mgs.save_repo(repo, branch_prefix="safety/x", env=mgs.git_env({"PATH": "/usr/bin:/bin"}),
                                    now=datetime.now(UTC)))
    assert calls == ["add", "add"]
    assert out is None  # clean empty repo: nothing unsaved, and no timeout surfaced


def test_a_slow_cold_walk_gets_more_than_the_per_step_knob(tmp_path: Path) -> None:
    """A huge checkout's walk can outlast the 60 s step knob (aidream, 2026-11-16): the walk gets
    a multiple of it, while every other step keeps the knob."""
    from matrx_scraper.cloud_browser.worker import machine_git_safety as mgs

    fake = tmp_path / "bin"
    fake.mkdir()
    (fake / "git").write_text(
        '#!/bin/sh\ncase "$*" in *add*) sleep 2; exit 0;; *rev-parse*) echo; exit 0;; esac\nsleep 2\n'
    )
    (fake / "git").chmod(0o755)
    env = {"PATH": f"{fake}:/usr/bin:/bin", "MATRX_SAFETY_GIT_TIMEOUT": "1"}
    repo = tmp_path / "r"
    repo.mkdir()

    async def run() -> None:
        with pytest.raises(mgs.GitFailed, match="timed out after 1s"):
            await mgs._git(repo, "remote", env=env)
        code, _ = await mgs._git(repo, "add", "-A", env=env, timeout_factor=mgs.STATUS_TIMEOUT_FACTOR)
        assert code == 0

    asyncio.run(run())
    src = Path(mgs.__file__).read_text()
    assert '"add", "-A", env=snap_env, timeout_factor=STATUS_TIMEOUT_FACTOR' in src


# --- 2026-11-20: ``cloud_computer_save_incomplete`` "safety_branches after 240s" (7 rows, one machine
# whose home holds a 125k-file aidream clone on the network home). A save walked that checkout up to
# THREE times (status, a cold status retry, ``add -A``) from a fresh throwaway index every stop, and the
# worker had no deadline: the 240 s stop budget cut the call and every result was lost.


def _walks(monkeypatch) -> list[str]:
    from matrx_scraper.cloud_browser.worker import machine_git_safety as mgs

    real = mgs._git
    seen: list[str] = []

    async def counting(repo, *args, env, check=True, timeout_factor=1.0):
        if "status" in args or "add" in args:
            seen.append("status" if "status" in args else "add")
        return await real(repo, *args, env=env, check=check, timeout_factor=timeout_factor)

    monkeypatch.setattr(mgs, "_git", counting)
    return seen


def test_a_save_walks_the_checkout_once(tmp_path: Path, monkeypatch) -> None:
    home, remotes = tmp_path / "home", tmp_path / "remotes"
    work, bare = repo_with_remote(home, "app", remotes)
    (work / "README.md").write_text("edited\n")
    (work / "new.py").write_text("x = 1\n")
    seen = _walks(monkeypatch)
    [repo] = save(home)["safety_branches"]
    assert repo["pushed"] is True
    assert sorted(git(bare, "ls-tree", "-r", "--name-only", repo["branch"]).split()) == ["README.md", "new.py"]
    assert seen == ["add"]  # one whole-tree walk, never status + add


def test_a_clean_repo_is_still_one_walk_and_not_listed(tmp_path: Path, monkeypatch) -> None:
    home, remotes = tmp_path / "home", tmp_path / "remotes"
    repo_with_remote(home, "clean", remotes)
    seen = _walks(monkeypatch)
    answer = save(home)
    assert answer["safety_branches"] == [] and seen == ["add"]


def test_the_snapshot_index_is_kept_so_the_next_save_is_incremental(tmp_path: Path) -> None:
    """The kept index (stat cache + untracked cache) lives under the home's ``.matrx`` and the next save
    reuses it; the person's own index is never written; a deleted file leaves the next snapshot."""
    home, remotes = tmp_path / "home", tmp_path / "remotes"
    work, bare = repo_with_remote(home, "app", remotes)
    own = work / ".git" / "index"
    (work / "a.txt").write_text("one\n")
    first = save(home)["safety_branches"][0]
    [kept] = list((home / ".matrx" / "git-safety").glob("*.index"))
    assert b"UNTR" in kept.read_bytes()  # untracked cache on: unchanged folders are not re-read next time
    own_before = own.read_bytes()
    (work / "a.txt").unlink()
    (work / "b.txt").write_text("two\n")
    second = save(home, NOW.replace(hour=21))["safety_branches"][0]
    assert first["pushed"] and second["pushed"]
    assert git(bare, "ls-tree", "-r", "--name-only", second["branch"]).split() == ["README.md", "b.txt"]
    assert own.read_bytes() == own_before


def test_the_answer_comes_back_inside_the_deadline_naming_what_was_not_finished(tmp_path: Path) -> None:
    """A walk slower than what is left of the stop budget: the worker answers in time, saying the
    budget was reached, instead of the caller cutting the call and losing every result."""
    import os
    import time

    home = tmp_path / "home"
    (home / "repos" / "big" / ".git").mkdir(parents=True)
    fake = tmp_path / "bin"
    fake.mkdir()
    (fake / "git").write_text('#!/bin/sh\ncase "$*" in *add*) sleep 30;; esac\necho\nexit 0\n')
    (fake / "git").chmod(0o755)
    env = {**os.environ, "PATH": f"{fake}:/usr/bin:/bin"}
    started = time.monotonic()
    answer = asyncio.run(push_safety_branches(home, machine_id="m", base_env=env, git_timeout_seconds=60,
                                              token_file="/nonexistent", now=NOW, deadline_seconds=6))
    assert time.monotonic() - started < 6
    [repo] = answer["safety_branches"]
    assert repo["pushed"] is False and "save budget reached" in repo["reason"]


def test_repositories_are_saved_together_not_one_after_another(tmp_path: Path) -> None:
    """Four repositories whose walk takes ~2 s each finish in about one walk's time, not four: a machine with
    many repositories must fit the stop's one save budget (fails when the loop is sequential)."""
    import os
    import time

    home = tmp_path / "home"
    for n in range(4):
        (home / "repos" / f"r{n}" / ".git").mkdir(parents=True)
    fake = tmp_path / "bin"
    fake.mkdir()
    (fake / "git").write_text('#!/bin/sh\ncase "$*" in *add*) sleep 2;; esac\necho\nexit 0\n')
    (fake / "git").chmod(0o755)
    env = {**os.environ, "PATH": f"{fake}:/usr/bin:/bin"}
    started = time.monotonic()
    asyncio.run(push_safety_branches(home, machine_id="m", base_env=env, git_timeout_seconds=60,
                                     token_file="/nonexistent", now=NOW))
    assert time.monotonic() - started < 6.5


# --- 2026-11-21: five ``cloud_computer_save_incomplete`` rows of one machine, "the save budget ran out before
# every repository finished", each with no repository named and no timings. The answer now says how long the home
# walk and every repository took, the home walk is bounded by the deadline, and a lock a killed walk left beside
# the kept snapshot index never refuses the next save.


def test_the_answer_names_each_repositorys_seconds_and_the_home_walk(tmp_path: Path) -> None:
    home, remotes = tmp_path / "home", tmp_path / "remotes"
    work, _bare = repo_with_remote(home, "app", remotes)
    repo_with_remote(home, "clean", remotes)
    (work / "README.md").write_text("edited\n")
    answer = save(home)
    assert isinstance(answer["find_seconds"], float) and isinstance(answer["elapsed_seconds"], float)
    outcomes = {t["repo"]: t["outcome"] for t in answer["timings"]}
    assert outcomes == {"repos/app": "pushed", "repos/clean": "clean"}
    assert all(isinstance(t["seconds"], float) and isinstance(t["waited_seconds"], float) for t in answer["timings"])


def test_a_home_walk_slower_than_the_deadline_still_answers_in_time(tmp_path: Path, monkeypatch) -> None:
    import time

    from matrx_scraper.cloud_browser.worker import machine_git_safety as mgs

    monkeypatch.setattr(mgs, "find_repos", lambda home: time.sleep(8) or [])
    async def run() -> tuple[dict, float]:
        # Timed inside the loop: the worker's loop answers the request; only asyncio.run's own exit waits for the
        # abandoned walk thread.
        started = time.monotonic()
        out = await push_safety_branches(tmp_path, machine_id="m", base_env={"PATH": "/usr/bin:/bin"},
                                         git_timeout_seconds=60, token_file="/nonexistent", now=NOW,
                                         deadline_seconds=5)
        return out, time.monotonic() - started

    answer, took = asyncio.run(run())
    assert took < 5
    assert answer["unfinished"] == "finding repositories" and answer["safety_branches"] == []


def test_a_lock_left_beside_the_kept_index_never_refuses_the_next_save(tmp_path: Path) -> None:
    home, remotes = tmp_path / "home", tmp_path / "remotes"
    work, _bare = repo_with_remote(home, "app", remotes)
    (work / "a.txt").write_text("one\n")
    assert save(home)["safety_branches"][0]["pushed"] is True
    [kept] = list((home / ".matrx" / "git-safety").glob("*.index"))
    kept.with_name(kept.name + ".lock").write_text("")  # what a walk killed at the deadline leaves
    (work / "b.txt").write_text("two\n")
    [repo] = save(home, NOW.replace(hour=21))["safety_branches"]
    assert repo["pushed"] is True, repo["reason"]
