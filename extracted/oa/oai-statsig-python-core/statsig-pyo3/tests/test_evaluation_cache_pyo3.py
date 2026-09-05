import json
from collections.abc import Callable, KeysView

import pytest
from pytest_httpserver import HTTPServer
from statsig_python_core import Statsig, StatsigBasePy, StatsigOptions, StatsigUser
from statsig_python_core.evaluation_cache import (
    _VALUE_CACHE_HIT_FIELD,
    _VALUE_CACHE_KEY_FIELD,
)
from utils import get_test_data_resource


def _shared_value() -> dict:
    return {"shared": "dynamic-returnable"}


@pytest.fixture
def statsig(httpserver: HTTPServer):
    specs = json.loads(get_test_data_resource("eval_proj_dcs.json"))
    experiment = specs["dynamic_configs"]["experiment_with_many_params"]
    for rule in experiment["rules"]:
        rule["returnValue"] = _shared_value()

    httpserver.expect_request(
        "/v2/download_config_specs"
    ).respond_with_json(specs)
    httpserver.expect_request("/v1/log_event").respond_with_json({"success": True})

    instance = Statsig(
        "secret-key",
        StatsigOptions(
            specs_url=httpserver.url_for("/v2/download_config_specs"),
            log_event_url=httpserver.url_for("/v1/log_event"),
        ),
    )
    instance.initialize().wait()
    yield instance
    instance.shutdown().wait()


def _conversion_calls(
    statsig: Statsig,
    user: StatsigUser,
) -> dict[str, Callable[[KeysView[int] | None], dict]]:
    return {
        "config": lambda keys: statsig._INTERNAL_get_dynamic_config(
            user, "big_number", None, keys
        ),
        "experiment": lambda keys: statsig._INTERNAL_get_experiment(
            user,
            "experiment_with_many_params",
            None,
            None,
            keys,
        ),
        "layer": lambda keys: statsig._INTERNAL_get_layer(
            user, "layer_with_many_params", None, keys
        ),
    }


def _consume_protocol(raw: dict, cache: dict[int, dict]) -> tuple[int, bool]:
    key = raw.pop(_VALUE_CACHE_KEY_FIELD)
    hit = raw.pop(_VALUE_CACHE_HIT_FIELD)

    assert isinstance(key, int)
    assert isinstance(hit, bool)

    if hit:
        cached = cache.get(key)
        if cached is not None:
            if "value" in raw:
                assert raw["value"] is cached
            else:
                raw["value"] = cached
        else:
            # A pending bulk hit reuses an object converted earlier in the same
            # native call, before Python has admitted that value to its cache.
            assert isinstance(raw.get("value"), dict)
            cache[key] = raw["value"]
    else:
        assert isinstance(raw.get("value"), dict)
        cache[key] = raw["value"]

    return key, hit


def _stable_component(raw: dict) -> dict:
    result = dict(raw)
    result.pop("__exposure", None)
    result.pop("exposureToken", None)
    return result


def _assert_no_cache_protocol(raw: dict) -> None:
    assert _VALUE_CACHE_KEY_FIELD not in raw
    assert _VALUE_CACHE_HIT_FIELD not in raw


def test_feature_gate_conversions_do_not_participate_in_cache_protocol(statsig):
    user = StatsigUser("my_user")

    first = statsig._INTERNAL_get_feature_gate(user, "test_public")
    second = statsig._INTERNAL_get_feature_gate(user, "test_public")

    _assert_no_cache_protocol(first)
    _assert_no_cache_protocol(second)
    assert first == second
    assert first["details"] is not second["details"]


def test_evaluation_conversions_do_not_materialize_secondary_exposures(statsig):
    user = StatsigUser("my_user")

    direct = [
        statsig._INTERNAL_get_feature_gate(user, "test_public"),
        statsig._INTERNAL_get_dynamic_config(user, "big_number", None, None),
        statsig._INTERNAL_get_experiment(
            user, "experiment_with_many_params", None, None, None
        ),
        statsig._INTERNAL_get_layer(user, "layer_with_many_params", None, None),
    ]
    bulk_result = statsig._INTERNAL_bulk_evaluate(user, None, None)
    bulk = [
        evaluation
        for category in bulk_result.values()
        for evaluation in category.values()
    ]

    for evaluation in direct + bulk:
        assert "secondaryExposures" not in evaluation


def test_internal_converters_only_omit_values_when_keys_are_supplied(statsig):
    user = StatsigUser("my_user")

    for convert in _conversion_calls(statsig, user).values():
        uncached = convert(None)
        _assert_no_cache_protocol(uncached)

        cache: dict[int, dict] = {}
        first = convert(cache.keys())
        first_key, first_hit = _consume_protocol(first, cache)
        first_details = first["details"]

        second = convert(cache.keys())
        assert "value" not in second
        second_details = second["details"]
        second_key, second_hit = _consume_protocol(second, cache)

        assert first_hit is False
        assert second_hit is True
        assert second_key == first_key
        assert second["value"] is first["value"]
        assert _stable_component(second) == _stable_component(first)
        assert second_details is not first_details

        if "__exposure" in first:
            assert first["__exposure"] is not second["__exposure"]


def test_different_users_share_an_identical_dynamic_returnable(statsig):
    statsig.override_dynamic_config("big_number", {"shared": True})
    cache: dict[int, dict] = {}

    first = statsig._INTERNAL_get_dynamic_config(
        StatsigUser("first-user"), "big_number", None, cache.keys()
    )
    first_key, first_hit = _consume_protocol(first, cache)
    second = statsig._INTERNAL_get_dynamic_config(
        StatsigUser("second-user"), "big_number", None, cache.keys()
    )

    assert "value" not in second
    second_key, second_hit = _consume_protocol(second, cache)

    assert first_hit is False
    assert second_hit is True
    assert second_key == first_key
    assert second["value"] is first["value"]
    assert second["details"] is not first["details"]


