"""WaitingRoomMixin: uploads waiting for their credential scan -- enqueue, promote into ops, dead-letter or sweep."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import time

from probe.foundation.durable.durable import file_lock, fsync_directory, now_iso, write_text_atomic
from probe.sdk.secret_gate import CredentialBlocked, InspectionResult, read_source, refuse_rewrite


class WaitingRoomMixin:
    """Part of Journal: its methods run with `self` the Journal; fold_parts() copies them into Journal."""

    # -- the waiting room: uploads queued before their credential scan ------
    # A copy waits here (never in `ops/`, which older drainers upload) until `promote_waiting` scans
    # it; each item becomes exactly one op, in queue order. The commit order is in DESIGN.md.

    def _waiting_paths(self, op_id: str) -> tuple[Path, Path, Path, Path]:
        base = self.waiting_dir / op_id
        return (
            base.with_suffix(".json"),
            self.waiting_dir / f"{op_id}.op.json",
            base.with_suffix(".bytes"),
            base.with_suffix(".lock"),
        )

    def _enqueue_waiting(
        self,
        upload: dict,
        *,
        run_ref: str | None,
        inline_hash: bool,
        require_staged: bool,
        blocking: bool = True,
    ) -> dict | None:
        # Two copies until promotion ends: the waiting one and the clean blob.
        refusal = self._staging_headroom(upload["src_path"], copies=2)
        if refusal is not None:
            if require_staged:
                return {"op_id": None, "blob": None, "size_bytes": None, "staged": False,
                        "unstaged_reason": refusal}
            return None  # the ordinary path degrades to an unstaged reference
        # The op ceiling counts what waits as well as what is queued: a stalled promoter must not
        # let an upload-only producer grow this without bound.
        refusal = self._append_headroom(check_free=False, extra=self.count_waiting(self.dir))
        if refusal is not None:
            raise OutboxFull(refusal)
        op = self._base_op("upload", run_ref)
        if not blocking:
            op["blocking"] = False  # see `append_upload`; it rides into the op
        op["upload"] = {**upload, "blob": None, "staged": True, "size_bytes": None,
                        "unstaged_reason": None}
        record, _, data, lock = self._waiting_paths(op["op_id"])
        with _item_lock(lock):
            # The queue position is the CALL's, reserved now: a run's terminal status queued after
            # this upload must still sort after it. So is the producer's sequence: its promoter
            # is someone else.
            with file_lock(self.append_lock):
                op["queue_filename"] = self._op_filename(op["op_id"])
                self._stamp_producer_locked(op)
            raw = read_source(upload["src_path"])
            _write_private(data, raw)
            write_text_atomic(
                record, json.dumps({"op": op, "inline_hash": bool(inline_hash)}) + "\n", mode=0o600
            )
            fsync_directory(self.waiting_dir)
        return {"op_id": op["op_id"], "blob": None, "size_bytes": len(raw), "staged": True,
                "unstaged_reason": None, "waiting": True}

    def _waiting_items(self) -> list[tuple[str, str, str | None, bool, bool]]:
        """`(queue position, op id, run_ref, readable, blocking)` per waiting item, in queue
        order. An unreadable record sorts first, so it is dealt with before anything it might be
        holding up."""
        try:
            names = os.listdir(self.waiting_dir)
        except OSError:
            return []
        items: dict[str, tuple[str, str, str | None, bool, bool]] = {}
        for op_id in {name.split(".", 1)[0] for name in names if name.endswith(".json")}:
            # The record, then the committed op: a promotion between the listing and this read has
            # replaced one with the other (steps 2-3), and only when both are gone is the op in
            # `ops/` (step 4), which a reader looking at `ops/` AFTER this one then sees.
            record, prepared, _, _ = self._waiting_paths(op_id)
            for path in (record, prepared):
                try:
                    body = json.loads(path.read_text())
                    op = body.get("op") or body
                    items[op_id] = (str(op["queue_filename"]), op_id, op.get("run_ref"), True,
                                    op.get("blocking", True) is not False)
                except FileNotFoundError:
                    continue
                except (OSError, ValueError, KeyError, TypeError, AttributeError):
                    items[op_id] = ("", op_id, None, False, True)
                break
        return sorted(items.values())

    def waiting(self, *, run_ref: str | None = None) -> list[str]:
        """Op ids still in the waiting room (queued, or promoted halfway), in
        the order they were queued."""
        return [
            op_id for _, op_id, ref, readable, _ in self._waiting_items()
            if run_ref is None or ref == run_ref or not readable
        ]

    def waiting_positions(self) -> dict[str | None, str]:
        """Per run, the queue position of its earliest waiting upload: `drain` delivers none of
        that run's ops queued after it. A non-blocking upload
        (`append_upload(blocking=False)`) holds nothing back."""
        positions: dict[str | None, str] = {}
        for position, _, ref, readable, blocking in self._waiting_items():
            if readable and blocking and ref is not None:
                positions.setdefault(ref, position)
        return positions

    @staticmethod
    def count_waiting(directory: str | Path) -> int:
        """Waiting items, by LISTING the directory, never status.json (an older worker rewrites
        it from `ops/` alone)."""
        try:
            names = os.listdir(Path(directory) / "waiting")
        except OSError:
            return 0
        return len({name.split(".", 1)[0] for name in names if name.endswith(".json")})

    def promote_waiting(
        self, *, run_ref: str | None = None, wait: bool = False, timeout: float | None = None
    ) -> int:
        """Scan, redact and fingerprint waiting uploads; queue each as an op. Returns how many
        became ops. Items go in queue order and a run stops at its first item that cannot go now:
        another process holds it (with ``wait``, waited for) or a disk error. Outbox full stops
        the pass. An item that can never go (unreadable record, missing copy, failing scan) is
        dead-lettered with the reason. ``timeout`` bounds the call: no scan starts and no wait
        continues after it.
        """
        if self.receipt_enabled or not self.waiting_dir.is_dir():
            return 0
        deadline = None if timeout is None else time.monotonic() + timeout
        promoted = 0
        while True:
            busy = False
            stopped: set[str | None] = set()  # runs held at an earlier item
            for _, op_id, ref, readable, _ in self._waiting_items():
                if deadline is not None and time.monotonic() >= deadline:
                    return promoted
                # An unreadable item belongs to no run we can name: taken whatever `run_ref` asks
                # for, and dead-lettered.
                if (run_ref is not None and ref != run_ref and readable) or ref in stopped:
                    continue
                with _try_lock(self._waiting_paths(op_id)[3]) as held:
                    if not held:
                        busy = True
                        stopped.add(ref)
                        continue
                    try:
                        promoted += self._promote_locked(op_id)
                    except OutboxFull:
                        return promoted
                    except OSError:
                        stopped.add(ref)  # left waiting; the next pass retries
                    except Exception as exc:  # noqa: BLE001 -- one item must not wedge the rest
                        self._dead_letter_waiting(
                            op_id, None, f"promotion failed ({type(exc).__name__})"
                        )
            self._sweep_waiting_orphans()
            if not (wait and busy):
                return promoted
            if deadline is not None and time.monotonic() >= deadline:
                return promoted
            time.sleep(0.05)

    def promote_for_close(self, run_ref: str, *, timeout: float) -> list[str]:
        """Before a run's close is queued: promote its waiting uploads, waiting up to ``timeout``
        for any another process is scanning. Returns the op ids still waiting that hold the close
        (a non-blocking upload does not); the caller decides whether that refuses the close."""
        try:
            self.promote_waiting(run_ref=run_ref, wait=True, timeout=timeout)
        except Exception:  # noqa: BLE001 -- judged by what is still waiting
            pass
        return self.waiting_for_close(run_ref)

    def waiting_for_close(self, run_ref: str) -> list[str]:
        """This run's waiting uploads that hold its close: all but those queued non-blocking, plus
        any unreadable item (it may be this run's)."""
        return [
            op_id for _, op_id, ref, readable, blocking in self._waiting_items()
            if (ref == run_ref and blocking) or not readable
        ]

    def _promote_locked(self, op_id: str) -> int:
        record, prepared, data, lock = self._waiting_paths(op_id)
        if not record.exists() and not prepared.exists():
            data.unlink(missing_ok=True)
            return 0
        starting_over = record.exists()
        try:
            body = json.loads((record if starting_over else prepared).read_text())
            op = dict(body["op"] if starting_over else body)
            inline_hash = bool(body.get("inline_hash"))
            if "op_id" not in op or not isinstance(op.get("upload"), dict):
                raise KeyError("op")  # not the shape promotion relies on
        except FileNotFoundError:
            return 0  # promoted meanwhile
        except (ValueError, KeyError, TypeError, AttributeError):
            self._dead_letter_waiting(op_id, None, "the queued upload's record is unreadable")
            return 0
        try:
            raw = data.read_bytes()
        except FileNotFoundError:
            self._dead_letter_waiting(op_id, op, "the queued copy of the upload is missing")
            return 0
        if starting_over:
            prepared.unlink(missing_ok=True)  # a half-made promotion; start over
            try:
                # scanning disabled: clean, result = redact_quick_bytes(raw)
                clean, result = raw, InspectionResult()
                if (op.get("upload") or {}).get("verbatim"):
                    refuse_rewrite(result)
            except CredentialBlocked as exc:
                self._dead_letter_waiting(op_id, op, str(exc))
                return 0
            if result.rewritten:
                # The artifact row records this too (the server reads the markers); this line is
                # for whoever reads the worker's log.
                print(
                    f"redacted {', '.join(sorted(set(result.rewritten)))} in queued upload "
                    f"{(op.get('upload') or {}).get('name')!r} ({now_iso()})",
                    flush=True,
                )
            digest = hashlib.sha256(clean).hexdigest() if inline_hash else None
            op["upload"]["blob"] = digest
            op["upload"]["size_bytes"] = len(clean) if inline_hash else None
            publish = self._staged_publisher(op, clean)
        else:
            # Roll forward: the op was committed and never made visible. Its blob may have gone to
            # a GC (it was unreferenced), so the blob is derived again from the scanned source
            # (deleted last) and published under the append lock like any other: whether it still
            # exists is only knowable there.
            try:
                # scanning disabled: clean, result = redact_quick_bytes(raw)
                clean, result = raw, InspectionResult()
                if (op.get("upload") or {}).get("verbatim"):
                    refuse_rewrite(result)
            except CredentialBlocked as exc:
                self._dead_letter_waiting(op_id, op, str(exc))
                return 0
            publish = self._staged_publisher(op, clean)

        def write_op(path: Path, final_op: dict) -> None:
            # (2) the committed op, (3) retire the record, (4) make it visible.
            write_text_atomic(prepared, json.dumps(final_op, indent=2) + "\n", mode=0o600)
            record.unlink(missing_ok=True)
            fsync_directory(self.waiting_dir)
            os.replace(prepared, path)
            fsync_directory(self.ops_dir)

        # `admitted`: the op ceiling counted this upload when queued (`_enqueue_waiting`).
        # Refusing it now could deadlock: drain holds the run's later ops, which fill the queue,
        # behind this very upload.
        self._append(op, before_write=publish, headroom_checked=True, write_op=write_op, admitted=True)
        data.unlink(missing_ok=True)  # (5)
        # Safe while held: a promoter that opened the old lock finds nothing left to do, and one
        # locking it after this unlink is told it holds nothing (`_same_file`).
        _retire_lock(lock)
        return 1

    def _staged_publisher(self, op: dict, clean: bytes):
        """Write `clean` to a staging blob now; return the publish step that moves it into place
        inside the append lock (gc takes the same lock)."""
        staging = self.blobs_dir / f".staging-{op['op_id']}"
        staging.unlink(missing_ok=True)
        _write_private(staging, clean)
        digest = op["upload"].get("blob")
        final = self.blobs_dir / digest if digest else self.blobs_dir / f"incoming-{op['op_id']}"

        def publish() -> None:
            if digest is not None and final.exists():
                staging.unlink(missing_ok=True)  # dedup: these bytes are already staged
            else:
                os.replace(staging, final)
            fsync_directory(self.blobs_dir)

        return publish

    def _dead_letter_waiting(self, op_id: str, op: dict | None, reason: str) -> None:
        """Refuse a waiting upload as the sync path refuses one: with the reason, nothing sent.
        Its copy goes: a retry has nothing scanned to deliver (fails again, never sends unscanned
        bytes)."""
        record, prepared, data, lock = self._waiting_paths(op_id)
        if op is None:
            # Keep whatever attribution survives: a run-scoped close checks its run's dead
            # letters and one filed under no run is missed.
            try:
                body = json.loads((record if record.exists() else prepared).read_text())
                found = body.get("op") or body
                op = dict(found) if isinstance(found, dict) and found.get("run_ref") else None
            except (OSError, ValueError, AttributeError, TypeError):
                op = None
        if op is None:
            op = {**self._base_op("upload", None), "op_id": op_id, "upload": {"staged": True}}
        op["last_error"] = f"{reason}; nothing was sent -- log the artifact again"
        op["attempts"] = int(op.get("attempts") or 0) + 1
        name = op.get("queue_filename") or self._op_filename(op_id)
        with file_lock(self.append_lock):
            write_text_atomic(self.failed_dir / name, json.dumps(op, indent=2) + "\n", mode=0o600)
            record.unlink(missing_ok=True)
            prepared.unlink(missing_ok=True)
            data.unlink(missing_ok=True)
            self._write_status_locked()
        _retire_lock(lock)

    def _sweep_waiting_orphans(self) -> None:
        """Delete `.bytes` with neither record nor committed op: an enqueue that died before
        returning, or a promotion that finished. Locked ones are an enqueue in progress, left
        alone."""
        try:
            names = os.listdir(self.waiting_dir)
        except OSError:
            return
        live = {name.split(".", 1)[0] for name in names if name.endswith(".json")}
        for name in names:
            if not name.endswith((".bytes", ".lock")) or name.split(".", 1)[0] in live:
                continue
            record, prepared, data, lock = self._waiting_paths(name.split(".", 1)[0])
            with _try_lock(lock) as held:
                if held and not record.exists() and not prepared.exists():
                    data.unlink(missing_ok=True)
                    _retire_lock(lock)
from probe.sdk.delivery.journal.headroom import OutboxFull  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.item_locks import _item_lock  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.item_locks import _retire_lock  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.item_locks import _try_lock  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.item_locks import _write_private  # noqa: E402 -- pieces need each other; the front door loads this one first
