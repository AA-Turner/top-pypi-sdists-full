import inspect
import json
from types import SimpleNamespace
import pytest
from statsig_python_core import (
    BulkEvaluationOptions,
    Statsig,
    StatsigOptions,
    StatsigRandomUserID,
    StatsigUser,
)
from mock_scrapi import MockScrapi, decode_log_event_request
from utils import get_test_data_resource
from pytest_httpserver import HTTPServer


@pytest.fixture
def statsig_setup(httpserver: HTTPServer):
    mock_scrapi = MockScrapi(httpserver)
    dcs_content = get_test_data_resource("eval_proj_dcs.json")
    mock_scrapi.stub(
        "/v2/download_config_specs", response=dcs_content, method="GET"
    )
    mock_scrapi.stub("/v1/log_event", response='{"success": true}', method="POST")

    options = StatsigOptions()
    options.specs_url = mock_scrapi.url_for_endpoint("/v2/download_config_specs")
    options.log_event_url = mock_scrapi.url_for_endpoint("/v1/log_event")
    options.output_log_level = "none"

    statsig = Statsig("secret-key", options)
    statsig.initialize().wait()

    yield statsig, mock_scrapi

    # Teardown code
    statsig.shutdown().wait()


@pytest.fixture
def callsite_logging_setup(httpserver: HTTPServer):
    mock_scrapi = MockScrapi(httpserver)
    specs = json.loads(get_test_data_resource("eval_proj_dcs.json"))
    sdk_configs = specs.setdefault("sdk_configs", {})
    sdk_configs["expo_callsite_logging_experiment::test_experiment_no_targeting"] = 1
    sdk_configs["expo_callsite_logging_layer::layer_with_many_params"] = 1
    mock_scrapi.stub(
        "/v2/download_config_specs",
        response=json.dumps(specs),
        method="GET",
    )
    mock_scrapi.stub("/v1/log_event", response='{"success": true}', method="POST")

    options = StatsigOptions()
    options.specs_url = mock_scrapi.url_for_endpoint("/v2/download_config_specs")
    options.log_event_url = mock_scrapi.url_for_endpoint("/v1/log_event")
    options.output_log_level = "none"

    statsig = Statsig("secret-key", options)
    statsig.initialize().wait()

    yield statsig, mock_scrapi

    statsig.shutdown().wait()


def _assert_callsite_metadata(event, expected_function_name: str):
    metadata = event["metadata"]
    assert metadata["exposure_source_file"] == "test_exposure_logging.py"
    assert metadata["exposure_source_function"] == expected_function_name
    assert isinstance(metadata["exposure_source_line"], int)


def test_public_exposure_logging_apis_do_not_accept_metadata():
    assert "exposure_metadata" not in inspect.signature(
        Statsig.get_experiment
    ).parameters
    assert "exposure_metadata" not in inspect.signature(Statsig.get_layer).parameters
    assert "exposure_metadata" not in inspect.signature(
        Statsig.manually_log_experiment_exposure
    ).parameters
    assert "exposure_metadata" not in inspect.signature(
        Statsig.manually_log_layer_parameter_exposure
    ).parameters


@pytest.mark.parametrize("qualified_name", [None, "Caller.evaluate"])
def test_callsite_function_name_supports_python_310(
    statsig_setup, monkeypatch, qualified_name
):
    statsig, _ = statsig_setup
    code = SimpleNamespace(co_filename="/app/caller.py", co_name="evaluate")
    if qualified_name is not None:
        code.co_qualname = qualified_name
    caller = SimpleNamespace(
        f_globals={"__name__": "app.caller"},
        f_code=code,
        f_lineno=42,
        f_back=None,
    )
    monkeypatch.setattr(
        inspect, "currentframe", lambda: SimpleNamespace(f_back=caller)
    )

    assert statsig._get_exposure_callsite_metadata() == {
        "exposure_source_file": "caller.py",
        "exposure_source_function": qualified_name or "evaluate",
        "exposure_source_line": 42,
    }


