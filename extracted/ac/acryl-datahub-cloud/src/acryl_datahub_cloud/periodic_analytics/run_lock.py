import logging
from datetime import datetime, timedelta, timezone
from typing import Callable, Dict, Optional, Protocol, Tuple

import boto3
from botocore.exceptions import ClientError
from pydantic import BaseModel

from acryl_datahub_cloud.periodic_analytics.config import ObjectStorageConfig
from acryl_datahub_cloud.periodic_analytics.storage import ObjectStore
from datahub.ingestion.api.source import SourceReport

logger = logging.getLogger(__name__)

# A steal races the process that let the lease expire (or another watcher
# that noticed the same expiry) — bounded so a pathological hot loop of
# simultaneous stealers can't spin forever, not because 3 is a principled
# number.
_MAX_STEAL_ATTEMPTS = 3
_PRECONDITION_FAILED_CODES = ("PreconditionFailed", "412")
_NOT_FOUND_CODES = ("NoSuchKey", "404")
# Executor clocks are assumed NTP-synced, but not perfectly — a stealer
# whose clock runs even a little ahead of the lease holder's could otherwise
# treat a still-live lease as expired and steal it early. Requiring the
# lease to be expired by more than this margin (not just expired) bounds how
# far ahead a stealer's clock can be before it causes a premature steal.
_DEFAULT_STEAL_SKEW_MINUTES = 5


class Lease(BaseModel):
    """Lock body. Timestamps are UTC ISO-8601 strings (not floats) so a raw
    `read_json`/manual S3 console dump of the lock object is human-readable."""

    run_id: str
    acquired_at: str
    expires_at: str

    def is_expired(self, now: datetime) -> bool:
        return datetime.fromisoformat(self.expires_at) <= now


class RunLockOwnershipLostError(RuntimeError):
    """Raised when a run discovers, immediately before a watermark/ledger
    commit, that its lease has been stolen. The tenant now belongs to
    whichever run stole it, so the run must abort rather than write state
    the new owner is also writing."""


class LockClient(Protocol):
    """A conditional-write key/value store — enough to build a lease lock on
    top of. Implementations only need to distinguish "already exists"/"etag
    mismatch" from "any other failure": the former are the expected
    contention cases, the latter must propagate so a broken lock backend
    fails the run loudly rather than silently disabling the protection it
    provides."""

    def create_if_absent(self, key: str, body: bytes) -> bool:
        """Create the object at `key` only if it doesn't already exist.
        Returns True if created, False if something is already there.
        Raises for any other failure (network, permissions, ...)."""
        ...

    def read(self, key: str) -> Optional[bytes]:
        """Return the object body, or None if `key` doesn't exist."""
        ...

    def read_with_etag(self, key: str) -> Optional[Tuple[bytes, str]]:
        """Return (body, etag), or None if `key` doesn't exist. The etag is
        needed to steal an expired lease via compare-and-swap rather than a
        blind delete-then-create."""
        ...

    def put_if_match(self, key: str, body: bytes, etag: str) -> bool:
        """Overwrite `key` with `body` only if its current etag still equals
        `etag`. Returns True if the write landed, False if the object
        changed underneath (someone else already wrote it — a lost CAS
        race, not an error). Raises for any other failure."""
        ...

    def delete(self, key: str) -> None:
        """Delete the object at `key`. No-op if it's already gone."""
        ...


class S3LockClient:
    """Real S3-backed lock client. Conditional create relies on IfNoneMatch
    support (native S3 and most S3-compatible stores as of 2024); conditional
    overwrite relies on IfMatch on PUT (native S3 since 2024). Nothing here is
    emulated with a read-then-write race."""

    def __init__(self, bucket: str) -> None:
        self._bucket = bucket
        # Credentials come from pod identity / the default boto3 chain, same
        # as pyarrow's S3FileSystem in storage.py — no separate credential
        # wiring needed here.
        self._client = boto3.client("s3")

    def create_if_absent(self, key: str, body: bytes) -> bool:
        try:
            self._client.put_object(
                Bucket=self._bucket, Key=key, Body=body, IfNoneMatch="*"
            )
            return True
        except ClientError as e:
            if _error_code(e) in _PRECONDITION_FAILED_CODES:
                return False
            raise

    def read(self, key: str) -> Optional[bytes]:
        try:
            response = self._client.get_object(Bucket=self._bucket, Key=key)
            body: bytes = response["Body"].read()
            return body
        except ClientError as e:
            if _error_code(e) in _NOT_FOUND_CODES:
                return None
            raise

    def read_with_etag(self, key: str) -> Optional[Tuple[bytes, str]]:
        try:
            response = self._client.get_object(Bucket=self._bucket, Key=key)
            body: bytes = response["Body"].read()
            etag: str = response["ETag"]
            return body, etag
        except ClientError as e:
            if _error_code(e) in _NOT_FOUND_CODES:
                return None
            raise

    def put_if_match(self, key: str, body: bytes, etag: str) -> bool:
        try:
            self._client.put_object(
                Bucket=self._bucket, Key=key, Body=body, IfMatch=etag
            )
            return True
        except ClientError as e:
            if _error_code(e) in _PRECONDITION_FAILED_CODES:
                return False
            raise

    def delete(self, key: str) -> None:
        # delete_object is already idempotent server-side (no error on a
        # missing key), so no existence check is needed here.
        self._client.delete_object(Bucket=self._bucket, Key=key)


