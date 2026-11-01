"""the reader's own tables: asks it took, messages it wrote, turns, run alerts handed to the mailbox."""

from __future__ import annotations
import sqlite3


class ReaderTablesMixin:
    """Part of Store: its methods run with `self` the Store; compose() folds them into Store."""

    def add_read_ask(self, ask_id: str, question: str, asked_at: float, wait: bool) -> bool:
        """Store an ask the mailbox handed over. False: already stored."""
        cur = self.db.execute("INSERT OR IGNORE INTO read_asks (id, question, asked_at, wait, taken_at) "
                              "VALUES (?, ?, ?, ?, ?)", (ask_id, question, asked_at, int(wait), self.clock()))
        return cur.rowcount > 0

    def waiting_read_asks(self) -> list[sqlite3.Row]:
        return list(self.db.execute("SELECT * FROM read_asks WHERE state = 'waiting' ORDER BY asked_at, id"))

    def end_read_ask(self, ask_id: str, state: str, reason: str | None = None) -> None:
        self.db.execute("UPDATE read_asks SET state = ?, ended_at = ?, reason = ? WHERE id = ? AND state = 'waiting'",
                        (state, self.clock(), reason, ask_id))

    def add_read_message(self, *, message_id: str, kind: str, text: str = "", ask: str | None = None,
                         question: str | None = None, reason: str | None = None,
                         origin_turn: int | None = None) -> None:
        self.db.execute("INSERT OR IGNORE INTO read_messages (id, kind, ask, question, text, reason, origin_turn, "
                        "made_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (message_id, kind, ask, question, text, reason, origin_turn, self.clock()))

    def read_ask_asked_at(self, ask_id: str) -> float | None:
        row = self.db.execute("SELECT asked_at FROM read_asks WHERE id = ?", (ask_id,)).fetchone()
        return float(row[0]) if row else None

    def read_messages(self, ids: list[str]) -> dict[str, sqlite3.Row]:
        """The reader's own messages with these ids, by id (`rid`: the row's own
        number, stable for the life of the store)."""
        out: dict[str, sqlite3.Row] = {}
        for start in range(0, len(ids), 500):
            chunk = ids[start:start + 500]
            marks = ", ".join("?" for _ in chunk)
            out.update((row["id"], row) for row in self.db.execute(
                f"SELECT rowid AS rid, * FROM read_messages WHERE id IN ({marks})", chunk))
        return out

    def unpublished_read_messages(self) -> list[sqlite3.Row]:
        return list(self.db.execute("SELECT * FROM read_messages WHERE published = 0 ORDER BY made_at, id"))

    def sent_read_texts(self, kinds: tuple[str, ...], limit: int) -> list[str]:
        """What the reader has said this session (rows of these `kinds`), newest
        first, at most `limit`."""
        marks = ", ".join("?" for _ in kinds)
        return [row["text"] for row in self.db.execute(
            f"SELECT text FROM read_messages WHERE kind IN ({marks}) AND text != '' "
            "ORDER BY made_at DESC, id DESC LIMIT ?", (*[str(k) for k in kinds], int(limit)))]

    def mark_read_message_published(self, message_id: str) -> None:
        self.db.execute("UPDATE read_messages SET published = 1 WHERE id = ?", (message_id,))

    # -- run alerts --
    def delivered_run_alerts(self, ids: list[int]) -> set[int]:
        """Which of these server alert ids the mailbox was already handed."""
        out: set[int] = set()
        for start in range(0, len(ids), 500):
            chunk = [int(i) for i in ids[start:start + 500]]
            marks = ", ".join("?" for _ in chunk)
            out.update(int(row["id"]) for row in self.db.execute(
                f"SELECT id FROM run_alerts WHERE id IN ({marks})", chunk))
        return out

    def add_run_alerts(self, ids: list[int], message_id: str) -> None:
        """Record that these alerts went to the mailbox in message `message_id`."""
        now = self.clock()
        self.db.executemany("INSERT OR IGNORE INTO run_alerts (id, message_id, seen_at) VALUES (?, ?, ?)",
                            [(int(i), message_id, now) for i in ids])

    def open_read_turn(self, trigger: str, ask: str | None, first_seq: int | None, last_seq: int | None) -> int:
        cur = self.db.execute("INSERT INTO read_turns (started, trigger, ask, first_seq, last_seq) "
                              "VALUES (?, ?, ?, ?, ?)", (self.clock(), trigger, ask, first_seq, last_seq))
        return int(cur.lastrowid)

    def close_read_turn(self, turn_id: int, *, outcome: str, error: str | None = None, rounds: int = 0,
                        input_tokens: int = 0, cached_tokens: int = 0, output_tokens: int = 0,
                        usd: float | None = None) -> None:
        self.db.execute("UPDATE read_turns SET ended = ?, outcome = ?, error = ?, rounds = ?, input_tokens = ?, "
                        "cached_tokens = ?, output_tokens = ?, usd = ? WHERE id = ?",
                        (self.clock(), outcome, (error or "")[:500] or None, rounds, input_tokens, cached_tokens,
                         output_tokens, usd, turn_id))
        if self.on_read_turn_closed is not None:
            self.on_read_turn_closed({"turn": turn_id, "outcome": str(outcome), "error": error, "rounds": rounds,
                                      "input_tokens": input_tokens, "output_tokens": output_tokens,
                                      "cached_tokens": cached_tokens, "usd": usd})

    def read_summary(self, *, since: float | None = None) -> dict:
        """What the reader did: turns by outcome, tokens and dollars (for `probe doctor`, the benches)."""
        where, args = ("WHERE started >= ?", (since,)) if since is not None else ("", ())
        outcomes = {r["outcome"] or "running": int(r["n"]) for r in self.db.execute(
            f"SELECT outcome, count(*) AS n FROM read_turns {where} GROUP BY outcome", args)}
        row = self.db.execute(f"SELECT count(*) AS n, sum(input_tokens) AS i, sum(cached_tokens) AS c, "
                              f"sum(output_tokens) AS o, sum(usd) AS usd FROM read_turns {where}", args).fetchone()
        messages = {r["kind"]: int(r["n"]) for r in self.db.execute(
            "SELECT kind, count(*) AS n FROM read_messages GROUP BY kind")}
        return {"turns": int(row["n"] or 0), "outcomes": outcomes, "input_tokens": int(row["i"] or 0),
                "cached_tokens": int(row["c"] or 0), "output_tokens": int(row["o"] or 0),
                "usd": float(row["usd"] or 0.0), "messages": messages}
