#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2024

# fmt: off
from copy import deepcopy

import pytest

from streamsets.sdk.sch_models import DeploymentBuilder, Pipeline
from streamsets.sdk.sch_models import PipelineBuilder as SchSdcPipelineBuilder
from streamsets.sdk.sch_models import StPipelineBuilder as SchStPipelineBuilder
from streamsets.sdk.sdc_models import PipelineBuilder as SdcPipelineBuilder
from streamsets.sdk.st_models import PipelineBuilder as StPipelineBuilder

from .resources.conftest_data import (
    AZURE_ENVIRONMENT_JSON, DEPLOYMENT_BUILDER_JSON, PIPELINE_BUILDER_DEFINITIONS_JSON, PIPELINE_BUILDER_JSON,
)

# fmt: on


@pytest.fixture(scope="function")
def pipeline_builder_json():
    data = deepcopy(PIPELINE_BUILDER_JSON)
    return data


@pytest.fixture(scope="function")
def pipeline_builder_definitions():
    data = deepcopy(PIPELINE_BUILDER_DEFINITIONS_JSON)
    return data


class DummyEngines:
    def get(self, id):
        return DummyEngine()


class DummyEngine:
    def __init__(self):
        self._data = {"startUpTime": 0}
        self._sch_pipeline = {"sdcId": 0}


class MockControlHub:
    def __init__(self):
        self.organization = "12345"

    @property
    def engines(self):
        return DummyEngines()


@pytest.fixture(scope="function")
def sdc_pipeline_builder(pipeline_builder_json, pipeline_builder_definitions):
    return SdcPipelineBuilder(pipeline=pipeline_builder_json, definitions=pipeline_builder_definitions)


@pytest.fixture(scope="function")
def sch_sdc_pipeline_builder(pipeline_builder_json, sdc_pipeline_builder):
    return SchSdcPipelineBuilder(
        pipeline=pipeline_builder_json,
        data_collector_pipeline_builder=sdc_pipeline_builder,
        control_hub=MockControlHub(),
    )


@pytest.fixture(scope="function")
def st_pipeline_builder(pipeline_builder_json, pipeline_builder_definitions):
    return StPipelineBuilder(pipeline=pipeline_builder_json, definitions=pipeline_builder_definitions)


@pytest.fixture(scope="function")
def sch_st_pipeline_builder(pipeline_builder_json, st_pipeline_builder):
    return SchStPipelineBuilder(
        pipeline=pipeline_builder_json,
        transformer_pipeline_builder=st_pipeline_builder,
        control_hub=MockControlHub(),
    )


@pytest.fixture(scope="function")
def deployment_builder_json():
    data = deepcopy(DEPLOYMENT_BUILDER_JSON)
    return data


@pytest.fixture(scope="function")
def self_deployment_builder(deployment_builder_json):
    additional_attributes = {"type": "SELF", "installType": None}

    data = {**deployment_builder_json, **additional_attributes}

    return DeploymentBuilder(data, MockControlHub())


@pytest.fixture(scope="function")
def gce_deployment_builder(deployment_builder_json):
    additional_attributes = {
        "type": "GCE",
        "initScript": None,
        "machineType": None,
        "region": None,
        "allowedResourceLocations": None,
        "secretManagerReplicationPolicy": None,
        "zones": None,
        "blockProjectSshKeys": None,
        "publicSshKey": None,
        "trackingUrl": None,
        "instanceServiceAccountEmail": None,
        "tags": None,
        "resourceLabels": None,
        "subnetwork": None,
        "attachPublicIp": None,
    }

    data = {**deployment_builder_json, **additional_attributes}

    return DeploymentBuilder(data, MockControlHub())


@pytest.fixture(scope="function")
def ec2_deployment_builder(deployment_builder_json):
    additional_attributes = {
        "type": "EC2",
        "initScript": None,
        "instanceType": None,
        "resourceTags": None,
        "sshKeySource": None,
        "sshKeyPairName": None,
        "instanceProfileArn": None,
        "trackingUrl": None,
    }

    data = {**deployment_builder_json, **additional_attributes}

    return DeploymentBuilder(data, MockControlHub())


@pytest.fixture(scope="function")
def azure_deployment_builder(deployment_builder_json):
    additional_attributes = {
        "type": "AZURE_VM",
        "initScript": None,
        "vmSize": None,
        "sshKeySource": None,
        "sshKeyPairName": None,
        "publicSshKey": None,
        "resourceGroup": None,
        "resourceTags": None,
        "managedIdentity": None,
        "trackingUrl": None,
        "zones": None,
        "attachPublicIp": None,
    }

    data = {**deployment_builder_json, **additional_attributes}

    return DeploymentBuilder(data, MockControlHub())


@pytest.fixture(scope="function")
def kubernetes_deployment_builder(deployment_builder_json):
    additional_attributes = {
        "type": "KUBERNETES",
        "kubernetesLabels": None,
        "memoryRequest": None,
        "cpuRequest": None,
        "memoryLimit": None,
        "cpuLimit": None,
        "yaml": None,
        "advancedMode": None,
        "hpa": None,
        "hpaMinReplicas": None,
        "hpaMaxReplicas": None,
        "hpaTargetCPUUtilizationPercentage": None,
    }

    data = {**deployment_builder_json, **additional_attributes}

    return DeploymentBuilder(data, MockControlHub())


@pytest.fixture(scope="function")
def pipeline_definitions():
    return {
        "stages": [
            {  # Snowflake destination
                "instanceName": "Snowflake_01",
                "library": "streamsets-datacollector-sdc-snowflake-lib",
                "stageName": "com_streamsets_pipeline_stage_destination_snowflake_SnowflakeDTarget",
                "stageVersion": "18",
                "configuration": [],
                "services": [],
                "uiInfo": {
                    "yPos": 50,
                    "stageType": "TARGET",
                    "description": "",
                    "label": "Snowflake 1",
                    "xPos": 60,
                },
                "inputLanes": [],
                "outputLanes": [],
                "eventLanes": [],
            }
        ]
    }


@pytest.fixture(scope="function")
def pipeline_data_json(pipeline_definitions, request):
    return {
        "pipelineId": 1,
        "commitId": None,
        "name": "Test Pipeline",
        "version": 1,
        "executorType": "COLLECTOR" if "sdc" in request.node.name else "TRANSFORMER",
        "pipelineDefinitions": pipeline_definitions,
    }


@pytest.fixture(scope="function")
def sch_sdc_pipeline(
    pipeline_data_json,
    pipeline_definitions,
    sch_sdc_pipeline_builder,
    mocker,
):
    return Pipeline(
        pipeline=pipeline_data_json,
        pipeline_definition=pipeline_definitions,
        rules_definition=None,
        library_definitions={},
        control_hub=mocker.Mock(),
        builder=sch_sdc_pipeline_builder,
    )


@pytest.fixture(scope="function")
def sch_st_pipeline(
    pipeline_data_json,
    pipeline_definitions,
    sch_st_pipeline_builder,
    mocker,
):
    return Pipeline(
        pipeline=pipeline_data_json,
        pipeline_definition=pipeline_definitions,
        rules_definition=None,
        library_definitions={},
        control_hub=mocker.Mock(),
        builder=sch_st_pipeline_builder,
    )


@pytest.fixture(scope="function")
def azure_environment_json():
    data = deepcopy(AZURE_ENVIRONMENT_JSON)
    return data
