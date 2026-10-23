"""The user's login-shell environment, read fresh for the children that need it (plan D11, D14).

The service starts with a clean environment (`client.ENV_ALLOWLIST`), so its
own children lack what the user's profile exports: a proxy, a CA bundle, a
package mirror (`UV_INDEX*`), where the agents keep their files, and the PATH
that finds an agent installed with nvm or volta. A scheduled update run with
that clean environment fails behind a corporate proxy and misses those agents'
plugins. So, once per update cycle and once per action, the service asks the
login shell -- `$SHELL -ilc`, as the desktop app does (prbe-ai/desktop
`src-tauri/src/wizard.rs`, `login_shell_command`) -- for PATH and the
`protocol.CONTEXT_ENV` variables, and hands them to that one child.

Never stored, never logged, never journaled: a proxy or index URL can carry
`user:password@`. The values live in the child's environment and nowhere else.

What runs is plain `printf` and `"$NAME"` between markers, which sh, bash, zsh
and fish all read the same way, so a profile's banners or prompts around them
are ignored; PATH first and on its own, so a later failure cannot cost it.

Stdlib only (the start path; plan S1).
"""

from __future__ import annotations

import asyncio
import contextlib
import os
import signal
from pathlib import Path

from .protocol import CONTEXT_ENV

#: A profile that takes longer than this is killed; what it printed is still read.
TIMEOUT_S = 10.0
PATH_MARKER = "__PROBE_SERVICE_PATH__"
ENV_MARKER = "__PROBE_SERVICE_ENV__"
FIELD_MARKER = "__PROBE_SERVICE_SEP__"
#: After the login PATH (or the service's own), in this order: as the app's `build_path`.
FALLBACK_DIRS = ("/opt/homebrew/bin", "/usr/local/bin", "/usr/bin", "/bin", "/usr/sbin", "/sbin")
#: The variables read, besides PATH: what a request's context may carry.
NAMES = tuple(sorted(CONTEXT_ENV))
#: At most this much of the shell's output is read.
MAX_OUTPUT = 1024 * 1024


def script() -> str:
    fields = FIELD_MARKER.join(["%s"] * len(NAMES))
    values = " ".join(f'"${name}"' for name in NAMES)
    return f"printf '{PATH_MARKER}%s{PATH_MARKER}' \"$PATH\"; printf '{ENV_MARKER}{fields}{ENV_MARKER}' {values}"


def _marked(output: str, marker: str) -> str | None:
    start = output.find(marker)
    if start < 0:
        return None
    start += len(marker)
    end = output.find(marker, start)
    return None if end < 0 else output[start:end]


def parse(output: str) -> tuple[str, dict] | None:
    """`(PATH, {name: value})` from what the shell printed, or None unless it
    printed a PATH with at least one absolute directory. A value that is empty,
    or is its own name unexpanded, was not set."""
    path = _marked(output, PATH_MARKER)
    if path is None or not any(part.startswith("/") for part in path.split(":")):
        return None
    values = {}
    fields = _marked(output, ENV_MARKER)
    if fields is not None:
        parts = fields.split(FIELD_MARKER)
        if len(parts) == len(NAMES):
            for name, value in zip(NAMES, parts):
                if value and value != f"${name}" and "\0" not in value:
                    values[name] = value
    return path, values


def build_path(login: str | None, inherited: str | None, home: Path) -> str:
    """The child's PATH: the login shell's (or, failing that, the service's own),
    then `~/.local/bin` and the usual system and Homebrew folders. First
    occurrence wins; relative entries are dropped. The app's `build_path`."""
    base = login if login and login.strip() else (inherited or "")
    seen: set = set()
    out = []
    for raw in [*base.split(":"), str(home / ".local" / "bin"), *FALLBACK_DIRS]:
        entry = raw.rstrip("/") if len(raw) > 1 else raw
        if entry.startswith("/") and entry not in seen:
            seen.add(entry)
            out.append(entry)
    return ":".join(out)


async def read(*, timeout: float = TIMEOUT_S) -> tuple[str, dict] | None:
    """Ask the login shell. None when there is no shell, it printed no PATH,
    or it could not start. Never raises."""
    shell = os.environ.get("SHELL") or ""
    if not shell or not os.path.isabs(shell):
        return None
    home = Path.home()
    try:
        child = await asyncio.create_subprocess_exec(
            shell,
            "-ilc",
            script(),
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            cwd=str(home) if home.is_dir() else "/",
            start_new_session=True,
        )
    except (OSError, ValueError):
        return None
    chunks: list = []

    async def drain() -> None:
        assert child.stdout is not None
        size = 0
        while size < MAX_OUTPUT:
            chunk = await child.stdout.read(65536)
            if not chunk:
                return
            chunks.append(chunk)
            size += len(chunk)

    try:
        await asyncio.wait_for(drain(), timeout)
    except asyncio.TimeoutError:
        pass
    finally:
        # The whole group: an interactive profile may have started jobs of its own.
        with contextlib.suppress(ProcessLookupError, PermissionError, OSError):
            os.killpg(child.pid, signal.SIGKILL)
        with contextlib.suppress(Exception):
            await asyncio.wait_for(child.wait(), 2.0)
    return parse(b"".join(chunks).decode("utf-8", "replace"))


async def child_env(*, vars: bool) -> dict:
    """What a child gets from the login shell: PATH merged as the app merges it,
    and, with `vars`, the context variables it sets. `{}`-plus-PATH when the
    shell gives nothing (the service's own PATH, merged the same way)."""
    found = await read()
    login_path, values = found if found is not None else (None, {})
    env = {"PATH": build_path(login_path, os.environ.get("PATH"), Path.home())}
    if vars:
        env.update(values)
    return env
