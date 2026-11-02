"""Tool binding adapters for PR review tools.

Provides binding functions that connect LangGraph nodes to existing
agdt Python functions for the PR review workflow.  Each binding is
a thin adapter that translates node-level tool invocations into
calls to the appropriate agdt implementation.

Tool IDs:
- ``azure_devops_approve_file`` — builds a ``submission_item`` for the approve
  outcome; must be submitted via the durable engine to persist to the v2 ledger
- ``azure_devops_request_changes`` — builds a ``submission_item`` for
  request-changes; must be submitted via the durable engine
- ``azure_devops_request_changes_with_suggestion`` — builds a ``submission_item``
  with inline suggestions; must be submitted via the durable engine
- ``azure_devops_post_suggestion`` — alias for
  ``azure_devops_request_changes_with_suggestion``
- ``add_pull_request_comment`` — immediately posts a general PR
  comment through the provider-neutral comment contract; does **not** write to
  global agent state
- ``submit_summary`` — posts a general PR summary comment
  (delegates to ``add_pull_request_comment``)
- ``azure_devops_add_pull_request_comment`` and ``azure_devops_submit_summary``
  remain compatibility aliases
- ``azure_devops_mark_file_reviewed`` — marks a file as reviewed in the ADO UI
"""

from __future__ import annotations

from typing import Any

from agentic_devtools.orchestration.tools.definition import ToolDefinition
from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry

# Tool ID constants
APPROVE_FILE = "azure_devops_approve_file"
REQUEST_CHANGES = "azure_devops_request_changes"
REQUEST_CHANGES_WITH_SUGGESTION = "azure_devops_request_changes_with_suggestion"
ADD_PR_COMMENT = "add_pull_request_comment"
ADD_PR_COMMENT_LEGACY = "azure_devops_add_pull_request_comment"
MARK_FILE_REVIEWED = "azure_devops_mark_file_reviewed"
POST_SUGGESTION = "azure_devops_post_suggestion"
SUBMIT_SUMMARY = "submit_summary"
SUBMIT_SUMMARY_LEGACY = "azure_devops_submit_summary"

ALL_REVIEW_TOOL_IDS = (
    APPROVE_FILE,
    REQUEST_CHANGES,
    REQUEST_CHANGES_WITH_SUGGESTION,
    ADD_PR_COMMENT,
    ADD_PR_COMMENT_LEGACY,
    MARK_FILE_REVIEWED,
    POST_SUGGESTION,
    SUBMIT_SUMMARY,
    SUBMIT_SUMMARY_LEGACY,
)


def _get_file_path(kwargs: dict[str, Any]) -> str:
    file_path = kwargs.get("file_path") or kwargs.get("filePath")
    if not file_path:
        # Accept file_key as fallback only when it is clearly path-like
        # (contains a path separator).  A bare slug+hash fileKey is not a
        # valid repo path and must not be forwarded to the submission mapper.
        file_key = kwargs.get("file_key", "")
        if isinstance(file_key, str) and ("/" in file_key or "\\" in file_key):
            file_path = file_key
    if not isinstance(file_path, str) or not file_path.strip():
        raise ValueError("file_path (or path-like file_key) is required")
    file_path = file_path.strip()
    # Security: reject path traversal segments (".." anywhere in the path).
    # LLM/tool inputs are untrusted; forwarding traversal paths to the ADO API
    # or mark-reviewed calls could target files outside the repo root.
    if ".." in file_path.replace("\\", "/").split("/"):
        raise ValueError("path traversal segments ('..') are not allowed in file_path")
    # Security: reject Windows drive-prefixed paths (e.g. C:\, C:/, C:tmp).
    # Such paths are never valid repo-relative references.
    if len(file_path) >= 2 and file_path[0].isalpha() and file_path[1] == ":":
        raise ValueError("drive-qualified paths are not allowed in file_path")
    # Security: reject UNC paths (e.g. \\server\share or //server/share).
    if file_path.startswith(("\\\\", "//")):
        raise ValueError("UNC paths are not allowed in file_path")
    # Security: reject Windows root-relative paths (e.g. \Windows\System32).
    # Note: leading "/" is allowed — the PR-review pipeline normalises repo paths
    # to the "/path/to/file" format via normalize_repo_path(), so a single leading
    # forward-slash is a valid normalised repo path, not a true absolute path.
    if file_path.startswith("\\"):
        raise ValueError("Windows root-relative paths are not allowed in file_path")
    return file_path


