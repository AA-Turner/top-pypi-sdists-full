from datetime import datetime

import pytest

from arraylake.cli.compute import _services_table
from arraylake.compute.types import DeploymentInfo, ServiceConfig, ServiceStatus, ServiceType


def _service(status: str) -> DeploymentInfo:
    return DeploymentInfo(
        name=f"svc-{status}",
        url="https://example.invalid",
        created=datetime(2026, 1, 1),
        config=ServiceConfig(service_type=ServiceType.dap, org="acme", is_public=False),
        status=status,
    )


@pytest.mark.parametrize("status", list(ServiceStatus))
def test_every_status_renders(status: ServiceStatus) -> None:
    """The API owns this vocabulary, so a colour map that lags it must not break `compute list`.

    Four of the eight members had no colour, and the lookup raised KeyError rather than
    rendering, so listing an org with a sleeping service failed outright.
    """
    assert _services_table([_service(status.value)], "acme").row_count == 1


def test_status_the_client_has_never_heard_of_renders() -> None:
    """An older client must still list services after the API adds a status."""
    service = _service(ServiceStatus.available.value)
    object.__setattr__(service, "status", "a-status-from-the-future")
    assert _services_table([service], "acme").row_count == 1
