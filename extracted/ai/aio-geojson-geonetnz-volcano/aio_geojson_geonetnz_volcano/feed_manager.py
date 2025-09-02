"""Feed Manager for GeoNet NZ Volcanic Alert Level feed."""

import logging

from aio_geojson_client.consts import UPDATE_ERROR, UPDATE_OK_NO_DATA
from aio_geojson_client.feed_manager import FeedManagerBase
from aiohttp import ClientSession

from .feed import GeonetnzVolcanoFeed

_LOGGER = logging.getLogger(__name__)


class GeonetnzVolcanoFeedManager(FeedManagerBase):
    """Feed Manager for GeoNet NZ Volcanic Alert Level feed."""

    def __init__(
        self,
        websession: ClientSession,
        generate_callback,
        update_callback,
        remove_callback,
        home_coordinates,
        filter_radius=None,
    ):
        """Initialize the GeoNet NZ Volcanic Alert Level Feed Manager."""
        feed = GeonetnzVolcanoFeed(
            websession, home_coordinates, filter_radius=filter_radius
        )
        super().__init__(
            feed, generate_callback, update_callback, remove_callback, None
        )

    async def _store_feed_entries(self, status, feed_entries):
        """Keep a copy of all feed entries for future lookups."""
        if feed_entries:
            external_ids = {entry.external_id: entry for entry in feed_entries}
            # Override existing entries.
            self.feed_entries.update(external_ids)

    async def _update_feed_remove_entries(self, feed_external_ids):
        """Do not remove entities."""
        _LOGGER.debug("Not removing entries %s", feed_external_ids)
        return 0

    async def _status_update(self, status, count_created, count_updated, count_removed):
        """Update entities if feed update did not provide data."""
        if status in (UPDATE_OK_NO_DATA, UPDATE_ERROR) or (
            count_created == 0 and count_updated == 0
        ):
            _LOGGER.debug("Updating entries %s", self._managed_external_ids)
            await self._update_entities(self._managed_external_ids)
