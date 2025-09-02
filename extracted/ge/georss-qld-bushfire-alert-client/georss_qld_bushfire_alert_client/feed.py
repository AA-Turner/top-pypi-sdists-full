"""Queensland Bushfire Alert feed."""

from __future__ import annotations

from typing import Final

from georss_client.consts import ATTR_ATTRIBUTION
from georss_client.feed import GeoRssFeed

from .feed_entry import QldBushfireAlertFeedEntry

# URL as published here: https://www.fire.qld.gov.au/Current-Incidents
URL: Final = "https://publiccontent-gis-psba-qld-gov-au.s3.amazonaws.com/content/Feeds/BushfireCurrentIncidents/bushfireAlert.xml"


class QldBushfireAlertFeed(GeoRssFeed):
    """Qld Bushfire Alert feed."""

    def __init__(
        self,
        home_coordinates: tuple[float, float],
        filter_radius: float | None = None,
        filter_categories: list[str] | None = None,
    ):
        """Initialise this service."""
        super().__init__(home_coordinates, URL, filter_radius=filter_radius)
        self._filter_categories: list[str] | None = filter_categories

    def _new_entry(
        self, home_coordinates: tuple[float, float], rss_entry, global_data
    ) -> QldBushfireAlertFeedEntry:
        """Generate a new entry."""
        attribution = (
            None
            if not global_data and ATTR_ATTRIBUTION not in global_data
            else global_data[ATTR_ATTRIBUTION]
        )
        return QldBushfireAlertFeedEntry(home_coordinates, rss_entry, attribution)

    def _filter_entries(self, entries):
        """Filter the provided entries."""
        entries = super()._filter_entries(entries)
        if self._filter_categories:
            return list(
                filter(lambda entry: entry.category in self._filter_categories, entries)
            )
        return entries
