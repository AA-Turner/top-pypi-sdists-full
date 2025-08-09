from abc import ABC, abstractmethod
import asyncio
from typing import TypeVar, Union

T = TypeVar("T")

class ICoroutine(ABC):

    @abstractmethod
    def run(self) -> Union[T, asyncio.Future]:
        """
        Execute the wrapped coroutine either synchronously or asynchronously, depending on the execution context.

        Returns
        -------
        T or asyncio.Future
            If called outside of an event loop, returns the result of the coroutine execution (type T).
            If called within an event loop, returns an asyncio.Future representing the scheduled coroutine.

        Notes
        -----
        - Executes the coroutine synchronously and returns its result when called outside an event loop.
        - Schedules the coroutine for asynchronous execution and returns a Future when called inside an event loop.
        - The caller is responsible for awaiting the Future if asynchronous execution is used.
        """

        # This method should be implemented by subclasses to handle coroutine execution.
        pass
