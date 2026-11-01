"""Host a dataset in Probe via the upload doors: put the manifest, send what is missing (single PUT or multipart), wait until verified."""

from __future__ import annotations
import math
import mimetypes
import os
import time
from typing import TYPE_CHECKING, Any, Mapping

from .. import errors
from probe.sdk.catalog.manifest import ManifestFile
from probe.sdk.catalog.refs import CatalogRefused
from probe.sdk.catalog.server import human_bytes

if TYPE_CHECKING:  # pragma: no cover
    from probe.sdk.catalog.identity import Prepared

    from ..client.client import Client
#: The bound on one manifest PUT (up to 16 MB of gzip).
MANIFEST_SECONDS = 30.0
#: Bound on one hosting door call, retries included: it may open 500 multipart uploads
#: (8 store calls at a time) and sign 1,000 PUTs; asking again is safe (it resumes).
DOOR_SECONDS = 60.0
#: Fewest blobs one door call answers while any wait (server: 500 multipart uploads per call,
#: up to 1,000 in all): N blobs need at most ceil(N / 500) calls, plus `DOOR_SPARE_CALLS`.
DOOR_ANSWERS_AT_LEAST = 500
DOOR_SPARE_CALLS = 4
#: How long hosting waits for the server verifier (it hashes each large upload) per round, and the poll interval.
HOSTED_VERIFY_SECONDS = 3600.0
HOSTED_VERIFY_POLL_SECONDS = 5.0
HOSTED_PREFIX = ".probe/datasets/"


# Hosting (C8)


def door_call_limit(blobs: int) -> int:
    """Most door calls one `host` makes for ``blobs`` distinct blobs: each call answers at
    least `DOOR_ANSWERS_AT_LEAST` still to send, plus `DOOR_SPARE_CALLS`."""
    return max(1, math.ceil(max(0, blobs) / DOOR_ANSWERS_AT_LEAST)) + DOOR_SPARE_CALLS


def host(
    client: "Client", name: str, prepared: Prepared, *, progress: Any = None, say: Any = None
) -> dict:
    """Put the manifest, then ask the door for what Probe lacks, round by round: send each
    round (a PUT + confirm each, or the multipart doors), wait for the large ones to verify,
    repeat until the door's `deferred` is 0, within `door_call_limit` calls. Returns
    ``{have, sent, rounds}`` (``have``: blobs Probe held before round one).
    ``progress(n, total, file)`` runs per file sent; ``say(line)`` once per round of a
    multi-round manifest and before a verification wait. Raises what the server raised
    (402 `hosted_data_bytes` over the cap) and `CatalogRefused` for an upload Probe refused
    or never verified."""
    manifest = prepared.manifest
    if manifest is None or prepared.local is None:
        raise CatalogRefused("only a local file or folder can be hosted")
    from ..delivery.transport.deadlines import deadline_scope

    digest = manifest.identity()
    with deadline_scope(time.monotonic() + MANIFEST_SECONDS):
        client.put_manifest(digest, manifest.gz())
    by_hash: dict[str, ManifestFile] = {}
    for f in manifest.files:
        if f.content_hash:
            by_hash.setdefault(f.content_hash, f)
    limit = door_call_limit(len(by_hash))
    sent: set[str] = set()
    have: list[str] | None = None
    total = 0
    for round_no in range(1, limit + 1):
        with deadline_scope(time.monotonic() + DOOR_SECONDS):
            answer = client.host_dataset_uploads(name, digest) or {}
        uploads = [u for u in answer.get("uploads") or [] if isinstance(u, Mapping)]
        deferred = answer.get("deferred")
        deferred = deferred if isinstance(deferred, int) and not isinstance(deferred, bool) and deferred > 0 else 0
        if have is None:
            have = [str(h) for h in answer.get("have") or []]
            total = len(uploads) + deferred
        # An already-sent upload comes back only while Probe verifies it; never sent twice.
        fresh = [u for u in uploads if u.get("content_hash") not in sent]
        files: list[tuple[Mapping[str, Any], ManifestFile]] = []
        for item in fresh:
            f = by_hash.get(str(item.get("content_hash")))
            if f is None:
                raise CatalogRefused(
                    f"the upload door asked for {item.get('content_hash')}, which this manifest does not name"
                )
            files.append((item, f))
        if callable(say) and (deferred or round_no > 1):
            size = sum(_declared_size(item, f) for item, f in files)
            say(f"hosting round {round_no}: {len(files):,} file(s) to send ({human_bytes(size)}), "
                f"{deferred:,} more after this round")
        verifying: list[tuple[str, ManifestFile]] = []
        for item, f in files:
            sent.add(str(f.content_hash))
            if callable(progress):
                progress(len(sent), max(total, len(sent)), f)
            upload_id = _upload_blob(client, item, f, name=name, manifest_hash=digest)
            if upload_id:
                verifying.append((upload_id, f))
        # Before the next call: a large blob is hosted only once verified; until then the door
        # re-answers it and registration counts it missing.
        _await_verified(client, verifying, say=say)
        if not deferred:
            return {"have": have, "sent": len(sent), "rounds": round_no}
    raise CatalogRefused(
        f"the hosting door still had files to send after {limit} calls ({len(sent):,} sent); "
        "nothing was registered: run it again to send the rest (what was sent is kept)"
    )


