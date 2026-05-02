"""
Zoom Phone Interface for FlowTask.

Provides a clean, reusable interface to interact with Zoom Phone API.
Handles authentication (with in-memory token cache), automatic 401
retry, binary file downloads, and all major Zoom Phone endpoints.
"""
import asyncio
import logging
import re
import time as _time
import urllib.parse
from email.message import Message
from typing import Optional, Dict, List, Any, Tuple
from datetime import datetime
from abc import ABC
from enum import Enum

import aiohttp
from .http import HTTPService


class CallStatus(Enum):
    """Call status enumeration"""
    ALL = "all"
    ACTIVE = "active"
    MISSED = "missed"
    INCOMING = "incoming"
    OUTGOING = "outgoing"


class RecordingType(Enum):
    """Recording type enumeration"""
    ON_DEMAND = "on_demand"
    AUTOMATIC = "automatic"
    ALL = "all"


class ZoomInterface(HTTPService, ABC):
    """
    Abstract interface for Zoom Phone operations.
    This interface should be implemented by components that interact with Zoom Phone API.

    The implementing class should extend HTTPService (or a similar HTTP client)
    to handle the actual HTTP requests with proper authentication.
    """

    BASE_URL = "https://api.zoom.us/v2"
    AUTH_URL = "https://zoom.us/oauth/token"

    # In-memory token cache
    _cached_token: Optional[str] = None
    _token_expiry: float = 0.0

    async def _ensure_session(self):
        """Ensure aiohttp session exists."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

    # ==========================================
    # Authentication
    # ==========================================

    async def _fetch_token(self) -> Tuple[str, int]:
        """Fetch a fresh OAuth token via Server-to-Server flow.

        Returns:
            Tuple of (access_token, expires_in_seconds).

        Raises:
            ValueError: If credentials are not configured.
            Exception: If the token request fails.
        """
        if not (self.client_id and self.client_secret and self.account_id):
            raise ValueError(
                "Zoom OAuth credentials not provided "
                "(client_id, client_secret, account_id)"
            )

        await self._ensure_session()

        auth = aiohttp.BasicAuth(self.client_id, self.client_secret)
        data = {
            "grant_type": "account_credentials",
            "account_id": self.account_id,
        }

        async with self.session.post(
            self.AUTH_URL, auth=auth, data=data
        ) as resp:
            if resp.status != 200:
                error = await resp.text()
                raise Exception(f"Failed to get access token: {error}")
            result = await resp.json()
            token = result.get("access_token")
            if not token:
                raise Exception("No access_token in Zoom OAuth response")
            return token, int(result.get("expires_in", 3600))

    async def _get_access_token(self) -> str:
        """Get a valid access token, using in-memory cache.

        The token is cached with a 60-second safety margin before
        expiry to avoid mid-request expirations.

        Returns:
            Valid access token string.
        """
        # Return cached token if still valid
        if self._cached_token and _time.time() < self._token_expiry:
            return self._cached_token

        # If the component set access_token directly, trust it
        if (
            hasattr(self, "access_token")
            and self.access_token
            and not self._cached_token
        ):
            self._cached_token = self.access_token
            # Assume 1h validity when set externally
            self._token_expiry = _time.time() + 3540
            return self._cached_token

        # Fetch a fresh token
        token, expires_in = await self._fetch_token()
        self._cached_token = token
        # 60-second buffer so we refresh before actual expiry
        self._token_expiry = _time.time() + expires_in - 60
        # Also propagate to the legacy attribute
        if hasattr(self, "access_token"):
            self.access_token = token
        return token

    async def _refresh_token(self) -> str:
        """Force-refresh the token (e.g. after a 401).

        Returns:
            New access token.
        """
        self._cached_token = None
        self._token_expiry = 0.0
        return await self._get_access_token()

    # ==========================================
    # Core HTTP
    # ==========================================

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        raw_response: bool = False,
        _retried: bool = False,
        _attempt: int = 0,
        **kwargs,
    ) -> Any:
        """Make an HTTP request to the Zoom API.

        Automatically retries:
        - **Once** on HTTP 401 by refreshing the access token.
        - **Up to 5 times** on HTTP 429 (rate limit) with exponential
          backoff.  Respects the ``Retry-After`` header when present.

        Args:
            method: HTTP method (GET, POST, etc.).
            endpoint: API endpoint path or full URL.
            params: Query parameters.
            json_data: JSON body.
            raw_response: Return raw bytes instead of JSON.
            _retried: Internal flag — prevents infinite 401 retry loops.
            _attempt: Internal counter for 429 backoff (0-indexed).
            **kwargs: Additional arguments (ignored).

        Returns:
            Parsed JSON dict or raw bytes.

        Raises:
            Exception: On non-recoverable API errors.
        """
        await self._ensure_session()
        token = await self._get_access_token()

        # Build full URL
        url = endpoint if endpoint.startswith("http") else f"{self.BASE_URL}{endpoint}"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        timeout = aiohttp.ClientTimeout(
            total=getattr(self, "timeout", 30)
        )

        async with self.session.request(
            method,
            url,
            params=params,
            json=json_data,
            headers=headers,
            timeout=timeout,
        ) as resp:
            # ── 401 retry (token refresh) ──────────────────────────────────
            if resp.status == 401 and not _retried:
                await self._refresh_token()
                return await self._make_request(
                    method,
                    endpoint,
                    params=params,
                    json_data=json_data,
                    raw_response=raw_response,
                    _retried=True,
                    _attempt=_attempt,
                )

            # ── 429 retry (rate limit, exponential backoff) ────────────────
            if resp.status == 429:
                max_attempts = 5
                if _attempt >= max_attempts:
                    error = await resp.text()
                    raise Exception(
                        f"Zoom API error ({resp.status}): {error}"
                    )
                # Honor Retry-After if Zoom sends it, otherwise back off
                retry_after = resp.headers.get("Retry-After")
                if retry_after:
                    wait = float(retry_after)
                else:
                    wait = min(2 ** _attempt, 32)   # 1, 2, 4, 8, 16, 32 s
                self._logger.warning(
                    f"⏳ Zoom 429 rate limit — waiting {wait:.1f}s "
                    f"(attempt {_attempt + 1}/{max_attempts})"
                )
                await asyncio.sleep(wait)
                return await self._make_request(
                    method,
                    endpoint,
                    params=params,
                    json_data=json_data,
                    raw_response=raw_response,
                    _retried=_retried,
                    _attempt=_attempt + 1,
                )

            # ── Other errors ───────────────────────────────────────────────
            if resp.status >= 400:
                error = await resp.text()
                raise Exception(
                    f"Zoom API error ({resp.status}): {error}"
                )

            if raw_response:
                return await resp.read()

            return await resp.json()

    # ==========================================
    # Binary Download
    # ==========================================

    async def download_binary(
        self,
        url: str,
        timeout_read: int = 120,
    ) -> Tuple[bytes, str, str]:
        """Download a binary file from Zoom with authentication.

        Follows redirects, extracts the filename from the
        ``Content-Disposition`` header (with UTF-8 support) and falls
        back to URL query parameters.

        Args:
            url: Full download URL.
            timeout_read: Read timeout in seconds (default 120).

        Returns:
            Tuple of ``(content_bytes, content_type, filename)``.

        Raises:
            Exception: If the download fails or returns an error.
        """
        await self._ensure_session()
        token = await self._get_access_token()

        headers = {"Authorization": f"Bearer {token}"}

        timeout = aiohttp.ClientTimeout(
            total=timeout_read + 60,
            connect=10,
            sock_read=timeout_read,
        )

        async with self.session.get(
            url,
            headers=headers,
            timeout=timeout,
            allow_redirects=True,
        ) as resp:
            if resp.status == 401:
                # Retry once with fresh token
                token = await self._refresh_token()
                headers = {"Authorization": f"Bearer {token}"}
                async with self.session.get(
                    url,
                    headers=headers,
                    timeout=timeout,
                    allow_redirects=True,
                ) as retry_resp:
                    retry_resp.raise_for_status()
                    content = await retry_resp.read()
                    content_type = retry_resp.headers.get(
                        "Content-Type", "application/octet-stream"
                    )
                    filename = self._extract_filename(
                        retry_resp, fallback="download"
                    )
                    return content, content_type, filename

            if resp.status >= 400:
                error = await resp.text()
                raise Exception(
                    f"Download failed ({resp.status}): {error[:300]}"
                )

            content = await resp.read()
            content_type = resp.headers.get(
                "Content-Type", "application/octet-stream"
            )
            filename = self._extract_filename(resp, fallback="download")
            return content, content_type, filename

    @staticmethod
    def _extract_filename(
        resp: aiohttp.ClientResponse, fallback: str = "download"
    ) -> str:
        """Extract filename from response headers or URL.

        Args:
            resp: aiohttp response object.
            fallback: Fallback filename if none found.

        Returns:
            Extracted or fallback filename.
        """
        content_disposition = resp.headers.get("Content-Disposition", "")

        if content_disposition:
            msg = Message()
            msg["Content-Disposition"] = content_disposition

            # Try RFC 5987 filename*=UTF-8'' first
            utf8_fn = msg.get_param(
                "filename*", header="Content-Disposition"
            )
            if utf8_fn and "''" in str(utf8_fn):
                _, enc_name = str(utf8_fn).split("''", 1)
                return urllib.parse.unquote(enc_name)

            # Standard filename param
            filename = msg.get_param(
                "filename", header="Content-Disposition"
            )
            if filename:
                return str(filename)

        # Try URL query param ?filename=...
        try:
            q = urllib.parse.parse_qs(
                urllib.parse.urlparse(str(resp.url)).query
            )
            if "filename" in q and q["filename"]:
                return q["filename"][0]
        except Exception:
            pass

        return fallback

    async def close(self):
        """Close the HTTP session"""
        if self.session and not self.session.closed:
            await self.session.close()

    async def __aenter__(self):
        """Async context manager entry"""
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()

    async def get_call_metadata_by_extension(
        self,
        extension_number: str,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        page_size: int = 30,
        next_page_token: Optional[str] = None,
        call_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Download call metadata by extension number.

        Args:
            extension_number: The extension number to query
            from_date: Start date for call history
            to_date: End date for call history
            page_size: Number of records per page (max 100)
            next_page_token: Token for pagination
            call_type: Filter by call type (incoming, outgoing, missed, etc.)

        Returns:
            Call metadata including call logs, durations, participants, etc.
        """
        params = {
            "page_size": min(page_size, 100),
            "extension_number": extension_number
        }

        if from_date:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date:
            params["to"] = to_date.strftime("%Y-%m-%d")
        if next_page_token:
            params["next_page_token"] = next_page_token
        if call_type:
            params["type"] = call_type

        return await self._make_request("GET", "/phone/call_history", params=params)

    async def get_call_by_id(self, call_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific call.

        Args:
            call_id: The unique call identifier

        Returns:
            Detailed call information
        """
        return await self._make_request("GET", f"/phone/call_history/{call_id}")

    async def get_call_logs(
        self,
        from_date: str,
        to_date: str,
        page_size: int = 100,
        next_page_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get general call logs for the entire account.

        Unlike ``get_call_metadata_by_extension`` this uses the
        ``/phone/call_logs`` endpoint which returns logs across all
        extensions.

        Args:
            from_date: Start date in ``YYYY-MM-DD`` format.
            to_date: End date in ``YYYY-MM-DD`` format.
            page_size: Number of records per page (max 100).
            next_page_token: Token for pagination.

        Returns:
            Dict with ``call_logs`` list and pagination info.
        """
        params = {
            "from": from_date,
            "to": to_date,
            "page_size": min(page_size, 100),
        }

        if next_page_token:
            params["next_page_token"] = next_page_token

        return await self._make_request("GET", "/phone/call_logs", params=params)

    async def get_user_id_by_extension(self, extension_number: str) -> Optional[str]:
        """Resolve a Zoom Phone extension number to its Zoom user ID.

        Paginates ``/phone/users`` until a user whose ``extension_number``
        matches is found.  Returns ``None`` if the extension is not found.

        Args:
            extension_number: The extension string to look up (e.g. ``"431"``).

        Returns:
            Zoom user ID string, or ``None`` if not found.
        """
        ext_target = str(extension_number).strip()
        next_page_token: Optional[str] = None

        while True:
            params: Dict[str, Any] = {"page_size": 100}
            if next_page_token:
                params["next_page_token"] = next_page_token

            data = await self._make_request("GET", "/phone/users", params=params)

            for user in data.get("users", []):
                raw_ext = user.get("extension_number")
                if raw_ext is None:
                    continue
                ext_str = str(int(raw_ext)) if isinstance(raw_ext, (int, float)) else str(raw_ext).strip()
                if ext_str == ext_target:
                    return user.get("id")

            next_page_token = data.get("next_page_token")
            if not next_page_token:
                break

        return None

    async def get_user_call_logs(
        self,
        user_id: str,
        from_date: str,
        to_date: str,
        page_size: int = 100,
        next_page_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Fetch call logs for a specific Zoom Phone user.

        Uses ``GET /phone/users/{userId}/call_logs``, which performs
        server-side attribution — calls answered through a call queue are
        correctly attributed to the agent who picked up, **not** to the
        queue itself.  This is the correct endpoint to use when filtering
        call logs by individual extension/agent.

        Unlike the account-level ``/phone/call_logs`` endpoint, Zoom
        *does* populate ``owner_extension_number`` and correctly reflects
        the answering agent even for queue-routed calls.

        Args:
            user_id: Zoom user ID (not email, not extension).
            from_date: Start date in ``YYYY-MM-DD`` format.
            to_date: End date in ``YYYY-MM-DD`` format.
            page_size: Records per page (max 100).
            next_page_token: Pagination token.

        Returns:
            Dict with ``call_logs`` list and pagination info.
        """
        params: Dict[str, Any] = {
            "from": from_date,
            "to": to_date,
            "page_size": min(page_size, 100),
        }
        if next_page_token:
            params["next_page_token"] = next_page_token

        return await self._make_request(
            "GET", f"/phone/users/{user_id}/call_logs", params=params
        )

    async def get_call_log_detail(self, call_log_id: str) -> Dict[str, Any]:
        """Fetch full detail of a single call log by its UUID.

        Uses ``GET /phone/call_logs/{callLogId}`` which — unlike the paginated
        account-level endpoint — returns the complete ``log_details`` array
        containing every leg (agent interaction) of the call.

        Args:
            call_log_id: The call UUID (the ``id`` field from the account-level
                ``/phone/call_logs`` response, e.g.
                ``"664f1ab7-c435-4fc4-a6be-44e16c609270"``).

        Returns:
            Dict with root call fields plus a ``log_details`` list where each
            entry represents one agent leg of the call.
        """
        return await self._make_request(
            "GET", f"/phone/call_logs/{call_log_id}"
        )

    # ==========================================
    # Call Recordings
    # ==========================================

    async def download_recording_by_call_id(
        self,
        call_id: str,
        download_access_token: Optional[str] = None
    ) -> bytes:
        """
        Download call recording by call ID.

        Args:
            call_id: The call ID
            download_access_token: Optional access token for download

        Returns:
            Recording file as bytes
        """
        # First get recording details
        recording_info = await self._make_request(
            "GET",
            f"/phone/call_history/{call_id}/recordings"
        )

        # Extract download URL
        if recording_info and "recordings" in recording_info:
            recording = recording_info["recordings"][0]
            download_url = recording.get("download_url")

            if download_url:
                # Download the actual file
                return await self._make_request(
                    "GET",
                    download_url,
                    raw_response=True
                )

        raise ValueError(f"No recording found for call ID: {call_id}")

    async def get_recording_metadata(
        self,
        call_id: str,
    ) -> Dict[str, Any]:
        """
        Get recording metadata for a call.

        Returns the list of recordings (with their IDs and download
        URLs) associated with a call log entry.

        Endpoint: ``GET /phone/call_logs/{callId}/recordings``

        Args:
            call_id: The call identifier (``call_id`` or ``id`` field
                from call logs).

        Returns:
            Dict with ``recordings`` list containing ``id``,
            ``download_url``, ``file_url``, etc.
        """
        return await self._make_request(
            "GET",
            f"/phone/call_logs/{call_id}/recordings",
        )

    async def list_recordings(
        self,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        page_size: int = 30,
        next_page_token: Optional[str] = None,
        recording_type: Optional[RecordingType] = None
    ) -> Dict[str, Any]:
        """
        List all call recordings.

        Args:
            from_date: Start date for recordings
            to_date: End date for recordings
            page_size: Number of records per page
            next_page_token: Token for pagination
            recording_type: Filter by recording type

        Returns:
            List of recordings with metadata
        """
        params = {"page_size": min(page_size, 100)}

        if from_date:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date:
            params["to"] = to_date.strftime("%Y-%m-%d")
        if next_page_token:
            params["next_page_token"] = next_page_token
        if recording_type:
            params["type"] = recording_type.value

        return await self._make_request("GET", "/phone/recordings", params=params)

    async def get_user_recordings(
        self,
        user_id: str,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        page_size: int = 30
    ) -> Dict[str, Any]:
        """
        Get recordings for a specific user.

        Args:
            user_id: Zoom user ID or email
            from_date: Start date
            to_date: End date
            page_size: Number of records per page

        Returns:
            User's recordings
        """
        params = {"page_size": min(page_size, 100)}

        if from_date:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date:
            params["to"] = to_date.strftime("%Y-%m-%d")

        return await self._make_request(
            "GET",
            f"/phone/users/{user_id}/recordings",
            params=params
        )

    # ==========================================
    # Recording Transcripts
    # ==========================================

    async def download_recording_transcript(
        self,
        call_id: str,
        recording_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Download phone recording transcript.

        Args:
            call_id: The call ID
            recording_id: Optional specific recording ID

        Returns:
            Transcript data with timestamps and text
        """
        endpoint = f"/phone/call_history/{call_id}/recordings"

        if recording_id:
            endpoint = f"{endpoint}/{recording_id}/transcript"

        return await self._make_request("GET", endpoint)

    async def get_recording_transcript_by_id(
        self,
        recording_id: str
    ) -> Dict[str, Any]:
        """
        Get transcript for a specific recording.

        Args:
            recording_id: The recording identifier

        Returns:
            Transcript with speaker labels and timestamps
        """
        return await self._make_request(
            "GET",
            f"/phone/recordings/{recording_id}/transcript"
        )

    async def download_transcript_by_recording_id(
        self,
        recording_id: str,
    ) -> bytes:
        """
        Download a transcript file by its recording ID.

        This is the binary download endpoint used by the master
        component (``Zoom.py``) to fetch ``.vtt`` / ``.txt`` transcripts.

        Endpoint:
            ``GET /phone/recording_transcript/download/{recordingId}``

        Args:
            recording_id: The recording identifier.

        Returns:
            Raw transcript file bytes.
        """
        return await self._make_request(
            "GET",
            f"/phone/recording_transcript/download/{recording_id}",
            raw_response=True,
        )

    # ==========================================
    # Phone Numbers
    # ==========================================

    async def list_phone_numbers(
        self,
        page_size: int = 30,
        next_page_token: Optional[str] = None,
        site_id: Optional[str] = None,
        extension_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List all phone numbers in the account.

        Args:
            page_size: Number of records per page
            next_page_token: Token for pagination
            site_id: Filter by site ID
            extension_type: Filter by extension type (user, callQueue, autoReceptionist, etc.)

        Returns:
            List of phone numbers with assignments
        """
        params = {"page_size": min(page_size, 100)}

        if next_page_token:
            params["next_page_token"] = next_page_token
        if site_id:
            params["site_id"] = site_id
        if extension_type:
            params["extension_type"] = extension_type

        return await self._make_request("GET", "/phone/numbers", params=params)

    async def get_phone_number(self, phone_number_id: str) -> Dict[str, Any]:
        """
        Get details of a specific phone number.

        Args:
            phone_number_id: The phone number ID

        Returns:
            Phone number details including assignment and capabilities
        """
        return await self._make_request("GET", f"/phone/numbers/{phone_number_id}")

    async def get_phone_number_by_number(self, number: str) -> Dict[str, Any]:
        """
        Get phone number details by actual phone number.

        Args:
            number: The phone number (e.g., "+15551234567")

        Returns:
            Phone number details
        """
        # List all numbers and filter
        result = await self.list_phone_numbers(page_size=100)

        for phone in result.get("phone_numbers", []):
            if phone.get("number") == number:
                return await self.get_phone_number(phone.get("id"))

        raise ValueError(f"Phone number not found: {number}")

    # ==========================================
    # Users & Profiles
    # ==========================================

    async def list_phone_users(
        self,
        page_size: int = 30,
        next_page_token: Optional[str] = None,
        site_id: Optional[str] = None,
        calling_type: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List all phone users in the account.

        Args:
            page_size: Number of records per page
            next_page_token: Token for pagination
            site_id: Filter by site
            calling_type: Filter by calling type (internal, external, etc.)
            status: Filter by status (active, inactive)

        Returns:
            List of phone users
        """
        params = {"page_size": min(page_size, 100)}

        if next_page_token:
            params["next_page_token"] = next_page_token
        if site_id:
            params["site_id"] = site_id
        if calling_type:
            params["calling_type"] = calling_type
        if status:
            params["status"] = status

        return await self._make_request("GET", "/phone/users", params=params)

    async def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Get a user's phone profile.

        Args:
            user_id: Zoom user ID or email

        Returns:
            User's phone profile including extensions, settings, and numbers
        """
        return await self._make_request("GET", f"/phone/users/{user_id}")

    async def get_user_settings(self, user_id: str) -> Dict[str, Any]:
        """
        Get a user's phone settings.

        Args:
            user_id: Zoom user ID or email

        Returns:
            User's phone settings and preferences
        """
        return await self._make_request("GET", f"/phone/users/{user_id}/settings")

    # ==========================================
    # Voicemail
    # ==========================================

    async def list_voicemails(
        self,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        page_size: int = 30,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List voicemails.

        Args:
            from_date: Start date
            to_date: End date
            page_size: Number of records per page
            status: Filter by status (read, unread)

        Returns:
            List of voicemails
        """
        params = {"page_size": min(page_size, 100)}

        if from_date:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date:
            params["to"] = to_date.strftime("%Y-%m-%d")
        if status:
            params["status"] = status

        return await self._make_request("GET", "/phone/voicemails", params=params)

    async def get_user_voicemails(
        self,
        user_id: str,
        page_size: int = 30,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get voicemails for a specific user.

        Args:
            user_id: Zoom user ID or email
            page_size: Number of records per page
            status: Filter by status

        Returns:
            User's voicemails
        """
        params = {"page_size": min(page_size, 100)}

        if status:
            params["status"] = status

        return await self._make_request(
            "GET",
            f"/phone/users/{user_id}/voicemails",
            params=params
        )

    # ==========================================
    # Sites & Extensions
    # ==========================================

    async def list_sites(
        self,
        page_size: int = 30,
        next_page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List all sites (locations).

        Args:
            page_size: Number of records per page
            next_page_token: Token for pagination

        Returns:
            List of sites
        """
        params = {"page_size": min(page_size, 100)}

        if next_page_token:
            params["next_page_token"] = next_page_token

        return await self._make_request("GET", "/phone/sites", params=params)

    async def get_extension_details(
        self,
        extension_id: str
    ) -> Dict[str, Any]:
        """
        Get details about a specific extension.

        Args:
            extension_id: The extension ID

        Returns:
            Extension details and configuration
        """
        return await self._make_request(
            "GET",
            f"/phone/extension/{extension_id}"
        )

    # ==========================================
    # SMS Messages (Legacy)
    # ==========================================

    async def list_sms_messages(
        self,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        page_size: int = 30,
        phone_number: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List SMS messages (legacy endpoint).

        Args:
            from_date: Start date
            to_date: End date
            page_size: Number of records per page
            phone_number: Filter by phone number

        Returns:
            List of SMS messages
        """
        params = {"page_size": min(page_size, 100)}

        if from_date:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date:
            params["to"] = to_date.strftime("%Y-%m-%d")
        if phone_number:
            params["phone_number"] = phone_number

        return await self._make_request("GET", "/phone/sms", params=params)

    async def send_sms(
        self,
        to_number: str,
        from_number: str,
        message: str,
        to_numbers: Optional[List[str]] = None,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send an SMS message via Zoom Phone.

        Endpoint: ``POST /phone/sms/messages``

        Required scopes (any one):
            ``phone_sms:write``, ``phone_sms:write:admin``,
            ``phone:write``, ``phone:write:admin``

        Args:
            to_number: Recipient phone number in E.164 format
                (e.g. ``+15551234567``). Ignored if ``to_numbers``
                is provided.
            from_number: Sender phone number in E.164 format.
                Must be an SMS-capable number assigned in Zoom Phone.
            message: SMS text content (max 500 characters). Messages
                longer than 160 characters are split into segments.
            to_numbers: Optional list of recipient phone numbers
                (max 10). If provided, ``to_number`` is ignored.
                For US/CA Toll numbers this creates a group message.
            session_id: Optional existing session ID to continue
                a conversation thread.

        Returns:
            Dict with ``message_id``, ``session_id``, and
            ``date_time`` on success (HTTP 201).
        """
        recipients = to_numbers or [to_number]
        data: Dict[str, Any] = {
            "sender": {"phone_number": from_number},
            "to_members": [
                {"phone_number": num} for num in recipients
            ],
            "message": message,
        }
        if session_id:
            data["session_id"] = session_id

        return await self._make_request(
            "POST", "/phone/sms/messages", json_data=data
        )

    # ==========================================
    # SMS Sessions (New API)
    # ==========================================

    async def list_sms_sessions(
        self,
        phone_number: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        filter_type: str = "last_message_time",
        page_size: int = 100,
        next_page_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        List SMS sessions for a phone number.

        Uses the newer ``/phone/sms/sessions`` endpoint which groups
        messages into conversational sessions.

        Args:
            phone_number: Phone number to query (e.g. ``18108001001``
                without the leading ``+``).
            from_date: Start date in ``YYYY-MM-DD`` format.
            to_date: End date in ``YYYY-MM-DD`` format.
                Required when *from_date* is provided; max range 31 days.
            filter_type: One of ``sent_message_time``,
                ``received_message_time``, ``last_message_time``,
                ``sent_received_message_time``.
            page_size: Number of sessions per page (max 100).
            next_page_token: Token for pagination.

        Returns:
            Dict with ``sms_sessions`` list and pagination info.
        """
        params = {
            "phone_number": phone_number.lstrip("+"),
            "page_size": min(page_size, 100),
        }

        if from_date:
            params["from"] = from_date
            params["filter_type"] = filter_type
            if to_date:
                params["to"] = to_date

        if next_page_token:
            params["next_page_token"] = next_page_token

        return await self._make_request("GET", "/phone/sms/sessions", params=params)

    async def get_sms_session_details(
        self,
        session_id: str,
        next_page_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get details (messages) for a specific SMS session.

        Args:
            session_id: The SMS session identifier.
            next_page_token: Token for pagination of messages.

        Returns:
            Dict with ``sms_histories`` list and pagination info.
        """
        params = {}
        if next_page_token:
            params["next_page_token"] = next_page_token

        return await self._make_request(
            "GET",
            f"/phone/sms/sessions/{session_id}",
            params=params or None,
        )

    # ==========================================
    # Call Queues
    # ==========================================

    async def list_call_queues(
        self,
        page_size: int = 30,
        next_page_token: Optional[str] = None,
        site_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List all call queues.

        Args:
            page_size: Number of records per page
            next_page_token: Token for pagination
            site_id: Filter by site

        Returns:
            List of call queues
        """
        params = {"page_size": min(page_size, 100)}

        if next_page_token:
            params["next_page_token"] = next_page_token
        if site_id:
            params["site_id"] = site_id

        return await self._make_request("GET", "/phone/call_queues", params=params)

    async def get_call_queue(self, queue_id: str) -> Dict[str, Any]:
        """
        Get details of a specific call queue.

        Args:
            queue_id: The call queue ID

        Returns:
            Call queue configuration and members
        """
        return await self._make_request("GET", f"/phone/call_queues/{queue_id}")

    # ==========================================
    # Extension / Phone Mapping
    # ==========================================

    @staticmethod
    def normalize_phone_number(phone: str) -> str:
        """
        Normalize a phone number to digits-only international format.

        Handles formats like:
            ``(786) 879-8923``, ``786-879-8923``, ``7868798923``,
            ``+17868798923``.

        For US numbers (10 digits) the ``1`` country-code prefix is
        added automatically.

        Args:
            phone: Raw phone string.

        Returns:
            Normalized digits-only string, e.g. ``17868798923``.
        """
        digits_only = re.sub(r"\D", "", str(phone))
        if len(digits_only) == 10:
            return f"1{digits_only}"
        return digits_only

    async def get_phone_numbers_by_extension(
        self,
        extension_number: str,
    ) -> List[str]:
        """
        Look up phone numbers assigned to an extension.

        Iterates over ``/phone/users`` with pagination and returns the
        phone numbers for the user whose ``extension_number`` matches.

        Args:
            extension_number: The extension to look up.

        Returns:
            List of phone number strings (may be empty).
        """
        ext_target = str(extension_number).strip()
        next_page_token = None

        while True:
            params: Dict[str, Any] = {"page_size": 100}
            if next_page_token:
                params["next_page_token"] = next_page_token

            data = await self._make_request("GET", "/phone/users", params=params)

            for user in data.get("users", []):
                ext_num = user.get("extension_number")
                if ext_num is None:
                    continue
                # Normalize extension (handle int/float from API)
                if isinstance(ext_num, (int, float)):
                    ext_str = str(int(ext_num))
                else:
                    ext_str = str(ext_num).strip()

                if ext_str == ext_target:
                    numbers = []
                    for phone_obj in user.get("phone_numbers", []):
                        if isinstance(phone_obj, dict):
                            number = phone_obj.get("number")
                            if number:
                                numbers.append(number)
                        elif isinstance(phone_obj, str):
                            numbers.append(phone_obj)
                    return numbers

            next_page_token = data.get("next_page_token")
            if not next_page_token:
                break

        return []

    @staticmethod
    def determine_bound(session: Dict[str, Any]) -> str:
        """
        Determine if an SMS session is inbound or outbound.

        Logic:
        - If the participant with ``is_session_owner=True`` has the
          queried phone number → ``outbound``.
        - If the participant with ``is_session_owner=False`` has the
          queried phone number → ``inbound``.

        Args:
            session: Session dict containing ``participants`` and
                ``queried_phone_number``.

        Returns:
            ``'outbound'``, ``'inbound'``, or ``'unknown'``.
        """
        participants = session.get("participants", [])
        queried_number = session.get("queried_phone_number", "").lstrip("+")

        if not participants or not queried_number:
            return "unknown"

        queried_normalized = re.sub(r"\D", "", queried_number)
        if len(queried_normalized) == 10:
            queried_normalized = f"1{queried_normalized}"

        for participant in participants:
            is_owner = participant.get("is_session_owner", False)
            phone_number = participant.get("phone_number", "").lstrip("+")
            participant_normalized = re.sub(r"\D", "", phone_number)
            if len(participant_normalized) == 10:
                participant_normalized = f"1{participant_normalized}"

            if queried_normalized == participant_normalized:
                return "outbound" if is_owner else "inbound"

        return "unknown"

    def get_extension_from_phone(
        self,
        phone_number: str,
    ) -> str:
        """Reverse-lookup: get extension from a phone number.

        Uses the internal ``_phone_to_extension_map`` that is built by
        the component during SMS processing.

        Args:
            phone_number: Phone number to look up.

        Returns:
            Extension string, or ``''`` if not found.
        """
        if not phone_number:
            return ""
        normalized = self.normalize_phone_number(phone_number)
        mapping = getattr(self, "_phone_to_extension_map", {})
        return mapping.get(normalized, "")

    # ==========================================
    # Utility Methods
    # ==========================================

    async def get_all_paginated_results(
        self,
        method_func,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Helper to get all results from a paginated endpoint.

        Args:
            method_func: The async method to call
            **kwargs: Arguments to pass to the method

        Returns:
            Combined list of all results
        """
        all_results = []
        next_page_token = None

        while True:
            if next_page_token:
                kwargs["next_page_token"] = next_page_token

            response = await method_func(**kwargs)

            # Extract items based on common response patterns
            items = None
            for key in [
                "phone_numbers", "users", "recordings",
                "call_history", "call_logs",
                "voicemails", "sites", "call_queues",
                "sms_sessions", "sms_histories",
            ]:
                if key in response:
                    items = response[key]
                    break

            if items:
                all_results.extend(items)

            # Check for next page
            next_page_token = response.get("next_page_token")
            if not next_page_token:
                break

        return all_results
