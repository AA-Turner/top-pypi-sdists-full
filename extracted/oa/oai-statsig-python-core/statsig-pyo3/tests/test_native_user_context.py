"""Differential tests against the real PyO3 evaluator and event logger.

Only the config/event HTTP service is local: no user construction, native
evaluation, result conversion, or exposure ownership is mocked.
"""

import copy
import gc
import importlib
import importlib.machinery
import json
import os
import random
import re
import subprocess
import sys
import textwrap
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor

import pytest
from mock_scrapi import MockScrapi
from statsig_python_core import (
    DynamicConfigEvaluationOptions,
    EvaluationCache,
    FeatureGateEvaluationOptions,
    Layer,
    LayerEvaluationOptions,
    PersistentStorage,
    Statsig,
    StatsigOptions,
    StatsigRandomUserID,
    StatsigUser,
    StatsigUserContext,
)
from utils import get_test_data_resource
from werkzeug import Response


def _specs():
    specs = json.loads(get_test_data_resource("eval_proj_dcs.json"))
    specs.pop("checksum", None)
    # Exercise exact-case lookup, standard/custom precedence, private attributes,
    # and fields unused until a later config refresh with explicit expectations.
    for index, (field, expected) in enumerate(
        [
            ("marker", "base"),
            ("country", "US"),
            ("CaseKey", "exact"),
            ("casekey", "lower"),
            ("secret_field", "private"),
            ("future_field", "kept"),
        ]
    ):
        condition_id = str(4_100_000_000 + index)
        specs["condition_map"][condition_id] = {
            "type": "user_field",
            "field": field,
            "operator": "any",
            "targetValue": [expected],
            "additionalValues": {},
            "idType": "userID",
        }
        gate = copy.deepcopy(specs["feature_gates"]["test_public"])
        gate["rules"][0]["conditions"] = [condition_id]
        specs["feature_gates"][f"context_{field}"] = gate
    return specs


def _custom_id_specs():
    specs = _specs()
    condition_id = "4200000000"
    specs["condition_map"][condition_id] = {
        "type": "unit_id",
        "operator": "any",
        "targetValue": ["match"],
        "additionalValues": {},
        "idType": "companyID",
    }
    gate = copy.deepcopy(specs["feature_gates"]["test_public"])
    gate["idType"] = gate["rules"][0]["idType"] = "companyID"
    gate["rules"][0]["conditions"] = [condition_id]
    specs["feature_gates"]["anonymous_custom_id"] = gate
    rollout = copy.deepcopy(specs["feature_gates"]["test_public"])
    rollout["idType"] = rollout["rules"][0]["idType"] = "companyID"
    rollout["rules"][0]["passPercentage"] = 50
    specs["feature_gates"]["anonymous_custom_id_rollout"] = rollout
    layer = copy.deepcopy(specs["layer_configs"]["layer_with_many_params"])
    layer["idType"] = "companyID"
    layer["defaultValue"] = {"matches": False}
    layer["rules"] = [copy.deepcopy(gate["rules"][0])]
    layer["rules"][0]["returnValue"] = {"matches": True}
    specs["layer_configs"]["anonymous_custom_id"] = layer
    return specs


@pytest.fixture
def make_sdk(httpserver):
    instances = []

    def create(*, specs=None, initialize=True, **option_overrides):
        index = len(instances)
        current = {"specs": specs or _specs()}
        spec_path = f"/sdk-{index}/v2/download_config_specs"
        event_path = f"/sdk-{index}/v1/log_event"
        httpserver.expect_request(spec_path).respond_with_handler(
            lambda _: Response(
                json.dumps(current["specs"]), mimetype="application/json"
            )
        )
        scrapi = MockScrapi(httpserver)
        scrapi.stub(event_path, response='{"success": true}', method="POST")
        options = StatsigOptions(
            specs_url=httpserver.url_for(spec_path),
            log_event_url=httpserver.url_for(event_path),
            output_log_level="none",
            **option_overrides,
        )
        sdk = Statsig(f"secret-context-test-{index}", options)
        instances.append(sdk)
        if initialize:
            assert sdk.initialize().wait(10)
            assert sdk.is_config_spec_ready()
        return sdk, scrapi, current

    yield create
    for sdk in reversed(instances):
        assert sdk.shutdown().wait(10)


def _options(kind):
    return {
        "feature_gate": FeatureGateEvaluationOptions,
        "dynamic_config": DynamicConfigEvaluationOptions,
        "layer": LayerEvaluationOptions,
    }[kind](disable_exposure_logging=True)


def _result(result):
    return result.to_dict()


def _compare(sdk, context, metadata, *, user_id=None, custom=None, names=None):
    metadata = copy.deepcopy(metadata)
    if custom is not None:
        metadata["custom"] = {**(metadata.get("custom") or {}), **custom}
    user = StatsigUser(user_id, **metadata)
    if names is None:
        specs = _specs()
        names = {
            "feature_gate": list(specs["feature_gates"]),
            "dynamic_config": [
                name
                for name, value in specs["dynamic_configs"].items()
                if value["entity"] != "experiment"
            ],
            "layer": list(specs["layer_configs"]),
        }
    for kind, entity_names in names.items():
        options = _options(kind)
        regular = getattr(sdk, f"get_{kind}")
        prepared = getattr(sdk, f"get_{kind}_with_context")
        for name in entity_names:
            old = regular(user, name, options=options)
            new = prepared(
                context, name, user_id=user_id, custom=custom, options=options
            )
            assert _result(new) == _result(old), (kind, name, user_id, metadata)
            if kind == "feature_gate":
                assert (
                    sdk.check_gate_with_context(
                        context, name, user_id=user_id, custom=custom, options=options
                    )
                    == old.value
                )


