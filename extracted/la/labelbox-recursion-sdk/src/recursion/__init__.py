"""Public entry point for the Recursion Python SDK.

Everything under `recursion_sdk/` is generated from the backend OpenAPI spec by
`yarn generate python-sdk`, including the `Recursion` namespace facade — which
is derived from the same `@SdkRoute(...)` declarations that shape the TypeScript
SDK, so `rl.synthesizers.create(...)` means the same call in both clients.

This module is the only hand-written surface: it wires auth and the base URL, the
same job `packages/sdk-ts/src/index.ts` does for TypeScript. It does not grow as
operations are added.
"""

from __future__ import annotations

from collections.abc import Mapping
from urllib.parse import urlparse

from recursion_sdk.client import AuthenticatedClient
from recursion_sdk.default_base_url import DEFAULT_BASE_URL
from recursion_sdk.facade import Recursion, RecursionApiError

__all__ = ["DEFAULT_BASE_URL", "Recursion", "RecursionApiError", "create_recursion_client"]

def create_recursion_client(
    api_key: str,
    base_url: str = DEFAULT_BASE_URL,
    headers: Mapping[str, str] | None = None,
    timeout_seconds: float | None = None,
) -> Recursion:
    """Construct an authenticated, namespaced client.

    :param api_key: Labelbox API key. Sent as ``Authorization: Bearer <key>``.
    :param base_url: Recursion API base URL. Defaults to the production gateway;
        override it to target staging or a local backend.
    :param headers: Extra headers sent on every request, for callers that need a
        per-request routing header (e.g. ``X-Proxy-Target-Url`` to pin the
        Labelbox Recursion proxy at an ephemeral preview backend). ``Authorization``
        is applied by the client itself and cannot be displaced from here.
    :param timeout_seconds: Per-request timeout. The generator's default is no
        timeout at all, which turns a hung backend into a hung caller.

    Example::

        rl = create_recursion_client(api_key=os.environ["LABELBOX_API_KEY"])
        environment = await rl.environments.get(environment_id)
        job = await rl.synthesizers.create(environment_id, body=body)

    Every non-2xx response raises :class:`recursion_sdk.facade.RecursionApiError`
    — documented in the spec or not — matching the TypeScript client's
    ``throwOnError: true``. Left to itself the generator returns ``None`` for an
    undocumented status and the parsed *error body* for a documented one, either
    of which is easy to mistake for success.
    """
    if not api_key or not api_key.strip():
        raise ValueError("api_key must be a non-empty Labelbox API key.")
    if not urlparse(base_url).hostname:
        raise ValueError(
            f"base_url must include a scheme and host (e.g. https://host); got {base_url!r}."
        )

    client = AuthenticatedClient(
        base_url=base_url,
        token=api_key,
        # Redirects are not followed: a cross-origin hop would otherwise carry the
        # Authorization header to another host. This is the generator's default;
        # it is named here because it is a security property, not an accident.
        follow_redirects=False,
        headers=dict(headers) if headers else {},
        # Deliberately False, which reads backwards. With it True the generated
        # code raises its own `UnexpectedStatus` for any status the spec does not
        # document, *before* the facade sees the response — so a caller following
        # the documented contract and catching `RecursionApiError` would miss
        # exactly the unexpected failures. Left False, every non-2xx reaches
        # `_unwrap`, which raises `RecursionApiError` uniformly whether the status
        # is documented or not. Pinned by a test.
        raise_on_unexpected_status=False,
        timeout=timeout_seconds,
    )
    return Recursion(client)
