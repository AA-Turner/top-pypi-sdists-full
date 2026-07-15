"""Evaluation subcommands for the cyclopts CLI."""

import contextlib
import fnmatch
import json
import typing as t
from pathlib import Path

import cyclopts
import yaml
from rich.table import Table

from dreadnode.app.cli.args import PlatformScopeArgs
from dreadnode.app.cli.shared import (
    _FLAG_STATUS,
    _collect_pages,
    _continuation,
    _fmt_duration,
    _fmt_id,
    _fmt_timestamp,
    _hint,
    _label,
    _print_json,
    _project_row,
    _render,
    _render_list,
    _short_id,
    _wait_for_job,
    confirm_destructive,
    console,
    merge_env_model_overrides,
    parse_env_model_overrides,
    print_link,
)
from dreadnode.app.model_catalog import resolve_model

cli = cyclopts.App(
    name="evaluation",
    help=(
        "Batch evaluation of agents against security tasks"
        " \u2014 measure capability, track regressions, and compare models."
    ),
)

# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

CleanupPolicy = t.Literal["always", "on_success"]

EvaluationStatus = t.Literal["queued", "running", "completed", "partial", "failed", "cancelled"]

EvaluationItemStatus = t.Literal[
    "queued",
    "claiming",
    "provisioning",
    "agent_running",
    "agent_finished",
    "verifying",
    "passed",
    "failed",
    "timed_out",
    "cancelled",
    "infra_error",
]

_TERMINAL_JOB_STATUSES = {"completed", "partial", "failed", "cancelled"}

# Block characters for progress bar (constants for Python 3.11 f-string compat)
_BAR_FULL = "\u2588"  # █
_BAR_MED = "\u2593"  # ▓
_BAR_LIGHT = "\u2591"  # ░


def _print_eval_link(profile: t.Any, eval_id: str) -> None:
    """Print a web link to an evaluation, if scope info is available."""
    org = getattr(profile, "org_key", None) or getattr(profile, "organization", None)
    ws = getattr(profile, "workspace_key", None) or getattr(profile, "workspace", None)
    if not org or not ws:
        return
    query: dict[str, str] = {"workspace": ws}
    proj = getattr(profile, "project_key", None) or getattr(profile, "project", None)
    if proj:
        query["project"] = proj
    query["eval"] = eval_id
    print_link(profile.url, f"{org}/evaluation", **query)


# ---------------------------------------------------------------------------
# Color helpers — single source of truth for status → color mapping
# ---------------------------------------------------------------------------

# Semantic status colors used for dots, count text, and table rendering.
# Uses the same mapping everywhere to avoid dot/text color mismatches.
_ITEM_STATUS_COLORS: dict[str, str] = {
    # Terminal — good
    "completed": "green",
    "passed": "green",
    # Terminal — bad
    "failed": "red",
    "timed_out": "red",
    "infra_error": "red",
    "cancelled": "dim",
    # In-progress
    "running": "yellow",
    "partial": "yellow",
    "claiming": "yellow",
    "provisioning": "yellow",
    "agent_running": "yellow",
    "agent_finished": "yellow",
    "verifying": "yellow",
    # Waiting
    "queued": "blue",
    "pending": "blue",
}


def _eval_status_color(status: str) -> str:
    """Return a Rich color for any evaluation or item status."""
    return _ITEM_STATUS_COLORS.get(status, "dim")


def _status_dot(status: str) -> str:
    """Colored Unicode dot for a status value."""
    color = _eval_status_color(status)
    return f"[{color}]\u25cf[/{color}]"


def _pass_rate_color(rate: float) -> str:
    """Return a Rich color encoding the quality of a pass rate (0.0-1.0)."""
    pct = rate * 100
    if pct >= 80:
        return "green"
    if pct >= 50:
        return "yellow"
    return "red"


def _colored_pass_rate(rate: float | None) -> str:
    """Format a pass rate with semantic color. Returns dim '-' when unavailable."""
    if rate is None:
        return "[dim]-[/dim]"
    pct = rate * 100
    color = _pass_rate_color(rate)
    return f"[{color}]{pct:.0f}%[/{color}]"


def _fmt_delta(
    val_a: float | None,
    val_b: float | None,
    *,
    higher_is_better: bool = True,
    unit: str = "",
    precision: int = 0,
) -> str:
    """Format a numeric delta with green (improvement) or red (regression)."""
    if val_a is None or val_b is None:
        return "[dim]-[/dim]"
    diff = val_b - val_a
    if diff == 0:
        return f"[dim]{diff:{f'.{precision}f'}}{unit}[/dim]"
    sign = "+" if diff > 0 else ""
    improved = (diff > 0) == higher_is_better
    color = "green" if improved else "red"
    return f"[{color}]{sign}{diff:{f'.{precision}f'}}{unit}[/{color}]"


def _fmt_delta_pct(rate_a: float | None, rate_b: float | None) -> str:
    """Format a pass-rate delta as percentage points (e.g. ``+13.0pp``)."""
    if rate_a is None or rate_b is None:
        return "[dim]-[/dim]"
    return _fmt_delta(rate_a * 100, rate_b * 100, higher_is_better=True, unit="pp", precision=1)


def _parse_sample_ref(ref: str) -> tuple[str, str]:
    """Parse an ``EVAL_ID/SAMPLE_ID`` reference into its two parts."""
    if "/" not in ref:
        raise ValueError(f"Expected EVAL_ID/SAMPLE_ID (e.g. 9ab81fc1/75e4914f), got '{ref}'")
    eval_part, sample_part = ref.split("/", 1)
    if not eval_part or not sample_part:
        raise ValueError(f"Expected EVAL_ID/SAMPLE_ID (e.g. 9ab81fc1/75e4914f), got '{ref}'")
    return eval_part, sample_part


def _fmt_progress(counts: dict[str, t.Any]) -> str:
    """Build a progress string like '45/100' from item counts."""
    finished = (
        int(counts.get("passed", 0))
        + int(counts.get("failed", 0))
        + int(counts.get("timed_out", 0))
        + int(counts.get("cancelled", 0))
        + int(counts.get("infra_error", 0))
    )
    total = finished + (
        int(counts.get("queued", 0))
        + int(counts.get("claiming", 0))
        + int(counts.get("provisioning", 0))
        + int(counts.get("agent_running", 0))
        + int(counts.get("agent_finished", 0))
        + int(counts.get("verifying", 0))
    )
    if total == 0:
        return "-"
    return f"{finished}/{total}"


def _calc_pass_rate(counts: dict[str, t.Any]) -> float | None:
    """Calculate pass rate from item counts. Returns None when undecided."""
    passed = int(counts.get("passed", 0))
    failed = int(counts.get("failed", 0))
    total_decided = passed + failed
    if total_decided == 0:
        return None
    return passed / total_decided


