"""Run once per key — a step's successful result reused across runs (``data.once``).

THE GENERAL PROBLEM. A step that costs money or writes records must, for the same logical
work, happen once: across a retry, a crash/resume, a second start of the same build, a
re-fired trigger, or a fan-out that produces the same item twice. Outcome replay
(``Checkpointer.get_outcome``) guarantees that only inside ONE run at ONE exact position.
``data.once`` widens it to a declared scope, and the scheduler decides BEFORE paying.

Authored on a node (opt-in, per step)::

    "data": {"once": {
        "key": ["kit_id", "build_id", "target"],  # dotted paths into the step's RESOLVED inputs;
                                                   # [] / absent = the whole input is the key
        "scope": "workflow",                       # run | workflow | organization
        "keep_days": 90,                           # absent = knob default; null = no expiry
        "on_changed_inputs": "run_again",          # run_again (default) | reuse_and_flag
        "share_across_users": false                # default: each person's runs keep their own result
    }}

THE RULES (each one has a test in ``tests/test_once_per_key.py``):

* The key comes from the step's resolved, schema-validated inputs — never from a request body.
* Identity is ``(organization, scope, scope id, step type, key)``. The organization is ALWAYS
  part of it, so a definition shared into another organization never sees this one's results.
  The stored key also covers the step's own SETTINGS (config + output kind), so two steps of the
  same type set up differently never collide, and the ACTING USER — one person's result is never
  another's unless the step declares ``share_across_users: true`` (the Studio says so).
* Files: every ``file_id`` in the inputs enters the digest as its CONTENT identity (the host's
  ``configure_file_identity_resolver``: content hash, else version/updated_at), never the id
  alone. A file with no identity (or no resolver) → the step runs, never reuses, and is flagged.
* The input digest = every resolved input + the node config (incl. a one-off override) + the
  output kind + the step type's own version (``NodeSpec.version``) + whatever the step says
  decides its answer besides its inputs (``executor.result_version`` — an AI step names the
  agent/mandate Holder and its version, so a prompt or model change is a miss). An AI step
  (category agent/llm) that cannot name its version never reuses: it runs and is flagged.
* Same key + same digest → the step does not run; a normal outcome is recorded with
  ``source="reused"`` and ``metadata.reused_from`` naming the origin run/step.
* Same key + different digest → runs again (default) and replaces the row, raising the
  ``engine.once_inputs_changed`` review flag; ``reuse_and_flag`` reuses and flags.
* A miss of a step that has an earlier saved answer in its scope (this key or any other), whose
  changed input fields — against the closest earlier input — all come from upstream steps that
  answered fresh in this run (not reused, not PURE), raises one ``engine.once_missed_upstream``
  flag naming them (instead of ``engine.once_inputs_changed``). A true first run raises nothing.
* Miss → a CLAIM with a lease. Another run (or a fan-out sibling) with the same key WAITS for
  the claimer instead of paying in parallel; the claimer renews the lease while it works; a
  claimer that dies stops renewing and the first waiter after expiry takes over.
* Never stored: failures, skips, manual or mocked results, results that dispatched Sends or
  wrote channels through ``ctx.channels`` (those are run topology, not a value), and DEGRADED
  results — the step warned or raised a review flag, its output failed its shape check, or the
  check could not run. The outcome says why (``metadata.once_not_saved``).
* A result whose stored value can no longer be read (its origin run's value store is gone) is
  a miss, never an error — and only THAT result is skipped: a fresh one another run settles
  meanwhile is reused. A reused result holding values on the server (``hold_on_server``) brings
  them into the reusing run, or is a miss when they are gone.
* A broken store never blocks a run and never hides: the step runs and the step carries an
  ``engine.once_unavailable`` review flag (deciding, reading, or saving failed; a lost claim).

The store is injected like the work-set store: :class:`MemoryStepResultStore` by default
(standalone, single process); aidream wires :class:`PostgresStepResultStore` over
``workflow.step_result``.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime, timedelta
from typing import Any, Literal, Protocol, runtime_checkable
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, ValidationError

logger = logging.getLogger(__name__)

OnceScope = Literal["run", "workflow", "organization"]

class OncePolicy(BaseModel):
    """A parsed ``data.once`` setting."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    key: list[str] = Field(default_factory=list)
    scope: OnceScope = "workflow"
    #: Days a stored result stays reusable. ``None`` = no expiry. When the author leaves it
    #: out, ``keep_days_from_knob`` is True and the ``workflow.once`` knob decides.
    keep_days: int | None = Field(default=None, ge=1, le=36_500)
    keep_days_from_knob: bool = True
    on_changed_inputs: Literal["run_again", "reuse_and_flag"] = "run_again"
    #: Off (default): the acting user is part of the key — one person's result is never
    #: another's. On: everyone in the organization (within the scope) shares the result.
    share_across_users: bool = False