def test_uses_compiled_extension():
    extension = importlib.import_module("statsig_python_core.statsig_python_core")
    assert any(
        extension.__file__.endswith(suffix)
        for suffix in importlib.machinery.EXTENSION_SUFFIXES
    )
    assert extension.StatsigUserContext is StatsigUserContext
    assert extension.StatsigRandomUserID is StatsigRandomUserID
    assert not hasattr(extension.StatsigBasePy, "_INTERNAL_get_experiment_with_context")
    assert not hasattr(Statsig, "get_experiment_with_context")
    assert callable(Statsig.get_experiment)


@pytest.mark.parametrize("max_entry_bytes", [1024, 65536])
def test_context_config_cache_shares_only_admitted_payloads(make_sdk, max_entry_bytes):
    cache = EvaluationCache(max_entry_bytes=max_entry_bytes)
    sdk, logs, _ = make_sdk(evaluation_cache=cache)
    value = {"nested": {"items": ["x" * 2048]}}
    sdk.override_dynamic_config("big_number", value)
    context = StatsigUserContext(custom={"marker": "base"})
    first = sdk.get_dynamic_config_with_context(context, "big_number", "first")
    second = sdk.get_dynamic_config_with_context(context, "big_number", "second")
    assert first.value == second.value == value
    assert first.details is not second.details
    if max_entry_bytes == 1024:
        assert first.value is not second.value
        first.value["nested"]["items"].append("changed")
        assert second.value == value
        assert cache.entry_count == 0
    else:
        assert first.value is second.value
        with pytest.raises(TypeError, match="immutable"):
            first.value["nested"]["items"].append("changed")
        assert cache.hits == 1
    assert sdk.flush_events().wait(10)
    assert {event["user"]["userID"] for event in _exposures(logs)} == {
        "first",
        "second",
    }


def test_anonymous_layer_cache_shares_payload_without_sharing_exposure_state(make_sdk):
    cache = EvaluationCache()
    sdk, logs, _ = make_sdk(evaluation_cache=cache)
    sdk.override_layer("layer_with_many_params", {"a_string": "shared"})
    metadata = {
        "custom": {"base": ["original"]},
        "private_attributes": {"secret": "hidden"},
    }
    context = StatsigUserContext(**metadata)
    policy = StatsigRandomUserID("cached", 16)
    layers = []
    for index in range(2):
        overlay = {"request": [index]}
        layers.append(
            sdk.get_layer_anonymous(
                "layer_with_many_params",
                policy,
                context=context,
                custom=overlay,
                country="US" if index == 0 else "CA",
            )
        )
        overlay["request"].append("mutated")
    assert layers[0].get_value() is layers[1].get_value()
    assert layers[0].details is not layers[1].details
    assert cache.hits == 1
    metadata["custom"]["base"].append("mutated")
    del metadata, context, overlay
    gc.collect()
    assert sdk.flush_events().wait(10)
    assert _exposures(logs) == []
    for layer in reversed(layers):
        assert layer.get_string("a_string", "fallback") == "shared"
    assert sdk.flush_events().wait(10)
    events = _exposures(logs)
    assert len(events) == 2
    assert len({event["user"]["userID"] for event in events}) == 2
    for event in events:
        user = event["user"]
        index = user["custom"]["request"][0]
        assert user["custom"] == {"base": ["original"], "request": [index]}
        assert user["country"] == ("US" if index == 0 else "CA")
        assert "privateAttributes" not in user


@pytest.mark.parametrize("user_id", [None, "", "my_user", "user-in-control", "用户🚀"])
@pytest.mark.parametrize(
    "custom_ids",
    [
        None,
        {},
        {"stableID": "stable-device", "companyID": "123", "random_id": "random-unit"},
        {"companyID": 123, "numericID": 42.5},
    ],
)
def test_all_entities_preserve_identity_and_metadata(make_sdk, user_id, custom_ids):
    sdk, _, _ = make_sdk()
    metadata = {
        "email": "someone@statsig.com",
        "country": "US",
        "locale": "en_US",
        "app_version": "1.2.3",
        "ip": "1.2.3.4",
        "user_agent": "Mozilla/5.0 Chrome/120.0.0.0",
        "custom": {
            "marker": "base",
            "country": "CA",
            "CaseKey": "exact",
            "casekey": "lower",
            "null_value": None,
            "number": 42,
            "is_employee": True,
            "array": ["one", 2, False],
            "nested": {"key": "value"},
            "future_field": "kept",
        },
        "custom_ids": custom_ids,
        "private_attributes": {"secret_field": "private", "private_number": 99},
        "statsig_environment": {"tier": "staging"},
    }
    _compare(sdk, StatsigUserContext(**metadata), metadata, user_id=user_id)


@pytest.mark.parametrize("context", [None, "prepared"])
def test_seeded_randomized_identity_and_overlay_parity(make_sdk, context):
    sdk, _, _ = make_sdk()
    base = (
        {"custom": {"marker": "base", "CaseKey": "exact", "casekey": "lower"}}
        if context
        else {}
    )
    prepared = StatsigUserContext(**base) if context else None
    rng = random.Random(9194)
    assignments = set()
    ids = set()
    names = {
        "feature_gate": [
            "test_50_50",
            "test_gate_with_targeting_gate",
            "context_marker",
            "context_CaseKey",
            "context_casekey",
        ],
        "layer": ["layer_with_many_params"],
        "dynamic_config": ["operating_system_config"],
    }
    for _ in range(128):
        # The same concrete UUID is passed to both evaluators on this iteration.
        user_id = str(uuid.UUID(int=rng.getrandbits(128), version=4))
        ids.add(user_id)
        overlay = rng.choice(
            [
                None,
                {},
                {"marker": None},
                {"marker": "changed"},
                {"CASEKEY": "other"},
                {"casekey": "lower"},
            ]
        )
        _compare(sdk, prepared, base, user_id=user_id, custom=overlay, names=names)
        assignments.add(
            sdk.check_gate_with_context(
                prepared, "test_50_50", user_id, options=_options("feature_gate")
            )
        )
    assert len(ids) == 128
    assert assignments == {True, False}