def _normalize_suggestions(raw_suggestions: Any) -> list[dict[str, Any]]:
    from pydantic import BaseModel as _BaseModel

    if raw_suggestions is None:
        return []
    if not isinstance(raw_suggestions, list):
        raise ValueError("suggestions must be a list")

    normalized: list[dict[str, Any]] = []
    for suggestion in raw_suggestions:
        if isinstance(suggestion, _BaseModel):
            # ReviewSuggestion (or any Pydantic model) — serialize to dict so
            # the mapper receives plain dicts regardless of the call path.
            normalized.append(suggestion.model_dump(exclude_none=True))
        elif not isinstance(suggestion, dict):
            raise ValueError("suggestions must contain only objects")
        else:
            normalized.append(suggestion)
    return normalized


def _build_submission_item(outcome: str, default_summary: str, **kwargs: Any) -> dict[str, Any]:
    from agentic_devtools.cli.azure_devops.pr_review_submit_mapper import map_answer_to_submission_item

    answer = {
        "outcome": outcome,
        "filePath": _get_file_path(kwargs),
        "summary": kwargs.get("summary", default_summary),
        "reviewMode": kwargs.get("review_mode", "diff"),
        "suggestions": [],
    }
    if outcome != "approve":
        answer["suggestions"] = _normalize_suggestions(kwargs.get("suggestions", []))

    return map_answer_to_submission_item(answer)


def _approve_file(**kwargs: Any) -> dict[str, Any]:
    """Build an approve ``submission_item`` for the v2 review pipeline.

    Returns a ``{"success": True, "submission_item": {...}}`` dict.  The
    caller is responsible for submitting the item via the durable engine so
    that the answer is persisted to the v2 ledger and posted to the PR.
    """
    try:
        submission_item = _build_submission_item("approve", "Approved", **kwargs)
        return {"success": True, "submission_item": submission_item}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


def _request_changes(**kwargs: Any) -> dict[str, Any]:
    """Build a request-changes ``submission_item`` for the v2 review pipeline.

    Returns a ``{"success": True, "submission_item": {...}}`` dict.  The
    caller is responsible for submitting the item via the durable engine so
    that the answer is persisted to the v2 ledger and posted to the PR.
    """
    try:
        submission_item = _build_submission_item("request-changes", "Changes requested", **kwargs)
        return {"success": True, "submission_item": submission_item}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


def _request_changes_with_suggestion(**kwargs: Any) -> dict[str, Any]:
    """Build a request-changes-with-suggestion ``submission_item`` for the v2 pipeline.

    Returns a ``{"success": True, "submission_item": {...}}`` dict.  The
    caller is responsible for submitting the item via the durable engine so
    that the answer (including inline suggestions) is persisted to the v2
    ledger and posted to the PR.
    """
    try:
        submission_item = _build_submission_item(
            "request-changes-with-suggestion",
            "Changes requested with suggestion",
            **kwargs,
        )
        return {"success": True, "submission_item": submission_item}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


def _post_suggestion(**kwargs: Any) -> dict[str, Any]:
    """Post an inline code suggestion for a file."""
    return _request_changes_with_suggestion(**kwargs)


