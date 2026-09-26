import copy
import json

import pytest
from mock_scrapi import MockScrapi
from statsig_python_core import (
    BulkEvaluationOptions,
    DynamicConfigEvaluationOptions,
    ExperimentEvaluationOptions,
    FeatureGateEvaluationOptions,
    LayerEvaluationOptions,
    Statsig,
    StatsigOptions,
    StatsigUser,
)
from utils import get_test_data_resource


@pytest.fixture
def targeting_setup(httpserver, request):
    target, percentage, id_type, disable_all = getattr(
        request, "param", ("Treatment", 100, "userID", False)
    )
    specs = json.loads(get_test_data_resource("eval_proj_dcs.json"))
    public_gate = copy.deepcopy(specs["feature_gates"]["test_public"])
    gate = copy.deepcopy(public_gate)
    gate["rules"][0].update(
        conditions=["experiment_target"], passPercentage=percentage
    )
    nested_gate = copy.deepcopy(public_gate)
    nested_gate["rules"][0]["conditions"] = ["parent_gate_target"]

    source = copy.deepcopy(specs["dynamic_configs"]["test_experiment_no_targeting"])
    source["idType"] = id_type
    source["rules"] = [
        {
            "name": "treatment",
            "id": "treatment",
            "groupName": "Treatment",
            "salt": "treatment",
            "passPercentage": 100,
            "conditions": ["source_gate_target"],
            "returnValue": {"value": "treatment"},
            "idType": id_type,
            "isExperimentGroup": True,
        }
    ]
    experiment = copy.deepcopy(source)
    experiment["rules"][0]["conditions"] = ["experiment_target"]
    config = copy.deepcopy(experiment)
    config["entity"] = "dynamic_config"
    config["rules"][0]["isExperimentGroup"] = False
    layer = copy.deepcopy(config)
    layer.update(type="layer", entity="layer", explicitParameters=["value"])

    specs["feature_gates"] = {
        "source_gate": public_gate,
        "parent_gate": gate,
        "nested_parent_gate": nested_gate,
    }
    specs["dynamic_configs"] = {
        "source_experiment": source,
        "parent_experiment": experiment,
        "parent_config": config,
    }
    specs["layer_configs"] = {"parent_layer": layer}
    specs["experiment_to_layer"] = {}
    specs["condition_map"]["experiment_target"] = {
        "type": "experiment_group",
        "targetValue": [target],
        "operator": "any",
        "field": "source_experiment",
        "additionalValues": {"experiment_name": "source_experiment"},
        "idType": id_type,
    }
    for condition, name in (
        ("source_gate_target", "source_gate"),
        ("parent_gate_target", "parent_gate"),
    ):
        specs["condition_map"][condition] = {
            "type": "pass_gate",
            "targetValue": name,
            "operator": None,
            "field": None,
            "additionalValues": {},
            "idType": id_type,
        }
    specs.pop("checksum", None)
    mock = MockScrapi(httpserver)
    mock.stub("/v2/download_config_specs", response=json.dumps(specs), method="GET")
    mock.stub("/v1/log_event", response='{"success":true}', method="POST")
    sdk = Statsig(
        "secret-test-key",
        StatsigOptions(
            specs_url=mock.url_for_endpoint("/v2/download_config_specs"),
            log_event_url=mock.url_for_endpoint("/v1/log_event"),
            fallback_to_statsig_api=False,
            enable_id_lists=False,
            disable_all_logging=disable_all,
            output_log_level="none",
        ),
    )
    sdk.initialize().wait()
    user = StatsigUser(
        "targeting-user" if id_type == "userID" else "",
        custom_ids={"stableID": "targeting-stable-id"},
    )
    yield sdk, mock, user
    sdk.shutdown().wait()


def exposure_events(mock):
    return [
        event
        for event in mock.get_logged_events()
        if event["eventName"]
        in {
            "statsig::gate_exposure",
            "statsig::config_exposure",
            "statsig::layer_exposure",
        }
    ]


def assert_direct_experiment_logs(sdk, mock, user):
    before = len(exposure_events(mock))
    experiment = sdk.get_experiment(user, "source_experiment")
    assert experiment.get_string("value", "missing") == "treatment"
    sdk.flush_events().wait()
    events = exposure_events(mock)
    assert len(events) == before + 1
    event = events[-1]
    assert event["eventName"] == "statsig::config_exposure"
    assert event["metadata"]["config"] == "source_experiment"
    assert event["metadata"]["ruleID"] == "treatment"
    assert any(item["gate"] == "source_gate" for item in event["secondaryExposures"])


@pytest.mark.parametrize(
    "targeting_setup,method,name,disabled,expected",
    [
        (
            ("Treatment", 100, "userID", False),
            "get_feature_gate", "parent_gate", False, True,
        ),
        (
            ("Treatment", 100, "userID", False),
            "get_feature_gate", "parent_gate", True, True,
        ),
        (("Treatment", 100, "userID", False), "check_gate", "parent_gate", True, True),
        (("Treatment", 0, "userID", False), "check_gate", "parent_gate", False, False),
        (
            ("Other", 100, "stableID", False),
            "get_feature_gate", "parent_gate", False, False,
        ),
        (
            ("Treatment", 100, "stableID", False),
            "check_gate", "nested_parent_gate", False, True,
        ),
    ],
    indirect=["targeting_setup"],
)
def test_gate_targeting_is_not_experiment_participation(
    targeting_setup, method, name, disabled, expected
):
    sdk, mock, user = targeting_setup
    result = getattr(sdk, method)(
        user, name, FeatureGateEvaluationOptions(disable_exposure_logging=disabled)
    )
    assert (result if method == "check_gate" else result.value) is expected
    sdk.flush_events().wait()
    events = exposure_events(mock)
    assert len(events) == (0 if disabled else 1)
    if not disabled:
        assert events[0]["eventName"] == "statsig::gate_exposure"
        assert events[0]["metadata"]["gate"] == name
    assert_direct_experiment_logs(sdk, mock, user)


