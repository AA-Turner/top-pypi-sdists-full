"""Fetch and condense GitHub Actions job logs for AI PR Loop repair comments.

These helpers are mostly deterministic; :func:`fetch_condensed_job_log`,
:func:`fetch_job_details`, :func:`fetch_run_event`, and
:func:`fetch_failed_check_context` perform I/O (``gh api`` or ``gh run view``
calls). ``_gh_api`` is imported lazily inside these I/O helpers to avoid a
circular import with ``github_provider``.
"""

from __future__ import annotations

import json
import re

from agentic_devtools.cli.ci.models import CheckRunStatus, FailedCheckContext, FailedStepLog
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError
from agentic_devtools.cli.subprocess_utils import run_safe

# GitHub Actions raw logs prefix every line with an RFC-3339 timestamp such as
# ``2026-06-23T10:00:00.1234567Z `` (note the trailing space before content).
_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z\s")

# Pytest metadata lines that are noise for diagnosing failures (prior art:
# ``agentic_devtools/cli/checks/commands.py`` ``_condense_output``).
_SKIP_PREFIXES = (
    "platform ",
    "cachedir: ",
    "rootdir: ",
    "configfile: ",
    "plugins: ",
    "collecting ",
    "collected ",
)

_EARLIER_TRUNCATED_MARKER = "[… earlier output truncated …]"

# Literal sentinel GitHub emits in the step-name column of ``gh run view
# --log-failed`` output when it cannot attribute a log line to a named step.
# ``parse_failed_step_logs`` treats it as an ordinary step name (see its
# docstring), but renderers should not present it as though it were real
# step-name data. Defined here, next to the parser, so the two cannot drift.
UNKNOWN_STEP_SENTINEL = "UNKNOWN STEP"
_RATE_LIMIT_STATUS_RE = re.compile(
    r"\b(?:http(?:/\d(?:\.\d)?)?|status(?:\s+code)?)\s*[:=]?\s*429\b",
    re.IGNORECASE,
)


def _is_rate_limit_text(text: str) -> bool:
    """Return whether CLI output identifies a GitHub rate-limit response."""
    lowered = text.lower()
    return "rate limit" in lowered or bool(_RATE_LIMIT_STATUS_RE.search(lowered))


def _provider_rate_limit_error(error: RetryableError) -> ProviderRateLimitError:
    """Convert retry metadata into the provider-level error used by actions."""
    return ProviderRateLimitError(
        retry_after_seconds=error.retry_after,
        reset_timestamp=error.reset_timestamp,
        remaining=error.remaining,
        provider=error.provider,
        credential_identity=error.credential_identity,
        source=error.source,
    )


def extract_job_id(html_url: str) -> int | None:
    """Parse the trailing ``/job/<id>`` from a check-run ``html_url``.

    Returns ``None`` when the URL has no ``/job/<digits>`` segment (e.g. CodeQL
    code-scanning URLs), so callers can degrade to a link-only rendering.
    """
    match = re.search(r"/job/(\d+)", html_url)
    if match is None:
        return None
    return int(match.group(1))


def condense_job_log(raw: str, *, max_lines: int = 200, max_chars: int = 8_000) -> str:
    """Strip GitHub Actions line-timestamps and known noise, keep the tail.

    Deterministic and I/O-free. Strips the per-line RFC-3339 timestamp prefix,
    drops per-test ``... PASSED`` lines and pytest metadata noise, collapses
    blank runs, then keeps the failure-relevant tail bounded by ``max_lines``
    and ``max_chars``. When anything is dropped from the front, a
    ``[… earlier output truncated …]`` marker is prepended.
    """
    cleaned: list[str] = []
    prev_blank = False
    for line in raw.splitlines():
        line = _TIMESTAMP_RE.sub("", line)
        stripped = line.strip()
        if not stripped:
            if not prev_blank:
                cleaned.append("")
                prev_blank = True
            continue
        prev_blank = False
        if stripped.endswith(" PASSED") and "::" in stripped:
            continue
        if any(stripped.startswith(prefix) for prefix in _SKIP_PREFIXES):
            continue
        cleaned.append(line)

    while cleaned and not cleaned[-1].strip():
        cleaned.pop()
    while cleaned and not cleaned[0].strip():
        cleaned.pop(0)

    truncated = False
    if len(cleaned) > max_lines:
        cleaned = cleaned[-max_lines:]
        truncated = True

    text = "\n".join(cleaned)
    if len(text) > max_chars:
        text = text[-max_chars:]
        truncated = True

    if truncated:
        return f"{_EARLIER_TRUNCATED_MARKER}\n{text}"
    return text


