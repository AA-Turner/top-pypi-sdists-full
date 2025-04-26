from pkg_resources import iter_entry_points

from opentelemetry_container_distro import (
    OpenTelemetryContainerConfigurator,
    OpenTelemetryContainerDistro,
)


def _first_entry_point(group):
    entry_points = list(iter_entry_points(group))
    assert len(entry_points) == 1
    return entry_points[0]


def test_registers_distro():
    entry_point = _first_entry_point('opentelemetry_distro')
    assert entry_point.load() == OpenTelemetryContainerDistro


def test_registers_configurator():
    entry_point = _first_entry_point('opentelemetry_configurator')
    assert entry_point.load() == OpenTelemetryContainerConfigurator
