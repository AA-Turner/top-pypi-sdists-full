"""Automatic version check + self-update with 1-hour TTL cache.

Checks if a newer version is available on the project's private GitLab registry
(remote install) or if ``origin/main`` has new commits (git clone install). The
registry check needs the same read token as the install itself; without one it
stays silent rather than reporting a phantom "up to date". When an update is
detected and ``auto_update`` is enabled in the user config, runs
``pysae-ai-tools self-update`` automatically. Otherwise, prints a yellow
notification inviting the user to update manually.

On the same hourly tick, when ``auto_update`` is enabled and no new release is
pending, a detached ``tools install --configure-only`` refreshes tool
configuration (auth tokens, MCP registration, contexts) so rotated secrets are
picked up without any binary install. It never runs alongside a self-update
(which reinstalls, and thus reconfigures, on its own).

Renewing the tokens this CLI manages is a separate tick with its own switch and
its own skip rules — see :mod:`pysae_ai_tools.token_rotation`. Nothing here
gates it: a credential nearing expiry must not depend on ``auto_update``.

Skipped in CI, non-interactive (piped stdout or stderr), or when ``--json`` is
in the argv — so scripted usage is never disrupted.
"""

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from .config import CACHE_DIR
from .env import cache
from .install_source import PACKAGE, PACKAGES_API, detect_install_source

CACHE_FILE = CACHE_DIR / "version-check.json"
LOCK_FILE = CACHE_DIR / "update.lock"
TTL_SECONDS = 3600  # 1 hour
LOCK_STALE_SECONDS = 600  # A self-update should never take >10 min.
TOKEN_VAR = "GITLAB_REGISTRY_TOKEN"

YELLOW = "\033[33m"
RESET = "\033[0m"


