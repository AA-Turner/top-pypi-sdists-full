"""Typed boundary qualification against real Rust evaluation and HTTP polling."""

import base64
import copy
import gc
import hashlib
import json
from queue import Queue
from threading import Condition
from time import monotonic, sleep
from weakref import ref

import pytest
from google.protobuf.descriptor_pb2 import FieldDescriptorProto
from google.protobuf.struct_pb2 import Struct
from mock_scrapi import MockScrapi
from statsig_python_core import (
    DynamicConfigEvaluationOptions,
    Statsig,
    StatsigOptions,
    StatsigUser,
    TypedConfigConversionError,
    TypedConfigUnavailableError,
)
from werkzeug import Response


def _rule(condition, value, *, group=False):
    return {
        "name": "selected",
        "id": "selected",
        "salt": "selected",
        "conditions": [condition],
        "passPercentage": 100,
        "returnValue": value,
        "idType": "userID",
        "isExperimentGroup": group,
        "groupName": "Treatment" if group else None,
    }


def _config(condition, value, *, experiment=False):
    return {
        "type": "dynamic_config",
        "salt": "typed",
        "enabled": True,
        "defaultValue": {},
        "idType": "userID",
        "version": 1,
        "entity": "experiment" if experiment else "dynamic_config",
        "rules": [_rule(condition, value, group=experiment)],
    }


def _specs():
    return {
        "time": 1_800_000_100_001,
        "has_updates": True,
        "feature_gates": {},
        "layer_configs": {},
        "experiment_to_layer": {},
        "condition_map": {
            "public": {
                "type": "public",
                "operator": "any",
                "targetValue": None,
                "idType": "userID",
            },
            "marker": {
                "type": "user_field",
                "field": "marker",
                "operator": "any",
                "targetValue": ["A"],
                "additionalValues": {},
                "idType": "userID",
            },
            "experiment": {
                "type": "experiment_group",
                "field": "source_experiment",
                "operator": "any",
                "targetValue": ["Treatment"],
                "additionalValues": {"experiment_name": "source_experiment"},
                "idType": "userID",
            },
        },
        "dynamic_configs": {
            "typed": _config("public", {"number": 1}),
            "empty": _config("public", {}),
            "null": _config("public", None),
            "context": _config("marker", {"selected": "A"}),
            "source_experiment": _config(
                "public", {"group": "Treatment"}, experiment=True
            ),
            "parent": _config("experiment", {"nested": True}),
        },
    }


@pytest.fixture
def native_sdk(httpserver):
    current = {"specs": _specs(), "requests": [], "condition": Condition()}

    def respond(request):
        with current["condition"]:
            specs = current["specs"]
            current["requests"].append((specs["time"], request.args.get("sinceTime")))
            current["condition"].notify_all()
        return Response(
            json.dumps(specs),
            status=current.get("status", 200),
            mimetype="application/json",
        )

    httpserver.expect_request("/v2/download_config_specs").respond_with_handler(respond)
    scrapi = MockScrapi(httpserver)
    scrapi.stub("/v1/log_event", response='{"success":true}', method="POST")
    sdk = Statsig(
        "secret-typed-native-test",
        StatsigOptions(
            specs_url=httpserver.url_for("/v2/download_config_specs"),
            log_event_url=httpserver.url_for("/v1/log_event"),
            specs_sync_interval_ms=1000,
            fallback_to_statsig_api=False,
            enable_id_lists=False,
            output_log_level="none",
        ),
    )
    try:
        assert sdk.initialize().wait(10)
        assert sdk.is_config_spec_ready()
        yield sdk, scrapi, current
    finally:
        assert sdk.shutdown().wait(10)


def _wait_for(predicate):
    deadline = monotonic() + 10
    while monotonic() < deadline:
        if predicate():
            return
        sleep(0.01)
    pytest.fail("Timed out waiting for native publication")


def _read(sdk, name="typed", user=None, *, message_type=Struct):
    return sdk.get_typed_config(
        name,
        user or StatsigUser("user"),
        options=DynamicConfigEvaluationOptions(disable_exposure_logging=True),
        message_type=message_type,
    )


def _publish(current, name="typed", *, value=None, version=None):
    updated = copy.deepcopy(current["specs"])
    updated["time"] += 1
    config = updated["dynamic_configs"][name]
    if version is not None:
        config["version"] = version
    if value is not None:
        config["rules"][0]["returnValue"] = value
    current["specs"] = updated
    return updated["time"]


