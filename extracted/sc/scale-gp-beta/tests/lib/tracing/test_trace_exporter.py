import logging
from queue import Empty, Queue
from typing import List
from unittest.mock import Mock, patch

import pytest

from scale_gp_beta import SGPClient
from scale_gp_beta._exceptions import APIError
from scale_gp_beta.lib.tracing.span import Span
from scale_gp_beta.lib.tracing.exceptions import ParamsCreationError
from scale_gp_beta.types.span_create_param import SpanCreateParam as SpanCreateRequest
from scale_gp_beta.lib.tracing.trace_exporter import TraceExporter


def create_test_span_request(id_str: str) -> SpanCreateRequest:
    return SpanCreateRequest(name=id_str, id=id_str, trace_id="trace-id", group_id="group-id", start_timestamp="start")


@pytest.fixture
def mock_sgp_client() -> Mock:
    client = Mock(spec=SGPClient)
    client.spans = Mock()
    client.spans.upsert_batch = Mock()
    return client


@pytest.fixture
def mock_span() -> Mock:
    span = Mock(spec=Span)
    span.span_id = "default_span_id"
    span.to_request_params.return_value = create_test_span_request("default_span")
    return span


def fill_queue(q: "Queue[Span]", num_spans: int) -> "list[SpanCreateRequest]":
    expected_requests: List[SpanCreateRequest] = []
    for i in range(num_spans):
        span_id = f"span_{i}"
        mock_s = Mock(spec=Span)
        request_param = create_test_span_request(span_id)
        mock_s.to_request_params.return_value = request_param
        q.put(mock_s)
        expected_requests.append(request_param)
    return expected_requests


class TestTraceExporterCreateBatches:
    def test_empty_queue(self):
        exporter = TraceExporter(max_batch_size=5, max_retries=3)
        q: Queue[Span] = Queue()
        batches = exporter._create_batches(q)
        assert batches == []
        assert q.empty()

    def test_less_than_max_batch_size(self):
        exporter = TraceExporter(max_batch_size=5, max_retries=3)
        q: Queue[Span] = Queue()
        expected_requests = fill_queue(q, 3)
        batches = exporter._create_batches(q)
        assert len(batches) == 1
        assert batches[0] == expected_requests
        assert q.empty()

    def test_exact_max_batch_size(self):
        exporter = TraceExporter(max_batch_size=3, max_retries=3)
        q: Queue[Span] = Queue()
        expected_requests = fill_queue(q, 3)
        batches = exporter._create_batches(q)
        assert len(batches) == 1
        assert batches[0] == expected_requests
        assert q.empty()

    def test_multiple_batches(self):
        exporter = TraceExporter(max_batch_size=2, max_retries=3)
        q: Queue[Span] = Queue()
        expected_requests = fill_queue(q, 5)

        batches = exporter._create_batches(q)
        assert len(batches) == 3
        assert batches[0] == expected_requests[0:2]
        assert batches[1] == expected_requests[2:4]
        assert batches[2] == [expected_requests[4]]
        assert q.empty()

    def test_max_batch_size_one(self):
        exporter = TraceExporter(max_batch_size=1, max_retries=3)
        q: Queue[Span] = Queue()
        expected_requests = fill_queue(q, 3)

        batches = exporter._create_batches(q)
        assert len(batches) == 3
        assert batches[0] == [expected_requests[0]]
        assert batches[1] == [expected_requests[1]]
        assert batches[2] == [expected_requests[2]]
        assert q.empty()

    def test_queue_becomes_empty_mid_batch(self):
        exporter = TraceExporter(max_batch_size=5, max_retries=3)
        q: Queue[Span] = Queue()
        initial_spans = [Mock(spec=Span) for _ in range(2)]
        expected_requests: List[SpanCreateRequest] = []
        for i, s in enumerate(initial_spans):
            req = create_test_span_request(f"s_{i}")
            s.to_request_params.return_value = req
            expected_requests.append(req)

        side_effect_list = [initial_spans[0], initial_spans[1], Empty]
        q.get_nowait = Mock(side_effect=side_effect_list)
        q.qsize = Mock(side_effect=[2, 1, 0, 0, 0])

        batches = exporter._create_batches(q)
        assert len(batches) == 1
        assert batches[0] == expected_requests
        assert q.get_nowait.call_count == 2


