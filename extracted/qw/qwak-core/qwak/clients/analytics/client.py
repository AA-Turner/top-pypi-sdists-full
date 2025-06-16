from datetime import timedelta
from time import sleep, time
from typing import Optional

import grpc
from _qwak_proto.qwak.analytics.analytics_pb2 import (
    QueryResultDownloadURLParams,
    QueryStatus,
)
from _qwak_proto.qwak.analytics.analytics_service_pb2 import (
    GetQueryResultDownloadURLRequest,
    GetQueryResultsPageRequest,
    GetQueryResultsPageResponse,
    QueryRequest,
)
from _qwak_proto.qwak.analytics.analytics_service_pb2_grpc import (
    AnalyticsQueryServiceStub,
)
from qwak.clients.location_discovery import LocationDiscoveryClient
from qwak.inner.di_configuration import QwakContainer
from qwak.inner.tool.grpc.grpc_tools import create_grpc_channel


class AnalyticsEngineError(RuntimeError):
    def __init__(self, failure_reason: str):
        super().__init__(
            f"Cannot retrieve results from the Qwak Analytics Engine\n{failure_reason}"
        )


class AnalyticsEngineClient:
    def __init__(self, grpc_channel: Optional[QwakContainer.core_grpc_channel] = None):
        self.grpc_client = self._create_grpc_client(grpc_channel)

    def get_analytics_data(self, query: str, timeout: timedelta = None) -> str:
        """
        Sends a given query to the Qwak Analytics Engine and returns the URL of the results file.

        Args:
            query (str): SQL query to be sent to the Qwak Analytics Engine
            timeout (timedelta): maximum time to wait for the query to complete. If None, the function will wait indefinitely.

        Returns:
            str: a path from which the results can be downloaded

        Raises:
            AnalyticsEngineError: if the query failed
            TimeoutError: if the query timed out
        """
        max_time = time() + timeout.total_seconds() if timeout else None
        query_id = self._send_query(query)

        while True:
            status_response = self._check_status(query_id)

            if status_response.status == QueryStatus.SUCCESS:
                download_url = self._get_download_url(query_id)
                return download_url
            elif status_response.status == QueryStatus.FAILED:
                raise AnalyticsEngineError(status_response.failure_reason)
            elif status_response.status == QueryStatus.CANCELED:
                raise AnalyticsEngineError("Query was cancelled")
            elif max_time and time() > max_time:
                raise TimeoutError()
            else:
                sleep(1)

    def _send_query(self, query: str) -> str:
        request = QueryRequest(query=query)
        response = self.grpc_client.Query(request)
        return response.query_id

    def _check_status(self, query_id: str) -> GetQueryResultsPageResponse:
        request = GetQueryResultsPageRequest(
            query_id=query_id, page_id=None, max_results=1
        )
        response = self.grpc_client.GetQueryResultsPage(request)
        return response

    def _get_download_url(self, query_id: str) -> str:
        request_params = QueryResultDownloadURLParams(query_id=query_id)
        request = GetQueryResultDownloadURLRequest(params=request_params)
        response = self.grpc_client.GetQueryResultDownloadURL(request)
        return response.download_url

    def _create_grpc_client(
        self, grpc_channel: Optional[grpc.Channel] = None
    ) -> AnalyticsQueryServiceStub:
        if grpc_channel:
            return AnalyticsQueryServiceStub(grpc_channel)

        channel = create_grpc_channel(
            url=self._get_analytics_engine_url(),
            status_for_retry=(
                grpc.StatusCode.UNAVAILABLE,
                grpc.StatusCode.CANCELLED,
            ),
        )
        return AnalyticsQueryServiceStub(channel)

    @staticmethod
    def _get_analytics_engine_url() -> str:
        """
        Fetches the analytics engine service URL from the LocationDiscoveryService.
        """
        return LocationDiscoveryClient().get_analytics_engine().service_url