def _progress_bar(counts: dict[str, t.Any], width: int = 20) -> str:
    """Build a colored text progress bar from item counts."""
    passed = int(counts.get("passed", 0))
    failed = int(counts.get("failed", 0))
    timed_out = int(counts.get("timed_out", 0))
    infra_error = int(counts.get("infra_error", 0))
    cancelled = int(counts.get("cancelled", 0))
    in_progress = (
        int(counts.get("queued", 0))
        + int(counts.get("claiming", 0))
        + int(counts.get("provisioning", 0))
        + int(counts.get("agent_running", 0))
        + int(counts.get("agent_finished", 0))
        + int(counts.get("verifying", 0))
    )
    total = passed + failed + timed_out + infra_error + cancelled + in_progress
    if total == 0:
        return f"[dim]{_BAR_LIGHT * width}[/]"

    def _fill(count: int) -> int:
        return max(1, int(count / total * width)) if count > 0 else 0

    bar = ""
    remaining = width

    for count, colour, char in [
        (passed, "green", _BAR_FULL),
        (failed, "red", _BAR_FULL),
        (timed_out, "yellow", _BAR_FULL),
        (infra_error, "red", _BAR_MED),
        (cancelled, "dim", _BAR_MED),
    ]:
        if count > 0:
            filled = min(_fill(count), remaining)
            bar += f"[{colour}]{char * filled}[/]"
            remaining -= filled

    if in_progress > 0 and remaining > 0:
        filled = min(_fill(in_progress), remaining)
        bar += f"[blue]{_BAR_LIGHT * filled}[/]"
        remaining -= filled

    if remaining > 0:
        bar += f"[dim]{_BAR_LIGHT * remaining}[/]"

    return bar


# ---------------------------------------------------------------------------
# Summary functions
# ---------------------------------------------------------------------------


_EVALUATION_LIST_ROW_FIELDS: tuple[str, ...] = (
    "status",
    "job_status",
    "model",
    "capability",
    "project_id",
    "item_counts",
    "queued_at",
    "started_at",
    "completed_at",
    "created_at",
    "updated_at",
)


_EVALUATION_SAMPLE_LIST_ROW_FIELDS: tuple[str, ...] = (
    "evaluation_id",
    "position",
    "status",
    "item_status",
    "task_name_snapshot",
    "task_ref",
    "error",
    "started_at",
    "completed_at",
    "created_at",
)


def _summarize_evaluation(p: dict[str, t.Any]) -> str:
    """One-line evaluation summary for list/create/cancel/retry output."""
    short = _short_id(str(p.get("id", "unknown")))
    job_status = p.get("job_status", p.get("status", "unknown"))
    name = p.get("name", "unnamed")
    model = p.get("model") or ""
    counts = p.get("item_counts", {})
    progress = _fmt_progress(counts)
    rate = _calc_pass_rate(counts)
    duration = _fmt_duration(
        p.get("started_at") or p.get("queued_at"),
        p.get("completed_at"),
    )

    color = _eval_status_color(job_status)
    parts = [
        short,
        _status_dot(job_status),
        f"[{color}]{job_status}[/{color}]",
        f"[bold]{name}[/bold]",
    ]
    if progress != "-":
        parts.append(f"[dim]{progress}[/dim]")
    if rate is not None:
        parts.append(_colored_pass_rate(rate))
    if duration != "-":
        parts.append(f"[dim]{duration}[/dim]")
    if model:
        parts.append(f"[dim]{model}[/dim]")
    return "  ".join(parts)


def _print_skipped_members(skipped: t.Any) -> None:
    """Surface TSS-EVAL-004 skipped members on a task-set eval create.

    ``skipped_members`` rides the create response only and is informational —
    the evaluation runs on the resolved subset. Cross-org members are reported
    as ``not_found`` under the non-disclosure rule (TSS-RES-004).
    """
    if not isinstance(skipped, list) or not skipped:
        return
    console.print(f"[yellow]Skipped {len(skipped)} unresolvable member(s):[/yellow]")
    for member in skipped:
        if not isinstance(member, dict):
            continue
        name = member.get("task_name", "unknown")
        version = member.get("task_version")
        reason = member.get("reason", "unresolvable")
        ref = f"{name}@{version}" if version else name
        console.print(f"  [dim]-[/dim] {ref} [dim]({reason})[/dim]")


# ---------------------------------------------------------------------------
# Manifest loading (preserved from original)
# ---------------------------------------------------------------------------


def _is_string_list(value: object) -> t.TypeGuard[list[str]]:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _coerce_task_names(value: object, *, field_name: str) -> list[str]:
    if isinstance(value, str):
        return [value]
    if _is_string_list(value):
        return value
    raise TypeError(f"{field_name} must be a string or list of strings")


def _load_evaluation_manifest(path: Path) -> dict[str, t.Any]:
    resolved = path.expanduser()
    if resolved.is_dir():
        resolved = resolved / "evaluation.yaml"
    if not resolved.exists():
        raise FileNotFoundError(f"No evaluation.yaml found at {resolved}")

    parsed = yaml.safe_load(resolved.read_text())
    if parsed is None:
        return {}
    if not isinstance(parsed, dict):
        raise TypeError("evaluation.yaml must contain a YAML mapping")

    request = dict(parsed)

    alias_fields = [field for field in ("task", "tasks", "task_names") if field in request]
    if len(alias_fields) > 1:
        raise ValueError("evaluation.yaml may specify only one of 'task', 'tasks', or 'task_names'")
    if "task" in request:
        request["task_names"] = _coerce_task_names(request.pop("task"), field_name="task")
    elif "tasks" in request:
        request["task_names"] = _coerce_task_names(request.pop("tasks"), field_name="tasks")
    elif "task_names" in request:
        request["task_names"] = _coerce_task_names(request["task_names"], field_name="task_names")

    # TSS-EVAL-010 — task_set is mutually exclusive with task/tasks/task_names/dataset.
    if "task_set" in request:
        if not isinstance(request["task_set"], str):
            raise TypeError("task_set must be a string '<org>/<name>'")
        conflicts = [field for field in ("task_names", "dataset") if field in request]
        if conflicts:
            raise ValueError(
                "evaluation.yaml may specify only one of 'task_set', "
                "'task'/'tasks'/'task_names', or 'dataset'"
            )

    if "project" in request and "project_id" in request:
        raise ValueError("evaluation.yaml may specify only one of 'project' or 'project_id'")
    if "project" in request and not isinstance(request["project"], str):
        raise TypeError("project must be a string")
    if "project_id" in request and not isinstance(request["project_id"], str):
        raise TypeError("project_id must be a string")

    return request


def _is_secret_selector_pattern(selector: str) -> bool:
    return any(char in selector for char in "*?[")


