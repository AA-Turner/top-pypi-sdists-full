#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2024
from copy import deepcopy

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
    try:
        sch.start_deployment(deployment)
        assert deployment.state == 'ACTIVE'
        with pytest.raises(requests.exceptions.HTTPError) as error_message:
            sch.delete_deployment(deployment, stop=False)
            assert EXPECTED_ERROR_MESSAGE == error_message["ISSUES"][0]["message"]
        sch.delete_deployment(deployment)
        with pytest.raises(ValueError):
            sch.deployments.get(id=deployment.id)
    except Exception as e:
        sch.delete_deployment(deployment, stop=True)
        raise e


def test_delete_active_environment(sch):
    # Create and start environment
    environment_builder = sch.get_environment_builder(environment_type='SELF')

    environment = environment_builder.build(
        environment_name='Self-managed--environment-{}'.format(get_random_string()),
        environment_tags=['self-managed-tag'],
        allow_nightly_engine_builds=False,
    )
    sch.add_environment(environment)
    try:
        sch.activate_environment(environment)
        assert environment.state == 'ACTIVE'
        sch.delete_environment(environment)
        with pytest.raises(ValueError):
            sch.environments.get(id=environment.id)
    except Exception as e:
        sch.delete_environment(environment, stop=True)
        raise e


def test_delete_active_environment_with_active_deployment(sch):
    EXPECTED_ERROR_MESSAGE_CONTAINS = "Environments can only be deactivated when they have no deployments"

    # Create and start environment
    environment_builder = sch.get_environment_builder(environment_type='SELF')

    environment = environment_builder.build(
        environment_name='Self-managed--environment-{}'.format(get_random_string()),
        environment_tags=['self-managed-tag'],
        allow_nightly_engine_builds=False,
    )
    sch.add_environment(environment)
    try:
        sch.activate_environment(environment)
        assert environment.state == 'ACTIVE'

        # Create and start deployment
        builder = sch.get_deployment_builder(deployment_type='SELF')
        deployment = builder.build(
            deployment_name='SDK Test Deployment SDC_Docker {}'.format(get_random_string()),
            engine_type="DC",
            engine_version="5.1.0",
            environment=environment,
        )
        sch.add_deployment(deployment)
        sch.start_deployment(deployment)
        assert deployment.state == 'ACTIVE'

        with pytest.raises(requests.exceptions.HTTPError) as error_message:
            sch.delete_environment(environment, stop=False)
            assert EXPECTED_ERROR_MESSAGE_CONTAINS in error_message["ISSUES"][0]["message"]
        sch.delete_environment(environment, stop=True)
        with pytest.raises(ValueError):
            sch.environments.get(id=environment.id)
    except Exception as e:
        sch.delete_environment(environment, stop=True)
        raise e


def test_delete_active_environment_with_inactive_deployment(sch):
    # Create and start environment
    environment_builder = sch.get_environment_builder(environment_type='SELF')

    environment = environment_builder.build(
        environment_name='Self-managed--environment-{}'.format(get_random_string()),
        environment_tags=['self-managed-tag'],
        allow_nightly_engine_builds=False,
    )
    sch.add_environment(environment)
    try:
        sch.activate_environment(environment)
        assert environment.state == 'ACTIVE'

        # Create deployment
        builder = sch.get_deployment_builder(deployment_type='SELF')
        deployment = builder.build(
            deployment_name='SDK Test Deployment SDC_Docker {}'.format(get_random_string()),
            engine_type="DC",
            engine_version="5.1.0",
            environment=environment,
        )
        sch.add_deployment(deployment)
        assert deployment.state != 'ACTIVE'
        sch.delete_environment(environment, stop=True)
        with pytest.raises(ValueError):
            sch.environments.get(id=environment.id)
    except Exception as e:
        sch.delete_environment(environment, stop=True)
        raise e


def test_delete_deactivated_environment_with_inactive_deployment(sch):
    # Create and start environment
    environment_builder = sch.get_environment_builder(environment_type='SELF')

    environment = environment_builder.build(
        environment_name='Self-managed--environment-{}'.format(get_random_string()),
        environment_tags=['self-managed-tag'],
        allow_nightly_engine_builds=False,
    )
    sch.add_environment(environment)
    try:
        sch.activate_environment(environment)
        assert environment.state == 'ACTIVE'

        # Create deployment
        builder = sch.get_deployment_builder(deployment_type='SELF')
        deployment = builder.build(
            deployment_name='SDK Test Deployment SDC_Docker {}'.format(get_random_string()),
            engine_type="DC",
            engine_version="5.1.0",
            environment=environment,
        )
        sch.add_deployment(deployment)

        # Deactivate environment
        sch.deactivate_environment(environment)
        assert environment.state == 'DEACTIVATED'
        sch.delete_environment(environment, stop=True)
        with pytest.raises(ValueError):
            sch.environments.get(id=environment.id)
    except Exception as e:
        sch.delete_environment(environment, stop=True)
        raise e


def test_connection_lazy_loading_behavior(sch, invalid_aws_engineless_test_connection):
    connection = sch.connections.get(id=invalid_aws_engineless_test_connection.id)

    original_data_internal = connection._data_internal.copy()
    original_connection_definition_internal = deepcopy(connection._connection_definition_internal)
    original_name = connection.name
    original_sdc_id = connection.sdc_id

    # Simulate pre-lazy-load state
    connection._connection_definition_internal = None

    # Manual overrides
    connection.name = "MANUAL_NAME_OVERRIDE"
    connection.sdc_id = "MANUAL_SDCID_OVERRIDE"

    try:
        # Trigger lazy loading
        connection._load_data()

        # Validate overridden fields are preserved
        assert connection.name == "MANUAL_NAME_OVERRIDE"
        assert connection.sdc_id == "MANUAL_SDCID_OVERRIDE"

    finally:
        connection._connection_definition_internal = original_connection_definition_internal
        connection._data_internal = original_data_internal
        connection.name = original_name
        connection.sdc_id = original_sdc_id
