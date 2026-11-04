import copy
import importlib
import json
from unittest.mock import patch

import pytest
from mock_scrapi import MockScrapi
from statsig_python_core import (
    BulkEvaluationOptions,
    DynamicConfigEvaluationOptions,
    EvaluationCache,
    Statsig,
    StatsigOptions,
    StatsigUser,
    StatsigUserContext,
)
from statsig_python_core._frozen_json import _deep_freeze, _FrozenDict, _FrozenList
from utils import get_test_data_resource


@pytest.fixture(params=["off", "on", "oversized"])
def sdk_and_cache(request):
    mode = request.param
    cache = None
    if mode == "on":
        cache = EvaluationCache()
    elif mode == "oversized":
        cache = EvaluationCache(max_entry_bytes=1)
    sdk = Statsig(
        "secret-frozen-dynamic-configs",
        StatsigOptions(
            disable_network=True,
            disable_all_logging=True,
            evaluation_cache=cache,
        ),
    )
    sdk.initialize().wait()
    try:
        yield sdk, cache, mode
    finally:
        sdk.shutdown().wait()


def _read_value(sdk, path, freeze):
    if path == "bulk":
        kwargs = {"dynamic_config_filter": ["config"]}
        if freeze is not None:
            kwargs["freeze_dynamic_configs"] = freeze
        options = BulkEvaluationOptions(**kwargs)
        return sdk.bulk_evaluate(StatsigUser("user"), options)["dynamic_configs"][
            "config"
        ]["value"]
    options = (
        None if freeze is None else DynamicConfigEvaluationOptions(freeze_value=freeze)
    )
    if path == "context":
        return sdk.get_dynamic_config_with_context(
            StatsigUserContext(custom={"context": "snapshot"}),
            "config",
            "user",
            options=options,
        ).value
    return sdk.get_dynamic_config(StatsigUser("user"), "config", options).value


@pytest.fixture(params=["override", "archived"])
def sdk_with_nested_config(request, httpserver):
    payload = {
        "nested": {
            "items": [
                1,
                {"enabled": True, "nothing": None, "ratio": 1.5, "text": "résumé"},
            ]
        },
        "empty_mapping": {},
        "empty_list": [],
    }
    if request.param == "archived":
        specs = json.loads(get_test_data_resource("eval_proj_dcs.json"))
        specs["dynamic_configs"]["config"] = {
            **specs["dynamic_configs"]["big_number"],
            "defaultValue": payload,
            "rules": [],
        }
        for category, name in (
            ("dynamic_configs", "experiment_with_many_params"),
            ("layer_configs", "layer_with_many_params"),
        ):
            specs[category][name]["defaultValue"] = payload
            specs[category][name]["rules"] = []
        httpserver.expect_request("/v2/download_config_specs").respond_with_json(specs)
        options = StatsigOptions(
            specs_url=httpserver.url_for("/v2/download_config_specs"),
            disable_all_logging=True,
        )
    else:
        options = StatsigOptions(disable_network=True, disable_all_logging=True)
    sdk = Statsig("secret-frozen-native-conversion", options)
    sdk.initialize().wait()
    if request.param == "override":
        sdk.override_dynamic_config("config", payload)
        sdk.override_experiment("experiment_with_many_params", payload)
        sdk.override_layer("layer_with_many_params", payload)
    try:
        yield sdk, payload
    finally:
        sdk.shutdown().wait()


@pytest.mark.parametrize("path", ["normal", "context", "bulk"])
def test_uncached_frozen_conversion_skips_python_tree_walk_and_constructors(
    sdk_with_nested_config, path
):
    sdk, payload = sdk_with_nested_config
    module = importlib.import_module("statsig_python_core.statsig")

    def finish_frozen_value(value):
        # The public API may retain its final identity check, but native
        # conversion must have frozen every container before reaching Python.
        assert type(value) is _FrozenDict
        return _deep_freeze(value)

    with (
        patch.object(module, "_deep_freeze", side_effect=finish_frozen_value) as finish,
        patch(
            "statsig_python_core._frozen_json._deep_freeze",
            side_effect=AssertionError("recursive Python freezing must not run"),
        ),
        patch.object(
            _FrozenDict,
            "__new__",
            side_effect=AssertionError("public dict constructor must not run"),
        ),
        patch.object(
            _FrozenList,
            "__new__",
            side_effect=AssertionError("public list constructor must not run"),
        ),
    ):
        first = _read_value(sdk, path, True)
        second = _read_value(sdk, path, True)
    assert finish.call_count == 2
    assert first == second == payload
    assert first is not second
    assert type(first["nested"]) is _FrozenDict
    assert type(first["nested"]["items"]) is _FrozenList
    assert type(first["nested"]["items"][1]) is _FrozenDict
    assert type(first["empty_mapping"]) is _FrozenDict
    assert type(first["empty_list"]) is _FrozenList
    assert copy.deepcopy(first) is first
    assert json.loads(json.dumps(first)) == payload
    with pytest.raises(TypeError, match="immutable"):
        first["nested"]["items"].append(2)


