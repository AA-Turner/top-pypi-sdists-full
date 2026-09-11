"""Unit tests for UDF route-decision metrics."""

from unittest.mock import patch

from sagemaker_studio.utils.udf import metrics


def test_route_decision_emits_one_metric_with_the_decision_dimensions():
    with patch("sagemaker_studio.utils.udf.metrics.log_session_metric") as logged:
        metrics.record_route_decision(
            capability="udf",
            worker_python="3.13",
            client_python="3.11",
            spark_version="4.1.1",
            source="probe",
            routed=True,
            session_id="s-1",
        )
    assert logged.call_count == 1
    kwargs = logged.call_args.kwargs
    assert kwargs["metric_name"] == "UDFRouteDecision"
    assert kwargs["session_id"] == "s-1"
    props = kwargs["additional_properties"]
    assert props["Routed"] == "true"
    assert props["WorkerPython"] == "3.13"
    assert props["ClientPython"] == "3.11"
    assert props["SparkVersion"] == "4.1.1"
    assert props["DetectionSource"] == "probe"
    assert props["Capability"] == "udf"


def test_route_decision_never_raises_when_the_metrics_backend_fails():
    with patch(
        "sagemaker_studio.utils.udf.metrics.log_session_metric", side_effect=RuntimeError("down")
    ):
        metrics.record_route_decision(
            capability="udf",
            worker_python="3.13",
            client_python="3.11",
            spark_version="4.1.1",
            source="probe",
            routed=True,
        )  # must not raise


def test_sidecar_failure_metric_carries_the_error_class():
    with patch("sagemaker_studio.utils.udf.metrics.log_session_metric") as logged:
        metrics.record_sidecar_failure(
            capability="pandas_udf",
            worker_python="3.13",
            spark_version="4.1.1",
            error_class="UDFSidecarError",
        )
    props = logged.call_args.kwargs["additional_properties"]
    assert props["ErrorClass"] == "UDFSidecarError"
    assert logged.call_args.kwargs["metric_name"] == "UDFSidecarFailure"


def test_sidecar_failure_never_raises_when_the_metrics_backend_fails():
    with patch(
        "sagemaker_studio.utils.udf.metrics.log_session_metric", side_effect=RuntimeError("down")
    ):
        metrics.record_sidecar_failure(
            capability="pandas_udf",
            worker_python="3.13",
            spark_version="4.1.1",
            error_class="UDFSidecarError",
        )  # must not raise
