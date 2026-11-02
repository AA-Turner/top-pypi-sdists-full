"""Codex's TranscriptLocator: sessions/ under CODEX_HOME."""

from __future__ import annotations
from pathlib import Path


def codex_root() -> Path:
    """Codex's default. `CODEX_HOME` is Codex's OWN relocation knob, and this
    package already honours it in `codex_config` and `agent_rules` -- resolving
    it here too is what keeps the Codex half from having the silent-zero bug the
    Claude half just lost."""
    override = _env_path(_ROOT_ENV[CODEX])
    if override:
        return override
    home = _env_path("CODEX_HOME")
    return (home / "sessions") if home else Path.home() / ".codex" / "sessions"
from probe.cli.imports.transcripts.roots import CODEX, _ROOT_ENV  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.harness.transcripts import _env_path  # noqa: E402 -- pieces need each other; the front door loads this one first