def test_snapshot_aliases_overlays_and_return_to_base(make_sdk):
    sdk, _, _ = make_sdk()
    original = {
        "custom": {
            "marker": "base",
            "nested": {"list": [1, 2]},
            "CaseKey": "exact",
            "casekey": "lower",
        },
        "country": "US",
        "custom_ids": {"stableID": "original"},
        "private_attributes": {"secret_field": "private"},
        "statsig_environment": {"tier": "staging"},
    }
    expected = copy.deepcopy(original)
    context = StatsigUserContext(**original)
    original["custom"]["marker"] = "changed"
    original["custom"]["nested"]["list"].append(3)
    original["custom_ids"]["stableID"] = "changed"
    original["private_attributes"]["secret_field"] = "changed"
    original["statsig_environment"]["tier"] = "production"
    for overlay in [
        None,
        {"marker": None},
        {"marker": "changed"},
        {"CaseKey": "changed"},
        {"country": "CA"},
        {},
        None,
    ]:
        _compare(sdk, context, expected, user_id="snapshot-user", custom=overlay)
    assert sdk.check_gate_with_context(context, "context_marker") is True
    assert (
        sdk.check_gate_with_context(context, "context_marker", custom={"marker": None})
        is False
    )
    assert (
        sdk.check_gate_with_context(
            context, "context_CaseKey", custom={"CASEKEY": "different"}
        )
        is True
    )
    assert (
        sdk.check_gate_with_context(
            context, "context_country", custom={"country": "CA"}
        )
        is True
    )
    # Changed metadata requires an explicit new snapshot.
    replacement = StatsigUserContext(**original)
    assert sdk.check_gate_with_context(replacement, "context_marker") is False
    with pytest.raises((AttributeError, TypeError)):
        context.custom = {"marker": "changed"}


def _exposures(scrapi):
    # Disabled checks still emit aggregate non_exposed_checks telemetry.
    return [
        event
        for event in scrapi.get_logged_events()
        if event["eventName"]
        in {
            "statsig::gate_exposure",
            "statsig::config_exposure",
            "statsig::layer_exposure",
        }
    ]


def _event_payload(event):
    result = copy.deepcopy(event)
    result.pop("time", None)
    # Receive times identify SDK instances, not evaluation semantics.
    result.get("metadata", {}).pop("receivedAt", None)
    return result


def test_automatic_exposures_match_full_users_and_keep_each_identity(make_sdk):
    old, old_logs, _ = make_sdk()
    new, new_logs, _ = make_sdk()
    metadata = {
        "country": "US",
        "custom": {"marker": "base"},
        "private_attributes": {"do_not_log": "private"},
    }
    context = StatsigUserContext(**metadata)
    for index in range(24):
        user_id = str(uuid.UUID(int=index + 1, version=4))
        overlay = {"request_number": index, "nested": {"index": index}}
        user = StatsigUser(
            user_id, **{**metadata, "custom": {**metadata["custom"], **overlay}}
        )
        for kind, name in [
            ("feature_gate", "test_gate_with_targeting_gate"),
            ("dynamic_config", "big_number"),
            ("layer", "layer_with_many_params"),
        ]:
            old_result = getattr(old, f"get_{kind}")(user, name)
            new_result = getattr(new, f"get_{kind}_with_context")(
                context, name, user_id, overlay
            )
            if kind == "layer":
                assert new_result.get("a_string") == old_result.get("a_string")
        # Subsequent Python mutation must not change already queued event data.
        overlay["nested"]["index"] = -1
    assert old.flush_events().wait(10)
    assert new.flush_events().wait(10)
    expected = [_event_payload(event) for event in _exposures(old_logs)]
    actual = [_event_payload(event) for event in _exposures(new_logs)]
    assert actual == expected
    assert len(actual) == 72
    assert len({event["user"]["userID"] for event in actual}) == 24
    for event in actual:
        assert "privateAttributes" not in event["user"]
        assert event["user"]["custom"]["nested"]["index"] >= 0


def test_lazy_layer_owns_original_context_and_overlay_after_collection(make_sdk):
    sdk, logs, _ = make_sdk()
    metadata = {
        "country": "US",
        "custom": {"marker": "base"},
        "private_attributes": {"secret": "hidden"},
    }
    context = StatsigUserContext(**metadata)
    overlay = {"request": ["original"]}
    layer = sdk.get_layer_with_context(
        context, "layer_with_many_params", "original-id", overlay
    )
    metadata["custom"]["marker"] = "mutated"
    overlay["request"].append("mutated")
    del context, metadata, overlay
    gc.collect()
    assert sdk.flush_events().wait(10)
    assert _exposures(logs) == []
    # Interleaving another identity must not overwrite data retained by the layer.
    sdk.get_layer_with_context(
        None, "layer_with_many_params", "other-id", {"marker": "other"}
    )
    layer.get("a_string")
    layer.get("a_string")
    layer.get("another_string")
    del layer
    gc.collect()
    assert sdk.flush_events().wait(10)
    events = _exposures(logs)
    assert len(events) == 2
    for event in events:
        assert event["user"]["userID"] == "original-id"
        assert event["user"]["custom"] == {"marker": "base", "request": ["original"]}
        assert "privateAttributes" not in event["user"]


