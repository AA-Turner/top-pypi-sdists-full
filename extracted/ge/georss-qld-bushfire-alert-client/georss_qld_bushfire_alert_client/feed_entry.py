"""Queensland Bushfire Alert feed entry."""

from __future__ import annotations

from georss_client.consts import CUSTOM_ATTRIBUTE
from georss_client.feed_entry import FeedEntry

REGEXP_ATTR_STATUS = f"Current Status: (?P<{CUSTOM_ATTRIBUTE}>[^<]+)[\n\r]"


class QldBushfireAlertFeedEntry(FeedEntry):
    """Qld Bushfire Alert feed entry."""

    def __init__(self, home_coordinates: tuple[float, float], rss_entry, attribution):
        """Initialise this service."""
        super().__init__(home_coordinates, rss_entry)
        self._attribution = attribution

    @property
    def attribution(self) -> str:
        """Return the attribution of this entry."""
        return self._attribution

    @property
    def status(self) -> str:
        """Return the status of this entry."""
        return self._search_in_description(REGEXP_ATTR_STATUS)
