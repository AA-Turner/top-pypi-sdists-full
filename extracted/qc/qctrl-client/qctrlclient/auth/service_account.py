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

import logging

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from .keycloak import get_keycloak_oidc_urls
from .oidc import OidcSessionAuth, OidcUrls

LOGGER = logging.getLogger(__name__)


class ServiceAccountAuth(OidcSessionAuth):
    """Authentication for service accounts."""

    def __init__(self, base_url: str, client_id: str, client_secret: str):
        self._base_url = base_url
        self._client_id = client_id
        self._client_secret = client_secret
        super().__init__()

    def _get_urls(self) -> OidcUrls:
        return get_keycloak_oidc_urls(self._base_url)

    def _create_session(self) -> OAuth2Session:
        client = BackendApplicationClient(client_id=self._client_id)
        return OAuth2Session(client=client)

    def _authenticate(self) -> None:
        self._oidc_session.fetch_token(
            self._urls.token_url,
            client_id=self._client_id,
            client_secret=self._client_secret,
        )
