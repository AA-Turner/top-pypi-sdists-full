
from pydantic import BaseModel

class GeoLocation(BaseModel):
    """
    The Geo Location object describes a geographical location, usually associated
    with an IP address
    """

    # Recommended:
    city: str | None = None
    continent: str | None = None
    country: str | None = None

    # Optional:
    coordinates: list[float] | None = None
    desc: str | None = None # The description of the geographical location.
    geohash: str | None = None
    is_on_premises: bool | None = None
    isp: str | None = None
    lat: float | None = None
    long: float | None = None
    postal_code: str | None = None
    provider: str | None = None # The provider of the geographical location data.
    region: str | None = None # The alphanumeric code that identifies the principal subdivision (e.g.
                              # province or state) of the country. Region codes are defined at ISO 3166-2
                              # and have a limit of three characters
                              # For example, see `https://www.iso.org/obp/ui/#iso:code:3166:US` for the
                              # region codes for the US
