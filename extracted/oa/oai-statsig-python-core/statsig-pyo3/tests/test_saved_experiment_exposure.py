import json
import time
from contextlib import ExitStack

import pytest
from statsig_python_core import (
    DataStore,
    DataStoreResponse,
    EventLoggingAdapter,
    Statsig,
    StatsigOptions,
    StatsigUser,
)
from utils import get_test_data_resource


class Specs(DataStore):
    def __init__(self, specs):
        super().__init__()
        self.specs = specs

    def get(self, key):
        return DataStoreResponse(self.specs, 1)


class Events(EventLoggingAdapter):
    def __init__(self):
        super().__init__()
        self.exposures = []

    def log_events(self, request):
        self.exposures.extend(
            e for e in request.payload["events"] if e["eventName"].endswith("_exposure")
        )
        return True


def new_sdk(stack, specs, disable_logging=False):
    events = Events()
    sdk = Statsig(
        "secret-key",
        StatsigOptions(
            data_store=Specs(json.dumps(specs)),
            event_logging_adapter=events,
            enable_id_lists=False,
            disable_network=True,
            disable_all_logging=disable_logging,
            output_log_level="none",
        ),
    )
    sdk.initialize().wait()
    stack.callback(lambda: sdk.shutdown().wait())
    return sdk, events


def test_saved_assignment_between_sdk_instances():
    specs = json.loads(get_test_data_resource("eval_proj_dcs.json"))
    experiment_name = "experiment_with_many_params"
    layer_name = "layer_with_many_params"
    experiment = specs["dynamic_configs"][experiment_name]
    experiment["version"] = 333
    specs.pop("checksum", None)
    user = StatsigUser(
        "user123",
        email="hidden@example.com",
        custom={"attribute": "custom-value"},
        private_attributes={"secret": "private-value"},
    )
    with ExitStack() as stack:
        producer, producer_events = new_sdk(stack, specs)
        layer, payload = producer.evaluate_layer_for_deferred_experiment_exposure(
            user, layer_name
        )
        assert layer.allocated_experiment_name == experiment_name
        assert layer.get("a_string") is not None
        assert payload
        assignment = json.loads(payload)["V1"]
        assert assignment["user"] == {"userID": "user123"}
        _, missing = producer.evaluate_layer_for_deferred_experiment_exposure(
            user, "missing"
        )
        assert missing is None
        with pytest.raises(TypeError):
            producer.evaluate_layer_for_deferred_experiment_exposure(user, None)
        producer.flush_events().wait()
        assert producer_events.exposures == []

        # The consumer no longer even has the experiment in its specs.
        del specs["dynamic_configs"][experiment_name]
        consumer, consumer_events = new_sdk(stack, specs)
        del assignment["user"]["userID"]
        with pytest.raises(ValueError, match="Missing saved experiment assignment unit"):
            consumer.log_deferred_experiment_exposure_DO_NOT_USE(
                json.dumps({"V1": assignment})
            )
        with pytest.raises(ValueError, match="Invalid saved"):
            consumer.log_deferred_experiment_exposure_DO_NOT_USE("{}")
        before = time.time_ns() // 1_000_000
        consumer.log_deferred_experiment_exposure_DO_NOT_USE(payload)
        consumer.flush_events().wait()
        (event,) = consumer_events.exposures
        assert event["eventName"] == "statsig::config_exposure"
        assert event["metadata"]["config"] == experiment_name
        assert event["metadata"]["ruleID"] == layer.rule_id
        assert event["metadata"]["configVersion"] == "333"
        assert event["user"]["userID"] == "user123"
        assert event["time"] >= before


def test_custom_unit_and_disabled_logging():
    specs = json.loads(get_test_data_resource("eval_proj_dcs.json"))
    layer_name = "Basic_test_layer"
    experiment_name = "test_experiment_no_targeting"
    # Keep the fixture's delegated assignment, with request rather than user randomization.
    for entity in (
        specs["layer_configs"][layer_name],
        specs["dynamic_configs"][experiment_name],
    ):
        entity["idType"] = "request_id"
        for rule in entity["rules"]:
            rule["idType"] = "request_id"
    specs.pop("checksum", None)
    user = StatsigUser("user123", custom_ids={"request_id": "original-request"})
    with ExitStack() as stack:
        producer, producer_events = new_sdk(stack, specs)
        layer, payload = producer.evaluate_layer_for_deferred_experiment_exposure(
            user, layer_name
        )
        assert payload
        assert json.loads(payload)["V1"]["user"] == {
            "userID": "user123",
            "customIDs": {"request_id": "original-request"},
        }
        assert layer.allocated_experiment_name == experiment_name
        producer.log_deferred_experiment_exposure_DO_NOT_USE(payload)
        producer.flush_events().wait()
        (saved,) = producer_events.exposures
        assert saved["user"]["customIDs"] == {"request_id": "original-request"}
        producer_events.exposures.clear()

        silent, events = new_sdk(stack, specs, disable_logging=True)
        assert (
            silent.evaluate_layer_for_deferred_experiment_exposure(user, layer_name)[1]
            is None
        )
        silent.log_deferred_experiment_exposure_DO_NOT_USE(payload)
        silent.flush_events().wait()
        assert events.exposures == []

        # Existing layer reads still log the ordinary parameter exposure.
        normal_layer = producer.get_layer(user, layer_name)
        normal_layer.get("value")
        producer.flush_events().wait()
        (event,) = producer_events.exposures
        assert event["eventName"] == "statsig::layer_exposure"
        assert event["metadata"]["parameterName"] == "value"
