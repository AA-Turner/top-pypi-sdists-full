"""Sandbox-facing job payloads, entrypoints, and result contracts for optimization."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import shutil
import typing as t
from pathlib import Path

import httpx
from gepa.utils.stop_condition import MaxTrackedCandidatesStopper, NoImprovementStopper
from pydantic import BaseModel, ConfigDict, Field

from dreadnode import Dreadnode
from dreadnode.agents.skills import attach_capability_skills
from dreadnode.agents.trajectory import Trajectory
from dreadnode.app.api.models import (
    OptimizationJobProgressUpdateRequest,
    OptimizationMetricPoint,
    OptimizationSummaryPatch,
)
from dreadnode.app.server.app import create_agent
from dreadnode.capabilities.capability import Capability
from dreadnode.core.metric import Metric
from dreadnode.core.scorer import scorer
from dreadnode.core.tls import create_platform_ssl_context
from dreadnode.evaluations.evaluation import current_dataset_row
from dreadnode.generators.proxy import resolve_dn_model_to_generator
from dreadnode.optimization.adapters.agent import DreadnodeAgentAdapter

if t.TYPE_CHECKING:
    from dreadnode.generators.generator import Generator
    from dreadnode.optimization.adapters.stack import CapabilityImprovementSurface
from dreadnode.optimization.api import optimize_anything
from dreadnode.optimization.config import (
    EngineConfig,
    MergeConfig,
    OptimizationConfig,
    ReflectionConfig,
    ReflectionLM,
    ReflectionPrompt,
    TrackingConfig,
)
from dreadnode.optimization.events import (
    BudgetUpdated,
    CandidateAccepted,
    CandidateRejected,
    IterationStart,
    OptimizationEnd,
    OptimizationError,
    OptimizationEvent,
    OptimizationStart,
    ParetoFrontUpdated,
    ValsetEvaluated,
)
from dreadnode.packaging.manifest import DatasetManifest
from dreadnode.training.recipes import RewardPromptRow, RewardRecipeRegistry

logger = logging.getLogger(__name__)

OptimizationJobStatus = t.Literal["completed"]


class OptimizationCapabilityPayload(BaseModel):
    """Resolved capability metadata available to the hosted optimizer runtime."""

    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    version: str
    runtime_digest: str | None = None
    manifest: dict[str, t.Any] = Field(default_factory=dict)
    file_manifest: list[dict[str, t.Any]] = Field(default_factory=list)
    artifact_s3_prefix: str


class OptimizationDatasetPayload(BaseModel):
    """Resolved dataset metadata available to the hosted optimizer runtime."""

    model_config = ConfigDict(extra="forbid")

    id: str
    reference: str
    name: str
    version: str
    format: str
    row_count: int | None = None
    splits: dict[str, t.Any] | None = None
    artifacts: dict[str, t.Any] = Field(default_factory=dict)
    summary: str | None = None


class BaseOptimizationJobPayload(BaseModel):
    """Common payload fields for hosted optimization execution."""

    model_config = ConfigDict(extra="forbid")

    schema_version: t.Literal["2026-03-19"] = "2026-03-19"
    job_id: str
    organization_id: str
    workspace_id: str
    created_by: str | None = None
    name: str | None = None
    backend: t.Literal["gepa"]
    target_kind: t.Literal["capability_agent", "capability_env"]
    model: str
    project: str | None = None
    run_ref: str | None = None
    agent_name: str | None = None
    objective: str | None = None
    reward_recipe: dict[str, t.Any] = Field(default_factory=dict)
    components: list[str] = Field(default_factory=lambda: ["instructions"])
    tags: list[str] = Field(default_factory=list)
    config: dict[str, t.Any] = Field(default_factory=dict)


class GEPAOptimizationJobPayload(BaseOptimizationJobPayload):
    """Resolved payload for a hosted GEPA optimization job."""

    backend: t.Literal["gepa"] = "gepa"
    target_kind: t.Literal["capability_agent", "capability_env"] = "capability_agent"
    capability: OptimizationCapabilityPayload
    dataset: OptimizationDatasetPayload | None = None
    """Present when the caller submitted a published dataset. Absent for
    capability_env jobs whose training surface is an inline ``task_refs`` list
    or a single ``task_ref``; the worker synthesizes trainset rows in that case."""
    val_dataset: OptimizationDatasetPayload | None = None
    task_ref: str | None = None
    """Optional default for capability_env jobs. When set (and ``task_refs`` is
    empty), the worker synthesizes a single-row trainset ``[{'task_ref': task_ref}]``."""
    task_refs: list[str] | None = None
    """Inline training-surface task list for capability_env. Mutually exclusive
    with ``dataset`` and ``task_ref``."""
    val_task_refs: list[str] | None = None
    """Inline held-out val tasks. Never merged with ``task_refs``; a candidate
    is mutated against train, scored for selection against val."""
    timeout_sec: int | None = None
    """Per-trial TaskEnvironment provisioning timeout. Only used when
    target_kind='capability_env'."""


OptimizationJobPayload = GEPAOptimizationJobPayload


class OptimizationJobResult(BaseModel):
    """Structured result written back by sandboxed optimization execution."""

    model_config = ConfigDict(extra="forbid")

    status: OptimizationJobStatus = "completed"
    summary: dict[str, t.Any] = Field(default_factory=dict)
    artifacts: dict[str, t.Any] = Field(default_factory=dict)
    external_job_id: str | None = None
    error: str | None = None


def _build_configured_dreadnode() -> Dreadnode:
    """Return a configured Dreadnode client from sandbox environment variables."""

    return Dreadnode().configure(
        server=os.environ["DREADNODE_SERVER"],
        api_key=os.environ["DREADNODE_API_KEY"],
        organization=os.environ["DREADNODE_ORGANIZATION"],
        workspace=os.environ["DREADNODE_WORKSPACE"],
        project=os.environ.get("DREADNODE_PROJECT") or None,
    )


def _build_platform_proxy_generator(model: str) -> Generator | None:
    """Resolve `dn/...` models to a configured OpenAI-compatible proxy generator."""

    resolved_model = resolve_dn_model_to_generator(model)
    return None if isinstance(resolved_model, str) else resolved_model


def _resolve_execution_model(model: str) -> str | Generator:
    """Return the effective execution model for hosted optimization agents."""

    proxy_generator = _build_platform_proxy_generator(model)
    return proxy_generator if proxy_generator is not None else model


def _resolve_reflection_lm(model: str) -> ReflectionLM:
    """Return a GEPA-compatible reflection LM for hosted optimization."""

    proxy_generator = _build_platform_proxy_generator(model)
    if proxy_generator is None:
        return model
    api_base = proxy_generator.params.api_base
    if not isinstance(api_base, str) or not api_base:
        raise RuntimeError("Missing platform proxy API base URL")

    def _completion(prompt: ReflectionPrompt) -> str:
        import litellm
        from openai import OpenAI

        messages = [{"role": "user", "content": prompt}] if isinstance(prompt, str) else prompt
        with OpenAI(
            api_key=proxy_generator.api_key,
            base_url=api_base,
            http_client=httpx.Client(verify=create_platform_ssl_context()),
        ) as client:
            completion = litellm.completion(
                model=proxy_generator.model,
                messages=messages,
                api_key=proxy_generator.api_key,
                api_base=api_base,
                custom_llm_provider="litellm_proxy",
                client=client,
            )
        content = completion.choices[0].message.content
        return content if isinstance(content, str) else str(content)

    return _completion


def _build_optimization_config(payload: GEPAOptimizationJobPayload) -> OptimizationConfig:
    """Translate the hosted payload config into the SDK optimization config."""

    raw = payload.config
    stop_callbacks: list[t.Any] = []
    if isinstance(raw.get("max_trials"), int):
        stop_callbacks.append(MaxTrackedCandidatesStopper(int(raw["max_trials"])))
    if isinstance(raw.get("max_trials_without_improvement"), int):
        stop_callbacks.append(NoImprovementStopper(int(raw["max_trials_without_improvement"])))
    return OptimizationConfig(
        backend=payload.backend,
        engine=EngineConfig(
            seed=int(raw.get("seed", 0)),
            display_progress_bar=bool(raw.get("display_progress_bar", False)),
            track_best_outputs=bool(raw.get("track_best_outputs", False)),
            max_metric_calls=(
                int(raw["max_metric_calls"])
                if isinstance(raw.get("max_metric_calls"), int)
                else raw.get("max_metric_calls")
            ),
            val_evaluation_policy=(
                str(raw["val_evaluation_policy"])
                if isinstance(raw.get("val_evaluation_policy"), str)
                else None
            ),
            candidate_selection_strategy=(
                str(raw["candidate_selection_strategy"])
                if isinstance(raw.get("candidate_selection_strategy"), str)
                else None
            ),
            cache_evaluation=bool(raw.get("cache_evaluation", False)),
            frontier_type=(
                t.cast(
                    "t.Literal['instance', 'objective', 'hybrid', 'cartesian']",
                    raw["frontier_type"],
                )
                if isinstance(raw.get("frontier_type"), str)
                else None
            ),
        ),
        reflection=ReflectionConfig(
            skip_perfect_score=(
                bool(raw["skip_perfect_score"])
                if isinstance(raw.get("skip_perfect_score"), bool)
                else None
            ),
            perfect_score=(
                float(raw["perfect_score"])
                if isinstance(raw.get("perfect_score"), int | float)
                else None
            ),
            batch_sampler=(
                str(raw["batch_sampler"]) if isinstance(raw.get("batch_sampler"), str) else None
            ),
            reflection_minibatch_size=(
                int(raw["reflection_minibatch_size"])
                if isinstance(raw.get("reflection_minibatch_size"), int)
                else None
            ),
            module_selector=(
                str(raw["module_selector"]) if isinstance(raw.get("module_selector"), str) else None
            ),
            reflection_lm=(
                str(raw["reflection_lm"])
                if isinstance(raw.get("reflection_lm"), str)
                else payload.model
            ),
            reflection_prompt_template=raw.get("reflection_prompt_template")
            if isinstance(raw.get("reflection_prompt_template"), (str, dict))
            else None,
        ),
        merge=MergeConfig(
            max_merge_invocations=(
                int(raw["max_merge_invocations"])
                if isinstance(raw.get("max_merge_invocations"), int)
                else None
            ),
            merge_val_overlap_floor=(
                int(raw["merge_val_overlap_floor"])
                if isinstance(raw.get("merge_val_overlap_floor"), int)
                else None
            ),
        ),
        tracking=TrackingConfig(
            capture_traces=bool(raw.get("capture_traces", True)),
            include_outputs=bool(raw.get("include_outputs", True)),
            include_errors=bool(raw.get("include_errors", True)),
            max_reflection_examples=int(raw.get("max_reflection_examples", 10)),
            max_side_info_chars=int(raw.get("max_side_info_chars", 4000)),
        ),
        stop_callbacks=stop_callbacks or None,
    )


def _load_dataset_rows(
    dn: Dreadnode,
    dataset_payload: OptimizationDatasetPayload,
) -> list[dict[str, t.Any]]:
    """Load a published dataset package into a list-of-dicts batch."""

    artifacts = {
        str(path): str(oid)
        for path, oid in dataset_payload.artifacts.items()
        if isinstance(path, str) and path and isinstance(oid, str) and oid
    }
    if not artifacts:
        raise ValueError(
            f"Optimization dataset payload '{dataset_payload.reference}' is missing artifacts"
        )

    splits: dict[str, str] | None = None
    if isinstance(dataset_payload.splits, dict):
        normalized_splits = {
            str(name): str(path)
            for name, path in dataset_payload.splits.items()
            if isinstance(name, str) and name and isinstance(path, str) and path
        }
        splits = normalized_splits or None

    # Hosted optimization already carries the dataset manifest metadata in the
    # resolved payload. Materialize it locally so Dataset.load() can resolve
    # artifact blobs directly from CAS without depending on OCI install state.
    manifest = DatasetManifest(
        artifacts=artifacts,
        format=dataset_payload.format,
        row_count=dataset_payload.row_count,
        splits=splits,
        summary=dataset_payload.summary,
    )
    dn.storage.store_manifest(
        "datasets",
        dataset_payload.name,
        dataset_payload.version,
        manifest.model_dump_json(indent=2),
    )

    dataset = dn.load_package(f"dataset://{dataset_payload.reference}")
    table = dataset.load()
    return [item for item in table.to_pylist() if isinstance(item, dict)]


def _resolve_agent(
    *,
    dn: Dreadnode,
    payload: GEPAOptimizationJobPayload,
) -> tuple[Capability, t.Any, t.Any]:
    """Load the capability and resolve the target agent definition."""

    # The OCI registry scopes artifacts per-org. The capability name in the
    # payload may use a different org prefix (e.g. "dreadnode/ai-red-teaming")
    # than the sandbox user's org (e.g. "rustling-alpaca-5537"). Try the
    # sandbox org first so the OCI auth check passes, then fall back to the
    # original name from the payload.
    bare_cap_name = payload.capability.name.rsplit("/", 1)[-1]
    sandbox_org = getattr(dn, "organization", None)
    oci_names: list[str] = []
    if isinstance(sandbox_org, str) and sandbox_org:
        oci_names.append(f"{sandbox_org}/{bare_cap_name}")
    if payload.capability.name not in oci_names:
        oci_names.append(payload.capability.name)

    pull_result = None
    for oci_name in oci_names:
        pull_result = dn.pull_package([f"capability://{oci_name}:{payload.capability.version}"])
        if pull_result.success:
            break

    assert pull_result is not None  # at least one name was tried

    capability_refs: list[str | Path] = []
    if pull_result.success:
        manifest_name = None
        pull_config = getattr(pull_result, "config", None)
        if isinstance(pull_config, dict):
            capability_manifest = pull_config.get("capability_manifest")
            if isinstance(capability_manifest, dict):
                raw_manifest_name = capability_manifest.get("name")
                if isinstance(raw_manifest_name, str) and raw_manifest_name:
                    manifest_name = raw_manifest_name

        for candidate in (
            pull_result.dest,
            manifest_name,
            bare_cap_name,
            payload.capability.name,
        ):
            if candidate is None:
                continue
            if candidate in capability_refs:
                continue
            capability_refs.append(candidate)
    else:
        logger.warning(
            "OCI pull failed for %s:%s (%s), falling back to REST API",
            payload.capability.name,
            payload.capability.version,
            "; ".join(pull_result.errors),
        )
        for candidate in (bare_cap_name, payload.capability.name):
            if candidate not in capability_refs:
                capability_refs.append(candidate)

    capability: Capability | None = None
    last_error: FileNotFoundError | None = None
    for capability_ref in capability_refs:
        try:
            capability = Capability(capability_ref, storage=dn.storage)
            break
        except FileNotFoundError as exc:
            last_error = exc

    if capability is None:
        fallback_path = _materialize_capability_from_payload(dn=dn, payload=payload)
        if fallback_path is not None:
            try:
                capability = Capability(fallback_path, storage=dn.storage)
            except FileNotFoundError as exc:
                last_error = exc

    if capability is None:
        if last_error is not None:
            raise last_error
        raise FileNotFoundError(
            f"Capability not found: {payload.capability.name}. Tried refs: {capability_refs}"
        )

    if not capability.agents:
        raise ValueError(f"Capability {payload.capability.name!r} does not expose any agents")

    if payload.agent_name is None:
        agent_def = capability.agents[0]
    else:
        agent_def = next(
            (candidate for candidate in capability.agents if candidate.name == payload.agent_name),
            None,
        )
        if agent_def is None:
            raise ValueError(
                f"Agent {payload.agent_name!r} was not found in capability {payload.capability.name!r}"
            )

    effective_model = _resolve_execution_model(payload.model)
    agent = create_agent(
        effective_model,
        capability=capability,
        agent_def=agent_def,
        extra_tools=capability.tools,
    )
    attach_capability_skills(agent=agent, capability=capability)
    return capability, agent_def, agent


def _materialize_capability_from_payload(
    *,
    dn: Dreadnode,
    payload: GEPAOptimizationJobPayload,
) -> Path | None:
    """Best-effort fallback to reconstruct a capability from artifact files."""

    api = getattr(dn, "api", None)
    organization = getattr(dn, "organization", None)
    if api is None or not isinstance(organization, str) or not organization:
        return None

    file_manifest = payload.capability.file_manifest
    if not isinstance(file_manifest, list) or not file_manifest:
        return None

    manifest = payload.capability.manifest
    local_name = (
        manifest.get("name")
        if isinstance(manifest, dict) and isinstance(manifest.get("name"), str)
        else payload.capability.name.rsplit("/", 1)[-1]
    )
    target_dir = dn.storage.capabilities_path / Path(local_name)

    # If a previous attempt already materialized the capability, reuse it.
    if (target_dir / "capability.yaml").exists():
        return target_dir

    bare_name = payload.capability.name.rsplit("/", 1)[-1]
    shutil.rmtree(target_dir, ignore_errors=True)
    target_dir.mkdir(parents=True, exist_ok=True)

    try:
        for entry in file_manifest:
            if not isinstance(entry, dict):
                continue
            relative_path = entry.get("path")
            if not isinstance(relative_path, str) or not relative_path:
                continue
            content = api.get_capability_file(
                organization,
                bare_name,
                payload.capability.version,
                relative_path,
            )
            dest = target_dir / relative_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(content if isinstance(content, bytes) else content.encode())
    except Exception:
        shutil.rmtree(target_dir, ignore_errors=True)
        raise

    if not (target_dir / "capability.yaml").exists():
        shutil.rmtree(target_dir, ignore_errors=True)
        return None
    return target_dir


def _extract_completion(output: Trajectory | t.Any) -> str:
    """Extract the final assistant-visible completion from an evaluation output."""

    if isinstance(output, Trajectory):
        for message in reversed(output.messages):
            if getattr(message, "role", None) != "assistant":
                continue
            content = getattr(message, "content", "")
            if isinstance(content, str):
                return content
            if isinstance(content, list):
                return "".join(
                    block.get("text", "") if isinstance(block, dict) else str(block)
                    for block in content
                )
        return output.get_summary()
    if output is None:
        return ""
    return str(output)


def _build_reward_prompt_row(
    row: t.Mapping[str, t.Any] | None,
) -> RewardPromptRow:
    """Translate a dataset row into the reward-recipe prompt-row contract."""

    if row is None:
        return RewardPromptRow()

    metadata = row.get("metadata")
    template_context = {
        key: value
        for key, value in row.items()
        if isinstance(key, str)
        and isinstance(value, str | int)
        and key not in {"expected_output", "answer", "reward", "metadata"}
    }
    reward_value = row.get("reward")
    # Accept either ``expected_output`` (the explicit reward contract) or
    # ``answer`` (the conventional ground-truth column on Q&A datasets such
    # as openai/gsm8k). Recipes like ``gsm8k_v1`` parse the trailing answer
    # marker out of the string regardless of which column it came from.
    expected_output = row.get("expected_output") or row.get("answer")
    return RewardPromptRow(
        expected_output=expected_output if isinstance(expected_output, str) else None,
        reward=float(reward_value) if isinstance(reward_value, int | float) else None,
        metadata=metadata if isinstance(metadata, dict) else {},
        template_context=template_context,
    )


def _build_reward_scorer(
    *,
    reward_recipe: dict[str, t.Any],
) -> t.Any:
    """Build a Dreadnode scorer backed by the declarative reward recipes."""

    registry = RewardRecipeRegistry()

    @scorer(name="reward")
    async def reward_scorer(output: Trajectory) -> Metric:
        row = current_dataset_row.get()
        completion = _extract_completion(output)
        result = registry.evaluate(
            reward_recipe=reward_recipe,
            completion=completion,
            prompt_row=_build_reward_prompt_row(row),
            task=None,
        )
        return Metric(value=float(result.reward), attributes=result.metrics)

    return reward_scorer


def _coerce_summary_candidate(candidate: t.Any) -> dict[str, str] | None:
    """Return a string-only candidate mapping suitable for persisted job summaries."""

    if not isinstance(candidate, dict):
        return None
    normalized = {
        key: value
        for key, value in candidate.items()
        if isinstance(key, str) and isinstance(value, str)
    }
    return normalized or None


def _build_metric_point(
    *,
    value: float | None,
    event: OptimizationEvent[t.Any],
    step: int | None,
) -> OptimizationMetricPoint | None:
    """Build a timestamped metric point when the event carries a numeric value."""

    if not isinstance(value, int | float):
        return None
    return OptimizationMetricPoint(
        value=float(value),
        step=step,
        timestamp=event.timestamp,
    )


def _build_progress_update_request(
    event: OptimizationEvent[t.Any],
) -> OptimizationJobProgressUpdateRequest | None:
    """Translate a Dreadnode optimization event into a hosted progress update."""

    data = event.as_dict().get("data", {})
    iteration = getattr(event, "iteration", None)
    step = iteration if isinstance(iteration, int) else None
    metrics: dict[str, list[OptimizationMetricPoint]] = {}
    summary: OptimizationSummaryPatch | None = None
    level: t.Literal["debug", "info", "warning", "error"] = "info"
    message: str | None = None
    event_type: str

    if isinstance(event, OptimizationStart):
        event_type = "optimization_start"
        summary = OptimizationSummaryPatch(
            objective=event.objective,
            train_size=event.dataset_size,
            val_size=event.valset_size,
            metadata={
                "backend": event.backend,
                "uses_adapter": event.uses_adapter,
            },
        )
        message = "Optimization started"
    elif isinstance(event, IterationStart):
        event_type = "iteration_start"
        message = f"Iteration {event.iteration} started"
    elif isinstance(event, CandidateAccepted):
        event_type = "candidate_accepted"
        point = _build_metric_point(value=event.score, event=event, step=step)
        if point is not None:
            metrics["accepted_score"] = [point]
        message = f"Accepted candidate {event.candidate_index}"
    elif isinstance(event, CandidateRejected):
        event_type = "candidate_rejected"
        point = _build_metric_point(value=event.candidate_score, event=event, step=step)
        if point is not None:
            metrics["rejected_score"] = [point]
        message = "Candidate rejected"
    elif isinstance(event, ValsetEvaluated):
        event_type = "valset_evaluated"
        point = _build_metric_point(value=event.average_score, event=event, step=step)
        if point is not None:
            metrics["val_score"] = [point]
        if event.is_best_program:
            summary = OptimizationSummaryPatch(
                best_candidate=_coerce_summary_candidate(event.candidate),
                best_score=event.average_score,
            )
        message = "Validation set evaluated"
    elif isinstance(event, BudgetUpdated):
        event_type = "budget_updated"
        used_point = _build_metric_point(
            value=event.metric_calls_used,
            event=event,
            step=step,
        )
        remaining_point = _build_metric_point(
            value=event.metric_calls_remaining,
            event=event,
            step=step,
        )
        delta_point = _build_metric_point(
            value=event.metric_calls_delta,
            event=event,
            step=step,
        )
        if used_point is not None:
            metrics["metric_calls_used"] = [used_point]
        if remaining_point is not None:
            metrics["metric_calls_remaining"] = [remaining_point]
        if delta_point is not None:
            metrics["metric_calls_delta"] = [delta_point]
        message = "Metric budget updated"
    elif isinstance(event, ParetoFrontUpdated):
        event_type = "pareto_front_updated"
        summary = OptimizationSummaryPatch(
            frontier_size=event.frontier_size,
            best_score=event.best_score,
        )
        frontier_point = _build_metric_point(
            value=event.frontier_size,
            event=event,
            step=step,
        )
        best_point = _build_metric_point(value=event.best_score, event=event, step=step)
        if frontier_point is not None:
            metrics["frontier_size"] = [frontier_point]
        if best_point is not None:
            metrics["frontier_best_score"] = [best_point]
        message = "Pareto frontier updated"
    elif isinstance(event, OptimizationError):
        event_type = "optimization_error"
        level = "error"
        message = event.error or "Optimization failed"
    elif isinstance(event, OptimizationEnd):
        event_type = "optimization_end"
        summary = OptimizationSummaryPatch(
            best_candidate=_coerce_summary_candidate(event.best_candidate),
            best_score=event.best_score,
            best_scores=event.best_scores or None,
            frontier_size=event.frontier_size,
        )
        if event.result is not None:
            summary.objective = event.result.objective
            summary.train_size = event.result.train_size
            summary.val_size = event.result.val_size
            summary.metadata = dict(event.result.metadata)
        best_point = _build_metric_point(value=event.best_score, event=event, step=step)
        frontier_point = _build_metric_point(
            value=event.frontier_size,
            event=event,
            step=step,
        )
        if best_point is not None:
            metrics["best_score"] = [best_point]
        if frontier_point is not None:
            metrics["frontier_size"] = [frontier_point]
        message = "Optimization completed"
    else:
        return None

    return OptimizationJobProgressUpdateRequest(
        event_type=event_type,
        message=message,
        level=level,
        iteration=step,
        summary=summary,
        metrics=metrics,
        data=data if isinstance(data, dict) else {},
    )


_TERMINAL_PROGRESS_EVENTS: frozenset[str] = frozenset(("optimization_end", "optimization_error"))
_TERMINAL_PROGRESS_RETRY_ATTEMPTS = 3
_TERMINAL_PROGRESS_RETRY_BACKOFF_SEC = 0.5


async def _post_progress_update(
    *,
    dn: Dreadnode,
    payload: GEPAOptimizationJobPayload,
    update: OptimizationJobProgressUpdateRequest,
) -> None:
    """Post one hosted optimization progress update back to the API.

    Non-terminal events stay best-effort: one attempt, log-and-continue on
    failure. Terminal events (``optimization_end`` / ``optimization_error``)
    are the authoritative signal the API uses to mark the job done in the
    HTTP-push runtime — a lost terminal push would leave the API polling until
    ``max_runtime_sec``. Retry those a bounded number of times with
    exponential backoff before giving up.
    """

    organization = dn.organization
    workspace = dn.workspace
    if not isinstance(organization, str) or not isinstance(workspace, str):
        logger.warning(
            "Skipping progress update event_type=%s — missing org/workspace on dn",
            update.event_type,
        )
        return

    is_terminal = update.event_type in _TERMINAL_PROGRESS_EVENTS
    attempts = _TERMINAL_PROGRESS_RETRY_ATTEMPTS if is_terminal else 1

    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        success = False
        try:
            await asyncio.to_thread(
                dn.api.post_optimization_job_progress,
                organization,
                workspace,
                payload.job_id,
                update,
            )
            success = True
        except Exception as exc:
            last_error = exc
            if attempt >= attempts:
                break
            backoff = _TERMINAL_PROGRESS_RETRY_BACKOFF_SEC * (2 ** (attempt - 1))
            logger.warning(
                "Terminal progress update failed attempt=%d/%d event_type=%s job_id=%s: %s: %s; retrying in %.1fs",
                attempt,
                attempts,
                update.event_type,
                payload.job_id,
                type(exc).__name__,
                exc,
                backoff,
            )
            await asyncio.sleep(backoff)

        if success:
            if is_terminal and attempt > 1:
                logger.info(
                    "Terminal progress update landed on attempt %d event_type=%s job_id=%s",
                    attempt,
                    update.event_type,
                    payload.job_id,
                )
            return

    if last_error is not None:
        logger.warning(
            "Progress update failed event_type=%s job_id=%s: %s: %s",
            update.event_type,
            payload.job_id,
            type(last_error).__name__,
            last_error,
        )


_VALID_ENV_SURFACES: frozenset[str] = frozenset(
    ("agent_prompt", "capability_prompt", "skill_descriptions", "skill_bodies")
)


def _resolve_env_surfaces(
    components: list[str],
) -> tuple[CapabilityImprovementSurface, ...]:
    """Filter the job payload's components to StackAware surface names, preserving order."""
    from dreadnode.optimization.adapters.stack import DEFAULT_SURFACES

    seen: set[str] = set()
    surfaces: list[CapabilityImprovementSurface] = []
    for component in components:
        if component in seen:
            continue
        if component not in _VALID_ENV_SURFACES:
            raise ValueError(
                f"Unsupported component for capability_env: {component!r} "
                f"(expected one of {sorted(_VALID_ENV_SURFACES)})"
            )
        seen.add(component)
        surfaces.append(t.cast("CapabilityImprovementSurface", component))
    return tuple(surfaces) if surfaces else DEFAULT_SURFACES


