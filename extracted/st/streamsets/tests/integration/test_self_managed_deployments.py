# Copyright 2022 StreamSets Inc.

# fmt: off
import random

import pytest

from streamsets.sdk.constants import (
    DEFAULT_MAX_CPU_LOAD_VALUE, DEFAULT_MAX_MEMORY_USED_VALUE, DEFAULT_MAX_PIPELINES_RUNNING_VALUE,
)
from streamsets.sdk.sch_models import Deployment, SelfManagedDeployment
from streamsets.sdk.utils import SeekableList, get_random_string

# fmt: on


@pytest.fixture(scope="module")
def sample_environment(sch):
    """A sample environment."""
    environment_builder = sch.get_environment_builder(environment_type='SELF')
    environment = environment_builder.build(
        environment_name='Sample Environment',
        environment_type='SELF',
        environment_tags=['self-managed-tag-{}'.format(get_random_string())],
        allow_nightly_engine_builds=False,
    )
    sch.add_environment(environment)
    sch.activate_environment(environment)

    try:
        yield environment
    finally:
        sch.delete_environment(environment)


@pytest.fixture(scope="module")
def sample_deployments(args, sch, sample_environment):
    """A set of sample deployments."""
    builder = sch.get_deployment_builder(deployment_type='SELF')
    sample_deployments = []

    # A set of sample deployments.
    # e.g. for SDC with DOCKER and TARBALL as install type.
    # and for transformer with DOCKER and TARBALL as install type.
    for engine_type in ['DC', 'TF']:
        engine_version = args.sdc_version if engine_type == "DC" else args.transformer_version
        scala_binary_version = None if engine_type == 'DC' else args.transformer_scala_version
        for install_type in ['DOCKER', 'TARBALL']:
            deployment = builder.build(
                deployment_name='Sample Deployment {}-{}'.format(engine_type, install_type),
                deployment_type='SELF',
                deployment_tags=['self-managed-tag-{}'.format(get_random_string())],
                engine_type=engine_type,
                engine_version=engine_version,
                scala_binary_version=scala_binary_version,
                environment=sample_environment,
            )
            deployment.install_type = install_type

            # JVM configs
            deployment.engine_configuration.java_configuration.maximum_java_heap_size_in_mb = 4096
            deployment.engine_configuration.java_configuration.minimum_java_heap_size_in_mb = 2048
            deployment.engine_configuration.java_configuration.java_options = '-Xdebug'
            # engine_labels
            deployment.engine_configuration.engine_labels = ['kirti123']
            deployment.engine_configuration.external_resource_source = 'www.google.com'
            sch.add_deployment(deployment)
            sample_deployments.append(deployment)

    try:
        yield sample_deployments
    finally:
        sch.delete_deployment(*sample_deployments)


def test_deployment_in_returns_true(sch, sample_deployments):
    for sample_deployment in sample_deployments:
        assert sample_deployment in sch.deployments


def test_deployment_contains(sch, sample_deployments):
    for sample_deployment in sample_deployments:
        assert sch.deployments.contains(deployment_id=sample_deployment.deployment_id)
        assert sch.deployments.contains(deployment_name=sample_deployment.deployment_name)
        assert not sch.deployments.contains(deployment_id='impossible_to_clash_with_this_^%@@!$!%^!!%#RWQ')


def test_deployments_len_works(sch):
    assert len(sch.deployments) >= 1


def test_deployments_get_all_returns_seekable_list(sch):
    assert isinstance(sch.deployments.get_all(), SeekableList)


def test_deployments_get_by_id(sch, sample_deployments):
    for sample_deployment in sample_deployments:
        sample_deployment_id = sample_deployment.deployment_id
        deployment = sch.deployments.get(deployment_id=sample_deployment_id)
        assert isinstance(deployment, SelfManagedDeployment)
        assert deployment.deployment_id == sample_deployment_id


def test_deployments_get_by_id_raises_value_error(sch, sample_deployments):
    for sample_deployment in sample_deployments:
        deployment_id = sample_deployment.deployment_id
        fake_deployment_id = '{}zxyf'.format(deployment_id)
        with pytest.raises(ValueError):
            sch.deployments.get(deployment_id=fake_deployment_id)


