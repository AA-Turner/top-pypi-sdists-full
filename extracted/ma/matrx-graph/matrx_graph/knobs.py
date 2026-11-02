"""Operational knobs for the engine — the values an admin turns.

Authority: ``common-docs/policies/limits-are-knobs-agents-set-them.md``. Read
through whatever model the host already registered for ``platform.feature_knob``,
falling back to a package-owned read-only mirror when nothing is registered (the
narrow-reader pattern proven in ``matrx_seo/knobs.py`` and
``matrx_batch/knobs.py``) — so nothing has to be injected by a host and a
standalone install reads the same rows.

Feature ``workflow.checkpoint_write`` — how hard the engine tries to save a
run's progress, and when a checkpoint is big enough to complain about:

======================== ========= =============================================
key                      start     meaning
======================== ========= =============================================
statement_timeout_ms     30000     ceiling for the checkpoint INSERT itself.
                                   The pool's ``command_timeout`` (10s) is the
                                   default for every statement and is what
                                   killed run 053e8b72 on a 1.1 MB row while
                                   the database was under deploy-train load;
                                   sibling runs wrote the same row in 2-3s.
max_retries              2         extra attempts after the first. A checkpoint
                                   INSERT is idempotent BY ID, so a re-issue is
                                   exactly-once: before every retry the row is
                                   READ BACK, and finding it proves the attempt
                                   the client gave up on had actually committed.
retry_backoff_ms         250       first backoff ceiling (full jitter, doubling).
warn_bytes               1048576   above this the write SCREAMS with the size and
                                   the node that grew it — the evidence trail for
                                   moving big fan-out payloads to storage by
                                   reference instead of inline. Also the ceiling
                                   the round-size guard holds every checkpoint
                                   row under (aidream tests/
                                   test_workflow_checkpoint_stays_small.py).
inline_value_max_bytes   4096      a value in a checkpoint whose JSON is larger
                                   than this is stored ONCE per run in
                                   workflow.checkpoint_value and the row keeps a
                                   reference (checkpoint/values.py, MKT-111).
                                   0 turns references off.
======================== ========= =============================================

**A missing row never raises here.** Unlike ``matrx_batch.knobs`` (where the
feature simply does not run without its rows), this knob sits *inside the write
path it protects*: raising would turn a survivable timeout into a hard failure,
and would brick a standalone install on a bare Postgres that has no
``platform.feature_knob`` table at all. So the degradation is LOUD — one ERROR
per process naming the remedy — and then the recorded starting policy applies.
Same reasoning, same posture as ``matrx_orm.core.write_retry``.
"""

from __future__ import annotations

import logging
import random
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, ClassVar
from matrx_utils.knob_fallback import knob_or_declared_default_sync, report_missing_row

logger = logging.getLogger("matrx_graph.knobs")

CHECKPOINT_WRITE_FEATURE = "workflow.checkpoint_write"

STATEMENT_TIMEOUT_MS_KEY = "statement_timeout_ms"
MAX_RETRIES_KEY = "max_retries"
RETRY_BACKOFF_MS_KEY = "retry_backoff_ms"
WARN_BYTES_KEY = "warn_bytes"
INLINE_VALUE_MAX_BYTES_KEY = "inline_value_max_bytes"

#: How long a resolved policy is trusted before it is re-read.
KNOB_CACHE_TTL_SECONDS = 60.0

#: The db config name the engine's own tables are bound to. Same default as
#: ``matrx_graph.db.standalone`` and the same value aidream's generated models
#: carry, so hosted and standalone read the one platform.feature_knob table.
KNOB_DATABASE = "supabase_automation_matrix"


@dataclass(frozen=True)
class CheckpointWritePolicy:
    """How hard to try to save a run's progress, and when to complain."""

    statement_timeout_ms: int
    max_retries: int
    retry_backoff_ms: int
    warn_bytes: int
    inline_value_max_bytes: int = 4096

    @property
    def statement_timeout_seconds(self) -> float:
        return self.statement_timeout_ms / 1000.0

    def backoff_seconds(self, attempt: int) -> float:
        """Full-jitter exponential backoff for ``attempt`` (0-based)."""
        ceiling_ms = min(self.retry_backoff_ms * (2**attempt), 10_000)
        return random.uniform(0.0, max(1, ceiling_ms)) / 1000.0


#: What the seeding migration recorded (0648_workflow_checkpoint_write_knobs.sql,
#: 2026-09-12, review due 2026-12-12). Used ONLY when the rows cannot be
#: resolved, and never quietly — see ``_announce_degradation``.
STARTING_CHECKPOINT_POLICY = CheckpointWritePolicy(
    statement_timeout_ms=30_000,
    max_retries=2,
    retry_backoff_ms=250,
    warn_bytes=1_048_576,
    inline_value_max_bytes=4096,
)

_model: Any = None
_cache: dict[str, tuple[float, dict[str, Any]]] = {}
_announced: set[str] = set()


