from datetime import datetime
from typing import List, Optional

from anyscale._private.anyscale_client import AnyscaleClientInterface
from anyscale._private.sdk import sdk_docs
from anyscale._private.sdk.base_sdk import Timer
from anyscale.cli_logger import BlockLogger
from anyscale.metrics._private.metrics_sdk import PrivateMetricsSDK
from anyscale.metrics.commands import (
    _NAMES_ARG_DOCSTRINGS,
    _NAMES_EXAMPLE,
    _QUERY_ARG_DOCSTRINGS,
    _QUERY_EXAMPLE,
    _QUERY_RANGE_ARG_DOCSTRINGS,
    _QUERY_RANGE_EXAMPLE,
    names as names,
    query as query,
    query_range as query_range,
)
from anyscale.metrics.models import MetricSeries, MetricsResource


class MetricsSDK:
    def __init__(
        self,
        *,
        client: Optional[AnyscaleClientInterface] = None,
        logger: Optional[BlockLogger] = None,
        timer: Optional[Timer] = None,
    ):
        self._private_sdk = PrivateMetricsSDK(client=client, logger=logger, timer=timer)

    @sdk_docs(
        doc_py_example=_NAMES_EXAMPLE,
        arg_docstrings=_NAMES_ARG_DOCSTRINGS,
    )
    def names(  # noqa: F811
        self,
        resource: MetricsResource,
        *,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> List[str]:
        """List the metric names that have data for a cluster, workspace, job or service."""
        return self._private_sdk.names(resource, start=start, end=end)

    @sdk_docs(
        doc_py_example=_QUERY_EXAMPLE,
        arg_docstrings=_QUERY_ARG_DOCSTRINGS,
    )
    def query(  # noqa: F811
        self,
        promql_query: str,
        resource: MetricsResource,
        *,
        time: Optional[datetime] = None,
    ) -> List[MetricSeries]:
        """Evaluate a PromQL expression at one moment for a cluster, workspace, job or service."""
        return self._private_sdk.query(promql_query, resource, time=time)

    @sdk_docs(
        doc_py_example=_QUERY_RANGE_EXAMPLE,
        arg_docstrings=_QUERY_RANGE_ARG_DOCSTRINGS,
    )
    def query_range(  # noqa: F811
        self,
        promql_query: str,
        resource: MetricsResource,
        *,
        start: datetime,
        end: datetime,
        step: Optional[str] = None,
    ) -> List[MetricSeries]:
        """Evaluate a PromQL expression at every step across a time window."""
        return self._private_sdk.query_range(
            promql_query, resource, start=start, end=end, step=step
        )
