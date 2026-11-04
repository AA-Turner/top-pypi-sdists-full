"""Persistent SSH session into a remote sandbox VM over the session mesh.

The ``computer`` MCP server's ``bash`` / ``read_file`` / ``write_file`` /
``edit_file`` tools can run over this instead of the desktop agent's HTTP
``/bash`` + ``/edit`` endpoints. One multiplexed ssh connection carries:

* a **persistent shell** (``bash --noprofile --norc -s``) that every ``bash``
  call feeds a command to, so ``cd``, exported variables and started
  background jobs survive between calls the way they do in Claude Code's own
  Bash tool; each command's output is delimited by a per-call sentinel that
  also carries the exit code and the new working directory;
* **exec channels** on the same master connection for file transfers, so a
  read or write never waits behind a running command.

A command that exceeds its timeout cannot be interrupted inside the shared
shell, so the shell is killed and reopened in the last working directory
(the remote side gets SIGHUP when the channel drops) — the same recovery the
reference bash tool uses.

Only the system ``ssh`` binary is needed on this side and ``sshd`` on the
sandbox; nothing is installed on either VM.
"""

from __future__ import annotations

import asyncio
import base64
import logging
import shlex
import shutil
import uuid
from pathlib import Path
from tempfile import mkdtemp

from plato.computer_use.base import ToolResult, _cap_bash_result

logger = logging.getLogger(__name__)

# Bytes of a file the read tool returns before it says the rest was cut.
MAX_READ_BYTES = 512 * 1024
# Bytes ``edit_file`` is willing to round-trip.
MAX_EDIT_BYTES = 4 * 1024 * 1024
# Bytes of an image ``read_file`` will inline as an ImageContent block.
MAX_IMAGE_BYTES = 5 * 1024 * 1024
# Lines a search returns before it says the rest was cut.
MAX_SEARCH_LINES = 200
_DIR_MARKER = "__PLATO_SANDBOX_DIR__"
_IMG_MARKER = "__PLATO_SANDBOX_IMG__"
_LINE_LIMIT = 16 * 1024 * 1024


