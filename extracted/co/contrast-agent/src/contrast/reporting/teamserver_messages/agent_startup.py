# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

import requests

from contrast import get_canonical_version
from contrast.utils.decorators import fail_loudly

from .base_ts_message import BaseTsAppMessage, b64url_stripped


class AgentStartup(BaseTsAppMessage):
    def __init__(self):
        super().__init__()
        self.base_url = f"{self.settings.api_url}/agents/v1.0/"
        self.app_path_b64 = b64url_stripped(self.settings.app_path)

        self.body = {"version": get_canonical_version()}

        if code := self.settings.config.app_code:
            self.body["application_code"] = code

        if group := self.settings.config.app_group:
            self.body["application_group"] = group

        if metadata := self.settings.config.app_metadata:
            self.body["application_metadata"] = metadata

        if application_tags := self.settings.config.app_tags:
            self.body["application_tags"] = application_tags

        if environment := self.settings.config.get("server.environment"):
            self.body["server_environment"] = environment

        if server_tags := self.settings.config.get("server.tags"):
            self.body["server_tags"] = server_tags

        if session_id := self.settings.config.session_id:
            self.body["session_id"] = session_id
        elif session_metadata := self.settings.config.get_session_metadata():
            self.body["session_metadata"] = session_metadata

    @property
    def name(self) -> str:
        return "agent-startup"

    @property
    def path(self) -> str:
        return "/".join(
            [
                "agents",
                self.server_name_b64,
                self.server_path_b64,
                self.server_type_b64,
                self.app_language_b64,
                self.app_name_b64,
                self.app_path_b64,
                "startup",
            ]
        )

    @property
    def expected_response_codes(self) -> list[int]:
        return [200]

    @property
    def request_method(self):
        return requests.put

    @property
    def disable_agent_on_401_and_408(self) -> bool:
        return True

    @fail_loudly("Failed to process AgentStartup response")
    def process_response(self, response, reporting_client):
        if not self.process_response_code(response, reporting_client):
            return

        if last_modified := response.headers.get("Last-Modified", None):
            self.settings.app_settings_last_modified = last_modified
