"""SkyRL's live samples (rl-next W37): every input row of a `generate()` call starts as the call enters, keyed
`{call}:{instance}:{repetition}` (its rows' `attempt_key`); each model call of its agent loop is progress; it ends when
its loop returns (else with the call), graded as its rows are. A Harbor generator's tries are live samples keyed by
`TrialResult.id`. No command: `COMMAND_REFUSAL`. Duck-typed on SkyRL (`NovaSky-AI/SkyRL@d87004689e3a`). Why: DESIGN.md
"Live samples"."""

from __future__ import annotations

import contextvars
import functools
from collections.abc import Mapping, Sequence
from typing import Any

from probe.generated.samples import AttemptPhase

from .. import _rl_owner
from .._live import LiveAttempts
from .outputs import OutputMapper, get_identity, make_live_key, read_reward

#: The refusal the server answers a cancel, retry or watch of a SkyRL sample with (the W30 spike, S2).
COMMAND_REFUSAL = "SkyRL retries a failed trial and masks its prompt group"
#: `SkyRLGymGenerator.agent_loop` runs one trajectory (`skyrl_gym_generator.py:332`); its model calls go through
#: `inference_engine_client.generate` (`:480`, `inference_servers/base.py:71`).
AGENT_LOOP = "agent_loop"
CLIENT_GENERATE = "generate"

#: A Harbor try's phases as progress: (Harbor's `TrialEvent` name, the phase, the activity line).
_TRY_PHASES = (("ENVIRONMENT_START", AttemptPhase.ENVIRONMENT, "environment starting"),
               ("AGENT_START", AttemptPhase.GENERATING, "agent running"),
               ("VERIFICATION_START", AttemptPhase.SCORING, "verifying"))
#: The generate call a trajectory's loop runs in (its live keys' first part), and the trajectory's own live key.
_CALL: contextvars.ContextVar[int | None] = contextvars.ContextVar("probe_skyrl_call", default=None)
_KEY: contextvars.ContextVar[str | None] = contextvars.ContextVar("probe_skyrl_live_key", default=None)