def test_sdk_configs_attach_callsite_metadata_to_experiment_and_layer_exposures(
    callsite_logging_setup,
):
    statsig, mock_scrapi = callsite_logging_setup
    user = StatsigUser("callsite-user")

    statsig.get_experiment(user, "test_experiment_no_targeting")
    layer = statsig.get_layer(user, "layer_with_many_params")
    layer.get_string("a_string", "ERR")
    statsig.flush_events().wait()

    events = mock_scrapi.get_logged_events()
    experiment_event = next(
        event
        for event in events
        if event["eventName"] == "statsig::config_exposure"
        and event["metadata"]["config"] == "test_experiment_no_targeting"
    )
    layer_event = next(
        event
        for event in events
        if event["eventName"] == "statsig::layer_exposure"
        and event["metadata"]["config"] == "layer_with_many_params"
    )

    _assert_callsite_metadata(
        experiment_event,
        "test_sdk_configs_attach_callsite_metadata_to_experiment_and_layer_exposures",
    )
    _assert_callsite_metadata(
        layer_event,
        "test_sdk_configs_attach_callsite_metadata_to_experiment_and_layer_exposures",
    )


@pytest.mark.parametrize("api", ["ordinary", "context", "anonymous"])
def test_layer_callsite_opt_in_tracks_refreshes_and_current_parameter_caller(
    statsig_setup, monkeypatch, api
):
    statsig, mock_scrapi = statsig_setup
    if api == "ordinary":
        layer = statsig.get_layer(StatsigUser("refresh-user"), "layer_with_many_params")
    elif api == "context":
        layer = statsig.get_layer_with_context(
            None, "layer_with_many_params", "refresh-user"
        )
    else:
        layer = statsig.get_layer_anonymous(
            "layer_with_many_params", StatsigRandomUserID("refresh", 16)
        )
    metadata = []
    log_exposure = statsig._INTERNAL_log_layer_param_exposure

    def record_exposure(exposure, param, callsite):
        metadata.append(callsite)
        return log_exposure(exposure, param, callsite)

    monkeypatch.setattr(statsig, "_INTERNAL_log_layer_param_exposure", record_exposure)
    layer.get_object("an_object", {})
    assert metadata[-1] is None

    key = "expo_callsite_logging_layer::layer_with_many_params"
    statsig._internal_sdk_configs = {key: 1}

    def first_caller():
        return layer.get_string("a_string", "ERR")

    def second_caller():
        return layer.get_string("a_string", "ERR")

    assert first_caller() != "ERR"
    assert second_caller() != "ERR"
    assert metadata[-2]["exposure_source_function"].endswith("first_caller")
    assert metadata[-1]["exposure_source_function"].endswith("second_caller")
    assert metadata[-2]["exposure_source_line"] != metadata[-1]["exposure_source_line"]

    statsig._internal_sdk_configs.clear()
    layer.get_array("an_array", [])
    assert metadata[-1] is None
    statsig.flush_events().wait()
    events = [
        event
        for event in mock_scrapi.get_logged_events()
        if event["eventName"] == "statsig::layer_exposure"
    ]
    assert len(events) == 3
    string_event = next(
        event for event in events if event["metadata"]["parameterName"] == "a_string"
    )
    assert string_event["metadata"]["exposure_source_function"].endswith("first_caller")


def test_layer_parameter_reads_honor_live_private_metadata_overrides(
    statsig_setup, monkeypatch
):
    statsig, mock_scrapi = statsig_setup
    layer = statsig.get_layer(StatsigUser("override-user"), "layer_with_many_params")
    original_metadata = statsig._get_layer_exposure_metadata
    override = {
        "exposure_source_file": "private-layer.py",
        "exposure_source_function": "layer_override",
        "exposure_source_line": 42,
    }
    names = []

    def layer_metadata(name):
        names.append(name)
        return override

    monkeypatch.setattr(statsig, "_get_layer_exposure_metadata", layer_metadata)
    assert layer.get_string("a_string", "ERR") != "ERR"
    assert names == ["layer_with_many_params"]

    monkeypatch.setattr(statsig, "_get_layer_exposure_metadata", original_metadata)
    config_keys = []

    def config_enabled(key):
        config_keys.append(key)
        return True

    monkeypatch.setattr(statsig, "_sdk_config_enabled", config_enabled)
    monkeypatch.setattr(
        statsig,
        "_get_exposure_callsite_metadata",
        lambda: dict(override, exposure_source_function="config_override"),
    )
    assert layer.get_object("an_object", {}) != {}
    assert config_keys == ["expo_callsite_logging_layer::layer_with_many_params"]
    statsig.flush_events().wait()
    events = {
        event["metadata"]["parameterName"]: event["metadata"]
        for event in mock_scrapi.get_logged_events()
        if event["eventName"] == "statsig::layer_exposure"
    }
    assert len(events) == 2
    assert events["a_string"]["exposure_source_function"] == "layer_override"
    assert events["an_object"]["exposure_source_function"] == "config_override"


