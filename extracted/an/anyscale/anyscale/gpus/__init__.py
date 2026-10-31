from datetime import datetime
from typing import Optional

from anyscale._private.anyscale_client import AnyscaleClientInterface
from anyscale._private.sdk import sdk_docs
from anyscale._private.sdk.base_sdk import Timer
from anyscale.cli_logger import BlockLogger
from anyscale.gpus._private.gpus_sdk import PrivateGpusSDK
from anyscale.gpus.commands import (
    _GET_ARG_DOCSTRINGS,
    _GET_EXAMPLE,
    _NODE_GPUS_ARG_DOCSTRINGS,
    _NODE_GPUS_EXAMPLE,
    get as get,
    node_gpus as node_gpus,
)
from anyscale.gpus.models import Gpu, NodeGpus


class GpusSDK:
    def __init__(
        self,
        *,
        client: Optional[AnyscaleClientInterface] = None,
        logger: Optional[BlockLogger] = None,
        timer: Optional[Timer] = None,
    ):
        self._private_sdk = PrivateGpusSDK(client=client, logger=logger, timer=timer)

    @sdk_docs(
        doc_py_example=_NODE_GPUS_EXAMPLE,
        arg_docstrings=_NODE_GPUS_ARG_DOCSTRINGS,
    )
    def node_gpus(  # noqa: F811
        self,
        cluster_id: str,
        node_id: str,
        *,
        time: Optional[datetime] = None,
    ) -> NodeGpus:
        """Get DCGM telemetry for every GPU on a node of a cluster."""
        return self._private_sdk.node_gpus(cluster_id, node_id, time=time)

    @sdk_docs(
        doc_py_example=_GET_EXAMPLE,
        arg_docstrings=_GET_ARG_DOCSTRINGS,
    )
    def get(  # noqa: F811
        self,
        cluster_id: str,
        gpu_uuid: str,
        *,
        time: Optional[datetime] = None,
    ) -> Gpu:
        """Get one GPU of a cluster by UUID: where it is and what it reports."""
        return self._private_sdk.get(cluster_id, gpu_uuid, time=time)