def clear_knob_cache() -> None:
    """Drop the process cache. Tests, and any caller that just wrote a knob."""
    _cache.clear()
    _announced.clear()


def _feature_knob_model() -> Any:
    """The model to read ``platform.feature_knob`` through.

    Prefers whatever the HOST already registered for that table — the sanctioned
    runtime lookup (``ModelRegistry.get_model_by_table``), so hosted we read the
    same model the rest of the platform does. Only when nothing is registered
    (matrx-graph running standalone) does the package define its own narrow
    read-only mirror, the pattern proven in ``matrx_seo``/``matrx_batch``.

    Built lazily so importing matrx_graph never requires matrx-orm.
    """
    global _model
    if _model is not None:
        return _model
    import matrx_orm as m

    try:
        hosted = m.model_registry.get_model_by_table(
            "platform", "feature_knob", database=KNOB_DATABASE
        )
    except Exception:  # noqa: BLE001 — ambiguous/unavailable registry → ship our own
        hosted = None
    if hosted is not None:
        _model = hosted
        return _model

    class GraphFeatureKnob(m.Model):
        feature = m.TextField(primary_key=True, null=False)
        key = m.TextField(primary_key=True, null=False)
        value = m.JSONBField(null=False)
        _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
        _database = KNOB_DATABASE
        _table_name = "feature_knob"
        _db_schema = "platform"
        _read_only = True

    m.model_registry.register_all([GraphFeatureKnob], skip_existing=True)
    _model = GraphFeatureKnob
    return _model


def _file_missing_rows(feature: str, keys: list[str] | tuple[str, ...]) -> None:
    """Each key absent from a feature's rows is a missing knob: filed to the error queue
    (``feature_knob_missing``) through matrx_utils, never only a log line."""
    for key in keys:
        report_missing_row(
            feature=feature,
            key=key,
            declared_default="the starting policy",
            consequence="Workflow runs use the starting value for this setting, and an admin cannot change it.",
        )


def _announce_degradation(feature: str, reason: str) -> None:
    if feature in _announced:
        return
    _announced.add(feature)
    logger.error(
        "[matrx_graph] knobs for '%s' unresolved (%s) — running on the recorded "
        "starting policy (%s). REMEDY: seed the platform.feature_knob rows for "
        "that feature (db/migrations/0648_workflow_checkpoint_write_knobs.sql) "
        "so an admin can turn them.",
        feature,
        reason,
        STARTING_CHECKPOINT_POLICY,
    )


def _coerce_int(raw: Any, fallback: int, low: int, high: int) -> int:
    try:
        value = int(str(raw).strip().strip('"'))
    except (TypeError, ValueError):
        return fallback
    return max(low, min(high, value))


async def _feature_values(feature: str) -> dict[str, Any] | None:
    cached = _cache.get(feature)
    now = time.monotonic()
    if cached is not None and now - cached[0] < KNOB_CACHE_TTL_SECONDS:
        return cached[1]
    try:
        rows = await _feature_knob_model().filter(feature=feature).values("key", "value")
    except Exception as exc:  # noqa: BLE001 — a knob read must never fail a write
        _announce_degradation(feature, f"{type(exc).__name__}: {exc}")
        return None
    values = {str(row["key"]): row["value"] for row in rows or []}
    _cache[feature] = (now, values)
    return values


async def checkpoint_write_policy() -> CheckpointWritePolicy:
    """The live checkpoint-write budget. Never raises."""
    values = await _feature_values(CHECKPOINT_WRITE_FEATURE)
    if values is None:
        return STARTING_CHECKPOINT_POLICY
    missing = [
        k
        for k in (STATEMENT_TIMEOUT_MS_KEY, MAX_RETRIES_KEY, RETRY_BACKOFF_MS_KEY, WARN_BYTES_KEY)
        if k not in values
    ]
    if missing:
        _file_missing_rows(CHECKPOINT_WRITE_FEATURE, missing)
        _announce_degradation(CHECKPOINT_WRITE_FEATURE, f"rows missing: {', '.join(missing)}")
        return STARTING_CHECKPOINT_POLICY
    return CheckpointWritePolicy(
        statement_timeout_ms=_coerce_int(
            values[STATEMENT_TIMEOUT_MS_KEY],
            STARTING_CHECKPOINT_POLICY.statement_timeout_ms,
            1_000,
            600_000,
        ),
        max_retries=_coerce_int(
            values[MAX_RETRIES_KEY], STARTING_CHECKPOINT_POLICY.max_retries, 0, 10
        ),
        retry_backoff_ms=_coerce_int(
            values[RETRY_BACKOFF_MS_KEY], STARTING_CHECKPOINT_POLICY.retry_backoff_ms, 1, 10_000
        ),
        warn_bytes=_coerce_int(
            values[WARN_BYTES_KEY], STARTING_CHECKPOINT_POLICY.warn_bytes, 1_024, 1_073_741_824
        ),
        # Added after the first four (MKT-111): its own absence must not throw the
        # other four back to their starting values, so it is read on its own.
        inline_value_max_bytes=_coerce_int(
            values.get(
                INLINE_VALUE_MAX_BYTES_KEY, STARTING_CHECKPOINT_POLICY.inline_value_max_bytes
            ),
            STARTING_CHECKPOINT_POLICY.inline_value_max_bytes,
            0,
            1_073_741_824,
        ),
    )


