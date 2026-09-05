import json
import time
from threading import Event

import pytest
from mock_scrapi import MockScrapi
from pytest_httpserver import HTTPServer
from statsig_python_core import Statsig, StatsigOptions, StatsigUser
from utils import get_test_data_resource
from werkzeug import Response


def _check_users(statsig, user_ids, gate_name="test_rule_sampling"):
    for user_id in user_ids:
        statsig.check_gate(
            StatsigUser(f"normal-company-rate-user-{user_id}"), gate_name
        )


def _gate_exposures(mock_scrapi, gate_name="test_rule_sampling"):
    return [
        event
        for event in mock_scrapi.get_logged_events()
        if event["eventName"] == "statsig::gate_exposure"
        and event["metadata"]["gate"] == gate_name
    ]


def _is_boosted(event):
    return event.get("statsigMetadata", {}).get("samplingReason") == "rollout_boost"


@pytest.mark.parametrize("refresh_case", ("incomplete", "missing", "null"))
def test_partial_rollout_boost_fails_closed_after_incomplete_live_refresh(
    httpserver: HTTPServer,
    refresh_case: str,
):
    live_gate_name = f"test_rule_sampling_live_refresh_{refresh_case}"
    initial_specs = json.loads(get_test_data_resource("dcs_with_sampling.json"))
    rule = initial_specs["feature_gates"]["test_rule_sampling"]["rules"][0]
    rule["passPercentage"] = 50
    initial_specs.setdefault("sdk_configs", {}).update(
        {
            "sampling_mode": "on",
            "rollout_boost_enabled": 1,
            "rollout_boost_duration_seconds": 3_600,
            "rollout_boost_window_seconds": 300,
            "rollout_boost_per_rollout_limit": 8,
            "rollout_boost_global_limit": 100,
            "rollout_boost_max_rollouts": 1,
            "rollout_boost_rules": json.dumps(
                {
                    live_gate_name: {
                        rule["id"]: [
                            time.time_ns() // 1_000_000,
                            rule["passPercentage"],
                        ]
                    }
                }
            ),
        }
    )
    initial_specs["feature_gates"][live_gate_name] = initial_specs["feature_gates"].pop(
        "test_rule_sampling"
    )
    updated_specs = json.loads(json.dumps(initial_specs))
    updated_specs["time"] = initial_specs["time"] + 1
    if refresh_case == "missing":
        updated_specs.pop("sdk_configs")
    elif refresh_case == "null":
        updated_specs["sdk_configs"] = None
    else:
        updated_specs["sdk_configs"].pop("rollout_boost_global_limit")

    allow_background_refresh = Event()
    incomplete_config_applied = Event()
    specs_request_count = 0

    def respond_with_specs(_request):
        nonlocal specs_request_count
        specs_request_count += 1
        if specs_request_count == 1:
            specs = initial_specs
        else:
            allow_background_refresh.wait(timeout=4.0)
            specs = updated_specs
        return Response(json.dumps(specs), content_type="application/json")

    httpserver.expect_request(
        "/v2/download_config_specs", method="GET"
    ).respond_with_handler(respond_with_specs)

    mock_scrapi = MockScrapi(httpserver)
    mock_scrapi.stub("/v1/log_event", response='{"success": true}', method="POST")

    options = StatsigOptions(
        specs_url=httpserver.url_for("/v2/download_config_specs"),
        log_event_url=httpserver.url_for("/v1/log_event"),
        specs_sync_interval_ms=1000,
    )
    options.output_log_level = "none"
    statsig = Statsig("secret-key", options)

    def record_specs_update(event):
        if event["data"]["values"]["time"] == updated_specs["time"]:
            incomplete_config_applied.set()

    statsig.subscribe("specs_updated", record_specs_update)

    try:
        statsig.initialize().wait()

        _check_users(statsig, range(8), live_gate_name)
        statsig.flush_events().wait()
        initial_events = _gate_exposures(mock_scrapi, live_gate_name)
        initial_boosted = [event for event in initial_events if _is_boosted(event)]
        assert 0 < len(initial_boosted) < 8
        assert any(not _is_boosted(event) for event in initial_events)
        for event in initial_boosted:
            assert event["statsigMetadata"]["samplingMode"] == "on"
            assert event["statsigMetadata"]["samplingRate"] == 1
            assert "rollout_start_time" not in event["statsigMetadata"]
            assert event["metadata"]["gate"] == live_gate_name
            assert event["metadata"]["ruleID"]

        mock_scrapi.reset()
        allow_background_refresh.set()
        assert incomplete_config_applied.wait(timeout=4.0)
        assert specs_request_count >= 2

        _check_users(statsig, range(8, 72), live_gate_name)
        statsig.flush_events().wait()
        assert not any(_is_boosted(event) for event in mock_scrapi.get_logged_events())
    finally:
        allow_background_refresh.set()
        statsig.shutdown().wait()
