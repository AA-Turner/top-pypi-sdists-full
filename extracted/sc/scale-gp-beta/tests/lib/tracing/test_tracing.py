import logging
from typing import Dict, Optional
from unittest.mock import Mock, MagicMock, patch

import pytest
from pytest import LogCaptureFixture

from scale_gp_beta.lib.tracing.span import Span, BaseSpan
from scale_gp_beta.lib.tracing.trace import Trace, BaseTrace
from scale_gp_beta.lib.tracing.tracing import create_span, create_trace, current_span, current_trace
from scale_gp_beta.lib.tracing.trace_queue_manager import TraceQueueManager


@pytest.fixture
def mock_queue_manager_instance() -> Mock:
    return Mock(spec=TraceQueueManager)

@pytest.fixture
def mock_active_trace_instance() -> Mock:
    trace_mock = Mock(spec=Trace)
    trace_mock.trace_id = "active-trace-id"
    trace_mock.group_id.return_value = "active-group-id"
    return trace_mock

@pytest.fixture
def mock_active_span_instance(mock_active_trace_instance: Mock) -> Mock:
    span_mock = Mock(spec=Span)
    span_mock.span_id = "active-span-id"
    span_mock.trace_id = mock_active_trace_instance.trace_id
    return span_mock


class TestCurrentHelpers:
    @patch("scale_gp_beta.lib.tracing.tracing.Scope.get_current_span")
    def test_current_span_calls_scope(self, mock_get_current_span: MagicMock) -> None:
        expected_span = Mock(spec=BaseSpan)
        mock_get_current_span.return_value = expected_span
        assert current_span() == expected_span
        mock_get_current_span.assert_called_once_with()

    @patch("scale_gp_beta.lib.tracing.tracing.Scope.get_current_trace")
    def test_current_trace_calls_scope(self, mock_get_current_trace: MagicMock) -> None:
        expected_trace = Mock(spec=BaseTrace)
        mock_get_current_trace.return_value = expected_trace
        assert current_trace() == expected_trace
        mock_get_current_trace.assert_called_once_with()