#: MKT-167 — the size above which a workflow EVENT's data values go by reference.
#: Its own feature, so screens and checkpoints are tuned apart: an event's inline
#: values are what every run screen folds on reopen, a checkpoint's are what a resume
#: reloads. Seeded by aidream db/migrations/20261015230000_event_inline_value_knob.sql.
EVENT_PAYLOAD_FEATURE = "workflow.event_payload"
STARTING_EVENT_INLINE_VALUE_MAX_BYTES = 32_768


async def event_inline_value_max_bytes() -> int:
    """The live event-value knob. Never raises; a missing row is loud once, then the
    starting value applies (same posture as :func:`checkpoint_write_policy`)."""
    values = await _feature_values(EVENT_PAYLOAD_FEATURE)
    if values is None:
        return STARTING_EVENT_INLINE_VALUE_MAX_BYTES
    if INLINE_VALUE_MAX_BYTES_KEY not in values:
        _file_missing_rows(EVENT_PAYLOAD_FEATURE, [INLINE_VALUE_MAX_BYTES_KEY])
        _announce_degradation(EVENT_PAYLOAD_FEATURE, f"row missing: {INLINE_VALUE_MAX_BYTES_KEY}")
        return STARTING_EVENT_INLINE_VALUE_MAX_BYTES
    return _coerce_int(
        values[INLINE_VALUE_MAX_BYTES_KEY], STARTING_EVENT_INLINE_VALUE_MAX_BYTES, 0, 1_073_741_824
    )


#: 2026-10-29 — the most left-out values one step report (or run record) lists before it gives only a count of the
#: rest (``checkpoint.value_store`` ``withheld`` / ``withheld_more``). Row: ``workflow.event_payload.withheld_list_max``.
WITHHELD_LIST_MAX_KEY = "withheld_list_max"
STARTING_WITHHELD_LIST_MAX = 20


async def withheld_list_max() -> int:
    """The live cap on a report's left-out list. Never raises; a missing row is loud once, then the starting value."""
    values = await _feature_values(EVENT_PAYLOAD_FEATURE)
    if values is None:
        return STARTING_WITHHELD_LIST_MAX
    if WITHHELD_LIST_MAX_KEY not in values:
        _file_missing_rows(EVENT_PAYLOAD_FEATURE, [WITHHELD_LIST_MAX_KEY])
        _announce_degradation(EVENT_PAYLOAD_FEATURE, f"row missing: {WITHHELD_LIST_MAX_KEY}")
        return STARTING_WITHHELD_LIST_MAX
    return _coerce_int(values[WITHHELD_LIST_MAX_KEY], STARTING_WITHHELD_LIST_MAX, 1, 10_000)


#: The size above which a step's output goes BY REFERENCE in the run row (``workflow.run.output``). The row
#: keeps the step's keys and a reference per large value; the value is stored once in the run's value store
#: (``workflow.checkpoint_value``) and every server reader of the run resolves it (``RunStore.load``).
#: 2026-10-27: run 61b8404f finished all 59 steps and ended failed because its 21.7 MB result row timed out
#: (``final_write_failed``); 2026-10-05 an 11 MB one did the same. Seeded live 2026-10-27
#: (``workflow.run_output.inline_value_max_bytes``). 0 keeps every output inline (the old behaviour).
RUN_OUTPUT_FEATURE = "workflow.run_output"
STARTING_RUN_OUTPUT_INLINE_VALUE_MAX_BYTES = 1_048_576


async def run_output_inline_value_max_bytes() -> int:
    """The live run-output knob. Never raises; a missing row is loud once and filed, then the starting value
    applies (same posture as :func:`event_inline_value_max_bytes`)."""
    values = await _feature_values(RUN_OUTPUT_FEATURE)
    if values is None:
        return STARTING_RUN_OUTPUT_INLINE_VALUE_MAX_BYTES
    if INLINE_VALUE_MAX_BYTES_KEY not in values:
        _file_missing_rows(RUN_OUTPUT_FEATURE, [INLINE_VALUE_MAX_BYTES_KEY])
        _announce_degradation(RUN_OUTPUT_FEATURE, f"row missing: {INLINE_VALUE_MAX_BYTES_KEY}")
        return STARTING_RUN_OUTPUT_INLINE_VALUE_MAX_BYTES
    return _coerce_int(
        values[INLINE_VALUE_MAX_BYTES_KEY], STARTING_RUN_OUTPUT_INLINE_VALUE_MAX_BYTES, 0, 1_073_741_824
    )