def test_layer_callsite_config_errors_still_return_value_and_log_exposure(
    statsig_setup, capsys
):
    statsig, mock_scrapi = statsig_setup
    layer = statsig.get_layer(
        StatsigUser("broken-config-user"), "layer_with_many_params"
    )

    class BrokenConfigs(dict):
        def get(self, key):
            raise RuntimeError("broken callsite config")

    statsig._internal_sdk_configs = BrokenConfigs()
    assert layer.get_string("a_string", "ERR") != "ERR"
    statsig.flush_events().wait()
    assert "broken callsite config" in capsys.readouterr().out
    events = [
        event
        for event in mock_scrapi.get_logged_events()
        if event["eventName"] == "statsig::layer_exposure"
    ]
    assert len(events) == 1
    assert "exposure_source_file" not in events[0]["metadata"]


def test_sdk_configs_attach_callsite_metadata_to_manual_exposures(
    callsite_logging_setup,
):
    statsig, mock_scrapi = callsite_logging_setup
    user = StatsigUser("manual-callsite-user")

    statsig.manually_log_experiment_exposure(user, "test_experiment_no_targeting")
    statsig.manually_log_layer_parameter_exposure(
        user,
        "layer_with_many_params",
        "a_string",
    )
    statsig.flush_events().wait()

    events = mock_scrapi.get_logged_events()
    experiment_event = next(
        event
        for event in events
        if event["eventName"] == "statsig::config_exposure"
        and event["metadata"]["config"] == "test_experiment_no_targeting"
    )
    layer_event = next(
        event
        for event in events
        if event["eventName"] == "statsig::layer_exposure"
        and event["metadata"]["config"] == "layer_with_many_params"
    )

    _assert_callsite_metadata(
        experiment_event,
        "test_sdk_configs_attach_callsite_metadata_to_manual_exposures",
    )
    _assert_callsite_metadata(
        layer_event,
        "test_sdk_configs_attach_callsite_metadata_to_manual_exposures",
    )


def test_callsite_metadata_lookup_is_skipped_without_sdk_config_opt_in(
    statsig_setup,
    monkeypatch,
):
    statsig, mock_scrapi = statsig_setup
    calls = []

    def track_callsite_lookup():
        calls.append(True)
        return {
            "exposure_source_file": "unexpected",
            "exposure_source_function": "unexpected",
            "exposure_source_line": 0,
        }

    monkeypatch.setattr(
        statsig,
        "_get_exposure_callsite_metadata",
        track_callsite_lookup,
    )

    user = StatsigUser("no-callsite-user")
    statsig.get_experiment(user, "test_experiment_no_targeting")
    layer = statsig.get_layer(user, "layer_with_many_params")
    layer.get_string("a_string", "ERR")
    statsig.manually_log_experiment_exposure(
        StatsigUser("manual-no-callsite-user"),
        "test_experiment_no_targeting",
    )
    statsig.manually_log_layer_parameter_exposure(
        StatsigUser("manual-no-layer-callsite-user"),
        "layer_with_many_params",
        "a_string",
    )
    statsig.flush_events().wait()

    assert calls == []
    for event in mock_scrapi.get_logged_events():
        assert "exposure_source_file" not in event["metadata"]
        assert "exposure_source_function" not in event["metadata"]
        assert "exposure_source_line" not in event["metadata"]


