"""
LiveKit Agents event handler for Aigie SDK.

Registers event listeners on AgentSession to automatically trace voice
conversations, including turns, LLM/STT/TTS calls, tool executions,
agent handoffs, and interruptions.

LiveKit Agents events are the primary integration mechanism:
- agent_state_changed: Agent lifecycle (initializing → idle → listening → thinking → speaking)
- conversation_item_added: Every message added to chat history
- function_tools_executed: Tool calls with results
- user_input_transcribed: Real-time user transcriptions
- metrics_collected: LLM/STT/TTS/EOU/Interruption metrics
- error: LLMError, STTError, TTSError, etc.
- close: Session end with reason

Trace Hierarchy:
    TRACE: Voice Conversation
    ├── SPAN: Turn 1 (type=turn)
    │   ├── SPAN: STT — transcription
    │   ├── SPAN: LLM — 150 tokens, TTFB 120ms
    │   ├── SPAN: Tool — search_weather
    │   └── SPAN: TTS — 2.3s audio
    ├── SPAN: Turn 2 (type=turn)
    │   ├── SPAN: LLM — 200 tokens
    │   └── SPAN: TTS — 1.8s audio
    └── SPAN: Agent Handoff → specialist
"""

import contextlib
import logging
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from ...buffer import EventType
from ...context_manager import merge_metadata
from .cost_tracking import VoiceCostTracker
from .metrics import MetricsAggregator, VoiceMetrics

logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _utc_isoformat() -> str:
    return datetime.now(timezone.utc).isoformat()


if TYPE_CHECKING:
    with contextlib.suppress(ImportError):
        from livekit.agents import AgentSession


