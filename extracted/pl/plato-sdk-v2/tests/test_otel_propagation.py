"""Tests for cross-world OTel trace context propagation.

Validates that:
1. get_current_trace_context() captures the current span's context
2. BaseWorld._setup_session() reads parent trace context from multiple sources
3. init_tracing() links child spans to parent via NonRecordingSpan
4. SessionConfig accepts parent_trace_id / parent_span_id
5. No duplicate spans are created (NonRecordingSpan doesn't record)
"""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, SpanExporter, SpanExportResult


class InMemorySpanExporter(SpanExporter):
    """Simple in-memory exporter for testing (compatible with all OTel SDK versions)."""

    def __init__(self):
        self._spans = []

    def export(self, spans):
        self._spans.extend(spans)
        return SpanExportResult.SUCCESS

    def shutdown(self):
        pass

    def get_finished_spans(self):
        return list(self._spans)

    def clear(self):
        self._spans.clear()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _reset_otel_state():
    """Reset OTel global state before each test.

    The global TracerProvider must also be reset, otherwise
    ``trace.set_tracer_provider()`` silently refuses the new provider.
    """
    import plato.otel as otel_mod

    otel_mod._initialized = False
    otel_mod._tracer_provider = None
    otel_mod._log_handler = None

    # Reset the global OTel TracerProvider so tests can set their own
    trace._TRACER_PROVIDER = None
    trace._TRACER_PROVIDER_SET_ONCE._done = False

    yield

    otel_mod._initialized = False
    otel_mod._tracer_provider = None
    otel_mod._log_handler = None
    trace._TRACER_PROVIDER = None
    trace._TRACER_PROVIDER_SET_ONCE._done = False


@pytest.fixture
def in_memory_exporter():
    """Set up an in-memory span exporter for inspection."""
    exporter = InMemorySpanExporter()
    provider = TracerProvider(resource=Resource.create({"service.name": "test"}))
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    yield exporter
    provider.shutdown()


# ---------------------------------------------------------------------------
# get_current_trace_context()
# ---------------------------------------------------------------------------


class TestGetCurrentTraceContext:
    """Tests for otel.get_current_trace_context()."""

    def test_returns_empty_dict_when_no_active_span(self):
        from plato.otel import get_current_trace_context

        # With a no-op provider, there's no valid span
        trace.set_tracer_provider(TracerProvider())
        ctx = get_current_trace_context()
        assert ctx == {}

    def test_captures_active_span_context(self, in_memory_exporter):
        from plato.otel import get_current_trace_context

        tracer = trace.get_tracer("test")
        with tracer.start_as_current_span("parent-op") as span:
            ctx = get_current_trace_context()

            span_context = span.get_span_context()
            expected_trace_id = format(span_context.trace_id, "032x")
            expected_span_id = format(span_context.span_id, "016x")

            assert ctx["parent_trace_id"] == expected_trace_id
            assert ctx["parent_span_id"] == expected_span_id

    def test_returns_hex_strings_of_correct_length(self, in_memory_exporter):
        from plato.otel import get_current_trace_context

        tracer = trace.get_tracer("test")
        with tracer.start_as_current_span("op"):
            ctx = get_current_trace_context()
            assert len(ctx["parent_trace_id"]) == 32  # 128-bit trace ID
            assert len(ctx["parent_span_id"]) == 16  # 64-bit span ID


class TestSessionSpanOverride:
    def test_session_span_uses_env_override_for_agent_name(self, in_memory_exporter):
        from plato.otel import session_span

        tracer = trace.get_tracer("test")
        with patch.dict(os.environ, {"PLATO_AGENT_DISPLAY_NAME": "backend-builder"}):
            with session_span(tracer, "claude-code", "1.2.3"):
                pass

        spans = [span for span in in_memory_exporter.get_finished_spans() if span.name == "session"]
        assert len(spans) == 1
        attrs = spans[0].attributes
        assert attrs["atif.agent.name"] == "backend-builder"
        assert attrs["plato.agent.impl_name"] == "claude-code"
        assert attrs["plato.agent.display_name"] == "backend-builder"


# ---------------------------------------------------------------------------
# init_tracing() with parent context
# ---------------------------------------------------------------------------


