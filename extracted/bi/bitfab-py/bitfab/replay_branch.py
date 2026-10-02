"""The database branch a single replay item runs against.

``get_current_replay_branch()`` hands you one inside a replayed function when
the source trace carried a DB snapshot reference and the Bitfab service
resolved a branch from it. Outside a replay item, or when no branch was
resolved, that accessor returns ``None`` and your code keeps reading
``os.environ["DATABASE_URL"]`` the normal way.

Immutable and scoped to one item: the accessor builds it from the replay
``ContextVar``, so parallel replay items each see their own branch and no
lease state lives on a long-lived object.

Internally the resolved per-item state is a ``DbBranchLease`` (the SDK/server
protocol term). Its useful fields are exposed directly here so customer code
never sees the word.
"""

from __future__ import annotations

import re
from typing import Any, TypedDict


class DbBranchLease(TypedDict, total=False):
    """Per-item DB branch the Bitfab service resolved from the source trace's
    ``db_snapshot_ref``. Carried on the replay context (camelCase keys, since
    it arrives straight off the wire). ``neonBranchId`` is the literal Neon
    branch id; passing it to ``release_db_branch_lease`` deletes that branch.
    """

    neonBranchId: str
    envKey: str
    databaseUrl: str
    expiresAt: str
    # The instant the branch was pinned to (the source trace's wall clock).
    # Echoed back in db_snapshot_usage on the replayed trace's completion.
    snapshotTimestamp: str
    providerConsoleUrl: str
    readOnly: bool
    region: str


class DbBranchOptions(TypedDict, total=False):
    """How the DB snapshot branch each replay item runs against is sized and
    warmed. Passed as ``client.replay(db_branch={...})``. Every key is
    optional, so this dict is only worth passing to override the mirror
    project's own sizing; to branch with those defaults, pass
    ``db_branch=True``.

    Attributes:
        min_cu: Autoscaling floor for the branch's compute, in Neon Compute
            Units (0.25 to 56). Omit to keep the mirror project's own default.
            Raise it when the mirror is provisioned smaller than the database
            it stands in for, so replay latency reflects your code rather than
            a cold, undersized branch.
        max_cu: Autoscaling ceiling, in Neon Compute Units. Equal to ``min_cu``
            pins the size, which keeps items comparable: otherwise a later item
            can run against an endpoint that already scaled up and post a
            better number for the same code.
        warmup_sql: SQL that warms the branch's cache. The server appends it to
            the branch's readiness check, so it runs BEFORE your function sees
            the branch and its time is not charged to the replayed call.
            Invalid SQL fails the branch rather than silently leaving it cold.
    """

    min_cu: float
    max_cu: float
    warmup_sql: str


def _snake_case(key: str) -> str:
    """Convert a camelCase lease key to its snake_case attribute name.

    Two passes so a run of capitals stays one word: ``dbURL`` is ``db_url``,
    not ``db_u_r_l``. Must match the Ruby SDK's conversion exactly, or the same
    server field would arrive under different names in the two SDKs.
    """
    return re.sub(
        r"([a-z\d])([A-Z])",
        r"\1_\2",
        re.sub(r"([A-Z\d]+)([A-Z][a-z])", r"\1_\2", key),
    ).lower()


_LEASE_FIELDS = (
    "neon_branch_id",
    "env_key",
    "expires_at",
    "snapshot_timestamp",
    "provider_console_url",
    "read_only",
    "region",
)


class ReplayBranch:
    """The database branch resolved for the replay item currently running."""

    # __slots__ is load-bearing, not an optimization: without it the instance
    # grows a __dict__ carrying _url, and anything that walks it (a logged
    # obj.__dict__, json.dumps with default=vars) would print the connection
    # string that __repr__ exists to redact.
    __slots__ = ("_context", "_extra", "_url", "trace_id", *_LEASE_FIELDS)

    #: The provider's own id for this branch, e.g. for correlating with its console.
    neon_branch_id: str
    #: Env var name the customer's app reads, e.g. ``DATABASE_URL``.
    env_key: str
    #: When this branch's URL stops being valid. ISO-8601.
    expires_at: str
    #: The instant this branch is pinned to: the source trace's wall clock,
    #: read just before the traced function ran. Compare it against the trace
    #: you meant to replay to confirm the branch is the right point in history.
    snapshot_timestamp: str | None
    #: Deep link to the branch in the provider console, if available.
    provider_console_url: str | None
    #: True if the branch is read-only. Use it to skip write operations
    #: during replay when the provider returned a read-only lease.
    read_only: bool | None
    #: The branch's region, e.g. ``aws-us-east-1``. A compute runs in its
    #: project's region, so a replay runner elsewhere pays that round trip
    #: on every query.
    region: str | None
    #: The historical trace ID that produced the input for this replay item.
    trace_id: str

    def __init__(
        self, lease: DbBranchLease, trace_id: str, context: dict[str, Any]
    ) -> None:
        """Built by :func:`get_current_replay_branch`; never constructed by callers."""
        # Copy the lease wholesale minus the connection string, so a field the
        # server starts sending reaches customer code without an SDK release.
        # Everything set here must stay plain data: ``database_url`` is the only
        # member allowed to mark the branch as accessed.
        self._extra: dict[str, Any] = {}
        for field in _LEASE_FIELDS:
            setattr(self, field, None)
        for key, value in lease.items():
            if key == "databaseUrl":
                continue
            name = _snake_case(key)
            if name in _LEASE_FIELDS:
                setattr(self, name, value)
            else:
                self._extra[name] = value
        self.trace_id = trace_id
        self._url = lease["databaseUrl"]
        self._context = context

    def __getattr__(self, name: str) -> Any:
        """Resolve a lease field this SDK version has no slot for."""
        if name == "_extra":
            raise AttributeError(name)
        try:
            return self._extra[name]
        except KeyError:
            raise AttributeError(name) from None

    @property
    def database_url(self) -> str:
        """Connection string for this item's branch. Point your database client
        at it instead of the live database for the duration of the replayed
        call.

        Reading it records on the trace that the replayed code obtained the
        branch URL, which is what separates "a branch was provisioned" from
        "the branch was actually used". The other fields inspect the lease
        without exposing the connection string, so they deliberately do not
        record anything.
        """
        self._context["db_snapshot_accessed"] = True
        return self._url

    def __repr__(self) -> str:
        """Redact the connection string so a logged branch cannot leak it."""
        return (
            f"ReplayBranch(trace_id={self.trace_id!r}, "
            f"expires_at={self.expires_at!r}, region={self.region!r}, "
            f"read_only={self.read_only!r}, "
            f"snapshot_timestamp={self.snapshot_timestamp!r})"
        )
