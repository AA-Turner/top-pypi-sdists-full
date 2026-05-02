import logging
import contextvars
from typing import Dict
from unittest.mock import Mock, MagicMock, patch
from typing_extensions import Generator

import pytest

from scale_gp_beta.lib.tracing.span import Span, BaseSpan, NoOpSpan
from scale_gp_beta.lib.tracing.trace_queue_manager import TraceQueueManager


@pytest.fixture
def mock_queue_manager() -> Mock:
    manager = Mock(spec=TraceQueueManager)
    manager.report_span_start = Mock()
    manager.report_span_end = Mock()
    return manager


@pytest.fixture
def mock_scope_set_current_span() -> Generator[MagicMock, None, None]:
    mock_token = Mock(spec=contextvars.Token)
    with patch("scale_gp_beta.lib.tracing.span.Scope.set_current_span", return_value=mock_token) as mock_set:
        yield mock_set


@pytest.fixture
def mock_scope_reset_current_span() -> Generator[MagicMock, None, None]:
    with patch("scale_gp_beta.lib.tracing.span.Scope.reset_current_span") as mock_reset:
        yield mock_reset


@pytest.fixture
def patched_utils(monkeypatch: pytest.MonkeyPatch) -> Dict[str, Mock]:  # type: ignore
    mock_gen_id = Mock(return_value="test-span-id")
    mock_iso = Mock(side_effect=["start-ts", "end-ts", "next-start-ts", "next-end-ts", "another-ts", "yet-another-ts"])

    monkeypatch.setattr("scale_gp_beta.lib.tracing.span.generate_span_id", mock_gen_id)  # type: ignore
    monkeypatch.setattr("scale_gp_beta.lib.tracing.span.iso_timestamp", mock_iso)  # type: ignore

    return {"iso_timestamp": mock_iso, "generate_span_id": mock_gen_id}


class TestBaseSpan:
    def test_initialization_defaults(self, mock_queue_manager: Mock, patched_utils: Dict[str, Mock]):
        span = BaseSpan(name="base_test", trace_id="trace1", queue_manager=mock_queue_manager)
        assert span.name == "base_test"
        assert span.trace_id == "trace1"
        assert span.span_id == "test-span-id"
        assert span.parent_span_id is None
        assert span.start_time is None
        assert span.end_time is None
        assert isinstance(span.input, dict) and len(span.input) == 0
        assert isinstance(span.output, dict) and len(span.output) == 0
        assert isinstance(span.metadata, dict) and len(span.metadata) == 0
        assert span._queue_manager == mock_queue_manager
        assert span._contextvar_token is None
        assert span.status == "SUCCESS"
        patched_utils["generate_span_id"].assert_called_once()

    def test_context_manager_calls_start_end(self, mock_queue_manager: Mock):
        span = BaseSpan(name="ctx_test", trace_id="trace_ctx", queue_manager=mock_queue_manager)
        span.start = Mock()
        span.end = Mock()

        with span as s:
            assert s == span
            span.start.assert_called_once()
            span.end.assert_not_called()
        span.end.assert_called_once()

    def test_context_manager_exception_handling(self, mock_queue_manager: Mock, patched_utils: Dict[str, Mock]):
        span = BaseSpan(name="exc_test", trace_id="trace_exc", queue_manager=mock_queue_manager)

        with pytest.raises(ValueError, match="Test error"):
            with span:
                span.start_time = patched_utils["iso_timestamp"]()
                raise ValueError("Test error")

        span.end_time = patched_utils["iso_timestamp"]()

        assert span.metadata is not None
        assert span.metadata["error"] is True
        assert span.metadata["error_type"] == "ValueError"
        assert span.metadata["error_message"] == "Test error"
        assert span.start_time == "start-ts"
        assert span.end_time == "end-ts"
        assert span.status == "ERROR"

    def test_to_request_params_basic(
            self, mock_queue_manager: Mock, patched_utils: Dict[str, Mock] # noqa: ARG002
    ):
        span = BaseSpan(name="req_test", trace_id="trace_req", queue_manager=mock_queue_manager)
        span.start_time = "start-ts-manual"
        span.end_time = "end-ts-manual"
        span.input = {"in_key": "in_val"}
        span.output = {"out_key": "out_val"}
        span.metadata = {"meta_key": "meta_val"}

        params = span.to_request_params()

        assert params.get("name") == "req_test"
        assert params.get("id") == "test-span-id"
        assert params.get("trace_id") == "trace_req"
        assert params.get("parent_id") is None
        assert params.get("start_timestamp") == "start-ts-manual"
        assert params.get("end_timestamp") == "end-ts-manual"
        assert params.get("input") == {"in_key": "in_val"}
        assert params.get("output") == {"out_key": "out_val"}
        assert params.get("metadata") == {"meta_key": "meta_val"}
        assert params.get("status") == "SUCCESS"

    def test_to_request_params_none_data(
            self, mock_queue_manager: Mock, patched_utils: Dict[str, Mock] # noqa: ARG002
    ):
        span = BaseSpan(name="none_data_test", trace_id="trace_none", queue_manager=mock_queue_manager)
        span.start_time = "start-ts-manual"
        span.end_time = "end-ts-manual"

        params = span.to_request_params()
        assert params.get("input") == {}
        assert params.get("output") == {}
        assert params.get("metadata") == {}
        assert params.get("status") == "SUCCESS"


