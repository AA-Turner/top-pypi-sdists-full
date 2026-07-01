"""In-process rollout helpers that compose ``Capability × Environment``.

This module is used by both hosted training jobs (running inside the training
sandbox) and SDK-direct training (running in the user's own Python process).
It mirrors the shape ``CapabilityEnvAdapter.evaluate()`` already ships for
optimization (``packages/sdk/dreadnode/optimization/adapters/env.py``), minus
optimization-specific candidate bookkeeping.

Exports:

- :func:`batched_environments` — async context manager that provisions a
  batch of ``TaskEnvironment`` concurrently (capped by a semaphore) and tears
  them down on exit, with failure-resilient cleanup.
- :func:`verify_env_state` — dispatches a task's ``verification`` dict against
  a live env. Handles ``env_flag``, ``env_script``, and ``llm_judge`` methods.
- :class:`VerificationResult` — ``(passed, score, metrics)`` container
  returned by ``verify_env_state``.

The ``trajectory_to_tinker_datums`` helper planned in TRAINING.MD lives in
:mod:`dreadnode.training.jobs` today (alongside the Worlds rollout path) and
will be extracted into this module in a follow-up refactor.
"""

import asyncio
import hashlib
import typing as t
from contextlib import asynccontextmanager
from dataclasses import dataclass, field

from loguru import logger

from dreadnode.core.environment import TaskEnvironment

if t.TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from dreadnode.agents.trajectory import Trajectory


# ---------------------------------------------------------------------------
# batched_environments
# ---------------------------------------------------------------------------


@asynccontextmanager
async def batched_environments(
    envs: list[TaskEnvironment],
    *,
    max_concurrent_setup: int = 32,
) -> "AsyncIterator[list[TaskEnvironment]]":
    """Provision a batch of envs in parallel; tear them all down on exit.

    Caps concurrent setup via a semaphore so a 64-rollout RL step doesn't
    pummel the sandbox provider at batch boundaries. Envs that fail ``setup()``
    are logged and excluded from the yielded list; their ``teardown()`` is
    *not* called (nothing to tear down). Envs that succeeded setup are always
    torn down on exit — even if the caller raises inside the ``async with``
    block.

    Args:
        envs: Pre-constructed ``TaskEnvironment`` instances. They must not
            already be set up (``setup()`` is called by this context manager).
        max_concurrent_setup: Maximum concurrent ``setup()`` calls. Defaults
            to 32; tune down under tight provider quota.

    Yields:
        The live envs (those that succeeded ``setup()``), in the input order
        with failed envs skipped.

    Example::

        envs = [
            TaskEnvironment(api_client=api, org=ORG, workspace=WS,
                            task_ref="pwn/flag", inputs=row.get("inputs"))
            for row in batch_rows
        ]
        async with batched_environments(envs, max_concurrent_setup=8) as live:
            rewards = await asyncio.gather(*[score(env) for env in live])
    """

    if max_concurrent_setup <= 0:
        raise ValueError(
            f"max_concurrent_setup must be positive (got {max_concurrent_setup})"
        )

    semaphore = asyncio.Semaphore(max_concurrent_setup)

    async def _guarded_setup(env: TaskEnvironment) -> bool:
        async with semaphore:
            try:
                await env.setup()
            except Exception:
                logger.exception(
                    "Env setup failed for task_ref={}; excluding from batch",
                    env.task_ref,
                )
                return False
            return True

    results = await asyncio.gather(*[_guarded_setup(e) for e in envs])
    live = [env for env, ok in zip(envs, results, strict=True) if ok]
    try:
        yield live
    finally:
        await asyncio.gather(
            *[env.teardown() for env in live],
            return_exceptions=True,
        )


# ---------------------------------------------------------------------------
# verify_env_state
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class VerificationResult:
    """Outcome of grading a rollout against a task's ``verification`` config.

    Attributes:
        passed: Whether the task was considered solved.
        score: Scalar in ``[0, 1]``. For binary env_flag / env_script this is
            ``1.0`` on pass and ``0.0`` on fail. For ``llm_judge`` this is the
            judge's rubric score.
        metrics: Free-form metadata attached to traces and training metrics
            (``method``, ``exit_code``, judge ``reason`` and attributes, …).
    """

    passed: bool
    score: float
    metrics: dict[str, t.Any] = field(default_factory=dict)


async def verify_env_state(
    env: TaskEnvironment,
    trajectory: "Trajectory | None",
    verification: dict[str, t.Any] | None,
    *,
    judge_context: dict[str, t.Any] | None = None,
) -> VerificationResult:
    """Grade the rollout against the task's verification config.

    Supports three dispatch keys on the ``verification`` dict:

    - ``env_flag`` — read a file from the env sandbox; compare against a
      sha256 hash (``hash``) or plaintext ``expected`` value.
    - ``env_script`` — execute a script inside the env; pass iff the exit
      code matches ``expected_exit_code`` (default 0).
    - ``llm_judge`` — score ``trajectory`` with :class:`~dreadnode.agents.AgentJudge`
      against a rubric; pass iff score clears ``passing_threshold``.

    Args:
        env: A provisioned :class:`TaskEnvironment` with ``execute()`` available.
        trajectory: The agent's rollout. Required for ``llm_judge``; ignored
            by ``env_flag`` / ``env_script``. Pass ``None`` for single-shot
            recipes that don't produce a trajectory.
        verification: The task's verification config (typically from
            ``env.task_verification``). ``None`` or missing ``method`` raises
            ``ValueError``.
        judge_context: Optional context passed through to ``AgentJudge.evaluate``
            when ``method=llm_judge``. Good for task instruction / env state.

    Returns:
        A :class:`VerificationResult`.

    Raises:
        ValueError: if ``verification`` is missing, method is unknown, or the
            chosen method's required fields are absent.
        RuntimeError: if ``env_flag`` / ``env_script`` invocation is attempted
            against an un-provisioned env (caller must ``setup()`` first).
    """

    if not isinstance(verification, dict):
        raise ValueError(
            "verify_env_state requires a verification dict; got "
            f"{type(verification).__name__}"
        )

    method = verification.get("method")
    if not isinstance(method, str) or not method:
        raise ValueError(
            "verification dict is missing 'method' (expected env_flag, "
            "env_script, or llm_judge)"
        )

    if method == "env_flag":
        return await _verify_env_flag(env=env, verification=verification)
    if method == "env_script":
        return await _verify_env_script(env=env, verification=verification)
    if method == "llm_judge":
        return await _verify_llm_judge(
            trajectory=trajectory,
            verification=verification,
            judge_context=judge_context,
        )

    raise ValueError(
        f"Unsupported verification method {method!r}. Expected one of: "
        "env_flag, env_script, llm_judge."
    )


