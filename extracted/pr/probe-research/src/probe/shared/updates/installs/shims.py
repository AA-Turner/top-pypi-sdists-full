"""uv receipts and the public probe* scripts on PATH for each version env."""

from __future__ import annotations

import contextlib
import os
import re
from pathlib import Path


RECEIPT = "uv-receipt.toml"
_INSTALL_PATH = re.compile(r'install-path\s*=\s*"([^"]+)"')


def _receipt_bins(env: Path) -> list[Path]:
    try:
        text = (env / RECEIPT).read_text(encoding="utf-8")
    except OSError:
        return []
    return [Path(m.group(1)).parent for m in _INSTALL_PATH.finditer(text)]


def bin_dir(tools: Path | None = None) -> Path:
    """Where `probe` is on PATH (`~/.local/bin`, as uv chose it for this
    machine): the record's, else the tool path's own receipt (the folder uv
    made), else uv's rule."""
    tools = tools or tool_dir()
    saved = record(tools).get("bin")
    if isinstance(saved, str) and saved:
        return Path(saved)
    versions = versions_root(tools)
    for found in _receipt_bins(tool_env(tools)):
        if versions not in found.parents:
            return found
    for name in ("UV_TOOL_BIN_DIR", "XDG_BIN_HOME"):
        if os.environ.get(name):
            return Path(os.environ[name])
    if os.environ.get("XDG_DATA_HOME"):
        return Path(os.environ["XDG_DATA_HOME"]).parent / "bin"
    return Path.home() / ".local" / "bin"


def fix_receipt(env: Path, bins: Path) -> bool:
    """A version env's uv receipt names its scripts where uv put them
    (`probe-versions/<v>/.bin`, which nothing runs). uv reads the receipt of
    whatever the tool path names, and a plain `uv tool install` (what
    `npx probe-research` runs on a stale CLI) then finds `~/.local/bin/probe`
    "not its own", deletes the tool path and fails. Point the receipt at the
    real scripts folder instead. True when it changed. Never raises."""
    path = env / RECEIPT
    try:
        text = path.read_text(encoding="utf-8")
        old = f'"{env.parent / ".bin"}/'
        if old not in text:
            return False
        tmp = path.with_name(f"{RECEIPT}.{os.getpid()}.tmp")
        tmp.write_text(text.replace(old, f'"{bins}/'), encoding="utf-8")
        os.replace(tmp, path)
        return True
    except OSError:
        return False


def entrypoints(env: Path) -> list[str]:
    """The scripts uv put on PATH for `env` (its receipt's `install-path`s),
    by name; `probe` when the receipt says none."""
    names = []
    try:
        text = (env / RECEIPT).read_text(encoding="utf-8")
    except OSError:
        text = ""
    for found in _INSTALL_PATH.finditer(text):
        name = Path(found.group(1)).name
        if name and name not in names:
            names.append(name)
    return names or ["probe"]


def _ours(link_text: str, tools: Path) -> bool:
    """Is a shim's link one of Probe's to put right: into the tool path or the
    versions folder, or to nothing at all?"""
    target = Path(link_text)
    if not target.is_absolute():
        return False
    for root in (tool_env(tools), versions_root(tools)):
        if target == root or root in target.parents:
            return True
    return not target.exists()


def ensure_shims(tools: Path | None = None) -> tuple[list[str], list[str]]:
    """The public scripts (`~/.local/bin/probe*`, `bin_dir`) for every
    entrypoint the tool path's receipt names, each a link through the tool
    path (so it follows every switch), as uv makes them (R-T1): an install
    into a version folder fills only that folder's `.bin`. A missing one is
    made; one of ours that names a version env or nothing is put right; a
    file or a link that is someone else's is left, and named. Returns
    `(what it did, what is in the way)`. Never raises."""
    tools = tools or tool_dir()
    made: list[str] = []
    blocked: list[str] = []
    env = tool_env(tools)
    try:
        bins = bin_dir(tools)
        names = entrypoints(env)
    except OSError as exc:
        return [], [f"the scripts folder could not be read: {exc}"]
    for name in names:
        want = env / "bin" / name
        if not (want.exists() or want.is_symlink()):
            continue
        shim = bins / name
        try:
            if shim.is_symlink():
                current = os.readlink(shim)
                if Path(current) == want:
                    continue
                if not _ours(current, tools):
                    blocked.append(f"{shim} names {current}, not Probe's {want}")
                    continue
            elif shim.exists():
                blocked.append(f"{shim} is a file Probe did not make")
                continue
            bins.mkdir(parents=True, exist_ok=True)
            tmp = bins / f".{name}.probe-{os.getpid()}"
            with contextlib.suppress(FileNotFoundError):
                tmp.unlink()
            os.symlink(want, tmp)
            os.replace(tmp, shim)
            made.append(f"{shim} -> {want}")
        except OSError as exc:
            blocked.append(f"{shim}: {exc}")
    return made, blocked
from probe.shared.updates.installs.active_record import record  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.updates.installs.layout import tool_dir, tool_env, versions_root  # noqa: E402 -- pieces need each other; the front door loads this one first
