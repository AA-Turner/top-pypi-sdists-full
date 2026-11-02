"""the watch's thresholds, windows and timings, each overridable by environment (the one place tests patch)."""

from __future__ import annotations
import os
from probe.service.watch.incident import Family
WINDOW_S = 15 * 60.0
#: Kept while an update drains or holds its barrier: they are not a hand-over's doing.
KEPT_WHILE_UPDATING = frozenset({Family.SERVICE_CRASH, Family.UPDATE_REJECTED, Family.UPDATE_FAILED, Family.TAP_LOAD})
#: `update_failed`: this many update cycles in a row ended `ok: false`.
UPDATE_FAILED_STREAK = 3
#: The read the child runs (`probe.core.run report`, PR 2a), and its bounds.
REPORT_READ = "report"
REPORT_TIMEOUT_S = 60.0
#: A (family, session) reported, or declined, is not asked about again for this
#: long: the child's own dedupe window, so no child starts only to say `deduped`.
DEDUPE_S = 6 * 3600.0
#: Incidents waiting at once (the oldest goes).
MAX_PENDING = 16
#: A report the child did not take (offline, the server, killed...) is tried
#: again this often, for this long after its first try.
RETRY_S = 30 * 60.0
RETRY_FOR_S = 24 * 3600.0
KEEP_EVENTS = 3
#: How often the watch looks (and sends what waits for the slot).
SCAN_S = 15.0
#: A daemon lease past its expiry by more than this, on two scans, is a lapsed worker.
LEASE_GRACE_S = 60.0
#: Lease reasons that are failures (`tap/companion_lease.py`); `stopped`,
#: `budget` and `handover` are on purpose, `disk_full` is the machine's. A
#: `gateway` release the worker marked `offline` (no network at all,
#: `probe.foundation.tls.network_down`) is the laptop's, not a failure.
LEASE_FAILURES = frozenset({"error", "gateway", "unauthorized"})
#: A hosted recorder's beat (`tap.hosted.Controls.beat`, every pass and every
#: second between) this old while its agent runs: `stalled`.
STALL_S = 300.0
#: A `tap watch` session's registration (its link re-registers every 20 s)
#: this old while its agent runs: `gone`.
GONE_S = 90.0
#: How often the slower checks run (the outbox, receipts), on the first scan too.
SLOW_CHECK_S = 5 * 60.0
#: The outbox's oldest write this old, with the queue refused or held: stuck.
OUTBOX_STUCK_S = 3600.0
#: A live session's transcript waiting this long past its last receipt: stalled.
CAPTURE_STALL_S = 3600.0
#: Each key the CLI config holds is asked whether the API takes it this often
#: (`watch.json` keeps when each was answered, so a restarted service does not
#: ask again).
CREDENTIAL_CHECK_S = 24 * 3600.0
#: One ask's timeout, and the whole check's: no retry ever starts past it.
CREDENTIAL_TIMEOUT_S = 5.0
CREDENTIAL_DEADLINE_S = 20.0
#: A key with no answer (offline, a timeout, a server error) is asked again
#: after this, not at every slow check.
CREDENTIAL_RETRY_S = 3600.0
#: The outbox's status files on a hung mount: given up on past this.
OUTBOX_TIMEOUT_S = 30.0
#: A capture stall names at most this many of its sessions.
CAPTURE_MAX_SESSIONS = 8
#: A report the server's rate limit refused is tried again after this.
RATE_LIMITED_RETRY_S = 2 * 3600.0
#: Between two scans, wall time ran ahead of monotonic time by more than this
#: (a sleep), or the scans were this far apart: everything measured in time
#: waits WAKE_GRACE_S (a worker renews its lease within its TTL, 240 s).
WAKE_SLACK_S = 30.0
WAKE_GAP_S = 120.0
WAKE_GRACE_S = 300.0
#: A guard record older than this is not news.
GUARD_FRESH_S = 24 * 3600.0
#: The login shell's variables are asked at most this often.
LOGIN_CACHE_S = 600.0
#: Test-only overrides (API v1, "Lifecycle"). Nothing in production sets them.
#: "0": no automatic report from this service or its keeper (the test suite's
#: services: a person's opt-outs are PROBE_TELEMETRY and PROBE_DIAGNOSTICS).
REPORTS_ENV = "PROBE_SERVICE_REPORTS"
SCAN_ENV = "PROBE_SERVICE_WATCH_S"


def reports_enabled() -> bool:
    return os.environ.get(REPORTS_ENV, "1") != "0"


def _env_float(name: str, default: float) -> float:
    try:
        value = float(os.environ.get(name) or default)
    except ValueError:
        return default
    return value if value > 0 else default