@patch("scale_gp_beta.lib.tracing.trace_exporter.time.sleep")
class TestTraceExporterExportBatch:
    def test_export_batch_success_first_try(
        self, mock_sleep: Mock, mock_sgp_client: Mock, caplog: pytest.LogCaptureFixture
    ):
        exporter = TraceExporter(max_batch_size=5, max_retries=3)
        batch_data = [create_test_span_request("span1")]

        with caplog.at_level(logging.INFO):
            exporter._export_batch(batch_data, mock_sgp_client)

        mock_sgp_client.spans.upsert_batch.assert_called_once_with(items=batch_data)
        mock_sleep.assert_not_called()
        assert "API error" not in caplog.text
        assert "Failed to export span batch" not in caplog.text

    def test_export_batch_success_after_retries(
        self, mock_sleep: Mock, mock_sgp_client: Mock, caplog: pytest.LogCaptureFixture
    ):
        exporter = TraceExporter(max_batch_size=5, max_retries=3)
        batch_data = [create_test_span_request("span1")]

        # Simulate APIError for the first two calls, then success
        mock_sgp_client.spans.upsert_batch.side_effect = [
            APIError("Simulated API Error 1", request=Mock(), body=None),
            APIError("Simulated API Error 2", request=Mock(), body=None),
            None,  # Success
        ]

        with caplog.at_level(logging.WARNING):
            exporter._export_batch(batch_data, mock_sgp_client)

        assert mock_sgp_client.spans.upsert_batch.call_count == 3
        mock_sgp_client.spans.upsert_batch.assert_called_with(items=batch_data)
        assert mock_sleep.call_count == 2
        assert caplog.text.count("API error occurred while exporting batch:") == 2
        assert "Failed to export span batch" not in caplog.text

    def test_export_batch_fails_all_retries(
        self, mock_sleep: Mock, mock_sgp_client: Mock, caplog: pytest.LogCaptureFixture
    ):
        max_r = 2
        exporter = TraceExporter(max_batch_size=5, max_retries=max_r)
        batch_data = [create_test_span_request("span1")]

        mock_sgp_client.spans.upsert_batch.side_effect = APIError(
            "Simulated Persistent API Error", request=Mock(), body=Mock()
        )

        with caplog.at_level(logging.WARNING):
            exporter._export_batch(batch_data, mock_sgp_client)

        assert mock_sgp_client.spans.upsert_batch.call_count == max_r
        assert mock_sleep.call_count == max_r - 1
        assert caplog.text.count("API error occurred while exporting batch:") == max_r
        assert f"Failed to export span batch after {max_r} attempts" in caplog.text

    def test_export_batch_max_retries_one(
        self, mock_sleep: Mock, mock_sgp_client: Mock, caplog: pytest.LogCaptureFixture
    ):
        exporter = TraceExporter(max_batch_size=5, max_retries=1)
        batch_data = [create_test_span_request("span1")]
        mock_sgp_client.spans.upsert_batch.side_effect = APIError("Simulated API Error", request=Mock(), body=Mock())

        with caplog.at_level(logging.ERROR):
            exporter._export_batch(batch_data, mock_sgp_client)

        mock_sgp_client.spans.upsert_batch.assert_called_once_with(items=batch_data)
        mock_sleep.assert_not_called()
        assert "Failed to export span batch after 1 attempts" in caplog.text


