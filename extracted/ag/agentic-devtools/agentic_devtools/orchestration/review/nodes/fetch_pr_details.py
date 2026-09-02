"""``fetch_pr_details`` node — fetches complete PR details from Azure DevOps.

Satisfies FR-001 through FR-010 by calling existing retrieval functions to
populate ``ReviewGraphState`` with the full diff payload, threads, iteration
metadata, Jira issue details, and last merge source commit hash.
"""

from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
from dataclasses import replace
from typing import Any
from urllib.parse import quote, unquote


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


def fetch_pr_details_node(state: dict[str, Any]) -> dict[str, Any]:
    """Fetch complete PR details from Azure DevOps.

    Reads ``pr_id`` from the graph state, calls the existing PR detail
    retrieval infrastructure, and populates the state with diff payload,
    threads, iterations, commit hash, and Jira issue details.

    Args:
        state: Current ``ReviewGraphState``.

    Returns:
        State update dict with ``files``, ``threads``, ``commit_hash``,
        ``repo_id``, ``project``, ``organization``, ``jira_issue_key``,
        ``config``, ``iterations``, and ``jira_issue``.
    """
    from agentic_devtools.cli.azure_devops.auth import get_auth_headers, get_pat
    from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
    from agentic_devtools.cli.azure_devops.helpers import (
        find_jira_issue_from_pr,
    )
    from agentic_devtools.cli.azure_devops.helpers import (
        get_pull_request_details as fetch_pr_via_rest,
    )
    from agentic_devtools.config import load_repo_config
    from agentic_devtools.state import get_value

    pr_id = state.get("pr_id")
    if not pr_id:
        return {"errors": [f"fetch_pr_details: pr_id is required but was {pr_id!r}"]}

    try:
        config = AzureDevOpsConfig.from_state()
    except Exception as exc:
        print(f"fetch_pr_details: failed to load ADO config: {exc}", file=sys.stderr)
        return {"errors": ["fetch_pr_details: failed to load ADO config"]}

    try:
        pat = get_pat()
        headers = get_auth_headers(pat)
    except Exception as exc:
        print(f"fetch_pr_details: authentication failed: {exc}", file=sys.stderr)
        return {"errors": ["fetch_pr_details: authentication failed"]}

    # Fetch basic PR data via existing helper
    # Normalize first so project values that already came from encoded
    # remotes/state are not double-encoded before reaching older REST
    # helpers that still expect a URL-safe project segment.
    project_for_urls = quote(unquote(config.project), safe="")
    config_for_urls = config
    if project_for_urls != config.project:
        if isinstance(config, AzureDevOpsConfig):
            config_for_urls = replace(config, project=project_for_urls)
        else:
            config_for_urls = copy.copy(config)
            config_for_urls.project = project_for_urls

    pr_data = fetch_pr_via_rest(int(pr_id), config_for_urls, headers)
    if not pr_data:
        return {"errors": [f"fetch_pr_details: failed to fetch PR #{pr_id}"]}

    # Extract commit hash
    last_merge = pr_data.get("lastMergeSourceCommit", {})
    commit_hash = last_merge.get("commitId", "")
    if not commit_hash or not commit_hash.strip():
        print(
            f"Warning: fetch_pr_details: lastMergeSourceCommit.commitId is missing or blank "
            f"for PR #{pr_id}; source-context lookups and commit-hash-based markers will be "
            f"unavailable",
            file=sys.stderr,
        )
        commit_hash = ""

    # Extract base commit hash (target branch merge base)
    last_merge_target = pr_data.get("lastMergeTargetCommit") or {}
    if not isinstance(last_merge_target, dict):
        last_merge_target = {}
    base_commit_hash = last_merge_target.get("commitId") or ""
    if not isinstance(base_commit_hash, str) or not base_commit_hash.strip():
        base_commit_hash = ""

    # Extract repo info
    repo = pr_data.get("repository", {})
    repo_id = repo.get("id", "")
    project_name = repo.get("project", {}).get("name")
    if isinstance(project_name, str) and project_name.strip():
        project = unquote(project_name)
    else:
        project = unquote(config.project)
    organization = config.organization

    # Fetch threads
    threads: list[dict[str, Any]] = []
    try:
        from agentic_devtools.cli.azure_devops.pull_request_details_commands import (
            _get_iteration_changes,
            _get_pull_request_iterations,
            _get_pull_request_threads,
        )

        raw_threads = _get_pull_request_threads(organization, project_for_urls, repo_id, int(pr_id), headers)
        if raw_threads:
            threads = raw_threads
    except Exception as exc:
        print(f"Warning: fetch_pr_details: failed to fetch threads: {exc}", file=sys.stderr)

    # Build file list from PR changes
    files: list[dict[str, Any]] = []
    latest_iteration_id = 0
    iteration_metadata: list[dict[str, Any]] = []
    try:
        iterations = _get_pull_request_iterations(organization, project_for_urls, repo_id, int(pr_id), headers)
        if iterations:
            # Extract lightweight metadata for all iterations (FR-003).
            # Guard against any non-dict placeholders that the ADO client
            # might return (e.g. None entries in a partial API response).
            iteration_metadata = [
                {
                    "id": it.get("id"),
                    "description": it.get("description"),
                    "sourceRefCommit": it.get("sourceRefCommit"),
                    "targetRefCommit": it.get("targetRefCommit"),
                    "createdDate": it.get("createdDate"),
                    "reason": it.get("reason"),
                }
                for it in iterations
                if isinstance(it, dict)
            ]

            latest_iteration = next((it for it in reversed(iterations) if isinstance(it, dict)), {})
            latest_iteration_id = latest_iteration.get("id", 0)
            iteration_id = latest_iteration_id if isinstance(latest_iteration_id, int) else 0
            diff_base_ref: str | None = None
            diff_compare_ref: str | None = None
            get_diff_lines_info = None
            get_diff_patch = None

            try:
                from agentic_devtools.cli.git.diff import (
                    get_diff_lines_info as _get_diff_lines_info,
                )
                from agentic_devtools.cli.git.diff import (
                    get_diff_patch as _get_diff_patch,
                )
                from agentic_devtools.cli.git.diff import (
                    normalize_ref_name,
                    sync_git_ref,
                )

                target_branch = normalize_ref_name(pr_data.get("targetRefName"))
                source_branch = normalize_ref_name(pr_data.get("sourceRefName"))
                # Reuse the already-validated dict/hash extracted above so
                # a non-dict lastMergeTargetCommit payload cannot raise
                # AttributeError here.
                base_commit = base_commit_hash or None
                source_commit = pr_data.get("lastMergeSourceCommit", {}).get("commitId")
                diff_base_ref = base_commit or (f"origin/{target_branch}" if target_branch else "origin/main")
                diff_compare_ref = source_commit or (f"origin/{source_branch}" if source_branch else "HEAD")
                if target_branch:
                    sync_git_ref(f"origin/{target_branch}")
                if source_branch:
                    sync_git_ref(f"origin/{source_branch}")
                get_diff_lines_info = _get_diff_lines_info
                get_diff_patch = _get_diff_patch
            except Exception as exc:
                print(
                    f"Warning: fetch_pr_details: git ref sync failed: {exc}",
                    file=sys.stderr,
                )

            changes = _get_iteration_changes(
                organization,
                project_for_urls,
                repo_id,
                int(pr_id),
                iteration_id,
                headers,
            )
            if changes:
                for change in changes:
                    item = change.get("item", {})
                    file_path = item.get("path", "")
                    if file_path and not item.get("isFolder", False):
                        file_entry: dict[str, Any] = {
                            "path": file_path,
                            "changeType": change.get("changeType", "edit"),
                            "item": item,
                        }
                        original_path = change.get("originalPath")
                        if isinstance(original_path, str) and original_path:
                            file_entry["originalPath"] = original_path
                        if (
                            callable(get_diff_lines_info)
                            and callable(get_diff_patch)
                            and diff_base_ref is not None
                            and diff_compare_ref is not None
                        ):
                            try:
                                # ADO paths include a leading slash (e.g. "/src/main.py").
                                # git diff functions expect repo-root-relative paths without it.
                                git_file_path = file_path.lstrip("/")
                                diff_info = get_diff_lines_info(
                                    diff_base_ref, diff_compare_ref, git_file_path, timeout=10
                                )
                            except subprocess.TimeoutExpired:
                                print(
                                    f"Warning: fetch_pr_details: diff computation timed out for {file_path}",
                                    file=sys.stderr,
                                )
                                file_entry["patch"] = None
                                file_entry["isBinary"] = False
                                file_entry["addedLines"] = []
                                file_entry["removedLines"] = []
                            except Exception as diff_exc:
                                print(
                                    f"Warning: fetch_pr_details: diff enrichment failed for {file_path}: {diff_exc}",
                                    file=sys.stderr,
                                )
                                file_entry["patch"] = None
                                file_entry["isBinary"] = False
                                file_entry["addedLines"] = []
                                file_entry["removedLines"] = []
                            else:
                                file_entry.update(
                                    {
                                        "isBinary": diff_info.added.is_binary,
                                        "addedLines": [
                                            {"line": line.line_number, "content": line.content}
                                            for line in diff_info.added.lines
                                        ],
                                        "removedLines": [
                                            {"line": line.line_number, "content": line.content}
                                            for line in diff_info.removed.lines
                                        ],
                                        "patch": None,
                                    }
                                )
                                if not diff_info.added.is_binary:
                                    try:
                                        file_entry["patch"] = get_diff_patch(
                                            diff_base_ref,
                                            diff_compare_ref,
                                            git_file_path,
                                            timeout=10,
                                        )
                                    except subprocess.TimeoutExpired:
                                        print(
                                            f"Warning: fetch_pr_details: diff computation timed out for {file_path}",
                                            file=sys.stderr,
                                        )
                                    except Exception as diff_exc:
                                        print(
                                            "Warning: fetch_pr_details: "
                                            f"diff enrichment failed for {file_path}: {diff_exc}",
                                            file=sys.stderr,
                                        )
                        files.append(file_entry)
    except Exception as exc:
        print(f"Warning: fetch_pr_details: failed to fetch iteration changes: {exc}", file=sys.stderr)

    # Load repo config
    repo_config: dict[str, Any] = {}
    try:
        from agentic_devtools.cli.azure_devops.pr_review_manifest import resolve_repo_root

        repo_root = os.environ.get("AGDT_REPO_ROOT") or resolve_repo_root()
        repo_config = load_repo_config(repo_root)
    except Exception:
        pass

    # Resolve linked Jira issue key for downstream context.
    jira_issue_key: str | None = None
    raw_issue_key = state.get("jira_issue_key")
    if isinstance(raw_issue_key, str):
        raw_issue_key = raw_issue_key.strip()
        if raw_issue_key:
            jira_issue_key = raw_issue_key
    if jira_issue_key is None:
        try:
            from_state = get_value("jira.issue_key")
            if isinstance(from_state, str):
                from_state = from_state.strip()
                if from_state:
                    jira_issue_key = from_state
        except Exception:
            pass
    if jira_issue_key is None:
        try:
            jira_issue_key = find_jira_issue_from_pr(int(pr_id), config_for_urls, headers)
        except Exception as exc:
            print(
                f"Warning: fetch_pr_details: Jira key auto-detection failed: {exc}",
                file=sys.stderr,
            )

    # Fetch Jira issue details (FR-004)
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

    # Save PR details to temp file for other nodes (FR-006)
    try:
        from agentic_devtools.state import get_state_dir

        state_dir = get_state_dir()
        output_path = state_dir / f"temp-langchain-pr-details-{pr_id}.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        artifact = {
            "pr_data": pr_data,
            "files": files,
            "threads": threads,
            "iterations": iteration_metadata,
            "jira_issue_key": jira_issue_key or "",
            "jira_issue": jira_issue,
        }
        output_path.write_text(json.dumps(artifact, indent=2, default=str), encoding="utf-8")
    except Exception as exc:
        print(f"Warning: fetch_pr_details: failed to persist artifact: {exc}", file=sys.stderr)

    errors: list[str] = []
    if not repo_id:
        errors.append("fetch_pr_details: repository id is missing from PR payload")
    if not files:
        errors.append("fetch_pr_details: no changed files were retrieved from the iterations API")

    return {
        "files": files,
        "threads": threads,
        "commit_hash": commit_hash,
        "base_commit_hash": base_commit_hash,
        "latest_iteration_id": latest_iteration_id,
        "iterations": iteration_metadata,
        "jira_issue": jira_issue,
        "repo_id": repo_id,
        "project": project,
        "organization": organization,
        "jira_issue_key": jira_issue_key or "",
        "config": repo_config,
        "errors": errors,
    }