def test_disabled_manual_and_deduplicated_exposures(make_sdk):
    sdk, logs, _ = make_sdk()
    context = StatsigUserContext(custom={"marker": "base"})
    user = StatsigUser("manual-id", custom={"marker": "base"})
    for kind, name in [
        ("feature_gate", "test_public"),
        ("dynamic_config", "big_number"),
        ("layer", "layer_with_many_params"),
    ]:
        result = getattr(sdk, f"get_{kind}_with_context")(
            context, name, user.user_id, options=_options(kind)
        )
        if kind == "layer":
            result.get("a_string")
    assert sdk.flush_events().wait(10)
    assert _exposures(logs) == []
    sdk.manually_log_gate_exposure(user, "test_public")
    sdk.manually_log_dynamic_config_exposure(user, "big_number")
    sdk.manually_log_experiment_exposure(user, "experiment_with_many_params")
    sdk.manually_log_layer_parameter_exposure(
        user, "layer_with_many_params", "a_string"
    )
    assert sdk.flush_events().wait(10)
    assert len(_exposures(logs)) == 4
    for _ in range(3):
        sdk.check_gate_with_context(context, "test_public", "dedup-id")
    assert sdk.flush_events().wait(10)
    assert (
        len(
            [
                event
                for event in _exposures(logs)
                if event["user"]["userID"] == "dedup-id"
            ]
        )
        == 1
    )


def test_override_transitions_and_instance_isolation(make_sdk):
    first, _, _ = make_sdk()
    second, _, _ = make_sdk()
    metadata = {"custom_ids": {"companyID": "company-1"}}
    context = StatsigUserContext(**metadata)
    for sdk in [first, second]:
        _compare(sdk, context, metadata, user_id="override-user")
    first.override_gate("test_public", False, "company-1")
    first.override_dynamic_config("big_number", {"foo": "override"}, "override-user")
    first.override_experiment_by_group_name(
        "experiment_with_many_params", "Control", "override-user"
    )
    first.override_layer(
        "layer_with_many_params", {"a_string": "override"}, "override-user"
    )
    _compare(first, context, metadata, user_id="override-user")
    assert (
        first.check_gate_with_context(context, "test_public", "override-user") is False
    )
    assert (
        second.check_gate_with_context(context, "test_public", "override-user") is True
    )
    first.remove_gate_override("test_public", "company-1")
    first.remove_dynamic_config_override("big_number", "override-user")
    first.remove_experiment_override("experiment_with_many_params", "override-user")
    first.remove_layer_override("layer_with_many_params", "override-user")
    _compare(first, context, metadata, user_id="override-user")


def test_global_fields_and_environment_remain_instance_specific(make_sdk):
    first, first_logs, _ = make_sdk(
        global_custom_fields={"marker": "base", "global_only": "first"},
        environment="staging",
    )
    second, second_logs, _ = make_sdk(
        global_custom_fields={"marker": "other", "global_only": "second"},
        environment="production",
    )
    metadata = {"custom": {"shared": True}, "private_attributes": {"marker": "private"}}
    context = StatsigUserContext(**metadata)
    for sdk in [first, second]:
        _compare(sdk, context, metadata, user_id="global-user")
        _compare(sdk, context, metadata, user_id="global-user", custom={"marker": None})
    assert first.check_gate_with_context(context, "context_marker", "first-id") is True
    assert (
        second.check_gate_with_context(context, "context_marker", "second-id") is False
    )
    assert first.flush_events().wait(10)
    assert second.flush_events().wait(10)
    for logs, marker, global_only, tier in [
        (first_logs, "base", "first", "staging"),
        (second_logs, "other", "second", "production"),
    ]:
        event = _exposures(logs)[0]
        assert event["user"]["custom"] == {
            "shared": True,
            "marker": marker,
            "global_only": global_only,
        }
        assert event["user"]["statsigEnvironment"] == {"tier": tier}
        assert "privateAttributes" not in event["user"]


class _MemoryStorage(PersistentStorage):
    def load(self, key):
        return {}

    def save(self, key, config_name, data):
        pass

    def delete(self, key, config_name):
        pass


def test_layer_sticky_values_are_applied_by_the_existing_manager(make_sdk):
    sdk, _, current = make_sdk(persistent_storage=_MemoryStorage())
    name = "layer_with_many_params"
    metadata = {"custom": {"marker": "base"}}
    context = StatsigUserContext(**metadata)
    values = {
        name: {
            "value": True,
            "json_value": {"a_string": "sticky"},
            "rule_id": "sticky-rule",
            "group_name": "Sticky Group",
            "secondary_exposures": [],
            "time": current["specs"]["time"],
            "config_delegate": "experiment_with_many_params",
            "explicit_parameters": ["a_string"],
        }
    }
    options = _options("layer")
    options.user_persisted_values = values
    regular = sdk.get_layer(StatsigUser("sticky-user", **metadata), name, options)
    prepared = sdk.get_layer_with_context(context, name, "sticky-user", options=options)
    assert prepared.get("a_string") == regular.get("a_string") == "sticky"
    # The sticky manager stamps receipt at each call, unlike downloaded specs.
    old = _result(regular)
    new = _result(prepared)
    old_received = old["details"].pop("received_at")
    new_received = new["details"].pop("received_at")
    assert new_received >= old_received
    assert new == old
    assert "Persisted" in prepared.details.reason


def test_config_refresh_uses_prepared_fields_that_become_relevant(make_sdk):
    specs = _specs()
    specs["feature_gates"]["context_future_field"]["rules"] = []
    sdk, _, current = make_sdk(specs=specs, specs_sync_interval_ms=1000)
    metadata = {"custom": {"future_field": "kept"}}
    context = StatsigUserContext(**metadata)
    assert sdk.check_gate_with_context(context, "context_future_field") is False
    refreshed = threading.Event()
    newer = _specs()
    newer["time"] += 100
    sdk.subscribe(
        "specs_updated",
        lambda event: (
            refreshed.set()
            if event["data"]["values"]["time"] == newer["time"]
            else None
        ),
    )
    current["specs"] = newer
    assert refreshed.wait(10), (
        "The local HTTP config update did not reach the native SDK"
    )
    assert sdk.check_gate_with_context(context, "context_future_field") is True
    _compare(sdk, context, metadata, names={"feature_gate": ["context_future_field"]})


