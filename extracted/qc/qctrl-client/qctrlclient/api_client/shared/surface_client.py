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

import os
from typing import Any, Protocol, TypeVar

import httpx

from qctrlclient.consistency_headers import HttpxConsistencyHandler, TokenCache

TClient = TypeVar("TClient", bound="BaseAuthenticatedClient")


class BaseAuthenticatedClient(Protocol):
    """Protocol for a base authenticated client."""

    def __init__(
        self,
        base_url: str,
        token: str = "",
        prefix: str = "Bearer",
        auth_header_name: str = "Authorization",
        verify_ssl: bool = True,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> None: ...

    def get_httpx_client(self) -> httpx.Client:
        """Return the synchronous httpx client used for requests."""
        ...

    def get_async_httpx_client(self) -> httpx.AsyncClient:
        """Return the asynchronous httpx client used for requests."""
        ...

    def set_httpx_client(  # noqa: PYI019
        self: TClient, client: httpx.Client
    ) -> TClient:
        """Set the synchronous httpx client used for requests."""
        ...

    def set_async_httpx_client(  # noqa: PYI019
        self: TClient, async_client: httpx.AsyncClient
    ) -> TClient:
        """Set the asynchronous httpx client used for requests."""
        ...


def create_surface_client(
    client_class: type[TClient],
    base_url_env_var: str,
    default_base_url: str,
    auth: httpx.Auth,
    token_cache: TokenCache,
    verify_ssl: bool = True,
) -> TClient:
    """
    Create and return a surface client instance.

    The consistency token is sent on every request and updated from every
    response. Pass the same cache that the service's server middleware uses, so
    a token received on an inbound request is forwarded on gateway calls made
    while handling it.

    The consistency hooks live on the httpx clients installed here. Copies made
    with `with_headers`, `with_cookies` or `with_timeout` (which use
    `attrs.evolve`) and any later `set_httpx_client` / `set_async_httpx_client`
    call replace those clients and drop the hooks.
    """
    base_url = os.getenv(base_url_env_var) or default_base_url

    client = client_class(
        base_url=base_url,
        token="",
        prefix="",
        verify_ssl=verify_ssl,
        httpx_args={"auth": auth},
    )

    handler = HttpxConsistencyHandler(token_cache)

    client_settings: dict[str, Any] = {
        "base_url": base_url,
        "cookies": {},
        "headers": {"Authorization": ""},
        "timeout": None,
        "verify": verify_ssl,
        "follow_redirects": False,
        "auth": auth,
    }
    client.set_httpx_client(
        httpx.Client(**client_settings, event_hooks=handler.as_event_hooks())  # type: ignore[arg-type]
    )
    client.set_async_httpx_client(
        httpx.AsyncClient(
            **client_settings,
            event_hooks=handler.as_async_event_hooks(),  # type: ignore[arg-type]
        )
    )

    return client
