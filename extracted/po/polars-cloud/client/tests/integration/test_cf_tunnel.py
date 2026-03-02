import time

import polars_cloud.constants
import pytest
import requests
from polars_cloud import ComputeContext, Workspace

from .conftest import ComputeContextSpecsInput  # noqa: TID252

# This applies the tunnel mark at the module level
pytestmark = pytest.mark.cf_tunnel


@pytest.mark.parametrize(
    "direct_compute",
    [ComputeContextSpecsInput(instance_type="t4g.micro", cluster_size=2)],
    # using 2 instances to test whether tunnel actually arrives at the leader
    indirect=True,
)
def test_cf_tunnel(direct_compute: ComputeContext, workspace: Workspace) -> None:
    cluster = polars_cloud.constants.API_CLIENT.get_compute_cluster(
        workspace.id,
        direct_compute._compute_id,  # type: ignore[arg-type]
    )

    assert cluster.tunnel_addr is not None, "tunnel_addr is None"
    url = f"https://{cluster.tunnel_addr}/api/v1/health"

    err: Exception | None = None
    for _ in range(10):
        try:
            response = requests.get(url)
            assert response.status_code == 200
            assert response.json()["status"] == "ok"
        except Exception as e:
            err = e
            time.sleep(1)
        else:
            return

    if err is not None:
        raise err


@pytest.mark.parametrize(
    "proxy_compute",
    [ComputeContextSpecsInput(instance_type="t4g.micro")],
    indirect=True,
)
def test_proxy_no_tunnel(proxy_compute: ComputeContext) -> None:
    cluster = polars_cloud.constants.API_CLIENT.get_compute_cluster(
        proxy_compute.workspace.id,
        proxy_compute._compute_id,  # type: ignore[arg-type]
    )

    assert cluster.tunnel_addr is None
