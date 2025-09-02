"""Generic GeoRSS feed manager."""
from __future__ import annotations

from georss_client.feed_manager import FeedManagerBase

from .feed import GenericFeed


class GenericFeedManager(FeedManagerBase):
    """Feed Manager for Generic GeoRSS feed."""

    def __init__(
        self,
        generate_callback,
        update_callback,
        remove_callback,
        coordinates: tuple[float, float],
        url: str | None,
        filter_radius: float = None,
        filter_categories=None,
    ):
        """Initialize the Generic GeoRSS Feed Manager."""
        feed = GenericFeed(
            coordinates,
            url,
            filter_radius=filter_radius,
            filter_categories=filter_categories,
        )
        super().__init__(feed, generate_callback, update_callback, remove_callback)
