import os
import tempfile

import pytest
from opentelemetry.sdk.resources import Resource

from opentelemetry_resourcedetector_kubernetes import (
    Attributes,
    KubernetesDownwardAPIVolumeResourceDetector,
)


def test_in_group_outside_kubernetes_returns_empty_resource(non_kubernetes_cgroups):
    resource = KubernetesDownwardAPIVolumeResourceDetector().detect()
    assert resource == Resource.get_empty()


def test_outside_of_cgroup_returns_empty_resource(no_cgroup):
    resource = KubernetesDownwardAPIVolumeResourceDetector().detect()
    assert resource == Resource.get_empty()


def test_non_existant_directory_uses_base_attributes(kubernetes_cgroups):
    assert not os.path.exists('/nope')
    resource = KubernetesDownwardAPIVolumeResourceDetector(directory='/nope').detect()
    assert 'container.id' in resource.attributes
    assert 'k8s.namespace.name' not in resource.attributes


@pytest.fixture(scope='module')
def downward():
    with tempfile.TemporaryDirectory() as directory:
        contents = {
            'k8s.namespace.name': 'cool-app',
            'k8s.pod.name': 'example-pod',
            'k8s.node.name': 'nodey-mcnoderson',
            'container.name': 'container-one',
            'container.image.name': 'cool-bits',
            'container.image.tag': '1.2.3',
            'k8s.this.is.not.a.thing': 'nope',
        }
        for key, value in contents.items():
            full_path = os.path.join(directory, key)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(value)
            with open(full_path, 'r', encoding='utf-8') as f:
                assert f.read() == value
        yield directory


@pytest.fixture(scope='module')
def resource(kubernetes_cgroups, downward: str) -> Resource:
    return KubernetesDownwardAPIVolumeResourceDetector(directory=downward).detect()


def test_container_id(attributes: Attributes, container_id: str):
    assert attributes['container.id'] == container_id


def test_container_runtime(attributes: Attributes):
    assert attributes['container.runtime'] == 'kubernetes'


def test_pod_uid(attributes: Attributes, pod_uid: str):
    assert attributes['k8s.pod.uid'] == pod_uid


def test_namespace(attributes: Attributes, pod_uid: str):
    assert attributes['k8s.namespace.name'] == 'cool-app'


# def test_pod_name(attributes: Attributes, pod_uid: str, downward: str):
#     assert attributes['k8s.pod.name'] == 'example-pod'


# def test_node_name(attributes: Attributes, pod_uid: str):
#     assert attributes['k8s.node.name'] == 'nodey-mcnoderson'


# def test_container_name(attributes: Attributes, pod_uid: str):
#     assert attributes['container.name'] == 'container-one'


# def test_container_image_name(attributes: Attributes, pod_uid: str):
#     assert attributes['container.image.name'] == 'cool-bits'


# def test_container_image_tag(attributes: Attributes, pod_uid: str):
#     assert attributes['container.image.tag'] == '1.2.3'
