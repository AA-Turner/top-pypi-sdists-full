import asyncio
from typing import Any, Coroutine as TypingCoroutine, TypeVar, Union
from orionis.services.asynchrony.contracts.coroutines import ICoroutine
from orionis.services.asynchrony.exceptions import OrionisCoroutineException
from orionis.services.introspection.objects.types import Type

T = TypeVar("T")

class Coroutine(ICoroutine):

    def __init__(self, func: TypingCoroutine[Any, Any, T]) -> None:
        """
        Initialize the Coroutine wrapper.

        Parameters
        ----------
        func : Coroutine
            The coroutine object to be wrapped. Must be an awaitable coroutine.

        Raises
        ------
        OrionisCoroutineException
            If the provided object is not a coroutine.

        Returns
        -------
        None
            This method does not return a value.

        Notes
        -----
        This constructor validates that the provided object is a coroutine using the framework's type introspection.
        If the validation fails, an exception is raised to prevent improper usage.
        """
        # Validate that the provided object is a coroutine
        if not Type(func).isCoroutine():
            raise OrionisCoroutineException(
                f"Expected a coroutine object, but got {type(func).__name__}."
            )

        # Store the coroutine object for later execution
        self.__func = func

    def run(self) -> Union[T, asyncio.Future]:
        """
        Executes the wrapped coroutine, either synchronously or asynchronously depending on the context.

        Parameters
        ----------
        None

        Returns
        -------
        T or asyncio.Future
            If called outside an event loop, returns the result of the coroutine after synchronous execution.
            If called within an event loop, returns an asyncio.Future representing the scheduled coroutine.

        Raises
        ------
        RuntimeError
            If the coroutine cannot be executed due to event loop issues.

        Notes
        -----
        - When invoked outside an active event loop, the coroutine is executed synchronously and its result is returned.
        - When invoked inside an active event loop, the coroutine is scheduled for asynchronous execution and a Future is returned.
        - This method automatically detects the execution context and chooses the appropriate execution strategy.
        """
        # Attempt to get the currently running event loop
        try:
            loop = asyncio.get_running_loop()

        # No running event loop; execute the coroutine synchronously and return its result
        except RuntimeError:
            return asyncio.run(self.__func)

        # If inside an active event loop, schedule the coroutine and return a Future
        if loop.is_running():
            return asyncio.ensure_future(self.__func)

        # If no event loop is running, execute the coroutine synchronously using the loop
        else:
            return loop.run_until_complete(self.__func)