def _declared_size(item: Mapping[str, Any], f: ManifestFile) -> int:
    """The size the door reserved for a blob, else the manifest's."""
    size = item.get("size_bytes")
    return size if isinstance(size, int) and not isinstance(size, bool) else f.size_bytes


def _upload_blob(
    client: "Client", item: Mapping[str, Any], f: ManifestFile, *, name: str, manifest_hash: str
) -> str | None:
    """Send one blob the door asked for. Returns the multipart upload id of a large one
    (verified after), None for a confirmed PUT. ``name``/``manifest_hash`` are the door
    call's, in case a large upload must reopen."""
    content_type = mimetypes.guess_type(f.relpath)[0] or "application/octet-stream"
    if item.get("multipart"):
        return _upload_parts(client, item, f, name=name, manifest_hash=manifest_hash)
    url = item.get("url")
    if not url:
        raise CatalogRefused(f"the upload door named no upload for {f.relpath}")
    client.transport.put_file(
        url, f.full, content_type=content_type, headers=item.get("headers") or item.get("upload_headers")
    )
    artifact_id = item.get("artifact_id")
    if artifact_id:
        confirm = str(item.get("confirm") or item.get("confirm_path") or "")
        try:
            client.confirm_hosted_blob(str(artifact_id), shared=confirm.startswith("/v1/shared/files/"))
        except errors.ConflictError as exc:
            # E.g. the stored object is LARGER than the size the door reserved (its cap check
            # trusted that size): never confirmed, so nothing can register it.
            raise CatalogRefused(
                f"Probe refused the upload of {f.relpath} ({human_bytes(_declared_size(item, f))} "
                f"reserved): {exc}. Did it change after it was hashed? Run it again."
            ) from exc
    return None


def _upload_parts(
    client: "Client", item: Mapping[str, Any], f: ManifestFile, *, name: str, manifest_hash: str
) -> str | None:
    """A blob over the single-PUT ceiling, via the multipart client at the Shared anchor:
    the door already opened (or resumed) the upload, so the op starts with its id and goes
    straight to parts and complete. A given-up upload is reopened by the door, never the
    generic create (`reopen_hosted`). Returns the upload id Probe verifies after, or None
    if the blob was hosted already."""
    from ..artifact.storage_handlers import multipart
    from ..artifact.anchors import Anchor

    spec = item["multipart"] if isinstance(item.get("multipart"), dict) else {}
    upload_id = spec.get("upload_id")
    if not upload_id or not spec.get("part_size") or not spec.get("part_count"):
        raise CatalogRefused(f"the upload door's multipart answer for {f.relpath} names no upload")
    st = os.stat(f.full)
    op = {
        "op_id": f"hosted-{f.content_hash}",
        "multipart": {
            "staged_path": f.full,
            "stage_mode": "none",
            "identity": multipart._identity(st),
            "staged_at": time.time(),
            "upload_id": upload_id,
            "artifact_id": item.get("artifact_id") or spec.get("artifact_id"),
            "part_size": spec["part_size"],
            "part_count": spec["part_count"],
            "state": spec.get("state") or "uploading",
        },
        "upload": {
            "anchor": Anchor.SHARED.value,
            "anchor_id": None,
            "name": f"{HOSTED_PREFIX}{f.content_hash}",
            "src_path": f.full,
            "blob": f.content_hash,
            "size_bytes": f.size_bytes,
            # Which door opens it again (`multipart._create`).
            "hosted": {"name": name, "manifest_hash": manifest_hash},
        },
    }
    multipart.advance(client, op, lambda: None, deadline=float("inf"), wait_for_verify=False)
    state = op["multipart"]
    if state.get("state") == "have":
        return None
    # A restart opened a new upload: that one is what Probe verifies.
    return str(state.get("upload_id") or upload_id)


