"""Tasks v2 module for cross-session task management with labels and dependencies."""

from .models import Task, TaskList, TaskStatus, TaskEvent
from .store import TaskStore, ConflictError
from .feature_flag import is_tasks_v2_enabled, get_current_task_list, get_session_id
from .waiter import TaskWaiter, register_with_broadcaster, unregister_from_broadcaster
from .broadcaster import TaskEventBroadcaster

# Auto-register TaskWaiter with the broadcaster so it receives completion events
register_with_broadcaster()

__all__ = [
    "Task",
    "TaskList",
    "TaskStatus",
    "TaskEvent",
    "TaskStore",
    "ConflictError",
    "TaskWaiter",
    "TaskEventBroadcaster",
    "is_tasks_v2_enabled",
    "get_current_task_list",
    "get_session_id",
    "register_with_broadcaster",
    "unregister_from_broadcaster",
]