def test_uninitialized_defaults_missing_entities_and_mutable_results(make_sdk):
    sdk, _, _ = make_sdk(initialize=False)
    context = StatsigUserContext(custom={"marker": "base"})
    names = {
        kind: ["missing_entity"] for kind in ["feature_gate", "dynamic_config", "layer"]
    }
    _compare(sdk, context, {"custom": {"marker": "base"}}, names=names)
    assert sdk.initialize().wait(10)
    _compare(sdk, context, {"custom": {"marker": "base"}}, names=names)
    for kind, name in [
        ("dynamic_config", "big_number"),
        ("layer", "layer_with_many_params"),
    ]:
        evaluate = getattr(sdk, f"get_{kind}_with_context")
        first = evaluate(context, name, "mutable-user", options=_options(kind))
        original = copy.deepcopy(first.get_value())
        first.get_value()["caller_mutation"] = {"only": "first-result"}
        second = evaluate(context, name, "mutable-user", options=_options(kind))
        assert second.get_value() == original
        assert first.get("missing_parameter", "fallback") == "fallback"


def test_concurrent_context_use_does_not_leak_ids_or_overlays(make_sdk):
    sdk, logs, _ = make_sdk()
    context = StatsigUserContext(custom={"marker": "base"})
    options = _options("feature_gate")

    def evaluate(index):
        user_id = f"thread-{index}"
        overlay = {"marker": "base" if index % 2 else "changed", "request": index}
        expected = sdk.check_gate(
            StatsigUser(user_id, custom=overlay), "context_marker", options
        )
        actual = sdk.check_gate_with_context(
            context, "context_marker", user_id, overlay
        )
        assert actual == expected == bool(index % 2)
        return user_id

    with ThreadPoolExecutor(max_workers=8) as pool:
        ids = list(pool.map(evaluate, range(128)))
    assert sdk.flush_events().wait(10)
    events = _exposures(logs)
    assert len(events) == len(ids)
    assert {event["user"]["userID"] for event in events} == set(ids)
    for event in events:
        index = int(event["user"]["userID"].split("-")[1])
        assert event["user"]["custom"]["request"] == index
        assert event["user"]["custom"]["marker"] == ("base" if index % 2 else "changed")


@pytest.mark.parametrize(
    "prefix,length", [("anon", 8), ("", 16), ("caller-prefix", 32), ("用户", 8)]
)
def test_anonymous_ids_are_fresh_and_follow_caller_policy(make_sdk, prefix, length):
    sdk, logs, _ = make_sdk()
    policy = StatsigRandomUserID(prefix, length)
    for _ in range(256):
        sdk.get_feature_gate_anonymous("test_50_50", policy)
    assert sdk.flush_events().wait(10)
    events = _exposures(logs)
    ids = [event["user"]["userID"] for event in events]
    assert len(ids) == len(set(ids)) == 256
    start = prefix + "-" if prefix else ""
    suffixes = [user_id[len(start) :] for user_id in ids]
    assert all(user_id.startswith(start) for user_id in ids)
    assert all(re.fullmatch(rf"[A-Za-z0-9]{{{length}}}", value) for value in suffixes)
    # A gross alphabet/truncation regression check, not a statistical proof of
    # cryptographic entropy. Native OsRng supplies the security property.
    assert set("".join(suffixes)) == set(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    )
    assert {event["metadata"]["gateValue"] for event in events} == {"true", "false"}
    with pytest.raises((AttributeError, TypeError)):
        policy.prefix = "changed"
    with pytest.raises((AttributeError, TypeError)):
        policy.length = 1


@pytest.mark.parametrize("prefix,length", [("anon", 0), ("anon", 1025), ("é" * 513, 8)])
def test_anonymous_policy_rejects_invalid_bounds(prefix, length):
    with pytest.raises(ValueError):
        StatsigRandomUserID(prefix, length)


@pytest.mark.parametrize("length", [1, 1024])
def test_anonymous_policy_accepts_length_boundaries(make_sdk, length):
    sdk, logs, _ = make_sdk()
    sdk.check_gate_anonymous("test_public", StatsigRandomUserID("", length))
    assert sdk.flush_events().wait(10)
    assert re.fullmatch(
        rf"[A-Za-z0-9]{{{length}}}", _exposures(logs)[0]["user"]["userID"]
    )


@pytest.mark.parametrize("method", ["check_gate", "get_feature_gate", "get_layer"])
def test_anonymous_per_call_custom_ids_target_like_merged_full_user(make_sdk, method):
    sdk, _, _ = make_sdk(specs=_custom_id_specs())
    policy = StatsigRandomUserID("custom-id", 16)
    kind = "layer" if method == "get_layer" else "feature_gate"
    cases = [
        (None, {"companyID": "match"}, True),
        ({"companyID": "match"}, None, True),
        ({"companyID": "match"}, {}, True),
        ({"companyID": "base"}, {"companyID": "match"}, True),
        ({"companyID": "match"}, {"companyID": "different"}, False),
        ({"companyID": "match"}, {"companyID": ""}, False),
        # Exact lookup wins across both maps, before the lowercase fallback.
        ({"companyID": "match"}, {"companyid": "different"}, True),
        ({"companyid": "different"}, {"companyID": "match"}, True),
        ({"companyid": "match"}, {"CompanyID": "different"}, True),
    ]

    def value(result):
        if method == "check_gate":
            return result
        if method == "get_layer":
            return result.get("matches")
        return result.value

    for base_ids, per_call_ids, expected in cases:
        context = StatsigUserContext(custom_ids=base_ids) if base_ids else None
        merged_ids = {**(base_ids or {}), **(per_call_ids or {})}
        anonymous = getattr(sdk, f"{method}_anonymous")(
            "anonymous_custom_id",
            policy,
            context=context,
            custom_ids=per_call_ids,
            options=_options(kind),
        )
        ordinary = getattr(sdk, method)(
            StatsigUser("full-user", custom_ids=merged_ids),
            "anonymous_custom_id",
            options=_options(kind),
        )
        assert value(anonymous) is value(ordinary) is expected, (base_ids, per_call_ids)
        # An overlay must not alter IDs retained in a reusable context.
        inherited = getattr(sdk, f"{method}_anonymous")(
            "anonymous_custom_id", policy, context=context, options=_options(kind)
        )
        base_user = getattr(sdk, method)(
            StatsigUser("full-user", custom_ids=base_ids),
            "anonymous_custom_id",
            options=_options(kind),
        )
        assert value(inherited) is value(base_user)


