"""Shared base class for all external API clients."""

from typing import Any, Dict, Optional

import httpx


class BaseAPIClient:
    """Common foundation for external API clients: httpx helpers.

    It used to also carry `_load_credentials`, which read the CLI's
    `~/.innoday/config.json` plus the OS keyring on behalf of subclasses. Neither
    exists on a deployed server, where the lookup returned `None` *silently* --
    so a server-side credential read through this class could only ever have
    produced an empty result that looked like "not configured". Both callers
    (`GitHubAPI`, `JiraAPI`) were unreachable or armed-but-never-fired; removed in
    #525. Credentials now arrive through each client's constructor, resolved from
    Supabase Vault by the caller.
    """

    def __init__(self, headers: Dict[str, str]):
        self.headers = headers

    async def _get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        auth: Optional[Any] = None,
    ) -> Any:
        async with httpx.AsyncClient() as client:
            kwargs: Dict[str, Any] = {"headers": self.headers, "params": params or {}}
            if auth:
                kwargs["auth"] = auth
            r = await client.get(url, **kwargs)
            if not r.is_success:
                raise Exception(f"GET {url} failed ({r.status_code}): {r.text}")
            return r.json()

    async def _post(
        self,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        auth: Optional[Any] = None,
    ) -> Any:
        async with httpx.AsyncClient() as client:
            kwargs: Dict[str, Any] = {"headers": self.headers, "json": json or {}}
            if auth:
                kwargs["auth"] = auth
            r = await client.post(url, **kwargs)
            if not r.is_success:
                raise Exception(f"POST {url} failed ({r.status_code}): {r.text}")
            return r.json()

    async def _patch(
        self,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        auth: Optional[Any] = None,
    ) -> Any:
        async with httpx.AsyncClient() as client:
            kwargs: Dict[str, Any] = {"headers": self.headers, "json": json or {}}
            if auth:
                kwargs["auth"] = auth
            r = await client.patch(url, **kwargs)
            if not r.is_success:
                raise Exception(f"PATCH {url} failed ({r.status_code}): {r.text}")
            return r.json()
