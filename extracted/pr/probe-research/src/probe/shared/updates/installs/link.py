"""the ToolLink interface (make/drop/swap the tool-path link, find an env's python) and the per-OS pick."""

from __future__ import annotations

import contextlib
import os
from pathlib import Path


def is_link(path: Path) -> bool:
    """A symlink, or on Windows a junction (how the tool path is switched there:
    a directory symlink needs Developer Mode or an administrator)."""
    if path.is_symlink():
        return True
    if os.name == "nt":
        is_junction = getattr(path, "is_junction", None)  # Python 3.12
        if is_junction is not None:
            return is_junction()
        try:
            os.readlink(path)
            return True
        except (OSError, ValueError):
            return False
    return False


def _make_link(target: Path, link: Path) -> None:
    if os.name == "nt":
        import _winapi

        _winapi.CreateJunction(str(target), str(link))
    else:
        os.symlink(target, link, target_is_directory=True)


def _drop_link(link: Path) -> None:
    """Remove the link itself, never what it names (rmdir on a junction)."""
    if os.name == "nt" and not link.is_symlink():
        os.rmdir(link)
    else:
        link.unlink()


def _swap_link(link: Path, env: Path) -> None:
    """Put `link` at `env`: one rename on POSIX. Windows cannot rename onto a
    folder (a junction is one), so the old link moves aside first, for the
    moment between two renames."""
    if os.name != "nt" or not (env.exists() or is_link(env)):
        os.replace(link, env)
        return
    aside = env.with_name(f".{env.name}.old-{os.getpid()}")
    os.rename(env, aside)
    try:
        os.rename(link, env)
    except OSError:
        os.rename(aside, env)
        raise
    with contextlib.suppress(OSError):
        _drop_link(aside)


def env_python(env: Path) -> Path:
    if os.name == "nt":
        return env / "Scripts" / "python.exe"
    return env / "bin" / "python"
