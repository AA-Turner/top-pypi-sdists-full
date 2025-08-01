# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import requests

from .base_ts_message import BaseTsMessage


class AgentConnection(BaseTsMessage):
    def __init__(self):
        super().__init__()
        self.base_url = f"{self.settings.api_url}/agents/v1.0/"

    @property
    def name(self):
        return "connection"

    @property
    def path(self):
        return "agents/connection"

    @property
    def request_method(self):
        return requests.get

    @property
    def expected_response_codes(self):
        return [204]

    def process_response(self, response, reporting_client):
        """This endpoint doesn't have a response body, so there's nothing to process."""
