"""the folder check's last-seen snapshot and growing files."""

from __future__ import annotations
import sqlite3


class FolderCheckMixin:
    """Part of Store: its methods run with `self` the Store; compose() folds them into Store."""

    # -- folder check --
    def file_row(self, path: str) -> sqlite3.Row | None:
        return self.db.execute("SELECT * FROM files WHERE path = ?", (path,)).fetchone()

    def file_snapshot(self) -> dict[str, tuple[int, float]]:
        """`{path: (size, mtime)}` of the last folder check."""
        return {r["path"]: (r["size"], r["mtime"] or 0.0) for r in self.db.execute("SELECT path, size, mtime FROM files")}

    def stored_text_bytes(self) -> int:
        """The characters of every last-seen text copy: a running total kept in
        `meta` by `set_file`, so the folder check never sums up to 64 MB on the
        event loop. Summed once, for a store written before the total existed."""
        value = self.meta("files_text_chars")
        if value is None:
            value = str(self.db.execute("SELECT coalesce(sum(length(text)), 0) + coalesce(sum(length(growing_text)), 0) "
                                        "AS n FROM files").fetchone()["n"])
            self.set_meta("files_text_chars", value)
        return int(value)

    def set_file(self, path: str, size: int, mtime: float, text: str | None, *,
                 changed_at: int | None = None) -> None:
        """`changed_at`: the folder check (`folders.CHECKS`) that found it new or
        changed; None for a check that only moves the snapshot on."""
        total = self.stored_text_bytes()  # before the row changes: a first sum must not count it
        row = self.db.execute("SELECT length(text) AS n FROM files WHERE path = ?", (path,)).fetchone()
        old = int(row["n"] or 0) if row else 0
        self.db.execute("INSERT INTO files (path, size, mtime, text, changed_at) VALUES (?, ?, ?, ?, ?) "
                        "ON CONFLICT(path) DO UPDATE SET size = excluded.size, mtime = excluded.mtime, "
                        "text = excluded.text, changed_at = excluded.changed_at",
                        (path, size, mtime, text, changed_at))
        self.set_meta("files_text_chars", str(max(0, total - old + len(text or ""))))

    def start_growing(self, path: str, size: int, text: str | None) -> None:
        """`path` changed at two checks in a row: what it was before (its size and
        text), so the line once it stops shows the whole change (`folders.GROWING`)."""
        total = self.stored_text_bytes()
        self.db.execute("UPDATE files SET growing_size = ?, growing_text = ? WHERE path = ?", (size, text, path))
        self.set_meta("files_text_chars", str(total + len(text or "")))

    def stop_growing(self, path: str) -> None:
        total = self.stored_text_bytes()
        row = self.db.execute("SELECT length(growing_text) AS n FROM files WHERE path = ?", (path,)).fetchone()
        self.db.execute("UPDATE files SET growing_size = NULL, growing_text = NULL WHERE path = ?", (path,))
        self.set_meta("files_text_chars", str(max(0, total - (int(row["n"] or 0) if row else 0))))

    def growing_files(self, *, changed_before: int | None = None) -> list[sqlite3.Row]:
        """The growing files (`start_growing`), oldest change first; `changed_before`:
        only those that last changed before that check (quiet since)."""
        sql = "SELECT * FROM files WHERE growing_size IS NOT NULL"
        args: tuple = ()
        if changed_before is not None:
            sql += " AND (changed_at IS NULL OR changed_at < ?)"
            args = (int(changed_before),)
        return list(self.db.execute(sql + " ORDER BY changed_at, path", args))