def test_native_current_users_attributes_options_and_coherent_metadata(native_sdk):
    sdk, _, _ = native_sdk
    first_user = StatsigUser("first", custom={"marker": "A"})
    second_user = StatsigUser("second", custom={"marker": "B"})
    for user, expected in (
        (first_user, {"selected": "A"}),
        (second_user, {}),
        (first_user, {"selected": "A"}),
    ):
        result = _read(sdk, "context", user)
        ordinary = sdk.get_dynamic_config(user, "context")
        assert result.value == ordinary.value == expected
        assert result.to_dict() == ordinary.to_dict()
    first_user.custom = {"marker": "B"}
    assert _read(sdk, "context", first_user).value == {}
    first_user.custom = {"marker": "A"}
    assert _read(sdk, "context", first_user).value == {"selected": "A"}
    for index in range(100):
        assert _read(sdk, user=StatsigUser(str(index))).value == {"number": 1}
    assert sdk._typed_configs.observers == []
    assert sdk._typed_configs._worker is None


def test_native_empty_missing_null_and_override_parity(native_sdk):
    sdk, _, _ = native_sdk
    empty = _read(sdk, "empty")
    assert empty.value == {}
    assert empty.details.reason == "Network:Recognized"
    assert empty.get_rule_id() == "selected" and empty.get_id_type() == "userID"
    for name in ("missing", "null"):
        with pytest.raises(TypedConfigUnavailableError):
            _read(sdk, name)
    sdk.override_dynamic_config("typed", {"number": 2})
    overridden = _read(sdk)
    assert (
        overridden.value
        == sdk.get_dynamic_config(StatsigUser("user"), "typed").value
        == {"number": 2}
    )
    assert overridden.details.reason == "LocalOverride:Recognized"
    sdk.remove_all_overrides()
    assert _read(sdk).value == {"number": 1}
    assert overridden.value == {"number": 2}


def test_native_argument_errors_are_not_swallowed(native_sdk):
    sdk, _, _ = native_sdk
    for name, user, options in (
        ("typed", object(), None),
        (object(), StatsigUser("user"), None),
        ("typed", StatsigUser("user"), object()),
    ):
        with pytest.raises(TypeError):
            sdk.get_typed_config(name, user, message_type=Struct, options=options)


def test_native_every_usable_read_reconverts(native_sdk):
    sdk, _, _ = native_sdk
    results = [_read(sdk) for _ in range(20)]
    assert all(result.value["number"] == 1 for result in results)
    assert all(
        result.to_dict()["details"] == results[0].to_dict()["details"]
        for result in results
    )
    assert len({id(result.value) for result in results}) == 20


def test_native_ordinary_exposures_nested_safeguards_and_observer_silence(native_sdk):
    sdk, scrapi, current = native_sdk
    user = StatsigUser("user")
    evaluated, callbacks = [], Queue()
    sdk.subscribe("dynamic_config_evaluated", evaluated.append)
    sdk.subscribe("experiment_evaluated", evaluated.append)
    sdk.register_typed_config_callback(
        "parent", user, callbacks.put, message_type=Struct
    )
    assert callbacks.empty()
    _publish(current, "parent", value={"nested": "updated"}, version=2)
    assert callbacks.get(timeout=10).value == {"nested": "updated"}
    assert sdk.flush_events().wait(10)
    assert not any(
        event["eventName"].endswith("_exposure") for event in scrapi.get_logged_events()
    )
    assert _read(sdk, "parent").value == {"nested": "updated"}
    assert sdk.flush_events().wait(10)
    assert not any(
        event["eventName"].endswith("_exposure") for event in scrapi.get_logged_events()
    )
    assert sdk.get_typed_config("parent", user, message_type=Struct).value == {
        "nested": "updated"
    }
    assert sdk.get_experiment(user, "source_experiment").group_name == "Treatment"
    assert sdk.flush_events().wait(10)
    exposures = [
        event["metadata"]["config"]
        for event in scrapi.get_logged_events()
        if event["eventName"] == "statsig::config_exposure"
    ]
    assert exposures == ["parent", "source_experiment"]
    assert {event["event_name"] for event in evaluated} == {
        "dynamic_config_evaluated",
        "experiment_evaluated",
    }


