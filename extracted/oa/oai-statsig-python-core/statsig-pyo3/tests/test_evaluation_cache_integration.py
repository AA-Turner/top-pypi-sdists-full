import json

import pytest
from mock_scrapi import MockScrapi
from pytest_httpserver import HTTPServer
from statsig_python_core import (
    EvaluationCache,
    Statsig,
    StatsigOptions,
    StatsigUser,
)
from statsig_python_core.evaluation_cache import (
    _VALUE_CACHE_HIT_FIELD,
    _VALUE_CACHE_KEY_FIELD,
)
from utils import get_test_data_resource


_EVALUATION_VALUE_CASES = (
    (
        "big_number",
        "override_dynamic_config",
        "get_dynamic_config",
        "dynamic_configs",
    ),
    (
        "experiment_with_many_params",
        "override_experiment",
        "get_experiment",
        "experiments",
    ),
    (
        "layer_with_many_params",
        "override_layer",
        "get_layer",
        "layer_configs",
    ),
)
_EVALUATION_VALUE_CASE_IDS = ("dynamic-config", "experiment", "layer")
_BULK_CATEGORIES = (
    "feature_gates",
    "dynamic_configs",
    "experiments",
    "layer_configs",
)
_CACHEABLE_BULK_CATEGORIES = (
    "dynamic_configs",
    "experiments",
    "layer_configs",
)


def _nested_evaluation_value() -> dict:
    return {
        "nested": {"value": "original"},
        "items": [1, {"value": "original"}],
    }


def _mutate_top_level(value: dict) -> None:
    value["top_level"] = "mutated"


def _mutate_nested_dict(value: dict) -> None:
    value["nested"]["value"] = "mutated"


def _mutate_nested_list(value: dict) -> None:
    value["items"].append(2)


def _mutate_dict_in_list(value: dict) -> None:
    value["items"][1]["value"] = "mutated"


_VALUE_MUTATIONS = (
    _mutate_top_level,
    _mutate_nested_dict,
    _mutate_nested_list,
    _mutate_dict_in_list,
)


def _create_statsig(
    httpserver: HTTPServer,
    cache: EvaluationCache | None,
) -> Statsig:
    specs = json.loads(get_test_data_resource("eval_proj_dcs.json"))
    experiment = specs["dynamic_configs"]["experiment_with_many_params"]
    for rule in experiment["rules"]:
        rule["returnValue"] = {"shared": "across-rules"}

    httpserver.expect_request(
        "/v2/download_config_specs/secret-key.json"
    ).respond_with_json(specs)
    httpserver.expect_request("/v1/log_event").respond_with_json({"success": True})

    options_kwargs = {
        "specs_url": httpserver.url_for("/v2/download_config_specs"),
        "log_event_url": httpserver.url_for("/v1/log_event"),
    }
    if cache is not None:
        options_kwargs["evaluation_cache"] = cache

    statsig = Statsig("secret-key", StatsigOptions(**options_kwargs))
    statsig.initialize().wait()
    return statsig


@pytest.fixture
def uncached_statsig(httpserver: HTTPServer):
    statsig = _create_statsig(httpserver, None)
    yield statsig
    statsig.shutdown().wait()


@pytest.fixture
def cached_statsig(httpserver: HTTPServer):
    cache = EvaluationCache()
    statsig = _create_statsig(httpserver, cache)
    yield statsig, cache
    statsig.shutdown().wait()


@pytest.fixture
def cached_statsig_with_event_capture(httpserver: HTTPServer):
    mock_scrapi = MockScrapi(httpserver)
    mock_scrapi.stub(
        "/v2/download_config_specs/secret-key.json",
        response=get_test_data_resource("eval_proj_dcs.json"),
        method="GET",
    )
    mock_scrapi.stub("/v1/log_event", response='{"success": true}', method="POST")

    cache = EvaluationCache()
    options = StatsigOptions(evaluation_cache=cache)
    options.specs_url = mock_scrapi.url_for_endpoint("/v2/download_config_specs")
    options.log_event_url = mock_scrapi.url_for_endpoint("/v1/log_event")
    options.output_log_level = "none"

    statsig = Statsig("secret-key", options)
    statsig.initialize().wait()
    yield statsig, cache, mock_scrapi
    statsig.shutdown().wait()


def _assert_no_cache_metadata(raw: dict) -> None:
    assert _VALUE_CACHE_KEY_FIELD not in raw
    assert _VALUE_CACHE_HIT_FIELD not in raw


