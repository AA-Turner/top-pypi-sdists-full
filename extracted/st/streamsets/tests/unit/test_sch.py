#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2024

# fmt: off
from copy import deepcopy

import pytest

from streamsets.sdk import ControlHub
from streamsets.sdk.sch_api import ApiClient
from streamsets.sdk.sch_models import AzureEnvironment, SelfManagedDeployment

from .resources.sch_data import DUMMY_DEPLOYMENT_JSON, DUMMY_DEPLOYMENT_JSON_2

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


class MockResponse:
    def __init__(self, json_response):
        self.response = json_response

    def json(self):
        return self.response

    @property
    def content(self):
        return self.response.encode()

    @property
    def text(self):
        return self.response


class MockCommand:
    def __init__(self, json_response):
        self._response = json_response

    @property
    def response(self):
        return MockResponse(self._response)


class MockApiClient(ApiClient):
    def __init__(self, *args, **kwargs):
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
            {
                "id": "DC:5.10.0::RC3",
                "engineType": "DC",
                "engineVersion": "5.10.0",
                "creator": "a2ce9742-b78a-11eb-b93c-352da592f75a@admin",
                "createTime": 1711051750490,
                "lastModifiedBy": "a2ce9742-b78a-11eb-b93c-352da592f75a@admin",
                "lastModifiedOn": 1711051750490,
                "defaultJavaVersion": 8,
                "supportedJavaVersions": "8,17",
                'advancedConfiguration': None,
            }
        )

    def get_all_engine_versions(self, *args, **kwargs):
        return MockCommand(
            [
                {
                    "id": "DC:5.10.0::RC3",
                    "engineType": "DC",
                    "engineVersion": "5.9.0",
                    "creator": "a2ce9742-b78a-11eb-b93c-352da592f75a@admin",
                    "createTime": 1711051750490,
                    "lastModifiedBy": "a2ce9742-b78a-11eb-b93c-352da592f75a@admin",
                    "lastModifiedOn": 1711051750490,
                    "disabled": True,
                    "defaultJavaVersion": 8,
                    "supportedJavaVersions": "8,17",
                }
            ]
        )

    def get_self_managed_deployment_install_command(
        self, deployment_id, install_mechanism='DEFAULT', install_type=None, java_version=None
    ):
        return MockCommand(VALID_INSTALL_SCRIPT)


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


def test_start_deployment_activation_error(dummy_deployment_data):
    sch = MockControlHub()
    deployment = SelfManagedDeployment(dummy_deployment_data)
    deployment._control_hub = sch
    with pytest.raises(RuntimeError):
        sch.start_deployment(deployment)


def test_update_deployment_activation_error(dummy_deployment_data):
    sch = MockControlHub()
    deployment = SelfManagedDeployment(dummy_deployment_data)
    deployment._control_hub = sch
    with pytest.raises(RuntimeError):
        sch.update_deployment(deployment)


def test_activate_environment_activation_error(azure_environment_json):
    sch = MockControlHub()
    environment = AzureEnvironment(azure_environment_json)
    environment._control_hub = sch
    with pytest.raises(RuntimeError):
        sch.activate_environment(environment)


def test_update_environment_activation_error(azure_environment_json):
    sch = MockControlHub()
    environment = AzureEnvironment(azure_environment_json)
    environment._control_hub = sch
    with pytest.raises(RuntimeError):
        sch.update_environment(environment)


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
