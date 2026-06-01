import gc
import json
from threading import Event
from time import monotonic, sleep
from weakref import ref

from pytest_httpserver import HTTPServer
from statsig_python_core import Statsig, StatsigOptions, StatsigUser
from werkzeug import Response

from utils import get_test_data_resource


def test_subscribe_receives_gate_event():
    statsig = Statsig("secret-key")
    received_events = []

    try:
        statsig.subscribe("gate_evaluated", received_events.append)

        statsig.check_gate(StatsigUser("a-user"), "test_gate")

        assert len(received_events) == 1
        event = received_events[0]
        assert event["event_name"] == "gate_evaluated"
        assert event["data"]["gate_name"] == "test_gate"
        assert event["data"]["reason"] == "Uninitialized"
    finally:
        statsig.shutdown().wait()


def test_subscribe_receives_specs_updated_event(httpserver: HTTPServer):
    dcs_content = get_test_data_resource("eval_proj_dcs.json")
    json_data = json.loads(dcs_content)

    httpserver.expect_request(
        "/v2/download_config_specs/secret-key.json"
    ).respond_with_json(json_data)
    httpserver.expect_request("/v1/log_event").respond_with_json({"success": True})

    options = StatsigOptions(
        specs_url=httpserver.url_for("/v2/download_config_specs"),
        log_event_url=httpserver.url_for("/v1/log_event"),
    )
    statsig = Statsig("secret-key", options)
    received_events = []

    try:
        statsig.subscribe("specs_updated", received_events.append)

        statsig.initialize().wait()

        assert received_events
        event = received_events[0]
        assert event["event_name"] == "specs_updated"
        assert "values" in event["data"]
        assert isinstance(event["data"]["values"]["time"], int)
    finally:
        statsig.shutdown().wait()


def test_subscribe_receives_internal_sdk_configs_updated_event(
    httpserver: HTTPServer,
):
    dcs_content = get_test_data_resource("dcs_with_sdk_configs.json")
    json_data = json.loads(dcs_content)

    httpserver.expect_request(
        "/v2/download_config_specs/secret-key.json"
    ).respond_with_json(json_data)
    httpserver.expect_request("/v1/log_event").respond_with_json({"success": True})

    options = StatsigOptions(
        specs_url=httpserver.url_for("/v2/download_config_specs"),
        log_event_url=httpserver.url_for("/v1/log_event"),
    )
    statsig = Statsig("secret-key", options)
    received_events = []

    try:
        statsig.subscribe(
            "__internal_sdk_configs_updated__", received_events.append
        )

        statsig.initialize().wait()

        assert received_events
        event = received_events[0]
        assert event["event_name"] == "__internal_sdk_configs_updated__"
        assert event["data"]["sdk_configs"]["sampling_mode"] == "shadow"
    finally:
        statsig.shutdown().wait()


def test_statsig_caches_internal_sdk_configs(httpserver: HTTPServer):
    dcs_content = get_test_data_resource("dcs_with_sdk_configs.json")
    json_data = json.loads(dcs_content)

    httpserver.expect_request(
        "/v2/download_config_specs/secret-key.json"
    ).respond_with_json(json_data)
    httpserver.expect_request("/v1/log_event").respond_with_json({"success": True})

    options = StatsigOptions(
        specs_url=httpserver.url_for("/v2/download_config_specs"),
        log_event_url=httpserver.url_for("/v1/log_event"),
    )
    statsig = Statsig("secret-key", options)

    try:
        assert statsig._internal_sdk_configs == {}

        statsig.initialize().wait()

        assert statsig._internal_sdk_configs["sampling_mode"] == "shadow"
        assert statsig._internal_sdk_configs["event_queue_size"] == 1800
    finally:
        statsig.shutdown().wait()