class TestNoOpSpan:
    def test_start(
            self,
            patched_utils: Dict[str, Mock], # noqa: ARG002
            mock_scope_set_current_span: MagicMock,
            mock_scope_reset_current_span: MagicMock
    ):
        span = NoOpSpan(name="noop_start")

        span.start()
        assert span.start_time == "start-ts"
        mock_scope_set_current_span.assert_called_once_with(span)
        assert span._contextvar_token == mock_scope_set_current_span.return_value
        mock_scope_reset_current_span.assert_not_called()

    def test_start_idempotency(self, caplog: pytest.LogCaptureFixture, mock_scope_set_current_span: MagicMock):
        span = NoOpSpan(name="noop_idem_start")
        span.start_time = "already-started-ts"

        with caplog.at_level(logging.WARNING):
            span.start()

        assert "already started" in caplog.text
        mock_scope_set_current_span.assert_not_called()

    def test_end(
            self,
            patched_utils: Dict[str, Mock], # noqa: ARG002
            mock_scope_reset_current_span: MagicMock
    ):
        span = NoOpSpan(name="noop_end")

        span.start()
        assert span.start_time == "start-ts"

        span.end()
        assert span.end_time == "end-ts"  # Second call to iso_timestamp
        mock_scope_reset_current_span.assert_called_once()
        assert span._contextvar_token is None

    def test_end_idempotency(self, caplog: pytest.LogCaptureFixture, mock_scope_reset_current_span: MagicMock):
        span = NoOpSpan(name="noop_idem_end")
        span.end_time = "already-ended-ts"

        with caplog.at_level(logging.WARNING):
            span.end()

        assert "already ended" in caplog.text
        mock_scope_reset_current_span.assert_not_called()

    def test_end_without_start_token(self, caplog: pytest.LogCaptureFixture, mock_scope_reset_current_span: MagicMock):
        # TODO, currently will throw an exception...
        pass

    def test_context_manager_noop(
            self,
            patched_utils: Dict[str, Mock], # noqa: ARG002
            mock_scope_set_current_span: MagicMock,
            mock_scope_reset_current_span: MagicMock
    ):
        span = NoOpSpan(name="noop_ctx")
        mock_token = mock_scope_set_current_span.return_value

        with span as s:
            assert s == span
            assert span.start_time == "start-ts"
            mock_scope_set_current_span.assert_called_once_with(span)
            assert span._contextvar_token == mock_token

        assert span.end_time == "end-ts"
        mock_scope_reset_current_span.assert_called_once_with(mock_token)
        assert span._contextvar_token is None


