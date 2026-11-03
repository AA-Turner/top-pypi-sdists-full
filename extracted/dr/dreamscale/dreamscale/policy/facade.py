"""The policy ``dreamscale.connect`` returns: one connection state machine over the existing
session machinery.

``AsyncPolicy`` owns a sequence of inner sessions (``AsyncRemotePolicy``: transport, image
preparation, contracts, RTC, blending). It adds what the public surface promises:

* ``predict``/``next_action`` reopen a released session transparently, and reopen is the
  only thing that ever opens a session (see ``dreamscale.policy.connection``);
* ``next_action`` returns within one control tick, with a model action or a hold;
* retries cover a closed list (data-plane drop, request stall, server_lost, time limit,
  server idle timeout, queueing); everything else raises with its fix;
* idle release after 60 s with nothing in flight; on a deployment kept warm, after its
  keep-warm duration (``always``: never); close at exit from the owning process.

``Policy`` is the synchronous wrapper over the same code (``_LoopRunner``).
"""

from __future__ import annotations

import asyncio
import atexit
import contextlib
import contextvars
import dataclasses
import logging
import math
import os
import sys
import time
import weakref
from collections.abc import Awaitable, Callable, Mapping, Sequence
from typing import Any

import httpx
from dreamscale_transport import catalog as _catalog
from dreamscale_transport.errors import (
    AUTH_FAILED,
    SESSION_CLOSED,
    SESSION_EXPIRED,
    QuicRequestError,
    TransportError,
)

from dreamscale import errors
from dreamscale.libero import LiberoObservation
from dreamscale.model_names import internal_model, public_model
from dreamscale.policy.connection import (
    CLASSIFY_TIMEOUT_S,
    CREATE_FLOOR_S,
    DEADLINE_TIMEOUTS_AS_DROP,
    DROP_CONFIRM_S,
    IDLE_RELEASE_S,
    MAX_OPEN_ATTEMPTS,
    MIN_OPEN_WINDOW_S,
    RATE_LIMITED_GIVE_UP_S,
    REQUEST_STALL_S,
    ConnectionMachine,
    Effect,
    Event,
    State,
    rate_limited_delay_s,
    retry_delay_s,
)
from dreamscale.policy.context import history_ticks, window_from_ticks
from dreamscale.policy.deployment import observation_helper
from dreamscale.policy.lifecycle import _LoopRunner
from dreamscale.policy.remote import SendFloorTimeout
from dreamscale.policy.run_loop import (
    AsyncActionController,
    StaleFirstChunkError,
    _hold_position_action,
    require_run_hold,
)
from dreamscale.policy.runtime.contract import RuntimeContract, runtime_contract_for_model
from dreamscale.policy.runtime.rtc import (
    DYNAMIC_FULL_HORIZON_RTC_CONTRACT_ID,
    LATE_BOUND_PREFIX_RTC_CONTRACT_ID,
    RtcConfig,
    RtcDelayEstimator,
    build_dynamic_full_horizon_rtc_request,
    build_late_bound_prefix_rtc_request,
    late_bound_prefix_rows,
)
from dreamscale.policy.types import (
    ActionChunkResult,
    ActResult,
    ObservationLike,
    PolicyContract,
    RunStrategy,
)
from dreamscale.so101 import So101Observation
from dreamscale.yam import YamEndEffectorObservation, YamObservation

log = logging.getLogger("dreamscale")

# True inside a predict() whose wait is bounded by the caller's own deadline, so a timeout
# there is the caller's, not a stall. Per task: a concurrent next_action refill or another
# predict is unaffected.
_USER_BOUND: contextvars.ContextVar[bool] = contextvars.ContextVar(
    "dreamscale_user_bound", default=False
)

DEFAULT_PREDICT_TIMEOUT_S = 60.0
# A deployment's timed keep-warm: how long an idle session on it stays connected (since its
# last call) before it is released. "always" holds without limit; anything else (off, or a
# value this SDK doesn't know) keeps the one-minute release.
KEEP_WARM_HOLD_S = {
    "10m": 600.0, "30m": 1800.0, "1h": 3600.0, "2h": 7200.0, "6h": 21600.0, "12h": 43200.0,
}
DEFAULT_WAIT_TIMEOUT_S = 60.0

# Exceptions a request raises when the link is gone (or the server ended the session).
# Anything else a request raises is a real error and propagates.
_LINK_ERRORS: tuple[type[BaseException], ...] = (
    TimeoutError,
    OSError,
    TransportError,
    StopAsyncIteration,
    asyncio.IncompleteReadError,
    errors.SessionExpiredError,
    errors.ConnectionLostError,
)


# Error frames from the data plane whose code means the session itself is gone. Every
# other frame (INFERENCE_FAILED, INVALID_OBSERVATION, PREPARATION_FAILED, ...) is a
# server-side answer to one request: it is raised to the caller and the session is kept.
_SESSION_GONE_CODES = frozenset({SESSION_CLOSED, SESSION_EXPIRED, AUTH_FAILED})
# Consecutive error frames on refills before a next_action loop raises.
ERROR_FRAMES_BEFORE_RAISE = 3


def is_link_error(exc: BaseException) -> bool:
    if isinstance(exc, SendFloorTimeout):
        return False  # the caller's budget ended before the send floor; nothing dropped
    if isinstance(exc, QuicRequestError):
        return exc.code in _SESSION_GONE_CODES
    if isinstance(exc, _LINK_ERRORS):
        return True
    # websockets' ConnectionClosed family, without importing it here.
    return any(cls.__name__ == "ConnectionClosed" for cls in type(exc).__mro__)


def _frame_fix(code: str, deployment: Any) -> str:
    """The fix for one error frame. An observation a deployment session's server refused
    points at that deployment's contract and helper; a catalog model's, at the Models page."""
    if code == "invalid_observation" and deployment is not None:
        return ("policy.contract lists the cameras, state width and history this deployment "
                f"reads; {observation_helper(deployment)} builds its observation")
    if code == "invalid_observation":
        return "check the observation against the model's contract (see the Models page)"
    return ("try again; if it keeps happening for this model, email team@dreamscalelabs.com "
            "with the session id")


def closed_fix(code: str, deployment: Any = None) -> str:
    """The fix when a frame closes the policy: an invalid observation keeps its own fix,
    anything else checks the model; either way the policy connects again."""
    first = (_frame_fix(code, deployment) if code == "invalid_observation"
             else "check `dreamscale models list`")
    return f"{first}, then call dreamscale.connect() again"


def server_frame_error(
    exc: QuicRequestError, *, model: str, deployment: Any = None
) -> errors.DreamscaleError:
    """An error frame as a Dreamscale error: the frame's code (lower case) and detail.
    ``deployment``: the session's own deployment, whose contract and helper are the fix."""
    code = exc.code.lower()
    error = errors.DreamscaleError(
        errors.ErrorInfo(
            code=code,
            problem=f"{public_model(model)} returned {exc.code}",
            cause=exc.detail or "the server could not answer this request",
            fix=_frame_fix(code, deployment),
        )
    )
    error.__cause__ = exc
    return error


def _deployment_of(inner: Any) -> Any:
    """The session's own deployment (π0.5's or an exported base's), if it has one."""
    return getattr(inner, "deployment", None)


def repeated_frame_error(
    exc: QuicRequestError, *, model: str, deployment: Any = None
) -> errors.DreamscaleError:
    """Three error frames in a row: the policy is closed with this error."""
    error = errors.DreamscaleError(
        errors.ErrorInfo(
            code=exc.code.lower(),
            problem=f"{public_model(model)} failed {ERROR_FRAMES_BEFORE_RAISE} requests in a row "
            f"({exc.code})",
            cause=exc.detail or "the server could not answer these requests",
            fix=closed_fix(exc.code.lower(), deployment),
        )
    )
    error.__cause__ = exc
    return error


def is_retryable_open_error(exc: BaseException) -> bool:
    """Open attempts retry only network failures, 429 and 5xx; everything else is final."""
    if isinstance(exc, httpx.TransportError):
        return True
    if isinstance(exc, errors.ServerError):
        return exc.status >= 500
    if isinstance(exc, errors.DreamscaleError):
        return exc.code == "rate_limited"
    return False


# Hold rules by action space and the contract's hold behaviour, not by model.
HOLD_MEASURED = "measured"  # absolute joints: command the positions measured this tick
# Delta end-effector (a simulator), a π0.5 deployment acting in its model's own space, or a
# contract that waits for each chunk (InternW0-Δ, RTC off: upstream's sync loop): wait for the
# real action, and the wait skips none of the plan.
HOLD_WAIT = "wait"
HOLD_LEGACY = "legacy"  # anything else: today's hold_behavior


def hold_rule(contract: RuntimeContract) -> str:
    if contract.action_space in ("libero_delta_eef", "model_defined"):
        return HOLD_WAIT
    if contract.hold_behavior == "wait":
        return HOLD_WAIT
    if (
        contract.action_space in ("absolute_joint_position", "raw_absolute_joint")
        and contract.hold_behavior == "current_position"
    ):
        return HOLD_MEASURED
    return HOLD_LEGACY


def hold_action(contract: RuntimeContract, observation: Any) -> tuple[float, ...]:
    """What to command when there is no model action this tick: always an action row of the
    contract's width (rows that aren't the state come from ``contract.hold_indices``)."""
    return _checked_hold(contract, _measured_hold(contract, observation))


def _checked_hold(contract: RuntimeContract, hold: Sequence[float]) -> tuple[float, ...]:
    hold = tuple(float(value) for value in hold)
    if contract.action_dim is not None and len(hold) != contract.action_dim:
        raise errors.observation_error(
            "observation", f"a hold of {len(hold)} values",
            f"an observation whose hold_action is an action row of {contract.action_dim} "
            "values (the robot's measured position in the model's action layout)",
        )
    return hold


