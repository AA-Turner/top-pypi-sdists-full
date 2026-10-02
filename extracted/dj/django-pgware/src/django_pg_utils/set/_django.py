"""Django-logger suppression for `hush`.

Raises the ``django.db.backends`` logger to CRITICAL so query logging cannot
leak sensitive parameters while a ``hush`` scope is active.

Unlike the PostgreSQL GUCs (which live on a thread-local Django connection and
are therefore naturally isolated per request), this logger is a single
process-global object shared by every thread. A naive save-the-level /
restore-the-level pair races: with two overlapping scopes, the second saves the
already-suppressed level, and whichever restores last wins — leaving the logger
either stuck at CRITICAL forever or, worse, restored to a verbose level while
another scope is still active and logging sensitive data (fail-open).

The fix is reference counting: the original level is captured only on the
0->1 transition and restored only on the 1->0 transition. While any scope is
active the logger stays at CRITICAL regardless of enter/exit ordering. The
counter and saved level are module-global and guarded by ``_logger_lock``.
"""

from __future__ import annotations

import logging
import threading

from django_pg_utils.set._result import SettingResult

_LOGGER_NAME = "django.db.backends"

# Guards the (count, saved-level) pair as a unit — not just the individual
# logger reads/writes, which is what made the old version racy.
_logger_lock = threading.Lock()
_suppress_count = 0
_saved_level: int | None = None


def suppress_django_logging() -> tuple[SettingResult, int]:
    """Raise the ``django.db.backends`` logger to CRITICAL (ref-counted).

    Returns ``(result, original_level)``. ``original_level`` is the true
    pre-suppression level (shared across overlapping scopes), suitable for the
    audit ``SettingResult`` — it is not needed by :func:`restore_django_logging`.
    """
    global _suppress_count, _saved_level
    logger = logging.getLogger(_LOGGER_NAME)
    with _logger_lock:
        if _suppress_count == 0:
            _saved_level = logger.level
            logger.setLevel(logging.CRITICAL)
        _suppress_count += 1
        original = _saved_level if _saved_level is not None else logger.level
    result = SettingResult(
        name=_LOGGER_NAME,
        connection="*",
        suppressed=True,
        original_value=str(original),
        error=None,
    )
    return result, original


def restore_django_logging() -> None:
    """Release one suppression; restore the logger when the last one exits.

    Idempotent below zero: a stray extra call (e.g. a double ``__exit__``) is a
    no-op rather than driving the counter negative.
    """
    global _suppress_count, _saved_level
    logger = logging.getLogger(_LOGGER_NAME)
    with _logger_lock:
        if _suppress_count == 0:
            return
        _suppress_count -= 1
        if _suppress_count == 0:
            if _saved_level is not None:
                logger.setLevel(_saved_level)
            _saved_level = None
