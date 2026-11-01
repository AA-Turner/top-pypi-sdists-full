"""the read tool: numbered lines of a file the read rules allow (and `probe file preview`'s door)."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path
from probe.daemon.store.events import scrub


# ---------------------------------------------------------------------------
# read
# ---------------------------------------------------------------------------


async def read_file(deps: Deps, path: str, offset: int | None = None, limit: int | None = None) -> str:
    """Read a file: numbered lines (`offset`: the first line, 1-based; `limit`:
    how many, at most 2000), or with neither, a preview of a CSV/TSV (header,
    first rows, shape), JSON (what it holds, pretty-printed), Parquet or NumPy
    .npy/.npz file (dtype, shape, first values). Never a pickle (loading one runs
    code) or an image. The files a safe `cat` may read (`shell.read_refusal`),
    and the Probe skills folder, read-only (a `cat` of it is not safe-listed);
    in bypass mode any file but Probe's own key and state. Scrubbed and capped.

    For the tool list: a READ tool (not in `WRITE_TOOLS`). Everything it touches
    on the store runs on the event loop; only the file's own reading goes to a
    thread."""
    from probe.daemon.session import read_render as reader
    from probe.daemon.worker.bite.bite import skills_root

    stop = write_refusal(deps)
    if stop is not None:
        return stop
    path = (path or "").strip()
    if not path:
        return "give a path"
    if "\0" in path:
        return "not read: the path holds a NUL byte"
    skills = None if deps.reader else skills_root()
    path = _in_skills(path, deps.cwd, skills)
    refused = _read_refusal(deps, path, deps.cwd, skills)
    if refused is not None:
        reason, never = refused
        if never:
            return f"not read: {reason} This is refused in every mode."
        if deps.reader:
            return f"not read: {reason} The reader reads only what a safe `cat` may read in the working folders."
        if not (deps.bypass and deps.mode_known):
            # The shell's read programs reach further (`shell.classify`): a plain file outside runs at once there.
            return (f"not read: {reason} The read tool reads only what a safe `cat` may read in the working "
                    "folders. Outside them, `cat` through the shell runs at once for a plain file; a hidden, "
                    "credential-shaped or private one asks the researcher.")
    full = Path(str(deps.home) + path[1:]) if path == "~" or path.startswith("~/") else deps.cwd / path
    text = scrub(await asyncio.to_thread(reader.render, full, offset, limit))
    if _logs_lookups(deps):
        deps.store.log_lookup(bite=deps.bite_id, tool="read", query=path, result=text[:2000])
    return text


def _read_refusal(deps: Deps, path: str, cwd: Path, skills: Path | None) -> tuple[str, bool] | None:
    from probe.daemon import shell as sh

    return sh.read_refusal(path, workdirs=deps.workdirs, home=deps.home, cwd=cwd, protected=deps.protected,
                           write_dirs=deps.write_dirs, read_dirs=[skills] if skills is not None else [],
                           hidden=_off_check(deps, cwd))


def read_check(deps: Deps, path: str, cwd: Path) -> tuple[str | None, Path]:
    """`probe file preview`'s door (the `bash` tool set): the read tool's rules
    for `path` from `cwd` -- a safe `cat`'s inside the working folders, the
    skills folder read-only (not the reader's), anything but Probe's own key and
    state in bypass mode (not the reader's). `(refusal, the file)`."""
    from probe.daemon.shell import local_commands
    from probe.daemon.worker.bite.bite import skills_root

    path = (path or "").strip()
    expanded = Path(str(deps.home) + path[1:]) if path == "~" or path.startswith("~/") else cwd / path
    if not path or "\0" in path:
        return "not read: give a path", expanded
    skills = None if deps.reader else skills_root()
    refused = _read_refusal(deps, path, cwd, skills)
    if refused is None:
        return None, expanded
    reason, never = refused
    if never:
        return f"not read: {reason} This is refused in every mode.", expanded
    if deps.reader or not (deps.bypass and deps.mode_known):
        return local_commands.PREVIEW_REFUSED.format(reason=reason), expanded
    return None, expanded


def _in_skills(path: str, cwd: Path, skills: Path | None) -> str:
    """A path the skills name relative to their folder (`track-work/reference.md`)
    is read there, when it names no file in the session's folder: `path` made
    absolute. Anything else, `path` as given."""
    if skills is None or os.path.isabs(path) or path.startswith("~") or os.path.lexists(cwd / path):
        return path
    inside = os.path.normpath(skills / path)
    if not inside.startswith(str(skills).rstrip(os.sep) + os.sep) or not os.path.isfile(inside):
        return path
    return inside
from probe.daemon.agent.tools.probe_cli.config import _off_check  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.refusals import write_refusal  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.tools import Deps, _logs_lookups  # noqa: E402 -- pieces need each other; the front door loads this one first
