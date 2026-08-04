# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal, Required, TypedDict

from .repo_spec_param import RepoSpecParam

__all__ = ["AgentConfigCreateParams"]


class AgentConfigCreateParams(TypedDict, total=False):
    harness: Required[Literal["claude-code", "codex", "litellm"]]
    """Harness strategy. See Harness enum for supported values."""

    model: Required[str]

    name: Required[str]

    system_prompt: Required[str]

    allowed_tools: List[
        Literal[
            "Read",
            "Write",
            "Edit",
            "Bash",
            "Glob",
            "Grep",
            "List",
            "WebFetch",
            "WebSearch",
            "Task",
            "TodoWrite",
            "NotebookEdit",
            "ExitPlanMode",
            "Slack",
            "Linear",
            "GitHub",
            "Confluence",
            "Notion",
            "Datadog",
            "PagerDuty",
            "Salesforce",
            "Figma",
            "Granola",
            "Jira",
            "Gmail",
            "GoogleCalendar",
            "GoogleDrive",
            "GoogleDocs",
            "GoogleSheets",
            "GoogleSlides",
            "Snowflake",
            "Redash",
            "Tableau",
            "Metabase",
            "Gong",
            "ZoomInfo",
            "Clay",
        ]
    ]
    """Tools enabled for this config. See AllowedTool enum for the catalogue."""

    description: str

    persistent_workspace: bool
    """Give tasks a persistent /workspace that survives sandbox death.

    Fixed for a task's life; defaults off.
    """

    repos: Iterable[RepoSpecParam]
    """Per-config repo override.

    None uses the deployment default; an empty list clones nothing.
    """
