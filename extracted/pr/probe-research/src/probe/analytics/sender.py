"""one queue and one daemon thread delivering batches in order, flushed (bounded) at exit."""

from __future__ import annotations

import atexit
import queue
import threading

from probe.foundation.version.version import VERSION as _cli_version
from probe.analytics import core as core
from probe.foundation.tls.tls import ssl_context
from probe.analytics.outcomes import IdentityMode
from probe.analytics.transport import _post_batch

# Above one POST timeout (core.SEND_TIMEOUT=3), so the last events (configure_completed,
# backfill.summary) survive slow links (review R1, amending D6's ~1s). Paid only on a bad network.
FLUSH_TIMEOUT_S = 3.5
QUEUE_MAX = 256


class _Sender:
    """One queue, one daemon thread, ordered delivery, silence everywhere: no
    stdout/stderr, since a stray traceback corrupts the wizard's full-screen frame."""

    def __init__(self) -> None:
        self.q: queue.Queue = queue.Queue(maxsize=QUEUE_MAX)
        self.transport = _post_batch  # test seam
        self._thread: threading.Thread | None = None
        self._lock = threading.Lock()
        self._stop = object()

    def start(self) -> None:
        with self._lock:
            if self._thread is None or not self._thread.is_alive():
                self._thread = threading.Thread(
                    target=self._run, daemon=True, name="probe-telemetry"
                )
                self._thread.start()

    def put(self, record: dict) -> None:
        try:
            self.q.put_nowait(record)
        except Exception:
            pass  # full queue: drop, never block or raise into the wizard

    def request_flush(self, timeout: float = FLUSH_TIMEOUT_S) -> None:
        """Bounded final delivery; called from atexit. Drops what misses the bound.

        A full queue cannot take the stop sentinel; the bounded join still lets an
        in-flight send finish, then the thread dies with the process (accepted loss).
        """
        try:
            self.q.put_nowait(self._stop)
        except Exception:
            pass
        thread = self._thread
        if thread is not None and thread.is_alive():
            thread.join(timeout)

    # Thread side.

    def _run(self) -> None:
        machine = core.machine_id()
        while True:
            item = self.q.get()
            batch: list[dict] = []
            has_seen_stop = item is self._stop
            if not has_seen_stop:
                batch.append(item)
            while True:
                try:
                    nxt = self.q.get_nowait()
                except queue.Empty:
                    break
                if nxt is self._stop:
                    has_seen_stop = True
                else:
                    batch.append(nxt)
            if batch:
                try:
                    # Send-time gate, as the plugin sender: a hosted --base-url over a self-host
                    # config must not ship self-host identity; gate the config the resolver reads.
                    if core.hosted_base_url(core.effective_base_url(core.read_cli_config())):
                        self.transport(self._entries(batch, machine))
                except Exception:
                    pass  # PostHog down costs the session nothing
            if has_seen_stop:
                return

    def _entries(self, records: list[dict], machine: str) -> list[dict]:
        """Batch entries, honoring each record's emit-time identity_mode."""
        anon_ident = {
            "distinct_id": f"machine:{machine}",
            "customer_id": None,
            "workspace_id": None,
            "authenticated": False,
        }
        auth_ident: dict | None = None
        entries: list[dict] = []
        for record in records:
            pinned = record.get("identity")
            if pinned is not None:
                # Resolved before the credential that produced it was revoked;
                # re-resolving here would find nothing. See pin_identity.
                entries.extend(
                    core.build_batch(
                        [record], pinned, client_kind="cli", lib="probe-cli",
                        client_version=_cli_version, machine=machine,
                    )
                )
                continue
            if record.get("identity_mode") == IdentityMode.AUTHENTICATED:
                if auth_ident is None:
                    try:
                        auth_ident = core.resolve_identity(
                            core.read_cli_config(), machine=machine, context=ssl_context()
                        )
                    except Exception:
                        auth_ident = anon_ident
                ident = auth_ident
            else:
                ident = anon_ident
            # Only the CLI enqueues here; the hosted MCP shares `build_batch` but has its own sender
            # (mcp/delivery/accounting.py; `cli/` is outside the MCP deploy filter). So these stay literals.
            entries.extend(
                core.build_batch(
                    [record],
                    ident,
                    client_kind="cli",
                    lib="probe-cli",
                    client_version=_cli_version,
                    machine=machine,
                )
            )
        return entries


_sender: _Sender | None = None
_sender_lock = threading.Lock()
_flush_registered = False


def _ensure_sender() -> _Sender:
    global _sender, _flush_registered
    with _sender_lock:
        if _sender is None:
            _sender = _Sender()
        _sender.start()
        if not _flush_registered:
            atexit.register(_flush_at_exit)
            _flush_registered = True
        return _sender


def _flush_at_exit() -> None:
    sender = _sender
    if sender is not None:
        try:
            sender.request_flush()
        except BaseException:  # noqa: BLE001 - a second Ctrl-C lands here as
            pass  # KeyboardInterrupt; atexit would print it onto the TUI frame
