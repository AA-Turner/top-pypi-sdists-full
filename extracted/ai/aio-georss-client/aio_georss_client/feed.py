"""GeoRSS Feed."""

from __future__ import annotations

from abc import ABC, abstractmethod
import asyncio
import codecs
from datetime import datetime
import logging
from pyexpat import ExpatError
from typing import Generic, TypeVar

import aiohttp
from aiohttp import ClientSession, client_exceptions

from .consts import (
    ATTR_ATTRIBUTION,
    DEFAULT_REQUEST_TIMEOUT,
    UPDATE_ERROR,
    UPDATE_OK,
    UPDATE_OK_NO_DATA,
)
from .feed_entry import FeedEntry
from .xml_parser import Feed, XmlParser
from .xml_parser.feed_item import FeedItem

_LOGGER = logging.getLogger(__name__)

T_FEED_ENTRY = TypeVar("T_FEED_ENTRY", bound=FeedEntry)


class GeoRssFeed(Generic[T_FEED_ENTRY], ABC):
    """GeoRSS feed base class."""

    def __init__(
        self,
        websession: ClientSession,
        home_coordinates: tuple[float, float],
        url: str,
        filter_radius: float | None = None,
        filter_categories: list[str] | None = None,
    ):
        """Initialise this service."""
        self._websession = websession
        self._home_coordinates: tuple[float, float] = home_coordinates
        self._filter_radius: float | None = filter_radius
        self._filter_categories: list[str] | None = filter_categories
        self._url: str = url
        self._last_timestamp: datetime | None = None

    def __repr__(self):
        """Return string representation of this feed."""
        return f"<{self.__class__.__name__}(home={self._home_coordinates}, url={self._url}, radius={self._filter_radius}, categories={self._filter_categories})>"

    @abstractmethod
    def _new_entry(
        self,
        home_coordinates: tuple[float, float],
        rss_entry: FeedItem,
        global_data: dict,
    ) -> T_FEED_ENTRY:
        """Generate a new entry."""

    def _client_session_timeout(self) -> int:
        """Define client session timeout in seconds. Override if necessary."""
        return DEFAULT_REQUEST_TIMEOUT

    def _additional_namespaces(self):
        """Provide additional namespaces, relevant for this feed."""

    async def update(self) -> tuple[str, list[T_FEED_ENTRY] | None]:
        """Update from external source and return filtered entries."""
        status, rss_data = await self._fetch()
        if status == UPDATE_OK:
            if rss_data:
                global_data = self._extract_from_feed(rss_data)
                # Extract data from feed entries.
                entries: list = [
                    self._new_entry(self._home_coordinates, rss_entry, global_data)
                    for rss_entry in rss_data.entries
                ]
                filtered_entries = self._filter_entries(entries)
                self._last_timestamp = self._extract_last_timestamp(filtered_entries)
                return UPDATE_OK, filtered_entries
            # Should not happen.
            return UPDATE_OK, None
        if status == UPDATE_OK_NO_DATA:
            # Happens for example if the server returns 304
            return UPDATE_OK_NO_DATA, None
        # Error happened while fetching the feed.
        self._last_timestamp = None
        return UPDATE_ERROR, None

    async def _fetch(
        self, method: str = "GET", headers=None, params=None
    ) -> tuple[str, Feed | None]:
        """Fetch GeoRSS data from external source."""
        try:
            timeout = aiohttp.ClientTimeout(total=self._client_session_timeout())
            async with self._websession.request(
                method, self._url, headers=headers, params=params, timeout=timeout
            ) as response:
                try:
                    response.raise_for_status()
                    text = await self._read_response(response)
                    parser = XmlParser(self._additional_namespaces())
                    feed_data = parser.parse(text)
                    self.parser = parser
                    self.feed_data = feed_data
                    return UPDATE_OK, feed_data
                except client_exceptions.ClientError as client_error:
                    _LOGGER.warning(
                        "Fetching data from %s failed with %s", self._url, client_error
                    )
                    return UPDATE_ERROR, None
                except ExpatError as expat_error:
                    _LOGGER.warning(
                        "Parsing data from %s failed with %s", self._url, expat_error
                    )
                    return UPDATE_OK_NO_DATA, None
        except client_exceptions.ClientError as client_error:
            _LOGGER.warning(
                "Requesting data from %s failed with client error: %s",
                self._url,
                client_error,
            )
            return UPDATE_ERROR, None
        except asyncio.TimeoutError:
            _LOGGER.warning(
                "Requesting data from %s failed with timeout error", self._url
            )
            return UPDATE_ERROR, None

    async def _read_response(self, response):
        """Pre-process the response."""
        if response:
            raw_response = await response.read()
            _LOGGER.debug("Response encoding %s", response.get_encoding())
            if raw_response.startswith(codecs.BOM_UTF8):
                return await response.text("utf-8-sig")
            return await response.text()
        return None

    def _filter_entries(self, entries: list[T_FEED_ENTRY]):
        """Filter the provided entries."""
        filtered_entries = entries
        _LOGGER.debug("Entries before filtering %s", filtered_entries)
        # Always remove entries without geometry
        filtered_entries = list(
            filter(
                lambda entry: entry.geometries is not None
                and len(entry.geometries) >= 1,
                filtered_entries,
            )
        )
        # Filter by distance.
        if self._filter_radius:
            filtered_entries = list(
                filter(
                    lambda entry: entry.distance_to_home <= self._filter_radius,
                    filtered_entries,
                )
            )
        # Filter by category.
        if self._filter_categories:
            filtered_entries = list(
                filter(
                    lambda entry: len(
                        {entry.category}.intersection(self._filter_categories)
                    )
                    > 0,
                    filtered_entries,
                )
            )
        _LOGGER.debug("Entries after filtering %s", filtered_entries)
        return filtered_entries

    def _extract_from_feed(self, feed: Feed) -> dict:
        """Extract global metadata from feed."""
        global_data: dict = {}
        author: str | None = feed.author
        if author:
            global_data[ATTR_ATTRIBUTION] = author
        return global_data

    def _extract_last_timestamp(
        self, feed_entries: list[T_FEED_ENTRY]
    ) -> datetime | None:
        """Determine latest (newest) entry from the filtered feed."""
        if feed_entries:
            dates: list[datetime] = sorted(
                [entry.published for entry in feed_entries if entry.published],
                reverse=True,
            )
            if dates:
                last_timestamp: datetime = dates[0]
                _LOGGER.debug("Last timestamp: %s", last_timestamp)
                return last_timestamp
        return None

    @property
    def last_timestamp(self) -> datetime | None:
        """Return the last timestamp extracted from this feed."""
        return self._last_timestamp
