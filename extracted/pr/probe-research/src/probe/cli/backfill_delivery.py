"""Join validated file intentions to the SDK's receipt-required uploader."""

from __future__ import annotations

import json
import mimetypes
from pathlib import Path

from ..sdk.client import Anchor
from ..sdk.journal import OutboxFull
from .backfill_coverage import Coverage
from .backfill_manifest import validate_manifest


def ingest_manifests(coverage: Coverage, folder: Path, outcomes) -> tuple[list[str], list[str]]:
    """Retain each independently valid row; invalid output cannot authorize writes.

    Returns ``(touched_paths, errors)``. The paths are what lets a caller act on
    just this unit afterwards: without them the only way to see the result is to
    re-read the whole file table, which is what made the resume loop
    O(units x files).
    """
    touched: list[str] = []
    errors = []
    for outcome in outcomes:
        if not outcome.manifest:
            continue
        checked = validate_manifest(outcome.manifest, outcome.unit.paths, root=folder)
        if not checked.complete:
            errors.append(f"{outcome.unit.unit_id}: {checked.describe()}")
        for row in checked.rows:
            coverage.remember_manifest(row["path"], row)
            touched.append(row["path"])
    return touched, errors


def enqueue(coverage: Coverage, client, folder: Path, *, paths=None) -> tuple[int, list[str]]:
    """Persist intent before enqueue; a queue acknowledgment is not a receipt.

    ``paths`` narrows this to one unit's files so delivery can start while later
    units are still being read, instead of waiting for the last agent to finish
    and then uploading the whole folder in one serial pass at the end.

    A full staging area is BACKPRESSURE, not a per-file failure. The outbox
    snapshots every upload before it is queued, so a fast producer can outrun
    the drain; recording that as an error would permanently mark files the next
    pass would have queued without trouble. Nothing is written for them, so the
    next per-unit call -- or the final flush -- simply tries again.
    """
    count = 0
    errors = []
    if paths is None:
        candidates = coverage.rows()
        covered = coverage.report()
        skip = set(covered["delivered"] + covered["references"])
    else:
        # Scoped to one unit, so the whole-folder report is the wrong question
        # AND the expensive one: it is a files-join-versions scan over every
        # row, and this now runs once per finished unit. `delivered_paths` asks
        # only about the handful of paths in hand.
        found = coverage.rows_for(paths)
        candidates = [found[path] for path in dict.fromkeys(paths) if path in found]
        skip = coverage.delivered_paths(paths)
    for row in candidates:
        if (row["path"] in skip or not row["present"] or not row["manifest"]
                or row["approved_hash"] != row["observed_hash"] or row["observation_error"]):
            continue
        manifest = json.loads(row["manifest"])
        reference = manifest.get("reference", False)
        source = folder / row["path"]
        intent = coverage.intend(row, reference=reference,
                                 uri=source.resolve().as_uri() if reference else None)
        correlation = intent["correlation"]
        try:
            previous = client.delivery_state(correlation)
            common = {"correlation": correlation, "anchor": Anchor.PROJECT,
                      "anchor_id": row["project_id"], "name": intent["artifact_name"],
                      "notes": manifest.get("notes"),
                      "content_type": mimetypes.guess_type(row["path"])[0],
                      "meta": {"backfill": {"schema": "2", "source_id": coverage.source_id,
                                             "relative_path": row["path"],
                                             "content_hash": row["approved_hash"]}}}
            if previous["state"] != "unknown":
                result = client.resume_delivery(correlation)
            elif reference:
                # A reference uploads no bytes, so this check is the ONLY thing
                # standing between a moved file and a pointer to the wrong one.
                # It goes through `verified_hash` so it cannot end up with a
                # weaker rule than the census that approved the file.
                digest, size, _ = coverage.verified_hash(folder, row["path"])
                if digest != row["approved_hash"] or size != row["size"]:
                    raise ValueError("Reference source changed after its approved census")
                result = client.enqueue_artifact_reference(
                    **common, uri=intent["uri"], content_hash=row["approved_hash"], size_bytes=row["size"])
            else:
                result = client.enqueue_artifact_upload(
                    **common, path=source, expected_content_hash=row["approved_hash"])
            if result["state"] == "delivered":
                receipt = client.delivery_receipt(correlation)
                if not receipt:
                    raise ValueError("Uploader reported delivery without its durable receipt")
                coverage.accept_receipt(correlation, receipt)
            elif result["state"] == "queued":
                coverage.enqueued(correlation)
                count += 1
            else:
                raise ValueError(result.get("error") or f"Upload is {result['state']}; retry the unresolved operation")
        except OutboxFull:
            # Backpressure. Record nothing and stop: every later row in this
            # pass would hit the same wall, and the drain needs the disk back
            # more than the queue needs another intent.
            errors.append(
                "Local staging is full; queued uploads must drain before more files are added."
            )
            break
        except Exception as exc:
            coverage.failure(correlation, str(exc))
            errors.append(f"{row['path']}: {str(exc)[:512]}")
    return count, errors


def lines(coverage: Coverage, *, incomplete_walk: bool = False) -> list[str]:
    report = coverage.report()
    unfinished = sum(len(report[key]) for key in ("new", "changed", "queued", "unresolved"))
    result = [
        f"{len(report['delivered']):,} files delivered with verified bytes · "
        f"{len(report['references']):,} references recorded · {len(report['queued']):,} queued.",
        f"{len(report['excluded']):,} excluded · {len(report['new']):,} new · "
        f"{len(report['changed']):,} changed pending review · {len(report['unresolved']):,} unresolved.",
    ]
    if report["dead"]:
        # Named separately from `unfinished`: these will not be retried by
        # re-running, so reporting them as "partial, re-run" would promise a
        # recovery that never comes. `--retry-dead` is the one that does.
        result.append(
            f"{len(report['dead']):,} file(s) failed every attempt and were not imported; "
            "the per-file report says why. Re-run with `--retry-dead` to plan them again."
        )
    if report["vanished"]:
        result.append(f"{len(report['vanished']):,} previously observed files are absent; any existing remote records are retained.")
    if unfinished or incomplete_walk:
        result.append("Backfill is partial. Re-run to recover delivery and review remaining work.")
    elif report["references"]:
        result.append("All observed files are accounted for. References record pointers; their source bytes were not uploaded.")
    else:
        result.append("Every observed file has a receipt matching its verified current bytes.")
    result.append(f"Per-file report: {coverage.write_report()}")
    result.append(f"Source ID: {coverage.source_id}")
    return result
