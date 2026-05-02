import inspect
from typing import Any, Awaitable, Callable, Optional, TypeVar, Union, cast

from deprecation import deprecated

from jetpack import _utils
from jetpack.config import _symbols
from jetpack.core._errors import NotAsyncError
from jetpack.core._jetpack_client import default_jetpack_client
from jetpack.core._jetroutine import Jetroutine
from jetpack.core._jetroutine import schedule as schedule

T = TypeVar("T")
__pdoc__ = {}
__pdoc__["jet"] = "Alias for jetroutine"
__pdoc__["function"] = "Alias for jetroutine"
DecoratedFunction = Callable[..., Awaitable[T]]


# @jetroutine is our general remote work decorator. It does not specify how the
# work will be done (RPC, job, queue, etc) and instead leaves that as an
# implementation detail.
def jetroutine(
    fn: Optional[Callable[..., T]] = None,
    # The stararg forces the arguments after that to be specified with the keyword
    #
    # > Parameters after “*” [...] are keyword-only parameters and may only be passed by keyword arguments
    # https://docs.python.org/3/reference/compound_stmts.html#function-definitions
    *,
    with_checkpointing: bool = False,
    endpoint_path: Optional[str] = None,
) -> Union[Jetroutine[T], Callable[[Callable[..., T]], Jetroutine[T]]]:
    """
    Decorator that wraps any async Python function, and runs it as a distributed function.

    Async python functions decorated with @jetroutine will be registered with
    the runtime when not running locally.
    Calling these functions on Jetpack will run them as remote distributed functions.

    #### Arguments:
    * **fn ([Callable[..., T])**: The function being decorated.
    * **with_checkpointing (bool)**: Determines whether the jetroutine's execution will be re-tried upon failure until it succeeds or exceeds the max number of retries. Also see @workflow for the canonical way user programs should set this.

    #### Returns:
     * **Jetroutine[T]**: A Jetroutine that executes the wrapped function


    #### Raises:
    * **NotAsyncError (jetpack.errors.NotAsyncError)**: Raised if the function being decorated is not async.
    * **ApplicationError (jetpack.errors.ApplicationError)**: Raised if the jetroutine's business logic raises an error. This is usually caused by incorrect business logic. `ApplicationError` is a subtype of `JetpackError` (`jetpack.errors.JetpackError`)
    * **SystemError (jetpack.errors.SystemError)**: Raised if there was a jetpack-system or kubernetes error during execution of the jetroutine. This is usually not an error caused by incorrect business logic. `SystemError` is a subtype of `JetpackError` (`jetpack.errors.JetpackError`)"""

    def wrapper(fn: Callable[..., T]) -> Jetroutine[T]:
        # Use asyncio.iscoroutine() instead?
        if not inspect.iscoroutinefunction(fn):
            raise NotAsyncError(
                f"Jetpack functions must be async. {_utils.qualified_func_name(fn)} is not async."
            )
        _symbols.get_symbol_table().register(fn, endpoint_path)
        jetroutineFunction: Jetroutine[T] = default_jetpack_client.jetroutine(
            fn, with_checkpointing
        )
        return jetroutineFunction

    return wrapper(fn) if fn else wrapper


@deprecated(details="Use jetroutine instead.")
def function(
    fn: Optional[Callable[..., T]] = None, *, with_checkpointing: bool = False
) -> Union[Jetroutine[T], Callable[[Callable[..., T]], Jetroutine[T]]]:
    # can enable this print to be more aggressive, since smarthop and other
    # customers may not have python's dev-mode on to see the @deprecated decorator's
    # warning message:
    # print("WARNING: @function is deprecated. Use @jetroutine instead.")
    """
    .. deprecated:: 0.5.0
       Use @jetroutine instead
    """

    return jetroutine(fn, with_checkpointing=with_checkpointing)


@deprecated(details="Use jetroutine instead.")
def jet(
    fn: Optional[Callable[..., T]] = None, *, with_checkpointing: bool = False
) -> Union[Jetroutine[T], Callable[[Callable[..., T]], Jetroutine[T]]]:
    return jetroutine(fn, with_checkpointing=with_checkpointing)


def workflow(
    fn: Optional[Callable[..., T]] = None
) -> Union[Jetroutine[T], Callable[[Callable[..., T]], Jetroutine[T]]]:
    """
    Workflow is syntactical sugar for @jetroutine(with_checkpointing=true).

    It is introduced as its own decorator because `with_checkpointing=true` changes the runtime semantics of the jetroutine being invoked. This change also applies transitively to any child jetroutines that are invoked by the decorated function.
    #### Arguments:
      * **fn: Optional[Callable[..., T] = None**: The function being decorated. Must be an `async` function
      * **endpoint_path: Optional[str] = None**: Optional endpoint path to publicly expose the function. See `@endpoint` for the canonical way user programs should set this.

    #### Returns:
      * **Jetroutine[T]**: A Jetroutine that executes the wrapped function

    #### Raises:
      * NotAsyncError (jetpack.errors.NotAsyncError): Raised if the function being decorated is not async.
      * ApplicationError (jetpack.errors.ApplicationError): Raised if the jetroutine's business logic raises an error. This is usually caused by incorrect business logic. `ApplicationError` is a subtype of `JetpackError` (`jetpack.errors.JetpackError`)
      * SystemError (jetpack.errors.SystemError): Raised if there was a jetpack-system or kubernetes error during execution of the jetroutine. This is usually not an error caused by incorrect business logic. `SystemError` is a subtype of `JetpackError` (`jetpack.errors.JetpackError`)
    """
    return jetroutine(fn, with_checkpointing=True)


def endpoint(
    fn: Optional[Callable[..., T]] = None,
    path: str = "",
) -> Union[Jetroutine[T], Callable[[Callable[..., T]], Jetroutine[T]]]:
    """endpoint is syntactical sugar for @jetroutine(path="/some/path")."""
    return jetroutine(fn, endpoint_path=path)
