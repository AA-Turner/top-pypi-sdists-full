"""Per-folder chat history for the Bingo IDE.

Each workspace folder keeps its own conversation record on disk, so reopening
the IDE in that folder restores the chat and the model keeps its memory —
independent of which model is connected. Different folders never share a record.
"""
from __future__ import annotations

import json
from pathlib import Path

from ..core.local_state import workspace_state_dir

_MAX_TURNS = 400     # cap on-disk growth (user + assistant lines)
_MEMORY_TURNS = 24   # recent turns fed back to the model as context

_VALID_ROLES = ("user", "assistant")


class ChatHistory:
    """A folder-scoped list of {role, content} conversation turns."""

    def __init__(self, root: Path | str) -> None:
        self._root = Path(root)
        self.turns: list[dict] = []
        try:
            self._path: Path | None = (
                workspace_state_dir(self._root) / "chat-history.json"
            )
        except Exception:
            self._path = None
        self._load()

    def _load(self) -> None:
        if not self._path or not self._path.exists():
            return
        try:
            data = json.loads(self._path.read_text(encoding="utf-8"))
        except Exception:
            return
        turns = data.get("turns") if isinstance(data, dict) else None
        if not isinstance(turns, list):
            return
        for t in turns:
            if (isinstance(t, dict) and t.get("role") in _VALID_ROLES
                    and isinstance(t.get("content"), str) and t["content"]):
                self.turns.append({"role": t["role"], "content": t["content"]})

    def _save(self) -> None:
        if not self._path:
            return
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self._path.with_suffix(".json.tmp")
            payload = {"root": str(self._root), "turns": self.turns}
            tmp.write_text(json.dumps(payload, ensure_ascii=False),
                           encoding="utf-8")
            tmp.replace(self._path)
        except Exception:
            pass  # history is best-effort; never break the UI on a write error

    def add(self, role: str, content: str) -> None:
        """Append a turn and persist. Roles outside user/assistant are ignored."""
        if role not in _VALID_ROLES or not content:
            return
        self.turns.append({"role": role, "content": content})
        if len(self.turns) > _MAX_TURNS:
            self.turns = self.turns[-_MAX_TURNS:]
        self._save()

    def context(self, limit: int = _MEMORY_TURNS) -> list[dict]:
        """Return the most recent turns to feed the model as prior context."""
        return list(self.turns[-limit:]) if limit > 0 else list(self.turns)

    def clear(self) -> None:
        """Forget this folder's conversation, on disk and in memory."""
        self.turns = []
        if self._path:
            try:
                self._path.unlink(missing_ok=True)
            except Exception:
                pass
