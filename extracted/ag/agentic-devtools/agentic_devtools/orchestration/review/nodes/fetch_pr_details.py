"""``fetch_pr_details`` node — fetches normalized pull-request review details."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from collections.abc import Mapping
from typing import Any

from agentic_devtools.adapters.retry import detect_transient_status_code


def _normalize_jira_issue(raw_issue: dict[str, Any]) -> dict[str, Any]:
    """Extract review-relevant fields from raw Jira API response.

    Returns a normalized dict with 8 keys suitable for downstream review
    context. Missing or malformed fields default to empty/None values.
    """
    raw_fields = raw_issue.get("fields")
    fields = raw_fields if isinstance(raw_fields, dict) else {}

    # Normalize key/summary to str — dict.get() can return None when the key
    # is explicitly present with a None value, so we guard explicitly.
    key_raw = raw_issue.get("key", "")
    key = key_raw if isinstance(key_raw, str) else ""
    summary_raw = fields.get("summary", "")
    summary = summary_raw if isinstance(summary_raw, str) else ""

    # Normalize description to str | None — the Jira API can return Atlassian
    # Document Format objects (dicts) for newer API versions.
    description_raw = fields.get("description")
    description = description_raw if isinstance(description_raw, str) else None

    # Treat a blank/whitespace env-var override as unset so that fields.get("")
    # is never invoked.
    ac_field_env = os.environ.get("JIRA_ACCEPTANCE_CRITERIA_FIELD", "").strip()
    ac_field = ac_field_env if ac_field_env else "customfield_10014"
    # Normalize acceptance_criteria to a non-empty str | None — Jira can return
    # non-string values (e.g. ADF dicts) or whitespace-only strings for the
    # custom field, neither of which should leak into downstream prompts.
    ac_value = fields.get(ac_field)
    acceptance_criteria = ac_value.strip() if isinstance(ac_value, str) and ac_value.strip() else None

    # Normalize labels to list[str] — drop any non-string entries the Jira API
    # might return so downstream consumers always get a clean list of strings.
    labels_raw = fields.get("labels")
    labels = [label for label in labels_raw if isinstance(label, str)] if isinstance(labels_raw, list) else []
    status_raw = fields.get("status")
    issuetype_raw = fields.get("issuetype")
    priority_raw = fields.get("priority")
    return {
        "key": key,
        "summary": summary,
        "description": description,
        "status": status_raw.get("name") if isinstance(status_raw, dict) else None,
        "issue_type": issuetype_raw.get("name") if isinstance(issuetype_raw, dict) else None,
        "labels": labels,
        "acceptance_criteria": acceptance_criteria,
        "priority": priority_raw.get("name") if isinstance(priority_raw, dict) else None,
    }


def _sanitize_provider_error(exc: Exception | SystemExit) -> str:
    """Map provider failures to actionable categories without exposing raw output."""
    message = str(exc).casefold()
    if isinstance(exc, subprocess.TimeoutExpired) or "timed out" in message or "timeout" in message:
        return "provider request timed out; retry the request"
    transient_status = detect_transient_status_code(message)
    if transient_status == 429 or re.search(r"\b(?:rate limit|secondary limit)\b", message):
        return "provider rate limited the request; retry later"
    if transient_status in {502, 503}:
        return "provider is temporarily unavailable; retry later"
    if re.search(r"\bcredentials?\b", message) or (
        re.search(r"(?<![a-z0-9])(?:token|pat)(?![a-z0-9])", message)
        and re.search(r"\b(?:missing|not\s+set|not\s+configured|not\s+provided|required)\b", message)
    ):
        return "provider credentials are missing; configure the required token"
    if re.search(r"\bhttp(?:/\d+(?:\.\d+)?)?\s+(?:401|403)\b", message) or any(
        marker in message for marker in ("unauthorized", "forbidden", "bad credentials")
    ):
        return "provider authorization failed; check token permissions"
    if (
        re.search(r"\bhttp(?:/\d+(?:\.\d+)?)?\s+404\b", message)
        or "not found" in message
        or "does not exist" in message
    ):
        return "pull request or repository not found; verify the PR number and repository"
    if any(marker in message for marker in ("malformed", "invalid json", "invalid response", "head sha")):
        return "provider returned malformed pull-request details; retry"
    return "provider request failed; verify provider settings and retry"


def fetch_pr_details_node(state: dict[str, Any]) -> dict[str, Any]:
    """Fetch normalized PR details and translate them into review graph state."""
    pr_id = state.get("pr_id")
    if pr_id is None or pr_id == "":
        return {"errors": [f"fetch_pr_details: pr_id is required but was {pr_id!r}"]}
    invalid_pr_id = f"fetch_pr_details: pr_id must be a positive integer but was {pr_id!r}"
    if isinstance(pr_id, bool):
        return {"errors": [invalid_pr_id]}
    if isinstance(pr_id, int):
        normalized_pr_id = pr_id
    elif isinstance(pr_id, str):
        normalized_pr_id_str = pr_id.strip()
        if not normalized_pr_id_str.isascii() or not normalized_pr_id_str.isdigit():
            return {"errors": [invalid_pr_id]}
        normalized_pr_id = int(normalized_pr_id_str)
    else:
        return {"errors": [invalid_pr_id]}
    if normalized_pr_id <= 0:
        return {"errors": [invalid_pr_id]}

    from agentic_devtools.adapters.pull_request_details import _deep_merge_state, detect_provider
    from agentic_devtools.state import load_state_locked

    try:
        provider_state = _deep_merge_state(load_state_locked(), state)
    except Exception:
        provider_state = state
    try:
        selected_provider = detect_provider(state=provider_state, allow_remote=False)
    except ValueError:
        return {
            "errors": [
                "fetch_pr_details: provider configuration is missing or unsupported; "
                "set platform.code_hosting or provider"
            ]
        }

    from agentic_devtools.cli.pull_request_details import get_pull_request_details

    try:
        details_payload = get_pull_request_details(
            provider=selected_provider,
            pull_request_id=normalized_pr_id,
            repository=None,
            state=provider_state,
        )
    except (Exception, SystemExit) as exc:
        return {"errors": [f"fetch_pr_details: {_sanitize_provider_error(exc)}"]}
    if not isinstance(details_payload, Mapping):
        return {
            "errors": [f"fetch_pr_details: {_sanitize_provider_error(RuntimeError('malformed provider response'))}"]
        }

    raw_pr_data = details_payload.get("pullRequest")
    pr_data = dict(raw_pr_data) if isinstance(raw_pr_data, Mapping) else {}
    raw_repository = details_payload.get("repository")
    repository = dict(raw_repository) if isinstance(raw_repository, Mapping) else {}
    raw_project = repository.get("project")
    project_data = raw_project if isinstance(raw_project, Mapping) else {}
    raw_files = details_payload.get("files")
    files = raw_files if isinstance(raw_files, list) else []
    raw_threads = details_payload.get("threads")
    threads = raw_threads if isinstance(raw_threads, list) else []
    raw_iterations = details_payload.get("iterations")
    if isinstance(raw_iterations, list):
        iterations = raw_iterations
    elif isinstance(raw_iterations, Mapping):
        raw_items = raw_iterations.get("items")
        iterations = raw_items if isinstance(raw_items, list) else []
    else:
        iterations = []

    iteration_ids = [
        item["id"]
        for item in iterations
        if isinstance(item, Mapping) and isinstance(item.get("id"), int) and not isinstance(item.get("id"), bool)
    ]
    latest_iteration_id = max(iteration_ids, default=0)
    raw_source_commit = pr_data.get("lastMergeSourceCommit")
    source_commit = raw_source_commit if isinstance(raw_source_commit, Mapping) else {}
    raw_target_commit = pr_data.get("lastMergeTargetCommit")
    target_commit = raw_target_commit if isinstance(raw_target_commit, Mapping) else {}
    commit_hash = source_commit.get("commitId")
    commit_hash = commit_hash.strip() if isinstance(commit_hash, str) else ""
    base_commit_hash = target_commit.get("commitId")
    base_commit_hash = base_commit_hash.strip() if isinstance(base_commit_hash, str) else ""
    repo_id = repository.get("id")
    repo_id = repo_id if isinstance(repo_id, str) else ""
    project = project_data.get("name")
    project = project if isinstance(project, str) else ""
    raw_organization = provider_state.get("organization")
    if not isinstance(raw_organization, str):
        azure_state = provider_state.get("azure_devops")
        raw_organization = azure_state.get("organization") if isinstance(azure_state, Mapping) else None
    organization = raw_organization if selected_provider == "azure_devops" and isinstance(raw_organization, str) else ""

    raw_jira_issue_key = state.get("jira_issue_key")
    jira_issue_key = raw_jira_issue_key.strip() if isinstance(raw_jira_issue_key, str) else ""
    jira_pattern: re.Pattern[str] | None = None
    if not jira_issue_key:
        raw_issue_key = state.get("issue_key")
        if isinstance(raw_issue_key, str) and raw_issue_key.strip():
            try:
                from agentic_devtools.cli.jira.config import build_jira_issue_pattern, get_jira_project_keys

                jira_pattern = build_jira_issue_pattern(get_jira_project_keys())
                match = jira_pattern.fullmatch(raw_issue_key.strip())
                if match:
                    jira_issue_key = match.group(1).upper()
            except Exception:
                jira_pattern = None
    if not jira_issue_key:
        try:
            from agentic_devtools.state import get_value

            state_issue_key = get_value("jira.issue_key")
            jira_issue_key = state_issue_key.strip() if isinstance(state_issue_key, str) else ""
        except Exception:
            jira_issue_key = ""
    if not jira_issue_key:
        try:
            if jira_pattern is None:
                from agentic_devtools.cli.jira.config import build_jira_issue_pattern, get_jira_project_keys

                jira_pattern = build_jira_issue_pattern(get_jira_project_keys())
            for candidate in (
                pr_data.get("sourceRefName"),
                pr_data.get("title"),
                pr_data.get("description"),
            ):
                if isinstance(candidate, str):
                    match = jira_pattern.search(candidate)
                    if match:
                        jira_issue_key = match.group(1).upper()
                        break
        except Exception as exc:
            print(
                f"Warning: fetch_pr_details: Jira key auto-detection failed: {exc}",
                file=sys.stderr,
            )

    repo_config: dict[str, Any] = {}
    non_fatal_errors: list[str] = []
    try:
        from agentic_devtools.cli.azure_devops.pr_review_manifest import resolve_repo_root
        from agentic_devtools.config import load_repo_config

        repo_root = os.environ.get("AGDT_REPO_ROOT") or resolve_repo_root()
        repo_config = load_repo_config(repo_root)
    except Exception as exc:
        warning = f"fetch_pr_details: failed to load repo config: {exc}"
        print(f"Warning: {warning}", file=sys.stderr)

    jira_issue: dict[str, Any] | None = None
    if jira_issue_key:
        try:
            from agentic_devtools.cli.jira.config import get_jira_base_url, get_jira_headers
            from agentic_devtools.cli.jira.helpers import _get_ssl_verify
            from agentic_devtools.tools.jira import JiraConfig, fetch_issue_context

            jira_config = JiraConfig(
                base_url=get_jira_base_url(),
                headers=get_jira_headers(),
                ssl_verify=_get_ssl_verify(),
            )
            context_result = fetch_issue_context(jira_config, jira_issue_key)
            raw_issue = context_result.get("issue")
            if isinstance(raw_issue, dict):
                jira_issue = _normalize_jira_issue(raw_issue)
        except Exception as exc:
            print(
                f"Warning: fetch_pr_details: failed to fetch Jira issue {jira_issue_key}: {exc}",
                file=sys.stderr,
            )

    try:
        from agentic_devtools.state import get_state_dir

        output_path = get_state_dir() / f"temp-langchain-pr-details-{pr_id}.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        artifact = {
            "pr_data": pr_data,
            "files": files,
            "threads": threads,
            "iterations": iterations,
            "jira_issue_key": jira_issue_key,
            "jira_issue": jira_issue,
        }
        output_path.write_text(json.dumps(artifact, indent=2, default=str), encoding="utf-8")
    except Exception as exc:
        non_fatal_errors.append(f"fetch_pr_details: failed to persist PR details artifact: {exc}")

    errors = non_fatal_errors
    if not repo_id:
        errors.append("fetch_pr_details: repository id is missing from PR payload")
    if not files:
        errors.append("fetch_pr_details: no changed files were retrieved")
    return {
        "files": files,
        "threads": threads,
        "commit_hash": commit_hash,
        "base_commit_hash": base_commit_hash,
        "latest_iteration_id": latest_iteration_id,
        "iterations": iterations,
        "jira_issue": jira_issue,
        "repo_id": repo_id,
        "project": project,
        "organization": organization,
        "jira_issue_key": jira_issue_key,
        "config": repo_config,
        "errors": errors,
    }
