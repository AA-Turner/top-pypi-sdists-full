"""Public helper surface shared by the agent batch package and its design lane.

Centralises the cross-cutting helpers the ``agent`` sub-commands and the design
lane (``run_design_pipeline``) reuse — explicit-ticket resolution, label-based
issue fetch, current-project detection, duration parsing — plus the shared
batch-run skeleton (:func:`run_batch`) that wraps a body function with run-id
stamping, crash tolerance and report publishing.

Every GitLab call here goes through the package glab socle
(``common.glab.runner``): the paginating list helper and the JSON helper, never
a hand-rolled pagination loop or ``json.loads`` on raw ``glab`` output.
"""

import json
import logging
import re
import subprocess
from collections.abc import Callable
from datetime import datetime
from typing import Any

import typer

from ..common.duration import parse_duration
from ..common.glab.runner import glab_api, glab_api_paginated
from .models import Outcome, OutcomeStatus, RunConfig, RunResult, Ticket
from .report import publish
from .tracking import set_run_id

logger = logging.getLogger(__name__)

_PER_PAGE = 100


def run_batch(cfg: RunConfig, run_id: str, body: Callable[[RunConfig, RunResult], None]) -> RunResult:
    """Run a batch ``body`` under the shared orchestration skeleton.

    Stamps every downstream tracking event with ``run_id`` (via contextvar),
    runs ``body`` under a broad crash guard, and always publishes the report —
    even on a partial run — before returning the accumulated result. This is the
    structure both the code-autopilot and design pipelines share; the caller
    supplies its own run-id (with its own prefix) and body.
    """
    result = RunResult(run_id=run_id)
    set_run_id(result.run_id)
    try:
        body(cfg, result)
    except Exception:
        logger.exception("batch pipeline crashed; publishing partial result")
    publish(result, cfg)
    return result


def detect_current_project() -> str | None:
    """Return the current repo's ``project_path`` via ``internal detect-context``.

    ``None`` when the context can't be resolved (not a repo, glab absent,
    malformed output) so the CLI can fall back to requiring ``--project``.
    """
    try:
        result = subprocess.run(
            ["pysae-ai-tools", "internal", "detect-context", "--local"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
            timeout=15,
        )
        ctx = json.loads(result.stdout)
        path = ctx.get("project_path")
        return str(path) if path else None
    except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError):
        return None


def parse_duration_seconds(s: str) -> int:
    """Parse '2h', '30m', '90s' or plain seconds into seconds. Rejects zero/negative.

    Raises :class:`typer.BadParameter` so it can back a CLI option directly.
    """
    try:
        seconds = int(parse_duration(s, allowed_units="smh").total_seconds())
    except ValueError as exc:
        raise typer.BadParameter(f"invalid duration: {s}") from exc
    if seconds <= 0:
        raise typer.BadParameter(f"duration must be > 0: {s}")
    return seconds


def _parse_issue(raw: dict[str, Any], project_path: str) -> Ticket:
    author = (raw.get("author") or {}).get("username", "") or ""
    return Ticket(
        iid=int(raw["iid"]),
        project_path=project_path,
        title=raw["title"],
        description=raw.get("description"),
        labels=list(raw.get("labels", [])),
        web_url=raw["web_url"],
        updated_at=datetime.fromisoformat(raw["updated_at"].replace("Z", "+00:00")),
        author_username=str(author),
    )


def fetch_with_label(projects: list[str], label: str) -> list[Ticket]:
    """Fetch open issues carrying ``label`` across ``projects`` (deduped).

    Pagination is delegated to the socle's :func:`glab_api_paginated`, which
    fetches page by page (never ``glab api --paginate``, whose concatenated
    JSON arrays break parsing past the first page).
    """
    seen: set[tuple[str, int]] = set()
    out: list[Ticket] = []
    for project in projects:
        encoded = project.replace("/", "%2F")
        endpoint = f"projects/{encoded}/issues?labels={label}&state=opened"
        for raw in glab_api_paginated(endpoint, per_page=_PER_PAGE, timeout=60):
            key = (project, int(raw["iid"]))
            if key in seen:
                continue
            seen.add(key)
            out.append(_parse_issue(raw, project))
    return out


def resolve_explicit_tickets(refs: list[str]) -> tuple[list[Ticket], list[Outcome]]:
    """Resolve full GitLab issue URLs to :class:`Ticket` objects.

    Accepts both the legacy ``/-/issues/<iid>`` and the modern
    ``/-/work_items/<iid>`` forms. Returns a ``(resolved, failures)`` tuple: a
    404, malformed URL, or network error on any ref yields an ESCALATED
    :class:`Outcome` instead of aborting the whole run.
    """
    resolved: list[Ticket] = []
    failures: list[Outcome] = []
    url_re = re.compile(r"https?://[^/]+/(.+?)/-/(?:issues|work_items)/(\d+)")
    for ref in refs:
        m = url_re.match(ref)
        if not m:
            logger.warning("skipping ticket ref '%s': only full URLs are supported in --tickets", ref)
            failures.append(
                Outcome(
                    ticket_iid=0,
                    project_path=ref,
                    status=OutcomeStatus.ESCALATED,
                    mr_url=None,
                    mr_iid=None,
                    escalation_reason="--tickets ref is not a full GitLab issue/work_items URL",
                    tokens_used=0,
                    duration_seconds=0,
                )
            )
            continue
        project_path, iid_str = m.group(1), m.group(2)
        iid = int(iid_str)
        encoded = project_path.replace("/", "%2F")
        raw = glab_api(f"projects/{encoded}/issues/{iid}", timeout=30)
        try:
            if raw is None:
                raise RuntimeError("glab api call failed")
            resolved.append(
                Ticket(
                    iid=iid,
                    project_path=project_path,
                    title=raw["title"],
                    description=raw.get("description"),
                    labels=list(raw.get("labels", [])),
                    web_url=raw["web_url"],
                    updated_at=datetime.fromisoformat(raw["updated_at"].replace("Z", "+00:00")),
                    author_username=str((raw.get("author") or {}).get("username", "") or ""),
                )
            )
        except (RuntimeError, KeyError) as exc:
            logger.warning("cannot resolve %s: %s", ref, exc)
            failures.append(
                Outcome(
                    ticket_iid=iid,
                    project_path=project_path,
                    status=OutcomeStatus.ESCALATED,
                    mr_url=None,
                    mr_iid=None,
                    escalation_reason=f"cannot resolve URL: {type(exc).__name__}",
                    tokens_used=0,
                    duration_seconds=0,
                )
            )
    return resolved, failures
