from typing import Union
from flowtask.exceptions import TaskError
from .abstract import AbstractTaskStorage


class RowTaskStorage(AbstractTaskStorage):
    """Task is saved directly into Task Table (SQL)."""
    _name_: str = "Row"

    def __init__(self, column_name: str = "task_definition", *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._column = column_name

    def set_definition(self, obj) -> None:
        try:
            self._task = obj
        except (KeyError, AttributeError) as exc:
            raise TaskError(
                f"Unable to load Task definition from Table: {exc}"
            ) from exc

    async def open_task(
        self, task: str, program: str, **kwargs
    ) -> Union[dict, str]:
        return self._task.get(self._column, None)
