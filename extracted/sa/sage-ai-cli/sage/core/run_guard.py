"""T6 — Run guard.

Refuses to execute install/destructive commands after a write to the
relevant manifest just got validator-rejected. Fixes the Novellia class
of bug where Sage rejected a poison `package.json` but then ran
`npm install` on whatever junk was already on disk.

State is per-session; cleared by a clean write to the same file.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

__all__ = ["RunGuard", "RunDecision"]


# Manifest → install command patterns that should be blocked when the
# manifest was just rejected.
_MANIFEST_INSTALL_RULES = (
    ("package.json",   re.compile(r"\b(?:npm|yarn|pnpm|bun)\s+(?:i|install|add|ci)\b", re.IGNORECASE)),
    ("requirements.txt", re.compile(r"\bpip(?:3)?\s+install\s+(?:.*-r\s+requirements\.txt|.*requirements)", re.IGNORECASE)),
    ("requirements.txt", re.compile(r"\bpip(?:3)?\s+install\b", re.IGNORECASE)),
    ("pyproject.toml", re.compile(r"\b(?:pip\s+install\s+(?:-e\s+)?\.|poetry\s+install|uv\s+sync|uv\s+pip\s+install)", re.IGNORECASE)),
    ("Cargo.toml",     re.compile(r"\bcargo\s+(?:build|update|fetch)\b", re.IGNORECASE)),
    ("go.mod",         re.compile(r"\bgo\s+(?:get|mod\s+download|install)\b", re.IGNORECASE)),
    ("Gemfile",        re.compile(r"\bbundle\s+install\b", re.IGNORECASE)),
)

# Always-dangerous patterns when ANY recent rejection happened
_DESTRUCTIVE_PATTERNS = (
    re.compile(r"\brm\s+-(?:r|R|f|rf|fr|Rf|fR)\b"),
    re.compile(r"\brm\s+--recursive\b"),
    re.compile(r"\bgit\s+reset\s+--hard\b"),
    re.compile(r"\bgit\s+clean\s+-(?:f|d|fd|df)\b"),
    re.compile(r"\bgit\s+checkout\s+(?:--|\.)"),
    re.compile(r":\(\)\s*\{\s*:.*\}"),  # fork bomb signature
    re.compile(r"\bdd\s+if=.*of=/dev/"),
)


@dataclass
class RunDecision:
    allowed: bool
    reason: str = ""


@dataclass
class RunGuard:
    """Tracks recent validator rejections and decides if subsequent RUN:
    commands are safe to execute.

    Lifecycle:
      - record_rejection(filepath, reason): mark the file as poisoned
      - record_clean_write(filepath):       clear the poison
      - allow(cmd): return RunDecision(allowed=bool, reason=str)
    """
    rejected: dict[str, str] = field(default_factory=dict)

    def record_rejection(self, filepath: str, reason: str) -> None:
        # Normalize basename so subdir paths still match (e.g. ./package.json,
        # frontend/package.json all map to the same manifest type)
        from pathlib import Path
        key = Path(filepath).name
        self.rejected[key] = reason

    def record_clean_write(self, filepath: str) -> None:
        from pathlib import Path
        key = Path(filepath).name
        self.rejected.pop(key, None)

    def allow(self, command: str) -> RunDecision:
        """Decide whether `command` is safe given current rejection state."""
        if not self.rejected:
            return RunDecision(allowed=True)

        # Check manifest-install rules
        for manifest, pattern in _MANIFEST_INSTALL_RULES:
            if manifest in self.rejected and pattern.search(command):
                return RunDecision(
                    allowed=False,
                    reason=(f"BLOCKED: {manifest} was rejected ({self.rejected[manifest]}); "
                            f"refusing {command!r} until a clean write replaces it"),
                )

        # Destructive commands are extra-suspicious when any rejection is fresh
        for pattern in _DESTRUCTIVE_PATTERNS:
            if pattern.search(command):
                rejected_files = ", ".join(self.rejected.keys())
                return RunDecision(
                    allowed=False,
                    reason=(f"BLOCKED: destructive command {command!r} while "
                            f"{rejected_files} have unresolved rejections"),
                )

        return RunDecision(allowed=True)
