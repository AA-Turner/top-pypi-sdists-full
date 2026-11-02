"""the writer's and the reader's saved conversations: start, save after a run, end."""

from __future__ import annotations
import sqlite3
#: Ended conversations keep their message history this many deep (the rest only
#: their row): enough to look at what went wrong, never a growing file.
KEEP_ENDED_HISTORIES = 2


class ConversationsMixin:
    """Part of Store: its methods run with `self` the Store; compose() folds them into Store."""

    # -- the conversation (T15) --
    def live_conversation(self) -> sqlite3.Row | None:
        return self.db.execute("SELECT * FROM conversations WHERE ended IS NULL ORDER BY id DESC LIMIT 1").fetchone()

    def start_conversation(self, instructions: str, fingerprint: str | None = None) -> int:
        """A fresh conversation (any live one ends first): its instructions are fixed
        for its life, so the cached prefix every later run sends stays the same.
        `fingerprint`: what made it (`Worker._fingerprint`); a resume checks it."""
        live = self.live_conversation()
        if live is not None:
            self.end_conversation(live["id"], "replaced by a fresh start")
        current = self.db.execute("INSERT INTO conversations (started, instructions, fingerprint) VALUES (?, ?, ?)",
                              (self.clock(), instructions, fingerprint))
        return int(current.lastrowid)

    def set_conversation_instructions(self, conversation_id: int, instructions: str,
                                      fingerprint: str | None = None) -> None:
        """A conversation whose first run never finished starts again with today's facts."""
        self.db.execute("UPDATE conversations SET instructions = ?, fingerprint = ? WHERE id = ?",
                        (instructions, fingerprint, conversation_id))

    def save_conversation(self, conversation_id: int, messages: str, *, compactions: int = 0) -> None:
        """The history after a run that finished (its compactions counted)."""
        self.db.execute("UPDATE conversations SET messages = ?, updated = ?, runs = runs + 1, "
                        "compactions = compactions + ? WHERE id = ?",
                        (messages, self.clock(), int(compactions), conversation_id))

    def end_conversation(self, conversation_id: int, reason: str) -> None:
        """No run continues it: the next one starts fresh from disk. Only the last
        KEEP_ENDED_HISTORIES ended conversations keep their history."""
        self.db.execute("UPDATE conversations SET ended = ?, end_reason = ? WHERE id = ? AND ended IS NULL",
                        (self.clock(), reason[:500], conversation_id))
        self.db.execute("UPDATE conversations SET messages = NULL WHERE ended IS NOT NULL AND id NOT IN "
                        "(SELECT id FROM conversations WHERE ended IS NOT NULL ORDER BY id DESC LIMIT ?)",
                        (KEEP_ENDED_HISTORIES,))

    # -- the reader (daemon reads): its own tables, never the writer's ----------
    #: The reader's conversation lives in `read_conversations`, NOT a column on
    #: `conversations`: `live_conversation()` above picks any open row, so an older
    #: CLI opening this store would adopt the reader's conversation as the writer's.
    def live_read_conversation(self) -> sqlite3.Row | None:
        return self.db.execute("SELECT * FROM read_conversations WHERE ended IS NULL "
                               "ORDER BY id DESC LIMIT 1").fetchone()

    def start_read_conversation(self, instructions: str, fingerprint: str | None = None) -> int:
        live = self.live_read_conversation()
        if live is not None:
            self.end_read_conversation(live["id"], "replaced by a fresh start")
        current = self.db.execute("INSERT INTO read_conversations (started, instructions, fingerprint) VALUES (?, ?, ?)",
                              (self.clock(), instructions, fingerprint))
        return int(current.lastrowid)

    def save_read_conversation(self, conversation_id: int, messages: str, *, compactions: int = 0) -> None:
        self.db.execute("UPDATE read_conversations SET messages = ?, updated = ?, runs = runs + 1, "
                        "compactions = compactions + ? WHERE id = ?",
                        (messages, self.clock(), int(compactions), conversation_id))

    def end_read_conversation(self, conversation_id: int, reason: str) -> None:
        self.db.execute("UPDATE read_conversations SET ended = ?, end_reason = ? WHERE id = ? AND ended IS NULL",
                        (self.clock(), reason[:500], conversation_id))
        self.db.execute("UPDATE read_conversations SET messages = NULL WHERE ended IS NOT NULL AND id NOT IN "
                        "(SELECT id FROM read_conversations WHERE ended IS NOT NULL ORDER BY id DESC LIMIT ?)",
                        (KEEP_ENDED_HISTORIES,))
