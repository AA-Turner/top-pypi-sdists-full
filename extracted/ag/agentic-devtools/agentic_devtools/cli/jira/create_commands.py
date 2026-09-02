"""
Jira create commands: create_epic, create_issue, create_subtask, create_issue_sync.
"""

import os
import sys
from typing import Any

from agentic_devtools.state import is_dry_run
from agentic_devtools.tools.jira import JiraConfig
from agentic_devtools.tools.jira import create_issue as _tools_create_issue

from .config import (
    get_jira_base_url,
    get_jira_headers,
    get_jira_project_keys,
)
from .formatting import build_user_story_description, merge_labels
from .helpers import (
    _get_requests,
    _get_ssl_verify,
    _parse_comma_separated,
    _parse_multiline_string,
)
from .state_helpers import get_jira_value, set_jira_value
from .vpn_wrapper import with_jira_vpn_context


def _build_jira_config() -> JiraConfig:
    """Construct a :class:`JiraConfig` from the current environment/state."""
    return JiraConfig(
        base_url=get_jira_base_url(),
        headers=get_jira_headers(),
        ssl_verify=_get_ssl_verify(),
        requests_module=_get_requests(),
    )


def get_subtask_type_name(
    config: JiraConfig | None = None,
    project_key: str | None = None,
    network_allowed: bool = True,
) -> str:
    """Resolve the Jira issue type name used for subtasks.

    Resolution order:
    1. ``jira.subtask_type`` state key
    2. ``jira.subtask_issue_type`` state key
    3. ``JIRA_SUBTASK_TYPE`` environment variable
    4. Cached project metadata (``is_subtask: true`` entry)
    5. Live Jira ``/rest/api/2/issuetype`` discovery (only when *network_allowed* is True)

    Args:
        config: Optional pre-built :class:`JiraConfig` to use for network discovery.
        project_key: Project key used to look up cached issue-type metadata.
        network_allowed: When ``False``, skips the live Jira API request and
            returns the best locally-available name (or the ``"Sub-task"`` fallback).
            Pass ``False`` for dry-run paths to avoid network calls.
    """
    for state_key in ("subtask_type", "subtask_issue_type"):
        configured_value = get_jira_value(state_key)
        if isinstance(configured_value, str) and configured_value.strip():
            return configured_value.strip()

    env_value = os.environ.get("JIRA_SUBTASK_TYPE")
    if isinstance(env_value, str) and env_value.strip():
        return env_value.strip()

    if project_key:
        from agentic_devtools.cli.config.project_config import get_issue_types_metadata

        metadata = get_issue_types_metadata(project_key)
        if isinstance(metadata, dict):
            issue_types = metadata.get("issue_types")
            if isinstance(issue_types, list):
                for issue_type in issue_types:
                    if not isinstance(issue_type, dict):
                        continue
                    if issue_type.get("is_subtask") is True:
                        name = issue_type.get("name")
                        if isinstance(name, str) and name.strip():
                            return name.strip()

    if not network_allowed:
        return "Sub-task"

    if config is None:
        try:
            config = _build_jira_config()
        except Exception as exc:
            print(f"Warning: Could not build Jira config for subtask type discovery: {exc}", file=sys.stderr)
            return "Sub-task"

    requests_module = config.requests_module if config.requests_module is not None else _get_requests()
    url = f"{config.base_url}/rest/api/2/issuetype"

    try:
        response = requests_module.get(url, headers=config.headers, verify=config.ssl_verify, timeout=30)
        response.raise_for_status()
    except Exception as exc:
        print(
            f"Warning: Could not discover the Jira subtask issue type from {url}: {exc}",
            file=sys.stderr,
        )
        return "Sub-task"

    try:
        payload = response.json()
    except ValueError:
        return "Sub-task"

    if not isinstance(payload, list):
        return "Sub-task"

    for issue_type in payload:
        if not isinstance(issue_type, dict):
            continue
        if issue_type.get("subtask") is True:
            name = issue_type.get("name")
            if isinstance(name, str) and name.strip():
                return name.strip()

    return "Sub-task"


def _format_jira_error(exc: Exception) -> str:
    """Format Jira API errors with response details when available."""
    response = getattr(exc, "response", None)
    if response is None:
        return str(exc)

    details: list[str] = []
    try:
        payload = response.json()
    except Exception:
        payload = None

    if isinstance(payload, dict):
        error_messages = payload.get("errorMessages")
        if isinstance(error_messages, list):
            details.append(f"Messages: {error_messages}")
        errors = payload.get("errors")
        if isinstance(errors, dict):
            details.append(f"Errors: {errors}")

    if not details:
        text = getattr(response, "text", None)
        if isinstance(text, str) and text.strip():
            details.append(text.strip())

    if details:
        return f"{exc} — {' | '.join(details)}"
    return str(exc)


