"""Compare flat gate results with the existing compiled dictionary API."""

import copy
import importlib
import importlib.machinery
import json
import re

import pytest
from statsig_python_core import (
    EvaluationDetails,
    FeatureGate,
    FeatureGateEvaluationOptions,
    StatsigRandomUserID,
    StatsigUser,
    StatsigUserContext,
)
from test_native_user_context import _exposures, _specs
from test_native_user_context import make_sdk as make_sdk


def _disabled():
    return FeatureGateEvaluationOptions(disable_exposure_logging=True)


def _parts_from_raw(raw):
    details = raw["details"]
    return (
        raw["value"],
        raw["ruleID"],
        raw["idType"],
        details["reason"],
        details["lcut"],
        details["received_at"],
        details["version"],
    )


def _assert_gate(actual, expected):
    assert type(actual) is FeatureGate
    assert type(actual.details) is EvaluationDetails
    assert actual.to_dict() == expected.to_dict()
    assert json.loads(json.dumps(actual.to_dict())) == expected.to_dict()
    assert actual.get_name() == expected.name
    assert actual.get_rule_id() == expected.rule_id
    assert actual.get_id_type() == expected.id_type
    assert actual.get_evaluation_details() is actual.details
    assert actual.value is expected.value
    assert vars(actual.details) == vars(expected.details)
    assert {key: value for key, value in vars(actual).items() if key != "details"} == {
        key: value for key, value in vars(expected).items() if key != "details"
    }


def _assert_parts(name, parts, raw):
    assert type(parts) is tuple
    assert len(parts) == 7
    assert type(parts[0]) is bool
    assert type(parts[1]) is str
    assert parts[2] is None or type(parts[2]) is str
    assert type(parts[3]) is str
    assert all(value is None or type(value) is int for value in parts[4:])
    assert parts == _parts_from_raw(raw)
    _assert_gate(FeatureGate._from_parts(name, parts), FeatureGate(name, raw))


def test_parts_methods_are_available_on_the_compiled_extension():
    extension = importlib.import_module("statsig_python_core.statsig_python_core")
    assert any(
        extension.__file__.endswith(suffix)
        for suffix in importlib.machinery.EXTENSION_SUFFIXES
    )
    for name in (
        "_INTERNAL_get_feature_gate_parts",
        "_INTERNAL_get_feature_gate_with_context_parts",
        "_INTERNAL_get_feature_gate_anonymous_parts",
    ):
        assert callable(getattr(extension.StatsigBasePy, name))


@pytest.mark.parametrize(
    "user_id", [None, "", "my_user", "user-in-control", "user-in-test-2", "用户🚀"]
)
@pytest.mark.parametrize("with_context", [False, True])
def test_all_fixture_gates_match_dictionary_results(make_sdk, user_id, with_context):
    sdk, _, current = make_sdk()
    metadata = (
        {
            "country": "US",
            "email": "someone@statsig.com",
            "locale": "en_US",
            "app_version": "1.2.3",
            "ip": "1.2.3.4",
            "user_agent": "Mozilla/5.0 Chrome/120.0.0.0",
            "custom": {"marker": "base", "CaseKey": "exact", "casekey": "lower"},
            "custom_ids": {
                "stableID": "stable-device",
                "companyID": "123",
                "random_id": "random-unit",
            },
            "private_attributes": {"secret_field": "private"},
            "statsig_environment": {"tier": "staging"},
        }
        if with_context
        else {}
    )
    context = StatsigUserContext(**metadata) if with_context else None
    options = _disabled()
    for overlay in (None, {}, {"marker": None}, {"marker": "changed", "country": "CA"}):
        merged = copy.deepcopy(metadata)
        if overlay is not None:
            merged["custom"] = {**merged.get("custom", {}), **overlay}
        user = StatsigUser(user_id, **merged)
        for name in current["specs"]["feature_gates"]:
            raw = sdk._INTERNAL_get_feature_gate(user, name, options)
            assert raw["name"] == name
            _assert_parts(
                name, sdk._INTERNAL_get_feature_gate_parts(user, name, options), raw
            )
            prepared_raw = sdk._INTERNAL_get_feature_gate_with_context(
                context, name, user_id, overlay, options
            )
            assert prepared_raw == raw, (name, user_id, overlay)
            parts = sdk._INTERNAL_get_feature_gate_with_context_parts(
                context, name, user_id, overlay, options
            )
            _assert_parts(name, parts, raw)
            expected = FeatureGate(name, raw)
            _assert_gate(sdk.get_feature_gate(user, name, options), expected)
            _assert_gate(
                sdk.get_feature_gate_with_context(
                    context, name, user_id, overlay, options
                ),
                expected,
            )


