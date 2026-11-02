"""Codex headless: exec --json, sandbox args, the features it lists (hooks off)."""

from __future__ import annotations
import re
import subprocess
from functools import lru_cache


@lru_cache(maxsize=8)
def codex_features(binary: str) -> frozenset[str] | None:
    """Feature names `codex features list` reports, or None if it would not say.

    Unlike `supported_flags`, unknown here means "do not pass": a feature name
    Codex does not know is an error, not an ignored option.
    """
    try:
        done = subprocess.run(
            [binary, "features", "list"],
            capture_output=True,
            text=True,
            timeout=HELP_TIMEOUT_S,
            stdin=subprocess.DEVNULL,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if done.returncode != 0:
        return None
    names = {line.split()[0] for line in (done.stdout or "").splitlines()
             if line.strip() and re.match(r"[a-z][a-z0-9_]*\s", line)}
    return frozenset(names) or None
from probe.cli.imports.folder.agents.flags import HELP_TIMEOUT_S  # noqa: E402 -- an import cycle: bound once this module's names exist
