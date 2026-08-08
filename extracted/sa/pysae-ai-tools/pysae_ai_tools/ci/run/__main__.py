"""CLI entry point: pysae-ai-tools ci_run <command> [args].

Commands:
    run <job_name>...  Run one job and its chain, or several jobs concurrently
    status             Show pipeline status overview
    retry              Retry all failed jobs in the pipeline
    create             Create a new pipeline
    jobs               List all jobs in the pipeline

Common flags (all commands):
    --project-id ID
    --pipeline-id ID
    --mr-iid IID
    --branch BRANCH

Examples:
    pysae-ai-tools ci run run deploy_review
    pysae-ai-tools ci run run tests-unit tests-integration  # parallel, waits for both
    pysae-ai-tools ci run run deploy_prod --follow          # track an already-started job
    pysae-ai-tools ci run status
    pysae-ai-tools ci run retry
    pysae-ai-tools ci run create --mr-iid 42
"""

import sys
from typing import Annotated

import typer

from ..common.cli import emit_json, parse_kv_pairs
from .chain_executor import (
    ChainResult,
    MultiChainResult,
    follow_job_chain,
    follow_jobs,
    run_job_chain,
    run_jobs,
    wait_for_pipeline,
)
from .cli_options import (
    BranchOption,
    ContextOptions,
    MrIidOption,
    PipelineIdOption,
    ProjectIdOption,
    ProjectUrlOption,
    build_context,
)
from .gitlab_api import (
    Pipeline,
    PipelineContext,
    create_pipeline,
    describe_context,
    find_pipeline,
    list_jobs,
    retry_pipeline,
)

WAIT_POLL_INTERVAL = 15  # seconds between status checks
WAIT_DEFAULT_TIMEOUT = 3600  # 1 hour max

app = typer.Typer(help="GitLab CI pipeline and job runner")


def _resolve_pipeline(ctx: PipelineContext) -> Pipeline:
    """Resolve the pipeline for ``ctx``, or exit reporting what was searched."""
    pipeline = find_pipeline(ctx)
    if not pipeline:
        print(f"ERROR: aucune pipeline trouvée ({describe_context(ctx)})", file=sys.stderr)
        raise typer.Exit(code=1)
    return pipeline


def _print_chain_result(result: ChainResult) -> None:
    """Print the result of a chain run as JSON."""
    output: dict[str, object] = {
        "success": result.success,
        "pipeline_id": result.pipeline.id,
        "pipeline_url": result.pipeline.web_url,
    }

    if result.target_job:
        output["target_job"] = {
            "id": result.target_job.id,
            "name": result.target_job.name,
            "status": result.target_job.status,
            "url": result.target_job.web_url,
        }

    if result.environment_url:
        output["environment_url"] = result.environment_url

    if result.error:
        output["error"] = result.error

    output["jobs"] = [{"name": r.job.name, "status": r.job.status, "action": r.action} for r in result.results]

    emit_json(output)


def _print_multi_result(result: MultiChainResult) -> None:
    """Print the aggregated result of a multi-target run as JSON."""
    output: dict[str, object] = {
        "success": result.success,
        "pipeline_id": result.pipeline.id,
        "pipeline_url": result.pipeline.web_url,
    }

    targets_out: list[dict[str, object]] = []
    for job in result.target_jobs:
        entry: dict[str, object] = {
            "name": job.name,
            "id": job.id,
            "status": job.status,
            "url": job.web_url,
        }
        if job.name in result.environment_urls:
            entry["environment_url"] = result.environment_urls[job.name]
        targets_out.append(entry)
    output["targets"] = targets_out

    if result.error:
        output["error"] = result.error

    output["jobs"] = [{"name": r.job.name, "status": r.job.status, "action": r.action} for r in result.results]

    emit_json(output)


