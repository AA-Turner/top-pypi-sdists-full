"""Client for Typesense Analytics module (async)."""

from .analytics_events import AsyncAnalyticsEvents
from .analytics_rules import AsyncAnalyticsRules
from .api_call import AsyncApiCall


class AsyncAnalytics:
    """Client for v30 Analytics endpoints (async)."""

    def __init__(self, api_call: AsyncApiCall) -> None:
        self.api_call = api_call
        self.rules = AsyncAnalyticsRules(api_call)
        self.events = AsyncAnalyticsEvents(api_call)
