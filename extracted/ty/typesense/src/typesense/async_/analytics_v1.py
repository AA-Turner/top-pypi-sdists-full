"""
This module provides async functionality for managing analytics (V1) in Typesense.

Classes:
    - AsyncAnalyticsV1: Handles async operations related to analytics, including access to analytics rules.

Methods:
    - __init__: Initializes the AsyncAnalyticsV1 object.

The AsyncAnalyticsV1 class serves as an entry point for analytics-related operations in Typesense,
currently providing access to AsyncAnalyticsRulesV1.

For more information on analytics, refer to the Analytics & Query Suggestion
[documentation](https://typesense.org/docs/27.0/api/analytics-query-suggestions.html)

This module uses type hinting and is compatible with Python 3.11+ as well as earlier
versions through the use of the typing_extensions library.
"""

from typing_extensions import deprecated

from .analytics_rules_v1 import AsyncAnalyticsRulesV1
from .api_call import AsyncApiCall


@deprecated("AsyncAnalyticsV1 is deprecated on v30+. Use client.analytics instead.")
class AsyncAnalyticsV1(object):
    """
    Class for managing analytics in Typesense (V1) (async).

    This class provides access to analytics-related functionalities,
    currently including operations on analytics rules.

    Attributes:
        rules (AsyncAnalyticsRulesV1): An instance of AsyncAnalyticsRulesV1 for managing analytics rules.
    """

    def __init__(self, api_call: AsyncApiCall) -> None:
        """
        Initialize the AsyncAnalyticsV1 object.

        Args:
            api_call (AsyncApiCall): The API call object for making requests.
        """
        self._rules = AsyncAnalyticsRulesV1(api_call)

    @property
    def rules(self) -> AsyncAnalyticsRulesV1:
        return self._rules
