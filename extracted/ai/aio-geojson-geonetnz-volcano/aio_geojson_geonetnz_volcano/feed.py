"""GeoNet NZ Volcanic Alert Level feed."""

from __future__ import annotations

from datetime import datetime
import logging
from typing import Optional

from aio_geojson_client.feed import GeoJsonFeed
from aiohttp import ClientSession
import pytz

from aio_geojson_geonetnz_volcano.consts import URL

from .feed_entry import GeonetnzVolcanoFeedEntry

_LOGGER = logging.getLogger(__name__)


class GeonetnzVolcanoFeed(GeoJsonFeed):
    """GeoNet NZ Volcanic Alert Level feed."""

    def __init__(self, websession: ClientSession, home_coordinates, filter_radius=None):
        """Initialise this service."""
        super().__init__(websession, home_coordinates, URL, filter_radius=filter_radius)

    def __repr__(self):
        """Return string representation of this feed."""
        return f"<{self.__class__.__name__}(home={self._home_coordinates}, url={self._url}, radius={self._filter_radius})>"

    def _new_entry(self, home_coordinates, feature, global_data):
        """Generate a new entry."""
        return GeonetnzVolcanoFeedEntry(home_coordinates, feature)

    def _now(self):
        """Return now with timezone."""
        return datetime.now(pytz.utc)

    def _extract_last_timestamp(self, feed_entries) -> datetime | None:
        """Extract timestamp. This feed does not provide a timestamp."""
        return None

    def _extract_from_feed(self, feed) -> Optional:
        """Extract global metadata from feed."""
        return None