#: How much text a regular-expression step reads (``text.regex_extract`` / ``text.regex_replace``).
#: Python's ``re`` has no match timeout: the safe-regex judge refuses the exponential shapes, and this
#: cap bounds the polynomial ones that stay allowed. Seeded live 2026-10-27 (row
#: ``workflow.regex.max_input_chars``); was a 500,000 constant.
REGEX_FEATURE = "workflow.regex"
REGEX_MAX_INPUT_CHARS_KEY = "max_input_chars"
STARTING_REGEX_MAX_INPUT_CHARS = 50_000


async def regex_max_input_chars() -> int:
    """The live regex-step input cap. Never raises; a missing row is loud once, then the starting value applies."""
    values = await _feature_values(REGEX_FEATURE)
    if values is None:
        return STARTING_REGEX_MAX_INPUT_CHARS
    if REGEX_MAX_INPUT_CHARS_KEY not in values:
        _file_missing_rows(REGEX_FEATURE, [REGEX_MAX_INPUT_CHARS_KEY])
        _announce_degradation(REGEX_FEATURE, f"row missing: {REGEX_MAX_INPUT_CHARS_KEY}")
        return STARTING_REGEX_MAX_INPUT_CHARS
    return _coerce_int(
        values[REGEX_MAX_INPUT_CHARS_KEY], STARTING_REGEX_MAX_INPUT_CHARS, 1_000, 10_000_000
    )

#: How many runs' organizations the checkpointer remembers (a run's organization never changes, so
#: the per-write read of the run row is skipped for a remembered run). Seeded by aidream
#: db/migrations/wf_136_run_org_cache_size_knob.sql. No fallback constant (the knob policy): when the
#: row cannot be read the engine remembers NOTHING and reads the run row every time, as before.
RUN_ORG_CACHE_FEATURE = "workflow"
RUN_ORG_CACHE_SIZE_KEY = "run_org_cache_size"


async def run_org_cache_size() -> int:
    """The live run-organization memory size; 0 (remember nothing) while the row cannot be read.
    Never raises; a missing row is loud once and filed (same posture as
    :func:`event_inline_value_max_bytes`)."""
    values = await _feature_values(RUN_ORG_CACHE_FEATURE)
    if values is None:
        return 0
    if RUN_ORG_CACHE_SIZE_KEY not in values:
        _file_missing_rows(RUN_ORG_CACHE_FEATURE, [RUN_ORG_CACHE_SIZE_KEY])
        _announce_degradation(RUN_ORG_CACHE_FEATURE, f"row missing: {RUN_ORG_CACHE_SIZE_KEY}")
        return 0
    return _coerce_int(values[RUN_ORG_CACHE_SIZE_KEY], 0, 0, 1_000_000)


#: Review flags (0117) — seeded live 2026-10-17 (db/migrations/20261017_review_flag_knobs.sql).
REVIEW_FLAGS_FEATURE = "workflow.review_flags"


@dataclass(frozen=True)
class ReviewFlagPolicy:
    notify_timeout_ms: int = 5000
    max_flags_per_run: int = 200
    max_flags_per_issue_per_run: int = 25


STARTING_REVIEW_FLAG_POLICY = ReviewFlagPolicy()


async def review_flag_policy() -> ReviewFlagPolicy:
    """The live review-flag limits. Never raises; a missing row is loud once."""
    values = await _feature_values(REVIEW_FLAGS_FEATURE)
    base = STARTING_REVIEW_FLAG_POLICY
    if values is None:
        return base
    keys = ("notify_timeout_ms", "max_flags_per_run", "max_flags_per_issue_per_run")
    missing = [k for k in keys if k not in values]
    if missing:
        _file_missing_rows(REVIEW_FLAGS_FEATURE, missing)
        _announce_degradation(REVIEW_FLAGS_FEATURE, f"rows missing: {', '.join(missing)}")
    return ReviewFlagPolicy(
        notify_timeout_ms=_coerce_int(
            values.get("notify_timeout_ms", base.notify_timeout_ms), base.notify_timeout_ms, 0, 60_000
        ),
        max_flags_per_run=_coerce_int(
            values.get("max_flags_per_run", base.max_flags_per_run), base.max_flags_per_run, 1, 100_000
        ),
        max_flags_per_issue_per_run=_coerce_int(
            values.get("max_flags_per_issue_per_run", base.max_flags_per_issue_per_run),
            base.max_flags_per_issue_per_run,
            1,
            10_000,
        ),
    )


# The dry-run feature uses a synchronous host-bound reader because its callers
# are synchronous graph-planning paths. Keep that seam alongside the package's
# asynchronous checkpoint policy rather than forcing either caller into a
# second knob module.
DRY_RUN_FEATURE = "workflow.dry_run"
_dry_run_reader: Callable[[str], Any] | None = None
_dry_run_announced = False
_dry_run_failed: set[str] = set()


def configure_dry_run_knobs(reader: Callable[[str], Any] | None) -> None:
    """Bind the host's one-argument reader for ``workflow.dry_run``."""
    global _dry_run_reader, _dry_run_announced
    _dry_run_reader = reader
    _dry_run_announced = False
    _dry_run_failed.clear()


