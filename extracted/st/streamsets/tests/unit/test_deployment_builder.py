# Copyright Streamsets 2023
import random

# fmt: off
import pytest

from streamsets.sdk.constants import (
    DEFAULT_MAX_CPU_LOAD_VALUE, DEFAULT_MAX_MEMORY_USED_VALUE, DEFAULT_MAX_PIPELINES_RUNNING_VALUE,
)
from streamsets.sdk.utils import get_random_string

# fmt: on

DEFAULT_LOCATION_VALUE = None
DEFAULT_LABEL_VALUE = None
DEFAULT_TAGS_VALUE = None
DEFAULT_ENGINE_BUILD_VALUE = None
DEFAULT_SCALA_BINARY_VALUE = None


class MockEnvironment:
    def __init__(self):
        self.environment_type = 'SELF'
        self.environment_id = '123456789'


@pytest.fixture(scope="function")
def passed_arguments():
    passed_arguments = {
        'deployment_name': 'deployment_name_{}'.format(get_random_string()),
        'engine_type': 'DC',
        'engine_version': '5.1.0',
        'environment': MockEnvironment(),
        'external_resource_location': 'https::{}.com'.format(get_random_string()),
        'engine_labels': ['engine_label_{}'.format(get_random_string()), 'engine_label_{}'.format(get_random_string())],
        'max_cpu_load': random.randint(1, 10),
        'max_memory_used': random.randint(1, 100),
        'max_pipelines_running': random.randint(1, 100000),
        'deployment_tags': [
            'deployment_tag_{}'.format(get_random_string()),
            'deployment_tag_{}'.format(get_random_string()),
        ],
        'engine_build': 'engine_build_{}'.format(get_random_string()),
        'scala_binary_version': '1.4.0',
    }
    return passed_arguments


@pytest.mark.parametrize(
    "deployment_builder, deployment_type",
    [
        ('self_deployment_builder', 'SELF'),
        ('gce_deployment_builder', 'GCE'),
        ('ec2_deployment_builder', 'EC2'),
        ('azure_deployment_builder', 'AZURE_VM'),
        ('kubernetes_deployment_builder', 'KUBERNETES'),
    ],
)
def test_deployment_builder_build_sanity(deployment_builder, deployment_type, passed_arguments, request):
    deployment_builder = request.getfixturevalue(deployment_builder)

    passed_arguments['environment'].environment_type = deployment_type

    deployment = deployment_builder.build(
        deployment_name=passed_arguments['deployment_name'],
        environment=passed_arguments['environment'],
        engine_type=passed_arguments['engine_type'],
        engine_version=passed_arguments['engine_version'],
    )
    assert deployment


@pytest.mark.parametrize(
    "deployment_builder, deployment_type",
    [
        ('self_deployment_builder', 'SELF'),
        ('gce_deployment_builder', 'GCE'),
        ('ec2_deployment_builder', 'EC2'),
        ('azure_deployment_builder', 'AZURE_VM'),
        ('kubernetes_deployment_builder', 'KUBERNETES'),
    ],
)
def test_deployment_builder_build_respects_arguments_passed(
    deployment_builder, passed_arguments, deployment_type, request
):
    passed_arguments['environment'].environment_type = deployment_type

    deployment_builder = request.getfixturevalue(deployment_builder)

    deployment = deployment_builder.build(
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
        engine_build=passed_arguments['engine_build'],
        scala_binary_version=passed_arguments['scala_binary_version'],
    )

    # Make sure all passed arguments are respected
    assert deployment._data['name'] == passed_arguments['deployment_name']
    assert deployment._data['type'] == deployment_type
    assert deployment._data['engineVersion'] == passed_arguments['engine_version']
    assert deployment._data['envId'] == passed_arguments['environment'].environment_id
    assert (
        deployment._data['engineConfiguration']['externalResourcesUri']
        == passed_arguments['external_resource_location']
    )
    assert deployment._data['engineConfiguration']['labels'] == passed_arguments['engine_labels']
    assert deployment._data['engineConfiguration']['maxCpuLoad'] == passed_arguments['max_cpu_load']
    assert deployment._data['engineConfiguration']['maxMemoryUsed'] == passed_arguments['max_memory_used']
    assert deployment._data['engineConfiguration']['maxPipelinesRunning'] == passed_arguments['max_pipelines_running']
    assert [deployment['tag'] for deployment in deployment._data['deploymentTags']] == passed_arguments[
        'deployment_tags'
    ]
    assert deployment._data['engineBuild'] == passed_arguments['engine_build']
    assert deployment._data['scalaBinaryVersion'] == passed_arguments['scala_binary_version']

    if deployment_type == "AWS":
        assert deployment._data['sshKeySource'] == "NONE"


