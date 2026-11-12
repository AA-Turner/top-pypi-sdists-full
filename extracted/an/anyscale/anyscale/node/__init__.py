from typing import List, Optional

from anyscale._private.anyscale_client import AnyscaleClientInterface
from anyscale._private.sdk import sdk_docs
from anyscale._private.sdk.base_sdk import Timer
from anyscale.cli_logger import BlockLogger
from anyscale.node._private.node_sdk import DEFAULT_MAX_ITEMS, PrivateNodeSDK
from anyscale.node.commands import (
    _GET_ARG_DOCSTRINGS,
    _GET_EXAMPLE,
    _LIST_ARG_DOCSTRINGS,
    _LIST_EXAMPLE,
    get as get,
    list as list,  # noqa: A004
)
from anyscale.node.models import Node, NodeList


class NodeSDK:
    def __init__(
        self,
        *,
        client: Optional[AnyscaleClientInterface] = None,
        logger: Optional[BlockLogger] = None,
        timer: Optional[Timer] = None,
    ):
        self._private_sdk = PrivateNodeSDK(client=client, logger=logger, timer=timer)

    @sdk_docs(
        doc_py_example=_GET_EXAMPLE,
        arg_docstrings=_GET_ARG_DOCSTRINGS,
    )
    def get(  # noqa: F811, PLR0913
        self,
        node_id: str,
        *,
        cluster_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        job_id: Optional[str] = None,
        service_id: Optional[str] = None,
        ray_session: Optional[str] = None,
    ) -> Node:
        """Get one node of a cluster, workspace, job or service: state, IPs, instance type,
        resources and labels.

        Needs Ray 2.50.0 or newer; on an older version the node is not found.
        """
        return self._private_sdk.get(
            node_id,
            cluster_id=cluster_id,
            workspace_id=workspace_id,
            job_id=job_id,
            service_id=service_id,
            ray_session=ray_session,
        )

    @sdk_docs(
        doc_py_example=_LIST_EXAMPLE,
        arg_docstrings=_LIST_ARG_DOCSTRINGS,
    )
    def list(  # noqa: A003, F811, PLR0913
        self,
        *,
        cluster_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        job_id: Optional[str] = None,
        service_id: Optional[str] = None,
        ray_session: Optional[str] = None,
        text_filter: Optional[str] = None,
        states: Optional[List[str]] = None,
        max_items: int = DEFAULT_MAX_ITEMS,
    ) -> NodeList:
        """List the nodes of a cluster, workspace, job or service, newest Ray session first,
        with optional filters.

        Needs Ray 2.50.0 or newer; on an older version the list is empty.
        """
        return self._private_sdk.list(
            cluster_id=cluster_id,
            workspace_id=workspace_id,
            job_id=job_id,
            service_id=service_id,
            ray_session=ray_session,
            text_filter=text_filter,
            states=states,
            max_items=max_items,
        )
