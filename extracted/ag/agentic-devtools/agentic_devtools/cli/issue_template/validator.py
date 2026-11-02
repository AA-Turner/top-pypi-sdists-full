"""Required property validation for issue templates.

Validates that required properties are present and non-empty on a
NormalizedIssue before rendering.
"""

from __future__ import annotations

from typing import Any

from agentic_devtools.adapters.types import NormalizedIssue, PropertySchema
from agentic_devtools.cli.issue_template.exceptions import TemplateValidationError


def _is_missing(value: Any) -> bool:
    """Check if a value counts as 'missing' for validation purposes.

    Missing rules (FR-005):
    - None -> missing
    - str empty/whitespace -> missing
    - list empty -> missing
    - bool False -> valid (not missing)
    - int 0 -> valid (not missing)
    """
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    if isinstance(value, list) and len(value) == 0:
        return True
    return False


def _get_property_value(issue: NormalizedIssue, name: str) -> Any:
    """Get a property value from canonical fields, raw dict, or raw["fields"] nested dict."""
    canonical_fields: dict[str, Any] = {
        "id": issue.issue_id,
        "issue_id": issue.issue_id,
        "title": issue.title,
        "description": issue.description,
        "status": issue.status,
        "url": issue.url,
        "provider": issue.provider,
        "labels": issue.labels,
        "created_at": issue.created_at,
        "updated_at": issue.updated_at,
    }

    if name in canonical_fields:
        return canonical_fields[name]
    if name in issue.raw:
        return issue.raw[name]
    # Fallback: raw["fields"] for Jira-style nested payloads
    fields = issue.raw.get("fields")
    if isinstance(fields, dict):
        return fields.get(name)
    return None


def validate_required_properties(
    issue: NormalizedIssue,
    properties: list[PropertySchema],
) -> None:
    """Validate that required properties are present on the issue.

    Checks each property with ``required=True`` against the issue's
    canonical fields, raw dict, and raw["fields"] nested dict (Jira pattern).
    Raises TemplateValidationError listing all missing property names.

    Args:
        issue: The normalized issue to validate.
        properties: List of property schemas to check.

    Raises:
        TemplateValidationError: When one or more required properties are missing.
    """
    missing: list[str] = []

    for prop in properties:
        if not prop.get("required", False):
            continue
        value = _get_property_value(issue, prop["name"])
        if _is_missing(value):
            missing.append(prop["name"])

    if missing:
        names = ", ".join(f"'{name}'" for name in missing)
        raise TemplateValidationError(
            f"Missing required properties: {names}. Provide them in the raw dict or ensure the adapter populates them."
        )
