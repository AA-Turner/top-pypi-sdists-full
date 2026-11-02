"""Model routing for per-file LLM model selection (FR-009).

Routes files to configured LLM models based on file-type patterns.
Falls back to the default model when no pattern matches.

Configuration is loaded from ``.github/agdt-config.json`` under
``review.model-routing``.
"""

from __future__ import annotations

import fnmatch
from typing import Any


def resolve_model_for_file(
    file_path: str,
    model_config: dict[str, Any] | None = None,
    *,
    default_model: str | None = None,
) -> str:
    """Resolve the LLM model to use for a given file.

    Checks file-pattern-based routing rules in order.  Returns the
    model for the first matching pattern, or the default model if no
    pattern matches.

    Args:
        file_path: Repository-relative path of the file.
        model_config: Parsed ``review.model-routing`` section from
            ``.github/agdt-config.json``.  Expected shape::

                {
                    "default-model": "gpt-4o",
                    "rules": [
                        {"pattern": "*.py", "model": "claude-opus-4"},
                        {"pattern": "*.ts", "model": "gpt-4o"}
                    ]
                }
        default_model: Optional caller-provided default model used before
            falling back to ``copilot.model_id``.

    Returns:
        Model identifier string.
    """
    if not model_config or not isinstance(model_config, dict):
        return _get_default_model(default_model)

    raw_default = model_config.get("default-model", "")
    configured_default_model = raw_default.strip() if isinstance(raw_default, str) else ""
    if not configured_default_model:
        configured_default_model = _get_default_model(default_model)

    rules = model_config.get("rules", [])
    if not isinstance(rules, list):
        return configured_default_model

    normalized_path = file_path.lstrip("/")

    for rule in rules:
        if not isinstance(rule, dict):
            continue
        pattern = rule.get("pattern", "")
        raw_model = rule.get("model", "")
        model = raw_model.strip() if isinstance(raw_model, str) else ""
        if not pattern or not model:
            continue
        if fnmatch.fnmatch(file_path, pattern) or fnmatch.fnmatch(normalized_path, pattern):
            return model
    return configured_default_model


def _get_default_model(configured_default_model: str | None = None) -> str:
    """Get the default model from state or config."""
    if isinstance(configured_default_model, str) and configured_default_model.strip():
        return configured_default_model.strip()

    try:
        from agentic_devtools.state import get_value

        model = get_value("copilot.model_id")
        if model:
            return model
    except Exception:
        pass

    return "gpt-4o"
