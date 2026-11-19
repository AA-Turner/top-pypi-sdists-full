import pytest
from opentelemetry.sdk.resources import ResourceDetector
from opentelemetry_resourcedetector_docker import DockerResourceDetector
from opentelemetry_resourcedetector_kubernetes import (
    KubernetesDownwardAPIEnvironmentResourceDetector,
    KubernetesDownwardAPIVolumeResourceDetector,
)
from opentelemetry_resourcedetector_process import ProcessResourceDetector

from opentelemetry_container_distro import OpenTelemetryContainerConfigurator


@pytest.fixture
def detector_classes() -> set[type[ResourceDetector]]:
    configurator = OpenTelemetryContainerConfigurator()
    return {rd.__class__ for rd in configurator.resource_detectors}


def test_configures_resource_detectors(
    detector_classes: set[type[ResourceDetector]],
):
    assert detector_classes


def test_configures_docker(detector_classes: set[type[ResourceDetector]]):
    assert DockerResourceDetector in detector_classes


def test_configures_process(detector_classes: set[type[ResourceDetector]]):
    assert ProcessResourceDetector in detector_classes


def test_configures_kubernetes(detector_classes: set[type[ResourceDetector]]):
    assert KubernetesDownwardAPIEnvironmentResourceDetector in detector_classes
    assert KubernetesDownwardAPIVolumeResourceDetector in detector_classes
