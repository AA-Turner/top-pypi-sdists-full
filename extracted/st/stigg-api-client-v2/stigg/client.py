from typing import Union, Optional, Dict, Any

import httpx
from httpx import Timeout
from tenacity import retry, retry_if_exception_type, stop_after_attempt

from stigg.generated.client import Client
from stigg.generated.async_client import AsyncClient
from stigg.generated import FetchEntitlementsQuery, GetEntitlements, GetEntitlementsState, GraphQLClientHttpError, GetPaywallInput, \
  GetPaywall, GraphQLClientInvalidResponseError, FetchEntitlementQuery, GetEntitlement, UsageMeasurementCreateInput, \
  ReportUsage, ReportUsageInput, GetActiveSubscriptionsInput, GetActiveSubscriptionsList
from stigg._edge_utils import build_get_entitlements_data, build_get_paywall_data, build_get_entitlement_data, build_get_subscriptions_data, build_get_entitlements_state_data

PRODUCTION_API_URL = "https://api.stigg.io/graphql"
PRODUCTION_EDGE_API_URL = "https://edge.api.stigg.io"

DEFAULT_REQUEST_TIMEOUT = Timeout(timeout=30.0)

STIGG_REQUESTS_RETRY_COUNT = 3
HTTP_TRANSPORT_RETRY_COUNT = 5

RETRY_KWARGS = {
    "retry": (
        retry_if_exception_type(GraphQLClientHttpError) | retry_if_exception_type(GraphQLClientInvalidResponseError)
    ),
    "stop": stop_after_attempt(STIGG_REQUESTS_RETRY_COUNT),
    "reraise": True,
}

X_GRAPHQL_OPERATION_NAME = 'x-graphql-operation-name'

