import enum
import typing as t

from uuid6 import uuid7 as _uuid7

from taktile_auth._logging import get_logger
from taktile_auth._metrics import emit_metric
from taktile_auth.counter import SharedCounter
from taktile_auth.exceptions import LoopDetectedException
from taktile_auth.settings import settings

logger = get_logger()


# CloudWatch metric emitter: ``(name, value, dimensions, unit) -> None``.
# Injectable so tests can substitute an in-memory recorder instead of
# patching at the module level.
EmitMetric = t.Callable[[str, float, t.Dict[str, str], str], None]


def uuid7() -> str:
    """RFC 9562 UUIDv7, sourced from the ``uuid6`` package.

    Note: Stdlib gains ``uuid.uuid7`` in Python 3.14; once taktile-auth raises
    its floor to 3.14 the uuid6 dependency can be dropped.
    """
    return str(_uuid7())


# ``warn`` never raises; ``error`` raises ``LoopDetectedException`` when
# the abort threshold is crossed.
RecursionMode = t.Literal["warn", "error"]


# Shared across every compute service participating in the PEP-295
# distributed counter. All services read/write to this realm so a single
# session prefix accumulates one counter, regardless of which service
# observed the hop.
RECURSION_CACHE_REALM = "recursion"


class RecursionDecision(str, enum.Enum):
    OK = "ok"
    WARN = "warn"
    ABORT = "abort"


_RECURSION_COUNTER_KEY_PREFIX = "_recursion_weight:"


def recursion_counter_key(session_prefix: str) -> str:
    """Cache key under which ``RecursionGate`` accumulates the weight for
    ``session_prefix``."""
    return f"{_RECURSION_COUNTER_KEY_PREFIX}{session_prefix}"


class RecursionGate:
    """PEP-295 hop counter.

    Modes:
      - ``warn``: increment, emit a metric on every hop, log on warn-threshold
        crossings, never raise.
      - ``error``: as ``warn`` plus raise ``LoopDetectedException`` once the
        post-increment weight reaches ``abort_weight``.

    Timeout contract: the boto client behind the counter should be
    configured with aggressive timeouts (~50ms recommended) so a slow
    write never stalls the auth path. The counter is best-effort —
    ``record_hop`` swallows any counter exception (including timeouts)
    and returns ``RecursionDecision.OK`` so auth proceeds.
    """

    def __init__(
        self,
        *,
        counter: SharedCounter,
        mode: RecursionMode,
        emit_metric: EmitMetric = emit_metric,
    ) -> None:
        self._counter = counter
        self._mode: RecursionMode = mode
        self._warn_weight = settings.RECURSION_WARN_WEIGHT
        self._abort_weight = settings.RECURSION_ABORT_WEIGHT
        self._ttl_seconds = settings.RECURSION_TTL_SECONDS
        self._emit_metric = emit_metric

    def start_session(self) -> str:
        """Mint a fresh session prefix. Does not touch the cache — first-hop
        sessions skip the DDB write."""
        return uuid7()

    def record_hop(
        self, session_prefix: str, weight: int
    ) -> RecursionDecision:
        """Account for one hop of ``weight``. Returns the decision."""
        if weight <= 0:
            return RecursionDecision.OK

        key = recursion_counter_key(session_prefix)
        try:
            new_weight = self._counter.increment(
                key, weight, self._ttl_seconds
            )
        except Exception as exc:
            # Fail open: counter accuracy is best-effort, but
            # auth availability is not. A transient counter outage
            # (DDB throttling, network blip) must not cascade
            # into auth failures.
            logger.warning(
                "PEP-295 recursion counter unavailable; skipping hop counter",
                extra={
                    "session_prefix": session_prefix,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                },
            )
            return RecursionDecision.OK

        decision = self._classify(new_weight)
        try:
            self._emit(session_prefix, new_weight, decision)
        except Exception as exc:
            logger.warning(
                "PEP-295 recursion gate telemetry emit failed",
                extra={
                    "session_prefix": session_prefix,
                    "weight": new_weight,
                    "decision": decision.value,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                },
            )

        if decision == RecursionDecision.ABORT and self._mode == "error":
            raise LoopDetectedException(
                session_prefix=session_prefix, weight=new_weight
            )
        return decision

    def is_aborted(self, session_prefix: str) -> bool:
        """Whether ``session_prefix`` has reached the abort threshold.

        A pure threshold predicate, independent of mode: ``True`` once the
        accumulated weight reaches ``abort_weight``. Mode governs whether
        ``record_hop`` *raises* at the threshold — it does not change whether a
        prefix is over the limit, so this reports ``True`` under ``warn`` too.
        Lets a caller turn a downstream failure into a terminal recursion stop.
        Best-effort: a counter read failure returns ``False`` so a transient
        cache outage never fabricates an abort.
        """
        if not session_prefix:
            return False
        try:
            weight = self._counter.get(recursion_counter_key(session_prefix))
        except Exception:
            return False
        return bool(weight >= self._abort_weight)

    def _classify(self, weight: int) -> RecursionDecision:
        if weight >= self._abort_weight:
            return RecursionDecision.ABORT
        if weight >= self._warn_weight:
            return RecursionDecision.WARN
        return RecursionDecision.OK

    def _emit(
        self,
        session_prefix: str,
        weight: int,
        decision: RecursionDecision,
    ) -> None:
        if decision == RecursionDecision.WARN:
            self._emit_metric(
                "RecursionGateWarning",
                1.0,
                {"Mode": self._mode},
                "Count",
            )
            logger.warning(
                "PEP-295 recursion gate warn threshold crossed",
                extra={
                    "session_prefix": session_prefix,
                    "weight": weight,
                    "warn_weight": self._warn_weight,
                },
            )
        elif decision == RecursionDecision.ABORT:
            # ``Mode`` dimension distinguishes a "would-have-aborted"
            # (warn mode) from an "actually aborted" (error mode).
            self._emit_metric(
                "RecursionGateAbort",
                1.0,
                {"Mode": self._mode},
                "Count",
            )
            log = logger.error if self._mode == "error" else logger.warning
            log(
                "PEP-295 recursion gate abort threshold crossed",
                extra={
                    "session_prefix": session_prefix,
                    "weight": weight,
                    "abort_weight": self._abort_weight,
                    "mode": self._mode,
                },
            )
