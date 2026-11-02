"""Project-level ``property_section_mapping`` resolution (wrapper layer).

Loads the mapping from ``.agdt/config/project.json`` through the existing
effective-project-config path (so ``config_mode: manual`` treats the project
layer as absent), applies ``issueTemplate`` (camelCase) → ``issue_template``
(snake_case alias) precedence, emits a :class:`DeprecationWarning` when the
alias is used, validates the mapping, and merges any explicitly supplied
``PropertyConfig`` mapping on top (explicit wins per key).

This layer is where all side effects (config discovery, deprecation warnings)
live; the pure ``render_issue`` core consumes the already-resolved mapping.
"""

from __future__ import annotations

import warnings
from collections.abc import Mapping
from pathlib import Path

from agentic_devtools.cli.issue_template.mapping_validation import (
    validate_issue_template_block,
    validate_property_section_mapping,
)

_DEPRECATION_MESSAGE = "'issue_template' is deprecated; use 'issueTemplate' in project.json"


def _resolve_project_block_mapping(*, git_root: Path | None = None) -> dict[str, str]:
    """Resolve and validate the project-config mapping layer.

    Applies canonical/alias precedence and emits a ``DeprecationWarning`` when
    the ``issue_template`` alias is present and non-null.
    """
    from agentic_devtools.cli.config.project_config import load_effective_project_config

    config = load_effective_project_config(git_root=git_root)

    alias_present = "issue_template" in config and config["issue_template"] is not None
    if alias_present:
        warnings.warn(_DEPRECATION_MESSAGE, DeprecationWarning, stacklevel=2)

    canonical = config.get("issueTemplate")
    if canonical is not None:
        return validate_issue_template_block(canonical, "issueTemplate")
    if alias_present:
        return validate_issue_template_block(config["issue_template"], "issue_template")
    return {}


def resolve_effective_mapping(
    explicit_mapping: Mapping[str, str] | None = None,
    *,
    git_root: Path | None = None,
) -> dict[str, str]:
    """Return the merged effective mapping (project layer + explicit override).

    ``explicit_mapping`` entries win per key over the project-config layer. An
    explicit mapping of ``None`` means "use the project config as-is".
    """
    project_mapping = _resolve_project_block_mapping(git_root=git_root)
    if explicit_mapping is None:
        return project_mapping
    explicit_canonical = validate_property_section_mapping(dict(explicit_mapping))
    merged = dict(project_mapping)
    merged.update(explicit_canonical)
    return merged
