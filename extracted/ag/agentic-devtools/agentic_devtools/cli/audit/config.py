"""Audit configuration resolution.

Resolves batch size and other audit settings with the precedence:
CLI argument > ``.github/agdt-config.json`` > hardcoded default.
"""

from __future__ import annotations

from agentic_devtools.cli.ci.scheduler import SKIP_LABEL
from agentic_devtools.config import load_repo_config

DEFAULT_BATCH_SIZE = 10
DEFAULT_THRESHOLD = 10

# Label constants
LABEL_AUDITED = "review-feedback-audited"
LABEL_IN_PROGRESS = "review-feedback-audit-in-progress"
LABEL_AI_PR_LOOP_IGNORE = SKIP_LABEL


def batch_branch_name(batch_id: str) -> str:
    """Return the staging branch name for an audit batch.

    Both the dispatch phase (which pushes prepared batch files to the branch)
    and the apply phase (which deletes the branch on success) derive the name
    from the batch id, so they share this helper to avoid drift.

    Args:
        batch_id: Audit batch identifier.

    Returns:
        Branch name of the form ``audit/batch-<first 8 chars of batch_id>``.
    """
    return f"audit/batch-{batch_id[:8]}"


def resolve_batch_size(cli_arg: int | None, repo_path: str) -> int:
    """Resolve the audit batch size from available sources.

    Precedence (highest to lowest):
    1. Explicit CLI argument (``--batch-size``)
    2. ``audit.batch-size`` in ``.github/agdt-config.json``
    3. Hardcoded default (10)

    Args:
        cli_arg: Batch size from CLI argument (None if not provided).
        repo_path: Path to the repository root for config file lookup.

    Returns:
        Resolved batch size (always >= 1).
    """
    if cli_arg is not None and cli_arg >= 1:
        return cli_arg

    config = load_repo_config(repo_path)
    audit_config = config.get("audit", {})
    if isinstance(audit_config, dict):
        config_batch_size = audit_config.get("batch-size")
        if isinstance(config_batch_size, int) and config_batch_size >= 1:
            return config_batch_size

    return DEFAULT_BATCH_SIZE


def resolve_threshold(cli_arg: int | None, repo_path: str) -> int:
    """Resolve the PR count threshold before triggering an audit.

    Precedence (highest to lowest):
    1. Explicit CLI argument (``--threshold``)
    2. ``audit.threshold`` in ``.github/agdt-config.json``
    3. Hardcoded default (10)

    Args:
        cli_arg: Threshold from CLI argument (None if not provided).
        repo_path: Path to the repository root for config file lookup.

    Returns:
        Resolved threshold (always >= 1).
    """
    if cli_arg is not None and cli_arg >= 1:
        return cli_arg

    config = load_repo_config(repo_path)
    audit_config = config.get("audit", {})
    if isinstance(audit_config, dict):
        config_threshold = audit_config.get("threshold")
        if isinstance(config_threshold, int) and config_threshold >= 1:
            return config_threshold

    return DEFAULT_THRESHOLD
