"""Low-level GitLab CI API wrapper using glab CLI."""

import json
import sys
from dataclasses import dataclass
from typing import Any

from ...common.glab.runner import run_glab


def _run_glab(*args: str, timeout: int = 30, stdin_data: str | None = None) -> str | None:
    """Run a glab command, return stdout or None on failure."""
    res = run_glab(*args, timeout=timeout, stdin_data=stdin_data)
    if not res.ok:
        if res.stderr:
            print(f"glab error: {res.stderr}", file=sys.stderr)
        return None
    return res.stdout


def _glab_json(*args: str, timeout: int = 30) -> Any | None:
    """Run glab and parse JSON output."""
    raw = _run_glab(*args, timeout=timeout)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print(f"Invalid JSON from glab: {raw[:200]}", file=sys.stderr)
        return None


@dataclass
class Job:
    """A GitLab CI job."""

    id: int
    name: str
    stage: str
    status: str
    when: str = "on_success"
    allow_failure: bool = False
    web_url: str = ""
    failure_reason: str = ""
    environment: str = ""
    pipeline_id: int = 0

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Job":
        pipeline = data.get("pipeline", {})
        # GitLab returns ``when: null`` for jobs in many states, so .get(..., default)
        # is not enough — fall back to "on_success" for any falsy value.
        return cls(
            id=data["id"],
            name=data["name"],
            stage=data.get("stage", ""),
            status=data.get("status", ""),
            when=data.get("when") or "on_success",
            allow_failure=bool(data.get("allow_failure", False)),
            web_url=data.get("web_url", ""),
            failure_reason=data.get("failure_reason", ""),
            environment=data.get("environment", ""),
            pipeline_id=pipeline.get("id", 0) if isinstance(pipeline, dict) else 0,
        )

    @property
    def is_terminal(self) -> bool:
        return self.status in ("success", "failed", "canceled", "skipped")

    @property
    def needs_play(self) -> bool:
        return self.status == "manual" or (self.status == "created" and self.when == "manual")


@dataclass
class Pipeline:
    """A GitLab CI pipeline."""

    id: int
    status: str
    web_url: str = ""
    ref: str = ""

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Pipeline":
        return cls(
            id=data["id"],
            status=data.get("status", ""),
            web_url=data.get("web_url", ""),
            ref=data.get("ref", ""),
        )


@dataclass
class PipelineContext:
    """Resolved pipeline context for running jobs."""

    project_id: str
    project_url: str = ""
    pipeline_id: str = ""
    mr_iid: str = ""
    source_branch: str = ""
    sha: str = ""


def describe_context(ctx: PipelineContext) -> str:
    """Summarise what :func:`find_pipeline` looked for, for error messages."""
    parts = [f"projet {ctx.project_id}"]
    if ctx.pipeline_id:
        parts.append(f"pipeline #{ctx.pipeline_id}")
    if ctx.mr_iid:
        parts.append(f"MR !{ctx.mr_iid}")
    if ctx.source_branch:
        parts.append(f"branche {ctx.source_branch}")
    if ctx.sha:
        parts.append(f"commit {ctx.sha[:8]}")
    if len(parts) == 1:
        parts.append("aucun ref à chercher — passe --branch, --mr-iid ou --pipeline-id")
    return ", ".join(parts)


def find_pipeline(ctx: PipelineContext) -> Pipeline | None:
    """Find the pipeline to work on, from the most explicit context to the least."""
    if ctx.pipeline_id:
        data = _glab_json("api", f"projects/{ctx.project_id}/pipelines/{ctx.pipeline_id}")
        if data:
            return Pipeline.from_api(data)

    # Try MR pipeline first
    if ctx.mr_iid:
        data = _glab_json("api", f"projects/{ctx.project_id}/merge_requests/{ctx.mr_iid}/pipelines")
        if data and isinstance(data, list) and data:
            return Pipeline.from_api(data[0])

    # Fall back to branch pipeline
    if ctx.source_branch:
        data = _glab_json("api", f"projects/{ctx.project_id}/pipelines?ref={ctx.source_branch}&per_page=1")
        if data and isinstance(data, list) and data:
            return Pipeline.from_api(data[0])

    # The branch may carry no pipeline of its own while its commit does under
    # another ref — a local branch sitting on an already-pushed tip, a tag
    # pipeline. Same commit means same code, so that pipeline is the right one.
    # GitLab only matches the full 40-char sha here, never an abbreviation.
    if ctx.sha:
        data = _glab_json("api", f"projects/{ctx.project_id}/pipelines?sha={ctx.sha}&per_page=1")
        if data and isinstance(data, list) and data:
            pipeline = Pipeline.from_api(data[0])
            print(
                f"Pipeline #{pipeline.id} résolue par commit {ctx.sha[:8]} (ref: {pipeline.ref})",
                file=sys.stderr,
            )
            return pipeline

    return None


