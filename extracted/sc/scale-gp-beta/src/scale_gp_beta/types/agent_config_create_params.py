# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, TypedDict

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
        ]
    ]
    """Tools enabled for this config. See AllowedTool enum for the catalogue."""

    description: str