class TestInitTracingParentContext:
    """Tests for init_tracing() parent context linking."""

    def test_init_without_parent_creates_independent_trace(self):
        """Without parent IDs, spans get their own trace ID."""
        from plato.otel import init_tracing

        exporter = InMemorySpanExporter()
        with patch("plato.otel.OTLPSpanExporter", return_value=exporter):
            init_tracing(
                service_name="child-world",
                session_id="session-123",
                otlp_endpoint="http://localhost:4318",
            )

        tracer = trace.get_tracer("child-world")
        with tracer.start_as_current_span("child-op") as span:
            # Should have its own trace ID (not linked to any parent)
            assert span.get_span_context().is_valid

    def test_init_with_parent_links_to_parent_trace(self):
        """With parent IDs, child spans share the parent's trace ID."""
        from plato.otel import init_tracing

        parent_trace_id = "0" * 31 + "1"  # 00000000000000000000000000000001
        parent_span_id = "0" * 15 + "2"  # 0000000000000002

        exporter = InMemorySpanExporter()
        with patch("plato.otel.OTLPSpanExporter", return_value=exporter):
            init_tracing(
                service_name="child-world",
                session_id="session-456",
                otlp_endpoint="http://localhost:4318",
                parent_trace_id=parent_trace_id,
                parent_span_id=parent_span_id,
            )

        tracer = trace.get_tracer("child-world")
        with tracer.start_as_current_span("child-op") as span:
            # Child span should share the parent's trace ID
            child_trace_id = format(span.get_span_context().trace_id, "032x")
            assert child_trace_id == parent_trace_id

    def test_parent_context_uses_non_recording_span(self):
        """Parent context should use NonRecordingSpan (no duplicate spans)."""
        from plato.otel import init_tracing

        parent_trace_id = "a" * 32
        parent_span_id = "b" * 16

        exporter = InMemorySpanExporter()
        with patch("plato.otel.OTLPSpanExporter", return_value=exporter):
            init_tracing(
                service_name="child-world",
                session_id="session-789",
                otlp_endpoint="http://localhost:4318",
                parent_trace_id=parent_trace_id,
                parent_span_id=parent_span_id,
            )

        # Create a child span
        tracer = trace.get_tracer("child-world")
        with tracer.start_as_current_span("child-op"):
            pass

        # Only the child span should be exported (not the NonRecordingSpan parent)
        spans = exporter.get_finished_spans()
        assert len(spans) == 1
        assert spans[0].name == "child-op"


# ---------------------------------------------------------------------------
# SessionConfig
# ---------------------------------------------------------------------------


class TestSessionConfig:
    """Tests for SessionConfig parent trace fields."""

    def test_session_config_accepts_parent_trace_fields(self):
        from plato.worlds.config import SessionConfig

        config = SessionConfig(
            session_id="s1",
            otel_url="http://localhost:4318",
            parent_trace_id="a" * 32,
            parent_span_id="b" * 16,
        )
        assert config.parent_trace_id == "a" * 32
        assert config.parent_span_id == "b" * 16

    def test_session_config_defaults_to_none(self):
        from plato.worlds.config import SessionConfig

        config = SessionConfig(session_id="s1")
        assert config.parent_trace_id is None
        assert config.parent_span_id is None


# ---------------------------------------------------------------------------
# BaseWorld._setup_session() integration
# ---------------------------------------------------------------------------


class TestSetupSessionPropagation:
    """Tests for BaseWorld._setup_session() reading parent trace context."""

    def _make_world(self):
        """Create a minimal BaseWorld instance for testing."""
        from plato.worlds.base import BaseWorld
        from plato.worlds.config import RunConfig
        from plato.worlds.models import Observation, StepResult

        class TestWorld(BaseWorld[RunConfig]):
            name = "otel-test"

            async def reset(self) -> Observation:
                return Observation()

            async def step(self) -> StepResult:
                return StepResult(observation=Observation(), done=True)

        world = TestWorld()
        return world

    def test_reads_parent_from_session_config(self):
        """Parent trace context from SessionConfig is passed to init_tracing."""
        from plato.worlds.config import RunConfig, SessionConfig

        world = self._make_world()
        world.config = RunConfig()
        world.session = SessionConfig(
            session_id="child-session",
            otel_url="http://localhost:4318",
            parent_trace_id="a" * 32,
            parent_span_id="b" * 16,
        )

        with patch("plato.worlds.base.init_tracing") as mock_init:
            world._setup_session()

        mock_init.assert_called_once_with(
            service_name="world-otel-test",
            session_id="child-session",
            otlp_endpoint="http://localhost:4318",
            parent_trace_id="a" * 32,
            parent_span_id="b" * 16,
        )

    def test_reads_parent_from_config_extra_fields(self):
        """Parent trace context from config extra fields (world_config)."""
        from plato.worlds.config import RunConfig, SessionConfig

        world = self._make_world()
        world.config = RunConfig(
            parent_trace_id="c" * 32,
            parent_span_id="d" * 16,
        )
        world.session = SessionConfig(
            session_id="child-session",
            otel_url="http://localhost:4318",
        )

        with patch("plato.worlds.base.init_tracing") as mock_init:
            world._setup_session()

        mock_init.assert_called_once_with(
            service_name="world-otel-test",
            session_id="child-session",
            otlp_endpoint="http://localhost:4318",
            parent_trace_id="c" * 32,
            parent_span_id="d" * 16,
        )

    def test_reads_parent_from_env_vars(self):
        """Parent trace context from environment variables (fallback)."""
        from plato.worlds.config import RunConfig, SessionConfig

        world = self._make_world()
        world.config = RunConfig()
        world.session = SessionConfig(
            session_id="child-session",
            otel_url="http://localhost:4318",
        )

        env_patch = {
            "OTEL_TRACE_ID": "e" * 32,
            "OTEL_PARENT_SPAN_ID": "f" * 16,
        }
        with patch("plato.worlds.base.init_tracing") as mock_init, patch.dict(os.environ, env_patch):
            world._setup_session()

        mock_init.assert_called_once_with(
            service_name="world-otel-test",
            session_id="child-session",
            otlp_endpoint="http://localhost:4318",
            parent_trace_id="e" * 32,
            parent_span_id="f" * 16,
        )

    def test_session_config_takes_priority_over_config_extras(self):
        """SessionConfig fields take priority over config extras."""
        from plato.worlds.config import RunConfig, SessionConfig

        world = self._make_world()
        world.config = RunConfig(
            parent_trace_id="from_config" + "0" * 22,
            parent_span_id="from_config" + "0" * 5,
        )
        world.session = SessionConfig(
            session_id="child-session",
            otel_url="http://localhost:4318",
            parent_trace_id="from_session" + "0" * 20,
            parent_span_id="from_session" + "0" * 4,
        )

        with patch("plato.worlds.base.init_tracing") as mock_init:
            world._setup_session()

        call_kwargs = mock_init.call_args[1]
        assert call_kwargs["parent_trace_id"] == "from_session" + "0" * 20
        assert call_kwargs["parent_span_id"] == "from_session" + "0" * 4

    def test_no_parent_context_when_none_available(self):
        """When no parent context is available, None is passed."""
        from plato.worlds.config import RunConfig, SessionConfig

        world = self._make_world()
        world.config = RunConfig()
        world.session = SessionConfig(
            session_id="child-session",
            otel_url="http://localhost:4318",
        )

        env_clean = {"OTEL_TRACE_ID": "", "OTEL_PARENT_SPAN_ID": ""}
        with patch("plato.worlds.base.init_tracing") as mock_init, patch.dict(os.environ, env_clean, clear=False):
            # Remove the env vars entirely
            os.environ.pop("OTEL_TRACE_ID", None)
            os.environ.pop("OTEL_PARENT_SPAN_ID", None)
            world._setup_session()

        call_kwargs = mock_init.call_args[1]
        assert call_kwargs["parent_trace_id"] is None
        assert call_kwargs["parent_span_id"] is None

    def test_no_setup_without_session_id(self):
        """_setup_session should be a no-op without a session_id."""
        from plato.worlds.config import RunConfig, SessionConfig

        world = self._make_world()
        world.config = RunConfig()
        world.session = SessionConfig()  # empty session_id

        with patch("plato.worlds.base.init_tracing") as mock_init:
            world._setup_session()

        mock_init.assert_not_called()