def _measured_hold(contract: RuntimeContract, observation: Any) -> tuple[float, ...]:
    if hold_rule(contract) == HOLD_MEASURED:
        measured = getattr(observation, "hold_action", None)
        if measured is None:
            measured = getattr(observation, "joint_positions", None)
        if measured is None:
            raise errors.observation_error(
                "observation", f"a {type(observation).__name__} without measured joint positions",
                "an observation with the robot's measured positions (hold_action or "
                "joint_positions), which the arm holds while no action is available",
            )
        return tuple(float(value) for value in measured)
    return _hold_position_action(contract=contract, observation=observation, last_action=None)


# Models whose robot kind this module can synthesise a calibration observation for (their
# catalog entries' ``client.calibration``). Any other model keeps today's behaviour
# (calibration on the first call).
CALIBRATION_MODELS = frozenset(
    entry.id for entry in _catalog.CATALOG if entry.client.calibration
)


def synthetic_observation(model: str, contract: RuntimeContract) -> Any | None:
    """An observation of the right shape for the robot kind, for network calibration at
    open, before the user has captured anything. Deterministic noise frames at the wire
    size, so the JPEG payload (and the measured upload) is realistic, not a few KB of
    black."""
    import numpy as np

    from dreamscale import libero, so101, yam

    if model not in CALIBRATION_MODELS:
        return None
    kind = robot_kind(contract)
    wire = contract.wire_image
    height, width = (wire.size[1], wire.size[0]) if wire is not None else (480, 640)
    if kind == "libero":
        height, width = 256, 256
    rng = np.random.default_rng(0)

    def frame() -> Any:
        return rng.integers(0, 256, size=(height, width, 3), dtype=np.uint8)

    if kind == "so101":
        return so101.observation(side_frame=frame(), wrist_frame=frame(), joint_positions=[0.0] * 6)
    if kind == "yam":
        return yam.observation(
            top_frame=frame(), left_frame=frame(), right_frame=frame(),
            left_joint_positions=[0.0] * 6, left_gripper=0.0,
            right_joint_positions=[0.0] * 6, right_gripper=0.0,
        )
    if kind == "libero":
        return libero.observation(agent_frame=frame(), wrist_frame=frame(), state=[0.0] * 8)
    return None


async def _wait_quietly(awaitable: Any, *, timeout_s: float) -> None:
    """Wait for another task's work (shielded, bounded), ignoring its errors but never
    swallowing a cancellation aimed at our own task."""
    try:
        await asyncio.wait_for(asyncio.shield(awaitable), timeout=timeout_s)
    except asyncio.CancelledError:
        if not _cancelled_by_someone_else():
            raise
    except BaseException:  # noqa: BLE001 - the other task reports its own outcome
        pass


def inner_for(controller: AsyncActionController) -> Any:
    return getattr(controller, "_policy", None)


def _cancelled_by_someone_else() -> bool:
    """True when a CancelledError reached us although nobody cancelled our own task
    (a shielded inner task was cancelled by a drop)."""
    task = asyncio.current_task()
    cancelling = getattr(task, "cancelling", None)
    return task is not None and callable(cancelling) and cancelling() == 0


def robot_kind(contract: RuntimeContract) -> str | None:
    """The robot an observation must come from: so101, yam, libero, or None (unchecked)."""
    if contract.action_space == "libero_delta_eef":
        return "libero"
    if contract.action_space == "model_defined":
        return None  # a π0.5 deployment's own robot: the session checks its observations
    if contract.joint_unit == "deg" and contract.action_dim == 6:
        return "so101"
    if contract.joint_unit == "rad" and contract.action_dim == 14:
        return "yam"
    return None


_OBSERVATION_KINDS: dict[type, str] = {
    So101Observation: "so101",
    YamObservation: "yam",
    YamEndEffectorObservation: "yam",
    LiberoObservation: "libero",
}
_OBSERVE_HELPERS = {
    "so101": "dreamscale.so101.observation",
    "yam": "dreamscale.yam.observation",
    "libero": "dreamscale.libero.observation",
}


def prepare_observation(observation: Any, *, model: str, contract: RuntimeContract) -> Any:
    """Check the observation against the connected model before anything is sent, and
    fill in what the policy knows (a LIBERO observation built without ``model=``)."""
    expected = robot_kind(contract)
    given = _OBSERVATION_KINDS.get(type(observation))
    if expected is not None and given is not None and given != expected:
        raise errors.observation_error(
            "observation",
            f"a {type(observation).__name__}",
            f"an observation from {_OBSERVE_HELPERS[expected]} for {public_model(model)}",
        )
    if isinstance(observation, LiberoObservation):
        from dreamscale.libero import stamped_for_model

        return stamped_for_model(observation, model)
    return observation


def require_instruction(instruction: Any) -> str:
    if not isinstance(instruction, str) or not instruction.strip():
        raise errors.observation_error(
            "instruction", "missing" if instruction is None else repr(instruction),
            "a non-empty text instruction, e.g. \"pick up the red block\"",
        )
    return instruction


def rtc_kind(resolved: Any) -> str:
    """The session's real-time chunking as ``policy.contract.rtc`` names it: "train_time"
    only for the late-bound prefix, the contract that pins committed actions."""
    if resolved is None or getattr(resolved, "rtc", "off") != "on":
        return "off"
    if getattr(resolved, "rtc_contract", None) == LATE_BOUND_PREFIX_RTC_CONTRACT_ID:
        return "train_time"
    return "inference_time"


def guides_committed_rows(resolved: Any, deployment: Any) -> bool:
    """Test-time RTC that takes committed actions as its guidance prefix: a deployment's dynamic
    full-horizon contract (π0.5's), which holds the new chunk to them for as long as the SDK's
    measured latency says the robot plays them. Shared models' test-time RTC doesn't."""
    return (
        deployment is not None
        and rtc_kind(resolved) == "inference_time"
        and getattr(resolved, "rtc_contract", None) == DYNAMIC_FULL_HORIZON_RTC_CONTRACT_ID
    )


def guided_rows_cap(contract: RuntimeContract) -> int:
    """The most committed rows test-time RTC holds a chunk to: the chunk less the fresh rows the
    dynamic request always leaves (its estimator's reserve)."""
    chunk = int(contract.chunk_size)
    reserve = _guided_estimator(contract).state().fresh_reserve_steps
    return max(0, chunk - int(reserve))


def _guided_estimator(contract: RuntimeContract) -> RtcDelayEstimator:
    return RtcDelayEstimator(
        chunk_size=int(contract.chunk_size), action_hz=float(contract.action_hz),
        control_mode="adaptive",
    )


def policy_contract(
    model: str, contract: RuntimeContract, *, deployment: Any, resolved: Any,
    history: Any = None,
) -> PolicyContract:
    """``policy.contract``: the session's runtime contract, its deployment, its RTC and its
    observation window (``history``: the session's ``observation_history``)."""
    rtc = rtc_kind(resolved)
    max_prefix_rows: int | None = 0
    if rtc == "train_time":
        if deployment is not None:
            max_prefix_rows = getattr(deployment, "rtc_max_prefix_rows", None)
            if max_prefix_rows is None:
                # ABC-VLA: the deployment's own cap on the rows a request pins.
                max_prefix_rows = getattr(deployment, "rtc_max_delay", None)
        else:
            # A catalog model's trained prefix bound (its entry's rtc_max_prefix_rows).
            entry = _catalog.entry(internal_model(model))
            max_prefix_rows = None if entry is None else entry.rtc_max_prefix_rows
    elif guides_committed_rows(resolved, deployment):
        # Test-time RTC holds at most a chunk less the fresh rows its request keeps
        # (build_dynamic_full_horizon_rtc_request's reserve).
        max_prefix_rows = guided_rows_cap(contract)
    state_dim = getattr(deployment, "state_dim", None)
    return PolicyContract(
        action_hz=float(contract.native_hz),
        chunk_size=int(contract.chunk_size),
        action_dim=None if contract.action_dim is None else int(contract.action_dim),
        state_dim=None if state_dim is None else int(state_dim),
        camera_keys=tuple(getattr(deployment, "camera_keys", ()) or ()),
        rtc=rtc,
        max_prefix_rows=max_prefix_rows,
        past_observations=history_ticks(history),
        action_history=int(contract.action_history),
    )


EXPECTED_PAST = (
    "observations from the same helper as observation, one per control tick at the "
    "model's rate (policy.contract.action_hz), oldest first, ending just before it"
)


def past_ticks(past_observations: Any, observation: Any, *, model: str,
               contract: RuntimeContract) -> list[Any] | None:
    """``predict(past_observations=)`` checked before anything is sent: each from the same
    helper as ``observation``, and, where they carry capture times, one control tick apart
    up to it (a gap would feed the model the wrong instants)."""
    if past_observations is None:
        return None
    if isinstance(past_observations, (str, bytes, Mapping)) or not isinstance(
        past_observations, Sequence
    ):
        raise errors.observation_error(
            "past_observations", type(past_observations).__name__, EXPECTED_PAST
        )
    ticks = []
    for tick in past_observations:
        if type(tick) is not type(observation):
            raise errors.observation_error(
                "past_observations", f"a {type(tick).__name__}", EXPECTED_PAST
            )
        ticks.append(prepare_observation(tick, model=model, contract=contract))
    times = [getattr(tick, "capture_time_ns", None) for tick in (*ticks, observation)]
    if len(times) > 1 and all(time_ns is not None for time_ns in times):
        period_ns = 1e9 / float(contract.native_hz)
        for index, (earlier, later) in enumerate(zip(times, times[1:], strict=False)):
            apart = (later - earlier) / period_ns
            if not 0.5 <= apart < 1.5:
                after = "observation" if index == len(ticks) - 1 else f"entry {index + 1}"
                raise errors.observation_error(
                    "past_observations",
                    f"entry {index} and {after} captured {apart:.2f} control ticks apart",
                    EXPECTED_PAST,
                )
    return ticks


EXPECTED_COMMITTED = (
    "the actions the robot will still execute after this observation, in order: rows of "
    "finite numbers in the same units and order as the chunk's actions"
)