def _error_code(e: ClientError) -> Optional[str]:
    return e.response.get("Error", {}).get("Code")


class InMemoryLockClient:
    """Fake LockClient for tests — a dict plus a per-key generation counter
    that stands in for a real backend's ETag, no moto/network involved.
    Shared across RunLock instances in the same process to simulate multiple
    runs contending for the same lock.

    The generation counter is what makes put_if_match a faithful CAS rather
    than an unconditional write: a caller can only win by presenting the
    etag it actually read, and every successful write (create or CAS put)
    bumps the counter so a stale etag can never match again. This is what
    lets a test express "two contenders both read the same expired lease,
    only one of their writes should land" — a blind delete-then-create fake
    has no way to make that assertion meaningful."""

    def __init__(self) -> None:
        self._objects: Dict[str, bytes] = {}
        self._etags: Dict[str, str] = {}
        self._generation = 0

    def _bump_etag(self, key: str) -> str:
        self._generation += 1
        etag = f"g{self._generation}"
        self._etags[key] = etag
        return etag

    def create_if_absent(self, key: str, body: bytes) -> bool:
        if key in self._objects:
            return False
        self._objects[key] = body
        self._bump_etag(key)
        return True

    def read(self, key: str) -> Optional[bytes]:
        return self._objects.get(key)

    def read_with_etag(self, key: str) -> Optional[Tuple[bytes, str]]:
        if key not in self._objects:
            return None
        return self._objects[key], self._etags[key]

    def put_if_match(self, key: str, body: bytes, etag: str) -> bool:
        if self._etags.get(key) != etag:
            return False
        self._objects[key] = body
        self._bump_etag(key)
        return True

    def delete(self, key: str) -> None:
        self._objects.pop(key, None)
        self._etags.pop(key, None)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class RunLock:
    """Distributed lease lock so at most one run of a given source kind
    executes per tenant at a time (see storage.ObjectStore.lock_key for how
    the key is scoped). Usage::

        with RunLock(client, key, run_id, lease_minutes, report) as acquired:
            if not acquired:
                return  # another run holds the lock, or the run lock is
                         # unavailable for this provider -- see build_run_lock
            ...
            run_lock.verify_ownership()  # before each watermark/ledger commit
            ...

    `client=None` means "no lock backend available for this provider" (see
    `build_run_lock`) -- the run proceeds without the protection this lock
    provides, so `acquired` is always True in that case.
    """

    def __init__(
        self,
        client: Optional[LockClient],
        key: str,
        run_id: str,
        lease_minutes: int,
        report: SourceReport,
        now_fn: Callable[[], datetime] = _utcnow,
        steal_skew_minutes: int = _DEFAULT_STEAL_SKEW_MINUTES,
    ) -> None:
        self._client = client
        self._key = key
        self._run_id = run_id
        self._lease_duration = timedelta(minutes=lease_minutes)
        self._report = report
        self._now_fn = now_fn
        self._steal_skew = timedelta(minutes=steal_skew_minutes)
        self._acquired = False

    def __enter__(self) -> bool:
        self._acquired = self._acquire()
        return self._acquired

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        if self._acquired:
            self._release()

    def _acquire(self) -> bool:
        if self._client is None:
            return True

        for _ in range(_MAX_STEAL_ATTEMPTS):
            if self._client.create_if_absent(self._key, self._new_lease_body()):
                return True

            existing = self._client.read_with_etag(self._key)
            if existing is None:
                # Raced with a concurrent release/steal between our failed
                # create and this read -- the key may be free again now, so
                # retry immediately rather than counting this as a hold.
                continue

            body, etag = existing
            lease = Lease.model_validate_json(body)
            if not lease.is_expired(self._now_fn() - self._steal_skew):
                return False  # a live run genuinely holds this lock

            # Expired beyond the skew buffer -- steal via compare-and-swap:
            # overwrite ONLY if the object is still exactly what we just
            # read (same etag). If another stealer's CAS lands first, our
            # put_if_match sees a changed etag and returns False -- we lose
            # this attempt cleanly and loop back to re-read, rather than
            # blindly deleting (which is what let two stealers both "win"
            # before this fix: an unconditional delete doesn't check what it
            # removes, so it could delete a competitor's freshly-written
            # lease instead of the stale one we saw).
            if self._client.put_if_match(self._key, self._new_lease_body(), etag):
                return True

        return False

    def _new_lease_body(self) -> bytes:
        now = self._now_fn()
        lease = Lease(
            run_id=self._run_id,
            acquired_at=now.isoformat(),
            expires_at=(now + self._lease_duration).isoformat(),
        )
        return lease.model_dump_json().encode("utf-8")

    def verify_ownership(self) -> bool:
        """Cheap re-check that we still hold the lease -- call immediately
        before any watermark/ledger commit. An overrunning run (a real run
        that took longer than lock_lease_minutes) can have its lease stolen
        mid-run; without this check the old run keeps writing state the
        steal winner also owns until `_release`'s post-hoc check catches
        it -- by which point the damage (a watermark or ledger entry written
        by both runs) is already done. Returns True when there is no lock
        backend (client=None) or the lease is still ours; False if another
        run's lease now holds the key."""
        if self._client is None:
            return True
        existing = self._client.read(self._key)
        if existing is None:
            return False
        lease = Lease.model_validate_json(existing)
        return lease.run_id == self._run_id

    def _release(self) -> None:
        if self._client is None:
            return

        existing = self._client.read_with_etag(self._key)
        if existing is None:
            return  # already gone -- nothing to release

        body, etag = existing
        lease = Lease.model_validate_json(body)
        if lease.run_id != self._run_id:
            # Our own run overran lock_lease_minutes and another run stole
            # the lock while we were still working -- deleting now would
            # release a lock we no longer own, letting a third run in on top
            # of the run that stole it. Leave it alone and surface this
            # loudly: it means the lease default is too short for this
            # tenant's real run time.
            self._report.warning(
                title="Run lock was stolen before release",
                message="another run's lease now holds this lock -- not deleting "
                "it. This run's lock_lease_minutes was too short for how long "
                "the run actually took.",
                context=self._key,
            )
            return

        # Important-1: CAS-release, not a blind delete. The read above only
        # proves WE owned the lease at that instant -- an unconditional
        # delete has a TOCTOU gap between that read and this write: if our
        # own lease expires (or a clock hiccup makes a steal look valid) and
        # a steal lands in that gap, a blind delete here would remove the new
        # owner's freshly-written lease instead of our own stale one (the
        # same class of bug the acquire-side steal was fixed for). Releasing
        # via put_if_match keyed on the etag we just read makes the release
        # land only if nothing changed underneath.
        #
        # We CAS-PUT an already-expired tombstone rather than trying to
        # delete conditionally -- object stores commonly support conditional
        # PUT (IfMatch) but not conditional DELETE. The tombstone's
        # expires_at is far enough in the past that the next acquirer's
        # normal expired-lease steal path (see _acquire) picks it up
        # immediately, which is functionally equivalent to deletion for the
        # uncontended case.
        if not self._client.put_if_match(self._key, self._tombstone_body(), etag):
            self._report.warning(
                title="Run lock was stolen before release",
                message="the lease changed between reading it and releasing it "
                "-- another run's steal landed in that gap. Not releasing; the "
                "new owner's lease is left intact.",
                context=self._key,
            )

    def _tombstone_body(self) -> bytes:
        now = self._now_fn()
        lease = Lease(
            run_id=self._run_id,
            acquired_at=now.isoformat(),
            expires_at=(now - self._steal_skew - timedelta(minutes=1)).isoformat(),
        )
        return lease.model_dump_json().encode("utf-8")


