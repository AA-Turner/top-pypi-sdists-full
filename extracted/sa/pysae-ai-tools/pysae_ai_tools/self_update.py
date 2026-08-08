"""Self-update pysae-ai-tools.

Two modes, picked from the uv install source (see ``install_source``):
- **Local checkout** (``uv tool install [-e] <repo>``): ``git pull`` + re-run ``install.sh``
- **Registry install** (via uv): ``uv tool upgrade pysae-ai-tools``, against the
  project's private GitLab index
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Annotated

import typer

from .common.windows import schedule_deferred_cmd
from .install_source import INDEX_ARGS, PACKAGE, detect_install_source

# After an update, (re)install + reconfigure the already-selected embedded tools (usage hooks +
# status line) and MCP servers, so both new server versions and config/code changes take effect.
# selected-only: never adds tools the user did not choose (a no-op when nothing is selected). Not
# configure-only — that would skip MCP server version bumps, which is exactly what we want here.
_RECONFIGURE_ARGS = ["--category", "embedded", "--category", "mcp", "--selected", "--non-interactive"]


def _local_checkout() -> Path | None:
    """Return the source repo when installed from a local checkout, else None.

    A local install only counts as a git checkout we can pull + reinstall when
    the recorded source directory is an actual git repo with an installer.
    """
    repo = detect_install_source().local_dir
    if repo is None:
        return None
    has_installer = (repo / "install.sh").exists() or (repo / "install.ps1").exists()
    if (repo / ".git").exists() and has_installer:
        return repo
    return None


def _run(cmd: list[str], cwd: Path | None = None) -> int:
    print(f"$ {' '.join(cmd)}", file=sys.stderr)
    return subprocess.run(cmd, cwd=cwd).returncode


def _has_local_changes(repo: Path) -> bool:
    """True when the working tree or index has uncommitted changes.

    Uses ``git status --porcelain`` (tracked + untracked); any output means
    the tree is dirty and a plain ``git pull`` could fail or be blocked.
    """
    result = subprocess.run(
        ["git", "-C", str(repo), "status", "--porcelain"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return bool((result.stdout or "").strip())


def _update_from_git(repo: Path, no_pull: bool, rebase: bool) -> None:
    """Update from git clone: pull + reinstall.

    When the working tree is dirty, the local changes are stashed (including
    untracked files) before pulling and restored afterwards, so the update
    works even mid-edit.
    """
    if not no_pull:
        # Stash local changes (tracked + untracked) so the pull isn't blocked
        # by a dirty tree, then pop them back once it succeeds.
        stashed = False
        if _has_local_changes(repo):
            print("Local changes detected — stashing before pull.", file=sys.stderr)
            stash_args = [
                "git",
                "-C",
                str(repo),
                "stash",
                "push",
                "--include-untracked",
                "--message",
                "pysae-ai-tools self-update",
            ]
            if _run(stash_args) != 0:
                print("FAILED: git stash failed. Resolve manually and retry.", file=sys.stderr)
                sys.exit(1)
            stashed = True

        pull_args = ["git", "-C", str(repo), "pull"]
        pull_args.append("--rebase" if rebase else "--ff-only")
        if _run(pull_args) != 0:
            if stashed:
                print(
                    "FAILED: git pull failed. Your changes are saved in the git stash — "
                    "restore them with 'git -C %s stash pop'." % repo,
                    file=sys.stderr,
                )
            else:
                print("FAILED: git pull failed. Resolve manually and retry.", file=sys.stderr)
            sys.exit(1)

        if stashed:
            print("Restoring local changes (git stash pop).", file=sys.stderr)
            if _run(["git", "-C", str(repo), "stash", "pop"]) != 0:
                print(
                    "WARNING: 'git stash pop' hit a conflict. Your changes are still in the "
                    "stash — resolve the conflict and run 'git -C %s stash pop' again." % repo,
                    file=sys.stderr,
                )
                sys.exit(1)

    is_windows = os.name == "nt"
    ps1 = repo / "install.ps1"
    sh = repo / "install.sh"

    if is_windows and ps1.exists():
        rc = _run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(ps1)])
    elif sh.exists():
        rc = _run(["bash", str(sh)])
    else:
        print(f"FAILED: no installer found in {repo}", file=sys.stderr)
        sys.exit(1)

    if rc != 0:
        print("FAILED: installer exited with errors.", file=sys.stderr)
        sys.exit(rc)


def _schedule_windows_deferred_upgrade() -> bool:
    """Spawn a detached cmd that finishes the upgrade after we exit.

    On Windows the running ``pysae-ai-tools.exe`` shim is locked, so
    ``uv tool upgrade`` succeeds at updating the venv but fails to copy
    the new shim onto the old one (os error 32). The bat polls for our
    PID, then re-runs the upgrade, the plugin install, and shell
    completion using the freshly-copied shim.
    """
    if os.name != "nt":
        return False

    # Log lives in its own directory so it survives the deferred script's
    # self-cleanup of its scratch dir.
    log = Path(tempfile.mkdtemp(prefix="pysae-update-")) / "update.log"

    script_lines = [
        f'uv tool upgrade {" ".join(INDEX_ARGS)} {PACKAGE} >> "{log}" 2>&1',
        f'pysae-ai-tools tools install --category plugin >> "{log}" 2>&1',
        f'pysae-ai-tools tools install {" ".join(_RECONFIGURE_ARGS)} >> "{log}" 2>&1',
        f'pysae-ai-tools install-completion >> "{log}" 2>&1',
    ]

    try:
        schedule_deferred_cmd(os.getpid(), script_lines)
    except OSError as exc:
        print(f"Failed to schedule deferred upgrade: {exc}", file=sys.stderr)
        return False

    print(f"Log: {log}", file=sys.stderr)
    return True


def _is_windows_lock_error(stdout: str, stderr: str) -> bool:
    """True when uv's failure is the running-shim file lock (locale-agnostic).

    uv surfaces the underlying ``io::Error`` whose ``Display`` impl ends with
    ``(os error 32)`` — Windows ``ERROR_SHARING_VIOLATION``. The
    accompanying message (``The process cannot access the file because…`` /
    ``Le processus ne peut pas accéder au fichier…``) is locale-translated
    by Windows, so we anchor on the numeric code only.
    """
    return "os error 32" in (stdout + stderr).lower()


def _uv_upgrade_actually_upgraded(stdout: str, stderr: str) -> bool:
    """Did ``uv tool upgrade`` actually move the package to a newer version?

    uv prints ``Updated <package> v<old> -> v<new>`` on a real upgrade and
    ``Nothing to upgrade`` (or similar) when the package was already at the
    latest. We only need the plugin reinstall + completion refresh in the
    real-upgrade case.
    """
    combined = f"{stdout}\n{stderr}".lower()
    return f"updated {PACKAGE}" in combined


def _print_upgrade_summary_only(stdout: str, stderr: str) -> None:
    """Print only uv's "Updated <pkg> v<old> -> v<new>" / "Downloaded …"
    progress lines, dropping the noisy "error: Failed to upgrade …
    Caused by: …" trailer that follows when uv hit the running-shim
    file lock on Windows. The deferred update we schedule next will
    finish the job, so the error is misleading.
    """
    skip_markers = ("error:", "  Caused by:")
    for line in stdout.splitlines():
        sys.stdout.write(line + "\n")
    for line in stderr.splitlines():
        if line.startswith(skip_markers):
            continue
        sys.stderr.write(line + "\n")


def _update_from_registry() -> None:
    """Update from the private GitLab registry via uv tool upgrade.

    The index is passed explicitly even though uv records it in the tool receipt
    at install time: an install predating the registry migration carries a
    receipt without it, and would otherwise upgrade against a public index.
    """
    print("Updating from the private GitLab registry...", file=sys.stderr)

    cmd = ["uv", "tool", "upgrade", *INDEX_ARGS, PACKAGE]
    print(f"$ {' '.join(cmd)}", file=sys.stderr)
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")

    if result.returncode != 0:
        # Windows file-lock case: the venv was upgraded but uv couldn't
        # overwrite the running shim. Hide uv's misleading "error: Failed
        # to upgrade" trailer (the deferred re-run we schedule next will
        # finish the job) and surface our own clean status message.
        if os.name == "nt" and _is_windows_lock_error(result.stdout, result.stderr):
            if _schedule_windows_deferred_upgrade():
                _print_upgrade_summary_only(result.stdout, result.stderr)
                print(
                    "\nThe upgrade will finish a few seconds after this process exits "
                    "(uv can't overwrite the running shim — deferring).",
                    file=sys.stderr,
                )
                print(
                    "Wait ~10s before running pysae-ai-tools again.",
                    file=sys.stderr,
                )
                return
        # All other failures: surface uv's full output verbatim.
        sys.stdout.write(result.stdout)
        sys.stderr.write(result.stderr)
        print("FAILED: uv tool upgrade failed.", file=sys.stderr)
        sys.exit(result.returncode)

    # Successful upgrade — show uv's full output.
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)

    # Skills + plugin manifest live inside the package, so when uv tool
    # upgrade was a no-op nothing on disk changed — no point re-running
    # the plugin install or the completion refresh.
    if not _uv_upgrade_actually_upgraded(result.stdout, result.stderr):
        print("Already at the latest version — skipping plugin reinstall.", file=sys.stderr)
        return

    # Redeploy the Pysae skills to every assistant present (Claude, Codex, …) with the new
    # version — assistant-agnostic, each deployment no-ops when its CLI is absent.
    print("Deploying skills to installed assistants...", file=sys.stderr)
    _run(["pysae-ai-tools", "tools", "install", "--category", "plugin"])

    # Re-apply config for the selected embedded tools (usage hooks/status line) and MCP servers.
    print("Reconfiguring embedded tools and MCP servers...", file=sys.stderr)
    _run(["pysae-ai-tools", "tools", "install", *_RECONFIGURE_ARGS])

    # Update shell completion
    from .install_completion import install_completion

    install_completion()


def main(
    no_pull: Annotated[bool, typer.Option("--no-pull", help="Skip git pull (only re-run installer)")] = False,
    rebase: Annotated[bool, typer.Option("--rebase", help="Use 'git pull --rebase' instead of '--ff-only'")] = False,
) -> None:
    """Update pysae-ai-tools to the latest version."""
    # Inherited by every child process we spawn (uv, tools install --category plugin,
    # install_completion). Suppresses the version-check banner during the
    # update — otherwise the still-cached "Update available" message gets
    # re-printed by sub-invocations before the cache is cleared.
    os.environ["PYSAE_SKIP_VERSION_CHECK"] = "1"

    repo = _local_checkout()

    if repo:
        print(f"Local checkout detected at {repo}", file=sys.stderr)
        _update_from_git(repo, no_pull, rebase)
    else:
        _update_from_registry()

    # One-shot relocation of any legacy on-disk state to the XDG dirs (idempotent, best-effort).
    from .migrate import run_migration

    run_migration()

    print("\npysae-ai-tools is up to date.", file=sys.stderr)