class TestTraceExporterExportIntegration:
    @patch("scale_gp_beta.lib.tracing.trace_exporter.TraceExporter._export_batch")
    @patch("scale_gp_beta.lib.tracing.trace_exporter.TraceExporter._create_batches")
    def test_export_orchestration_no_batches(
        self,
        mock_create_batches: Mock,
        mock_export_batch_method: Mock,
        mock_sgp_client: Mock,
        caplog: pytest.LogCaptureFixture,
    ):
        mock_create_batches.return_value = []
        exporter = TraceExporter(max_batch_size=5, max_retries=3)
        q: Queue[Span] = Queue()

        with caplog.at_level(logging.DEBUG):
            exporter.export(mock_sgp_client, q)

        mock_create_batches.assert_called_once_with(q)
        mock_export_batch_method.assert_not_called()
        assert "No new span batches to export" in caplog.text

    @patch("scale_gp_beta.lib.tracing.trace_exporter.TraceExporter._export_batch")
    @patch("scale_gp_beta.lib.tracing.trace_exporter.TraceExporter._create_batches")
    def test_export_orchestration_multiple_batches(
        self,
        mock_create_batches: Mock,
        mock_export_batch_method: Mock,
        mock_sgp_client: Mock,
        caplog: pytest.LogCaptureFixture,
    ):
        batch1_data = [create_test_span_request("s1")]
        batch2_data = [create_test_span_request("s2")]
        mock_create_batches.return_value = [batch1_data, batch2_data]

        exporter = TraceExporter(max_batch_size=5, max_retries=3)
        q: Queue[Span] = Queue()  # Queue content doesn't matter as _create_batches is mocked

        with caplog.at_level(logging.INFO):
            exporter.export(mock_sgp_client, q)

        mock_create_batches.assert_called_once_with(q)
        assert mock_export_batch_method.call_count == 2
        mock_export_batch_method.assert_any_call(batch1_data, mock_sgp_client)
        mock_export_batch_method.assert_any_call(batch2_data, mock_sgp_client)
        assert "Exporting 2 span batches" in caplog.text

    def test_export_e2e_success(self, mock_sgp_client: Mock, caplog: pytest.LogCaptureFixture):
        exporter = TraceExporter(max_batch_size=2, max_retries=1)
        q: Queue[Span] = Queue()
        num_spans = 3
        fill_queue(q, num_spans)

        with caplog.at_level(logging.INFO):
            exporter.export(mock_sgp_client, q)

        assert mock_sgp_client.spans.upsert_batch.call_count == 2

        first_call_args = mock_sgp_client.spans.upsert_batch.call_args_list[0]
        second_call_args = mock_sgp_client.spans.upsert_batch.call_args_list[1]

        assert len(first_call_args[1]["items"]) == 2
        assert len(second_call_args[1]["items"]) == 1

        assert "Exporting 2 span batches" in caplog.text
        assert "Failed to export" not in caplog.text

    def test_export_e2e_one_batch_fails(self, mock_sgp_client: Mock, caplog: pytest.LogCaptureFixture):
        exporter = TraceExporter(max_batch_size=1, max_retries=1)
        q: Queue[Span] = Queue()
        expected_requests = fill_queue(q, 2)  # Two batches of 1: [s0], [s1]

        # First batch succeeds, second fails
        mock_sgp_client.spans.upsert_batch.side_effect = [
            None,
            APIError("Failure on second batch", request=Mock(), body=Mock()),
        ]

        with caplog.at_level(logging.INFO):
            exporter.export(mock_sgp_client, q)

        assert mock_sgp_client.spans.upsert_batch.call_count == 2
        mock_sgp_client.spans.upsert_batch.assert_any_call(items=[expected_requests[0]])
        mock_sgp_client.spans.upsert_batch.assert_any_call(items=[expected_requests[1]])

        text: str = caplog.text
        assert "Exporting 2 span batches" in text
        assert "Failed to export span batch after 1 attempts" in text
        assert text.count("API error occurred while exporting batch: Failure on second batch") == 1


