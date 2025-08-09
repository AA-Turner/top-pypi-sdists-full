import asyncio
from typing import Any, Coroutine as TypingCoroutine, TypeVar, Union
from orionis.services.asynchrony.contracts.coroutines import ICoroutine
from orionis.services.asynchrony.exceptions import OrionisCoroutineException
from orionis.services.introspection.objects.types import Type

T = TypeVar("T")

class Coroutine(ICoroutine):

    def __init__(self, func: TypingCoroutine[Any, Any, T]) -> None:
        """
        Wraps a coroutine object and validates its type.

        Parameters
        ----------
        func : Coroutine
            The coroutine object to be wrapped and managed.

        Raises
        ------
        OrionisCoroutineException
            If the provided object is not a coroutine.
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
        Executes the wrapped coroutine, adapting to the current event loop context.

        Returns
        -------
        T or asyncio.Future
            The result of the coroutine if executed synchronously, or an asyncio.Future if scheduled asynchronously.

        Raises
        ------
        RuntimeError
            If the coroutine cannot be executed due to event loop issues.

        Notes
        -----
        - If called outside an active event loop, the coroutine is executed synchronously and its result is returned.
        - If called within an active event loop, the coroutine is scheduled for asynchronous execution and a Future is returned.
        - The method automatically detects the execution context and chooses the appropriate execution strategy.
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
