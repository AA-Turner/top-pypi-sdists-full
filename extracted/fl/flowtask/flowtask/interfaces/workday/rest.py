"""Workday REST API client (``/ccx/api``).

Minimal async client for Workday's REST surface, sharing :class:`WorkdayConfig`
(credentials, tenant, prod/sandbox ``env`` selector) with the SOAP
``WorkdayService``. Unlike the WSDL services — which have **no** operation to
read raw time clock events — the REST API exposes them, echoing back the
client-assigned ``Time_Clock_Event_ID`` as ``reference_ID`` and the effective
``timeEntryCode`` applied to *In* events. That makes post-punch verification
possible.

Verified endpoints (Workday implementation tenant, 2026-07-03):

- ``GET /ccx/api/v1/{tenant}/workers?search={text}`` — worker lookup; each row
  carries ``id`` (the Workday WID) and ``descriptor``.
- ``GET /ccx/api/timeTracking/v5/{tenant}/timeClockEvents?worker={WID}`` — raw
  clock events. The ``worker`` parameter **requires a WID**; Employee_ID values
  are rejected with ``400 "not found"``.

Example::

    from flowtask.interfaces.workday.config import WorkdayConfig
    from flowtask.interfaces.workday.rest import WorkdayRestClient

    client = WorkdayRestClient(config=WorkdayConfig(env="sandbox"))
    workers = await client.find_worker("123456")
    events = await client.get_time_clock_events(workers[0]["id"])
"""

from __future__ import annotations

import base64
import logging
import time as _time
from typing import Any, Optional

import httpx

from flowtask.interfaces.workday.config import WorkdayConfig


class WorkdayRestClient:
    """Async client for Workday's ``/ccx/api`` REST endpoints.

    Uses the same OAuth *refresh-token* grant as ``SOAPClient`` (no Redis
    dependency — the bearer token is cached in-memory until shortly before
    expiry). Host and credentials come from :class:`WorkdayConfig`, so the
    ``WORKDAY_ENV`` prod/sandbox selector applies here too.

    Args:
        config: Explicit credentials / tenant. ``None`` → ``WorkdayConfig()``
            (conf fallbacks + ``WORKDAY_ENV``).
        timeout: HTTP timeout in seconds (default 30).
        time_tracking_version: REST version segment for the timeTracking
            service (default ``"v5"`` — the version available on this tenant;
            ``v6`` returned 400 when probed).
    """

    def __init__(
        self,
        *,
        config: WorkdayConfig | None = None,
        timeout: int = 30,
        time_tracking_version: str = "v5",
    ) -> None:
        self.config = config or WorkdayConfig()
        self.timeout = timeout
        self.time_tracking_version = time_tracking_version
        self._token: Optional[str] = None
        self._token_expires_at: float = 0.0
        self._logger = logging.getLogger("flowtask.workday.rest")

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------

    @property
    def base_url(self) -> str:
        """REST base: ``{workday_url}/ccx/api`` (env-aware host)."""
        return f"{self.config.workday_url.rstrip('/')}/ccx/api"

    def set_token(self, token: str, expires_in: int = 300) -> None:
        """Reuse an externally obtained bearer token (e.g. from the SOAP flow).

        Args:
            token: A valid Workday OAuth access token.
            expires_in: Seconds the token remains valid (default 300).
        """
        self._token = token
        self._token_expires_at = _time.monotonic() + max(expires_in - 10, 0)

    async def get_token(self) -> str:
        """Return a cached bearer token, refreshing via OAuth when expired.

        Performs the same ``refresh_token`` grant as ``SOAPClient`` (Basic auth
        with client_id/client_secret against ``token_url``).

        Returns:
            A valid access token.
        """
        if self._token and _time.monotonic() < self._token_expires_at:
            return self._token

        cid = self.config.resolved_client_id
        secret = self.config.resolved_client_secret
        basic = base64.b64encode(f"{cid}:{secret}".encode()).decode()
        async with httpx.AsyncClient(timeout=self.timeout) as http:
            resp = await http.post(
                self.config.resolved_token_url,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.config.resolved_refresh_token,
                },
                headers={
                    "Authorization": f"Basic {basic}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )
            resp.raise_for_status()
            payload = resp.json()

        self.set_token(payload["access_token"], int(payload.get("expires_in", 300)))
        self._logger.debug("Workday REST token refreshed (env=%s)", self.config.resolved_env)
        return self._token  # type: ignore[return-value]

    # ------------------------------------------------------------------
    # Core GET
    # ------------------------------------------------------------------

    async def get(self, path: str, params: dict[str, Any] | None = None) -> dict:
        """Perform an authenticated GET against ``{base_url}{path}``.

        Args:
            path: Path below ``/ccx/api`` (must start with ``/``).
            params: Optional query parameters.

        Returns:
            The parsed JSON body.

        Raises:
            httpx.HTTPStatusError: on non-2xx responses.
        """
        token = await self.get_token()
        url = f"{self.base_url}{path}"
        async with httpx.AsyncClient(timeout=self.timeout) as http:
            resp = await http.get(
                url,
                params=params or {},
                headers={"Authorization": f"Bearer {token}"},
            )
            resp.raise_for_status()
            return resp.json()

    # ------------------------------------------------------------------
    # Endpoints
    # ------------------------------------------------------------------

    async def find_worker(self, search: str, *, limit: int = 20) -> list[dict]:
        """Search workers; each result carries ``id`` (WID) and ``descriptor``.

        Args:
            search: Free-text search (name; associate/employee id support is
                tenant-dependent — verify before relying on it).
            limit: Max results (default 20).

        Returns:
            List of worker dicts (empty when no match).
        """
        payload = await self.get(
            f"/v1/{self.config.tenant}/workers",
            {"search": search, "limit": limit},
        )
        return payload.get("data", [])

    async def get_time_clock_events(
        self, worker_wid: str, *, limit: int = 100
    ) -> list[dict]:
        """Return the raw time clock events of a worker.

        Each event carries ``reference_ID`` (the client-assigned
        ``Time_Clock_Event_ID`` when the event was created via
        ``Put_Time_Clock_Events``), ``dateTime`` (UTC ISO), ``eventType``,
        ``comment``, ``timeZone``, and — on *In* events of time-tracking
        eligible workers — the effective ``timeEntryCode``.

        Args:
            worker_wid: The worker's Workday WID (NOT an Employee_ID — the
                REST API rejects those).
            limit: Max events returned (default 100).

        Returns:
            List of event dicts (empty when the worker has none).
        """
        payload = await self.get(
            f"/timeTracking/{self.time_tracking_version}/{self.config.tenant}/timeClockEvents",
            {"worker": worker_wid, "limit": limit},
        )
        return payload.get("data", [])

    async def find_time_clock_event(
        self, worker_wid: str, reference_id: str
    ) -> dict | None:
        """Locate one clock event by its client-assigned ``reference_ID``.

        Convenience for punch verification: after ``Put_Time_Clock_Events``
        succeeds, the event is visible here within ~1 s (verified live).

        Args:
            worker_wid: The worker's Workday WID.
            reference_id: The ``Time_Clock_Event_ID`` sent on the Put.

        Returns:
            The matching event dict, or ``None`` when not (yet) present.
        """
        for event in await self.get_time_clock_events(worker_wid):
            if event.get("reference_ID") == reference_id:
                return event
        return None