def test_native_conversion_error_does_not_undo_exposure_or_substitute(native_sdk):
    sdk, scrapi, current = native_sdk
    first = sdk.get_typed_config(
        "typed", StatsigUser("first"), message_type=FieldDescriptorProto
    )
    lcut = _publish(current, value={"number": "invalid"}, version=2)
    _wait_for(lambda: _read(sdk).details.lcut == lcut)
    for user_id in ("first", "new"):
        with pytest.raises(TypedConfigConversionError) as caught:
            sdk.get_typed_config(
                "typed", StatsigUser(user_id), message_type=FieldDescriptorProto
            )
        assert caught.value.__cause__ is not None
    assert first.value.number == 1 and first.details.version == 1
    assert sdk.flush_events().wait(10)
    assert any(
        event["user"]["userID"] == "new"
        for event in scrapi.get_logged_events()
        if event["eventName"] == "statsig::config_exposure"
    )


def test_native_background_revisions_no_replay_and_independent_getter(
    native_sdk, monkeypatch
):
    sdk, _, current = native_sdk
    user = StatsigUser("user")
    observed, callbacks = Queue(), Queue()

    observe = sdk._typed_configs._observe

    def observed_evaluation(observer, *, baseline=False):
        try:
            observe(observer, baseline=baseline)
        finally:
            observed.put(None)

    monkeypatch.setattr(sdk._typed_configs, "_observe", observed_evaluation)

    def on_config(result):
        callbacks.put((result, _read(sdk)))

    sdk.register_typed_config_callback("typed", user, on_config, message_type=Struct)
    observed.get(timeout=5)
    assert callbacks.empty()
    lcut = _publish(current, "empty", version=2)
    _wait_for(lambda: _read(sdk).details.lcut == lcut)
    observed.get(timeout=5)
    assert callbacks.empty()
    for version in (2, 1):
        lcut = _publish(current, version=version)
        delivered, latest = callbacks.get(timeout=10)
        assert delivered.value == latest.value == {"number": 1}
        assert delivered.value is not latest.value
        assert delivered.details.version == version and delivered.details.lcut == lcut
        assert latest.details.reason == "Network:Recognized"
        assert callbacks.empty()


def test_native_rejected_update_reports_error_then_recovers_without_last_good(
    native_sdk,
):
    sdk, _, current = native_sdk
    user, callbacks = StatsigUser("user"), Queue()

    options = {"message_type": FieldDescriptorProto}
    first = _read(sdk, **options)
    sdk.register_typed_config_callback("typed", user, callbacks.put, **options)
    lcut = _publish(current, value={"number": "invalid"}, version=2)
    _wait_for(lambda: _read(sdk).details.lcut == lcut)
    _wait_for(
        lambda: sdk._typed_configs.observers[0].error == "TypedConfigConversionError"
    )
    for caller in (user, StatsigUser("unseen")):
        with pytest.raises(TypedConfigConversionError):
            _read(sdk, user=caller, **options)
    assert callbacks.empty()
    _publish(current, value={"number": 3}, version=3)
    delivered = callbacks.get(timeout=10)
    assert (
        delivered.details.version == 3
        and delivered.details.reason == "Network:Recognized"
    )
    assert delivered.value == _read(sdk, **options).value
    assert first.details.version == 1


@pytest.mark.parametrize("failure", ["stale", "http_failure"])
def test_native_retained_specs_evaluate_unseen_users_after_refresh_failure(
    native_sdk, failure
):
    sdk, _, current = native_sdk
    first = _read(sdk)
    if failure == "stale":
        stale = copy.deepcopy(current["specs"])
        stale["time"] -= 1
        stale["dynamic_configs"]["typed"]["rules"][0]["returnValue"] = {"number": 99}
        current["specs"] = stale
    else:
        current["status"] = 500
    with current["condition"]:
        initial_count = len(current["requests"])
        assert current["condition"].wait_for(
            lambda: len(current["requests"]) >= initial_count + 2,
            timeout=10,
        )
    unseen = _read(sdk, user=StatsigUser("previously-unseen"))
    assert unseen.value == first.value == {"number": 1}
    assert unseen.details.lcut == first.details.lcut
    assert unseen.details.version == first.details.version
    assert unseen.value is not first.value


