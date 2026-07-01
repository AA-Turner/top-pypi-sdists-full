"""Optimize subcommands for the cyclopts CLI."""

import json
import typing as t

import cyclopts

from dreadnode.app.cli.args import PlatformScopeArgs
from dreadnode.app.cli.shared import (
    _FLAG_STATUS,
    ArtifactRef,
    _render,
    _render_artifacts,
    _render_list,
    _render_logs,
    _status_color,
    _wait_for_job,
    confirm_destructive,
    console,
)
from dreadnode.app.model_catalog import resolve_model

RewardRecipeChoice = t.Literal[
    "contains_v1",
    "exact_match_v1",
    "gsm8k_v1",
    "row_reward_v1",
    "trajectory_imitation_v1",
]

OptimizationStatus = t.Literal[
    "queued",
    "running",
    "completed",
    "failed",
    "cancelled",
]

OptimizationBackend = t.Literal["gepa"]

TargetKind = t.Literal["capability_agent", "capability_env"]

EnvComponent = t.Literal[
    "agent_prompt",
    "capability_prompt",
    "skill_descriptions",
    "skill_bodies",
]
_DEFAULT_ENV_COMPONENTS: tuple[EnvComponent, ...] = (
    "agent_prompt",
    "capability_prompt",
    "skill_descriptions",
    "skill_bodies",
)

cli = cyclopts.App(name="optimize", help="Optimize agents with jobs.")


# ---------------------------------------------------------------------------
# Local helpers
# ---------------------------------------------------------------------------


def _summarize_optimization_job(p: dict[str, t.Any]) -> str:
    job_id = p.get("id", "unknown")
    status = p.get("status", "unknown")
    name = p.get("name") or f"{p.get('backend')}/{p.get('target_kind')}"
    color = _status_color(status)
    return f"[dim]{job_id}[/dim] [{color}]{status}[/{color}] [cyan]{name}[/cyan]"


_OPTIMIZATION_JOB_LIST_ROW_FIELDS: tuple[str, ...] = (
    "status",
    "backend",
    "target_kind",
    "model",
    "capability",
    "started_at",
    "completed_at",
    "created_at",
    "updated_at",
)


def _wait_for_optimization_job(
    client: t.Any,
    *,
    org: str,
    workspace: str,
    job_id: str,
    poll_interval_sec: float,
    timeout_sec: float | None,
) -> t.Any:
    return _wait_for_job(
        lambda: client.get_optimization_job(org, workspace, job_id),
        job_id=job_id,
        label="optimization",
        poll_interval_sec=poll_interval_sec,
        timeout_sec=timeout_sec,
    )


# ---------------------------------------------------------------------------
# submit (default command — runs when `dn optimize` has no subcommand)
# ---------------------------------------------------------------------------


