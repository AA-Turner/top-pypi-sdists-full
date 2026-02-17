"""Client for Typesense Analytics module (async)."""

from .analytics_events import AnalyticsEvents
from .analytics_rules import AnalyticsRules
from .api_call import ApiCall


class Analytics:
    """Client for v30 Analytics endpoints (async)."""

    def __init__(self, api_call: ApiCall) -> None:
        self.api_call = api_call
        self.rules = AnalyticsRules(api_call)
        self.events = AnalyticsEvents(api_call)