class LiveKitAgentsHandler:
    """
    Aigie event handler for LiveKit Agents sessions.

    Non-intrusive — listens to AgentSession events without modifying
    the pipeline. Automatically creates traces, spans, and metrics.

    Payload contract (must match backend SpanBody / TraceBody):
        SPAN_CREATE / SPAN_UPDATE payloads use the keys ``"id"`` and
        ``"parent_id"`` — NOT ``"span_id"`` / ``"parent_span_id"``. The shared
        client._flush_events resolver picks ``payload["id"]`` first; if a span
        uses ``"span_id"`` it falls through to ``trace_id`` and every span in
        the conversation upserts the same DB row (seen in kytte-prod April 21+
        livekit traces). Keep the keys aligned with google_adk / strands.

    Example:
        >>> from livekit.agents import AgentSession
        >>> from aigie.integrations.livekit_agents import LiveKitAgentsHandler
        >>>
        >>> handler = LiveKitAgentsHandler()
        >>> session = AgentSession()
        >>> handler.register(session)
        >>> # Session events are now automatically traced
    """

    def __init__(
        self,
        config: Any | None = None,
        trace_name: str | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
    ):
        if config is None:
            from .config import LiveKitAgentsConfig

            config = LiveKitAgentsConfig.from_env()

        self.config = config
        self.trace_name = trace_name or "Voice Conversation"
        self.metadata = metadata or {}
        self.tags = tags or []
        self.user_id = user_id
        self.session_id = session_id

        # Trace state
        self.trace_id: str | None = None
        self.conversation_span_id: str | None = None
        self.current_turn_span_id: str | None = None

        # Agent state tracking
        self._agent_state: str | None = None
        self._previous_state: str | None = None
        self._session_started: bool = False
        self._session_closed: bool = False

        # Turn tracking
        self._turn_count = 0
        self._in_turn = False
        self._current_transcription = ""
        self._current_bot_response = ""

        # Metrics
        self._current_turn_metrics: VoiceMetrics | None = None
        self._metrics_aggregator = MetricsAggregator()
        self._cost_tracker = VoiceCostTracker()

        # Session-level usage aggregated by livekit 1.5.x session_usage_updated
        self._session_usage: dict[str, Any] = {}

        # TTFB tracking (time from STT final result to first agent audio)
        self._stt_committed_at: datetime | None = None
        self._agent_speech_started_at: datetime | None = None

        # Per-turn interruption tracking
        self._turn_interruption_count: int = 0

        # Error tracking
        self._errors: list[dict[str, Any]] = []

        # Model info (populated from metrics events)
        self._llm_model: str | None = None
        self._stt_model: str | None = None
        self._tts_model: str | None = None

        # Session reference (set by register())
        self._session = None

        # Aigie client (lazy)
        self._aigie = None

    def _get_aigie(self):
        """Lazy load Aigie client."""
        if self._aigie is None:
            from ...client import get_aigie

            self._aigie = get_aigie()
        return self._aigie

    # ========================================================================
    # Registration
    # ========================================================================

    @staticmethod
    def _wrap_async(coro_fn):
        """Wrap an async handler into a sync callback for LiveKit's .on().

        LiveKit's EventEmitter requires synchronous callbacks.
        We schedule the coroutine on the running event loop.
        """

        def wrapper(event):
            import asyncio

            try:
                loop = asyncio.get_running_loop()
                loop.create_task(coro_fn(event))
            except RuntimeError:
                pass  # No running loop — best effort

        return wrapper

    def register(self, session: "AgentSession") -> None:
        """Register event listeners on an AgentSession.

        This is the main entry point — call after session creation.
        """
        # Store session reference for tool extraction at trace start
        self._session = session

        try:
            session.on("agent_state_changed", self._wrap_async(self._on_agent_state_changed))
            session.on(
                "conversation_item_added", self._wrap_async(self._on_conversation_item_added)
            )
            session.on(
                "function_tools_executed", self._wrap_async(self._on_function_tools_executed)
            )
            session.on("user_input_transcribed", self._wrap_async(self._on_user_input_transcribed))
            session.on("metrics_collected", self._wrap_async(self._on_metrics_collected))
            session.on("error", self._wrap_async(self._on_error))
            session.on("close", self._wrap_async(self._on_close))

            try:
                session.on("speech_created", self._wrap_async(self._on_speech_created))
            except Exception as e:
                logger.debug("[AIGIE] speech_created event not available: %s", e)

            # livekit-agents 1.5.x deprecates metrics_collected. Register the
            # replacement event so we keep capturing aggregate usage once the
            # deprecation is enforced, without losing data on older versions.
            try:
                session.on(
                    "session_usage_updated",
                    self._wrap_async(self._on_session_usage_updated),
                )
            except Exception as e:
                logger.debug("[AIGIE] session_usage_updated event not available: %s", e)

            logger.debug("[AIGIE] Registered LiveKit Agents event listeners")
        except Exception as e:
            logger.warning(f"[AIGIE] Failed to register event listeners: {e}")

    # ========================================================================
    # Event Handlers
    # ========================================================================

    async def _on_agent_state_changed(self, event: Any) -> None:
        """Handle agent state transitions.

        States: initializing → idle → listening → thinking → speaking
        We create a trace on first state change, and track turn boundaries.
        """
        try:
            new_state = getattr(event, "new_state", None)
            old_state = getattr(event, "old_state", None)
            self._previous_state = str(old_state) if old_state else None
            self._agent_state = str(new_state) if new_state else None

            aigie = self._get_aigie()
            if not aigie or not aigie._initialized:
                return

            # Start trace on first event
            if not self._session_started:
                self._session_started = True
                await self._start_conversation(aigie)

            # Detect turn boundaries:
            # "thinking" means LLM is processing → start of a new response cycle
            if self._agent_state == "thinking" and not self._in_turn:
                await self._start_turn(aigie)

            # "idle" or "listening" after "speaking" means turn ended
            if self._agent_state in ("idle", "listening") and self._in_turn:
                await self._end_turn(aigie)

        except Exception as e:
            logger.debug(f"[AIGIE] Error in agent_state_changed handler: {e}")

    async def _on_conversation_item_added(self, event: Any) -> None:
        """Track messages added to conversation history."""
        try:
            item = getattr(event, "item", None)
            if not item:
                return

            role = getattr(item, "role", None)
            content = getattr(item, "content", None)
            text = ""

            if isinstance(content, str):
                text = content
            elif isinstance(content, list):
                for part in content:
                    if hasattr(part, "text"):
                        text += getattr(part, "text", "")
                    elif isinstance(part, str):
                        text += part

            if role == "user":
                self._current_transcription = text[: self.config.max_transcription_length]
            elif role == "assistant":
                self._current_bot_response = text[: self.config.max_content_length]

            # livekit-agents 1.5.x: ChatMessage.metrics replaces metrics_collected
            # for per-turn latency/usage. Merge into current turn metrics only
            # when the older event hasn't already populated them.
            msg_metrics = getattr(item, "metrics", None)
            if msg_metrics and self._current_turn_metrics is not None:
                ttfb = getattr(msg_metrics, "ttfb", None) or getattr(msg_metrics, "ttft", None)
                if ttfb is not None and self._current_turn_metrics.llm_ttfb_ms is None:
                    self._current_turn_metrics.llm_ttfb_ms = ttfb * 1000

                duration = getattr(msg_metrics, "duration", None)
                if duration is not None and self._current_turn_metrics.llm_duration_ms is None:
                    self._current_turn_metrics.llm_duration_ms = duration * 1000

                input_tokens = getattr(msg_metrics, "input_tokens", None) or getattr(
                    msg_metrics, "prompt_tokens", None
                )
                if input_tokens:
                    self._current_turn_metrics.input_tokens = input_tokens

                output_tokens = getattr(msg_metrics, "output_tokens", None) or getattr(
                    msg_metrics, "completion_tokens", None
                )
                if output_tokens:
                    self._current_turn_metrics.output_tokens = output_tokens

        except Exception as e:
            logger.debug(f"[AIGIE] Error in conversation_item_added handler: {e}")

    async def _on_session_usage_updated(self, event: Any) -> None:
        """Capture aggregate session usage (tokens, cost per model).

        Replacement for the deprecated metrics_collected aggregation path in
        livekit-agents 1.5.x. Stores raw usage dict on the handler so it gets
        flushed into the trace metadata on close.
        """
        try:
            usage = getattr(event, "usage", None) or getattr(event, "summary", None)
            if usage is None:
                return
            if hasattr(usage, "to_dict"):
                self._session_usage = usage.to_dict()
            elif isinstance(usage, dict):
                self._session_usage = dict(usage)
        except Exception as e:
            logger.debug(f"[AIGIE] Error in session_usage_updated handler: {e}")

    async def _on_function_tools_executed(self, event: Any) -> None:
        """Track tool executions with their inputs and outputs."""
        try:
            aigie = self._get_aigie()
            if not aigie or not aigie._initialized or not self.trace_id:
                return

            calls = getattr(event, "function_calls", []) or []
            outputs = getattr(event, "function_call_outputs", []) or []

            for i, call in enumerate(calls):
                tool_name = getattr(call, "name", "unknown")
                tool_args = getattr(call, "arguments", None)
                tool_output = outputs[i] if i < len(outputs) else None
                output_str = ""
                if tool_output:
                    output_str = str(getattr(tool_output, "output", ""))[:1000]

                span_id = str(uuid.uuid4())

                # Build tool metadata with optional category hint
                _tool_metadata: dict = merge_metadata(
                    {
                        "tool_name": tool_name,
                        "framework": "livekit_agents",
                    }
                )
                try:
                    from ...tool_category import infer_tool_category

                    category = infer_tool_category(tool_name, None)
                    if category:
                        _tool_metadata["tool_category"] = category
                except ImportError:
                    pass

                await aigie._buffer.add(
                    EventType.SPAN_CREATE,
                    {
                        "trace_id": self.trace_id,
                        "id": span_id,
                        "parent_id": self.current_turn_span_id or self.conversation_span_id,
                        "name": f"Tool: {tool_name}",
                        "type": "tool",
                        "input": str(tool_args)[:1000] if tool_args else None,
                        "output": output_str or None,
                        "metadata": merge_metadata(_tool_metadata),
                        "start_time": _utc_isoformat(),
                        "end_time": _utc_isoformat(),
                    },
                )

        except Exception as e:
            logger.debug(f"[AIGIE] Error in function_tools_executed handler: {e}")

    async def _on_user_input_transcribed(self, event: Any) -> None:
        """Track real-time user transcriptions."""
        try:
            transcript = getattr(event, "transcript", "")
            is_final = getattr(event, "is_final", False)

            if is_final and transcript:
                self._current_transcription = transcript[: self.config.max_transcription_length]

                if self.config.capture_ttfb:
                    self._stt_committed_at = _utc_now()
                    self._agent_speech_started_at = None

                # Start turn if not already in one
                if not self._in_turn:
                    aigie = self._get_aigie()
                    if aigie and aigie._initialized:
                        await self._start_turn(aigie)

        except Exception as e:
            logger.debug(f"[AIGIE] Error in user_input_transcribed handler: {e}")

    async def _on_metrics_collected(self, event: Any) -> None:
        """Process LiveKit's native metrics events.

        LiveKit emits typed metrics:
        - LLMMetrics: ttft, duration, completion_tokens, prompt_tokens
        - STTMetrics: duration, audio_duration
        - TTSMetrics: ttfb, duration, characters_count
        - EOUMetrics: end_of_utterance_delay
        - InterruptionMetrics: num_interruptions, num_backchannels
        """
        try:
            metrics = getattr(event, "metrics", None)
            if not metrics:
                return

            metrics_type = getattr(metrics, "type", None) or type(metrics).__name__

            if self._current_turn_metrics is None:
                self._current_turn_metrics = VoiceMetrics()

            if "llm" in str(metrics_type).lower():
                self._current_turn_metrics.record_llm_metrics(metrics)
                # Extract model info
                md = getattr(metrics, "metadata", None)
                if md:
                    self._llm_model = getattr(md, "model_name", None) or self._llm_model

                # Create LLM span
                aigie = self._get_aigie()
                if aigie and aigie._initialized and self.trace_id:
                    await self._create_llm_span(aigie, metrics)

            elif "stt" in str(metrics_type).lower():
                self._current_turn_metrics.record_stt_metrics(metrics)

                # Extract STT model info
                md = getattr(metrics, "metadata", None)
                if md:
                    self._stt_model = getattr(md, "model_name", None) or self._stt_model

                # Create STT span
                if self.config.trace_stt:
                    aigie = self._get_aigie()
                    if aigie and aigie._initialized and self.trace_id:
                        await self._create_stt_span(aigie, metrics)

            elif "tts" in str(metrics_type).lower():
                self._current_turn_metrics.record_tts_metrics(metrics)

                # Extract TTS model info
                md = getattr(metrics, "metadata", None)
                if md:
                    self._tts_model = getattr(md, "model_name", None) or self._tts_model

                if self.config.trace_tts:
                    aigie = self._get_aigie()
                    if aigie and aigie._initialized and self.trace_id:
                        await self._create_tts_span(aigie, metrics)

            elif "eou" in str(metrics_type).lower():
                self._current_turn_metrics.record_eou_metrics(metrics)

            elif "interruption" in str(metrics_type).lower():
                self._metrics_aggregator.record_interruption_metrics(metrics)

                if self.config.capture_interruptions:
                    num = getattr(metrics, "num_interruptions", 0) or 0
                    self._turn_interruption_count += num
                    if num > 0 and self.current_turn_span_id:
                        aigie = self._get_aigie()
                        if aigie and aigie._initialized and self.trace_id:
                            await aigie._buffer.add(
                                EventType.SPAN_UPDATE,
                                {
                                    "trace_id": self.trace_id,
                                    "id": self.current_turn_span_id,
                                    "metadata": merge_metadata(
                                        {
                                            "interrupted": True,
                                            "interruption_count": self._turn_interruption_count,
                                        }
                                    ),
                                },
                            )

        except Exception as e:
            logger.debug(f"[AIGIE] Error in metrics_collected handler: {e}")

    async def _on_error(self, event: Any) -> None:
        """Track errors from the voice pipeline."""
        try:
            error = getattr(event, "error", None)
            source = getattr(event, "source", "unknown")

            error_info = merge_metadata(
                {
                    "type": type(error).__name__ if error else "UnknownError",
                    "message": str(error)[:500] if error else "Unknown error",
                    "source": str(source),
                    "timestamp": _utc_isoformat(),
                }
            )
            self._errors.append(error_info)

            aigie = self._get_aigie()
            if aigie and aigie._initialized and self.trace_id:
                span_id = str(uuid.uuid4())
                await aigie._buffer.add(
                    EventType.SPAN_CREATE,
                    {
                        "trace_id": self.trace_id,
                        "id": span_id,
                        "parent_id": self.current_turn_span_id or self.conversation_span_id,
                        "name": f"Error: {error_info['type']}",
                        "type": "error",
                        "metadata": error_info,
                        "start_time": _utc_isoformat(),
                        "end_time": _utc_isoformat(),
                        "status": "error",
                    },
                )

        except Exception as e:
            logger.debug(f"[AIGIE] Error in error handler: {e}")

    async def _on_close(self, event: Any) -> None:
        """Handle session close — finalize trace."""
        try:
            if self._session_closed:
                return
            self._session_closed = True

            # End any open turn
            aigie = self._get_aigie()
            if not aigie or not aigie._initialized:
                return

            if self._in_turn:
                await self._end_turn(aigie)

            await self._end_conversation(aigie, event)

        except Exception as e:
            logger.debug(f"[AIGIE] Error in close handler: {e}")

    async def _on_speech_created(self, event: Any) -> None:
        """Track speech creation events for turn detection."""
        try:
            if self._current_turn_metrics:
                self._current_turn_metrics.record_bot_started_speaking()

            if self.config.capture_ttfb and self._agent_speech_started_at is None:
                self._agent_speech_started_at = _utc_now()
        except Exception as e:
            logger.debug("[AIGIE] Error in speech_created handler: %s", e)

    # ========================================================================
    # Trace Management
    # ========================================================================

    async def _start_conversation(self, aigie: Any) -> None:
        """Create the top-level trace and conversation span."""
        self.trace_id = str(uuid.uuid4())
        self.conversation_span_id = str(uuid.uuid4())

        # Extract available tools from session function context
        available_tools = []
        try:
            fnc_ctx = getattr(self._session, "fnc_ctx", None) or getattr(self, "_fnc_ctx", None)
            if fnc_ctx:
                funcs = (
                    getattr(fnc_ctx, "ai_functions", None) or getattr(fnc_ctx, "tools", None) or {}
                )
                if isinstance(funcs, dict):
                    for name, func in funcs.items():
                        tool_def = {"name": name, "type": "tool"}
                        desc = getattr(func, "description", None) or getattr(func, "__doc__", None)
                        if desc:
                            tool_def["description"] = str(desc)[:500]
                        available_tools.append(tool_def)
                elif hasattr(funcs, "__iter__"):
                    for func in funcs:
                        name = getattr(func, "name", getattr(func, "__name__", ""))
                        if name:
                            tool_def = {"name": name, "type": "tool"}
                            desc = getattr(func, "description", None)
                            if desc:
                                tool_def["description"] = str(desc)[:500]
                            available_tools.append(tool_def)
        except Exception:
            pass

        trace_metadata: dict = merge_metadata(
            {
                **self.metadata,
                "framework": "livekit_agents",
                "type": "voice_conversation",
            }
        )
        if available_tools:
            trace_metadata["available_tools"] = available_tools

        await aigie._buffer.add(
            EventType.TRACE_CREATE,
            {
                "trace_id": self.trace_id,
                "name": self.trace_name,
                "metadata": trace_metadata,
                "tags": self.tags,
                "user_id": self.user_id,
                "session_id": self.session_id,
                "start_time": _utc_isoformat(),
            },
        )

        await aigie._buffer.add(
            EventType.SPAN_CREATE,
            {
                "trace_id": self.trace_id,
                "id": self.conversation_span_id,
                "name": "Conversation",
                "type": "conversation",
                "metadata": merge_metadata(
                    {
                        "framework": "livekit_agents",
                        "llm_model": self.config.llm_model or self._llm_model,
                        "stt_model": self.config.stt_model or self._stt_model,
                        "tts_model": self.config.tts_model or self._tts_model,
                    }
                ),
                "start_time": _utc_isoformat(),
            },
        )

    async def _end_conversation(self, aigie: Any, close_event: Any) -> None:
        """Finalize the conversation trace with aggregated metrics."""
        if not self.trace_id:
            return

        reason = getattr(close_event, "reason", None)
        error = getattr(close_event, "error", None)

        agg = self._metrics_aggregator.to_dict()
        cost_summary = self._cost_tracker.get_summary()

        # Update conversation span
        await aigie._buffer.add(
            EventType.SPAN_UPDATE,
            {
                "trace_id": self.trace_id,
                "id": self.conversation_span_id,
                "end_time": _utc_isoformat(),
                "metadata": merge_metadata(
                    {
                        "close_reason": str(reason) if reason else None,
                        "has_errors": len(self._errors) > 0,
                        "error_count": len(self._errors),
                        **agg,
                        **cost_summary,
                    }
                ),
                "status": "error" if error else "ok",
            },
        )

        # Update trace
        trace_metadata = merge_metadata(
            {
                "turn_count": agg["turn_count"],
                "total_cost": cost_summary["total_cost"],
                "total_tokens": agg["total_tokens"],
                "avg_llm_ttfb_ms": agg["avg_llm_ttfb_ms"],
                "interruption_count": agg["interruption_count"],
            }
        )
        if self._session_usage:
            trace_metadata["session_usage"] = self._session_usage

        await aigie._buffer.add(
            EventType.TRACE_UPDATE,
            {
                "trace_id": self.trace_id,
                "end_time": _utc_isoformat(),
                "metadata": trace_metadata,
            },
        )

    async def _start_turn(self, aigie: Any) -> None:
        """Start a new conversation turn."""
        if not self.trace_id:
            return

        self._in_turn = True
        self._turn_count += 1
        self._current_turn_metrics = VoiceMetrics()
        self._current_transcription = ""
        self._current_bot_response = ""
        self._stt_committed_at = None
        self._agent_speech_started_at = None
        self._turn_interruption_count = 0

        self.current_turn_span_id = str(uuid.uuid4())

        await aigie._buffer.add(
            EventType.SPAN_CREATE,
            {
                "trace_id": self.trace_id,
                "id": self.current_turn_span_id,
                "parent_id": self.conversation_span_id,
                "name": f"Turn {self._turn_count}",
                "type": "turn",
                "metadata": merge_metadata({"turn_number": self._turn_count}),
                "start_time": _utc_isoformat(),
            },
        )

    async def _end_turn(self, aigie: Any) -> None:
        """End the current conversation turn and record metrics."""
        if not self.trace_id or not self.current_turn_span_id:
            return

        self._in_turn = False

        # Record turn metrics
        metrics = self._current_turn_metrics
        if metrics:
            self._metrics_aggregator.record_turn(metrics)

            # Track costs
            self._cost_tracker.add_turn(
                stt_model=self.config.stt_model or self._stt_model,
                tts_model=self.config.tts_model or self._tts_model,
                llm_model=self.config.llm_model or self._llm_model,
                audio_duration_seconds=metrics.audio_duration_seconds or 0,
                tts_characters=metrics.tts_characters,
                input_tokens=metrics.input_tokens,
                output_tokens=metrics.output_tokens,
            )

        ttfb_ms: float | None = None
        if (
            self.config.capture_ttfb
            and self._stt_committed_at is not None
            and self._agent_speech_started_at is not None
        ):
            ttfb_ms = (
                self._agent_speech_started_at - self._stt_committed_at
            ).total_seconds() * 1000

        extra_metadata: dict = {}
        if self.config.capture_ttfb and ttfb_ms is not None:
            extra_metadata["ttfb_ms"] = ttfb_ms
        if self.config.capture_interruptions and self._turn_interruption_count > 0:
            extra_metadata["interrupted"] = True
            extra_metadata["interruption_count"] = self._turn_interruption_count

        turn_data = {
            "trace_id": self.trace_id,
            "id": self.current_turn_span_id,
            "end_time": _utc_isoformat(),
            "input": self._current_transcription if self.config.capture_transcriptions else None,
            "output": self._current_bot_response if self.config.capture_bot_responses else None,
            "metadata": merge_metadata(
                {
                    "turn_number": self._turn_count,
                    **(metrics.to_dict() if metrics else {}),
                    **extra_metadata,
                }
            ),
        }

        await aigie._buffer.add(EventType.SPAN_UPDATE, turn_data)

        self.current_turn_span_id = None
        self._current_turn_metrics = None

    async def _create_llm_span(self, aigie: Any, metrics: Any) -> None:
        """Create an LLM span from LLMMetrics."""
        span_id = str(uuid.uuid4())
        ttft = getattr(metrics, "ttft", None)
        duration = getattr(metrics, "duration", None)
        prompt_tokens = getattr(metrics, "prompt_tokens", 0) or 0
        completion_tokens = getattr(metrics, "completion_tokens", 0) or 0
        tps = getattr(metrics, "tokens_per_second", None)

        md = getattr(metrics, "metadata", None)
        model_name = getattr(md, "model_name", None) if md else self._llm_model
        provider = getattr(md, "model_provider", None) if md else None

        cost_usd: float | None = None
        if self.config.use_cost_tracking:
            from .cost_tracking import calculate_llm_cost

            cost_usd = calculate_llm_cost(model_name, prompt_tokens, completion_tokens)

        await aigie._buffer.add(
            EventType.SPAN_CREATE,
            {
                "trace_id": self.trace_id,
                "id": span_id,
                "parent_id": self.current_turn_span_id or self.conversation_span_id,
                "name": f"LLM: {model_name or 'unknown'}",
                "type": "llm",
                "metadata": merge_metadata(
                    {
                        "model": model_name,
                        "provider": provider,
                        "framework": "livekit_agents",
                        "ttft_ms": ttft * 1000 if ttft else None,
                        "duration_ms": duration * 1000 if duration else None,
                        "input_tokens": prompt_tokens,
                        "output_tokens": completion_tokens,
                        "tokens_per_second": tps,
                        "cost_usd": cost_usd,
                    }
                ),
                "usage": {
                    "input_tokens": prompt_tokens,
                    "output_tokens": completion_tokens,
                    "total_tokens": prompt_tokens + completion_tokens,
                },
                "start_time": _utc_isoformat(),
                "end_time": _utc_isoformat(),
            },
        )

    async def _create_stt_span(self, aigie: Any, metrics: Any) -> None:
        """Create an STT span from STTMetrics."""
        span_id = str(uuid.uuid4())
        duration = getattr(metrics, "duration", None)
        audio_duration = getattr(metrics, "audio_duration", None)

        md = getattr(metrics, "metadata", None)
        model_name = getattr(md, "model_name", None) if md else self._stt_model

        transcript = self._current_transcription or None

        await aigie._buffer.add(
            EventType.SPAN_CREATE,
            {
                "trace_id": self.trace_id,
                "id": span_id,
                "parent_id": self.current_turn_span_id or self.conversation_span_id,
                "name": "stt",
                "type": "stt",
                "input": None,
                "output": transcript,
                "metadata": merge_metadata(
                    {
                        "model": model_name,
                        "framework": "livekit_agents",
                        "stt.transcript": transcript,
                        "stt.duration_ms": duration * 1000 if duration else None,
                        "stt.audio_duration_ms": audio_duration * 1000 if audio_duration else None,
                    }
                ),
                "start_time": _utc_isoformat(),
                "end_time": _utc_isoformat(),
            },
        )

    async def _create_tts_span(self, aigie: Any, metrics: Any) -> None:
        """Create a TTS span from TTSMetrics."""
        span_id = str(uuid.uuid4())
        ttfb = getattr(metrics, "ttfb", None)
        duration = getattr(metrics, "duration", None)
        characters_count = getattr(metrics, "characters_count", None)

        md = getattr(metrics, "metadata", None)
        model_name = getattr(md, "model_name", None) if md else self._tts_model

        text = self._current_bot_response or None

        await aigie._buffer.add(
            EventType.SPAN_CREATE,
            {
                "trace_id": self.trace_id,
                "id": span_id,
                "parent_id": self.current_turn_span_id or self.conversation_span_id,
                "name": "tts",
                "type": "tts",
                "input": text,
                "metadata": merge_metadata(
                    {
                        "model": model_name,
                        "framework": "livekit_agents",
                        "tts.text": text,
                        "tts.char_count": characters_count,
                        "tts.ttfb_ms": ttfb * 1000 if ttfb else None,
                        "tts.duration_ms": duration * 1000 if duration else None,
                    }
                ),
                "start_time": _utc_isoformat(),
                "end_time": _utc_isoformat(),
            },
        )

    # ========================================================================
    # Public API
    # ========================================================================

    def get_metrics(self) -> dict[str, Any]:
        """Get aggregated conversation metrics."""
        return self._metrics_aggregator.to_dict()

    def get_costs(self) -> dict[str, Any]:
        """Get cost tracking summary."""
        return self._cost_tracker.get_summary()

    def get_errors(self) -> list[dict[str, Any]]:
        """Get list of errors encountered during the session."""
        return list(self._errors)
