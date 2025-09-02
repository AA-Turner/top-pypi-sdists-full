"""Generic GeoRSS feed."""
from __future__ import annotations

from georss_client import ATTR_ATTRIBUTION, GeoRssFeed

from .feed_entry import GenericFeedEntry


class GenericFeed(GeoRssFeed):
    """Generic GeoRSS feed."""

    def __init__(
        self,
        home_coordinates: tuple[float, float],
        url: str | None,
        filter_radius: float = None,
        filter_categories=None,
    ):
        """Initialise this service."""
        super().__init__(
            home_coordinates,
            url,
            filter_radius=filter_radius,
            filter_categories=filter_categories,
        )

    def _new_entry(
        self, home_coordinates: tuple[float, float], rss_entry, global_data
    ) -> GenericFeedEntry:
        """Generate a new entry."""
        attribution: str = (
            None
            if not global_data and ATTR_ATTRIBUTION not in global_data
            else global_data[ATTR_ATTRIBUTION]
        )
        return GenericFeedEntry(home_coordinates, rss_entry, attribution)
