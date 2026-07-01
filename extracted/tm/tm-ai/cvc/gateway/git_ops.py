"""
Git router — CVC's git operations for the dashboard.

Implements the full GitStatusInfo / GitBranchesResponse / GitCheckoutResponse
/ GitSyncResult contracts that the React dashboard (GitBranchChip.tsx) expects.
The shapes are defined in cvc/web/src/lib/types.ts.

All routes are scoped to the active workspace (the legacy
`_workspace_mgr.current.path`). If no workspace is active, return
`is_repo: false` / empty `branches` rather than 500-ing.
"""

from __future__ import annotations

import json
import logging
import os
import re
import subprocess
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger("cvc.gateway.git_ops")

router = APIRouter()


# ---------------------------------------------------------------------------
# Workspace resolution
# ---------------------------------------------------------------------------

async def _workspace_path(explicit: str | None = None) -> Path | None:
    """Return the active workspace's filesystem path, or None.

    Priority:
    0. ``explicit`` — a path passed by the caller (query param from the
       frontend).  Always wins when provided and valid — this eliminates
       all race conditions during page refresh where the server-side
       pointer hasn't caught up with the client-side state.
    1. ``host_state.db`` — the durable SQLite KV store that
       WorkspaceManager writes to on every switch.
    2. ``~/.cvc/active_workspace`` — legacy sidecar (backup).
    3. ``_workspace_mgr.current.path`` — in-memory (authoritative when
       it agrees with the disk-side source).
    4. First workspace in ``workspaces.json`` (bare fallback).
    """
    # ── 0. Explicit path from the frontend ──────────────────────────
    if explicit:
        p = Path(explicit).expanduser()
        if p.exists():
            return p
        logger.debug("explicit workspace_path %s does not exist", explicit)

    # ── 1. host_state.db — durable SQLite KV ────────────────────────
    try:
        from cvc.host_state import load_active_workspace as _load_ws
        wsp = _load_ws()
        if wsp:
            p = Path(wsp)
            if p.exists():
                return p
    except Exception:
        pass

    # ── 2. Legacy sidecar file ──────────────────────────────────────
    active_file_path: Path | None = None
    try:
        active = Path(os.path.expanduser("~/.cvc/active_workspace"))
        if active.exists():
            wid = active.read_text(encoding="utf-8").strip()
            if wid:
                p = Path(wid)
                if p.exists():
                    active_file_path = p
                else:
                    # Treat as a workspace_id — look it up in workspaces.json
                    try:
                        ws_file = Path(os.path.expanduser("~/.cvc/workspaces.json"))
                        if ws_file.exists():
                            data = json.loads(ws_file.read_text(encoding="utf-8"))
                            items = data if isinstance(data, list) else data.get("workspaces", [])
                            for ws in items:
                                if (ws.get("id") == wid or ws.get("workspace_id") == wid
                                        or ws.get("name") == wid):
                                    pp = ws.get("path")
                                    if pp and Path(pp).exists():
                                        active_file_path = Path(pp)
                                        break
                    except Exception:
                        pass
    except Exception:
        pass

    # ── 3. In-memory WorkspaceManager ───────────────────────────────
    try:
        import cvc.gateway as gw
        mgr = getattr(gw, "_workspace_mgr", None)
        if mgr is not None and getattr(mgr, "current", None):
            cur = mgr.current
            if isinstance(cur, dict):
                path = cur.get("path")
            else:
                path = getattr(cur, "path", None)
            if path and Path(path).exists():
                if active_file_path is None or Path(path) == active_file_path:
                    return Path(path)
    except Exception:
        pass

    # ── 4. Sidecar fallback ─────────────────────────────────────────
    if active_file_path is not None:
        return active_file_path

    # ── 5. First workspace in workspaces.json ───────────────────────
    try:
        ws_file = Path(os.path.expanduser("~/.cvc/workspaces.json"))
        if ws_file.exists():
            data = json.loads(ws_file.read_text(encoding="utf-8"))
            items = data if isinstance(data, list) else data.get("workspaces", [])
            if items:
                p = items[0].get("path")
                if p and Path(p).exists():
                    return Path(p)
    except Exception:
        pass

    return None


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def _get_github_token() -> str | None:
    """Read a GitHub token from ~/.cvc/config.yaml (api_keys.github).

    Used as a credential for HTTPS git operations against github.com when
    the user's gitconfig credential helper isn't configured (or has a
    stale token). Returns None if no token is configured.
    """
    import re as _re

    for cfg_path in (
        Path(os.path.expanduser("~/.cvc/config.yaml")),
        Path(os.path.expanduser("~/.cvc/config.json")),
    ):
        try:
            if not cfg_path.exists():
                continue
            text = cfg_path.read_text(encoding="utf-8")
            # YAML: `api_keys:\n  github: ghu_...` — indented under api_keys
            m = _re.search(
                r"^\s*github:\s*['\"]?(gh[prsu]_[A-Za-z0-9_]+)",
                text,
                _re.MULTILINE,
            )
            if m:
                return m.group(1)
            # Fallback: any `github: <token>` in the file
            m = _re.search(
                r"github:\s*['\"]?(gh[prsu]_[A-Za-z0-9_]+)",
                text,
            )
            if m:
                return m.group(1)
            # JSON
            import json as _json
            try:
                data = _json.loads(text)
            except Exception:
                continue
            if isinstance(data, dict):
                ak = data.get("api_keys") or {}
                tok = ak.get("github") if isinstance(ak, dict) else None
                if not tok:
                    tok = data.get("github_token") or data.get("github")
                if isinstance(tok, str) and tok.startswith(("gh", "gho", "ghu", "ghs", "ghr")):
                    return tok
        except Exception:
            continue
    return None


