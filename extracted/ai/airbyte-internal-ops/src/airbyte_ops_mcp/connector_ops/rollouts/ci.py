# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Helpers for linking rollout output to the current CI run."""

from __future__ import annotations

import os


def build_ci_run_url() -> str:
    """Build the GitHub Actions run URL from standard CI environment variables.

    Falls back to a generic repository URL if the run variables are missing.
    """
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    repo = os.environ.get("GITHUB_REPOSITORY", "airbytehq/airbyte-ops-mcp")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    if run_id:
        return f"{server}/{repo}/actions/runs/{run_id}"
    return f"{server}/{repo}"
