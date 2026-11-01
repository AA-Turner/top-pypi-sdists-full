"""finish a run's recording: journal the lists the server takes, keep and resend late hashes, or discard and abandon."""

from __future__ import annotations

import contextlib
import json
import os
import shutil
from pathlib import Path
from typing import Any
from ....foundation.safe_warn import safe_warn as _diagnostics
from probe.sdk.capture.lineage.lineage import Collected, FINISH_WAIT_S, _active, _stop, collect_all
FEATURE = "run_inputs"
#: The server takes a run's write list (``POST /v1/runs/{id}/outputs``).
OUTPUTS_FEATURE = "run_outputs"
#: The server keys a read on (run, path, host, observation_id) (0290, F7), so
#: a late hash REPLACES the read's unhashed row. No feature names that: it
#: shipped in the same server change as `run_outputs`, so a server declaring
#: `run_outputs` understands it. An older one ignores the field (its model
#: does not forbid extras) but would keep a late hash as a SECOND row, so the
#: id is sent, and late hashes re-sent, only to a server that declares it.
OBSERVATIONS_FEATURE = OUTPUTS_FEATURE
BATCH_ROWS = 2000
#: The spools `collect` read, for `discard` to remove -- and only those.
_consumed: dict[str, list[Path]] = {}


def _server_takes(client: Any, feature: str) -> bool | None:
    """Whether the server takes ``feature``'s list: True, False (it declared
    it does not -- a definite answer), or None (unreachable: ask again later)."""
    try:
        return bool(client.supports_feature(feature))
    except Exception:  # noqa: BLE001
        return None


def _server_takes_reads(client: Any) -> bool | None:
    """Whether the server accepts read lists (see :func:`_server_takes`)."""
    return _server_takes(client, FEATURE)


#: The journal tag on a late hash re-send (`_resend_late`): `probe sync`
#: drops one for a server that would keep it as a second row.
LATE_TAG = "late_hash"


def _journal_rows(
    client: Any, run_id: str, route: str, rows: list[dict], coverage: dict | None, *, tag: str | None = None
) -> None:
    """``rows`` as NON-blocking ``POST /v1/runs/{id}/<route>`` ops of
    BATCH_ROWS each, EACH carrying the coverage (the server stores the same
    object again): a list is lineage evidence and must never hold a run's
    close. An empty list still carries its coverage, so "recorded nothing"
    reads apart from "not recorded". ``coverage=None`` (late hashes, F7)
    sends none: the server would REPLACE the run's with it. ``tag`` marks
    the ops in the queue (a late re-send: `LATE_TAG`, for `probe sync`)."""
    batches = [rows[i : i + BATCH_ROWS] for i in range(0, len(rows), BATCH_ROWS)] or [[]]
    for batch in batches:
        body: dict[str, Any] = {route: batch}
        if coverage is not None:
            body["coverage"] = coverage
        extra = {"tag": tag} if tag is not None else {}
        client.journal.append_http(
            "POST", f"/v1/runs/{run_id}/{route}", body, run_ref=run_id, blocking=False, **extra
        )


def send(client: Any, run_id: str, rows: list[dict], coverage: dict) -> bool:
    """Journal the read list as non-blocking ops. False when it was not sent:
    an unreachable server keeps the spools for recovery; a server that does
    not take reads drops them, since nothing will ever accept them."""
    takes = _server_takes_reads(client)
    if takes is False:
        discard(run_id)
    if not takes:
        _consumed.pop(run_id, None)
        return False
    if _server_takes(client, OBSERVATIONS_FEATURE) is not True:
        rows = [_without_observation(row) for row in rows]
    _journal_rows(client, run_id, "inputs", rows, coverage)
    discard(run_id)
    return True


def send_outputs(client: Any, run_id: str, rows: list[dict], coverage: dict) -> bool:
    """Journal the write list as non-blocking ``POST /v1/runs/{id}/outputs``
    ops -- only to a server that declares ``run_outputs``. Does not touch the
    spools (:func:`_deliver` discards them once)."""
    if _server_takes(client, OUTPUTS_FEATURE) is not True:
        return False
    _journal_rows(client, run_id, "outputs", rows, coverage)
    return True


def _deliver(
    client: Any,
    run_id: str,
    got: Collected,
    *,
    reads: bool,
    writes: bool,
    observations: bool = False,
    keep_late: bool = False,
) -> None:
    """Journal the lists the server takes and the run did not opt out of, then
    drop the spools they came from. ``observations``: the server keys reads
    on their observation id (`OBSERVATIONS_FEATURE`); without it the ids are
    left out. ``keep_late``: what this close ran out of time to hash is kept
    for a later process to hash and re-send (`_keep_late`)."""
    sent_reads = reads and "inputs" not in got.opted_out
    sent_writes = writes and "outputs" not in got.opted_out
    if sent_reads:
        rows = got.inputs if observations else [_without_observation(r) for r in got.inputs]
        _journal_rows(client, run_id, "inputs", rows, got.inputs_coverage)
    if sent_writes:
        _journal_rows(client, run_id, "outputs", got.outputs, got.outputs_coverage)
    if keep_late and observations:
        _keep_late(run_id, [x for x in got.late if ("p" in x and sent_reads) or ("w" in x and sent_writes)])
    discard(run_id)