def committed_rows(
    committed_actions: Any, *, action_dim: int | None
) -> tuple[tuple[float, ...], ...] | None:
    """``predict(committed_actions=)`` checked before anything is sent."""
    if committed_actions is None:
        return None
    if isinstance(committed_actions, (str, bytes, Mapping)):
        raise errors.observation_error(
            "committed_actions", type(committed_actions).__name__, EXPECTED_COMMITTED
        )
    try:
        rows = [tuple(row) for row in committed_actions]
    except TypeError:
        raise errors.observation_error(
            "committed_actions", type(committed_actions).__name__, EXPECTED_COMMITTED
        ) from None
    widths = {len(row) for row in rows}
    expected_width = action_dim if action_dim is not None else next(iter(widths), None)
    if widths and widths != {expected_width}:
        given = ", ".join(str(width) for width in sorted(widths))
        raise errors.observation_error(
            "committed_actions", f"rows of {given} values",
            f"rows of {expected_width} values: {EXPECTED_COMMITTED}",
        )
    checked = []
    for row in rows:
        if any(isinstance(value, (bool, str, bytes)) for value in row):
            raise errors.observation_error(
                "committed_actions", "non-numeric values", EXPECTED_COMMITTED
            )
        try:
            values = tuple(float(value) for value in row)
        except (TypeError, ValueError, OverflowError):
            raise errors.observation_error(
                "committed_actions", "non-numeric values", EXPECTED_COMMITTED
            ) from None
        if not all(math.isfinite(value) for value in values):
            raise errors.observation_error(
                "committed_actions", "non-finite values", EXPECTED_COMMITTED
            )
        checked.append(values)
    return tuple(checked)