class StiggClient(Client):
    def __init__(self, enable_edge: bool, edge_api_url: str, *args, **kwargs):
        self.enable_edge = enable_edge
        self.edge_api_url = edge_api_url

        super().__init__(*args, **kwargs)

    def execute(
        self,
        query: str,
        operation_name: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> httpx.Response:
      headers = kwargs.get("headers", {})
      headers[X_GRAPHQL_OPERATION_NAME] = operation_name
      kwargs['headers'] = headers

      return super().execute(query, operation_name, variables, **kwargs)

    @retry(**RETRY_KWARGS)
    def get_data(self,  *args, **kwargs):
        return super().get_data(*args, **kwargs)

    def get_entitlement(self, input: FetchEntitlementQuery, **kwargs: Any) -> GetEntitlement:
        if self.enable_edge is False:
            return super().get_entitlement(input, **kwargs)

        url, params = build_get_entitlement_data(self.edge_api_url, input)

        response = self.http_client.get(url=url, params=params, **kwargs)
        data = self.get_data(response)
        return GetEntitlement.model_validate(data)

    def get_entitlements(self, query: FetchEntitlementsQuery, **kwargs: Any) -> GetEntitlements:
        if self.enable_edge is False:
            return super().get_entitlements(query, **kwargs)

        url, params = build_get_entitlements_data(self.edge_api_url, query)
        response = self.http_client.get(url=url, params=params, **kwargs)
        data = self.get_data(response)
        return GetEntitlements.model_validate(data)

    def get_entitlements_state(self, query: FetchEntitlementsQuery, **kwargs: Any) -> GetEntitlementsState:
        if self.enable_edge is False:
            return super().get_entitlements_state(query, **kwargs)

        url, params = build_get_entitlements_state_data(self.edge_api_url, query)
        response = self.http_client.get(url=url, params=params, **kwargs)
        data = self.get_data(response)
        return GetEntitlementsState.model_validate(data)

    def get_active_subscriptions_list(self, input: GetActiveSubscriptionsInput, **kwargs: Any) -> GetActiveSubscriptionsList:
        if self.enable_edge is False:
            return super().get_active_subscriptions_list(input, **kwargs)

        url, params = build_get_subscriptions_data(self.edge_api_url, input)

        response = self.http_client.get(url=url, params=params, **kwargs)
        data = self.get_data(response)
        return GetActiveSubscriptionsList.model_validate(data)

    def get_paywall(self, input: GetPaywallInput, **kwargs: Any) -> GetPaywall:
        if input.customer_id is not None or self.enable_edge is False:
            return super().get_paywall(input, **kwargs)

        url, params = build_get_paywall_data(self.edge_api_url, input)

        response = self.http_client.get(url=url, params=params, **kwargs)
        data = self.get_data(response)
        return GetPaywall.model_validate(data)

    def report_usage(self, input: Union[UsageMeasurementCreateInput, ReportUsageInput], **kwargs: Any) -> ReportUsage:
      return super().report_usage(input, **kwargs)


class AsyncStiggClient(AsyncClient):
    def __init__(self, enable_edge: bool, edge_api_url: str, *args, **kwargs):
        self.enable_edge = enable_edge
        self.edge_api_url = edge_api_url

        super().__init__(*args, **kwargs)

    def execute(
        self,
        query: str,
        operation_name: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> httpx.Response:
      headers = kwargs.get("headers", {})
      headers[X_GRAPHQL_OPERATION_NAME] = operation_name
      kwargs['headers'] = headers

      return super().execute(query, operation_name, variables, **kwargs)


    @retry(**RETRY_KWARGS)
    def get_data(self,  *args, **kwargs):
        return super().get_data(*args, **kwargs)

    async def get_entitlement(self, input: FetchEntitlementQuery, **kwargs: Any) -> GetEntitlement:
        if self.enable_edge is False:
            return await super().get_entitlement(input, **kwargs)

        url, params = build_get_entitlement_data(self.edge_api_url, input)

        response = await self.http_client.get(url=url, params=params, **kwargs)
        data = self.get_data(response)
        return GetEntitlement.model_validate(data)

    async def get_entitlements(self, query: FetchEntitlementsQuery, **kwargs: Any) -> GetEntitlements:
        if self.enable_edge is False:
            return await super().get_entitlements(query, **kwargs)

        url, params = build_get_entitlements_data(self.edge_api_url, query)

        response = await self.http_client.get(url=url, params=params, **kwargs)
        data = self.get_data(response)
        return GetEntitlements.model_validate(data)

    async def get_entitlements_state(self, query: FetchEntitlementsQuery, **kwargs: Any) -> GetEntitlementsState:
        if self.enable_edge is False:
            return await super().get_entitlements_state(query, **kwargs)

        url, params = build_get_entitlements_state_data(self.edge_api_url, query)

        response = await self.http_client.get(url=url, params=params, **kwargs)
        data = self.get_data(response)
        return GetEntitlementsState.model_validate(data)

    async def get_active_subscriptions_list(self, input: GetActiveSubscriptionsInput, **kwargs: Any) -> GetActiveSubscriptionsList:
        if self.enable_edge is False:
            return await super().get_active_subscriptions_list(input, **kwargs)

        url, params = build_get_subscriptions_data(self.edge_api_url, input)

        response = await self.http_client.get(url=url, params=params, **kwargs)
        data = self.get_data(response)
        return GetActiveSubscriptionsList.model_validate(data)

    async def get_paywall(self, input: GetPaywallInput, **kwargs: Any) -> GetPaywall:
        if input.customer_id is not None or self.enable_edge is False:
            return await super().get_paywall(input, **kwargs)

        url, params = build_get_paywall_data(self.edge_api_url, input)

        response = await self.http_client.get(url=url, params=params, **kwargs)
        data = self.get_data(response)
        return GetPaywall.model_validate(data)

    async def report_usage(self, input: Union[UsageMeasurementCreateInput, ReportUsageInput], **kwargs: Any) -> ReportUsage:
        return await super().report_usage(input, **kwargs)


def get_headers(api_key: str):
    return {"X-API-KEY": api_key, "X-API-VERSION": "1", "Content-Type": "application/json"}


class Stigg:
    @staticmethod
    def create_client(
        api_key: str,
        api_url: str = PRODUCTION_API_URL,
        enable_edge: bool = True,
        edge_api_url: str = PRODUCTION_EDGE_API_URL,
    ) -> StiggClient:
        headers = get_headers(api_key)
        transport = httpx.HTTPTransport(retries=HTTP_TRANSPORT_RETRY_COUNT)
        http_client = httpx.Client(
            headers=headers,
            timeout=DEFAULT_REQUEST_TIMEOUT,
            transport=transport
        )
        return StiggClient(
            enable_edge=enable_edge,
            edge_api_url=edge_api_url,
            url=api_url,
            headers=headers,
            http_client=http_client,
        )

    @staticmethod
    def create_async_client(
        api_key: str,
        api_url: str = PRODUCTION_API_URL,
        enable_edge: bool = True,
        edge_api_url: str = PRODUCTION_EDGE_API_URL,
    ) -> AsyncStiggClient:
        headers = get_headers(api_key)
        transport = httpx.AsyncHTTPTransport(retries=HTTP_TRANSPORT_RETRY_COUNT)
        http_client = httpx.AsyncClient(
            headers=headers,
            timeout=DEFAULT_REQUEST_TIMEOUT,
            transport=transport,
        )
        return AsyncStiggClient(
            enable_edge=enable_edge,
            edge_api_url=edge_api_url,
            url=api_url,
            headers=headers,
            http_client=http_client,
        )
