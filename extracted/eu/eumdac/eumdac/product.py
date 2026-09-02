"""Module containing the Data Store Product class."""

from __future__ import annotations

import re
from contextlib import contextmanager
from datetime import datetime
from functools import total_ordering
from typing import TYPE_CHECKING, Tuple, Dict

from eumdac.request import get
from eumdac.logging import logger

if TYPE_CHECKING:  # pragma: no cover
    import sys
    from typing import IO, Any, Optional

    if sys.version_info < (3, 9):
        from typing import Generator, Mapping, MutableMapping, Pattern, Sequence
    else:
        from collections.abc import Mapping, MutableMapping, Generator, Sequence
        from re import Pattern
    from eumdac.datastore import DataStore
    from eumdac.collection import Collection

from eumdac.errors import EumdacError, eumdac_raise_for_status
import eumdac.common


@total_ordering
class Product:
    """Product of a Collection in the Data Store

    Attributes:
    -----------
    - `datastore`:
        Reference to the Data Store
    - `download_url`:
        URL to the download endpoint of the Data Store

    Arguments:
    ----------
    - `collection_id`:
        Data Store ID of the collection
    - `product_id`:
        Data Store ID of the product
    - `datastore`:
        Reference to the Data Store
    """

    _id: str
    datastore: DataStore
    collection: Collection
    _sensing_start: Optional[datetime] = None
    _sensing_end: Optional[datetime] = None
    _publication_time: Optional[datetime] = None
    _browse_properties: Optional[Mapping[str, Any]] = None
    _download_properties: Optional[Mapping[str, Any]] = None
    _geometry: Optional[Mapping[str, Any]] = None
    _entries: Optional[Sequence[str]] = None
    _extract_filename: Pattern[str] = re.compile(r'filename="(.*?)"')
    _extract_sensing_time: Pattern[str] = re.compile(
        r"(?P<start>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?)?"
        r"\d*Z?[\\/]+"
        r"(?P<end>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?)?"
    )
    _extract_ingestion_time: Pattern[str] = re.compile(
        r"(?P<updated>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?)?"
    )

    def __init__(self, collection_id: str, product_id: str, datastore: DataStore) -> None:
        """
        Init the product from Collection id, Product id, and a Data Store reference
        """
        self._id = product_id
        self.datastore = datastore
        self.collection = self.datastore.get_collection(collection_id)

    def __str__(self) -> str:
        """Return the string representation of the Product id"""
        return str(self._id)

    def __repr__(self) -> str:
        return f"{self.__class__}({self.collection._id}, {self._id})"

    def __eq__(self, other: Any) -> bool:
        """Compare products based on Collection and Product id"""
        return isinstance(other, self.__class__) and (
            self.collection._id,
            self._id,
        ) == (
            other.collection._id,
            other._id,
        )

    def __lt__(self, other: Product) -> bool:
        """Compare products based on Collection and Product id"""
        return (self.collection._id, self._id) < (other.collection._id, other._id)

    def __hash__(self) -> int:
        """Return the hash representation of the product"""
        return hash(repr(self))

    def _parse_browse_properties(
        self, properties: dict[str, str | Any], geometry: Optional[dict[str, Any]]
    ) -> None:
        # Remove collection ID
        properties.pop("parentIdentifier")
        # Bring MD5 to base properties
        if "md5" in properties["extraInformation"]:
            properties.update({"md5": properties["extraInformation"]["md5"]})  # type: ignore
        else:
            properties.update({"md5": None})
        self._browse_properties = properties
        # Handle geometry
        if not geometry or len(geometry) == 0:
            self._geometry = None
        else:
            self._geometry = geometry
        # Handle entries
        self._entries = [link["title"] for link in properties["links"]["sip-entries"]]  # type: ignore

    def _parse_date_properties(self, properties: dict[str, str | Any]) -> None:
        self._parse_sensing_times(properties["date"])
        self._parse_publication_time(properties["updated"])

    def _ensure_properties(self) -> None:
        if self._browse_properties is not None:
            return
        url = self.datastore.urls.get(
            "datastore",
            "browse product",
            vars={"collection_id": self.collection._id, "product_id": self._id},
        )
        auth = self.datastore.token.auth
        response = get(
            url,
            params={"format": "json"},
            auth=auth,
            headers=eumdac.common.headers,
        )
        eumdac_raise_for_status(
            f"Product {self._id} not found in {self.collection._id}",
            response,
            ProductError,
        )

        # DSSHD-658: Better reporting of parsing errors
        try:
            response_json = response.json()
        except Exception as decode_error:
            logger.debug(f"Failed to parse JSON response: {response.text}")
            raise EumdacError(
                "Could not parse response received from server",
                {"response": response.text, "status_code": response.status_code},
            ) from decode_error

        properties = response_json["properties"]
        geometry: Optional[dict[str, Any]] = None
        if "geometry" in response_json:
            geometry = response_json["geometry"]

        self._parse_browse_properties(properties, geometry)

    def _ensure_download_properties(self) -> None:
        if self._download_properties is not None:
            return
        url = self.datastore.urls.get(
            "datastore",
            "download product metadata",
            vars={"collection_id": self.collection._id, "product_id": self._id},
        )
        auth = self.datastore.token.auth
        response = get(
            url,
            params={"format": "json"},
            auth=auth,
            headers=eumdac.common.headers,
        )
        eumdac_raise_for_status(
            f"Product {self._id} not found in {self.collection._id}",
            response,
            ProductError,
        )
        response_data = response.json()
        download_properties = response_data["properties"]
        self._download_properties = download_properties

    def _ensure_sensing_publication_dates(self) -> None:
        """Sensing start date"""
        if self._sensing_start and self._sensing_end:
            return

        self._ensure_properties()
        self._parse_sensing_times(self._browse_properties["date"])  # type: ignore[index]
        self._parse_publication_time(self._browse_properties["updated"])  # type: ignore[index]

    def _parse_sensing_times(self, times_str: str) -> None:
        try:
            sensing_time = self._extract_sensing_time.search(  # type: ignore[union-attr]
                times_str
            ).groupdict()
            # Prepare sensing start
            sensing_start = sensing_time["start"]
            if len(sensing_start) > 19:
                sensing_start = sensing_start.ljust(26, "0")
            self._sensing_start = datetime.fromisoformat(sensing_start)
            # Prepare sensing end
            sensing_end = sensing_time["end"]
            if len(sensing_end) > 19:
                sensing_end = sensing_end.ljust(26, "0")
            self._sensing_end = datetime.fromisoformat(sensing_end)
        except Exception as e:
            raise ProductError(
                f"Couldn't parse sensing times from received value: {times_str}"
            ) from e

    def _parse_publication_time(self, time_str: str) -> None:
        ingestion_time = self._extract_ingestion_time.search(  # type: ignore[union-attr]
            time_str
        ).groupdict()
        ingestion_time = ingestion_time["updated"]
        if len(ingestion_time) > 19:
            ingestion_time = ingestion_time.ljust(26, "0")
        self._publication_time = datetime.fromisoformat(ingestion_time)

    @property
    def sensing_start(self) -> datetime:
        """Sensing start time for the product"""
        self._ensure_sensing_publication_dates()
        return self._sensing_start  # type: ignore

    @property
    def sensing_end(self) -> datetime:
        """Sensing start time for the product"""
        self._ensure_sensing_publication_dates()
        return self._sensing_end  # type: ignore

    @property
    def satellite(self) -> str:
        """Platform or Mission related to the product"""
        self._ensure_properties()
        satellites = [
            acquisition["platform"]["platformShortName"]
            for acquisition in self._browse_properties["acquisitionInformation"]  # type: ignore[index]
        ]
        return ", ".join(satellites)

    @property
    def instrument(self) -> str:
        """Instrument related to the product"""
        self._ensure_properties()
        instruments = [
            acquisition["instrument"]["instrumentShortName"]
            for acquisition in self._browse_properties["acquisitionInformation"]  # type: ignore[index]
        ]
        return ", ".join(instruments)

    @property
    def size(self) -> int:
        """Size of the product"""
        self._ensure_properties()
        return self._browse_properties["productInformation"]["size"]  # type: ignore[index]

    @property
    def acronym(self) -> str:
        """Acronym or Product Type of the product"""
        self._ensure_properties()
        return self._browse_properties["productInformation"]["productType"]  # type: ignore[index]

    @property
    def product_type(self) -> str:
        """Product Type or Acronym of the product"""
        return self.acronym

    @property
    def timeliness(self) -> Optional[str]:
        """Timeliness of the product"""
        self._ensure_properties()
        if "timeliness" in self._browse_properties["productInformation"]:  # type: ignore[index]
            return str(self._browse_properties["productInformation"]["timeliness"])  # type: ignore[index]
        else:
            # Timeliness may not always be in the browse properties, it may be in the download ones
            self._ensure_download_properties()
            if "timeliness" in self._download_properties["productInformation"]:  # type: ignore[index]
                return str(self._download_properties["productInformation"]["timeliness"])  # type: ignore[index]
        return None

    @property
    def md5(self) -> Optional[str]:
        """MD5 checksum of the product SIP"""
        self._ensure_properties()
        return self._browse_properties["md5"]  # type: ignore[index]

    @property
    def processingTime(self) -> Optional[str]:
        """Processing time"""
        self._ensure_download_properties()
        if "processingDate" in self._download_properties["productInformation"]["processingInformation"]:  # type: ignore[index]
            return self._download_properties["productInformation"]["processingInformation"]["processingDate"]  # type: ignore[index]
        return None

    @property
    def processorVersion(self) -> Optional[str]:  # type: ignore[valid-type]
        """Processor version"""
        self._ensure_download_properties()
        if "processorVersion" in self._download_properties["productInformation"]["processingInformation"]:  # type: ignore[index]
            return self._download_properties["productInformation"]["processingInformation"]["processorVersion"]  # type: ignore[index]
        return None

    @property
    def format(self) -> Optional[str]:
        """Format"""
        self._ensure_download_properties()
        if "format" in self._download_properties["productInformation"]["processingInformation"]:  # type: ignore[index]
            return self._download_properties["productInformation"]["processingInformation"]["format"]  # type: ignore[index]
        return None

    @property
    def qualityStatus(self) -> Optional[str]:
        """Quality status"""
        self._ensure_download_properties()
        if "qualityStatus" in self._download_properties["productInformation"]["qualityInformation"]:  # type: ignore[index]
            return self._download_properties["productInformation"]["qualityInformation"]["qualityStatus"]  # type: ignore[index]
        return None

    @property
    def ingested(self) -> Optional[datetime]:
        """Publication time for the product"""
        self._ensure_sensing_publication_dates()
        return self._publication_time  # type: ignore

    @property
    def orbit_type(self) -> str:
        """Orbit Type (GEO/LEO)"""
        self._ensure_download_properties()
        return self._download_properties["acquisitionInformation"][0]["platform"]["orbitType"]  # type: ignore[index]

    @property
    def orbit_is_LEO(self) -> bool:
        """Is Orbit Type LEO?"""
        self._ensure_download_properties()
        return self.orbit_type == "LEO"  # type: ignore[index]

    @property
    def orbit_number(self) -> Optional[int]:
        """Orbit Number of LEO product"""
        self._ensure_properties()
        if "orbitNumber" in self._browse_properties["acquisitionInformation"][0]["acquisitionParameters"]:  # type: ignore[index]
            return self._browse_properties["acquisitionInformation"][0]["acquisitionParameters"]["orbitNumber"]  # type: ignore[index]
        return None

    @property
    def orbit_direction(self) -> Optional[str]:
        """Orbit Direction of LEO product"""
        self._ensure_properties()
        if "orbitDirection" in self._browse_properties["acquisitionInformation"][0]["acquisitionParameters"]:  # type: ignore[index]
            return self._browse_properties["acquisitionInformation"][0]["acquisitionParameters"][  # type: ignore[index]
                "orbitDirection"
            ]
        return None

    @property
    def relative_orbit(self) -> Optional[int]:
        """Relative Orbit Number of LEO product"""
        self._ensure_properties()
        if (
            "relOrbitStart"
            in self._browse_properties["acquisitionInformation"][0]["acquisitionParameters"]  # type: ignore[index]
        ):
            return self._browse_properties["acquisitionInformation"][0]["acquisitionParameters"][  # type: ignore[index]
                "relOrbitStart"
            ]
        elif (
            "relativeOrbitNumber"
            in self._browse_properties["acquisitionInformation"][0]["acquisitionParameters"]  # type: ignore[index]
        ):
            return self._browse_properties["acquisitionInformation"][0]["acquisitionParameters"][  # type: ignore[index]
                "relativeOrbitNumber"
            ]
        else:
            return None

    @property
    def cycle_number(self) -> Optional[int]:
        """Cycle Number of LEO product"""
        self._ensure_properties()
        if (
            "cycleNumber"
            in self._browse_properties["acquisitionInformation"][0]["acquisitionParameters"]  # type: ignore[index]
        ):
            return self._browse_properties["acquisitionInformation"][0]["acquisitionParameters"][  # type: ignore[index]
                "cycleNumber"
            ]
        return None

    @property
    def is_mtg(self) -> bool:
        """Is MTG collection?"""
        self._ensure_download_properties()
        return (
            "mtgCoverage"
            in self._download_properties["acquisitionInformation"][0]["acquisitionParameters"]  # type: ignore[index]
        )

    @property
    def repeat_cycle(self) -> Optional[str]:
        """Repeat cycle number (only for MTG products)"""
        self._ensure_download_properties()
        if (
            self.is_mtg
            and "repeatCycleIdentifier"
            in self._download_properties["acquisitionInformation"][0]["acquisitionParameters"]["mtgCoverage"]  # type: ignore[index]
        ):
            return self._download_properties["acquisitionInformation"][0]["acquisitionParameters"]["mtgCoverage"][  # type: ignore[index]
                "repeatCycleIdentifier"
            ]
        return None

    @property
    def region_coverage(self) -> Optional[str]:
        """Region Coverage (only for MTG products)"""
        self._ensure_download_properties()
        if (
            self.is_mtg
            and "majorRegionCoverage"
            in self._download_properties["acquisitionInformation"][0]["acquisitionParameters"]["mtgCoverage"]  # type: ignore[index]
        ):
            return self._download_properties["acquisitionInformation"][0]["acquisitionParameters"]["mtgCoverage"][  # type: ignore[index]
                "majorRegionCoverage"
            ]
        return None

    @property
    def subregion_identifier(self) -> Optional[str]:
        """Sub-Region (only for MTG products)"""
        self._ensure_download_properties()
        if (
            self.is_mtg
            and "subRegionIdentifier"
            in self._download_properties["acquisitionInformation"][0]["acquisitionParameters"]["mtgCoverage"]  # type: ignore[index]
        ):
            return self._download_properties["acquisitionInformation"][0]["acquisitionParameters"]["mtgCoverage"][  # type: ignore[index]
                "subRegionIdentifier"
            ]
        return None

    @property
    def metadata(self) -> MutableMapping[str, Any]:
        """Product metadata"""
        self._ensure_properties()
        self._ensure_download_properties()
        return {
            "geometry": self._geometry.copy() if self._geometry else None,  # type: ignore
            "properties": self._browse_properties.copy(),  # type: ignore[union-attr]
            "download_properties": self._download_properties.copy(),  # type: ignore[union-attr]
        }

    @property
    def entries(self) -> Sequence[str]:
        """Files inside the product"""
        self._ensure_properties()
        if not self._entries:
            return []
        else:
            return tuple(self._entries)

    @property
    def url(self) -> str:
        """URL of the product"""
        access_token = None
        if hasattr(self.datastore.token, "access_token"):
            access_token = str(self.datastore.token.access_token)

        url = self.datastore.urls.get(
            "datastore",
            "download product",
            vars={"collection_id": self.collection._id, "product_id": self._id},
        )
        download_url = str(url)
        if access_token is not None:
            download_url += "?access_token=" + access_token

        return download_url

    @contextmanager
    def open(
        self,
        entry: Optional[str] = None,
        chunk: Optional[Tuple[int, int]] = None,
        custom_headers: Optional[Dict[str, str]] = None,
    ) -> Generator[IO[bytes], None, None]:
        """Opens a stream to download the product content.

        Note:
            A Data Store product refers to a zip archive containing the data.

        Arguments:
            - `entry` (optional):
                specific file inside the product
            - `chunk` (optional):
                Byte range to download as (start, end). If None, downloads the full content.
            - `custom_headers` (optional):
                Additional HTTP headers to include in the request.

        Yields:
            Generator[IO[bytes]]: Chunks of the downloaded content.
        """
        url = self.datastore.urls.get(
            "datastore",
            "download product",
            vars={"collection_id": self.collection._id, "product_id": self._id},
        )
        auth = self.datastore.token.auth
        params = None
        if entry is not None:
            url += "/entry"
            params = {"name": entry}

        headers = eumdac.common.headers.copy()
        if chunk:
            headers = {**headers, "Range": f"bytes={chunk[0]}-{chunk[1]-1}"}
        if custom_headers:
            headers.update(custom_headers)

        with get(
            url,
            auth=auth,
            params=params,
            stream=True,
            headers=headers,
        ) as response:
            eumdac_raise_for_status(
                f"Could not download Product {self._id} of Collection {self.collection._id}",
                response,
                ProductError,
            )
            if "Content-Disposition" in response.headers:
                match = self._extract_filename.search(response.headers["Content-Disposition"])
                filename = match.group(1)  # type: ignore[union-attr]
            else:
                filename = self.metadata["properties"]["identifier"]
            response.raw.name = filename
            response.raw.decode_content = True
            yield response.raw


class ProductError(EumdacError):
    """Errors related to products"""