def fetch_condensed_job_log(check: CheckRunStatus, *, repo: str, token: str | None = None) -> str:
    """Fetch and condense the plain-text log for a failing check's Actions job.

    Resolves the job id from ``check.html_url``, downloads the single job's
    plain-text log via ``GET /repos/{repo}/actions/jobs/{job_id}/logs`` (the
    ``gh`` CLI follows the 302 redirect to the plain-text download), then
    condenses it. Returns ``""`` on non-rate-limit failures (no job id, missing
    repo, non-2xx/410 expired, empty body).

    Raises:
        ProviderRateLimitError: When the provider returns a rate-limit response.
    """
    job_id = extract_job_id(check.html_url)
    if job_id is None:
        return ""
    if not repo:
        return ""
    try:
        from agentic_devtools.cli.ci.github_provider import _gh_api  # noqa: PLC0415

        raw = _gh_api(f"/repos/{repo}/actions/jobs/{job_id}/logs", token=token)
    except (ProviderRateLimitError, RetryableError) as exc:
        if exc.is_rate_limit:
            if isinstance(exc, RetryableError):
                raise _provider_rate_limit_error(exc) from exc
            raise
        return ""
    except Exception:
        return ""
    if not raw or not raw.strip():
        return ""
    return condense_job_log(raw)


def parse_failed_step_logs(raw: str) -> list[FailedStepLog]:
    """Parse ``gh run view --log-failed`` output into per-step condensed logs.

    Each well-formed line is ``<job name>\\t<step name>\\t<content>``. Lines are
    grouped by the step-name (second tab) field, preserving the order in which
    each step first appears, and each step's content is condensed independently
    via :func:`condense_job_log`. Lines with fewer than two tabs attach to the
    most recently seen step (continuation lines); any such lines before the
    first step are dropped. The literal ``UNKNOWN STEP`` is treated as a normal
    step name. Deterministic and I/O-free.
    """
    order: list[str] = []
    contents: dict[str, list[str]] = {}
    current: str | None = None
    for line in raw.splitlines():
        bits = line.split("\t", 2)
        if len(bits) == 3:
            step_name = bits[1]
            if step_name not in contents:
                order.append(step_name)
                contents[step_name] = []
            contents[step_name].append(bits[2])
            current = step_name
        elif current is not None:
            contents[current].append(line)
    return [FailedStepLog(step_name=name, condensed_log=condense_job_log("\n".join(contents[name]))) for name in order]


def fetch_job_details(job_id: int, *, repo: str, token: str | None = None) -> dict | None:
    """Fetch a GitHub Actions job's details for display-name composition.

    Calls ``GET /repos/{repo}/actions/jobs/{job_id}`` and returns the parsed
    JSON object (containing ``workflow_name``, ``name``, and ``run_id``).
    Returns ``None`` on non-rate-limit failures (missing repo, request error,
    non-object or malformed JSON).

    Raises:
        ProviderRateLimitError: When the provider returns a rate-limit response.
    """
    if not repo:
        return None
    try:
        from agentic_devtools.cli.ci.github_provider import _gh_api  # noqa: PLC0415

        raw = _gh_api(f"/repos/{repo}/actions/jobs/{job_id}", token=token)
        data = json.loads(raw)
    except (ProviderRateLimitError, RetryableError) as exc:
        if exc.is_rate_limit:
            if isinstance(exc, RetryableError):
                raise _provider_rate_limit_error(exc) from exc
            raise
        return None
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    return data


