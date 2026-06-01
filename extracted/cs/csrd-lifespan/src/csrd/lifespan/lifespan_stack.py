import warnings
from collections.abc import AsyncIterator, Callable, Mapping
from contextlib import AbstractAsyncContextManager, AsyncExitStack, asynccontextmanager
from typing import Any

from fastapi import FastAPI

LifespanFunction = Callable[[FastAPI], AbstractAsyncContextManager[Mapping[str, Any] | None]]


def _callable_name(callable_: Callable[..., Any]) -> str:
    try:
        return callable_.__name__
    except AttributeError:
        return getattr(type(callable_), "__name__", repr(callable_))


def _normalize(
    functions: tuple[LifespanFunction | list[LifespanFunction], ...],
) -> list[LifespanFunction]:
    collector: list[LifespanFunction] = []
    for function in functions:
        if isinstance(function, list):
            collector.extend(function)
        else:
            collector.append(function)

    return collector


class lifespan_stack:
    def __init__(self, *lifespan_functions: LifespanFunction | list[LifespanFunction]) -> None:
        self._lifespan_functions = _normalize(lifespan_functions)

    @asynccontextmanager
    async def __call__(self, app: FastAPI) -> AsyncIterator[dict[str, Any]]:
        state: dict[str, Any] = {}
        async with AsyncExitStack() as exit_stack:
            for lifespan_function in self._lifespan_functions:
                result = await exit_stack.enter_async_context(lifespan_function(app))

                # If the lifespan function yielded None then it doesnt need to store anything in state
                if result is None:
                    continue

                if isinstance(result, Mapping):
                    state |= result
                else:
                    warnings.warn(
                        f"Unexpected value from lifespan {_callable_name(lifespan_function)!r}: {result!r}",
                        stacklevel=2,
                    )

            # Mirror state onto app.state so code that inspects app.state
            # (e.g. actuator auto-discovery) can find lifespan-provided
            # objects.  Starlette >=1.0 stores lifespan state in the ASGI
            # scope (request.state) rather than app.state, so without this
            # mirror, hasattr(app.state, "db_adapter") would be False.
            for key, value in state.items():
                setattr(app.state, key, value)

            yield state


__all__ = ("lifespan_stack",)