class TestCreateTrace:
    @patch("scale_gp_beta.lib.tracing.tracing.NoOpTrace")
    @patch("scale_gp_beta.lib.tracing.tracing.is_disabled")
    def test_create_trace_when_disabled(
        self, mock_is_disabled: MagicMock, mock_noop_trace_init: MagicMock,
        caplog: LogCaptureFixture
    ) -> None:
        mock_is_disabled.return_value = True
        mock_noop_trace_instance = mock_noop_trace_init.return_value
        trace_id_arg = "custom-trace-id-disabled"
        trace_name_arg = "custom-trace-name-disabled"

        with caplog.at_level(logging.DEBUG):
            trace = create_trace(trace_id=trace_id_arg, name=trace_name_arg)

        assert trace == mock_noop_trace_instance
        mock_is_disabled.assert_called_once_with()
        mock_noop_trace_init.assert_called_once_with(
            name=trace_name_arg,
            trace_id=trace_id_arg,
            span_id=None,
            group_id=None,
            span_type="TRACER",
            metadata={},
            input={},
            output={},
        )
        assert "Tracing is disabled. Not creating a new trace." in caplog.text

    @patch("scale_gp_beta.lib.tracing.tracing.Trace")
    @patch("scale_gp_beta.lib.tracing.tracing.tracing_queue_manager")
    @patch("scale_gp_beta.lib.tracing.tracing.Scope.get_current_trace")
    def test_create_trace_when_enabled(
        self,
        mock_get_current_trace: MagicMock,
        mock_tqm_func: MagicMock,
        mock_trace_init: MagicMock,
        mock_queue_manager_instance: Mock,
        caplog: LogCaptureFixture
    ) -> None:
        mock_get_current_trace.return_value = None
        mock_tqm_func.return_value = mock_queue_manager_instance
        mock_trace_instance = mock_trace_init.return_value
        mock_trace_instance.trace_id = "generated-trace-id"
        trace_id_arg = "custom-trace-id-enabled"
        trace_name_arg = "custom-trace-name-enabled"

        with caplog.at_level(logging.DEBUG):
            trace = create_trace(trace_id=trace_id_arg, name=trace_name_arg)

        assert trace == mock_trace_instance
        mock_tqm_func.assert_called_once_with()
        mock_trace_init.assert_called_once_with(
            name=trace_name_arg,
            trace_id=trace_id_arg,
            span_id=None,
            group_id=None,
            queue_manager=mock_queue_manager_instance,
            span_type="TRACER",
            metadata={},
            input={},
            output={},
        )
        assert f"Created new trace: {mock_trace_instance.trace_id}" in caplog.text
        assert "already active" not in caplog.text

    @patch("scale_gp_beta.lib.tracing.tracing.Trace")
    @patch("scale_gp_beta.lib.tracing.tracing.tracing_queue_manager")
    @patch("scale_gp_beta.lib.tracing.tracing.Scope.get_current_trace")
    def test_create_trace_when_another_trace_is_active(
        self,
        mock_get_current_trace: MagicMock,
        mock_tqm_func: MagicMock,
        mock_trace_init: MagicMock,
        mock_active_trace_instance: Mock,
        mock_queue_manager_instance: Mock,
        caplog: LogCaptureFixture
    ) -> None:
        mock_get_current_trace.return_value = mock_active_trace_instance
        mock_tqm_func.return_value = mock_queue_manager_instance
        trace_id_arg = "new-trace-while-active"
        trace_name_arg = "new-trace-name-while-active"

        with caplog.at_level(logging.WARNING):
            create_trace(trace_id=trace_id_arg, name=trace_name_arg)

        mock_get_current_trace.assert_called_once_with()
        assert f"Trace with id {mock_active_trace_instance.trace_id} is already active." in caplog.text
        mock_trace_init.assert_called_once()