def dry_run_knob(key: str, mirror: Any) -> Any:
    """Read a dry-run knob, loudly falling back to its declared mirror."""
    global _dry_run_announced
    if _dry_run_reader is None:
        if not _dry_run_announced:
            _dry_run_announced = True
            print(
                "[matrx_graph] no host knob reader bound for 'workflow.dry_run'; using "
                "the package's mirrored defaults (bind configure_dry_run_knobs())",
                file=sys.stderr,
            )
        return mirror
    try:
        return knob_or_declared_default_sync(
            lambda: _dry_run_reader(key),
            feature=DRY_RUN_FEATURE,
            key=key,
            declared_default=mirror,
            consequence=f"Workflow dry runs use the built-in value {mirror!r} for {key}, and an admin cannot change it.",
        )
    except Exception as exc:  # noqa: BLE001 - announced degradation, not a crash
        if key not in _dry_run_failed:
            _dry_run_failed.add(key)
            print(
                f"[matrx_graph] host knob reader failed for {DRY_RUN_FEATURE!r}.{key!r}: "
                f"{exc!r}; using mirrored default {mirror!r} until the host primes it",
                file=sys.stderr,
            )
        return mirror


# ---------------------------------------------------------------------------
# THE STEP WALL CLOCK — feature ``workflow.step_clock``
# ---------------------------------------------------------------------------
#
# ``NodeSpec.timeout_ms`` has always existed and NO shipped node spec sets it,
# so until 2026-09-15 every agent, AI and tool step in this engine ran with no
# clock at all: ``await executor.execute(...)`` with nothing above it.
#
# What that costs, measured live (aidream, Masterwork run
# ``e991e70e-4c2f-4444-8c9f-e107888da36a``, node ``chief``, 2026-09-15): ONE
# provider call reported ``api_duration_ms = 1,087,650`` — eighteen minutes and
# eight seconds — and the node took 18m52s (``node_outcome.duration_ms =
# 1132252``). The same node finished the same work in ~82s on two interactive
# runs of the identical Masterwork minutes earlier. The provider stream stalled
# mid-answer (``chars_streamed`` frozen at 12,591 for eighteen minutes) and then
# resumed; because the connection stayed open and keepalives kept arriving, every
# read-level timeout in the stack kept resetting. Only a WALL CLOCK over the whole
# step catches that shape.
#
# So the clock is now always on: an authored ``NodeSpec.timeout_ms`` still wins,
# and every node that declares none gets the platform ceiling below.
#
# ======================== ========= ========================================
# key                      start     meaning
# ======================== ========= ========================================
# default_step_seconds     600       wall-clock ceiling for ONE attempt of one
#                                    node that declares no timeout of its own.
# ======================== ========= ========================================
#
# Seeded by ``db/migrations/0710_workflow_step_clock_knobs.sql``.
STEP_CLOCK_FEATURE = "workflow.step_clock"

DEFAULT_STEP_SECONDS_KEY = "default_step_seconds"

#: KNOB MIRROR of platform.feature_knob "workflow.step_clock"
#: "default_step_seconds". Used ONLY when the row cannot be resolved, and never
#: quietly — see ``_announce_step_clock_degradation``.
STARTING_DEFAULT_STEP_SECONDS = 600

#: The clock can be widened but never removed. A ceiling of "no ceiling" is the
#: defect this feature exists to close, so a row of 0/negative/garbage is
#: refused in favor of the mirror.
MIN_STEP_SECONDS = 5
MAX_STEP_SECONDS = 86_400

_step_clock_announced = False


def _announce_step_clock_degradation(reason: str) -> None:
    global _step_clock_announced
    if _step_clock_announced:
        return
    _step_clock_announced = True
    logger.error(
        "[matrx_graph] knobs for '%s' unresolved (%s) — every node that declares no "
        "timeout of its own is bounded at the recorded starting ceiling of %ss. "
        "REMEDY: seed the platform.feature_knob rows for that feature "
        "(db/migrations/0710_workflow_step_clock_knobs.sql) so an admin can turn it.",
        STEP_CLOCK_FEATURE,
        reason,
        STARTING_DEFAULT_STEP_SECONDS,
    )


async def default_step_seconds() -> int:
    """The live wall-clock ceiling for one node attempt. Never raises.

    A knob read that cannot answer falls back to the announced mirror, because a
    workflow must not fail over an unreadable ceiling — but it must never run
    UNBOUNDED either, which is why there is no ``None`` in this return type.
    """
    values = await _feature_values(STEP_CLOCK_FEATURE)
    if values is None or DEFAULT_STEP_SECONDS_KEY not in (values or {}):
        if values is not None:
            _file_missing_rows(STEP_CLOCK_FEATURE, [DEFAULT_STEP_SECONDS_KEY])
        _announce_step_clock_degradation(
            "feature rows unreadable"
            if values is None
            else f"row missing: {DEFAULT_STEP_SECONDS_KEY}"
        )
        return STARTING_DEFAULT_STEP_SECONDS
    return _coerce_int(
        values[DEFAULT_STEP_SECONDS_KEY],
        STARTING_DEFAULT_STEP_SECONDS,
        MIN_STEP_SECONDS,
        MAX_STEP_SECONDS,
    )


