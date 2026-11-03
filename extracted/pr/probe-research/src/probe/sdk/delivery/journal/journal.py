"""Journal: the durable outbox, one ordered queue of op files for every deferred write.
Stores and never sends; layout, op schema and failure policy in DESIGN.md."""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
import re
from typing import TYPE_CHECKING

from ....foundation.os_backend import os_backend as oscompat
from ....foundation.compose.compose import fold_parts
# scanning disabled: from .redaction import default_scrub, scrub_string, scrub_text
# scanning disabled: from .stamp_scrub import scrub_body, scrub_envelope, scrub_op


log = logging.getLogger(__name__)


if TYPE_CHECKING:
    from probe.sdk.delivery.journal.failures.pause import PauseMixin
    from probe.sdk.delivery.journal.paths import QueueDiscoveryMixin
    from probe.sdk.delivery.journal.headroom import HeadroomMixin
    from probe.sdk.delivery.journal.receipts.receipts import ReceiptsMixin
    from probe.sdk.delivery.journal.receipts.index import ReceiptIndexMixin
    from probe.sdk.delivery.journal.append import AppendMixin
    from probe.sdk.delivery.journal.uploads import UploadQueueMixin
    from probe.sdk.delivery.journal.waiting_room import WaitingRoomMixin
    from probe.sdk.delivery.journal.producers import ProducersMixin
    from probe.sdk.delivery.journal.failures.failures import FailuresMixin
    from probe.sdk.delivery.journal.failures.discards import DiscardsMixin
    from probe.sdk.delivery.journal.status_file import StatusFileMixin
    from probe.sdk.delivery.journal.run_ops import RunOpsMixin

    class _JournalParts(
        PauseMixin,
        QueueDiscoveryMixin,
        HeadroomMixin,
        ReceiptsMixin,
        ReceiptIndexMixin,
        AppendMixin,
        UploadQueueMixin,
        WaitingRoomMixin,
        ProducersMixin,
        FailuresMixin,
        DiscardsMixin,
        StatusFileMixin,
        RunOpsMixin,
    ):
        """Journal's parts as bases, for editors and type checkers; at runtime fold_parts() copies them in."""
else:
    _JournalParts = object


