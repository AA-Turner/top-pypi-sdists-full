from mistralai.workflows.core.task.create_task import task, task_from
from mistralai.workflows.core.task.protocol import StatefulTaskProtocol, StatelessTaskProtocol
from mistralai.workflows.core.task.task import Task

__all__ = [
    "StatefulTaskProtocol",
    "StatelessTaskProtocol",
    "Task",
    "task",
    "task_from",
]