async def step_timeout_seconds(
    declared_timeout_ms: int | None, *, node_clock: Any = None
) -> tuple[float, str]:
    """``(seconds, source)`` for one node attempt.

    Precedence: the node's own ``data.step_clock`` (its knob row when it
    resolves, else its declared seconds) → the NodeSpec's ``timeout_ms`` → the
    platform ceiling. ``source`` is the word the failure message uses, so a
    person reading a timed-out run can tell a ceiling the workflow's own author
    set from the platform's.
    """
    if node_clock is not None:
        seconds = int(node_clock.seconds)
        if node_clock.knob_feature and node_clock.knob_key:
            values = await _feature_values(node_clock.knob_feature)
            if values is not None and node_clock.knob_key in values:
                seconds = _coerce_int(
                    values[node_clock.knob_key], seconds, MIN_STEP_SECONDS, MAX_STEP_SECONDS
                )
            else:
                logger.error(
                    "[matrx_graph] step clock knob %s.%s unresolved — the step keeps its "
                    "declared %ss. REMEDY: seed that platform.feature_knob row.",
                    node_clock.knob_feature,
                    node_clock.knob_key,
                    seconds,
                )
        return float(max(MIN_STEP_SECONDS, min(MAX_STEP_SECONDS, seconds))), "declared"
    if declared_timeout_ms is not None and declared_timeout_ms > 0:
        return declared_timeout_ms / 1000.0, "declared"
    return float(await default_step_seconds()), "platform"


# Backward-compatible public name used by existing dry-run callers.
FEATURE = DRY_RUN_FEATURE

__all__ = [
    "CHECKPOINT_WRITE_FEATURE",
    "DEFAULT_STEP_SECONDS_KEY",
    "DRY_RUN_FEATURE",
    "FEATURE",
    "MAX_STEP_SECONDS",
    "MIN_STEP_SECONDS",
    "STARTING_DEFAULT_STEP_SECONDS",
    "STEP_CLOCK_FEATURE",
    "CheckpointWritePolicy",
    "checkpoint_write_policy",
    "clear_knob_cache",
    "configure_dry_run_knobs",
    "default_step_seconds",
    "dry_run_knob",
    "step_timeout_seconds",
]


# --------------------------------------------------------------------------- #
# workflow.response_checks — how hard a step tries to meet its own target      #
# --------------------------------------------------------------------------- #
#
# Rows seeded by db/migrations/wf_081_response_checks_knobs.sql (agent-set
# starting values, review 2026-11-07). A missing row degrades LOUDLY to the
# recorded starting policy below — a check never fails a run over a knob read.

RESPONSE_CHECKS_FEATURE = "workflow.response_checks"


@dataclass(frozen=True)
class ResponseCheckPolicy:
    max_revisions: int
    max_revisions_ceiling: int
    length_tolerance_pct: float
    max_revisions_per_run: int


STARTING_RESPONSE_CHECK_POLICY = ResponseCheckPolicy(
    max_revisions=1, max_revisions_ceiling=4, length_tolerance_pct=20.0, max_revisions_per_run=20
)

#: The ceiling's own absolute bound. A knob may lower or raise the ceiling
#: within this, never remove it (an unbounded revision loop is the defect).
ABSOLUTE_MAX_REVISIONS = 10


async def response_check_policy() -> ResponseCheckPolicy:
    """The live revision bounds. Never raises."""
    start = STARTING_RESPONSE_CHECK_POLICY
    values = await _feature_values(RESPONSE_CHECKS_FEATURE)
    if not values:
        _announce_degradation(RESPONSE_CHECKS_FEATURE, "feature rows unreadable or absent")
        return start
    ceiling = _coerce_int(
        values.get("max_revisions_ceiling", start.max_revisions_ceiling),
        start.max_revisions_ceiling, 0, ABSOLUTE_MAX_REVISIONS,
    )
    try:
        tol = float(str(values.get("length_tolerance_pct", start.length_tolerance_pct)).strip('"'))
    except ValueError:
        tol = start.length_tolerance_pct
    return ResponseCheckPolicy(
        max_revisions=_coerce_int(
            values.get("max_revisions", start.max_revisions), start.max_revisions, 0, ceiling
        ),
        max_revisions_ceiling=ceiling,
        length_tolerance_pct=max(0.0, min(100.0, tol)),
        max_revisions_per_run=_coerce_int(
            values.get("max_revisions_per_run", start.max_revisions_per_run),
            start.max_revisions_per_run, 0, 10_000,
        ),
    )


#: RUN ONCE PER KEY (``data.once``, matrx_graph/once.py). Seeded live with migration
#: ``workflow_once_knobs`` (2026-10-26). A missing row is loud once, then the starting value applies.
ONCE_FEATURE = "workflow.once"


