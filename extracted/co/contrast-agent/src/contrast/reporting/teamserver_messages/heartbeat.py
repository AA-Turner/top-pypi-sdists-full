# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import requests

from .base_ts_message import BaseTsAppMessage
from contrast.utils.decorators import fail_loudly
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class Heartbeat(BaseTsAppMessage):
    def __init__(self):
        super().__init__()
        self.base_url = f"{self.settings.api_url}/agents/v1.0/"

    @property
    def name(self):
        return "heartbeat"

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
                "heartbeat",
            ]
        )

    @property
    def request_method(self):
        return requests.post

    @fail_loudly("Failed to process Heartbeat response")
    def process_response(self, response, reporting_client):
        """
        This endpoint should only ever return a statuscode and empty body.
        Only in the case of a silencing status code, should we take an action.
        """
        self.process_response_code(response, reporting_client)
