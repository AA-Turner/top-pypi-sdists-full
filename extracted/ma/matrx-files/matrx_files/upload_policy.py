"""Package-side upload policy — quota pre-flight, usage metering, RAG enqueue.

SPEC-SERVER §8 / decision S16. Until this module existed, the standalone
file service (`matrx_files.standalone.app`) built its TUS router with **no
host policy at all** — its own comment said so: *"no account tiers (quota
checker defaults to allow) … default finalize (plain manager.finalize_async)"*.
matrx-frontend and matrx-local are both cut over to that service, so on the
live path **nothing metered and nothing enqueued RAG**. Three of the five
§8 seams move INTO the package here, as configurable defaults:

* the quota pre-flight (`package_quota_checker`),
* the finalize that writes the usage delta (`build_package_finalize`),
* the RAG enqueue into ``files.file_rag_jobs`` (`enqueue_file_rag_job`).

Automatic analysis and content-processing dispatch deliberately do NOT move:
they reach into aidream services and stay a host injection (S16). Path
sanitization and system-origin relocation were already the package default.

🚨 THE METERING GRAIN IS WRONG, AND ON PURPOSE — READ BEFORE TRUSTING A NUMBER
-----------------------------------------------------------------------------
``billing.apply_usage_delta`` is keyed ``p_user_id`` and writes
``files.user_storage_usage(user_id, …)``. **D11 meters storage to the
ORGANIZATION.** So from the moment this module is wired, every standalone
write is counted **PER USER**, not per organization. That is a large
improvement on counting nothing — the ledger stops being 1–6% of truth — but
it is NOT the grain billing wants.

**FS-L6 must re-grain the ledger to the organization BEFORE any grandfather
floor is computed from it.** A floor computed off this per-user ledger is
computed off the wrong ledger. Re-graining is a billing-lane change to the
RPC and to ``files.user_storage_usage``; FS-L3 does not do it, and neither
does this module. Nobody may read "metering is on" as "metering is right".

The five operational limits this service enforces are the C12 knobs, by those
names: ``files.max_file_bytes``, ``files.max_path_chars``,
``files.max_items_per_mapping``, ``files.daily_upload_bytes``,
``files.rate_limit_per_min`` (org-default layer, registry owned by
SPEC-ENGINE / FS-C7). That registry is not seeded yet, so enforcement today
runs through ``files.check_upload_quota`` over ``files.account_tiers``,
which FS-L6 retires — not this spec.
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any

logger = logging.getLogger(__name__)

# Matches aidream's own auto-RAG schedule delay so a file uploaded through the
# standalone service and one uploaded through the host land in the same queue
# with the same latency.
RAG_SCHEDULE_DELAY_MINUTES = 5


class UploadPolicyNotConfigured(RuntimeError):
    """A policy seam was asked to act without the input it requires.

    Raised — never swallowed, never defaulted — so the caller learns which
    seam is unwired and what to pass. A quota checker that silently allows,
    or a finalize that silently skips metering, is the exact defect §8 exists
    to remove.
    """


@dataclass(frozen=True)
class UploadQuotaDecision:
    """The package's own quota decision — structurally the ``QuotaDecision``
    protocol ``matrx_files.api.router_tus`` depends on (``allowed``,
    ``reason``, ``raw``), plus the numbers a refusal message needs."""

    allowed: bool
    reason: str | None = None
    detail: str | None = None
    limit: int | None = None
    used: int | None = None
    attempted: int | None = None
    raw: dict[str, Any] = field(default_factory=dict)


def _db(fm: Any) -> Any:
    """The package's own database client off a FileManager.

    ``fm.sync_engine.db`` is the public ``matrx_files.cloud_sync``
    ``DatabaseClient``; the host reaches it the same way
    (``aidream/common/account_tiers.py``). No raw SQL and no aidream import.
    """
    db = getattr(getattr(fm, "sync_engine", None), "db", None)
    if db is None:
        raise UploadPolicyNotConfigured(
            "upload policy: the FileManager has no sync_engine.db, so quota and "
            "usage cannot be read or written. Build the FileService with real "
            "database credentials (SUPABASE_MATRIX_*) before wiring this policy."
        )
    return db


async def package_quota_checker(
    fm: Any,
    user_id: str,
    size_bytes: int,
    *,
    is_guest: bool = False,
) -> UploadQuotaDecision:
    """Pre-flight ``size_bytes`` for ``user_id`` against the live limits.

    Reads ``files.check_upload_quota`` through the package's own database
    client. A user with **no** quota row is allowed and says so
    (``reason="no_quota_row"``) — that is a real, named answer the caller can
    log, not a silent allow.
    """
    data = await _db(fm).check_upload_quota_async(user_id, size_bytes, is_guest=is_guest)
    if not data:
        return UploadQuotaDecision(allowed=True, reason="no_quota_row", raw={})
    return UploadQuotaDecision(
        allowed=bool(data.get("allowed")),
        reason=data.get("reason"),
        detail=data.get("detail"),
        limit=data.get("limit"),
        used=data.get("used"),
        attempted=data.get("attempted"),
        raw=dict(data),
    )


def build_quota_checker(file_service: Any, *, is_guest: bool = False) -> Callable[
    [str, int], Awaitable[UploadQuotaDecision]
]:
    """A ``QuotaChecker`` bound to ``file_service`` for ``build_tus_router``."""

    async def _check(user_id: str, size_bytes: int) -> UploadQuotaDecision:
        return await package_quota_checker(
            file_service.file_manager, user_id, size_bytes, is_guest=is_guest
        )

    return _check


async def enqueue_file_rag_job(
    *,
    file_id: str,
    user_id: str,
    organization_id: str,
    trigger_source: str = "auto",
    delay_minutes: int = RAG_SCHEDULE_DELAY_MINUTES,
) -> str | None:
    """Write one ``files.file_rag_jobs`` row for the sweeper to pick up.

    The same table, status and trigger vocabulary aidream's own upload path
    writes (``aidream/services/auto_ingest/file_jobs.py``) and
    ``aidream/workers/file_rag_sweeper.py`` drains — one queue, not two.

    ``organization_id`` is REQUIRED and passed explicitly. The table is
    org-scoped and the no-db-assigned-org ruling forbids a database default,
    a personal fallback or parent inheritance; an absent organization is a
    refusal here, never a guess.

    Returns the new job id, or ``None`` when a live job for this file already
    exists (a re-upload while one is pending — that job reads current content
    when it runs, so a second row would be duplicate work).
    """
    if not organization_id:
        raise UploadPolicyNotConfigured(
            f"RAG enqueue for file {file_id}: organization_id is required and was "
            "absent. Pass the organization the file belongs to explicitly — the "
            "database never chooses, inherits or defaults one."
        )
    from matrx_orm import IntegrityError

    from matrx_files.db.models_files import FileRagJobs

    try:
        row = await FileRagJobs.create(
            file_id=file_id,
            user_id=user_id,
            organization_id=organization_id,
            status="pending",
            trigger_source=trigger_source,
            scheduled_for=datetime.now(UTC) + timedelta(minutes=delay_minutes),
        )
    except IntegrityError:
        logger.info(
            "[matrx-files] RAG enqueue skipped for file %s — a live job already exists",
            file_id,
        )
        return None
    logger.info(
        "[matrx-files] RAG job %s scheduled for file %s at +%dmin",
        row.id,
        file_id,
        delay_minutes,
    )
    return str(row.id)


# ``(file_id, user_id, organization_id, metadata) -> bool``. The DECISION lives
# with the caller on purpose: SPEC-SERVER C11 puts ``index_for_knowledge`` in
# exactly one place — the per-mapping knob ``knowledge.index_for_knowledge``
# inside ``files.sync_mappings.knobs``, precedence mapping knob → org default,
# owned by SPEC-ENGINE (FS-C7). This module owns the MECHANISM and must never
# grow a second copy of the rule.
RagIndexDecider = Callable[[str, str, str, dict[str, Any]], Awaitable[bool]]


def build_package_finalize(
    *,
    index_for_knowledge: RagIndexDecider | None,
    is_guest: bool = False,
):
    """A ``FinalizeCallable`` that finalizes, meters, and (when asked) enqueues RAG.

    Replaces ``router_tus._default_finalize``, which called
    ``manager.finalize_async`` and nothing else. Order matters: the row is
    finalized first, then metered, then queued — a failure to queue must never
    lose the file or the bytes.

    ``index_for_knowledge`` is a REQUIRED keyword with no default. Pass a
    decider to arm the RAG lane, or pass ``None`` to state deliberately that
    this deployment has no knob source wired — ``None`` is announced once, at
    wiring time, with the remedy (see ``describe_finalize_arming``), never
    discovered as a per-upload silence.

    🚨 The usage delta written here is keyed on the USER (D11 wants the
    ORGANIZATION) — see this module's header. FS-L6 re-grains it.
    """

    async def _finalize(
        fm: Any,
        manager: Any,
        *,
        upload_id: str,
        user_id: str,
        request_id: str | None,
    ) -> Any:
        extra: dict[str, str] = {}
        if request_id:
            extra["request_id"] = request_id
        finalized = await manager.finalize_async(
            upload_id=upload_id,
            owner_id=user_id,
            extra_metadata=extra,
        )

        size_bytes = int(getattr(finalized, "size_bytes", 0) or 0)
        # Metering is not best-effort: a write that is not counted is a write
        # the ledger lies about, and the grandfather floor is computed from
        # this ledger. A failure here surfaces to the caller.
        await _db(fm).apply_usage_delta_async(
            user_id,
            bytes_delta=size_bytes,
            files_delta=1,
            record_upload=True,
            upload_bytes=size_bytes,
        )

        if index_for_knowledge is None:
            return finalized

        metadata = dict(getattr(finalized, "metadata", None) or {})
        organization_id = str(
            getattr(finalized, "organization_id", None)
            or metadata.get("organization_id")
            or ""
        )
        file_id = str(getattr(finalized, "file_id", ""))
        if not await index_for_knowledge(file_id, user_id, organization_id, metadata):
            return finalized
        await enqueue_file_rag_job(
            file_id=file_id,
            user_id=user_id,
            organization_id=organization_id,
        )
        return finalized

    _finalize.matrx_rag_armed = index_for_knowledge is not None  # type: ignore[attr-defined]
    _finalize.matrx_meters_usage = True  # type: ignore[attr-defined]
    return _finalize


def describe_finalize_arming(finalize: Any) -> str:
    """The one sentence a service logs at boot about its own upload policy.

    A screen — or a log — is absent or honest. A service that does not enqueue
    RAG says so, and says what would arm it.
    """
    if not getattr(finalize, "matrx_meters_usage", False):
        return (
            "Upload policy: NOT metering. Uploads through this service do not move "
            "files.user_storage_usage. Remedy: build the TUS router with "
            "matrx_files.upload_policy.build_package_finalize(...)."
        )
    if getattr(finalize, "matrx_rag_armed", False):
        return (
            "Upload policy: metering ON (per USER — D11 wants per ORGANIZATION; "
            "FS-L6 re-grains it), RAG enqueue ARMED."
        )
    return (
        "Upload policy: metering ON (per USER — D11 wants per ORGANIZATION; FS-L6 "
        "re-grains it), RAG enqueue NOT ARMED — no index_for_knowledge source is "
        "wired on this deployment. Remedy: the knob knowledge.index_for_knowledge "
        "lives in files.sync_mappings.knobs (SPEC-SERVER C11, registry FS-C7); pass "
        "a decider reading it to build_package_finalize(index_for_knowledge=...)."
    )


# ---------------------------------------------------------------------------
# ONE FACTORY, AND A LIVENESS GUARD THAT EXERCISES WHAT IT BUILT.
#
# Every guard on this wiring so far has been an INSPECTION. The first read the
# source of `create_app` for the string `configure_quota_check(`. The second
# read the AST for the two kwarg NAMES. The third added "and neither argument is
# the literal None". All three are defeated by the same four lines, because none
# of them ever CALLS anything:
#
#     _quota_checker = build_quota_checker(...)   # or a lambda that says yes
#     return build_tus_router(..., quota_checker_dep=_allow, finalize=_nothing)
#
# A quota check that cannot say no and a finalize that does not meter are
# exactly the un-metered state §8 exists to prevent, and they wear the right
# names. So the wiring is now built by ONE factory, and the guard takes that
# factory, builds the policy over probe doubles, and RUNS every hook:
#
#   * the quota checker must REFUSE an over-quota answer and ALLOW an
#     under-quota one (a stub that always says yes fails the first; a stub that
#     always says no fails the second),
#   * the finalize must move the ledger by exactly the finalized size,
#   * and when RAG is armed, the enqueue must actually be REACHED — proven by
#     the organization refusal it is required to raise, which no stub raises.
# ---------------------------------------------------------------------------


class UploadPolicyNotLive(RuntimeError):
    """A wired hook was inspected as present and then proved inert.

    Raised by :func:`assert_upload_policy_is_live` naming which hook failed
    which probe, because "the kwarg is there" has been true of every version of
    this service that metered nothing.
    """


def build_upload_policy(
    file_service: Any,
    *,
    index_for_knowledge: RagIndexDecider | None,
    is_guest: bool = False,
) -> dict[str, Any]:
    """THE upload policy for a service, built in one place.

    `standalone/app.py` calls this and declares the result on `app.state`, so
    the guard that exercises the wiring and the app that serves it are building
    the same object from the same code — not two descriptions of an intention.
    """
    finalize = build_package_finalize(
        index_for_knowledge=index_for_knowledge, is_guest=is_guest
    )
    return {
        "quota_checker": build_quota_checker(file_service, is_guest=is_guest),
        "finalize": finalize,
        "arming": describe_finalize_arming(finalize),
    }


class _ProbeQuotaDb:
    """The database's own row shape, so the checker does its real translation."""

    def __init__(self, *, allowed: bool) -> None:
        self.allowed = allowed
        self.calls: list[tuple[str, int]] = []
        self.deltas: list[dict[str, Any]] = []

    async def check_upload_quota_async(self, user_id, size_bytes, *, is_guest=False):
        self.calls.append((user_id, size_bytes))
        if self.allowed:
            return {"allowed": True, "reason": None, "limit": 1_073_741_824, "used": 1}
        return {
            "allowed": False,
            "reason": "storage_limit_exceeded",
            "detail": "1.0 GB of 1.0 GB used",
            "limit": 1_073_741_824,
            "used": 1_073_741_824,
            "attempted": size_bytes,
        }

    async def apply_usage_delta_async(
        self, user_id, *, bytes_delta, files_delta, record_upload=False, upload_bytes=0
    ):
        self.deltas.append(
            {
                "user_id": user_id,
                "bytes_delta": bytes_delta,
                "files_delta": files_delta,
                "record_upload": record_upload,
                "upload_bytes": upload_bytes,
            }
        )