def test_missing_and_uninitialized_results_preserve_optional_metadata(make_sdk):
    sdk, _, _ = make_sdk(initialize=False)
    user = StatsigUser("defaults")
    context = StatsigUserContext()
    policy = StatsigRandomUserID("defaults", 16)
    options = _disabled()
    for initialized in (False, True):
        if initialized:
            assert sdk.initialize().wait(10)
        for name in ("missing_entity", "test_public"):
            raw = sdk._INTERNAL_get_feature_gate(user, name, options)
            _assert_parts(
                name, sdk._INTERNAL_get_feature_gate_parts(user, name, options), raw
            )
            _assert_parts(
                name,
                sdk._INTERNAL_get_feature_gate_with_context_parts(
                    context, name, user.user_id, options=options
                ),
                raw,
            )
            _assert_parts(
                name,
                sdk._INTERNAL_get_feature_gate_anonymous_parts(
                    name, policy, options=options
                ),
                raw,
            )
            expected = FeatureGate(name, raw)
            _assert_gate(sdk.get_feature_gate(user, name, options), expected)
            _assert_gate(
                sdk.get_feature_gate_with_context(
                    context, name, user.user_id, options=options
                ),
                expected,
            )
            _assert_gate(
                sdk.get_feature_gate_anonymous(name, policy, options=options), expected
            )
            if not initialized:
                assert expected.details.to_dict() == {
                    "reason": "Uninitialized",
                    "lcut": None,
                    "received_at": None,
                    "version": None,
                }
            elif name == "missing_entity":
                assert expected.details.reason.endswith(":Unrecognized")
                assert expected.details.version is None


def test_overrides_errors_and_zero_version_keep_native_metadata(make_sdk):
    specs = _specs()
    specs["feature_gates"]["test_public"]["version"] = 0
    unsupported = copy.deepcopy(specs["feature_gates"]["test_public"])
    unsupported["rules"][0]["conditions"] = ["missing-parts-test-condition"]
    specs["feature_gates"]["parts_unsupported"] = unsupported
    # A cyclic gate reaches the evaluator's bounded recursion error path.
    cyclic = copy.deepcopy(specs["feature_gates"]["test_public"])
    cyclic["rules"][0]["conditions"] = ["4100000100"]
    specs["feature_gates"]["parts_cycle"] = cyclic
    specs["condition_map"]["4100000100"] = {
        "type": "pass_gate",
        "targetValue": "parts_cycle",
        "operator": None,
        "field": None,
        "additionalValues": {},
        "idType": "userID",
    }
    sdk, _, _ = make_sdk(specs=specs)
    user = StatsigUser("override-user")
    context = StatsigUserContext()
    policy = StatsigRandomUserID("override", 16)
    options = _disabled()
    for overridden in (False, True, False):
        if overridden:
            sdk.override_gate("test_public", False)
        else:
            sdk.remove_gate_override("test_public")
        for name in ("test_public", "parts_unsupported", "parts_cycle"):
            raw = sdk._INTERNAL_get_feature_gate(user, name, options)
            _assert_parts(
                name, sdk._INTERNAL_get_feature_gate_parts(user, name, options), raw
            )
            _assert_parts(
                name,
                sdk._INTERNAL_get_feature_gate_with_context_parts(
                    context, name, user.user_id, options=options
                ),
                raw,
            )
            _assert_parts(
                name,
                sdk._INTERNAL_get_feature_gate_anonymous_parts(
                    name, policy, options=options
                ),
                raw,
            )
            expected = FeatureGate(name, raw)
            _assert_gate(sdk.get_feature_gate(user, name, options), expected)
            _assert_gate(
                sdk.get_feature_gate_with_context(
                    context, name, user.user_id, options=options
                ),
                expected,
            )
            _assert_gate(
                sdk.get_feature_gate_anonymous(name, policy, options=options), expected
            )
            if name == "parts_unsupported":
                assert expected.details.reason.endswith(":Unsupported")
            elif name == "parts_cycle":
                assert expected.value is False
                assert expected.details.reason.startswith("Error:")
                assert expected.details.lcut is None
                assert expected.details.received_at is None
                assert expected.details.version is None
            elif overridden:
                assert expected.value is False
                assert expected.details.reason == "LocalOverride:Recognized"
            else:
                assert expected.value is True
                assert expected.details.version == 0


