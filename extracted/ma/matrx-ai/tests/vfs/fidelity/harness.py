from __future__ import annotations

import asyncio
import difflib
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import VfsCommandRunner, load_all
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv

# The fidelity harness compares VFS output (which mimics GNU coreutils byte-for-byte)
# against the OS's native binaries via subprocess. On Linux, /usr/bin/<name> is
# already GNU coreutils. On macOS the system binaries are BSD and produce different
# error wording, exit codes, and -A/-R formatting — so we resolve each command to
# the brew-installed `g`-prefixed equivalent. When neither is available, the suite
# is skip-marked (see conftest.py) rather than producing meaningless diffs.
_COREUTILS_NAMES: frozenset[str] = frozenset({
    "ls", "cat", "head", "tail", "cp", "mv", "rm", "rmdir", "mkdir",
    "find", "chmod", "chown", "stat", "wc", "cut", "tr", "sort", "uniq",
    "echo", "printf", "tar", "df", "du", "touch", "ln", "readlink", "realpath",
    "grep", "sed", "awk", "diff", "patch", "gzip", "file", "xargs",
})

_BREW_BIN_PATHS = ("/opt/homebrew/bin", "/usr/local/bin")
_REAL_PATH = "/usr/bin:/bin:/usr/sbin:" + ":".join(_BREW_BIN_PATHS)


def _resolve_gnu_binary(name: str) -> str | None:
    """Return absolute path to the GNU version of `name`, or None if unavailable.

    On Linux the system binary is already GNU coreutils. On macOS we look for the
    brew `coreutils` package's `g`-prefixed variants. We always probe by absolute
    path so that test PATH manipulation can't shadow the result.
    """
    if sys.platform.startswith("linux"):
        path = shutil.which(name, path="/usr/bin:/bin:/usr/sbin")
        if path:
            return path
        return None

    # macOS / *BSD: brew GNU coreutils ship as g-prefixed under /opt/homebrew or
    # /usr/local. Some commands (sed, awk, grep, find, gzip) come from separate
    # brew formulas (gnu-sed, gawk, grep, findutils, gzip) which also use the
    # g-prefix convention.
    g_path = shutil.which(f"g{name}", path=":".join(_BREW_BIN_PATHS))
    if g_path:
        return g_path
    return None


def gnu_coreutils_available() -> bool:
    """Cheap probe used by conftest to decide whether to run the fidelity suite."""
    return _resolve_gnu_binary("ls") is not None

# Used to scrub the host-side temp dir prefix from real-mode output.  Both
# stdout and stderr can leak the real path because GNU coreutils echo whatever
# argv we passed in.  We replace it with the empty string so the comparison is
# against the same logical path the virtual run sees ("/foo" vs "/foo").
_TIMESTAMP_RE = re.compile(
    rb"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+\s+(?:\d{2}:\d{2}|\d{4})"
)
# `ls -l` emits `drwxr-xr-x  1 user user  size <month> <day> <hh:mm> name`
# We strip the user/group/size/date columns down to mode + name to focus on
# what the VFS can actually reproduce.
_LS_LONG_RE = re.compile(
    rb"^([dl\-bcsp][rwxsStTl\-]{9})\.?\s+\d+\s+\S+\s+\S+\s+\d+\s+"
    rb"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+\s+"
    rb"(?:\d{2}:\d{2}|\d{4})\s+(.*)$",
    re.MULTILINE,
)
_LS_TOTAL_RE = re.compile(rb"^total\s+\d+\n", re.MULTILINE)


@dataclass(slots=True)
class CommandOutcome:
    stdout: bytes
    stderr: bytes
    exit_code: int


def argv_real(argv: list[str], tmpdir: str) -> list[str]:
    # Translate every absolute "/foo" arg to "<tmpdir>/foo".  Args starting with
    # "-" are options and pass through unchanged.  Args that are not absolute
    # (relative names, patterns) also pass through.
    out: list[str] = []
    for a in argv:
        if a.startswith("/") and not a.startswith("//"):
            # Strip leading slash, join with tmpdir.  Use rstrip so "/" maps to
            # the tmpdir itself.
            rel = a.lstrip("/")
            out.append(str(Path(tmpdir) / rel) if rel else tmpdir)
        else:
            out.append(a)
    return out


def argv_virtual(argv: list[str]) -> list[str]:
    return list(argv)