@dataclass(frozen=True)
class OncePolicyKnobs:
    #: How long a claim stays valid without renewal. The claimer renews every third of it while
    #: the step works; a dead claimer frees the key this long after its last renewal.
    lease_seconds: int = 60
    #: How often a waiter re-reads a claim held by another process (in-process waiters wake at once).
    wait_poll_seconds: int = 1
    #: Days a stored result stays reusable when the step's ``data.once`` names no ``keep_days``.
    keep_days_default: int = 30
    #: How many of a missed step's newest saved results its input is compared with to say which
    #: upstream step changed it (``engine.once_missed_upstream``). 0 = never explain.
    miss_compare_limit: int = 10


STARTING_ONCE_KNOBS = OncePolicyKnobs()


async def once_knobs() -> OncePolicyKnobs:
    """The live ``workflow.once`` knobs. Never raises."""
    values = await _feature_values(ONCE_FEATURE)
    base = STARTING_ONCE_KNOBS
    if values is None:
        return base
    keys = ("lease_seconds", "wait_poll_seconds", "keep_days_default", "miss_compare_limit")
    missing = [k for k in keys if k not in values]
    if missing:
        _file_missing_rows(ONCE_FEATURE, missing)
        _announce_degradation(ONCE_FEATURE, f"rows missing: {', '.join(missing)}")
    return OncePolicyKnobs(
        lease_seconds=_coerce_int(values.get("lease_seconds", base.lease_seconds), base.lease_seconds, 5, 3_600),
        wait_poll_seconds=_coerce_int(
            values.get("wait_poll_seconds", base.wait_poll_seconds), base.wait_poll_seconds, 1, 60
        ),
        keep_days_default=_coerce_int(
            values.get("keep_days_default", base.keep_days_default), base.keep_days_default, 1, 36_500
        ),
        miss_compare_limit=_coerce_int(
            values.get("miss_compare_limit", base.miss_compare_limit), base.miss_compare_limit, 0, 100
        ),
    )


#: ONE AT A TIME PER KEY (``data.one_at_a_time``, matrx_graph/one_at_a_time.py). Seeded live
#: 2026-10-27 (row ``workflow.one_at_a_time.max_wait_seconds``). The turn's lease and poll come
#: from ``workflow.once`` (same store). A missing row is loud once, then the starting value applies.
ONE_AT_A_TIME_FEATURE = "workflow.one_at_a_time"


@dataclass(frozen=True)
class OneAtATimeKnobs:
    #: Longest a step waits for its turn before it fails with the reason (never runs unguarded).
    #: Also what ends two runs waiting on each other in opposite order.
    max_wait_seconds: int = 600


STARTING_ONE_AT_A_TIME_KNOBS = OneAtATimeKnobs()


async def one_at_a_time_knobs() -> OneAtATimeKnobs:
    """The live ``workflow.one_at_a_time`` knobs. Never raises."""
    values = await _feature_values(ONE_AT_A_TIME_FEATURE)
    base = STARTING_ONE_AT_A_TIME_KNOBS
    if values is None:
        return base
    if "max_wait_seconds" not in values:
        _file_missing_rows(ONE_AT_A_TIME_FEATURE, ["max_wait_seconds"])
        _announce_degradation(ONE_AT_A_TIME_FEATURE, "rows missing: max_wait_seconds")
    return OneAtATimeKnobs(
        max_wait_seconds=_coerce_int(
            values.get("max_wait_seconds", base.max_wait_seconds), base.max_wait_seconds, 1, 86_400
        ),
    )


#: FAN-OUT BOUNDS (2026-10-27, run 1aa73a14: a ``control.map`` launched 199 paid agent items at
#: once on a process whose database pool holds 10 connections — every item queued on the pool,
#: 10-second acquire timeouts failed the spine opens (``RuntimeTrackingOpenFailed``) and saves, and
#: ~141 paid calls landed before any cost was known). Seeded live with migration
#: ``20261027030000_run_cost_is_the_ledger_and_fan_out_knobs`` (review due 2026-12-27). A missing
#: row is loud once, then the starting value applies — never unbounded.
FAN_OUT_FEATURE = "workflow.fan_out"


@dataclass(frozen=True)
class FanOutPolicy:
    #: Items of ONE fanned step (control.map, work_queue, an ``each`` edge) live at once when the
    #: step declares no ``data.concurrency`` of its own. The rest queue.
    default_item_concurrency: int = 4
    #: The ceiling a step's own ``data.concurrency`` is clamped to for fanned items — what keeps a
    #: per-step override from re-opening the pool exhaustion.
    max_item_concurrency: int = 8
    #: How many items of a COST-BEARING fanned step (AI / LLM) launch before the first one settles,
    #: so the run knows what an item costs before it pays for the rest.
    paid_first_wave: int = 1


STARTING_FAN_OUT_POLICY = FanOutPolicy()


