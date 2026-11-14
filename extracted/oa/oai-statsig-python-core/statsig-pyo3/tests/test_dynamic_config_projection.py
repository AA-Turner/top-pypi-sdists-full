"""Projection against the compiled evaluator, normal specs and local overrides."""

import copy
import json
import multiprocessing
import time
import uuid
from functools import partial

import pytest
from statsig_python_core import (
    DynamicConfigEvaluationOptions,
    EvaluationCache,
    InternedStore,
    Statsig,
    StatsigOptions,
    StatsigUser,
)
import test_native_user_context as native_context
from utils import get_test_data_resource


make_native_sdk = native_context.make_sdk
PROJECTION_FLAG = "python_dynamic_config_field_projection"


@pytest.fixture
def make_sdk(make_native_sdk):
    return partial(make_native_sdk, experimental_flags={PROJECTION_FLAG})


def _specs():
    specs = json.loads(get_test_data_resource("eval_proj_dcs.json"))
    specs.pop("checksum", None)
    config = specs["dynamic_configs"]["big_number"]
    config["defaultValue"] = {
        "wanted": {"items": [None, True, 3, -4, 1.25, {"text": "æ"}]},
        "null": None,
        "ignored": {"models": [{"instructions": "unused"}]},
    }
    specs["condition_map"]["projection-marker"] = {
        "type": "user_field",
        "field": "marker",
        "operator": "any",
        "targetValue": ["target"],
        "additionalValues": {},
        "idType": "userID",
    }
    rule = dict(specs["feature_gates"]["test_public"]["rules"][0])
    rule.update(
        id="projection-target",
        conditions=["projection-marker"],
        returnValue={"wanted": {"items": ["targeted"]}, "ignored": [1, 2]},
    )
    config["rules"] = [rule]
    return specs


def _metadata(result):
    details = result.details
    return (
        result.name,
        result.rule_id,
        result.id_type,
        details.reason,
        details.lcut,
        details.version,
    )


def _wait_for_version(read, version):
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        result = read()
        if result.details.version == version:
            return result
        time.sleep(0.01)
    pytest.fail(f"SDK did not publish config version {version}")


def _exposure_payloads(sdk, logs):
    assert sdk.flush_events().wait(10)
    return [native_context._event_payload(event) for event in native_context._exposures(logs)]


@pytest.mark.parametrize("entry_limit", [None, 1024 * 1024, 128], ids=["no-cache", "admitted", "oversized"])
def test_projects_native_values_without_poisoning_full_value_cache(make_sdk, entry_limit):
    cache = EvaluationCache(max_entry_bytes=entry_limit) if entry_limit else None
    sdk, _, _ = make_sdk(specs=_specs(), evaluation_cache=cache)
    user = StatsigUser("projection-user")
    full = sdk.get_dynamic_config(user, "big_number")
    expected = copy.deepcopy(full.value)
    if entry_limit == 128:
        assert cache.oversized_bypasses == 1 and cache.entry_count == 0
    cache_counts = (cache.hits, cache.misses, cache.entry_count) if cache else None

    selected = sdk.get_dynamic_config_fields(
        user, "big_number", ("wanted", "null", "missing", "wanted")
    )
    assert selected.value == {"wanted": full.value["wanted"], "null": None}
    assert _metadata(selected) == _metadata(full)
    assert type(selected.value) is dict
    assert type(selected.value["wanted"]) is dict
    assert type(selected.value["wanted"]["items"]) is list
    selected.value["wanted"]["items"][-1]["text"] = "changed"
    selected.value["wanted"]["items"].append("changed")

    again = sdk.get_dynamic_config_fields(user, "big_number", ["wanted"])
    assert again.value == {"wanted": expected["wanted"]}
    assert selected.value["wanted"]["items"][-1] == "changed"
    if cache is not None:
        assert (cache.hits, cache.misses, cache.entry_count) == cache_counts
    assert sdk.get_dynamic_config(user, "big_number").value == expected
    assert "ignored" in expected