def fetch_run_event(run_id: int, *, repo: str, token: str | None = None) -> str:
    """Fetch a workflow run's triggering event name.

    Calls ``GET /repos/{repo}/actions/runs/{run_id}`` and returns the ``event``
    field (e.g. ``"pull_request"``). Returns ``""`` on non-rate-limit failures
    (missing repo, request error, non-object or malformed JSON,
    missing/non-string ``event``).

    Raises:
        ProviderRateLimitError: When the provider returns a rate-limit response.
    """
    if not repo:
        return ""
    try:
        from agentic_devtools.cli.ci.github_provider import _gh_api  # noqa: PLC0415

        raw = _gh_api(f"/repos/{repo}/actions/runs/{run_id}", token=token)
        data = json.loads(raw)
    except (ProviderRateLimitError, RetryableError) as exc:
        if exc.is_rate_limit:
            if isinstance(exc, RetryableError):
                raise _provider_rate_limit_error(exc) from exc
            raise
        return ""
    except Exception:
        return ""
    if not isinstance(data, dict):
        return ""
    event = data.get("event", "")
    return event if isinstance(event, str) else ""


def fetch_failed_check_context(
    check: CheckRunStatus,
    *,
    repo: str,
    token: str | None = None,
    run_event_cache: dict[int, str] | None = None,
) -> FailedCheckContext | None:
    """Compose a failing check's display name and per-failing-step condensed logs.

    Resolves the job id from ``check.html_url`` (returns ``None`` when absent,
    e.g. CodeQL code-scanning, so the renderer degrades to link-only). Fetches
    the job's ``workflow_name``/``name`` and the run's ``event`` to build the
    ``"<workflow_name> / <job_name> (<event>)"`` display name (segments dropped
    gracefully). Fetches per-failing-step logs via ``gh run view --log-failed``;
    when that yields nothing, falls back to the whole-job condensed log as a
    single :class:`FailedStepLog` with an empty ``step_name``. Run-event lookups
    are de-duplicated through ``run_event_cache``.

    Raises:
        ProviderRateLimitError: When any provider call is rate-limited and
            cooldown handling must be triggered by the caller.
    """
    job_id = extract_job_id(check.html_url)
    if job_id is None:
        return None
    if not repo:
        return None

    details = fetch_job_details(job_id, repo=repo, token=token)
    workflow_name = ""
    job_name = ""
    run_id = None
    if details is not None:
        workflow_name = str(details.get("workflow_name") or "")
        job_name = str(details.get("name") or "")
        run_id = details.get("run_id")

    event = ""
    if isinstance(run_id, int):
        if run_event_cache is not None and run_id in run_event_cache:
            event = run_event_cache[run_id]
        else:
            event = fetch_run_event(run_id, repo=repo, token=token)
            if run_event_cache is not None:
                run_event_cache[run_id] = event

    if not job_name:
        display_name = ""
    elif workflow_name:
        display_name = f"{workflow_name} / {job_name}"
        if event:
            display_name = f"{display_name} ({event})"
    else:
        display_name = job_name

    raw_steps = ""
    try:
        import os  # noqa: PLC0415

        env = {**os.environ, "GH_TOKEN": token} if token else None
        result = run_safe(
            ["gh", "run", "view", "--job", str(job_id), "--log-failed", "--repo", repo],
            capture_output=True,
            text=True,
            shell=False,
            env=env,
        )
        if result.returncode == 0:
            raw_steps = result.stdout or ""
        elif _is_rate_limit_text(result.stderr or ""):
            raise RetryableError(
                "GitHub Actions log command was rate limited",
                provider="github",
                is_rate_limit=True,
            )
    except (ProviderRateLimitError, RetryableError) as exc:
        if exc.is_rate_limit:
            if isinstance(exc, RetryableError):
                raise _provider_rate_limit_error(exc) from exc
            raise
        raw_steps = ""
    except Exception:
        raw_steps = ""

    step_logs: tuple[FailedStepLog, ...] = ()
    if raw_steps.strip():
        parsed = parse_failed_step_logs(raw_steps)
        step_logs = tuple(s for s in parsed if s.condensed_log.strip())
    if not step_logs:
        whole = fetch_condensed_job_log(check, repo=repo, token=token)
        if whole:
            step_logs = (FailedStepLog(step_name="", condensed_log=whole),)
    return FailedCheckContext(display_name=display_name, step_logs=step_logs)