class _ProbeFinalizedRow:
    file_id = "00000000-0000-0000-0000-0000000000f1"
    size_bytes = 4096
    #: DELIBERATELY absent. An armed RAG lane must REFUSE it by name, which is
    #: how this guard proves the enqueue was reached rather than skipped.
    organization_id = ""
    metadata: dict[str, Any] = {}


class _ProbeTus:
    def __init__(self) -> None:
        self.calls = 0

    async def finalize_async(self, *, upload_id, owner_id, extra_metadata):
        self.calls += 1
        return _ProbeFinalizedRow()


def _probe_service(db: Any) -> Any:
    from types import SimpleNamespace

    return SimpleNamespace(
        file_manager=SimpleNamespace(sync_engine=SimpleNamespace(db=db, tus=_ProbeTus()))
    )


async def assert_upload_policy_is_live(
    build: Callable[..., dict[str, Any]],
    *,
    is_guest: bool = False,
) -> None:
    """Build the policy with `build` over probe doubles and RUN every hook.

    `build` is a factory taking a file service and `index_for_knowledge`, i.e.
    :func:`build_upload_policy` or whatever a host wires in its place. Nothing
    here touches a real database, a real bucket or a real row.

    Raises :class:`UploadPolicyNotLive` naming the hook and the probe it failed.
    """
    # ---- the quota checker must be able to say NO ----------------------------
    over = _ProbeQuotaDb(allowed=False)
    policy = build(_probe_service(over), index_for_knowledge=None, is_guest=is_guest)

    for hook in ("quota_checker", "finalize"):
        if not callable(policy.get(hook)):
            raise UploadPolicyNotLive(
                f"upload policy: {hook!r} is {policy.get(hook)!r}, not a callable. "
                "The kwarg name being present is not the hook being wired."
            )

    decision = await policy["quota_checker"]("probe-user", 5 * 1024 * 1024)
    if getattr(decision, "allowed", decision) is not False:
        raise UploadPolicyNotLive(
            "upload policy: the quota checker ALLOWED an over-quota upload "
            f"({decision!r}). That is the allow-everything default §8 exists to "
            "replace, and it is what shipped un-metered for months."
        )
    if not over.calls:
        raise UploadPolicyNotLive(
            "upload policy: the quota checker refused without consulting the quota "
            "source at all — a hardcoded no is not a checker either."
        )

    # ---- and must be able to say YES (a refuse-everything stub fails here) ----
    under = _ProbeQuotaDb(allowed=True)
    allowed_policy = build(
        _probe_service(under), index_for_knowledge=None, is_guest=is_guest
    )
    ok = await allowed_policy["quota_checker"]("probe-user", 1024)
    if getattr(ok, "allowed", None) is not True:
        raise UploadPolicyNotLive(
            f"upload policy: the quota checker REFUSED an under-quota upload ({ok!r}). "
            "A checker that cannot say yes is broken in the other direction."
        )

    # ---- the finalize must move the ledger by the finalized size -------------
    ledger = _ProbeQuotaDb(allowed=True)
    metering = build(_probe_service(ledger), index_for_knowledge=None, is_guest=is_guest)
    fm = _probe_service(ledger).file_manager
    await metering["finalize"](
        fm, fm.sync_engine.tus, upload_id="probe", user_id="probe-user", request_id=None
    )
    if not ledger.deltas:
        raise UploadPolicyNotLive(
            "upload policy: the finalize wrote NO usage delta. The file lands and the "
            "ledger does not move — nothing fails, the numbers are simply wrong."
        )
    moved = ledger.deltas[-1]["bytes_delta"]
    if moved != _ProbeFinalizedRow.size_bytes:
        raise UploadPolicyNotLive(
            f"upload policy: the finalize moved the ledger by {moved}, not by the "
            f"finalized size {_ProbeFinalizedRow.size_bytes}."
        )

    # ---- and when RAG is armed, the enqueue must be REACHED ------------------
    async def _always_index(file_id, user_id, organization_id, metadata) -> bool:
        return True

    armed = build(
        _probe_service(_ProbeQuotaDb(allowed=True)),
        index_for_knowledge=_always_index,
        is_guest=is_guest,
    )
    if not getattr(armed["finalize"], "matrx_rag_armed", False):
        raise UploadPolicyNotLive(
            "upload policy: a decider was passed and the finalize still reports RAG "
            "NOT ARMED — the decider is being dropped on the floor."
        )
    armed_fm = _probe_service(_ProbeQuotaDb(allowed=True)).file_manager
    try:
        await armed["finalize"](
            armed_fm, armed_fm.sync_engine.tus,
            upload_id="probe", user_id="probe-user", request_id=None,
        )
    except UploadPolicyNotConfigured:
        pass  # reached the enqueue, which refused the absent organization. Live.
    else:
        raise UploadPolicyNotLive(
            "upload policy: an ARMED finalize finished without reaching the RAG "
            "enqueue — the probe row carries no organization_id, so a live enqueue "
            "must have refused it by name. A hook that is never called cannot fail."
        )
