"""
The --max-records cap for `fivetran debug --record` and `fivetran debug --replay`.

The cap limits how many write operations (op.upsert/update/delete) a recording lets
through. Once it is reached, the next write raises MaxRecordsReached, which halts the connector's
update() and is treated as a normal, successful end of sync. The cap (default 100) is stored as
"capped_count" in the fixture header, and a replay applies the recorded cap so it stops at the same write.
"""

import threading
from typing import Optional

DEFAULT_MAX_RECORDS = 100


class MaxRecordsReached(Exception):
    """
    Control-flow signal raised by op.upsert/update/delete once the
    --max-records cap is reached. It is caught at the SDK's Update() RPC boundary
    and treated as a normal end of sync.

    Because it is an ordinary Exception, connector code that wraps a write in
    `except Exception` can swallow it. The connector then keeps running, but its
    later writes are still rejected, so no extra records are written.

    Because it unwinds like any other exception, only the author's try/finally
    blocks run; cleanup written as plain statements after the halted loop is skipped.
    """


class MaxRecordHandler:
    """
    Class-level cap state, shared between the CLI, which starts and stops a recording or replay, and
    Operations, which runs deep inside connector code where no instance can be passed around.
    """

    _capped_count: Optional[int] = None
    _write_attempts: int = 0

    # Guards _capped_count and _write_attempts, because connectors may call op.* from several threads.
    _lock: threading.Lock = threading.Lock()

    @classmethod
    def start(cls, max_records: int = DEFAULT_MAX_RECORDS) -> None:
        """Reset the counters and set the cap."""
        with cls._lock:
            cls._write_attempts = 0
            cls._capped_count = max_records

    @classmethod
    def stop(cls) -> None:
        """Remove the cap and zero the counters. Safe to call when not recording or replaying."""
        with cls._lock:
            cls._capped_count = None
            cls._write_attempts = 0

    @classmethod
    def capped_count(cls) -> Optional[int]:
        """The active cap, or None when no recording or replay is in progress."""
        return cls._capped_count

    @classmethod
    def _cap_exceeded_locked(cls) -> bool:
        """True once more writes have been attempted than --max-records allows. Caller must already hold _lock."""
        return cls._capped_count is not None and cls._write_attempts > cls._capped_count

    @classmethod
    def is_stopped_by_cap(cls) -> bool:
        """True once a write was rejected for exceeding --max-records, so the sync is already ending."""
        if cls._capped_count is None:
            return False
        with cls._lock:
            return cls._cap_exceeded_locked()

    @classmethod
    def raise_if_cap_reached(cls) -> None:
        """
        Called by Operations.upsert/update/delete before a record is built.

        Every call is counted. The first `capped_count` pass; the next one, and every
        one after it, raises MaxRecordsReached. The count and the check happen together
        under the lock, so concurrent threads can never both slip past the cap. The check
        runs before the record is built because thread pools keep running queued tasks
        after one of them raised.

        Does nothing, and takes no lock, when no cap is active, so a normal `fivetran debug` is unaffected.
        """
        if cls._capped_count is None:
            return
        with cls._lock:
            capped_count = cls._capped_count
            if capped_count is None:
                return
            cls._write_attempts += 1
            over_cap = cls._cap_exceeded_locked()
        if over_cap:
            raise MaxRecordsReached(
                f"--max-records cap of {capped_count} operations "
                "reached; stopping the sync early by design."
            )