def test_shutdown_flushes(statsig_setup):
    statsig, mock_scrapi = statsig_setup

    statsig.check_gate(StatsigUser("my_user"), "test_public")
    statsig.shutdown().wait()
    events = mock_scrapi.get_logged_events()

    assert len(events) == 1
    assert events[0]["eventName"] == "statsig::gate_exposure"


def test_gate_exposures(statsig_setup):
    statsig, mock_scrapi = statsig_setup

    statsig.check_gate(StatsigUser("my_user"), "test_public")
    statsig.flush_events().wait()
    events = mock_scrapi.get_logged_events()

    assert len(events) == 1
    assert events[0]["eventName"] == "statsig::gate_exposure"


def test_bulk_evaluate_delays_gate_exposure_until_token_logged(statsig_setup):
    statsig, mock_scrapi = statsig_setup

    result = statsig.bulk_evaluate(
        StatsigUser("my_user"),
        BulkEvaluationOptions(
            feature_gate_filter=["test_public"],
            dynamic_config_filter=[],
            experiment_filter=[],
            layer_filter=[],
        ),
    )

    gate = result["feature_gates"]["test_public"]
    assert gate["value"] is True
    assert gate["exposureToken"] is not None

    statsig.flush_events().wait()
    assert mock_scrapi.get_logged_events() == []

    assert statsig.log_delayed_exposure(gate["exposureToken"]) is True
    assert statsig.log_delayed_exposure(gate["exposureToken"]) is False

    statsig.flush_events().wait()
    events = mock_scrapi.get_logged_events()

    assert len(events) == 1
    assert events[0]["eventName"] == "statsig::gate_exposure"
    assert events[0]["metadata"]["gate"] == "test_public"


def test_bulk_evaluate_delays_dynamic_config_exposure_until_token_logged(statsig_setup):
    statsig, mock_scrapi = statsig_setup
    name = "test_custom_config"
    result = statsig.bulk_evaluate(
        StatsigUser("my_user"),
        BulkEvaluationOptions(
            feature_gate_filter=[],
            dynamic_config_filter=[name],
            experiment_filter=[],
            layer_filter=[],
        ),
    )
    config = result["dynamic_configs"][name]
    assert config["value"]["header_text"] == "old user test"
    token = config["exposureToken"]
    assert token is not None

    statsig.flush_events().wait()
    assert mock_scrapi.get_logged_events() == []
    assert statsig.log_delayed_exposure(token) is True
    assert statsig.log_delayed_exposure(token) is False
    statsig.flush_events().wait()
    events = mock_scrapi.get_logged_events()
    assert len(events) == 1
    assert events[0]["eventName"] == "statsig::config_exposure"
    assert events[0]["metadata"]["config"] == name


def test_bulk_evaluate_release_drops_gate_token(statsig_setup):
    statsig, mock_scrapi = statsig_setup

    result = statsig.bulk_evaluate(
        StatsigUser("my_user"),
        BulkEvaluationOptions(
            feature_gate_filter=["test_public"],
            dynamic_config_filter=[],
            experiment_filter=[],
            layer_filter=[],
        ),
    )
    token = result["feature_gates"]["test_public"]["exposureToken"]

    assert statsig.release_delayed_exposure(token) is True
    assert statsig.log_delayed_exposure(token) is False

    statsig.flush_events().wait()
    assert mock_scrapi.get_logged_events() == []


def test_bulk_evaluate_deduped_exposure_has_no_second_token(statsig_setup):
    statsig, _ = statsig_setup

    user = StatsigUser("my_user")
    first = statsig.bulk_evaluate(
        user,
        BulkEvaluationOptions(
            feature_gate_filter=["test_public"],
            dynamic_config_filter=[],
            experiment_filter=[],
            layer_filter=[],
        ),
    )
    second = statsig.bulk_evaluate(
        user,
        BulkEvaluationOptions(
            feature_gate_filter=["test_public"],
            dynamic_config_filter=[],
            experiment_filter=[],
            layer_filter=[],
        ),
    )

    assert first["feature_gates"]["test_public"]["exposureToken"] is not None
    assert second["feature_gates"]["test_public"]["exposureToken"] is None