def _override_evaluation_value(
    statsig: Statsig,
    override_method: str,
    spec_name: str,
    user_id: str,
    value: dict | None = None,
) -> None:
    getattr(statsig, override_method)(
        spec_name,
        value if value is not None else _nested_evaluation_value(),
        user_id,
    )


def _override_all_evaluation_values(statsig: Statsig, user_id: str) -> None:
    for spec_name, override_method, _, _ in _EVALUATION_VALUE_CASES:
        _override_evaluation_value(statsig, override_method, spec_name, user_id)


def _assert_value_tree_is_deeply_immutable(value: dict) -> None:
    for mutate in _VALUE_MUTATIONS:
        with pytest.raises(TypeError, match="immutable"):
            mutate(value)


@pytest.mark.parametrize(
    ("spec_name", "override_method", "getter_method", "_bulk_category"),
    _EVALUATION_VALUE_CASES,
    ids=_EVALUATION_VALUE_CASE_IDS,
)
def test_evaluation_values_are_deeply_mutable_without_cache(
    uncached_statsig,
    spec_name,
    override_method,
    getter_method,
    _bulk_category,
):
    statsig = uncached_statsig
    user_id = "uncached-mutation-user"
    user = StatsigUser(user_id)
    _override_evaluation_value(statsig, override_method, spec_name, user_id)

    first = getattr(statsig, getter_method)(user, spec_name)
    second = getattr(statsig, getter_method)(user, spec_name)
    first_value = first.get_value()
    second_value = second.get_value()

    assert type(first_value) is dict
    assert type(first_value["nested"]) is dict
    assert type(first_value["items"]) is list
    assert first_value is not second_value
    assert first_value["nested"] is not second_value["nested"]
    assert first_value["items"] is not second_value["items"]
    assert first.get_object("nested", {}) is first_value["nested"]
    assert first.get_array("items", []) is first_value["items"]

    for mutate in _VALUE_MUTATIONS:
        mutate(first_value)

    assert first_value["top_level"] == "mutated"
    assert first_value["nested"]["value"] == "mutated"
    assert first_value["items"][-1] == 2
    assert first_value["items"][1]["value"] == "mutated"
    assert second_value == _nested_evaluation_value()


@pytest.mark.parametrize(
    ("spec_name", "override_method", "getter_method", "_bulk_category"),
    _EVALUATION_VALUE_CASES,
    ids=_EVALUATION_VALUE_CASE_IDS,
)
def test_evaluation_values_are_deeply_immutable_with_cache(
    cached_statsig,
    spec_name,
    override_method,
    getter_method,
    _bulk_category,
):
    statsig, cache = cached_statsig
    user_id = "cached-mutation-user"
    user = StatsigUser(user_id)
    _override_evaluation_value(statsig, override_method, spec_name, user_id)

    first = getattr(statsig, getter_method)(user, spec_name)
    second = getattr(statsig, getter_method)(user, spec_name)
    first_value = first.get_value()
    second_value = second.get_value()

    assert first_value == _nested_evaluation_value()
    assert first_value is second_value
    assert first.get_object("nested", {}) is first_value["nested"]
    assert first.get_array("items", []) is first_value["items"]
    assert json.loads(json.dumps(first_value)) == _nested_evaluation_value()
    assert cache.misses == 1
    assert cache.hits == 1
    assert cache.entry_count == 1
    _assert_value_tree_is_deeply_immutable(first_value)


def test_bulk_evaluation_values_remain_mutable_without_cache(uncached_statsig):
    statsig = uncached_statsig
    user_id = "uncached-bulk-mutation-user"
    user = StatsigUser(user_id)
    _override_all_evaluation_values(statsig, user_id)

    first = statsig.bulk_evaluate(user)
    second = statsig.bulk_evaluate(user)

    assert type(first) is dict
    first["__outer_mutation"] = True
    assert "__outer_mutation" not in second

    for category in _BULK_CATEGORIES:
        name, first_evaluation = next(iter(first[category].items()))
        second_evaluation = second[category][name]
        assert type(first_evaluation) is dict
        first_evaluation["__evaluation_mutation"] = True
        assert "__evaluation_mutation" not in second_evaluation
        first_evaluation["details"]["reason"] = "mutated"
        assert second_evaluation["details"]["reason"] != "mutated"

    for spec_name, _, _, category in _EVALUATION_VALUE_CASES:
        first_value = first[category][spec_name]["value"]
        second_value = second[category][spec_name]["value"]
        assert type(first_value) is dict
        assert first_value is not second_value

        for mutate in _VALUE_MUTATIONS:
            mutate(first_value)

        assert second_value == _nested_evaluation_value()


