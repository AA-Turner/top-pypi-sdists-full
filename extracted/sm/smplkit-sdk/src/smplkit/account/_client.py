"""The Smpl Account client — account-level settings on ``client.account``.

``AccountClient`` / ``AsyncAccountClient`` expose the authenticated account's
own configuration, mirroring the product UI's Account area:

- ``account.settings`` — get/save the account settings object

The settings endpoint isn't JSON:API — its body is a raw JSON object — so the
settings sub-client uses httpx directly rather than going through a generated
client.

The client supports two construction shapes:

* **Wired** into :class:`smplkit.SmplClient` — built from the app base URL and
  api key the top-level client has already resolved. This is the common path.
* **Standalone** — ``AccountClient(api_key=..., base_url=..., ...)`` resolves
  the app base URL itself. There are no pooled transports to tear down (each
  settings call opens and closes its own short-lived httpx client), so
  ``close()`` / ``aclose()`` are no-ops kept for interface symmetry.
"""

from __future__ import annotations

from typing import Any

import httpx

from smplkit._config import _service_url, resolve_client_config
from smplkit._errors import _raise_for_status
from smplkit.account.models import AccountSettings, AsyncAccountSettings


def _check_status(status_code: int, content: bytes) -> None:
    _raise_for_status(int(status_code), content)


def _resolve_account_target(
    *,
    api_key: str | None,
    base_url: str | None,
    profile: str | None,
    base_domain: str | None,
    scheme: str | None,
    debug: bool | None,
    extra_headers: dict[str, str] | None,
) -> tuple[str, str, dict[str, str]]:
    """Resolve the (app_base_url, api_key, extra_headers) for the settings client.

    ``base_url``/``api_key`` are used directly when both are supplied (the
    path the top-level client takes after it has already resolved them);
    otherwise the config resolver fills in whatever is missing.
    """
    cfg = resolve_client_config(
        profile=profile,
        api_key=api_key,
        base_domain=base_domain,
        scheme=scheme,
        debug=debug,
    )
    resolved_key = api_key if api_key is not None else cfg.api_key
    app_url = base_url if base_url is not None else _service_url(cfg.scheme, "app", cfg.base_domain)
    headers: dict[str, str] = {}
    headers.update(cfg.extra_headers or {})
    headers.update(extra_headers or {})
    return app_url.rstrip("/"), resolved_key, headers


class SettingsClient:
    """Sync account-settings get/save (``client.account.settings``).

    The endpoint isn't JSON:API — body is a raw JSON object — so we
    use httpx directly rather than going through a generated client.
    """

    def __init__(self, app_base_url: str, api_key: str, extra_headers: dict[str, str] | None = None) -> None:
        self._base_url = app_base_url
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            **(extra_headers or {}),
        }

    def get(self) -> AccountSettings:
        """Fetch the authenticated account's current settings.

        Returns:
            An :class:`AccountSettings` active record. Mutate its fields and
            call ``save()`` to persist the changes.
        """
        with httpx.Client(base_url=self._base_url, headers=self._headers, timeout=30.0) as h:
            resp = h.get("/api/v1/accounts/current/settings")
        _check_status(resp.status_code, resp.content)
        return AccountSettings(self, data=resp.json() or {})

    def _save(self, data: dict[str, Any]) -> AccountSettings:
        with httpx.Client(base_url=self._base_url, headers=self._headers, timeout=30.0) as h:
            resp = h.put("/api/v1/accounts/current/settings", json=data)
        _check_status(resp.status_code, resp.content)
        return AccountSettings(self, data=resp.json() or {})