@patch("scale_gp_beta.lib.tracing.trace_exporter.time.sleep")
class TestTraceExporterExportFn:
    def test_export_fn_called_instead_of_upsert_batch(self, mock_sleep: Mock, mock_sgp_client: Mock):
        export_fn = Mock()
        exporter = TraceExporter(max_batch_size=5, max_retries=3, export_fn=export_fn)
        batch_data = [create_test_span_request("span1")]

        exporter._export_batch(batch_data, mock_sgp_client)

        export_fn.assert_called_once_with(batch_data)
        mock_sgp_client.spans.upsert_batch.assert_not_called()
        mock_sleep.assert_not_called()

    def test_export_fn_success_first_try(
        self, mock_sleep: Mock, mock_sgp_client: Mock, caplog: pytest.LogCaptureFixture
    ):
        export_fn = Mock()
        exporter = TraceExporter(max_batch_size=5, max_retries=3, export_fn=export_fn)
        batch_data = [create_test_span_request("span1")]

        with caplog.at_level(logging.INFO):
            exporter._export_batch(batch_data, mock_sgp_client)

        export_fn.assert_called_once_with(batch_data)
        mock_sleep.assert_not_called()
        assert "Failed to export span batch" not in caplog.text

    def test_export_fn_retries_on_api_error(
        self, mock_sleep: Mock, mock_sgp_client: Mock, caplog: pytest.LogCaptureFixture
    ):
        export_fn = Mock(
            side_effect=[
                APIError("transient error 1", request=Mock(), body=None),
                APIError("transient error 2", request=Mock(), body=None),
                None,
            ]
        )
        exporter = TraceExporter(max_batch_size=5, max_retries=3, export_fn=export_fn)
        batch_data = [create_test_span_request("span1")]

        with caplog.at_level(logging.WARNING):
            exporter._export_batch(batch_data, mock_sgp_client)

        assert export_fn.call_count == 3
        assert mock_sleep.call_count == 2
        assert "Failed to export span batch" not in caplog.text
        mock_sgp_client.spans.upsert_batch.assert_not_called()

    def test_export_fn_fails_all_retries_drops_batch(
        self,
        mock_sleep: Mock,  # noqa: ARG002
        mock_sgp_client: Mock,
        caplog: pytest.LogCaptureFixture
    ):
        max_r = 2
        export_fn = Mock(side_effect=APIError("persistent error", request=Mock(), body=Mock()))
        exporter = TraceExporter(max_batch_size=5, max_retries=max_r, export_fn=export_fn)
        batch_data = [create_test_span_request("span1")]

        with caplog.at_level(logging.ERROR):
            exporter._export_batch(batch_data, mock_sgp_client)

        assert export_fn.call_count == max_r
        assert f"Failed to export span batch after {max_r} attempts" in caplog.text
        mock_sgp_client.spans.upsert_batch.assert_not_called()

    def test_export_fn_retries_on_non_api_error(
        self, mock_sleep: Mock, mock_sgp_client: Mock, caplog: pytest.LogCaptureFixture
    ):
        export_fn = Mock(
            side_effect=[
                RuntimeError("transient storage error 1"),
                RuntimeError("transient storage error 2"),
                None,
            ]
        )
        exporter = TraceExporter(max_batch_size=5, max_retries=3, export_fn=export_fn)
        batch_data = [create_test_span_request("span1")]

        with caplog.at_level(logging.WARNING):
            exporter._export_batch(batch_data, mock_sgp_client)

        assert export_fn.call_count == 3
        assert mock_sleep.call_count == 2
        assert "export_fn raised an unexpected error" in caplog.text
        assert "Failed to export span batch" not in caplog.text
        mock_sgp_client.spans.upsert_batch.assert_not_called()

    def test_export_fn_fails_all_retries_non_api_error_drops_batch(
        self,
        mock_sleep: Mock,  # noqa: ARG002
        mock_sgp_client: Mock,
        caplog: pytest.LogCaptureFixture,
    ):
        max_r = 2
        export_fn = Mock(side_effect=RuntimeError("persistent storage error"))
        exporter = TraceExporter(max_batch_size=5, max_retries=max_r, export_fn=export_fn)
        batch_data = [create_test_span_request("span1")]

        with caplog.at_level(logging.ERROR):
            exporter._export_batch(batch_data, mock_sgp_client)

        assert export_fn.call_count == max_r
        assert f"Failed to export span batch after {max_r} attempts" in caplog.text
        mock_sgp_client.spans.upsert_batch.assert_not_called()

    def test_export_fn_receives_correct_batch_contents(
        self,
        mock_sleep: Mock,  # noqa: ARG002
        mock_sgp_client: Mock
    ):
        received: list[list[SpanCreateRequest]] = []
        exporter = TraceExporter(max_batch_size=5, max_retries=1, export_fn=lambda batch: received.append(batch))
        q: Queue[Span] = Queue()
        expected = fill_queue(q, 3)

        exporter.export(mock_sgp_client, q)

        assert len(received) == 1
        assert received[0] == expected
        mock_sgp_client.spans.upsert_batch.assert_not_called()

    def test_export_fn_called_per_batch(
        self,
        mock_sleep: Mock,  # noqa: ARG002
        mock_sgp_client: Mock
    ):
        received: list[list[SpanCreateRequest]] = []
        exporter = TraceExporter(max_batch_size=2, max_retries=1, export_fn=lambda batch: received.append(batch))
        q: Queue[Span] = Queue()
        expected = fill_queue(q, 5)  # 3 batches: [0,1], [2,3], [4]

        exporter.export(mock_sgp_client, q)

        assert len(received) == 3
        assert received[0] == expected[0:2]
        assert received[1] == expected[2:4]
        assert received[2] == [expected[4]]
        mock_sgp_client.spans.upsert_batch.assert_not_called()


