"""Redaction + hashing for the runtime process channel.

Process metadata leaves the device (in a future phase) and is displayed to the
operator (dry-run), so argv is scrubbed of secret-looking tokens / credentials /
usernames before it is retained, and the working directory is reduced to a
project-root basename. Environment and memory are never read.

The token/credential/username scrubbing is the same pass the agent report uses
(:func:`runlayer_cli.scan.agents.redact.sanitize_path`) so the two channels stay
consistent; this module adds only the argv-list wrapper, the correlation hash,
and the cwd basename reduction.

Standard-library only (plus the sibling ``agents.redact`` / ``paths`` helpers,
themselves stdlib + RE2 ``regex_safe`` only) so this stays inside the frozen
``aiwatch`` bundle.
"""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from pathlib import PurePosixPath, PureWindowsPath

from runlayer_cli.scan.agents.redact import sanitize_path

# Cap the retained argv so an outlier command line (a huge inlined blob) can't
# bloat the payload or the dry-run display. The hash is still over the full argv
# so correlation is unaffected by this display cap.
MAX_ARGV_TOKENS = 64
MAX_ARGV_TOKEN_LEN = 512


def redact_argv(argv: Sequence[str], *, usernames: Sequence[str] = ()) -> list[str]:
    """Scrub each argv token, capping list + token length.

    Every token runs through :func:`sanitize_path` (URL creds, home/known
    usernames, secret tokens). A plain flag/value with nothing sensitive passes
    through unchanged. Over-long tokens are truncated with an ellipsis marker so
    a giant inlined argument can't dominate the payload.
    """
    redacted: list[str] = []
    for token in argv[:MAX_ARGV_TOKENS]:
        clean = sanitize_path(token, usernames=usernames) or ""
        if len(clean) > MAX_ARGV_TOKEN_LEN:
            clean = clean[:MAX_ARGV_TOKEN_LEN] + "...(truncated)"
        redacted.append(clean)
    if len(argv) > MAX_ARGV_TOKENS:
        redacted.append(f"...(+{len(argv) - MAX_ARGV_TOKENS} more)")
    return redacted


def redact_exe(exe: str | None, *, usernames: Sequence[str] = ()) -> str | None:
    """Scrub an executable path before it is retained/displayed.

    The exe path is kept readable (unlike argv it is rarely secret-bearing) but
    still run through :func:`sanitize_path` so a home-directory install location
    does not leak the account name -- matching how the agent channel treats
    every scan-derived path.
    """
    if not exe:
        return exe
    return sanitize_path(exe, usernames=usernames)


def command_hash(argv: Sequence[str]) -> str:
    """Stable SHA-256 over the full (unredacted) argv, for correlation only.

    Uses a unit-separator join so ``["a b"]`` and ``["a", "b"]`` never collide.
    The hash is one-way and is the only representation of the complete command
    line that is retained; the readable argv is the redacted form.
    """
    payload = "\x1f".join(argv)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def redact_cwd_project(cwd: str | None, *, usernames: Sequence[str] = ()) -> str | None:
    """Reduce a working directory to its project-root basename.

    The full path would leak the host directory layout; only the leaf directory
    name is retained (and still scrubbed, in case the basename is itself an
    account name or a secret-looking token). Both separators are handled so a
    Windows cwd collapses correctly even when the scan runs on POSIX.
    """
    if not cwd:
        return None
    posix_name = PurePosixPath(cwd).name
    windows_name = PureWindowsPath(cwd).name
    name = windows_name if len(windows_name) < len(posix_name) else posix_name
    if not name:
        return None
    return sanitize_path(name, usernames=usernames)