def _add_pull_request_comment(**kwargs: Any) -> dict[str, Any]:
    """Add a general comment to a pull request.

    Uses the provider-neutral contract and resolves the provider from the
    explicit argument or configured platform state.
    """
    pull_request_id = kwargs.get("pull_request_id")
    content = kwargs.get("content", "")

    if pull_request_id is None or not isinstance(content, str) or not content.strip():
        return {"success": False, "error": "pull_request_id and content are required"}

    try:
        from agentic_devtools.cli.pull_request_comments import _build_request, dispatch_pull_request_comment

        request = _build_request(
            provider=kwargs.get("provider"),
            repository=kwargs.get("repository"),
            pull_request_id=pull_request_id,
            content=content,
            path=kwargs.get("path"),
            line=kwargs.get("line"),
            end_line=kwargs.get("end_line"),
            dry_run=kwargs.get("dry_run"),
            idempotency_marker=kwargs.get("idempotency_marker"),
            use_state_defaults=False,
        )
        result = dispatch_pull_request_comment(request)
        return result.as_dict()
    except Exception as exc:
        return {"success": False, "error": str(exc)}


def _mark_file_reviewed(**kwargs: Any) -> dict[str, Any]:
    """Mark a file as reviewed in the Azure DevOps UI."""
    from agentic_devtools.cli.azure_devops.mark_reviewed import mark_file_reviewed

    try:
        file_path = _get_file_path(kwargs)
    except ValueError as exc:
        return {"success": False, "error": str(exc)}
    pull_request_id = kwargs.get("pull_request_id")
    repo_id = kwargs.get("repo_id", "")

    if pull_request_id is None:
        return {"success": False, "error": "file_path and pull_request_id are required"}

    if not repo_id:
        return {"success": False, "error": "repo_id is required"}

    try:
        from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig

        config = AzureDevOpsConfig.from_state()
        mark_file_reviewed(
            file_path=file_path,
            pull_request_id=int(pull_request_id),
            config=config,
            repo_id=repo_id,
        )
        return {"success": True}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


def _submit_summary(**kwargs: Any) -> dict[str, Any]:
    """Submit a summary comment for the pull request."""
    payload = dict(kwargs)
    if "content" not in payload and "summary" in payload:
        payload["content"] = payload["summary"]
    return _add_pull_request_comment(**payload)


def _add_pull_request_comment_ado_legacy(**kwargs: Any) -> dict[str, Any]:
    """Legacy Azure DevOps alias — always routes to azure_devops provider."""
    return _add_pull_request_comment(**{**kwargs, "provider": "azure_devops"})


def _submit_summary_ado_legacy(**kwargs: Any) -> dict[str, Any]:
    """Legacy Azure DevOps summary alias — always routes to azure_devops provider."""
    return _submit_summary(**{**kwargs, "provider": "azure_devops"})


def _schema(*required: str, properties: dict[str, Any]) -> dict[str, Any]:
    schema: dict[str, Any] = {"type": "object", "properties": properties}

    required_list = list(required)
    if "file_path" in required_list:
        required_list = [r for r in required_list if r != "file_path"]
        # file_path or filePath must be provided; file_key is accepted only as
        # an optional runtime fallback (when it happens to be path-like), so it
        # is deliberately excluded from the schema-level anyOf requirement to
        # prevent callers from passing a bare slug+hash that will fail at runtime.
        schema["anyOf"] = [
            {"required": ["file_path"]},
            {"required": ["filePath"]},
        ]

    if required_list:
        schema["required"] = required_list
    return schema


