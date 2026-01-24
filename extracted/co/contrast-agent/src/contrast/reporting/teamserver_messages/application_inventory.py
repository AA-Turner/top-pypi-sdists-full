# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from dataclasses import asdict
from contrast_fireball import DiscoveredRoute
import requests

from .base_ts_message import BaseTsAppMessage
from contrast.utils.decorators import fail_loudly
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class ApplicationInventory(BaseTsAppMessage):
    def __init__(self, routes: set[DiscoveredRoute]):
        # This message does not need "Application-Path" header, but it doesn't hurt
        # either.
        super().__init__()
        self.base_url = f"{self.settings.api_url}/agents/v1.1/"

        self.body = {
            "routes": [asdict(route) for route in routes],
        }

        session_id = self.settings.config.session_id
        if session_id:
            self.body.update({"session_id": session_id})

    @property
    def name(self):
        return "application-inventory"

    @property
    def path(self):
        return "/".join(
            [
                "applications",
                self.server_name_b64,
                self.server_path_b64,
                self.server_type_b64,
                self.app_language_b64,
                self.app_name_b64,
                "inventory",
            ]
        )

    @property
    def request_method(self):
        return requests.post

    @fail_loudly("Failed to process ApplicationInventory response")
    def process_response(self, response, reporting_client):
        self.process_response_code(response, reporting_client)
