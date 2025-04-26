#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2024

# fmt: off
import pytest
import requests

from streamsets.sdk.sch_models import Deployment
from streamsets.sdk.utils import get_random_string

# fmt: on


def test_add_deployment_adds_disabled_engine(args, test_environment, sch):
    # Check if there's disabled engines that can be used to create a deployment
    configuration = sch.api_client.get_organization_configuration(sch.organization).response.json()
    for config in configuration:
        if config["id"] == "dpm.disabled.engine.version.override.list":
            if not config['possibleValues']:
                pytest.skip("Currently unable to move disabled engines into the override list")
            engine_version_id = config['possibleValues'][0]

    engine_version_id_split = engine_version_id.split(":")
    engine_type = engine_version_id_split[0]
    engine_version = engine_version_id_split[1]
    engine_build = engine_version_id_split[-1]

    # Verify that the engine used to build the deployment is disabled
    assert sch.engine_versions.get(id="{}:{}::{}".format(engine_type, engine_version, engine_build)).disabled

    builder = sch.get_deployment_builder(deployment_type='SELF')
    deployment = builder.build(
        deployment_name='SDK Test Deployment SDC_Docker {}'.format(get_random_string()),
        engine_type=engine_type,
        engine_version=engine_version,
        engine_build=engine_build,
        environment=test_environment,
    )
    sch.add_deployment(deployment)
    try:
        retrieved_deployment = sch.deployments.get(deployment_name=deployment.deployment_name)
        assert isinstance(retrieved_deployment, Deployment)
    finally:
        sch.delete_deployment(deployment)


def test_delete_active_deployment(test_environment, sch):
    EXPECTED_ERROR_MESSAGE = "Cannot delete deployment that is currently ACTIVE or ACTIVATION_ERROR - stop it first"
    builder = sch.get_deployment_builder(deployment_type='SELF')
    deployment = builder.build(
        deployment_name='SDK Test Deployment SDC_Docker {}'.format(get_random_string()),
        engine_type="DC",
        engine_version="5.1.0",
        environment=test_environment,
    )
    sch.add_deployment(deployment)
    sch.start_deployment(deployment)
    assert deployment.state == 'ACTIVE'
    with pytest.raises(requests.exceptions.HTTPError) as error_message:
        sch.delete_deployment(deployment, stop=False)
        assert EXPECTED_ERROR_MESSAGE == error_message["ISSUES"][0]["message"]
    sch.delete_deployment(deployment)
    with pytest.raises(ValueError):
        sch.deployments.get(deployment_id=deployment.deployment_id)
