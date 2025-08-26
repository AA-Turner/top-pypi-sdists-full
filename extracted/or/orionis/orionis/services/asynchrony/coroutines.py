import asyncio
from typing import Any, Callable, Coroutine as TypingCoroutine, TypeVar, Union
from orionis.services.asynchrony.contracts.coroutines import ICoroutine
from orionis.services.asynchrony.exceptions import OrionisCoroutineException
from orionis.services.introspection.objects.types import Type

T = TypeVar("T")

class Coroutine(ICoroutine):

    def __init__(self, func: Union[TypingCoroutine[Any, Any, T], Callable[..., TypingCoroutine[Any, Any, T]]]) -> None:
        """
        Initialize a Coroutine wrapper for managing and executing coroutine objects.

        This constructor accepts either a coroutine object directly or a callable that
        returns a coroutine when invoked. The wrapped coroutine can later be executed
        using the run() method with automatic context detection.

        Parameters
        ----------
        func : Union[TypingCoroutine[Any, Any, T], Callable[..., TypingCoroutine[Any, Any, T]]]
            The coroutine object to be wrapped and managed, or a callable that returns
            a coroutine. This will be stored internally for later execution.

        Returns
        -------
        None
            This is a constructor method and does not return any value.

        Notes
        -----
        - The coroutine type validation is performed during execution in the run() method,
          not during initialization.
        - Both coroutine objects and coroutine functions are accepted as valid input.
        """

        # Store the coroutine object or callable for later execution
        self.__func = func

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
        if not callable(self.__func):
            raise OrionisCoroutineException(
                f"Cannot invoke non-callable object of type {type(self.__func).__name__}"
            )

        try:

            # Check if the callable is a coroutine function
            if asyncio.iscoroutinefunction(self.__func):

                # Create the coroutine object
                coroutine_obj = self.__func(*args, **kwargs)

                try:

                    # Check if we're inside a running event loop
                    loop = asyncio.get_running_loop()
                    return loop.create_task(coroutine_obj)

                except RuntimeError:

                    # No running event loop, execute synchronously
                    try:

                        # Use asyncio.run to execute the coroutine and return its result
                        return asyncio.run(coroutine_obj)

                    except Exception as e:

                        # Wrap and raise any exceptions that occur during execution
                        raise OrionisCoroutineException(
                            f"Failed to execute coroutine synchronously: {str(e)}"
                        ) from e

            else:

                # Execute regular callable directly
                return self.__func(*args, **kwargs)

        except OrionisCoroutineException:

            # Re-raise our custom exceptions as-is
            raise

        except Exception as e:

            # Wrap and raise any other exceptions that occur during invocation
            raise RuntimeError(
                f"Unexpected error during callable invocation: {str(e)}"
            ) from e

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

        # Validate that the provided object is a coroutine
        if not Type(self.__func).isCoroutine():
            raise OrionisCoroutineException(
                f"Expected a coroutine object, but got {type(self.__func).__name__}."
            )

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