@pytest.mark.parametrize(
    "deployment_builder, deployment_type",
    [
        ('self_deployment_builder', 'SELF'),
        ('gce_deployment_builder', 'GCE'),
        ('ec2_deployment_builder', 'EC2'),
        ('azure_deployment_builder', 'AZURE_VM'),
        ('kubernetes_deployment_builder', 'KUBERNETES'),
    ],
)
def test_deployment_builder_build_respects_default_values(
    deployment_builder, deployment_type, passed_arguments, request
):
    deployment_builder = request.getfixturevalue(deployment_builder)
    passed_arguments['environment'].environment_type = deployment_type

    deployment = deployment_builder.build(
        deployment_name=passed_arguments['deployment_name'],
        environment=passed_arguments['environment'],
        engine_type=passed_arguments['engine_type'],
        engine_version=passed_arguments['engine_version'],
    )

    # Make sure default values are respected
    assert deployment._data['engineConfiguration']['externalResourcesUri'] == DEFAULT_LOCATION_VALUE
    assert deployment._data['engineConfiguration']['labels'] == DEFAULT_LABEL_VALUE
    assert deployment._data['engineConfiguration']['maxCpuLoad'] == DEFAULT_MAX_CPU_LOAD_VALUE
    assert deployment._data['engineConfiguration']['maxMemoryUsed'] == DEFAULT_MAX_MEMORY_USED_VALUE
    assert deployment._data['engineConfiguration']['maxPipelinesRunning'] == DEFAULT_MAX_PIPELINES_RUNNING_VALUE
    assert deployment._data['deploymentTags'] == DEFAULT_TAGS_VALUE
    assert deployment._data['engineBuild'] == DEFAULT_ENGINE_BUILD_VALUE
    assert deployment._data['scalaBinaryVersion'] == DEFAULT_SCALA_BINARY_VALUE


@pytest.mark.parametrize(
    "key_to_change, value",
    [
        ('deployment_name', 1),
        ('engine_type', 1),
        ('engine_version', 1),
        ('external_resource_location', 1),
        ('engine_labels', 'STRING VALUE'),
        ('max_cpu_load', 'STRING VALUE'),
        ('max_memory_used', 'STRING VALUE'),
        ('max_pipelines_running', 'STRING VALUE'),
        ('deployment_tags', 'STRING VALUE'),
        ('engine_build', 1),
        ('scala_binary_version', 1),
    ],
)
def test_deployment_builder_build_fails_on_invalid_types(
    key_to_change, value, self_deployment_builder, passed_arguments, request
):
    passed_arguments['environment'].environment_type = 'SELF'
    passed_arguments[key_to_change] = value

    with pytest.raises(TypeError):
        self_deployment_builder.build(
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
            engine_build=passed_arguments['engine_build'],
            scala_binary_version=passed_arguments['scala_binary_version'],
        )


@pytest.mark.parametrize(
    "deployment_builder, deployment_type",
    [
        ('self_deployment_builder', 'SELF'),
        ('gce_deployment_builder', 'GCE'),
        ('ec2_deployment_builder', 'EC2'),
        ('azure_deployment_builder', 'AZURE_VM'),
        ('kubernetes_deployment_builder', 'KUBERNETES'),
    ],
)
def test_deployment_builder_build_fails_for_value_over_100_for_max_cpu_load(
    deployment_builder, passed_arguments, deployment_type, request
):
    passed_arguments['environment'].environment_type = deployment_type

    deployment_builder = request.getfixturevalue(deployment_builder)

    with pytest.raises(ValueError):
        deployment_builder.build(
            deployment_name=passed_arguments['deployment_name'],
            engine_type=passed_arguments['engine_type'],
            engine_version=passed_arguments['engine_version'],
            environment=passed_arguments['environment'],
            external_resource_location=passed_arguments['external_resource_location'],
            engine_labels=passed_arguments['engine_labels'],
            max_cpu_load=1000.0,
        )


@pytest.mark.parametrize(
    "deployment_builder, deployment_type",
    [
        ('self_deployment_builder', 'SELF'),
        ('gce_deployment_builder', 'GCE'),
        ('ec2_deployment_builder', 'EC2'),
        ('azure_deployment_builder', 'AZURE_VM'),
        ('kubernetes_deployment_builder', 'KUBERNETES'),
    ],
)
def test_deployment_builder_build_fails_for_value_over_100_for_max_memory_used(
    deployment_builder, passed_arguments, deployment_type, request
):
    passed_arguments['environment'].environment_type = deployment_type

    deployment_builder = request.getfixturevalue(deployment_builder)

    with pytest.raises(ValueError):
        deployment_builder.build(
            deployment_name=passed_arguments['deployment_name'],
            engine_type=passed_arguments['engine_type'],
            engine_version=passed_arguments['engine_version'],
            environment=passed_arguments['environment'],
            external_resource_location=passed_arguments['external_resource_location'],
            engine_labels=passed_arguments['engine_labels'],
            max_memory_used=1000.0,
        )
