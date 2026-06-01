"""Stdlib ``logging.Filter`` that injects request context into log records.

Attach this filter to any handler (typically via ``logging.yml``) to make
context fields available to formatters::

    filters:
      context:
        "()": csrd.logging.RequestContextFilter

    formatters:
      structured:
        style: "{"
        format: "{asctime} hitId={hit_id} userId={user_id} level={levelname} {message}"

Fields added to each record:

* ``hit_id`` — request trace ID from ``csrd.context``
* ``user_id`` — authenticated user's ``sub`` claim
* ``app_id`` — application identifier header
* ``api_version`` — resolved API version for the request
"""

import logging

from csrd.context import get_api_version, get_app_id
from csrd.context.platform import hit_id_context, user_info_context


class RequestContextFilter(logging.Filter):
    """Injects request context fields into every log record.

    Unknown/unavailable fields default to ``"-"`` so formatters never
    raise ``KeyError``.
    """

    _FALLBACK = "-"

    def filter(self, record: logging.LogRecord) -> bool:
        record.hit_id = self._get_hit_id()  # type: ignore[attr-defined]
        record.user_id = self._get_user_id()  # type: ignore[attr-defined]
        record.app_id = get_app_id() or self._FALLBACK  # type: ignore[attr-defined]
        record.api_version = get_api_version() or self._FALLBACK  # type: ignore[attr-defined]
        return True

    @staticmethod
    def _get_hit_id() -> str:
        val = hit_id_context.get()
        return val if val and val != "unknown" else "-"

    @staticmethod
    def _get_user_id() -> str:
        user = user_info_context.get()
        if user is not None:
            sub = getattr(user, "sub", None)
            if sub:
                return str(sub)
        return "-"


__all__ = ("RequestContextFilter",)