def _acquire_update_lock() -> bool:
    """Atomically acquire the update lock. Returns True on success.

    A stale lock (older than ``LOCK_STALE_SECONDS``) is force-removed to recover
    from crashed processes. The lock file holds the owner PID for debugging.
    """
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
    except OSError:
        return False

    try:
        if LOCK_FILE.exists():
            age = time.time() - LOCK_FILE.stat().st_mtime
            if age > LOCK_STALE_SECONDS:
                LOCK_FILE.unlink(missing_ok=True)
    except OSError:
        pass

    try:
        fd = os.open(str(LOCK_FILE), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return False
    except OSError:
        return False

    try:
        os.write(fd, str(os.getpid()).encode())
    finally:
        os.close(fd)
    return True


def _release_update_lock() -> None:
    try:
        LOCK_FILE.unlink(missing_ok=True)
    except OSError:
        pass


def _load_cache() -> dict[str, object]:
    try:
        if CACHE_FILE.exists():
            data = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
    except (json.JSONDecodeError, OSError):
        pass
    return {}


def _save_cache(data: dict[str, object]) -> None:
    try:
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        CACHE_FILE.write_text(json.dumps(data), encoding="utf-8")
    except OSError:
        pass


def _resolve_message() -> str | None:
    """Probe for an available update, picking the channel from the install source.

    A local directory install is polled against ``origin/main``; a registry
    install against the private GitLab registry. A local install that isn't a
    git repo has nothing to poll — never fall back to the registry for it (that
    would wrongly compare its build version against the published release).
    """
    source = detect_install_source()
    if source.local_dir is not None:
        if (source.local_dir / ".git").exists():
            return _check_git_updates(source.local_dir)
        return None
    return _check_registry_updates()


def _check_git_updates(repo: Path) -> str | None:
    """Check if origin/main has new commits. Returns a message or None."""
    try:
        subprocess.run(
            ["git", "-C", str(repo), "fetch", "--quiet", "origin", "main"],
            capture_output=True,
            timeout=10,
        )
        r = subprocess.run(
            ["git", "-C", str(repo), "rev-list", "--count", "HEAD..origin/main"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if r.returncode == 0:
            count = int(r.stdout.strip())
            if count > 0:
                return f"{count} new commit(s) available on origin/main"
    except (subprocess.TimeoutExpired, ValueError, OSError):
        pass
    return None


def _registry_token() -> str:
    """The PAT that reads the private registry — environment first, then cache.

    The same precedence the credential itself follows, read straight from the
    cache rather than through the ``env`` resolver: this runs on the way to a
    command the user actually asked for, and must not prompt or reach AWS. A
    missing token is not an error — the caller degrades to "no update known".
    """
    token = os.environ.get(TOKEN_VAR)
    if token:
        return token
    return cache.read(TOKEN_VAR) or ""


def _check_registry_updates() -> str | None:
    """Check the private GitLab registry for a newer release. Message or None.

    Ordered by publication date rather than by version: GitLab sorts versions as
    strings, which puts ``0.1.999`` above ``0.1.1000``. Publication order is the
    real one here, since the version is derived from the commit count.

    Every failure — no token, a revoked one, GitLab unreachable — is silence
    rather than noise: an update check runs on the way to a command the user
    actually asked for, and must never speak up about its own plumbing.
    """
    try:
        from pysae_ai_tools import __version__

        if ".dev" in __version__:
            return None

        token = _registry_token()
        if not token:
            return None

        import httpx

        r = httpx.get(
            PACKAGES_API,
            params={
                "package_type": "pypi",
                "package_name": PACKAGE,
                "order_by": "created_at",
                "sort": "desc",
                "per_page": 1,
            },
            headers={"PRIVATE-TOKEN": token},
            timeout=5.0,
            follow_redirects=True,
        )
        r.raise_for_status()
        packages = r.json()
        if not isinstance(packages, list) or not packages:
            return None
        latest = str(packages[0].get("version") or "")
        if latest and latest != __version__:
            return f"Update available: {__version__} → {latest}"
    except Exception:  # noqa: BLE001
        pass
    return None


def _progress_fd() -> int:
    """Descriptor the updater writes its progress to — stderr, falling back to
    discard when stderr has no real descriptor (captured streams)."""
    try:
        return sys.stderr.fileno()
    except (AttributeError, OSError, ValueError):
        return subprocess.DEVNULL


def _run_self_update() -> bool:
    """Invoke ``pysae-ai-tools self-update`` in a subprocess. Returns success."""
    exe = shutil.which("pysae-ai-tools")
    cmd = [exe, "self-update"] if exe else [sys.executable, "-m", "pysae_ai_tools", "self-update"]
    try:
        # Everything the updater's children print (git pull, install.sh, uv) is
        # progress, never data: keep it off the caller's stdout, which a command
        # substitution may be capturing and about to eval as shell.
        return subprocess.run(cmd, stdout=_progress_fd(), timeout=180).returncode == 0
    except (subprocess.TimeoutExpired, OSError):
        return False


def _spawn_configure_refresh() -> None:
    """Re-apply tool configuration in the background (auth, MCP registration,
    contexts) so rotated secrets are picked up — never installing or updating a
    binary. Detached, silent and best-effort: it never blocks or fails the
    current command. Throttled to once per TTL window by the shared cache."""
    # Don't recurse: the current command is itself a tools install.
    if len(sys.argv) > 2 and sys.argv[1] == "tools" and "install" in sys.argv[2:]:
        return
    exe = shutil.which("pysae-ai-tools")
    cmd = (
        [exe, "tools", "install", "--configure-only"]
        if exe
        else [sys.executable, "-m", "pysae_ai_tools", "tools", "install", "--configure-only"]
    )
    # The child skips its own version check (no nested self-update / refresh).
    env = {**os.environ, "PYSAE_SKIP_VERSION_CHECK": "1"}
    try:
        subprocess.Popen(
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=env,
            start_new_session=(os.name != "nt"),
            creationflags=(0x00000008 | 0x00000200) if os.name == "nt" else 0,
        )
    except OSError:
        pass


def _print_notification(message: str) -> None:
    print(f"{YELLOW}  {message}{RESET}", file=sys.stderr)
    print(f"{YELLOW}  Run: pysae-ai-tools self-update{RESET}", file=sys.stderr)


def _should_skip() -> bool:
    """Return True if the check should be silently skipped for this invocation."""
    # Avoid recursion when the user (or we) just ran self-update.
    if len(sys.argv) > 1 and sys.argv[1] == "self-update":
        return True

    # Skip when a parent process is already running self-update — this prevents
    # nested invocations (e.g. ``pysae-ai-tools tools install claude-plugin``
    # called from ``self-update``) from re-displaying the stale cached message.
    if os.environ.get("PYSAE_SKIP_VERSION_CHECK"):
        return True

    # Respect force override for tests / debugging.
    if os.environ.get("PYSAE_FORCE_VERSION_CHECK"):
        return False

    # Skip in CI, non-interactive output, or JSON-output mode.
    if os.environ.get("CI"):
        return True
    if not sys.stderr.isatty():
        return True
    # A captured stdout means a command substitution is consuming this run as
    # data — `eval "$(pysae-ai-tools env shell-init)"` in an rc file, the shell
    # completion hook, a pipeline. Anything the update prints there gets eval'd
    # or parsed by the caller, so never start one.
    if not sys.stdout.isatty():
        return True
    if "--json" in sys.argv:
        return True
    return False


def maybe_check_version() -> None:
    """Run version check (and auto-update if enabled). Cached for 1 hour."""
    if _should_skip():
        return

    # Make the config file discoverable on first interactive use, even when
    # no update is available. Skip paths (CI, --json, …) leave $HOME untouched.
    from pysae_ai_tools.config import load_config

    config = load_config()

    cache = _load_cache()
    last_check = cache.get("last_check", 0)
    if isinstance(last_check, (int, float)) and time.time() - last_check < TTL_SECONDS:
        msg = cache.get("message")
        if msg and isinstance(msg, str):
            _print_notification(msg)
        return

    message = _resolve_message()

    _save_cache({"last_check": time.time(), "message": message or ""})

    # Same hourly tick, same flag: refresh tool configuration when no release is
    # pending. On a release tick, self-update reinstalls (and reconfigures) on
    # its own, so the two never run together.
    if config.auto_update and not message:
        _spawn_configure_refresh()

    if not message:
        return

    if not config.auto_update:
        _print_notification(message)
        return

    from pysae_ai_tools.config import CONFIG_FILE

    # Serialize concurrent updates: only one process may run self-update.
    if not _acquire_update_lock():
        # Another instance is already updating — stay silent.
        return

    try:
        print(f"{YELLOW}  {message}{RESET}", file=sys.stderr)
        print(
            f"{YELLOW}  Auto-updating… " f"(disable with auto_update = false in {CONFIG_FILE}){RESET}",
            file=sys.stderr,
        )

        if _run_self_update():
            # Clear the cached message so subsequent invocations stay silent.
            _save_cache({"last_check": time.time(), "message": ""})
        else:
            print(
                f"{YELLOW}  Auto-update failed — run 'pysae-ai-tools self-update' manually{RESET}",
                file=sys.stderr,
            )
    finally:
        _release_update_lock()
