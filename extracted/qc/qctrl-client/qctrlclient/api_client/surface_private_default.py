# Copyright 2026 Q-CTRL. All rights reserved.
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

from typing import TypeVar

import httpx

from qctrlclient.api_client.shared.surface_client import (
    BaseAuthenticatedClient,
    create_surface_client,
)
from qctrlclient.consistency_headers import TokenCache

TClient = TypeVar("TClient", bound=BaseAuthenticatedClient)
_BASE_URL_ENV_VAR = "QCTRL_API_PRIVATE_DEFAULT_BASE_URL"
_DEFAULT_BASE_URL = "https://api.private.q-ctrl.com"


def create_private_default_client(
    client_class: type[TClient],
    auth: httpx.Auth,
    token_cache: TokenCache,
) -> TClient:
    """
    Create and return a private default surface client instance.

    In most cases, this client should be instantiated in a module and exported, and should use the same TokenCache instance as all other API clients.

    Examples
    --------
    >>> token_cache = SimpleTokenCache()
    >>> public_api_client = create_public_default_client(..., token_cache=token_cache)
    >>> private_api_client = create_private_default_client(..., token_cache=token_cache)
    """
    return create_surface_client(
        client_class=client_class,
        base_url_env_var=_BASE_URL_ENV_VAR,
        default_base_url=_DEFAULT_BASE_URL,
        auth=auth,
        token_cache=token_cache,
    )