def test_deployments_get_all_works(sch, sample_deployments):
    for sample_deployment in sample_deployments:
        assert not (
            {sample_deployment.deployment_id} - {deployment.deployment_id for deployment in sch.deployments.get_all()}
        )


def test_deployments_cast_to_list(sch, sample_deployments):
    deployments = list(sch.deployments)
    assert isinstance(deployments, list)
    for sample_deployment in sample_deployments:
        assert isinstance(sample_deployment, Deployment)


def test_deployments_with_filters(sch):
    assert len(sch.deployments.get_all(len=1)) == 1


def test_start_stop(sch, sample_deployments):
    sch.start_deployment(*sample_deployments)
    for deployment in sample_deployments:
        assert deployment.json_state == 'ENABLED'
        assert deployment.state == 'ACTIVE'

    sch.stop_deployment(*sample_deployments)
    for deployment in sample_deployments:
        assert deployment.json_state == 'DISABLED'
        assert deployment.state == 'DEACTIVATED'


def test_fetch(sch, sample_deployments):
    # Fetch by deployment_name
    name = 'Sample Deployment DC-DOCKER'
    fetched_by_name_deployment = sch.deployments.get(deployment_name=name)
    assert fetched_by_name_deployment.deployment_name == name

    # Fetch by id
    deployment_id = fetched_by_name_deployment.deployment_id
    fetched_by_id_deployment = sch.deployments.get(deployment_id=deployment_id)
    assert fetched_by_id_deployment.deployment_id == deployment_id

    # Fetch all the deployments
    all_deployments = sch.deployments
    assert len(all_deployments) >= len(sample_deployments)

    # Fetch only specific number of deployments
    deployments_number = 2
    limited_number_deployments = sch.deployments.get_all(len=deployments_number)
    assert len(limited_number_deployments) == deployments_number


def test_update(sch, sample_deployments):
    for sample_deployment in sample_deployments:
        update_name = 'updated name {}'.format(get_random_string())
        sample_deployment.deployment_name = update_name
        extra_tag = 'updatedTag{}'.format(get_random_string())
        sample_deployment.tags = sample_deployment.tags + [extra_tag]

        # Update stage libraries
        stage_libraries = sample_deployment.engine_configuration.stage_libs
        if sample_deployment.engine_configuration.engine_type == 'DC':
            additional_stage_libs = ['jython_2_7', 'jdbc']
        else:
            additional_stage_libs = ['jdbc', 'snowflake-with-no-dependency']

        stage_libraries.extend(additional_stage_libs)

        # Update install type
        expected_install_type = 'DOCKER'
        sample_deployment.install_type = expected_install_type

        # Update external_resource_source
        expected_external_resource_source = 'http://www.google.com'
        sample_deployment.engine_configuration.external_resource_source = expected_external_resource_source

        # Update java configurations
        expected_maximum_java_heap_size_in_mb = 4096
        expected_minimum_java_heap_size_in_mb = 2048
        expected_java_opts = '-Xdebug'

        java_config = sample_deployment.engine_configuration.java_configuration
        java_config.maximum_java_heap_size_in_mb = expected_maximum_java_heap_size_in_mb
        java_config.minimum_java_heap_size_in_mb = expected_minimum_java_heap_size_in_mb
        java_config.java_options = expected_java_opts

        sch.update_deployment(sample_deployment)

        # Verify
        fetched_deployment = sch.deployments.get(deployment_id=sample_deployment.deployment_id)
        assert fetched_deployment.deployment_name == update_name

        assert fetched_deployment.install_type == expected_install_type
        assert fetched_deployment.engine_configuration.external_resource_source == expected_external_resource_source

        # stage libs
        assert set(additional_stage_libs).issubset(set(fetched_deployment.engine_configuration.stage_libs))

        # jvm config
        fetched_java_config = fetched_deployment.engine_configuration.java_configuration
        assert fetched_java_config.maximum_java_heap_size_in_mb == expected_maximum_java_heap_size_in_mb
        assert fetched_java_config.minimum_java_heap_size_in_mb == expected_minimum_java_heap_size_in_mb
        assert fetched_java_config.java_options == expected_java_opts

        # deployment tag
        assert extra_tag in fetched_deployment.deployment_tags

        # Can Delete Deployment
        can_delete_command = sch.api_client.can_delete_deployment(sample_deployment.deployment_id)
        assert can_delete_command.response.status_code == 200


