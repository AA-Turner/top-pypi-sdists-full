from collections.abc import Mapping
import pytest
from opentelemetry.sdk.resources import Resource

from opentelemetry_resourcedetector_kubernetes import KubernetesResourceDetector


@pytest.fixture(scope="module")
def resource(kubernetes_cgroups: None) -> Resource:
    return KubernetesResourceDetector().detect()


def test_getting_ids(kubernetes_cgroups: None, pod_uid: str, container_id: str):
    detector = KubernetesResourceDetector()
    assert detector.pod_uid() == pod_uid
    assert detector.container_id() == container_id


def test_detecting_within_kubernetes(kubernetes_cgroups: None):
    assert KubernetesResourceDetector().running_in_kubernetes()


def test_container_id(attributes: Mapping[str, object], container_id: str):
    assert attributes["container.id"] == container_id


def test_container_runtime(attributes: Mapping[str, object]):
    assert attributes["container.runtime"] == "kubernetes"


def test_pod_uid(attributes: Mapping[str, object], pod_uid: str):
    assert attributes["k8s.pod.uid"] == pod_uid
