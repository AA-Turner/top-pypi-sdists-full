"""CodeFilesMixin, Run's methods: store the code files git cannot supply as one artifact row per
file, in parallel windows."""

from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import time
from datetime import datetime, timezone

from ....foundation.safe_warn import safe_warn as _diagnostics
from ... import errors
from ...secret_gate import (
    CredentialBlocked,
    check_upload)
from ...capture import code as _snapshot
#: The half-failed outage rule needs a window at least this big; below it only
#: a window that failed entirely is an outage.
OUTAGE_MIN_WINDOW = 8
#: Presign -> PUT -> confirm happens in windows of this many files, so a client
#: that dies mid-upload strands at most one window of pending rows for the
#: server's reaper, not a whole 7,942-file tree. Must stay <= the server's
#: confirm cap (500): one window is one confirm call.
CAPTURE_WINDOW = 256
#: Concurrent presigned PUTs per window.
CAPTURE_PUT_WORKERS = 16


class CodeFilesMixin:
    """Part of Run: its methods run with `self` the Run; compose() folds them into Run."""

    def _upload_pending_files(
        self,
        root: str,
        pending: list[dict],
        *,
        strict: bool | None,
        max_upload_bytes: int,
    ) -> dict:
        """Store the files git cannot supply as one artifact row PER FILE.

        Windows of ``CAPTURE_WINDOW``: presign the window (the server dedupes on
        content and answers ``have`` for bytes it already holds), PUT the misses
        ``CAPTURE_PUT_WORKERS`` wide against checksum-pinned URLs, confirm, retry
        the unconfirmed ONCE with fresh URLs, then the next window. Symlinks are
        never uploaded: the manifest carries their target and restore writes
        them from it.

        Every byte that leaves the machine was verified first: the file is opened
        the way the archive path opens it (``snapshot.open_verified_file`` --
        ``O_NOFOLLOW``, size and sha re-checked on the descriptor) and that same
        descriptor is streamed. A file that drifted since the manifest is
        reported ``changed``, never sent. The whole tree is bounded by
        ``max_upload_bytes`` exactly like the archive (``SnapshotTooLarge``).

        Fail-open exactly like the archive path: a server error stops the
        upload, warns, and the returned ``pending_upload`` is every file whose
        bytes did not land -- so ``check_run`` still reads the run as not
        reproducible. Three things stop the walk early, each with one warning
        and the rest named as unstored: a window whose PUTs all fail against
        storage (or half of a window of ``OUTAGE_MIN_WINDOW`` or more), a
        window storage rejects outright, and ``CAPTURE_DEADLINE_SECONDS``
        elapsing. Under ``strict=True`` any file that storage failed to take
        (not one that drifted on disk) raises at the end. Every file that is
        not stored is listed in
        ``unstored`` with a reason so a reader can see WHICH files, not just how
        many; the list is capped, the count is not.

        Returns ``{"fallback": "archive"}`` when the first presign answers
        404/405: the server predates the batch doors and the caller stores the
        archive instead.
        """
        files = [e for e in pending if e.get("mode") != "120000"]
        n_symlinks = len(pending) - len(files)
        total = sum(int(e.get("size") or 0) for e in files)
        if total > max_upload_bytes:
            raise _snapshot.SnapshotTooLarge(
                f"pending files total {total} bytes, above the {max_upload_bytes}-byte "
                "cap; raise --max-upload-mb or add the large paths to .gitignore/a "
                "reference rule rather than shipping a partial capture"
            )
        captured_at = datetime.now(timezone.utc).isoformat()
        stored: set[str] = set()
        unstored: dict[str, str] = {}  # path -> reason; sorted and capped on the way out
        n_uploaded = n_deduped = 0
        client = self._client

        def _wire_name(path: str) -> str:
            # NFC (the server canonicalises to it and echoes that form) with
            # POSIX separators; the manifest keeps the path as the filesystem
            # spelled it.
            return _snapshot.wire_name(path)

        def _mark_stored(path: str) -> None:
            stored.add(path)
            unstored.pop(path, None)

        def _result(reason: str | None = None) -> dict:
            missing = [e["path"] for e in files if e["path"] not in stored]
            for p in missing:
                # A file no verdict ever named was never reached: the upload
                # stopped (a server error, an outage) before its window. Files
                # whose window WAS in flight carry their own reason already.
                unstored.setdefault(p, "upload stopped before this file")
            listed = sorted(unstored.items())
            return {
                "uploaded": bool(stored),
                "pending_upload": len(missing),
                "storage": CODE_STORAGE_ARTIFACTS,
                **({"reason": reason} if reason else {}),
                "n_files": len(stored),
                "n_uploaded": n_uploaded,
                "n_deduped": n_deduped,
                "n_symlinks": n_symlinks,
                "unstored": [
                    {"path": p, "reason": r} for p, r in listed[: _snapshot.DRIFTED_META_LIMIT]
                ],
                "captured_at": captured_at,
            }

        if not files:
            return _result("nothing to upload")

        drifted_paths: set[str] = set()  # the tree moved: named, never a strict failure

        def _put(entry: dict, out: dict) -> tuple[str, str | None, str]:
            """Verify, then stream. Returns (path, error, kind) where kind is
            ``ok`` | ``drift`` (never sent) | ``rejected`` (storage said no:
            not retried) | ``refused`` (the local credential gate said no: not
            retried, never an outage) | ``transport`` (network / 5xx: retried
            once)."""
            path = entry["path"]
            try:
                verdict, fh = _snapshot.open_verified_file(root, entry)
            except _snapshot.SnapshotError as exc:
                return path, str(exc), "drift"
            if verdict != "ok" or fh is None:
                return path, f"{verdict} since the manifest was taken", "drift"
            with fh:
                try:
                    client.transport.put_fileobj(
                        out["upload_url"],
                        fh,
                        size=int(entry["size"]),
                        content_type="application/octet-stream",
                        headers=out.get("upload_headers") or None,
                    )
                except CredentialBlocked as exc:
                    # THIS machine's gate said no (the file grew past the
                    # inspection limit, or moved under the stream): storage
                    # never saw it. Checked before RosError, which it is.
                    return path, f"refused by the credential gate: {_gate_reason(exc)}", "refused"
                except errors.TransportError as exc:
                    return path, _redact_signed(str(exc)), "transport"
                except errors.RosError as exc:
                    status = exc.status or 0
                    throttled = status in (408, 429)
                    return (
                        path,
                        _redact_signed(str(exc)),
                        "transport" if status >= 500 or throttled else "rejected",
                    )
                except Exception as exc:  # noqa: BLE001 -- reported per file below
                    return path, _redact_signed(str(exc)), "transport"
            return path, None, "ok"

        def _presign(entries: list[dict]) -> dict:
            # Path and size only: this path never calls `prepare_upload`, and a
            # snapshot must not be redacted anyway. The CONTENT was scanned when
            # the manifest was built (snapshot._ContentGate), and `_put` streams
            # only bytes whose sha256 still matches that record.
            for entry in entries:
                check_upload(os.path.join(root, entry["path"]))
            items = [
                {
                    "name": _wire_name(e["path"]),
                    "content_hash": e["sha256"],
                    "size_bytes": int(e.get("size") or 0),
                    "mode": "100755" if e.get("mode") == "100755" else "100644",
                }
                for e in entries
            ]
            return client.presign_capture_batch(self.id, items, captured_at=captured_at)

        twins: dict[str, list[str]] = {}  # artifact id -> extra paths it also serves

        def _paths_for(aid: str) -> list[str]:
            return [need[aid][0]["path"], *twins.get(aid, ())]

        def _take_slots(entries: list[dict], presigned: dict, need: dict) -> None:
            """Join the server's answer to the window BY POSITION (the server
            guarantees one slot per item, in order); a missing or empty slot is
            a verdict of its own, never a silent success."""
            slots = presigned.get("items") or []
            for idx, entry in enumerate(entries):
                nonlocal n_deduped
                path = entry["path"]
                out = slots[idx] if idx < len(slots) else None
                if not isinstance(out, dict):
                    unstored[path] = "no verdict from storage"
                    continue
                if out.get("error"):
                    unstored[path] = str(out["error"])
                    continue
                if out.get("have"):
                    n_deduped += 1
                    _mark_stored(path)
                    continue
                aid, url = out.get("artifact_id"), out.get("upload_url")
                if not aid or not url:
                    unstored[path] = "no verdict from storage"
                    continue
                if aid in need:
                    # Two manifest paths that normalise to ONE name with the same
                    # bytes (an NFC and an NFD spelling of the same file) share one
                    # row: upload it once, and give every spelling the verdict.
                    twins.setdefault(aid, []).append(path)
                    continue
                need[aid] = (entry, out)

        deadline = _capture_deadline()
        started_at = time.monotonic()

        def _check_deadline() -> None:
            if time.monotonic() - started_at >= deadline:
                raise errors.TransportError(f"capture deadline of {deadline:.0f}s reached")

        try:
            for start in range(0, len(files), CAPTURE_WINDOW):
                _check_deadline()
                window = files[start : start + CAPTURE_WINDOW]
                try:
                    presigned = _presign(window)
                except errors.RosError as exc:
                    if start == 0 and exc.status in (404, 405):
                        return {"fallback": CODE_STORAGE_ARCHIVE, "reason": "no batch doors"}
                    raise
                need: dict[str, tuple[dict, dict]] = {}  # artifact_id -> (entry, item_out)
                _take_slots(window, presigned, need)

                pending_ids = list(need)
                for attempt in (1, 2):
                    if not pending_ids:
                        break
                    if attempt == 2:
                        _check_deadline()
                        # Fresh URLs for the stragglers: a presigned PUT expires,
                        # and the server hands the same rows back for the same
                        # identities. A `have` on the retry means another run
                        # stored those bytes meanwhile.
                        retry_entries = [need[aid][0] for aid in pending_ids]
                        fresh: dict[str, tuple[dict, dict]] = {}
                        _take_slots(retry_entries, _presign(retry_entries), fresh)
                        for aid in list(pending_ids):
                            if aid in fresh:
                                need[aid] = fresh[aid]
                            else:
                                # Stored (`have`), or a verdict already recorded
                                # for the primary spelling: its twins follow it.
                                primary = need[aid][0]["path"]
                                for p in twins.get(aid, ()):
                                    if primary in stored:
                                        _mark_stored(p)
                                    else:
                                        unstored[p] = unstored.get(
                                            primary, "no verdict from storage"
                                        )
                                pending_ids.remove(aid)
                        if not pending_ids:
                            break
                    failed_put: dict[str, tuple[str, str]] = {}  # aid -> (kind, error)
                    pool = ThreadPoolExecutor(max_workers=CAPTURE_PUT_WORKERS)
                    try:
                        futures = {pool.submit(_put, *need[aid]): aid for aid in pending_ids}
                        for fut in as_completed(futures):
                            _path, error, kind = fut.result()
                            if error is None:
                                # The bytes are in the store; only a confirm
                                # makes them a file of this run. Recorded now
                                # so a confirm that never returns is named as
                                # what it is, not as "never attempted".
                                for p in _paths_for(futures[fut]):
                                    unstored[p] = "uploaded, not confirmed by storage"
                            else:
                                failed_put[futures[fut]] = (kind, error)
                    except BaseException:
                        # Ctrl-C mid-window: the queued PUTs must not run to
                        # completion behind the user's back.
                        pool.shutdown(wait=False, cancel_futures=True)
                        raise
                    else:
                        pool.shutdown(wait=True)
                    for aid, (kind, error) in failed_put.items():
                        for path in _paths_for(aid):
                            if kind == "drift":
                                drifted_paths.add(path)
                                unstored[path] = error
                            elif kind == "rejected":
                                unstored[path] = f"upload rejected: {error}"
                            elif kind == "refused":
                                unstored[path] = error
                            else:
                                unstored[path] = f"upload failed: {error}"
                    to_confirm = [aid for aid in pending_ids if aid not in failed_put]
                    unconfirmed: list[str] = []
                    if to_confirm:
                        result = client.confirm_capture_batch(to_confirm)
                        seen: set[str] = set()
                        for aid in result.get("confirmed") or []:
                            if aid in need:
                                seen.add(aid)
                                n_uploaded += 1
                                for p in _paths_for(aid):
                                    _mark_stored(p)
                        for aid in result.get("unconfirmed") or []:
                            if aid in need:
                                seen.add(aid)
                                unconfirmed.append(aid)
                                for p in _paths_for(aid):
                                    unstored[p] = "not confirmed by storage"
                        # Only `unconfirmed` (HEAD did not see the object yet)
                        # is worth a second PUT + confirm. The other buckets
                        # are verdicts: `refused` is a live row that is not a
                        # capture row (the researcher registered that name
                        # and bytes on purpose), `failed` is a row the upload
                        # reaper gave up on, `unknown` has no live row.
                        for bucket, reason in (
                            ("refused", "already an artifact of this run, not captured"),
                            ("failed", "reaped by storage before the upload landed"),
                            ("unknown", "no live artifact row for this file"),
                        ):
                            for aid in result.get(bucket) or []:
                                if aid in need:
                                    seen.add(aid)
                                    for p in _paths_for(aid):
                                        unstored[p] = reason
                        for aid in to_confirm:
                            if aid not in seen:
                                if attempt == 1:
                                    unconfirmed.append(aid)
                                else:
                                    for p in _paths_for(aid):
                                        unstored[p] = "no verdict from storage"
                    transport_failed = [a for a, (k, _) in failed_put.items() if k == "transport"]
                    rejected = [a for a, (k, _) in failed_put.items() if k == "rejected"]
                    if attempt == 1 and len(pending_ids) >= 2:
                        # Evaluated AFTER the confirm so the PUTs that landed are
                        # banked before the walk stops. Every PUT in a window
                        # failed against storage on the first pass -- or, in a window of OUTAGE_MIN_WINDOW or
                        # more, at least half of them: that is an outage, not
                        # 128 individual mishaps, and a flaky link must not be
                        # walked for hours. A window storage REJECTED outright
                        # (a proxy that strips the checksum header, a bucket
                        # policy) is the same verdict. (The retry pass is only
                        # the stragglers; two flaky files in a small window
                        # are retried, not declared an outage.)
                        all_failed = len(transport_failed) == len(pending_ids)
                        half_failed = len(pending_ids) >= OUTAGE_MIN_WINDOW and len(
                            transport_failed
                        ) * 2 >= len(pending_ids)
                        if all_failed or half_failed:
                            first = failed_put[transport_failed[0]][1]
                            raise errors.TransportError(f"storage unreachable: {first}")
                        if len(rejected) == len(pending_ids):
                            first = failed_put[rejected[0]][1]
                            raise errors.TransportError(
                                f"storage rejected every upload in this window: {first}"
                            )
                    # Every verdict above was recorded as it happened and a
                    # later success pops it, so the second pass needs no
                    # bookkeeping of its own: whatever is still named after it
                    # is the final word.
                    pending_ids = transport_failed + unconfirmed
        except errors.RosError as exc:
            if strict is True or (strict is None and not client.fail_open):
                raise
            out = _result("upload failed")
            _diagnostics.warn(
                f"code capture stopped after {len(stored)} of {len(files)} files "
                f"({_redact_signed(str(exc))}); {out['pending_upload']} remain unstored and "
                "this run is not reproducible from the record alone.",
                stacklevel=3,
            )
            return out

        out = _result()
        if out["unstored"]:
            first = out["unstored"][0]
            message = (
                f"{out['pending_upload']} of {len(files)} captured files could not be stored "
                f"(first: {first['path']}: {first['reason']}); this run is not fully "
                "reproducible from the record alone."
            )
            # `strict` means "raise if my code was not saved": a file STORAGE
            # failed to take (a rejected or failed PUT, a refused name, a
            # confirm that never came back) raises; a file that changed on
            # disk while it was read is the tree moving, and stays a warning.
            storage_failed = [u for u in out["unstored"] if u["path"] not in drifted_paths]
            if storage_failed and (strict is True or (strict is None and not client.fail_open)):
                raise errors.RosError(message)
            _diagnostics.warn(message, stacklevel=3)
        return out
from probe.sdk.run.files.code_upload import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    CODE_STORAGE_ARCHIVE,
    CODE_STORAGE_ARTIFACTS,
    _capture_deadline,
    _redact_signed,
)
from probe.sdk.run.files.files import _gate_reason  # noqa: E402 -- pieces need each other; the front door loads this one first