def test_anonymous_private_layer_accepts_keyword_ids_and_retains_exposure(make_sdk):
    sdk, logs, _ = make_sdk(specs=_custom_id_specs())
    name = "anonymous_custom_id"
    policy = StatsigRandomUserID("keyword", 16)
    context = StatsigUserContext(
        country="CA", custom_ids={"stableID": "device", "companyID": "base"}
    )
    ids = {"companyID": "match"}
    raw = sdk._INTERNAL_get_layer_anonymous(
        name=name,
        id_options=policy,
        context=context,
        custom_ids=ids,
        country="US",
        options=LayerEvaluationOptions(),
        evaluation_cache_keys=None,
    )
    public = sdk.get_layer_anonymous(
        name,
        policy,
        context=context,
        custom_ids=ids,
        country="US",
        options=_options("layer"),
    )
    ordinary = sdk.get_layer(
        StatsigUser(
            "reference", country="US", custom_ids={"stableID": "device", **ids}
        ),
        name,
        _options("layer"),
    )
    assert Layer(None, name, raw).to_dict() == public.to_dict() == ordinary.to_dict()
    assert public.get("matches") is True
    ids["companyID"] = "mutated"
    del ids, context
    gc.collect()
    assert sdk.flush_events().wait(10)
    assert _exposures(logs) == []
    sdk._INTERNAL_log_layer_param_exposure(raw["__exposure"], "matches")
    assert sdk.flush_events().wait(10)
    (event,) = _exposures(logs)
    assert re.fullmatch(r"keyword-[A-Za-z0-9]{16}", event["user"]["userID"])
    assert event["user"]["customIDs"] == {"stableID": "device", "companyID": "match"}
    assert event["user"]["country"] == "US"


@pytest.mark.parametrize(
    "kind,name",
    [
        ("feature_gate", "test_50_50"),
        ("feature_gate", "test_gate_with_targeting_gate"),
        ("feature_gate", "anonymous_custom_id_rollout"),
        ("layer", "layer_with_many_params"),
    ],
)
@pytest.mark.parametrize("with_request", [False, True])
def test_anonymous_generated_identity_replays_with_full_user_and_exposures(
    make_sdk, kind, name, with_request
):
    sdk, logs, _ = make_sdk(specs=_custom_id_specs())
    ordinary, ordinary_logs, _ = make_sdk(specs=_custom_id_specs())
    base = {
        "country": "CA",
        "locale": "fr-CA",
        "ip": "192.0.2.10",
        "user_agent": "base-agent",
        "custom": {"marker": "base", "country": "MX", "nested": ["original"]},
        "custom_ids": {"stableID": "stable-device", "companyID": "base-company"},
        "private_attributes": {"secret_field": "private"},
        "statsig_environment": {"tier": "staging"},
    }
    context = StatsigUserContext(**base)
    request = (
        {
            "country": "US",
            "locale": "en-US",
            "ip": "192.0.2.20",
            "user_agent": "request-agent",
        }
        if with_request
        else {}
    )
    results = []
    expected_metadata = []
    for index in range(32):
        overlay = {
            "request_number": index,
            "marker": "changed" if index % 2 else "base",
            "nested": [index],
        }
        per_call_ids = {
            "companyID": index % 8,
            "fractionalID": index + 0.5,
            "requestID": f"request-{index}",
            "emptyID": "",
        }
        if index % 2:
            per_call_ids["stableID"] = f"request-device-{index}"
        expected_metadata.append(
            copy.deepcopy(
                {
                    **base,
                    **request,
                    "custom": {**base["custom"], **overlay},
                    "custom_ids": {**base["custom_ids"], **per_call_ids},
                }
            )
        )
        result = getattr(sdk, f"get_{kind}_anonymous")(
            name,
            StatsigRandomUserID("replay", 16),
            context=context,
            custom=overlay,
            custom_ids=per_call_ids,
            **request,
        )
        results.append(result)
        # Queued and lazy exposures must own a snapshot, not these containers.
        overlay["nested"].append("mutated")
        per_call_ids["companyID"] = "mutated"
        per_call_ids.clear()
        if kind == "layer":
            result.get("a_string")
    assert sdk.flush_events().wait(10)
    events = _exposures(logs)
    assert len(events) == 32
    by_index = {event["user"]["custom"]["request_number"]: event for event in events}
    for index, result in enumerate(results):
        generated_id = by_index[index]["user"]["userID"]
        assert re.fullmatch(r"replay-[A-Za-z0-9]{16}", generated_id)
        user = StatsigUser(generated_id, **expected_metadata[index])
        assert (
            by_index[index]["user"]["customIDs"]
            == expected_metadata[index]["custom_ids"]
        )
        # Compare on the same SDK so receive-time metadata is identical.
        replay = getattr(sdk, f"get_{kind}")(user, name, _options(kind))
        assert _result(result) == _result(replay)
        exposed = getattr(ordinary, f"get_{kind}")(user, name)
        if kind == "layer":
            assert exposed.get("a_string") == result.get("a_string")
    assert ordinary.flush_events().wait(10)
    assert [_event_payload(event) for event in events] == [
        _event_payload(event) for event in _exposures(ordinary_logs)
    ]
    assert all("privateAttributes" not in event["user"] for event in events)
    if name == "anonymous_custom_id_rollout":
        assert len({event["user"]["userID"] for event in events}) == 32
        # The company ID drives rollout bucketing; fresh userIDs do not move
        # repeated evaluations of the same company between rollout buckets.
        for index in range(8):
            assert len({results[i].value for i in range(index, 32, 8)}) == 1