async def fetch_and_build_payload(dn: Dreadnode, job_id: str) -> GEPAOptimizationJobPayload:
    """Build a GEPA optimization payload from a live job row.

    Replacement for the worker's resolver phase. The sandbox receives only the
    job UUID on its command line; everything else — refs, config, target kind,
    components — is pulled over HTTP from the job row, and capability/dataset
    artifacts are installed through the normal SDK package path.

    Keeps the existing ``GEPAOptimizationJobPayload`` shape as an internal
    adapter so ``run_gepa_job`` stays untouched. Phase C collapses this
    intermediate.
    """

    from dreadnode.packaging.manifest import DatasetManifest

    organization = dn.organization
    workspace = dn.workspace
    if not isinstance(organization, str) or not isinstance(workspace, str):
        raise TypeError("Sandbox Dreadnode client is missing org/workspace — cannot fetch job")
    job = await asyncio.to_thread(dn.api.get_optimization_job, organization, workspace, str(job_id))
    await _push_runtime_checkpoint(dn=dn, job_id=str(job_id), message="job_fetched")

    if job.backend != "gepa":
        raise ValueError(f"Unsupported optimization backend: {job.backend}")

    capability_ref = job.capability.name
    capability_version = job.capability.version
    await asyncio.to_thread(
        dn.pull_package,
        [f"capability://{capability_ref}:{capability_version}"],
    )
    await _push_runtime_checkpoint(dn=dn, job_id=str(job_id), message="capability_pulled")
    capability_payload = OptimizationCapabilityPayload(
        id=job.capability.artifact_id or "",
        name=capability_ref,
        version=capability_version,
        runtime_digest=job.capability.runtime_digest,
        manifest={},
        file_manifest=[],
        artifact_s3_prefix="",
    )

    def _load_dataset(ref: t.Any) -> OptimizationDatasetPayload:
        reference = f"{ref.name}@{ref.version}"
        dn.pull_package([f"dataset://{ref.name}:{ref.version}"])
        raw_manifest = dn.storage.get_manifest("datasets", ref.name, ref.version)
        manifest = DatasetManifest.model_validate_json(raw_manifest)
        return OptimizationDatasetPayload(
            id="",
            reference=reference,
            name=ref.name,
            version=ref.version,
            format=manifest.format,
            row_count=manifest.row_count,
            splits=manifest.splits,
            artifacts=dict(manifest.artifacts),
            summary=manifest.summary,
        )

    dataset_payload: OptimizationDatasetPayload | None = None
    if job.dataset_ref is not None:
        dataset_payload = await asyncio.to_thread(_load_dataset, job.dataset_ref)

    val_dataset_payload: OptimizationDatasetPayload | None = None
    if job.val_dataset_ref is not None:
        val_dataset_payload = await asyncio.to_thread(_load_dataset, job.val_dataset_ref)

    config = dict(job.config or {})
    timeout_sec_config = config.get("timeout_sec")
    timeout_sec = (
        int(timeout_sec_config)
        if isinstance(timeout_sec_config, int) and timeout_sec_config > 0
        else None
    )

    return GEPAOptimizationJobPayload(
        job_id=str(job.id),
        organization_id=str(job.organization_id),
        workspace_id=str(job.workspace_id),
        name=job.name,
        backend="gepa",
        target_kind=job.target_kind,
        model=job.model,
        project=job.project,
        run_ref=job.run_ref,
        agent_name=job.agent_name,
        objective=job.objective,
        reward_recipe=job.reward_recipe.model_dump(mode="json"),
        components=list(job.components or []),
        tags=list(job.tags or []),
        config=config,
        capability=capability_payload,
        dataset=dataset_payload,
        val_dataset=val_dataset_payload,
        task_ref=None,
        task_refs=list(job.task_refs) if job.task_refs else None,
        val_task_refs=list(job.val_task_refs) if job.val_task_refs else None,
        timeout_sec=timeout_sec,
    )