@patch("scale_gp_beta.lib.tracing.trace_exporter.ParamsCreationError", ParamsCreationError)
class TestTraceExporterSingleSpan:
    def test_create_one_span_batch_success(self, mock_span: Mock):
        exporter = TraceExporter(max_batch_size=5, max_retries=3)
        expected_request = mock_span.to_request_params()
        mock_span.reset_mock()

        batch = exporter._create_one_span_batch(mock_span)

        assert batch == [expected_request]
        mock_span.to_request_params.assert_called_once()

    def test_create_one_span_batch_param_creation_error(self, caplog: pytest.LogCaptureFixture):
        exporter = TraceExporter(max_batch_size=5, max_retries=3)
        mock_span_failing = Mock(spec=Span)
        error_message = "Failed to create params due to missing attribute"
        mock_span_failing.to_request_params.side_effect = ParamsCreationError(error_message)

        with caplog.at_level(logging.WARNING):
            batch = exporter._create_one_span_batch(mock_span_failing)

        assert batch == []
        assert f"ParamsCreationError:" in caplog.text
        assert error_message in caplog.text
        assert "dropping" in caplog.text

    @patch("scale_gp_beta.lib.tracing.trace_exporter.TraceExporter._export_batch")
    def test_export_span_orchestration(
        self, mock_export_batch: Mock, mock_sgp_client: Mock, mock_span: Mock, caplog: pytest.LogCaptureFixture
    ):
        exporter = TraceExporter(max_batch_size=5, max_retries=3)
        expected_request = mock_span.to_request_params()
        mock_span.reset_mock()
        expected_batch = [expected_request]

        with caplog.at_level(logging.INFO):
            exporter.export_span(mock_sgp_client, mock_span)

        mock_span.to_request_params.assert_called_once()
        mock_export_batch.assert_called_once_with(expected_batch, mock_sgp_client)
        assert f"Exporting single span with id {mock_span.span_id}" in caplog.text

    def test_export_span_e2e_success(self, mock_sgp_client: Mock, mock_span: Mock, caplog: pytest.LogCaptureFixture):
        exporter = TraceExporter(max_batch_size=5, max_retries=3)
        expected_request = mock_span.to_request_params()
        expected_batch = [expected_request]

        with caplog.at_level(logging.INFO):
            exporter.export_span(mock_sgp_client, mock_span)

        mock_sgp_client.spans.upsert_batch.assert_called_once_with(items=expected_batch)
        assert f"Exporting single span with id {mock_span.span_id}" in caplog.text
        assert "Failed to export" not in caplog.text

    def test_export_span_uses_export_fn(self, mock_sgp_client: Mock, mock_span: Mock, caplog: pytest.LogCaptureFixture):
        received: list[list[SpanCreateRequest]] = []
        exporter = TraceExporter(max_batch_size=5, max_retries=3, export_fn=lambda batch: received.append(batch))

        with caplog.at_level(logging.INFO):
            exporter.export_span(mock_sgp_client, mock_span)

        assert len(received) == 1
        assert received[0] == [mock_span.to_request_params()]
        mock_sgp_client.spans.upsert_batch.assert_not_called()
        assert f"Exporting single span with id {mock_span.span_id}" in caplog.text