def test_bulk_evaluation_freezes_only_cached_value_trees(cached_statsig):
    statsig, _ = cached_statsig
    user_id = "cached-bulk-mutation-user"
    user = StatsigUser(user_id)
    _override_all_evaluation_values(statsig, user_id)

    first = statsig.bulk_evaluate(user)
    second = statsig.bulk_evaluate(user)

    assert type(first) is dict
    first["__outer_mutation"] = True
    assert "__outer_mutation" not in second

    for category in _CACHEABLE_BULK_CATEGORIES:
        name, first_evaluation = next(iter(first[category].items()))
        second_evaluation = second[category][name]
        assert type(first_evaluation) is dict
        first_evaluation["__evaluation_mutation"] = True
        assert "__evaluation_mutation" not in second_evaluation
        assert type(first_evaluation["details"]) is dict
        first_evaluation["details"]["reason"] = "mutated"
        assert second_evaluation["details"]["reason"] != "mutated"

    gate_name, first_gate = next(iter(first["feature_gates"].items()))
    second_gate = second["feature_gates"][gate_name]
    assert type(first_gate["details"]) is dict
    first_gate["details"]["reason"] = "mutated"
    assert second_gate["details"]["reason"] != "mutated"

    for spec_name, _, _, category in _EVALUATION_VALUE_CASES:
        first_value = first[category][spec_name]["value"]
        second_value = second[category][spec_name]["value"]
        assert first_value is second_value
        _assert_value_tree_is_deeply_immutable(first_value)


def test_cache_bypass_preserves_mutable_evaluation_values(httpserver: HTTPServer):
    cache = EvaluationCache(
        max_bytes=512,
        max_entries=4,
        max_entry_bytes=512,
    )
    statsig = _create_statsig(httpserver, cache)
    user_id = "oversized-mutation-user"
    user = StatsigUser(user_id)
    value = _nested_evaluation_value()
    value["large"] = "x" * 4096
    _override_evaluation_value(
        statsig,
        "override_dynamic_config",
        "big_number",
        user_id,
        value,
    )

    try:
        first = statsig.get_dynamic_config(user, "big_number").get_value()
        second = statsig.get_dynamic_config(user, "big_number").get_value()

        assert type(first) is dict
        assert first is not second
        assert cache.entry_count == 0
        assert cache.oversized_bypasses == 2

        for mutate in _VALUE_MUTATIONS:
            mutate(first)

        assert second == value
    finally:
        statsig.shutdown().wait()


def test_bulk_cache_bypass_detaches_shared_oversized_values(
    httpserver: HTTPServer,
):
    cache = EvaluationCache(
        max_bytes=512,
        max_entries=4,
        max_entry_bytes=512,
    )
    statsig = _create_statsig(httpserver, cache)
    user_id = "oversized-bulk-user"
    user = StatsigUser(user_id)
    value = _nested_evaluation_value()
    value["large"] = "x" * 4096

    for spec_name, override_method, _, _ in _EVALUATION_VALUE_CASES:
        _override_evaluation_value(
            statsig,
            override_method,
            spec_name,
            user_id,
            value,
        )

    try:
        bulk = statsig.bulk_evaluate(user)
        values = [
            bulk[category][spec_name]["value"]
            for spec_name, _, _, category in _EVALUATION_VALUE_CASES
        ]

        assert all(type(result) is dict for result in values)
        assert all(result == value for result in values)
        assert len({id(result) for result in values}) == len(values)
        assert cache.oversized_bypasses >= len(values)

        _mutate_nested_dict(values[0])
        assert values[1] == value
        assert values[2] == value
    finally:
        statsig.shutdown().wait()


