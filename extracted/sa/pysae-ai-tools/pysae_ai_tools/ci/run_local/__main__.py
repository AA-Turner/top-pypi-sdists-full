"""CLI entry point: ``pysae-ai-tools ci run-local <command>``.

Reconstruct a GitLab CI job's environment locally and run it.

Commands:
    run <job>      Resolve, build the env, fetch input artifacts, then execute
                   (in the job's Docker image by default; --no-docker for the host).
    inspect <job>  Show the resolved job (image, scripts, variable keys) without running.
"""

import dataclasses
import subprocess
import sys
from pathlib import Path
from typing import Annotated

import typer

from ...common.docker import daemon_running
from ...internal.detect_context.detect import Context, DetectArgs, detect
from ..common.cli import emit_json, parse_kv_pairs
from ..run.include_resolver import gather_yaml_documents
from . import artifacts as artifacts_mod
from . import executor, script_gen, variables
from .job_resolver import build_resolved_job
from .models import ResolvedJob, RunResult
from .yaml_loader import merge_documents, split_jobs

app = typer.Typer(help="Run a GitLab CI job locally (reconstructed environment).", no_args_is_help=True)


def _err(message: str) -> None:
    print(message, file=sys.stderr)


def _repo_root(workdir: str) -> Path:
    if workdir:
        return Path(workdir).resolve()
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            return Path(result.stdout.strip())
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return Path.cwd()


def _resolve_context(project_id: str, pipeline_id: str, mr_iid: str, branch: str) -> Context:
    try:
        ctx = detect(DetectArgs(mr_iid=mr_iid, pipeline_id=pipeline_id))
    except Exception as exc:  # detect is best-effort
        _err(f"Warning: detect-context failed: {exc}")
        ctx = Context()
    if project_id:
        ctx.project_id = project_id
    if pipeline_id:
        ctx.pipeline_id = pipeline_id
    if mr_iid:
        ctx.mr_iid = mr_iid
    if branch:
        ctx.git_branch = branch
    return ctx


def _load_full_map(repo_root: Path) -> dict[str, object]:
    ci_file = repo_root / ".gitlab-ci.yml"
    if not ci_file.exists():
        _err(f"No .gitlab-ci.yml found at {ci_file}.")
        raise typer.Exit(code=1)
    local_content = ci_file.read_text(encoding="utf-8")
    documents = gather_yaml_documents(local_content, repo_root)
    return merge_documents(documents)


def _resolve_job_or_exit(name: str, full_map: dict[str, object]) -> ResolvedJob:
    try:
        return build_resolved_job(name, full_map)
    except KeyError:
        available = sorted(n for n in split_jobs(full_map) if not n.startswith("."))
        _err(f"Job '{name}' not found. Available jobs: {', '.join(available) or '(none)'}")
        raise typer.Exit(code=1) from None


def _yaml_global_vars(full_map: dict[str, object]) -> dict[str, str]:
    raw = full_map.get("variables")
    if not isinstance(raw, dict):
        return {}
    out: dict[str, str] = {}
    for key, value in raw.items():
        if isinstance(value, dict):  # GitLab "value:/description:" form
            value = value.get("value", "")
        if isinstance(value, bool):
            out[str(key)] = "true" if value else "false"
        elif value is not None:
            out[str(key)] = str(value)
    return out


def _resolve_image(image: str, env: dict[str, str]) -> str:
    """Expand ``$VAR`` references in an image name (override or resolved)."""
    return variables.expand_value(image, env) if image else ""


def _build_environment(
    ctx: Context,
    job: ResolvedJob,
    *,
    ci_project_dir: str,
    pipeline_id: str,
    yaml_global: dict[str, str],
    cli_vars: dict[str, str],
    remote_vars: bool,
    scope: str,
) -> variables.EnvResult:
    predefined = variables.predefined(ctx, job.name, job.stage, ci_project_dir, pipeline_id)
    group_vars: list[variables.CiVariable] = []
    project_vars: list[variables.CiVariable] = []
    warnings: list[str] = []
    if remote_vars:
        if ctx.project_path:
            group_vars = variables.fetch_group_vars(ctx.project_path, scope, warnings)
        if ctx.project_id:
            project_vars = variables.fetch_project_vars(ctx.project_id, scope, warnings)
    env_result = variables.build_env(
        predefined_vars=predefined,
        yaml_global=yaml_global,
        yaml_job=job.variables,
        group_vars=group_vars,
        project_vars=project_vars,
        cli_vars=cli_vars,
    )
    env_result.warnings.extend(warnings)
    return env_result