@pytest.mark.parametrize(
    "country,expected", [(None, True), ("", False), ("CA", False), ("US", True)]
)
def test_anonymous_request_fields_override_context_including_empty(
    make_sdk, country, expected
):
    sdk, logs, _ = make_sdk()
    context = StatsigUserContext(
        country="US", locale="en-US", ip="192.0.2.1", user_agent="base"
    )
    assert (
        sdk.check_gate_anonymous(
            "context_country",
            StatsigRandomUserID("anon", 8),
            context=context,
            country=country,
            locale="",
            ip="",
            user_agent="",
            custom={"country": "MX"},
        )
        is expected
    )
    assert sdk.flush_events().wait(10)
    user = _exposures(logs)[0]["user"]
    assert user.get("country", "") == ("US" if country is None else country)
    for field in ("locale", "ip", "userAgent"):
        assert user.get(field, "") == ""


def test_anonymous_layer_retains_id_and_metadata_until_lazy_exposure(make_sdk):
    sdk, logs, _ = make_sdk()
    source = {"marker": "base", "nested": ["original"]}
    overlay = {"request": ["original"]}
    base_ids = {"stableID": "stable-device", "companyID": "base-company"}
    per_call_ids = {"companyID": "request-company", "requestID": 123}
    context = StatsigUserContext(
        custom=source,
        custom_ids=base_ids,
        private_attributes={"secret": "hidden"},
    )
    policy = StatsigRandomUserID("lazy", 16)
    layer = sdk.get_layer_anonymous(
        "layer_with_many_params",
        policy,
        context=context,
        custom=overlay,
        custom_ids=per_call_ids,
        country="US",
    )
    source["nested"].append("mutated")
    overlay["request"].append("mutated")
    base_ids["stableID"] = "mutated"
    per_call_ids["companyID"] = "mutated"
    per_call_ids.clear()
    del source, overlay, base_ids, per_call_ids, context, policy
    gc.collect()
    assert sdk.flush_events().wait(10)
    assert _exposures(logs) == []
    sdk.get_layer_anonymous(
        "layer_with_many_params",
        StatsigRandomUserID("other", 8),
        custom_ids={"companyID": "another-request"},
    )
    layer.get("a_string")
    layer.get("a_string")
    layer.get("another_string")
    del layer
    gc.collect()
    assert sdk.flush_events().wait(10)
    events = _exposures(logs)
    assert len(events) == 2
    assert len({event["user"]["userID"] for event in events}) == 1
    for event in events:
        assert re.fullmatch(r"lazy-[A-Za-z0-9]{16}", event["user"]["userID"])
        assert event["user"]["custom"] == {
            "marker": "base",
            "nested": ["original"],
            "request": ["original"],
        }
        assert event["user"]["country"] == "US"
        assert event["user"]["customIDs"] == {
            "stableID": "stable-device",
            "companyID": "request-company",
            "requestID": 123,
        }
        assert "privateAttributes" not in event["user"]


def test_anonymous_uninitialized_missing_defaults_and_disabled_exposures(make_sdk):
    sdk, logs, _ = make_sdk(initialize=False)
    policy = StatsigRandomUserID("anon", 8)
    for initialized in (False, True):
        if initialized:
            assert sdk.initialize().wait(10)
        assert sdk.check_gate_anonymous("missing_entity", policy) is False
        assert (
            sdk.get_layer_anonymous("missing_entity", policy).get("missing", "fallback")
            == "fallback"
        )
        for _ in range(8):
            sdk.get_feature_gate_anonymous(
                "test_public", policy, options=_options("feature_gate")
            )
            sdk.get_layer_anonymous(
                "layer_with_many_params", policy, options=_options("layer")
            ).get("a_string")
    assert sdk.flush_events().wait(10)
    # Missing gates still emit their ordinary default-result exposure. The
    # checks with logging disabled must add no gate or layer exposures.
    events = _exposures(logs)
    assert len(events) == 2
    assert all(
        event["eventName"] == "statsig::gate_exposure"
        and event["metadata"]["gate"] == "missing_entity"
        for event in events
    )


def test_anonymous_native_path_never_calls_python_user_or_entropy(
    make_sdk, monkeypatch
):
    sdk, logs, _ = make_sdk()
    policy = StatsigRandomUserID("native", 8)
    context = StatsigUserContext(custom={"marker": "base"})

    def forbidden(*_args, **_kwargs):
        raise AssertionError(
            "Anonymous evaluation entered Python user construction or entropy"
        )

    module = importlib.import_module("statsig_python_core.statsig")
    package = importlib.import_module("statsig_python_core")
    extension = importlib.import_module("statsig_python_core.statsig_python_core")
    # Catch a Python wrapper that accidentally builds an ordinary native user.
    with monkeypatch.context() as patches:
        for target in (module, package, extension):
            patches.setattr(target, "StatsigUser", forbidden, raising=False)
        patches.setattr(os, "urandom", forbidden)
        patches.setattr(random, "getrandbits", forbidden)
        patches.setattr(random.SystemRandom, "getrandbits", forbidden)
        patches.setattr(uuid, "uuid4", forbidden)
        assert sdk.check_gate_anonymous(
            "context_marker", policy, context=context, custom_ids={"companyID": "one"}
        )
        assert sdk.get_feature_gate_anonymous(
            "test_public", policy, custom_ids={"companyID": "two"}
        ).value
        sdk.get_layer_anonymous(
            "layer_with_many_params", policy, custom_ids={"companyID": "three"}
        ).get("a_string")
    assert sdk.flush_events().wait(10)
    assert len(_exposures(logs)) == 3


