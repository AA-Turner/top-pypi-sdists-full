import gzip
import json
from typing import Any

from pytest_httpserver import HTTPServer
from statsig_python_core import (
    BulkEvaluationOptions,
    Statsig,
    StatsigOptions,
    StatsigUser,
)

from mock_scrapi import MockScrapi
from utils import get_test_data_resource


def _assert_common_evaluation_fields(
    *,
    name: str,
    gcir_evaluation: dict[str, Any],
    bulk_evaluation: dict[str, Any],
) -> None:
    assert bulk_evaluation["value"] == gcir_evaluation["value"], name
    assert bulk_evaluation["ruleID"] == gcir_evaluation["rule_id"], name
    assert bulk_evaluation["idType"] == gcir_evaluation.get("id_type"), name
    assert bulk_evaluation["details"]["reason"].endswith(":Recognized"), name


def _decode_log_event_requests(mock_scrapi: MockScrapi) -> list[dict[str, Any]]:
    events = []
    for request in mock_scrapi.get_requests_for_endpoint("/v1/log_event"):
        payload = json.loads(gzip.decompress(request.get_data()))
        events.extend(payload["events"])
    return [
        event
        for event in events
        if event.get("eventName") != "statsig::diagnostics"
    ]


def _first_token(
    section: dict[str, dict[str, Any]],
) -> tuple[str, dict[str, Any], str]:
    for name, evaluation in section.items():
        token = evaluation["exposureToken"]
        if token is not None:
            return name, evaluation, token
    raise AssertionError("Expected at least one delayed exposure token")


def _first_layer_token_with_param(
    section: dict[str, dict[str, Any]],
) -> tuple[str, dict[str, Any], str, str]:
    for name, evaluation in section.items():
        token = evaluation["exposureToken"]
        value = evaluation["value"]
        if token is not None and value:
            return name, evaluation, token, next(iter(value.keys()))
    raise AssertionError("Expected at least one delayed layer token with a parameter")


def test_bulk_evaluate_all_entities_matches_gcir(httpserver: HTTPServer):
    mock_scrapi = MockScrapi(httpserver)
    dcs_content = get_test_data_resource("eval_proj_dcs.json")
    specs = json.loads(dcs_content)
    mock_scrapi.stub(
        "/v2/download_config_specs/secret-key.json", response=dcs_content, method="GET"
    )
    mock_scrapi.stub("/v1/log_event", response='{"success": true}', method="POST")

    options = StatsigOptions()
    options.specs_url = mock_scrapi.url_for_endpoint("/v2/download_config_specs")
    options.log_event_url = mock_scrapi.url_for_endpoint("/v1/log_event")
    options.output_log_level = "none"

    statsig = Statsig("secret-key", options)
    statsig.initialize().wait()

    try:
        user = StatsigUser("bulk-gcir-parity-user")
        gcir = json.loads(statsig.get_client_initialize_response(user, hash="none"))

        feature_gate_names = list(gcir["feature_gates"].keys())
        layer_names = list(gcir["layer_configs"].keys())
        dynamic_config_names = []
        experiment_names = []

        for name in gcir["dynamic_configs"].keys():
            spec = specs["dynamic_configs"][name]
            if spec.get("entity") == "experiment":
                experiment_names.append(name)
            else:
                dynamic_config_names.append(name)

        bulk = statsig.bulk_evaluate(user)

        assert set(bulk["feature_gates"].keys()) == set(feature_gate_names)
        assert set(bulk["dynamic_configs"].keys()) == set(dynamic_config_names)
        assert set(bulk["experiments"].keys()) == set(experiment_names)
        assert set(bulk["layer_configs"].keys()) == set(layer_names)

        for name in feature_gate_names:
            _assert_common_evaluation_fields(
                name=name,
                gcir_evaluation=gcir["feature_gates"][name],
                bulk_evaluation=bulk["feature_gates"][name],
            )

        for name in dynamic_config_names:
            _assert_common_evaluation_fields(
                name=name,
                gcir_evaluation=gcir["dynamic_configs"][name],
                bulk_evaluation=bulk["dynamic_configs"][name],
            )

        for name in experiment_names:
            _assert_common_evaluation_fields(
                name=name,
                gcir_evaluation=gcir["dynamic_configs"][name],
                bulk_evaluation=bulk["experiments"][name],
            )

        for name in layer_names:
            _assert_common_evaluation_fields(
                name=name,
                gcir_evaluation=gcir["layer_configs"][name],
                bulk_evaluation=bulk["layer_configs"][name],
            )

        assert mock_scrapi.get_logged_events() == []

        gate_name, _, gate_token = _first_token(bulk["feature_gates"])
        config_name, _, config_token = _first_token(bulk["dynamic_configs"])
        experiment_name, _, experiment_token = _first_token(bulk["experiments"])
        layer_name, _, layer_token, parameter_name = _first_layer_token_with_param(
            bulk["layer_configs"]
        )

        assert statsig.log_delayed_exposure(gate_token) is True
        assert statsig.log_delayed_exposure(config_token) is True
        assert statsig.log_delayed_exposure(experiment_token) is True
        assert (
            statsig.log_delayed_layer_parameter_exposure(layer_token, parameter_name)
            is True
        )
        assert statsig.log_delayed_exposure(gate_token) is False

        statsig.flush_events().wait()
        logged_events = _decode_log_event_requests(mock_scrapi)

        gate_events = [
            event
            for event in logged_events
            if event["eventName"] == "statsig::gate_exposure"
            and event["metadata"]["gate"] == gate_name
        ]
        config_events = [
            event
            for event in logged_events
            if event["eventName"] == "statsig::config_exposure"
            and event["metadata"]["config"] == config_name
        ]
        experiment_events = [
            event
            for event in logged_events
            if event["eventName"] == "statsig::config_exposure"
            and event["metadata"]["config"] == experiment_name
        ]
        layer_events = [
            event
            for event in logged_events
            if event["eventName"] == "statsig::layer_exposure"
            and event["metadata"]["config"] == layer_name
            and event["metadata"]["parameterName"] == parameter_name
        ]

        assert len(gate_events) == 1
        assert len(config_events) == 1
        assert len(experiment_events) == 1
        assert len(layer_events) == 1

        consumed_tokens = {gate_token, config_token, experiment_token}
        tokens_to_release = [
            evaluation["exposureToken"]
            for section in bulk.values()
            for evaluation in section.values()
            if evaluation["exposureToken"] is not None
            and evaluation["exposureToken"] not in consumed_tokens
        ]
        assert statsig.release_delayed_exposures(tokens_to_release) == len(
            tokens_to_release
        )
    finally:
        statsig.shutdown().wait()


