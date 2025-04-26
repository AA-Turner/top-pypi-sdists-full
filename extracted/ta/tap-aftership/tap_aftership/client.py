"""REST client handling, including AfterShipStream base class."""

from pathlib import Path
from typing import Any, Dict, Optional

from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.streams import RESTStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class AfterShipStream(RESTStream):
    """AfterShip stream class."""

    url_base = "https://api.aftership.com"
    records_jsonpath = "$[*]"  # Or override `parse_response`.
    next_page_token_jsonpath = "$.data.page"

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object."""
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="aftership-api-key",
            value=str(self.config.get("api_key")),
            location="header",
        )

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        if next_page_token:
            params["page"] = next_page_token
        if "end_date" in self.config:
            params["updated_at_max"] = self.config["end_date"]
        if "start_date" in self.config:
            params["updated_at_min"] = self.config["start_date"]

        return params
