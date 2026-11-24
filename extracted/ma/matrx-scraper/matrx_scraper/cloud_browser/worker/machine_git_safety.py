"""Ruling 19 safety branch: before a Cloud Computer stops, unsaved git work leaves the machine.

Every repository under the home with uncommitted changes (tracked or untracked, minus what
``.gitignore`` excludes) or commits no remote has is pushed to ``safety/<machine-id>-<date>``
on its own remote, with the owner's GitHub credential already delivered to the machine (the
tmpfs token file the daemon's git credential helper reads, ``machine_agent.GIT_TOKEN_FILE``).

Nothing the person sees changes: the snapshot commit is built in its OWN index (``GIT_INDEX_FILE``),
first seeded from a COPY of the person's so a huge checkout on the network home is not re-hashed, then
KEPT under ``~/.matrx/git-safety`` with the untracked cache on, so each later save re-reads only what
changed. One ``add -A`` is the save's only whole-tree walk (dirty = its tree differs from HEAD's); their
working tree, index, branches and stash are never touched. A ``deadline_seconds`` from the caller bounds
every step, and the answer names whatever the deadline stopped (2026-11-20). The push skips the repository's own hooks (``--no-verify``: a failing pre-push hook must not
keep unsaved work on a machine about to stop). Each repository gets its own branch name
(``safety/<machine-id>-<date>-<repo>``), so several clones of one remote never collide; a
same-day branch that already exists is never overwritten: the push falls to a time-stamped
name. An SSH remote is answered at once ("not pushed: ssh remote") — the machine pushes over
HTTPS with the owner's GitHub connection, and an SSH push would only wait for the timeout. Every repository with work is answered — ``pushed: true`` with the branch, or
``pushed: false`` with the reason — so the stop can say exactly what was saved.
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import re
import shutil
import tempfile
import time
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .machine_agent import GIT_CREDENTIAL_HELPER, GIT_TOKEN_FILE

logger = logging.getLogger(__name__)

#: Folders never searched for repositories (our own state, caches, the synced Cloud folder).
SKIP_DIRS = frozenset({"Cloud", "node_modules", ".cache", ".npm", ".matrx", ".local", ".venv", "venv",
                       "__pycache__", "profiles", "snap"})
#: How deep under the home a repository may sit (``~/repos/org/name`` is depth 3).
MAX_DEPTH = 4


def find_repos(home: Path, *, max_depth: int = MAX_DEPTH) -> list[Path]:
    """Work trees under ``home`` (a ``.git`` inside), never descending into one or a skipped folder."""
    found: list[Path] = []

    def walk(folder: Path, depth: int) -> None:
        try:
            children = sorted(folder.iterdir())
        except OSError:
            return
        if (folder / ".git").exists():
            found.append(folder)
            return
        if depth >= max_depth:
            return
        for child in children:
            if child.is_dir() and not child.is_symlink() and child.name not in SKIP_DIRS \
                    and not (child.name.startswith(".") and child.name != ".config"):
                walk(child, depth + 1)

    walk(home, 0)
    return found


class GitFailed(RuntimeError):
    pass


def git_env(base_env: Mapping[str, str], token_file: str = GIT_TOKEN_FILE) -> dict[str, str]:
    """The machine's git environment (``base_env`` = the agent daemon's): the owner's GitHub
    token through the env-only helper."""
    env = dict(base_env)
    env.update(
        MATRX_GIT_TOKEN_FILE=token_file,
        GIT_TERMINAL_PROMPT="0",
        # Never write the person's index from a read (``git status`` refreshes it otherwise).
        GIT_OPTIONAL_LOCKS="0",
        GIT_CONFIG_COUNT="2",
        GIT_CONFIG_KEY_0="credential.https://github.com.helper",
        GIT_CONFIG_VALUE_0=GIT_CREDENTIAL_HELPER,
        # The worker and the agent share the home but a repo cloned by root (sudo) must still answer.
        GIT_CONFIG_KEY_1="safe.directory",
        GIT_CONFIG_VALUE_1="*",
        GIT_AUTHOR_NAME="Matrx Cloud Computer",
        GIT_AUTHOR_EMAIL="cloud-computer@aimatrx.com",
        GIT_COMMITTER_NAME="Matrx Cloud Computer",
        GIT_COMMITTER_EMAIL="cloud-computer@aimatrx.com",
    )
    return env


#: The whole-tree walk (``add -A`` into the snapshot index) reads every file of a checkout (a huge repo on
#: the network home is the one step that outlasts the knob: aidream 2026-11-16, "git status timed out after
#: 60s"), so it gets this many times the per-step knob; every other step keeps the knob as is.
STATUS_TIMEOUT_FACTOR = 3.0
#: ``git hash-object -t tree /dev/null``: the tree of a repository with nothing in it.
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
#: Where each repository's snapshot index lives between stops (under the home, never searched for repos).
#: Kept, so the next save's walk is incremental: its stat cache and untracked cache (``core.untrackedCache``)
#: mean only what changed since the last save is re-read, never the whole checkout again.
INDEX_DIR = Path(".matrx") / "git-safety"
#: Seconds kept back from the caller's deadline for the answer to travel back.
DEADLINE_MARGIN_SECONDS = 3.0
#: Repositories saved at the same time on one machine.
SAVE_CONCURRENCY = 4


class SaveBudgetReached(GitFailed):
    """The caller's deadline is too close to start (or finish) a git step: what is done is answered."""


