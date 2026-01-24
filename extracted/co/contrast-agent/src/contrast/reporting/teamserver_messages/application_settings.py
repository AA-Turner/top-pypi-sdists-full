# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

import requests

from contrast.utils.decorators import fail_loudly

from .base_ts_message import BaseTsAppMessage


class ApplicationSettings(BaseTsAppMessage):
    def __init__(self):
        super().__init__()
        self.base_url = f"{self.settings.api_url}/agents/v1.0/"
        self.extra_headers["If-Modified-Since"] = (
            self.settings.app_settings_last_modified
        )
        self.body = ""

    @property
    def name(self):
        return "application-settings"

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
                "settings",
            ]
        )

    @property
    def expected_response_codes(self) -> list[int]:
        return [200]

    @property
    def request_method(self):
        return requests.get

    @fail_loudly("Failed to process ApplicationSettings response")
    def process_response(self, response, reporting_client):
        if not self.process_response_code(response, reporting_client):
            return

        body = response.json()
        last_modified = response.headers.get("Last-Modified", None)

        self.settings.apply_application_settings(body, last_modified)
        self.settings.log_effective_config()
        if reporting_client is not None and self.settings.is_agent_config_enabled():
            reporting_client.new_effective_config(
                self.settings.generate_effective_config()
            )