class _Pacer:
    """Returns at the model's ticks and never catches up: a late caller gets the next
    action immediately and the actions its lateness covered are skipped."""

    def __init__(self, clock: Callable[[], float]) -> None:
        self._clock = clock
        self.next_due: float | None = None

    def wait_deadline(self, period_s: float, *, pace: bool) -> float:
        now = self._clock()
        if not pace or self.next_due is None:
            return now + period_s
        return max(now, self.next_due)

    async def finish(
        self,
        period_s: float,
        *,
        pace: bool,
        sleep: Callable[[float], Awaitable[Any]],
        excused_s: float = 0.0,
    ) -> int:
        """Align to the tick (pace=True). Returns how many actions went stale; lateness
        ``excused_s`` covers (the robot held while the SDK waited) stales none."""
        if not pace:
            return 0
        now = self._clock()
        if self.next_due is None:
            self.next_due = now + period_s
            return 0
        if now < self.next_due:
            await sleep(self.next_due - now)
            now = self.next_due
        late = now - self.next_due
        skipped = int(max(0.0, late - excused_s) // period_s)
        self.next_due = (now if late >= period_s else self.next_due) + period_s
        return skipped


_OPEN_POLICIES: weakref.WeakSet = weakref.WeakSet()


def _close_open_policies_at_exit() -> None:
    # Sync wrappers first: they close their async core through its still-running loop.
    ordered = sorted(_OPEN_POLICIES, key=lambda p: isinstance(p, AsyncPolicy))
    for policy in ordered:
        if getattr(policy, "_pid", None) != os.getpid():
            continue  # a forked child never closes its parent's sessions
        with contextlib.suppress(Exception):
            policy._close_at_exit()


atexit.register(_close_open_policies_at_exit)


def default_progress() -> Callable[[str], None]:
    """Status output: stderr when it is a terminal, otherwise the ``dreamscale`` logger."""
    stderr = getattr(sys, "stderr", None)
    if stderr is not None and getattr(stderr, "isatty", lambda: False)():
        from rich.console import Console

        from dreamscale.terminal import ProgressPrinter

        return ProgressPrinter(console=Console(stderr=True, highlight=False, soft_wrap=True))
    return lambda line: log.info("%s", line)


class AsyncPolicy:
    """What ``dreamscale.aconnect`` returns. See the module docstring."""

    def __init__(
        self,
        *,
        model: str,
        opener: Callable[..., Awaitable[Any]],
        progress: Callable[[str], None] | None,
        idle_release_s: float = IDLE_RELEASE_S,
        request_stall_s: float = REQUEST_STALL_S,
        clock: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], Awaitable[Any]] = asyncio.sleep,
    ) -> None:
        self._model = model  # the internal id (contracts, calibration, stamping)
        self._opener = opener
        self._progress = progress
        self._idle_release_s = float(idle_release_s)
        self._request_stall_s = float(request_stall_s)
        self._clock = clock
        self._sleep = sleep
        self._machine = ConnectionMachine(State.RELEASED)
        self._inner: Any | None = None
        self._controller: AsyncActionController | None = None
        self._snapshot: dict[str, Any] = {}
        self._failure: BaseException | None = None
        self._failure_candidate: BaseException | None = None
        self._rate_limited_since: float | None = None
        self._pending_drop_failure: BaseException | None = None
        self._pinned_failure: BaseException | None = None
        self._last_activity: float = clock()
        self._last_call_at: float = float("-inf")
        self._waiters = 0
        self._deadline_timeouts = 0
        self._error_frames = 0
        # (session, instruction) the open session last prepared (models that prepare tasks).
        self._prepared_task: tuple[Any, str] | None = None
        # Open tasks cancelled because their caller left: close() waits for their cleanup
        # (the DELETE of whatever they created) before returning.
        self._abandoned: set[asyncio.Task[Any]] = set()
        self._task: asyncio.Task[Any] | None = None  # the open / retry task
        self._teardown: asyncio.Task[Any] | None = None  # release / drop in progress
        self._idle_task: asyncio.Task[Any] | None = None
        self._changed = asyncio.Event()
        self._in_flight = 0
        self._pinned = False
        self._opened_once = False
        self._attempt = 0
        self._last_create_at: float | None = None
        self._calibration_profile: Any = None
        self._pacer = _Pacer(clock)
        self._pid = os.getpid()
        self._loop: asyncio.AbstractEventLoop | None = None
        self._closing = False
        self.queue_position: int | None = None
        self.queue_eta_s: int | None = None
        # (session id, chunk id, receipt time.time_ns()) of the last predict() chunk.
        self._predict_receipt: tuple[str, int, int] | None = None
        # Test-time RTC's delay estimate for predict(committed_actions=): the session shape it
        # counts in (chunk, rate), the estimate, and the session whose calibration seeded it.
        self._guided_delays: tuple[Any, RtcDelayEstimator, str | None] | None = None
        _OPEN_POLICIES.add(self)

    # ------------------------------------------------------------------ public surface

    async def predict(
        self,
        observation: ObservationLike,
        instruction: str | None = None,
        *,
        timeout_s: float = DEFAULT_PREDICT_TIMEOUT_S,
        past_observations: Sequence[ObservationLike] | None = None,
        action_history: Sequence[Sequence[float]] | None = None,
        committed_actions: Sequence[Sequence[float]] | None = None,
    ) -> ActionChunkResult:
        """One observation in, one action chunk out, stateless: everything the model reads
        travels with the call. ``past_observations``/``action_history``: the control ticks
        just before this one and the actions executed on them, oldest first (as many as
        ``policy.contract`` says; fewer at an episode's start are padded and counted in
        ``history_padded``). ``committed_actions`` (the actions the robot will still execute
        after this observation) on train-time RTC: the server pins as many as it expects to
        play before the chunk arrives (``prefix_rows``), at most ``policy.contract``'s
        ``max_prefix_rows``. Hy-VLA's are 40-value pose rows expressed against this
        observation's state: the SDK recomputes each row's relative half (values 0-19) from
        its absolute half (values 20-39) against this observation's state, so rows planned
        against an earlier chunk's state can be passed as they are."""
        self._guard()
        instruction = require_instruction(instruction)
        contract = self.runtime_contract
        observation = prepare_observation(observation, model=self._model, contract=contract)
        past = past_ticks(past_observations, observation, model=self._model, contract=contract)
        rows = committed_rows(committed_actions, action_dim=contract.action_dim)
        deadline = self._clock() + float(timeout_s)
        for attempt in (1, 2):
            inner = await self._ready_inner(deadline)
            self._require_history(inner, past, action_history)
            rtc_context = None
            if rows is not None:
                rtc_context = self._committed_rtc_context(inner, rows)
            remaining = deadline - self._clock()
            if remaining <= 0:
                raise errors.catalog("action_timeout", detail=f"{float(timeout_s):g} s")
            # A wait bounded by the caller's own deadline is not a stall: a timeout there
            # is raised and the session is kept.
            user_bound = remaining < self._request_stall_s
            token = _USER_BOUND.set(user_bound)
            try:
                async with self._call():
                    await asyncio.wait_for(
                        self._prepare_task(inner, instruction), timeout=remaining
                    )
                    # After preparation: Isaac's context window exists only from then on.
                    request, padded = self._history_window(inner, observation, past)
                    remaining = deadline - self._clock()
                    # The outer wait bounds the whole call, including the session's request
                    # lock; the inner timeout is what detects a stall.
                    result = await asyncio.wait_for(
                        inner._predict_chunk(
                            request,
                            instruction=instruction,
                            timeout_s=min(self._request_stall_s, remaining),
                            actions_remaining=None,
                            is_calibration=False,
                            calibration_context=None,
                            rtc_context=rtc_context,
                            action_history=tuple(action_history or ()),
                        ),
                        timeout=remaining,
                    )
                self._deadline_timeouts = 0
                self._error_frames = 0
                if guides_committed_rows(
                    getattr(inner, "resolved_optimization_config", None),
                    getattr(inner, "deployment", None),
                ):
                    # The actions the robot played while this chunk was on its way (at the
                    # rate it's commanded): every predict() measures it, so a committed call
                    # after the first has it.
                    trip_s = result.timing.obs_to_action_ms / 1000.0
                    self._guided_delay(inner).record(
                        math.ceil(max(0.0, trip_s) * float(inner.runtime_contract.action_hz)),
                        eligible=True,
                    )
                if result.chunk_id is not None:
                    # The server measures the return trip from the next request's report.
                    self._predict_receipt = (
                        str(inner.session_id), int(result.chunk_id), time.time_ns()
                    )
                commands = int(inner.runtime_contract.action_history)
                missing_commands = max(0, commands - len(action_history or ()))
                return dataclasses.replace(
                    result, history_padded=max(padded, missing_commands)
                )
            except asyncio.CancelledError:
                if not _cancelled_by_someone_else():
                    raise
                failure: BaseException = errors.catalog("connection_lost")
            except SendFloorTimeout as exc:
                raise errors.catalog(
                    "action_timeout",
                    detail=f"{float(timeout_s):g} s; requests to shared models are spaced "
                    "at least 0.4 s apart: wait, or raise timeout_s",
                ) from exc
            except TimeoutError as exc:
                if user_bound:
                    self._deadline_timeouts += 1
                    if (
                        self._deadline_timeouts >= DEADLINE_TIMEOUTS_AS_DROP
                        and inner is self._inner
                        and self._machine.state is State.READY
                    ):
                        # Three short timeouts in a row with nothing answered: that is a
                        # dead link, not a tight budget.
                        self._deadline_timeouts = 0
                        self._fire(Event.LINK_LOST)
                    raise errors.catalog(
                        "action_timeout", detail=f"{float(timeout_s):g} s"
                    ) from exc
                failure = exc
            except QuicRequestError as exc:
                if not is_link_error(exc):
                    self._after_error_frame(inner)
                    raise server_frame_error(
                        exc, model=self._model, deployment=_deployment_of(inner)
                    ) from exc
                failure = exc
            except BaseException as exc:
                if not is_link_error(exc):
                    raise
                failure = exc
            finally:
                _USER_BOUND.reset(token)
            # The hook has already released the session; resend once on a new one.
            if attempt == 2 or self._pinned_failure is not None:
                raise errors.catalog(
                    "reconnect_failed", detail=str(failure) or None
                ) from failure

        raise AssertionError("unreachable")

    def _require_history(self, inner: Any, past: list[Any] | None, action_history: Any) -> None:
        """Refuse a call that leaves out history the model can't run without: FLUX
        deployments read measured states (the server refuses a request without its full
        window), and FLUX models condition on their executed actions. Elsewhere a missing
        history is allowed and counted in ``history_padded``."""
        from dreamscale.policy.context import EpisodeHistory

        model = public_model(self._model)
        history = getattr(inner, "observation_history", None)
        if past is not None and isinstance(history, EpisodeHistory):
            raise errors.catalog("past_observations_unsupported", model=model)
        ticks = history_ticks(history)
        commands = int(inner.runtime_contract.action_history)
        needs_states = getattr(history, "state_steps", 0) > 0
        missing = [
            *(["past_observations"] if needs_states and past is None else []),
            *(["action_history"] if commands and action_history is None else []),
        ]
        if missing:
            wanted = [
                *([f"past_observations (the last {ticks} observations)"] if ticks else []),
                *([f"action_history (the last {commands} executed actions)"]
                  if commands else []),
            ]
            raise errors.catalog(
                "history_required", model=model, missing=" or ".join(missing),
                wanted=" and ".join(wanted),
            )

    @staticmethod
    def _history_window(inner: Any, observation: Any, past: list[Any] | None) -> tuple[Any, int]:
        """The request's observation with its window built from ``past`` (the session's own
        window rules), and the ticks filled in; without ``past``, the observation alone and
        every tick the window reads counted as filled in."""
        history = getattr(inner, "observation_history", None)
        if past is None:
            return observation, history_ticks(history)
        return window_from_ticks(history, observation, past)

    def _committed_rtc_context(self, inner: Any, rows: tuple[tuple[float, ...], ...]) -> Any:
        """Train-time RTC: the late-bound prefix request (the caller's committed rows, the send
        time and the previous predict() chunk's receipt on this session: the server's return
        estimate). Test-time RTC: the rows as its guidance prefix, held for as many actions as
        this policy's measured latency says the robot plays before the chunk arrives."""
        resolved = getattr(inner, "resolved_optimization_config", None)
        if guides_committed_rows(resolved, getattr(inner, "deployment", None)):
            estimator = self._guided_delay(inner)
            return build_dynamic_full_horizon_rtc_request(
                config=RtcConfig(enabled=True, contract_id=DYNAMIC_FULL_HORIZON_RTC_CONTRACT_ID),
                state=estimator.state(),
                action_dim=inner.runtime_contract.action_dim,
                reference_actions=rows,
                estimator_source=estimator.source,
                estimator_sample_count=estimator.sample_count,
            )
        kind = rtc_kind(resolved)
        if kind != "train_time":
            raise errors.catalog(
                "committed_actions_unsupported", model=public_model(self._model), kind=kind,
                deployment=getattr(inner, "deployment", None) is not None,
            )
        previous = self._predict_receipt
        if previous is not None and previous[0] != str(inner.session_id):
            previous = None  # another session's chunk: the new server never sent it
        return build_late_bound_prefix_rtc_request(
            reference_actions=rows,
            previous_chunk_id=None if previous is None else previous[1],
            previous_chunk_receipt_unix_ns=None if previous is None else previous[2],
            client_send_unix_ns=time.time_ns(),
            max_rows=late_bound_prefix_rows(getattr(inner, "deployment", None)),
        )

    def _guided_delay(self, inner: Any) -> RtcDelayEstimator:
        """This policy's test-time RTC delay estimate: the return trips of its predict() calls
        (kept across reconnects, which a fresh session would otherwise start at zero), seeded
        from each session's network calibration where there is one."""
        contract = inner.runtime_contract
        shape = (int(contract.chunk_size), float(contract.action_hz))
        session = str(inner.session_id)
        if self._guided_delays is None or self._guided_delays[0] != shape:
            self._guided_delays = (shape, _guided_estimator(contract), None)
        _, estimator, seeded = self._guided_delays
        profile = getattr(inner, "_calibration_profile", None)
        if seeded != session and profile is not None:
            estimator.seed_calibration(profile)
            self._guided_delays = (shape, estimator, session)
        return estimator

    @property
    def contract(self) -> PolicyContract:
        """What the connected model returns and accepts: rate, chunk, widths, cameras, RTC."""
        inner = self._inner
        snapshot = self._snapshot
        return policy_contract(
            self._model,
            self.runtime_contract,
            deployment=getattr(inner, "deployment", None) if inner is not None
            else snapshot.get("deployment"),
            resolved=getattr(inner, "resolved_optimization_config", None) if inner is not None
            else snapshot.get("resolved_optimization_config"),
            history=getattr(inner, "observation_history", None) if inner is not None
            else snapshot.get("observation_history"),
        )

    async def next_action(
        self,
        observation: ObservationLike,
        instruction: str | None = None,
        *,
        pace: bool = True,
        timeout_s: float | None = None,
    ) -> tuple[float, ...]:
        """One executable action per call, on the model's clock."""
        self._guard()
        instruction = require_instruction(instruction)
        contract = self.runtime_contract
        observation = prepare_observation(observation, model=self._model, contract=contract)
        period_s = 1.0 / float(contract.action_hz)
        rule = hold_rule(contract)
        self._last_call_at = self._clock()
        wait_deadline = self._pacer.wait_deadline(period_s, pace=pace)
        hard_deadline = self._clock() + (
            DEFAULT_WAIT_TIMEOUT_S if timeout_s is None else float(timeout_s)
        )
        step_deadline = hard_deadline if rule == HOLD_WAIT else wait_deadline
        # Lateness on the tick that receives action 0 belongs to the startup, not to the
        # new plan: skipping applies only when a plan was already being executed.
        controller_before = self._controller
        dispatched_before = controller_before is not None and controller_before.dispatched
        action: tuple[float, ...] | None = None
        blocked_from = self._clock()
        while action is None:
            self._guard()
            if self._machine.state is State.READY:
                step = await self._step(observation, instruction, step_deadline)
                if step is not None and (not step.stalled or rule != HOLD_WAIT):
                    action = step.action
                    if step.stalled:
                        action = hold_action(contract, observation)
                        assert self._controller is not None
                        await self._controller.record_act_result(
                            step.action, ActResult(accepted_action=action)
                        )
                    break
            elif self._machine.state is State.RELEASED:
                self._fire(Event.OPEN)
            if rule != HOLD_WAIT:
                action = hold_action(contract, observation)
                break
            remaining = hard_deadline - self._clock()
            if remaining <= 0:
                raise errors.catalog(
                    "action_timeout",
                    detail=f"{DEFAULT_WAIT_TIMEOUT_S if timeout_s is None else timeout_s:g} s",
                )
            self._changed.clear()
            self._waiters += 1
            try:
                with contextlib.suppress(TimeoutError):
                    await asyncio.wait_for(self._changed.wait(), timeout=min(remaining, 0.5))
            finally:
                self._waiters -= 1
        # Under "wait" the robot holds while this call blocks for a chunk: none of the plan
        # went by then. Only the caller's own lateness skips actions.
        blocked_s = self._clock() - blocked_from if rule == HOLD_WAIT else 0.0
        skipped = await self._pacer.finish(
            period_s, pace=pace, sleep=self._sleep, excused_s=blocked_s
        )
        if skipped and dispatched_before and self._controller is controller_before:
            self._controller.skip(skipped)
        return action

    async def prefetch(
        self,
        observation: ObservationLike,
        instruction: str | None = None,
        *,
        timeout_s: float = DEFAULT_PREDICT_TIMEOUT_S,
    ) -> None:
        """Request this policy's first chunk now, ahead of handing the robot over to it (from
        another deployment's policy, or after a pause): the next ``next_action()``, with the
        same instruction, starts from that chunk instead of holding for one. (Unlike
        ``prepare``, it doesn't pin the session, and it sends the request; it prepares the
        instruction too.)

        Call it about one round trip before the switch, on a policy already connected (it
        opens a released one, and blocks meanwhile). It returns once the request is under
        way, without waiting for the chunk. Whatever the policy had queued from before is
        dropped; the latest prefetch counts. A chunk that then waits unmerged for longer
        than its round trip is requested again from the first ``next_action()``'s
        observation, never replayed from an old pose. On a shared model whose request
        spacing hasn't passed, the request goes with that first ``next_action()``."""
        self._guard()
        instruction = require_instruction(instruction)
        contract = self.runtime_contract
        observation = prepare_observation(observation, model=self._model, contract=contract)
        deadline = self._clock() + float(timeout_s)
        while True:
            await self._ready_inner(deadline)
            controller = self._controller
            if controller is None:
                continue  # lost while opening: open again
            try:
                async with self._call():
                    await asyncio.wait_for(
                        self._prepare_task(inner_for(controller), instruction),
                        timeout=max(0.0, deadline - self._clock()),
                    )
                    # The request's own stall limit, as for any refill (not the caller's).
                    stall_s = min(self._request_stall_s, max(0.0, deadline - self._clock()))
                    await controller.prepare(
                        observation, instruction=instruction, timeout_s=stall_s, ahead=True,
                    )
            except asyncio.CancelledError:
                if not _cancelled_by_someone_else():
                    raise
                continue  # a drop cancelled the request: open again
            except TimeoutError as exc:
                raise errors.catalog("action_timeout", detail=f"{float(timeout_s):g} s") from exc
            except QuicRequestError as exc:
                if is_link_error(exc) or self._controller is not controller:
                    continue
                controller.forget_request()
                failed = inner_for(controller)
                self._after_error_frame(failed)
                raise server_frame_error(
                    exc, model=self._model, deployment=_deployment_of(failed)
                ) from exc
            except BaseException as exc:
                if is_link_error(exc) or self._controller is not controller:
                    continue
                raise
            if self._controller is controller:
                return
            # The link was lost while preparing: open again and send on the new session.

    async def close(self) -> None:
        """Close the session now. Optional: idle release (after a minute idle; on a deployment
        kept warm, after its keep-warm duration, never for always) and atexit also close
        it."""
        if self._machine.is_closed:
            await self._await_shutdown()  # a failure-closed policy may still be deleting
            return
        _OPEN_POLICIES.discard(self)
        if os.getpid() != self._pid:
            # A forked child closes its handle only; the parent's session is the parent's.
            self._machine.state = State.CLOSED
            return
        self._closing = True
        self._fire(Event.CLOSE)
        await self._await_shutdown()

    async def __aenter__(self) -> AsyncPolicy:
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        await self.close()

    @property
    def model(self) -> str:
        """The model's public name (what you passed to connect, in its current spelling)."""
        return public_model(self._model)

    @property
    def state(self) -> str:
        return self._machine.state.value

    # Forwarded, undocumented session API. Using any of these pins the session: no idle
    # release and no transparent reopen, today's semantics.

    async def prepare(self, *, instruction: str, timeout_s: float | None = None) -> None:
        """For the pinned run API (``run``, ``begin_episode``/``step``) on models that prepare
        each instruction (Isaac 0.5): pin the session (no idle release) and warm the model up
        for ``instruction``. It sends no request. Other models have nothing to prepare and
        raise ValueError. For handing the robot to this policy's ``next_action()``, use
        ``prefetch`` (any model): it prepares the instruction where the model needs it and
        sends the first request."""
        inner = await self._pin()
        async with self._call(), self._frames_as_errors():
            await inner.prepare(instruction=instruction, timeout_s=timeout_s)

    async def run(self, **kwargs: Any) -> Any:
        require_run_hold(self.runtime_contract)  # before pinning: next_action still reconnects
        inner = await self._pin()
        async with self._call(), self._frames_as_errors():
            return await inner.run(**kwargs)

    async def begin_episode(self, **kwargs: Any) -> None:
        inner = await self._pin()
        async with self._call(), self._frames_as_errors():
            await inner.begin_episode(**kwargs)

    async def step(self, observation: Any, **kwargs: Any) -> Any:
        inner = await self._pin()
        async with self._call(), self._frames_as_errors():
            return await inner.step(observation, **kwargs)

    @contextlib.asynccontextmanager
    async def _frames_as_errors(self):
        """A raw error frame escaping a forwarded call becomes the policy's error."""
        try:
            yield
        except QuicRequestError as exc:
            deployment = _deployment_of(self._inner)  # before the shutdown detaches it
            await self._await_shutdown()
            raise (self._pinned_failure or server_frame_error(
                exc, model=self._model, deployment=deployment,
            )) from exc

    async def end_episode(self) -> None:
        if self._inner is None:
            return
        async with self._call():
            await self._inner.end_episode()

    async def push_history(self, observation: Any) -> None:
        inner = await self._pin()
        await inner.push_history(observation)

    @property
    def runtime_contract(self) -> RuntimeContract:
        inner = self._inner
        if inner is not None:
            return inner.runtime_contract
        return self._snapshot.get("runtime_contract") or runtime_contract_for_model(self._model)

    def __getattr__(self, name: str) -> Any:
        # Session attributes (session_id, region, transport_mode, runtime_stats, ...) follow
        # the current session; while released, the last session's values.
        if name.startswith("__"):
            raise AttributeError(name)
        inner = self.__dict__.get("_inner")
        if inner is not None:
            return getattr(inner, name)
        snapshot = self.__dict__.get("_snapshot", {})
        if name in snapshot:
            return snapshot[name]
        raise AttributeError(name)

    # ------------------------------------------------------------------ machine driver

    def _fire(self, event: Event) -> None:
        transition = self._machine.fire(event)
        self._changed.set()
        effect = transition.effect
        if effect is Effect.START_OPEN:
            self._task = asyncio.ensure_future(self._open_run())
        elif effect is Effect.ANNOUNCE_QUEUE:
            pass  # wait_until_ready prints the position; queue_position/eta are updated
        elif effect is Effect.ARM_IDLE:
            self._arm_idle()
        elif effect is Effect.SCHEDULE_RETRY:
            self._task = asyncio.ensure_future(self._retry_run())
        elif effect is Effect.LATCH_FAILURE:
            self._ready_cleared()
        elif effect is Effect.RELEASE_SESSION:
            inner, controller = self._detach_inner()
            self._teardown = asyncio.ensure_future(self._release_run(inner, controller))
        elif effect is Effect.DROP_SESSION:
            inner, controller = self._detach_inner()
            self._teardown = asyncio.ensure_future(self._drop_run(inner, controller))
        elif effect is Effect.SHUTDOWN:
            previous = self._teardown
            self._teardown = asyncio.ensure_future(self._shutdown_run(previous))
        if transition.state is State.CLOSED:
            self._ready_cleared()

    def _ready_cleared(self) -> None:
        self._cancel_idle()

    def _guard(self) -> None:
        if os.getpid() != self._pid:
            raise errors.catalog("forked_policy")
        if self._pinned_failure is not None:
            raise self._pinned_failure
        if self._machine.is_closed:
            if self._failure is not None:
                raise self._failure
            raise errors.catalog("policy_closed")

    def _latch(self, exc: BaseException) -> None:
        self._failure = exc

    @contextlib.asynccontextmanager
    async def _call(self):
        self._in_flight += 1
        try:
            yield
        finally:
            self._in_flight -= 1
            self._last_activity = self._clock()
            if self._in_flight == 0 and self._machine.is_ready:
                self._arm_idle()

    async def _ready_inner(self, deadline: float) -> Any:
        """The ready session, opening one when released; raises on a latched failure or
        when ``deadline`` passes first."""
        self._loop = asyncio.get_running_loop()
        self._waiters += 1
        try:
            while True:
                self._guard()
                if self._machine.state is State.READY and self._inner is not None:
                    return self._inner
                remaining = deadline - self._clock()
                if remaining <= 0:
                    raise errors.catalog("action_timeout", detail="the timeout")
                if self._machine.state is State.RELEASED:
                    if self._opened_once and remaining < MIN_OPEN_WINDOW_S:
                        # A reopen cannot finish in that time; don't start one.
                        raise errors.catalog("action_timeout", detail="the timeout")
                    self._fire(Event.OPEN)
                self._changed.clear()
                with contextlib.suppress(TimeoutError):
                    await asyncio.wait_for(self._changed.wait(), timeout=min(remaining, 1.0))
        finally:
            self._waiters -= 1
            self._abandon_open_if_unwanted()

    def _abandon_open_if_unwanted(self) -> None:
        """No session without a waiting caller: an open still in progress when the last
        caller gives up is cancelled (its cleanup deletes whatever was created)."""
        if self._caller_active():
            return
        if self._machine.state in (State.OPENING, State.QUEUED, State.RECONNECTING):
            task, self._task = self._task, None
            self._attempt = 0
            self._fire(Event.ABANDONED)
            if task is not None and not task.done() and task is not asyncio.current_task():
                task.cancel()
                self._abandoned.add(task)
                task.add_done_callback(self._abandoned.discard)

    async def _pin(self) -> Any:
        inner = await self._ready_inner(self._clock() + 3600.0)
        self._pinned = True
        self._cancel_idle()
        return inner

    async def _step(self, observation: Any, instruction: str, wait_deadline: float) -> Any:
        controller = self._controller
        if controller is None:
            return None
        try:
            async with self._call():
                await self._prepare_task(inner_for(controller), instruction)
                budget = max(0.0, wait_deadline - self._clock())
                step = await controller.step(
                    observation,
                    instruction=instruction,
                    timeout_s=budget,
                    wait_for_chunk=budget > 0.0,
                )
        except asyncio.CancelledError:
            if _cancelled_by_someone_else():
                return None  # a drop cancelled the shielded request; hold this tick
            raise
        except StaleFirstChunkError:
            raise  # already a dreamscale.Error (first_chunk_misaligned) with its fix
        except QuicRequestError as exc:
            if is_link_error(exc) or self._controller is not controller:
                return None
            # One failed refill must not kill a robot loop: hold (or keep waiting) and
            # request again on the next tick; three in a row with no chunk raise.
            controller.forget_request()
            self._error_frames += 1
            self._after_error_frame(inner_for(controller))
            if self._error_frames >= ERROR_FRAMES_BEFORE_RAISE:
                # Same path as exhausted reconnects: the policy closes with this failure
                # and every later call raises it, so a failing pool is never looped on.
                failure = repeated_frame_error(
                    exc, model=self._model, deployment=_deployment_of(inner_for(controller))
                )
                self._latch(failure)
                if self._machine.can(Event.REQUESTS_FAILED):
                    self._fire(Event.REQUESTS_FAILED)
                # The session's DELETE is in flight; a caller that exits right after this
                # raise (and the loop with it) must not strand it.
                teardown = self._teardown
                if teardown is not None and not teardown.done():
                    await _wait_quietly(teardown, timeout_s=DROP_CONFIRM_S + 5.0)
                raise failure from exc
            return None
        except BaseException as exc:
            if is_link_error(exc) or self._controller is not controller:
                return None
            raise
        if self._controller is not controller:
            return None  # the link was lost inside this step
        if not step.stalled:
            self._deadline_timeouts = 0
        if step.chunk_events:
            self._error_frames = 0  # a chunk arrived: the error-frame streak is over
        return step

    async def _prepare_task(self, inner: Any, instruction: str) -> None:
        """Prepare a new instruction on models that warm each one first (Isaac 0.5).

        The warm-up takes seconds on a fresh GPU; done as part of the first request, it
        reads as a stalled link (REQUEST_STALL_S) and the session is dropped. Prepared
        explicitly, it runs under the task's own timeout.
        """
        if inner is None or not getattr(inner, "requires_task_preparation", False):
            return
        prepared = self._prepared_task
        if prepared is not None and prepared[0] is inner and prepared[1] == instruction:
            return
        await inner.prepare(instruction=instruction)
        self._prepared_task = (inner, instruction)

    def _after_error_frame(self, inner: Any) -> None:
        """An error frame releases the session (confirmed DELETE); the next call opens a
        fresh one. Transports differ in what they do after a frame (the tunnel stops
        reading, the relay keeps the failed chunk cached), so the rule does not depend on
        them: identical behaviour on QUIC, the WebSocket tunnel and the relay."""
        if inner is None or inner is not self._inner or self._machine.state is not State.READY:
            return
        self._fire(Event.LINK_LOST)

    # -------------------------------------------------------------------- open path

    async def _open_run(self) -> None:
        try:
            await self._open_attempt()
        except asyncio.CancelledError:
            raise
        except BaseException as exc:  # a bug in the open path must surface, never hang
            if self._machine.state in (State.OPENING, State.QUEUED):
                self._latch(exc)
                self._fire(Event.OPEN_FAILED_FATAL)

    async def _open_attempt(self) -> None:
        teardown = self._teardown
        if teardown is not None and not teardown.done():
            await _wait_quietly(teardown, timeout_s=DROP_CONFIRM_S + 5.0)
        if self._machine.state is not State.OPENING:
            return
        if self._pending_drop_failure is not None:
            exc, self._pending_drop_failure = self._pending_drop_failure, None
            self._latch(exc)
            self._fire(Event.OPEN_FAILED_FATAL)
            return
        self._attempt += 1
        reopening = self._opened_once
        try:
            await self._respect_create_floor()
            self._last_create_at = self._clock()
            inner = await self._opener(
                on_progress=self._emit, on_session_status=self._on_session_status
            )
        except asyncio.CancelledError:
            raise
        except BaseException as exc:
            if self._machine.state not in (State.OPENING, State.QUEUED):
                return
            if is_retryable_open_error(exc):
                self._failure_candidate = exc
                self._fire(Event.OPEN_FAILED_RETRYABLE)
            else:
                self._latch(exc)
                self._fire(Event.OPEN_FAILED_FATAL)
            return
        if self._machine.state not in (State.OPENING, State.QUEUED) or not self._caller_active():
            # Closed, abandoned, or nobody is left waiting: a session nobody uses is closed.
            await self._close_unadopted(inner)
            if self._machine.state in (State.OPENING, State.QUEUED):
                self._attempt = 0
                self._fire(Event.ABANDONED)
            return
        try:
            profile, calibrated = await self._calibrate_at_open(inner, reopening=reopening)
        except asyncio.CancelledError:
            # Cancelled before adoption (startup timeout, Ctrl-C, close during a reopen):
            # the session would otherwise leak until the server's idle timeout.
            await self._close_unadopted(inner)
            raise
        except BaseException as exc:
            if not is_link_error(exc) and not isinstance(exc, QuicRequestError):
                # Calibration is an optimisation; it never fails a connect.
                self._emit(f"Calibration skipped: {type(exc).__name__}.")
                profile, calibrated = None, True
            else:
                # A link error or an error frame: this session is released like any
                # other that answered with a frame. Close it and try again (bounded).
                await self._close_unadopted(inner)
                if self._machine.state not in (State.OPENING, State.QUEUED):
                    return
                self._failure_candidate = exc
                self._fire(Event.OPEN_FAILED_RETRYABLE)
                return
        if self._machine.state not in (State.OPENING, State.QUEUED) or not self._caller_active():
            await self._close_unadopted(inner)
            if self._machine.state in (State.OPENING, State.QUEUED):
                self._attempt = 0
                self._fire(Event.ABANDONED)
            return
        self._adopt(inner, profile=profile, calibrated=calibrated)
        self._attempt = 0
        self._rate_limited_since = None
        self._opened_once = True
        self._fire(Event.SESSION_READY)
        if reopening:
            self._emit("Reconnected.")

    async def _close_unadopted(self, inner: Any) -> None:
        """Close a session that was opened but never served a caller (shielded, bounded:
        this runs on cancellation paths too)."""
        await _wait_quietly(inner.close(), timeout_s=DROP_CONFIRM_S)

    async def _calibrate_at_open(self, inner: Any, *, reopening: bool) -> tuple[Any, bool]:
        """Network calibration belongs to opening, never to a caller's tick budget.

        Returns (profile, calibrated): ``calibrated`` is False only for a robot kind this
        module cannot synthesise an observation for; the controller then calibrates on its
        first call, as before.
        """
        if reopening and self._calibration_profile is not None:
            inner._calibration_profile = self._calibration_profile
            return self._calibration_profile, True
        if getattr(inner.resolved_optimization_config, "calibration", "off") == "off":
            return None, True
        observation = synthetic_observation(self._model, inner.runtime_contract)
        if observation is None:
            return None, False
        # Calibration requests are marked is_calibration and carry no action history or
        # RTC reference actions, so nothing from them seeds the first real request.
        profile = await inner._calibrate(
            observation, instruction="calibration", timeout_s=self._request_stall_s
        )
        return profile, True

    def _caller_active(self) -> bool:
        """Someone is waiting for a session: a blocked caller, or a loop that called
        next_action within the last two seconds."""
        return self._waiters > 0 or self._clock() - self._last_call_at < 2.0

    async def _retry_run(self) -> None:
        exc = getattr(self, "_failure_candidate", None)
        if isinstance(exc, errors.DreamscaleError) and exc.code == "rate_limited":
            await self._wait_out_rate_limit(exc)
            return
        self._rate_limited_since = None
        if self._attempt >= MAX_OPEN_ATTEMPTS:
            self._latch(
                errors.catalog("gpu_unreachable", detail=str(exc) or None)
                if exc is not None
                else errors.catalog("gpu_unreachable")
            )
            self._failure.__cause__ = exc  # type: ignore[union-attr]
            self._fire(Event.ATTEMPTS_EXHAUSTED)
            return
        delay = retry_delay_s(self._attempt + 1, retry_after_s=getattr(exc, "retry_after_s", None))
        if delay > 0:
            await self._sleep(delay)
        self._retry_if_wanted()

    async def _wait_out_rate_limit(self, exc: errors.DreamscaleError) -> None:
        """A 429 is the control plane asking a fleet to slow down: wait as it says, without
        spending an attempt. A robot that waits too long reports it as what it is."""
        now = self._clock()
        if self._rate_limited_since is None:
            self._rate_limited_since = now
        if now - self._rate_limited_since >= RATE_LIMITED_GIVE_UP_S:
            self._rate_limited_since = None
            self._latch(exc)
            self._fire(Event.ATTEMPTS_EXHAUSTED)
            return
        self._attempt = max(0, self._attempt - 1)
        await self._sleep(rate_limited_delay_s(getattr(exc, "retry_after_s", None)))
        self._retry_if_wanted()

    def _retry_if_wanted(self) -> None:
        if self._machine.state is not State.RECONNECTING:
            return
        if self._caller_active():
            self._fire(Event.RETRY)
        else:
            # Nobody is waiting: sessions only open because of a user call.
            self._attempt = 0
            self._rate_limited_since = None
            self._fire(Event.ABANDONED)

    async def _respect_create_floor(self) -> None:
        if self._last_create_at is None:
            return
        wait = self._last_create_at + CREATE_FLOOR_S - self._clock()
        if wait > 0:
            await self._sleep(wait)

    def _on_session_status(self, session: Any) -> None:
        if getattr(session, "status", None) == "queued":
            self.queue_position = session.queue_position
            self.queue_eta_s = session.queue_eta_s
            if self._machine.can(Event.SERVER_QUEUED):
                self._fire(Event.SERVER_QUEUED)
        else:
            self.queue_position = None
            self.queue_eta_s = None

    def _adopt(self, inner: Any, *, profile: Any, calibrated: bool) -> None:
        inner.on_request_failure = lambda exc, session=inner: self._on_request_failure(
            exc, session
        )
        controller = AsyncActionController(
            policy=inner,
            strategy=RunStrategy(timeout_s=self._request_stall_s),
            skip_calibration=calibrated,
            anchor_first_chunk=True,
        )
        if profile is not None:
            inner._calibration_profile = profile
            controller._planner.seed_calibration(profile)
            self._calibration_profile = profile
        self._inner = inner
        self._controller = controller
        self._pinned = False
        self._deadline_timeouts = 0
        # Not the error-frame streak: it survives a reopen, so a pool that fails every
        # request cannot drive an endless release/reopen cycle.
        self._snapshot = {
            name: getattr(inner, name, None)
            for name in (
                "session_id", "region", "speed", "transport_mode", "action_hz",
                "native_action_hz", "chunk_size", "runtime_contract",
                "resolved_optimization_config", "runtime_stats", "context", "control",
                "deployment", "observation_history",
            )
        }

    def _detach_inner(self) -> tuple[Any, AsyncActionController | None]:
        inner, controller = self._inner, self._controller
        if inner is not None and getattr(inner, "_calibration_profile", None) is not None:
            self._calibration_profile = inner._calibration_profile
        self._inner = None
        self._controller = None
        self._cancel_idle()
        return inner, controller

    def _on_request_failure(self, exc: BaseException, session: Any) -> None:
        if session is not self._inner or self._machine.state is not State.READY:
            return  # a late failure from a session that is already gone
        if isinstance(exc, SendFloorTimeout):
            return  # the caller's budget ended before the send floor, not a stall
        if isinstance(exc, TimeoutError) and _USER_BOUND.get():
            return  # bounded by the caller's own deadline, not a stall
        if self._pinned and isinstance(exc, QuicRequestError) and not is_link_error(exc):
            # run()/prepare()/episodes: the frame ends this policy with its own error,
            # and the session (whose reader may have stopped) is deleted.
            failure = server_frame_error(exc, model=self._model)
            failure.info = errors.ErrorInfo(
                failure.info.code, failure.info.problem, failure.info.cause,
                closed_fix(failure.code, _deployment_of(self._inner)),
            )
            self._fail_pinned(failure)
            return
        if not is_link_error(exc):
            return
        if self._pinned:
            # Today's semantics for run/prepare/episodes: the next call raises. The dead
            # session is still closed so it stops counting toward the robot limit.
            failure = errors.catalog(
                "reconnect_failed",
                detail="the connection to the GPU dropped during run()/prepare()/an "
                "episode, which this policy does not resume",
            )
            failure.__cause__ = exc
            self._fail_pinned(failure)
            return
        self._fire(Event.LINK_LOST)

    def _fail_pinned(self, failure: errors.DreamscaleError) -> None:
        """A pinned session (run/prepare/episodes) that lost its link or got an error
        frame ends this policy: closed(failure), the dead session deleted."""
        self._pinned_failure = failure
        self._latch(failure)
        self._fire(Event.LINK_LOST)  # releases: classify + confirmed DELETE
        if self._machine.can(Event.DROP_FAILED):
            self._fire(Event.DROP_FAILED)  # released → closed(failure)

    # -------------------------------------------------------------------- idle

    def _arm_idle(self) -> None:
        if self._pinned or not self._machine.is_ready:
            return
        if self._idle_task is not None and not self._idle_task.done():
            return
        self._last_activity = self._clock()
        self._idle_task = asyncio.ensure_future(self._idle_run())

    def _idle_hold_s(self) -> float | None:
        """How long the session stays connected idle: its deployment's timed keep-warm
        (control planes that say so, on connect and on every heartbeat), None for always
        (no limit), else the one-minute release. close() and exit release it at once."""
        connection = getattr(self._inner, "_connection", None)
        latest = getattr(getattr(connection, "heartbeat", None), "latest", None)
        if isinstance(latest, dict):
            value = latest.get("deployment_keep_warm")
        else:
            value = getattr(getattr(connection, "session", None), "deployment_keep_warm", None)
        if value == "always":
            return None
        hold_s = KEEP_WARM_HOLD_S.get(value, 0.0) if isinstance(value, str) else 0.0
        return max(self._idle_release_s, hold_s)

    def _cancel_idle(self) -> None:
        task, self._idle_task = self._idle_task, None
        if task is not None and not task.done():
            task.cancel()

    def _busy(self) -> bool:
        if self._in_flight:
            return True
        controller = self._controller
        if controller is not None and controller.awaiting_chunk:
            return True
        inner = self._inner
        pending = getattr(inner, "_pending_chunk", None)
        if pending is not None and not pending.done():
            return True
        background = getattr(inner, "_background_tasks", None)
        return bool(background and any(not task.done() for task in background))

    async def _idle_run(self) -> None:
        """The idle clock starts when the last call completes and only runs with nothing
        in flight, background refills included. Its length follows the deployment's
        keep-warm, read again every window (heartbeats refresh it)."""
        poll_s = min(1.0, self._idle_release_s / 4.0)
        while True:
            hold_s = self._idle_hold_s()
            if hold_s is None:
                # Kept warm always: held while the code holds the policy.
                await self._sleep(self._idle_release_s)
                continue
            remaining = self._last_activity + hold_s - self._clock()
            if remaining > 0:
                await self._sleep(min(remaining, self._idle_release_s))
                continue
            if self._busy():
                # Something is still in flight: the window restarts when it lands.
                self._last_activity = self._clock()
                await self._sleep(poll_s)
                continue
            break
        if self._machine.can(Event.IDLE_ELAPSED) and not self._pinned:
            self._fire(Event.IDLE_ELAPSED)

    # -------------------------------------------------------------------- teardown

    async def _release_run(self, inner: Any, controller: AsyncActionController | None) -> None:
        """Idle: the normal close (detach when the session keeps its server warm, else
        delete), bounded. If it did not go through, confirm the DELETE so the next open starts
        from a clean cap. (On a deployment kept warm the idle window is its keep-warm: see
        _idle_run.)"""
        if controller is not None:
            with contextlib.suppress(Exception):
                await controller.close()
        if inner is None:
            return
        connection = inner._connection
        try:
            await asyncio.wait_for(inner.close(), timeout=DROP_CONFIRM_S)
        except (TimeoutError, Exception):
            if not getattr(connection, "keep_warm", 0):
                await self._confirm_delete(connection.client, inner.session_id)
            with contextlib.suppress(Exception):
                await connection.client.close()

    async def _drop_run(self, inner: Any, controller: AsyncActionController | None) -> None:
        """Close-then-open, confirmed: classify the lost session, then delete it until the
        control plane says so. The next user call opens a new one."""
        if controller is not None:
            with contextlib.suppress(Exception):
                await controller.close()
        failure: BaseException | None = None
        if inner is not None:
            connection = inner._connection
            reports = getattr(connection, "transport_reports", None)
            if reports is not None:
                reports.mute()  # "QUIC path lost" would mislead: the line below says what did
            client, session_id = connection.client, inner.session_id
            lost = await self._lost_session(client, session_id)
            if getattr(lost, "reason", None) == "quota_exhausted":
                failure = errors.catalog("insufficient_credits")
            else:
                self._emit(
                    lost_session_line(lost, inner.runtime_contract, holding=controller is not None),
                    always=True,
                )
            if failure is None and not await self._confirm_delete(client, session_id):
                failure = errors.catalog(
                    "reconnect_failed",
                    detail="the lost session could not be closed in time (it may still count "
                    "toward your organization's robot limit for a minute)",
                )
            # The session is deleted; release the local resources without a second
            # DELETE (or a detach) from the connection's own close.
            cleanups = (connection.heartbeat.stop(), connection.transport.close(), client.close())
            for cleanup in cleanups:
                with contextlib.suppress(Exception):
                    await asyncio.wait_for(cleanup, timeout=2.0)
            connection.closed = True
            with contextlib.suppress(Exception):
                await asyncio.wait_for(inner.close(), timeout=5.0)
        if failure is not None:
            if self._machine.state is State.RELEASED:
                self._latch(failure)
                self._fire(Event.DROP_FAILED)
            elif self._machine.state in (State.OPENING, State.QUEUED, State.RECONNECTING):
                self._pending_drop_failure = failure

    async def _lost_session(self, client: Any, session_id: str) -> Any | None:
        """The control plane's view of a session whose link was lost (None if unreachable)."""
        try:
            return await asyncio.wait_for(client.get_session(session_id), CLASSIFY_TIMEOUT_S)
        except Exception:
            return None

    async def _confirm_delete(self, client: Any, session_id: str) -> bool:
        deadline = self._clock() + DROP_CONFIRM_S
        while True:
            try:
                await asyncio.wait_for(
                    client.delete_session(session_id),
                    timeout=max(0.5, deadline - self._clock()),
                )
                return True  # 2xx or 404: the control plane no longer counts it
            except errors.AuthError:
                return True  # the key is gone; nothing we can close
            except Exception:
                if self._clock() >= deadline:
                    return False
                await self._sleep(min(1.0, DROP_CONFIRM_S / 5.0))

    async def _shutdown_run(self, previous: asyncio.Task[Any] | None) -> None:
        self._cancel_idle()
        if previous is not None and not previous.done():
            # A release or drop in progress still has to confirm its DELETE.
            await _wait_quietly(previous, timeout_s=DROP_CONFIRM_S + 5.0)
        task, self._task = self._task, None
        if task is not None and not task.done() and task is not asyncio.current_task():
            task.cancel()
            await _wait_quietly(task, timeout_s=DROP_CONFIRM_S + 5.0)
        # Opens abandoned earlier are still deleting what they created.
        for abandoned in list(self._abandoned):
            if not abandoned.done():
                await _wait_quietly(abandoned, timeout_s=DROP_CONFIRM_S + 5.0)
        inner, controller = self._detach_inner()
        if controller is not None:
            with contextlib.suppress(Exception):
                await controller.close()
        if inner is not None:
            try:
                await asyncio.wait_for(inner.close(), timeout=DROP_CONFIRM_S)
            except (TimeoutError, Exception) as exc:
                connection = inner._connection
                if getattr(connection, "keep_warm", 0) or not await self._confirm_delete(
                    connection.client, inner.session_id
                ):
                    raise
                log.debug("session %s closed on retry after %r", inner.session_id, exc)

    async def _await_shutdown(self) -> None:
        teardown = self._teardown
        if teardown is not None and not teardown.done():
            await _wait_quietly(teardown, timeout_s=DROP_CONFIRM_S + 5.0)
        for abandoned in list(self._abandoned):
            if not abandoned.done():
                await _wait_quietly(abandoned, timeout_s=DROP_CONFIRM_S + 5.0)

    def _close_at_exit(self) -> None:
        loop = self._loop
        loop_alive = loop is not None and loop.is_running() and not loop.is_closed()
        if self._machine.is_closed:
            if loop_alive:
                asyncio.run_coroutine_threadsafe(self._await_shutdown(), loop).result(
                    timeout=20.0
                )
            return
        if loop_alive:
            asyncio.run_coroutine_threadsafe(self.close(), loop).result(timeout=20.0)
            return
        inner = self._inner
        self._machine.state = State.CLOSED
        if inner is not None:
            _release_blocking(inner)

    def _emit(self, line: str, *, always: bool = False) -> None:
        if self._progress is None:
            return
        if line.startswith("Run summary:") and not self._closing:
            return
        reopening = self._machine.state in (State.OPENING, State.QUEUED, State.RECONNECTING)
        if self._opened_once and reopening and not always:
            # Reopen: only the queue and why it waits (a server starting in the next-closest
            # region, a training run making room) matter to the user; the rest is one
            # "Reconnected."
            if not (line.startswith(("Waiting for", "✗"))
                    or any(why in line for why in _REOPEN_WAIT_NOTES)):
                return
        self._progress(line)


