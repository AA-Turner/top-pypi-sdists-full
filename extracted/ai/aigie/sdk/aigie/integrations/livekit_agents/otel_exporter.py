"""
LiveKit-aware OTel SpanExporter for Aigie.

Maps LiveKit Agents' native OpenTelemetry spans to Aigie's trace/span
format and sends them via the Aigie event buffer.

LiveKit OTel spans (livekit-agents 1.5.x):
- agent_session (root)
- user_turn / agent_speaking / user_speaking
- llm_request / llm_request_run
- tts_request / tts_request_run
- eou_detection
- drain_agent_activity

LiveKit OTel attributes (lk.* and gen_ai.*):
- gen_ai.request.model, gen_ai.usage.input_tokens, gen_ai.usage.output_tokens
- lk.response.text, lk.response.ttfb, lk.response.ttft
- lk.user_transcript, lk.user_input
- lk.function_tool.name, lk.function_tool.arguments, lk.function_tool.output
- lk.input_text (TTS), lk.e2e_latency, lk.is_interruption
- lk.chat_ctx, lk.room_name, lk.job_id, lk.agent_name
"""

import logging
import uuid
from collections import OrderedDict
from collections.abc import Sequence
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)


class _LRUDict(OrderedDict):
    """Bounded LRU dictionary for trace ID correlation."""

    def __init__(self, max_size: int = 1000):
        super().__init__()
        self._max_size = max_size

    def __setitem__(self, key, value):
        if key in self:
            self.move_to_end(key)
        super().__setitem__(key, value)
        if len(self) > self._max_size:
            self.popitem(last=False)


def otel_trace_id_to_uuid(otel_trace_id: int) -> str:
    """Convert 128-bit OTel trace ID to UUID4 string format."""
    hex_id = format(otel_trace_id, "032x")
    return str(uuid.UUID(hex_id))


def otel_span_id_to_str(otel_span_id: int) -> str:
    """Convert 64-bit OTel span ID to a UUID-like string."""
    hex_id = format(otel_span_id, "016x")
    return str(uuid.UUID(f"00000000-0000-0000-{hex_id[:4]}-{hex_id[4:]}"))


