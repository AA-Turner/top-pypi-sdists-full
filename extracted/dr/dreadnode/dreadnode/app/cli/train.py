"""Train subcommands for the cyclopts CLI."""

import json
import typing as t

import cyclopts

from dreadnode.app.cli.args import PlatformScopeArgs
from dreadnode.app.cli.shared import (
    _FLAG_QUERY,
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

if t.TYPE_CHECKING:
    from dreadnode.app.api.models import RewardRecipe

RLAlgorithm = t.Literal["importance_sampling", "ppo"]
ExecutionMode = t.Literal["sync", "one_step_off_async", "fully_async"]
TrainingStatus = t.Literal["queued", "running", "completed", "failed", "cancelled"]
TrainingBackend = t.Literal["tinker"]
TrainerType = t.Literal["sft", "rl"]

cli = cyclopts.App(name="train", help="Fine-tune models with hosted SFT and RL jobs.")


# ---------------------------------------------------------------------------
# Local helpers
# ---------------------------------------------------------------------------


def _summarize_training_job(p: dict[str, t.Any]) -> str:
    job_id = p.get("id", "unknown")
    status = p.get("status", "unknown")
    name = p.get("name") or f"{p.get('backend')}/{p.get('trainer_type')}"
    color = _status_color(status)
    return f"[dim]{job_id}[/dim] [{color}]{status}[/{color}] [cyan]{name}[/cyan]"


_TRAINING_JOB_LIST_ROW_FIELDS: tuple[str, ...] = (
    "status",
    "backend",
    "trainer_type",
    "model",
    "project_ref",
    "started_at",
    "completed_at",
    "created_at",
    "updated_at",
)


def _build_optional_reward_recipe(
    reward_recipe: str | None,
    reward_params: str | None,
) -> "RewardRecipe | None":
    from dreadnode.app.api.models import RewardRecipe

    if not reward_recipe:
        return None
    params: dict[str, t.Any] = {}
    if reward_params:
        try:
            raw_params = json.loads(reward_params)
        except json.JSONDecodeError as exc:
            raise ValueError("--reward-params must be valid JSON") from exc
        if not isinstance(raw_params, dict):
            raise ValueError("--reward-params must decode to a JSON object")
        params = raw_params
    return RewardRecipe(name=reward_recipe, params=params)


def _wait_for_training_job(
    client: t.Any,
    *,
    org: str,
    workspace: str,
    job_id: str,
    poll_interval_sec: float,
    timeout_sec: float | None,
) -> t.Any:
    return _wait_for_job(
        lambda: client.get_training_job(org, workspace, job_id),
        job_id=job_id,
        label="training",
        poll_interval_sec=poll_interval_sec,
        timeout_sec=timeout_sec,
    )


def _resolve_project_ref(explicit_project_ref: str | None, profile: t.Any) -> str | None:
    if explicit_project_ref:
        return explicit_project_ref
    profile_project = getattr(profile, "project_key", None)
    if isinstance(profile_project, str) and profile_project:
        return profile_project
    fallback_project = getattr(profile, "project", None)
    if isinstance(fallback_project, str) and fallback_project:
        return fallback_project
    return None


# ---------------------------------------------------------------------------
# sft
# ---------------------------------------------------------------------------


@cli.command()
def sft(
    *,
    model: t.Annotated[
        str,
        cyclopts.Parameter(
            help=("Base model tinker_id. Run `dreadnode train catalog` to list supported values.")
        ),
    ],
    capability: t.Annotated[
        str,
        cyclopts.Parameter(help="Capability ref in NAME@VERSION form"),
    ],
    dataset: t.Annotated[
        str | None,
        cyclopts.Parameter(help="Training dataset ref in NAME@VERSION form"),
    ] = None,
    trajectory_dataset: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(
            negative_iterable=(),
            help="Trajectory dataset ref in NAME@VERSION form (repeatable)",
        ),
    ] = None,
    eval_dataset: t.Annotated[
        str | None,
        cyclopts.Parameter(
            help="Evaluation dataset ref in NAME@VERSION form",
        ),
    ] = None,
    name: t.Annotated[
        str | None,
        cyclopts.Parameter(help="Optional training job name"),
    ] = None,
    project_ref: t.Annotated[
        str | None, cyclopts.Parameter(help="Project reference for tracking")
    ] = None,
    run_ref: t.Annotated[str | None, cyclopts.Parameter(help="Run reference for tracking")] = None,
    tag: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(negative_iterable=(), help="Tag for the job (repeatable)"),
    ] = None,
    max_sequence_length: t.Annotated[
        int | None, cyclopts.Parameter(help="Maximum sequence length")
    ] = None,
    batch_size: t.Annotated[int | None, cyclopts.Parameter(help="Training batch size")] = None,
    gradient_accumulation_steps: t.Annotated[
        int | None, cyclopts.Parameter(help="Gradient accumulation steps")
    ] = None,
    learning_rate: t.Annotated[float | None, cyclopts.Parameter(help="Learning rate")] = None,
    steps: t.Annotated[
        int | None,
        cyclopts.Parameter(
            help="Max optimizer steps (a compute cap). If set with --epochs, "
            "training stops at whichever is reached first."
        ),
    ] = None,
    epochs: t.Annotated[
        int | None,
        cyclopts.Parameter(
            help="Number of passes over the training data. Primary length knob; "
            "defaults to 1 epoch when neither --epochs nor --steps is set."
        ),
    ] = None,
    lora_rank: t.Annotated[int | None, cyclopts.Parameter(help="LoRA rank")] = None,
    lora_alpha: t.Annotated[int | None, cyclopts.Parameter(help="LoRA alpha")] = None,
    checkpoint_interval: t.Annotated[
        int | None, cyclopts.Parameter(help="Steps between checkpoints")
    ] = None,
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
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Submit a hosted SFT training job."""
    from dreadnode.app.api.models import (
        CapabilityRef,
        CreateTinkerSFTJobRequest,
        DatasetRef,
        TinkerSFTJobConfig,
    )

    api, profile = platform.connect()

    capability_ref = ArtifactRef.parse_versioned(capability, profile.org_key)

    dataset_ref: DatasetRef | None = None
    if dataset:
        ds_ref = ArtifactRef.parse_versioned(dataset, profile.org_key)
        dataset_ref = DatasetRef(name=ds_ref.name, version=ds_ref.version)

    trajectory_dataset_refs: list[DatasetRef] = []
    for raw_ref in list(trajectory_dataset or []):
        traj_ref = ArtifactRef.parse_versioned(raw_ref, profile.org_key)
        trajectory_dataset_refs.append(DatasetRef(name=traj_ref.name, version=traj_ref.version))

    eval_dataset_ref: DatasetRef | None = None
    if eval_dataset:
        eval_ref = ArtifactRef.parse_versioned(eval_dataset, profile.org_key)
        eval_dataset_ref = DatasetRef(name=eval_ref.name, version=eval_ref.version)

    request = CreateTinkerSFTJobRequest(
        name=name,
        model=resolve_model(model),
        project_ref=_resolve_project_ref(project_ref, profile),
        run_ref=run_ref,
        capability_ref=CapabilityRef(
            name=capability_ref.name,
            version=capability_ref.version,
        ),
        tags=list(tag or []),
        config=TinkerSFTJobConfig(
            dataset_ref=dataset_ref,
            trajectory_dataset_refs=trajectory_dataset_refs,
            eval_dataset_ref=eval_dataset_ref,
            max_sequence_length=max_sequence_length,
            batch_size=batch_size,
            gradient_accumulation_steps=gradient_accumulation_steps,
            learning_rate=learning_rate,
            steps=steps,
            epochs=epochs,
            lora_rank=lora_rank,
            lora_alpha=lora_alpha,
            checkpoint_interval=checkpoint_interval,
        ),
    )
    job = api.create_training_job(profile.org_key, profile.workspace_key, request)
    if wait:
        job = _wait_for_training_job(
            api,
            org=profile.org_key,
            workspace=profile.workspace_key,
            job_id=job.id,
            poll_interval_sec=poll_interval_sec,
            timeout_sec=timeout_sec,
        )
    _render(job, as_json=as_json, summary=_summarize_training_job)
    if wait and job.status != "completed":
        raise RuntimeError(job.error or f"Training job {job.id} ended with status {job.status}")


# ---------------------------------------------------------------------------
# rl
# ---------------------------------------------------------------------------


@cli.command()
def rl(
    *,
    model: t.Annotated[
        str,
        cyclopts.Parameter(
            help=("Base model tinker_id. Run `dreadnode train catalog` to list supported values.")
        ),
    ],
    capability: t.Annotated[
        str,
        cyclopts.Parameter(help="Capability ref in NAME@VERSION form"),
    ],
    algorithm: RLAlgorithm,
    prompt_dataset: t.Annotated[
        str | None,
        cyclopts.Parameter(
            help="Prompt dataset ref in NAME@VERSION form",
        ),
    ] = None,
    trajectory_dataset: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(
            negative_iterable=(),
            help="Trajectory dataset ref in NAME@VERSION form (repeatable)",
        ),
    ] = None,
    world_manifest_id: t.Annotated[
        str | None, cyclopts.Parameter(help="World manifest ID for environment")
    ] = None,
    world_runtime_id: t.Annotated[str | None, cyclopts.Parameter(help="World runtime ID")] = None,
    world_agent_name: t.Annotated[
        str | None, cyclopts.Parameter(help="Agent name in the world")
    ] = None,
    world_goal: t.Annotated[
        str | None, cyclopts.Parameter(help="Goal for world-based training")
    ] = None,
    task: t.Annotated[
        str | None,
        cyclopts.Parameter(help="Task ref"),
    ] = None,
    reward_recipe: t.Annotated[str | None, cyclopts.Parameter(help="Reward recipe name")] = None,
    reward_params: t.Annotated[
        str | None, cyclopts.Parameter(help="Reward recipe parameters as JSON")
    ] = None,
    world_reward: t.Annotated[
        str | None, cyclopts.Parameter(help="World reward policy name")
    ] = None,
    world_reward_params: t.Annotated[
        str | None, cyclopts.Parameter(help="World reward policy parameters as JSON")
    ] = None,
    execution_mode: ExecutionMode = "sync",
    prompt_split: t.Annotated[
        str | None, cyclopts.Parameter(help="Dataset split for prompts")
    ] = None,
    name: t.Annotated[
        str | None,
        cyclopts.Parameter(help="Optional training job name"),
    ] = None,
    project_ref: t.Annotated[
        str | None, cyclopts.Parameter(help="Project reference for tracking")
    ] = None,
    run_ref: t.Annotated[str | None, cyclopts.Parameter(help="Run reference for tracking")] = None,
    tag: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(negative_iterable=(), help="Tag for the job (repeatable)"),
    ] = None,
    steps: t.Annotated[int | None, cyclopts.Parameter(help="Number of training steps")] = None,
    lora_rank: t.Annotated[int | None, cyclopts.Parameter(help="LoRA rank")] = None,
    max_turns: t.Annotated[
        int | None, cyclopts.Parameter(help="Maximum conversation turns")
    ] = None,
    max_episode_steps: t.Annotated[
        int | None, cyclopts.Parameter(help="Maximum steps per episode")
    ] = None,
    num_rollouts: t.Annotated[
        int | None, cyclopts.Parameter(help="Number of rollouts per step")
    ] = None,
    batch_size: t.Annotated[int | None, cyclopts.Parameter(help="Training batch size")] = None,
    learning_rate: t.Annotated[float | None, cyclopts.Parameter(help="Learning rate")] = None,
    weight_sync_interval: t.Annotated[
        int | None, cyclopts.Parameter(help="Steps between weight syncs")
    ] = None,
    max_steps_off_policy: t.Annotated[
        int | None, cyclopts.Parameter(help="Maximum off-policy steps")
    ] = None,
    max_new_tokens: t.Annotated[
        int | None, cyclopts.Parameter(help="Maximum new tokens per generation")
    ] = None,
    temperature: t.Annotated[float | None, cyclopts.Parameter(help="Sampling temperature")] = None,
    stop: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(negative_iterable=(), help="Stop sequence (repeatable)"),
    ] = None,
    checkpoint_interval: t.Annotated[
        int | None, cyclopts.Parameter(help="Steps between checkpoints")
    ] = None,
    eval_dataset: t.Annotated[
        str | None,
        cyclopts.Parameter(
            help=(
                "Optional held-out prompt dataset ref (NAME@VERSION). Scored "
                "every --eval-interval steps with temperature=0 using the "
                "same --reward-recipe. Emits eval/reward[_max|_min] series."
            )
        ),
    ] = None,
    eval_interval: t.Annotated[
        int | None,
        cyclopts.Parameter(help="Eval cadence in optimizer steps (default 10)"),
    ] = None,
    eval_max_rollouts: t.Annotated[
        int | None,
        cyclopts.Parameter(help="Cap on prompts sampled per eval pass"),
    ] = None,
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
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Submit a hosted RL training job."""
    from dreadnode.app.api.models import (
        CapabilityRef,
        CreateTinkerRLJobRequest,
        DatasetRef,
        TinkerRLJobConfig,
        WorldRewardPolicy,
    )

    api, profile = platform.connect()

    capability_ref = ArtifactRef.parse_versioned(capability, profile.org_key)

    prompt_dataset_ref: DatasetRef | None = None
    if prompt_dataset:
        prompt_ref = ArtifactRef.parse_versioned(prompt_dataset, profile.org_key)
        prompt_dataset_ref = DatasetRef(name=prompt_ref.name, version=prompt_ref.version)

    trajectory_dataset_refs: list[DatasetRef] = []
    for raw_ref in list(trajectory_dataset or []):
        traj_ref = ArtifactRef.parse_versioned(raw_ref, profile.org_key)
        trajectory_dataset_refs.append(DatasetRef(name=traj_ref.name, version=traj_ref.version))

    if prompt_dataset_ref is None and not trajectory_dataset_refs and world_manifest_id is None:
        raise ValueError(
            "dn train rl requires --prompt-dataset, --world-manifest-id, or at least one --trajectory-dataset"
        )

    eval_dataset_ref: DatasetRef | None = None
    if eval_dataset:
        eval_ref = ArtifactRef.parse_versioned(eval_dataset, profile.org_key)
        eval_dataset_ref = DatasetRef(name=eval_ref.name, version=eval_ref.version)

    parsed_world_reward: WorldRewardPolicy | None = None
    if world_reward:
        parsed_world_reward_params: dict[str, t.Any] = {}
        if world_reward_params:
            try:
                raw_params = json.loads(world_reward_params)
            except json.JSONDecodeError as exc:
                raise ValueError("--world-reward-params must be valid JSON") from exc
            if not isinstance(raw_params, dict):
                raise ValueError("--world-reward-params must decode to a JSON object")
            parsed_world_reward_params = raw_params
        parsed_world_reward = WorldRewardPolicy(
            name=world_reward,
            params=parsed_world_reward_params,
        )

    request = CreateTinkerRLJobRequest(
        name=name,
        model=resolve_model(model),
        project_ref=_resolve_project_ref(project_ref, profile),
        run_ref=run_ref,
        capability_ref=CapabilityRef(
            name=capability_ref.name,
            version=capability_ref.version,
        ),
        tags=list(tag or []),
        config=TinkerRLJobConfig(
            algorithm=algorithm,
            task_ref=task,
            world_manifest_id=world_manifest_id,
            world_runtime_id=world_runtime_id,
            world_agent_name=world_agent_name,
            world_goal=world_goal,
            prompt_dataset_ref=prompt_dataset_ref,
            trajectory_dataset_refs=trajectory_dataset_refs,
            reward_recipe=_build_optional_reward_recipe(reward_recipe, reward_params),
            world_reward=parsed_world_reward,
            execution_mode=execution_mode,
            prompt_split=prompt_split,
            steps=steps,
            lora_rank=lora_rank,
            max_turns=max_turns,
            max_episode_steps=max_episode_steps,
            num_rollouts=num_rollouts,
            batch_size=batch_size,
            learning_rate=learning_rate,
            weight_sync_interval=weight_sync_interval,
            max_steps_off_policy=max_steps_off_policy,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            stop=list(stop or []) or None,
            checkpoint_interval=checkpoint_interval,
            eval_dataset_ref=eval_dataset_ref,
            eval_interval=eval_interval,
            eval_max_rollouts=eval_max_rollouts,
        ),
    )
    job = api.create_training_job(profile.org_key, profile.workspace_key, request)
    if wait:
        job = _wait_for_training_job(
            api,
            org=profile.org_key,
            workspace=profile.workspace_key,
            job_id=job.id,
            poll_interval_sec=poll_interval_sec,
            timeout_sec=timeout_sec,
        )
    _render(job, as_json=as_json, summary=_summarize_training_job)
    if wait and job.status != "completed":
        raise RuntimeError(job.error or f"Training job {job.id} ended with status {job.status}")


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
        TrainingStatus | None,
        cyclopts.Parameter(name=_FLAG_STATUS),
    ] = None,
    backend: TrainingBackend | None = None,
    trainer_type: TrainerType | None = None,
    project_ref: t.Annotated[
        str | None, cyclopts.Parameter(help="Project reference filter")
    ] = None,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """List hosted training jobs."""
    api, profile = platform.connect()
    jobs = api.list_training_jobs(
        profile.org_key,
        profile.workspace_key,
        page=page,
        page_size=page_size,
        status=status,
        backend=backend,
        trainer_type=trainer_type,
        project_ref=project_ref,
    )
    _render_list(
        jobs,
        as_json=as_json,
        summary=_summarize_training_job,
        empty_msg="No training jobs found",
        fields=_TRAINING_JOB_LIST_ROW_FIELDS,
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
    """Get a hosted training job."""
    api, profile = platform.connect()
    job = api.get_training_job(profile.org_key, profile.workspace_key, job_id)
    _render(job, as_json=as_json, summary=_summarize_training_job)


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
    """Wait for a hosted training job to reach a terminal state."""
    api, profile = platform.connect()
    job = _wait_for_training_job(
        api,
        org=profile.org_key,
        workspace=profile.workspace_key,
        job_id=job_id,
        poll_interval_sec=poll_interval_sec,
        timeout_sec=timeout_sec,
    )
    _render(job, as_json=as_json, summary=_summarize_training_job)
    if job.status != "completed":
        raise RuntimeError(job.error or f"Training job {job.id} ended with status {job.status}")


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
    """Show hosted training logs."""
    api, profile = platform.connect()
    log_data = api.list_training_job_logs(profile.org_key, profile.workspace_key, job_id)
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
    """Show hosted training artifacts."""
    api, profile = platform.connect()
    artifact_data = api.get_training_job_artifacts(profile.org_key, profile.workspace_key, job_id)
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
    """Cancel a hosted training job.

    Args:
        job_id: The training job ID.
        yes: Skip the confirmation prompt.
        as_json: Output as JSON.
    """
    api, profile = platform.connect()

    if not confirm_destructive(f"Cancel training job [cyan]{job_id}[/cyan]?", yes=yes):
        console.print("[dim]Cancelled[/dim]")
        return

    job = api.cancel_training_job(profile.org_key, profile.workspace_key, job_id)
    _render(job, as_json=as_json, summary=_summarize_training_job)


# ---------------------------------------------------------------------------
# catalog
# ---------------------------------------------------------------------------


@cli.command()
def catalog(
    *,
    query: t.Annotated[
        str | None,
        cyclopts.Parameter(
            name=_FLAG_QUERY,
            help="Free-text search over model id / display name",
        ),
    ] = None,
    family: t.Annotated[
        str | None,
        cyclopts.Parameter(help="Filter by model family (e.g. llama, qwen)"),
    ] = None,
    algorithm: t.Annotated[
        str | None,
        cyclopts.Parameter(help="Filter by supported algorithm (sft, importance_sampling, ppo)"),
    ] = None,
    min_size_b: t.Annotated[
        float | None,
        cyclopts.Parameter(help="Minimum active parameter count (B)"),
    ] = None,
    max_size_b: t.Annotated[
        float | None,
        cyclopts.Parameter(help="Maximum active parameter count (B)"),
    ] = None,
    limit: t.Annotated[
        int,
        cyclopts.Parameter(
            help="Maximum rows to render",
            validator=cyclopts.validators.Number(gte=1, lte=100),
        ),
    ] = 20,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """List supported training base models.

    The values printed in the ``tinker_id`` column are what you pass as
    ``--model`` on ``dreadnode train sft`` / ``dreadnode train rl``.
    """
    api, _profile = platform.connect()
    response = api.get_training_catalog(
        query=query,
        family=family,
        algorithm=algorithm,
        min_size_b=min_size_b,
        max_size_b=max_size_b,
        limit=limit,
    )

    if as_json:
        import json

        print(json.dumps(response.model_dump(mode="json"), indent=2))
        return

    if not response.models:
        print("[dim]No training models match those filters.[/dim]")
        return

    from rich.console import Console
    from rich.table import Table

    table = Table(title=f"Tinker training models ({response.total} match)")
    table.add_column("tinker_id", style="cyan", no_wrap=True)
    table.add_column("display", style="white")
    table.add_column("family", style="magenta")
    table.add_column("type", style="yellow")
    table.add_column("size (B)", justify="right")
    table.add_column("context", justify="right")
    table.add_column("algorithms", style="green")
    for m in response.models:
        table.add_row(
            m.tinker_id,
            m.display_name,
            m.family,
            m.type,
            f"{m.size_b:g}",
            f"{m.context_length:,}",
            ", ".join(m.supported_algorithms),
        )
    Console().print(table)
    if response.total > len(response.models):
        print(
            f"[dim]Showing {len(response.models)} of {response.total}. Pass --limit to widen.[/dim]"
        )