def test_bulk_evaluate_layer_token_logs_distinct_params_once(statsig_setup):
    statsig, mock_scrapi = statsig_setup

    result = statsig.bulk_evaluate(
        StatsigUser("my_user"),
        BulkEvaluationOptions(
            feature_gate_filter=[],
            dynamic_config_filter=[],
            experiment_filter=[],
            layer_filter=["layer_with_many_params"],
        ),
    )

    layer = result["layer_configs"]["layer_with_many_params"]
    token = layer["exposureToken"]
    assert token is not None
    assert layer["value"]["a_string"] == "test_2"

    assert statsig.log_delayed_layer_parameter_exposure(token, "a_string") is True
    assert statsig.log_delayed_layer_parameter_exposure(token, "a_string") is True
    assert statsig.log_delayed_layer_parameter_exposure(token, "another_string") is True

    statsig.flush_events().wait()
    events = mock_scrapi.get_logged_events()
    layer_events = [e for e in events if e["eventName"] == "statsig::layer_exposure"]

    assert len(layer_events) == 2
    assert {e["metadata"]["parameterName"] for e in layer_events} == {
        "a_string",
        "another_string",
    }

    assert statsig.release_delayed_exposure(token) is True
    assert statsig.log_delayed_layer_parameter_exposure(token, "a_string") is False


def test_bulk_evaluate_disable_all_logging_returns_no_tokens(httpserver: HTTPServer):
    mock_scrapi = MockScrapi(httpserver)
    dcs_content = get_test_data_resource("eval_proj_dcs.json")
    mock_scrapi.stub(
        "/v2/download_config_specs", response=dcs_content, method="GET"
    )
    mock_scrapi.stub("/v1/log_event", response='{"success": true}', method="POST")

    options = StatsigOptions()
    options.specs_url = mock_scrapi.url_for_endpoint("/v2/download_config_specs")
    options.log_event_url = mock_scrapi.url_for_endpoint("/v1/log_event")
    options.disable_all_logging = True
    options.output_log_level = "none"

    statsig = Statsig("secret-key", options)
    statsig.initialize().wait()

    result = statsig.bulk_evaluate(
        StatsigUser("my_user"),
        BulkEvaluationOptions(
            feature_gate_filter=["test_public"],
            dynamic_config_filter=[],
            experiment_filter=[],
            layer_filter=["layer_with_many_params"],
        ),
    )

    assert result["feature_gates"]["test_public"]["exposureToken"] is None
    assert result["layer_configs"]["layer_with_many_params"]["exposureToken"] is None

    statsig.shutdown().wait()


def test_layer_exposure(statsig_setup):
    statsig, mock_scrapi = statsig_setup

    layer = statsig.get_layer(StatsigUser("my_user"), "layer_with_many_params")
    statsig.flush_events().wait()

    log_requests = mock_scrapi.get_requests_for_endpoint("/v1/log_event")
    events = mock_scrapi.get_logged_events()

    assert len(log_requests) == 1
    assert len(events) == 0

    layer.get_string("a_string", "ERR")
    statsig.flush_events().wait()

    log_requests = mock_scrapi.get_requests_for_endpoint("/v1/log_event")
    events = mock_scrapi.get_logged_events()

    assert len(log_requests) == 2
    assert len(events) == 1
    assert events[0]["eventName"] == "statsig::layer_exposure"


def test_custom_event(statsig_setup):
    statsig, mock_scrapi = statsig_setup

    statsig.log_event(StatsigUser("my_user"), "my_custom_event")
    statsig.flush_events().wait()

    events = mock_scrapi.get_logged_events()
    event = events[0]

    assert len(events) == 1
    assert event["eventName"] == "my_custom_event"


def test_custom_event_with_number(statsig_setup):
    statsig, mock_scrapi = statsig_setup

    statsig.log_event(StatsigUser("my_user"), "my_custom_event_with_num", 1.23)
    statsig.flush_events().wait()

    events = mock_scrapi.get_logged_events()
    event = events[0]

    assert len(events) == 1
    assert event["eventName"] == "my_custom_event_with_num"
    assert event["value"] == 1.23