def build_run_lock(
    store: ObjectStore,
    source_kind: str,
    metric_family: str,
    run_id: str,
    lease_minutes: int,
    report: SourceReport,
    now_fn: Callable[[], datetime] = _utcnow,
    steal_skew_minutes: int = _DEFAULT_STEAL_SKEW_MINUTES,
) -> RunLock:
    """Picks the right LockClient for `store.config.provider` and wraps it in
    a RunLock keyed on (tenant, source_kind, metric_family)."""
    return RunLock(
        client=_build_lock_client(store.config, source_kind, report),
        key=store.lock_key(source_kind, metric_family),
        run_id=run_id,
        lease_minutes=lease_minutes,
        report=report,
        now_fn=now_fn,
        steal_skew_minutes=steal_skew_minutes,
    )


def _build_lock_client(
    config: ObjectStorageConfig, source_kind: str, report: SourceReport
) -> Optional[LockClient]:
    if config.provider == "s3":
        return S3LockClient(bucket=config.bucket.split("://", 1)[-1].rstrip("/"))
    if config.provider == "gcs":
        # TODO: google-cloud-storage (for if_generation_match=0 conditional
        # create) isn't a periodic_analytics dependency -- only boto3 is,
        # for S3 -- so there's no conditional-create client to build here
        # yet. Add the dependency and a GcsLockClient before relying on this
        # lock for a gcs-provider tenant.
        report.warning(
            title="Run lock unavailable for gcs provider",
            message="no conditional-create client available for gcs -- "
            "proceeding without the concurrent-run lock. Two concurrent runs "
            "over the same tenant could double-count buckets or corrupt "
            "manifests.",
            context=source_kind,
        )
        return None
    # provider=local -- tests and local debug runs are single-process by
    # construction, so there's nothing for a lock to protect against.
    return None
