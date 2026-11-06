"""Values added after your SDK version to a closed set, such as a new turn status."""

from __future__ import annotations

from dataclasses import dataclass

import structlog
from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

from mistralai.vibe.harness.app_server import session as harness_session

__all__ = ["UnknownValue", "read_value"]

logger = structlog.get_logger(__name__)


@dataclass(frozen=True, slots=True)
class UnknownValue:
    """A value added after your SDK version, such as a turn status ``"paused"``.

    A field that can get new values, such as ``TurnUpdated.status``, is typed as its known values
    or ``UnknownValue``. ``text`` is the value as Mistral sent it, and ``str(value)`` gives it too.
    It is not a ``str``, so a type checker still flags a typo in a known value.

    Use it to log or to fall back, never to match on its text: once a later SDK knows the value,
    it reads as the plain string, and ``case agents.UnknownValue(text="paused")`` stops matching
    with no error. ``str(status) == "paused"`` matches before and after.
    """

    text: str
    """The value as Mistral sent it, such as ``"paused"``."""

    def __str__(self) -> str:
        return self.text

    @classmethod
    def __get_pydantic_core_schema__(cls, source: object, handler: GetCoreSchemaHandler) -> CoreSchema:
        # In a pydantic record, such as ApprovalTool, it dumps as its text.
        return core_schema.is_instance_schema(
            cls, serialization=core_schema.plain_serializer_function_ser_schema(cls._write)
        )

    @staticmethod
    def _write(value: UnknownValue) -> str:
        return value.text


# The (field, value) pairs already logged: one debug line each, not one per read.
_logged: set[tuple[str, str]] = set()


def read_value[T: str](value: T | harness_session.UnknownValue, field: str) -> T | UnknownValue:
    """``value`` as the host's model read it: a known value as it is, an unknown one as an
    ``UnknownValue``, with a debug line the first time (shown with ``AGENTS_SDK_DEBUG=1``)."""
    if not isinstance(value, harness_session.UnknownValue):
        return value
    if (field, value.text) not in _logged:
        _logged.add((field, value.text))
        logger.debug("Read a value this SDK version does not know", field=field, value=value.text)
    return UnknownValue(value.text)