def test_same_value_from_different_rules_reuses_only_the_value(statsig):
    cache: dict[int, dict] = {}
    first = statsig._INTERNAL_get_experiment(
        StatsigUser("user-in-control"),
        "experiment_with_many_params",
        None,
        None,
        cache.keys(),
    )
    first_key, first_hit = _consume_protocol(first, cache)
    second = statsig._INTERNAL_get_experiment(
        StatsigUser("user-in-test-1"),
        "experiment_with_many_params",
        None,
        None,
        cache.keys(),
    )

    assert "value" not in second
    second_key, second_hit = _consume_protocol(second, cache)

    assert first_hit is False
    assert second_hit is True
    assert second_key == first_key
    assert first["ruleID"] != second["ruleID"]
    assert first["groupName"] != second["groupName"]
    assert first["value"] == second["value"] == _shared_value()
    assert first["value"] is second["value"]
    assert first["details"] is not second["details"]


def test_same_value_is_shared_across_config_experiment_and_layer(statsig):
    user = StatsigUser("my_user")
    shared = {"cross": ["config", "experiment", "layer"]}
    statsig.override_dynamic_config("big_number", shared)
    statsig.override_experiment("experiment_with_many_params", shared)
    statsig.override_layer("layer_with_many_params", shared)
    cache: dict[int, dict] = {}

    results = []
    for convert in _conversion_calls(statsig, user).values():
        raw = convert(cache.keys())
        transferred_value = "value" in raw
        key, hit = _consume_protocol(raw, cache)
        results.append((raw, key, hit, transferred_value))

    assert [item[2] for item in results] == [False, True, True]
    assert [item[3] for item in results] == [True, False, False]
    assert len({item[1] for item in results}) == 1
    assert results[0][0]["value"] is results[1][0]["value"]
    assert results[0][0]["value"] is results[2][0]["value"]


def test_bulk_conversion_deduplicates_pending_values_and_keeps_metadata_fresh(statsig):
    user = StatsigUser("my_user")
    shared = {"bulk": {"shared": True}}
    statsig.override_dynamic_config("big_number", shared)
    statsig.override_experiment("experiment_with_many_params", shared)
    statsig.override_layer("layer_with_many_params", shared)
    cache: dict[int, dict] = {}

    first = StatsigBasePy._INTERNAL_bulk_evaluate(statsig, user, None, cache.keys())
    selected_first = [
        first["dynamic_configs"]["big_number"],
        first["experiments"]["experiment_with_many_params"],
        first["layer_configs"]["layer_with_many_params"],
    ]

    transferred = ["value" in evaluation for evaluation in selected_first]
    first_protocol = [
        _consume_protocol(evaluation, cache) for evaluation in selected_first
    ]

    assert transferred == [True, True, True]
    assert [hit for _, hit in first_protocol] == [False, True, True]
    assert len({key for key, _ in first_protocol}) == 1
    assert selected_first[0]["value"] is selected_first[1]["value"]
    assert selected_first[0]["value"] is selected_first[2]["value"]

    second = StatsigBasePy._INTERNAL_bulk_evaluate(statsig, user, None, cache.keys())
    selected_second = [
        second["dynamic_configs"]["big_number"],
        second["experiments"]["experiment_with_many_params"],
        second["layer_configs"]["layer_with_many_params"],
    ]
    assert all("value" not in evaluation for evaluation in selected_second)

    for previous, evaluation in zip(selected_first, selected_second):
        _, hit = _consume_protocol(evaluation, cache)
        assert hit is True
        assert evaluation["value"] is previous["value"]
        assert evaluation["details"] is not previous["details"]

    for evaluation in first["feature_gates"].values():
        _assert_no_cache_protocol(evaluation)
    for evaluation in second["feature_gates"].values():
        _assert_no_cache_protocol(evaluation)

    assert selected_first[2]["__exposure"] is not selected_second[2]["__exposure"]


def test_value_hashes_track_override_transitions(statsig):
    user_id = "my_user"
    user = StatsigUser(user_id)
    calls = _conversion_calls(statsig, user)
    caches: dict[str, dict[int, dict]] = {name: {} for name in calls}

    original_keys = {}
    for name, convert in calls.items():
        cache = caches[name]
        raw = convert(cache.keys())
        key, hit = _consume_protocol(raw, cache)
        assert hit is False
        original_keys[name] = key

    statsig.override_dynamic_config("big_number", {"marker": "config"}, user_id)
    statsig.override_experiment(
        "experiment_with_many_params", {"marker": "experiment"}, user_id
    )
    statsig.override_layer("layer_with_many_params", {"marker": "layer"}, user_id)

    for name, convert in calls.items():
        cache = caches[name]
        raw = convert(cache.keys())
        key, hit = _consume_protocol(raw, cache)
        assert hit is False
        assert key != original_keys[name]

    statsig.remove_dynamic_config_override("big_number", user_id)
    statsig.remove_experiment_override("experiment_with_many_params", user_id)
    statsig.remove_layer_override("layer_with_many_params", user_id)

    for name, convert in calls.items():
        cache = caches[name]
        raw = convert(cache.keys())
        assert "value" not in raw
        key, hit = _consume_protocol(raw, cache)
        assert hit is True
        assert key == original_keys[name]