def _resolve_secret_ids(api: t.Any, selectors: list[str]) -> list[str] | None:
    if not selectors:
        return None

    secrets_response = api.list_secrets()
    raw_secrets = (
        secrets_response.get("secrets", [])
        if isinstance(secrets_response, dict)
        else getattr(secrets_response, "secrets", [])
    )

    ordered_secrets: list[tuple[str, str]] = []
    secrets_by_name: dict[str, str] = {}
    for secret in raw_secrets:
        name = getattr(secret, "name", None)
        secret_id = getattr(secret, "id", None)
        if not isinstance(name, str) or not isinstance(secret_id, str):
            continue
        normalized_name = name.upper()
        ordered_secrets.append((normalized_name, secret_id))
        secrets_by_name[normalized_name] = secret_id

    resolved_ids: list[str] = []
    seen_ids: set[str] = set()
    missing_exact: list[str] = []

    for raw_selector in selectors:
        selector = raw_selector.strip().upper()
        if not selector:
            continue

        if _is_secret_selector_pattern(selector):
            for name, secret_id in ordered_secrets:
                if not fnmatch.fnmatchcase(name, selector) or secret_id in seen_ids:
                    continue
                resolved_ids.append(secret_id)
                seen_ids.add(secret_id)
            continue

        secret_id = secrets_by_name.get(selector)
        if secret_id is None:
            missing_exact.append(selector)
            continue
        if secret_id in seen_ids:
            continue
        resolved_ids.append(secret_id)
        seen_ids.add(secret_id)

    if missing_exact:
        if len(missing_exact) == 1:
            raise ValueError(f"Secret not found: {missing_exact[0]}")
        raise ValueError("Secrets not found: " + ", ".join(sorted(missing_exact)))

    return resolved_ids or None


# ---------------------------------------------------------------------------
# Wait helper
# ---------------------------------------------------------------------------


def _wait_for_evaluation(
    api: t.Any,
    *,
    org: str,
    workspace: str,
    evaluation_id: str,
    poll_interval_sec: float,
    timeout_sec: float | None,
) -> dict[str, t.Any]:
    def poll() -> dict[str, t.Any]:
        job = api.get_evaluation_job(org, workspace, evaluation_id)
        # _wait_for_job checks dict["status"]; evaluation API returns "job_status"
        job["status"] = job.get("job_status", job.get("status"))
        return job

    return _wait_for_job(
        poll,
        job_id=evaluation_id,
        label="evaluation",
        poll_interval_sec=poll_interval_sec,
        timeout_sec=timeout_sec,
    )


# ---------------------------------------------------------------------------
# Render helpers for `get` detail view
# ---------------------------------------------------------------------------


def _render_get_detail(job: dict[str, t.Any], analytics: dict[str, t.Any] | None) -> None:
    """Render the rich detail output for the ``get`` command."""
    job_status = job.get("job_status", job.get("status", "unknown"))
    name = job.get("name", "unnamed")
    eval_id = str(job.get("id", "unknown"))
    counts = job.get("item_counts", {})

    # Header — status dot + status text carry the color; name is bold neutral
    color = _eval_status_color(job_status)
    console.print(f"{_status_dot(job_status)} [{color}]{job_status}[/{color}]  [bold]{name}[/bold]")
    console.print(f"{_label('ID')}{_fmt_id(eval_id)}")
    console.print()

    # Config — one row per field for readability
    if job.get("model"):
        console.print(f"{_label('Model')}{job['model']}")
    if job.get("capability"):
        console.print(f"{_label('Capability')}[cyan]{job['capability']}[/cyan]")
    req_conc = job.get("requested_concurrency")
    eff_conc = job.get("effective_concurrency")
    if req_conc is not None:
        conc_str = str(req_conc)
        if eff_conc is not None and eff_conc != req_conc:
            conc_str += f" [dim](eff: {eff_conc})[/dim]"
        console.print(f"{_label('Concurrency')}{conc_str}")
    if job.get("task_timeout_sec"):
        console.print(f"{_label('Timeout')}{job['task_timeout_sec']}s")
    if job.get("cleanup_policy"):
        console.print(f"{_label('Cleanup')}{job['cleanup_policy']}")
    console.print()

    # Progress bar — pass rate gets semantic color
    bar = _progress_bar(counts, width=30)
    progress = _fmt_progress(counts)
    rate = _calc_pass_rate(counts)
    rate_str = _colored_pass_rate(rate) if rate is not None else "[dim]-[/dim]"
    console.print(f"{_label('Progress')}{bar}  [dim]{progress}[/dim]  pass: {rate_str}")

    # Non-zero status counts — same color source as the dots
    status_parts: list[str] = []
    for field_name in [
        "passed",
        "failed",
        "timed_out",
        "infra_error",
        "cancelled",
        "agent_running",
        "provisioning",
        "queued",
        "claiming",
        "agent_finished",
        "verifying",
    ]:
        count = int(counts.get(field_name, 0))
        if count > 0:
            fc = _eval_status_color(field_name)
            status_parts.append(f"[{fc}]{field_name}={count}[/{fc}]")
    if status_parts:
        console.print(f"{_continuation()}{'  '.join(status_parts)}")
    console.print()

    # Timing — timestamps are dim (reference data), elapsed is normal
    console.print(f"{_label('Queued')}[dim]{_fmt_timestamp(job.get('queued_at'))}[/dim]")
    if job.get("started_at"):
        console.print(f"{_label('Started')}[dim]{_fmt_timestamp(job.get('started_at'))}[/dim]")
    if job.get("completed_at"):
        console.print(f"{_label('Completed')}[dim]{_fmt_timestamp(job.get('completed_at'))}[/dim]")
    duration = _fmt_duration(
        job.get("started_at") or job.get("queued_at"),
        job.get("completed_at"),
    )
    console.print(f"{_label('Elapsed')}{duration}")

    # Results (from analytics, when available)
    if analytics:
        console.print()
        pr = analytics.get("pass_rate")
        passed_c = analytics.get("passed_count", 0)
        failed_c = analytics.get("failed_count", 0)
        error_c = analytics.get("error_count", 0)

        # Headline: pass rate + ✓/✗ counts with semantic color
        parts = [_colored_pass_rate(pr)]
        if passed_c:
            parts.append(f"[green]\u2713 {passed_c} passed[/green]")
        if failed_c:
            parts.append(f"[red]\u2717 {failed_c} failed[/red]")
        if error_c:
            parts.append(f"[red]{error_c} errors[/red]")
        if not passed_c and not failed_c and not error_c:
            parts.append("[dim]no results[/dim]")
        console.print(f"{_label('Results')}{'  '.join(parts)}")

        snapshot = analytics.get("analytics_snapshot") or {}

        # Per-task breakdown
        task_breakdown = snapshot.get("task_breakdown", [])
        if isinstance(task_breakdown, list):
            for entry in task_breakdown:
                tname = entry.get("task_name", "unknown")
                tp = entry.get("passed_count", 0)
                ts = entry.get("total_samples", 0)
                tpr = entry.get("pass_rate")
                tpr_str = _colored_pass_rate(tpr)
                console.print(
                    f"{_continuation()}[cyan]{tname}[/cyan]  {tpr_str} [dim]({tp}/{ts})[/dim]"
                )

        # Duration percentiles
        durations = snapshot.get("runtime_durations_ms", {})
        if durations:
            p50 = durations.get("p50_ms") or durations.get("p50")
            p95 = durations.get("p95_ms") or durations.get("p95")
            d_max = durations.get("max_ms") or durations.get("max")
            dur_parts: list[str] = []
            if p50 is not None:
                dur_parts.append(f"p50={p50 / 1000:.0f}s")
            if p95 is not None:
                dur_parts.append(f"p95={p95 / 1000:.0f}s")
            if d_max is not None:
                dur_parts.append(f"max={d_max / 1000:.0f}s")
            if dur_parts:
                console.print(f"{_continuation()}[dim]durations: {'  '.join(dur_parts)}[/dim]")

    # Error
    error = job.get("error_summary")
    if error:
        console.print()
        console.print(f"{_label('Error')}[red]{error}[/red]")