def _build_real_tree(tmpdir: Path, tree: dict[str, Any]) -> None:
    # Pre-create directories first so files can be placed inside them.
    dirs = [p for p, v in tree.items() if p.endswith("/") or v is None]
    files = [(p, v) for p, v in tree.items() if not (p.endswith("/") or v is None)]
    for p in sorted(dirs, key=len):
        rel = p.strip("/").strip()
        if not rel:
            continue
        (tmpdir / rel).mkdir(parents=True, exist_ok=True)
    for p, v in files:
        rel = p.lstrip("/")
        target = tmpdir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(v, bytes):
            target.write_bytes(v)
        elif isinstance(v, str):
            target.write_bytes(v.encode("utf-8"))
        else:
            target.write_bytes(b"")


async def _build_virtual_tree(vfs: MatrxAsyncFS, tree: dict[str, Any]) -> None:
    dirs = [p for p, v in tree.items() if p.endswith("/") or v is None]
    files = [(p, v) for p, v in tree.items() if not (p.endswith("/") or v is None)]
    for p in sorted(dirs, key=len):
        norm = p.rstrip("/")
        if not norm or norm == "/":
            continue
        await vfs._makedirs(norm, exist_ok=True)
    for p, v in files:
        parent = "/".join(p.split("/")[:-1])
        if parent and parent != "/":
            await vfs._makedirs(parent, exist_ok=True)
        if isinstance(v, bytes):
            data = v
        elif isinstance(v, str):
            data = v.encode("utf-8")
        else:
            data = b""
        await vfs._pipe_file(p, data)