def create_issue_sync(
    project_key: str,
    summary: str,
    issue_type: str,
    description: str,
    labels: list[str],
    epic_name: str | None = None,
    parent_key: str | None = None,
) -> dict[str, Any]:
    """
    Create a Jira issue synchronously.

    This is a thin backward-compatible wrapper that constructs a
    :class:`JiraConfig` from the environment and delegates to
    :func:`agentic_devtools.tools.jira.create_issue`.

    Args:
        project_key: Jira project key
        summary: Issue summary
        issue_type: Issue type (Task, Epic, Sub-task, etc.)
        description: Issue description
        labels: Labels to apply
        epic_name: Epic name (required for Epic type)
        parent_key: Parent issue key (for Sub-tasks)

    Returns:
        API response dictionary
    """
    config = _build_jira_config()
    result = _tools_create_issue(
        config=config,
        project_key=project_key,
        summary=summary,
        issue_type=issue_type,
        description=description,
        labels=labels,
        epic_name=epic_name,
        parent_key=parent_key,
    )
    return result["raw_response"]


@with_jira_vpn_context
def create_epic(dry_run_override: bool = False) -> None:
    """Create a Jira Epic. See commands.py for detailed docstring.

    Args:
        dry_run_override: Invocation-scoped dry-run trigger supplied by the
            ``agdt-create-epic`` router when ``--dry-run`` is passed. It is
            OR-ed with the persistent ``dry_run`` and ``jira.dry_run`` state
            triggers and never written back to state (FR-002, NFR-004).
    """
    project_key = get_jira_value("project_key")
    if not project_key:
        keys = get_jira_project_keys()
        project_key = keys[0] if keys else None
    if not project_key:
        print("Error: No Jira project key configured. Run agdt-setup or set jira.project_key.", file=sys.stderr)
        sys.exit(1)
    summary = get_jira_value("summary")
    epic_name = get_jira_value("epic_name")
    role = get_jira_value("role")
    desired_outcome = get_jira_value("desired_outcome")
    benefit = get_jira_value("benefit")

    missing = []
    if not summary:
        missing.append("jira.summary")
    if not epic_name:
        missing.append("jira.epic_name")
    if not role:
        missing.append("jira.role")
    if not desired_outcome:
        missing.append("jira.desired_outcome")
    if not benefit:
        missing.append("jira.benefit")

    if missing:
        print(f"Error: Missing required fields: {', '.join(missing)}", file=sys.stderr)
        print("\nUsage:", file=sys.stderr)
        print('  agdt-set jira.summary "Epic Title"', file=sys.stderr)
        print('  agdt-set jira.epic_name "Epic Name"', file=sys.stderr)
        print('  agdt-set jira.role "user role"', file=sys.stderr)
        print('  agdt-set jira.desired_outcome "what you want"', file=sys.stderr)
        print('  agdt-set jira.benefit "why you want it"', file=sys.stderr)
        print("  agdt-create-epic", file=sys.stderr)
        sys.exit(1)

    # At this point all required values are non-None (validated above)
    assert summary is not None
    assert role is not None
    assert desired_outcome is not None
    assert benefit is not None

    acceptance_criteria = _parse_multiline_string(get_jira_value("acceptance_criteria"))
    additional_information = _parse_multiline_string(get_jira_value("additional_information"))
    custom_labels = _parse_comma_separated(get_jira_value("labels"))
    dry_run = dry_run_override or is_dry_run() or get_jira_value("dry_run")

    description = build_user_story_description(
        role=role,
        desired_outcome=desired_outcome,
        benefit=benefit,
        acceptance_criteria=acceptance_criteria,
        additional_information=additional_information,
    )

    labels = merge_labels(custom_labels)

    if dry_run:
        print(f"[DRY RUN] Would create Epic in project {project_key}")
        print(f"Summary: {summary}")
        print(f"Epic Name: {epic_name}")
        print(f"Labels: {', '.join(labels)}")
        print(f"\nDescription:\n{description}")
        return

    print(f"Creating Epic in project {project_key}...")

    try:
        result = create_issue_sync(
            project_key=project_key,
            summary=summary,
            issue_type="Epic",
            description=description,
            labels=labels,
            epic_name=epic_name,
        )

        issue_key = result.get("key")
        print(f"Epic created successfully: {issue_key}")
        print(f"URL: {get_jira_base_url()}/browse/{issue_key}")
        set_jira_value("created_issue_key", issue_key)

    except Exception as e:
        print(f"Error creating epic: {e}", file=sys.stderr)
        sys.exit(1)