@pytest.mark.parametrize("sdk_and_cache", ["on", "oversized"], indirect=True)
@pytest.mark.parametrize("path", ["normal", "context", "bulk"])
def test_freezing_preserves_sdk_cache_sizing_and_admission(sdk_and_cache, path):
    sdk, cache, mode = sdk_and_cache
    payload = {"nested": {"items": [1]}}
    sdk.override_dynamic_config("config", payload)
    module = importlib.import_module("statsig_python_core.evaluation_cache")
    original_measure = module._deep_freeze_and_measure
    original_estimate = module._estimated_deep_size

    def estimate_mutable_conversion(value, limit):
        assert type(value) is dict
        return original_estimate(value, limit)

    def measure_mutable_conversion(value):
        # With the SDK cache enabled, its existing sizing/admission path owns
        # freezing; a native pre-freeze would add work before this traversal.
        assert type(value) is dict
        return original_measure(value)

    with (
        patch.object(
            module, "_deep_freeze_and_measure", side_effect=measure_mutable_conversion
        ) as measure,
        patch.object(
            module, "_estimated_deep_size", side_effect=estimate_mutable_conversion
        ) as estimate,
    ):
        first = _read_value(sdk, path, True)
        second = _read_value(sdk, path, True)
    assert first == second == payload
    if mode == "on":
        assert estimate.call_count == 1
        assert measure.call_count == 1
        assert first is second
        assert cache.entry_count == 1
        assert cache.estimated_size_bytes > 0
        assert cache.misses == cache.hits == 1
    else:
        assert estimate.call_count == 2
        assert measure.call_count == 0
        assert first is not second
        assert cache.entry_count == 0
        assert cache.estimated_size_bytes == 0
        assert cache.oversized_bypasses == 2


def test_mixed_bulk_frozen_config_does_not_freeze_other_families_with_same_value(
    sdk_with_nested_config,
):
    sdk, payload = sdk_with_nested_config
    result = sdk.bulk_evaluate(
        StatsigUser("user"),
        BulkEvaluationOptions(
            dynamic_config_filter=["config"],
            experiment_filter=["experiment_with_many_params"],
            layer_filter=["layer_with_many_params"],
            freeze_dynamic_configs=True,
        ),
    )
    config = result["dynamic_configs"]["config"]["value"]
    experiment = result["experiments"]["experiment_with_many_params"]["value"]
    layer = result["layer_configs"]["layer_with_many_params"]["value"]
    assert config == experiment == layer == payload
    assert type(config) is _FrozenDict
    assert type(experiment) is type(layer) is dict
    assert experiment is not layer
    for value in (experiment, layer):
        assert type(value["nested"]["items"]) is list
        value["nested"]["items"].append("mutable")
    assert config == payload
    assert (
        sdk.get_experiment(StatsigUser("user"), "experiment_with_many_params").value
        == payload
    )
    assert (
        sdk.get_layer(StatsigUser("user"), "layer_with_many_params").get_value()
        == payload
    )
    control = _read_value(sdk, "bulk", False)
    assert type(control) is dict
    control["nested"]["items"].append("mutable")
    assert config == payload


@pytest.mark.parametrize("path", ["normal", "context", "bulk"])
@pytest.mark.parametrize(
    "freeze", [None, False, True], ids=["unset", "disabled", "enabled"]
)
@pytest.mark.parametrize(
    "payload", [{}, {"nested": {"items": [1]}}], ids=["empty", "nested"]
)
def test_freezing_is_per_evaluation_and_independent_of_cache_admission(
    sdk_and_cache, path, freeze, payload
):
    sdk, cache, mode = sdk_and_cache
    sdk.override_dynamic_config("config", payload)
    module = importlib.import_module("statsig_python_core.statsig")
    with patch.object(module, "_deep_freeze", wraps=_deep_freeze) as freezer:
        first = _read_value(sdk, path, freeze)
        second = _read_value(sdk, path, freeze)
    assert freezer.call_count == (2 if freeze is True else 0)
    assert first == second == payload
    assert json.loads(json.dumps(first)) == payload
    assert (first is second) is (mode == "on")
    if freeze is True or mode == "on":
        assert isinstance(first, _FrozenDict)
        assert copy.deepcopy(first) is first
        with pytest.raises(TypeError, match="immutable"):
            first["mutated"] = True
        if payload:
            with pytest.raises(TypeError, match="immutable"):
                first["nested"]["items"].append(2)
    else:
        assert type(first) is dict
        first["mutated"] = True
        assert second == payload
    if mode == "oversized":
        assert cache.oversized_bypasses >= 2
        assert cache.entry_count == 0


def test_bulk_freezes_only_dynamic_configs(sdk_and_cache):
    sdk, _, mode = sdk_and_cache
    payload = {"nested": {"items": [1]}}
    sdk.override_dynamic_config("config", payload)
    sdk.override_experiment("experiment", payload)
    sdk.override_layer("layer", payload)
    result = sdk.bulk_evaluate(
        StatsigUser("user"),
        BulkEvaluationOptions(
            dynamic_config_filter=["config"],
            experiment_filter=["experiment"],
            layer_filter=["layer"],
            freeze_dynamic_configs=True,
        ),
    )
    config = result["dynamic_configs"]["config"]["value"]
    experiment = result["experiments"]["experiment"]["value"]
    layer = result["layer_configs"]["layer"]["value"]
    with pytest.raises(TypeError, match="immutable"):
        config["nested"]["items"].append(2)
    for value in (experiment, layer):
        if mode == "on":
            with pytest.raises(TypeError, match="immutable"):
                value["nested"]["items"].append(2)
        else:
            value["nested"]["items"].append(2)
    assert config == payload


