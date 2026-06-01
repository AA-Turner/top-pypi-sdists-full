"""
Pipecat observer handler for Aigie SDK.

Implements BaseObserver to automatically trace Pipecat pipeline executions,
including conversations, turns, STT/TTS/LLM calls, and interruptions.

Provides comprehensive voice metrics tracking including TTFB and latency.
"""

import contextlib
import logging
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any


from ...buffer import EventType
from ...context_manager import merge_metadata
from ...cost_tracking import UsageMetadata, calculate_cost
from .config import PipecatConfig
from .drift_detection import VoiceDriftDetector
from .error_detection import VoiceErrorDetector
from .metrics import MetricsAggregator, VoiceMetrics

logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    """Get current time in UTC with timezone info."""
    return datetime.now(timezone.utc)


def _utc_isoformat() -> str:
    """Get current UTC time as ISO format string."""
    return datetime.now(timezone.utc).isoformat()


if TYPE_CHECKING:
    with contextlib.suppress(ImportError):
        from pipecat.observers.base_observer import FramePushed


class AigieObserver:
    """
    Aigie observer for Pipecat pipeline monitoring.

    Non-intrusive - observes frame flow without blocking the pipeline.
    Implements the BaseObserver pattern from Pipecat.

    Trace Hierarchy:
        TRACE: Voice Conversation
        ├── SPAN: Turn 1 (type=turn)
        │   ├── SPAN: STT - "Hello, how can I help?"
        │   ├── SPAN: LLM - 150 tokens
        │   └── SPAN: TTS - 2.3s audio
        ├── SPAN: Turn 2 (type=turn)
        │   ├── SPAN: STT - "What's the weather?"
        │   ├── SPAN: LLM - 200 tokens
        │   └── SPAN: TTS - 3.1s audio

    Example:
        >>> from pipecat.pipeline.task import PipelineTask
        >>> from aigie.integrations.pipecat import AigieObserver
        >>>
        >>> observer = AigieObserver()
        >>> task = PipelineTask(pipeline, observers=[observer])
        >>> await task.run()
    """

    def __init__(
        self,
        config: PipecatConfig | None = None,
        trace_name: str | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
    ):
        """
        Initialize Pipecat observer.

        Args:
            config: Configuration for tracing behavior
            trace_name: Name for the trace (default: "Voice Conversation")
            metadata: Additional metadata to attach
            tags: Tags to apply to trace and spans
            user_id: User ID for the trace
            session_id: Session ID for the trace
        """
        self.config = config or PipecatConfig.from_env()
        self.trace_name = trace_name or "Voice Conversation"
        self.metadata = metadata or {}
        self.tags = tags or []
        self.user_id = user_id
        self.session_id = session_id

        # State tracking
        self.trace_id: str | None = None
        self.conversation_span_id: str | None = None
        self.current_turn_span_id: str | None = None
        self.current_stt_span_id: str | None = None
        self.current_llm_span_id: str | None = None
        self.current_tts_span_id: str | None = None

        # Timing state for TTFB calculations
        self._stt_start_time: datetime | None = None
        self._llm_start_time: datetime | None = None
        self._tts_start_time: datetime | None = None
        self._turn_start_time: datetime | None = None
        self._conversation_start_time: datetime | None = None
        self._user_stopped_speaking_time: datetime | None = None

        # Track if we've seen first results (for TTFB)
        self._stt_first_result: bool = False
        self._llm_first_token: bool = False
        self._tts_first_audio: bool = False

        # Service call tracking maps for concurrent calls
        self._stt_calls: dict[str, dict[str, Any]] = {}
        self._llm_calls: dict[str, dict[str, Any]] = {}
        self._tts_calls: dict[str, dict[str, Any]] = {}

        # Metrics tracking
        self._current_turn_metrics: VoiceMetrics | None = None
        self._metrics_aggregator = MetricsAggregator()

        # Error detection
        self._error_detector = VoiceErrorDetector()
        self._has_errors = False
        self._error_messages: list[str] = []

        # Drift detection
        self._drift_detector = VoiceDriftDetector()

        # Turn tracking
        self._turn_count = 0
        self._in_turn = False

        # Transcription accumulator for the current turn
        self._current_transcription = ""
        self._current_bot_response = ""

        # Conversation completion guard — EndFrame fires per processor
        self._conversation_completed = False

        # Aigie client (lazy loaded)
        self._aigie = None

    def _get_aigie(self):
        """Lazy load Aigie client."""
        if self._aigie is None:
            from ...client import get_aigie

            self._aigie = get_aigie()
        return self._aigie

    # ========================================================================
    # BaseObserver Interface
    # ========================================================================

    async def on_process_frame(self, data) -> None:
        """Handle frame processing events (required by Pipecat >= 0.0.100)."""
        pass

    async def on_push_frame(self, data: "FramePushed") -> None:
        """
        Route frames to specific handlers.

        This is the main entry point called by Pipecat for each frame.

        IMPORTANT: on_push_frame is called once per frame transfer between
        processors. A frame traversing N processors generates N-1 push events.
        Individual handlers use state-based guards to ensure each event type
        is handled exactly once (e.g., only one trace per StartFrame).
        """
        if not self.config.enabled:
            return

        frame = data.frame
        frame_class = type(frame).__name__

        # Dynamically route based on frame type name
        # This avoids import issues when pipecat isn't installed
        handler_map = {
            # Conversation lifecycle
            "StartFrame": self._handle_start_frame,
            "EndFrame": self._handle_end_frame,
            "CancelFrame": self._handle_cancel_frame,
            # Turn tracking
            "UserStartedSpeakingFrame": self._handle_user_started_speaking,
            "UserStoppedSpeakingFrame": self._handle_user_stopped_speaking,
            "BotStartedSpeakingFrame": self._handle_bot_started_speaking,
            "BotStoppedSpeakingFrame": self._handle_bot_stopped_speaking,
            "InterruptionFrame": self._handle_interruption,
            # STT frames
            "TranscriptionFrame": self._handle_transcription,
            "InterimTranscriptionFrame": self._handle_interim_transcription,
            # LLM frames
            "LLMFullResponseStartFrame": self._handle_llm_start,
            "LLMFullResponseEndFrame": self._handle_llm_end,
            "TextFrame": self._handle_text_frame,
            "LLMTextFrame": self._handle_llm_text,
            # TTS frames
            "TTSStartedFrame": self._handle_tts_started,
            "TTSStoppedFrame": self._handle_tts_stopped,
            "TTSAudioRawFrame": self._handle_tts_audio,
            "AudioRawFrame": self._handle_audio_frame,
            # Metrics frames
            "MetricsFrame": self._handle_metrics,
            "TTFBMetricsFrame": self._handle_ttfb_metrics,
            "ProcessingMetricsFrame": self._handle_processing_metrics,
            # Error frames
            "ErrorFrame": self._handle_error,
        }

        handler = handler_map.get(frame_class)
        if handler:
            try:
                await handler(data)
            except Exception as e:
                logger.warning(f"[AIGIE] Error handling {frame_class}: {e}")

    # ========================================================================
    # Conversation Lifecycle Handlers
    # ========================================================================

    async def _handle_start_frame(self, data: "FramePushed") -> None:
        """Handle StartFrame - create trace and conversation span."""
        if not self.config.trace_conversations:
            return

        # Guard: only create trace on first StartFrame
        if self.trace_id:
            return

        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        try:
            self.trace_id = str(uuid.uuid4())
            self._conversation_start_time = _utc_now()

            # Reset state for new conversation
            self._reset_conversation_state()

            # Create trace
            trace_data = {
                "id": self.trace_id,
                "name": self.trace_name,
                "metadata": merge_metadata(
                    {
                        "framework": "pipecat",
                        "type": "voice_conversation",
                        **self.metadata,
                    }
                ),
                "tags": self.tags,
                "start_time": self._conversation_start_time.isoformat(),
            }

            if self.user_id:
                trace_data["user_id"] = self.user_id
            if self.session_id:
                trace_data["session_id"] = self.session_id

            await aigie._buffer.add(EventType.TRACE_CREATE, trace_data)
            await aigie._buffer.flush()

            # Create Conversation span as a wrapper for the entire conversation
            # Use "workflow" type which is a valid SpanType
            self.conversation_span_id = str(uuid.uuid4())
            conv_span_data = {
                "id": self.conversation_span_id,
                "trace_id": self.trace_id,
                "parent_id": None,  # Direct child of trace root
                "name": "Conversation",
                "type": "workflow",  # Valid SpanType
                "start_time": self._conversation_start_time.isoformat(),
                "metadata": merge_metadata(
                    {
                        "framework": "pipecat",
                        "span_category": "conversation",
                    }
                ),
                "tags": self.tags,
            }
            await aigie._buffer.add(EventType.SPAN_CREATE, conv_span_data)

            # Start drift detection
            self._drift_detector.start_conversation()

            logger.debug(f"[AIGIE] Conversation started: {self.trace_id}")

        except Exception as e:
            logger.warning(f"[AIGIE] Error in _handle_start_frame: {e}")

    async def _handle_end_frame(self, data: "FramePushed") -> None:
        """Handle EndFrame - complete conversation span and trace."""
        await self._complete_conversation(status="success")

    async def _handle_cancel_frame(self, data: "FramePushed") -> None:
        """Handle CancelFrame - complete conversation with cancelled status."""
        await self._complete_conversation(status="cancelled")

    async def _complete_conversation(self, status: str = "success") -> None:
        """Complete the conversation trace and spans."""
        if not self.trace_id or self._conversation_completed:
            return
        self._conversation_completed = True

        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        try:
            end_time = _utc_now()

            # Complete any pending turn
            if self._in_turn:
                await self._complete_turn()

            # Complete conversation span
            if self.conversation_span_id:
                duration_ms = 0
                if self._conversation_start_time:
                    duration_ms = (end_time - self._conversation_start_time).total_seconds() * 1000

                # Get aggregated metrics
                metrics = self._metrics_aggregator.to_dict()

                update_data = {
                    "id": self.conversation_span_id,
                    "trace_id": self.trace_id,
                    "end_time": end_time.isoformat(),
                    "duration_ns": int(duration_ms * 1_000_000),
                    "status": status,
                    "is_error": status == "error" or self._has_errors,
                    "metadata": merge_metadata(
                        {
                            "turn_count": self._turn_count,
                            "duration_ms": duration_ms,
                            **metrics,
                        }
                    ),
                }

                if self._error_messages:
                    update_data["error"] = "; ".join(self._error_messages[:3])

                await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

            # Finalize drift detection
            drift_summary = self._drift_detector.get_summary()

            # Build execution plan
            total_tokens = (
                self._metrics_aggregator.total_input_tokens
                + self._metrics_aggregator.total_output_tokens
            )
            execution_plan = {
                "agent": self.trace_name or "Voice Conversation",
                "turn_count": self._turn_count,
                "total_tokens": total_tokens,
                "duration_ms": duration_ms,
                "status": status if not self._has_errors else "error",
                "error_count": self._error_detector.stats.total_errors,
                "drift_count": drift_summary.get("drift_count", 0),
                "interruption_count": self._metrics_aggregator.interruption_count,
            }

            # Update trace with final metrics (include name to restore if backend auto-create overwrote it)
            trace_update = {
                "id": self.trace_id,
                "name": self.trace_name,
                "status": status if not self._has_errors else "error",
                "end_time": end_time.isoformat(),
                "metadata": merge_metadata(
                    {
                        "turn_count": self._turn_count,
                        "interruption_count": self._metrics_aggregator.interruption_count,
                        "total_input_tokens": self._metrics_aggregator.total_input_tokens,
                        "total_output_tokens": self._metrics_aggregator.total_output_tokens,
                        "avg_user_bot_latency_ms": self._metrics_aggregator.avg_user_bot_latency_ms,
                        "error_count": self._error_detector.stats.total_errors,
                        "execution_plan": execution_plan,
                        "drift_report": drift_summary,
                    }
                ),
                "total_tokens": self._metrics_aggregator.total_input_tokens
                + self._metrics_aggregator.total_output_tokens,
                "prompt_tokens": self._metrics_aggregator.total_input_tokens,
                "completion_tokens": self._metrics_aggregator.total_output_tokens,
            }

            if self._error_messages:
                trace_update["error"] = "; ".join(self._error_messages[:3])

            await aigie._buffer.add(EventType.TRACE_UPDATE, trace_update)

            # Flush everything, then re-send TRACE_CREATE to restore name.
            # Backend's _process_span_event_list auto-creates traces with "Auto-created..."
            # A final TRACE_CREATE after all spans ensures the correct name wins.
            await aigie._buffer.flush()
            await aigie._buffer.add(
                EventType.TRACE_CREATE, {"id": self.trace_id, "name": self.trace_name}
            )
            await aigie._buffer.flush()

            logger.debug(
                f"[AIGIE] Conversation completed: {self.trace_id} (turns={self._turn_count})"
            )

        except Exception as e:
            logger.warning(f"[AIGIE] Error completing conversation: {e}")
        finally:
            # Reset trace_id so we don't process further frames for this conversation
            self.trace_id = None

    # ========================================================================
    # Turn Tracking Handlers
    # ========================================================================

    async def _handle_user_started_speaking(self, data: "FramePushed") -> None:
        """Handle UserStartedSpeakingFrame - start a new turn."""
        if not self.config.trace_turns:
            return

        # Guard: don't start a new turn if we're already in one
        if self._in_turn:
            return

        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return

        try:
            # Start new turn
            self._turn_count += 1
            self._in_turn = True
            self._turn_start_time = _utc_now()
            self._current_turn_metrics = VoiceMetrics()
            self._current_turn_metrics.record_user_started_speaking()
            self._current_transcription = ""
            self._current_bot_response = ""

            # Reset TTFB tracking for new turn
            self._stt_first_result = False
            self._llm_first_token = False
            self._tts_first_audio = False

            # Create turn span at start so child spans can reference it
            # We'll update it with full data when the turn completes
            # Use "chain" type which is a valid SpanType (turn is not in the enum)
            #
            # NOTE: Turn spans have parent_id=None (direct children of trace root)
            # This creates a FLAT/LINEAR structure in the Flow View:
            #   Conversation → Turn 1 → Turn 2 → Turn 3
            # Instead of nested structure where all turns are inside Conversation box.
            self.current_turn_span_id = str(uuid.uuid4())
            span_data = {
                "id": self.current_turn_span_id,
                "trace_id": self.trace_id,
                "parent_id": None,  # Direct child of trace for linear Flow View
                "name": f"Turn {self._turn_count}",
                "type": "chain",  # Valid SpanType - a turn is a chain of operations
                "start_time": self._turn_start_time.isoformat(),
                "metadata": merge_metadata(
                    {
                        "turn_number": self._turn_count,
                        "span_category": "turn",  # Keep original type in metadata
                        "conversation_id": self.conversation_span_id,  # Link to conversation
                    }
                ),
                "tags": self.tags,
                # Note: Don't set status here - will be set to "success" when turn completes
            }

            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

            # Start drift detection for this turn
            self._drift_detector.start_turn(self._turn_count)

            logger.debug(f"[AIGIE] Turn {self._turn_count} started")

        except Exception as e:
            logger.warning(f"[AIGIE] Error in _handle_user_started_speaking: {e}")

    async def _handle_user_stopped_speaking(self, data: "FramePushed") -> None:
        """Handle UserStoppedSpeakingFrame - record user speech end time."""
        if self._current_turn_metrics:
            self._current_turn_metrics.record_user_stopped_speaking()
            self._user_stopped_speaking_time = _utc_now()

    async def _handle_bot_started_speaking(self, data: "FramePushed") -> None:
        """Handle BotStartedSpeakingFrame - record bot speech start (for latency)."""
        if self._current_turn_metrics:
            self._current_turn_metrics.record_bot_started_speaking()

    async def _handle_bot_stopped_speaking(self, data: "FramePushed") -> None:
        """Handle BotStoppedSpeakingFrame - complete the turn."""
        if self._current_turn_metrics:
            self._current_turn_metrics.record_bot_stopped_speaking()

        # Complete the turn
        await self._complete_turn()

    async def _handle_interruption(self, data: "FramePushed") -> None:
        """Handle InterruptionFrame - record interruption event."""
        if not self.config.capture_interruptions:
            return

        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return

        try:
            self._metrics_aggregator.record_interruption()

            # Record interruption for drift detection
            self._drift_detector.record_interruption()

            # Create interruption event span
            # Use "guardrail" type which is a valid SpanType (event is not in the enum)
            span_id = str(uuid.uuid4())
            timestamp = _utc_now()

            span_data = {
                "id": span_id,
                "trace_id": self.trace_id,
                "parent_id": self.current_turn_span_id or self.conversation_span_id,
                "name": "Interruption",
                "type": "guardrail",  # Valid SpanType - interruption is like a guardrail event
                "start_time": timestamp.isoformat(),
                "end_time": timestamp.isoformat(),
                "duration_ns": 0,
                "metadata": merge_metadata(
                    {
                        "interruption": True,
                        "turn_number": self._turn_count,
                        "span_category": "interruption",  # Keep original type in metadata
                    }
                ),
                # Use "error" status for interruptions (valid SpanStatus: success, failure, error)
                "status": "error",
                "level": "WARNING",
                "status_message": "User interrupted the bot response",
            }

            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

            logger.debug(f"[AIGIE] Interruption recorded in turn {self._turn_count}")

        except Exception as e:
            logger.warning(f"[AIGIE] Error in _handle_interruption: {e}")

    async def _complete_turn(self) -> None:
        """Complete the current turn span."""
        if not self._in_turn or not self.current_turn_span_id or not self._turn_start_time:
            return

        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return

        try:
            end_time = _utc_now()
            duration_ms = (end_time - self._turn_start_time).total_seconds() * 1000

            # Record turn metrics
            if self._current_turn_metrics:
                self._metrics_aggregator.record_turn(self._current_turn_metrics)

            # Prepare turn metadata
            turn_metadata = merge_metadata(
                {
                    "turn_number": self._turn_count,
                    "duration_ms": duration_ms,
                }
            )

            if self._current_turn_metrics:
                turn_metadata.update(self._current_turn_metrics.to_dict())

            if self.config.capture_transcriptions and self._current_transcription:
                transcription = self._current_transcription
                if len(transcription) > self.config.max_transcription_length:
                    transcription = transcription[: self.config.max_transcription_length] + "..."
                turn_metadata["user_transcription"] = transcription

            if self.config.capture_bot_responses and self._current_bot_response:
                response = self._current_bot_response
                if len(response) > self.config.max_transcription_length:
                    response = response[: self.config.max_transcription_length] + "..."
                turn_metadata["bot_response"] = response

            # Update the turn span with completion data
            # Note: Backend merge issues may cause some fields not to appear
            update_data = {
                "id": self.current_turn_span_id,
                "trace_id": self.trace_id,
                "end_time": end_time.isoformat(),
                "duration_ns": int(duration_ms * 1_000_000),
                "status": "success",
                "metadata": turn_metadata,
            }

            if self._current_transcription:
                update_data["input"] = self._current_transcription[
                    : self.config.max_transcription_length
                ]
            if self._current_bot_response:
                update_data["output"] = self._current_bot_response[
                    : self.config.max_transcription_length
                ]

            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

            logger.debug(
                f"[AIGIE] Turn {self._turn_count} completed (duration={duration_ms:.0f}ms)"
            )

        except Exception as e:
            logger.warning(f"[AIGIE] Error completing turn: {e}")
        finally:
            self._in_turn = False
            self.current_turn_span_id = None
            self._current_turn_metrics = None

    # ========================================================================
    # STT Handlers
    # ========================================================================

    async def _handle_transcription(self, data: "FramePushed") -> None:
        """Handle TranscriptionFrame - final transcription result."""
        if not self.config.trace_stt:
            return

        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return

        try:
            frame = data.frame
            text = getattr(frame, "text", "") or ""

            # Accumulate transcription
            if text:
                if self._current_transcription:
                    self._current_transcription += " " + text
                else:
                    self._current_transcription = text

            # Record TTFB if this is first result
            if not self._stt_first_result and self._current_turn_metrics:
                self._current_turn_metrics.record_stt_first_result()
                self._stt_first_result = True

            # Record STT for drift detection
            stt_ttfb = (
                self._current_turn_metrics.stt_ttfb_ms if self._current_turn_metrics else None
            )
            self._drift_detector.record_stt(text, ttfb_ms=stt_ttfb)

            # Create STT span
            # Use "tool" type which is a valid SpanType (stt is not in the enum)
            span_id = str(uuid.uuid4())
            timestamp = _utc_now()

            span_data = {
                "id": span_id,
                "trace_id": self.trace_id,
                "parent_id": self.current_turn_span_id or self.conversation_span_id,
                "name": "STT",
                "type": "tool",  # Valid SpanType - STT is a tool call
                "start_time": timestamp.isoformat(),
                "end_time": timestamp.isoformat(),
                "duration_ns": 0,
                "metadata": merge_metadata(
                    {
                        "service": "stt",
                        "span_category": "stt",  # Keep original type in metadata
                    }
                ),
                "status": "success",
            }

            # Include model name if configured
            if self.config.stt_model:
                span_data["model"] = self.config.stt_model
                span_data["metadata"]["model"] = self.config.stt_model

            if self.config.capture_transcriptions and text:
                span_data["output"] = text[: self.config.max_transcription_length]
                span_data["metadata"]["transcription"] = text[
                    : self.config.max_transcription_length
                ]

            # Include TTFB if available
            if self._current_turn_metrics and self._current_turn_metrics.stt_ttfb_ms:
                span_data["metadata"]["ttfb_ms"] = self._current_turn_metrics.stt_ttfb_ms

            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        except Exception as e:
            logger.warning(f"[AIGIE] Error in _handle_transcription: {e}")

    async def _handle_interim_transcription(self, data: "FramePushed") -> None:
        """Handle InterimTranscriptionFrame - partial transcription."""
        # For interim results, we just track TTFB
        if not self._stt_first_result and self._current_turn_metrics:
            self._current_turn_metrics.record_stt_first_result()
            self._stt_first_result = True

    # ========================================================================
    # LLM Handlers
    # ========================================================================

    async def _handle_llm_start(self, data: "FramePushed") -> None:
        """Handle LLMFullResponseStartFrame - LLM processing started."""
        if not self.config.trace_llm:
            return

        # Guard: don't start if already tracking an LLM call
        if self.current_llm_span_id:
            return

        # Just record start time and generate span ID - we'll create the span at end
        # This works around backend merge issues where SPAN_UPDATE doesn't merge properly
        self._llm_start_time = _utc_now()
        self.current_llm_span_id = str(uuid.uuid4())

        if self._current_turn_metrics:
            self._current_turn_metrics.record_llm_start()

    async def _handle_llm_end(self, data: "FramePushed") -> None:
        """Handle LLMFullResponseEndFrame - LLM processing completed."""
        if not self.current_llm_span_id or not self._llm_start_time:
            return

        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return

        try:
            end_time = _utc_now()
            duration_ms = (end_time - self._llm_start_time).total_seconds() * 1000

            # Extract token usage if available from the frame
            frame = data.frame
            input_tokens = getattr(frame, "input_tokens", 0) or 0
            output_tokens = getattr(frame, "output_tokens", 0) or 0

            if self._current_turn_metrics:
                self._current_turn_metrics.record_llm_end(input_tokens, output_tokens)

            # Record LLM for drift detection
            llm_ttfb = (
                self._current_turn_metrics.llm_ttfb_ms if self._current_turn_metrics else None
            )
            self._drift_detector.record_llm(
                self._current_bot_response or "",
                ttfb_ms=llm_ttfb,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
            )

            # Calculate total tokens
            total_tokens = input_tokens + output_tokens

            # Calculate cost if model is configured
            input_cost = 0.0
            output_cost = 0.0
            total_cost = 0.0
            if self.config.llm_model and (input_tokens > 0 or output_tokens > 0):
                try:
                    usage = UsageMetadata(
                        input_tokens=input_tokens,
                        output_tokens=output_tokens,
                        total_tokens=total_tokens,
                        model=self.config.llm_model,
                    )
                    cost_breakdown = calculate_cost(usage)
                    if cost_breakdown:
                        input_cost = float(cost_breakdown.input_cost)
                        output_cost = float(cost_breakdown.output_cost)
                        total_cost = float(cost_breakdown.total_cost)
                except Exception as cost_err:
                    logger.warning(
                        f"[AIGIE] Cost calculation failed for model {self.config.llm_model}: {cost_err}"
                    )

            # Build metadata with token usage in the format backend expects
            # Backend expects prompt_tokens/completion_tokens (not input_tokens/output_tokens)
            metadata = merge_metadata(
                {
                    "service": "llm",
                    "duration_ms": duration_ms,
                    # Store tokens with both naming conventions for compatibility
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "prompt_tokens": input_tokens,  # Backend expects this name
                    "completion_tokens": output_tokens,  # Backend expects this name
                    "total_tokens": total_tokens,
                    # Cost information
                    "input_cost": input_cost,
                    "output_cost": output_cost,
                    "total_cost": total_cost,
                    "cost": total_cost,  # Some backends use 'cost' directly
                    # Token usage nested object for some backends
                    "token_usage": {
                        "prompt_tokens": input_tokens,
                        "completion_tokens": output_tokens,
                        "total_tokens": total_tokens,
                        "input_tokens": input_tokens,
                        "output_tokens": output_tokens,
                        "input_cost": input_cost,
                        "output_cost": output_cost,
                        "total_cost": total_cost,
                    },
                }
            )

            # Include model in metadata
            if self.config.llm_model:
                metadata["model"] = self.config.llm_model

            # Include TTFB if available
            if self._current_turn_metrics and self._current_turn_metrics.llm_ttfb_ms:
                metadata["ttfb_ms"] = self._current_turn_metrics.llm_ttfb_ms

            # Create COMPLETE span with all data at once (workaround for backend merge issues)
            # NOTE: Top-level token fields (prompt_tokens, completion_tokens, total_tokens)
            # cause LLM spans to not appear in the UI, so we only put them in metadata
            # However, token_usage as an object might work (matching span.py pattern)
            span_data = {
                "id": self.current_llm_span_id,
                "trace_id": self.trace_id,
                "parent_id": self.current_turn_span_id or self.conversation_span_id,
                "name": "LLM",
                "type": "llm",
                "start_time": self._llm_start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration_ns": int(duration_ms * 1_000_000),
                "status": "success",
                "metadata": metadata,
                # Token usage as object (matching span.py format)
                "token_usage": {
                    "prompt_tokens": input_tokens,
                    "completion_tokens": output_tokens,
                    "total_tokens": total_tokens,
                    "unit": "TOKENS",
                    "input_cost": input_cost,
                    "output_cost": output_cost,
                    "total_cost": total_cost,
                },
                # Also use the 'usage' key that some backends expect
                "usage": {
                    "prompt_tokens": input_tokens,
                    "completion_tokens": output_tokens,
                    "total_tokens": total_tokens,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "input_cost": input_cost,
                    "output_cost": output_cost,
                    "total_cost": total_cost,
                },
                # Top-level cost fields
                "input_cost": input_cost,
                "output_cost": output_cost,
                "total_cost": total_cost,
            }

            # Include model at top level
            if self.config.llm_model:
                span_data["model"] = self.config.llm_model

            # Include input (user transcription)
            if self._current_transcription:
                span_data["input"] = self._current_transcription[
                    : self.config.max_transcription_length
                ]

            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)


            logger.debug(
                f"[AIGIE] LLM completed (duration={duration_ms:.0f}ms, tokens={input_tokens + output_tokens})"
            )

        except Exception as e:
            logger.warning(f"[AIGIE] Error in _handle_llm_end: {e}")
        finally:
            self.current_llm_span_id = None
            self._llm_start_time = None

    async def _handle_text_frame(self, data: "FramePushed") -> None:
        """Handle TextFrame - text output (may be from LLM)."""
        frame = data.frame
        text = getattr(frame, "text", "") or ""

        if text:
            self._current_bot_response += text

    async def _handle_llm_text(self, data: "FramePushed") -> None:
        """Handle LLMTextFrame - streaming LLM text."""
        # Record TTFB on first token
        if not self._llm_first_token and self._current_turn_metrics:
            self._current_turn_metrics.record_llm_first_token()
            self._llm_first_token = True

        frame = data.frame
        text = getattr(frame, "text", "") or ""
        if text:
            self._current_bot_response += text

    # ========================================================================
    # TTS Handlers
    # ========================================================================

    async def _handle_tts_started(self, data: "FramePushed") -> None:
        """Handle TTSStartedFrame - TTS processing started."""
        if not self.config.trace_tts:
            return

        # Guard: don't start if already tracking a TTS call
        if self.current_tts_span_id:
            return

        # Just record start time and generate span ID - we'll create the span at end
        self._tts_start_time = _utc_now()
        self.current_tts_span_id = str(uuid.uuid4())

        if self._current_turn_metrics:
            self._current_turn_metrics.record_tts_start()

    async def _handle_tts_stopped(self, data: "FramePushed") -> None:
        """Handle TTSStoppedFrame - TTS processing completed."""
        if not self.current_tts_span_id or not self._tts_start_time:
            return

        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return

        try:
            end_time = _utc_now()
            duration_ms = (end_time - self._tts_start_time).total_seconds() * 1000

            # Get character count from bot response
            characters = len(self._current_bot_response)
            if self._current_turn_metrics:
                self._current_turn_metrics.record_tts_end(characters)

            # Build metadata
            metadata = merge_metadata(
                {
                    "service": "tts",
                    "duration_ms": duration_ms,
                    "characters": characters,
                }
            )

            # Include model in metadata
            if self.config.tts_model:
                metadata["model"] = self.config.tts_model

            # Include TTFB if available
            if self._current_turn_metrics and self._current_turn_metrics.tts_ttfb_ms:
                metadata["ttfb_ms"] = self._current_turn_metrics.tts_ttfb_ms

            # Create COMPLETE span with all data at once
            # Use "tool" type which is a valid SpanType (tts is not in the enum)
            span_data = {
                "id": self.current_tts_span_id,
                "trace_id": self.trace_id,
                "parent_id": self.current_turn_span_id or self.conversation_span_id,
                "name": "TTS",
                "type": "tool",  # Valid SpanType - TTS is a tool call
                "start_time": self._tts_start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration_ns": int(duration_ms * 1_000_000),
                "status": "success",
                "metadata": metadata,
            }

            # Include model at top level
            if self.config.tts_model:
                span_data["model"] = self.config.tts_model

            # Include the bot response (text to be synthesized) as input
            if self._current_bot_response:
                span_data["input"] = self._current_bot_response[
                    : self.config.max_transcription_length
                ]

            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

            logger.debug(
                f"[AIGIE] TTS completed (duration={duration_ms:.0f}ms, chars={characters})"
            )

        except Exception as e:
            logger.warning(f"[AIGIE] Error in _handle_tts_stopped: {e}")
        finally:
            self.current_tts_span_id = None
            self._tts_start_time = None

    async def _handle_tts_audio(self, data: "FramePushed") -> None:
        """Handle TTSAudioRawFrame - raw TTS audio data."""
        # Record TTFB on first audio frame
        if not self._tts_first_audio and self._current_turn_metrics:
            self._current_turn_metrics.record_tts_first_audio()
            self._tts_first_audio = True

        # Capture audio metadata if enabled
        if self.config.capture_audio_metadata and self._current_turn_metrics:
            frame = data.frame
            self._current_turn_metrics.audio_sample_rate = getattr(frame, "sample_rate", None)
            self._current_turn_metrics.audio_channels = getattr(frame, "num_channels", None)

    async def _handle_audio_frame(self, data: "FramePushed") -> None:
        """Handle generic AudioRawFrame."""
        # Similar to TTS audio handling for TTFB
        if not self._tts_first_audio and self._current_turn_metrics:
            self._current_turn_metrics.record_tts_first_audio()
            self._tts_first_audio = True

    # ========================================================================
    # Metrics Handlers
    # ========================================================================

    async def _handle_metrics(self, data: "FramePushed") -> None:
        """Handle MetricsFrame - general metrics from pipeline."""
        if not self.config.capture_token_usage:
            return

        frame = data.frame

        # Extract any token metrics
        if self._current_turn_metrics:
            input_tokens = getattr(frame, "input_tokens", None)
            output_tokens = getattr(frame, "output_tokens", None)

            if input_tokens is not None:
                self._current_turn_metrics.input_tokens = input_tokens
            if output_tokens is not None:
                self._current_turn_metrics.output_tokens = output_tokens

    async def _handle_ttfb_metrics(self, data: "FramePushed") -> None:
        """Handle TTFBMetricsFrame - time-to-first-byte metrics."""
        if not self.config.capture_ttfb or not self._current_turn_metrics:
            return

        frame = data.frame

        # Extract TTFB values if provided by the frame
        ttfb = getattr(frame, "ttfb", None)
        if ttfb and isinstance(ttfb, (int, float)):
            # Determine which service this TTFB is for
            processor = getattr(frame, "processor", None)
            if processor:
                processor_name = str(processor).lower()
                if "stt" in processor_name or "transcription" in processor_name:
                    self._current_turn_metrics.stt_ttfb_ms = ttfb
                elif "llm" in processor_name:
                    self._current_turn_metrics.llm_ttfb_ms = ttfb
                elif "tts" in processor_name:
                    self._current_turn_metrics.tts_ttfb_ms = ttfb

    async def _handle_processing_metrics(self, data: "FramePushed") -> None:
        """Handle ProcessingMetricsFrame - processing time metrics."""
        # Currently just log, can be extended for detailed metrics
        pass

    # ========================================================================
    # Error Handlers
    # ========================================================================

    async def _handle_error(self, data: "FramePushed") -> None:
        """Handle ErrorFrame - pipeline error."""
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return

        try:
            frame = data.frame
            error_msg = getattr(frame, "error", None) or getattr(frame, "message", "Unknown error")
            error_str = str(error_msg)

            self._has_errors = True
            if error_str not in self._error_messages:
                self._error_messages.append(error_str)

            # Detect and classify the error
            detected = self._error_detector.detect_from_text(
                error_str, source="pipeline", context={"turn_number": self._turn_count}
            )

            # Record error for drift detection
            self._drift_detector.record_error(error_str, service="pipeline")

            # Create error event span
            # Use "guardrail" type which is a valid SpanType (event is not in the enum)
            span_id = str(uuid.uuid4())
            timestamp = _utc_now()

            span_data = {
                "id": span_id,
                "trace_id": self.trace_id,
                "parent_id": self.current_turn_span_id or self.conversation_span_id,
                "name": "Error",
                "type": "guardrail",  # Valid SpanType - error is like a guardrail event
                "start_time": timestamp.isoformat(),
                "end_time": timestamp.isoformat(),
                "duration_ns": 0,
                "status": "error",
                "is_error": True,
                "error": error_str[:500],
                "metadata": merge_metadata(
                    {
                        "error_type": detected.error_type.value if detected else "unknown",
                        "severity": detected.severity.value if detected else "high",
                        "span_category": "error",  # Keep original type in metadata
                    }
                ),
            }

            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

            logger.warning(f"[AIGIE] Pipeline error: {error_str[:100]}")

        except Exception as e:
            logger.warning(f"[AIGIE] Error in _handle_error: {e}")

    # ========================================================================
    # Helper Methods
    # ========================================================================

    def _reset_conversation_state(self) -> None:
        """Reset all state for a new conversation."""
        self._conversation_completed = False
        self.conversation_span_id = None
        self.current_turn_span_id = None
        self.current_stt_span_id = None
        self.current_llm_span_id = None
        self.current_tts_span_id = None

        self._stt_start_time = None
        self._llm_start_time = None
        self._tts_start_time = None
        self._turn_start_time = None
        self._user_stopped_speaking_time = None

        self._stt_first_result = False
        self._llm_first_token = False
        self._tts_first_audio = False

        self._stt_calls.clear()
        self._llm_calls.clear()
        self._tts_calls.clear()

        self._current_turn_metrics = None
        self._metrics_aggregator = MetricsAggregator()
        self._error_detector = VoiceErrorDetector()
        self._drift_detector = VoiceDriftDetector()

        self._has_errors = False
        self._error_messages = []
        self._turn_count = 0
        self._in_turn = False
        self._current_transcription = ""
        self._current_bot_response = ""