def register_review_tools(registry: ConcreteToolRegistry) -> None:
    """Register all PR review tool bindings with a tool registry.

    Args:
        registry: The tool registry to register tools with.
    """
    tools = [
        (
            APPROVE_FILE,
            _approve_file,
            "Approve a file in the PR review",
            _schema(
                "file_path",
                properties={
                    "file_path": {"type": "string"},
                    "filePath": {"type": "string"},
                    "file_key": {"type": "string"},
                    "summary": {"type": "string"},
                },
            ),
            False,
        ),
        (
            REQUEST_CHANGES,
            _request_changes,
            "Request changes on a file",
            _schema(
                "file_path",
                properties={
                    "file_path": {"type": "string"},
                    "filePath": {"type": "string"},
                    "file_key": {"type": "string"},
                    "summary": {"type": "string"},
                    "review_mode": {"type": "string"},
                    "suggestions": {"type": "array", "items": {"type": "object"}},
                },
            ),
            False,
        ),
        (
            REQUEST_CHANGES_WITH_SUGGESTION,
            _request_changes_with_suggestion,
            "Request changes with code suggestion",
            _schema(
                "file_path",
                properties={
                    "file_path": {"type": "string"},
                    "filePath": {"type": "string"},
                    "file_key": {"type": "string"},
                    "summary": {"type": "string"},
                    "review_mode": {"type": "string"},
                    "suggestions": {"type": "array", "items": {"type": "object"}},
                },
            ),
            False,
        ),
        (
            POST_SUGGESTION,
            _post_suggestion,
            "Post a suggestion on a file",
            _schema(
                "file_path",
                "suggestions",
                properties={
                    "file_path": {"type": "string"},
                    "filePath": {"type": "string"},
                    "file_key": {"type": "string"},
                    "summary": {"type": "string"},
                    "review_mode": {"type": "string"},
                    "suggestions": {"type": "array", "items": {"type": "object"}},
                },
            ),
            False,
        ),
        (
            ADD_PR_COMMENT_LEGACY,
            _add_pull_request_comment_ado_legacy,
            "Add a general PR comment (legacy Azure DevOps alias)",
            _schema(
                "pull_request_id",
                "content",
                properties={
                    "pull_request_id": {"type": "integer"},
                    "content": {"type": "string"},
                    "repository": {"type": "string"},
                },
            ),
            True,
        ),
        (
            SUBMIT_SUMMARY_LEGACY,
            _submit_summary_ado_legacy,
            "Submit review summary comment (legacy Azure DevOps alias)",
            _schema(
                "pull_request_id",
                "summary",
                properties={
                    "pull_request_id": {"type": "integer"},
                    "summary": {"type": "string"},
                    "content": {"type": "string"},
                    "repository": {"type": "string"},
                },
            ),
            True,
        ),
        (
            MARK_FILE_REVIEWED,
            _mark_file_reviewed,
            "Mark a file as reviewed in ADO UI",
            _schema(
                "file_path",
                "pull_request_id",
                "repo_id",
                properties={
                    "file_path": {"type": "string"},
                    "filePath": {"type": "string"},
                    "file_key": {"type": "string"},
                    "pull_request_id": {"type": "integer"},
                    "repo_id": {"type": "string"},
                },
            ),
            True,
        ),
    ]

    for tool_id, fn, description, input_schema, mutating in tools:
        definition = ToolDefinition(
            name=tool_id,
            description=description,
            input_schema=input_schema,
            mutating=mutating,
            category="azure_devops",
        )
        registry.register(definition, fn=fn)

    provider_neutral_tools = [
        (
            ADD_PR_COMMENT,
            _add_pull_request_comment,
            "Add a general PR comment",
            _schema(
                "pull_request_id",
                "content",
                properties={
                    "pull_request_id": {"type": "integer"},
                    "content": {"type": "string"},
                    "provider": {"type": "string", "enum": ["azure_devops", "github"]},
                    "repository": {"type": "string"},
                },
            ),
            True,
        ),
        (
            SUBMIT_SUMMARY,
            _submit_summary,
            "Submit review summary comment",
            _schema(
                "pull_request_id",
                "summary",
                properties={
                    "pull_request_id": {"type": "integer"},
                    "summary": {"type": "string"},
                    "content": {"type": "string"},
                    "provider": {"type": "string", "enum": ["azure_devops", "github"]},
                    "repository": {"type": "string"},
                },
            ),
            True,
        ),
    ]

    for tool_id, fn, description, input_schema, mutating in provider_neutral_tools:
        definition = ToolDefinition(
            name=tool_id,
            description=description,
            input_schema=input_schema,
            mutating=mutating,
            category="pull_request",
        )
        registry.register(definition, fn=fn)
