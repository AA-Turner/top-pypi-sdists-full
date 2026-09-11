"""Reusable user-facing copy for the dlt runtime CLI."""

# Python internals
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
        "Your organization has used all available runtime minutes."
        " Upgrade your plan to continue."
    ),
    "skipped_trial_expired": (
        "Your organization's trial has ended. Upgrade your plan to keep running jobs."
    ),
    "skipped_fresh": (
        "Skipped - job cannot be started due to one or more upstream"
        " freshness checks failing"
    ),
    "skipped_upstream_pending": (
        "Waiting on upstream job(s) being re-run in this batch — this job will run"
        " automatically when they finish."
    ),
    "skipped_out_of_interval": (
        "Trigger time is outside the script's configured interval window"
        " (interval_start / interval_end)."
    ),
    "skipped_already_covered": "A previous run already covers this interval.",
    "skipped_paused": (
        "This schedule is paused, so the scheduler did not start this run."
        " Resume the schedule to let it run again."
    ),
    "skipped_workspace_archived": (
        "The workspace is archived and read-only. Unarchive it to start new runs."
    ),
}


# concurrency==1 (the common default) reads more naturally as a singular
# statement than the generic "concurrency limit reached" copy.
TRIGGER_CONCURRENCY_ONE_MESSAGE: Final[str] = (
    "An instance of this job is already running."
)


# Pause / resume of a job's schedule. Mirrors the web copy in
# `clients/web/src/lib/strings.ts` — keep them consistent.
JOB_PAUSED_LIST_TAG: Final[str] = "paused"
JOB_PAUSE_MESSAGE: Final[str] = (
    "Scheduled runs for job `{job_ref}` are paused until you resume schedule"
)
JOB_RESUME_MESSAGE: Final[str] = (
    "Scheduled runs for job `{job_ref}` are resumed. The first run covers the whole period it"
    " was paused for."
)
# The API is idempotent, so a no-op is reported rather than failed.
JOB_ALREADY_PAUSED_MESSAGE: Final[str] = (
    "Scheduled runs for job `{job_ref}` are already paused"
)
JOB_NOT_PAUSED_MESSAGE: Final[str] = "Scheduled runs for job `{job_ref}` are not paused"
JOB_NO_SELECTOR_MATCH: Final[str] = "No jobs matched the selector(s)"
JOB_SCHEDULE_TOGGLE_FAILED: Final[str] = (
    "Failed to {action} scheduled runs for: {job_refs}"
)


# Suggestion lines printed after a `skipped_concurrency_limit` message.
# Each entry is an f-string template; format with `.format(job_ref=...)`.
TRIGGER_CONCURRENCY_SUGGESTIONS: Final[tuple[str, ...]] = (
    "  dlthub job cancel {job_ref}              — cancel the running instance and retry",
    "  dlthub job logs {job_ref} --follow       — follow the running instance's logs",
    "  dlthub job runs info {job_ref}        — show info on the running run",
)


# Extra line for interactive jobs (notebooks, marimo apps, ...) — points at
# the already-running instance's web UI so the user can pick up where they
# left off without restarting.
TRIGGER_CONCURRENCY_OPEN_LINE: Final[str] = "  Show the running instance: {url}"


# Ctrl+C during device-flow login. `{device_code}` is interpolated at render time.
LOGIN_CANCELLED_RESUME_HINT: Final[str] = (
    "\nLogin cancelled. To resume later, run:\n  dlthub login --resume {device_code}"
)


# Non-interactive workspace picker: header + per-org command lines.
# `{org_id}` is interpolated at render time; `<workspace_uuid>` and `<new-name>`
# stay as literal placeholders for the user to substitute.
NON_INTERACTIVE_PICKER_HEADER: Final[str] = (
    "Cannot pick a workspace non-interactively. Re-run with one of the commands below."
)
NON_INTERACTIVE_PICKER_SELECT_LINE: Final[str] = (
    "Select:  dlthub workspace connect <workspace_uuid> --org-id {org_id}"
)
NON_INTERACTIVE_PICKER_CREATE_LINE: Final[str] = (
    "Create:  dlthub workspace connect <new-name> --create --org-id {org_id}"
)


# Tail appended to every error that requires unpinning organization_id.
UNPIN_ORG_REMEDIATION: Final[str] = (
    "Remove RUNTIME__ORGANIZATION_ID or organization_id under [runtime] in"
    " your dlt config to switch organizations, then run `connect` again."
)

# `--org-id <id>` failed validation against the user's active orgs list.
ORG_ID_NOT_ACTIVE: Final[str] = (
    "--org-id '{org_id}' is not one of your active organizations. Valid: {valid}."
)

# Pinned `organization_id` refers to an org the user is no longer in.
PINNED_ORG_NOT_ACCESSIBLE: Final[str] = (
    "Organization '{pinned_org_id}' pinned in your dlt config is not"
    " accessible. {remediation} Or check `dlthub workspace list` for"
    " membership."
)

