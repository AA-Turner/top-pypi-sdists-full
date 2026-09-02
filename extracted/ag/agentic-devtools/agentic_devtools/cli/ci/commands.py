"""CLI entry points for CI orchestration commands.

Provides ``agdt-ai-pr-loop``, ``agdt-speckit-trigger``, and
``agdt-assign-implementation-agent`` commands
that read event data from environment variables and invoke the
pipeline v2 entry point.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import shutil
import sys
import uuid
from dataclasses import asdict

from agentic_devtools.cli.ci.agent_assignment import (
    AgentAssignmentResult,
    _gh_api_call,
    _resolve_assignment_token,
    _validate_repo_format,
    assign_issue_to_agent,
)
from agentic_devtools.cli.ci.exceptions import MalformedEventError
from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.guards import check_edit_relevance
from agentic_devtools.cli.ci.logging_config import setup_logging
from agentic_devtools.cli.ci.pipeline.command import run_ai_pr_loop_v2
from agentic_devtools.cli.ci.retry import RetryableError
from agentic_devtools.cli.ci.speckit_trigger import DEPRECATION_MESSAGE


def _python_orchestrator_enabled() -> bool:
    """Return True when the Python CI orchestrator path is enabled."""
    return os.environ.get("AGDT_USE_PYTHON_ORCHESTRATOR", "").lower() in ("1", "true")


def ai_pr_loop_command() -> None:
    """CLI entry point for the AI PR loop pipeline.

    Reads event data from ``GITHUB_EVENT_PATH`` and ``GITHUB_EVENT_NAME``
    environment variables, constructs a GitHub Actions provider, and
    invokes the idempotent action-evaluator pipeline (``run_ai_pr_loop_v2``).

    Routing is controlled by one feature flag:

    ``AGDT_USE_PYTHON_ORCHESTRATOR`` must be ``"1"`` or ``"true"`` to
    activate any Python-side processing.  When absent/false the function
    exits with code 0 so the legacy YAML path handles the run.

    Exit codes:
        0: Success or deferred to legacy path
        1: Guard blocked
        2: Malformed event
        3: Merge blocked
        4: Metadata resolution failed
        5: Repair dispatched
        6: Provider rate limit paused
        10: Missing dependency or configuration
    """
    # Feature flag check
    if not _python_orchestrator_enabled():
        # Legacy path — let the YAML handle it
        sys.exit(0)

    setup_logging()

    # Check gh CLI dependency
    if shutil.which("gh") is None:
        print("Error: 'gh' CLI not found on PATH. Install GitHub CLI to use agdt-ai-pr-loop.", file=sys.stderr)
        sys.exit(10)

    # Read event data
    event_path = os.environ.get("GITHUB_EVENT_PATH", "")
    event_name = os.environ.get("GITHUB_EVENT_NAME", "")

    if not event_path or not event_name:
        print("Error: GITHUB_EVENT_PATH and GITHUB_EVENT_NAME must be set.", file=sys.stderr)
        sys.exit(10)

    try:
        with open(event_path, encoding="utf-8") as f:
            raw_payload = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Error: Failed to read event payload: {exc}", file=sys.stderr)
        sys.exit(10)

    # Determine repository
    repo = os.environ.get("GITHUB_REPOSITORY", "")

    # Create provider and run pipeline
    provider = GitHubActionsProvider(repo=repo)

    try:
        event_payload = provider.parse_event(raw_payload, event_name)
    except MalformedEventError as exc:
        json.dump({"error": "malformed_event", "event_name": exc.event_name, "reason": exc.reason}, sys.stderr)
        sys.stderr.write("\n")
        sys.exit(2)

    # Edit-relevance preflight — skip body-only edits before pipeline calls
    should_skip, skip_reason = check_edit_relevance(event_payload)
    if should_skip:
        logger = logging.getLogger(__name__)
        logger.info("PR #%d: %s", event_payload.pr_number, skip_reason)
        sys.exit(0)

    exit_code = run_ai_pr_loop_v2(provider, event_payload)
    sys.exit(exit_code)


def speckit_trigger_command() -> None:
    """CLI entry point for the SpecKit trigger handler — DEPRECATED.

    This command is deprecated. Phase 1 is now handled by the unified
    ``speckit-phase-progression.yml`` workflow. The ``speckit-issue-trigger.yml``
    workflow dispatches to it directly via ``workflow_dispatch``.

    Exit codes:
        1: Always exits with 1 to indicate deprecation
    """
    print(f"Error: {DEPRECATION_MESSAGE}", file=sys.stderr)
    sys.exit(1)


def assign_implementation_agent_command() -> None:
    """Assign the SpecKit implementation coding agent to an issue."""
    parser = argparse.ArgumentParser(description="Assign SpecKit implementation coding agent")
    parser.add_argument("--issue-number", type=int, required=True, help="Issue number to assign")
    parser.add_argument("--spec-dir", type=str, required=True, help="Spec directory relative to repo root")
    parser.add_argument(
        "--spec-context",
        type=str,
        default=None,
        help="Optional inherited spec.md path for task-level specs",
    )
    parser.add_argument("--repo", type=str, default=None, help="Repository in owner/repo format")
    parser.add_argument("--model", type=str, default=None, help="Copilot model override")
    args = parser.parse_args()

    repo = (args.repo or os.environ.get("GITHUB_REPOSITORY", "")).strip()
    if not repo:
        print("Error: repository is required. Pass --repo or set GITHUB_REPOSITORY.", file=sys.stderr)
        sys.exit(1)
    normalized_repo = _validate_repo_format(repo)
    if normalized_repo is None:
        print("Error: repository must be in owner/repo format (e.g. owner/repo).", file=sys.stderr)
        sys.exit(1)
    repo = normalized_repo

    spec_dir = args.spec_dir.strip().strip("/")
    if not spec_dir:
        print("Error: --spec-dir must not be empty after normalization.", file=sys.stderr)
        sys.exit(1)
    issue_number = args.issue_number
    if issue_number <= 0:
        print("Error: --issue-number must be a positive integer.", file=sys.stderr)
        sys.exit(1)
    model = (args.model or "").strip() or None
    spec_context = (args.spec_context or "").strip() or None

    if spec_context is None:
        problem_statement = (
            "Implement all tasks defined in the planning artifacts located at "
            f"{spec_dir}/ "
            "(path is relative to the repository root — resolve to an absolute path before reading files). "
            f"Read {spec_dir}/tasks.md for the task list, {spec_dir}/plan.md for architecture, and {spec_dir}/spec.md "
            "for requirements. Follow the speckit.implement agent workflow."
        )
    else:
        normalized_spec_context = spec_context.replace("\\", "/")
        parent_spec_dir = normalized_spec_context.rsplit("/", 1)[0] if "/" in normalized_spec_context else "."
        parent_plan_path = f"{parent_spec_dir}/plan.md" if parent_spec_dir != "." else "plan.md"
        problem_statement = (
            "Implement all tasks defined in the planning artifacts located at "
            f"{spec_dir}/ "
            "(path is relative to the repository root — resolve to an absolute path before reading files). "
            f"Read {spec_dir}/tasks.md for the task list. This is a task-level spec that inherits requirements and "
            f"architecture from parent artifacts: {normalized_spec_context} and {parent_plan_path}. "
            "Follow the speckit.implement agent workflow."
        )
    result = assign_issue_to_agent(
        repo=repo,
        issue_number=issue_number,
        problem_statement=problem_statement,
        custom_instructions=problem_statement,
        custom_agent="speckit.implement",
        model=model,
        token_env_vars=("SPECKIT_PR_TOKEN", "COPILOT_GITHUB_TOKEN"),
    )
    print(json.dumps(asdict(result)))
    sys.exit(0 if result.success else 1)


_SPECKIT_AGENT_BY_PHASE = {1: "speckit.specify", 2: "speckit.clarify", 3: "speckit.plan"}
_DEFAULT_SPECKIT_BASE_BRANCH = "main"
_SPECKIT_PHASE_LABEL_COLOR = "5319E7"
_SPECKIT_PROCESSING_LABEL_COLOR = "0366D6"
_SPECKIT_SPEC_DIR_PART_PATTERN = re.compile(r"^[A-Za-z0-9._-]+$")
_SPECKIT_MARKER_PATTERN = re.compile(
    r"<!--\s*speckit:agent-assigned schema_version=1 engine=cloud-agent "
    r"issue=(\d+) phase=(\d+) hierarchy=([^\s]+) correlation_id=([0-9a-fA-F-]+)\s*-->"
)


def _cloud_agent_result(
    result: AgentAssignmentResult,
    *,
    issue_number: int,
    phase: int,
    correlation_id: str,
    status: str,
) -> dict:
    payload = asdict(result)
    payload.update(
        {
            "engine": "cloud-agent",
            "phase": phase,
            "issue_number": issue_number,
            "correlation_id": correlation_id,
            "status": status,
        }
    )
    return payload


def _parse_paginated_documents(payload_text: str) -> list[object]:
    """Parse one or more concatenated JSON documents from ``gh api --paginate``."""
    decoder = json.JSONDecoder()
    payload = payload_text.strip()
    documents: list[object] = []
    index = 0
    while index < len(payload):
        while index < len(payload) and payload[index].isspace():
            index += 1
        parsed, next_index = decoder.raw_decode(payload, index)
        documents.append(parsed)
        index = next_index
    flattened: list[object] = []
    for document in documents:
        if isinstance(document, list):
            flattened.extend(document)
        else:
            flattened.append(document)
    return flattened


def _derive_speckit_base_branch(*, phase: int, hierarchy_level: str, issue_number: int) -> str:
    """Return the expected cloud-agent base branch for the given SpecKit phase.

    Mirrors the ``expectedCloudBaseRef`` function in
    ``extract-phase-info.js`` — both must be kept in sync.

    Phase 2 targets the phase-1 output branch so the clarify agent has
    access to the specify artifacts. Non-task phase 3 targets the phase-2
    output branch for the same reason. All other phases (phase 1, and task
    phase 3) target ``main``.
    """
    if phase == 2:
        return f"speckit/{issue_number}/phase-1-specify"
    if phase == 3 and hierarchy_level != "task":
        return f"speckit/{issue_number}/phase-2-clarify"
    return _DEFAULT_SPECKIT_BASE_BRANCH


def _ensure_speckit_tracking_labels(*, repo: str, phase: int, token: str) -> None:
    """Ensure cloud-agent tracking labels exist before applying them to the issue."""
    labels = {
        f"speckit:agent-assigned-phase-{phase}": (
            _SPECKIT_PHASE_LABEL_COLOR,
            "SpecKit cloud-agent phase dispatch is active for this issue.",
        ),
        "speckit:processing": (
            _SPECKIT_PROCESSING_LABEL_COLOR,
            "SpecKit processing is active for this issue.",
        ),
    }
    existing_payload = _parse_paginated_documents(
        _gh_api_call(
            f"/repos/{repo}/labels?per_page=100",
            method="GET",
            paginate=True,
            token=token,
        )
    )
    existing_names = {
        str(label.get("name"))
        for label in existing_payload
        if isinstance(label, dict) and isinstance(label.get("name"), str)
    }
    for label_name, (color, description) in labels.items():
        if label_name in existing_names:
            continue
        try:
            _gh_api_call(
                f"/repos/{repo}/labels",
                method="POST",
                body={"name": label_name, "color": color, "description": description},
                token=token,
            )
        except RuntimeError as exc:
            message = str(exc).lower()
            if "already_exists" in message or "already exists" in message or re.search(r"\b422\b", message):
                continue
            raise


def _cloud_agent_pr_matches(pr: object, *, issue_number: int, phase: int) -> bool:
    if not isinstance(pr, dict):
        return False
    user = pr.get("user")
    if not isinstance(user, dict) or user.get("login") not in {"copilot-swe-agent", "copilot-swe-agent[bot]"}:
        return False
    body = pr.get("body")
    if not isinstance(body, str):
        return False
    match = _SPECKIT_MARKER_PATTERN.search(body)
    if not match:
        return False
    marker_issue_number = int(match.group(1))
    marker_phase = int(match.group(2))
    marker_hierarchy_level = str(match.group(3)).lower()
    if marker_issue_number != issue_number or marker_phase != phase:
        return False
    expected_base = _derive_speckit_base_branch(
        phase=marker_phase,
        hierarchy_level=marker_hierarchy_level,
        issue_number=marker_issue_number,
    )
    base = pr.get("base")
    base_ref = base.get("ref") if isinstance(base, dict) else None
    return base_ref == expected_base


def _cloud_agent_in_flight(*, repo: str, issue_number: int, phase: int, token: str) -> bool:
    labels_payload = _parse_paginated_documents(
        _gh_api_call(
            f"/repos/{repo}/issues/{issue_number}/labels",
            method="GET",
            paginate=True,
            token=token,
        )
    )
    if any(
        isinstance(label, dict) and label.get("name") == f"speckit:agent-assigned-phase-{phase}"
        for label in labels_payload
    ):
        return True
    pulls_payload = _parse_paginated_documents(
        _gh_api_call(
            f"/repos/{repo}/pulls?state=open&per_page=100",
            method="GET",
            paginate=True,
            token=token,
        )
    )
    return any(_cloud_agent_pr_matches(pr, issue_number=issue_number, phase=phase) for pr in pulls_payload)


def _post_cloud_agent_issue_mutation(*, repo: str, issue_number: int, body: str, token: str) -> None:
    _gh_api_call(
        f"/repos/{repo}/issues/{issue_number}/comments",
        method="POST",
        body={"body": body},
        token=token,
    )


def assign_speckit_agent_command() -> None:
    """Dispatch and track one asynchronous Cloud Coding Agent SpecKit phase."""
    parser = argparse.ArgumentParser(description="Assign a Cloud Coding Agent to a SpecKit phase")
    parser.add_argument("--issue-number", type=int, required=True)
    parser.add_argument("--phase", type=int, choices=(1, 2, 3), required=True)
    parser.add_argument("--hierarchy-level", default="feature", choices=("epic", "feature", "task", "unknown"))
    parser.add_argument("--spec-dir", default=None)
    parser.add_argument("--custom-agent", default=None)
    parser.add_argument("--custom-instructions", default="")
    parser.add_argument("--model", default=None)
    parser.add_argument("--base-branch", default=None)
    parser.add_argument("--correlation-id", default="")
    parser.add_argument("--repo", default=None)
    args = parser.parse_args()

    repo = (args.repo or os.environ.get("GITHUB_REPOSITORY", "")).strip()
    validated_repo = _validate_repo_format(repo) if repo else None
    if validated_repo is None:
        print(json.dumps({"engine": "cloud-agent", "status": "invalid-repository"}))
        sys.exit(1)
    if args.issue_number <= 0:
        print(json.dumps({"engine": "cloud-agent", "status": "invalid-issue-number"}))
        sys.exit(1)
    repo = validated_repo
    phase = args.phase
    hierarchy_level = args.hierarchy_level
    raw_spec_dir = (args.spec_dir or "").strip()
    spec_dir = None
    if raw_spec_dir:
        normalized_spec_dir = raw_spec_dir.replace("\\", "/").rstrip("/")
        parts = normalized_spec_dir.split("/")
        if (
            len(parts) < 2
            or parts[0] != "specs"
            or any(part in {"", ".", ".."} or not _SPECKIT_SPEC_DIR_PART_PATTERN.fullmatch(part) for part in parts)
        ):
            print(json.dumps({"engine": "cloud-agent", "status": "invalid-spec-dir"}))
            sys.exit(1)
        spec_dir = normalized_spec_dir
    if phase == 3 and hierarchy_level.strip().lower() == "task" and not spec_dir:
        print(json.dumps({"engine": "cloud-agent", "status": "invalid-spec-dir"}))
        sys.exit(1)
    expected_base_branch = _derive_speckit_base_branch(
        phase=phase, hierarchy_level=hierarchy_level, issue_number=args.issue_number
    )
    if args.base_branch is None:
        args.base_branch = expected_base_branch
    elif args.base_branch != expected_base_branch:
        print(json.dumps({"engine": "cloud-agent", "status": "invalid-base-branch"}))
        sys.exit(1)
    token_identity, token = _resolve_assignment_token(("SPECKIT_PR_TOKEN", "COPILOT_GITHUB_TOKEN"))
    raw_correlation_id = args.correlation_id.strip()
    if raw_correlation_id:
        try:
            correlation_id = str(uuid.UUID(raw_correlation_id))
        except ValueError:
            print(json.dumps({"engine": "cloud-agent", "status": "invalid-correlation-id"}))
            sys.exit(1)
    else:
        correlation_id = str(uuid.uuid4())
    model = (
        args.model or os.environ.get("SPECKIT_COPILOT_MODEL") or os.environ.get("COPILOT_MODEL") or "claude-opus-4.6"
    ).strip()
    custom_agent = args.custom_agent or _SPECKIT_AGENT_BY_PHASE[phase]
    marker = (
        "<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent "
        f"issue={args.issue_number} phase={phase} hierarchy={hierarchy_level} correlation_id={correlation_id} -->"
    )
    phase_contract_instructions = []
    if phase in {1, 2}:
        phase_contract_instructions.append(
            "This run is unattended. Do not wait for user answers; resolve clarifications "
            "from available issue/spec context and continue."
        )
    if phase == 3:
        phase_contract_instructions.append(
            "Complete the full phase-3 artifact chain in this PR: planning plus downstream "
            "tasks/analysis generation as applicable "
            "to the hierarchy level, so progression can evaluate terminal artifacts from the merged branch."
        )
    if phase == 3 and hierarchy_level.strip().lower() == "task" and spec_dir:
        phase_contract_instructions.append(
            "This is a task-level phase running from `main`. For every SpecKit scaffold command "
            "that resolves the active feature in this run (including "
            "`agdt-speckit-scaffold-plan`, `agdt-speckit-scaffold-tasks`, and "
            f"`agdt-speckit-scaffold-update-agent-context`), prefix the command with "
            f'`SPECIFY_FEATURE_DIRECTORY="{spec_dir}"` from the repository root so the '
            "task spec and inherited parent context resolve correctly."
        )
    phase_instructions = "\n".join(
        [
            f"Execute SpecKit phase {phase} with the {custom_agent} workflow for issue #{args.issue_number}.",
            f"Hierarchy level: {hierarchy_level}. Target base branch: {args.base_branch}.",
            *phase_contract_instructions,
            marker,
            "Copy the marker into the pull request description unchanged.",
        ]
    )
    instructions = f"{args.custom_instructions.strip()}\n\n{phase_instructions}".strip()
    problem_statement = f"Complete SpecKit phase {phase} for issue #{args.issue_number} using {custom_agent}."

    if not token:
        result = AgentAssignmentResult(
            success=False,
            method="",
            token_identity="",
            error="Missing assignment token. Set SPECKIT_PR_TOKEN or COPILOT_GITHUB_TOKEN",
        )
        print(
            json.dumps(
                _cloud_agent_result(
                    result,
                    issue_number=args.issue_number,
                    phase=phase,
                    correlation_id=correlation_id,
                    status="assignment-failed",
                )
            )
        )
        sys.exit(1)

    try:
        if _cloud_agent_in_flight(repo=repo, issue_number=args.issue_number, phase=phase, token=token):
            result = AgentAssignmentResult(
                success=True,
                method="already_in_flight",
                token_identity=token_identity,
            )
            print(
                json.dumps(
                    _cloud_agent_result(
                        result,
                        issue_number=args.issue_number,
                        phase=phase,
                        correlation_id=correlation_id,
                        status="already-in-flight",
                    )
                )
            )
            sys.exit(0)
    except (RetryableError, RuntimeError, json.JSONDecodeError) as exc:
        result = AgentAssignmentResult(
            success=False,
            method="",
            token_identity=token_identity,
            error=f"In-flight check failed: {exc}",
        )
        print(
            json.dumps(
                _cloud_agent_result(
                    result,
                    issue_number=args.issue_number,
                    phase=phase,
                    correlation_id=correlation_id,
                    status="assignment-failed",
                )
            )
        )
        sys.exit(1)

    result = assign_issue_to_agent(
        repo=repo,
        issue_number=args.issue_number,
        problem_statement=problem_statement,
        custom_instructions=instructions,
        base_branch=args.base_branch,
        custom_agent=custom_agent,
        model=model,
        allow_preexisting_assignment=False,
        token_env_vars=("SPECKIT_PR_TOKEN", "COPILOT_GITHUB_TOKEN"),
    )
    if not result.success or not result.session_confirmed:
        status = "assignment-failed"
        if result.success and not result.session_confirmed:
            status = "assignment-unconfirmed"
            result = AgentAssignmentResult(
                success=False,
                method=result.method,
                task_id=result.task_id,
                task_url=result.task_url,
                attempts=result.attempts,
                token_identity=result.token_identity,
                error=(
                    "Assignment accepted but no confirmed Copilot session/task signal was observed; "
                    "authoritative tracking state was not recorded."
                ),
                session_confirmed=False,
            )
        print(
            json.dumps(
                _cloud_agent_result(
                    result,
                    issue_number=args.issue_number,
                    phase=phase,
                    correlation_id=correlation_id,
                    status=status,
                )
            )
        )
        sys.exit(1)

    try:
        _ensure_speckit_tracking_labels(repo=repo, phase=phase, token=token)
        _gh_api_call(
            f"/repos/{repo}/issues/{args.issue_number}/labels",
            method="POST",
            body={"labels": [f"speckit:agent-assigned-phase-{phase}", "speckit:processing"]},
            token=token,
        )
        _post_cloud_agent_issue_mutation(
            repo=repo,
            issue_number=args.issue_number,
            body=marker,
            token=token,
        )
    except (RetryableError, RuntimeError, json.JSONDecodeError) as exc:
        result = AgentAssignmentResult(
            success=False,
            method=result.method,
            task_id=result.task_id,
            task_url=result.task_url,
            attempts=result.attempts,
            token_identity=token_identity,
            error=f"Partial tracking failure: {exc}",
            session_confirmed=result.session_confirmed,
        )
        print(
            json.dumps(
                _cloud_agent_result(
                    result,
                    issue_number=args.issue_number,
                    phase=phase,
                    correlation_id=correlation_id,
                    status="partial-tracking-failure",
                )
            )
        )
        sys.exit(1)

    notice_warning = ""
    try:
        _post_cloud_agent_issue_mutation(
            repo=repo,
            issue_number=args.issue_number,
            body=(
                f"🚀 Cloud Agent started SpecKit phase {phase} for hierarchy `{hierarchy_level}` "
                f"against `{args.base_branch}` (correlation ID `{correlation_id}`)."
            ),
            token=token,
        )
    except (RetryableError, RuntimeError, json.JSONDecodeError) as exc:
        notice_warning = f"Non-authoritative notice failed: {exc}"

    result = AgentAssignmentResult(
        success=True,
        method=result.method,
        task_id=result.task_id,
        task_url=result.task_url,
        attempts=result.attempts,
        token_identity=token_identity,
        session_confirmed=result.session_confirmed,
    )
    payload = _cloud_agent_result(
        result,
        issue_number=args.issue_number,
        phase=phase,
        correlation_id=correlation_id,
        status="dispatched",
    )
    if notice_warning:
        payload["warning"] = notice_warning
    print(json.dumps(payload))
    sys.exit(0)
