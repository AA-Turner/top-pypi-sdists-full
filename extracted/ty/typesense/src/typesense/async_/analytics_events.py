"""Client for Analytics events and status operations (async)."""

import sys

if sys.version_info >= (3, 11):
    import typing
else:
    import typing_extensions as typing

from .api_call import AsyncApiCall
from typesense.types.analytics import (
    AnalyticsEvent as AnalyticsEventSchema,
    AnalyticsEventCreateResponse,
    AnalyticsEventsResponse,
    AnalyticsStatus,
)


class AsyncAnalyticsEvents:
    events_path: typing.Final[str] = "/analytics/events"
    flush_path: typing.Final[str] = "/analytics/flush"
    status_path: typing.Final[str] = "/analytics/status"

    def __init__(self, api_call: AsyncApiCall) -> None:
        self.api_call = api_call

    async def create(self, event: AnalyticsEventSchema) -> AnalyticsEventCreateResponse:
        response: AnalyticsEventCreateResponse = await self.api_call.post(
            AsyncAnalyticsEvents.events_path,
            body=event,
            as_json=True,
            entity_type=AnalyticsEventCreateResponse,
        )
        return response

    async def retrieve(
        self,
        *,
        user_id: str,
        name: str,
        n: int,
    ) -> AnalyticsEventsResponse:
        params: typing.Dict[str, typing.Union[str, int]] = {
            "user_id": user_id,
            "name": name,
            "n": n,
        }
        response: AnalyticsEventsResponse = await self.api_call.get(
            AsyncAnalyticsEvents.events_path,
            params=params,
            as_json=True,
            entity_type=AnalyticsEventsResponse,
        )
        return response

    async def flush(self) -> AnalyticsEventCreateResponse:
        response: AnalyticsEventCreateResponse = await self.api_call.post(
            AsyncAnalyticsEvents.flush_path,
            body={},
            as_json=True,
            entity_type=AnalyticsEventCreateResponse,
        )
        return response

    async def status(self) -> AnalyticsStatus:
        response: AnalyticsStatus = await self.api_call.get(
            AsyncAnalyticsEvents.status_path,
            as_json=True,
            entity_type=AnalyticsStatus,
        )
        return response