@cli.command(name="submit")
def submit(
    *,
    model: t.Annotated[
        str,
        cyclopts.Parameter(
            help=(
                "Model identifier. Run `dn inference-model list` for platform "
                "models; pass any LiteLLM-compatible BYOK ID after configuring "
                "credentials with `dn secret list`."
            ),
        ),
    ],
    capability: t.Annotated[
        str,
        cyclopts.Parameter(
            help=(
                "Capability ref in NAME@VERSION form (e.g. acme/web-security@1.0.0). "
                "Run `dn capability list` to discover available capabilities."
            ),
        ),
    ],
    reward_recipe: t.Annotated[
        RewardRecipeChoice,
        cyclopts.Parameter(
            help="Hosted reward recipe name",
        ),
    ],
    dataset: t.Annotated[
        str | None,
        cyclopts.Parameter(
            help=(
                "Agent-scored dataset ref (NAME@VERSION, e.g. acme/wikiqa@1.2.0). "
                "Rows drive the agent's user message and reward-recipe scoring. "
                "Mutually exclusive with --task and --task-dataset."
            ),
        ),
    ] = None,
    task: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(
            negative_iterable=(),
            help=(
                "Env-scored training task (repeatable). One value = single task, "
                "multiple = train-across-tasks. Mutually exclusive with --dataset "
                "and --task-dataset."
            ),
        ),
    ] = None,
    task_dataset: t.Annotated[
        str | None,
        cyclopts.Parameter(
            help=(
                "Env-scored dataset ref (NAME@VERSION, e.g. acme/web-tasks@2.1.0) "
                "where rows carry task_ref plus per-row content (inputs, scoring "
                "fields). Use when the corpus warrants versioning — otherwise "
                "reach for --task. Mutually exclusive with --dataset and --task."
            ),
        ),
    ] = None,
    val_dataset: t.Annotated[
        str | None,
        cyclopts.Parameter(
            help="Optional held-out validation dataset (NAME@VERSION, e.g. acme/wikiqa-val@1.0.0).",
        ),
    ] = None,
    val_task: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(
            negative_iterable=(),
            help=(
                "Env-scored held-out validation task (repeatable). Never merged "
                "with training — candidates are mutated against train, scored "
                "for selection against val."
            ),
        ),
    ] = None,
    reward_params: t.Annotated[
        str | None, cyclopts.Parameter(help="Reward recipe parameters as JSON")
    ] = None,
    agent_name: t.Annotated[
        str | None,
        cyclopts.Parameter(
            help="Optional agent name when the capability exports multiple agents",
        ),
    ] = None,
    objective: t.Annotated[
        str | None,
        cyclopts.Parameter(help="Optional natural-language optimization objective"),
    ] = None,
    name: t.Annotated[
        str | None,
        cyclopts.Parameter(help="Optional optimization job name"),
    ] = None,
    run_ref: t.Annotated[str | None, cyclopts.Parameter(help="Run reference for tracking")] = None,
    tag: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(negative_iterable=(), help="Tag for the job (repeatable)"),
    ] = None,
    seed: t.Annotated[
        int | None, cyclopts.Parameter(help="Random seed for reproducibility")
    ] = None,
    max_metric_calls: t.Annotated[
        int | None, cyclopts.Parameter(help="Maximum metric evaluation calls")
    ] = None,
    max_trials: t.Annotated[
        int | None, cyclopts.Parameter(help="Maximum optimization trials before stopping")
    ] = None,
    max_trials_without_improvement: t.Annotated[
        int | None,
        cyclopts.Parameter(
            help="Stop after this many finished trials without improving the best score"
        ),
    ] = None,
    max_runtime_sec: t.Annotated[
        int | None,
        cyclopts.Parameter(help="Maximum hosted runtime seconds before the job is timed out"),
    ] = None,
    reflection_lm: t.Annotated[
        str | None, cyclopts.Parameter(help="Language model for reflection steps")
    ] = None,
    max_reflection_examples: t.Annotated[
        int | None, cyclopts.Parameter(help="Maximum examples for reflection")
    ] = None,
    max_side_info_chars: t.Annotated[
        int | None, cyclopts.Parameter(help="Maximum characters of side information")
    ] = None,
    track_best_outputs: t.Annotated[
        bool,
        cyclopts.Parameter(negative=()),
    ] = False,
    display_progress_bar: t.Annotated[
        bool,
        cyclopts.Parameter(negative=()),
    ] = False,
    capture_traces: t.Annotated[
        bool,
        cyclopts.Parameter(negative="--no-capture-traces"),
    ] = True,
    include_outputs: t.Annotated[
        bool,
        cyclopts.Parameter(negative="--no-include-outputs"),
    ] = True,
    include_errors: t.Annotated[
        bool,
        cyclopts.Parameter(negative="--no-include-errors"),
    ] = True,
    wait: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    poll_interval_sec: t.Annotated[
        float,
        cyclopts.Parameter(
            validator=cyclopts.validators.Number(gt=0), help="Polling interval in seconds"
        ),
    ] = 5.0,
    timeout_sec: t.Annotated[
        float | None, cyclopts.Parameter(help="Timeout in seconds for waiting")
    ] = None,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    env_timeout_sec: t.Annotated[
        int | None,
        cyclopts.Parameter(
            help="Per-trial TaskEnvironment timeout in seconds (env-mode only).",
        ),
    ] = None,
    parallel_rows: t.Annotated[
        int | None,
        cyclopts.Parameter(
            validator=cyclopts.validators.Number(gte=1),
            help="Dataset rows scored concurrently within one candidate (env-mode only; default 1).",
        ),
    ] = None,
    dataset_input_mapping: t.Annotated[
        str | None,
        cyclopts.Parameter(
            help=(
                "Optional dataset->task input remap as JSON. Use to align a dataset "
                "whose columns don't match the agent's expected input — e.g. "
                '\'{"question": "goal"}\' for openai/gsm8k.'
            ),
        ),
    ] = None,
    concurrency: t.Annotated[
        int | None,
        cyclopts.Parameter(
            validator=cyclopts.validators.Number(gte=1),
            help="Candidates evaluated in parallel across the search (default 1).",
        ),
    ] = None,
    component: t.Annotated[
        list[EnvComponent] | None,
        cyclopts.Parameter(
            negative_iterable=(),
            help=(
                "Capability surface to optimize (env-mode only, repeatable). "
                "Defaults to all four: agent_prompt, capability_prompt, "
                "skill_descriptions, skill_bodies."
            ),
        ),
    ] = None,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Submit a hosted optimization job."""
    from dreadnode.app.api.models import (
        CapabilityRef,
        CreateGEPAOptimizationJobRequest,
        DatasetRef,
        OptimizationJobConfig,
        RewardRecipe,
    )

    # Each training-surface flag is self-identifying. Pick exactly one;
    # target_kind is inferred from which one the user chose.
    train_sources = [
        ("--task", bool(task)),
        ("--task-dataset", task_dataset is not None),
        ("--dataset", dataset is not None),
    ]
    active_train = [name for name, present in train_sources if present]
    if len(active_train) == 0:
        raise ValueError(
            "submit requires a training surface: --task (env, inline), "
            "--task-dataset (env, dataset), or --dataset (agent, dataset)"
        )
    if len(active_train) > 1:
        raise ValueError(
            f"training surface is ambiguous — provide only one of {active_train}. "
            "--task is env with inline task list; --task-dataset is env with "
            "curated dataset rows; --dataset is agent-scored."
        )

    is_env = bool(task) or task_dataset is not None
    target_kind: TargetKind = "capability_env" if is_env else "capability_agent"

    if val_task and val_dataset:
        raise ValueError(
            "val surface is ambiguous — provide only one of --val-task or --val-dataset"
        )
    if not is_env:
        if val_task:
            raise ValueError("--val-task is only valid in env mode (with --task or --task-dataset)")
        if env_timeout_sec is not None:
            raise ValueError("--env-timeout-sec is only valid in env mode")
        if parallel_rows is not None:
            raise ValueError("--parallel-rows is only meaningful in env mode")
        if component:
            raise ValueError("--component is only valid in env mode")

    api, profile = platform.connect()

    capability_ref = ArtifactRef.parse_versioned(capability, profile.org_key)

    # Both --dataset and --task-dataset resolve to the same request field
    # (``dataset_ref``); the distinction is user-facing intent encoded via
    # the flag choice. The server-side target_kind + validator keep the two
    # modes unambiguous.
    dataset_ref_source = dataset or task_dataset
    dataset_ref: DatasetRef | None = None
    if dataset_ref_source:
        dataset_parsed = ArtifactRef.parse_versioned(dataset_ref_source, profile.org_key)
        dataset_ref = DatasetRef(name=dataset_parsed.name, version=dataset_parsed.version)

    val_dataset_ref: DatasetRef | None = None
    if val_dataset:
        val_ref = ArtifactRef.parse_versioned(val_dataset, profile.org_key)
        val_dataset_ref = DatasetRef(name=val_ref.name, version=val_ref.version)

    parsed_reward_params: dict[str, t.Any] = {}
    if reward_params:
        try:
            raw_params = json.loads(reward_params)
        except json.JSONDecodeError as exc:
            raise ValueError("--reward-params must be valid JSON") from exc
        if not isinstance(raw_params, dict):
            raise ValueError("--reward-params must decode to a JSON object")
        parsed_reward_params = raw_params

    config_kwargs: dict[str, t.Any] = {
        "capture_traces": capture_traces,
        "include_outputs": include_outputs,
        "include_errors": include_errors,
    }
    if seed is not None:
        config_kwargs["seed"] = seed
    if max_metric_calls is not None:
        config_kwargs["max_metric_calls"] = max_metric_calls
    if max_trials is not None:
        config_kwargs["max_trials"] = max_trials
    if max_trials_without_improvement is not None:
        config_kwargs["max_trials_without_improvement"] = max_trials_without_improvement
    if max_runtime_sec is not None:
        config_kwargs["max_runtime_sec"] = max_runtime_sec
    if reflection_lm is not None:
        config_kwargs["reflection_lm"] = reflection_lm
    if max_reflection_examples is not None:
        config_kwargs["max_reflection_examples"] = max_reflection_examples
    if max_side_info_chars is not None:
        config_kwargs["max_side_info_chars"] = max_side_info_chars
    if track_best_outputs:
        config_kwargs["track_best_outputs"] = True
    if display_progress_bar:
        config_kwargs["display_progress_bar"] = True
    if concurrency is not None:
        config_kwargs["concurrency"] = concurrency
    if parallel_rows is not None:
        config_kwargs["parallel_rows"] = parallel_rows
    if dataset_input_mapping is not None:
        try:
            parsed_mapping = json.loads(dataset_input_mapping)
        except json.JSONDecodeError as exc:
            raise ValueError("--dataset-input-mapping must be valid JSON") from exc
        if not isinstance(parsed_mapping, (dict, list)):
            raise ValueError("--dataset-input-mapping must decode to a JSON object or array")
        config_kwargs["dataset_input_mapping"] = parsed_mapping

    if target_kind == "capability_env":
        components: list[str] = list(component) if component else list(_DEFAULT_ENV_COMPONENTS)
    else:
        components = ["instructions"]

    request_kwargs: dict[str, t.Any] = {
        "name": name,
        "target_kind": target_kind,
        "model": resolve_model(model),
        # Prefer the resolved UUID over the key string. ``validate_scope``
        # (run by ``platform.connect()``) populates ``project_id`` via a
        # workspace-scoped lookup, so when it's set the server can resolve
        # the project unambiguously. Falls back to the key when no project
        # is configured on the profile.
        "project": profile.project_id or profile.project_key,
        "run_ref": run_ref,
        "capability_ref": CapabilityRef(
            name=capability_ref.name,
            version=capability_ref.version,
        ),
        "agent_name": agent_name,
        "dataset_ref": dataset_ref,
        "val_dataset_ref": val_dataset_ref,
        "reward_recipe": RewardRecipe(
            name=reward_recipe,
            params=parsed_reward_params,
        ),
        "components": components,
        "objective": objective,
        "config": OptimizationJobConfig(**config_kwargs),
        "tags": list(tag or []),
    }
    if task:
        request_kwargs["task_refs"] = list(task)
    if val_task:
        request_kwargs["val_task_refs"] = list(val_task)
    if env_timeout_sec is not None:
        request_kwargs["timeout_sec"] = env_timeout_sec

    request = CreateGEPAOptimizationJobRequest(**request_kwargs)
    job = api.create_optimization_job(profile.org_key, profile.workspace_key, request)
    if wait:
        job = _wait_for_optimization_job(
            api,
            org=profile.org_key,
            workspace=profile.workspace_key,
            job_id=job.id,
            poll_interval_sec=poll_interval_sec,
            timeout_sec=timeout_sec,
        )
    _render(job, as_json=as_json, summary=_summarize_optimization_job)
    if wait and job.status != "completed":
        raise RuntimeError(job.error or f"Optimization job {job.id} ended with status {job.status}")


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------


@cli.command(name="list")
def list_(
    *,
    page: t.Annotated[int, cyclopts.Parameter(validator=cyclopts.validators.Number(gte=1))] = 1,
    page_size: t.Annotated[
        int,
        cyclopts.Parameter(validator=cyclopts.validators.Number(gte=1)),
    ] = 20,
    status: t.Annotated[
        OptimizationStatus | None,
        cyclopts.Parameter(name=_FLAG_STATUS),
    ] = None,
    backend: OptimizationBackend | None = None,
    target_kind: TargetKind | None = None,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """List hosted optimization jobs."""
    api, profile = platform.connect()
    jobs = api.list_optimization_jobs(
        profile.org_key,
        profile.workspace_key,
        page=page,
        page_size=page_size,
        status=status,
        backend=backend,
        target_kind=target_kind,
        project=profile.project_key,
    )
    _render_list(
        jobs,
        as_json=as_json,
        summary=_summarize_optimization_job,
        empty_msg="No optimization jobs found",
        fields=_OPTIMIZATION_JOB_LIST_ROW_FIELDS,
    )


# ---------------------------------------------------------------------------
# get
# ---------------------------------------------------------------------------


@cli.command()
def get(
    job_id: str,
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Get a hosted optimization job."""
    api, profile = platform.connect()
    job = api.get_optimization_job(profile.org_key, profile.workspace_key, job_id)
    _render(job, as_json=as_json, summary=_summarize_optimization_job)