# ---------------------------------------------------------------------------
# End-to-end: parent -> child trace linking
# ---------------------------------------------------------------------------


class TestEndToEndTraceLinking:
    """End-to-end test: parent span -> get_current_trace_context -> init_tracing -> child span."""

    def test_child_spans_appear_under_parent_trace(self):
        """Full flow: capture parent context, init child, verify trace ID matches.

        Simulates what happens across two separate processes (parent world and
        child world).  Since we're in a single process, we must reset the
        global TracerProvider between the parent and child phases.
        """
        import plato.otel as otel_mod
        from plato.otel import get_current_trace_context, init_tracing

        # --- Parent world (process 1) ---
        parent_exporter = InMemorySpanExporter()
        parent_provider = TracerProvider(resource=Resource.create({"service.name": "parent-world"}))
        parent_provider.add_span_processor(SimpleSpanProcessor(parent_exporter))
        trace.set_tracer_provider(parent_provider)

        parent_tracer = trace.get_tracer("parent-world")
        with parent_tracer.start_as_current_span("launch_child") as parent_span:
            parent_trace_id = format(parent_span.get_span_context().trace_id, "032x")

            # Capture context (this is what the parent world would do)
            ctx = get_current_trace_context()
            assert ctx["parent_trace_id"] == parent_trace_id

        parent_provider.shutdown()

        # Reset global state (simulates being in a new process)
        trace._TRACER_PROVIDER = None
        trace._TRACER_PROVIDER_SET_ONCE._done = False
        otel_mod._initialized = False
        otel_mod._tracer_provider = None
        otel_mod._log_handler = None

        # --- Child world (process 2) ---
        child_exporter = InMemorySpanExporter()
        with patch("plato.otel.OTLPSpanExporter", return_value=child_exporter):
            init_tracing(
                service_name="child-world",
                session_id="child-session",
                otlp_endpoint="http://localhost:4318",
                parent_trace_id=ctx["parent_trace_id"],
                parent_span_id=ctx["parent_span_id"],
            )

        child_tracer = trace.get_tracer("child-world")
        with child_tracer.start_as_current_span("child-operation") as child_span:
            child_trace_id = format(child_span.get_span_context().trace_id, "032x")
            # Child span must share the parent's trace ID
            assert child_trace_id == parent_trace_id

        # Verify only child spans are exported (not the NonRecordingSpan)
        child_spans = child_exporter.get_finished_spans()
        assert len(child_spans) == 1
        assert child_spans[0].name == "child-operation"

        # Verify the child span's parent is the parent span
        child_parent_span_id = format(child_spans[0].parent.span_id, "016x")
        assert child_parent_span_id == ctx["parent_span_id"]