def test_cache_is_opt_in_and_default_results_preserve_existing_behavior(
    uncached_statsig,
):
    statsig = uncached_statsig
    user = StatsigUser("my_user")

    first_gate = statsig.get_feature_gate(user, "test_public")
    first_config = statsig.get_dynamic_config(user, "big_number")
    first_experiment = statsig.get_experiment(user, "experiment_with_many_params")
    first_layer = statsig.get_layer(user, "layer_with_many_params")

    second_gate = statsig.get_feature_gate(user, "test_public")
    second_config = statsig.get_dynamic_config(user, "big_number")
    second_experiment = statsig.get_experiment(user, "experiment_with_many_params")
    second_layer = statsig.get_layer(user, "layer_with_many_params")

    assert first_gate is not second_gate
    assert first_gate.details is not second_gate.details

    value_pairs = (
        (first_config.value, second_config.value),
        (first_experiment.value, second_experiment.value),
        (first_layer.get_value(), second_layer.get_value()),
    )
    for first, second in value_pairs:
        assert type(first) is dict
        assert type(second) is dict
        assert first is not second
        first["__uncached_mutation"] = True
        assert first["__uncached_mutation"] is True
        assert "__uncached_mutation" not in second

    first_bulk = statsig.bulk_evaluate(user)
    second_bulk = statsig.bulk_evaluate(user)
    for bulk in (first_bulk, second_bulk):
        for category in (
            "feature_gates",
            "dynamic_configs",
            "experiments",
            "layer_configs",
        ):
            for evaluation in bulk[category].values():
                _assert_no_cache_metadata(evaluation)

    first_bulk_value = first_bulk["dynamic_configs"]["big_number"]["value"]
    second_bulk_value = second_bulk["dynamic_configs"]["big_number"]["value"]
    assert type(first_bulk_value) is dict
    assert first_bulk_value is not second_bulk_value
    first_bulk_value["__uncached_mutation"] = True
    assert "__uncached_mutation" not in second_bulk_value


def test_feature_gates_do_not_participate_in_the_cache(cached_statsig):
    statsig, cache = cached_statsig
    user = StatsigUser("my_user")

    first_gate = statsig.get_feature_gate(user, "test_public")
    second_gate = statsig.get_feature_gate(user, "test_public")

    assert second_gate.to_dict() == first_gate.to_dict()
    assert second_gate.details is not first_gate.details
    assert cache.misses == 0
    assert cache.hits == 0
    assert cache.entry_count == 0


def test_cache_reuses_config_experiment_and_layer_values(cached_statsig):
    statsig, cache = cached_statsig
    user = StatsigUser("my_user")
    statsig.override_dynamic_config("big_number", {"kind": "config"})
    statsig.override_experiment("experiment_with_many_params", {"kind": "experiment"})
    statsig.override_layer("layer_with_many_params", {"kind": "layer"})

    first_config = statsig.get_dynamic_config(user, "big_number")
    first_experiment = statsig.get_experiment(user, "experiment_with_many_params")
    first_layer = statsig.get_layer(user, "layer_with_many_params")

    second_config = statsig.get_dynamic_config(user, "big_number")
    second_experiment = statsig.get_experiment(user, "experiment_with_many_params")
    second_layer = statsig.get_layer(user, "layer_with_many_params")

    assert second_config.value is first_config.value
    assert second_experiment.value is first_experiment.value
    assert second_layer.get_value() is first_layer.get_value()
    assert second_config.details is not first_config.details
    assert second_experiment.details is not first_experiment.details
    assert second_layer.details is not first_layer.details

    assert cache.misses == 3
    assert cache.hits == 3
    assert cache.entry_count == 3
    assert cache.estimated_size_bytes <= cache.max_bytes

    with pytest.raises(TypeError, match="immutable"):
        second_config.value["foo"] = "changed"


def test_cache_preserves_empty_config_experiment_and_layer_values(cached_statsig):
    statsig, _ = cached_statsig
    user = StatsigUser("empty-value-user")
    statsig.override_dynamic_config("big_number", {})
    statsig.override_experiment("experiment_with_many_params", {})
    statsig.override_layer("layer_with_many_params", {})

    first_values = (
        statsig.get_dynamic_config(user, "big_number").value,
        statsig.get_experiment(user, "experiment_with_many_params").value,
        statsig.get_layer(user, "layer_with_many_params").get_value(),
    )
    second_values = (
        statsig.get_dynamic_config(user, "big_number").value,
        statsig.get_experiment(user, "experiment_with_many_params").value,
        statsig.get_layer(user, "layer_with_many_params").get_value(),
    )

    for first, second in zip(first_values, second_values):
        assert first == {}
        assert second is first
        with pytest.raises(TypeError, match="immutable"):
            second["mutation"] = True


def test_cache_shares_an_identical_value_across_users(cached_statsig):
    statsig, cache = cached_statsig
    statsig.override_dynamic_config("big_number", {"shared": True})

    first = statsig.get_dynamic_config(StatsigUser("first-user"), "big_number")
    second = statsig.get_dynamic_config(StatsigUser("second-user"), "big_number")

    assert second.value is first.value
    assert second.to_dict() == first.to_dict()
    assert second.details is not first.details
    assert cache.misses == 1
    assert cache.hits == 1
    assert cache.entry_count == 1