@pytest.mark.parametrize("sdk_and_cache", ["off"], indirect=True)
@pytest.mark.parametrize("path", ["normal", "context", "bulk"])
def test_opt_out_on_a_later_read_returns_mutable_values(sdk_and_cache, path):
    sdk = sdk_and_cache[0]
    sdk.override_dynamic_config("config", {"nested": {"items": [1]}})
    frozen = _read_value(sdk, path, True)
    control = _read_value(sdk, path, False)
    control["nested"]["items"].append(2)
    assert frozen == {"nested": {"items": [1]}}
    assert _read_value(sdk, path, None) == frozen


@pytest.mark.parametrize("path", ["normal", "context", "bulk"])
def test_freezing_preserves_old_snapshots_after_override_changes(sdk_and_cache, path):
    sdk = sdk_and_cache[0]
    sdk.override_dynamic_config("config", {"items": [1]})
    previous = _read_value(sdk, path, True)
    sdk.override_dynamic_config("config", {"items": [2]})
    current = _read_value(sdk, path, True)
    assert previous == {"items": [1]}
    assert current == {"items": [2]}
    assert previous is not current


@pytest.mark.parametrize("value", [None, 1, "true", [], {}])
def test_freeze_options_reject_non_boolean_values(value):
    with pytest.raises(TypeError):
        DynamicConfigEvaluationOptions(freeze_value=value)
    with pytest.raises(TypeError):
        BulkEvaluationOptions(freeze_dynamic_configs=value)


@pytest.mark.parametrize("path", ["normal", "context", "bulk"])
@pytest.mark.parametrize(
    "freeze", [None, False, True], ids=["unset", "disabled", "enabled"]
)
def test_missing_configs_preserve_empty_values_and_caller_defaults(
    sdk_and_cache, path, freeze
):
    sdk, cache, _ = sdk_and_cache
    if path == "bulk":
        kwargs = {"dynamic_config_filter": ["missing"]}
        if freeze is not None:
            kwargs["freeze_dynamic_configs"] = freeze
        evaluation = sdk.bulk_evaluate(
            StatsigUser("user"), BulkEvaluationOptions(**kwargs)
        )["dynamic_configs"]["missing"]
        if freeze is not True:
            assert "value" not in evaluation
            return
        value = evaluation["value"]
        get_param = value.get
    else:
        options = (
            None
            if freeze is None
            else DynamicConfigEvaluationOptions(freeze_value=freeze)
        )
        if path == "context":
            evaluation = sdk.get_dynamic_config_with_context(
                StatsigUserContext(), "missing", "user", options=options
            )
        else:
            evaluation = sdk.get_dynamic_config(StatsigUser("user"), "missing", options)
        value = evaluation.value
        get_param = evaluation.get
    assert value == {}
    if freeze is True:
        assert isinstance(value, _FrozenDict)
        with pytest.raises(TypeError, match="immutable"):
            value["mutated"] = True
    else:
        value["mutated"] = True
    empty_default = {}
    assert get_param("missing", empty_default) is empty_default
    default = {"items": []}
    assert get_param("missing", default) is default
    default["items"].append(1)
    if cache is not None:
        assert cache.entry_count == 0


@pytest.mark.parametrize("freeze", [False, True])
@pytest.mark.parametrize("disable_exposure_logging", [False, True])
def test_freezing_preserves_config_exposure_logging(
    httpserver, freeze, disable_exposure_logging
):
    scrapi = MockScrapi(httpserver)
    scrapi.stub(
        "/v2/download_config_specs",
        response=get_test_data_resource("eval_proj_dcs.json"),
    )
    scrapi.stub("/v1/log_event", response='{"success": true}', method="POST")
    sdk = Statsig(
        "secret-frozen-config-exposures",
        StatsigOptions(
            specs_url=scrapi.url_for_endpoint("/v2/download_config_specs"),
            log_event_url=scrapi.url_for_endpoint("/v1/log_event"),
            output_log_level="none",
        ),
    )
    sdk.initialize().wait()
    try:
        sdk.get_dynamic_config(
            StatsigUser("exposure-user"),
            "big_number",
            DynamicConfigEvaluationOptions(
                freeze_value=freeze,
                disable_exposure_logging=disable_exposure_logging,
            ),
        )
        sdk.flush_events().wait()
        events = [
            event
            for event in scrapi.get_logged_events()
            if event["eventName"] == "statsig::config_exposure"
        ]
        assert len(events) == (0 if disable_exposure_logging else 1)
        if events:
            assert events[0]["user"]["userID"] == "exposure-user"
            assert events[0]["metadata"]["config"] == "big_number"
    finally:
        sdk.shutdown().wait()
