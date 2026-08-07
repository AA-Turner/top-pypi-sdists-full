"""Hourly, unattended renewal of the managed access tokens.

The same shape as :mod:`version_check` — a TTL-throttled tick riding on every
command — but a **separate** concern, and deliberately not the same switch: a
credential nearing expiry is not a version to install, so ``auto_update`` must
not silence it. ``auto_rotate_tokens`` gates this pass alone.

The work runs in a detached child (``tools rotate-tokens``) rather than inline:
introspecting and rotating means two round-trips to GitLab, which no command
should pay for. The child is silent and writes nothing to the caller's streams,
so this is safe under a command substitution — unlike the version check, this
tick therefore also runs when stdout is captured or ``--json`` was asked for,
which is how most of the CLI is actually invoked.

Never in CI: there the token comes from a shared pipeline variable that no job
can write back, and rotating it would revoke it for every other job. The veto is
enforced again in :func:`pysae_ai_tools.install.registry_credential.sweep`, so no
path can rotate on a runner.
"""

import os
import shutil
import subprocess
import sys

from .common.registry_auth import journal

TTL_SECONDS = 3600  # 1 hour, like the version check.

# Commands whose own run already arbitrates rotation, or that must not spawn a
# child while replacing the package on disk.
_EXEMPT_COMMANDS = frozenset({"self-update", "uninstall"})


def _should_skip() -> bool:
    """True when this invocation must not start a rotation pass."""
    argv = sys.argv[1:]

    if os.environ.get("CI"):
        return True

    # Set on every child we spawn: the pass is already running.
    if os.environ.get("PYSAE_SKIP_TOKEN_ROTATION") or os.environ.get("PYSAE_SKIP_VERSION_CHECK"):
        return True

    if argv and argv[0] in _EXEMPT_COMMANDS:
        return True

    # `tools install` and `tools rotate-tokens` rotate as part of their own work —
    # spawning a second pass alongside would race it for the same credential.
    if argv[:1] == ["tools"] and ({"install", "rotate-tokens"} & set(argv[1:])):
        return True

    return False


def _due(now_seconds: float | None) -> bool:
    return now_seconds is None or now_seconds >= TTL_SECONDS


def _spawn() -> None:
    """Run the rotation pass detached, silent and best-effort."""
    exe = shutil.which("pysae-ai-tools")
    cmd = [exe, "tools", "rotate-tokens"] if exe else [sys.executable, "-m", "pysae_ai_tools", "tools", "rotate-tokens"]
    env = {**os.environ, "PYSAE_SKIP_TOKEN_ROTATION": "1", "PYSAE_SKIP_VERSION_CHECK": "1"}
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


def maybe_rotate_tokens() -> None:
    """Start a rotation pass when one is due. Cached for an hour, never blocking."""
    if _should_skip():
        return

    from .config import load_config

    if not load_config().auto_rotate_tokens:
        return

    if not _due(journal.age_seconds(journal.read().last_swept_at)):
        return

    _spawn()
