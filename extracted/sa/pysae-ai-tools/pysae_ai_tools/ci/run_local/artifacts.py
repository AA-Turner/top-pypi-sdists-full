"""Download the input artifacts a job needs, into the local working directory.

Mirrors GitLab's resolution: an explicit ``dependencies:`` list wins; otherwise
the artifacts of the job's ``needs:`` are pulled. We deliberately do *not*
reproduce the "all jobs from earlier stages" default (no ``needs``/``deps``) —
it is too broad to be useful locally, so that case is logged and skipped.
"""

import io
import zipfile
from pathlib import Path

from ..common.glab import run_glab_bytes
from ..run.gitlab_api import PipelineContext, find_pipeline, list_jobs
from .models import ResolvedJob


def _source_job_names(job: ResolvedJob) -> list[str]:
    if job.dependencies is not None:
        return job.dependencies
    return job.needs


def download_inputs(
    *,
    job: ResolvedJob,
    project_id: str,
    pipeline_id: str,
    source_branch: str,
    mr_iid: str,
    workdir: Path,
    warnings: list[str],
) -> list[str]:
    """Fetch and unzip the artifacts of the job's input jobs into ``workdir``."""
    names = _source_job_names(job)
    if not names:
        return []

    ctx = PipelineContext(
        project_id=project_id,
        pipeline_id=pipeline_id,
        mr_iid=mr_iid,
        source_branch=source_branch,
    )
    pipeline = find_pipeline(ctx)
    if not pipeline:
        warnings.append(
            f"No pipeline found to source artifacts for {names} — run without inputs (use --no-artifacts to silence)."
        )
        return []

    jobs = list_jobs(ctx, pipeline.id)
    # Keep the highest job id per name (latest run of that job).
    by_name: dict[str, int] = {}
    for j in sorted(jobs, key=lambda x: x.id):
        by_name[j.name] = j.id

    downloaded: list[str] = []
    for name in names:
        job_id = by_name.get(name)
        if job_id is None:
            warnings.append(f"Input job '{name}' not found in pipeline #{pipeline.id} — its artifacts were skipped.")
            continue
        content = run_glab_bytes("api", f"projects/{project_id}/jobs/{job_id}/artifacts")
        if content is None:
            warnings.append(f"Could not download artifacts of '{name}' (job #{job_id}) — skipped.")
            continue
        try:
            with zipfile.ZipFile(io.BytesIO(content)) as zf:
                zf.extractall(workdir)
        except zipfile.BadZipFile:
            warnings.append(f"Artifacts archive of '{name}' (job #{job_id}) is not a valid zip — skipped.")
            continue
        downloaded.append(name)

    return downloaded