@app.command()
def run(
    job_names: Annotated[
        list[str] | None,
        typer.Argument(help="Target job name(s); pass several to run and track them concurrently"),
    ] = None,
    project_id: ProjectIdOption = "",
    project_url: ProjectUrlOption = "",
    pipeline_id: PipelineIdOption = "",
    mr_iid: MrIidOption = "",
    branch: BranchOption = "",
    follow: Annotated[
        bool,
        typer.Option(
            "--follow/--no-follow",
            "-f",
            help="Only follow an already-started job until it finishes — never trigger, retry, "
            "resolve its dependency chain, or create a pipeline.",
        ),
    ] = False,
) -> None:
    """Run one job (and its dependency chain), or several jobs concurrently.

    With a single job name, behaves as before. With several names (e.g.
    ``tests-unit tests-integration``) the chains run in parallel and the
    command only returns once every target has reached a terminal state.

    With ``--follow`` nothing is triggered: the target(s) must already be
    started (auto-triggered or played elsewhere) and the command just waits
    for them to reach a terminal state and reports the outcome.
    """
    if not job_names:
        print("ERROR: nom du job requis. Ex: pysae-ai-tools ci run run deploy_review", file=sys.stderr)
        raise typer.Exit(code=1)

    ctx = build_context(ContextOptions(project_id, project_url, pipeline_id, mr_iid, branch))

    if follow:
        if len(job_names) == 1:
            follow_result = follow_job_chain(ctx, job_names[0])
            _print_chain_result(follow_result)
            if not follow_result.success:
                raise typer.Exit(code=1)
            return
        follow_multi = follow_jobs(ctx, job_names)
        _print_multi_result(follow_multi)
        if not follow_multi.success:
            raise typer.Exit(code=1)
        return

    if len(job_names) == 1:
        result = run_job_chain(ctx, job_names[0])
        _print_chain_result(result)
        if not result.success:
            raise typer.Exit(code=1)
        return

    multi = run_jobs(ctx, job_names)
    _print_multi_result(multi)
    if not multi.success:
        raise typer.Exit(code=1)


@app.command()
def status(
    project_id: ProjectIdOption = "",
    project_url: ProjectUrlOption = "",
    pipeline_id: PipelineIdOption = "",
    mr_iid: MrIidOption = "",
    branch: BranchOption = "",
) -> None:
    """Show pipeline status overview."""
    ctx = build_context(ContextOptions(project_id, project_url, pipeline_id, mr_iid, branch))
    pipeline = _resolve_pipeline(ctx)

    output: dict[str, object] = {
        "pipeline_id": pipeline.id,
        "pipeline_url": pipeline.web_url,
        "pipeline_status": pipeline.status,
    }

    jobs_list = list_jobs(ctx, pipeline.id)
    output["jobs"] = [
        {"name": j.name, "stage": j.stage, "status": j.status, "id": j.id}
        for j in sorted(jobs_list, key=lambda j: j.id)
    ]

    emit_json(output)


@app.command()
def retry(
    project_id: ProjectIdOption = "",
    project_url: ProjectUrlOption = "",
    pipeline_id: PipelineIdOption = "",
    mr_iid: MrIidOption = "",
    branch: BranchOption = "",
) -> None:
    """Retry all failed jobs in the pipeline."""
    ctx = build_context(ContextOptions(project_id, project_url, pipeline_id, mr_iid, branch))
    pipeline = _resolve_pipeline(ctx)

    result = retry_pipeline(ctx, pipeline.id)
    if result:
        emit_json({"pipeline_id": result.id, "pipeline_url": result.web_url, "status": result.status})
    else:
        print("ERROR: impossible de relancer la pipeline", file=sys.stderr)
        raise typer.Exit(code=1)


