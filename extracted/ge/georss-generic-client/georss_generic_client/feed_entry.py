"""Generic GeoRSS feed entry."""

from __future__ import annotations

from georss_client import FeedEntry


class GenericFeedEntry(FeedEntry):
    """Generic feed entry."""

    def __init__(
        self, home_coordinates: tuple[float, float], rss_entry, attribution: str
    ):
        """Initialise this service."""
        super().__init__(home_coordinates, rss_entry)
        self._attribution = attribution

    @property
    def attribution(self) -> str:
        """Return the attribution of this entry."""
        return self._attribution