def _is_credential_error(stderr: str) -> bool:
    """Return True if the git error message looks like an auth/credential failure."""
    s = (stderr or "").lower()
    return any(
        marker in s
        for marker in (
            "could not read password",
            "could not read username",
            "authentication failed",
            "403 forbidden",
            "401 unauthorized",
            "terminal prompts disabled",
            "no interactive",
            "support for password",
        )
    )


def _run_git(args: list[str], cwd: Path, timeout: int = 15) -> subprocess.CompletedProcess:
    """Run a git command in cwd, raising HTTPException(500) on failure."""
    try:
        return subprocess.run(
            ["git", *args],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=500, detail=f"git {' '.join(args)} timed out")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="git binary not found on PATH")


def _run_git_with_credential_fallback(
    args: list[str], cwd: Path, timeout: int = 30
) -> tuple[subprocess.CompletedProcess, str | None]:
    """Run a git command, retrying with a GitHub token credential if the
    first attempt fails with an auth/credential error.

    Returns (final_completed_process, token_used_or_None).
    """
    proc = _run_git(args, cwd, timeout=timeout)
    if proc.returncode == 0:
        return proc, None

    # Try SSH fallback for github.com remotes — git will switch to the
    # SSH URL on retry because the HTTPS fetch failed.
    if not _is_credential_error(proc.stderr or proc.stdout):
        return proc, None

    token = _get_github_token()
    if not token:
        return proc, None

    # Rewrite all remotes to HTTPS-with-token for the duration of this call.
    # We use a temporary GIT_ASKPASS-style credential helper instead of
    # rewriting .git/config, which is permanent and racy.
    # `git -c credential.helper=...` accepts an inline helper.
    helper_cmd = f"!f() {{ echo username=x-access-token; echo password={token}; }}; f"
    try:
        proc2 = subprocess.run(
            ["git", "-c", f"credential.helper={helper_cmd}", *args],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if proc2.returncode == 0:
            return proc2, token
        # Still failed — return the second attempt so caller can see why
        return proc2, token
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return proc, token


def _is_git_repo(p: Path) -> bool:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=str(p), capture_output=True, text=True, timeout=5,
        )
        return r.returncode == 0 and r.stdout.strip() == "true"
    except Exception:
        return False


def _current_branch(cwd: Path) -> tuple[str, str, bool]:
    """Return (branch_name_or_HEAD, head_sha, detached)."""
    name_proc = _run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd)
    branch = name_proc.stdout.strip() or "HEAD"
    detached = branch == "HEAD"
    sha_proc = _run_git(["rev-parse", "HEAD"], cwd)
    head = sha_proc.stdout.strip()[:12]
    return branch, head, detached


