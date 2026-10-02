r"""Contain a caching runnable wrapper."""

from __future__ import annotations

__all__ = ["CachingRunnable"]

import logging
from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin
from coola.hashing import hash_object
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.runnables.config import get_config_list
from langchain_core.runnables.utils import Input, Output

if TYPE_CHECKING:
    from collections.abc import Callable

    from persista.cache import Cache

logger: logging.Logger = logging.getLogger(__name__)


class CachingRunnable(Runnable[Input, Output], MultilineDisplayMixin):
    r"""Wrap a ``Runnable`` to cache its output, keyed by a hash of the
    input.

    On each call, ``key_fn(input)`` is used to look up a previously
    cached result in ``cache``. On a cache hit, the cached result is
    returned without calling the wrapped runnable. On a cache miss,
    the wrapped runnable is invoked and its result is stored in
    ``cache`` before being returned. If ``cache`` is ``None``, caching
    is disabled entirely and every call goes straight to the wrapped
    runnable.

    ``batch``/``abatch`` look up each input's cache entry individually,
    then call the wrapped runnable's own ``batch``/``abatch`` for only
    the inputs that missed -- so a partially-cached batch still benefits
    from the wrapped runnable's batching, rather than falling back to
    one call per miss.

    Unlike subclassing a caching base class, this wrapper works with any
    ``Runnable`` — including third-party ones you don't control — since
    caching is composed around the runnable rather than baked into its
    class hierarchy.

    Args:
        runnable: The runnable whose output should be cached.
        cache: The :class:`~persista.cache.Cache` instance used
            to store cached results. If ``None``, caching is disabled.
            The caller configures the cache's backing store and TTL;
            ``CachingRunnable`` has no caching policy of its own
            beyond what ``cache`` provides. ``cache`` must already be
            open (via :meth:`~persista.cache.Cache.open` /
            :meth:`~persista.cache.Cache.aopen`, or used as a context
            manager) before it is passed in -- ``CachingRunnable``
            does not manage its lifecycle.
        key_fn: A function that derives a cache key from an input. The
            returned string is used directly as the ``cache`` key.
            Defaults to ``hash_object``, which dispatches through
            ``coola``'s hasher registry (e.g. using ``DocumentHasher``
            for ``Document`` inputs). Override this if you need
            input-specific hashing behavior that differs from the
            registered default.

    Example:
        ```pycon
        >>> from langchain_core.runnables import RunnableLambda
        >>> from persista.cache import Cache
        >>> from zenpyre.runnables import CachingRunnable
        >>> runnable = RunnableLambda(lambda x: x.upper())
        >>> with Cache() as cache:
        ...     cached = CachingRunnable(runnable=runnable, cache=cache)
        ...     cached.invoke("hello")
        ...
        'HELLO'

        ```
    """

    def __init__(
        self,
        runnable: Runnable[Input, Output],
        cache: Cache | None = None,
        key_fn: Callable[[Input], str] | None = None,
    ) -> None:
        self._runnable = runnable
        self._cache = cache
        self._key_fn = key_fn if key_fn is not None else hash_object

    def invoke(
        self,
        input: Input,  # noqa: A002
        config: RunnableConfig | None = None,
        **kwargs: Any,
    ) -> Output:
        if self._cache is None:
            return self._runnable.invoke(input, config=config, **kwargs)

        key = self._key_fn(input)
        hit, result = self._cache.try_get(key)
        if hit:
            logger.debug("Cache hit: %s", key)
            return result

        logger.debug("Cache miss: %s", key)
        result = self._runnable.invoke(input, config=config, **kwargs)
        self._cache.set(key, result)
        return result

    async def ainvoke(
        self,
        input: Input,  # noqa: A002
        config: RunnableConfig | None = None,
        **kwargs: Any,
    ) -> Output:
        if self._cache is None:
            return await self._runnable.ainvoke(input, config=config, **kwargs)

        key = self._key_fn(input)
        hit, result = await self._cache.atry_get(key)
        if hit:
            logger.debug("Cache hit: %s", key)
            return result

        logger.debug("Cache miss: %s", key)
        result = await self._runnable.ainvoke(input, config=config, **kwargs)
        await self._cache.aset(key, result)
        return result

    def batch(
        self,
        inputs: list[Input],
        config: RunnableConfig | list[RunnableConfig] | None = None,
        *,
        return_exceptions: bool = False,
        **kwargs: Any,
    ) -> list[Output]:
        if not inputs:
            return []
        if self._cache is None:
            return self._runnable.batch(
                inputs, config=config, return_exceptions=return_exceptions, **kwargs
            )

        configs = get_config_list(config, len(inputs))
        keys = [self._key_fn(inp) for inp in inputs]

        hits = self._cache.try_get_many(keys)
        results: list[Any] = [None] * len(inputs)
        miss_indices: list[int] = []
        for i, key in enumerate(keys):
            if key in hits:
                results[i] = hits[key]
            else:
                miss_indices.append(i)

        if miss_indices:
            logger.debug("Cache miss: %d/%d input(s)", len(miss_indices), len(inputs))
            miss_outputs = self._runnable.batch(
                [inputs[i] for i in miss_indices],
                config=[configs[i] for i in miss_indices],
                return_exceptions=return_exceptions,
                **kwargs,
            )
            new_items: dict[str, Any] = {}
            for idx, output in zip(miss_indices, miss_outputs, strict=True):
                results[idx] = output
                if return_exceptions and isinstance(output, BaseException):
                    continue
                new_items[keys[idx]] = output
            self._cache.set_many(new_items)

        return results

    async def abatch(
        self,
        inputs: list[Input],
        config: RunnableConfig | list[RunnableConfig] | None = None,
        *,
        return_exceptions: bool = False,
        **kwargs: Any,
    ) -> list[Output]:
        if not inputs:
            return []
        if self._cache is None:
            return await self._runnable.abatch(
                inputs, config=config, return_exceptions=return_exceptions, **kwargs
            )

        configs = get_config_list(config, len(inputs))
        keys = [self._key_fn(inp) for inp in inputs]

        hits = await self._cache.atry_get_many(keys)
        results: list[Any] = [None] * len(inputs)
        miss_indices: list[int] = []
        for i, key in enumerate(keys):
            if key in hits:
                results[i] = hits[key]
            else:
                miss_indices.append(i)

        if miss_indices:
            logger.debug("Cache miss: %d/%d input(s)", len(miss_indices), len(inputs))
            miss_outputs = await self._runnable.abatch(
                [inputs[i] for i in miss_indices],
                config=[configs[i] for i in miss_indices],
                return_exceptions=return_exceptions,
                **kwargs,
            )
            new_items: dict[str, Any] = {}
            for idx, output in zip(miss_indices, miss_outputs, strict=True):
                results[idx] = output
                if return_exceptions and isinstance(output, BaseException):
                    continue
                new_items[keys[idx]] = output
            await self._cache.aset_many(new_items)

        return results

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {
            "runnable": self._runnable,
            "cache": self._cache,
            "key_fn": self._key_fn,
        }