# Why a reopen waits, from the control plane's starting_note: said even while reopening.
_REOPEN_WAIT_NOTES = ("next-closest region", "making room")


# Statuses of a session the control plane ended: its server stopped (a restart, a lost unit) or
# the session closed. Any other answer (still ready, or none) means the robot's link failed.
_ENDED_STATUSES = ("closed", "failed", "expired")


def lost_session_line(session: Any | None, contract: RuntimeContract, *, holding: bool) -> str:
    """What the robot's terminal hears when a session's link is lost: whether its server
    stopped (a new one starts) or the connection dropped, and, under next_action(), what the
    arm does meanwhile. The queue line that follows gives the estimate."""
    if getattr(session, "reason", None) == "idle_timeout":
        line = "The session closed while idle; starting a new one"
    elif getattr(session, "status", None) in _ENDED_STATUSES:
        line = "The server running this session stopped; starting a new one"
    else:
        line = "Lost the connection to the server; reconnecting"
    if not holding:
        return line + "."
    if hold_rule(contract) == HOLD_WAIT:
        return line + " (next_action() waits for it)."
    return line + " (the arm holds still until it's back)."


def _release_blocking(inner: Any) -> None:
    """Best-effort close of a session from atexit, where the event loop is gone."""
    connection = getattr(inner, "_connection", None)
    client = getattr(getattr(connection, "client", None), "_client", None)
    session_id = getattr(inner, "session_id", None)
    if client is None or session_id is None:
        return
    base = str(client.base_url).rstrip("/")
    headers = {"Authorization": client.headers.get("authorization", "")}
    with contextlib.suppress(Exception):
        if getattr(connection, "keep_warm", 0):
            httpx.post(f"{base}/v1/sessions/{session_id}/detach", headers=headers, timeout=5.0)
        else:
            httpx.delete(f"{base}/v1/sessions/{session_id}", headers=headers, timeout=5.0)