@app.command()
def inspect(
    job_name: Annotated[str, typer.Argument(help="Job name as written in .gitlab-ci.yml")],
    project_id: Annotated[str, typer.Option("--project-id")] = "",
    pipeline_id: Annotated[str, typer.Option("--pipeline-id")] = "",
    mr_iid: Annotated[str, typer.Option("--mr-iid")] = "",
    branch: Annotated[str, typer.Option("--branch")] = "",
    workdir: Annotated[str, typer.Option("--workdir", help="Repo root (default: git toplevel)")] = "",
    remote_vars: Annotated[bool, typer.Option("--remote-vars/--no-remote-vars")] = True,
    scope: Annotated[str, typer.Option("--scope", help="environment_scope filter for UI variables")] = "*",
    image_override: Annotated[
        str, typer.Option("--image", help="Override the job image (e.g. the runner's default image)")
    ] = "",
    as_json: Annotated[bool, typer.Option("--json", help="Emit structured JSON")] = False,
) -> None:
    """Show the resolved job without running it (variable values are never printed)."""
    ctx = _resolve_context(project_id, pipeline_id, mr_iid, branch)
    repo_root = _repo_root(workdir)
    full_map = _load_full_map(repo_root)
    job = _resolve_job_or_exit(job_name, full_map)

    env_result = _build_environment(
        ctx,
        job,
        ci_project_dir=str(repo_root),
        pipeline_id=pipeline_id,
        yaml_global=_yaml_global_vars(full_map),
        cli_vars={},
        remote_vars=remote_vars,
        scope=scope,
    )
    image = _resolve_image(image_override or job.image, env_result.env)

    if as_json:
        payload = {
            "job": job.name,
            "stage": job.stage,
            "image": image,
            "needs": job.needs,
            "dependencies": job.dependencies,
            "before_script": job.before_script,
            "script": job.script,
            "after_script": job.after_script,
            "variables": [{"key": k, "source": env_result.provenance[k]} for k in sorted(env_result.env)],
            "warnings": [*job.warnings, *env_result.warnings],
        }
        emit_json(payload)
        return

    print(f"Job:   {job.name}  (stage: {job.stage})")
    print(f"Image: {image or '(none)'}")
    if job.needs:
        print(f"Needs: {', '.join(job.needs)}")
    if job.dependencies is not None:
        print(f"Dependencies: {', '.join(job.dependencies) or '(none)'}")
    for section, commands in (
        ("before_script", job.before_script),
        ("script", job.script),
        ("after_script", job.after_script),
    ):
        if commands:
            print(f"\n{section}:")
            for cmd in commands:
                print(f"  $ {cmd}")
    print(f"\nVariables ({len(env_result.env)}) — keys and source only:")
    for key in sorted(env_result.env):
        print(f"  {key}  ←  {env_result.provenance[key]}")
    for warning in (*job.warnings, *env_result.warnings):
        _err(f"⚠ {warning}")