def test_bulk_evaluate_filter_semantics(httpserver: HTTPServer):
    mock_scrapi = MockScrapi(httpserver)
    dcs_content = get_test_data_resource("eval_proj_dcs.json")
    mock_scrapi.stub(
        "/v2/download_config_specs/secret-key.json", response=dcs_content, method="GET"
    )
    mock_scrapi.stub("/v1/log_event", response='{"success": true}', method="POST")

    options = StatsigOptions()
    options.specs_url = mock_scrapi.url_for_endpoint("/v2/download_config_specs")
    options.log_event_url = mock_scrapi.url_for_endpoint("/v1/log_event")
    options.output_log_level = "none"

    statsig = Statsig("secret-key", options)
    statsig.initialize().wait()

    try:
        user = StatsigUser("bulk-filter-semantics-user")

        all_results = statsig.bulk_evaluate(user)
        assert all_results["feature_gates"]
        assert all_results["dynamic_configs"]
        assert all_results["experiments"]
        assert all_results["layer_configs"]

        no_gates = statsig.bulk_evaluate(
            user,
            BulkEvaluationOptions(feature_gate_filter=[]),
        )
        assert no_gates["feature_gates"] == {}
        assert no_gates["dynamic_configs"]
        assert no_gates["experiments"]
        assert no_gates["layer_configs"]

        no_results = statsig.bulk_evaluate(
            user,
            BulkEvaluationOptions(
                feature_gate_filter=[],
                dynamic_config_filter=[],
                experiment_filter=[],
                layer_filter=[],
            ),
        )
        assert no_results == {
            "feature_gates": {},
            "dynamic_configs": {},
            "experiments": {},
            "layer_configs": {},
        }
    finally:
        statsig.shutdown().wait()


def test_bulk_evaluate_options_can_skip_local_overrides(httpserver: HTTPServer):
    mock_scrapi = MockScrapi(httpserver)
    dcs_content = get_test_data_resource("eval_proj_dcs.json")
    mock_scrapi.stub(
        "/v2/download_config_specs/secret-key.json", response=dcs_content, method="GET"
    )
    mock_scrapi.stub("/v1/log_event", response='{"success": true}', method="POST")

    options = StatsigOptions()
    options.specs_url = mock_scrapi.url_for_endpoint("/v2/download_config_specs")
    options.log_event_url = mock_scrapi.url_for_endpoint("/v1/log_event")
    options.output_log_level = "none"

    statsig = Statsig("secret-key", options)
    statsig.initialize().wait()

    try:
        user = StatsigUser("bulk-local-override-user")
        statsig.override_gate("test_public", False)

        with_override = statsig.bulk_evaluate(
            user,
            BulkEvaluationOptions(
                feature_gate_filter=["test_public"],
                dynamic_config_filter=[],
                experiment_filter=[],
                layer_filter=[],
            ),
        )
        without_override = statsig.bulk_evaluate(
            user,
            BulkEvaluationOptions(
                feature_gate_filter=["test_public"],
                dynamic_config_filter=[],
                experiment_filter=[],
                layer_filter=[],
                include_local_override=False,
            ),
        )

        assert with_override["feature_gates"]["test_public"]["value"] is False
        assert without_override["feature_gates"]["test_public"]["value"] is True
    finally:
        statsig.shutdown().wait()
