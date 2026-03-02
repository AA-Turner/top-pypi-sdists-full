"""
Google Tasks MCP Tools

This module provides MCP tools for interacting with Google Tasks API.
"""

import asyncio
import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from googleapiclient.errors import HttpError  # type: ignore
from mcp import Resource

from auth.oauth_config import is_oauth21_enabled, is_external_oauth21_provider
from auth.service_decorator import require_google_service
from core.server import server
from core.utils import handle_http_errors

logger = logging.getLogger(__name__)

LIST_TASKS_MAX_RESULTS_DEFAULT = 20
LIST_TASKS_MAX_RESULTS_MAX = 10_000
LIST_TASKS_MAX_POSITION = "99999999999999999999"


def _format_reauth_message(error: Exception, user_google_email: str) -> str:
    base = f"API error: {error}. You might need to re-authenticate."
    if is_oauth21_enabled():
        if is_external_oauth21_provider():
            hint = (
                "LLM: Ask the user to provide a valid OAuth 2.1 bearer token in the "
                "Authorization header and retry."
            )
        else:
            hint = (
                "LLM: Ask the user to authenticate via their MCP client's OAuth 2.1 "
                "flow and retry."
            )
    else:
        hint = (
            "LLM: Try 'start_google_auth' with the user's email "
            f"({user_google_email}) and service_name='Google Tasks'."
        )
    return f"{base} {hint}"


class StructuredTask:
    def __init__(self, task: Dict[str, str], is_placeholder_parent: bool) -> None:
        self.id = task["id"]
        self.title = task.get("title", None)
        self.status = task.get("status", None)
        self.due = task.get("due", None)
        self.notes = task.get("notes", None)
        self.updated = task.get("updated", None)
        self.completed = task.get("completed", None)
        self.is_placeholder_parent = is_placeholder_parent
        self.subtasks: List["StructuredTask"] = []

    def add_subtask(self, subtask: "StructuredTask") -> None:
        self.subtasks.append(subtask)

    def __repr__(self) -> str:
        return f"StructuredTask(title={self.title}, {len(self.subtasks)} subtasks)"


def _adjust_due_max_for_tasks_api(due_max: str) -> str:
    """
    Compensate for the Google Tasks API treating dueMax as an exclusive bound.

    The API stores due dates at day resolution and compares using < dueMax, so to
    include tasks due on the requested date we bump the bound by one day.
    """
    try:
        parsed = datetime.fromisoformat(due_max.replace("Z", "+00:00"))
    except ValueError:
        logger.warning(
            "[list_tasks] Unable to parse due_max '%s'; sending unmodified value",
            due_max,
        )
        return due_max

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)

    adjusted = parsed + timedelta(days=1)
    if adjusted.tzinfo == timezone.utc:
        return adjusted.isoformat().replace("+00:00", "Z")
    return adjusted.isoformat()
