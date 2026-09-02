"""
InnoDay CLI API Client

HTTP client wrapper for communicating with the InnoDay API.
"""

import json
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import httpx
from rich.console import Console

console = Console()


class APIError(Exception):
    """API communication error."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict] = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class InnoDayAPIClient:
    """HTTP client for the InnoDay API."""

    def __init__(self, config, timeout: Optional[float] = None):
        """``timeout`` overrides the configured per-request timeout.

        The default suits a read. It does not suit a **sync**, which enumerates a
        whole GitHub organization server-side before it answers: BPAI takes ~32
        seconds, so the 30-second default cut it off every time and the CLI
        reported `Error: ReadTimeout (no message)` -- a message that names neither
        what timed out nor that the work was very nearly done.
        """
        self.config = config
        self.api_base_url = config.get_api_url().rstrip("/")

        org_alias = config.get_current_organization()
        if org_alias:
            org_details = config._config.get("organizations", {}).get(org_alias, {})
            self.organization_id = org_details.get("id")
        else:
            self.organization_id = None

        self.project_id = config.get_current_project_id()

        # What the caller typed/resolved, alias or id. Kept so the client can
        # resolve an org alias to a UUID on first use -- see `ensure_org`.
        # `organization_id` above comes from the LOCAL map, which `innoday login`
        # never populates, so on a freshly-authenticated machine it is None and
        # every org-scoped URL silently loses its `/organizations/{id}/` prefix.
        self._org_ref = org_alias
        self._org_resolution_in_flight = False

        self.user_id = config.get_user_id()

        default_headers = {}

        # Identity is the Bearer CLI token (device-flow / PAT) — the only
        # identity the API accepts. X-Team-Secret is still sent when configured:
        # it is a deployment door key, not identity, and is orthogonal.
        cli_token = config.get_cli_token()
        if cli_token:
            default_headers["Authorization"] = f"Bearer {cli_token}"

        team_secret = config.get_team_secret()
        if team_secret:
            default_headers["X-Team-Secret"] = team_secret

        self.api_client = httpx.AsyncClient(
            timeout=httpx.Timeout(
                timeout if timeout is not None else config.get_api_timeout()
            ),
            follow_redirects=True,
            headers=default_headers,
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        await self.api_client.aclose()

    def _build_api_url(self, endpoint: str) -> str:
        """Build full API URL with organization scoping.

        Callers use both conventions — a bare endpoint (`tickets`) and a full
        path (`/api/v1/onboarding/resolve`). The prefix below is applied by
        string concatenation, so a leading slash does NOT make the path
        absolute the way `urljoin` alone would: a full path used to become
        `/api/v1/api/v1/...` and 404. Strip any prefix the caller already
        supplied so both forms resolve to the same URL.
        """
        endpoint = endpoint.lstrip("/")
        for prefix in ("api/v1/",):
            if endpoint.startswith(prefix):
                endpoint = endpoint[len(prefix) :]

        if self.organization_id and (
            endpoint.startswith("tickets") or endpoint.startswith("repositories")
        ):
            endpoint = f"api/v1/organizations/{self.organization_id}/{endpoint}"
        else:
            endpoint = f"api/v1/{endpoint}"
        return urljoin(self.api_base_url + "/", endpoint)

    async def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle HTTP response and errors."""
        try:
            response_data = response.json() if response.content else {}
        except json.JSONDecodeError:
            response_data = {"message": response.text}

        if response.is_success:
            return response_data

        error_message = response_data.get(
            "detail", response_data.get("message", f"HTTP {response.status_code}")
        )

        if response.status_code == 404:
            raise APIError(
                f"Not found: {error_message}", response.status_code, response_data
            )
        elif response.status_code == 401:
            raise APIError(
                f"Unauthorized: {error_message}", response.status_code, response_data
            )
        elif response.status_code == 403:
            raise APIError(
                f"Forbidden: {error_message}", response.status_code, response_data
            )
        elif response.status_code == 422:
            raise APIError(
                f"Validation error: {error_message}",
                response.status_code,
                response_data,
            )
        elif response.status_code >= 500:
            raise APIError(
                f"Server error: {error_message}", response.status_code, response_data
            )
        else:
            raise APIError(
                f"Request failed: {error_message}", response.status_code, response_data
            )

    async def ping_api(self) -> Dict[str, Any]:
        """Test API connectivity."""
        try:
            response = await self.api_client.get(f"{self.api_base_url}/")
            return await self._handle_response(response)
        except httpx.ConnectError:
            raise APIError("Could not connect to API server")
        except httpx.TimeoutException:
            raise APIError("API request timed out")

    async def get_api_health(self) -> Dict[str, Any]:
        """Get API health status.

        `/health` is mounted at the app root, NOT under `/api/v1`. This built
        `_build_api_url("health")` -> `/api/v1/health`, which does not exist and
        answers 401 behind the team-secret middleware, so the method could never
        have worked -- which is why it sat with zero callers while three other
        places re-implemented a `/health` read with raw httpx.
        """
        response = await self.api_client.get(f"{self.api_base_url}/health")
        return await self._handle_response(response)

    async def list_tickets(
        self,
        status: Optional[str] = None,
        assignee: Optional[str] = None,
        all_projects: bool = False,
    ) -> List[Dict[str, Any]]:
        """List tickets, scoped to the current project unless told otherwise.

        `self.project_id` is set by the global `--project` flag or by the
        cwd's `.innoday/project.yml`. Ignoring it meant the org-wide route
        answered every query -- so `--project <id> tickets list` returned all
        of the organization's tickets while looking project-scoped, which is
        the worst shape a wrong answer can take. `tickets create` already
        treats the same value as the ticket's project, so scoping the listing
        to it is the consistent reading.

        Pass all_projects=True for the org-wide list.
        """
        if not self.organization_id:
            raise APIError("Organization ID is required for ticket operations")

        if self.project_id and not all_projects:
            url = self._build_api_url(
                f"organizations/{self.organization_id}"
                f"/projects/{self.project_id}/tickets"
            )
        else:
            url = self._build_api_url("tickets")
        params = {}
        if status:
            params["status"] = status.lower().replace("_", " ")
        if assignee:
            params["assignee"] = assignee

        response = await self.api_client.get(url, params=params)
        return await self._handle_response(response)

    async def get_ticket(self, ticket_id: str) -> Dict[str, Any]:
        """Get a specific ticket by ID."""
        if not self.organization_id:
            raise APIError("Organization ID is required for ticket operations")

        url = self._build_api_url(f"tickets/{ticket_id}")
        response = await self.api_client.get(url)
        return await self._handle_response(response)

    async def create_ticket(self, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new ticket."""
        if not self.organization_id:
            raise APIError("Organization ID is required for ticket operations")

        if "status" in ticket_data and ticket_data["status"]:
            ticket_data = {
                **ticket_data,
                "status": ticket_data["status"].lower().replace("_", " "),
            }

        url = self._build_api_url("tickets")
        response = await self.api_client.post(url, json=ticket_data)
        return await self._handle_response(response)

    async def update_ticket(
        self, ticket_id: str, ticket_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing ticket."""
        if not self.organization_id:
            raise APIError("Organization ID is required for ticket operations")

        if "status" in ticket_data and ticket_data["status"]:
            ticket_data = {
                **ticket_data,
                "status": ticket_data["status"].lower().replace("_", " "),
            }

        url = self._build_api_url(f"tickets/{ticket_id}")
        response = await self.api_client.put(url, json=ticket_data)
        return await self._handle_response(response)

    async def cancel_ticket(self, ticket_id: str, note: str) -> Dict[str, Any]:
        """Cancel a ticket. Soft-cancel only -- sets status to CANCELLED and
        records `note` as a comment; never deletes the row. `note` is
        mandatory (see GH #291)."""
        if not self.organization_id:
            raise APIError("Organization ID is required for ticket operations")

        url = self._build_api_url(f"tickets/{ticket_id}/cancel")
        response = await self.api_client.post(url, json={"note": note})
        return await self._handle_response(response)

    async def add_comment(
        self, ticket_id: str, comment_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add a comment to a ticket."""
        if not self.organization_id:
            raise APIError("Organization ID is required for ticket operations")

        url = self._build_api_url(f"tickets/{ticket_id}/comments")
        response = await self.api_client.post(url, json=comment_data)
        return await self._handle_response(response)

    async def get_comments(self, ticket_id: str) -> List[Dict[str, Any]]:
        """Get all comments for a ticket."""
        if not self.organization_id:
            raise APIError("Organization ID is required for ticket operations")

        url = self._build_api_url(f"tickets/{ticket_id}/comments")
        response = await self.api_client.get(url)
        return await self._handle_response(response)

    async def ensure_org(self) -> Optional[str]:
        """Resolve the organization alias to a UUID, once, if it isn't cached.

        Called from the generic verbs rather than from each command, because the
        alternative is the same six-line preamble in ~40 handlers -- and the ones
        that forget it do not error, they emit an unscoped URL.

        Silent on failure: this is a convenience, and the caller's own error
        handling reports an unresolvable org better than a network hiccup raised
        from inside an unrelated request would.
        """
        if self.organization_id or not self._org_ref:
            return self.organization_id
        if self._org_resolution_in_flight:
            # `_resolve_org_id` issues a GET through this same client; without
            # this guard that request would try to resolve the org again.
            return None
        from src.cli.utils.context import _resolve_org_id

        self._org_resolution_in_flight = True
        try:
            self.organization_id = await _resolve_org_id(
                self.config, self, self._org_ref
            )
        except Exception:  # noqa: BLE001 -- best effort, see above
            pass
        finally:
            self._org_resolution_in_flight = False
        return self.organization_id

    async def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> httpx.Response:
        """Generic GET request to API endpoint."""
        await self.ensure_org()
        url = self._build_api_url(endpoint)
        return await self.api_client.get(url, params=params)

    async def post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        """Generic POST request to API endpoint."""
        await self.ensure_org()
        url = self._build_api_url(endpoint)
        return await self.api_client.post(url, json=json, headers=headers)

    async def put(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        """Generic PUT request to API endpoint.

        ``params`` matches :meth:`get` and is not redundant with ``json``: some
        update routes declare their fields as bare ``Optional[...]`` handler
        arguments, which FastAPI binds from the **query string**, not the body
        (``PUT .../projects/{p}/repositories/{r}`` is one). Sending those in
        ``json`` looks right and silently changes nothing.
        """
        await self.ensure_org()
        url = self._build_api_url(endpoint)
        return await self.api_client.put(url, json=json, headers=headers, params=params)

    async def patch(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        """Generic PATCH request to API endpoint."""
        await self.ensure_org()
        url = self._build_api_url(endpoint)
        return await self.api_client.patch(url, json=json, headers=headers)

    async def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        """Generic DELETE request to API endpoint."""
        await self.ensure_org()
        url = self._build_api_url(endpoint)
        return await self.api_client.delete(url, headers=headers)

    def validate_organization_id(self) -> bool:
        return self.organization_id is not None

    def get_base_url(self) -> str:
        return self.api_base_url


async def create_api_client(config) -> InnoDayAPIClient:
    return InnoDayAPIClient(config)
