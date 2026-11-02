"""JobKind protocol and its registry keyed by Kind: run a job's payload, its serial lock, how progress starts."""

from __future__ import annotations
from probe.foundation.compat.compat import StrEnum


class Kind(StrEnum):
    TRANSCRIPTS = "transcripts"
    FOLDER = "folder"


def _dispatch(kind: str, payload: dict, progress):
    if kind == Kind.TRANSCRIPTS:
        from ..transcripts.background import run_background_job
        return run_background_job(payload, progress=progress)
    from ..folder.coverage.coverage import CoverageError
    from ..folder.flow.background_job import run_background_job

    # Only when there is one: a source tree without the meter's module has a
    # folder lane that takes no meter either.
    metered = {"meter": _runner._attempt_meter} if _runner._attempt_meter is not None else {}
    try:
        return run_background_job(payload, progress=progress, **metered)
    except CoverageError as exc:
        raise JobError(str(exc)) from exc
from probe.cli.imports.jobs.errors import JobError  # noqa: E402 -- pieces need each other; the front door loads this one first
# runner rebinds it (`global`) as a job runs: read it there, never a copy taken at import.
from probe.cli.imports.jobs import runner as _runner  # noqa: E402 -- pieces need each other; the front door loads this one first