class SshSandbox:
    """One ssh identity, one master connection, one long-lived shell."""

    def __init__(
        self,
        host: str,
        private_key: str,
        *,
        user: str = "root",
        connect_timeout: int = 20,
        logger: logging.Logger | None = None,
    ) -> None:
        self._host = host
        self._user = user
        self._private_key = private_key
        self._connect_timeout = connect_timeout
        self._logger = logger or logging.getLogger(__name__)
        self._dir: Path | None = None
        self._key_path: Path | None = None
        self._socket: Path | None = None
        self._shell: asyncio.subprocess.Process | None = None
        self._cwd = "~"
        self._lock = asyncio.Lock()

    # ---- lifecycle ----

    @property
    def target(self) -> str:
        return f"{self._user}@{self._host}"

    async def start(self) -> None:
        """Write the key, open the master connection, and start the shell."""
        self._dir = Path(mkdtemp(prefix="plato-sandbox-"))
        self._dir.chmod(0o700)
        self._key_path = self._dir / "id"
        self._key_path.write_text(self._private_key.rstrip("\n") + "\n")
        self._key_path.chmod(0o600)
        self._socket = self._dir / "ctl"
        try:
            await self._open_shell()
            probe = await self.bash("true", timeout=self._connect_timeout)
            if probe.error:
                raise RuntimeError(probe.error)
        except Exception:
            await self.close()
            raise
        self._logger.info("Sandbox shell open on %s", self.target)

    async def close(self) -> None:
        await self._kill_shell()
        if self._socket is not None and self._socket.exists():
            try:
                proc = await asyncio.create_subprocess_exec(
                    *self._ssh_prefix(),
                    "-O",
                    "exit",
                    self.target,
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL,
                )
                await asyncio.wait_for(proc.wait(), timeout=5)
            except Exception:  # noqa: BLE001 - best-effort teardown
                pass
        if self._dir is not None:
            shutil.rmtree(self._dir, ignore_errors=True)
            self._dir = None

    # ---- ssh plumbing ----

    def _ssh_prefix(self) -> list[str]:
        """``ssh`` plus the options every channel shares (tests override this)."""
        assert self._key_path is not None and self._socket is not None
        return [
            "ssh",
            "-i",
            str(self._key_path),
            "-o",
            "BatchMode=yes",
            "-o",
            "IdentitiesOnly=yes",
            "-o",
            "StrictHostKeyChecking=no",
            "-o",
            "UserKnownHostsFile=/dev/null",
            "-o",
            "LogLevel=ERROR",
            "-o",
            f"ConnectTimeout={self._connect_timeout}",
            "-o",
            "ServerAliveInterval=15",
            "-o",
            "ServerAliveCountMax=4",
            "-o",
            f"ControlPath={self._socket}",
            "-o",
            "ControlMaster=auto",
            "-o",
            "ControlPersist=600",
        ]

    async def _exec(self, command: str, *, stdin: bytes | None = None, timeout: float = 60) -> tuple[int, bytes, bytes]:
        """Run one command on its own channel (file transfers, probes).

        Starts in the persistent shell's cwd, not the login home. A fresh SSH
        channel would otherwise land in ``~`` while the model believes it is
        wherever it last ``cd``-ed, so every relative path the file and search
        tools take — ``grep pattern .`` after ``cd /repo`` — would silently
        resolve against the wrong directory and come back empty.
        """
        proc = await asyncio.create_subprocess_exec(
            *self._ssh_prefix(),
            self.target,
            command if self._cwd == "~" else f"cd {shlex.quote(self._cwd)} 2>/dev/null || cd ~\n{command}",
            stdin=asyncio.subprocess.PIPE if stdin is not None else asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            limit=_LINE_LIMIT,
        )
        try:
            out, err = await asyncio.wait_for(proc.communicate(stdin), timeout=timeout)
        except TimeoutError:
            proc.kill()
            await proc.wait()
            raise
        return proc.returncode or 0, out, err

    async def _open_shell(self) -> None:
        # stderr is folded into stdout inside the remote shell so the model
        # sees a command's output in order, as one stream.
        self._shell = await asyncio.create_subprocess_exec(
            *self._ssh_prefix(),
            self.target,
            "bash --noprofile --norc -s",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            limit=_LINE_LIMIT,
        )
        assert self._shell.stdin is not None
        self._shell.stdin.write(
            (f'exec 2>&1\n__plato_state="$(mktemp -d)"\ncd {shlex.quote(self._cwd)} 2>/dev/null || cd ~\n').encode()
        )
        await self._shell.stdin.drain()

    async def _kill_shell(self) -> None:
        shell, self._shell = self._shell, None
        if shell is None or shell.returncode is not None:
            return
        shell.kill()
        # Over ssh the channel drop ends the remote side at once; the short
        # wait only guards against a client that lingers on an inherited pipe.
        try:
            await asyncio.wait_for(shell.wait(), timeout=1)
        except TimeoutError:
            pass

    # ---- tools ----

    async def bash(self, command: str, timeout: int = 120) -> ToolResult:
        """Run ``command`` in the persistent shell; output capped, state kept."""
        async with self._lock:
            if not command.strip():
                return ToolResult()
            sentinel = f"__PLATO_SANDBOX_{uuid.uuid4().hex}__"
            # The command runs in a subshell so an `exit`, a syntax error or
            # a stray `set -e` cannot take the persistent shell down; on the
            # way out it records its cwd and exported variables, which the
            # persistent shell restores before printing the sentinel — so
            # `cd`/`export` still carry over to the next call. The newline
            # before `)` closes a trailing comment. The subshell's stdin is
            # /dev/null: the rest of this script is still unread on the shell's
            # stdin, so a command reading stdin (cat, read, python) would
            # otherwise swallow the sentinel and hang until the timeout.
            script = (
                'rm -f -- "$__plato_state/cwd" "$__plato_state/env"\n'
                "(\n"
                f"{command}\n"
                '__plato_rc=$?; pwd > "$__plato_state/cwd"; export -p > "$__plato_state/env"; exit "$__plato_rc"\n'
                ") </dev/null\n"
                "__plato_rc=$?\n"
                '[ -f "$__plato_state/cwd" ] && cd -- "$(cat "$__plato_state/cwd")" 2>/dev/null\n'
                '[ -f "$__plato_state/env" ] && . "$__plato_state/env" 2>/dev/null\n'
                f'printf \'\\n{sentinel} %s %s\\n\' "$__plato_rc" "$PWD"\n'
            )
            lines: list[str] = []
            try:
                # (Re)opening and sending sit inside the try: over a dropped
                # mesh either one raises, and that must be a tool error.
                if self._shell is None or self._shell.returncode is not None:
                    await self._open_shell()
                assert self._shell is not None and self._shell.stdin is not None and self._shell.stdout is not None
                self._shell.stdin.write(script.encode())
                await self._shell.stdin.drain()
                deadline = asyncio.get_running_loop().time() + timeout
                while True:
                    remaining = deadline - asyncio.get_running_loop().time()
                    if remaining <= 0:
                        raise TimeoutError
                    try:
                        raw = await asyncio.wait_for(self._shell.stdout.readline(), timeout=remaining)
                    except ValueError:
                        # A line over _LINE_LIMIT: asyncio drops the buffered part and the
                        # rest arrives as the next line, so the stream stays in sync.
                        marker = f"[output line longer than {_LINE_LIMIT} bytes cut]\n"
                        if not lines or lines[-1] != marker:
                            lines.append(marker)
                        continue
                    if not raw:
                        raise EOFError("sandbox shell exited")
                    line = raw.decode("utf-8", "replace")
                    if line.startswith(sentinel):
                        _, code, cwd = line.rstrip("\n").split(" ", 2)
                        self._cwd = cwd
                        # Drop the newline the sentinel printf added, then
                        # trailing newlines as Claude Code's Bash tool does.
                        text = "".join(lines)
                        if text.endswith("\n"):
                            text = text[:-1]
                        text = text.rstrip("\n")
                        rc = int(code)
                        return _cap_bash_result(
                            ToolResult(output=text or None, error=None if rc == 0 else f"command exited with code {rc}")
                        )
                    lines.append(line)
            # Only kill here: reopening while the mesh is still down would leave
            # a dead shell for the next call. The next call reopens in _cwd.
            except TimeoutError:
                await self._kill_shell()
                return _cap_bash_result(
                    ToolResult(
                        output="".join(lines).rstrip("\n") or None,
                        error=f"command timed out after {timeout}s; the shell was restarted (cwd {self._cwd} kept)",
                    )
                )
            except (EOFError, OSError) as exc:  # OSError: BrokenPipeError, ConnectionResetError
                await self._kill_shell()
                return _cap_bash_result(
                    ToolResult(output="".join(lines).rstrip("\n") or None, error=f"sandbox shell reset: {exc}")
                )

    async def read_file(self, path: str, view_range: list[int] | None = None) -> ToolResult:
        """Numbered lines of a file (optionally a 1-based inclusive range), a directory
        listing, or - for an image - the bytes themselves as an ImageContent block.

        The image branch is what makes this tool a replacement for the harness's own
        file read rather than a downgrade of it: a screenshot a test wrote, a chart a
        script just plotted and a mockup in the repo are all things the model has to
        *see*, and no amount of shell gets a PNG into the conversation as pixels. The
        kind is decided on the sandbox by ``file --mime-type`` (one round trip, not
        two) and the bytes come back raw on the same channel; the base64 the model's
        API needs is applied here, at the edge, where it costs nothing.
        """
        quoted = shlex.quote(path)
        # Slice on the sandbox when a range is asked for. Reading the first
        # MAX_READ_BYTES and slicing here cannot reach a range that starts past
        # the cap — it would answer a request for lines 5000-5100 of a large
        # file with nothing but the truncation note — so the cap has to apply
        # to the requested lines rather than to the head of the file.
        first_line = max(1, view_range[0]) if view_range else 1
        if view_range and len(view_range) > 1 and view_range[1] != -1:
            slicer = f"sed -n {shlex.quote(f'{first_line},{max(first_line, view_range[1])}p')} -- {quoted}"
        elif view_range:
            slicer = f"sed -n {shlex.quote(f'{first_line},$p')} -- {quoted}"
        else:
            slicer = f"cat -- {quoted}"
        command = (
            f"if [ -d {quoted} ]; then echo {_DIR_MARKER}; ls -la -- {quoted}; "
            # The text branch pipes into `head`, whose exit status is the
            # pipeline's — so a missing or unreadable file would otherwise come
            # back as an empty success. Check before reading.
            f"elif [ ! -r {quoted} ]; then echo {shlex.quote(f'cannot read {path}')} >&2; exit 1; "
            # `file` is absent on a minimal image; treating that as text keeps the
            # common path working instead of failing the read outright.
            f"else mime=$(file -b --mime-type -- {quoted} 2>/dev/null || echo text/plain); "
            f'case "$mime" in '
            f"image/*) printf '%s\\n' {_IMG_MARKER}\"$mime\"; head -c {MAX_IMAGE_BYTES + 1} -- {quoted};; "
            f"*) {slicer} | head -c {MAX_READ_BYTES + 1};; "
            f"esac; fi"
        )
        rc, out, err = await self._exec(command)
        if rc != 0:
            return ToolResult(error=err.decode("utf-8", "replace").strip() or f"read failed with code {rc}")
        if out.startswith(_IMG_MARKER.encode()):
            header, _, data = out.partition(b"\n")
            media_type = header[len(_IMG_MARKER) :].decode("utf-8", "replace").strip()
            if len(data) > MAX_IMAGE_BYTES:
                return ToolResult(
                    error=f"{path} is larger than {MAX_IMAGE_BYTES} bytes; resize it on the sandbox first"
                )
            return ToolResult(
                output=f"{path} ({media_type}, {len(data)} bytes)",
                base64_image=base64.b64encode(data).decode("ascii"),
                media_type=media_type,
            )
        text = out.decode("utf-8", "replace")
        if text.startswith(_DIR_MARKER):
            return ToolResult(output=text[len(_DIR_MARKER) :].lstrip("\n"))
        truncated = len(out) > MAX_READ_BYTES
        if truncated:
            text = out[:MAX_READ_BYTES].decode("utf-8", "replace")
        lines = text.split("\n")
        if text.endswith("\n"):
            lines = lines[:-1]
        # `lines` is already the requested slice, so it is numbered from the
        # range's first line rather than from the top of the file.
        numbered = "\n".join(f"{first_line + i:6d}\t{line}" for i, line in enumerate(lines))
        if truncated:
            numbered += f"\n[truncated: only the first {MAX_READ_BYTES} bytes of {path} are shown]"
        return ToolResult(output=numbered)

    async def _search(self, command: str, empty: str, limit: int) -> ToolResult:
        """Run a ripgrep pipeline and cap what comes back.

        ripgrep exits 1 on "no matches", which is not a failure, so the result is
        read off stdout/stderr rather than the code: output means hits, silence
        with a complaint on stderr means ripgrep itself could not run.
        """
        rc, out, err = await self._exec(command)
        text = out.decode("utf-8", "replace").rstrip("\n")
        if not text:
            message = err.decode("utf-8", "replace").strip()
            if message:
                return ToolResult(error=message)
            return ToolResult(output=empty)
        lines = text.split("\n")
        if len(lines) > limit:
            lines = lines[:limit]
            lines.append(f"[truncated: first {limit} of more results; narrow the search]")
        return ToolResult(output="\n".join(lines))

    @staticmethod
    def _preferring_rg(rg: list[str], fallback: list[str], limit: int, *, sort: bool = False, rg_pipe: str = "") -> str:
        """``rg`` when the sandbox has it, POSIX tools when it does not.

        ripgrep is what these tools are shaped around - it honours .gitignore and
        is orders of magnitude faster on a repo - but it is not part of a base
        Ubuntu image, and a search tool that fails on a machine without it is
        worse than a slower one. The choice is made on the sandbox in the same
        round trip, so neither side has to remember which VM has what.
        """
        # "newest last" is the documented contract. Both branches emit
        # "<mtime> <path>", so the sort is numeric rather than lexicographic —
        # a name sort would drop exactly the recently-written files a glob is
        # usually looking for. It sorts newest *first* so the cap below keeps
        # them, then `tac` restores the documented order and `cut` drops the key.
        pipe = " | sort -rn" if sort else ""
        # `-f2-` on a space delimiter keeps paths containing spaces intact.
        post = " | cut -d' ' -f2- | tac" if sort else ""
        # One extra line so the cap can tell "exactly at the limit" from "there is more".
        rg_branch = shlex.join(rg) + (f" | {rg_pipe}" if rg_pipe else "")
        return (
            f"if command -v rg >/dev/null 2>&1; then {rg_branch}; "
            f"else {shlex.join(fallback)}; fi{pipe} | head -n {limit + 1}{post}"
        )

    async def grep(
        self,
        pattern: str,
        path: str | None = None,
        glob: str | None = None,
        *,
        context: int = 0,
        ignore_case: bool = False,
        files_with_matches: bool = False,
        limit: int = MAX_SEARCH_LINES,
    ) -> ToolResult:
        """Search file *contents* on the sandbox with ripgrep."""
        parts = ["rg", "--no-heading", "--color", "never"]
        if files_with_matches:
            parts.append("--files-with-matches")
        else:
            parts.append("--line-number")
        if ignore_case:
            parts.append("--ignore-case")
        if context and not files_with_matches:
            parts += ["--context", str(int(context))]
        if glob:
            parts += ["--glob", glob]
        parts += ["--", pattern, path or "."]

        fallback = ["grep", "--recursive", "--binary-files=without-match", "--color=never"]
        fallback.append("--files-with-matches" if files_with_matches else "--line-number")
        if ignore_case:
            fallback.append("--ignore-case")
        if context and not files_with_matches:
            fallback += ["--context", str(int(context))]
        if glob:
            # grep matches --include against the file name alone, so only the last
            # segment of a glob like '**/*.py' carries over; the rest is ripgrep's.
            fallback += ["--include", glob.rsplit("/", 1)[-1]]
        fallback += ["-e", pattern, path or "."]

        command = self._preferring_rg(parts, fallback, limit)
        return await self._search(command, f"no matches for {pattern!r}", limit)

    async def glob(self, pattern: str, path: str | None = None, *, limit: int = MAX_SEARCH_LINES) -> ToolResult:
        """List files on the sandbox whose *path* matches a glob, newest last."""
        parts = ["rg", "--files", "--glob", pattern, "--", path or "."]
        # find has no '**'; its '*' already crosses separators, so collapsing the
        # two and anchoring a bare pattern under the search root is equivalent.
        find_pattern = pattern.replace("**", "*")
        if not find_pattern.startswith("*"):
            find_pattern = f"*/{find_pattern}"
        # ripgrep has no mtime output, so its paths get a stat pass; find does it
        # in one go with -printf. Either way the shared sort pipe strips the key.
        fallback = ["find", path or ".", "-type", "f", "-path", find_pattern, "-printf", "%T@ %p\\n"]

        command = self._preferring_rg(
            # `2>/dev/null` and the `|| true`: a file listed by rg can be gone by
            # the time stat reaches it, and losing one racing path is far better
            # than failing the whole glob.
            parts,
            fallback,
            limit,
            sort=True,
            rg_pipe="xargs -r -d '\\n' stat -c '%Y %n' -- 2>/dev/null || true",
        )
        return await self._search(command, f"no files match {pattern!r}", limit)

    async def write_file(self, path: str, content: str) -> ToolResult:
        quoted = shlex.quote(path)
        rc, _out, err = await self._exec(
            f'mkdir -p -- "$(dirname -- {quoted})" && cat > {quoted}', stdin=content.encode()
        )
        if rc != 0:
            return ToolResult(error=err.decode("utf-8", "replace").strip() or f"write failed with code {rc}")
        return ToolResult(output=f"wrote {len(content.encode())} bytes to {path}")

    async def edit_file(self, path: str, old_str: str, new_str: str) -> ToolResult:
        """Replace the one occurrence of ``old_str``; refuses zero or several."""
        quoted = shlex.quote(path)
        rc, out, err = await self._exec(f"head -c {MAX_EDIT_BYTES + 1} -- {quoted}")
        if rc != 0:
            return ToolResult(error=err.decode("utf-8", "replace").strip() or f"read failed with code {rc}")
        if len(out) > MAX_EDIT_BYTES:
            return ToolResult(error=f"{path} is larger than {MAX_EDIT_BYTES} bytes; edit it with bash instead")
        text = out.decode("utf-8", "replace")
        count = text.count(old_str)
        if count != 1:
            return ToolResult(error=f"old_str occurs {count} times in {path}; it must occur exactly once")
        return await self.write_file(path, text.replace(old_str, new_str, 1))


__all__ = ["SshSandbox", "MAX_READ_BYTES", "MAX_EDIT_BYTES", "MAX_IMAGE_BYTES", "MAX_SEARCH_LINES"]
