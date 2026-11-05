"""NamedFiles: the files a `probe exec` step names as inputs and outputs, hashed and sent with one run budget."""

from __future__ import annotations
import hashlib
import os
import socket
from typing import Any
from probe.sdk.capture.lineage.lineage import FINISH_WAIT_S, _named_hash, excluded


# -- files a step NAMES (`probe exec --input/--output`, F39) --------------------
#: The read hook lives only in Python children (`sitecustomize`), so a shell
#: step (`head -n 500 > dev.jsonl`, `cat a b | shuf > train.jsonl`, `jq`)
#: records nothing by itself. `probe exec --input PATH --output PATH` names its
#: files; they are hashed with the recorder's own hasher (one budget, rows,
#: the 64-byte `hash` floor) when the step starts and when it exits, and sent
#: as the run's reads and writes, so the existing hash matching draws the
#: arrows. Off/read paths are skipped as the recorder skips them.


def expand_named(patterns: "list[str] | tuple[str, ...]", base: str | None = None) -> list[str]:
    """Absolute regular-file paths for ``patterns``: globs (``**`` spans
    folders) taken from ``base`` (else the working directory), a folder means
    every file under it. Sorted, without repeats, at most MAX_PATHS."""
    import glob as _glob

    root = os.path.abspath(base or os.getcwd())
    found: dict[str, None] = {}
    for pattern in patterns or ():
        if not isinstance(pattern, str) or not pattern:
            continue
        expanded = os.path.expanduser(pattern)
        full = expanded if os.path.isabs(expanded) else os.path.join(root, expanded)
        hits = sorted(_glob.glob(full, recursive=True)) if _glob.has_magic(full) else [full]
        for hit in hits:
            hit = os.path.normpath(hit)
            if os.path.isdir(hit):
                for folder, dirs, files in os.walk(hit):
                    dirs.sort()
                    for name in sorted(files):
                        found.setdefault(os.path.join(folder, name), None)
                        if len(found) >= MAX_PATHS:
                            return sorted(found)
            elif os.path.isfile(hit):
                found.setdefault(hit, None)
            if len(found) >= MAX_PATHS:
                return sorted(found)
    return sorted(found)


def _named_recordable(path: str) -> bool:
    """A named file the recorder would record: not one it never records
    (:func:`excluded`), storable."""
    return not excluded(path) and _sendable(path)


class NamedFiles:
    """One `probe exec` step's named files: :meth:`start` before the command
    runs (sends the inputs, remembers what the outputs were), :meth:`finish`
    when it exits (sends the outputs it changed or created). Never raises."""

    def __init__(
        self,
        client: Any,
        run_id: str,
        *,
        inputs: "list[str] | tuple[str, ...]" = (),
        outputs: "list[str] | tuple[str, ...]" = (),
        base: str | None = None,
        wait_s: float = FINISH_WAIT_S,
    ) -> None:
        self.client = client
        self.run_id = run_id
        self.inputs = [p for p in (inputs or ()) if isinstance(p, str) and p]
        self.outputs = [p for p in (outputs or ()) if isinstance(p, str) and p]
        self.base = base
        self.wait_s = wait_s
        self.started_at = _now_iso()
        self.before: dict[str, tuple | None] = {}
        self.sent_inputs = 0
        self.sent_outputs = 0

    def start(self) -> int:
        """Hash and send the named inputs; note the named outputs' identity now.
        Returns how many input rows were sent."""
        try:
            self.started_at = _now_iso()
            for path in expand_named(self.outputs, self.base):
                try:
                    self.before[path] = _ident(os.stat(path))
                except OSError:
                    self.before[path] = None
            if self.inputs:
                self.sent_inputs = self._send_inputs(expand_named(self.inputs, self.base))
        except Exception:  # noqa: BLE001 -- lineage evidence never stops a step
            pass
        return self.sent_inputs

    def finish(self) -> int:
        """Hash and send the named outputs the step created or changed.
        Returns how many output rows were sent."""
        try:
            if self.outputs:
                self.sent_outputs = self._send_outputs(expand_named(self.outputs, self.base))
        except Exception:  # noqa: BLE001
            pass
        return self.sent_outputs

    def _stat_all(self, paths: list[str]) -> list[tuple[str, tuple]]:
        out = []
        for path in paths:
            if not _named_recordable(path):
                continue
            try:
                st = os.stat(path)
            except OSError:
                continue
            if _stat_is_file(st):
                out.append((path, _ident(st)))
        return out

    def _send_inputs(self, paths: list[str]) -> int:
        if _server_takes_reads(self.client) is not True:
            return 0
        observations = _server_takes(self.client, OBSERVATIONS_FEATURE) is True
        stated = self._stat_all(paths)
        if not stated:
            return 0
        answers = _named_hash(stated, self.wait_s)
        # scanning disabled: from . import redaction

        # scanning disabled: host = redaction.scrub_string(socket.gethostname())
        host = socket.gethostname()
        rows: list[dict] = []
        for path, ident in stated:
            sha = fp = rows_n = None
            stable = True
            result = answers.get(ident)
            if result is not None:
                sha, fp, rows_n = result
                stable = sha is not None or fp is not None
            row = _typed_row(
                path, sha, fp, ident[2], host, stable, self.started_at,
                _read_observation(self.run_id, host, path, ident) if observations else None, rows=rows_n,
            )
            if row is not None:
                rows.append(row)
        if rows:
            # No coverage: the step's close sends the run's own (one would REPLACE it).
            _journal_rows(self.client, self.run_id, "inputs", rows, None)
            self._wake()
        return len(rows)

    def _wake(self) -> None:
        """Wake delivery for what was just journaled (best effort)."""
        try:
            wake = getattr(self.client, "_after_enqueue", None)
            if callable(wake):
                wake()
        except Exception:  # noqa: BLE001
            pass

    def _send_outputs(self, paths: list[str]) -> int:
        if _server_takes(self.client, OUTPUTS_FEATURE) is not True:
            return 0
        stated = [
            (path, ident) for path, ident in self._stat_all(paths)
            if self.before.get(path) is None or list(self.before[path]) != list(ident)
        ]
        if not stated:
            return 0
        answers = _named_hash(stated, self.wait_s)
        # scanning disabled: from . import redaction

        # scanning disabled: host = redaction.scrub_string(socket.gethostname())
        host = socket.gethostname()
        rows: list[dict] = []
        for path, ident in stated:
            sha = fp = rows_n = None
            result = answers.get(ident)
            if result is not None:
                sha, fp, rows_n = result
            observation = hashlib.sha256(
                "\0".join((self.run_id, host, path, "named-output", self.started_at)).encode("utf-8", "surrogatepass")
            ).hexdigest()[:32]
            row = _typed_output_row(
                path, sha, fp, ident[2], host, self.started_at, _iso_from_ns(ident[3]), observation, rows=rows_n
            )
            if row is not None:
                rows.append(row)
        if rows:
            _journal_rows(self.client, self.run_id, "outputs", rows, None)
            self._wake()
        return len(rows)
from probe.sdk.capture.lineage.exclusions import _sendable  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.capture.lineage.finishing import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    OBSERVATIONS_FEATURE,
    OUTPUTS_FEATURE,
    _journal_rows,
    _server_takes,
    _server_takes_reads,
)
from probe.sdk.capture.lineage.rows import _iso_from_ns, _read_observation, _typed_output_row, _typed_row  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.capture.lineage.spool.spool import MAX_PATHS, _ident, _now_iso, _stat_is_file  # noqa: E402 -- pieces need each other; the front door loads this one first
