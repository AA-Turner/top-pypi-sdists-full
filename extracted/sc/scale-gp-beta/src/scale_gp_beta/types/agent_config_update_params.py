# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal, TypedDict

from .repo_spec_param import RepoSpecParam

__all__ = ["AgentConfigUpdateParams"]


class AgentConfigUpdateParams(TypedDict, total=False):
    task_id: str
    """
    If set, after persisting the patch we shallow-merge the changed fields into this
    task's params column on Agentex so the worker picks up the new values on its
    next turn. Caller-provided context — Agentex enforces task ownership via its own
    auth, so the side-effect no-ops if the caller doesn't own the task.
    """

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

    description: str

    harness: Literal["claude-code", "codex", "litellm"]
    """Supported agent harness strategies.

    Mirrors `PROVIDERS` in golden-agent's `project/harness/activity.py`.
    """

    model: str

    name: str

    persistent_workspace: bool

    repos: Iterable[RepoSpecParam]

    system_prompt: str
