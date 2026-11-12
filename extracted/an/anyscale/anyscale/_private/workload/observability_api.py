"""Reading a cluster's Ray task and actor data from the observability API.

The control plane does not serve task and actor aggregates: its `/tasks_dashboard` and
`/actors_dashboard` aggregate routes answer 501. The data comes from `observability_api`,
a service on the cloud's system workload cluster, and the console reaches it in three
steps that this module repeats:

1. Describe the system workload for the cluster's cloud, starting the system cluster when
   asked. A cold start takes minutes; the console polls every 5 s until the response
   carries the service URL, and so does this.
2. GET the auth URL from that response: it exchanges a short-lived token for the cookie
   the service checks on every request.
3. GET the data path with that cookie.
"""

from typing import Any, Dict, Optional

from anyscale._private.anyscale_client import AnyscaleClientInterface
from anyscale._private.sdk.timer import Timer
from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.models import ClusterState, DescribeSystemWorkloadResponse


# How the console polls describe while the system cluster comes up.
POLL_INTERVAL_S = 5
# How long to wait for it in all before giving up.
DEFAULT_START_TIMEOUT_S = 600

# States describe can report after which waiting changes nothing.
_FAILED_STATES = frozenset(
    {
        ClusterState.STARTUPERRORED,
        ClusterState.UPDATINGERRORED,
        ClusterState.TERMINATINGERRORED,
    }
)


def fetch_observability_api_json(  # noqa: PLR0913
    client: AnyscaleClientInterface,
    logger: BlockLogger,
    timer: Timer,
    *,
    cluster_id: str,
    path: str,
    params: Dict[str, Any],
    start_cluster: bool,
    timeout_s: float = DEFAULT_START_TIMEOUT_S,
) -> Dict[str, Any]:
    """GET `/clusters/{cluster_id}/{path}` on the cloud's observability API, as JSON.

    Resolves the cluster's cloud, waits for that cloud's system cluster to serve the API
    (starting it when `start_cluster`), then makes the call.
    """
    cloud_id = client.get_cluster_cloud_id(cluster_id)
    served = _wait_for_service(
        client,
        logger,
        timer,
        cloud_id=cloud_id,
        cluster_id=cluster_id,
        start_cluster=start_cluster,
        timeout_s=timeout_s,
    )
    assert served.workload_service_url and served.workload_service_url_auth
    return client.get_observability_api_json(
        service_url=served.workload_service_url,
        auth_url=served.workload_service_url_auth,
        path=f"/clusters/{cluster_id}/{path}",
        params=params,
    )


def _wait_for_service(  # noqa: PLR0913
    client: AnyscaleClientInterface,
    logger: BlockLogger,
    timer: Timer,
    *,
    cloud_id: str,
    cluster_id: str,
    start_cluster: bool,
    timeout_s: float,
) -> DescribeSystemWorkloadResponse:
    last_status: Optional[str] = None
    for _ in timer.poll(timeout_s=timeout_s, interval_s=POLL_INTERVAL_S):
        described = client.describe_ray_observability_api(
            cloud_id=cloud_id, cluster_id=cluster_id, start_cluster=start_cluster
        )
        if not described.is_enabled:
            raise ValueError(
                f"Ray task and actor data is not enabled for cloud '{cloud_id}': the "
                "cloud has no system cluster. It can be turned on in the cloud's settings."
            )
        if described.workload_service_url and described.workload_service_url_auth:
            return described
        status = str(described.status) if described.status else "not running"
        if described.status in _FAILED_STATES:
            raise ValueError(
                f"The system cluster of cloud '{cloud_id}' is {status} and cannot serve "
                "task and actor data until it is restarted."
            )
        if not start_cluster:
            raise ValueError(
                f"The system cluster of cloud '{cloud_id}' is {status}. Let the command "
                "start it (drop --no-start-cluster / pass start_cluster=True), or try "
                "again once it is running."
            )
        if status != last_status:
            logger.info(
                f"Waiting for the system cluster of cloud '{cloud_id}' to serve task and "
                f"actor data (status: {status})..."
            )
            last_status = status
    raise TimeoutError(
        f"Timed out after {int(timeout_s)}s waiting for the system cluster of cloud "
        f"'{cloud_id}' (last status: {last_status})."
    )
