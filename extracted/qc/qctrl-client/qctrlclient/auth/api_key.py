# Copyright 2025 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.


from __future__ import annotations

from functools import cached_property

from qctrlclient.client import GraphQLClient

from .base import BaseAuth
from .mixins import JwtMixin


class ApiKeyAuth(BaseAuth, JwtMixin):
    """Q-CTRL authentication handler using an API key."""

    _REFETCH_THRESHOLD = 60  # seconds

    def __init__(self, api_url: str, api_key: str):
        self._api_url = api_url
        self._api_key = api_key
        self._access_token: str | None = None

    def _get_access_token(self) -> str:
        if self._access_token is None or self._expires_within(
            self._access_token, self._REFETCH_THRESHOLD
        ):
            self._access_token = self._fetch_access_token()

        return self._access_token

    @cached_property
    def _graphql_client(self) -> GraphQLClient:
        """Returns a client for sending GraphQL requests."""
        return GraphQLClient(self._api_url)

    def _fetch_access_token(self) -> str:
        """Fetches an access token using the API key
        from the API.
        """
        result = self._graphql_client.execute(
            """
            query($apiKey: String!) {
                accessToken(apiKey: $apiKey) {
                    accessToken
                    errors {
                        fields
                        message
                    }
                }
            }
        """,
            {"apiKey": self._api_key},
        )

        return result["accessToken"]["accessToken"]
