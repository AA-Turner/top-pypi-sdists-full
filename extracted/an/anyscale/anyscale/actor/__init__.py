from typing import Optional, Union

from anyscale._private.anyscale_client import AnyscaleClientInterface
from anyscale._private.sdk import sdk_docs
from anyscale._private.sdk.base_sdk import Timer
from anyscale.actor._private.actor_sdk import DEFAULT_MAX_ITEMS, PrivateActorSDK
from anyscale.actor.commands import (
    _AGGREGATE_ARG_DOCSTRINGS,
    _AGGREGATE_EXAMPLE,
    aggregate as aggregate,
)
from anyscale.actor.models import ActorAggregateBy, ActorAggregates
from anyscale.cli_logger import BlockLogger


class ActorSDK:
    def __init__(
        self,
        *,
        client: Optional[AnyscaleClientInterface] = None,
        logger: Optional[BlockLogger] = None,
        timer: Optional[Timer] = None,
    ):
        self._private_sdk = PrivateActorSDK(client=client, logger=logger, timer=timer)

    @sdk_docs(
        doc_py_example=_AGGREGATE_EXAMPLE,
        arg_docstrings=_AGGREGATE_ARG_DOCSTRINGS,
    )
    def aggregate(  # noqa: F811, PLR0913
        self,
        *,
        by: Union[str, ActorAggregateBy],
        cluster_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        job_id: Optional[str] = None,
        service_id: Optional[str] = None,
        ray_session: Optional[str] = None,
        max_items: int = DEFAULT_MAX_ITEMS,
        start_cluster: bool = True,
    ) -> ActorAggregates:
        """Group the Ray actors of a cluster, workspace, job or service by name, job or
        exit detail, with counts per state."""
        return self._private_sdk.aggregate(
            by=by,
            cluster_id=cluster_id,
            workspace_id=workspace_id,
            job_id=job_id,
            service_id=service_id,
            ray_session=ray_session,
            max_items=max_items,
            start_cluster=start_cluster,
        )