class Policy:
    """What ``dreamscale.connect`` returns: ``AsyncPolicy`` driven from a worker loop."""

    def __init__(self, *, runner: _LoopRunner, async_policy: AsyncPolicy) -> None:
        self._runner = runner
        self._facade = async_policy
        self._pid = os.getpid()
        self.last_run_result: Any = None
        _OPEN_POLICIES.add(self)

    @property
    def model(self) -> str:
        return self._facade.model

    @property
    def state(self) -> str:
        return self._facade.state

    @property
    def contract(self) -> PolicyContract:
        return self._facade.contract

    def _guard(self) -> None:
        if os.getpid() != self._pid:
            raise errors.catalog("forked_policy")

    def predict(
        self,
        observation: ObservationLike,
        instruction: str | None = None,
        *,
        timeout_s: float = DEFAULT_PREDICT_TIMEOUT_S,
        past_observations: Sequence[ObservationLike] | None = None,
        action_history: Sequence[Sequence[float]] | None = None,
        committed_actions: Sequence[Sequence[float]] | None = None,
    ) -> ActionChunkResult:
        self._guard()
        return self._runner.run(
            self._facade.predict(
                observation, instruction, timeout_s=timeout_s,
                past_observations=past_observations, action_history=action_history,
                committed_actions=committed_actions,
            )
        )

    def next_action(
        self,
        observation: ObservationLike,
        instruction: str | None = None,
        *,
        pace: bool = True,
        timeout_s: float | None = None,
    ) -> tuple[float, ...]:
        self._guard()
        return self._runner.run(
            self._facade.next_action(observation, instruction, pace=pace, timeout_s=timeout_s)
        )

    def prefetch(
        self,
        observation: ObservationLike,
        instruction: str | None = None,
        *,
        timeout_s: float = DEFAULT_PREDICT_TIMEOUT_S,
    ) -> None:
        """See ``AsyncPolicy.prefetch``."""
        self._guard()
        self._runner.run(self._facade.prefetch(observation, instruction, timeout_s=timeout_s))

    def prepare(self, *, instruction: str, timeout_s: float | None = None) -> None:
        """See ``AsyncPolicy.prepare`` (the pinned run API; ``prefetch`` for next_action)."""
        self._guard()
        self._runner.run(self._facade.prepare(instruction=instruction, timeout_s=timeout_s))

    def begin_episode(self, **kwargs: Any) -> None:
        self._runner.run(self._facade.begin_episode(**kwargs))

    def step(self, observation: Any, **kwargs: Any) -> Any:
        return self._runner.run(self._facade.step(observation, **kwargs))

    def end_episode(self) -> None:
        self._runner.run_cleanup(self._facade.end_episode())

    def run(self, **kwargs: Any) -> Any:
        from dreamscale.policy.remote import _sync_run

        self._guard()
        require_run_hold(self._facade.runtime_contract)
        self._runner.run(self._facade._pin())
        return _sync_run(self, **kwargs)

    @property
    def _async_policy(self) -> Any:
        """The current inner session (for the shared synchronous run loop)."""
        return self._facade._inner

    def close(self) -> None:
        _OPEN_POLICIES.discard(self)
        if os.getpid() != self._pid:
            # A forked child has no loop thread: close its handle only, never block.
            self._facade._machine.state = State.CLOSED
            _OPEN_POLICIES.discard(self._facade)
            return
        try:
            self._runner.run_cleanup(self._facade.close())  # also drains a pending DELETE
        finally:
            self._runner.shutdown()

    def _close_at_exit(self) -> None:
        if self._runner._thread.is_alive():
            with contextlib.suppress(Exception):
                self.close()
                return
        self._facade._close_at_exit()

    def __enter__(self) -> Policy:
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()

    def __getattr__(self, name: str) -> Any:
        if name.startswith("__"):
            raise AttributeError(name)
        facade = self.__dict__.get("_facade")
        if facade is None:
            raise AttributeError(name)
        return getattr(facade, name)


