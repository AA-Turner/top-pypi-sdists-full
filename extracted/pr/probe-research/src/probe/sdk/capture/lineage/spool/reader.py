"""find the spools a close may consume and read their observations, earliest per path and identity."""

from __future__ import annotations
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any
from ....recording_rules import recording_rules as _ignore


def _header(raw: str) -> dict | None:
    """A spool line when it is a header (``{"run", "owner", "follows"}``:
    the run the lines after it are bound to, the process whose close takes
    them, and whether that one is a binding owner the writer follows)."""
    if not raw.startswith('{"run"'):
        return None
    try:
        header = json.loads(raw)
    except ValueError:
        return None
    return header if isinstance(header, dict) else None


def _spool_header(spool: Path, *, last: bool = False) -> dict:
    """A spool's first header, or -- ``last`` -- the one in force now (a
    header is written at every open: a worker that joined a run of its own
    appends to the spool its bound hook began); {} when there is none."""
    found: dict = {}
    try:
        with open(spool, encoding="utf-8", errors="replace") as handle:
            if not last:
                return _header(handle.readline(4096)) or {}
            for raw in handle:
                header = _header(raw)
                if header is not None:
                    found = header
    except OSError:
        return {}
    return found


def _spools(run_id: str, *, closing: bool = False) -> tuple[list[Path], int]:
    """(the spools this process may read and then delete, how many it may not).
    It may take this host's, written by this process or by one that has ended.
    A live rank's or worker's spool is its own to send; another host's pids
    mean nothing here. ``closing``: this process is closing the run, so it
    also takes the live spools of the workers it bound (their header names it
    the owner, and says it FOLLOWS this process's binding, F5) -- they stopped
    recording the run when it did, and what they spooled after is cut. A
    live worker that only inherited the run by a fork, with no binding to
    follow, keeps recording it: its spool is left until it ends."""
    host, me = _host(), os.getpid()
    mine, pending = [], 0
    with internal():
        for spool in sorted(run_dir(run_id).glob("*.jsonl")):
            owner = _spool_owner(spool)
            if owner is None or owner[0] != host:
                continue
            if owner[1] == me or not _pid_alive(owner[1]):
                mine.append(spool)
                continue
            header = _spool_header(spool, last=True) if closing else {}
            if header.get("owner") == me and header.get("follows") is True:
                mine.append(spool)
            else:
                pending += 1
    return mine, pending


def _closed_marks(directory: Path) -> dict[int, datetime]:
    """owner pid -> when it stopped recording the run it had bound its workers
    to (`_mark_closed`), for this host's markers in ``directory``."""
    out: dict[int, datetime] = {}
    for marker in directory.glob(f"closed.{_host()}.*.json"):
        try:
            record = json.loads(marker.read_text(encoding="utf-8"))
            out[int(record["owner"])] = datetime.fromisoformat(record["at"])
        except (OSError, ValueError, KeyError, TypeError):
            continue
    return out


def _after(seen_at: Any, cut: datetime | None) -> bool:
    """Whether a spool line's time is after its binding owner's close."""
    if cut is None or not isinstance(seen_at, str):
        return False
    try:
        return datetime.fromisoformat(seen_at) > cut
    except ValueError:
        return False


def _collectable_spools(run_id: str) -> list[Path]:
    return _spools(run_id)[0]


#: At most this many `.probeignore` rule sets are taken from one run's spools.
MAX_HANDED_RULES = 16


def _sidecar(spool: Path) -> Path:
    """The ``.wf.json`` sidecar beside ``<host>.<pid>.jsonl``."""
    return spool.with_suffix(WF_SUFFIX)


