import logging
import contextvars
from typing import Dict, Generator
from unittest.mock import Mock, MagicMock, patch

import pytest
from pytest import MonkeyPatch, LogCaptureFixture

from scale_gp_beta.lib.tracing.span import NoOpSpan
from scale_gp_beta.lib.tracing.trace import Trace, BaseTrace, NoOpTrace
from scale_gp_beta.lib.tracing.trace_queue_manager import TraceQueueManager


@pytest.fixture
def mock_queue_manager() -> Mock:
    manager = Mock(spec=TraceQueueManager)
    manager.report_trace_start = Mock()
    manager.report_trace_end = Mock()
    return manager


@pytest.fixture
def mock_scope_set_current_trace() -> Generator[MagicMock, None, None]:
    mock_token = Mock(spec=contextvars.Token)
    with patch("scale_gp_beta.lib.tracing.trace.Scope.set_current_trace", return_value=mock_token) as mock_set:
        yield mock_set

@pytest.fixture
def mock_scope_set_current_span() -> Generator[MagicMock, None, None]:
    mock_token = Mock(spec=contextvars.Token)
    with patch("scale_gp_beta.lib.tracing.span.Scope.set_current_span", return_value=mock_token) as mock_set:
        yield mock_set


@pytest.fixture
def mock_scope_reset_current_trace() -> Generator[MagicMock, None, None]:
    with patch("scale_gp_beta.lib.tracing.trace.Scope.reset_current_trace") as mock_reset:
        yield mock_reset


@pytest.fixture
def mock_scope_reset_current_span() -> Generator[MagicMock, None, None]:
    with patch("scale_gp_beta.lib.tracing.span.Scope.reset_current_span") as mock_reset:
        yield mock_reset


@pytest.fixture
def patched_trace_utils(monkeypatch: MonkeyPatch) -> Dict[str, Mock]:
    """Mocks utility functions for predictable values related to traces."""
    mock_gen_trace_id = Mock(return_value="test-trace-id")
    monkeypatch.setattr("scale_gp_beta.lib.tracing.trace.generate_trace_id", mock_gen_trace_id)
    return {"generate_trace_id": mock_gen_trace_id}


class TestBaseTrace:
    def test_initialization_defaults(self, mock_queue_manager: Mock) -> None:
        trace = BaseTrace(queue_manager=mock_queue_manager, trace_id="test-trace-id", root_span=NoOpSpan("test-root"))
        assert trace.trace_id == "test-trace-id"
        assert trace.queue_manager == mock_queue_manager
        assert trace._in_progress is False
        assert trace._contextvar_token is None

    def test_initialization_with_custom_trace_id(self, mock_queue_manager: Mock) -> None:
        custom_id = "my-custom-trace-id"
        trace = BaseTrace(queue_manager=mock_queue_manager, trace_id=custom_id, root_span=NoOpSpan("test-root"))
        assert trace.trace_id == custom_id
        assert trace.queue_manager == mock_queue_manager

    def test_context_manager_calls_start_end(self, mock_queue_manager: Mock) -> None:
        trace = BaseTrace(queue_manager=mock_queue_manager, trace_id="test-trace", root_span=NoOpSpan("test-root"))
        trace.start = Mock()
        trace.end = Mock()

        with trace as t:
            assert t == trace
            trace.start.assert_called_once()
            trace.end.assert_not_called()
        trace.end.assert_called_once()

    def test_context_manager_propagates_exception(self, mock_queue_manager: Mock) -> None:
        trace = BaseTrace(queue_manager=mock_queue_manager, trace_id="test-trace", root_span=NoOpSpan("test-root"))
        trace.end = Mock()

        with pytest.raises(ValueError, match="Test error in trace"):
            with trace:
                raise ValueError("Test error in trace")
        trace.end.assert_called_once()


class TestNoOpTrace:
    def test_initialization(self, patched_trace_utils: Dict[str, Mock]) -> None:
        trace = NoOpTrace(trace_id="noop-trace", name="noop-trace-name")
        assert trace.trace_id == "noop-trace"
        assert trace.queue_manager is None
        assert trace._in_progress is False
        assert trace._contextvar_token is None

        assert trace.root_span.name == "noop-trace-name"
        assert trace.root_span._contextvar_token is None
        patched_trace_utils["generate_trace_id"].assert_not_called()


    def test_initialization_default_id(self, patched_trace_utils: Dict[str, Mock]) -> None:
        trace = NoOpTrace(name="noop-trace-name")
        assert trace.trace_id == "test-trace-id"
        patched_trace_utils["generate_trace_id"].assert_called_once()


