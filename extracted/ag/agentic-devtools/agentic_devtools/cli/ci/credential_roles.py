"""Credential-role contract for AI PR loop GitHub operations."""

from __future__ import annotations

import os

DEFAULT_CLASSIC_REPO_WORKFLOW_PAT = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
REPO_VARIABLE_WRITER_PAT = "REPO_VARIABLE_WRITER_PAT"
AGDT_PR_APPROVER_PAT = "AGDT_PR_APPROVER_PAT"
COPILOT_GITHUB_TOKEN = "COPILOT_GITHUB_TOKEN"
LEGACY_SPECKIT_PR_TOKEN = "SPECKIT_PR_TOKEN"
GH_TOKEN = "GH_TOKEN"


def get_token(env_var: str) -> str:
    """Return a stripped token value from *env_var* or an empty string."""
    return os.environ.get(env_var, "").strip()


def require_default_repo_workflow_token(action: str) -> str:
    """Return the default workflow PAT for ordinary repository/API operations."""
    token = get_token(DEFAULT_CLASSIC_REPO_WORKFLOW_PAT)
    if token:
        return token
    gh_token = get_token(GH_TOKEN)
    if gh_token and os.environ.get("AI_PR_LOOP_CREDENTIAL_IDENTITY", "").strip() == DEFAULT_CLASSIC_REPO_WORKFLOW_PAT:
        return gh_token
    raise RuntimeError(f"{DEFAULT_CLASSIC_REPO_WORKFLOW_PAT} is required to {action}.")
