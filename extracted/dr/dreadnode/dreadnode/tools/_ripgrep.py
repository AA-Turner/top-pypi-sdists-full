"""
Ripgrep utility layer — find the rg binary, with detection caching.

Used by glob.py and grep.py. If rg is not available on the system,
callers fall back to pure-Python implementations.
"""

import asyncio
import shutil

_rg_path: str | None = None


async def find_rg() -> str | None:
    """Return the path to the rg binary, or None if not installed.

    Positive results are cached; negatives re-check on every call so a
    later install is picked up without restarting the process.
    """
    global _rg_path  # noqa: PLW0603
    if _rg_path is not None:
        return _rg_path

    # shutil.which is synchronous but fast (just PATH scan).
    path = shutil.which("rg")
    if path is not None:
        _rg_path = path
    return path


async def run_rg(args: list[str], cwd: str) -> tuple[int, str, str]:
    """Run rg with the given args and return (exit_code, stdout, stderr).

    Raises FileNotFoundError if rg is not available.
    """
    rg = await find_rg()
    if rg is None:
        raise FileNotFoundError("ripgrep (rg) not found on PATH")

    proc = await asyncio.create_subprocess_exec(
        rg,
        *args,
        cwd=cwd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout_bytes, stderr_bytes = await proc.communicate()
    return (
        proc.returncode or 0,
        stdout_bytes.decode("utf-8", errors="replace"),
        stderr_bytes.decode("utf-8", errors="replace"),
    )