def test_anonymous_concurrent_use_preserves_sdk_and_request_isolation(make_sdk):
    first, first_logs, _ = make_sdk(
        global_custom_fields={"sdk": "first"}, environment="staging"
    )
    second, second_logs, _ = make_sdk(
        global_custom_fields={"sdk": "second"}, environment="production"
    )
    second.override_gate("context_marker", False)
    context = StatsigUserContext(
        custom={"marker": "base"}, custom_ids={"stableID": "shared-device"}
    )
    policy = StatsigRandomUserID("thread", 16)

    def evaluate(index):
        sdk = first if index % 2 else second
        actual = sdk.check_gate_anonymous(
            "context_marker",
            policy,
            context=context,
            custom={"request": index},
            custom_ids={"requestID": index, "companyID": f"company-{index % 2}"},
            country="US" if index % 2 else "CA",
        )
        assert actual is bool(index % 2)

    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(evaluate, range(128)))
    ids = set()
    for sdk, logs, label, parity, country, tier in [
        (first, first_logs, "first", 1, "US", "staging"),
        (second, second_logs, "second", 0, "CA", "production"),
    ]:
        assert sdk.flush_events().wait(10)
        events = _exposures(logs)
        assert len(events) == 64
        for event in events:
            user = event["user"]
            assert user["userID"] not in ids
            ids.add(user["userID"])
            assert user["custom"]["request"] % 2 == parity
            assert user["custom"]["sdk"] == label
            assert user["customIDs"] == {
                "stableID": "shared-device",
                "requestID": user["custom"]["request"],
                "companyID": f"company-{parity}",
            }
            assert user["country"] == country
            assert user["statsigEnvironment"] == {"tier": tier}
    assert len(ids) == 128


@pytest.mark.skipif(not hasattr(os, "fork"), reason="requires os.fork")
def test_anonymous_rng_has_no_duplicate_stream_after_fork(httpserver):
    # Isolate the fork in a watchdog process; follow the supported lifecycle:
    # shutdown before fork, then construct an SDK in each process. Reuse the
    # policy created before fork so copied RNG/prefetched-ID state is exercised.
    httpserver.expect_request("/fork/specs").respond_with_json(_specs())
    logs = MockScrapi(httpserver)
    logs.stub("/fork/v1/log_event", response='{"success": true}', method="POST")
    code = textwrap.dedent("""
        import os
        from statsig_python_core import Statsig, StatsigOptions, StatsigRandomUserID
        policy = StatsigRandomUserID('fork', 16)
        def run(label, count):
            sdk = Statsig('secret-anonymous-fork', StatsigOptions(
                specs_url=SPECS_URL, log_event_url=EVENTS_URL,
                output_log_level='none', event_logging_flush_interval_ms=600000,
            ))
            assert sdk.initialize().wait(10)
            for index in range(count):
                sdk.get_feature_gate_anonymous('test_public', policy, custom={'process': label, 'index': index})
            assert sdk.shutdown().wait(10)
        run('before', 1)
        child = os.fork()
        if child == 0:
            run('child', 128)
            os._exit(0)
        run('parent', 128)
        _, status = os.waitpid(child, 0)
        assert os.waitstatus_to_exitcode(status) == 0
    """)
    code = (
        "SPECS_URL = "
        + repr(httpserver.url_for("/fork/specs"))
        + "\nEVENTS_URL = "
        + repr(httpserver.url_for("/fork/v1/log_event"))
        + "\n"
        + code
    )
    process = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        timeout=45,
        check=False,
    )
    assert process.returncode == 0, (process.stdout, process.stderr)
    events = _exposures(logs)
    assert len(events) == 257
    assert len({event["user"]["userID"] for event in events}) == 257
    assert {
        label: sum(event["user"]["custom"]["process"] == label for event in events)
        for label in ("before", "parent", "child")
    } == {"before": 1, "parent": 128, "child": 128}


def test_anonymous_layer_uses_existing_persisted_values_manager(make_sdk):
    sdk, logs, current = make_sdk(persistent_storage=_MemoryStorage())
    name = "layer_with_many_params"
    options = LayerEvaluationOptions()
    options.user_persisted_values = {
        name: {
            "value": True,
            "json_value": {"a_string": "sticky"},
            "rule_id": "sticky-rule",
            "group_name": "Sticky Group",
            "secondary_exposures": [],
            "time": current["specs"]["time"],
            "config_delegate": "experiment_with_many_params",
            "explicit_parameters": ["a_string"],
        }
    }
    layer = sdk.get_layer_anonymous(
        name, StatsigRandomUserID("sticky", 16), options=options
    )
    assert layer.get("a_string") == "sticky"
    assert "Persisted" in layer.details.reason
    assert sdk.flush_events().wait(10)
    events = _exposures(logs)
    assert len(events) == 1
    replay = sdk.get_layer(StatsigUser(events[0]["user"]["userID"]), name, options)
    assert replay.get("a_string") == "sticky"
    actual, expected = _result(layer), _result(replay)
    actual["details"].pop("received_at")
    expected["details"].pop("received_at")
    assert actual == expected
