"""Stream type classes for tap-aftership."""

from pathlib import Path

import requests
from singer_sdk.pagination import BaseAPIPaginator, BasePageNumberPaginator

from tap_aftership.client import AfterShipStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class TrackingsPaginator(BasePageNumberPaginator):
    """Paginator for the trackings AfterShip stream."""

    def has_more(self, response: requests.Response) -> bool:
        """Check if the trackings endpoint has more pages left."""
        # Only return a next page if this is a successful response with more trackings
        # to process
        response_json = response.json()
        if (
            "data" in response_json
            and "trackings" in response_json["data"]
            and response_json["data"]["trackings"]
            and response.status_code == 200
        ):
            return True
        else:
            return False


class TrackingsStream(AfterShipStream):
    """Define custom stream."""

    name = "trackings"
    path = "/v4/trackings"
    primary_keys = ["id"]
    replication_key = None

    schema_filepath = SCHEMAS_DIR / "tracking.json"
    records_jsonpath = "$.data.trackings[*]"

    def get_new_paginator(self) -> BaseAPIPaginator:
        """Get a new TrackingsPaginator for the trackings API endpoint."""
        return TrackingsPaginator(start_value=1)