async def _git(
    repo: Path, *args: str, env: dict[str, str], check: bool = True, timeout_factor: float = 1.0,
) -> tuple[int, str]:
    verb = next((a for a in args if not a.startswith("-")), args[0])
    timeout = float(env.get("MATRX_SAFETY_GIT_TIMEOUT", "0") or 0) or None
    if timeout is not None:
        timeout *= timeout_factor
    deadline = float(env.get("MATRX_SAFETY_DEADLINE", "0") or 0) or None
    cut_by_deadline = False
    if deadline is not None:
        left = deadline - time.monotonic()
        if left <= 1.0:
            raise SaveBudgetReached(f"save budget reached before git {verb}")
        if timeout is None or left < timeout:
            timeout, cut_by_deadline = left, True
    proc = await asyncio.create_subprocess_exec(
        "git", "-C", str(repo), *args, env=env,
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT,
    )
    try:
        out, _ = await asyncio.wait_for(proc.communicate(), timeout=timeout)
    except TimeoutError:
        proc.kill()
        if cut_by_deadline:
            raise SaveBudgetReached(f"save budget reached during git {verb}") from None
        raise GitFailed(f"git {verb} timed out after {timeout:.0f}s") from None
    text = out.decode(errors="replace").strip()
    if check and proc.returncode != 0:
        raise GitFailed(f"git {args[0]}: {text.splitlines()[-1] if text else proc.returncode}")
    return proc.returncode or 0, text


def _reason(text: str) -> str:
    low = text.lower()
    if "authentication failed" in low or "could not read username" in low or "403" in low:
        return "GitHub refused the push (no GitHub connection, or it cannot write to this repository)"
    if "could not resolve host" in low or "unable to access" in low:
        return "the remote could not be reached"
    return text[:300]


#: ``git@host:path``, ``ssh://…``, ``user@host:path`` — a remote the machine cannot push to.
_SSH_REMOTE = re.compile(r"^(ssh://|git\+ssh://|ssh\+git://|[\w.-]+@[\w.-]+:)")


def is_ssh_remote(url: str) -> bool:
    return bool(_SSH_REMOTE.match(url.strip()))


def repo_slug(repo: Path, home: Path | None = None) -> str:
    """A short, stable name part for one repository: its folder name and a hash of its path
    under the home (three clones of one remote get three branches)."""
    try:
        rel = str(repo.relative_to(home)) if home is not None else str(repo)
    except ValueError:
        rel = str(repo)
    name = "".join(c if c.isalnum() or c in "-_" else "-" for c in repo.name)[:24].strip("-") or "repo"
    return f"{name}-{hashlib.sha1(rel.encode()).hexdigest()[:6]}"


def _snapshot_env(env: dict[str, str], index: Path) -> dict[str, str]:
    """``env`` writing to the snapshot index, with the untracked cache on (kept in that index only)."""
    count = int(env.get("GIT_CONFIG_COUNT", "0") or 0)
    return {**env, "GIT_INDEX_FILE": str(index), "GIT_CONFIG_COUNT": str(count + 1),
            f"GIT_CONFIG_KEY_{count}": "core.untrackedCache", f"GIT_CONFIG_VALUE_{count}": "true"}


