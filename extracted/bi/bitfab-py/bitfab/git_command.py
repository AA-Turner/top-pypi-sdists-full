from __future__ import annotations

import os
import subprocess


def run_git(
    cwd: str,
    args: list[str],
    timeout: float,
    env: dict[str, str] | None = None,
) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            env={**os.environ, **env} if env else None,
        )
    except Exception:
        return None
    return result.stdout if result.returncode == 0 else None
