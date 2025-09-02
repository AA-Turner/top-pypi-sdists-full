"""IGN Sismología feed entry."""
from __future__ import annotations

from datetime import datetime
from typing import Final

import dateparser
from georss_client.consts import CUSTOM_ATTRIBUTE
from georss_client.feed_entry import FeedEntry

ATTRIBUTION: Final = "Instituto Geográfico Nacional"
IMAGE_URL_PATTERN: Final = (
    "http://www.ign.es/web/resources/sismologia/www/"
    "dir_images_terremotos/detalle/{}.gif"
)
REGEXP_ATTR_MAGNITUDE: Final = rf"magnitud (?P<{CUSTOM_ATTRIBUTE}>[^ ]+) "
REGEXP_ATTR_REGION: Final = r"magnitud [^ ]+ en (?P<{}>[A-ZÁÉÓÜÑ0-9 \-\.]+) en".format(
    CUSTOM_ATTRIBUTE
)
REGEXP_ATTR_PUBLISHED_DATE: Final = rf"-Info.terremoto: (?P<{CUSTOM_ATTRIBUTE}>.+)$"
REGEXP_ATTR_SHORT_ID: Final = (
    r"http:\/\/www\.ign\.es\/web\/ign\/portal\/"
    r"sis-catalogo-terremotos\/-\/catalogo-terremotos\/"
    rf"detailTerremoto\?evid=(?P<{CUSTOM_ATTRIBUTE}>\w+)$"
)


class IgnSismologiaFeedEntry(FeedEntry):
    """IGN Sismología feed entry."""

    def __init__(self, home_coordinates: tuple[float, float], rss_entry):
        """Initialise this service."""
        super().__init__(home_coordinates, rss_entry)

    @property
    def attribution(self) -> str:
        """Return the attribution of this entry."""
        return ATTRIBUTION

    @property
    def published(self) -> datetime | None:
        """Return the published date of this entry."""
        published_date = self._search_in_title(REGEXP_ATTR_PUBLISHED_DATE)
        if published_date:
            published_date = dateparser.parse(
                published_date,
                settings={"DATE_ORDER": "DMY", "PREFER_LOCALE_DATE_ORDER": False},
            )
        return published_date

    @property
    def magnitude(self) -> float | float:
        """Return the magnitude of this entry."""
        magnitude = self._search_in_description(REGEXP_ATTR_MAGNITUDE)
        if magnitude:
            magnitude = float(magnitude)
        return magnitude

    @property
    def region(self) -> float | None:
        """Return the region of this entry."""
        return self._search_in_description(REGEXP_ATTR_REGION)

    def _short_id(self) -> str | None:
        """Return the short id of this entry."""
        return self._search_in_external_id(REGEXP_ATTR_SHORT_ID)

    @property
    def image_url(self) -> str | None:
        """Return the image url of this entry."""
        short_id = self._short_id()
        if short_id:
            return IMAGE_URL_PATTERN.format(short_id)
        return None
