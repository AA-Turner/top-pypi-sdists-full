"""probe sync: deliver one offline run with the syncer's login, refusing a queue recorded for another server or tenant."""

from __future__ import annotations
from typing import TYPE_CHECKING
import time
from pathlib import Path

from ... import errors
from ..journal.journal import Journal

if TYPE_CHECKING:
    from ...client.client import Client


def _origin(url: str | None) -> str:
    return (url or "").strip().rstrip("/").lower()


def check_origin(directory: Path, client: Client, *, allow_mismatch: bool = False) -> list[str]:
    """Refuse a queue recorded against another server or, tenant unknown, another login
    context, unless ``allow_mismatch``. Returns warnings (a mismatch allowed, or a context
    change the tenant check covers)."""
    manifest = read_manifest(directory) or {}
    warnings_: list[str] = []
    recorded_url, current_url = manifest.get("base_url"), getattr(client.settings, "base_url", None)
    if recorded_url and current_url and _origin(recorded_url) != _origin(current_url):
        message = (
            f"recorded against {recorded_url}, but this login syncs to {current_url}"
        )
        if not allow_mismatch:
            raise errors.ScopeError(
                f"{directory}: {message}. Log in to that server, or pass --allow-mismatch "
                "to deliver it here anyway."
            )
        warnings_.append(message + " (--allow-mismatch)")
    recorded_ctx, current_ctx = manifest.get("context"), _context_name()
    if recorded_ctx and current_ctx and recorded_ctx != current_ctx:
        message = f"recorded under login context {recorded_ctx!r}, synced under {current_ctx!r}"
        if manifest.get("customer_id"):
            warnings_.append(message + " (same team: checked against the recorded one)")
        elif not allow_mismatch:
            # With no recorded team the context is the only evidence of whose run this is:
            # another context may be another team's login.
            raise errors.ScopeError(
                f"{directory}: {message}, and the team it was recorded for is unknown. "
                f"Switch back to context {recorded_ctx!r} (`probe wizard --action account`), or pass "
                "--allow-mismatch to deliver it with this login."
            )
        else:
            warnings_.append(message + " (--allow-mismatch)")
    return warnings_


def check_tenant(directory: Path, client: Client) -> dict:
    """Refuse a queue recorded for another tenant. Returns the syncer's identity."""
    manifest = read_manifest(directory) or {}
    me = client.me() or {}
    recorded = manifest.get("customer_id")
    current = me.get("customer_id")
    if recorded and current and recorded != current:
        raise errors.ScopeError(
            f"{directory}: this run was recorded for team {recorded!r}, but you are "
            f"logged in to {current!r}. Sign in to that team (`probe wizard --action login "
            "--context <name>`) to sync it."
        )
    return me


def require_server(client: Client) -> None:
    if not client.supports_feature("run_offline_create"):
        raise errors.CapabilityUnavailable(
            "run_offline_create",
            "this research-os server predates offline sync: it would treat the run as "
            "abandoned and close it mid-sync. Upgrade the server, then `probe sync` again; "
            "the queue is kept.",
        )


