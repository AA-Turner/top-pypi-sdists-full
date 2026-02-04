from __future__ import annotations
import json
import time
from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
    TYPE_CHECKING,
    Union,
    Iterator,
)
from datetime import datetime, timezone
from uuid import uuid4
from dataclasses import dataclass

from .models import Attachment, PartialTrackAIEvent
from . import analytics as _core
from opentelemetry import context as context_api

if TYPE_CHECKING:
    from .analytics import ManualSpan


class Interaction:
    """
    Thin helper returned by analytics.begin().
    Each mutator just relays a partial update back to Analytics.
    """

    __slots__ = (
        "_event_id",
        "_user_id",
        "_event",
        "_convo_id",
        "_analytics",
        "__weakref__",
    )

    def __init__(
        self,
        event_id: Optional[str] = None,
        user_id: Optional[str] = None,
        event: Optional[str] = None,
        convo_id: Optional[str] = None,
    ):
        self._event_id = event_id or str(uuid4())
        self._user_id = user_id
        self._event = event
        self._convo_id = convo_id
        self._analytics = _core

    # -- mutators ----------------------------------------------------------- #
    def set_input(self, text: str) -> None:
        self._analytics._track_ai_partial(
            PartialTrackAIEvent(event_id=self._event_id, ai_data={"input": text})
        )

    def add_attachments(self, attachments: List[Attachment]) -> None:
        self._analytics._track_ai_partial(
            PartialTrackAIEvent(event_id=self._event_id, attachments=attachments)
        )

    def set_properties(self, props: Dict[str, Any]) -> None:
        self._analytics._track_ai_partial(
            PartialTrackAIEvent(event_id=self._event_id, properties=props)
        )

    def set_property(self, key: str, value: Any) -> None:
        self.set_properties({key: value})

    def finish(self, *, output: str | None = None, **extra) -> None:

        payload = PartialTrackAIEvent(
            event_id=self._event_id,
            ai_data={"output": output} if output is not None else None,
            is_pending=False,
            **extra,
        )
        self._analytics._track_ai_partial(payload)

    def start_span(
        self,
        kind: Literal["task", "tool"],
        name: str,
        version: int | None = None,
    ) -> "ManualSpan":
        """
        Create a manual span tied to this interaction.

        The span automatically inherits association properties from this interaction
        (event_id, user_id, event, convo_id) for proper tracing.

        Args:
            kind: Type of span - "task" or "tool"
            name: Name of the span
            version: Optional version number

        Returns:
            ManualSpan instance that must be explicitly ended with .end()
        """
        return self._analytics.start_span(
            kind,
            name,
            version,
            event_id=self._event_id,
            user_id=self._user_id,
            event=self._event,
            convo_id=self._convo_id,
        )

    def track_tool(
        self,
        *,
        name: str,
        input: Any | None = None,
        output: Any | None = None,
        duration_ms: float | int | None = None,
        start_time: datetime | int | float | None = None,
        error: BaseException | str | None = None,
        properties: Dict[str, Any] | None = None,
        version: int | None = None,
    ) -> None:
        """
        Retroactively log a tool span tied to this interaction.
        """
        if not _core._tracing_enabled or not _core.TracerWrapper.verify_initialized():
            return

        # Duration normalization
        dur_ms = float(duration_ms) if duration_ms is not None else 0.0
        if dur_ms < 0:
            dur_ms = 0.0
        duration_ns = int(round(dur_ms * 1_000_000))

        # start_time normalization (epoch nanoseconds)
        start_ns: int | None = None
        if isinstance(start_time, datetime):
            dt = start_time
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            else:
                dt = dt.astimezone(timezone.utc)

            epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
            delta = dt - epoch
            total_us = (
                delta.days * 86400 + delta.seconds
            ) * 1_000_000 + delta.microseconds
            start_ns = total_us * 1_000
        elif isinstance(start_time, (int, float)):
            v = float(start_time)
            # Heuristic: values smaller than ~1973 in ms are likely epoch-seconds
            start_ns = (
                int(round(v * 1_000_000_000))
                if abs(v) < 1e11
                else int(round(v * 1_000_000))
            )

        if start_ns is None:
            start_ns = time.time_ns() - duration_ns

        end_ns = start_ns + duration_ns

        tlp_kind = _core.TraceloopSpanKindValues.TOOL
        span_name = f"{name}.{tlp_kind.value}"

        tracer = _core.trace.get_tracer("traceloop.tracer")
        span = tracer.start_span(span_name, start_time=start_ns)

        try:
            span.set_attribute(_core.SpanAttributes.TRACELOOP_SPAN_KIND, tlp_kind.value)
            span.set_attribute(_core.SpanAttributes.TRACELOOP_ENTITY_NAME, name)
            if version is not None:
                span.set_attribute(
                    _core.SpanAttributes.TRACELOOP_ENTITY_VERSION, version
                )

            association_props = {
                "event_id": self._event_id,
                "user_id": self._user_id,
                "event": self._event,
                "convo_id": self._convo_id,
            }
            for key, value in association_props.items():
                if value is not None:
                    span.set_attribute(f"traceloop.association.properties.{key}", value)

            if properties:
                for key, value in properties.items():
                    if key in association_props:
                        continue
                    if value is None:
                        continue
                    if isinstance(value, (str, bool, int, float)):
                        attr_val: Any = value
                    else:
                        try:
                            attr_val = json.dumps(value, cls=_core.JSONEncoder)
                        except Exception:
                            attr_val = str(value)
                    span.set_attribute(
                        f"traceloop.association.properties.{key}", attr_val
                    )

            if duration_ms is not None:
                span.set_attribute("traceloop.entity.duration_ms", dur_ms)

            if _core._should_send_prompts():
                if input is not None:
                    try:
                        json_input = json.dumps(
                            {"args": [input]}, cls=_core.JSONEncoder
                        )
                        span.set_attribute(
                            _core.SpanAttributes.TRACELOOP_ENTITY_INPUT,
                            _core._truncate_json_if_needed(json_input),
                        )
                    except Exception as e:
                        _core.logger.debug(
                            f"[raindrop] Could not serialize input for span: {e}"
                        )

                if output is not None:
                    try:
                        json_output = json.dumps(output, cls=_core.JSONEncoder)
                        span.set_attribute(
                            _core.SpanAttributes.TRACELOOP_ENTITY_OUTPUT,
                            _core._truncate_json_if_needed(json_output),
                        )
                    except Exception as e:
                        _core.logger.debug(
                            f"[raindrop] Could not serialize output for span: {e}"
                        )

            if error is not None:
                exc = (
                    error if isinstance(error, BaseException) else Exception(str(error))
                )
                span.set_status(_core.Status(_core.StatusCode.ERROR, str(exc)))
                span.record_exception(exc)
            else:
                span.set_status(_core.Status(_core.StatusCode.OK))
        finally:
            span.end(end_time=end_ns)

        if _core.debug_logs:
            _core.logger.debug(
                f'[raindrop] track_tool: logged tool span "{name}" (duration_ms={duration_ms})'
            )

    # convenience
    @property
    def id(self) -> str:
        return self._event_id
