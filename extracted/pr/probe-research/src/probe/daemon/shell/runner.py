"""run an allowed command: minimal environment, blanked git drivers, head/tail-capped output, whole-group kill."""

from __future__ import annotations

import asyncio
import os
import re
import signal
import tempfile
from pathlib import Path
from typing import Callable
from probe.sdk.settings.settings import DAEMON_SHELL_CONFIG
from probe.daemon.shell.classifier.refusals import _Refuse
from probe.daemon.shell.parse import _expand, _split, _tokenize, _walk
from probe.daemon.shell.verdict import ShellResult
from probe.daemon.shell.words import _clean_path


# --- the runner ------------------------------------------------------------

#: git settings forced on every command (the highest-precedence config level).
_GIT_CONFIG = (
    ("core.hooksPath", "/dev/null"),
    ("core.fsmonitor", "false"),
    ("core.pager", "cat"),
    ("diff.external", ""),
    ("core.sshCommand", "false"),
    ("protocol.allow", "never"),
    ("log.showSignature", "false"),
    ("gpg.program", "false"),
    ("gpg.openpgp.program", "false"),
    ("gpg.x509.program", "false"),
    ("gpg.ssh.program", "false"),
    ("diff.ignoreSubmodules", "all"),
    ("status.submoduleSummary", "false"),
    ("submodule.recurse", "false"),
)
#: Per-driver programs a repository can name; `run` blanks every one it defines.
_GIT_DRIVER_KEYS = r"^(filter|diff)\..+\.(clean|smudge|process|textconv|command)$"


#: A config path that never exists, so a `probe` run by the daemon's shell has no key.
NO_PROBE_CONFIG = DAEMON_SHELL_CONFIG


def minimal_env(env_extra: dict[str, str] | None = None) -> dict[str, str]:
    """The whole environment a command gets: nothing from the parent but PATH and HOME.

    No Probe token, no API keys, no BASH_ENV (bash would source it), no GIT_DIR.
    And no Probe config: `PROBE_CONFIG_PATH` names a file that does not exist, so a
    `probe` started from here has no key and writes nothing -- the daemon writes to
    Probe only through its probe tool (pre-check, lease, logbook), even when bypass
    mode runs whatever the shell is given.
    """
    env = {
        "PATH": _clean_path(os.environ.get("PATH")),
        "HOME": os.environ.get("HOME") or str(Path.home()),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TERM": "dumb",
        "NO_COLOR": "1",
        # `python -c` imports nothing from the folder it runs in (Python 3.11+), and
        # writes no `.pyc`: a command Jev approved runs only the code its text shows.
        "PYTHONSAFEPATH": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PAGER": "cat",
        "GIT_PAGER": "cat",
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_OPTIONAL_LOCKS": "0",  # reads never rewrite the index (no post-index-change hook)
        "GIT_CONFIG_COUNT": str(len(_GIT_CONFIG)),
        "PROBE_CONFIG_PATH": NO_PROBE_CONFIG,
        "PROBE_TELEMETRY": "off",
    }
    for n, (key, value) in enumerate(_GIT_CONFIG):
        env[f"GIT_CONFIG_KEY_{n}"] = key
        env[f"GIT_CONFIG_VALUE_{n}"] = value
    if env_extra:
        env.update(env_extra)
    return env


def _git_dirs(command: str, cwd: str, home: str) -> set[str]:
    """The folders git may run in during `command` (best effort; for blanking drivers)."""
    try:
        parts = _split(_tokenize(command))
    except _Refuse:
        return {cwd} if re.search(r"\bgit\b", command) else set()
    dirs: set[str] = set()
    for part, cands in _walk(parts, cwd, home):
        words = part.words
        if not words or os.path.basename(words[0].value) != "git":
            continue
        here = {os.path.realpath(c) for c in cands}
        k = 1
        while k < len(words) and words[k].value.startswith("-"):
            if words[k].value == "-C" and k + 1 < len(words):
                path = _expand(words[k + 1], home)
                here = {os.path.realpath(os.path.join(d, path)) for d in here}
                k += 1
            k += 1
        dirs |= here
    return {d for d in dirs if os.path.isdir(d)}


async def _blank_git_drivers(env: dict[str, str], dirs: set[str]) -> None:
    """Add a blank value for every filter / diff driver program the repositories define.

    A clean filter runs inside `git status` and `git diff`, and there is no flag
    to turn it off; a blank command is skipped. `git config` itself runs nothing.
    """
    keys: set[str] = set()
    for folder in sorted(dirs):
        try:
            proc = await asyncio.create_subprocess_exec(
                "git", "config", "-z", "--get-regexp", _GIT_DRIVER_KEYS,
                cwd=folder, env=env, stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL,
            )  # fmt: skip
        except OSError:
            return  # no git: nothing to protect
        try:
            out, _ = await asyncio.wait_for(proc.communicate(), 10)
        except TimeoutError:
            proc.kill()
            await proc.wait()
            continue
        for entry in out.decode("utf-8", "replace").split("\0"):
            key = entry.split("\n", 1)[0]
            if key:
                keys.add(key)
    n = int(env.get("GIT_CONFIG_COUNT", "0"))
    for key in sorted(keys):
        env[f"GIT_CONFIG_KEY_{n}"] = key
        env[f"GIT_CONFIG_VALUE_{n}"] = ""
        n += 1
    env["GIT_CONFIG_COUNT"] = str(n)


