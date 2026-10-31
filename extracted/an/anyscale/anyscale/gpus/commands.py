from datetime import datetime
from typing import Optional

from anyscale._private.sdk import sdk_command
from anyscale.gpus._private.gpus_sdk import PrivateGpusSDK
from anyscale.gpus.models import Gpu, NodeGpus


_GPUS_SDK_SINGLETON_KEY = "gpus_sdk"

_NODE_GPUS_EXAMPLE = """
import anyscale

node = anyscale.gpus.node_gpus(cluster_id="ses_abc123", node_id="nod_abc123")
print(node.instance_type, node.gpu_count)
for gpu in node.gpus:
    print(gpu.gpu_index, gpu.uuid, gpu.state, gpu.utilization_pct, gpu.fb_used_mib)
"""

_NODE_GPUS_ARG_DOCSTRINGS = {
    "cluster_id": "ID of the cluster the node belongs to.",
    "node_id": "ID of the node.",
    "time": "Snapshot as of this moment. None means now. The backend looks back over "
    "the cluster's lifetime (capped at seven days), so a terminated or dead node still "
    "returns its last-known telemetry, as OFFLINE GPUs.",
}

_GET_EXAMPLE = """
import anyscale

gpu = anyscale.gpus.get(cluster_id="ses_abc123", gpu_uuid="GPU-8f2e...")
print(gpu.placement.node_id, gpu.placement.instance_type)
print(gpu.telemetry.state, gpu.telemetry.utilization_pct, gpu.telemetry.xids)
"""

_GET_ARG_DOCSTRINGS = {
    "cluster_id": "ID of the cluster to look in.",
    "gpu_uuid": "The GPU's UUID (GPU-...), as the driver and DCGM report it.",
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
def node_gpus(
    cluster_id: str,
    node_id: str,
    *,
    time: Optional[datetime] = None,
    _private_sdk: Optional[PrivateGpusSDK] = None,
) -> NodeGpus:
    """Get DCGM telemetry for every GPU on a node of a cluster."""
    return _private_sdk.node_gpus(cluster_id, node_id, time=time)  # type: ignore


@sdk_command(
    _GPUS_SDK_SINGLETON_KEY,
    PrivateGpusSDK,
    doc_py_example=_GET_EXAMPLE,
    arg_docstrings=_GET_ARG_DOCSTRINGS,
)
def get(
    cluster_id: str,
    gpu_uuid: str,
    *,
    time: Optional[datetime] = None,
    _private_sdk: Optional[PrivateGpusSDK] = None,
) -> Gpu:
    """Get one GPU of a cluster by UUID: where it is and what it reports."""
    return _private_sdk.get(cluster_id, gpu_uuid, time=time)  # type: ignore