async def _push_runtime_checkpoint(*, dn: Dreadnode, job_id: str, message: str) -> None:
    """Best-effort `runtime_checkpoint` push so silent bootstrap hangs are visible.

    Never raises — the checkpoints are diagnostic. If the API is unreachable
    we still want the runtime to try to finish the job.
    """

    organization = dn.organization
    workspace = dn.workspace
    if not isinstance(organization, str) or not isinstance(workspace, str):
        return
    try:
        await asyncio.to_thread(
            dn.api.post_optimization_job_progress,
            organization,
            workspace,
            job_id,
            OptimizationJobProgressUpdateRequest(
                event_type="runtime_checkpoint",
                level="info",
                message=message,
            ),
        )
    except Exception as exc:
        logger.warning(
            "runtime_checkpoint push failed message=%s: %s: %s",
            message,
            type(exc).__name__,
            exc,
        )


async def run_job_by_id(job_id: str) -> OptimizationJobResult:
    """Sandbox entry point for HTTP-driven hosted optimization.

    Identical in outcome to ``run_gepa_job`` against a pre-staged payload file
    — the difference is that the sandbox pulls its own inputs over HTTP
    instead of reading a JSON the API worker wrote. Same GEPA run, same
    progress pushes, same terminal signalling.

    Emits `runtime_checkpoint` events at each bootstrap step. A silent hang
    between two of them pinpoints which phase never returns.
    """

    dn = _build_configured_dreadnode()
    await _push_runtime_checkpoint(dn=dn, job_id=job_id, message="bootstrap_complete")
    payload = await fetch_and_build_payload(dn, job_id)
    await _push_runtime_checkpoint(dn=dn, job_id=job_id, message="payload_fetched")
    return await run_gepa_job(payload)