def create_pipeline(
    ctx: PipelineContext,
    ref: str = "",
    inputs: dict[str, str] | None = None,
    variables: dict[str, str] | None = None,
) -> Pipeline | None:
    """Create a new pipeline.

    Args:
        ctx: Pipeline context (project_id, mr_iid, source_branch).
        ref: Explicit ref. If empty, uses MR head ref or source_branch.
        inputs: GitLab spec:inputs (sent as JSON body).
        variables: CI/CD variables (sent as JSON body ``variables[]``).
    """
    if not ref:
        if ctx.mr_iid:
            ref = f"refs/merge-requests/{ctx.mr_iid}/head"
        elif ctx.source_branch:
            ref = ctx.source_branch
        else:
            return None

    if inputs or variables:
        # Both inputs and variables must be sent as JSON body
        payload_dict: dict[str, object] = {"ref": ref}
        if inputs:
            payload_dict["inputs"] = inputs
        if variables:
            payload_dict["variables"] = [{"key": k, "value": v} for k, v in variables.items()]
        payload = json.dumps(payload_dict)
        raw = _run_glab(
            "api",
            "-X",
            "POST",
            f"projects/{ctx.project_id}/pipeline",
            "-H",
            "Content-Type: application/json",
            "--input",
            "-",
            stdin_data=payload,
        )
        if raw:
            try:
                return Pipeline.from_api(json.loads(raw))
            except json.JSONDecodeError:
                return None
        return None

    data = _glab_json("api", "-X", "POST", f"projects/{ctx.project_id}/pipeline", "-f", f"ref={ref}")
    if data:
        return Pipeline.from_api(data)
    return None


def get_pipeline(ctx: PipelineContext, pipeline_id: int) -> Pipeline | None:
    """Get a pipeline's current state."""
    data = _glab_json("api", f"projects/{ctx.project_id}/pipelines/{pipeline_id}")
    if data:
        return Pipeline.from_api(data)
    return None


def retry_pipeline(ctx: PipelineContext, pipeline_id: int) -> Pipeline | None:
    """Retry all failed jobs in a pipeline."""
    data = _glab_json("api", "-X", "POST", f"projects/{ctx.project_id}/pipelines/{pipeline_id}/retry")
    if data:
        return Pipeline.from_api(data)
    return None


def list_jobs(ctx: PipelineContext, pipeline_id: int) -> list[Job]:
    """List all jobs in a pipeline (excluding retried)."""
    data = _glab_json(
        "api", f"projects/{ctx.project_id}/pipelines/{pipeline_id}/jobs?per_page=100&include_retried=false"
    )
    if not data or not isinstance(data, list):
        return []
    return [Job.from_api(j) for j in data]


def get_job(ctx: PipelineContext, job_id: int) -> Job | None:
    """Get a single job's current state."""
    data = _glab_json("api", f"projects/{ctx.project_id}/jobs/{job_id}")
    if data:
        return Job.from_api(data)
    return None


def play_job(ctx: PipelineContext, job_id: int) -> Job | None:
    """Play a manual job."""
    data = _glab_json("api", "-X", "POST", f"projects/{ctx.project_id}/jobs/{job_id}/play")
    if data:
        return Job.from_api(data)
    return None


def retry_job(ctx: PipelineContext, job_id: int) -> Job | None:
    """Retry a failed or skipped job."""
    data = _glab_json("api", "-X", "POST", f"projects/{ctx.project_id}/jobs/{job_id}/retry")
    if data:
        return Job.from_api(data)
    return None


def get_environment_url(ctx: PipelineContext, env_name: str) -> str:
    """Get the external URL for a GitLab environment."""
    data = _glab_json("api", f"projects/{ctx.project_id}/environments?search={env_name}")
    if data and isinstance(data, list) and data:
        return str(data[0].get("external_url", ""))
    return ""