def test_cache_shares_a_value_across_different_rules_and_sources(cached_statsig):
    statsig, cache = cached_statsig

    first_experiment = statsig.get_experiment(
        StatsigUser("user-in-control"), "experiment_with_many_params"
    )
    second_experiment = statsig.get_experiment(
        StatsigUser("user-in-test-1"), "experiment_with_many_params"
    )

    assert second_experiment.value is first_experiment.value
    assert second_experiment.rule_id != first_experiment.rule_id
    assert second_experiment.group_name != first_experiment.group_name
    assert second_experiment.details is not first_experiment.details

    shared = {"shared": {"across": "sources"}}
    statsig.override_dynamic_config("big_number", shared)
    statsig.override_experiment("experiment_with_many_params", shared)
    statsig.override_layer("layer_with_many_params", shared)

    config = statsig.get_dynamic_config(StatsigUser("source-user"), "big_number")
    experiment = statsig.get_experiment(
        StatsigUser("source-user"), "experiment_with_many_params"
    )
    layer = statsig.get_layer(StatsigUser("source-user"), "layer_with_many_params")

    assert experiment.value is config.value
    assert layer.get_value() is config.value
    assert cache.entry_count == 2
    assert cache.misses == 2
    assert cache.hits == 3


def test_layer_cache_hit_preserves_each_users_exposure_data(
    cached_statsig_with_event_capture,
):
    statsig, cache, mock_scrapi = cached_statsig_with_event_capture
    statsig.override_layer(
        "layer_with_many_params",
        {"a_string": "shared-layer-value"},
    )
    users = (
        StatsigUser(
            "first-layer-cache-user",
            email="first@example.com",
            country="US",
            custom={"cache_marker": "first"},
            custom_ids={"companyID": "first-company"},
        ),
        StatsigUser(
            "second-layer-cache-user",
            email="second@example.com",
            country="CA",
            custom={"cache_marker": "second"},
            custom_ids={"companyID": "second-company"},
        ),
    )

    first_layer = statsig.get_layer(users[0], "layer_with_many_params")
    second_layer = statsig.get_layer(users[1], "layer_with_many_params")

    assert first_layer.get_value() is second_layer.get_value()
    assert cache.misses == 1
    assert cache.hits == 1

    statsig.flush_events().wait()
    assert mock_scrapi.get_logged_events() == []

    assert first_layer.get_string("a_string", "fallback") == "shared-layer-value"
    assert second_layer.get_string("a_string", "fallback") == "shared-layer-value"
    statsig.flush_events().wait()

    layer_events = [
        event
        for event in mock_scrapi.get_logged_events()
        if event["eventName"] == "statsig::layer_exposure"
    ]
    assert len(layer_events) == 2

    events_by_user_id = {event["user"]["userID"]: event for event in layer_events}
    assert set(events_by_user_id) == {
        "first-layer-cache-user",
        "second-layer-cache-user",
    }

    expected_users = {
        "first-layer-cache-user": {
            "email": "first@example.com",
            "country": "US",
            "cache_marker": "first",
            "companyID": "first-company",
        },
        "second-layer-cache-user": {
            "email": "second@example.com",
            "country": "CA",
            "cache_marker": "second",
            "companyID": "second-company",
        },
    }
    for user_id, expected in expected_users.items():
        event = events_by_user_id[user_id]
        assert event["user"]["email"] == expected["email"]
        assert event["user"]["country"] == expected["country"]
        assert event["user"]["custom"]["cache_marker"] == expected["cache_marker"]
        assert event["user"]["customIDs"]["companyID"] == expected["companyID"]
        assert event["metadata"]["config"] == "layer_with_many_params"
        assert event["metadata"]["parameterName"] == "a_string"
        assert event["metadata"]["ruleID"] == "override"