@with_jira_vpn_context
def create_issue() -> None:
    """Create a Jira issue (Task, Story, Bug, etc.). See commands.py for detailed docstring."""
    project_key = get_jira_value("project_key")
    if not project_key:
        keys = get_jira_project_keys()
        project_key = keys[0] if keys else None
    if not project_key:
        print("Error: No Jira project key configured. Run agdt-setup or set jira.project_key.", file=sys.stderr)
        sys.exit(1)
    summary = get_jira_value("summary")
    issue_type = get_jira_value("issue_type") or "Task"
    role = get_jira_value("role")
    desired_outcome = get_jira_value("desired_outcome")
    benefit = get_jira_value("benefit")

    missing = []
    if not summary:
        missing.append("jira.summary")
    if not role:
        missing.append("jira.role")
    if not desired_outcome:
        missing.append("jira.desired_outcome")
    if not benefit:
        missing.append("jira.benefit")

    if missing:
        print(f"Error: Missing required fields: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    # At this point all required values are non-None (validated above)
    assert summary is not None
    assert role is not None
    assert desired_outcome is not None
    assert benefit is not None

    acceptance_criteria = _parse_multiline_string(get_jira_value("acceptance_criteria"))
    additional_information = _parse_multiline_string(get_jira_value("additional_information"))
    custom_labels = _parse_comma_separated(get_jira_value("labels"))
    dry_run = is_dry_run() or get_jira_value("dry_run")

    description = build_user_story_description(
        role=role,
        desired_outcome=desired_outcome,
        benefit=benefit,
        acceptance_criteria=acceptance_criteria,
        additional_information=additional_information,
    )

    labels = merge_labels(custom_labels)

    if dry_run:
        print(f"[DRY RUN] Would create {issue_type} in project {project_key}")
        print(f"Summary: {summary}")
        print(f"Labels: {', '.join(labels)}")
        print(f"\nDescription:\n{description}")
        return

    print(f"Creating {issue_type} in project {project_key}...")

    try:
        result = create_issue_sync(
            project_key=project_key,
            summary=summary,
            issue_type=issue_type,
            description=description,
            labels=labels,
        )

        issue_key = result.get("key")
        print(f"{issue_type} created successfully: {issue_key}")
        print(f"URL: {get_jira_base_url()}/browse/{issue_key}")
        set_jira_value("created_issue_key", issue_key)

    except Exception as e:
        print(f"Error creating issue: {_format_jira_error(e)}", file=sys.stderr)
        sys.exit(1)


@with_jira_vpn_context
def create_subtask() -> None:
    """Create a Jira Sub-task. See commands.py for detailed docstring."""
    parent_key = get_jira_value("parent_key")
    summary = get_jira_value("summary")
    role = get_jira_value("role")
    desired_outcome = get_jira_value("desired_outcome")
    benefit = get_jira_value("benefit")

    missing = []
    if not parent_key:
        missing.append("jira.parent_key")
    if not summary:
        missing.append("jira.summary")
    if not role:
        missing.append("jira.role")
    if not desired_outcome:
        missing.append("jira.desired_outcome")
    if not benefit:
        missing.append("jira.benefit")

    if missing:
        print(f"Error: Missing required fields: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    # At this point all required values are non-None (validated above)
    assert summary is not None
    assert role is not None
    assert desired_outcome is not None
    assert benefit is not None

    if parent_key:
        project_key = parent_key.split("-")[0]
    else:  # pragma: no cover — parent_key is always required above
        keys = get_jira_project_keys()
        project_key = keys[0] if keys else None
    if not project_key:  # pragma: no cover — defensive; parent_key always provides a key
        print("Error: No Jira project key configured. Run agdt-setup or set jira.project_key.", file=sys.stderr)
        sys.exit(1)

    acceptance_criteria = _parse_multiline_string(get_jira_value("acceptance_criteria"))
    additional_information = _parse_multiline_string(get_jira_value("additional_information"))
    custom_labels = _parse_comma_separated(get_jira_value("labels"))
    dry_run = is_dry_run() or get_jira_value("dry_run")

    description = build_user_story_description(
        role=role,
        desired_outcome=desired_outcome,
        benefit=benefit,
        acceptance_criteria=acceptance_criteria,
        additional_information=additional_information,
    )

    labels = merge_labels(custom_labels)

    subtask_type_name = get_subtask_type_name(project_key=project_key, network_allowed=not dry_run)

    if dry_run:
        print(f"[DRY RUN] Would create {subtask_type_name} under {parent_key}")
        print(f"Summary: {summary}")
        print(f"\nDescription:\n{description}")
        return

    print(f"Creating Sub-task under {parent_key}...")

    try:
        result = create_issue_sync(
            project_key=project_key,
            summary=summary,
            issue_type=subtask_type_name,
            description=description,
            labels=labels,
            parent_key=parent_key,
        )

        issue_key = result.get("key")
        print(f"Sub-task created successfully: {issue_key}")
        print(f"URL: {get_jira_base_url()}/browse/{issue_key}")
        set_jira_value("created_issue_key", issue_key)

    except Exception as e:
        print(f"Error creating subtask: {_format_jira_error(e)}", file=sys.stderr)
        sys.exit(1)