@pytest.mark.parametrize("kind", ["config", "experiment", "layer"])
@pytest.mark.parametrize("disabled", [False, True])
def test_other_parent_targeting_is_not_experiment_participation(
    targeting_setup, kind, disabled
):
    sdk, mock, user = targeting_setup
    method, options = {
        "config": (sdk.get_dynamic_config, DynamicConfigEvaluationOptions),
        "experiment": (sdk.get_experiment, ExperimentEvaluationOptions),
        "layer": (sdk.get_layer, LayerEvaluationOptions),
    }[kind]
    parent = method(
        user, f"parent_{kind}", options(disable_exposure_logging=disabled)
    )
    if kind == "layer":
        sdk.flush_events().wait()
        assert exposure_events(mock) == []
    assert parent.get_string("value", "missing") == "treatment"
    sdk.flush_events().wait()
    events = exposure_events(mock)
    assert len(events) == (0 if disabled else 1)
    if not disabled:
        assert events[0]["metadata"]["config"] == f"parent_{kind}"
        assert events[0]["eventName"] == (
            "statsig::layer_exposure" if kind == "layer" else "statsig::config_exposure"
        )
    assert_direct_experiment_logs(sdk, mock, user)


@pytest.mark.parametrize("kind", ["gate", "config", "experiment", "layer"])
@pytest.mark.parametrize("release", [False, True])
def test_bulk_targeting_does_not_log_or_reserve_source_exposure(
    targeting_setup, kind, release
):
    sdk, mock, user = targeting_setup
    filters = {
        "feature_gate_filter": [],
        "dynamic_config_filter": [],
        "experiment_filter": [],
        "layer_filter": [],
    }
    filter_name, section = {
        "gate": ("feature_gate_filter", "feature_gates"),
        "config": ("dynamic_config_filter", "dynamic_configs"),
        "experiment": ("experiment_filter", "experiments"),
        "layer": ("layer_filter", "layer_configs"),
    }[kind]
    filters[filter_name] = [f"parent_{kind}"]
    parent = sdk.bulk_evaluate(user, BulkEvaluationOptions(**filters))[section][
        f"parent_{kind}"
    ]
    assert parent["value"] == (True if kind == "gate" else {"value": "treatment"})
    token = parent["exposureToken"]
    assert token is not None
    sdk.flush_events().wait()
    assert exposure_events(mock) == []

    if release:
        assert sdk.release_delayed_exposure(token)
    elif kind == "layer":
        assert sdk.log_delayed_layer_parameter_exposure(token, "value")
        assert sdk.log_delayed_layer_parameter_exposure(token, "value")
    else:
        assert sdk.log_delayed_exposure(token)
        assert not sdk.log_delayed_exposure(token)
    sdk.flush_events().wait()
    events = exposure_events(mock)
    assert len(events) == (0 if release else 1)
    if not release:
        key = "gate" if kind == "gate" else "config"
        assert events[0]["metadata"][key] == f"parent_{kind}"
    assert_direct_experiment_logs(sdk, mock, user)


@pytest.mark.parametrize(
    "targeting_setup",
    [("Treatment", 100, "userID", False), ("Treatment", 100, "stableID", False)],
    indirect=True,
)
def test_unfiltered_bulk_retains_explicit_experiment_token(targeting_setup):
    sdk, mock, user = targeting_setup
    result = sdk.bulk_evaluate(user, BulkEvaluationOptions())
    sdk.flush_events().wait()
    assert exposure_events(mock) == []
    source = result["experiments"]["source_experiment"]
    assert source["value"] == {"value": "treatment"}
    assert source["exposureToken"] is not None
    parent_token = result["feature_gates"]["parent_gate"]["exposureToken"]
    assert sdk.log_delayed_exposure(parent_token)
    sdk.flush_events().wait()
    assert [event["eventName"] for event in exposure_events(mock)] == [
        "statsig::gate_exposure"
    ]
    assert sdk.log_delayed_exposure(source["exposureToken"])
    sdk.flush_events().wait()
    events = exposure_events(mock)
    assert len(events) == 2
    assert events[-1]["eventName"] == "statsig::config_exposure"
    assert events[-1]["metadata"]["config"] == "source_experiment"


@pytest.mark.parametrize(
    "targeting_setup", [("Treatment", 100, "stableID", True)], indirect=True
)
def test_disabled_logging_bulk_keeps_values_without_exposure_tokens(targeting_setup):
    sdk, mock, user = targeting_setup
    result = sdk.bulk_evaluate(user, BulkEvaluationOptions())
    assert result["feature_gates"]["parent_gate"]["value"] is True
    assert result["experiments"]["source_experiment"]["value"] == {"value": "treatment"}
    for section in ("feature_gates", "dynamic_configs", "experiments", "layer_configs"):
        assert all(item["exposureToken"] is None for item in result[section].values())
    sdk.flush_events().wait()
    assert mock.get_logged_events() == []