class SkyrlLive:
    """One SkyRL training process's live samples, written as its producer (`skyrl`)."""

    def __init__(self, samples: Any, mapper: OutputMapper, guard: _rl_owner.HookGuard) -> None:
        self.attempts = LiveAttempts(samples)
        self._mapper = mapper
        self._guard = guard
        self._turns: dict[str, int] = {}

    # -- a generate call -----------------------------------------------------------------------------------
    def start_call(self, inputs: Mapping[str, Any], call_id: int, version: int | None,
                   scheduled_step: int | None) -> list[str]:  # fmt: skip
        """The call's input rows as live samples, in one write. Returns their keys."""
        starts = self._mapper.map_starts(inputs, call_id=call_id, version=version, scheduled_step=scheduled_step)
        return self.attempts.start(starts)

    def enter_call(self, call_id: int) -> contextvars.Token:
        """The loops this call's tasks run know their call (a task copies the context it is made in)."""
        return _CALL.set(call_id)

    def exit_call(self, token: contextvars.Token) -> None:
        _CALL.reset(token)

    def end_rows(self, parts: Sequence[Mapping[str, Any]], keys: Sequence[str]) -> None:
        """The call returned: each sample a loop did not end yet ends graded as its rows are (a step-wise trajectory's
        rows all carry its grade); a key with no row ends `ungraded`."""
        ends: dict[str, dict] = {}
        for part in parts:
            key = part.get("attempt_key")
            if key in ends or key not in keys:
                continue
            is_error = part.get("error_reason") is not None
            end: dict[str, Any] = {"key": key, "outcome": self.attempts.get_outcome(part.get("reward"), is_error=is_error)}
            if is_error:
                end.update(error_reason=part["error_reason"], error_message=part.get("error_message"))
            ends[key] = end
        rest = [{"key": key, "outcome": self.attempts.get_outcome(None)} for key in keys if key not in ends]
        self.attempts.end([*ends.values(), *rest])

    def end_error(self, keys: Sequence[str], error: BaseException) -> None:
        self.attempts.end_error(keys, error)

    # -- a trajectory's loop and its model calls -----------------------------------------------------------
    def wrap_loop(self, generator: Any) -> None:
        """``generator.agent_loop`` on this instance: its trajectory's sample ends when it returns, and each model
        call inside it is progress (``generator.inference_engine_client.generate``)."""
        loop = getattr(generator, AGENT_LOOP, None)
        if not callable(loop):
            return

        @functools.wraps(loop)
        async def call_agent_loop(*args: Any, **kwargs: Any) -> Any:
            call_id, trajectory = _CALL.get(), kwargs.get("trajectory_id")
            identity = get_identity(trajectory) if call_id is not None else None
            key = make_live_key(call_id, *identity) if identity is not None else None
            token = _KEY.set(key)
            try:
                output = await loop(*args, **kwargs)
            except BaseException as exc:
                if key is not None:
                    self._guard.call("a live sample", self.attempts.end_error, [key], exc)
                raise
            finally:
                _KEY.reset(token)
                self._turns.pop(key, None)
            if key is not None:
                self._guard.call("a live sample", self._end_loop, key, output)
            return output

        object.__setattr__(generator, AGENT_LOOP, call_agent_loop)
        client = getattr(generator, "inference_engine_client", None)
        if client is not None:
            self._guard.call("the model calls", self._wrap_client, client)

    def _wrap_client(self, client: Any) -> None:
        generate = getattr(client, CLIENT_GENERATE)

        @functools.wraps(generate)
        async def call_client_generate(*args: Any, **kwargs: Any) -> Any:
            key = _KEY.get()
            if key is None:
                return await generate(*args, **kwargs)
            number = self._turns.get(key, 0) + 1
            self._guard.call("a live sample", self.attempts.send_progress, [key], phase=AttemptPhase.GENERATING,
                             turns=number - 1, activity=f"model call {number}")
            output = await generate(*args, **kwargs)
            self._turns[key] = number
            self._guard.call("a live sample", self.attempts.send_progress, [key], phase=AttemptPhase.ENVIRONMENT,
                             turns=number, activity=f"model replied ({_get_stop_reason(output)})")
            return output

        object.__setattr__(client, CLIENT_GENERATE, call_client_generate)

    def _end_loop(self, key: str, output: Any) -> None:
        """A loop's output (`TrajectoryOutput`, or a step-wise `StepWiseOutput` graded by its last step,
        `skyrl_gym_generator.py:55-87`): its reward, or `stop_reason=error` (not graded)."""
        steps = getattr(output, "step_outputs", None)
        last = steps[-1] if isinstance(steps, list) and steps else output
        is_error = getattr(last, "stop_reason", None) == "error"
        reward, _ = read_reward(getattr(last, "reward", None))
        end: dict[str, Any] = {"key": key, "outcome": self.attempts.get_outcome(reward, is_error=is_error)}
        if is_error:
            end.update(error_reason="unknown", error_message="SkyRL stop_reason=error")
        self.attempts.end([end])

    # -- a Harbor try (`harbor.HarborJoin`) ----------------------------------------------------------------
    def watch_try(self, trial: Any, hook: Any) -> None:
        """One Harbor trial SkyRL's Harbor generator made: a live sample keyed by its `TrialResult.id` from START, its
        phases as progress, its end graded as Harbor's own part (``hook``, Probe's trial hook, whose END ran first)."""
        from harbor.trial.hooks import TrialEvent

        trial.add_hook(TrialEvent.START, self._make_hook(self._start_try))
        for name, phase, activity in _TRY_PHASES:
            event = getattr(TrialEvent, name, None)  # each of Harbor's own events (`trial/hooks.py:17-26`)
            if event is not None:
                trial.add_hook(event, self._make_hook(self._send_try_progress, phase, activity))
        trial.add_hook(TrialEvent.END, self._make_hook(self._end_try, hook))

    def _make_hook(self, handle: Any, *extra: Any) -> Any:
        """A Harbor trial hook that never raises: Harbor passes a hook's exception into the trial (`trial.py:597-606`)."""

        async def call_hook(event: Any) -> None:
            self._guard.call("a live Harbor try", handle, event, *extra)

        return call_hook

    def _start_try(self, event: Any) -> None:
        from probe.connectors.harbor.samples import build_scenario, build_task_key, get_attempt_key, read_event

        result, lock = read_event(event)
        start = {"key": get_attempt_key(result), "task_key": build_task_key(result, lock),
                 "scenario": build_scenario(result, lock, {}), **self._mapper.where}
        self.attempts.start([start])

    def _send_try_progress(self, event: Any, phase: AttemptPhase, activity: str) -> None:
        self.attempts.send_progress([str(event.result.id)], phase=phase, activity=activity)

    def _end_try(self, event: Any, hook: Any) -> None:
        """Graded by Harbor's own verifier (its valid grade; SkyRL's rows carry the reward the trainer uses), broken
        when Probe's Harbor part names why."""
        attempt = getattr(hook, "attempt", None)
        head = attempt.parts[0] if attempt is not None and attempt.parts else {}
        is_error = head.get("error_reason") is not None or getattr(event.result, "exception_info", None) is not None
        end: dict[str, Any] = {"key": str(event.result.id),
                               "outcome": self.attempts.get_outcome(_read_grade(event), is_error=is_error)}
        if is_error:
            end.update(error_reason=head.get("error_reason") or "unknown", error_message=head.get("error_message"))
        self.attempts.end([end])


def _read_grade(event: Any) -> float | None:
    """A Harbor trial's valid grade at its END (the connector's own reading), else None: a result Probe cannot read
    still ends its sample, `ungraded`."""
    from probe.connectors.harbor.samples import read_event, read_rewards

    try:
        is_valid, grade, _ = read_rewards(read_event(event)[0])
    except Exception:  # noqa: BLE001 -- fail open: the try still ends
        return None
    return grade if is_valid else None


def _get_stop_reason(output: Any) -> str:
    """An `InferenceEngineOutput`'s first stop reason (one prompt per agent-loop call)."""
    reasons = output.get("stop_reasons") if isinstance(output, Mapping) else None
    return str(reasons[0]) if isinstance(reasons, list) and reasons else "done"
