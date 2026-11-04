"""The per-run Claude Code session record shared by the claude-code agent (writer)
and the worlds that resume it (readers, e.g. structured-execution retries).

A run writes ``<session_record_dir>/session.json`` (a ``SessionRecord``) plus the
transcript ``<session_id>.jsonl``; a later run resumes that exact session with
``resume_session_id``, on the same or another VM.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

#: Directory name for session records, wherever they are kept. Listed in
#: ``WorkspaceMarker.DEFAULT_DVCIGNORE`` so workspace checkpoints never pick it up.
SESSION_RECORD_DIR_NAME = ".plato-agent-sessions"

#: Where a run records its session unless the caller points it elsewhere: the
#: agent VM's home, outside any workspace. ``~`` is expanded on the agent VM.
DEFAULT_SESSION_RECORD_DIR = f"~/{SESSION_RECORD_DIR_NAME}"

#: The record file inside a session record directory.
SESSION_RECORD_FILE = "session.json"


class SessionRecord(BaseModel):
    """``<session_record_dir>/session.json``: the Claude Code session a run used,
    so a later run can resume it with ``resume_session_id``. Readers ignore fields
    they don't know, so the writer can add fields without breaking older readers."""

    session_id: str = Field(min_length=1)
    cwd: str
    transcript: str | None = Field(
        description="The transcript's file name in session_record_dir, None when the run left none"
    )
    num_turns: int
    context_tokens: int | None = Field(description="Context size of the run's last main-agent turn, in tokens")
    resumed_from: str | None = Field(description="The session this run resumed (resume_session_id), if any")
    recorded_at: datetime


__all__ = ["DEFAULT_SESSION_RECORD_DIR", "SESSION_RECORD_DIR_NAME", "SESSION_RECORD_FILE", "SessionRecord"]