class _Capture:
    """Keeps the first and last `keep` bytes of a stream, counting the rest."""

    def __init__(self, keep: int) -> None:
        self.keep = keep
        self.head = bytearray()
        self.tail = bytearray()
        self.total = 0

    def feed(self, chunk: bytes) -> None:
        self.total += len(chunk)
        room = self.keep - len(self.head)
        if room > 0:
            self.head += chunk[:room]
            chunk = chunk[room:]
        if chunk:
            self.tail += chunk
            if len(self.tail) > self.keep:
                del self.tail[: len(self.tail) - self.keep]

    def text(self, max_chars: int) -> tuple[str, bool]:
        dropped = self.total - len(self.head) - len(self.tail)
        if dropped == 0:
            full = (self.head + self.tail).decode("utf-8", "replace")
            if len(full) <= max_chars:
                return full, False
            head_text, tail_text = full, full
        else:
            head_text = self.head.decode("utf-8", "replace")
            tail_text = self.tail.decode("utf-8", "replace")
        half = max(max_chars // 2, 1)
        head_text, tail_text = head_text[:half], tail_text[-half:]
        kept = len(head_text.encode()) + len(tail_text.encode())
        marker = f"\n[... {max(self.total - kept, 0)} bytes of output left out ...]\n"
        return head_text + marker + tail_text, True


def _kill_group(proc: asyncio.subprocess.Process) -> None:
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass


#: How often `run` asks its `watch` whether the command may go on.
WATCH_POLL_S = 1.0
#: How long a killed process group is waited for before `run` gives up on reaping it.
REAP_S = 5.0


async def stop_group(proc: asyncio.subprocess.Process, reader: asyncio.Future | None = None) -> None:
    """Kill the command's whole process group and reap it (bounded), whatever
    else is happening: also on the way out of a cancelled task, so a bite cut
    short at the session's end leaves nothing running behind it."""
    _kill_group(proc)
    cancelled = False  # a cancellation that arrives meanwhile is passed on once the group is reaped
    if reader is not None:
        try:
            await asyncio.wait({reader}, timeout=REAP_S)
        except asyncio.CancelledError:
            cancelled = True
        if not reader.done():
            reader.cancel()
        elif not reader.cancelled():
            reader.exception()  # retrieved: a pipe error of a killed command is not news
    try:
        await asyncio.wait_for(proc.wait(), REAP_S)
    except asyncio.CancelledError:
        cancelled = True
    except (TimeoutError, OSError):
        pass  # a group that will not die in time: it was killed, and the loop reaps it later
    if cancelled:
        raise asyncio.CancelledError


async def run(
    command: str,
    *,
    cwd: Path,
    timeout_s: float = 60,
    max_output_chars: int = 30_000,
    env_extra: dict[str, str] | None = None,
    watch: Callable[[], str | None] | None = None,
    stdin: bytes | None = None,
) -> ShellResult:
    """Run a command `classify` passed (or the researcher approved).

    `/bin/bash --noprofile --norc`, `minimal_env()`, stdin closed (or `stdin`'s
    bytes, from an unlinked temporary file: a probe command's output fed to a
    filter), stdout and stderr together. At `timeout_s` the whole process group is killed. `watch`,
    asked right before the launch and every `WATCH_POLL_S` while it runs, returns
    why it must stop now (the daemon's lease: the researcher moved the switch) or
    None; nothing is started, or the group is killed, and the result says so in
    `stopped`. A cancelled caller kills and
    reaps the group before the cancellation goes on.
    """
    env = minimal_env(env_extra)
    dirs = _git_dirs(command, os.path.realpath(str(cwd)), env["HOME"])
    if dirs:
        await _blank_git_drivers(env, dirs)
    # Asked once more right before the launch: preparing git awaited subprocesses,
    # and the answer may have changed meanwhile. A stop now starts nothing.
    stopped = watch() if watch is not None else None
    if stopped is not None:
        return ShellResult(exit_code=None, output="", truncated=False, timed_out=False, stopped=stopped,
                           started=False)
    source = None
    if stdin is not None:
        source = tempfile.TemporaryFile()
        source.write(stdin)
        source.seek(0)
    try:
        proc = await asyncio.create_subprocess_exec(
            "/bin/bash", "--noprofile", "--norc", "-c", "--", command,
            cwd=str(cwd), env=env, stdin=source if source is not None else asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT,
            start_new_session=True,  # its own process group, so a timeout kills everything
        )  # fmt: skip
    finally:
        if source is not None:
            source.close()  # the command holds its own copy of the file
    capture = _Capture(max(max_output_chars, 1) * 2)

    async def pump() -> None:
        assert proc.stdout is not None
        while chunk := await proc.stdout.read(65536):
            capture.feed(chunk)
        await proc.wait()

    reader = asyncio.ensure_future(pump())
    loop = asyncio.get_running_loop()
    deadline = loop.time() + timeout_s
    timed_out = False
    try:
        while True:
            left = deadline - loop.time()
            if left <= 0:
                timed_out = True
                break
            done, _ = await asyncio.wait({reader}, timeout=min(WATCH_POLL_S, left) if watch else left)
            if done:
                reader.result()
                break
            if watch is not None:
                stopped = watch()
                if stopped is not None:
                    break
    except BaseException:
        await stop_group(proc, reader)
        raise
    if timed_out or stopped is not None:
        await stop_group(proc, reader)
    output, truncated = capture.text(max_output_chars)
    return ShellResult(
        exit_code=None if (timed_out or stopped is not None) else proc.returncode,
        output=output,
        truncated=truncated,
        timed_out=timed_out,
        stopped=stopped,
    )