def sync_dir(
    directory: Path,
    client: Client,
    *,
    project: str | None = None,
    experiment: str | None = None,
    on_conflict: str | None = None,
    amend_all: bool = False,
    allow_mismatch: bool = False,
) -> dict:
    """Deliver one offline run with ``client`` (the syncer's login). ``project``/
    ``experiment``/``on_conflict`` re-file the run's create (:func:`amend`), only a REFUSED
    one unless ``amend_all`` (the caller named this run's folder)."""
    from ..outbox.drain.drain import drain

    manifest = read_manifest(directory) or {}
    warnings_ = check_origin(directory, client, allow_mismatch=allow_mismatch)
    me = check_tenant(directory, client)
    if not manifest.get("customer_id"):
        # Nothing to check against: the recording machine never reached the API under its
        # credential. Allowed (any writer may sync), never silent.
        warnings_.append(
            "recorded on a machine that had never reached the API, so the team it was "
            "recorded for is unknown; syncing it into this login's team "
            f"({me.get('customer_id') or 'unknown'})"
        )
    amended = 0
    if project is not None or experiment is not None or on_conflict is not None:
        amended = amend(
            directory,
            project=project,
            experiment=experiment,
            on_conflict=on_conflict,
            only_refused=not amend_all,
        )
    journal = Journal(directory)
    unmergeable = 0
    if not client.supports_feature("run_config_merge"):
        # Config merges were queued offline on the promise that the syncing server decides
        # (`OfflineClient.DEFERRED_FEATURES`). This one cannot store them and would answer
        # 200 while dropping the field.
        unmergeable = sum(
            1 for _, op in journal.pending() if "config_merge" in (op.get("body") or {})
        )
        if unmergeable:
            warnings_.append(
                f"this server cannot merge a run's config after it started (feature "
                f"run_config_merge): {unmergeable} config update(s) recorded offline are "
                "not stored; the run keeps the config it was created with. Upgrade the "
                "server to keep them."
            )
    # The run's own read/write lists its process never queued (it died before
    # its close): into the queue first, so the checks below and the drain
    # see them.
    if manifest.get("creation_key"):
        from ...capture import lineage as _inputs

        _inputs.recover_offline(local_ref(str(manifest["creation_key"])), directory)
    dropped_lineage = _drop_untaken_lineage(journal, client)
    started = time.monotonic()
    report = drain(journal, client_factory=lambda _context: client)
    # A list queued after that check (a recovery elsewhere) was dropped at
    # delivery instead (`lineage_gate`): counted with the rest.
    for feature, count in _take_gated(directory).items():
        dropped_lineage[feature] = dropped_lineage.get(feature, 0) + count
    late = dropped_lineage.pop(_LATE, 0)
    if late:
        warnings_.append(
            f"this server does not key a run's reads by observation (feature "
            f"{_OBSERVATIONS_FEATURE}): {late} late hash list(s) recorded offline were not "
            "re-sent; those reads stay unhashed. Upgrade the server to keep them."
        )
    for feature, count in dropped_lineage.items():
        warnings_.append(
            f"this server does not take a run's {LINEAGE_ROUTES[feature]} list (feature "
            f"{feature}): {count} list(s) recorded offline were dropped instead of "
            "delivered; the run's other data is unaffected. Upgrade the server to keep them."
        )
    state = describe(directory)
    entry = read_mapping(directory).get(str(manifest.get("creation_key"))) or {}
    if entry.get("via") == "online" and report.delivered:
        warnings_.append(
            f"its create had reached the server online before the outage (run "
            f"{entry.get('id')}), so it was delivered onto that run. Having heard nothing "
            "since init, the server may have marked it crashed and queued a crash notice "
            "meanwhile; its queued close sets the final status now"
        )
    dropped = state["dropped_writes"]
    if dropped:
        warnings_.append(
            f"{dropped} write(s) were dropped while recording (the disk was under the "
            "outbox's free-space floor, or the queue was unwritable) and were never in "
            f"this queue; the run is marked probe_finish.dropped_writes={dropped}"
        )
    return {
        **state,
        "delivered": report.delivered,
        "dead_lettered": report.dead_lettered,
        "remaining": report.remaining,
        "auth_blocked": report.auth_blocked,
        "amended": amended,
        "errors": list(report.errors),
        "warnings": warnings_,
        "seconds": round(time.monotonic() - started, 3),
        "clean": report.clean and state["state"] == "synced" and not dropped and not unmergeable,
    }
from probe.sdk.delivery.offline.lineage import _LATE, _OBSERVATIONS_FEATURE, _drop_untaken_lineage, _take_gated  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.offline.offline import _context_name, local_ref  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.offline.queue import amend, describe, read_manifest, read_mapping  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.offline.lineage import LINEAGE_ROUTES  # noqa: E402 -- pieces need each other; the front door loads this one first