@pytest.mark.parametrize("flag_options", [{}, {"experimental_flags": set()}])
def test_disabled_projection_skips_selectors_and_uses_full_cache(make_native_sdk, flag_options):
    cache = EvaluationCache()
    sdk, logs, _ = make_native_sdk(specs=_specs(), evaluation_cache=cache, **flag_options)
    user = StatsigUser("flag-off", custom={"marker": "target"})
    # None would fail selector validation on the projection path.
    actual = sdk.get_dynamic_config_fields(user, "big_number", None)
    full = sdk.get_dynamic_config(user, "big_number", DynamicConfigEvaluationOptions(
        disable_exposure_logging=True,
    ))
    assert actual.value is full.value
    assert set(actual.value) == {"wanted", "ignored"}
    assert _metadata(actual) == _metadata(full)
    assert cache.hits == 1
    assert len(_exposure_payloads(sdk, logs)) == 1


def test_missing_argument_uses_instance_error_boundary(make_sdk):
    sdk, _, _ = make_sdk(specs=_specs())
    assert sdk.get_dynamic_config_fields(StatsigUser("user"), "big_number") is None


def test_projection_reuses_plain_selectors_and_normalizes_str_subclasses(make_sdk):
    class Selector(str):
        def __hash__(self):
            raise AssertionError("str subclass reached dictionary membership")

        def __eq__(self, other):
            raise AssertionError("str subclass reached dictionary comparison")

    sdk, _, _ = make_sdk(specs=_specs())
    wanted = bytearray(b"wanted").decode()
    selected = sdk.get_dynamic_config_fields(StatsigUser("user"), "big_number", [wanted, Selector("null")])
    wanted_key, null_key = selected.value
    assert wanted_key is wanted
    assert type(null_key) is str and null_key == "null"


def test_projected_config_honors_explicit_freeze(make_sdk):
    sdk, _, _ = make_sdk(specs=_specs())
    config = sdk.get_dynamic_config_fields(
        StatsigUser("frozen"), "big_number", ["wanted"],
        DynamicConfigEvaluationOptions(freeze_value=True),
    )
    assert set(config.value) == {"wanted"}
    with pytest.raises(TypeError):
        config.value["wanted"]["items"].append("change")


@pytest.mark.parametrize("fields", ["wanted", b"wanted", None, ["wanted", 4]])
def test_projection_rejects_invalid_fields_through_error_boundary(make_sdk, fields):
    sdk, _, _ = make_sdk(specs=_specs())
    assert sdk.get_dynamic_config_fields(StatsigUser("user"), "big_number", fields) is None


@pytest.mark.parametrize("initialize", [False, True])
def test_missing_and_uninitialized_configs_preserve_metadata_and_defaults(make_sdk, initialize):
    sdk, _, _ = make_sdk(specs=_specs(), initialize=initialize)
    user = StatsigUser("missing-user")
    full = sdk.get_dynamic_config(user, "missing-config")
    selected = sdk.get_dynamic_config_fields(
        user, "missing-config", ["wanted"], DynamicConfigEvaluationOptions(freeze_value=True),
    )
    assert selected.value == full.value == {}
    assert _metadata(selected) == _metadata(full)
    with pytest.raises(TypeError):
        selected.value["unexpected"] = True


def test_user_changes_and_local_overrides_remain_fresh(make_sdk):
    sdk, _, _ = make_sdk(specs=_specs())
    user = StatsigUser("changing-user", custom={"marker": "base"})
    original = sdk.get_dynamic_config_fields(user, "big_number", ["wanted"])
    user.custom = {"marker": "target"}
    targeted = sdk.get_dynamic_config_fields(user, "big_number", ["wanted"])
    assert targeted.value == {"wanted": {"items": ["targeted"]}}
    assert targeted.rule_id == "projection-target"
    assert original.rule_id != targeted.rule_id
    assert original.value["wanted"]["items"][0] is None

    for value in [1, 2]:
        sdk.override_dynamic_config(
            "big_number", {"wanted": {"items": [value]}, "ignored": value}, "changing-user"
        )
        selected = sdk.get_dynamic_config_fields(user, "big_number", ["wanted"])
        assert selected.value == {"wanted": {"items": [value]}}
        assert _metadata(selected) == _metadata(sdk.get_dynamic_config(user, "big_number"))
    sdk.remove_dynamic_config_override("big_number", "changing-user")
    assert sdk.get_dynamic_config_fields(user, "big_number", ["wanted"]).value == targeted.value


