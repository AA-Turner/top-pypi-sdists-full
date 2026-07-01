"""
cvc.operations.handoff — Cross-session / cross-workspace handoff.

A :class:`HandoffPackage` is a compact, portable snapshot of what a CVC
workspace recently knew about — enough that a fresh runtime in a
*different* workspace (or the same one on another machine) can start
its next chat already primed with the outgoing intent.

Goal
----
Typing ``cvc handoff export`` at the end of a session produces a single
small JSON file.  Running ``cvc handoff import <file>`` in the next
workspace makes the incoming runtime inject a synthetic "handoff"
system message (and record the event in the receiving scratchpad) so
the next turn carries the prior session's outcomes into the new context
*without* polluting the Merkle DAG.

This is strictly additive — no Merkle writes, no commits — so handoff is
safe between unrelated workspaces (e.g., library → downstream consumer).

Schema
------
See :class:`HandoffPackage` fields.  Version 1 is stable.
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger("cvc.operations.handoff")

SCHEMA_VERSION = 1
DEFAULT_FILENAME = ".cvc-handoff.json"


class HandoffTurn(BaseModel):
    """One compressed user-turn + engram fingerprint from the source."""

    query: str = Field(default="", max_length=400)
    engram_hash: str | None = None
    engram_tokens: int | None = None
    noeme_count: int | None = None
    provider: str = ""
    model: str = ""
    ts: float = 0.0


class HandoffPackage(BaseModel):
    """
    Portable snapshot of a CVC workspace session.

    Small by design — a few KB max.  Tailored to be rendered as a system
    message at the start of the *next* chat.
    """

    schema_version: int = SCHEMA_VERSION
    source_workspace: str = ""
    source_branch: str | None = None
    created_at: float = Field(default_factory=time.time)
    brief: str = Field(default="", max_length=2000)
    recent_turns: list[HandoffTurn] = Field(default_factory=list)
    recent_commits: list[str] = Field(default_factory=list)
    engram_hashes: list[str] = Field(default_factory=list)
    stats: dict[str, Any] = Field(default_factory=dict)

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render_system_message(self) -> str:
        """
        Render the package as a single system-message string.

        The injector treats this as an extra preamble, placed after the
        dev system prompt and before the Engram.  It is intentionally
        terse — a brief + a bulletted recent-turn summary — so it does
        not dominate the context.
        """
        lines = ["# CVC Handoff (incoming)"]
        if self.source_workspace:
            lines.append(f"# source: {self.source_workspace}")
        if self.source_branch:
            lines.append(f"# branch: {self.source_branch}")
        lines.append(f"# turns: {len(self.recent_turns)}")
        if self.brief.strip():
            lines.append("")
            lines.append(self.brief.strip())
        if self.recent_turns:
            lines.append("")
            lines.append("## recent intent")
            for t in self.recent_turns[-10:]:
                q = (t.query or "").strip().replace("\n", " ")
                if len(q) > 200:
                    q = q[:199] + "…"
                lines.append(f"- {q}")
        if self.recent_commits:
            lines.append("")
            lines.append("## recent commits")
            for c in self.recent_commits[-10:]:
                lines.append(f"- {c}")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # I/O
    # ------------------------------------------------------------------

    def to_json(self) -> str:
        return self.model_dump_json(indent=2, exclude_none=False)

    def write_to(self, path: Path) -> Path:
        """Serialise to *path*.  Directory is created if missing."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.to_json(), encoding="utf-8")
        return path

    @classmethod
    def read_from(cls, path: Path) -> "HandoffPackage":
        """
        Parse a handoff JSON file.

        Raises :class:`ValueError` on schema mismatch so callers can show
        a friendly error.  Unknown fields from a *newer* producer are
        ignored (forward-compatibility).
        """
        raw = Path(path).read_text(encoding="utf-8")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"handoff file is not valid JSON: {exc}") from exc
        version = int(data.get("schema_version", 0) or 0)
        if version > SCHEMA_VERSION:
            # Forward-compatible: warn, but try to parse.
            logger.warning(
                "handoff schema v%d is newer than runtime v%d — attempting to parse anyway",
                version,
                SCHEMA_VERSION,
            )
        if version < 1:
            raise ValueError(
                f"handoff schema v{version} is not supported (runtime expects v{SCHEMA_VERSION})"
            )
        return cls.model_validate(data)
