"""Reusable user-facing copy for the dlt runtime CLI."""

from typing import Final


# Friendly one-liner per TriggerJob status.
# See `dlt_runtime_common.schemas.TriggerStatus` for the canonical enum.
# `skipped_concurrency_limit` here holds the generic (concurrency > 1) copy;
# the concurrency==1 case is `TRIGGER_CONCURRENCY_ONE_MESSAGE` below.
TRIGGER_STATUS_MESSAGES: Final[dict[str, str]] = {
    "skipped_concurrency_limit": (
        "Concurrency limit reached for this job — another run is already active."
    ),
    "skipped_org_concurrency_limit": (
        "Your organization has reached its maximum number of concurrent runs."
        " Cancel another run or upgrade your plan."
    ),
    "skipped_minutes_limit": (
        "Your organization has reached its compute-minutes limit for this billing"
        " period. Upgrade your plan to continue."
    ),
    "skipped_trial_expired": (
        "Your organization's trial has ended. Upgrade your plan to keep running jobs."
    ),
    "skipped_fresh": "Skipped — the job is already fresh.",
    "skipped_upstream_pending": (
        "Waiting on upstream job(s) being re-run in this batch — this job will run"
        " automatically when they finish."
    ),
    "skipped_out_of_interval": (
        "Trigger time is outside the script's configured interval window"
        " (interval_start / interval_end)."
    ),
    "skipped_already_covered": "A previous run already covers this interval.",
}


# concurrency==1 (the common default) reads more naturally as a singular
# statement than the generic "concurrency limit reached" copy.
TRIGGER_CONCURRENCY_ONE_MESSAGE: Final[str] = (
    "An instance of this job is already running."
)


# Suggestion lines printed after a `skipped_concurrency_limit` message.
# Each entry is an f-string template; format with `.format(job_ref=...)`.
TRIGGER_CONCURRENCY_SUGGESTIONS: Final[tuple[str, ...]] = (
    "  dlt runtime cancel {job_ref}              — cancel the running instance and retry",
    "  dlt runtime logs {job_ref} --follow       — follow the running instance's logs",
    "  dlt runtime job-run {job_ref} info        — show info on the running run",
)


# Extra line for interactive jobs (notebooks, marimo apps, ...) — points at
# the already-running instance's web UI so the user can pick up where they
# left off without restarting.
TRIGGER_CONCURRENCY_OPEN_LINE: Final[str] = "  Show the running instance: {url}"


# Suggestion line printed after a `skipped_fresh` message.
# Reason: --refresh bypasses the freshness check on this job, but it can
# cascade and re-run upstream jobs whose freshness is still satisfied.
TRIGGER_REFRESH_HINT: Final[str] = (
    "  Re-run with --refresh to bypass the freshness check."
    " Note: --refresh may cascade and re-run upstream jobs."
)