@app.command()
def run(
    job_name: Annotated[str, typer.Argument(help="Job name as written in .gitlab-ci.yml")],
    use_docker: Annotated[
        bool, typer.Option("--docker/--no-docker", help="Run in the job image (default) or host shell")
    ] = True,
    generate_only: Annotated[
        bool, typer.Option("--generate-only", help="Write scripts then stop, do not execute")
    ] = False,
    remote_vars: Annotated[
        bool, typer.Option("--remote-vars/--no-remote-vars", help="Fetch group/project UI variables")
    ] = True,
    fetch_artifacts: Annotated[
        bool, typer.Option("--artifacts/--no-artifacts", help="Download needs/dependencies artifacts")
    ] = True,
    echo: Annotated[bool, typer.Option("--echo/--no-echo", help="Echo each command before running it")] = True,
    pull: Annotated[bool, typer.Option("--pull/--no-pull", help="docker pull the image before running")] = True,
    var: Annotated[
        list[str] | None, typer.Option("--var", help="Extra variable KEY=VALUE (highest precedence)")
    ] = None,
    scope: Annotated[str, typer.Option("--scope", help="environment_scope filter for UI variables")] = "*",
    image_override: Annotated[
        str, typer.Option("--image", help="Override the job image (e.g. the runner's default image)")
    ] = "",
    out_dir: Annotated[
        str, typer.Option("--out-dir", help="Where to write the generated scripts (default: .ci/local/<job-name>)")
    ] = "",
    workdir: Annotated[str, typer.Option("--workdir", help="Repo root (default: git toplevel)")] = "",
    project_id: Annotated[str, typer.Option("--project-id")] = "",
    pipeline_id: Annotated[str, typer.Option("--pipeline-id")] = "",
    mr_iid: Annotated[str, typer.Option("--mr-iid")] = "",
    branch: Annotated[str, typer.Option("--branch")] = "",
) -> None:
    """Reconstruct the job environment and execute it locally."""
    ctx = _resolve_context(project_id, pipeline_id, mr_iid, branch)
    repo_root = _repo_root(workdir)
    full_map = _load_full_map(repo_root)
    job = _resolve_job_or_exit(job_name, full_map)
    cli_vars = parse_kv_pairs(var)

    # Build the env first (so we can expand the image), but its CI_PROJECT_DIR
    # depends on the backend — resolve the backend now.
    container_project_dir = f"/builds/{ctx.project_path}" if ctx.project_path else "/builds/project"
    ci_project_dir = container_project_dir if use_docker else str(repo_root)

    env_result = _build_environment(
        ctx,
        job,
        ci_project_dir=ci_project_dir,
        pipeline_id=pipeline_id,
        yaml_global=_yaml_global_vars(full_map),
        cli_vars=cli_vars,
        remote_vars=remote_vars,
        scope=scope,
    )
    image = _resolve_image(image_override or job.image, env_result.env)
    warnings = [*job.warnings, *env_result.warnings]

    if use_docker:
        if not image:
            _err(
                "Backend is Docker but the job declares no image (it would use the runner's default image). "
                "Pass --image <ref> to supply it, or --no-docker to run on the host."
            )
            raise typer.Exit(code=1)
        if not generate_only and not daemon_running():
            _err("Backend is Docker but the Docker daemon is not running. Start it or use --no-docker.")
            raise typer.Exit(code=1)

    # Generate scripts (default: ./.ci/local/<job-name>/, overridable with --out-dir).
    run_dir = script_gen.create_run_dir(job.name, Path(out_dir).resolve() if out_dir else None)
    env_path = script_gen.write_env_file(env_result.env, run_dir)
    runtime_env_path = Path(f"{executor.CONTAINER_RUN_DIR}/env.sh") if use_docker else env_path
    runner_path = script_gen.write_runner(job, runtime_env_path, run_dir, echo=echo)
    _err(f"Generated runner: {runner_path}")
    _err(f"Generated env (0600, contains secrets — do not print/commit): {env_path}")

    # Fetch input artifacts into the working dir (mounted into the container).
    downloaded: list[str] = []
    if fetch_artifacts:
        downloaded = artifacts_mod.download_inputs(
            job=job,
            project_id=ctx.project_id,
            pipeline_id=pipeline_id or ctx.pipeline_id,
            source_branch=ctx.mr_source_branch or ctx.git_branch,
            mr_iid=ctx.mr_iid,
            workdir=repo_root,
            warnings=warnings,
        )
        if downloaded:
            _err(f"Downloaded artifacts from: {', '.join(downloaded)}")

    result = RunResult(
        job=job.name,
        backend="docker" if use_docker else "host",
        image=image,
        script_path=str(runner_path),
        env_path=str(env_path),
        downloaded_artifacts=downloaded,
        warnings=warnings,
        generated_only=generate_only,
    )

    if generate_only:
        _err("Generation only — not executing.")
        emit_json(dataclasses.asdict(result))
        return

    if use_docker:
        _err(f"Running job '{job.name}' in {image} …")
        exit_code = executor.run_docker(
            image=image,
            run_dir_host=run_dir,
            workdir_host=repo_root,
            container_project_dir=container_project_dir,
            pull=pull,
            warnings=warnings,
        )
    else:
        _err(f"Running job '{job.name}' on the host shell …")
        exit_code = executor.run_host(runner_path)

    result.exit_code = exit_code
    result.warnings = warnings
    emit_json(dataclasses.asdict(result))
    if exit_code != 0:
        raise typer.Exit(code=exit_code)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