class FidelityHarness:
    def __init__(self, tree: dict[str, Any]) -> None:
        self._tmpdir_obj = tempfile.TemporaryDirectory(prefix="vfs-fidelity-")
        self.tmpdir = Path(self._tmpdir_obj.name)
        self.tree = tree

        load_all()

        self.backend = MemoryBackend()
        self.workspace_id = "fidelity"
        self.vfs = MatrxAsyncFS(
            backend=self.backend, workspace_id=self.workspace_id, asynchronous=True
        )
        self.runner = VfsCommandRunner(self.vfs)
        self._built = False

    async def setup(self) -> None:
        if self._built:
            return
        await self.backend.ensure_workspace_root(self.workspace_id)
        _build_real_tree(self.tmpdir, self.tree)
        await _build_virtual_tree(self.vfs, self.tree)
        self._built = True

    def cleanup(self) -> None:
        try:
            self._tmpdir_obj.cleanup()
        except OSError:
            pass

    async def __aenter__(self) -> FidelityHarness:
        await self.setup()
        return self

    async def __aexit__(self, *exc: Any) -> None:
        self.cleanup()

    # ------------------------------------------------------------------
    # Runners
    # ------------------------------------------------------------------

    async def run_real(
        self,
        argv: list[str],
        cwd: str | None = None,
    ) -> CommandOutcome:
        translated = argv_real(argv, str(self.tmpdir))
        # Use basename argv[0] so error messages say "ls: ..." not "/usr/bin/ls: ..."
        run_cwd = str(self.tmpdir) if cwd is None else cwd
        # Run subprocess in a thread to keep the test loop free.
        return await asyncio.to_thread(self._run_real_sync, translated, run_cwd)

    def _run_real_sync(self, argv: list[str], cwd: str) -> CommandOutcome:
        # Route coreutils invocations through the GNU binary so output matches
        # our GNU-mimicry virtual implementation. On Linux the system binary
        # under /usr/bin IS GNU; on macOS we pick up brew's g-prefixed variants.
        #
        # Two platform quirks govern the diagnostic prefix coreutils print
        # ("rmdir: ...", "ls: ..."), and we must neutralise BOTH so the captured
        # output matches what the virtual side emits:
        #
        #   1. Linux GNU coreutils derive the prefix from the FULL argv[0] we
        #      pass. Handing them the absolute path (the historical harness bug)
        #      produced "/usr/bin/rmdir: ..." and made every error comparison
        #      fail in CI. Fix: keep argv[0] = the SHORT name and supply the
        #      resolved binary out-of-band via ``executable=`` (POSIX exec takes
        #      the program from ``executable`` while the child still sees the
        #      argv[0] we set).
        #
        #   2. brew's coreutils are compiled to ALWAYS report their g-prefixed
        #      name ("gls: ...") regardless of argv[0], so on macOS we still have
        #      to strip that leading "g" from the captured diagnostics.
        head = argv[0]
        executable: str | None = None
        strip_g_prefix = False
        if head in _COREUTILS_NAMES:
            resolved = _resolve_gnu_binary(head)
            if resolved is not None:
                executable = resolved
                strip_g_prefix = Path(resolved).name == f"g{head}"
        try:
            res = subprocess.run(
                argv,
                executable=executable,
                cwd=cwd,
                capture_output=True,
                timeout=10,
                env={"LC_ALL": "C", "LANG": "C", "PATH": _REAL_PATH},
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            return CommandOutcome(
                stdout=exc.stdout or b"",
                stderr=(exc.stderr or b"") + b"timeout\n",
                exit_code=124,
            )
        stdout, stderr = res.stdout, res.stderr
        if strip_g_prefix:
            # Rewrite the brew "g<name>:" diagnostic label to the canonical short
            # name so both sides compare equal.
            prefix_re = re.compile(rb"(?m)^g(" + head.encode() + rb"):")
            stdout = prefix_re.sub(rb"\1:", stdout)
            stderr = prefix_re.sub(rb"\1:", stderr)
        return CommandOutcome(stdout=stdout, stderr=stderr, exit_code=res.returncode)

    async def run_virtual(
        self,
        argv: list[str],
        cwd: str | None = None,
    ) -> CommandOutcome:
        translated = argv_virtual(argv)
        env = ShellEnv(cwd=cwd or "/")
        result = await self.runner.run(translated, env, b"", env.cwd)
        return CommandOutcome(
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.exit_code,
        )

    # ------------------------------------------------------------------
    # Normalization helpers
    # ------------------------------------------------------------------

    def normalize_real(self, data: bytes) -> bytes:
        # Strip the temp dir prefix so paths read identically to the virtual side.
        # Substitution rules:
        #   - "<tmpdir>/<rest>" -> "/<rest>"      (preserves the leading slash)
        #   - "<tmpdir>"        -> "/"            (the tmpdir alone IS the root)
        # We do these in two steps: first replace "<tmpdir>/" with "/", then
        # replace the bare tmpdir with "/".
        prefix = str(self.tmpdir).encode()
        out = data.replace(prefix + b"/", b"/")
        out = out.replace(prefix, b"/")
        return out

    def diff_outcomes(
        self,
        real: CommandOutcome,
        virt: CommandOutcome,
        *,
        normalize_paths: bool = True,
        strip_timestamps: bool = False,
    ) -> list[str]:
        real_out = self.normalize_real(real.stdout) if normalize_paths else real.stdout
        real_err = self.normalize_real(real.stderr) if normalize_paths else real.stderr
        virt_out = virt.stdout
        virt_err = virt.stderr
        if strip_timestamps:
            real_out = strip_ls_timestamps(real_out)
            virt_out = strip_ls_timestamps(virt_out)
        diffs: list[str] = []
        if real.exit_code != virt.exit_code:
            diffs.append(f"exit: real={real.exit_code} virtual={virt.exit_code}")
        if real_out != virt_out:
            diffs.append("stdout differs:\n" + _udiff(real_out, virt_out, "stdout"))
        if real_err != virt_err:
            diffs.append("stderr differs:\n" + _udiff(real_err, virt_err, "stderr"))
        return diffs


def _udiff(a: bytes, b: bytes, label: str) -> str:
    sa = a.decode("utf-8", errors="replace").splitlines(keepends=True)
    sb = b.decode("utf-8", errors="replace").splitlines(keepends=True)
    return "".join(
        difflib.unified_diff(sa, sb, fromfile=f"real.{label}", tofile=f"virtual.{label}")
    )


def strip_ls_timestamps(text: bytes) -> bytes:
    # Collapse host-only owner/group/allocated-size/date fields while retaining
    # the permission bits and displayed name. The host temp root's `.` / `..`
    # modes are also environmental, so only those two modes are normalized.
    out = _LS_TOTAL_RE.sub(b"total *\n", text)
    out = _LS_LONG_RE.sub(_normalize_ls_long_line, out)
    out = _TIMESTAMP_RE.sub(b"<DATE>", out)
    return out


def _normalize_ls_long_line(match: re.Match[bytes]) -> bytes:
    mode = match.group(1)
    name = match.group(2)
    if name in {b".", b".."}:
        mode = b"d<MODE>"
    return mode + b" " + name


def assert_outcomes_equal(
    harness: FidelityHarness,
    real: CommandOutcome,
    virt: CommandOutcome,
    argv: list[str],
    *,
    normalize_paths: bool = True,
    strip_timestamps: bool = False,
) -> None:
    diffs = harness.diff_outcomes(
        real, virt, normalize_paths=normalize_paths, strip_timestamps=strip_timestamps
    )
    if not diffs:
        return
    msg_lines = [
        f"COMMAND: {' '.join(argv)}",
        f"REAL:    exit={real.exit_code} stdout={real.stdout!r} stderr={real.stderr!r}",
        f"VIRTUAL: exit={virt.exit_code} stdout={virt.stdout!r} stderr={virt.stderr!r}",
        "DIFFERENCES:",
        *diffs,
    ]
    raise AssertionError("\n".join(msg_lines))
