"""LineageGate: at delivery, hold or drop an offline run's queued read/write lists the server does not take."""

from __future__ import annotations
from typing import TYPE_CHECKING
import os
from pathlib import Path

from ... import errors
from ..journal.journal import Journal

if TYPE_CHECKING:
    from ...client.client import Client


def _lineage_feature(op: dict) -> str | None:
    """The feature a queued op needs when it is a run's read or write list
    (``POST /v1/runs/<ref>/inputs`` / ``.../outputs``), else None."""
    target = op.get("path")
    if op.get("method") != "POST" or not isinstance(target, str) or not target.startswith("/v1/runs/"):
        return None
    if target.count("/") != 4:
        return None
    route = target.rsplit("/", 1)[1]
    return next((feature for feature, name in LINEAGE_ROUTES.items() if name == route), None)


#: Lists `lineage_gate` dropped at delivery, by queue folder, for `sync_dir`.
_GATED: dict[str, dict[str, int]] = {}


def _take_gated(directory: Path) -> dict[str, int]:
    return _GATED.pop(os.path.realpath(directory), {})


def lineage_gate(journal: Journal, client: Client, op: dict) -> bool:
    """At DELIVERY (`journal._execute`, offline run's op): whether this op is a read or
    write list the server does not take and must be dropped. `sync_dir` filters the queue
    before its drain, but a recovery can append a list after; asking per op closes the gap.
    An unreachable server is not a no: the op is sent and fails as any would."""
    feature = _lineage_feature(op)
    if feature is None:
        return False
    try:
        if not client.supports_feature(feature):
            counts = _GATED.setdefault(os.path.realpath(journal.dir), {})
            counts[feature] = counts.get(feature, 0) + 1
            return True
        if feature == "run_inputs" and not client.supports_feature(_OBSERVATIONS_FEATURE):
            return _unobserved(journal, op)
    except errors.RosError:
        return False
    return False


#: The server keys a read on its observation id (0290), declared with
#: `run_outputs` (`inputs.OBSERVATIONS_FEATURE`).
_OBSERVATIONS_FEATURE = "run_outputs"
#: `_GATED`'s key for late hashes dropped at delivery.
_LATE = "late_hashes"


def _unobserved(journal: Journal, op: dict) -> bool:
    """A read list queued offline for a server that does not key reads on their observation
    id (0290): its rows go without the id, and a LATE re-send (tagged ``inputs.LATE_TAG``
    in the queue, F7) is dropped: such a server would keep its hashed rows beside the
    unhashed ones instead of replacing them. True when the op is dropped."""
    from ...capture.lineage.finishing import LATE_TAG

    body = op.get("body")
    if not isinstance(body, dict):
        return False
    if op.get("tag") == LATE_TAG:
        counts = _GATED.setdefault(os.path.realpath(journal.dir), {})
        counts[_LATE] = counts.get(_LATE, 0) + 1
        return True
    rows = body.get("inputs")
    if isinstance(rows, list):
        body["inputs"] = [
            {k: v for k, v in row.items() if k != "observation_id"} if isinstance(row, dict) else row
            for row in rows
        ]
    return False


def _drop_untaken_lineage(journal: Journal, client: Client) -> dict[str, int]:
    """Remove the queued read and write lists (``POST /v1/runs/<ref>/inputs``,
    ``.../outputs``) the SYNC server does not declare it takes: queued offline on the
    promise that this server decides (`OfflineClient.DEFERRED_FEATURES`); against one
    without the route each would dead-letter and leave the sync unclean. Returns
    {feature: lists dropped}."""
    dropped: dict[str, int] = {}
    for feature in LINEAGE_ROUTES:
        try:
            if client.supports_feature(feature):
                continue
        except errors.RosError:
            continue  # unreachable: the drain will say so
        for path, op in journal.pending():
            if _lineage_feature(op) == feature:
                try:
                    path.unlink()
                except OSError:
                    continue
                dropped[feature] = dropped.get(feature, 0) + 1
    return dropped
from probe.sdk.delivery.sinks.offline import LINEAGE_ROUTES  # noqa: E402 -- pieces need each other; the front door loads this one first