class LiveKitAigieSpanExporter:
    """
    OpenTelemetry SpanExporter that converts LiveKit spans to Aigie format.

    Uses LiveKit's exact OTel attribute names (lk.* and gen_ai.*) for
    accurate data extraction.
    """

    def __init__(self, aigie_client: Any):
        self.aigie = aigie_client
        self._trace_map = _LRUDict(max_size=1000)
        self._created_traces: set = set()

    def export(self, spans: Sequence[Any]) -> Any:
        """Export a batch of OTel spans to Aigie."""
        try:
            from opentelemetry.sdk.trace.export import SpanExportResult
        except ImportError:
            return None

        try:
            for span in spans:
                self._process_span(span)
            return SpanExportResult.SUCCESS
        except Exception as e:
            logger.warning("[AIGIE-OTel] Export failed: %s", e)
            try:
                return SpanExportResult.FAILURE
            except Exception:
                return None

    def _process_span(self, span: Any) -> None:
        """Process a single OTel span."""
        if not self.aigie or not getattr(self.aigie, "_buffer", None):
            return

        from ...buffer import EventType
        from ...utils.safe import schedule_async

        otel_trace_id = span.context.trace_id
        trace_id = self._get_or_create_trace_id(otel_trace_id)
        span_id = otel_span_id_to_str(span.context.span_id)
        attrs = dict(span.attributes) if span.attributes else {}

        # Create trace on first span
        if otel_trace_id not in self._created_traces:
            self._created_traces.add(otel_trace_id)
            import os

            schedule_async(
                self.aigie._buffer.add(
                    EventType.TRACE_CREATE,
                    {
                        "trace_id": trace_id,
                        "name": "Voice Conversation",
                        "session_id": attrs.get("lk.room_name"),
                        "environment": os.environ.get("ENVIRONMENT", "production"),
                        "metadata": {
                            "framework": "livekit_agents",
                            "type": "voice_conversation",
                            "source": "otel",
                            "room_name": attrs.get("lk.room_name"),
                            "job_id": attrs.get("lk.job_id"),
                            "agent_name": attrs.get("lk.agent_name"),
                        },
                        "start_time": self._ns_to_iso(span.start_time),
                    },
                )
            )

        # Parent span
        parent_span_id = None
        if span.parent and span.parent.span_id:
            parent_span_id = otel_span_id_to_str(span.parent.span_id)

        span_type = self._get_span_type(span)

        # Extract model name for top-level field
        model_name = (
            attrs.get("gen_ai.request.model")
            or attrs.get("gen_ai.response.model")
            or attrs.get("lk.tts.label")
            or attrs.get("lk.stt.model")
        )

        # Calculate completion_start_time for LLM spans
        completion_start_time = None
        if span_type == "llm" and span.start_time and span.end_time:
            ttft = attrs.get("lk.response.ttft") or attrs.get("lk.response.ttfb")
            if ttft is not None:
                ttft_ns = int(ttft * 1e9)
                completion_start_time = self._ns_to_iso(span.start_time + ttft_ns)

        payload = {
            "trace_id": trace_id,
            "id": span_id,
            "parent_id": parent_span_id,
            "name": self._get_display_name(span, span_type, attrs),
            "type": span_type,
            "model": model_name,
            "level": "DEFAULT",
            "input": self._extract_input(attrs, span_type, span),
            "output": self._extract_output(attrs, span_type, span),
            "metadata": self._extract_metadata(attrs, span_type, span),
            "start_time": self._ns_to_iso(span.start_time),
            "end_time": self._ns_to_iso(span.end_time),
        }

        if completion_start_time:
            payload["completion_start_time"] = completion_start_time

        # Token usage (use prompt_tokens/completion_tokens to match backend)
        usage = self._extract_usage(attrs)
        if usage:
            payload["usage"] = usage

        # Error status
        try:
            from opentelemetry.trace import StatusCode

            if span.status and span.status.status_code == StatusCode.ERROR:
                payload["status"] = "error"
                payload["level"] = "ERROR"
                if span.status.description:
                    payload["status_message"] = span.status.description
                    payload["metadata"]["error_message"] = span.status.description
        except ImportError:
            pass

        schedule_async(self.aigie._buffer.add(EventType.SPAN_CREATE, payload))

    def _get_or_create_trace_id(self, otel_trace_id: int) -> str:
        if otel_trace_id not in self._trace_map:
            self._trace_map[otel_trace_id] = otel_trace_id_to_uuid(otel_trace_id)
        return self._trace_map[otel_trace_id]

    def _get_span_type(self, span: Any) -> str:
        """Detect span type from LiveKit span name and attributes."""
        attrs = span.attributes or {}
        name = span.name.lower()

        # gen_ai operations → LLM
        if attrs.get("gen_ai.operation.name") or attrs.get("gen_ai.request.model"):
            return "llm"

        # LiveKit span name patterns
        if "llm" in name:
            return "llm"
        if "tts" in name:
            return "tts"
        if "stt" in name or "eou" in name or "audio_recognition" in name:
            return "stt"
        if "function_tool" in name or "tool" in name:
            return "tool"
        if "user_turn" in name:
            return "turn"
        if "agent_session" in name:
            return "conversation"
        if "agent_speaking" in name:
            return "generation"
        if "user_speaking" in name:
            return "transcription"
        if "drain" in name:
            return "lifecycle"

        return "span"

    def _get_display_name(self, span: Any, span_type: str, attrs: dict) -> str:
        """Generate readable display name."""
        if span_type == "llm":
            model = attrs.get("gen_ai.request.model", "")
            return f"LLM: {model}" if model else span.name

        if span_type == "tts":
            label = attrs.get("lk.tts.label", "")
            return f"TTS: {label}" if label else span.name

        if span_type == "tool":
            tool_name = attrs.get("lk.function_tool.name", "")
            return f"Tool: {tool_name}" if tool_name else span.name

        if span_type == "turn":
            return "User Turn"

        if span_type == "conversation":
            return "Agent Session"

        return span.name

    def _extract_input(self, attrs: dict, span_type: str, span: Any) -> str | None:
        """Extract input using LiveKit's exact attribute names."""
        if span_type == "llm":
            model = attrs.get("gen_ai.request.model", "")
            tokens = attrs.get("gen_ai.usage.input_tokens", 0)
            return f"Prompt ({tokens} tokens) → {model}" if model else None

        if span_type == "tts":
            text = attrs.get("lk.input_text", "")
            return text[:500] if text else None

        if span_type == "turn":
            return attrs.get("lk.user_transcript") or attrs.get("lk.user_input") or None

        if span_type == "tool":
            return str(attrs.get("lk.function_tool.arguments", ""))[:500] or None

        if span_type == "conversation":
            return attrs.get("lk.instructions") or None

        return None

    def _extract_output(self, attrs: dict, span_type: str, span: Any) -> str | None:
        """Extract output using LiveKit's exact attribute names."""
        if span_type == "llm":
            text = attrs.get("lk.response.text", "")
            if text:
                return text[:1000]
            tokens = attrs.get("gen_ai.usage.output_tokens", 0)
            return f"Completion ({tokens} tokens)"

        if span_type == "tts":
            streaming = attrs.get("lk.tts.streaming", False)
            return f"Audio (streaming={streaming})"

        if span_type == "turn":
            return attrs.get("lk.response.text") or None

        if span_type == "tool":
            output = attrs.get("lk.function_tool.output", "")
            return str(output)[:500] if output else None

        if span_type == "generation":
            return attrs.get("lk.response.text") or None

        return None

    def _extract_metadata(self, attrs: dict, span_type: str, span: Any) -> dict[str, Any]:
        """Extract metadata including voice-specific metrics."""
        metadata: dict[str, Any] = {
            "framework": "livekit_agents",
            "source": "otel",
        }

        # Common LiveKit attributes
        for key in ("lk.room_name", "lk.job_id", "lk.agent_name", "lk.speech_id"):
            val = attrs.get(key)
            if val is not None:
                metadata[key.replace("lk.", "")] = val

        if span_type == "llm":
            metadata["model"] = attrs.get("gen_ai.request.model")
            metadata["provider"] = attrs.get("gen_ai.provider.name")
            metadata["ttft_ms"] = self._to_ms(attrs.get("lk.response.ttft"))
            metadata["ttfb_ms"] = self._to_ms(attrs.get("lk.response.ttfb"))
            metadata["input_tokens"] = attrs.get("gen_ai.usage.input_tokens")
            metadata["output_tokens"] = attrs.get("gen_ai.usage.output_tokens")
            metadata["input_cached_tokens"] = attrs.get("gen_ai.usage.input_cached_tokens")

            # Extract function calls from response
            func_calls = attrs.get("lk.response.function_calls")
            if func_calls:
                metadata["function_calls"] = str(func_calls)[:500]

        elif span_type == "tts":
            metadata["model"] = attrs.get("lk.tts.label")
            metadata["streaming"] = attrs.get("lk.tts.streaming")
            metadata["input_text_length"] = len(attrs.get("lk.input_text", ""))

        elif span_type == "turn":
            metadata["user_transcript"] = attrs.get("lk.user_transcript")
            metadata["is_interruption"] = attrs.get("lk.is_interruption")
            metadata["e2e_latency"] = attrs.get("lk.e2e_latency")
            metadata["eou_delay"] = attrs.get("lk.eou.endpointing_delay")
            metadata["transcription_delay"] = attrs.get("lk.transcription_delay")
            metadata["transcript_confidence"] = attrs.get("lk.transcript_confidence")

        elif span_type == "tool":
            metadata["tool_name"] = attrs.get("lk.function_tool.name")
            metadata["tool_id"] = attrs.get("lk.function_tool.id")
            metadata["is_error"] = attrs.get("lk.function_tool.is_error")

        elif span_type == "conversation":
            metadata["agent_label"] = attrs.get("lk.agent_label")
            metadata["interrupted"] = attrs.get("lk.interrupted")

        # Duration
        if span.start_time and span.end_time:
            metadata["duration_ns"] = span.end_time - span.start_time

        return {k: v for k, v in metadata.items() if v is not None}

    def _extract_usage(self, attrs: dict) -> dict[str, Any] | None:
        """Extract token usage from gen_ai attributes."""
        input_tokens = attrs.get("gen_ai.usage.input_tokens")
        output_tokens = attrs.get("gen_ai.usage.output_tokens")

        if input_tokens is not None or output_tokens is not None:
            inp = int(input_tokens or 0)
            out = int(output_tokens or 0)
            return {"prompt_tokens": inp, "completion_tokens": out, "total_tokens": inp + out}

        return None

    @staticmethod
    def _to_ms(value: float | None) -> float | None:
        """Convert seconds to milliseconds (LiveKit uses seconds)."""
        if value is None:
            return None
        return value * 1000 if value < 100 else value

    @staticmethod
    def _ns_to_iso(ns_timestamp: int | None) -> str | None:
        """Convert nanosecond timestamp to ISO format."""
        if ns_timestamp is None:
            return None
        dt = datetime.fromtimestamp(ns_timestamp / 1e9, tz=timezone.utc)
        return dt.isoformat()

    def shutdown(self) -> None:
        """Shutdown — flush remaining events."""
        if self.aigie and getattr(self.aigie, "_buffer", None):
            from ...utils.safe import schedule_async

            schedule_async(self.aigie.flush())

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        self.shutdown()
        return True
