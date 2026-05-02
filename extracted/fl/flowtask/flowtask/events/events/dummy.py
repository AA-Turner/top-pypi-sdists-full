from ...utils import cPrint
from .abstract import AbstractEvent


class Dummy(AbstractEvent):
    async def __call__(self, *args, **kwargs):
        status = kwargs.pop("status", "event")
        task = kwargs.pop("task", None)
        cPrint(
            f" == TASK {task} EXECUTED {status} WITH: {self._kwargs}, {args}, {kwargs} === ",
            level="INFO",
        )
