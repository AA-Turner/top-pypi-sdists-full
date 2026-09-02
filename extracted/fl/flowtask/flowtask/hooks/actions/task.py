from .abstract import AbstractAction
from ...interfaces.task import TaskSupport


class Task(TaskSupport, AbstractAction):
    """Task.

    Calling an FlowTask Task.
    """
