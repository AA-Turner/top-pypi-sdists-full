import pytest
from opentelemetry.sdk.resources import Resource

from opentelemetry_resourcedetector_kubernetes import (
    Attributes,
    KubernetesResourceDetector,
)


@pytest.fixture(scope='module')
def resource(kubernetes_cgroups) -> Resource:
    return KubernetesResourceDetector().detect()


def test_getting_ids(kubernetes_cgroups, pod_uid, container_id):
    detector = KubernetesResourceDetector()
    assert detector.pod_uid() == pod_uid
    assert detector.container_id() == container_id


def test_detecting_within_kubernetes(kubernetes_cgroups):
    assert KubernetesResourceDetector().running_in_kubernetes()


def test_container_id(attributes: Attributes, container_id: str):
    assert attributes['container.id'] == container_id


def test_container_runtime(attributes: Attributes):
    assert attributes['container.runtime'] == 'kubernetes'


def test_pod_uid(attributes: Attributes, pod_uid: str):
    assert attributes['k8s.pod.uid'] == pod_uid