class Journal(_JournalParts):
    def __init__(
        self,
        directory: str | Path | None = None,
        *,
        context: dict | None = None,
        attribution: str = "ambient",
    ):
        self.dir = Path(directory).expanduser() if directory else default_dir()
        self.ops_dir = self.dir / "ops"
        self.failed_dir = self.dir / "failed"
        self.blobs_dir = self.dir / "blobs"
        #: Uploads queued before their credential scan (see `promote_waiting`). No earlier
        #: release reads it, so an older drainer sharing this journal never picks up
        #: unscanned bytes.
        self.waiting_dir = self.dir / "waiting"
        #: Held by whoever is promoting (a promote-only worker or a drain's promotion pass), so
        #: a kick does not fork another promoter; separate from the drain lease an OLDER worker
        #: may hold.
        self.promote_lease = self.dir / ".promote.lock"
        self.status_file = self.dir / "status.json"
        self.paused_file = self.dir / "paused"
        self.append_lock = self.dir / ".append.lock"
        self.drain_lock = self.dir / ".drain.lock"
        #: Held shared by a run's close while it waits for the drain lock, so a
        #: pass gives the lock up at its next op (`_DrainHold`, #3618).
        self.drain_want = self.dir / ".drain.want"
        #: One flock per run slot, held while a pass sends that run's upload
        #: with the drain lock let go (`_DrainHold`, #3618).
        self.run_locks_dir = self.dir / ".run-locks"
        #: Present while a takeover barrier (SDK reliability 2.3) holds queued status ops aside in
        #: `failed/`: the cheap test telling every drain pass and new client whether to look for
        #: abandoned holds.
        self.holds_marker = self.dir / "takeover-holds"
        self.producers_dir = self.dir / "producers"
        #: default {"name", "base_url"} pin stamped onto appended ops.
        self.context = context
        if attribution not in ("ambient", "backfill"):
            raise ValueError("invalid outbox attribution")
        self.attribution = attribution
        self.receipt_enabled = self.dir.name == DELIVERY_NAMESPACE
        self.intents_dir = self.dir / "intents"
        self.receipts_dir = self.dir / "receipts"
        self.receipt_index = self.dir / "receipts-v1.sqlite3"
        self.correlation_locks = self.dir / "correlation-stripes"
        self.recovery_file = self.dir / ".recover"
        #: The longest a drainer may hold this writer's telemetry (seconds), below
        #: `PROBE_SEND_INTERVAL_SEC`: an explicit `drain_interval` / `PROBE_EXPORT_INTERVAL_SEC`
        #: (review of #3785, I18). None: the window alone decides.
        self.window_cap: float | None = None
        #: parity F4: set via register_producer; None = unstamped ops.
        self._producer_id: str | None = None
        self._producer_role: str | None = None
        #: Backpressure state for `_append_headroom`: the pending count last seen in status.json, re-read
        #: before any refusal (a count read once refused every write: plan 0.1, DESIGN.md).
        self._pending_estimate: int | None = None
        self._recounted_at = float("-inf")
        self._appends_since_statvfs = _STATVFS_EVERY
        self._last_free_ok = True
        self._headroom_warned = False
        #: The queue's sequence high-water mark, taken once per Journal before its first
        #: sequence (see `_op_filename`); None until then, and again once applied.
        self._seq_floor: int | None = None
        self._seq_recovered = False
        #: The sibling namespace's pending count, re-read with the free-space
        #: sample rather than on every append (plan 1.3); `None` = not yet read.
        self._sibling_pending: int | None = None
        self._appends_since_sibling = 0
        #: This queue's op-count ceiling: None is `MAX_PENDING_OPS`, 0 is none. An OFFLINE run's
        #: queue (plan 2.12) sets 0: nothing drains it until `probe sync`, so a ceiling meant to
        #: catch a stalled drainer would drop every point after the 500,000th and the close with
        #: them. The free-space floor still applies.
        self.op_ceiling: int | None = None

    @classmethod
    def for_receipts(cls, directory=None, *, context=None, attribution="backfill") -> Journal:
        """New operations live outside every pre-receipt worker's ops directory."""
        base = Path(directory).expanduser() if directory else default_dir()
        if base.name != DELIVERY_NAMESPACE:
            base = base / DELIVERY_NAMESPACE
        return cls(base, context=context, attribution=attribution)

    @classmethod
    def for_credential(
        cls, directory=None, fingerprint: str = "", *, context=None, attribution="ambient"
    ) -> Journal:
        """The queue of one credential (see `CREDENTIAL_NAMESPACE`)."""
        base = Path(directory).expanduser() if directory else default_dir()
        if not fingerprint or not re.fullmatch(r"[0-9a-f]{16}", fingerprint):
            raise ValueError("a credential queue needs a 16-hex fingerprint")
        return cls(base / CREDENTIAL_NAMESPACE / fingerprint, context=context, attribution=attribution)

    @property
    def outbox_root(self) -> Path:
        """The outbox directory this queue lives in (itself, for the root)."""
        path = self.dir
        if path.name == DELIVERY_NAMESPACE:
            path = path.parent
        if path.parent.name == CREDENTIAL_NAMESPACE:
            path = path.parent.parent
        return path

    def namespaces(self) -> list[Journal]:
        """This queue and the queues under it, each once: the root, its receipt namespace, and
        every credential queue with its own receipt namespace."""
        if self.receipt_enabled:
            return [self]
        out = [self]
        child = self.for_receipts(self.dir, context=self.context, attribution=self.attribution)
        if child.dir.exists():
            out.append(child)
        if self.dir.parent.name != CREDENTIAL_NAMESPACE:
            for path in _credential_queue_dirs(self.dir):
                queue = Journal(path, context=self.context, attribution=self.attribution)
                out.append(queue)
                receipts = self.for_receipts(path, context=self.context, attribution=self.attribution)
                if receipts.dir.exists():
                    out.append(receipts)
        return out

    def _ensure(self) -> None:
        # Once per Journal, not per append: this ran 4 mkdir + 4 chmod on EVERY write; chmod is a
        # SETATTR write RPC on NFS, not a cached stat, so on a shared $HOME it was eight round
        # trips per metric point. `_ensure_again` clears the flag whenever a write actually fails,
        # so a directory deleted underneath us is still recreated.
        if getattr(self, "_layout_ready", False):
            return
        self._ensure_layout()

    def _ensure_layout(self) -> None:
        for directory in (self.dir, self.ops_dir, self.failed_dir, self.blobs_dir, self.waiting_dir):
            directory.mkdir(parents=True, exist_ok=True, mode=0o700)
            # mkdir mode is masked by umask; queue contents are research data, so re-assert (codex
            # finding: primitives default to umask).
            try:
                os.chmod(directory, 0o700)
            except OSError:
                pass
        self._layout_ready = True
        if not getattr(self, "_spool_checked", False):
            # One-time fold of a surviving pre-journal spool (T1-C). Two stats when there is
            # nothing to import. ONLY the default journal auto-imports: a custom/temporary journal
            # directory must never steal (and delete) the machine's global spool (codex).
            self._spool_checked = True
            if self.dir == default_dir():
                try:
                    self.import_spool()
                except Exception:  # noqa: BLE001 -- legacy debris must not block a write
                    pass

    # -- reads --------------------------------------------------------------
    @staticmethod
    def _read_dir(directory: Path) -> list[tuple[Path, dict]]:
        if not directory.exists():
            return []
        out: list[tuple[Path, dict]] = []
        for path in sorted(directory.iterdir()):
            if not path.name.endswith(".json"):
                continue
            try:
                out.append((path, json.loads(path.read_text())))
            except (OSError, ValueError):  # ValueError: a torn file, JSON or not UTF-8 at all
                continue
        return out

    def pending(self) -> list[tuple[Path, dict]]:
        return self._read_dir(self.ops_dir)

    def failed(self) -> list[tuple[Path, dict]]:
        return self._read_dir(self.failed_dir)

    def outbox_queues(self) -> "list[Journal]":
        """Every queue of the outbox this one belongs to: the root, its receipt
        namespace, and each credential queue (#2035) with its own."""
        root = Journal(self.outbox_root, context=self.context, attribution=self.attribution)
        return root.namespaces()

    def worker_alive(self) -> bool:
        """Whether a worker holds this queue's lease right now (non-blocking)."""
        try:
            handle = (self.dir / ".worker.lock").open("a+")
        except OSError:
            return False
        try:
            oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
        except (BlockingIOError, OSError):
            return True
        else:
            oscompat.flock(handle.fileno(), oscompat.LOCK_UN)
            return False
        finally:
            handle.close()
