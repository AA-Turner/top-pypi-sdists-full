#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2024
import copy

# fmt: off
from copy import deepcopy

import pytest

from streamsets.sdk import ControlHub
from streamsets.sdk.sch_api import ApiClient
from streamsets.sdk.sch_models import KubernetesDeployment, SelfManagedDeployment

from .conftest import MockCommand
from .resources.sch_data import ALL_ENGINE_VERSIONS, DUMMY_DEPLOYMENT_JSON, DUMMY_DEPLOYMENT_JSON_2

# fmt: on

VALID_INSTALL_SCRIPT = "Install Script"


class MockControlHub(ControlHub):
    def __init__(self, *args, **kwargs):
        self.api_client = MockApiClient()
        pass  # do not call super()

    def delete_deployment(self, *deployments):
        return

    def update_deployment(self, deployment):
        if (
            "labels" in deployment._data["engineConfiguration"]
            and deployment._data["engineConfiguration"]["labels"][0] == "Don't Update"
        ):
            return MockCommand(activation_error_data())
        super().update_deployment(deployment)


class MockApiClient(ApiClient):
    def __init__(self, *args, **kwargs):
        self._disabled_ids = []
        self._wait_calls = []
        self._force_calls = []
        self.fail_disable = False
        pass  # do not call super()

    def enable_deployments(self, deployment_ids):
        return True

    def create_deployment(self, data):
        return MockCommand(
            {
                "engineConfiguration": {
                    'advancedConfiguration': None,
                    'externalResourcesUri': None,
                    'maxCpuLoad': None,
                    'maxMemoryUsed': None,
                    'maxPipelinesRunning': None,
                    'jvmConfig': None,
                    'labels': None,
                    'stageLibs': None,
                    'scalaBinaryVersion': None,
                }
            }
        )

    def update_deployment(self, *args, **kwargs):
        return MockCommand(activation_error_data())

    def get_deployment(self, deployment_id):
        return MockCommand(activation_error_data())

    def enable_environments(self, environment_ids):
        return True

    def get_environment(self, environment_id):
        return MockCommand(activation_error_data())

    def update_environment(self, *args, **kwargs):
        return MockCommand(activation_error_data())

    def get_engine_version(self, engine_version_id):
        return MockCommand(
            next(filter(lambda engine_config: engine_config['id'] == engine_version_id, ALL_ENGINE_VERSIONS))
        )

    def get_all_engine_versions(self, *args, **kwargs):
        return MockCommand(copy.deepcopy(ALL_ENGINE_VERSIONS))

    def get_self_managed_deployment_install_command(
        self, deployment_id, install_mechanism='DEFAULT', install_type=None, java_version=None
    ):
        return MockCommand(VALID_INSTALL_SCRIPT)

    def disable_deployments(self, deployment_ids):
        if self.fail_disable:
            raise Exception("disable failed (mock)")
        self._disabled_ids = list(deployment_ids)
        return True

    def wait_for_deployment_state_display_label(self, deployment_id, state_display_label, **kwargs):
        self._wait_calls.append((deployment_id, state_display_label))

    def force_stop_deployment(self, deployment_id, confirm=False):
        self._force_calls.append((deployment_id, bool(confirm)))
        return MockCommand({"ok": True})


@pytest.fixture(scope="function")
def dummy_deployment_data():
    data = deepcopy(DUMMY_DEPLOYMENT_JSON)
    return data


@pytest.fixture(scope="function")
def dummy_deployment_data_2():
    data = deepcopy(DUMMY_DEPLOYMENT_JSON_2)
    return data


def activation_error_data():
    return {
        'stateDisplayLabel': 'ACTIVATION_ERROR',
        'status': 'ERROR',
        'statusDetail': 'Unexpected status CREATE_FAILED detected while checking deployment',
    }


def test_invalid_java_version_install_script(dummy_deployment_data):
    sch = MockControlHub()
    deployment = SelfManagedDeployment(dummy_deployment_data)
    deployment._control_hub = sch
    with pytest.raises(Exception):
        sch.get_self_managed_deployment_install_script(deployment, java_version='3')


def test_supported_java_version_install_script(dummy_deployment_data):
    sch = MockControlHub()
    deployment = SelfManagedDeployment(dummy_deployment_data)
    deployment._control_hub = sch
    assert sch.get_self_managed_deployment_install_script(deployment, java_version='17') == VALID_INSTALL_SCRIPT


def test_default_java_version_install_script(dummy_deployment_data):
    sch = MockControlHub()
    deployment = SelfManagedDeployment(dummy_deployment_data)
    deployment._control_hub = sch
    assert sch.get_self_managed_deployment_install_script(deployment) == VALID_INSTALL_SCRIPT


def test_broken_add_deployment(dummy_deployment_data):
    sch = MockControlHub()
    deployment = SelfManagedDeployment(dummy_deployment_data)
    deployment._control_hub = sch
    original_deployment_data = deployment._data
    with pytest.raises(KeyError):
        sch.add_deployment(deployment)
    assert deployment._data == original_deployment_data


def test_add_deployment_adds_disabled_engine(dummy_deployment_data_2):
    sch = MockControlHub()
    deployment = SelfManagedDeployment(dummy_deployment_data_2)
    deployment._control_hub = sch
    sch.add_deployment(deployment)


def test_stop_deployment_no_force(dummy_deployment_data):
    sch = MockControlHub()
    payload = deepcopy(dummy_deployment_data)
    deployment = SelfManagedDeployment(payload)
    deployment._control_hub = sch

    dep_id = payload["id"]
    deployment._data_internal["id"] = dep_id
    deployment._data_internal["deploymentId"] = dep_id
    deployment._data_internal["type"] = "SELF"

    result = sch.stop_deployment(deployment, force=False)

    assert result is True

    assert sch.api_client._disabled_ids == [dep_id]

    assert any(state == "DEACTIVATED" for (_id, state) in sch.api_client._wait_calls)
    assert any(call[0] == dep_id for call in sch.api_client._wait_calls)


def test_stop_deployment_with_force_non_k8s_skips_force(caplog, dummy_deployment_data):
    sch = MockControlHub()
    sch.api_client.fail_disable = True

    payload = deepcopy(dummy_deployment_data)
    deployment = SelfManagedDeployment(payload)
    deployment._control_hub = sch

    dep_id = payload["id"]
    deployment._data_internal["id"] = dep_id
    deployment._data_internal["type"] = "SELF"

    with pytest.raises(ValueError, match=r"force=True was specified, but no Kubernetes deployments were provided"):
        sch.stop_deployment(deployment, force=True)

    assert sch.api_client._force_calls == []
    assert sch.api_client._disabled_ids == []
    assert sch.api_client._wait_calls == []


def test_stop_deployment_with_force_k8s_calls_force(dummy_deployment_data, caplog):
    sch = MockControlHub()
    sch.api_client.fail_disable = True

    payload = deepcopy(dummy_deployment_data)
    payload['type'] = 'KUBERNETES'
    deployment = KubernetesDeployment(payload)
    deployment._control_hub = sch

    dep_id = payload["id"]
    deployment._data_internal["id"] = dep_id
    deployment._data_internal["deploymentId"] = dep_id
    deployment._data_internal["type"] = "KUBERNETES"

    result = sch.stop_deployment(deployment, force=True)

    assert sch.api_client._force_calls == [(dep_id, True)]
    assert sch.api_client._disabled_ids == []

    assert any((_id == dep_id and state == "DEACTIVATION_ERROR") for (_id, state) in sch.api_client._wait_calls)

    assert isinstance(result, MockCommand)
