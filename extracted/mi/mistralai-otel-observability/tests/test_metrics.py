"""Metric instrument and histogram view tests."""

import math

from conftest import SDKHarness, fake_clock, histogram_points, metrics_by_name, point_attributes

from mistralai.observability.otel import OperationDuration, StreamingChunk, TokenUsage
from mistralai.observability.otel import semconv_constants as c


def test_metrics_and_histogram_views(harness: SDKHarness) -> None:
    """Metrics should use the expected histogram instruments and views."""
    harness.observability.record_token_usage(TokenUsage(input_tokens=3, output_tokens=5, attributes={"team": "evals"}))
    harness.observability.record_operation_duration(
        OperationDuration(duration_s=0.25, operation_name="chat", attributes={"team": "evals"})
    )
    timer = harness.observability.start_streaming_timer(
        StreamingChunk(operation_name="chat", attributes={"team": "evals"}),
        clock=fake_clock([0.0, 0.1, 0.16]),
    )
    assert math.isclose(timer.record_chunk(), 0.1)
    assert math.isclose(timer.record_chunk(), 0.06)

    harness.observability.flush()
    collected_metrics = metrics_by_name(harness.metric_reader.get_metrics_data())

    token_points = histogram_points(collected_metrics[c.METRIC_GEN_AI_CLIENT_TOKEN_USAGE])
    assert {point_attributes(point)[c.ATTR_GEN_AI_TOKEN_TYPE]: point.sum for point in token_points} == {
        c.TOKEN_TYPE_INPUT: 3,
        c.TOKEN_TYPE_OUTPUT: 5,
    }
    assert all(point_attributes(point)["team"] == "evals" for point in token_points)
    assert token_points[0].explicit_bounds == (1, 4, 16, 64, 256, 1024, 4096, 16384, 65536)

    duration_point = histogram_points(collected_metrics[c.METRIC_GEN_AI_CLIENT_OPERATION_DURATION])[0]
    assert math.isclose(duration_point.sum, 0.25)
    assert point_attributes(duration_point)[c.ATTR_GEN_AI_OPERATION_NAME] == "chat"

    first_chunk_point = histogram_points(collected_metrics[c.METRIC_GEN_AI_CLIENT_OPERATION_TIME_TO_FIRST_CHUNK])[0]
    per_chunk_point = histogram_points(collected_metrics[c.METRIC_GEN_AI_CLIENT_OPERATION_TIME_PER_OUTPUT_CHUNK])[0]
    assert math.isclose(first_chunk_point.sum, 0.1)
    assert math.isclose(per_chunk_point.sum, 0.06)
