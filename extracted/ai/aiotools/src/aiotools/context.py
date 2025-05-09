"""
Provides an implementation of asynchronous context manager and its applications.

.. versionchanged::

   As aiotools 1.7+ drops support for Python 3.7 or earlier, most attributes
   are just aliases of the standard contextlib.
"""

import asyncio
import contextlib
from contextvars import ContextVar
from typing import (
    Generic,
    Iterable,
    List,
    Optional,
    TypeVar,
)

from .types import AClosable, AsyncClosable

__all__ = [
    "resetting",
    "AsyncContextManager",
    "async_ctx_manager",
    "actxmgr",
    "aclosing",
    "closing_async",
    "AsyncContextGroup",
    "actxgroup",
]

T = TypeVar("T")
T_AClosable = TypeVar("T_AClosable", bound=AClosable)
T_AsyncClosable = TypeVar("T_AsyncClosable", bound=AsyncClosable)


AbstractAsyncContextManager = contextlib.AbstractAsyncContextManager
AsyncContextManager = contextlib._AsyncGeneratorContextManager
AsyncExitStack = contextlib.AsyncExitStack
async_ctx_manager = contextlib.asynccontextmanager


class resetting(Generic[T]):
    """
    An extra context manager to auto-reset the given context variable.
    It supports both the standard contextmanager protocol and the
    async-contextmanager protocol.

    .. versionadded:: 1.8.0
    """

    def __init__(self, ctxvar: ContextVar[T], value: T) -> None:
        self._ctxvar = ctxvar
        self._value = value

    def __enter__(self) -> None:
        self._token = self._ctxvar.set(self._value)

    async def __aenter__(self) -> None:
        self._token = self._ctxvar.set(self._value)

    def __exit__(self, *exc_info) -> Optional[bool]:
        self._ctxvar.reset(self._token)
        return None

    async def __aexit__(self, *exc_info) -> Optional[bool]:
        self._ctxvar.reset(self._token)
        return None


class aclosing(Generic[T_AClosable]):
    """
    An analogy to :func:`contextlib.closing` for async generators.

    The motivation has been proposed by:

    * https://github.com/njsmith/async_generator
    * https://vorpus.org/blog/some-thoughts-on-asynchronous-api-design-\
in-a-post-asyncawait-world/#cleanup-in-generators-and-async-generators
    * https://www.python.org/dev/peps/pep-0533/
    """

    def __init__(self, thing: T_AClosable) -> None:
        self.thing = thing

    async def __aenter__(self) -> T_AClosable:
        return self.thing

    async def __aexit__(self, *exc_info) -> Optional[bool]:
        await self.thing.aclose()
        return None


class closing_async(Generic[T_AsyncClosable]):
    """
    An analogy to :func:`contextlib.closing` for objects defining the ``close()``
    method as an async function.

    .. versionadded:: 1.5.6
    """

    def __init__(self, thing: T_AsyncClosable) -> None:
        self.thing = thing

    async def __aenter__(self) -> T_AsyncClosable:
        return self.thing

    async def __aexit__(self, *exc_info) -> Optional[bool]:
        await self.thing.close()
        return None


class AsyncContextGroup:
    """
    Merges a group of context managers into a single context manager.
    Internally it uses :func:`asyncio.gather()` to execute them with overlapping,
    to reduce the execution time via asynchrony.

    Upon entering, you can get values produced by the entering steps from
    the passed context managers (those ``yield``-ed) using an ``as`` clause of
    the ``async with``
    statement.

    After exits, you can check if the context managers have finished
    successfully by ensuring that the return values of ``exit_states()`` method
    are ``None``.

    .. note::

       You cannot return values in context managers because they are
       generators.

    If an exception is raised before the ``yield`` statement of an async
    context manager, it is stored at the corresponding manager index in the
    as-clause variable.  Similarly, if an exception is raised after the
    ``yield`` statement of an async context manager, it is stored at the
    corresponding manager index in the ``exit_states()`` return value.

    Any exceptions in a specific context manager does not interrupt others;
    this semantic is same to ``asyncio.gather()``'s when
    ``return_exceptions=True``.  This means that, it is user's responsibility
    to check if the returned context values are exceptions or the intended ones
    inside the context body after entering.

    :param context_managers: An iterable of async context managers.
                             If this is ``None``, you may add async context
                             managers one by one using the :meth:`~.add`
                             method.

    """

    def __init__(
        self, context_managers: Optional[Iterable[AbstractAsyncContextManager]] = None
    ):  # noqa
        self._cm = list(context_managers) if context_managers else []
        self._cm_yields: List[asyncio.Task] = []
        self._cm_exits: List[asyncio.Task] = []

    def add(self, cm):
        """
        TODO: fill description
        """
        self._cm.append(cm)

    async def __aenter__(self):
        # Exceptions in context managers are stored into _cm_yields list.
        # NOTE: There is no way to "skip" the context body even if the entering
        #       process fails.
        self._cm_yields[:] = await asyncio.gather(
            *(e.__aenter__() for e in self._cm), return_exceptions=True
        )
        return self._cm_yields

    async def __aexit__(self, *exc_info):
        # Clear references to context variables.
        self._cm_yields.clear()
        # Exceptions are stored into _cm_exits list.
        self._cm_exits[:] = await asyncio.gather(
            *(e.__aexit__(*exc_info) for e in self._cm), return_exceptions=True
        )

    def exit_states(self):
        """
        TODO: fill description
        """
        return self._cm_exits


# Shorter aliases
actxmgr = async_ctx_manager
actxgroup = AsyncContextGroup