def reopen_hosted(client: "Client", upload: Mapping[str, Any]) -> dict:
    """Reopen a hosted blob's large upload, in the multipart create's answer shape
    (`multipart._create`), after Probe gave up on the first (e.g. idle past its sweep).
    Its name `.probe/datasets/<sha256>` may only be staged by the hosting door (the generic
    Shared create refuses it, 422), so the door is asked again: it re-stages and answers a
    fresh `multipart`, or lists it under `have` if hosted by now."""
    from ..delivery.transport.deadlines import deadline_scope

    door, blob = upload["hosted"], str(upload.get("blob"))
    with deadline_scope(time.monotonic() + DOOR_SECONDS):
        answer = client.host_dataset_uploads(door["name"], door["manifest_hash"]) or {}
    if blob in [str(h) for h in answer.get("have") or []]:
        return {"have": True, "artifact_id": None}
    item = next(
        (u for u in answer.get("uploads") or [] if isinstance(u, Mapping) and u.get("content_hash") == blob),
        None,
    )
    spec = item.get("multipart") if item is not None else None
    if not (isinstance(spec, Mapping) and spec.get("upload_id") and spec.get("part_size") and spec.get("part_count")):
        raise CatalogRefused(
            f"the hosting door did not open the upload of blob {blob} again; nothing was registered: "
            "run it again (what was sent is kept)"
        )
    return {
        "upload_id": spec["upload_id"],
        "artifact_id": item.get("artifact_id"),
        "part_size": spec["part_size"],
        "part_count": spec["part_count"],
        "state": spec.get("state") or "uploading",
    }


def _await_verified(client: "Client", waiting: list[tuple[str, ManifestFile]], *, say: Any = None) -> None:
    """Wait, within `HOSTED_VERIFY_SECONDS`, until every large upload in ``waiting`` is `verified`
    (hosted). The server verifier hashes them one after another, so they are waited for in turn."""
    if not waiting:
        return
    from ..artifact.storage_handlers import multipart
    from ..artifact.anchors import Anchor

    if callable(say):
        size = sum(f.size_bytes for _id, f in waiting)
        say(f"waiting for Probe to verify {len(waiting):,} large file(s) ({human_bytes(size)})")
    shared = {"anchor": Anchor.SHARED.value}
    deadline = time.monotonic() + HOSTED_VERIFY_SECONDS
    for upload_id, f in waiting:
        while True:
            status = multipart._status(client, shared, upload_id) or {}
            state = status.get("state")
            if state == "verified":
                break
            if state != "verifying":
                raise CatalogRefused(
                    f"Probe could not verify the upload of {f.relpath}: it is {state or 'gone'} "
                    f"({status.get('failure_reason') or 'no reason given'}); nothing was registered: run it again"
                )
            if time.monotonic() >= deadline:
                raise CatalogRefused(
                    f"Probe was still verifying {f.relpath} after {HOSTED_VERIFY_SECONDS:g}s; nothing was "
                    "registered: run it again later to register it (the upload is kept)"
                )
            time.sleep(HOSTED_VERIFY_POLL_SECONDS)
