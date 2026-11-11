import json
from threading import Event
from typing import Optional, Dict, List, Tuple, Any

import pytest
from pytest_httpserver import HTTPServer

from statsig_python_core import (
    ObservabilityClient,
    StatsigOptions,
    StatsigUser,
    Statsig,
)
from utils import get_test_data_resource


class MockObservabilityClient(ObservabilityClient):
    init_called = False
    dist_called = False
    error_called = False
    metrics: List[
        Tuple[str, str, Any, Optional[Dict[str, str]]]
    ]  # (type, metric_name, value, tags)

    VERBOSE = False

    def __new__(cls, test_param: str = ""):
        instance = super().__new__(cls)
        instance.test_param = test_param
        instance.metrics = []
        instance.error_received = Event()
        instance.propagation_received = Event()
        return instance

    def init(self) -> None:
        self.init_called = True

        self._log("Initializing ExampleObservationClient")

    def increment(
        self, metric_name: str, value: int = 1, tags: Optional[Dict[str, str]] = None
    ) -> None:
        self._log(f"Incrementing {metric_name} by {value} with tags {tags}")
        self.metrics.append(("increment", metric_name, value, tags))

    def gauge(
        self, metric_name: str, value: float, tags: Optional[Dict[str, str]] = None
    ) -> None:
        self._log(f"Gauging {metric_name} by {value} with tags {tags}")
        self.metrics.append(("gauge", metric_name, value, tags))

    def dist(
        self, metric_name: str, value: float, tags: Optional[Dict[str, str]] = None
    ) -> None:
        self._log(f"Distribution {metric_name} by {value} with tags {tags}")
        self.dist_called = True
        self.metrics.append(("distribution", metric_name, value, tags))
        if metric_name == "statsig.sdk.config_propagation_diff":
            self.propagation_received.set()

    def error(self, tag: str, error: str) -> None:
        self._log(f"Error callback for {tag}: {error}")
        self.error_called = True
        self.metrics.append(("error", tag, error, None))
        self.error_received.set()

    def should_enable_high_cardinality_for_this_tag(self, tag):
        return True

    def _log(self, message: str):
        if self.VERBOSE:
            print(message)


@pytest.fixture
def statsig_setup(httpserver: HTTPServer):
    dcs_content = get_test_data_resource("eval_proj_dcs.json")
    json_data = json.loads(dcs_content)
    del json_data["checksum"]

    repaired_json_data = json_data.copy()
    repaired_json_data["checksum"] = "equal-lcut-repair-checksum"

    httpserver.expect_ordered_request(
        "/v2/download_config_specs"
    ).respond_with_json(json_data)
    httpserver.expect_request(
        "/v2/download_config_specs"
    ).respond_with_json(repaired_json_data)

    httpserver.expect_request("/v1/log_event").respond_with_json({"success": True})

    observability_client = MockObservabilityClient()

    options = StatsigOptions()
    options.specs_url = httpserver.url_for("/v2/download_config_specs")
    options.log_event_url = httpserver.url_for("/v1/log_event")
    options.observability_client = observability_client
    options.specs_sync_interval_ms = 1000
    options.output_log_level = "error"
    statsig = Statsig("secret-key", options)

    statsig.initialize().wait()

    yield statsig, observability_client, httpserver, str(json_data["time"])

    statsig.shutdown().wait()


def test_observability_client_usage_with_test_param():
    observability_client = MockObservabilityClient(test_param="test_param")
    assert observability_client.test_param == "test_param"


def test_observability_client_usage(statsig_setup):
    """Test that MockObservabilityClient correctly tracks init(), dist() calls."""
    statsig, observability_client, httpserver, _ = statsig_setup
    user = StatsigUser(user_id="test-user")

    statsig.check_gate(user, "test-gate")

    statsig.flush_events().wait()

    assert observability_client.init_called, "init() should have been called"

    dist_event = next(
        (
            m
            for m in observability_client.metrics
            if m[0] == "distribution" and m[1] == "statsig.sdk.initialization"
        ),
        None,
    )
    assert dist_event is not None, "distribution() should have been called"
    assert isinstance(dist_event[2], float)
    tags = dist_event[3]
    assert tags is not None
    assert tags["init_success"] == "true"
    assert tags["store_populated"] == "true"
    assert tags["source"] == "Network"
    assert tags["sdk_key"] == "secret-key"
    assert tags["sdk_type"] == "statsig-server-core-python"
    assert tags["sdk_version"]
    assert tags["init_source_api"] == f"http://{httpserver.host}:{httpserver.port}/v2"


def test_error_callback_usage(httpserver: HTTPServer):
    """Test that error_callback() is called."""
    observability_client = MockObservabilityClient()

    httpserver.expect_request("/v2/download_config_specs").respond_with_data(status=401)
    httpserver.expect_request("/v1/log_event").respond_with_json({"success": True})
    options = StatsigOptions(
        specs_url=httpserver.url_for("/v2/download_config_specs"),
        log_event_url=httpserver.url_for("/v1/log_event"),
        observability_client=observability_client,
        fallback_to_statsig_api=False,
    )
    statsig = Statsig("secret-key", options)
    try:
        statsig.initialize().wait()
        assert observability_client.error_received.wait(timeout=5)
        error_event = next(m for m in observability_client.metrics if m[0] == "error")
        assert isinstance(error_event[2], str)
    finally:
        statsig.shutdown().wait()


def test_equal_lcut_repair_reports_both_high_cardinality_tags(statsig_setup):
    _, observability_client, _, expected_lcut = statsig_setup
    assert observability_client.propagation_received.wait(timeout=5)

    dist_event = next(
        m for m in observability_client.metrics
        if m[:2] == ("distribution", "statsig.sdk.config_propagation_diff")
    )
    assert isinstance(dist_event[2], float)
    tags = dist_event[3]
    assert tags["lcut"] == expected_lcut
    assert tags["prev_lcut"] == expected_lcut