def test_deployment_lock(sch, sample_deployments):
    for deployment in sample_deployments:
        sch.lock_deployment(deployment)
        assert deployment.locked
        sch.unlock_deployment(deployment)
        assert not deployment.locked


def test_deployments_with_additional_parameters(args, sch, sample_environment):
    """A set of sample deployments."""
    builder = sch.get_deployment_builder(deployment_type='SELF')
    passed_arguments = {
        'deployment_name': 'deployment_name_{}'.format(get_random_string()),
        'engine_type': 'DC',
        'engine_version': args.sdc_version,
        'environment': sample_environment,
        'external_resource_location': 'https::{}.com'.format(get_random_string()),
        'engine_labels': ['engine_label_{}'.format(get_random_string()), 'engine_label_{}'.format(get_random_string())],
        'max_cpu_load': random.randint(1, DEFAULT_MAX_CPU_LOAD_VALUE),
        'max_memory_used': random.randint(1, DEFAULT_MAX_MEMORY_USED_VALUE),
        'max_pipelines_running': random.randint(1, DEFAULT_MAX_PIPELINES_RUNNING_VALUE),
        'deployment_tags': [
            'deployment_tag_{}'.format(get_random_string()),
            'deployment_tag_{}'.format(get_random_string()),
        ],
        'engine_build': 'engine_build_{}'.format(get_random_string()),
        'scala_binary_version': '1.4.0',
    }

    deployment = builder.build(
        deployment_name=passed_arguments['deployment_name'],
        engine_type=passed_arguments['engine_type'],
        engine_version=passed_arguments['engine_version'],
        environment=passed_arguments['environment'],
        external_resource_location=passed_arguments['external_resource_location'],
        engine_labels=passed_arguments['engine_labels'],
        max_cpu_load=passed_arguments['max_cpu_load'],
        max_memory_used=passed_arguments['max_memory_used'],
        max_pipelines_running=passed_arguments['max_pipelines_running'],
        deployment_tags=passed_arguments['deployment_tags'],
    )
    sch.add_deployment(deployment)

    try:
        deployment = sch.deployments.get(deployment_name=deployment.deployment_name)
        engine_configuration = deployment.engine_configuration
        # Make sure all passed arguments are respected
        assert deployment._data['name'] == passed_arguments['deployment_name']
        assert deployment._data['type'] == 'SELF'
        assert deployment._data['environment'] == passed_arguments['environment'].environment_id
        assert deployment._data['rawDeploymentTags'] == passed_arguments['deployment_tags']
        assert engine_configuration._data['engineVersion'] == passed_arguments['engine_version']
        assert engine_configuration._data['externalResourcesUri'] == passed_arguments['external_resource_location']
        for label in engine_configuration._data['labels']:
            assert label in passed_arguments['engine_labels']
        assert engine_configuration._data['maxCpuLoad'] == passed_arguments['max_cpu_load']
        assert engine_configuration._data['maxMemoryUsed'] == passed_arguments['max_memory_used']
        assert engine_configuration._data['maxPipelinesRunning'] == passed_arguments['max_pipelines_running']

    except Exception as e:
        raise e

    finally:
        sch.delete_deployment(deployment)


def test_install_script(sch, sample_deployments):
    for deployment in sample_deployments:
        sch.start_deployment(deployment)
        assert deployment.install_script()
        sch.stop_deployment(deployment)


def test_clone_deployment(sch, sdc_deployment):
    cloned_deployment = sch.clone_deployment(sdc_deployment)
    assert cloned_deployment
    sch.delete_deployment(cloned_deployment)