@pytest.mark.parametrize(
    "parts",
    [
        (False, "", None, "", None, None, None),
        (False, "", "", "", 0, 0, 0),
        (True, "rule:override", "companyID", "LocalOverride:Recognized", 0, None, 0),
        (False, "default", None, "Error:evaluation failure", None, None, None),
        (
            True,
            "规则🚀",
            "custom-ID",
            "Network:Recognized",
            2**63,
            2**63 + 1,
            2**32 - 1,
        ),
    ],
)
def test_factory_preserves_defaults_and_ordinary_mutable_objects(parts):
    value, rule_id, id_type, reason, lcut, received_at, version = parts
    raw = {
        "value": value,
        "ruleID": rule_id,
        "idType": id_type,
        "details": {
            "reason": reason,
            "lcut": lcut,
            "received_at": received_at,
            "version": version,
        },
    }
    name = "mutable-规则"
    expected = FeatureGate(name, raw)
    actual = FeatureGate._from_parts(name, parts)
    _assert_gate(actual, expected)
    second = FeatureGate._from_parts(name, parts)
    assert actual is not second
    assert actual.details is not second.details
    actual.name = "changed"
    actual.rule_id = "caller-rule"
    actual.id_type = "caller-id"
    actual.value = not value
    actual.details.reason = "caller-reason"
    actual.details.lcut = 99
    actual.details.received_at = 100
    actual.details.version = 101
    actual.caller_attribute = "allowed"
    actual.details.caller_attribute = "also allowed"
    assert actual.to_dict() == {
        "name": "changed",
        "rule_id": "caller-rule",
        "id_type": "caller-id",
        "value": not value,
        "details": {
            "reason": "caller-reason",
            "lcut": 99,
            "received_at": 100,
            "version": 101,
        },
    }
    assert actual.caller_attribute == "allowed"
    assert actual.details.caller_attribute == "also allowed"
    _assert_gate(second, expected)


@pytest.mark.parametrize("entrypoint", ["parts", "public"])
@pytest.mark.parametrize("with_request", [False, True])
def test_anonymous_results_replay_each_logged_identity(
    make_sdk, entrypoint, with_request
):
    sdk, logs, current = make_sdk()
    base = {
        "country": "CA",
        "locale": "fr-CA",
        "ip": "192.0.2.10",
        "user_agent": "base-agent",
        "custom": {"marker": "base", "CaseKey": "exact", "country": "MX"},
        "custom_ids": {"stableID": "stable-device", "companyID": "123"},
        "private_attributes": {"secret_field": "private"},
        "statsig_environment": {"tier": "staging"},
    }
    request = (
        {
            "country": "",
            "locale": "en-US",
            "ip": "192.0.2.20",
            "user_agent": "request-agent",
        }
        if with_request
        else {}
    )
    context = StatsigUserContext(**base)
    policy = StatsigRandomUserID("parts-replay", 16)
    saved = []
    names = [*current["specs"]["feature_gates"], "missing_entity"]
    for index, name in enumerate(names):
        custom = {
            "request_number": index,
            "nested": [index],
            "marker": "base" if index % 2 else None,
        }
        metadata = copy.deepcopy(
            {**base, **request, "custom": {**base["custom"], **custom}}
        )
        if entrypoint == "parts":
            result = sdk._INTERNAL_get_feature_gate_anonymous_parts(
                name, policy, context=context, custom=custom, **request
            )
        else:
            result = sdk.get_feature_gate_anonymous(
                name, policy, context=context, custom=custom, **request
            )
        saved.append((name, result, metadata))
        custom["nested"].append("mutated-after-evaluation")
    assert sdk.flush_events().wait(10)
    events = _exposures(logs)
    assert len(events) == len(saved)
    by_index = {event["user"]["custom"]["request_number"]: event for event in events}
    assert len(by_index) == len(saved)
    assert len({event["user"]["userID"] for event in events}) == len(saved)
    for index, (name, result, metadata) in enumerate(saved):
        event = by_index[index]
        generated_id = event["user"]["userID"]
        assert re.fullmatch(r"parts-replay-[A-Za-z0-9]{16}", generated_id)
        assert event["user"]["custom"] == metadata["custom"]
        assert "privateAttributes" not in event["user"]
        assert event["metadata"]["gate"] == name
        user = StatsigUser(generated_id, **metadata)
        # Replay on the same SDK to retain identical receive-time metadata.
        raw = sdk._INTERNAL_get_feature_gate(user, name, _disabled())
        if entrypoint == "parts":
            _assert_parts(name, result, raw)
        else:
            _assert_gate(result, FeatureGate(name, raw))
        assert event["metadata"]["gateValue"] == str(raw["value"]).lower()
        assert event["metadata"]["ruleID"] == raw["ruleID"]
    assert sdk.flush_events().wait(10)
    assert len(_exposures(logs)) == len(saved)