def test_cached_dynamic_config_values_are_deeply_immutable(cached_statsig):
    statsig, _ = cached_statsig
    user = StatsigUser("cache-user")

    first = statsig.get_dynamic_config(user, "big_number")
    second = statsig.get_dynamic_config(user, "big_number")

    assert first.value is second.value
    assert first.details is not second.details

    statsig.override_dynamic_config(
        "big_number",
        {
            "nested": {"value": "cached"},
            "items": [1, {"value": "cached"}],
        },
        "cache-user",
    )

    overridden = statsig.get_dynamic_config(user, "big_number")
    overridden_again = statsig.get_dynamic_config(user, "big_number")

    assert overridden.value is overridden_again.value
    assert overridden.value is not first.value
    assert overridden.get_object("nested", {}) == {"value": "cached"}
    assert overridden.get_array("items", []) == [1, {"value": "cached"}]
    assert json.loads(json.dumps(overridden.value)) == overridden.value

    with pytest.raises(TypeError, match="immutable"):
        overridden.value["nested"]["value"] = "changed"
    with pytest.raises(TypeError, match="immutable"):
        overridden.value["items"].append(2)
    with pytest.raises(TypeError, match="immutable"):
        overridden.value["items"][1]["value"] = "changed"

    statsig.remove_dynamic_config_override("big_number", "cache-user")
    restored = statsig.get_dynamic_config(user, "big_number")
    assert restored.value is first.value


def test_bulk_evaluate_uses_cache_without_reusing_per_call_state(cached_statsig):
    statsig, cache = cached_statsig
    user = StatsigUser("my_user")

    first = statsig.bulk_evaluate(user)
    hits_before = cache.hits
    second = statsig.bulk_evaluate(user)

    assert first.keys() == second.keys()
    assert cache.hits > hits_before
    for category in (
        "feature_gates",
        "dynamic_configs",
        "experiments",
        "layer_configs",
    ):
        for evaluation in second[category].values():
            _assert_no_cache_metadata(evaluation)

    for category in ("dynamic_configs", "experiments", "layer_configs"):
        for name, first_evaluation in first[category].items():
            second_evaluation = second[category][name]
            assert second_evaluation["value"] is first_evaluation["value"]
            assert second_evaluation["details"] is not first_evaluation["details"]

    for name, first_layer in first["layer_configs"].items():
        assert (
            first_layer["__exposure"] is not second["layer_configs"][name]["__exposure"]
        )

    first_tokens = {
        evaluation.get("exposureToken")
        for category in first.values()
        for evaluation in category.values()
        if evaluation.get("exposureToken") is not None
    }
    second_tokens = {
        evaluation.get("exposureToken")
        for category in second.values()
        for evaluation in category.values()
        if evaluation.get("exposureToken") is not None
    }
    assert first_tokens.isdisjoint(second_tokens)


def test_cache_keys_track_override_transitions(cached_statsig):
    statsig, _ = cached_statsig
    user_id = "my_user"
    user = StatsigUser(user_id)

    original_config = statsig.get_dynamic_config(user, "big_number")
    original_experiment = statsig.get_experiment(user, "experiment_with_many_params")
    original_layer = statsig.get_layer(user, "layer_with_many_params")

    statsig.override_dynamic_config("big_number", {"marker": "config"}, user_id)
    statsig.override_experiment(
        "experiment_with_many_params", {"marker": "experiment"}, user_id
    )
    statsig.override_layer("layer_with_many_params", {"marker": "layer"}, user_id)

    overridden_config = statsig.get_dynamic_config(user, "big_number")
    overridden_experiment = statsig.get_experiment(user, "experiment_with_many_params")
    overridden_layer = statsig.get_layer(user, "layer_with_many_params")

    assert overridden_config.value == {"marker": "config"}
    assert overridden_config.value is not original_config.value
    assert overridden_experiment.value == {"marker": "experiment"}
    assert overridden_experiment.value is not original_experiment.value
    assert overridden_layer.get_value() == {"marker": "layer"}
    assert overridden_layer.get_value() is not original_layer.get_value()

    statsig.remove_dynamic_config_override("big_number", user_id)
    statsig.remove_experiment_override("experiment_with_many_params", user_id)
    statsig.remove_layer_override("layer_with_many_params", user_id)

    restored_config = statsig.get_dynamic_config(user, "big_number")
    restored_experiment = statsig.get_experiment(user, "experiment_with_many_params")
    restored_layer = statsig.get_layer(user, "layer_with_many_params")

    assert restored_config.value is original_config.value
    assert restored_experiment.value is original_experiment.value
    assert restored_layer.get_value() is original_layer.get_value()


def test_statsig_rejects_an_unbounded_raw_dict_cache():
    options = StatsigOptions(evaluation_cache={})
    with pytest.raises(TypeError, match="EvaluationCache"):
        Statsig("secret-key", options)