#: A close's leftovers for a later process: ``late.<host>.<pid>.json``.
_LATE_PREFIX = "late."


def _keep_late(run_id: str, late: list[dict]) -> None:
    """Keep what the close ran out of TIME to hash, beside the run's
    ``owner.json`` (which says which server and credential it is for), for
    the next process on this host to hash and re-send (`_resend_late`). Not
    what the budget cut: that was the run's to spend."""
    if not late:
        return
    path = run_dir(run_id) / f"{_LATE_PREFIX}{_host()}.{os.getpid()}.json"
    tmp = path.with_name(path.name + ".tmp")
    with internal(), contextlib.suppress(OSError):
        tmp.write_text(json.dumps({"run_id": run_id, "rows": late[: 2 * MAX_PATHS]}), encoding="utf-8")
        os.replace(tmp, path)


def _late_files(directory: Path) -> list[Path]:
    return sorted(directory.glob(f"{_LATE_PREFIX}{_host()}.*.json"))


def discard(run_id: str) -> None:
    """Delete the spools this process read (or may read) for ``run_id`` -- never
    a live process's -- and the run's folder once no spool is left in it and no
    live process has marked it."""
    spools = _consumed.pop(run_id, None)
    if spools is None:
        spools = _collectable_spools(run_id)
    directory = run_dir(run_id)
    with internal():
        for spool in spools:
            for path in (spool, _sidecar(spool)):
                with contextlib.suppress(OSError):
                    path.unlink()
        _drop_markers(directory)
        if (
            not any(directory.glob("*.jsonl"))
            and not _late_files(directory)
            and not _live_elsewhere(directory)
        ):
            shutil.rmtree(directory, ignore_errors=True)


def finalize(
    client: Any, run_id: str, *, wait_s: float = FINISH_WAIT_S, ignore: Any = None
) -> None:
    """Collect and send ``run_id``'s reads and writes. Never raises (but lets
    a Ctrl-C through): these lists are lineage evidence, never a reason to
    fail a run's close."""
    try:
        # Asked BEFORE hashing: against a server that cannot take a list,
        # hashing for it up to the run's budget would be work for nothing.
        # Unreachable, the spools stay for the next run on this machine to send.
        takes_reads = _server_takes(client, FEATURE)
        takes_writes = _server_takes(client, OUTPUTS_FEATURE) if _writes_noted(run_id) else False
        if takes_reads is None or takes_writes is None:
            _stop(run_id)
            return
        if not takes_reads and not takes_writes:
            _stop(run_id)
            discard(run_id)
            return
        got = collect_all(
            run_id, wait_s=wait_s, ignore=ignore, reads=takes_reads, writes=takes_writes
        )
        _deliver(
            client,
            run_id,
            got,
            reads=takes_reads,
            writes=takes_writes,
            observations=_server_takes(client, OBSERVATIONS_FEATURE) is True,
            keep_late=True,
        )
    except KeyboardInterrupt:
        # Ctrl-C while the close waits on hashing: stop waiting. The spools
        # stay, and the next run on this host sends them. Then the interrupt
        # goes on: swallowed here, the close it cut short went on to close the
        # run `completed`, as if nobody had pressed Ctrl-C; `Run.finish()`
        # queues `canceled` for it instead (review of #2016).
        _stop(run_id)
        _consumed.pop(run_id, None)
        _diagnostics.warn(f"probe: read capture for run {run_id} left for later (interrupted)")
        raise
    except Exception as exc:  # noqa: BLE001
        _diagnostics.warn(f"probe: read capture for run {run_id} not sent: {exc}")


def _read_owner(run_id: str) -> dict:
    try:
        with internal():
            owner = json.loads((run_dir(run_id) / "owner.json").read_text())
    except (OSError, ValueError):
        return {}
    return owner if isinstance(owner, dict) else {}


def _writes_noted(run_id: str, owner: dict | None = None) -> bool:
    """Whether ``run_id``'s writes were noted: this process's own recorder
    says, else whoever started recording it (``owner.json``). An owner record
    that does not say predates write capture."""
    state = _active.get(run_id)
    if state is not None:
        return state.writes
    owner = _read_owner(run_id) if owner is None else owner
    return owner.get("writes") is True


def abandon(run_id: str) -> None:
    """Stop recording ``run_id`` and leave its spools for recovery."""
    _stop(run_id)
    _consumed.pop(run_id, None)
from probe.sdk.capture.lineage.rows import _without_observation  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.capture.lineage.spool.reader import _collectable_spools, _sidecar  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.capture.lineage.spool.spool import MAX_PATHS, _drop_markers, _host, _live_elsewhere, internal, run_dir  # noqa: E402 -- pieces need each other; the front door loads this one first