# ---------------------------------------------------------------------------
# create
# ---------------------------------------------------------------------------


@cli.command()
def create(
    name: t.Annotated[
        str | None,
        cyclopts.Parameter(name="name"),
    ] = None,
    *,
    task: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(name="--task", negative_iterable=()),
    ] = None,
    task_set: t.Annotated[
        str | None,
        cyclopts.Parameter(name="--task-set"),
    ] = None,
    file: t.Annotated[
        Path | None,
        cyclopts.Parameter(name="--file"),
    ] = None,
    runtime_id: str | None = None,
    model: str | None = None,
    capability: str | None = None,
    engine: str | None = None,
    secret: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(name="--secret", negative_iterable=()),
    ] = None,
    concurrency: int | None = None,
    task_timeout_sec: int | None = None,
    max_steps: t.Annotated[
        int | None,
        cyclopts.Parameter(
            help=(
                "Maximum agent tool/generation steps per sample. "
                "Enforced via a headless session policy; the task timeout "
                "still applies as a wall-clock bound."
            ),
        ),
    ] = None,
    cleanup_policy: CleanupPolicy | None = None,
    judge_model: str | None = None,
    env_model: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(
            name="--env-model",
            help=(
                "Override a task ENVIRONMENT (defender) model by role: ROLE=MODEL_ID "
                "(e.g. --env-model blue=dn/claude-sonnet-4-6, repeatable). Distinct "
                "from --model (solver) and --judge-model. The role must be declared "
                "overridable in the task's models map."
            ),
            negative_iterable=(),
        ),
    ] = None,
    wait: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    poll_interval_sec: t.Annotated[
        float,
        cyclopts.Parameter(validator=cyclopts.validators.Number(gt=0)),
    ] = 10.0,
    timeout_sec: float | None = None,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Launch an evaluation against one or more security tasks.

    Builds the evaluation request from CLI flags, an evaluation.yaml
    manifest (``--file``), or both (flags override the manifest).
    Use ``--wait`` to block until the evaluation completes and print
    a results summary. When ``--model`` requires provider credentials,
    create fails fast if the required user Secrets are not configured.

    Args:
        name: Evaluation name (e.g. my-eval-v3). Optional when set in --file.
        task: Security task to evaluate on, NAME[@VERSION] or org/name@version
            (e.g. security-bandit-00 or acme/web-rce@1.2.0). Repeatable.
        task_set: Task set to expand into the evaluation, '<org>/<name>'
            (e.g. acme/apex-web). Mutually exclusive with --task. Members
            unresolvable under your visibility are skipped and reported.
        file: Path to evaluation.yaml request manifest.
        runtime_id: Runtime record ID for tracking; does not select a model.
        model: Model identifier (e.g. dn/gpt-5 or openai/gpt-4o-mini for BYOK).
            Required unless --capability provides one. Run
            `dn inference-model list` for platform models; pass any
            LiteLLM-compatible BYOK ID after configuring credentials.
        capability: Capability to load, NAME[@VERSION] or org/name@version
            (e.g. acme/web-security@1.0.0). Also pass --model if it has no
            entry-agent model. Run `dn capability list` to discover.
        engine: Loop-owner override for the agent under evaluation
            (e.g. claude-code). When omitted, the agent's declared engine
            (or native) is used. Requires the harness in the eval sandbox.
        secret: Secret selector to inject into evaluation sandboxes. Repeatable.
            Exact names are strict; glob selectors are best-effort. Run
            `dn secret list` to discover configured names.
        concurrency: Maximum concurrent evaluation samples.
        task_timeout_sec: Timeout per task in seconds.
        max_steps: Maximum agent tool/generation steps per sample.
            Enforced via a headless session policy; the task timeout still
            applies as a wall-clock bound.
        cleanup_policy: Sandbox cleanup policy.
        judge_model: Override the judge model for all tasks in this evaluation.
        wait: Block until the evaluation reaches a terminal state.
        poll_interval_sec: Seconds between status polls when --wait is set.
        timeout_sec: Maximum seconds to wait before timing out.
        as_json: Output as JSON.
    """
    request = _load_evaluation_manifest(file) if file else {}
    if name:
        request["name"] = name
    if model:
        request["model"] = resolve_model(model)
    if task:
        request["task_names"] = task
    if task_set:
        request["task_set"] = task_set
    if request.get("task_set") and (request.get("task_names") or request.get("dataset")):
        raise ValueError(
            "Provide only one of --task-set, --task, or a dataset — they are mutually exclusive."
        )
    if runtime_id:
        request["runtime_id"] = runtime_id
    if capability:
        request["capability"] = capability
    if engine:
        request["engine"] = engine
    if secret is not None:
        request["_secret_selectors"] = secret
    if concurrency is not None:
        request["concurrency"] = concurrency
    if task_timeout_sec is not None:
        request["task_timeout_sec"] = task_timeout_sec
    if max_steps is not None:
        request["max_steps"] = max_steps
    if cleanup_policy:
        request["cleanup_policy"] = cleanup_policy
    if judge_model:
        request["judge_model"] = resolve_model(judge_model)
    parsed_env_models = parse_env_model_overrides(env_model, resolve=resolve_model)
    merged_env_models = merge_env_model_overrides(request.get("model_overrides"), parsed_env_models)
    if merged_env_models is not None:
        request["model_overrides"] = merged_env_models

    if not request.get("name"):
        raise ValueError(
            "dn evaluation create requires a name. Pass one positionally or in --file."
        )
    if not request.get("model") and not request.get("capability"):
        raise ValueError(
            "dn evaluation create requires --model or --capability. "
            "--runtime-id alone does not choose an execution model. "
            "See `dn inference-model list` for available models "
            "and `dn capability list` for available capabilities."
        )

    api, profile = platform.connect()
    secret_selectors = request.pop("_secret_selectors", None)
    if secret_selectors is not None:
        resolved_secret_ids = _resolve_secret_ids(api, list(secret_selectors))
        if resolved_secret_ids:
            request["secret_ids"] = resolved_secret_ids
        else:
            request.pop("secret_ids", None)
    project_key = request.pop("project", None)
    if project_key:
        project = api.get_project(profile.org_key, profile.workspace_key, project_key)
        request["project_id"] = str(project.id)
    if "project_id" not in request and profile.project_id:
        request["project_id"] = profile.project_id

    payload = api.create_evaluation(profile.org_key, profile.workspace_key, request)

    eval_id = str(payload.get("id", ""))

    if not as_json:
        _print_skipped_members(payload.get("skipped_members"))

    if wait:
        payload = _wait_for_evaluation(
            api,
            org=profile.org_key,
            workspace=profile.workspace_key,
            evaluation_id=eval_id,
            poll_interval_sec=poll_interval_sec,
            timeout_sec=timeout_sec,
        )
        # Fetch analytics for the results summary
        analytics: dict[str, t.Any] | None = None
        with contextlib.suppress(Exception):
            analytics = api.get_evaluation_analytics(
                profile.org_key, profile.workspace_key, eval_id
            )

        if as_json:
            if analytics:
                payload["analytics"] = analytics
            _print_json(payload)
        else:
            _render_get_detail(payload, analytics)
            _print_eval_link(profile, eval_id)

        job_status = payload.get("job_status", payload.get("status", "unknown"))
        if job_status != "completed":
            raise RuntimeError(
                payload.get("error_summary") or f"Evaluation ended with status {job_status}"
            )
        return

    _render(payload, as_json=as_json, summary=_summarize_evaluation)
    if not as_json and eval_id:
        short = _short_id(eval_id)
        _hint(f"dn evaluation get {short}")
        _print_eval_link(profile, eval_id)


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------


@cli.command(name="list", alias="ls")
def list_(
    *,
    status: t.Annotated[
        EvaluationStatus | None,
        cyclopts.Parameter(name=_FLAG_STATUS),
    ] = None,
    project: t.Annotated[
        str | None,
        cyclopts.Parameter(name="--project-id"),
    ] = None,
    limit: int = 50,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Show evaluations in your workspace.

    Args:
        status: Filter by evaluation status (e.g. running, completed, failed).
        project: Filter by project ID.
        limit: Maximum results to show.
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    items = _collect_pages(
        lambda page, page_size: api.list_evaluation_jobs(
            profile.org_key,
            profile.workspace_key,
            page=page,
            page_size=page_size,
            status=status,
            project_id=project,
        ),
        limit=limit,
        page_size=50,
    )
    _render_list(
        items,
        as_json=as_json,
        summary=_summarize_evaluation,
        empty_msg="No evaluations found",
        fields=_EVALUATION_LIST_ROW_FIELDS,
    )


# ---------------------------------------------------------------------------
# get
# ---------------------------------------------------------------------------


@cli.command()
def get(
    evaluation_id: t.Annotated[str, cyclopts.Parameter(name="evaluation-id")],
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Show evaluation configuration, progress, and results.

    Displays configuration, current sample progress, and timing. When
    the evaluation has finished, also shows pass rates, per-task
    breakdown, and duration percentiles from the analytics snapshot.

    Args:
        evaluation_id: The evaluation ID (e.g. 0fe36a23-...).
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    payload = api.get_evaluation_job(profile.org_key, profile.workspace_key, evaluation_id)

    # Fetch analytics if the evaluation is in a terminal state
    job_status = payload.get("job_status", payload.get("status", "unknown"))
    analytics: dict[str, t.Any] | None = None
    if job_status in _TERMINAL_JOB_STATUSES:
        with contextlib.suppress(Exception):
            analytics = api.get_evaluation_analytics(
                profile.org_key, profile.workspace_key, evaluation_id
            )

    if as_json:
        if analytics:
            payload["analytics"] = analytics
        _print_json(payload)
    else:
        _render_get_detail(payload, analytics)
        short = _short_id(evaluation_id)
        if job_status in _TERMINAL_JOB_STATUSES:
            _hint(f"dn evaluation list-samples {short}")
        else:
            _hint(f"dn evaluation list-samples {short}")
        _print_eval_link(profile, evaluation_id)


# ---------------------------------------------------------------------------
# list-samples
# ---------------------------------------------------------------------------


@cli.command(name="list-samples")
def list_samples(
    evaluation_id: t.Annotated[str, cyclopts.Parameter(name="evaluation-id")],
    *,
    status: t.Annotated[
        EvaluationItemStatus | None,
        cyclopts.Parameter(name=_FLAG_STATUS),
    ] = None,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """List samples in an evaluation.

    Each sample represents one agent run against a security task.
    Use ``--status failed`` to drill into failures.

    Args:
        evaluation_id: The evaluation ID.
        status: Filter by sample status (e.g. passed, failed, timed_out).
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    payload = api.list_evaluation_items(profile.org_key, profile.workspace_key, evaluation_id)

    items: list[dict[str, t.Any]]
    if isinstance(payload, dict):
        items = payload.get("items", [])
    else:
        items = payload

    # Client-side status filter (API does not support it)
    if status:
        items = [item for item in items if item.get("item_status", item.get("status")) == status]

    if as_json:
        rows = [_project_row(item, _EVALUATION_SAMPLE_LIST_ROW_FIELDS) for item in items]
        _print_json(rows)
        return

    if not items:
        console.print("[dim]No samples found[/dim]")
        return

    table = Table(show_header=True, show_edge=False, pad_edge=False, box=None)
    table.add_column("#", style="dim", width=4)
    table.add_column("ID", width=10)
    table.add_column("", width=2)
    table.add_column("Status", width=16)
    table.add_column("Task")
    table.add_column("Duration", style="dim", justify="right")
    table.add_column("Error")

    status_counts: dict[str, int] = {}
    for item in items:
        item_status = item.get("item_status", item.get("status", "unknown"))
        status_counts[item_status] = status_counts.get(item_status, 0) + 1
        error = item.get("error")

        error_display = ""
        if error:
            error_display = f"[red]{error[:60]}[/red]"

        duration = _fmt_duration(item.get("started_at"), item.get("completed_at"))
        task_name = item.get("task_name_snapshot", "unknown")
        sample_short = _short_id(str(item.get("id", "")))

        table.add_row(
            str(item.get("position", "?")),
            sample_short,
            _status_dot(item_status),
            item_status,
            f"[cyan]{task_name}[/cyan]",
            duration,
            error_display,
        )

    console.print(table)

    # Summary footer — dots for visual continuity with table rows
    total = len(items)
    summary_parts = [f"[dim]{total} samples[/dim]"]
    for s in ["passed", "failed", "timed_out", "infra_error", "cancelled"]:
        c = status_counts.get(s, 0)
        if c > 0:
            summary_parts.append(f"{_status_dot(s)} [dim]{c} {s}[/dim]")
    active = sum(
        status_counts.get(s, 0)
        for s in [
            "queued",
            "claiming",
            "provisioning",
            "agent_running",
            "agent_finished",
            "verifying",
        ]
    )
    if active > 0:
        summary_parts.append(f"{_status_dot('agent_running')} [dim]{active} in progress[/dim]")
    console.print(f"\n{'  '.join(summary_parts)}")

    short_eval = _short_id(evaluation_id)
    sample_id_hint = _short_id(items[0].get("id", "")) if len(items) == 1 else "<sample-id>"
    _hint(f"dn evaluation get-sample {short_eval}/{sample_id_hint}")