@pytest.mark.parametrize("anonymous", [False, True])
@pytest.mark.parametrize("with_context", [False, True])
@pytest.mark.parametrize("entrypoint", ["parts", "public"])
def test_empty_custom_and_absent_custom_remain_distinct_in_exposures(
    make_sdk, anonymous, with_context, entrypoint
):
    sdk, logs, _ = make_sdk()
    context = StatsigUserContext() if with_context else None
    for label, custom in (("absent", None), ("empty", {})):
        if anonymous:
            method = (
                sdk._INTERNAL_get_feature_gate_anonymous_parts
                if entrypoint == "parts"
                else sdk.get_feature_gate_anonymous
            )
            method(
                "test_public",
                StatsigRandomUserID(label, 16),
                context=context,
                custom=custom,
            )
        else:
            method = (
                sdk._INTERNAL_get_feature_gate_with_context_parts
                if entrypoint == "parts"
                else sdk.get_feature_gate_with_context
            )
            method(context, "test_public", user_id=label, custom=custom)
    assert sdk.flush_events().wait(10)
    events = _exposures(logs)
    assert len(events) == 2
    users = {
        event["user"]["userID"].split("-", 1)[0]: event["user"] for event in events
    }
    assert "custom" not in users["absent"]
    assert users["empty"]["custom"] == {}


@pytest.mark.parametrize("kind", ["ordinary", "context", "anonymous"])
def test_callbacks_fire_once_per_call_and_exposures_keep_deduplication(make_sdk, kind):
    sdk, logs, _ = make_sdk()
    user = StatsigUser("callback-user")
    context = StatsigUserContext()
    policy = StatsigRandomUserID("callback", 16)
    name = "test_public"
    # The dictionary baseline must not add an exposure or a subscribed callback.
    raw = sdk._INTERNAL_get_feature_gate(user, name, _disabled())
    callbacks = []
    sdk.subscribe("gate_evaluated", callbacks.append)

    def evaluate(entrypoint, options=None):
        if kind == "ordinary":
            methods = {
                "raw": sdk._INTERNAL_get_feature_gate,
                "parts": sdk._INTERNAL_get_feature_gate_parts,
                "public": sdk.get_feature_gate,
            }
            return methods[entrypoint](user, name, options)
        if kind == "context":
            methods = {
                "raw": sdk._INTERNAL_get_feature_gate_with_context,
                "parts": sdk._INTERNAL_get_feature_gate_with_context_parts,
                "public": sdk.get_feature_gate_with_context,
            }
            return methods[entrypoint](context, name, user.user_id, options=options)
        methods = {
            "parts": sdk._INTERNAL_get_feature_gate_anonymous_parts,
            "public": sdk.get_feature_gate_anonymous,
        }
        return methods[entrypoint](name, policy, options=options)

    for entrypoint in ("parts", "public"):
        evaluate(entrypoint, _disabled())
    assert len(callbacks) == 2
    assert sdk.flush_events().wait(10)
    assert _exposures(logs) == []
    if kind != "anonymous":
        assert evaluate("raw") == raw
    for entrypoint in ("parts", "public", "parts", "public"):
        evaluate(entrypoint)
    assert len(callbacks) == (6 if kind == "anonymous" else 7)
    for event in callbacks:
        assert event["event_name"] == "gate_evaluated"
        assert event["data"] == {
            "gate_name": name,
            "rule_id": raw["ruleID"],
            "value": raw["value"],
            "reason": raw["details"]["reason"],
        }
    assert sdk.flush_events().wait(10)
    events = _exposures(logs)
    assert len(events) == (4 if kind == "anonymous" else 1)
    assert len({event["user"]["userID"] for event in events}) == len(events)
