"""a session's Probe-off stretches (gaps): kept in its record, written to and merged from its gap file."""

from __future__ import annotations
from pathlib import Path


from .. import capture_gate
from probe.service.sessions.recorders.recording import Recording


class GapsMixin:
    """Part of RecorderHost: its methods run with `self` the RecorderHost; compose() folds them into RecorderHost."""

    @staticmethod
    def _sessions_dir(rec: Recording) -> Path:
        """Where the session's switch and gap file are (its registrant's state folder)."""
        env = rec.params.get("env") if isinstance(rec.params.get("env"), dict) else {}
        return capture_gate.sessions_dir_for(env, rec.params.get("state_dir"))

    def _keep_gaps(self, rec: Recording, gaps: list) -> None:
        """The session's gaps in its record (saved with `recorders.json`) and
        for the drains of this process, at once; its gap file next, off this
        lock and off the loop (`_flush_gap_file`). Under `_gate_lock`."""
        rec.params[capture_gate.GAPS_KEY] = gaps
        if gaps:
            capture_gate.unsettled(rec.sid, gaps)
        else:
            capture_gate.settled(rec.sid)
            rec.params.pop(capture_gate.GAPS_KEY, None)
        rec.gap_file_due = True

    def _flush_gap_file(self, rec: Recording) -> None:
        """Write the session's gap file when it is behind its record (or holds
        gaps its record does not: a removal that failed). Under the session's
        gap-file lock (`capture_gate.locked`), which every writer takes: what
        another writer (a `tap watch` of the session, tap 0.10.19) put there
        since this recording last wrote or read it is merged into its record
        first, never written over. Never for a recording a newer one of the
        session replaced. Not on the loop."""
        if self._superseded(rec) or not rec.file_merged:
            return  # never a gap only the file holds, before the record took it in
        sessions = self._sessions_dir(rec)
        merged: list = []
        with self._gap_file_lock:  # one writer at a time, so the last one written is the newest
            try:
                with capture_gate.locked(sessions, rec.sid):
                    written = self._write_gap_file(rec, sessions, merged)
            except OSError:
                written = False  # the lock could not be had now: tried again at the next look
            if merged:
                self.log(f"capture gate: session {rec.sid}'s gap file holds gaps another recorder wrote; "
                         f"its gaps (transcript bytes) are {merged[0]}")
                self._save()
                self._notify()
            if written is None:
                return
            if not written:
                rec.gap_file_due = True
                if not rec.gap_file_failing:
                    rec.gap_file_failing = True
                    self.log(f"capture gate: session {rec.sid}'s gap file could not be written; "
                             "tried again at each look")
            elif rec.gap_file_failing:
                rec.gap_file_failing = False
                self.log(f"capture gate: session {rec.sid}'s gap file is written again")

    def _write_gap_file(self, rec: Recording, sessions: Path, merged: list) -> bool | None:
        """`_flush_gap_file`'s write, under the session's gap-file lock: True
        written, False not (tried again later), None nothing to write. What it
        merged from another writer goes in `merged`."""
        signature = capture_gate.file_signature(sessions, rec.sid)
        if signature != rec.file_sig:
            # Written by another writer since this recording last saw it.
            raw = capture_gate.read_gap_file_raw(sessions, rec.sid)
            if raw is None:
                return False  # cannot be read now: never written over unread
            joined = self._merge_from_file(rec, raw)
            if joined is not None:
                merged.append(joined)
            rec.file_sig = signature
        on_file = capture_gate.read_gap_file(sessions, rec.sid)
        with self._gate_lock:
            if self._superseded(rec):
                return None
            gaps = capture_gate.gaps_of(rec.params)
            due = rec.gap_file_due or on_file != capture_gate.normalized(gaps)
            rec.gap_file_due = False
        if not due:
            return None
        if not capture_gate.write_gap_file(sessions, rec.sid, gaps, rec.transcript):
            return False
        rec.file_sig = capture_gate.file_signature(sessions, rec.sid)
        return True

    def _merge_from_file(self, rec: Recording, on_file: list) -> list | None:
        """Gaps another writer put in the session's gap file join its record:
        all but the ones this recording settled, and an open gap this record
        already closed (the same start: its own, from before it saw it close).
        The record's gaps after, or None when nothing joined."""
        with self._gate_lock:
            if self._superseded(rec):
                return None
            gaps = capture_gate.gaps_of(rec.params)
            closed_at = {g[0] for g in gaps if g[1] is not None}
            extra = [g for g in on_file if (g[0], g[1]) not in rec.settled_gaps
                     and not (g[1] is None and g[0] in closed_at)]
            merged = capture_gate.normalized(gaps + extra)
            if merged == capture_gate.normalized(gaps):
                return None
            self._keep_gaps(rec, merged)
            return merged

    @staticmethod
    def _carry_gaps(previous: Recording, session: dict) -> None:
        """A session's off stretches go on in its new record. Under `_gate_lock`."""
        if capture_gate.GAPS_KEY in previous.params:
            session[capture_gate.GAPS_KEY] = previous.params[capture_gate.GAPS_KEY]