@pytest.mark.parametrize("value", ["custom value", 1.23])
def test_custom_event_with_timestamp_override(statsig_setup, value):
    statsig, mock_scrapi = statsig_setup
    timestamp = 1_700_000_000_123

    statsig.log_event(
        StatsigUser("my_user"),
        "my_custom_event_with_timestamp_override",
        value,
        timestamp_ms=timestamp,
    )
    statsig.flush_events().wait()

    events = mock_scrapi.get_logged_events()
    event = events[0]

    assert len(events) == 1
    assert event["eventName"] == "my_custom_event_with_timestamp_override"
    assert event["time"] == timestamp


def test_custom_event_with_number_and_metadata(statsig_setup):
    statsig, mock_scrapi = statsig_setup

    statsig.log_event(
        StatsigUser("my_user"), "my_custom_event_with_num", 1.23, {"some": "value"}
    )
    statsig.flush_events().wait()

    events = mock_scrapi.get_logged_events()
    event = events[0]

    assert len(events) == 1
    assert event["eventName"] == "my_custom_event_with_num"
    assert event["value"] == 1.23
    assert event["metadata"]["some"] == "value"


def test_custom_event_with_string(statsig_setup):
    statsig, mock_scrapi = statsig_setup

    statsig.log_event(StatsigUser("my_user"), "my_custom_event_with_str", "cool beans")
    statsig.flush_events().wait()

    events = mock_scrapi.get_logged_events()
    event = events[0]

    assert len(events) == 1
    assert event["eventName"] == "my_custom_event_with_str"
    assert event["value"] == "cool beans"


def test_custom_event_with_string_and_metadata(statsig_setup):
    statsig, mock_scrapi = statsig_setup

    statsig.log_event(
        StatsigUser("my_user"),
        "my_custom_event_with_str",
        "cool beans",
        {"some": "value"},
    )
    statsig.flush_events().wait()

    events = mock_scrapi.get_logged_events()
    event = events[0]

    assert len(events) == 1
    assert event["eventName"] == "my_custom_event_with_str"
    assert event["value"] == "cool beans"
    assert event["metadata"]["some"] == "value"


def test_custom_event_with_typed_metadata(statsig_setup):
    statsig, mock_scrapi = statsig_setup

    metadata = {
        "an_int": 123,
        "a_float": 1.5,
        "a_bool": True,
        "a_none": None,
        "an_object": {"nested_int": 7, "nested_str": "x"},
        "an_array": [1, "a", False, {"k": "v"}],
    }

    statsig.log_event(
        StatsigUser("my_user"),
        "my_custom_event_with_typed_metadata",
        "value",
        metadata,
    )
    statsig.flush_events().wait()

    events = mock_scrapi.get_logged_events()
    assert len(events) == 1

    event = events[0]
    assert event["eventName"] == "my_custom_event_with_typed_metadata"
    assert event["value"] == "value"

    assert event["metadata"]["an_int"] == 123
    assert event["metadata"]["a_float"] == 1.5
    assert event["metadata"]["a_bool"] is True
    assert "a_none" in event["metadata"]
    assert event["metadata"]["a_none"] is None
    assert event["metadata"]["an_object"] == {"nested_int": 7, "nested_str": "x"}
    assert event["metadata"]["an_array"] == [1, "a", False, {"k": "v"}]


def test_statsig_metadata(statsig_setup):
    statsig, mock_scrapi = statsig_setup

    statsig.check_gate(StatsigUser("my_user"), "test_public")
    statsig.flush_events().wait()
    request = mock_scrapi.get_requests_for_endpoint("/v1/log_event")[0]
    req_json = decode_log_event_request(request)
    statsig_metadata = req_json["statsigMetadata"]

    assert statsig_metadata["sdkType"] == "statsig-server-core-python"
    assert statsig_metadata["sdkVersion"] is not None
    assert statsig_metadata["sessionID"] is not None

    lang_version = statsig_metadata["languageVersion"]
    assert lang_version is not None and lang_version != "unknown"

    os = statsig_metadata["os"]
    assert os is not None and os != "unknown"

    arch = statsig_metadata["arch"]
    assert arch is not None and arch != "unknown"
