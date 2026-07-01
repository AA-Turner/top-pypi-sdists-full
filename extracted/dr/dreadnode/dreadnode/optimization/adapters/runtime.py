"""SessionRuntimeAdapter — capability optimization that drives the actual
production agent runtime per trial via :class:`ManagedRuntimeClient`.

Where :class:`StackAwareCapabilityAdapter` (parent) and
:class:`CapabilityEnvAdapter` build a minimally-constructed agent and call
``Agent.run`` directly, this adapter:

* Boots a single in-process :class:`ManagedRuntimeClient` for the
  optimization run (same code path the TUI uses), so the agent runs
  with capability hooks, policy hooks, MCP servers, worker manager,
  compaction — everything production wires up.
* Per trial, materializes the candidate to a deterministic path under
  :class:`~dreadnode.storage.Storage`'s ``optimization_candidate_path``,
  registers the materialized :class:`Capability` in the live registry
  under a transient name, opens a session against that name, drives
  turns, and unregisters on teardown.
* Optional ``task_ref`` mirrors :class:`CapabilityEnvAdapter`: when set,
  each row provisions a ``dn.task_env(...)`` and uses the rendered
  instruction as the agent prompt; otherwise the dataset's
  ``goal_field`` is used (parent behavior).

Runtime client mapping (verified against
:mod:`dreadnode.app.client.runtime_client`):

* ``run_turn(session_id=..., message=...)`` — drives one turn to
  completion.
* ``delete_session(session_id)`` — used by ``persist_sessions="none"``.
* Trajectory access goes through ``get_state().get_session(id)._trajectory``
  rather than the client (no public client method exposes the live
  trajectory; in-process state is the supported pattern, same as the
  ``GET /api/sessions/{id}/messages`` endpoint).

This file is a SKETCH — the lifecycle and registry plumbing is real,
but ``evaluate`` has not been driven against a live runtime yet.
"""

import asyncio
import contextlib
import hashlib
import json
import statistics
import typing as t

from pydantic import Field, PrivateAttr

from dreadnode.optimization.adapters._env_eval import (
    build_trajectory_record,
    numeric_metrics,
    score_from_metrics,
)
from dreadnode.optimization.adapters.stack import (
    MaterializedCapabilityCandidate,
    StackAwareCapabilityAdapter,
)
from dreadnode.optimization.backends.base import OptimizationEvaluationBatch
from dreadnode.optimization.result import OptimizationEvaluation

if t.TYPE_CHECKING:
    from dreadnode.app.client.managed_client import ManagedRuntimeClient

# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #


def _canonical_candidate_hash(candidate: dict[str, str]) -> str:
    """Deterministic hash of a candidate's keys+values.

    Used as the on-disk directory name for the materialized capability
    so identical candidates across iterations land in the same place
    and are trivially de-duplicable. Sort keys to make it order-stable.
    """
    payload = json.dumps(candidate, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------- #
# adapter
# --------------------------------------------------------------------------- #


class SessionRuntimeAdapter(StackAwareCapabilityAdapter):
    """Capability optimization that runs each trial through a real
    ``ManagedRuntimeClient`` session.

    See ``OPTIMIZE_RUNTIME.MD`` §5 for the full design. Inherits seed,
    materialize, propose_new_texts, make_reflective_dataset from
    :class:`StackAwareCapabilityAdapter` and overrides ``evaluate`` +
    ``materialize_candidate`` (to write under ``Storage`` instead of
    ``tempfile``) and ``_format_feedback`` (optional turn excerpt).
    """

    # --- Production-fidelity wiring -----------------------------------------
    policy: str | dict[str, t.Any] = "headless"
    """Policy name or dict passed to ``RuntimeClient.create_session``.
    The headless policy contributes a ``max_steps`` hook automatically;
    pass a dict to override e.g. ``{"name": "headless", "max_steps": 10}``."""
    system_prompt_append: str | None = None
    """Mirrors the CLI ``--system-prompt`` overlay; threaded into
    :class:`ManagedRuntimeClient` at boot."""

    # --- Sandbox controls ---------------------------------------------------
    task_ref: str | None = None
    """Optional task reference; if set, each row provisions ``dn.task_env``.
    Mirrors :class:`CapabilityEnvAdapter`."""
    timeout_sec: int | None = None
    parallel_rows: int = Field(default=1, ge=1)

    # --- Persistence / artifact retention -----------------------------------
    persist_sessions: t.Literal["all", "accepted", "none"] = "all"
    """Which trial sessions to persist. ``"accepted"`` is a future
    enhancement (deferred sync until candidate accept signal); first cut
    treats it the same as ``"all"``."""
    materialize_retention: t.Literal["all", "frontier_only"] = "frontier_only"
    """Which materialized capability trees to keep on disk after the
    optimization run terminates."""
    trace_excerpt_chars: int = 0
    """When >0, inline a tool-call summary into the reflective dataset's
    ``Feedback`` field. Tunes how much trajectory context the GEPA
    reflection LM sees per row. Default off for parity with parent."""

    # --- Optimization job context (set by the bridge wrapper) ---------------
    optimization_job_id: str | None = None
    """Threaded into ``Storage.optimization_job_path`` so materialized
    trees land under ``<storage>/optimizations/<job>/iter-N/<hash>/``.
    The bridge that wraps the adapter (the same code that calls
    ``api.create_optimization_job``) is expected to set this before the
    first ``evaluate`` call."""

    # --- Private state ------------------------------------------------------
    _client: "ManagedRuntimeClient | None" = PrivateAttr(default=None)
    _frontier_hashes: set[str] = PrivateAttr(default_factory=set)
    _iteration: int = PrivateAttr(default=0)

    # =========================================================================
    # Lifecycle
    # =========================================================================

    async def _ensure_runtime(self) -> "ManagedRuntimeClient":
        """Boot the in-process :class:`ManagedRuntimeClient` once per run.

        Raises if the resulting client is not in-process — remote
        runtimes cannot see transient candidate capabilities since
        registration is in-process registry mutation.
        """
        if self._client is not None:
            return self._client

        from dreadnode.app.client.managed_client import ManagedRuntimeClient

        client = ManagedRuntimeClient(
            auto_start=True,
            system_prompt_append=self.system_prompt_append,
        )
        await client.start()
        if not client._in_process:
            raise RuntimeError(
                "SessionRuntimeAdapter requires in-process ManagedRuntimeClient — "
                "remote runtimes cannot see transient candidate capabilities."
            )
        self._client = client
        return client

    async def aclose(self) -> None:
        """Shut down the in-process runtime. Safe to call multiple times."""
        if self._client is None:
            return
        with contextlib.suppress(Exception):
            await self._client.close()
        self._client = None

    # =========================================================================
    # Materialization (override: write under Storage, not tempfile)
    # =========================================================================

    def materialize_candidate(
        self,
        candidate: dict[str, str],
        *,
        job_id: str | None = None,
        iteration: int | None = None,
        candidate_hash: str | None = None,
    ) -> MaterializedCapabilityCandidate:
        """Materialize the candidate under
        ``Storage.optimization_candidate_path(job_id, iteration, hash)``.

        Falls through to :meth:`StackAwareCapabilityAdapter.materialize_candidate`
        (which uses :class:`tempfile.TemporaryDirectory`) when called
        without optimization context — preserves the parent's behavior
        for callers that don't go through the adapter's ``evaluate``.
        """
        if not (job_id and iteration is not None and candidate_hash):
            return super().materialize_candidate(candidate)

        from shutil import copytree

        from dreadnode import _get_default_instance
        from dreadnode.capabilities.capability import Capability

        self._validate_candidate(candidate)
        storage = _get_default_instance().storage
        target_root = (
            storage.optimization_candidate_path(job_id, iteration, candidate_hash)
            / self.capability.path.name
        )
        if target_root.exists():
            # Same hash already materialized (re-evaluating an accepted
            # candidate, or a hash collision across runs in the same job).
            # Reuse the existing tree; this is the de-dup story.
            pass
        else:
            target_root.parent.mkdir(parents=True, exist_ok=True)
            copytree(self.capability.path, target_root)

            for key, value in candidate.items():
                component = self._components.get(key)
                if key == "agent_prompt":
                    self._write_agent_prompt(target_root, value)
                    continue
                if key == "capability_prompt":
                    self._write_capability_prompt(target_root, value)
                    continue
                if component is None:
                    raise ValueError(f"Unknown candidate component: {key}")
                self._write_component(target_root, component, value)

            # Stash the input alongside the tree for inspectability.
            (target_root.parent / "candidate.json").write_text(
                json.dumps(candidate, indent=2, sort_keys=True)
            )

        materialized = Capability(target_root)
        selected_agent = self._resolve_agent_def(materialized, self._agent_def.name)
        return MaterializedCapabilityCandidate(
            root=target_root,
            capability=materialized,
            agent_def=selected_agent,
            _temp_dir=None,  # we own the lifecycle, not tempfile
        )

    # =========================================================================
    # Evaluate
    # =========================================================================

    async def evaluate(
        self,
        batch: list[dict[str, t.Any]],
        candidate: dict[str, str],
        *,
        capture_traces: bool = False,
    ) -> OptimizationEvaluationBatch:
        """Materialize → register transient capability → drive trial sessions."""
        from dreadnode.app.server.app import get_state

        client = await self._ensure_runtime()
        if not self.optimization_job_id:
            raise RuntimeError(
                "SessionRuntimeAdapter.evaluate requires optimization_job_id to "
                "be set on the adapter (the bridge wraps create_optimization_job "
                "and stamps it). For ad-hoc / non-bridge usage, set a synthetic "
                "id on the adapter directly."
            )

        self._iteration += 1
        candidate_hash = _canonical_candidate_hash(candidate)

        materialized = await asyncio.to_thread(
            self.materialize_candidate,
            candidate,
            job_id=self.optimization_job_id,
            iteration=self._iteration,
            candidate_hash=candidate_hash,
        )

        # Replace the source capability's registry entry with the
        # materialized one under its OWN name. The materialized capability
        # has the same ``name`` field as the source (only its prompt/skill
        # text differs), so we just swap the dict entry for the duration of
        # the trial and restore on teardown. ``all_tools()`` dedupes by tool
        # name and the MCP manager owns its own client state independent of
        # the registry entry, so swapping the entry does not interrupt
        # MCP-backed tools or workers.
        capability_name = materialized.capability.name
        registry = get_state().capability_registry
        if registry is None:
            raise RuntimeError(
                "ManagedRuntimeClient started but capability_registry is None — "
                "runtime lifespan probably did not complete."
            )
        prior_entry = registry.capabilities.get(capability_name)
        registry.capabilities[capability_name] = materialized.capability
        try:
            per_row = await self._evaluate_rows(
                client=client,
                capability_name=capability_name,
                agent_name=materialized.agent_def.name,
                batch=batch,
                capture_traces=capture_traces,
            )
        finally:
            if prior_entry is not None:
                registry.capabilities[capability_name] = prior_entry
            else:
                registry.capabilities.pop(capability_name, None)
            # Retention: keep materialized tree on disk only if it lands
            # on the frontier. Bridge code should call
            # ``adapter.mark_frontier(candidate_hash)`` from its
            # ``candidate_accepted`` event handler.
            if (
                self.materialize_retention == "frontier_only"
                and candidate_hash not in self._frontier_hashes
            ):
                materialized.cleanup()

        outputs = [row["output"] for row in per_row]
        scores = [row["score"] for row in per_row]
        objective_scores = [row["objective_scores"] for row in per_row]
        trajectories = (
            [row["trajectory"] for row in per_row if row["trajectory"] is not None]
            if capture_traces
            else None
        )
        return OptimizationEvaluationBatch(
            outputs=outputs,
            scores=scores,
            trajectories=trajectories or None,
            objective_scores=objective_scores or None,
        )

    async def _evaluate_rows(
        self,
        *,
        client: "ManagedRuntimeClient",
        capability_name: str,
        agent_name: str,
        batch: list[dict[str, t.Any]],
        capture_traces: bool,
    ) -> list[dict[str, t.Any]]:
        """Per-row trial driver. Concurrency-bounded by ``parallel_rows``."""
        sem = asyncio.Semaphore(self.parallel_rows)

        async def run_one(row: dict[str, t.Any]) -> dict[str, t.Any]:
            async with sem:
                if self.task_ref is not None:
                    return await self._evaluate_row_with_task_env(
                        client=client,
                        capability_name=capability_name,
                        agent_name=agent_name,
                        row=row,
                        capture_traces=capture_traces,
                    )
                return await self._evaluate_row_qa(
                    client=client,
                    capability_name=capability_name,
                    agent_name=agent_name,
                    row=row,
                    capture_traces=capture_traces,
                )

        return await asyncio.gather(*(run_one(row) for row in batch))

    async def _evaluate_row_qa(
        self,
        *,
        client: "ManagedRuntimeClient",
        capability_name: str,
        agent_name: str,
        row: dict[str, t.Any],
        capture_traces: bool,
    ) -> dict[str, t.Any]:
        """Q&A path — dataset row's ``goal_field`` is the prompt; no sandbox."""
        prompt = self._row_goal_prompt(row)
        session = await client.create_session(
            capability=capability_name,
            agent=agent_name,
            model=self.model,
            policy=self.policy,
        )
        trajectory: t.Any = None
        error: BaseException | None = None
        output: t.Any = None
        metrics: dict[str, t.Any] = {}
        try:
            await self._send_and_drain(client, session.session_id, prompt)
            trajectory = await self._fetch_trajectory(client, session.session_id)
            output = trajectory
            metrics = await self._score_output(output)
        except Exception as exc:
            error = exc
        finally:
            if self.persist_sessions == "none":
                await self._delete_session(client, session.session_id)

        record = (
            build_trajectory_record(
                row=row,
                prompt=prompt,
                output=output,
                metrics=metrics,
                error=error,
                task_ref="<qa>",
            )
            if capture_traces
            else None
        )
        return {
            "output": output,
            "score": score_from_metrics(metrics, error=error, score_name=self.score_name),
            "objective_scores": numeric_metrics(metrics),
            "trajectory": record,
            "session_id": str(session.session_id),
        }

    async def _evaluate_row_with_task_env(
        self,
        *,
        client: "ManagedRuntimeClient",
        capability_name: str,
        agent_name: str,
        row: dict[str, t.Any],
        capture_traces: bool,
    ) -> dict[str, t.Any]:
        """Task-env path — provision a sandbox per row, render its instruction
        as the prompt. Mirrors :class:`CapabilityEnvAdapter` semantics but
        drives the agent through the runtime client instead of
        ``Agent.run`` directly.

        Implementation note: the existing
        :func:`score_row_with_task_env` helper calls ``agent.run(prompt)``
        directly. For the runtime-client path we don't have a raw
        ``agent`` — we have a session id. So we provision the env, send
        the prompt through the client, fetch the trajectory, then call
        the user's scorers (which can read ``current_task_environment``
        while the env is still open).
        """
        from dreadnode import _get_default_instance

        dn = _get_default_instance()
        task_ref = str(row.get("task_ref") or self.task_ref)
        inputs = row.get("inputs") if isinstance(row.get("inputs"), dict) else None
        env = dn.task_env(task_ref, inputs=inputs, timeout_sec=self.timeout_sec)

        session = await client.create_session(
            capability=capability_name,
            agent=agent_name,
            model=self.model,
            policy=self.policy,
        )
        trajectory: t.Any = None
        error: BaseException | None = None
        output: t.Any = None
        metrics: dict[str, t.Any] = {}
        prompt: str | None = None

        def _resolve_prompt() -> str:
            rendered = env.render_instruction() or env.instruction
            if not rendered:
                raise ValueError(
                    f"Task {task_ref!r} has no instruction — capability_env "
                    "optimization requires the task to drive the agent's prompt."
                )
            return rendered

        try:
            async with env:
                prompt = _resolve_prompt()
                await self._send_and_drain(client, session.session_id, prompt)
                trajectory = await self._fetch_trajectory(client, session.session_id)
                output = trajectory
                metrics = await self._score_output(output)
        except Exception as exc:
            # Captures sandbox provision failures (``env.__aenter__``), the
            # missing-instruction guard above, and any per-turn error so a
            # single bad row fails locally instead of aborting the whole
            # ``asyncio.gather`` batch in :meth:`_evaluate_rows`.
            error = exc
        finally:
            if self.persist_sessions == "none":
                await self._delete_session(client, session.session_id)

        record = (
            build_trajectory_record(
                row=row,
                prompt=prompt or "",
                output=output,
                metrics=metrics,
                error=error,
                task_ref=task_ref,
            )
            if capture_traces
            else None
        )
        return {
            "output": output,
            "score": score_from_metrics(metrics, error=error, score_name=self.score_name),
            "objective_scores": numeric_metrics(metrics),
            "trajectory": record,
            "session_id": str(session.session_id),
        }

    async def evaluate_candidate(
        self,
        candidate: dict[str, str],
        example: dict[str, t.Any] | None = None,
    ) -> OptimizationEvaluation:
        """Single-row eval entry, GEPA-compatible ``(score, side_info)`` shape."""
        batch = [example] if example is not None else self.dataset
        if not batch:
            raise ValueError("SessionRuntimeAdapter requires at least one dataset example.")
        evaluation_batch = await self.evaluate(batch, candidate, capture_traces=True)
        score = statistics.mean(evaluation_batch.scores) if evaluation_batch.scores else 0.0
        side_info: dict[str, t.Any] = {
            "scores": evaluation_batch.scores,
            "batch_size": len(batch),
        }
        if evaluation_batch.trajectories is not None:
            side_info["trajectories"] = evaluation_batch.trajectories
        return OptimizationEvaluation(score=score, side_info=side_info)

    # =========================================================================
    # Frontier tracking (called by the bridge from candidate_accepted events)
    # =========================================================================

    def mark_frontier(self, candidate_hash: str) -> None:
        """Pin a candidate's materialized tree against ``frontier_only`` cleanup."""
        self._frontier_hashes.add(candidate_hash)

    # =========================================================================
    # Reflective feedback (override: optional turn excerpt)
    # =========================================================================

    def _format_feedback(self, *, score: float, trajectory: dict[str, t.Any]) -> str:
        parts = [f"Score: {score:.4f}"]
        if error := trajectory.get("error"):
            parts.append(f"Error: {error}")
        if metrics := trajectory.get("metrics"):
            parts.append(f"Metrics: {metrics}")
        if self.trace_excerpt_chars > 0:
            if turns := trajectory.get("turns"):
                parts.append(self._summarize_turns(turns, max_chars=self.trace_excerpt_chars))
        return " | ".join(parts)

    @staticmethod
    def _summarize_turns(turns: list[dict[str, t.Any]], *, max_chars: int) -> str:
        """Compact one-line summary of tool calls + assistant snippets."""
        if not turns:
            return "Turns: (none)"
        parts = ["Turns:"]
        for row in turns:
            for call in row.get("tool_calls") or []:
                name = call.get("name") or call.get("function", {}).get("name") or "?"
                parts.append(f"step{row.get('step', '?')}:{name}()")
            if asst := row.get("assistant"):
                snippet = asst.replace("\n", " ")[:80]
                parts.append(f"step{row.get('step', '?')}:assistant({snippet!r})")
        s = " ".join(parts)
        return s if len(s) <= max_chars else s[:max_chars] + "…"

    # =========================================================================
    # RuntimeClient adapters
    # =========================================================================
    # ``run_turn`` (runtime_client.py:610) blocks until the turn reaches a
    # terminal state and returns the terminal-event payload. We don't actually
    # need that payload for scoring — scorers consume the full ``Trajectory``,
    # which the in-process ``SessionRuntime`` owns. Since we're in-process
    # anyway (asserted in ``_ensure_runtime``), we read the trajectory
    # directly from runtime state. This is technically reaching past the
    # client API, but it's the supported in-process pattern: for example the
    # ``GET /api/sessions/{id}/messages`` endpoint does the same thing
    # (``app.py:2698``).

    async def _send_and_drain(
        self,
        client: "ManagedRuntimeClient",
        session_id: str,
        prompt: str,
    ) -> None:
        """Run one turn to completion via the runtime client."""
        await client.run_turn(session_id=session_id, message=prompt)

    async def _fetch_trajectory(
        self,
        client: "ManagedRuntimeClient",  # noqa: ARG002 — kept for symmetry / future remote support
        session_id: str,
    ) -> t.Any:
        """Read the live ``Trajectory`` from in-process server state.

        ``ManagedRuntimeClient`` runs the runtime in this process; the
        session's ``Trajectory`` is the same object the agent populated
        during the turn we just drove.
        """
        from dreadnode.app.server.app import get_state

        session = get_state().get_session(session_id)
        if session is None:
            return None
        return session._trajectory

    async def _delete_session(
        self,
        client: "ManagedRuntimeClient",
        session_id: str,
    ) -> None:
        """Best-effort session deletion. Skips silently on error so
        ``persist_sessions="none"`` cleanup doesn't mask the trial result."""
        with contextlib.suppress(Exception):
            await client.delete_session(session_id)

    # =========================================================================
    # Scorer hookup
    # =========================================================================

    async def _score_output(self, output: t.Any) -> dict[str, t.Any]:
        # When called from the task-env path, ``current_task_environment`` is
        # set by the caller's ``async with env`` so scorers can probe the live
        # sandbox; same as CapabilityEnvAdapter._score_row.
        from dreadnode.core.scorer import Scorer

        fitted = Scorer.fit_many(self.scorers)
        metric_map = await Scorer.evaluate(output, fitted, assert_scores=False)
        return {name: values[0] for name, values in metric_map.items() if values}

    def _row_goal_prompt(self, row: dict[str, t.Any]) -> str:
        prompt = row.get(self.goal_field)
        if not isinstance(prompt, str) or not prompt:
            raise ValueError(
                f"SessionRuntimeAdapter Q&A mode requires row[{self.goal_field!r}] "
                f"to be a non-empty string; got {prompt!r}"
            )
        return prompt
