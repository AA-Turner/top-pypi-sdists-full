"""Per-trace database snapshot ref capture.

Every root span carries a snapshot ref that pins the DB state at trace open by
wall-clock timestamp. Capturing the timestamp is free (no IO) and harmless, so
it happens on every trace regardless of configuration: that lets any trace be
replayed against a historical branch later. The provider/branch is resolved at
replay time. Mirrors the TypeScript SDK's ``DbSnapshotRef`` wire shape (camelCase
key, since the server speaks the same protocol for both SDKs).
"""

from typing import TypedDict


class DbSnapshotRef(TypedDict, total=False):
    """Snapshot ref attached to every root trace.

    Attributes:
        sdkWallClockBeforeFn: ISO wall-clock timestamp the SDK observed
            immediately before invoking the wrapped function. Always present.
    """

    sdkWallClockBeforeFn: str


def build_snapshot_ref(sdk_wall_clock_before_fn: str) -> DbSnapshotRef:
    """Build a snapshot ref for one trace. Synchronous, no IO.

    Stores only the wall clock the SDK observed immediately before invoking the
    wrapped function; the server-side resolver uses that as the snapshot
    timestamp. No provider is captured (it is resolved at replay time).
    """
    return {"sdkWallClockBeforeFn": sdk_wall_clock_before_fn}
