"""Shared placeholder definitions for the issue-template subsystem.

Single source of truth for the ``{{placeholder}}`` syntax used by both the
renderer (:mod:`agentic_devtools.cli.issue_template.renderer`) and the template
validator (:mod:`agentic_devtools.cli.issue_template.validate_templates`).

Exports:
- ``PLACEHOLDER_RE``: compiled regex matching a valid ``{{name}}`` placeholder.
- ``PLACEHOLDER_ALIASES``: alias name -> canonical name mapping.
- ``CANONICAL_PLACEHOLDER_NAMES``: the full set of canonical placeholder names
  the renderer resolves against a ``NormalizedIssue``.
- ``BASE_REQUIRED_PROPERTIES``: the fallback required-property set used when no
  type-specific schema is available (``--file`` mode without ``--type``).
"""

from __future__ import annotations

import re

#: Compiled regex matching a valid ``{{name}}`` placeholder. The captured group
#: is the placeholder name (an identifier starting with a letter/underscore).
PLACEHOLDER_RE = re.compile(r"\{\{([a-zA-Z_][a-zA-Z0-9_]*)\}\}")

#: Alias mapping: alias name -> canonical name. Both the alias and the canonical
#: name resolve to the same value and are treated equivalently. The canonical
#: ``id`` maps to ``NormalizedIssue.issue_id``.
PLACEHOLDER_ALIASES: dict[str, str] = {"issue_id": "id"}

#: The full set of canonical placeholder names the renderer accepts. ``type`` is
#: resolved directly from the resolved ``type_slug`` at render time.
CANONICAL_PLACEHOLDER_NAMES: frozenset[str] = frozenset(
    {
        "id",
        "title",
        "description",
        "status",
        "type",
        "url",
        "provider",
        "labels",
        "created_at",
        "updated_at",
    }
)

#: Fallback required-property set used when no type-specific schema is available.
BASE_REQUIRED_PROPERTIES: frozenset[str] = frozenset({"title", "description"})
