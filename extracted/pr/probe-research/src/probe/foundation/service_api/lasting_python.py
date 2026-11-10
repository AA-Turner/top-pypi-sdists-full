"""Which interpreter a process that outlives its command may run on: never one a launcher deletes (`uvx`,
`uv run --with`). Not in the tap's copies (`start.py` is): only the service and the CLI ask."""

from __future__ import annotations

import json
import os
import sys

from . import paths
from .start import _is_runnable, runtime_python

#: uv's run and build environments, folders of its cache root (which holds CACHEDIR.TAG).
_UV_CACHE_FOLDERS = ("archive-v0", "builds-v0")
#: pipx's `pipx run` cache: the old `<PIPX_HOME>/.cache`, then the platform cache (Linux, macOS).
_PIPX_CACHES = ("/pipx/.cache/", "/.cache/pipx/", "/Library/Caches/pipx/")


def find_lasting_python() -> str | None:
    """The CLI's interpreter for a process that outlives the command starting it (an import's worker): the
    recorded one (`runtime_python`, else this one), unless a launcher may delete it (`is_launcher_copy`),
    then the machine's installed CLI's (its own runtime.json, else the uv tool env's); None when none is."""
    candidates = (runtime_python() or sys.executable, _read_machine_python(), str(paths.fallback_python()))
    for candidate in candidates:
        if candidate and _is_runnable(candidate) and not is_launcher_copy(candidate):
            return candidate
    return None


def _read_machine_python() -> str | None:
    """The machine's install's interpreter as the machine root's runtime.json records it, read from another
    copy's own root (`<machine root>/copies/<key>`, D13: a pipx install, a moved UV_TOOL_DIR); None elsewhere."""
    if not paths.is_copy_root():
        return None
    try:
        data = json.loads((paths.root_dir().parent.parent / paths.RUNTIME_NAME).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict) or data.get("machine") not in (None, paths.machine_key()):
        return None
    return data["python"] if isinstance(data.get("python"), str) else None


def is_launcher_copy(path: str | os.PathLike) -> bool:
    """Is `path` in a launcher's temporary environment, which the launcher may delete: uv's run and
    build environments (`<cache>/archive-v0/<hash>`, `<cache>/builds-v0/.tmp*`, `uv tool run` / `uvx`)
    or pipx's cache. Never an interpreter to name in anything that outlives this run. Narrower than
    `detect_install`'s EPHEMERAL: a tool env a person put under `~/.cache/uv` (`UV_TOOL_DIR`) is not
    one, nor a folder of their own that happens to be called `archive-v0` (no uv cache around it)."""
    spelled = str(path).replace(os.sep, "/")
    for mark in _PIPX_CACHES:
        at = spelled.find(mark)
        # `<cache>/<hash>/...` is `pipx run`'s; `<cache>/venvs/...` is a PIPX_HOME someone put there.
        if at >= 0 and not spelled[at + len(mark):].startswith("venvs/"):
            return True
    parts = spelled.split("/")
    for at, part in enumerate(parts[1:], start=1):
        # A pipx home anywhere (`PIPX_HOME`): `<home>/.cache/<hash>` is `pipx run`'s, beside `venvs`.
        if part == ".cache" and at + 1 < len(parts) and parts[at + 1] != "venvs":
            home = "/".join(parts[:at]) or "/"
            if os.path.isdir(os.path.join(home, "venvs")) and os.path.isdir(os.path.join(home, "shared")):
                return True
        if part in _UV_CACHE_FOLDERS:
            root = "/".join(parts[:at]) or "/"
            # uv marks its cache root; one gone already is no interpreter to name either.
            if os.path.isfile(os.path.join(root, "CACHEDIR.TAG")) or not os.path.isdir(root):
                return True
    return False