class AsyncSettingsClient:
    """Async account-settings get/save (``client.account.settings``).

    The async counterpart of :class:`SettingsClient`; reads and saves
    perform their network round-trips with ``await``.
    """

    def __init__(self, app_base_url: str, api_key: str, extra_headers: dict[str, str] | None = None) -> None:
        self._base_url = app_base_url
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            **(extra_headers or {}),
        }

    async def get(self) -> AsyncAccountSettings:
        """Fetch the authenticated account's current settings.

        Returns:
            An :class:`AsyncAccountSettings` active record. Mutate its fields
            and ``await`` its ``save()`` to persist the changes.
        """
        async with httpx.AsyncClient(base_url=self._base_url, headers=self._headers, timeout=30.0) as h:
            resp = await h.get("/api/v1/accounts/current/settings")
        _check_status(resp.status_code, resp.content)
        return AsyncAccountSettings(self, data=resp.json() or {})

    async def _save(self, data: dict[str, Any]) -> AsyncAccountSettings:
        async with httpx.AsyncClient(base_url=self._base_url, headers=self._headers, timeout=30.0) as h:
            resp = await h.put("/api/v1/accounts/current/settings", json=data)
        _check_status(resp.status_code, resp.content)
        return AsyncAccountSettings(self, data=resp.json() or {})


# ---------------------------------------------------------------------------
# AccountClient (client.account)
# ---------------------------------------------------------------------------


class AccountClient:
    """The Smpl Account client (sync).

    Exposes the authenticated account's own configuration, reachable as
    ``client.account`` (:class:`smplkit.SmplClient`) or constructed directly::

        from smplkit import AccountClient

        with AccountClient(api_key="sk_...") as account:
            settings = account.settings.get()
            settings.environment_order = ["production", "staging"]
            settings.save()

    Sub-client: ``settings`` (get/save). Pure CRUD — no ``install()`` required.

    Args:
        api_key: API key. When omitted, resolved from ``SMPLKIT_API_KEY`` or
            ``~/.smplkit``.
        base_url: Full app-service base URL. Usually resolved from
            ``base_domain``/``scheme``; supplied directly by the top-level
            clients which have already computed it.
        profile: Named ``~/.smplkit`` profile section.
        base_domain: Base domain for API requests (default ``"smplkit.com"``).
        scheme: URL scheme (default ``"https"``).
        debug: Enable SDK debug logging.
        extra_headers: Extra headers attached to every request.
    """

    settings: SettingsClient

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        profile: str | None = None,
        base_domain: str | None = None,
        scheme: str | None = None,
        debug: bool | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        app_url, resolved_key, headers = _resolve_account_target(
            api_key=api_key,
            base_url=base_url,
            profile=profile,
            base_domain=base_domain,
            scheme=scheme,
            debug=debug,
            extra_headers=extra_headers,
        )
        self.settings = SettingsClient(app_url, resolved_key, headers or None)

    def close(self) -> None:
        """No-op — the settings client opens a short-lived httpx client per call."""

    def __enter__(self) -> AccountClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class AsyncAccountClient:
    """The Smpl Account client (async) — counterpart of :class:`AccountClient`.

    Reads and saves perform their network round-trips with ``await``. Pure
    CRUD; no ``install()`` required.

    Args:
        api_key: API key. When omitted, resolved from ``SMPLKIT_API_KEY`` or
            ``~/.smplkit``.
        base_url: Full app-service base URL. Usually resolved from
            ``base_domain``/``scheme``; supplied directly by the top-level
            clients which have already computed it.
        profile: Named ``~/.smplkit`` profile section.
        base_domain: Base domain for API requests (default ``"smplkit.com"``).
        scheme: URL scheme (default ``"https"``).
        debug: Enable SDK debug logging.
        extra_headers: Extra headers attached to every request.
    """

    settings: AsyncSettingsClient

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        profile: str | None = None,
        base_domain: str | None = None,
        scheme: str | None = None,
        debug: bool | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        app_url, resolved_key, headers = _resolve_account_target(
            api_key=api_key,
            base_url=base_url,
            profile=profile,
            base_domain=base_domain,
            scheme=scheme,
            debug=debug,
            extra_headers=extra_headers,
        )
        self.settings = AsyncSettingsClient(app_url, resolved_key, headers or None)

    async def aclose(self) -> None:
        """No-op — the settings client opens a short-lived httpx client per call."""

    async def __aenter__(self) -> AsyncAccountClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.aclose()


# The settings sub-clients are reached through ``client.account.settings``;
# present them as ``smplkit.account.<Name>`` in IDE hover / help() rather
# than the private ``smplkit.account._client`` path.
SettingsClient.__module__ = "smplkit.account"
AsyncSettingsClient.__module__ = "smplkit.account"
