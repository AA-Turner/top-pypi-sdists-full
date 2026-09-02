"""Schema discovery helpers for the GitHub Issues adapter.

Provides constants and pure functions used by
:class:`~agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter` to
infer issue types from labels/issue-form templates and extract field schemas
from form YAML definitions.
"""

from __future__ import annotations

import re
from typing import Any

from agentic_devtools.adapters.types import PropertySchema

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Synonym map: maps slugified label/form names to their canonical type slug.
# Only well-established GitHub ecosystem conventions qualify.
SYNONYM_MAP: dict[str, str] = {
    "bug_report": "bug",
    "enhancement": "feature",
    "feature_request": "feature",
}

# Human-readable descriptions for well-known canonical type slugs.
DESCRIPTION_MAP: dict[str, str] = {
    "bug": "Bug report",
    "feature": "Feature request",
    "documentation": "Documentation improvement",
    "task": "Task or chore",
    "issue": "GitHub issue",
}

# Baseline properties returned for any issue type when no form template
# provides richer schema information.
DEFAULT_PROPERTIES: list[PropertySchema] = [
    PropertySchema(name="title", type="string", required=True, allowed_values=None),
    PropertySchema(name="body", type="string", required=False, allowed_values=None),
    PropertySchema(name="labels", type="array", required=False, allowed_values=None),
    PropertySchema(name="assignees", type="array", required=False, allowed_values=None),
]

# Labels recognized as type indicators (lowercase).
# Note: synonym labels (e.g. "enhancement") are intentionally excluded —
# they are always canonicalized before this check, so their canonical forms
# ("feature") are what get matched here.
WELL_KNOWN_LABELS: set[str] = {"bug", "feature", "documentation", "task"}

# Regex: non-alphanumeric except underscore
_NON_ALPHANUM_RE = re.compile(r"[^a-z0-9_]")
# Regex: whitespace or hyphens
_WS_HYPHEN_RE = re.compile(r"[\s\-]+")


# ---------------------------------------------------------------------------
# Pure functions
# ---------------------------------------------------------------------------


def slugify(text: str) -> str:
    """Convert *text* to a normalized slug.

    Lowercase, replace whitespace/hyphens with ``_``, strip non-alphanumeric
    characters except ``_``.
    """
    result = text.lower()
    result = _WS_HYPHEN_RE.sub("_", result)
    result = _NON_ALPHANUM_RE.sub("", result)
    return result


def canonicalize(slug: str) -> str:
    """Apply synonym map to *slug*, returning the canonical type slug."""
    return SYNONYM_MAP.get(slug, slug)


def copy_default_properties() -> list[PropertySchema]:
    """Return a fresh copy of DEFAULT_PROPERTIES with independent dict instances.

    Callers may freely mutate the returned list and its ``PropertySchema``
    entries without affecting the shared module-level constant.
    """
    return [
        PropertySchema(
            name=p["name"],
            type=p["type"],
            required=p["required"],
            allowed_values=list(p["allowed_values"]) if p["allowed_values"] is not None else None,
        )
        for p in DEFAULT_PROPERTIES
    ]


def parse_form_fields(body: list[dict[str, Any]]) -> list[PropertySchema]:
    """Parse GitHub issue form YAML body elements into property schemas.

    Skips ``markdown`` elements. Derives ``name`` from ``id`` attribute when
    present, otherwise slugifies the ``label``. Builds ``allowed_values`` from
    option labels for dropdown/checkboxes fields.

    Malformed elements (missing both ``id`` and ``label``, or missing ``type``)
    are silently skipped.
    """
    properties: list[PropertySchema] = []

    for element in body:
        if not isinstance(element, dict):
            continue

        field_type = element.get("type")
        if not isinstance(field_type, str):
            continue

        # Skip markdown/non-input elements
        if field_type == "markdown":
            continue

        attributes: dict[str, Any] = element.get("attributes") or {}
        if not isinstance(attributes, dict):
            attributes = {}

        # Derive field name from id or slugified label
        field_id = element.get("id")
        label = attributes.get("label")

        if isinstance(field_id, str) and field_id.strip():
            name = field_id.strip()
        elif isinstance(label, str) and label.strip():
            name = slugify(label.strip())
            if not name:
                continue  # Skip labels that slugify to an empty identifier
        else:
            continue  # Skip elements without identifiable name

        # Determine required flag
        validations: dict[str, Any] = attributes.get("validations") or {}
        if not isinstance(validations, dict):
            validations = {}
        required = bool(validations.get("required", False))

        # For checkboxes, also check option-level required
        allowed_values: list[str] | None = None

        if field_type == "checkboxes":
            options = attributes.get("options")
            if isinstance(options, list):
                raw_values: list[str] = []
                for opt in options:
                    if isinstance(opt, dict):
                        opt_label = opt.get("label")
                        if isinstance(opt_label, str):
                            raw_values.append(opt_label)
                        # Option-level required makes field required
                        if not required and opt.get("required") is True:
                            required = True
                # Return None rather than [] when no usable labels were found
                allowed_values = raw_values if raw_values else None

        elif field_type == "dropdown":
            options = attributes.get("options")
            if isinstance(options, list):
                raw_dropdown: list[str] = []
                for o in options:
                    if isinstance(o, str):
                        raw_dropdown.append(o)
                    elif isinstance(o, dict):
                        o_label = o.get("label")
                        if isinstance(o_label, str):
                            raw_dropdown.append(o_label)
                    # else: skip invalid entries (None, int, nested dicts, etc.)
                # Return None rather than [] when no usable values were found
                allowed_values = raw_dropdown if raw_dropdown else None

        properties.append(
            PropertySchema(
                name=name,
                type=field_type,
                required=required,
                allowed_values=allowed_values,
            )
        )

    return properties
