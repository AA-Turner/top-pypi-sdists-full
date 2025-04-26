#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2024

from copy import deepcopy

import pytest

from streamsets.sdk import ControlHub
from streamsets.sdk.sch_api import ApiClient
from streamsets.sdk.sch_models import SelfManagedDeployment

from .resources.self_managed_deployments_data import DUMMY_DEPLOYMENT_JSON

VALID_INSTALL_SCRIPT = "Install Script"


@pytest.fixture(scope="function")
def dummy_deployment_data():
    data = deepcopy(DUMMY_DEPLOYMENT_JSON)
    return data


class MockControlHub(ControlHub):
    def __init__(self, *args, **kwargs):
        self.api_client = MockApiClient()
        pass  # do not call super()


class MockResponse:
    def __init__(self, json_response):
        self.response = json_response

    def json(self):
        return self.response

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
            }
        )

    def get_self_managed_deployment_install_command(
        self, deployment_id, install_mechanism='DEFAULT', install_type=None, java_version=None
    ):
        return MockCommand(VALID_INSTALL_SCRIPT)


@pytest.fixture(scope="function")
def self_managed_deployment(dummy_deployment_data):
    sch = MockControlHub()
    deployment = SelfManagedDeployment(dummy_deployment_data)
    deployment._control_hub = sch
    return deployment


def test_invalid_java_version_install_script(self_managed_deployment):
    with pytest.raises(Exception):
        self_managed_deployment.install_script(java_version='3')


def test_supported_java_version_install_script(self_managed_deployment):
    assert self_managed_deployment.install_script(java_version='17') == VALID_INSTALL_SCRIPT


def test_default_java_version_install_script(self_managed_deployment):
    assert self_managed_deployment.install_script() == VALID_INSTALL_SCRIPT


@pytest.mark.parametrize("install_mechanism", [mechanism for mechanism in SelfManagedDeployment.InstallMechanism])
def test_valid_install_mechanism(self_managed_deployment, install_mechanism):
    install_script = self_managed_deployment.install_script(install_mechanism=install_mechanism.value)
    assert type(install_script) is str
    assert len(install_script) > 0


@pytest.mark.parametrize("install_type", [install_type for install_type in SelfManagedDeployment.InstallType])
def test_valid_install_type(self_managed_deployment, install_type):
    install_script = self_managed_deployment.install_script(install_type=install_type.value)
    assert install_script == VALID_INSTALL_SCRIPT


def test_invalid_install_mechanism(self_managed_deployment):
    invalid_install_mechanism = "foo"

    with pytest.raises(ValueError):
        self_managed_deployment.install_script(install_mechanism=invalid_install_mechanism)


def test_invalid_install_type(self_managed_deployment):
    invalid_install_type = "foo"

    with pytest.raises(ValueError):
        self_managed_deployment.install_script(install_type=invalid_install_type)
