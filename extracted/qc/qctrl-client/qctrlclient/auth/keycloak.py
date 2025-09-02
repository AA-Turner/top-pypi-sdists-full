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

from .helpers import url_join
from .oidc import OidcUrls


def get_keycloak_oidc_urls(base_url: str, realm: str = "q-ctrl") -> OidcUrls:
    """Returns the OIDC urls for Keycloak."""
    oidc_url = url_join(base_url, f"auth/realms/{realm}/protocol/openid-connect")

    return OidcUrls(
        base_url=base_url,
        token_url=url_join(oidc_url, "token"),
        base_authorization_url=url_join(oidc_url, "auth"),
        user_info_url=url_join(oidc_url, "userinfo"),
    )