def parse_once(raw: Any) -> OncePolicy | None:
    """``data.once`` → :class:`OncePolicy`; None when absent. Raises ``ValueError`` (with the
    reason) on a malformed setting — the compiler turns it into a CompilationError."""
    if raw is None or raw is False:
        return None
    if raw is True:
        return OncePolicy()
    if not isinstance(raw, dict):
        raise ValueError(f"expected an object or true, got {type(raw).__name__}")
    data = dict(raw)
    keep_from_knob = "keep_days" not in data
    if "keep_days_from_knob" in data:
        raise ValueError("unknown key 'keep_days_from_knob'")
    key = data.get("key", [])
    if isinstance(key, str):
        data["key"] = [key]
    elif key is None:
        data["key"] = []
    try:
        policy = OncePolicy.model_validate({**data, "keep_days_from_knob": keep_from_knob})
    except ValidationError as exc:
        raise ValueError(str(exc)) from exc
    for path in policy.key:
        if not path.strip() or any(not part for part in path.split(".")):
            raise ValueError(f"key part {path!r} is not a dotted path into the step's inputs")
    return policy


# ── key and digest ───────────────────────────────────────────────────────────


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str, ensure_ascii=False)


def _sha(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


_MISSING = object()


def _at_path(value: Any, path: str) -> Any:
    for part in path.split("."):
        if isinstance(value, dict):
            if part not in value:
                return _MISSING
            value = value[part]
        elif isinstance(value, list) and part.lstrip("-").isdigit():
            index = int(part)
            if not -len(value) <= index < len(value):
                return _MISSING
            value = value[index]
        else:
            return _MISSING
    return value


def settings_digest(config: Any, output_kind: str | None) -> str:
    """The step's own settings — part of its key, so differently set-up steps never collide."""
    return _sha({"config": config, "output_kind": output_kind})


def result_key(
    step_type: str,
    policy: OncePolicy,
    inputs: dict[str, Any],
    *,
    settings: str = "",
    actor: str | None = None,
) -> tuple[str | None, list[str]]:
    """The stored key for these inputs, or ``(None, missing_paths)`` when a declared key part
    is absent from them (the step then runs normally and the engine flags it).

    ``settings`` (:func:`settings_digest`) and ``actor`` (the acting user; ignored when the
    policy shares across users) are part of every key."""
    who = None if policy.share_across_users else (actor or "")
    if not policy.key:
        return _sha({"step_type": step_type, "settings": settings, "actor": who, "inputs": inputs}), []
    parts: list[Any] = []
    missing: list[str] = []
    for path in policy.key:
        value = _at_path(inputs, path)
        if value is _MISSING:
            missing.append(path)
        parts.append(None if value is _MISSING else value)
    if missing:
        return None, missing
    return _sha({"step_type": step_type, "settings": settings, "actor": who, "paths": policy.key, "parts": parts}), []


def file_ids_in(value: Any) -> set[str]:
    """Every file a step's inputs reference by id: a ``file_id`` string (a MediaRef or any
    object carrying one) or a ``file_ids`` list, at any depth."""
    found: set[str] = set()
    stack = [value]
    while stack:
        item = stack.pop()
        if isinstance(item, dict):
            for k, v in item.items():
                if k == "file_id" and isinstance(v, str) and v.strip():
                    found.add(v.strip())
                elif k == "file_ids" and isinstance(v, list):
                    found.update(x.strip() for x in v if isinstance(x, str) and x.strip())
                else:
                    stack.append(v)
        elif isinstance(item, list):
            stack.extend(item)
    return found


def input_digest(
    *,
    inputs: dict[str, Any],
    config: Any,
    output_kind: str | None,
    step_version: str,
    result_version: str | None,
    file_identities: dict[str, str] | None = None,
) -> str:
    """Everything that decides the step's answer. Two digests are equal only when reusing the
    result is exactly as good as running the step again. ``file_identities``: each referenced
    file's content identity (a file edited under the same id is a different input)."""
    return _sha(
        {
            "inputs": inputs,
            "config": config,
            "output_kind": output_kind,
            "step_version": step_version,
            "result_version": result_version,
            "files": file_identities or {},
        }
    )


# ── store contract ───────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class StepResultKey:
    organization_id: str
    scope: OnceScope
    scope_id: str
    step_type: str
    result_key: str


@dataclass(frozen=True, slots=True)
class ClaimPosition:
    """Where a claim was made — the invocation's correlation identity. A claim made at MY exact
    position is my own earlier life (a crashed leg of this run being resumed) and is taken over
    at once instead of waiting out its lease."""

    run_id: str
    node_id: str
    dispatch_id: str = ""
    item_index: int = 0


@dataclass(frozen=True, slots=True)
class StoredResult:
    input_digest: str
    output: dict[str, Any]
    output_kind: str | None
    verdict: dict[str, Any]
    emissions: dict[str, Any]
    origin_run_id: str
    origin_node_id: str
    origin_step: int
    origin_dispatch_id: str
    origin_item_index: int
    origin_attempt: int
    succeeded_at: datetime
    expires_at: datetime | None
    #: Digest of what the ORIGIN run was started with (its subject: brand, topic, a child's input).
    #: A miss is explained only against earlier answers of runs started with the same thing.
    run_input_digest: str | None = None
    #: The organization the ORIGIN run lives in. A step set to run in another organization
    #: (``data.in_organization``) saves its result THERE, so the producing run can live elsewhere;
    #: the row then never points across organizations (the database refuses it) and keeps the
    #: origin in its system-owned metadata instead. None = the result's own organization.
    origin_organization_id: str | None = None


@dataclass(frozen=True, slots=True)
class StepResultRow:
    """One row as read — the result half and the claim half are independent: a row being
    re-produced (bypass, changed inputs, expiry) keeps its previous good result until the new
    one is settled, so a failed re-run never destroys it."""

    id: str
    result: StoredResult | None
    claim_token: str | None
    claim_position: ClaimPosition | None
    lease_expires_at: datetime | None


@runtime_checkable
class StepResultStore(Protocol):
    """Durable claims and results for ``data.once``.

    Every write is a compare-and-swap on what the caller observed, so two processes deciding
    from the same read can never both win: ``insert_claim`` relies on the identity's unique
    constraint, ``take_claim`` on ``(id, claim_token, succeeded_at)`` being unchanged, and
    ``settle``/``release``/``renew`` on the caller still holding ``claim_token``.
    """

    async def read(self, key: StepResultKey) -> StepResultRow | None: ...

    async def insert_claim(
        self, key: StepResultKey, *, token: str, position: ClaimPosition, lease_until: datetime
    ) -> bool: ...

    async def take_claim(
        self,
        key: StepResultKey,
        *,
        row_id: str,
        observed_token: str | None,
        observed_succeeded_at: datetime | None,
        token: str,
        position: ClaimPosition,
        lease_until: datetime,
    ) -> bool: ...

    async def renew(self, key: StepResultKey, *, token: str, lease_until: datetime) -> bool: ...

    async def settle(self, key: StepResultKey, *, token: str, result: StoredResult) -> bool: ...

    async def release(self, key: StepResultKey, *, token: str) -> None: ...

    async def resolve_output(self, result: StoredResult) -> dict[str, Any]:
        """The stored output with every by-reference value read back. Raises ``LookupError``
        when a referenced value is gone (the caller treats that as a miss)."""
        ...

    async def wait(self, key: StepResultKey, seconds: float) -> None:
        """Return when the row may have changed, or after ``seconds``."""
        ...


# ── the decision ─────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class Hit:
    result: StoredResult
    #: The stored digest differs from mine — only reachable under ``reuse_and_flag``.
    digest_changed: bool


@dataclass(slots=True)
class Claim:
    key: StepResultKey
    token: str
    #: A live or expired claim was taken from someone else (a dead claimer, or my own
    #: earlier life) — not a fresh row.
    took_over: bool
    #: A good result exists but is being replaced (changed inputs / bypass / expiry).
    replacing: StoredResult | None
    #: The result is being written under this claim — a renewal that now finds the claim
    #: cleared is the settle landing, not a takeover.
    settling: bool = False
    settled: bool = False
    renewer: asyncio.Task[None] | None = field(default=None, repr=False)


@dataclass(frozen=True, slots=True)
class Wait:
    holder: ClaimPosition | None
    lease_expires_at: datetime | None


#: Consecutive lost compare-and-swaps after which ``acquire`` calls the store broken. Structural
#: (a healthy store never comes near it), not a tuning knob.
MAX_LOST_SWAPS = 50


class StepResultStoreError(RuntimeError):
    """The step-result store misbehaves (not contention): the caller runs the step and says so."""


def _usable(result: StoredResult | None, now: datetime) -> bool:
    return result is not None and (result.expires_at is None or result.expires_at > now)


async def acquire(
    store: StepResultStore,
    key: StepResultKey,
    *,
    digest: str,
    position: ClaimPosition,
    lease_seconds: float,
    reuse_changed: bool,
    bypass: bool,
    unusable_at: datetime | None = None,
    now: Callable[[], datetime] | None = None,
) -> Hit | Claim | Wait:
    """Decide for ONE invocation: reuse a stored result, hold the claim to produce it, or wait
    for the invocation that holds it now. Never raises on contention; a store error propagates
    (the caller runs the step normally and screams).

    ``unusable_at``: the ``succeeded_at`` of a stored result this invocation already found
    unusable (its values are gone, or it no longer fits the step's output). Only THAT result is
    ignored — a fresh one another invocation settles meanwhile is reused, never paid for twice.
    """
    clock = now or (lambda: datetime.now(UTC))
    # A lost compare-and-swap means another writer moved the row forward (claimed it, settled
    # it, released it), and the next read sees that move — so a healthy store settles within a
    # few rounds. A store whose swaps never land (its read disagrees with its unique index, a
    # filter that never matches what it returned) would spin here forever, hammering the
    # database: past MAX_LOST_SWAPS it is a broken store and says so.
    for _round in range(MAX_LOST_SWAPS):
        row = await store.read(key)
        moment = clock()
        lease_until = moment + timedelta(seconds=lease_seconds)
        if row is None:
            token = str(uuid4())
            if await store.insert_claim(key, token=token, position=position, lease_until=lease_until):
                return Claim(key=key, token=token, took_over=False, replacing=None)
            continue
        result = row.result
        if unusable_at is not None and result is not None and result.succeeded_at == unusable_at:
            result_usable = False
        else:
            result_usable = _usable(result, moment)
        if not bypass and result_usable:
            assert result is not None
            if result.input_digest == digest:
                return Hit(result=result, digest_changed=False)
            if reuse_changed:
                return Hit(result=result, digest_changed=True)
        claim_live = (
            row.claim_token is not None
            and row.lease_expires_at is not None
            and row.lease_expires_at > moment
        )
        if claim_live and row.claim_position != position:
            return Wait(holder=row.claim_position, lease_expires_at=row.lease_expires_at)
        token = str(uuid4())
        if await store.take_claim(
            key,
            row_id=row.id,
            observed_token=row.claim_token,
            observed_succeeded_at=result.succeeded_at if result is not None else None,
            token=token,
            position=position,
            lease_until=lease_until,
        ):
            return Claim(
                key=key,
                token=token,
                took_over=row.claim_token is not None,
                replacing=result if _usable(result, moment) else None,
            )
    raise StepResultStoreError(
        f"run once per key: {MAX_LOST_SWAPS} compare-and-swaps on {key.step_type} key "
        f"{key.result_key[:12]} in a row never landed — the store's read and writes disagree "
        f"({type(store).__name__})"
    )


# ── in-memory store ──────────────────────────────────────────────────────────


class MemoryStepResultStore:
    """Process-local store — the zero-setup default and the engine tests' store. Same CAS
    semantics as the Postgres store; ``wait`` wakes on the next change instead of polling."""

    def __init__(self) -> None:
        self._rows: dict[StepResultKey, StepResultRow] = {}
        self._changed: dict[StepResultKey, asyncio.Event] = {}
        self._lock = asyncio.Lock()

    def _touch(self, key: StepResultKey) -> None:
        event = self._changed.pop(key, None)
        if event is not None:
            event.set()

    def rows(self) -> dict[StepResultKey, StepResultRow]:
        """Every row (tests and debugging)."""
        return dict(self._rows)

    async def read(self, key: StepResultKey) -> StepResultRow | None:
        return self._rows.get(key)

    async def recent_results(self, key: StepResultKey, *, node_id: str, limit: int) -> list[StoredResult]:
        """The newest saved results of the step ``node_id`` under ``key``'s identity minus its
        result key (any key) — what a miss is compared with to say why it missed."""
        found = [
            row.result for k, row in self._rows.items()
            if row.result is not None and row.result.origin_node_id == node_id
            and (k.organization_id, k.scope, k.scope_id, k.step_type)
            == (key.organization_id, key.scope, key.scope_id, key.step_type)
        ]
        return sorted(found, key=lambda r: r.succeeded_at, reverse=True)[:limit]

    async def insert_claim(
        self, key: StepResultKey, *, token: str, position: ClaimPosition, lease_until: datetime
    ) -> bool:
        async with self._lock:
            if key in self._rows:
                return False
            self._rows[key] = StepResultRow(
                id=str(uuid4()), result=None, claim_token=token, claim_position=position,
                lease_expires_at=lease_until,
            )
            self._touch(key)
            return True

    async def take_claim(
        self,
        key: StepResultKey,
        *,
        row_id: str,
        observed_token: str | None,
        observed_succeeded_at: datetime | None,
        token: str,
        position: ClaimPosition,
        lease_until: datetime,
    ) -> bool:
        async with self._lock:
            row = self._rows.get(key)
            if row is None or row.id != row_id or row.claim_token != observed_token:
                return False
            current = row.result.succeeded_at if row.result is not None else None
            if current != observed_succeeded_at:
                return False
            self._rows[key] = replace(
                row, claim_token=token, claim_position=position, lease_expires_at=lease_until
            )
            self._touch(key)
            return True

    async def renew(self, key: StepResultKey, *, token: str, lease_until: datetime) -> bool:
        async with self._lock:
            row = self._rows.get(key)
            if row is None or row.claim_token != token:
                return False
            self._rows[key] = replace(row, lease_expires_at=lease_until)
            return True

    async def settle(self, key: StepResultKey, *, token: str, result: StoredResult) -> bool:
        async with self._lock:
            row = self._rows.get(key)
            if row is None or row.claim_token != token:
                return False
            self._rows[key] = StepResultRow(
                id=row.id, result=result, claim_token=None, claim_position=None, lease_expires_at=None
            )
            self._touch(key)
            return True

    async def release(self, key: StepResultKey, *, token: str) -> None:
        async with self._lock:
            row = self._rows.get(key)
            if row is None or row.claim_token != token:
                return
            if row.result is None:
                del self._rows[key]
            else:
                self._rows[key] = replace(row, claim_token=None, claim_position=None, lease_expires_at=None)
            self._touch(key)

    async def resolve_output(self, result: StoredResult) -> dict[str, Any]:
        return result.output

    async def wait(self, key: StepResultKey, seconds: float) -> None:
        event = self._changed.setdefault(key, asyncio.Event())
        try:
            await asyncio.wait_for(event.wait(), timeout=max(seconds, 0.0))
        except TimeoutError:
            return

    def expire_lease(self, key: StepResultKey) -> None:
        """Test hook: make the current claim's lease already expired (a dead claimer)."""
        row = self._rows[key]
        self._rows[key] = replace(row, lease_expires_at=datetime.now(UTC) - timedelta(seconds=1))
        self._touch(key)


# ── Postgres store ───────────────────────────────────────────────────────────


def _uuid(value: str) -> str:
    return str(UUID(str(value)))


class PostgresStepResultStore:
    """Durable store over ``workflow.step_result`` (host-injected ``WfStepResult`` model).

    Every write is a single guarded statement (``bulk_insert_ignore`` on the identity's unique
    index, ``update_where``/``delete_where`` filtered on the observed claim token) — never a
    read-then-write without a guard. Large output values go to the ORIGIN run's
    ``workflow.checkpoint_value`` store by reference (the same rule and knob as a node
    outcome's output), so one big result is stored once however many runs reuse it.
    """

    def __init__(self, *, poll_seconds: float = 1.0) -> None:
        self._poll_seconds = poll_seconds

    @staticmethod
    def _model() -> Any:
        from matrx_graph.db._registry import get_model

        return get_model("WfStepResult")

    @staticmethod
    def _identity(key: StepResultKey) -> dict[str, Any]:
        return {
            "organization_id": _uuid(key.organization_id),
            "scope": key.scope,
            "scope_id": _uuid(key.scope_id),
            "step_type": key.step_type,
            "result_key": key.result_key,
        }

    async def read(self, key: StepResultKey) -> StepResultRow | None:
        rows = await self._model().filter(**self._identity(key)).values(
            "id", "input_digest", "output", "output_kind", "verdict", "emissions",
            "origin_run_id", "origin_node_id", "origin_step", "origin_dispatch_id",
            "origin_item_index", "origin_attempt", "succeeded_at", "expires_at",
            "claim_token", "claim_run_id", "claim_node_id", "claim_dispatch_id",
            "claim_item_index", "lease_expires_at", "deleted_at", "metadata",
        )
        if not rows:
            return None
        row = rows[0]
        result = self._result_of(row)
        position = None
        if row.get("claim_token") is not None and row.get("claim_run_id") is not None:
            position = ClaimPosition(
                run_id=str(row["claim_run_id"]),
                node_id=str(row.get("claim_node_id") or ""),
                dispatch_id=str(row.get("claim_dispatch_id") or ""),
                item_index=int(row.get("claim_item_index") or 0),
            )
        return StepResultRow(
            id=str(row["id"]),
            result=result,
            claim_token=str(row["claim_token"]) if row.get("claim_token") is not None else None,
            claim_position=position,
            lease_expires_at=row.get("lease_expires_at"),
        )

    _RESULT_FIELDS = (
        "input_digest", "output", "output_kind", "verdict", "emissions",
        "origin_run_id", "origin_node_id", "origin_step", "origin_dispatch_id",
        "origin_item_index", "origin_attempt", "succeeded_at", "expires_at", "deleted_at", "metadata",
    )

    @staticmethod
    def _result_of(row: dict[str, Any]) -> StoredResult | None:
        result = None
        # An ARCHIVED result (deleted_at — e.g. a test run's cleanup, platform.archive_test_run)
        # is never reused: it reads as expired at the moment it was archived, so the next run
        # re-produces it under a normal claim and settle() revives the row.
        archived_at = row.get("deleted_at")
        meta = row.get("metadata") or {}
        # A result produced by a run in another organization keeps its origin in metadata (the
        # column never points across organizations — see settle).
        origin_run_id = row.get("origin_run_id") or meta.get("origin_run_id")
        if row.get("succeeded_at") is not None and row.get("input_digest") and origin_run_id:
            result = StoredResult(
                input_digest=str(row["input_digest"]),
                output=row.get("output") or {},
                output_kind=row.get("output_kind"),
                verdict=row.get("verdict") or {},
                emissions=row.get("emissions") or {},
                origin_run_id=str(origin_run_id),
                origin_node_id=str(row.get("origin_node_id") or ""),
                origin_step=int(row.get("origin_step") or 0),
                origin_dispatch_id=str(row.get("origin_dispatch_id") or ""),
                origin_item_index=int(row.get("origin_item_index") or 0),
                origin_attempt=int(row.get("origin_attempt") or 1),
                succeeded_at=row["succeeded_at"],
                expires_at=archived_at if archived_at is not None else row.get("expires_at"),
                run_input_digest=meta.get("run_input_digest"),
                origin_organization_id=meta.get("origin_organization_id"),
            )
        return result

    async def recent_results(self, key: StepResultKey, *, node_id: str, limit: int) -> list[StoredResult]:
        """The newest live saved results of the step ``node_id`` under ``key``'s identity minus
        its result key — what a miss is compared with to say why it missed."""
        identity = self._identity(key)
        identity.pop("result_key")
        rows = await (
            self._model()
            .filter(**identity, origin_node_id=node_id, succeeded_at__isnull=False, deleted_at__isnull=True)
            .order_by("-succeeded_at")
            .limit(limit)
            .values(*self._RESULT_FIELDS)
        )
        return [r for r in (self._result_of(row) for row in rows) if r is not None]

    @staticmethod
    def _claim_fields(token: str, position: ClaimPosition, lease_until: datetime) -> dict[str, Any]:
        return {
            "claim_token": token,
            "claim_run_id": _uuid(position.run_id),
            "claim_node_id": position.node_id,
            "claim_dispatch_id": position.dispatch_id,
            "claim_item_index": position.item_index,
            "lease_expires_at": lease_until,
        }

    async def insert_claim(
        self, key: StepResultKey, *, token: str, position: ClaimPosition, lease_until: datetime
    ) -> bool:
        landed = await self._model().bulk_insert_ignore(
            [{**self._identity(key), **self._claim_fields(token, position, lease_until)}],
            on_conflict=["organization_id", "scope", "scope_id", "step_type", "result_key"],
        )
        return (int(landed) if isinstance(landed, int) else len(landed)) == 1

    async def take_claim(
        self,
        key: StepResultKey,
        *,
        row_id: str,
        observed_token: str | None,
        observed_succeeded_at: datetime | None,
        token: str,
        position: ClaimPosition,
        lease_until: datetime,
    ) -> bool:
        filters: dict[str, Any] = {"id": _uuid(row_id), **self._identity(key)}
        if observed_token is None:
            filters["claim_token__isnull"] = True
        else:
            filters["claim_token"] = _uuid(observed_token)
        if observed_succeeded_at is None:
            filters["succeeded_at__isnull"] = True
        else:
            filters["succeeded_at"] = observed_succeeded_at
        result = await self._model().update_where(
            filters, **self._claim_fields(token, position, lease_until)
        )
        return result.rows_affected == 1

    async def renew(self, key: StepResultKey, *, token: str, lease_until: datetime) -> bool:
        result = await self._model().update_where(
            {**self._identity(key), "claim_token": _uuid(token)}, lease_expires_at=lease_until
        )
        return result.rows_affected == 1

    async def settle(self, key: StepResultKey, *, token: str, result: StoredResult) -> bool:
        output = await self._intern_output(result.origin_run_id, result.output)
        # A row may only reference a run of its own organization (platform.assert_same_org on
        # origin_run_id). A step run in another organization (data.in_organization) is saved THERE
        # while its run lives elsewhere: the column stays empty and the origin rides in metadata
        # (2026-10-28, runs 08bfe86c / f725c0f9: IntegrityError, nothing was ever saved).
        cross_org = bool(
            result.origin_organization_id
            and _uuid(result.origin_organization_id) != _uuid(key.organization_id)
        )
        metadata: dict[str, Any] = {}
        if result.run_input_digest:
            metadata["run_input_digest"] = result.run_input_digest
        if cross_org:
            metadata["origin_run_id"] = _uuid(result.origin_run_id)
            metadata["origin_organization_id"] = _uuid(str(result.origin_organization_id))
        updated = await self._model().update_where(
            {**self._identity(key), "claim_token": _uuid(token)},
            input_digest=result.input_digest,
            output=output,
            output_kind=result.output_kind,
            verdict=result.verdict,
            emissions=result.emissions,
            origin_run_id=None if cross_org else _uuid(result.origin_run_id),
            origin_node_id=result.origin_node_id,
            origin_step=result.origin_step,
            origin_dispatch_id=result.origin_dispatch_id,
            origin_item_index=result.origin_item_index,
            origin_attempt=result.origin_attempt,
            succeeded_at=result.succeeded_at,
            expires_at=result.expires_at,
            **({"metadata": metadata} if metadata else {}),
            claim_token=None,
            claim_run_id=None,
            claim_node_id=None,
            claim_dispatch_id=None,
            claim_item_index=None,
            lease_expires_at=None,
            deleted_at=None,
        )
        return updated.rows_affected == 1

    async def release(self, key: StepResultKey, *, token: str) -> None:
        model = self._model()
        # A row that never held a result goes away; one that did keeps its result.
        await model.delete_where(
            **self._identity(key), claim_token=_uuid(token), succeeded_at__isnull=True
        )
        await model.update_where(
            {**self._identity(key), "claim_token": _uuid(token)},
            claim_token=None,
            claim_run_id=None,
            claim_node_id=None,
            claim_dispatch_id=None,
            claim_item_index=None,
            lease_expires_at=None,
        )

    async def _intern_output(self, run_id: str, output: dict[str, Any]) -> dict[str, Any]:
        from matrx_graph.checkpoint.postgres import _value_store_available
        from matrx_graph.checkpoint.value_store import store_run_values
        from matrx_graph.checkpoint.values import outcome_input_row
        from matrx_graph.knobs import event_inline_value_max_bytes

        if not _value_store_available():
            return output
        interned, values = outcome_input_row(output, await event_inline_value_max_bytes())
        if values:
            await store_run_values(run_id, values)
        return interned

    async def resolve_output(self, result: StoredResult) -> dict[str, Any]:
        from matrx_graph.checkpoint.value_store import _load_all
        from matrx_graph.checkpoint.values import (
            MissingCheckpointValueError,
            referenced_hashes,
            resolve_values,
        )

        hashes = referenced_hashes(result.output)
        if not hashes:
            return result.output
        # One read returns at most MAX_HASHES_PER_READ hashes: batch through all of them, and a value the
        # origin run genuinely lacks stays a loud LookupError below (the reuse is then flagged, never partial).
        store = await _load_all(result.origin_run_id, hashes)
        try:
            return resolve_values(result.output, store)
        except MissingCheckpointValueError as exc:
            raise LookupError(str(exc)) from exc

    async def wait(self, key: StepResultKey, seconds: float) -> None:
        await asyncio.sleep(max(0.0, min(seconds, self._poll_seconds)))


# ── injection point ──────────────────────────────────────────────────────────

_store: StepResultStore | None = None


def configure_step_result_store(store: StepResultStore | None) -> None:
    """Install the host's store (aidream: PostgresStepResultStore). None resets to the
    in-memory default (tests)."""
    global _store
    _store = store


def get_step_result_store() -> StepResultStore:
    global _store
    if _store is None:
        _store = MemoryStepResultStore()
    return _store


ResultVersionFn = Callable[[Any, Any, Any], Awaitable[str | None]]

#: ``(file_ids, organization_id) -> {file_id: content identity or None}`` — the host answers
#: what each file's content is (a content hash, else its version / updated_at). None for a file
#: it cannot identify; the step then never reuses.
FileIdentityFn = Callable[[set[str], str], Awaitable[dict[str, str | None]]]

_file_identity: FileIdentityFn | None = None


def configure_file_identity_resolver(fn: FileIdentityFn | None) -> None:
    """Install the host's file identity reader (aidream: files.files). None = not installed:
    a step whose inputs reference a file then never reuses (flagged)."""
    global _file_identity
    _file_identity = fn


def get_file_identity_resolver() -> FileIdentityFn | None:
    return _file_identity


__all__ = [
    "Claim",
    "ClaimPosition",
    "FileIdentityFn",
    "Hit",
    "MemoryStepResultStore",
    "OncePolicy",
    "OnceScope",
    "PostgresStepResultStore",
    "ResultVersionFn",
    "StepResultKey",
    "StepResultRow",
    "StepResultStore",
    "StepResultStoreError",
    "StoredResult",
    "Wait",
    "acquire",
    "configure_file_identity_resolver",
    "configure_step_result_store",
    "file_ids_in",
    "get_file_identity_resolver",
    "get_step_result_store",
    "input_digest",
    "parse_once",
    "result_key",
    "settings_digest",
]
