"""Utilities for caching objects and querysets."""

import functools
import hashlib
from typing import Any, Optional

from django.conf import settings
from django.core.cache import cache
from django.db import models


class ObjectCacheMixin:
    """A mixin which adds a simple object cache to a Django manager."""

    def get_cached(
        self,
        pk,
        timeout: Optional[int] = None,
        select_related: Optional[str] = None,
    ) -> Any:
        """Return the requested object either from DB or from cache.

        Can be disabled globally through the setting ``APP_UTILS_OBJECT_CACHE_DISABLED``.

        Args:
            pk: Primary key for object to fetch
            timeout: Timeout in seconds for cache
            select_related: select_related query to be applied (if any)

        Returns:
            model instance if found

        Exceptions:
            ``Model.DoesNotExist`` if object can not be found

        Example:

        .. code-block:: python

            # adding the Mixin to the model manager
            class MyModelManager(ObjectCacheMixin, models.Manager):
                pass

            # using the cache method
            obj = MyModel.objects.get_cached(pk=42, timeout=3600)

        """
        is_cache_disabled = bool(
            getattr(settings, "APP_UTILS_OBJECT_CACHE_DISABLED", False)
        )
        if is_cache_disabled:
            value = self._fetch_object_for_cache(pk=pk, select_related=select_related)
            return value

        func = functools.partial(
            self._fetch_object_for_cache, pk=pk, select_related=select_related
        )
        return cache.get_or_set(
            self._create_object_cache_key(pk, select_related), func, timeout
        )

    def clear_cache(self, pk: int):
        """Clear cache for a potentially cached object.

        This will also clear cached variants with select_related (if any).

        Args:
            pk: Primary key for object to fetch
        """
        key_base = self._create_object_base_cache_key(pk)
        cache.delete_pattern(f"{key_base}*")

    def _create_object_base_cache_key(self, pk: int) -> str:
        model_meta = self.model._meta
        return f"{model_meta.app_label}-{model_meta.model_name}-{pk}"

    def _create_object_cache_key(
        self, pk: int, select_related: Optional[str] = None
    ) -> str:
        key = self._create_object_base_cache_key(pk)
        suffix = (
            hashlib.md5(select_related.encode("utf-8")).hexdigest()
            if select_related
            else ""
        )
        return f"{key}-{suffix}" if suffix else key

    def _fetch_object_for_cache(self, pk, select_related: Optional[str] = None):
        qs = self.select_related(select_related) if select_related else self
        return qs.get(pk=pk)


def cached_queryset(queryset: models.QuerySet, key: str, timeout: int) -> Any:
    """caches the given queryset

    Args:
        queryset: the query set to cache
        key: key to be used to reference this cache
        timeout: Timeout in seconds for cache

    Returns:
        query set

    Example:

        .. code-block:: python

            queryset = cached_queryset(
                MyModel.objects.filter(name__contains="dummy"),
                key="my_cache_key",
                timeout=3600
            )

    """
    return cache.get_or_set(key, lambda: queryset, timeout)
