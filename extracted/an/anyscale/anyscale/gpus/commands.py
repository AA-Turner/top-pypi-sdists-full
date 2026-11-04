from datetime import datetime
from typing import Optional

from anyscale._private.sdk import sdk_command
from anyscale.gpus._private.gpus_sdk import PrivateGpusSDK
from anyscale.gpus.models import Gpu, NodeGpus


_GPUS_SDK_SINGLETON_KEY = "gpus_sdk"

# The cluster is named by exactly one of these; both commands take them the same way.
_RESOURCE_ARG_DOCSTRINGS = {
    "cluster_id": "ID of the cluster. Pass exactly one of cluster_id, workspace_id, "
    "job_id or service_id.",
    "workspace_id": "ID of the workspace; its cluster is read.",
    "job_id": "ID of the job; the cluster of its latest run is read (for a job in a job "
    "queue, the queue's cluster).",
    "service_id": "ID of the service; the cluster of its primary version is read. Read "
    "another version by its cluster_id.",
}

_NODE_GPUS_EXAMPLE = """
import anyscale

node = anyscale.gpus.node_gpus("nod_abc123", job_id="prodjob_abc123")
print(node.cluster_id, node.instance_type, node.gpu_count)
for gpu in node.gpus:
    print(gpu.gpu_index, gpu.uuid, gpu.state, gpu.utilization_pct, gpu.fb_used_mib)
"""

_NODE_GPUS_ARG_DOCSTRINGS = {
    "node_id": "ID of the node.",
    **_RESOURCE_ARG_DOCSTRINGS,
    "time": "Snapshot as of this moment. None means now. The backend looks back over "
    "the cluster's lifetime (capped at seven days), so a terminated or dead node still "
    "returns its last-known telemetry, as OFFLINE GPUs.",
}

_GET_EXAMPLE = """
import anyscale

gpu = anyscale.gpus.get("GPU-8f2e...", workspace_id="expwrk_abc123")
print(gpu.placement.node_id, gpu.placement.instance_type)
print(gpu.telemetry.state, gpu.telemetry.utilization_pct, gpu.telemetry.xids)
"""

_GET_ARG_DOCSTRINGS = {
    "gpu_uuid": "The GPU's UUID (GPU-...), as the driver and DCGM report it.",
    **_RESOURCE_ARG_DOCSTRINGS,
    "time": "Snapshot as of this moment. None means now. The backend looks back over "
    "the cluster's lifetime (capped at seven days), so a GPU whose node is gone still "
    "resolves, as OFFLINE; only a UUID never seen in that window is not found.",
}


@sdk_command(
    _GPUS_SDK_SINGLETON_KEY,
    PrivateGpusSDK,
    doc_py_example=_NODE_GPUS_EXAMPLE,
    arg_docstrings=_NODE_GPUS_ARG_DOCSTRINGS,
)
def node_gpus(  # noqa: PLR0913
    node_id: str,
    *,
    cluster_id: Optional[str] = None,
    workspace_id: Optional[str] = None,
    job_id: Optional[str] = None,
    service_id: Optional[str] = None,
    time: Optional[datetime] = None,
    _private_sdk: Optional[PrivateGpusSDK] = None,
) -> NodeGpus:
    """Get DCGM telemetry for every GPU on a node of a cluster, workspace, job or service."""
    return _private_sdk.node_gpus(  # type: ignore
        node_id,
        cluster_id=cluster_id,
        workspace_id=workspace_id,
        job_id=job_id,
        service_id=service_id,
        time=time,
    )


@sdk_command(
    _GPUS_SDK_SINGLETON_KEY,
    PrivateGpusSDK,
    doc_py_example=_GET_EXAMPLE,
    arg_docstrings=_GET_ARG_DOCSTRINGS,
)
def get(  # noqa: PLR0913
    gpu_uuid: str,
    *,
    cluster_id: Optional[str] = None,
    workspace_id: Optional[str] = None,
    job_id: Optional[str] = None,
    service_id: Optional[str] = None,
    time: Optional[datetime] = None,
    _private_sdk: Optional[PrivateGpusSDK] = None,
) -> Gpu:
    """Get one GPU by UUID: where it is and what it reports."""
    return _private_sdk.get(  # type: ignore
        gpu_uuid,
        cluster_id=cluster_id,
        workspace_id=workspace_id,
        job_id=job_id,
        service_id=service_id,
        time=time,
    )