class _SpooledWrites:
    """What a run's spools say about its writes: path -> the EARLIEST note of
    it (``{"w", "t", "n", "o", "b"}``); path -> the identity each recorder
    last saw the file have while it lived (its ``.wf.json`` sidecar, see
    `check_writes`); whether a recorder hit its cap; and whether a process of
    the run opted out after its hook started (``"writes_off"`` /
    ``"reads_off"`` lines, see :func:`start`). ``keep=False`` learns the
    opt-outs only."""

    def __init__(self, keep: bool = True) -> None:
        self.keep = keep
        self.rows: dict[str, dict] = {}
        self.seen: dict[str, set[tuple]] = {}
        self.truncated = False
        self.writes_off = False
        self.reads_off = False

    def add_sidecar(self, spool: Path) -> None:
        """Take in what the recorder of ``spool`` last saw of its writes."""
        if not self.keep:
            return
        try:
            with open(_sidecar(spool), encoding="utf-8") as handle:
                seen = json.load(handle)
        except (OSError, ValueError):
            return
        if not isinstance(seen, dict):
            return
        for path, raw in list(seen.items())[:MAX_PATHS]:
            try:
                ident = tuple(int(v) for v in raw)
            except (TypeError, ValueError):
                continue
            if isinstance(path, str) and len(ident) == 5:
                self.seen.setdefault(path, set()).add(ident)

    def add(self, row: dict) -> None:
        path = row.get("w")
        if not isinstance(path, str) or not self.keep:
            return
        prior = self.rows.get(path)
        if prior is None:
            if len(self.rows) >= MAX_PATHS:
                self.truncated = True
                return
            self.rows[path] = row
        elif str(row.get("t", "")) < str(prior.get("t", "")):
            self.rows[path] = row


def _read_spools(
    spools: list[Path], handed: list[Any] | None = None, writes: _SpooledWrites | None = None
) -> tuple[dict[tuple, dict], bool]:
    """Every observation in these spools, earliest per (path, identity), read
    line by line. True when a recorder hit its cap (it says so in its spool) or
    the spools hold more than MAX_PATHS observations. The ``.probeignore`` rules
    a recorder handed over in its spool (:func:`hand_to_launcher`) are appended
    to ``handed`` when given; the noted WRITES go to ``writes`` when given (and
    are skipped otherwise).

    Lines under a header binding them to ANOTHER run are not this run's and
    are skipped. A worker's lines bound through an owner that has since
    stopped recording the run (F5, `_mark_closed`) are cut there: what it
    spooled after the close is not the closed run's."""
    merged: dict[tuple, dict] = {}
    truncated = full = False
    if handed is None:
        handed = []
    marks: dict[Path, dict[int, datetime]] = {}
    with internal():
        for spool in spools:
            if spool.parent not in marks:
                marks[spool.parent] = _closed_marks(spool.parent)
            this_run, cut = True, None
            if writes is not None:
                writes.add_sidecar(spool)
            try:
                handle = open(spool, encoding="utf-8", errors="replace")  # noqa: SIM115
            except OSError:
                continue
            with handle:
                for raw in handle:
                    header = _header(raw)
                    if header is not None:
                        this_run = header.get("run") in (None, _folder_run(spool.parent.name))
                        owner = header.get("owner")
                        cut = marks[spool.parent].get(owner) if isinstance(owner, int) else None
                        continue
                    if not this_run:
                        continue
                    if raw.startswith(('{"w', '{"reads_off"')):  # write notes, opt-outs
                        if writes is None:
                            continue
                        try:
                            row = json.loads(raw)
                        except ValueError:
                            continue
                        if not isinstance(row, dict):
                            continue
                        if row.get("writes_off"):
                            writes.writes_off = True
                        elif row.get("reads_off"):
                            writes.reads_off = True
                        elif row.get("wtruncated"):
                            writes.truncated = True
                        elif not _after(row.get("t"), cut):
                            writes.add(row)
                        continue
                    if full and '"ignore"' not in raw:
                        continue  # past the cap only a rule line still counts
                    try:
                        row = json.loads(raw)
                        if row.get("truncated"):
                            truncated = True
                            continue
                        if "ignore" in row:
                            rules = _ignore.from_record(row["ignore"])
                            if rules is not None and rules not in handed and len(handed) < MAX_HANDED_RULES:
                                handed.append(rules)
                            continue
                        key = (row["p"], (row["d"], row["i"], row["s"], row["m"], row.get("c")))
                    except (ValueError, KeyError, TypeError, AttributeError):
                        continue
                    if cut is not None and _after(row.get("t"), cut):
                        continue  # a worker's read after its owner's close
                    prior = merged.get(key)
                    if prior is None:
                        if len(merged) >= MAX_PATHS:
                            # Stop taking reads, not rules: a rule line may
                            # sit after the cap.
                            truncated = full = True
                            continue
                        merged[key] = row
                    elif str(row.get("t", "")) < str(prior.get("t", "")):
                        merged[key] = row
    return merged, truncated
from probe.sdk.capture.lineage.spool.spool import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    MAX_PATHS,
    WF_SUFFIX,
    _folder_run,
    _host,
    _pid_alive,
    _spool_owner,
    internal,
    run_dir,
)