def test_shared_statsig_caches_internal_sdk_configs(httpserver: HTTPServer):
    dcs_content = get_test_data_resource("dcs_with_sdk_configs.json")
    json_data = json.loads(dcs_content)

    httpserver.expect_request(
        "/v2/download_config_specs/secret-key.json"
    ).respond_with_json(json_data)
    httpserver.expect_request("/v1/log_event").respond_with_json({"success": True})

    options = StatsigOptions(
        specs_url=httpserver.url_for("/v2/download_config_specs"),
        log_event_url=httpserver.url_for("/v1/log_event"),
    )
    Statsig.remove_shared()
    statsig = Statsig.new_shared("secret-key", options)

    try:
        assert statsig._internal_sdk_configs == {}

        statsig.initialize().wait()

        assert statsig._internal_sdk_configs["sampling_mode"] == "shadow"
        assert statsig._internal_sdk_configs["event_queue_size"] == 1800
    finally:
        statsig.shutdown().wait()
        Statsig.remove_shared()


def test_statsig_refreshes_internal_sdk_configs_after_background_sync(
    httpserver: HTTPServer,
):
    dcs_content = get_test_data_resource("dcs_with_sdk_configs.json")
    initial_specs = json.loads(dcs_content)
    updated_specs = json.loads(dcs_content)
    updated_specs["time"] = initial_specs["time"] + 1
    updated_specs["sdk_configs"]["sampling_mode"] = "live"
    updated_specs["sdk_configs"]["event_queue_size"] = 2400

    specs_request_count = 0
    allow_background_refresh = Event()

    def respond_with_specs(_request):
        nonlocal specs_request_count
        specs_request_count += 1
        if specs_request_count == 1:
            specs = initial_specs
        else:
            allow_background_refresh.wait(timeout=2.0)
            specs = updated_specs
        return Response(json.dumps(specs), content_type="application/json")

    httpserver.expect_request(
        "/v2/download_config_specs/secret-key.json"
    ).respond_with_handler(respond_with_specs)
    httpserver.expect_request("/v1/log_event").respond_with_json({"success": True})

    options = StatsigOptions(
        specs_url=httpserver.url_for("/v2/download_config_specs"),
        log_event_url=httpserver.url_for("/v1/log_event"),
        specs_sync_interval_ms=1000,
    )
    statsig = Statsig("secret-key", options)

    try:
        statsig.initialize().wait()

        assert statsig._internal_sdk_configs["sampling_mode"] == "shadow"
        assert statsig._internal_sdk_configs["event_queue_size"] == 1800

        statsig.unsubscribe_all()
        allow_background_refresh.set()
        deadline = monotonic() + 4.0
        while monotonic() < deadline:
            if statsig._internal_sdk_configs.get("sampling_mode") == "live":
                break
            sleep(0.01)

        assert specs_request_count >= 2
        assert statsig._internal_sdk_configs["sampling_mode"] == "live"
        assert statsig._internal_sdk_configs["event_queue_size"] == 2400
    finally:
        statsig.shutdown().wait()


def test_internal_sdk_config_listener_does_not_retain_statsig():
    statsig = Statsig("secret-key")
    statsig_ref = ref(statsig)

    statsig.shutdown().wait()
    del statsig
    gc.collect()

    assert statsig_ref() is None


def test_unsubscribe_by_id_stops_callback_delivery():
    statsig = Statsig("secret-key")
    received_events = []

    try:
        subscription_id = statsig.subscribe(
            "gate_evaluated", received_events.append
        )
        statsig.unsubscribe_by_id(subscription_id)

        statsig.check_gate(StatsigUser("a-user"), "test_gate")

        assert received_events == []
    finally:
        statsig.shutdown().wait()


def test_unsubscribe_by_event_stops_callback_delivery():
    statsig = Statsig("secret-key")
    received_events = []

    try:
        statsig.subscribe("gate_evaluated", received_events.append)
        statsig.unsubscribe("gate_evaluated")

        statsig.check_gate(StatsigUser("a-user"), "test_gate")

        assert received_events == []
    finally:
        statsig.shutdown().wait()


def test_unsubscribe_all_stops_callback_delivery():
    statsig = Statsig("secret-key")
    received_events = []

    try:
        statsig.subscribe("*", received_events.append)
        statsig.subscribe("gate_evaluated", received_events.append)
        statsig.unsubscribe_all()

        statsig.check_gate(StatsigUser("a-user"), "test_gate")

        assert received_events == []
    finally:
        statsig.shutdown().wait()