def test_native_callback_initiated_shutdown_stops_worker(native_sdk):
    sdk, _, current = native_sdk
    completed, forbidden = Queue(), []

    def stop(result):
        future = sdk.shutdown()
        completed.put((result, future))

    sdk.register_typed_config_callback(
        "typed", StatsigUser("user"), stop, message_type=Struct
    )
    sdk.register_typed_config_callback(
        "typed", StatsigUser("other"), forbidden.append, message_type=Struct
    )
    _publish(current, version=2)
    result, future = completed.get(timeout=10)
    assert result.details.version == 2 and future.wait(10)
    sdk._typed_configs._worker.join(5)
    assert not sdk._typed_configs._worker.is_alive()
    assert sdk._typed_configs.observers == [] and forbidden == []


def test_native_shutdown_releases_sdk_capturing_observer_closures(native_sdk):
    sdk, _, _ = native_sdk

    def callback(result, owner=sdk):
        assert owner.is_initialized()

    callback_ref = ref(callback)
    sdk.register_typed_config_callback(
        "typed",
        StatsigUser("user"),
        callback,
        message_type=Struct,
    )
    del callback
    assert sdk.shutdown().wait(10)
    gc.collect()
    assert callback_ref() is None
    assert sdk._typed_configs.observers == []


def test_id_list_only_publication_updates_typed_selection_without_lcut_change(
    httpserver,
):
    specs = _specs()
    specs["condition_map"]["member"] = {
        "type": "unit_id",
        "operator": "in_segment_list",
        "targetValue": "members",
        "idType": "userID",
    }
    specs["dynamic_configs"]["typed"] = _config("member", {"number": 2})
    specs["dynamic_configs"]["typed"]["defaultValue"] = {"number": 1}

    def body_for(user_id):
        encoded = base64.b64encode(hashlib.sha256(user_id.encode()).digest()).decode()
        return "+" + encoded[:8] + "\n"

    current = {"generation": 1, "body": body_for("other-user")}
    downloads = []
    specs_sent = False

    def download_specs(_request):
        nonlocal specs_sent
        response = (
            specs if not specs_sent else {"has_updates": False, "time": specs["time"]}
        )
        specs_sent = True
        return Response(json.dumps(response), mimetype="application/json")

    def manifest(_request):
        return Response(
            json.dumps(
                {
                    "members": {
                        "name": "members",
                        "url": httpserver.url_for("/members"),
                        "size": len(current["body"]),
                        "creationTime": current["generation"],
                        "fileID": str(current["generation"]),
                    }
                }
            ),
            mimetype="application/json",
        )

    def download(_request):
        downloads.append(current["generation"])
        return Response(current["body"], mimetype="text/plain")

    httpserver.expect_request("/v2/download_config_specs").respond_with_handler(
        download_specs
    )
    httpserver.expect_request("/v1/get_id_lists").respond_with_handler(manifest)
    httpserver.expect_request("/members").respond_with_handler(download)
    httpserver.expect_request("/v1/log_event").respond_with_json({"success": True})
    sdk = Statsig(
        "secret-typed-id-list-test",
        StatsigOptions(
            specs_url=httpserver.url_for("/v2/download_config_specs"),
            id_lists_url=httpserver.url_for("/v1/get_id_lists"),
            log_event_url=httpserver.url_for("/v1/log_event"),
            specs_sync_interval_ms=1000,
            id_lists_sync_interval_ms=1000,
            fallback_to_statsig_api=False,
            enable_id_lists=True,
            output_log_level="none",
        ),
    )
    try:
        assert sdk.initialize().wait(10) and sdk.is_initialized()
        assert 1 in downloads
        user, callbacks = StatsigUser("user"), Queue()
        first = _read(sdk)
        assert first.value == {"number": 1}
        sdk.register_typed_config_callback(
            "typed", user, callbacks.put, message_type=Struct
        )
        assert callbacks.empty()
        current.update(generation=2, body=body_for("user"))
        updated = callbacks.get(timeout=10)
        assert updated.value == {"number": 2}
        assert updated.details.lcut == first.details.lcut == specs["time"]
        assert (
            updated.details.version == 1
            and updated.details.reason == "Network:Recognized"
        )
        assert updated._revision != first._revision
        assert _read(sdk).value == updated.value and callbacks.empty()
        assert 2 in downloads and first.value == {"number": 1}
    finally:
        assert sdk.shutdown().wait(10)
