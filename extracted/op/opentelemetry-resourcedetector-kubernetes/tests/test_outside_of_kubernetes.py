from opentelemetry.sdk.resources import Resource

from opentelemetry_resourcedetector_kubernetes import KubernetesResourceDetector


def test_detecting_in_cgroup_outside_kubernetes(non_kubernetes_cgroups):
    assert not KubernetesResourceDetector().running_in_kubernetes()


def test_in_group_outside_kubernetes_returns_empty_resource(non_kubernetes_cgroups):
    assert KubernetesResourceDetector().detect() == Resource.get_empty()


def test_detecting_outside_of_cgroup(no_cgroup):
    assert not KubernetesResourceDetector().running_in_kubernetes()


def test_outside_of_cgroup_returns_empty_resource(no_cgroup):
    assert KubernetesResourceDetector().detect() == Resource.get_empty()
