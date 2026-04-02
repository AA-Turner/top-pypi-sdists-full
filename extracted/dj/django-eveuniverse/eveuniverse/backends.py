"""Backend for Celery Once."""

from celery_once import AlreadyQueued
from django.core.cache import cache


class DjangoBackend:
    """A celery once backend.

    This is a general purpose backend, which should work with many different
    Django installations.

    However, it uses Django's cache for locking and is therefore not guaranteed to be
    thread safe. This depends on which cache backend is used and how it is implemented.

    If in doubt and when possible we recommend using celery once's redis backend.
    """

    def __init__(self, settings):
        pass

    @staticmethod
    def raise_or_lock(key, timeout):
        """Set a global lock or raise AlreadyQueued if the lock could not be acquired."""
        acquired = cache.add(key=key, value="lock", timeout=timeout)
        if not acquired:
            raise AlreadyQueued(int(cache.ttl(key)))  # type: ignore

    @staticmethod
    def clear_lock(key):
        """Remove a global lock."""
        return cache.delete(key)