def test_first_projection_after_new_spec_publication_observes_new_rule_and_value(make_sdk):
    sdk, _, current = make_sdk(
        specs=_specs(), specs_sync_interval_ms=1000,
        evaluation_cache=EvaluationCache(),
    )
    user = StatsigUser("update-user", custom={"marker": "target"})
    previous = sdk.get_dynamic_config_fields(user, "big_number", ["wanted"])
    replacement = copy.deepcopy(current["specs"])
    replacement["time"] += 1000
    config = replacement["dynamic_configs"]["big_number"]
    config["version"] += 1
    config["rules"][0]["id"] = "projection-updated"
    config["rules"][0]["returnValue"]["wanted"] = {"items": ["updated"]}
    current["specs"] = replacement
    full = _wait_for_version(lambda: sdk.get_dynamic_config(user, "big_number"), config["version"])

    selected = sdk.get_dynamic_config_fields(user, "big_number", ["wanted"])
    assert selected.value == {"wanted": {"items": ["updated"]}}
    assert selected.rule_id == "projection-updated"
    assert _metadata(selected) == _metadata(full)
    assert previous.value == {"wanted": {"items": ["targeted"]}}


def test_exposures_and_private_attribute_handling_match_full_reads(make_sdk):
    control, control_logs, _ = make_sdk(specs=_specs())
    treatment, treatment_logs, _ = make_sdk(specs=_specs())
    for marker, disabled in [("base", False), ("target", False), ("base", True), ("target", True)]:
        user = StatsigUser(
            f"{marker}-{disabled}",
            custom={"marker": marker},
            private_attributes={"private": "never-log"},
        )
        options = DynamicConfigEvaluationOptions(disable_exposure_logging=disabled)
        full = control.get_dynamic_config(user, "big_number", options)
        selected = treatment.get_dynamic_config_fields(user, "big_number", ["wanted"], options)
        assert selected.value == {"wanted": full.value["wanted"]}
        assert _metadata(selected) == _metadata(full)
    actual = _exposure_payloads(treatment, treatment_logs)
    assert actual == _exposure_payloads(control, control_logs)
    assert sorted(event["user"]["userID"] for event in actual) == ["base-False", "target-False"]
    assert all("privateAttributes" not in event["user"] for event in actual)


def test_empty_projection_still_evaluates_and_exposes(make_sdk):
    sdk, logs, _ = make_sdk(specs=_specs())
    selected = sdk.get_dynamic_config_fields(
        StatsigUser("empty-fields", custom={"marker": "target"}), "big_number", []
    )
    assert selected.value == {}
    assert selected.rule_id == "projection-target"
    assert len(_exposure_payloads(sdk, logs)) == 1


def test_projection_with_mmap_specs_uses_owned_selected_subtrees(httpserver):
    # mmap preload is process-wide. Serve the fixture to an isolated interpreter.
    httpserver.expect_request("/specs").respond_with_json(_specs())
    httpserver.expect_request("/events").respond_with_json({"success": True})
    with multiprocessing.get_context("spawn").Pool(1) as pool:
        urls = httpserver.url_for("/specs"), httpserver.url_for("/events")
        pool.apply_async(_assert_mmap_projection, urls).get(timeout=30)


def _assert_mmap_projection(specs_url, events_url):
    key = f"secret-projection-{uuid.uuid4()}"
    assert InternedStore.fetch_and_write_mmap(key, specs_url).wait(10)
    assert InternedStore.preload_mmap([key], optional=[]).loaded == 1
    assert InternedStore.mmap_reader_memory_snapshot().mapped_bytes > 0
    sdk = Statsig(key, StatsigOptions(
        specs_url=specs_url, log_event_url=events_url, experimental_flags={PROJECTION_FLAG},
    ))
    try:
        assert sdk.initialize().wait(10)
        user = StatsigUser("mmap-user")
        full = sdk.get_dynamic_config(user, "big_number")
        selected = sdk.get_dynamic_config_fields(user, "big_number", ["wanted"])
        assert selected.value == {"wanted": full.value["wanted"]}
        selected.value["wanted"]["items"].append("changed")
        assert sdk.get_dynamic_config_fields(user, "big_number", ["wanted"]).value == {
            "wanted": full.value["wanted"]
        }
    finally:
        assert sdk.shutdown().wait(10)
