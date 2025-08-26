from abc import ABC, abstractmethod
import asyncio
from typing import TypeVar, Union

T = TypeVar("T")

class ICoroutine(ABC):

    @abstractmethod
    def invoke(self, *args, **kwargs) -> Union[T, asyncio.Task, None]:
        """
        Invoke the callable coroutine function with the provided arguments.

        This method executes a callable coroutine function or regular function with the given
        arguments and keyword arguments. It automatically detects the execution context and
        handles both synchronous and asynchronous execution appropriately.

        Parameters
        ----------
        *args : tuple
            Positional arguments to pass to the callable function.
        **kwargs : dict
            Keyword arguments to pass to the callable function.

        Returns
        -------
        Union[T, asyncio.Task, None]
            - T: The result of the coroutine if executed synchronously
            - asyncio.Task: A task object if scheduled for asynchronous execution
            - None: If the callable is not a coroutine function

        Raises
        ------
        OrionisCoroutineException
            If an error occurs during coroutine execution.
        RuntimeError
            If an error occurs during callable execution that is not coroutine-related.

        Notes
        -----
        - Only callable objects can be invoked with this method
        - For coroutine functions, execution context is automatically detected
        - Non-coroutine callables are executed directly and return None
        - Exceptions are wrapped with appropriate context information

        Examples
        --------
        >>> async def my_coro(x, y):
        ...     return x + y
        >>> coro = Coroutine(my_coro)
        >>> result = coro.invoke(1, 2)  # Returns Task or result depending on context
        """
        pass

    @abstractmethod
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
        pass