# ------------------------------------------------------------------------ public entry

_DEFAULT_PROGRESS = object()
# Accepted for compatibility with a102/a103 code and the CLI; absent from the documented
# signature. Each keeps today's behaviour.
LEGACY_CONNECT_KWARGS = frozenset(
    {
        "acceleration", "control", "rtc", "calibration", "region", "provider", "speed",
        "idle_timeout", "keep_warm", "startup_timeout", "transport", "control_hz",
        "deployment", "endpoint", "context", "optimization_config", "steady_send",
    }
)


def _resolve_progress(on_progress: Any) -> Callable[[str], None] | None:
    if on_progress is _DEFAULT_PROGRESS:
        return default_progress()
    if on_progress is print:
        from dreamscale.terminal import make_progress_printer

        return make_progress_printer()
    return on_progress


def _check_legacy_kwargs(legacy: dict[str, Any]) -> None:
    unknown = sorted(set(legacy) - LEGACY_CONNECT_KWARGS)
    if unknown:
        raise TypeError(f"connect() got an unexpected keyword argument {unknown[0]!r}")


async def aconnect(
    model: str,
    *,
    deployment: str | None = None,
    checkpoint: str | None = None,
    api_key: str | None = None,
    on_progress: Any = _DEFAULT_PROGRESS,
    **legacy: Any,
) -> AsyncPolicy:
    """Connect to a model. Returns once the session is ready (the queue position shows
    while it waits). A deployment runs by its name, ``connect("<account>/<slug>")`` (or just
    its slug), on the model it was built on; ``deployment=`` (its name or ``ckpt_…`` ID) does
    the same beside the base model, and ``checkpoint=`` is its older name. Auth comes from
    ``api_key=``, ``DREAMSCALE_API_KEY`` or ``dreamscale login``."""
    from dreamscale.policy.remote import _aconnect

    _check_legacy_kwargs(legacy)
    # A public name (pi0.5-bimanualyam) or the internal id; the SDK keys on the latter.
    model = internal_model(model)
    progress = _resolve_progress(on_progress)
    startup_timeout = legacy.get("startup_timeout")

    async def opener(*, on_progress: Any, on_session_status: Any) -> Any:
        return await _aconnect(
            model,
            on_progress=on_progress,
            on_session_status=on_session_status,
            **({"deployment": deployment} if deployment is not None else {}),
            **({"checkpoint": checkpoint} if checkpoint is not None else {}),
            **({"api_key": api_key} if api_key is not None else {}),
            **legacy,
        )

    policy = AsyncPolicy(model=model, opener=opener, progress=progress)
    try:
        await policy._ready_inner(
            policy._clock() + (float(startup_timeout) if startup_timeout else 7200.0)
        )
    except BaseException:
        with contextlib.suppress(Exception):
            await policy.close()
        raise
    return policy


def connect(
    model: str,
    *,
    deployment: str | None = None,
    checkpoint: str | None = None,
    api_key: str | None = None,
    on_progress: Any = _DEFAULT_PROGRESS,
    **legacy: Any,
) -> Policy:
    """Connect to a model (synchronous). See ``aconnect``."""
    _check_legacy_kwargs(legacy)
    runner = _LoopRunner()
    try:
        async_policy = runner.run(
            aconnect(
                model, deployment=deployment, checkpoint=checkpoint, api_key=api_key,
                on_progress=on_progress, **legacy,
            )
        )
    except BaseException:
        runner.shutdown()
        raise
    return Policy(runner=runner, async_policy=async_policy)