class TestCreateSpan:

    @patch("scale_gp_beta.lib.tracing.tracing.NoOpSpan")
    @patch("scale_gp_beta.lib.tracing.tracing.Scope.get_current_span")
    @patch("scale_gp_beta.lib.tracing.tracing.is_disabled")
    def test_create_span_when_disabled(
        self,
        mock_is_disabled: MagicMock,
        mock_get_current_span: MagicMock,
        mock_noop_span_init: MagicMock,
        mock_active_trace_instance: Mock # noqa: ARG002
    ) -> None:
        mock_get_current_span.return_value = None
        mock_is_disabled.return_value = True
        mock_noop_span_instance = mock_noop_span_init.return_value
        span_name = "disabled_span"
        span_id_arg = "custom-span-id-disabled"

        mock_parent_trace = Mock(spec=Trace)
        mock_parent_trace.trace_id = "parent-trace-id-for-disabled"

        span = create_span(name=span_name, span_id=span_id_arg, trace_id=mock_parent_trace.trace_id)

        assert span == mock_noop_span_instance
        mock_is_disabled.assert_called_once_with()
        mock_noop_span_init.assert_called_once_with(
            name=span_name,
            span_id=span_id_arg,
            parent_span_id=None,
            group_id=None,
            trace_id=mock_parent_trace.trace_id,
            input={}, output={}, metadata={},
            span_type="STANDALONE"
        )

    @patch("scale_gp_beta.lib.tracing.tracing.NoOpSpan")
    @patch("scale_gp_beta.lib.tracing.tracing.Scope.get_current_span")
    @patch("scale_gp_beta.lib.tracing.tracing.Scope.get_current_trace")
    def test_create_span_no_parent_no_active_trace(
        self,
        mock_get_current_trace: MagicMock,
        mock_get_current_span: MagicMock,
        mock_noop_span_init: MagicMock,
        caplog: LogCaptureFixture
    ) -> None:
        mock_get_current_trace.return_value = None
        mock_get_current_span.return_value = None
        mock_noop_span_instance = mock_noop_span_init.return_value
        span_name = "orphaned_span"
        span_id_arg = "custom-span-id-orphaned"
        group_id_arg = "custom-group-id-orphaned"

        with caplog.at_level(logging.DEBUG):
            span = create_span(name=span_name, span_id=span_id_arg, group_id=group_id_arg)

        assert span == mock_noop_span_instance
        mock_get_current_trace.assert_called_once_with()
        mock_noop_span_init.assert_called_once_with(
            name=span_name,
            span_id=span_id_arg,
            parent_span_id=None,
            group_id=group_id_arg,
            trace_id=None,
            input={}, output={}, metadata={},
            span_type="STANDALONE"
        )
        assert "Attempting to create a span with no trace" in caplog.text

    @patch("scale_gp_beta.lib.tracing.tracing.Span")
    @patch("scale_gp_beta.lib.tracing.tracing.tracing_queue_manager")
    @patch("scale_gp_beta.lib.tracing.tracing.Scope.get_current_span")
    @patch("scale_gp_beta.lib.tracing.tracing.Scope.get_current_trace")
    def test_create_span_with_explicit_trace_parent(
        self,
        mock_get_current_trace: MagicMock, # noqa: ARG002
        mock_get_current_span: MagicMock,
        mock_tqm_func: MagicMock,
        mock_span_init: MagicMock,
        mock_queue_manager_instance: Mock,
        caplog: LogCaptureFixture,
        mock_active_span_instance: Mock
    ) -> None:
        mock_tqm_func.return_value = mock_queue_manager_instance
        mock_span_instance = mock_span_init.return_value
        mock_span_instance.span_id = "generated-span-id-trace-parent"
        mock_get_current_span.return_value = mock_active_span_instance

        mock_parent_trace = Mock(spec=Trace)
        mock_parent_trace.trace_id = "explicit-parent-trace-id"
        mock_parent_trace.group_id = "explicit-parent-group-id"
        span_name = "span_with_trace_parent"
        span_id_arg = "custom-id-trace-parent"
        input_arg = {"input_key": "input_val"}
        output_arg = {"output_key": "output_val"}
        metadata_arg: Dict[str, Optional[str]] = {"meta_key": "meta_val"}


        with caplog.at_level(logging.DEBUG):
            span = create_span(
                name=span_name,
                span_id=span_id_arg,
                trace_id=mock_parent_trace.trace_id,
                group_id=mock_parent_trace.group_id,
                input=input_arg,
                output=output_arg,
                metadata=metadata_arg
            )

        assert span == mock_span_instance
        mock_tqm_func.assert_called_once_with()
        mock_span_init.assert_called_once_with(
            name=span_name,
            span_id=span_id_arg,
            parent_span_id=mock_active_span_instance.span_id,
            group_id=mock_parent_trace.group_id,
            trace_id=mock_parent_trace.trace_id,
            input=input_arg,
            output=output_arg,
            metadata=metadata_arg,
            queue_manager=mock_queue_manager_instance,
            span_type="STANDALONE"
        )
        assert f"Created new span: {mock_span_instance.span_id}" in caplog.text

    @pytest.mark.skip(reason="Currently do not support searching for parent span and finding current trace")
    @patch("scale_gp_beta.lib.tracing.tracing.Span")
    @patch("scale_gp_beta.lib.tracing.tracing.tracing_queue_manager")
    @patch("scale_gp_beta.lib.tracing.tracing.Scope.get_current_span")
    @patch("scale_gp_beta.lib.tracing.tracing.Scope.get_current_trace")
    def test_create_span_with_explicit_span_parent(
        self,
        mock_get_current_trace: MagicMock, # noqa: ARG002
        mock_get_current_span: MagicMock, # noqa: ARG002
        mock_tqm_func: MagicMock,
        mock_span_init: MagicMock,
        mock_queue_manager_instance: Mock,
    ) -> None:
        mock_tqm_func.return_value = mock_queue_manager_instance

        mock_parent_s = Mock(spec=Span)
        mock_parent_s.group_id = "explicit-parent-group-id"
        mock_parent_s.trace_id = "parent-span-trace-id"
        mock_parent_s.span_id = "parent-span-actual-id"
        span_name = "span_with_span_parent"

        create_span(name=span_name, parent_id=mock_parent_s.span_id, group_id=mock_parent_s.group_id)

        # NOTE: this will grab the trace_id from current context and not mock_parent_s.trace_id
        mock_span_init.assert_called_once_with(
            name=span_name,
            span_id=None,
            parent_span_id=mock_parent_s.span_id,
            trace_id=mock_parent_s.trace_id,
            group_id=mock_parent_s.group_id,
            input={}, output={}, metadata={},
            queue_manager=mock_queue_manager_instance,
            span_type="STANDALONE"
        )

    @patch("scale_gp_beta.lib.tracing.tracing.Span")
    @patch("scale_gp_beta.lib.tracing.tracing.tracing_queue_manager")
    @patch("scale_gp_beta.lib.tracing.tracing.Scope.get_current_span")
    @patch("scale_gp_beta.lib.tracing.tracing.Scope.get_current_trace")
    def test_create_span_no_explicit_parent_uses_scope_trace(
        self,
        mock_get_current_trace: MagicMock,
        mock_get_current_span: MagicMock,
        mock_tqm_func: MagicMock,
        mock_span_init: MagicMock,
        mock_active_trace_instance: Mock,
        mock_queue_manager_instance: Mock,
    ) -> None:
        mock_get_current_trace.return_value = mock_active_trace_instance
        mock_get_current_span.return_value = None
        mock_tqm_func.return_value = mock_queue_manager_instance

        create_span(name="span_uses_scope_trace")

        mock_get_current_trace.assert_called_once_with()
        mock_get_current_span.assert_called_once_with()
        mock_span_init.assert_called_once_with(
            name="span_uses_scope_trace",
            span_id=None,
            parent_span_id=None,
            group_id=mock_active_trace_instance.group_id,
            trace_id=mock_active_trace_instance.trace_id,
            input={}, output={}, metadata={},
            queue_manager=mock_queue_manager_instance,
            span_type="STANDALONE"
        )

    @patch("scale_gp_beta.lib.tracing.tracing.Span")
    @patch("scale_gp_beta.lib.tracing.tracing.tracing_queue_manager")
    @patch("scale_gp_beta.lib.tracing.tracing.Scope.get_current_span")
    @patch("scale_gp_beta.lib.tracing.tracing.Scope.get_current_trace")
    def test_create_span_no_explicit_parent_uses_scope_span(
        self,
        mock_get_current_trace: MagicMock,
        mock_get_current_span: MagicMock,
        mock_tqm_func: MagicMock,
        mock_span_init: MagicMock,
        mock_active_trace_instance: Mock,
        mock_active_span_instance: Mock,
        mock_queue_manager_instance: Mock,
    ) -> None:
        mock_get_current_trace.return_value = mock_active_trace_instance
        mock_get_current_span.return_value = mock_active_span_instance
        mock_tqm_func.return_value = mock_queue_manager_instance

        create_span(name="span_uses_scope_span")

        mock_get_current_trace.assert_called_once_with()
        mock_get_current_span.assert_called_once_with()
        mock_span_init.assert_called_once_with(
            name="span_uses_scope_span",
            span_id=None,
            parent_span_id=mock_active_span_instance.span_id,
            trace_id=mock_active_trace_instance.trace_id,
            group_id=mock_active_trace_instance.group_id,
            input={}, output={}, metadata={},
            queue_manager=mock_queue_manager_instance,
            span_type="STANDALONE"
        )