def _dirty_count(cwd: Path) -> int:
    """Count modified/untracked files in cwd."""
    p = _run_git(["status", "--porcelain"], cwd)
    return sum(1 for line in p.stdout.splitlines() if line.strip())


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.get("/status")
async def git_status(workspace_path: str | None = None) -> dict[str, Any]:
    """Return the dashboard's GitStatusInfo contract."""
    ws = await _workspace_path(workspace_path)
    if ws is None:
        return {"is_repo": False, "path": None}
    if not _is_git_repo(ws):
        return {"is_repo": False, "path": str(ws)}

    try:
        branch, head, detached = _current_branch(ws)
        dirty = _dirty_count(ws)
        return {
            "is_repo": True,
            "path": str(ws),
            "branch": branch,
            "head": head,
            "detached": detached,
            "dirty": dirty > 0,
            "dirty_count": dirty,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("git_status failed for %s", ws)
        raise HTTPException(status_code=500, detail=f"git status failed: {e}")


@router.get("/branches")
async def git_branches(fetch: bool = True, workspace_path: str | None = None) -> dict[str, Any]:
    """Return the dashboard's GitBranchesResponse contract.

    `fetch=True` runs `git fetch` first (slow on cold cache) to populate
    remote refs. `fetch=False` uses the local refs only — faster.
    """
    ws = await _workspace_path(workspace_path)
    if ws is None or not _is_git_repo(ws):
        return {
            "branches": [], "local": [], "remote": [],
            "current": "", "detached": False, "count": 0,
            "remote_count": 0, "fetched": False, "fetch_error": None,
        }

    fetch_error: str | None = None
    fetched = False
    if fetch:
        proc, _token_used = _run_git_with_credential_fallback(
            ["fetch", "--all", "--prune"], ws, timeout=30
        )
        fetched = proc.returncode == 0
        if not fetched:
            fetch_error = (proc.stderr or proc.stdout).strip()[:500]

    # Get current branch
    try:
        branch, _head, detached = _current_branch(ws)
    except Exception:
        branch, detached = "HEAD", True

    # Local branches
    local_entries: list[dict[str, Any]] = []
    try:
        r = _run_git(
            ["for-each-ref", "--format=%(refname:short)|%(objectname:short)|%(committerdate:iso8601)|%(subject)|%(upstream:short)|%(upstream:track)",
             "refs/heads/"],
            ws,
        )
        for line in r.stdout.splitlines():
            if not line.strip():
                continue
            parts = line.split("|", 5)
            if len(parts) < 5:
                continue
            name, sha, date, subject, upstream = parts[:5]
            track = parts[5] if len(parts) > 5 else ""
            ahead = behind = 0
            gone = False
            if upstream:
                m = re.search(r"ahead (\d+)", track)
                if m:
                    ahead = int(m.group(1))
                m = re.search(r"behind (\d+)", track)
                if m:
                    behind = int(m.group(1))
                if "gone" in track:
                    gone = True
            local_entries.append({
                "name": name,
                "head": sha,
                "last_commit_at": date,
                "last_commit_subject": subject,
                "is_current": name == branch,
                "kind": "local",
                "upstream": upstream or None,
                "ahead": ahead,
                "behind": behind,
                "gone": gone,
            })
    except Exception as e:
        logger.exception("listing local branches: %s", e)

    # Remote branches
    remote_entries: list[dict[str, Any]] = []
    try:
        r = _run_git(
            ["for-each-ref", "--format=%(refname:short)|%(objectname:short)|%(committerdate:iso8601)|%(subject)",
             "refs/remotes/"],
            ws,
        )
        local_names = {e["name"] for e in local_entries}
        for line in r.stdout.splitlines():
            if not line.strip():
                continue
            parts = line.split("|", 3)
            if len(parts) < 4:
                continue
            name, sha, date, subject = parts
            # Skip HEAD pointer refs like "origin/HEAD"
            if name.endswith("/HEAD"):
                continue
            remote = name.split("/", 1)[0] if "/" in name else ""
            short = name.split("/", 1)[1] if "/" in name else name
            has_local = short in local_names
            tracked_by_local = any(
                e.get("upstream") and e["upstream"].split("/", 1)[-1] == name
                for e in local_entries
            )
            remote_entries.append({
                "name": name,
                "head": sha,
                "last_commit_at": date,
                "last_commit_subject": subject,
                "is_current": False,
                "kind": "remote",
                "short_name": short,
                "remote": remote,
                "has_local": has_local,
                "tracked_by_local": tracked_by_local,
            })
    except Exception as e:
        logger.exception("listing remote branches: %s", e)

    all_branches = local_entries + remote_entries
    return {
        "branches": all_branches,  # back-compat
        "local": local_entries,
        "remote": remote_entries,
        "current": branch,
        "detached": detached,
        "count": len(all_branches),
        "remote_count": len(remote_entries),
        "fetched": fetched,
        "fetch_error": fetch_error,
    }


class CheckoutBody(BaseModel):
    name: str
    create: bool = False
    force: bool = False


@router.post("/checkout")
async def git_checkout(body: CheckoutBody, workspace_path: str | None = None) -> dict[str, Any]:
    ws = await _workspace_path(workspace_path)
    if ws is None or not _is_git_repo(ws):
        raise HTTPException(status_code=400, detail="no active git repo")

    args = ["checkout"]
    if body.create:
        args += ["-b"]
    elif body.force:
        args += ["-f"]
    args.append(body.name)

    r = _run_git(args, ws, timeout=15)
    if r.returncode != 0:
        raise HTTPException(status_code=400, detail=(r.stderr or r.stdout).strip()[:500])

    branch, head, _detached = _current_branch(ws)
    return {
        "status": "ok",
        "branch": branch,
        "head": head,
        "created": body.create,
    }


class SyncBody(BaseModel):
    push: bool = True


@router.post("/sync")
async def git_sync(body: SyncBody, workspace_path: str | None = None) -> dict[str, Any]:
    """Sync the active branch with its upstream: fetch + pull (rebase), then push if requested.

    Returns GitSyncResult discriminated by `status`:
      - "ok"         : pulled and pushed cleanly
      - "diverged"   : local + remote diverged, push rejected (force needed)
      - "dirty"      : working tree dirty, pull aborted
      - "no_upstream" : no upstream tracking branch
    """
    ws = await _workspace_path(workspace_path)
    if ws is None or not _is_git_repo(ws):
        raise HTTPException(status_code=400, detail="no active git repo")

    branch, _head, _detached = _current_branch(ws)

    # Find upstream
    upstream_proc = _run_git(
        ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], ws, timeout=5,
    )
    if upstream_proc.returncode != 0 or not upstream_proc.stdout.strip():
        return {
            "status": "no_upstream",
            "branch": branch,
            "remote": "",
            "fetched": False,
            "pulled": 0,
        }
    upstream = upstream_proc.stdout.strip()
    remote = upstream.split("/", 1)[0]

    # Dirty check before pull
    if _dirty_count(ws) > 0:
        return {
            "status": "dirty",
            "branch": branch,
            "remote": remote,
            "fetched": False,
            "pulled": 0,
        }

    # Fetch — use credential fallback so a stale osxkeychain token
    # doesn't break the sync.
    fetch_proc, _token_used = _run_git_with_credential_fallback(
        ["fetch", remote], ws, timeout=60
    )
    fetched = fetch_proc.returncode == 0
    if not fetched:
        raise HTTPException(
            status_code=500,
            detail=f"fetch {remote} failed: {(fetch_proc.stderr or fetch_proc.stdout).strip()[:500]}",
        )

    # Pull (rebase for cleaner history)
    pull_proc, _ = _run_git_with_credential_fallback(
        ["pull", "--rebase", "--autostash", remote, branch], ws, timeout=60
    )
    if pull_proc.returncode != 0:
        # Diverged?
        out = (pull_proc.stdout or "") + (pull_proc.stderr or "")
        if "diverged" in out.lower() or "non-fast-forward" in out.lower() or "rejected" in out.lower():
            return {
                "status": "diverged",
                "branch": branch,
                "remote": remote,
                "fetched": True,
                "pulled": 0,
            }
        raise HTTPException(status_code=500, detail=f"pull failed: {out.strip()[:500]}")
    pulled = 1 if pull_proc.returncode == 0 else 0

    # Push
    pushed_ok = True
    if body.push:
        push_proc, _ = _run_git_with_credential_fallback(
            ["push", remote, branch], ws, timeout=60
        )
        pushed_ok = push_proc.returncode == 0
        if not pushed_ok:
            out = (push_proc.stdout or "") + (push_proc.stderr or "")
            if "non-fast-forward" in out.lower() or "rejected" in out.lower():
                return {
                    "status": "diverged",
                    "branch": branch,
                    "remote": remote,
                    "fetched": True,
                    "pulled": pulled,
                }

    return {
        "status": "ok" if pushed_ok else "diverged",
        "branch": branch,
        "remote": remote,
        "fetched": True,
        "pulled": pulled,
    }
