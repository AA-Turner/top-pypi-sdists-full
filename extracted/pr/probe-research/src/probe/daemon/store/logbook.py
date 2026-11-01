"""bites, model rounds and the logbook of every probe command the daemon ran or was refused; run summaries."""

from __future__ import annotations

import json
import sqlite3
from probe.daemon.store.events import scrub
#: Fact: a conversation run paused and the next bite carries on (`worker.CARRY_ON`).
CARRY_ON = "carry_on"
#: A bite's outcome when its run finished, and when it paused (`Worker._paused`).
BITE_DONE = "done"
BITE_PAUSED = "paused"
#: A run that stopped unfinished, its events covered as skipped (`Worker._cut_short`).
BITE_SKIPPED = "cut short: skipped"


class LogbookMixin:
    """Part of Store: its methods run with `self` the Store; compose() folds them into Store."""

    # -- bites --
    def open_bite(self, trigger: str, first_seq: int | None, last_seq: int | None) -> int:
        cur = self.db.execute("INSERT INTO bites (started, trigger, first_seq, last_seq) VALUES (?, ?, ?, ?)",
                              (self.clock(), trigger, first_seq, last_seq))
        return int(cur.lastrowid)

    def close_bite(self, bite_id: int, *, outcome: str, error: str | None = None, input_tokens: int = 0,
                   output_tokens: int = 0, cached_tokens: int = 0) -> None:
        self.db.execute("UPDATE bites SET ended = ?, outcome = ?, error = ?, input_tokens = ?, output_tokens = ?, "
                        "cached_tokens = ?, attempts = attempts + 1 WHERE id = ?",
                        (self.clock(), outcome, error, input_tokens, output_tokens, cached_tokens, bite_id))
        if self.on_bite_closed is not None:
            self.on_bite_closed({"bite": bite_id, "outcome": outcome, "error": error, "input_tokens": input_tokens,
                                 "output_tokens": output_tokens, "cached_tokens": cached_tokens})

    def recent_bites(self, limit: int = 10) -> list[sqlite3.Row]:
        return list(self.db.execute("SELECT * FROM bites ORDER BY id DESC LIMIT ?", (limit,)))

    def tokens_today(self) -> int:
        since = self.clock() - 86400
        row = self.db.execute("SELECT coalesce(sum(input_tokens + output_tokens), 0) AS t FROM bites WHERE started >= ?",
                              (since,)).fetchone()
        return int(row["t"])

    # -- logbook --
    def log_write(self, *, bite: int | None, op_id: str, argv: list[str], head: str, status: str,
                  reason: str | None = None, output: str | None = None, exit_code: int | None = None,
                  request: str | None = None) -> int:
        cur = self.db.execute(
            "INSERT INTO writes (bite, op_id, at, argv, head, status, reason, output, exit_code, request) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (bite, op_id, self.clock(), json.dumps([scrub(a) for a in argv]), head, status, reason,
             scrub(output or "")[:20_000] if output is not None else None, exit_code, request),
        )
        return int(cur.lastrowid)

    def update_write(self, row_id: int, *, status: str, reason: str | None, output: str | None = None,
                     exit_code: int | None = None) -> None:
        """A logbook line written before its command ran (`running`), now with how it ended."""
        self.db.execute("UPDATE writes SET status = ?, reason = ?, output = ?, exit_code = ? WHERE id = ?",
                        (status, reason, scrub(output or "")[:20_000] if output is not None else None, exit_code,
                         row_id))

    def recent_writes(self, limit: int = 10) -> list[sqlite3.Row]:
        return list(self.db.execute("SELECT * FROM writes WHERE status != 'read' ORDER BY id DESC LIMIT ?", (limit,)))

    def open_failures(self, *, bites: int, limit: int) -> list[sqlite3.Row]:
        """Failed, refused or queued writes of the last `bites` bites that no
        later write of the same command and target ran after: what is still NOT
        recorded. A queued write (Probe did not answer; the outbox sends it
        later) stands in for an earlier failure of the same command."""
        row = self.db.execute("SELECT min(started) AS s FROM (SELECT started FROM bites ORDER BY id DESC LIMIT ?)",
                              (bites,)).fetchone()
        rows = self.db.execute("SELECT * FROM writes WHERE at >= ? AND status IN ('failed', 'not_run', 'ran', "
                               "'queued') ORDER BY id", (row["s"] or 0,))
        open_: dict[tuple[str, str], sqlite3.Row] = {}
        for r in rows:
            key = (r["head"], write_target(r["head"], json.loads(r["argv"])))
            if r["status"] == "ran":
                open_.pop(key, None)
            else:
                open_[key] = r
        return sorted(open_.values(), key=lambda r: r["id"], reverse=True)[:limit]

    def filed(self, limit: int = 40, *, skip_heads: tuple[str, ...] = ()) -> list[sqlite3.Row]:
        """The writes that ran, newest first, one per command and target: what the
        record holds so far, in the logbook's own words."""
        seen: set[tuple[str, str]] = set()
        out: list[sqlite3.Row] = []
        # The newest few thousand writes are plenty: this runs before every model request.
        for r in self.db.execute("SELECT * FROM writes WHERE status = 'ran' ORDER BY id DESC LIMIT 5000"):
            if r["head"] in skip_heads:
                continue
            key = (r["head"], write_target(r["head"], json.loads(r["argv"])))
            if key in seen:
                continue
            seen.add(key)
            out.append(r)
            if len(out) >= limit:
                break
        return out

    def landed_writes(self, limit: int = 5000) -> list[sqlite3.Row]:
        """The writes that ran, newest first, each with the events its run
        covered (`first_event`, `last_event`: event ids, NULL for a run that
        covered none)."""
        return list(self.db.execute(
            "SELECT w.*, e1.event_id AS first_event, e2.event_id AS last_event FROM writes w "
            "LEFT JOIN bites b ON b.id = w.bite LEFT JOIN events e1 ON e1.seq = b.first_seq "
            "LEFT JOIN events e2 ON e2.seq = b.last_seq WHERE w.status = 'ran' ORDER BY w.id DESC LIMIT ?",
            (limit,)))

    def writes_count(self) -> int:
        return int(self.db.execute("SELECT count(*) AS n FROM writes WHERE status = 'ran'").fetchone()["n"])

    def log_lookup(self, *, bite: int | None, tool: str, query: str, result: str) -> None:
        self.db.execute("INSERT INTO lookups (bite, at, tool, query, result) VALUES (?, ?, ?, ?, ?)",
                        (bite, self.clock(), tool, scrub(query)[:4000], scrub(result)[:4000]))

    def search_logbook(self, query: str, limit: int = 20, *, writes_only: bool = False) -> list[sqlite3.Row]:
        """The logbook's lines matching `query`, newest first. `writes_only` (the
        reader): the commands only -- the writer's lookups hold what it read,
        files the reader may not open, and a write's output is matched by none."""
        like = f"%{query}%"
        if writes_only:
            return list(self.db.execute(
                "SELECT 'write' AS what, id, at, argv AS body, status, reason FROM writes WHERE argv LIKE ? "
                "AND status != 'read' ORDER BY at DESC LIMIT ?", (like, limit)))
        return list(self.db.execute(
            "SELECT 'write' AS what, id, at, argv AS body, status, reason FROM writes WHERE argv LIKE ? OR output LIKE ? "
            "UNION ALL SELECT 'lookup', id, at, tool || ': ' || query, '', result FROM lookups "
            "WHERE query LIKE ? OR result LIKE ? ORDER BY at DESC LIMIT ?",
            (like, like, like, like, limit)))

    # -- each run's one-line summary --
    def note(self) -> str:
        row = self.db.execute("SELECT body FROM notes ORDER BY version DESC LIMIT 1").fetchone()
        return row["body"] if row else ""

    def set_note(self, body: str, *, bite: int | None) -> None:
        body = scrub(body.strip())
        if body and body != self.note():
            self.db.execute("INSERT INTO notes (at, bite, body) VALUES (?, ?, ?)", (self.clock(), bite, body))

    # -- model rounds (T10) --
    def add_round(self, *, bite: int | None, model: str | None, input_tokens: int, cached_tokens: int,
                  output_tokens: int, tools: list[str], usd: float | None) -> None:
        self.db.execute("INSERT INTO rounds (bite, at, model, input_tokens, cached_tokens, output_tokens, tools, usd) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (bite, self.clock(), model, int(input_tokens), int(cached_tokens), int(output_tokens),
                         json.dumps(tools), usd))

    def usage_summary(self, *, since: float | None = None) -> dict:
        """What the model rounds cost (since `since`): tokens, the cached share of the
        input, the dollars of the rounds a price is known for, and how many were not."""
        where, args = ("WHERE at >= ?", (since,)) if since is not None else ("", ())
        row = self.db.execute(
            "SELECT count(*) AS n, coalesce(sum(input_tokens), 0) AS i, coalesce(sum(cached_tokens), 0) AS c, "
            "coalesce(sum(output_tokens), 0) AS o, coalesce(sum(usd), 0) AS usd, "
            f"sum(CASE WHEN usd IS NULL THEN 1 ELSE 0 END) AS unpriced FROM rounds {where}", args).fetchone()
        models = [r["model"] for r in self.db.execute(
            f"SELECT DISTINCT model FROM rounds {where} ORDER BY model", args) if r["model"]]
        return {"rounds": int(row["n"]), "input_tokens": int(row["i"]), "cached_tokens": int(row["c"]),
                "output_tokens": int(row["o"]), "usd": float(row["usd"] or 0.0),
                "unpriced_rounds": int(row["unpriced"] or 0), "models": models}


def write_target(head: str, argv: list[str]) -> str:
    """What a logged write acted on: a shell write's command, else the first
    positional after the command's words (`probe run tag R ...` -> R), else its
    anchor option (`--run R`). `--group` is a run's sweep group (`run start
    --group`); `--artifact` went with the notes on files."""
    if head == "shell":
        return argv[-1] if argv else ""
    words = argv[1 + len(head.split()):] if argv[:1] == ["probe"] else argv
    for i, word in enumerate(words):
        if not word.startswith("-"):
            if i == 0 or not words[i - 1].startswith("--") or "=" in words[i - 1]:
                return word
    for i, word in enumerate(words[:-1]):
        if word in ("--run", "--project", "--experiment", "--group", "--note"):
            return words[i + 1]
    return ""
