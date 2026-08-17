r"""Provide a caching chat model wrapper."""

from __future__ import annotations

__all__ = ["CachingChatModel"]

import logging
from collections.abc import Callable  # noqa: TC003
from typing import TYPE_CHECKING, Any, ClassVar

from coola.hashing import hash_object
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage  # noqa: TC002
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.runnables import Runnable  # noqa: TC002
from langchain_core.tools import BaseTool  # noqa: TC002
from pydantic import ConfigDict

from zenpyre.runnables import hashing as _hashing  # noqa: F401
from zenpyre.utils.imports import is_persista_available

if TYPE_CHECKING:
    from collections.abc import Sequence

    from langchain_core.callbacks import (
        AsyncCallbackManagerForLLMRun,
        CallbackManagerForLLMRun,
    )

if is_persista_available():  # pragma: no cover
    from persista.cache import Cache  # noqa: TC002

logger: logging.Logger = logging.getLogger(__name__)


class CachingChatModel(BaseChatModel):
    r"""Wrap a chat model to cache its output, keyed by a hash of the
    messages, stop words, and call kwargs.

    Unlike :class:`~zenpyre.runnables.CachingRunnable`, this class is a
    genuine :class:`~langchain_core.language_models.BaseChatModel`
    subclass -- it can be used anywhere a chat model is expected, and
    ``bind_tools`` returns another ``CachingChatModel`` wrapping the
    bound inner model, so caching keeps working after tools are bound.

    On each call, a cache key is derived from ``(messages, stop,
    kwargs)`` and used to look up a previously cached ``ChatResult`` in
    ``response_cache``. On a cache hit, the cached result is returned
    without calling the wrapped chat model. On a cache miss, the
    wrapped chat model is invoked and its result is stored in
    ``response_cache`` before being returned. If ``response_cache`` is
    ``None``, caching is disabled entirely and every call goes straight
    to the wrapped chat model.

    The field is named ``response_cache`` rather than ``cache`` because
    :class:`~langchain_core.language_models.BaseChatModel` already
    declares a ``cache: BaseCache | bool | None`` field for its own,
    unrelated built-in caching (``langchain.cache``); reusing that name
    would silently collide with it and break LangChain's cache-lookup
    hooks (``_generate_with_cache`` / ``_agenerate_with_cache``), which
    read ``self.cache`` expecting that type.

    ``response_cache`` must already be open (via
    :meth:`~persista.cache.Cache.open` / :meth:`~persista.cache.Cache.aopen`,
    or used as a context manager) before it is passed in --
    ``CachingChatModel`` does not manage its lifecycle, since the same
    cache instance is typically shared across multiple wrappers or
    callers.

    Args:
        chat_model: The chat model whose output should be cached.
        response_cache: The :class:`~persista.cache.Cache` instance
            used to store cached results. If ``None``, caching is
            disabled. The caller configures the cache's backing store
            and TTL; ``CachingChatModel`` has no caching policy of its
            own beyond what ``response_cache`` provides.
        key_fn: A function that derives a cache key from a
            ``(messages, stop, kwargs)`` tuple. The returned string is
            used directly as the ``response_cache`` key. Defaults to
            ``hash_object``, which dispatches through ``coola``'s
            hasher registry (e.g. using ``SerializableHasher`` for
            LangChain messages).

    Example:
        ```pycon
        >>> from langchain_core.language_models import FakeListChatModel
        >>> from persista.cache import Cache
        >>> from zenpyre.chat_models import CachingChatModel
        >>> with Cache() as cache:
        ...     chat_model = CachingChatModel(
        ...         chat_model=FakeListChatModel(responses=["hello"]),
        ...         response_cache=cache,
        ...     )
        ...     chat_model.invoke("hi").content
        ...
        'hello'

        ```
    """

    model_config: ClassVar[ConfigDict] = ConfigDict(arbitrary_types_allowed=True)

    chat_model: Runnable[Any, BaseMessage]
    response_cache: Cache | None = None
    key_fn: Callable[[Any], str] | None = None

    @property
    def _llm_type(self) -> str:
        inner = getattr(self.chat_model, "_llm_type", self.chat_model.__class__.__qualname__)
        return f"caching-{inner}"

    @property
    def _identifying_params(self) -> dict[str, Any]:
        inner = getattr(self.chat_model, "_identifying_params", {})
        return {"chat_model": dict(inner), "response_cache": self.response_cache}

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        if self.response_cache is None:
            return self._call_chat_model(messages, stop=stop, run_manager=run_manager, **kwargs)

        key = self._make_key(messages, stop, kwargs)
        hit, result = self.response_cache.try_get(key)
        if hit:
            logger.debug("Cache hit: %s", key)
            return result

        logger.debug("Cache miss: %s", key)
        result = self._call_chat_model(messages, stop=stop, run_manager=run_manager, **kwargs)
        self.response_cache.set(key, result)
        return result

    async def _agenerate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: AsyncCallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        if self.response_cache is None:
            return await self._acall_chat_model(
                messages, stop=stop, run_manager=run_manager, **kwargs
            )

        key = self._make_key(messages, stop, kwargs)
        hit, result = await self.response_cache.atry_get(key)
        if hit:
            return result

        logger.debug("Cache miss: %s", key)
        result = await self._acall_chat_model(
            messages, stop=stop, run_manager=run_manager, **kwargs
        )
        await self.response_cache.aset(key, result)
        return result

    def bind_tools(
        self,
        tools: Sequence[dict[str, Any] | type | Callable[..., Any] | BaseTool],
        *,
        tool_choice: str | None = None,
        **kwargs: Any,
    ) -> Runnable[Any, BaseMessage]:
        bound = self.chat_model.bind_tools(tools, tool_choice=tool_choice, **kwargs)
        return self.model_copy(update={"chat_model": bound})

    def _call_chat_model(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None,
        run_manager: CallbackManagerForLLMRun | None,  # noqa: ARG002
        **kwargs: Any,
    ) -> ChatResult:
        message = self.chat_model.invoke(messages, stop=stop, **kwargs)
        return ChatResult(generations=[ChatGeneration(message=message)])

    async def _acall_chat_model(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None,
        run_manager: AsyncCallbackManagerForLLMRun | None,  # noqa: ARG002
        **kwargs: Any,
    ) -> ChatResult:
        message = await self.chat_model.ainvoke(messages, stop=stop, **kwargs)
        return ChatResult(generations=[ChatGeneration(message=message)])

    def _make_key(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None,
        kwargs: dict[str, Any],
    ) -> str:
        key_fn = self.key_fn if self.key_fn is not None else hash_object
        return key_fn((messages, stop, kwargs))
