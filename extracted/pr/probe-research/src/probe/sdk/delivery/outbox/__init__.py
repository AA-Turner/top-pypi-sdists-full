"""Draining the journal (worker, lease, linger, rescue, detached drainer); the old `probe.sdk.outbox_worker`.
Names are served live, so a patch on the defining piece reaches callers here; code imports pieces."""

from __future__ import annotations

import importlib

# Every piece loads here, as `probe.sdk.outbox_worker` loaded whole: a piece first imported at interpreter
# exit would exec there (CPython 3.12 then loses an uncaught Ctrl-C's exit code).
for _piece in (
    "probe.sdk.delivery.outbox.lease",
    "probe.sdk.delivery.outbox.linger",
    "probe.sdk.delivery.outbox.drainers.detached",
    "probe.sdk.delivery.outbox.rescuer",
    "probe.sdk.delivery.outbox.outbox",
):
    importlib.import_module(_piece)
del _piece

#: Every name the front door serves -> the module that defines it.
_HOMES = {
    # probe.sdk.delivery.outbox.lease
    "_lease_path": "probe.sdk.delivery.outbox.lease",
    "_caps_path": "probe.sdk.delivery.outbox.lease",
    "_stop_path": "probe.sdk.delivery.outbox.lease",
    "_write_caps": "probe.sdk.delivery.outbox.lease",
    "_drop_caps": "probe.sdk.delivery.outbox.lease",
    "_pid_alive": "probe.sdk.delivery.outbox.lease",
    "_LEGACY_KINDS": "probe.sdk.delivery.outbox.lease",
    "live_worker_kinds": "probe.sdk.delivery.outbox.lease",
    "ready_for": "probe.sdk.delivery.outbox.lease",
    "_asked_to_stop": "probe.sdk.delivery.outbox.lease",
    "_lease_is_free": "probe.sdk.delivery.outbox.lease",
    "worker_holder": "probe.sdk.delivery.outbox.lease",
    # probe.sdk.delivery.outbox.linger
    "_LINGER_SECONDS": "probe.sdk.delivery.outbox.linger",
    "_LINGER_POLL_SECONDS": "probe.sdk.delivery.outbox.linger",
    "LINGER_ENV": "probe.sdk.delivery.outbox.linger",
    "_work_arrived": "probe.sdk.delivery.outbox.linger",
    "LingerEnd": "probe.sdk.delivery.outbox.linger",
    "_linger_polls": "probe.sdk.delivery.outbox.linger",
    "_linger": "probe.sdk.delivery.outbox.linger",
    "_has_queued_op": "probe.sdk.delivery.outbox.linger",
    # probe.sdk.delivery.outbox.drainers.detached
    "_AUTH_RETRY_COOLDOWN_SECONDS": "probe.sdk.delivery.outbox.drainers.detached",
    "_LOG_NAME": "probe.sdk.delivery.outbox.drainers.detached",
    "_auth_block_is_fresh": "probe.sdk.delivery.outbox.drainers.detached",
    "_env_fingerprints": "probe.sdk.delivery.outbox.drainers.detached",
    "env_fingerprints": "probe.sdk.delivery.outbox.drainers.detached",
    "_holds_the_queues_credential": "probe.sdk.delivery.outbox.drainers.detached",
    "_own_credential_queue": "probe.sdk.delivery.outbox.drainers.detached",
    "_ADOPTED_KICK_SECONDS": "probe.sdk.delivery.outbox.drainers.detached",
    "_ADOPTED_KICKED_AT": "probe.sdk.delivery.outbox.drainers.detached",
    "_adopted_credential_queues": "probe.sdk.delivery.outbox.drainers.detached",
    "_HELD_RESPAWN_SECONDS": "probe.sdk.delivery.outbox.drainers.detached",
    "_held_is_fresh": "probe.sdk.delivery.outbox.drainers.detached",
    "maybe_spawn": "probe.sdk.delivery.outbox.drainers.detached",
    "_spawn_detached": "probe.sdk.delivery.outbox.drainers.detached",
    "_COPIED_LOGINS": "probe.sdk.delivery.outbox.drainers.detached",
    "note_copied_login": "probe.sdk.delivery.outbox.drainers.detached",
    "is_copied_login": "probe.sdk.delivery.outbox.drainers.detached",
    "_worker_env": "probe.sdk.delivery.outbox.drainers.detached",
    "_hand_to_service": "probe.sdk.delivery.outbox.drainers.detached",
    "_KILLED_LEASE_POLL_SECONDS": "probe.sdk.delivery.outbox.drainers.detached",
    "spawn_past_a_kill": "probe.sdk.delivery.outbox.drainers.detached",
    "_spawn_took": "probe.sdk.delivery.outbox.drainers.detached",
    # probe.sdk.delivery.outbox.rescuer
    "RESCUE_ENV": "probe.sdk.delivery.outbox.rescuer",
    "RESCUE_EVERY_SECONDS": "probe.sdk.delivery.outbox.rescuer",
    "RESCUE_IDLE_SECONDS": "probe.sdk.delivery.outbox.rescuer",
    "_RESCUE_WAITING_SECONDS": "probe.sdk.delivery.outbox.rescuer",
    "rescue_enabled": "probe.sdk.delivery.outbox.rescuer",
    "_rescue_stamp": "probe.sdk.delivery.outbox.rescuer",
    "_multipart_waiting_since": "probe.sdk.delivery.outbox.rescuer",
    "_waiting_since": "probe.sdk.delivery.outbox.rescuer",
    "_rescue_roots": "probe.sdk.delivery.outbox.rescuer",
    "_writes_held_back": "probe.sdk.delivery.outbox.rescuer",
    "_rescue_due": "probe.sdk.delivery.outbox.rescuer",
    "_claim": "probe.sdk.delivery.outbox.rescuer",
    "_RESTORE_STAMP": "probe.sdk.delivery.outbox.rescuer",
    "claim_restore": "probe.sdk.delivery.outbox.rescuer",
    "maybe_restore": "probe.sdk.delivery.outbox.rescuer",
    "maybe_rescue": "probe.sdk.delivery.outbox.rescuer",
    "lift_stale_pause": "probe.sdk.delivery.outbox.rescuer",
    "_discards_held_in_queues": "probe.sdk.delivery.outbox.rescuer",
    "_rescuer_env": "probe.sdk.delivery.outbox.rescuer",
    "spawn_rescuer": "probe.sdk.delivery.outbox.rescuer",
    "adopt_before_discard": "probe.sdk.delivery.outbox.rescuer",
    "_RESCUE_LOCK_TIMEOUT_SECONDS": "probe.sdk.delivery.outbox.rescuer",
    "drain_adopted": "probe.sdk.delivery.outbox.rescuer",
    "rescue": "probe.sdk.delivery.outbox.rescuer",
    "_restore_root": "probe.sdk.delivery.outbox.rescuer",
    "_refuse_restored": "probe.sdk.delivery.outbox.rescuer",
    "_settle_restore": "probe.sdk.delivery.outbox.rescuer",
    "_look_again_later": "probe.sdk.delivery.outbox.rescuer",
    # probe.sdk.delivery.outbox.outbox
    "OutboxOutcome": "probe.sdk.delivery.outbox.outbox",
    "_BACKOFF_START_SECONDS": "probe.sdk.delivery.outbox.outbox",
    "_BACKOFF_CAP_SECONDS": "probe.sdk.delivery.outbox.outbox",
    "_EXIT_GRACE_SECONDS": "probe.sdk.delivery.outbox.outbox",
    "_WAITING_PASSES": "probe.sdk.delivery.outbox.outbox",
    "_promote_only": "probe.sdk.delivery.outbox.outbox",
    "_pinned_base_url": "probe.sdk.delivery.outbox.outbox",
    "_LANE_REPASS_SECONDS": "probe.sdk.delivery.outbox.outbox",
    "_LANE_LOOK_SECONDS": "probe.sdk.delivery.outbox.outbox",
    "_queued_names": "probe.sdk.delivery.outbox.outbox",
    "_wake_stamp": "probe.sdk.delivery.outbox.outbox",
    "_sleep_until_new_work": "probe.sdk.delivery.outbox.outbox",
    "run": "probe.sdk.delivery.outbox.outbox",
    "_run_leased": "probe.sdk.delivery.outbox.outbox",
    # imported by the old module: the same objects, read through a piece that imports them
    "os": "probe.sdk.delivery.outbox.lease",
    "subprocess": "probe.sdk.delivery.outbox.drainers.detached",
    "sys": "probe.sdk.delivery.outbox.drainers.detached",
    "time": "probe.sdk.delivery.outbox.linger",
    "StrEnum": "probe.sdk.delivery.outbox.linger",
    "oscompat": "probe.sdk.delivery.outbox.lease",
    "durable": "probe.sdk.delivery.outbox.lease",
    "_diagnostics": "probe.sdk.delivery.outbox.drainers.detached",
}
#: `from <old path> import *` takes what the old module's did: every public name.
__all__ = [name for name in _HOMES if not name.startswith("_")]


def __getattr__(name: str):
    home = _HOMES.get(name)
    if home is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return getattr(importlib.import_module(home), name)


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(_HOMES))
