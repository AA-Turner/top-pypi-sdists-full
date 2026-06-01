from pytest_httpserver import HTTPServer
from statsig_python_core import (
    EventLoggingAdapter,
    LogEventRequest,
    Statsig,
    StatsigOptions,
    StatsigUser,
)

from mock_scrapi import MockScrapi
from utils import get_test_data_resource


class CapturingEventLoggingAdapter(EventLoggingAdapter):
    def __init__(self):
        super().__init__()
        self.requests: list[LogEventRequest] = []

    def log_events(self, request: LogEventRequest) -> bool:
        self.requests.append(request)
        return True


def test_event_logging_adapter_receives_sdk_exposures(httpserver: HTTPServer):
    mock_scrapi = MockScrapi(httpserver)
    dcs_content = get_test_data_resource("eval_proj_dcs.json")
    mock_scrapi.stub(
        "/v2/download_config_specs/secret-key.json", response=dcs_content, method="GET"
    )
    mock_scrapi.stub("/v1/log_event", response='{"success": true}', method="POST")

    adapter = CapturingEventLoggingAdapter()

    options = StatsigOptions(
        specs_url=mock_scrapi.url_for_endpoint("/v2/download_config_specs"),
        event_logging_adapter=adapter,
        output_log_level="none",
    )

    statsig = Statsig("secret-key", options)
    statsig.initialize().wait()
    try:
        user = StatsigUser("my_user")
        statsig.check_gate(user, "test_public")
        statsig.log_event(
            user,
            "custom_event",
            42,
            {
                "string": "value",
                "int": 7,
                "float": 1.5,
                "bool": True,
                "list": ["a", 2, False, None],
            },
        )
        statsig.flush_events().wait()
    finally:
        statsig.shutdown().wait()

    exposure_request = None
    exposure_events = []
    for request in adapter.requests:
        exposure_events = [
            event
            for event in request.payload["events"]
            if event.get("eventName") == "statsig::gate_exposure"
        ]
        if exposure_events:
            exposure_request = request
            break

    assert exposure_request is not None
    assert len(exposure_events) == 1
    assert exposure_events[0]["user"]["userID"] == "my_user"
    assert exposure_events[0]["metadata"]["gate"] == "test_public"
    assert exposure_request.event_count == len(exposure_request.payload["events"])
    assert exposure_request.retries == 0
    assert exposure_request.payload["statsigMetadata"]["sdkType"] == (
        "statsig-server-core-python"
    )

    custom_events = [
        event
        for request in adapter.requests
        for event in request.payload["events"]
        if event.get("eventName") == "custom_event"
    ]
    assert len(custom_events) == 1
    assert custom_events[0]["value"] == 42.0
    assert custom_events[0]["metadata"] == {
        "string": "value",
        "int": 7,
        "float": 1.5,
        "bool": True,
        "list": ["a", 2, False, None],
    }
    assert mock_scrapi.times_called_for_endpoint("/v1/log_event") == 0