# `--org-id <id>` disagrees with the org pinned in config.toml.
ORG_ID_CONFLICTS_WITH_PIN: Final[str] = (
    "--org-id '{org_id}' conflicts with the organization pinned in"
    " your dlt config ('{pinned_label}'). {remediation}"
)

# Resolved workspace lives in a different org than the one pinned / in scope.
WORKSPACE_BELONGS_TO_OTHER_ORG: Final[str] = (
    "Workspace '{ws_name}' belongs to organization '{ws_org}', not the"
    " one in scope ('{effective_label}'). {remediation}"
)

# Positional `workspace connect <name>` doesn't resolve — refuse to silently create.
WORKSPACE_NAME_NOT_FOUND: Final[str] = (
    "Workspace '{name}' not found among your owned workspaces. Pass"
    " `dlthub workspace connect {name} --create` to create a new workspace."
)

# User declined the interactive create-on-miss prompt.
WORKSPACE_CONNECT_CREATE_DECLINED: Final[str] = (
    "Workspace '{name}' not found among your owned workspaces and creation"
    " was cancelled. Pass `dlthub workspace connect {name} --create` to create"
    " a new workspace."
)

# `workspace connect <name> --create` was used but a workspace with that name already exists.
WORKSPACE_NAME_ALREADY_EXISTS: Final[str] = (
    "Workspace '{name}' already exists in organization '{org_label}'."
    " Drop `--create` to connect to the existing workspace."
)

# `--create` was set but no positional workspace name was given.
WORKSPACE_CREATE_REQUIRES_NAME: Final[str] = (
    "`--create` requires a workspace name. Run `dlthub workspace connect"
    " <name> --create`."
)

NOT_CONNECTED_TO_WORKSPACE: Final[str] = (
    "Not connected to workspace. Run `dlthub workspace connect <name>` first."
)

WORKSPACE_API_KEY_NO_WORKSPACE: Final[str] = (
    "A workspace API key is in use, but no workspace is connected. Run"
    " `dlthub workspace connect` to connect to the key's workspace."
)

# The pin may come from RUNTIME__WORKSPACE_ID, which `workspace connect` cannot rewrite.
WORKSPACE_API_KEY_PIN_MISMATCH: Final[str] = (
    "A workspace API key is in use, but the configured workspace ID"
    " {workspace_id} does not match the key's workspace"
    " {bound_workspace_id}. Update RUNTIME__WORKSPACE_ID or workspace_id"
    " under [runtime] in your dlt config, or remove it and run `dlthub"
    " workspace connect`."
)

WORKSPACE_API_KEY_WRONG_WORKSPACE: Final[str] = (
    "This workspace API key is bound to workspace '{bound_workspace_name}'"
    " ({bound_workspace_id}) and cannot connect to '{workspace}'."
)

WORKSPACE_API_KEY_WRONG_ORG: Final[str] = (
    "This workspace API key is bound to organization '{key_org_name}'"
    " ({key_org_id}) and cannot connect in organization '{org_id}'."
)

WORKSPACE_API_KEY_ORG_MISMATCH: Final[str] = (
    "A workspace API key is in use, but the pinned organization ID"
    " {organization_id} does not match the key's organization"
    " '{key_org_name}' ({key_org_id}). Remove RUNTIME__ORGANIZATION_ID or"
    " organization_id under [runtime] in your dlt config to use this key."
)

# Rejected up front so every later branch can assume one of the two known kinds.
API_KEY_UNRECOGNIZED: Final[str] = (
    "Unrecognized API key format. Personal keys start with `dlt_u_` and"
    " workspace keys with `dlt_sa_`. Check the configured api_key."
)

# An API key is a non-interactive credential, so it must never open the picker.
PERSONAL_API_KEY_CONNECT_REQUIRES_NAME: Final[str] = (
    "API key mode requires an explicit workspace argument. Run `dlthub"
    " workspace connect <name>` or `dlthub workspace connect <name>"
    " --create`."
)

WORKSPACE_API_KEY_CANNOT_CREATE: Final[str] = (
    "A workspace API key cannot create workspaces. Create one in the dltHub"
    " web app, switch to a personal API key, or run `dlthub login`."
)

WORKSPACE_API_KEY_NO_ACCESS: Final[str] = (
    "This API key has no accessible workspace. Its workspace may have been archived."
)

# A job selector / name / ref did not resolve locally or on the server.
JOB_SELECTOR_NOT_FOUND: Final[str] = (
    "Job '{selector}' not found. Run `dlthub job list` to see available"
    " selectors, or pass a full `jobs.<section>.<name>` ref / UUID."
)

# A secret with no value is unreadable afterwards, so it can never be diagnosed.
VARIABLE_SECRET_NEEDS_VALUE: Final[str] = (
    "A secret needs a value. Pass --value, or type one when prompted."
)