@app.command()
def create(
    project_id: ProjectIdOption = "",
    project_url: ProjectUrlOption = "",
    pipeline_id: PipelineIdOption = "",
    mr_iid: MrIidOption = "",
    branch: BranchOption = "",
    ref: Annotated[str, typer.Option("--ref", help="Git ref (branch/tag) for the pipeline")] = "",
    input_var: Annotated[
        list[str] | None,
        typer.Option("--input", help="Pipeline spec:input as key=value (repeatable, sent as JSON body)"),
    ] = None,
    var: Annotated[
        list[str] | None,
        typer.Option("--var", help="Pipeline CI variable as key=value (repeatable, sent as variables[])"),
    ] = None,
) -> None:
    """Create a new pipeline."""
    ctx = build_context(ContextOptions(project_id, project_url, pipeline_id, mr_iid, branch))

    inputs = parse_kv_pairs(input_var, flag="--input") or None
    variables = parse_kv_pairs(var, flag="--var") or None

    pipeline = create_pipeline(ctx, ref=ref, inputs=inputs, variables=variables)
    if pipeline:
        emit_json({"pipeline_id": pipeline.id, "pipeline_url": pipeline.web_url, "status": pipeline.status})
    else:
        print("ERROR: impossible de creer la pipeline", file=sys.stderr)
        raise typer.Exit(code=1)


@app.command()
def jobs(
    project_id: ProjectIdOption = "",
    project_url: ProjectUrlOption = "",
    pipeline_id: PipelineIdOption = "",
    mr_iid: MrIidOption = "",
    branch: BranchOption = "",
) -> None:
    """List all jobs in the pipeline."""
    ctx = build_context(ContextOptions(project_id, project_url, pipeline_id, mr_iid, branch))
    pipeline = _resolve_pipeline(ctx)

    jobs_list = list_jobs(ctx, pipeline.id)
    output = [
        {"id": j.id, "name": j.name, "stage": j.stage, "status": j.status, "when": j.when}
        for j in sorted(jobs_list, key=lambda j: j.id)
    ]
    emit_json(output)


@app.command()
def wait(
    project_id: ProjectIdOption = "",
    project_url: ProjectUrlOption = "",
    pipeline_id: PipelineIdOption = "",
    mr_iid: MrIidOption = "",
    branch: BranchOption = "",
    timeout: Annotated[int, typer.Option("--timeout", help="Max wait time in seconds")] = WAIT_DEFAULT_TIMEOUT,
    wait_manual: Annotated[
        bool,
        typer.Option(
            "--wait-manual/--no-wait-manual",
            help="If false (default), treat 'manual' as terminal (automatic jobs done, waiting on human).",
        ),
    ] = False,
) -> None:
    """Wait for a pipeline to reach a terminal state.

    Terminal states: success, failed, canceled, skipped. By default, 'manual'
    is also treated as terminal — it means all automatic jobs finished and the
    pipeline is paused waiting for a human to play a manual job, so further
    waiting would block indefinitely. Use --wait-manual to keep waiting past
    that point (rare — only if another system will trigger the manual job).
    """
    ctx = build_context(ContextOptions(project_id, project_url, pipeline_id, mr_iid, branch))
    pipeline = _resolve_pipeline(ctx)

    def _tick(current: Pipeline, elapsed: float) -> None:
        print(f"Pipeline #{pipeline.id} : {current.status}... ({int(elapsed)}s)", file=sys.stderr)

    final, timed_out = wait_for_pipeline(
        ctx,
        pipeline.id,
        timeout=timeout,
        interval=WAIT_POLL_INTERVAL,
        wait_manual=wait_manual,
        on_tick=_tick,
    )
    if final is None:
        print("ERROR: impossible de recuperer le statut de la pipeline", file=sys.stderr)
        raise typer.Exit(code=1)
    if timed_out:
        print(f"ERROR: timeout apres {timeout}s (status: {final.status})", file=sys.stderr)
        raise typer.Exit(code=1)

    emit_json(
        {
            "pipeline_id": final.id,
            "pipeline_url": final.web_url,
            "status": final.status,
        }
    )
    # success and manual (automatic part succeeded) are both non-error exits
    if final.status not in ("success", "manual"):
        raise typer.Exit(code=1)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
