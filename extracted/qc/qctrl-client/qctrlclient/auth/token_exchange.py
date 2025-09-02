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

import requests

from .base import BaseAuth
from .mixins import JwtMixin
from .service_account import ServiceAccountAuth


class TokenExchangeAuth(BaseAuth, JwtMixin):
    """Q-CTRL authentication handler using OIDC token exchange."""

    _REFETCH_THRESHOLD = 60  # seconds

    def __init__(self, base_url: str, client_id: str, client_secret: str, user_id: str):
        self._base_url = base_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._user_id = user_id
        self._access_token: str | None = None

    def _get_access_token(self) -> str:
        if self._access_token is None or self._expires_within(
            self._access_token, self._REFETCH_THRESHOLD
        ):
            self._access_token = self._fetch_access_token()

        return self._access_token

    @cached_property
    def _service_account_auth(self) -> ServiceAccountAuth:
        return ServiceAccountAuth(
            self._base_url, client_id=self._client_id, client_secret=self._client_secret
        )

    def _fetch_access_token(self) -> str:
        token_url = f"{self._base_url}/auth/realms/q-ctrl/protocol/openid-connect/token"

        data = {
            "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
            "subject_token": self._service_account_auth.access_token,
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "requested_subject": self._user_id,
        }
        response = requests.post(url=token_url, data=data, timeout=60)
        data = response.json()
        return data["access_token"]
