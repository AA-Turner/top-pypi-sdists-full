"""
Tool-level tests for action restrictions in consolidated Google Tasks tools.
"""

import os
import sys
from unittest.mock import AsyncMock, Mock

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from auth.permissions import set_permissions
from core.utils import UserInputError
import gtasks.tasks_tools as tasks_tools


def _unwrap(tool):
    """Unwrap a FunctionTool + decorator chain to the original async function."""
    fn = tool.fn if hasattr(tool, "fn") else tool
    while hasattr(fn, "__wrapped__"):
        fn = fn.__wrapped__
    return fn


@pytest.fixture(autouse=True)
def _reset_permissions_state():
    """Ensure each test starts and ends with no active permissions."""
    set_permissions(None)
    yield
    set_permissions(None)


@pytest.mark.asyncio
async def test_manage_task_denies_delete_under_manage():
    """tasks:manage should deny destructive delete action in manage_task."""
    set_permissions({"tasks": "manage"})

    with pytest.raises(UserInputError, match="delete"):
        await _unwrap(tasks_tools.manage_task)(
            service=Mock(),
            user_google_email="user@example.com",
            action="delete",
            task_list_id="list-1",
            task_id="task-1",
        )


@pytest.mark.asyncio
async def test_manage_task_list_denies_clear_completed_under_manage():
    """tasks:manage should deny clear_completed in manage_task_list."""
    set_permissions({"tasks": "manage"})

    with pytest.raises(UserInputError, match="clear_completed"):
        await _unwrap(tasks_tools.manage_task_list)(
            service=Mock(),
            user_google_email="user@example.com",
            action="clear_completed",
            task_list_id="list-1",
        )


@pytest.mark.asyncio
async def test_manage_task_allows_delete_under_full(monkeypatch):
    """tasks:full should allow delete path in manage_task."""
    set_permissions({"tasks": "full"})
    service = Mock()
    delete_impl = AsyncMock(return_value="deleted")
    monkeypatch.setattr(tasks_tools, "_delete_task_impl", delete_impl)

    result = await _unwrap(tasks_tools.manage_task)(
        service=service,
        user_google_email="user@example.com",
        action="delete",
        task_list_id="list-1",
        task_id="task-1",
    )

    assert result == "deleted"
    delete_impl.assert_awaited_once_with(
        service, "user@example.com", "list-1", "task-1"
    )


@pytest.mark.asyncio
async def test_manage_task_list_allows_clear_completed_under_full(monkeypatch):
    """tasks:full should allow clear_completed path in manage_task_list."""
    set_permissions({"tasks": "full"})
    service = Mock()
    clear_impl = AsyncMock(return_value="cleared")
    monkeypatch.setattr(tasks_tools, "_clear_completed_tasks_impl", clear_impl)

    result = await _unwrap(tasks_tools.manage_task_list)(
        service=service,
        user_google_email="user@example.com",
        action="clear_completed",
        task_list_id="list-1",
    )

    assert result == "cleared"
    clear_impl.assert_awaited_once_with(service, "user@example.com", "list-1")