async def _seed_index(repo: Path, index: Path, head: str, env: dict[str, str]) -> None:
    """A fresh snapshot index: a COPY of the person's (stat cache included, so ``add -A`` hashes only
    what changed and their own index file is never written), else HEAD's tree."""
    _, own_index = await _git(repo, "rev-parse", "--git-path", "index", env=env, check=False)
    own = Path(own_index) if own_index else None
    if own is not None and not own.is_absolute():
        own = repo / own
    await asyncio.to_thread(index.unlink, missing_ok=True)
    if own is not None and own.is_file():
        await asyncio.to_thread(shutil.copyfile, own, index)
    elif head:
        await _git(repo, "read-tree", head, env=_snapshot_env(env, index))


async def _snapshot_tree(repo: Path, index: Path, head: str, env: dict[str, str]) -> str:
    """The working tree as git would commit it (``add -A``: tracked and untracked, minus ignored) —
    the ONE whole-tree walk of a save. ``index`` is kept between saves (incremental); a missing or
    unreadable one is re-seeded. A cold walk that times out is retried once (the killed walk warmed the
    file cache; aidream: three live saves lost, 2026-11-15)."""
    snap_env = _snapshot_env(env, index)
    # The index is private to this save (no other git ever writes it), so a lock beside it is always stale: a
    # walk killed at the save budget leaves it, and every later save's ``add -A`` would refuse ("File exists").
    await asyncio.to_thread(index.with_name(index.name + ".lock").unlink, missing_ok=True)
    if not await asyncio.to_thread(index.is_file):
        await _seed_index(repo, index, head, env)
    for attempt in (1, 2):
        try:
            await _git(repo, "add", "-A", env=snap_env, timeout_factor=STATUS_TIMEOUT_FACTOR)
            break
        except SaveBudgetReached:
            raise
        except GitFailed as exc:
            if attempt == 2:
                raise
            if "timed out" in str(exc):
                logger.warning("safety branches: git add timed out in %s, retrying once warm", repo)
            else:  # an unreadable kept index: start again from the person's
                await _seed_index(repo, index, head, env)
    _, tree = await _git(repo, "write-tree", env=snap_env)
    return tree


async def save_repo(
    repo: Path, *, branch_prefix: str, env: dict[str, str], now: datetime, slug: str | None = None,
    index_file: Path | None = None,
) -> dict[str, Any] | None:
    """Push ``repo``'s unsaved work to a safety branch. None = nothing unsaved (not listed).

    ``index_file``: where this repository's snapshot index is kept between saves (None = a throwaway)."""
    name = str(repo)
    try:
        _, head = await _git(repo, "rev-parse", "--verify", "-q", "HEAD", env=env, check=False)
        head = head if len(head) == 40 else ""
        if index_file is not None:
            index_file.parent.mkdir(parents=True, exist_ok=True)
            tree = await _snapshot_tree(repo, index_file, head, env)
        else:
            with tempfile.TemporaryDirectory() as tmp:
                tree = await _snapshot_tree(repo, Path(tmp) / "index", head, env)
        head_tree = ""
        if head:
            _, head_tree = await _git(repo, "rev-parse", f"{head}^{{tree}}", env=env)
        dirty = tree != (head_tree or EMPTY_TREE)
        unpushed = ""
        if head:
            _, unpushed = await _git(repo, "rev-list", "--max-count=1", "HEAD", "--not", "--remotes", env=env)
        if not dirty and not unpushed:
            return None
        _, remotes = await _git(repo, "remote", env=env)
        remote = "origin" if "origin" in remotes.split() else (remotes.split() or [None])[0]
        if remote is None:
            return {"repo": name, "branch": None, "pushed": False,
                    "reason": "no remote to push to (the work stays on the machine's home)"}
        _, url = await _git(repo, "remote", "get-url", "--push", remote, env=env, check=False)
        if is_ssh_remote(url):
            return {"repo": name, "branch": None, "pushed": False,
                    "reason": "not pushed: ssh remote (the machine pushes over HTTPS with your GitHub "
                              "connection; the work stays on the machine's home)"}
        commit = head
        if dirty:
            parents = ["-p", head] if head else []
            _, commit = await _git(
                repo, "commit-tree", tree, *parents,
                "-m", f"Safety snapshot before the Cloud Computer stopped ({now.isoformat()})",
                env=env,
            )
        tail = f"-{slug}" if slug else ""
        branch = f"{branch_prefix}-{now.strftime('%Y%m%d')}{tail}"
        push = ("push", "--no-verify", remote)
        code, text = await _git(repo, *push, f"{commit}:refs/heads/{branch}", env=env, check=False)
        if code != 0 and ("rejected" in text or "non-fast-forward" in text or "fetch first" in text):
            branch = f"{branch_prefix}-{now.strftime('%Y%m%d-%H%M%S')}{tail}"
            code, text = await _git(repo, *push, f"{commit}:refs/heads/{branch}", env=env, check=False)
        if code != 0:
            return {"repo": name, "branch": branch, "pushed": False, "reason": _reason(text)}
        return {"repo": name, "branch": branch, "pushed": True, "reason": None, "commit": commit,
                "uncommitted": bool(dirty), "unpushed_commits": bool(unpushed)}
    except GitFailed as exc:
        return {"repo": name, "branch": None, "pushed": False, "reason": str(exc)[:300]}
    except OSError as exc:
        return {"repo": name, "branch": None, "pushed": False, "reason": f"git could not run: {exc}"}