# ---------------------------------------------------------------------------
# get-sample
# ---------------------------------------------------------------------------


@cli.command(name="get-sample")
def get_sample(
    ref: t.Annotated[
        str,
        cyclopts.Parameter(name="eval/sample"),
    ],
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Show details of a single evaluation sample.

    Displays the sample's lifecycle status, timing breakdown, sandbox
    IDs, error details, and verification result.

    Args:
        ref: Sample reference as EVAL_ID/SAMPLE_ID (e.g. 9ab81fc1/75e4914f).
        as_json: Output as JSON.
    """
    evaluation_id, sample_id = _parse_sample_ref(ref)
    api, profile = platform.connect()
    payload = api.get_evaluation_item(
        profile.org_key, profile.workspace_key, evaluation_id, sample_id
    )

    if as_json:
        _print_json(payload)
        return

    item_status = payload.get("item_status", payload.get("status", "unknown"))
    task = payload.get("task_name_snapshot", "unknown")
    position = payload.get("position", "?")

    # Header — dot + status carry color; task name is cyan (entity cross-ref)
    color = _eval_status_color(item_status)
    console.print(
        f"{_status_dot(item_status)} [{color}]{item_status}[/{color}]"
        f"  [dim]#{position}[/dim]  [cyan]{task}[/cyan]"
    )
    console.print()

    # Identity — short prefix is prominent (it's what you copy for get-sample)
    console.print(f"{_label('ID')}{_fmt_id(str(payload.get('id', '-')))}")
    if payload.get("model"):
        console.print(f"{_label('Model')}{payload['model']}")
    if payload.get("run_id"):
        console.print(f"{_label('Run ID')}[dim]{payload['run_id']}[/dim]")
    if payload.get("retry_count", 0) > 0:
        console.print(
            f"{_label('Retries')}{payload['retry_count']}/{payload.get('max_retries', 0)}"
        )

    # Timing — timestamps are dim reference data, elapsed is prominent
    has_timing = False
    for label_text, field in [
        ("Queued", "queued_at"),
        ("Started", "started_at"),
        ("Agent Done", "agent_finished_at"),
        ("Verified", "verified_at"),
        ("Completed", "completed_at"),
    ]:
        if payload.get(field):
            if not has_timing:
                console.print()
                has_timing = True
            console.print(f"{_label(label_text)}[dim]{_fmt_timestamp(payload[field])}[/dim]")

    duration = _fmt_duration(payload.get("started_at"), payload.get("completed_at"))
    if duration != "-":
        console.print(f"{_label('Elapsed')}{duration}")

    # Agent execution telemetry (from metadata_json._dreadnode.agent_result)
    dreadnode_meta = (payload.get("metadata_json") or {}).get("_dreadnode", {})
    agent_result = dreadnode_meta.get("agent_result", {})
    if agent_result:
        console.print()
        stop = agent_result.get("stop_reason")
        if stop:
            stop_color = "green" if stop == "end_turn" else "red" if stop == "error" else "yellow"
            console.print(f"{_label('Stop Reason')}[{stop_color}]{stop}[/{stop_color}]")

        steps = agent_result.get("generation_steps", 0)
        total_tool = agent_result.get("total_tool_calls", 0)
        step_parts = [f"{steps} generation steps"]
        if total_tool:
            step_parts.append(f"{total_tool} tool calls")
        console.print(f"{_label('Execution')}{'  '.join(step_parts)}")

        tools = agent_result.get("tool_calls", [])
        if tools:
            console.print(f"{_label('Tools')}[dim]{', '.join(tools)}[/dim]")

        total_tok = agent_result.get("total_tokens", 0)
        if total_tok:
            in_tok = agent_result.get("input_tokens", 0)
            out_tok = agent_result.get("output_tokens", 0)
            console.print(
                f"{_label('Tokens')}{total_tok:,} total  [dim]{in_tok:,} in  {out_tok:,} out[/dim]"
            )

        dur_ms = agent_result.get("duration_ms", 0)
        if dur_ms:
            dur_s = dur_ms / 1000
            console.print(f"{_label('Agent Time')}{dur_s:.1f}s")

        gen_errors = agent_result.get("generation_errors", 0)
        tool_errors = agent_result.get("tool_errors", 0)
        if gen_errors or tool_errors:
            err_parts: list[str] = []
            if gen_errors:
                err_parts.append(f"{gen_errors} generation")
            if tool_errors:
                err_parts.append(f"{tool_errors} tool")
            console.print(f"{_label('Exec Errors')}[red]{'  '.join(err_parts)}[/red]")

        agent_error = agent_result.get("error")
        if agent_error:
            console.print(f"{_label('Agent Error')}[red]{agent_error}[/red]")

    # Sandboxes — dim IDs (plumbing, not primary info)
    agent_sb = payload.get("agent_sandbox_id")
    env_sb = payload.get("env_sandbox_id")
    if agent_sb or env_sb:
        console.print()
        if agent_sb:
            console.print(f"{_label('Agent SB')}[dim]{agent_sb}[/dim]")
        if env_sb:
            console.print(f"{_label('Env SB')}[dim]{env_sb}[/dim]")

    # Error (item-level error, distinct from agent execution error)
    error = payload.get("error")
    if error:
        console.print()
        console.print(f"{_label('Error')}[red]{error}[/red]")

    # Phase-aware provisioning failure — written by the eval worker when the
    # env-sandbox / runtime-sandbox phases fail outside of a task-authored
    # provision script. Surfaces which phase stalled + elapsed, so operators
    # don't have to open Logfire for every timeout (ENG-6249).
    provision_failure = dreadnode_meta.get("provision_failure") or {}
    if provision_failure:
        console.print()
        phase_raw = str(provision_failure.get("phase") or "unknown")
        phase_label = {
            "env_sandbox": "env sandbox",
            "provision_script": "provision script",
            "runtime_sandbox": "runtime sandbox",
        }.get(phase_raw, phase_raw)
        elapsed_ms = provision_failure.get("elapsed_ms") or 0
        elapsed_s = int(elapsed_ms) // 1000
        timed_out = bool(provision_failure.get("timed_out"))
        verb = "timed out provisioning" if timed_out else "failed to provision"
        console.print(f"{_label('Provisioning')}[red]{verb} {phase_label} after {elapsed_s}s[/red]")
        if not timed_out:
            cause_type = provision_failure.get("cause_type") or ""
            cause_message = provision_failure.get("cause_message") or ""
            if cause_type or cause_message:
                console.print(f"{_label('Cause')}[dim]{cause_type}: {cause_message}[/dim]")

    # Verification result
    result = payload.get("result_json")
    if result:
        console.print()
        console.print(f"{_label('Result')}")
        console.print(json.dumps(result, indent=2))


# ---------------------------------------------------------------------------
# get-transcript
# ---------------------------------------------------------------------------


@cli.command(name="get-transcript")
def get_transcript(
    ref: t.Annotated[
        str,
        cyclopts.Parameter(name="eval/sample"),
    ],
    *,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Download the agent conversation transcript for a sample.

    Returns the session transcript linked to this evaluation item as raw JSON.
    The payload is a `SessionTranscriptResponse` with the following top-level
    fields:

    - `session`: session metadata (id, title, model, agent, project, timestamps)
    - `messages`: ordered list of messages, each with `id`, `seq`, `parent_id`,
      `role`, `content`, `tool_calls`, `tool_call_id`, `metadata`, `agent`,
      `model`, `created_at`, and `compacted_at`
    - `current_system_prompt`: the active system prompt for restore
    - `has_more`: pagination flag

    Returns 404 if the item has no linked session (old evals or items where
    the runtime's session registration failed). Available mid-run — the link
    is established as soon as the runtime creates the session, before the
    agent begins streaming.

    Args:
        ref: Sample reference as EVAL_ID/SAMPLE_ID (e.g. 9ab81fc1/75e4914f).
    """
    evaluation_id, sample_id = _parse_sample_ref(ref)
    api, profile = platform.connect()
    payload = api.get_evaluation_item_transcript(
        profile.org_key,
        profile.workspace_key,
        evaluation_id,
        sample_id,
    )
    _print_json(payload)


# ---------------------------------------------------------------------------
# wait
# ---------------------------------------------------------------------------


@cli.command()
def wait(
    evaluation_id: t.Annotated[str, cyclopts.Parameter(name="evaluation-id")],
    *,
    poll_interval_sec: t.Annotated[
        float,
        cyclopts.Parameter(validator=cyclopts.validators.Number(gt=0)),
    ] = 10.0,
    timeout_sec: float | None = None,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Block until an evaluation reaches a terminal state.

    Polls the evaluation status and exits when it completes, fails,
    or is cancelled. Exits non-zero if the evaluation did not complete
    successfully.

    Args:
        evaluation_id: The evaluation ID.
        poll_interval_sec: Seconds between status polls.
        timeout_sec: Maximum seconds to wait before timing out.
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    payload = _wait_for_evaluation(
        api,
        org=profile.org_key,
        workspace=profile.workspace_key,
        evaluation_id=evaluation_id,
        poll_interval_sec=poll_interval_sec,
        timeout_sec=timeout_sec,
    )

    # Fetch analytics for results
    analytics: dict[str, t.Any] | None = None
    with contextlib.suppress(Exception):
        analytics = api.get_evaluation_analytics(
            profile.org_key, profile.workspace_key, evaluation_id
        )

    if as_json:
        if analytics:
            payload["analytics"] = analytics
        _print_json(payload)
    else:
        _render_get_detail(payload, analytics)
        _print_eval_link(profile, evaluation_id)

    job_status = payload.get("job_status", payload.get("status", "unknown"))
    if job_status != "completed":
        raise RuntimeError(
            payload.get("error_summary") or f"Evaluation ended with status {job_status}"
        )


# ---------------------------------------------------------------------------
# cancel
# ---------------------------------------------------------------------------


@cli.command()
def cancel(
    evaluation_id: t.Annotated[str, cyclopts.Parameter(name="evaluation-id")],
    *,
    yes: t.Annotated[bool, cyclopts.Parameter(name="--yes", alias="-y", negative=())] = False,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Cancel a running evaluation.

    Requests cancellation and terminates active sandboxes. Samples
    that are already in progress will be marked as cancelled.

    Args:
        evaluation_id: The evaluation ID.
        yes: Skip the confirmation prompt.
        as_json: Output as JSON.
    """
    api, profile = platform.connect()

    # Verify eval exists and is not already terminal
    job = api.get_evaluation_job(profile.org_key, profile.workspace_key, evaluation_id)
    job_status = job.get("job_status", job.get("status", "unknown"))
    if job_status in _TERMINAL_JOB_STATUSES:
        raise ValueError(f"Evaluation is already {job_status}")

    name = job.get("name", evaluation_id[:8])
    if not confirm_destructive(f"Cancel evaluation [cyan]{name}[/cyan]?", yes=yes):
        console.print("[dim]Aborted[/dim]")
        return
    if not yes:
        console.print()

    payload = api.cancel_evaluation(profile.org_key, profile.workspace_key, evaluation_id)
    _render(payload, as_json=as_json, summary=_summarize_evaluation)


# ---------------------------------------------------------------------------
# retry
# ---------------------------------------------------------------------------


@cli.command()
def retry(
    evaluation_id: t.Annotated[str, cyclopts.Parameter(name="evaluation-id")],
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Retry failed and errored samples in an evaluation.

    Resets samples that ended in failed, timed_out, or infra_error
    back to queued so they are picked up by workers again.

    Args:
        evaluation_id: The evaluation ID.
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    payload = api.retry_failed_evaluation(profile.org_key, profile.workspace_key, evaluation_id)
    _render(payload, as_json=as_json, summary=_summarize_evaluation)
    if not as_json:
        short = _short_id(evaluation_id)
        _hint(f"dn evaluation wait {short}")


# ---------------------------------------------------------------------------
# export
# ---------------------------------------------------------------------------


@cli.command()
def export(
    evaluation_id: t.Annotated[str, cyclopts.Parameter(name="evaluation-id")],
    *,
    output: t.Annotated[Path | None, cyclopts.Parameter(name="--output", alias="-o")] = None,
    transcripts: t.Annotated[bool, cyclopts.Parameter(negative="--no-transcripts")] = True,
    status: t.Annotated[
        EvaluationItemStatus | None,
        cyclopts.Parameter(name=_FLAG_STATUS),
    ] = None,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Export evaluation results, samples, and transcripts.

    Writes evaluation metadata, per-sample results, and agent transcripts
    to a directory. Transcripts are included by default; use --no-transcripts
    to skip them.

    Each transcript file is a `SessionTranscriptResponse` JSON payload — see
    `dn evaluation get-transcript --help` for the shape. Samples without a
    linked session (old evals or items where the runtime's session
    registration failed) are skipped with a warning.

    Args:
        evaluation_id: The evaluation ID (full or 8-char prefix).
        output: Output directory (default: ./eval-<short-id>/).
        transcripts: Include agent transcripts (default: yes).
        status: Only export samples with this status (e.g. failed, timed_out).
        as_json: Dump combined JSON to stdout instead of writing files.
    """
    api, profile = platform.connect()
    org, ws = profile.org_key, profile.workspace_key

    # Fetch job + analytics + samples
    job = api.get_evaluation_job(org, ws, evaluation_id)
    eval_id = str(job.get("id", evaluation_id))

    analytics: dict[str, t.Any] | None = None
    with contextlib.suppress(Exception):
        analytics = api.get_evaluation_analytics(org, ws, eval_id)

    raw = api.list_evaluation_items(org, ws, eval_id)
    samples: list[dict[str, t.Any]] = raw.get("items", []) if isinstance(raw, dict) else raw

    if status:
        samples = [s for s in samples if s.get("item_status", s.get("status")) == status]

    # Fetch transcripts
    transcript_map: dict[str, t.Any] = {}
    if transcripts:
        for sample in samples:
            sid = str(sample.get("id", ""))
            try:
                transcript_map[sid] = api.get_evaluation_item_transcript(org, ws, eval_id, sid)
            except Exception:
                if not as_json:
                    pos = sample.get("position", "?")
                    console.print(
                        f"  [yellow]warning: transcript unavailable for sample {pos}[/yellow]"
                    )

    # JSON mode — single combined payload to stdout
    if as_json:
        combined: dict[str, t.Any] = {"job": job, "analytics": analytics, "samples": samples}
        if transcripts:
            combined["transcripts"] = transcript_map
        _print_json(combined)
        return

    # File mode
    short = _short_id(eval_id)
    out_dir = output or Path(f"eval-{short}")
    out_dir.mkdir(parents=True, exist_ok=True)

    # evaluation.json — job + analytics
    (out_dir / "evaluation.json").write_text(
        json.dumps({"job": job, "analytics": analytics}, indent=2, default=str)
    )

    # samples.jsonl — one line per sample
    with (out_dir / "samples.jsonl").open("w") as f:
        for sample in samples:
            f.write(json.dumps(sample, default=str) + "\n")

    # transcripts/
    transcript_count = 0
    if transcripts and transcript_map:
        t_dir = out_dir / "transcripts"
        t_dir.mkdir(exist_ok=True)
        for sample in samples:
            sid = str(sample.get("id", ""))
            if sid in transcript_map:
                pos = sample.get("position", 0)
                fname = f"{pos:03d}-{_short_id(sid)}.json"
                (t_dir / fname).write_text(json.dumps(transcript_map[sid], indent=2, default=str))
                transcript_count += 1

    # Summary
    console.print(f"  Exported to [bold]{out_dir}[/bold]")
    parts = [f"{len(samples)} samples"]
    if transcripts:
        parts.append(f"{transcript_count} transcripts")
    if status:
        parts.append(f"filtered: {status}")
    console.print(f"  [dim]{'  |  '.join(parts)}[/dim]")


# ---------------------------------------------------------------------------
# compare
# ---------------------------------------------------------------------------


@cli.command()
def compare(
    eval_a: t.Annotated[str, cyclopts.Parameter(name="eval-a")],
    eval_b: t.Annotated[str, cyclopts.Parameter(name="eval-b")],
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Compare two evaluation runs side by side.

    Shows pass rate delta, per-task breakdown, duration changes,
    and error pattern differences between two evaluations.

    Args:
        eval_a: First evaluation ID (baseline).
        eval_b: Second evaluation ID (comparison).
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    org, ws = profile.org_key, profile.workspace_key

    job_a = api.get_evaluation_job(org, ws, eval_a)
    job_b = api.get_evaluation_job(org, ws, eval_b)

    analytics_a: dict[str, t.Any] | None = None
    analytics_b: dict[str, t.Any] | None = None
    with contextlib.suppress(Exception):
        analytics_a = api.get_evaluation_analytics(org, ws, str(job_a.get("id", eval_a)))
    with contextlib.suppress(Exception):
        analytics_b = api.get_evaluation_analytics(org, ws, str(job_b.get("id", eval_b)))

    if as_json:
        _print_json(
            {
                "a": {"job": job_a, "analytics": analytics_a},
                "b": {"job": job_b, "analytics": analytics_b},
            }
        )
        return

    # -- Header --
    id_a = str(job_a.get("id", eval_a))
    id_b = str(job_b.get("id", eval_b))
    status_a = job_a.get("job_status", job_a.get("status", "unknown"))
    status_b = job_b.get("job_status", job_b.get("status", "unknown"))
    name_a = job_a.get("name", "unnamed")
    name_b = job_b.get("name", "unnamed")

    console.print(
        f"  [dim]A[/dim]  {_short_id(id_a)}  "
        f"{_status_dot(status_a)} [{_eval_status_color(status_a)}]{status_a}[/{_eval_status_color(status_a)}]  "
        f"[bold]{name_a}[/bold]"
    )
    console.print(
        f"  [dim]B[/dim]  {_short_id(id_b)}  "
        f"{_status_dot(status_b)} [{_eval_status_color(status_b)}]{status_b}[/{_eval_status_color(status_b)}]  "
        f"[bold]{name_b}[/bold]"
    )
    console.print()

    # -- Config diff --
    for field, label in [("model", "Model"), ("capability", "Capability")]:
        va = job_a.get(field)
        vb = job_b.get(field)
        if va or vb:
            if va == vb:
                console.print(f"{_label(label)}{va}")
            else:
                console.print(
                    f"{_label(label)}{va or '[dim]-[/dim]'} [dim]\u2192[/dim] {vb or '[dim]-[/dim]'}"
                )

    # -- Pass rate --
    rate_a = analytics_a.get("pass_rate") if analytics_a else None
    rate_b = analytics_b.get("pass_rate") if analytics_b else None
    console.print()
    console.print(
        f"{_label('Pass rate')}"
        f"{_colored_pass_rate(rate_a)} [dim]\u2192[/dim] {_colored_pass_rate(rate_b)}"
        f"  {_fmt_delta_pct(rate_a, rate_b)}"
    )

    # -- Count deltas --
    for field, label, hib in [
        ("passed_count", "Passed", True),
        ("failed_count", "Failed", False),
        ("error_count", "Errors", False),
    ]:
        ca = analytics_a.get(field, 0) if analytics_a else None
        cb = analytics_b.get(field, 0) if analytics_b else None
        if ca or cb:
            console.print(
                f"{_label(label)}{ca or 0} [dim]\u2192[/dim] {cb or 0}"
                f"  {_fmt_delta(ca, cb, higher_is_better=hib)}"
            )

    # -- Per-task breakdown --
    snap_a = (analytics_a.get("analytics_snapshot") or {}) if analytics_a else {}
    snap_b = (analytics_b.get("analytics_snapshot") or {}) if analytics_b else {}

    tasks_a = {e["task_name"]: e for e in snap_a.get("task_breakdown", []) if isinstance(e, dict)}
    tasks_b = {e["task_name"]: e for e in snap_b.get("task_breakdown", []) if isinstance(e, dict)}
    all_tasks = sorted(set(tasks_a) | set(tasks_b))

    if all_tasks:
        console.print()
        console.print(f"{_label('Tasks')}")
        for tname in all_tasks:
            ta = tasks_a.get(tname)
            tb = tasks_b.get(tname)
            ra = ta.get("pass_rate") if ta else None
            rb = tb.get("pass_rate") if tb else None
            console.print(
                f"{_continuation()}[cyan]{tname}[/cyan]  "
                f"{_colored_pass_rate(ra)} [dim]\u2192[/dim] {_colored_pass_rate(rb)}"
                f"  {_fmt_delta_pct(ra, rb)}"
            )

    # -- Duration changes --
    dur_a = snap_a.get("runtime_durations_ms", {})
    dur_b = snap_b.get("runtime_durations_ms", {})
    if dur_a or dur_b:
        console.print()
        for field, label in [("p50_ms", "p50"), ("p95_ms", "p95"), ("max_ms", "max")]:
            da = dur_a.get(field) or dur_a.get(field.replace("_ms", ""))
            db = dur_b.get(field) or dur_b.get(field.replace("_ms", ""))
            if da is not None or db is not None:
                da_s = f"{da / 1000:.0f}s" if da is not None else "-"
                db_s = f"{db / 1000:.0f}s" if db is not None else "-"
                delta = (
                    _fmt_delta(da, db, higher_is_better=False, unit="ms", precision=0)
                    if da and db
                    else "[dim]-[/dim]"
                )
                console.print(f"{_label(label)}{da_s} [dim]\u2192[/dim] {db_s}  {delta}")

    # -- Error pattern changes --
    errors_a = {e["error"] for e in snap_a.get("error_summary", []) if isinstance(e, dict)}
    errors_b = {e["error"] for e in snap_b.get("error_summary", []) if isinstance(e, dict)}
    new_errors = errors_b - errors_a
    resolved_errors = errors_a - errors_b

    if new_errors or resolved_errors:
        console.print()
        console.print(f"{_label('Errors')}")
        for err in sorted(new_errors):
            console.print(f"{_continuation()}[red]+ {err[:80]}[/red]")
        for err in sorted(resolved_errors):
            console.print(f"{_continuation()}[green]- {err[:80]}[/green]")