class TestSpan:
    def test_initialization(self, mock_queue_manager: Mock, patched_utils: Dict[str, Mock]): # noqa: ARG002
        span = Span(name="op_span", trace_id="trace_op", queue_manager=mock_queue_manager)
        assert span.name == "op_span"
        assert span.trace_id == "trace_op"
        assert span.span_id == "test-span-id"
        assert span._queue_manager == mock_queue_manager

    def test_start(
            self,
            mock_queue_manager: Mock,
            patched_utils: Dict[str, Mock], # noqa: ARG002
            mock_scope_set_current_span: MagicMock,
            mock_scope_reset_current_span: MagicMock
    ):
        span = Span(name="op_start", trace_id="t1", queue_manager=mock_queue_manager)

        span.start()
        assert span.start_time == "start-ts"
        mock_queue_manager.report_span_start.assert_called_once_with(span)
        mock_scope_set_current_span.assert_called_once_with(span)
        assert span._contextvar_token == mock_scope_set_current_span.return_value
        mock_scope_reset_current_span.assert_not_called()

    def test_start_idempotency(self, mock_queue_manager: Mock, caplog: pytest.LogCaptureFixture,
                               mock_scope_set_current_span: MagicMock):
        span = Span(name="op_idem_start", trace_id="t_idem", queue_manager=mock_queue_manager)
        span.start_time = "already-started-ts"

        with caplog.at_level(logging.WARNING):
            span.start()

        assert "already started" in caplog.text
        mock_queue_manager.report_span_start.assert_not_called()
        mock_scope_set_current_span.assert_not_called()

    def test_end(
            self,
            mock_queue_manager: Mock,
            patched_utils: Dict[str, Mock], # noqa: ARG002
            mock_scope_set_current_span: MagicMock,
            mock_scope_reset_current_span: MagicMock
    ):
        span = Span(name="op_end", trace_id="t2", queue_manager=mock_queue_manager)

        span.start()
        assert span.start_time == "start-ts"
        mock_queue_manager.report_span_start.assert_called_once_with(span)

        span.end()
        assert span.end_time == "end-ts"
        mock_queue_manager.report_span_end.assert_called_once_with(span)
        mock_scope_reset_current_span.assert_called_once_with(mock_scope_set_current_span.return_value)
        assert span._contextvar_token is None

    def test_end_idempotency(self, mock_queue_manager: Mock, caplog: pytest.LogCaptureFixture, mock_scope_reset_current_span: MagicMock):
        span = Span(name="op_idem_end", trace_id="t_idem_end", queue_manager=mock_queue_manager)
        span.end_time = "already-ended-ts"

        with caplog.at_level(logging.WARNING):
            span.end()

        assert "already ended" in caplog.text
        mock_queue_manager.report_span_end.assert_not_called()
        mock_scope_reset_current_span.assert_not_called()

    def test_end_without_start_token(self, mock_queue_manager: Mock, caplog: pytest.LogCaptureFixture, mock_scope_reset_current_span: MagicMock):
        span = Span(name="op_end_no_token", trace_id="t_no_tok", queue_manager=mock_queue_manager)
        span.start_time = "some-start-time"
        span._contextvar_token = None

        with caplog.at_level(logging.WARNING):
            span.end()

        assert "attempting to end without a valid context token" in caplog.text
        assert span.end_time is None
        mock_queue_manager.report_span_end.assert_not_called()
        mock_scope_reset_current_span.assert_not_called()

    def test_context_manager_operational(
            self,
            mock_queue_manager: Mock,
            patched_utils: Dict[str, Mock], # noqa: ARG002
            mock_scope_set_current_span: MagicMock,
            mock_scope_reset_current_span: MagicMock
    ):
        span = Span(name="op_ctx", trace_id="t_ctx_op", queue_manager=mock_queue_manager)
        mock_token = mock_scope_set_current_span.return_value

        with span as s:
            assert s == span
            assert span.start_time == "start-ts"
            mock_queue_manager.report_span_start.assert_called_once_with(span)
            mock_scope_set_current_span.assert_called_once_with(span)
            assert span._contextvar_token == mock_token

        assert span.end_time == "end-ts"
        mock_queue_manager.report_span_end.assert_called_once_with(span)
        mock_scope_reset_current_span.assert_called_once_with(mock_token)
        assert span._contextvar_token is None

    def test_context_manager_operational_with_exception(
            self,
            mock_queue_manager: Mock,
            patched_utils: Dict[str, Mock], # noqa: ARG002
            mock_scope_set_current_span: MagicMock,
            mock_scope_reset_current_span: MagicMock
    ):
        span = Span(name="op_ctx_exc", trace_id="t_ctx_op_exc", queue_manager=mock_queue_manager)
        mock_token = mock_scope_set_current_span.return_value

        with pytest.raises(RuntimeError, match="Operational error"):
            with span:
                assert span.start_time == "start-ts"
                mock_queue_manager.report_span_start.assert_called_once_with(span)
                mock_scope_set_current_span.assert_called_once_with(span)
                raise RuntimeError("Operational error")

        assert span.end_time == "end-ts"
        mock_queue_manager.report_span_end.assert_called_once_with(span)
        mock_scope_reset_current_span.assert_called_once_with(mock_token)
        assert span._contextvar_token is None

        # NOTE: will likely change this functionality soon
        assert span.metadata is not None
        assert span.metadata["error"] is True
        assert span.metadata["error_type"] == "RuntimeError"
        assert span.metadata["error_message"] == "Operational error"
        assert span.status == "ERROR"
