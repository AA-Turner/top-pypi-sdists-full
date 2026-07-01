from __future__ import annotations

"""Per-step heal remap cache.

Identity-keyed via WeakKeyDictionary: the key is a Locator instance, not its
selector string. Two distinct Locator instances with the same selector heal
independently (correct: they may be in different scopes or frames).

Values:
- str  → the fresh selector to retry on (e.g. "#email_input" or "xpath=...").
- None → negative sentinel: heal already attempted and missed for this locator
         in this step; subsequent actions skip the API call and run the
         original (which surfaces Playwright's real diagnostics).

Lifecycle: set in `_Step.__aenter__` / `__enter__`, reset on `__aexit__` / `__exit__`.
Outside a step, get_cache() returns None and the wrapper takes the unwrapped path.
"""
import weakref
from contextvars import ContextVar

_heal_cache: ContextVar = ContextVar("testmu_heal_cache", default=None)


def get_cache():
    return _heal_cache.get()


def set_cache(cache):
    return _heal_cache.set(cache)


def reset_cache(token):
    _heal_cache.reset(token)


def new_cache():
    """Construct a fresh per-step cache. Centralised so the type can change later."""
    return weakref.WeakKeyDictionary()
