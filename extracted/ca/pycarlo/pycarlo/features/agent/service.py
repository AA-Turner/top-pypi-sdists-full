from __future__ import annotations

from datetime import datetime
from typing import Optional

from pycarlo.common.settings import (
    HEADER_MCD_TELEMETRY_REASON,
    HEADER_MCD_TELEMETRY_SERVICE,
    RequestReason,
)
from pycarlo.core import Client
from pycarlo.features.agent.models import (
    AgentSpanFilter,
    SpanAttributeFilter,
    SpanQueryResult,
)
from pycarlo.features.agent.queries import GET_AGENT_SPAN_SAMPLE_V2


class AgentService:
    """Service for querying agent spans."""

    def __init__(self, mc_client: Optional[Client] = None):
        self._mc_client = mc_client or Client()

    def get_agent_spans(
        self,
        mcon: str,
        span_ids: Optional[list[str]] = None,
        trace_ids: Optional[list[str]] = None,
        agent_span_filters: Optional[list[AgentSpanFilter]] = None,
        attribute_filters: Optional[list[SpanAttributeFilter]] = None,
        ingestion_start_time: Optional[datetime] = None,
        ingestion_end_time: Optional[datetime] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> SpanQueryResult:
        """
        Query agent spans using getAgentSpanSampleV2.

        :param mcon: MCON identifier for the table
        :param span_ids: Filter by specific span IDs
        :param trace_ids: Filter by specific trace IDs
        :param agent_span_filters: Filter by agent, workflow, task, or span name
        :param attribute_filters: Filter by attribute key-value pairs from attr_map
        :param ingestion_start_time: Start of ingestion time range
        :param ingestion_end_time: End of ingestion time range
        :param limit: Maximum number of results to return
        :param offset: Pagination offset
        :return: SpanQueryResult containing columns and rows
        """
        variables: dict[str, object] = {"mcon": mcon}

        if span_ids is not None:
            variables["spanIds"] = span_ids
        if trace_ids is not None:
            variables["traceIds"] = trace_ids
        if agent_span_filters is not None:
            variables["agentSpanFilters"] = [f.to_dict() for f in agent_span_filters]
        if attribute_filters is not None:
            variables["attributeFilters"] = [f.to_dict() for f in attribute_filters]
        if ingestion_start_time is not None:
            variables["ingestionStartTime"] = ingestion_start_time.isoformat()
        if ingestion_end_time is not None:
            variables["ingestionEndTime"] = ingestion_end_time.isoformat()
        if limit is not None:
            variables["limit"] = limit
        if offset is not None:
            variables["offset"] = offset

        response = self._mc_client(
            query=GET_AGENT_SPAN_SAMPLE_V2,
            variables=variables,
            additional_headers={
                HEADER_MCD_TELEMETRY_REASON: RequestReason.SERVICE.value,
                HEADER_MCD_TELEMETRY_SERVICE: "agent_service",
            },
        )

        result = response.get_agent_span_sample_v2  # type: ignore[union-attr]
        return SpanQueryResult(
            columns=list(result.columns or []),  # type: ignore[arg-type]
            rows=list(result.rows or []),  # type: ignore[arg-type]
            has_error=bool(result.has_error),
            error=str(result.error) if result.error else None,
        )
