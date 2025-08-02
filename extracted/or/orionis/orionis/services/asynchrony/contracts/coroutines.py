from abc import ABC, abstractmethod
import asyncio
from typing import TypeVar, Union

T = TypeVar("T")

class ICoroutine(ABC):

    @abstractmethod
    def run(self) -> Union[T, asyncio.Future]:
        """
        Executes the wrapped coroutine, either synchronously or asynchronously depending on the context.

        Parameters
        ----------
        None

        Returns
        -------
        T or asyncio.Future
            If called outside an event loop, returns the result of the coroutine execution (type T).
            If called within an event loop, returns an asyncio.Future representing the scheduled coroutine.

        Notes
        -----
        - When invoked outside of an event loop, the coroutine is executed synchronously and its result is returned.
        - When invoked inside an event loop, the coroutine is scheduled for asynchronous execution and a Future is returned.
        - The caller is responsible for awaiting the Future if asynchronous execution is used.
        """

        # This method should be implemented by subclasses to handle coroutine execution.
        pass