async def fan_out_policy() -> FanOutPolicy:
    """The live ``workflow.fan_out`` bounds. Never raises; never returns an unbounded policy."""
    values = await _feature_values(FAN_OUT_FEATURE)
    base = STARTING_FAN_OUT_POLICY
    if values is None:
        return base
    keys = ("default_item_concurrency", "max_item_concurrency", "paid_first_wave")
    missing = [k for k in keys if k not in values]
    if missing:
        _file_missing_rows(FAN_OUT_FEATURE, missing)
        _announce_degradation(FAN_OUT_FEATURE, f"rows missing: {', '.join(missing)}")
    ceiling = _coerce_int(
        values.get("max_item_concurrency", base.max_item_concurrency), base.max_item_concurrency, 1, 1_000
    )
    default = min(
        ceiling,
        _coerce_int(
            values.get("default_item_concurrency", base.default_item_concurrency),
            base.default_item_concurrency,
            1,
            1_000,
        ),
    )
    first_wave = _coerce_int(
        values.get("paid_first_wave", base.paid_first_wave), base.paid_first_wave, 1, 1_000
    )
    return FanOutPolicy(
        default_item_concurrency=default, max_item_concurrency=ceiling, paid_first_wave=first_wave
    )


#: RANK TERMS BY SPREAD (``data.spread_rank``, nodes/data/spread_rank.py). Seeded live 2026-10-27
#: (feature ``workflow.spread_rank``, one row per key below). A value the step sets on itself wins;
#: an empty step setting reads the row. A missing row is filed and loud once, then the starting
#: value applies (same posture as :func:`once_knobs`).
SPREAD_RANK_FEATURE = "workflow.spread_rank"


@dataclass(frozen=True)
class SpreadRankKnobs:
    #: Fewest distinct homes a term needs (a term in one place has no spread).
    min_homes: int = 2
    #: ``min_homes`` relative to the number of homes; 0 = the fixed ``min_homes``.
    min_homes_share: float = 0.0
    #: The relative minimum never falls below this many homes.
    min_homes_floor: int = 1
    #: A term in more than this share of all homes is filler and dropped (unless backed).
    filler_home_share: float = 0.5
    #: The filler cap never falls below this many homes (small inputs keep their themes).
    filler_cap_min_homes: int = 5
    #: A term the source names itself (``backed``) in at least this share of its homes escapes the cap.
    backed_share: float = 0.5
    #: ... or in at least this share of ALL homes.
    backed_home_share: float = 0.01
    #: A longer phrase covering at least this share of a shorter one's homes replaces it.
    longer_phrase_cover: float = 0.8
    #: Fold plural spellings and same-head phrase variants into one term.
    fold_variants: bool = True
    #: A phrase variant must itself appear in this many homes to fold into its head.
    variant_min_homes: int = 2
    #: How many ranked terms the step returns.
    top_n: int = 500


STARTING_SPREAD_RANK_KNOBS = SpreadRankKnobs()

_SPREAD_RANK_INT_RANGES: dict[str, tuple[int, int]] = {
    "min_homes": (1, 100_000),
    "min_homes_floor": (1, 100_000),
    "filler_cap_min_homes": (0, 10_000_000),
    "variant_min_homes": (1, 100_000),
    "top_n": (1, 100_000),
}
_SPREAD_RANK_SHARES = ("min_homes_share", "filler_home_share", "backed_share", "backed_home_share", "longer_phrase_cover")


def _coerce_share(raw: Any, fallback: float) -> float:
    try:
        value = float(str(raw).strip().strip('"'))
    except (TypeError, ValueError):
        return fallback
    return max(0.0, min(1.0, value))


def _coerce_bool(raw: Any, fallback: bool) -> bool:
    if isinstance(raw, bool):
        return raw
    text = str(raw).strip().strip('"').lower()
    if text in ("true", "1", "yes"):
        return True
    if text in ("false", "0", "no"):
        return False
    return fallback


async def spread_rank_knobs() -> SpreadRankKnobs:
    """The live ``workflow.spread_rank`` knobs. Never raises."""
    values = await _feature_values(SPREAD_RANK_FEATURE)
    base = STARTING_SPREAD_RANK_KNOBS
    if values is None:
        return base
    keys = (*_SPREAD_RANK_INT_RANGES, *_SPREAD_RANK_SHARES, "fold_variants")
    missing = [k for k in keys if k not in values]
    if missing:
        _file_missing_rows(SPREAD_RANK_FEATURE, missing)
        _announce_degradation(SPREAD_RANK_FEATURE, f"rows missing: {', '.join(missing)}")
    out: dict[str, Any] = {}
    for key, (low, high) in _SPREAD_RANK_INT_RANGES.items():
        fallback = getattr(base, key)
        out[key] = _coerce_int(values.get(key, fallback), fallback, low, high)
    for key in _SPREAD_RANK_SHARES:
        fallback = getattr(base, key)
        out[key] = _coerce_share(values.get(key, fallback), fallback)
    out["fold_variants"] = _coerce_bool(values.get("fold_variants", base.fold_variants), base.fold_variants)
    return SpreadRankKnobs(**out)