async def run_gepa_job(payload: GEPAOptimizationJobPayload) -> OptimizationJobResult:
    """Execute one hosted GEPA optimization job from a resolved payload."""

    dn = _build_configured_dreadnode()

    capability, agent_def, agent = await asyncio.to_thread(_resolve_agent, dn=dn, payload=payload)

    # Training surface resolution — the three sources are mutually exclusive
    # (validated server-side at job creation). In order of precedence:
    #   1. Published dataset        → load rows from S3
    #   2. Inline task_refs         → synthesize [{"task_ref": ref}, ...]
    #   3. Single task_ref          → synthesize [{"task_ref": task_ref}]
    trainset: list[dict[str, t.Any]]
    if payload.dataset is not None:
        trainset = await asyncio.to_thread(_load_dataset_rows, dn, payload.dataset)
    elif payload.task_refs:
        trainset = [{"task_ref": ref} for ref in payload.task_refs]
    elif payload.task_ref:
        trainset = [{"task_ref": payload.task_ref}]
    else:
        raise ValueError(
            "Optimization payload is missing a training surface — need one of "
            "dataset, task_refs, or task_ref."
        )

    # Val surface — same precedence, but optional. ``val_task_refs`` never
    # merges with trainset; the adapter/optimizer treats them as a held-out
    # evaluation corpus.
    valset: list[dict[str, t.Any]] | None
    if payload.val_dataset is not None:
        valset = await asyncio.to_thread(_load_dataset_rows, dn, payload.val_dataset)
    elif payload.val_task_refs:
        valset = [{"task_ref": ref} for ref in payload.val_task_refs]
    else:
        valset = None
    reward_scorer = _build_reward_scorer(reward_recipe=payload.reward_recipe)
    raw_input_mapping = payload.config.get("dataset_input_mapping")
    dataset_input_mapping: list[str] | dict[str, str] | None = None
    if isinstance(raw_input_mapping, list):
        dataset_input_mapping = [str(k) for k in raw_input_mapping]
    elif isinstance(raw_input_mapping, dict):
        dataset_input_mapping = {str(k): str(v) for k, v in raw_input_mapping.items()}

    parallel_rows = max(1, int(payload.config.get("parallel_rows") or 1))
    concurrency = max(1, int(payload.config.get("concurrency") or 1))

    adapter: t.Any
    if payload.target_kind == "capability_env":
        # ``task_ref`` on the adapter is a *fallback* used for trainset rows
        # that don't carry their own. Inline ``task_refs`` inject ``task_ref``
        # into every row, so any value works as the default; we pick the
        # first ref to keep traces readable. A single ``task_ref`` provides
        # itself. Rows from a published dataset may override per-row.
        default_task_ref = (
            payload.task_ref
            or (payload.task_refs[0] if payload.task_refs else None)
            or (trainset[0].get("task_ref") if trainset else None)
        )
        if not default_task_ref:
            raise ValueError(
                "capability_env optimization has no resolvable task_ref "
                "(every trainset row lacks a task_ref and no default was set)."
            )
        from dreadnode.optimization.adapters.env import CapabilityEnvAdapter

        adapter = CapabilityEnvAdapter(
            capability=capability,
            model=_resolve_execution_model(payload.model),
            agent_name=agent_def.name,
            task_ref=default_task_ref,
            timeout_sec=payload.timeout_sec,
            allowed_surfaces=_resolve_env_surfaces(payload.components),
            parallel_rows=parallel_rows,
            dataset=trainset,
            scorers=[reward_scorer],
            score_name="reward",
            name=payload.name or f"{capability.name} hosted env optimization",
            dataset_input_mapping=dataset_input_mapping,
            objective=payload.objective,
        )
        # The hosted runtime builds a local ``Dreadnode`` instance that never
        # becomes the module-level default, so the adapter's fallback to
        # ``_get_default_instance()`` would fail with "no active org/workspace".
        # Hand it the configured ``dn`` directly.
        adapter._dreadnode_factory = lambda: dn
    else:
        adapter = DreadnodeAgentAdapter(
            agent=agent,
            dataset=trainset,
            scorers=[reward_scorer],
            score_name="reward",
            name=payload.name or f"{agent.name or 'agent'} hosted optimization",
            dataset_input_mapping=dataset_input_mapping,
        )
    config = _build_optimization_config(payload)
    if config.reflection is not None and config.reflection.reflection_lm is not None:
        config.reflection.reflection_lm = _resolve_reflection_lm(config.reflection.reflection_lm)
    optimization = optimize_anything(
        name=payload.name or f"optimization-{payload.job_id}",
        objective=payload.objective,
        trainset=trainset,
        valset=valset,
        config=config,
        adapter=adapter,
        backend="gepa",
        concurrency=concurrency,
        tags=["optimization", "hosted", *payload.tags],
    )
    result = None
    async with optimization.stream() as events:
        async for event in events:
            progress_update = _build_progress_update_request(event)
            if progress_update is not None:
                await _post_progress_update(
                    dn=dn,
                    payload=payload,
                    update=progress_update,
                )
            if isinstance(event, OptimizationEnd):
                result = event.result

    if result is None:
        raise RuntimeError("Optimization finished without a terminal result")
    summary = result.to_dict()
    summary["frontier_size"] = result.frontier_size
    artifacts: dict[str, t.Any] = {
        "capability": f"{payload.capability.name}@{payload.capability.version}",
        "agent_name": payload.agent_name or agent.name,
    }
    # Dataset artifact reference is only meaningful when the training surface
    # was a published dataset. Inline ``task_refs`` / single ``task_ref`` jobs
    # don't have a dataset to cite.
    if payload.dataset is not None:
        artifacts["dataset"] = payload.dataset.reference
    elif payload.task_refs:
        artifacts["task_refs"] = list(payload.task_refs)
    elif payload.task_ref:
        artifacts["task_ref"] = payload.task_ref
    if payload.val_dataset is not None:
        artifacts["val_dataset"] = payload.val_dataset.reference
    elif payload.val_task_refs:
        artifacts["val_task_refs"] = list(payload.val_task_refs)
    return OptimizationJobResult(
        status="completed",
        summary=summary,
        artifacts=artifacts,
    )


def main(argv: list[str] | None = None) -> int:
    """Sandbox entry point for HTTP-driven hosted optimization.

    The sandbox fetches its own job context over HTTP from the API, runs
    GEPA, and pushes terminal state back through the progress endpoint.
    No payload file in, no result file out — the job UUID is everything
    the sandbox needs to bootstrap.
    """

    parser = argparse.ArgumentParser(description="Run a hosted optimization job")
    parser.add_argument(
        "--job-id",
        dest="job_id",
        required=True,
        help="UUID of the optimization job to run.",
    )
    args = parser.parse_args(argv)
    asyncio.run(run_job_by_id(args.job_id))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