async def push_safety_branches(
    home: Path, *, machine_id: str, base_env: Mapping[str, str], git_timeout_seconds: float,
    token_file: str = GIT_TOKEN_FILE, now: datetime | None = None, deadline_seconds: float | None = None,
) -> dict[str, Any]:
    """Every repository under ``home`` with unsaved work → its safety branch. Never raises.
    ``git_timeout_seconds`` bounds each git command (AI Dream sends its knob); a hung remote
    never holds a stop. ``deadline_seconds`` (AI Dream sends what is left of the stop's save budget):
    no git step outlives it, and the answer still comes back in time naming every repository it
    could not finish ("save budget reached"), so what WAS pushed is never lost with the call."""
    now = now or datetime.now(UTC)
    safe_id = "".join(c for c in machine_id if c.isalnum() or c in "-_")[:40] or "machine"
    env = git_env(base_env, token_file)
    env["MATRX_SAFETY_GIT_TIMEOUT"] = str(max(1.0, float(git_timeout_seconds)))
    if deadline_seconds is not None:
        env["MATRX_SAFETY_DEADLINE"] = str(time.monotonic() + max(1.0, float(deadline_seconds) - DEADLINE_MARGIN_SECONDS))
    started = time.monotonic()
    deadline = float(env.get("MATRX_SAFETY_DEADLINE", "0") or 0) or None
    try:
        # The home walk is bounded by the deadline too: on a slow network home it is the one step no git
        # timeout covers, and an answer that never comes loses every result with the call.
        repos = await asyncio.wait_for(
            asyncio.to_thread(find_repos, Path(home)),
            timeout=None if deadline is None else max(0.5, deadline - time.monotonic()),
        )
    except TimeoutError:
        return {"repos_checked": 0, "safety_branches": [], "unfinished": "finding repositories",
                "find_seconds": round(time.monotonic() - started, 1), "timings": [],
                "elapsed_seconds": round(time.monotonic() - started, 1)}
    find_seconds = round(time.monotonic() - started, 1)
    #: Per repository: seconds queued behind the others, seconds saving, and the outcome. The answer carries it so
    #: a save that runs out of budget names which repository took the time (2026-11-21: five rows that could not).
    timings: list[dict[str, Any]] = []
    # Repositories are independent (own index file, own remote): saved a few at a time, never one after another,
    # so a machine with many repositories fits the stop's one save budget (2026-11-20: four rows "the save budget
    # ran out before every repository finished").
    gate = asyncio.Semaphore(SAVE_CONCURRENCY)

    async def one(repo: Path) -> dict[str, Any] | None:
        slug = repo_slug(repo, Path(home))
        try:
            rel = str(repo.relative_to(home))
        except ValueError:
            rel = str(repo)
        queued = time.monotonic()
        async with gate:
            began = time.monotonic()
            result = await save_repo(repo, branch_prefix=f"safety/{safe_id}", env=env, now=now, slug=slug,
                                     index_file=Path(home) / INDEX_DIR / f"{slug}.index")
        timings.append({
            "repo": rel, "waited_seconds": round(began - queued, 1), "seconds": round(time.monotonic() - began, 1),
            "outcome": "clean" if result is None else ("pushed" if result["pushed"] else str(result["reason"])[:120]),
        })
        if result is not None:
            result["repo"] = rel
        return result

    results = [r for r in await asyncio.gather(*(one(repo) for repo in repos)) if r is not None]
    if any(not r["pushed"] for r in results):
        logger.error("safety branches: %s", [(r["repo"], r["reason"]) for r in results if not r["pushed"]])
    return {"repos_checked": len(repos), "safety_branches": results, "find_seconds": find_seconds,
            "timings": timings, "elapsed_seconds": round(time.monotonic() - started, 1)}