class TestTrace:
    def test_initialization(self, mock_queue_manager: Mock, patched_trace_utils: Dict[str, Mock]) -> None:
        trace = Trace(queue_manager=mock_queue_manager, trace_id="op-trace-id", name="op-trace-name", span_id="root-span-id")
        assert trace.trace_id == "op-trace-id"
        assert trace.queue_manager == mock_queue_manager
        assert trace.root_span.name == "op-trace-name"
        assert trace.root_span.span_id == "root-span-id"
        patched_trace_utils["generate_trace_id"].assert_not_called()

    def test_start(
        self,
        mock_queue_manager: Mock,
        mock_scope_set_current_trace: MagicMock,
        mock_scope_set_current_span: MagicMock,
        mock_scope_reset_current_trace: MagicMock, # noqa: ARG002
        patched_trace_utils: Dict[str, Mock] # noqa: ARG002
    ) -> None:
        trace = Trace(queue_manager=mock_queue_manager, trace_id="start-test-trace", name="start-test-trace", span_id="root-span-id")
        trace.start()

        assert trace._in_progress is True
        mock_queue_manager.report_trace_start.assert_called_once_with(trace)
        mock_scope_set_current_trace.assert_called_once_with(trace)
        assert trace._contextvar_token == mock_scope_set_current_trace.return_value
        mock_scope_set_current_span.assert_called_once_with(trace.root_span)
        assert trace.root_span._contextvar_token == mock_scope_set_current_span.return_value

    def test_start_idempotency(
        self,
        mock_queue_manager: Mock,
        mock_scope_set_current_trace: MagicMock,
        mock_scope_set_current_span: MagicMock,
        caplog: LogCaptureFixture,
        patched_trace_utils: Dict[str, Mock] # noqa: ARG002
    ) -> None:
        trace = Trace(queue_manager=mock_queue_manager, trace_id="idem-start-trace", name="idem-start-trace", span_id="root-span-id")
        trace.start()

        mock_queue_manager.reset_mock()
        mock_scope_set_current_trace.reset_mock()
        mock_scope_set_current_span.reset_mock()

        with caplog.at_level(logging.WARNING):
            trace.start()

        assert f"Trace already started: {trace.trace_id}" in caplog.text
        mock_queue_manager.report_trace_start.assert_not_called()
        mock_scope_set_current_trace.assert_not_called()
        mock_scope_set_current_span.assert_not_called()

    def test_end_normal_flow(
        self,
        mock_queue_manager: Mock,
        mock_scope_set_current_trace: MagicMock,
        mock_scope_set_current_span: MagicMock,
        mock_scope_reset_current_trace: MagicMock,
        mock_scope_reset_current_span: MagicMock,
        patched_trace_utils: Dict[str, Mock] # noqa: ARG002
    ) -> None:
        trace = Trace(queue_manager=mock_queue_manager, trace_id="end-test-trace", name="end-test-trace", span_id="root-span-id")
        trace.start()

        expected_token = mock_scope_set_current_trace.return_value
        expected_span_token = mock_scope_set_current_span.return_value
        assert trace._contextvar_token == expected_token
        assert trace._in_progress is True
        assert trace.root_span._contextvar_token == expected_span_token

        trace.end()

        assert trace._in_progress is False
        mock_queue_manager.report_trace_end.assert_called_once_with(trace)
        mock_queue_manager.report_span_end.assert_called_once_with(trace.root_span)
        mock_scope_reset_current_trace.assert_called_once_with(expected_token)
        mock_scope_reset_current_span.assert_called_once_with(expected_span_token)
        assert trace._contextvar_token is None
        assert trace.root_span._contextvar_token is None

    def test_end_when_not_in_progress(
        self,
        mock_queue_manager: Mock,
        mock_scope_reset_current_trace: MagicMock,
        mock_scope_reset_current_span: MagicMock,
        caplog: LogCaptureFixture,
        patched_trace_utils: Dict[str, Mock] # noqa: ARG002
    ) -> None:
        trace = Trace(queue_manager=mock_queue_manager, trace_id="not-active-trace", name="not-active-trace", span_id="root-span-id")

        with caplog.at_level(logging.WARNING):
            trace.end()

        assert f"Ending trace which is not active: {trace.trace_id}" in caplog.text
        mock_queue_manager.report_trace_end.assert_not_called()
        mock_queue_manager.report_span_end.assert_not_called()
        mock_scope_reset_current_trace.assert_not_called()
        mock_scope_reset_current_span.assert_not_called()

    def test_end_when_token_is_none(
        self,
        mock_queue_manager: Mock,
        mock_scope_reset_current_trace: MagicMock,
        mock_scope_reset_current_span: MagicMock,
        caplog: LogCaptureFixture,
        patched_trace_utils: Dict[str, Mock] # noqa: ARG002
    ) -> None:
        trace = Trace(queue_manager=mock_queue_manager, trace_id="no-token-trace", name="no-token-trace", span_id="root-span-id")
        trace._in_progress = True
        trace._contextvar_token = None

        with caplog.at_level(logging.WARNING):
            trace.end()

        assert f"Ending trace which is not active: {trace.trace_id}, contextvar_token not set" in caplog.text
        mock_queue_manager.report_trace_end.assert_not_called()
        mock_queue_manager.report_span_end.assert_not_called()
        mock_scope_reset_current_trace.assert_not_called()
        mock_scope_reset_current_span.assert_not_called()

    def test_context_manager_operational_trace(
        self,
        mock_queue_manager: Mock,
        mock_scope_set_current_trace: MagicMock,
        mock_scope_set_current_span: MagicMock,
        mock_scope_reset_current_trace: MagicMock,
        mock_scope_reset_current_span: MagicMock,
        patched_trace_utils: Dict[str, Mock] # noqa: ARG002
    ) -> None:
        trace = Trace(queue_manager=mock_queue_manager, trace_id="ctx-op-trace", name="ctx-op-trace", span_id="root-span-id")
        expected_token = mock_scope_set_current_trace.return_value
        expected_span_token = mock_scope_set_current_span.return_value

        with trace as t:
            assert t == trace
            assert trace._in_progress is True
            mock_queue_manager.report_trace_start.assert_called_once_with(trace)
            mock_queue_manager.report_span_start.assert_called_once_with(trace.root_span)
            mock_scope_set_current_trace.assert_called_once_with(trace)
            mock_scope_set_current_span.assert_called_once_with(trace.root_span)
            assert trace._contextvar_token == expected_token
            assert trace.root_span._contextvar_token == expected_span_token

        assert trace._in_progress is False
        assert trace.root_span._contextvar_token is None
        mock_queue_manager.report_trace_end.assert_called_once_with(trace)
        mock_queue_manager.report_span_end.assert_called_once_with(trace.root_span)
        mock_scope_reset_current_trace.assert_called_once_with(expected_token)
        mock_scope_reset_current_span.assert_called_once_with(expected_span_token)
        assert trace._contextvar_token is None

    def test_updating_trace_status(
            self,
            mock_queue_manager: Mock,
            patched_trace_utils: Dict[str, Mock] # noqa: ARG002
    ) -> None:
        trace = Trace(queue_manager=mock_queue_manager, name="request_123")
        with pytest.raises(AttributeError):
            trace.status = "ERROR"  # type: ignore[attr-defined]
        assert trace.root_span.status == "SUCCESS"


    def test_setting_trace_metadata(
            self,
            mock_queue_manager: Mock,
            patched_trace_utils: Dict[str, Mock] # noqa: ARG002
    ) -> None:
        trace = Trace(queue_manager=mock_queue_manager, name="request_123")
        trace.metadata = {"foo": "bar"}
        trace.metadata["other"] = "baz"
        assert trace.root_span.metadata == {"foo": "bar", "other": "baz"}

    def test_setting_trace_input(
            self,
            mock_queue_manager: Mock,
            patched_trace_utils: Dict[str, Mock]  # noqa: ARG002
    ) -> None:
        trace = Trace(queue_manager=mock_queue_manager, name="request_123")
        trace.input = {"foo": "bar"}
        assert trace.root_span.input == {"foo": "bar"}

    def test_setting_trace_output(
            self,
            mock_queue_manager: Mock,
            patched_trace_utils: Dict[str, Mock]  # noqa: ARG002
    ) -> None:
        trace = Trace(queue_manager=mock_queue_manager, name="request_123")
        trace.output = {"foo": "bar"}
        assert trace.root_span.output == {"foo": "bar"}

    def test_set_error(self, mock_queue_manager: Mock) -> None:
        trace = Trace(queue_manager=mock_queue_manager, name="request_123")
        e = AttributeError("this is a test")
        assert trace.metadata == {}
        trace.set_error(exception=e)

        assert trace.metadata == {"error": True, "error_message": "this is a test", "error_type": "AttributeError"}
