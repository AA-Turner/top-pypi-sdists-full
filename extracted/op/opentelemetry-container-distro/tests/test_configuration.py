from typing import Set, Type

import pytest
from opentelemetry_resourcedetector_docker import DockerResourceDetector
from opentelemetry_resourcedetector_kubernetes import (
    KubernetesDownwardAPIEnvironmentResourceDetector,
    KubernetesDownwardAPIVolumeResourceDetector,
)
from opentelemetry_resourcedetector_process import ProcessResourceDetector

from opentelemetry_container_distro import OpenTelemetryContainerConfigurator


@pytest.fixture
def detector_classes() -> set:
    configurator = OpenTelemetryContainerConfigurator()
    return {rd.__class__ for rd in configurator.resource_detectors}


def test_configures_resource_detectors():
    assert detector_classes


def test_configures_docker(detector_classes: Set[Type]):
    assert DockerResourceDetector in detector_classes


def test_configures_process(detector_classes: Set[Type]):
    assert ProcessResourceDetector in detector_classes


def test_configures_kubernetes(detector_classes: Set[Type]):
    assert KubernetesDownwardAPIEnvironmentResourceDetector in detector_classes
    assert KubernetesDownwardAPIVolumeResourceDetector in detector_classes
