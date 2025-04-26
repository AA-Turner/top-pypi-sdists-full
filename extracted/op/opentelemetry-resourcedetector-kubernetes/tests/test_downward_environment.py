import os
from unittest import mock

import pytest
from opentelemetry.sdk.resources import Resource

from opentelemetry_resourcedetector_kubernetes import (
    Attributes,
    KubernetesDownwardAPIEnvironmentResourceDetector,
)


def test_in_group_outside_kubernetes_returns_empty_resource(non_kubernetes_cgroups):
    resource = KubernetesDownwardAPIEnvironmentResourceDetector().detect()
    assert resource == Resource.get_empty()


def test_outside_of_cgroup_returns_empty_resource(no_cgroup):
    resource = KubernetesDownwardAPIEnvironmentResourceDetector().detect()
    assert resource == Resource.get_empty()


@pytest.fixture(scope='module')
def downward_environment_variables():
    variables = {
        'ALT_K8S_NAMESPACE_NAME': 'cool-app',
        'ALT_K8S_POD_NAME': 'example-pod',
        'ALT_K8S_NODE_NAME': 'nodey-mcnoderson',
        'ALT_K8S_THIS_IS_NOT_A_THING': 'nope',
        'ALT_CONTAINER_NAME': 'container-one',
        'ALT_CONTAINER_IMAGE_NAME': 'cool-bits',
        'ALT_CONTAINER_IMAGE_TAG': '1.2.3',
    }
    with mock.patch.dict(os.environ, variables):
        yield


@pytest.fixture(scope='module')
def resource(kubernetes_cgroups, downward_environment_variables) -> Resource:
    return KubernetesDownwardAPIEnvironmentResourceDetector(prefix='ALT').detect()


def test_container_id(attributes: Attributes, container_id: str):
    assert attributes['container.id'] == container_id


def test_container_runtime(attributes: Attributes):
    assert attributes['container.runtime'] == 'kubernetes'


def test_pod_uid(attributes: Attributes, pod_uid: str):
    assert attributes['k8s.pod.uid'] == pod_uid


def test_namespace(attributes: Attributes, pod_uid: str):
    assert attributes['k8s.namespace.name'] == 'cool-app'


def test_pod_name(attributes: Attributes, pod_uid: str):
    assert attributes['k8s.pod.name'] == 'example-pod'


def test_node_name(attributes: Attributes, pod_uid: str):
    assert attributes['k8s.node.name'] == 'nodey-mcnoderson'


def test_container_name(attributes: Attributes, pod_uid: str):
    assert attributes['container.name'] == 'container-one'


def test_container_image_name(attributes: Attributes, pod_uid: str):
    assert attributes['container.image.name'] == 'cool-bits'


def test_container_image_tag(attributes: Attributes, pod_uid: str):
    assert attributes['container.image.tag'] == '1.2.3'
