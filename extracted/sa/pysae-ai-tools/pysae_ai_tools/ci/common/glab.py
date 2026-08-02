"""CI-specific glab helpers: project/pipeline/job id resolution via ``detect_context``.

The low-level ``glab`` invocation now lives in the shared
:mod:`...common.glab.runner`. This module keeps a thin ``run_glab`` compat shim
(the historical ``str | None`` contract the ``ci`` commands consume) and the
CI-only :func:`resolve_target`, which depends on ``detect_context``.
"""

import sys
from dataclasses import dataclass

from ...common.glab.runner import glab_api as glab_api
from ...common.glab.runner import run_glab as _run_glab_result
from ...common.glab.runner import run_glab_bytes as run_glab_bytes
from ...internal.detect_context.detect import DetectArgs, detect


def run_glab(*args: str, timeout: int = 30) -> str | None:
    """Run a glab command and return its stdout, or ``None`` on failure.

    Compat wrapper over :func:`...common.glab.runner.run_glab` preserving the
    ``str | None`` contract (and the stderr diagnostic) the ci commands rely on.
    """
    res = _run_glab_result(*args, timeout=timeout)
    if not res.ok:
        if res.stderr:
            print(f"glab error: {res.stderr}", file=sys.stderr)
        return None
    return res.stdout


@dataclass
class CiTarget:
    """Resolved project / pipeline / job identifiers."""

    project_id: str = ""
    pipeline_id: str = ""
    job_id: str = ""


def resolve_target(
    *,
    project_id: str = "",
    pipeline_id: str = "",
    job_id: str = "",
    mr_iid: str = "",
    refs: list[str] | None = None,
) -> CiTarget:
    """Fill in missing ids via detect_context (job/pipeline URLs, MR, CI env)."""
    target = CiTarget(project_id=project_id, pipeline_id=pipeline_id, job_id=job_id)
    if target.project_id and (target.pipeline_id or target.job_id):
        return target
    try:
        detected = detect(
            DetectArgs(
                refs=refs or [],
                mr_iid=mr_iid,
                job_id=job_id,
                pipeline_id=pipeline_id,
            )
        )
    except Exception as exc:  # detect_context is best-effort
        print(f"detect_context failed: {exc}", file=sys.stderr)
        return target
    target.project_id = target.project_id or detected.project_id
    target.pipeline_id = target.pipeline_id or detected.pipeline_id
    target.job_id = target.job_id or detected.job_id
    return target