from probe.sdk.delivery.journal.headroom import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _STATVFS_EVERY,
)
from probe.sdk.delivery.journal.paths import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _credential_queue_dirs,
    default_dir,
)
from probe.sdk.delivery.ops.ops import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    CREDENTIAL_NAMESPACE,
    DELIVERY_NAMESPACE,
)
from probe.sdk.delivery.journal.failures.pause import PauseMixin  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.paths import QueueDiscoveryMixin  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.headroom import HeadroomMixin  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.receipts.receipts import ReceiptsMixin  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.receipts.index import ReceiptIndexMixin  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.append import AppendMixin  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.uploads import UploadQueueMixin  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.waiting_room import WaitingRoomMixin  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.producers import ProducersMixin  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.failures.failures import FailuresMixin  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.failures.discards import DiscardsMixin  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.status_file import StatusFileMixin  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.run_ops import RunOpsMixin  # noqa: E402 -- pieces need each other; the front door loads this one first

# Journal's parts read it back at import time, so they load after it and are folded in here.
fold_parts(
    Journal,
    PauseMixin,
    QueueDiscoveryMixin,
    HeadroomMixin,
    ReceiptsMixin,
    ReceiptIndexMixin,
    AppendMixin,
    UploadQueueMixin,
    WaitingRoomMixin,
    ProducersMixin,
    FailuresMixin,
    DiscardsMixin,
    StatusFileMixin,
    RunOpsMixin,
)