async def _verify_env_flag(
    *,
    env: TaskEnvironment,
    verification: dict[str, t.Any],
) -> VerificationResult:
    flag_path = verification.get("flag_path", "/tmp/flag")
    if not isinstance(flag_path, str) or not flag_path:
        raise ValueError("env_flag verification requires a non-empty 'flag_path'")
    timeout_sec = int(verification.get("timeout_sec", 10))

    exit_code, output = await env.execute(
        f"cat {flag_path}",
        timeout_sec=timeout_sec,
    )
    if exit_code != 0:
        return VerificationResult(
            passed=False,
            score=0.0,
            metrics={
                "method": "env_flag",
                "reason": "flag_read_failed",
                "exit_code": exit_code,
                "flag_path": flag_path,
            },
        )

    actual = output.strip()
    expected_hash = verification.get("hash")
    expected_plain = verification.get("expected")

    if isinstance(expected_hash, str) and expected_hash:
        digest = f"sha256:{hashlib.sha256(actual.encode()).hexdigest()}"
        passed = digest == expected_hash
        return VerificationResult(
            passed=passed,
            score=1.0 if passed else 0.0,
            metrics={
                "method": "env_flag",
                "match_kind": "hash",
                "flag_path": flag_path,
            },
        )
    if isinstance(expected_plain, str):
        passed = actual == expected_plain
        return VerificationResult(
            passed=passed,
            score=1.0 if passed else 0.0,
            metrics={
                "method": "env_flag",
                "match_kind": "exact",
                "flag_path": flag_path,
            },
        )

    raise ValueError(
        "env_flag verification requires either 'hash' (sha256:…) or 'expected' "
        "(plaintext). Got neither."
    )


async def _verify_env_script(
    *,
    env: TaskEnvironment,
    verification: dict[str, t.Any],
) -> VerificationResult:
    script_path = verification.get("script_path")
    if not isinstance(script_path, str) or not script_path:
        raise ValueError("env_script verification requires a 'script_path' string")

    expected_exit_code = int(verification.get("expected_exit_code", 0))
    timeout_sec = int(verification.get("timeout_sec", 30))

    exit_code, output = await env.execute(script_path, timeout_sec=timeout_sec)
    passed = exit_code == expected_exit_code
    # Cap the output in metrics so we don't log megabytes of script stdout.
    tail = output[-500:] if output else ""
    return VerificationResult(
        passed=passed,
        score=1.0 if passed else 0.0,
        metrics={
            "method": "env_script",
            "exit_code": exit_code,
            "expected_exit_code": expected_exit_code,
            "script_path": script_path,
            "output_tail": tail,
        },
    )


async def _verify_llm_judge(
    *,
    trajectory: "Trajectory | None",
    verification: dict[str, t.Any],
    judge_context: dict[str, t.Any] | None,
) -> VerificationResult:
    if trajectory is None:
        raise ValueError(
            "llm_judge verification requires a trajectory — single-shot "
            "recipes must verify via env_flag / env_script instead."
        )

    model = verification.get("model")
    rubric = verification.get("rubric")
    if not isinstance(model, str) or not model:
        raise ValueError("llm_judge verification requires a 'model' string")
    if not isinstance(rubric, str) or not rubric:
        raise ValueError(
            "llm_judge verification requires a 'rubric' (short name, path, "
            "or inline text)"
        )

    passing_threshold = float(verification.get("passing_threshold", 0.5))
    system_prompt = verification.get("system_prompt")
    if system_prompt is not None and not isinstance(system_prompt, str):
        raise ValueError("llm_judge 'system_prompt' must be a string when set")

    # Lazy import — AgentJudge pulls in scorers + yaml; keep env_rollouts
    # cheap to import from code paths that don't need llm_judge verification.
    from dreadnode.agents.judge import AgentJudge

    judge = AgentJudge(
        model=model,
        rubric=rubric,
        passing_threshold=passing_threshold,
        system_prompt=system_prompt,
    )
    result = await judge.evaluate(trajectory, context=judge_context)
    return VerificationResult(
        passed=result.passed,
        score=result.score,
        metrics={
            "method": "llm_judge",
            "model": model,
            "rubric": rubric,
            "passing_threshold": passing_threshold,
            "reason": result.reason,
        },
    )


__all__ = [
    "VerificationResult",
    "batched_environments",
    "verify_env_state",
]
