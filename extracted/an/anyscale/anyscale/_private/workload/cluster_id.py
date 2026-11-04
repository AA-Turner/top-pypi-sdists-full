"""The cluster behind a workspace, job or service ID.

Node and GPU views read one cluster, but the console does not show cluster IDs: users
have the ID of their workspace, job or service. These commands take exactly one of the
four IDs and look the cluster up here, before calling the cluster-scoped endpoint.
"""

from typing import Optional

from anyscale._private.anyscale_client import AnyscaleClientInterface


RESOURCE_ID_ARGS = "cluster_id, workspace_id, job_id or service_id"


def resolve_cluster_id(
    client: AnyscaleClientInterface,
    *,
    cluster_id: Optional[str] = None,
    workspace_id: Optional[str] = None,
    job_id: Optional[str] = None,
    service_id: Optional[str] = None,
) -> str:
    """The cluster ID for exactly one of the four IDs.

    - cluster_id: returned as given.
    - workspace_id: the workspace's cluster.
    - job_id: the cluster of the job's latest run (for a job in a job queue, the queue's
      cluster).
    - service_id: the cluster of the service's primary version. Other versions are read
      by their cluster_id.
    """
    given = [value for value in (cluster_id, workspace_id, job_id, service_id) if value]
    if len(given) != 1:
        raise ValueError(f"Exactly one of {RESOURCE_ID_ARGS} is required.")

    if cluster_id:
        return cluster_id
    if workspace_id:
        return _workspace_cluster_id(client, workspace_id)
    if job_id:
        return _require(
            client.get_job_cluster_id(job_id),
            f"Job '{job_id}' has no cluster yet: its latest run has not started.",
        )
    assert service_id
    return _service_cluster_id(client, service_id)


def _workspace_cluster_id(client: AnyscaleClientInterface, workspace_id: str) -> str:
    workspace = client.get_workspace(name=None, id=workspace_id, cloud=None, project=None)
    if workspace is None:
        raise ValueError(f"Workspace '{workspace_id}' not found.")
    return _require(workspace.cluster_id, f"Workspace '{workspace_id}' has no cluster yet.")


def _service_cluster_id(client: AnyscaleClientInterface, service_id: str) -> str:
    service = client.get_service_by_id(service_id)
    if service is None:
        raise ValueError(f"Service '{service_id}' not found.")
    # A version runs on a job; its first job is the one the version's cluster belongs to,
    # the same lookup `controller_logs_for_service_version` makes.
    version = service.primary_version
    job_ids = (version.production_job_ids if version is not None else None) or []
    no_cluster = f"Service '{service_id}' has no cluster yet: its primary version has not started."
    if not job_ids:
        raise ValueError(no_cluster)
    return _require(client.get_job_cluster_id(job_ids[0]), no_cluster)


def _require(cluster_id: Optional[str], message: str) -> str:
    if not cluster_id:
        raise ValueError(message)
    return cluster_id
