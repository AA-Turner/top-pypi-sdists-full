"""httpx-based Apollo GraphQL and ACR client."""

from __future__ import annotations

import logging

import httpx

from cube_common.config import (
    ACR_TOKEN_URL,
    APOLLO_GRAPHQL_URL,
    APOLLO_GRAPHQL_USER_AGENT,
)

logger = logging.getLogger(__name__)


class ApolloError(Exception):
    """Raised when an Apollo API call fails."""


class ApolloClient:
    """Async client for Apollo GraphQL API and ACR token endpoint."""

    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self._token: str | None = None
        self._http = httpx.AsyncClient(timeout=90)

    async def close(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> ApolloClient:
        return self

    async def __aexit__(self, *exc) -> None:
        await self.close()

    async def get_token(self) -> str:
        """Get an OAuth2 access token from ACR. Caches the token for the session."""
        if self._token:
            return self._token

        resp = await self._http.post(
            ACR_TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
        if resp.status_code != 200:
            raise ApolloError(f"Token request failed ({resp.status_code}): {resp.text}")

        body = resp.json()
        token = body.get("access_token")
        if not token:
            raise ApolloError(f"No access_token in response: {body}")

        self._token = token
        return token

    def clear_token(self) -> None:
        """Clear cached token so the next call fetches a fresh one."""
        self._token = None

    async def graphql(self, query: str, variables: dict | None = None) -> dict:
        """Execute a GraphQL query against Apollo. Returns the 'data' dict.

        Raises ApolloError on HTTP or GraphQL-level errors.
        """
        token = await self.get_token()

        payload: dict = {"query": query}
        if variables:
            payload["variables"] = variables

        resp = await self._http.post(
            APOLLO_GRAPHQL_URL,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
                "Fetch-User-Agent": APOLLO_GRAPHQL_USER_AGENT,
            },
        )

        if resp.status_code != 200:
            raise ApolloError(f"GraphQL request failed ({resp.status_code}): {resp.text}")

        body = resp.json()

        data = body.get("data")

        if "errors" in body:
            parts: list[str] = []
            for e in body["errors"]:
                msg = e.get("message", str(e))
                detail = msg
                if "path" in e:
                    detail += f" (path: {'.'.join(str(p) for p in e['path'])})"
                ext = e.get("extensions") or {}
                if ext:
                    code = ext.get("errorCode") or ext.get("code")
                    name = ext.get("errorName") or ext.get("classification")
                    params = ext.get("parameters")
                    if code:
                        detail += f" [code: {code}]"
                    if name:
                        detail += f" [type: {name}]"
                    if params:
                        detail += f" [details: {params}]"
                parts.append(detail)
            error_summary = "; ".join(parts)

            # GraphQL can return partial data alongside errors (e.g. when
            # some fields are unavailable due to schema version differences).
            # Only raise when there is no usable data at all.
            if data:
                logger.warning("GraphQL partial errors (returning data): %s", error_summary)
            else:
                raise ApolloError(f"GraphQL errors: {error_summary}")

        return data or {}
