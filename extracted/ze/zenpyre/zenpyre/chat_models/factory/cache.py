r"""Provide a concrete chat model factory that wraps another chat model
factory with caching."""

from __future__ import annotations

__all__ = ["CachingChatModelFactory"]

from typing import TYPE_CHECKING, Any

from coola.display import MultilineDisplayMixin

from zenpyre.chat_models.cache import CachingChatModel
from zenpyre.chat_models.factory.base import BaseChatModelFactory
from zenpyre.utils.resolve import resolve_object

if TYPE_CHECKING:
    from collections.abc import Callable

    from langchain_core.language_models import BaseChatModel
    from persista.cache import Cache

    from zenpyre.utils.config import BaseConfig


class CachingChatModelFactory(BaseChatModelFactory, MultilineDisplayMixin):
    """A concrete chat model factory that wraps another chat model
    factory and caches the resulting model's outputs via
    :class:`~zenpyre.chat_models.CachingChatModel`.

    The wrapped chat model is built by delegating to the inner
    factory, then wrapped in a
    :class:`~zenpyre.chat_models.CachingChatModel` so every call to the
    model transparently reads from and writes to ``cache``. Unlike
    :class:`~zenpyre.runnables.CachingRunnable`, the returned object is
    a genuine :class:`~langchain_core.language_models.BaseChatModel`
    instance, so ``bind_tools`` and other ``BaseChatModel``-specific
    methods keep working after wrapping.

    Args:
        chat_model_factory: The wrapped chat model factory, an
            objectory configuration, or a :class:`~BaseConfig` that
            resolves to a :class:`~BaseChatModelFactory`.
        cache: The :class:`~persista.cache.Cache` instance used
            to store cached results. If ``None``, caching is disabled.
        key_fn: A function that derives a cache key from an input. See
            :class:`~zenpyre.chat_models.CachingChatModel` for details.

    Example:
        ```pycon
        >>> from langchain_core.language_models import FakeListChatModel
        >>> from persista.cache import Cache
        >>> from zenpyre.chat_models.factory import CachingChatModelFactory, ChatModelFactory
        >>> factory = CachingChatModelFactory(
        ...     chat_model_factory=ChatModelFactory(FakeListChatModel(responses=["hello"])),
        ...     cache=Cache(),
        ... )
        >>> chat_model = factory.make_chat_model()

        ```
    """

    def __init__(
        self,
        chat_model_factory: BaseChatModelFactory | dict[str, Any] | BaseConfig,
        cache: Cache | None = None,
        key_fn: Callable[[Any], str] | None = None,
    ) -> None:
        self._chat_model_factory = resolve_object(chat_model_factory, cls=BaseChatModelFactory)
        self._cache = cache
        self._key_fn = key_fn

    def make_chat_model(self) -> BaseChatModel:
        chat_model = self._chat_model_factory.make_chat_model()
        return CachingChatModel(
            chat_model=chat_model,
            response_cache=self._cache,
            key_fn=self._key_fn,
        )

    def _get_repr_kwargs(self) -> dict[str, Any]:
        return {
            "chat_model_factory": self._chat_model_factory,
            "cache": self._cache,
            "key_fn": self._key_fn,
        }