# ---------------------------------------------------------------------------
# wait
# ---------------------------------------------------------------------------


@cli.command()
def wait(
    job_id: str,
    *,
    poll_interval_sec: t.Annotated[
        float,
        cyclopts.Parameter(
            validator=cyclopts.validators.Number(gt=0), help="Polling interval in seconds"
        ),
    ] = 5.0,
    timeout_sec: t.Annotated[
        float | None, cyclopts.Parameter(help="Timeout in seconds for waiting")
    ] = None,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Wait for a hosted optimization job to reach a terminal state."""
    api, profile = platform.connect()
    job = _wait_for_optimization_job(
        api,
        org=profile.org_key,
        workspace=profile.workspace_key,
        job_id=job_id,
        poll_interval_sec=poll_interval_sec,
        timeout_sec=timeout_sec,
    )
    _render(job, as_json=as_json, summary=_summarize_optimization_job)
    if job.status != "completed":
        raise RuntimeError(job.error or f"Optimization job {job.id} ended with status {job.status}")


# ---------------------------------------------------------------------------
# logs
# ---------------------------------------------------------------------------


@cli.command()
def logs(
    job_id: str,
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Show hosted optimization logs."""
    api, profile = platform.connect()
    log_data = api.list_optimization_job_logs(profile.org_key, profile.workspace_key, job_id)
    _render_logs(log_data, as_json=as_json)


# ---------------------------------------------------------------------------
# artifacts
# ---------------------------------------------------------------------------


@cli.command()
def artifacts(
    job_id: str,
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Show hosted optimization artifacts."""
    api, profile = platform.connect()
    artifact_data = api.get_optimization_job_artifacts(
        profile.org_key, profile.workspace_key, job_id
    )
    _render_artifacts(artifact_data, as_json=as_json)


# ---------------------------------------------------------------------------
# cancel
# ---------------------------------------------------------------------------


@cli.command()
def cancel(
    job_id: str,
    *,
    yes: t.Annotated[bool, cyclopts.Parameter(name="--yes", alias="-y", negative=())] = False,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Cancel a hosted optimization job.

    Args:
        job_id: The optimization job ID.
        yes: Skip the confirmation prompt.
        as_json: Output as JSON.
    """
    api, profile = platform.connect()

    if not confirm_destructive(f"Cancel optimization job [cyan]{job_id}[/cyan]?", yes=yes):
        console.print("[dim]Cancelled[/dim]")
        return

    job = api.cancel_optimization_job(profile.org_key, profile.workspace_key, job_id)
    _render(job, as_json=as_json, summary=_summarize_optimization_job)


# ---------------------------------------------------------------------------
# retry
# ---------------------------------------------------------------------------


@cli.command()
def retry(
    job_id: str,
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Retry a terminal hosted optimization job."""
    api, profile = platform.connect()
    job = api.retry_optimization_job(profile.org_key, profile.workspace_key, job_id)
    _render(job, as_json=as_json, summary=_summarize_optimization_job)
