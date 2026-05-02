"""
Unofficial Spotify Creators GraphQL connector.

Uses the persisted-query (APQ) GraphQL endpoint at creators-graph.spotify.com
to fetch podcast analytics data from the Spotify Creators (formerly Anchor)
dashboard.

Authentication relies on the same PKCE OAuth 2.0 flow used by the Spotify
Creators web app.  The only credential the user needs to supply is the
``sp_dc`` cookie value from an active Spotify session.  Everything else is
derived automatically.

The API is not publicly documented and may change at any time.
Use at your own risk.
"""

from __future__ import annotations

import base64
import hashlib
import re
import secrets
import time
from datetime import date as Date
from threading import RLock
from typing import Any

import requests
import yaml
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from .types import (
    ANCHOR_LEGACY_API_URL,
    ANCHOR_LEGACY_API_VERSION,
    AUTH_URL,
    CLIENT_ANALYTICS,
    CLIENT_PUBLIC,
    CLIENT_SHELL,
    CREATORS_ORIGIN,
    CREATORS_REFERER,
    GRAPHQL_URL,
    OAUTH_REDIRECT_URI,
    OAUTH_SCOPE,
    OPERATION_HASHES,
    SPOTIFY_CLIENT_ID,
    TOKEN_URL,
    JsonDict,
    JsonValue,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MAX_REQUEST_ATTEMPTS = 6
DELAY_BASE = 2.0
# Re-fetch the bearer token this many seconds before it expires
TOKEN_REFRESH_BUFFER_SECS = 300

# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class CredentialsExpired(Exception):
    """Raised when the sp_dc cookie has expired and login is required."""


class AuthenticationError(Exception):
    """Raised for unexpected authentication responses."""


class MaxRetriesException(Exception):
    """Raised when all retry attempts for a request are exhausted."""


# ---------------------------------------------------------------------------
# Connector
# ---------------------------------------------------------------------------


class SpotifyGraphQLConnector:
    """
    Connector for the Spotify Creators GraphQL persisted-query API.

    Parameters
    ----------
    sp_dc:
        The value of the ``sp_dc`` cookie from an active Spotify session.
        Obtain it by logging in to https://creators.spotify.com and
        inspecting the ``sp_dc`` cookie in your browser's DevTools.
    sp_key:
        The value of the ``sp_key`` cookie from an active Spotify session.
        Found alongside ``sp_dc`` in your browser's DevTools under
        ``https://accounts.spotify.com``.
    show_uri:
        The Spotify show URI, e.g. ``spotify:show:1HaFboRBVORs2VCpNACYLn``.
        If not provided it will be resolved automatically from the first
        show returned by ``WebGetUserAndShows``.
    station_id:
        The numeric Anchor/Spotify station ID (used by legacy endpoints such
        as ``WebGetIndexedEpisodeList``).  Resolved automatically when
        ``show_uri`` is known if not provided.
    """

    # Class-level type annotations
    sp_dc: str
    sp_key: str
    show_uri: str | None
    station_id: str | None
    _bearer: str | None
    _bearer_expires_at: float
    _auth_lock: RLock
    _auth_poisoned: bool  # True when sp_dc is known-expired; stop retrying

    def __init__(
        self,
        sp_dc: str,
        sp_key: str,
        show_uri: str | None = None,
        station_id: str | None = None,
    ) -> None:
        self.sp_dc = sp_dc
        self.sp_key = sp_key
        self.show_uri = show_uri
        self.station_id = station_id
        self._bearer = None
        self._bearer_expires_at = 0.0
        self._auth_lock = RLock()
        self._auth_poisoned = False

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _ensure_auth(self) -> None:
        """Ensure a valid bearer token is available, refreshing if needed."""
        with self._auth_lock:
            if self._auth_poisoned:
                raise CredentialsExpired(
                    "sp_dc cookie has expired. Please supply a fresh SPOTIFY_SP_DC value."
                )
            now = time.monotonic()
            if self._bearer is None or now >= self._bearer_expires_at - TOKEN_REFRESH_BUFFER_SECS:
                self._authenticate()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
    )
    def _authenticate(self) -> None:
        """
        Perform the PKCE OAuth 2.0 code exchange to obtain a bearer token.

        Mirrors the flow used by the Spotify Creators web app:
        1. Generate a PKCE code_verifier / code_challenge.
        2. GET /oauth2/v2/auth with sp_dc + sp_key cookies - Spotify returns
           an HTML page containing ``const authorizationResponse = {...};``.
        3. Parse the auth code out of that JS object.
        4. POST /api/token with the code + code_verifier to get the bearer token.
        """
        if self._auth_poisoned:
            raise CredentialsExpired(
                "sp_dc / sp_key cookies have expired. Please supply fresh values."
            )

        # --- PKCE setup ---
        state = secrets.token_urlsafe(32)
        code_verifier = secrets.token_urlsafe(64)
        # Spotify requires standard base64url (not urlsafe_b64encode which uses - and _)
        # but then also needs + replaced with - and / with _ - token_urlsafe already does
        # the right thing; we just need to strip padding and fix the standard chars.
        digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
        code_challenge = (
            base64.b64encode(digest).decode("utf-8").rstrip("=").replace("/", "_").replace("+", "-")
        )

        logger.debug("Fetching OAuth authorisation page …")
        resp = requests.get(
            AUTH_URL,
            params={
                "response_type": "code",
                "client_id": SPOTIFY_CLIENT_ID,
                "scope": OAUTH_SCOPE,
                "redirect_uri": OAUTH_REDIRECT_URI,
                "code_challenge": code_challenge,
                "code_challenge_method": "S256",
                "state": state,
                "response_mode": "web_message",
                "prompt": "none",
            },
            cookies={
                "sp_dc": self.sp_dc,
                "sp_key": self.sp_key,
            },
            timeout=60,
        )
        resp.raise_for_status()

        body = resp.text
        logger.trace("auth page body = {}", body)

        # Detect an expired / invalid session
        if "login_required" in body:
            self._auth_poisoned = True
            raise CredentialsExpired(
                "Spotify returned login_required. The sp_dc/sp_key cookies have expired."
            )

        # Spotify embeds the auth response as:
        #   const authorizationResponse = {...};
        match = re.search(r"const authorizationResponse = (.*?);", body, re.DOTALL)
        if not match:
            raise AuthenticationError(
                "Could not find authorizationResponse in Spotify auth page. "
                f"Page snippet: {body[:500]!r}"
            )

        raw = match.group(1)
        try:
            # The embedded object is not strict JSON (unquoted keys), but PyYAML
            # parses it correctly as it's a superset of JSON.
            auth_response: dict[str, Any] = yaml.safe_load(raw)
        except Exception as exc:
            raise AuthenticationError(f"Failed to parse authorizationResponse: {exc}") from exc

        if auth_response.get("type") != "authorization_response":
            raise AuthenticationError(
                f"Expected type='authorization_response', got: {auth_response!r}"
            )

        response_body = auth_response.get("response", {})
        if not isinstance(response_body, dict):
            raise AuthenticationError(f"Unexpected response body shape: {auth_response!r}")

        if response_body.get("state") != state:
            raise AuthenticationError("State parameter mismatch in authentication response")

        auth_code = response_body.get("code")
        if not auth_code:
            raise AuthenticationError(f"No auth code in response: {response_body!r}")

        # --- Token exchange ---
        logger.debug("Exchanging authorisation code for bearer token …")
        token_resp = requests.post(
            TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "client_id": SPOTIFY_CLIENT_ID,
                "code": auth_code,
                "redirect_uri": OAUTH_REDIRECT_URI,
                "code_verifier": code_verifier,
            },
            timeout=60,
        )
        token_resp.raise_for_status()
        token_data = token_resp.json()

        self._bearer = token_data["access_token"]
        expires_in: int = token_data.get("expires_in", 3600)
        self._bearer_expires_at = time.monotonic() + expires_in
        logger.debug("Obtained bearer token (expires in {}s)", expires_in)

    def _graphql_headers(self, creator_client: str = CLIENT_SHELL) -> dict[str, str]:
        """Return the HTTP headers used for every GraphQL request."""
        assert self._bearer is not None, "_ensure_auth() must be called first"
        return {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:147.0) "
                "Gecko/20100101 Firefox/147.0"
            ),
            "Accept": "*/*",
            "Accept-Language": "en",
            "Content-Type": "application/json",
            "x-creator-client": creator_client,
            "Authorization": f"Bearer {self._bearer}",
            "Origin": CREATORS_ORIGIN,
            "Referer": CREATORS_REFERER,
        }

    def _resolve_date_range(
        self,
        date_range_window: str,
        start_date: Date | str | None,
        end_date: Date | str | None,
    ) -> dict[str, JsonValue]:
        """
        Build the date-range variables for a GraphQL request.

        When *start_date* / *end_date* are provided they take precedence:
        ``dateRangeWindow`` is forced to ``"WINDOW_CUSTOM"`` and a
        ``customDateRange`` sub-object is added.  Both ``datetime.date``
        objects and ISO-format strings (``"YYYY-MM-DD"``) are accepted.

        Parameters
        ----------
        date_range_window:
            Named window such as ``"WINDOW_LAST_THIRTY_DAYS"``.  Ignored when
            *start_date* / *end_date* are supplied.
        start_date:
            Inclusive start of the custom range.
        end_date:
            Inclusive end of the custom range.

        Raises
        ------
        ValueError
            If only one of *start_date* / *end_date* is provided.
        """
        if start_date is not None or end_date is not None:
            if start_date is None or end_date is None:
                raise ValueError(
                    "Both start_date and end_date must be provided together "
                    "(received only one of the two)."
                )
            start_str = start_date.isoformat() if isinstance(start_date, Date) else start_date
            end_str = end_date.isoformat() if isinstance(end_date, Date) else end_date
            return {
                "dateRangeWindow": "WINDOW_CUSTOM",
                "customDateRange": {"startDate": start_str, "endDate": end_str},
            }
        return {"dateRangeWindow": date_range_window}

    def _query(
        self,
        operation_name: str,
        variables: dict[str, JsonValue] | None = None,
        creator_client: str = CLIENT_SHELL,
    ) -> JsonDict:
        """
        Execute a persisted GraphQL query and return the parsed response.

        Parameters
        ----------
        operation_name:
            One of the keys in ``OPERATION_HASHES``.
        variables:
            GraphQL variables dict (may be empty / ``None``).
        creator_client:
            Value for the ``x-creator-client`` header.

        Returns
        -------
        The ``data`` field of the GraphQL response as a ``JsonDict``.

        Raises
        ------
        KeyError
            If ``operation_name`` is not registered in ``OPERATION_HASHES``.
        requests.HTTPError
            On non-2xx responses after all retries are exhausted.
        """
        sha = OPERATION_HASHES[operation_name]
        payload: JsonDict = {
            "operationName": operation_name,
            "variables": variables or {},
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": sha,
                }
            },
        }

        for attempt in range(1, MAX_REQUEST_ATTEMPTS + 1):
            self._ensure_auth()
            headers = self._graphql_headers(creator_client)

            logger.debug(
                "GraphQL {} (attempt {}/{})",
                operation_name,
                attempt,
                MAX_REQUEST_ATTEMPTS,
            )
            resp = requests.post(
                GRAPHQL_URL,
                json=payload,
                headers=headers,
                timeout=60,
            )

            if resp.status_code == 200:
                body: JsonDict = resp.json()
                if "errors" in body:
                    logger.warning("GraphQL errors in {}: {}", operation_name, body["errors"])
                data = body.get("data")
                if not isinstance(data, dict):
                    return body  # return the whole envelope if data is missing
                return data  # type: ignore[return-value]

            if resp.status_code == 401:
                logger.warning("401 Unauthorised - refreshing token …")
                with self._auth_lock:
                    # Invalidate cached token so _ensure_auth re-fetches it
                    self._bearer = None
                    self._bearer_expires_at = 0.0
                delay = DELAY_BASE**attempt
                time.sleep(delay)
                continue

            if resp.status_code in (429, 502, 503, 504):
                delay = DELAY_BASE**attempt
                logger.warning(
                    "HTTP {} on {} - retrying in {:.1f}s …",
                    resp.status_code,
                    operation_name,
                    delay,
                )
                time.sleep(delay)
                continue

            # Any other error: log the query details and raise immediately
            try:
                resp.raise_for_status()
            except requests.HTTPError:
                logger.error(
                    "GraphQL request for {} failed. Payload: {} Response: {}",
                    operation_name,
                    payload,
                    resp.text,
                )
                raise

        raise MaxRetriesException(
            f"All {MAX_REQUEST_ATTEMPTS} attempts failed for {operation_name}"
        )

    # ------------------------------------------------------------------
    # Auto-resolution helpers
    # ------------------------------------------------------------------

    def _ensure_show_uri(self) -> str:
        """Return the configured show URI, resolving it automatically if needed."""
        if self.show_uri:
            return self.show_uri
        logger.debug("show_uri not set - resolving from getShowsForUser …")
        data = self.get_shows_for_user()
        # Native response shape: data.showsForUser.shows[].uri  (same key for both endpoints)
        shows_for_user = data.get("showsForUser") if isinstance(data, dict) else None
        shows: list[JsonValue] = []
        if isinstance(shows_for_user, dict):
            raw_shows = shows_for_user.get("shows")
            if isinstance(raw_shows, list):
                shows = raw_shows
        if not shows:
            raise ValueError(
                "Could not automatically resolve show_uri. Please set SPOTIFY_SHOW_URI explicitly."
            )
        # Prefer the first hosted show (S4P) since those have full analytics access;
        # fall back to the first show of any type.
        chosen: JsonValue = None
        for show in shows:
            if isinstance(show, dict) and show.get("hostingProvider") == "S4P":
                chosen = show
                break
        if chosen is None:
            chosen = shows[0]
        if not isinstance(chosen, dict):
            raise ValueError(f"Unexpected show entry shape: {chosen!r}")
        uri = chosen.get("uri")
        if not isinstance(uri, str):
            raise ValueError(f"Could not extract uri from show entry: {chosen!r}")
        self.show_uri = uri
        logger.info("Resolved show_uri = {}", self.show_uri)
        return self.show_uri

    def _ensure_station_id(self) -> str:
        """
        Return the station ID, resolving it from the show URI if needed.

        The station ID is the numeric Anchor/Spotify station ID used by
        legacy GraphQL variables like ``stationId``.  It is available as
        ``stationId`` on each show entry in the ``WebGetUserShows`` response.
        """
        if self.station_id:
            return self.station_id
        show_uri = self._ensure_show_uri()
        # Native response shape: data.showsForUser.shows[].{uri, stationId}
        # get_user_shows (WebGetUserShows) returns stationId; get_shows_for_user does not.
        data = self.get_user_shows()
        shows_for_user = data.get("showsForUser") if isinstance(data, dict) else None
        if isinstance(shows_for_user, dict):
            shows: list[JsonValue] = shows_for_user.get("shows", [])  # type: ignore[assignment]
            logger.debug("Looking for stationId in {} shows from get_user_shows …", len(shows))
            logger.trace("Shows: {}", shows)
            for show in shows:
                if not isinstance(show, dict):
                    continue
                if show.get("uri") == show_uri:
                    sid = show.get("stationId") or show.get("id")
                    if sid is not None:
                        self.station_id = str(sid)
                        logger.info("Resolved station_id = {}", self.station_id)
                        return self.station_id
                    else:
                        raise ValueError(
                            f"Show entry for uri {show_uri} is missing stationId: {show!r}"
                        )
        raise ValueError(
            "Could not automatically resolve station_id. Please set SPOTIFY_STATION_ID explicitly."
        )

    # ------------------------------------------------------------------
    # Public API: user / show discovery
    # ------------------------------------------------------------------

    def get_user_metadata(self) -> JsonDict:
        """
        Fetch basic metadata about the authenticated Spotify user.

        Corresponds to the ``getUserMetadata`` persisted query.
        """
        return self._query("getUserMetadata", creator_client=CLIENT_PUBLIC)

    def get_user_shows(self) -> JsonDict:
        """
        Fetch all shows (podcasts) owned by the authenticated user.

        Corresponds to the ``WebGetUserShows`` persisted query.
        Returns basic show info: uri, name, stationId, coverArt, permissionsV2.
        """
        return self._query(
            "WebGetUserShows",
            creator_client=CLIENT_PUBLIC,
        )

    def get_shows_for_user(self) -> JsonDict:
        """
        Fetch all shows for the authenticated user with rich metadata.

        Returns richer data than ``get_user_shows``: includes ``authorName``,
        ``category``, ``description``, and ``hostingProvider`` in addition to
        the basic fields.

        Corresponds to the ``getShowsForUser`` persisted query
        (``x-creator-client: microfrontend-analytics``).
        """
        return self._query(
            "getShowsForUser",
            creator_client=CLIENT_ANALYTICS,
        )

    def get_user_and_shows(
        self,
        show_filter: str = "ALL",
    ) -> JsonDict:
        """
        Fetch the authenticated user together with their shows.

        Parameters
        ----------
        show_filter:
            One of ``"ALL"``, ``"ACTIVE"``, ``"INACTIVE"``.
            Defaults to ``"ALL"``.

        Corresponds to the ``WebGetUserAndShows`` persisted query.
        """
        return self._query(
            "WebGetUserAndShows",
            variables={"showFilter": show_filter},
        )

    def get_user_registration(self, country_code: str = "US") -> JsonDict:
        """
        Fetch user registration / onboarding state for a given country.

        Parameters
        ----------
        country_code:
            ISO 3166-1 alpha-2 country code, e.g. ``"US"`` or ``"DE"``.

        Corresponds to the ``WebGetUserRegistration`` persisted query.
        """
        return self._query(
            "WebGetUserRegistration",
            variables={"countryCode": country_code},
            creator_client=CLIENT_PUBLIC,
        )

    # ------------------------------------------------------------------
    # Public API: show-level
    # ------------------------------------------------------------------

    def get_show_type(self, show_uri: str | None = None) -> JsonDict:
        """
        Fetch the show type (e.g. PODCAST, AUDIOBOOK) for a given show URI.

        Parameters
        ----------
        show_uri:
            Spotify show URI.  Resolved automatically when not provided.

        Corresponds to the ``WebGetShowTypeByUri`` persisted query.
        """
        uri = show_uri or self._ensure_show_uri()
        return self._query(
            "WebGetShowTypeByUri",
            variables={"showUri": uri},
        )

    def get_show_overview_stats(self, show_uri: str | None = None) -> JsonDict:
        """
        Fetch near-real-time overview statistics for a show.

        Returns aggregate listener/stream counts and trending data.

        Parameters
        ----------
        show_uri:
            Spotify show URI.  Resolved automatically when not provided.

        Corresponds to the ``getShowOverviewStatsNRT`` persisted query.
        """
        uri = show_uri or self._ensure_show_uri()
        return self._query(
            "getShowOverviewStatsNRT",
            variables={"showUri": uri},
            creator_client=CLIENT_PUBLIC,
        )

    def get_streams_and_downloads_all_time(self, show_uri: str | None = None) -> JsonDict:
        """
        Fetch all-time streams and downloads for a show across all platforms.

        Returns all-time streams and downloads counts.

        Parameters
        ----------
        show_uri:
            Spotify show URI.  Resolved automatically when not provided.

        Corresponds to the ``getShowAllPlatformsStatsNRT`` persisted query.
        """
        uri = show_uri or self._ensure_show_uri()
        return self._query(
            "getShowAllPlatformsStatsNRT",
            variables={"showUri": uri},
            creator_client=CLIENT_ANALYTICS,
        )

    def get_show_clips(
        self,
        show_uri: str | None = None,
        page_size: int = 1000,
    ) -> JsonDict:
        """
        Fetch all clips (short-form video previews) for a show.

        Parameters
        ----------
        show_uri:
            Spotify show URI.  Resolved automatically when not provided.
        page_size:
            Maximum number of clips to return.  Defaults to ``1000``.

        Corresponds to the ``getShowClips`` persisted query.
        """
        uri = show_uri or self._ensure_show_uri()
        return self._query(
            "getShowClips",
            variables={"showUri": uri, "pageSize": page_size},
            creator_client=CLIENT_PUBLIC,
        )

    def get_monetization_lifecycle_state(self, show_uri: str | None = None) -> JsonDict:
        """
        Fetch the monetisation lifecycle state for a show.

        Parameters
        ----------
        show_uri:
            Spotify show URI.  Resolved automatically when not provided.

        Corresponds to the ``WebGetMonetizationLifecycleState`` persisted query.
        """
        uri = show_uri or self._ensure_show_uri()
        return self._query(
            "WebGetMonetizationLifecycleState",
            variables={"showUri": uri},
        )

    # ------------------------------------------------------------------
    # Public API: episode list
    # ------------------------------------------------------------------

    def get_episode_list(
        self,
        station_id: str
        | None = None,  # deprecated, ignored; kept first for legacy positional calls
        current_page: int = 1,
        page_size: int = 10,
        sort_order: str | None = None,
        sort_by: str | None = None,
        search: str | None = None,
        episode_filter: str | None = None,
        *,
        show_uri: str | None = None,
    ) -> JsonDict:
        """
        Fetch a paginated, searchable list of episodes for a show.

        Parameters
        ----------
        show_uri:
            Spotify show URI (e.g. ``spotify:show:1HaFboRBVORs2VCpNACYLn``).
            Resolved automatically when not provided.
        current_page:
            1-based page number.
        page_size:
            Episodes per page (max observed: 50).
        sort_order:
            ``"ASC"`` or ``"DESC"``.  ``None`` uses the API default.
        sort_by:
            Field to sort by (e.g. ``"publishDate"``).  ``None`` uses the API default.
        search:
            Free-text search string to filter episodes by title.
        episode_filter:
            API-specific filter string (e.g. ``"PUBLISHED"``).
        station_id:
            Deprecated.  The API now keys episode lists by ``showUri``;
            this argument is accepted for backwards compatibility (including
            existing positional calls like ``get_episode_list(STATION_ID, ...)``)
            and ignored.  Use ``show_uri=`` (keyword-only) instead.

        Corresponds to the ``WebGetIndexedEpisodeList`` persisted query.
        """
        if station_id is not None:
            logger.warning(
                "get_episode_list(station_id=...) is deprecated and ignored; "
                "the upstream API now keys episode lists by showUri. "
                "Pass show_uri= instead (or rely on auto-resolution)."
            )
        uri = show_uri or self._ensure_show_uri()
        return self._query(
            "WebGetIndexedEpisodeList",
            variables={
                "showUri": uri,
                "currentPage": current_page,
                "pageSize": page_size,
                "sortOrder": sort_order,
                "sortBy": sort_by,
                "search": search,
                "filter": episode_filter,
            },
            creator_client=CLIENT_PUBLIC,
        )

    def get_all_episodes(
        self,
        station_id: str
        | None = None,  # deprecated, ignored; kept first for legacy positional calls
        page_size: int = 50,
        *,
        show_uri: str | None = None,
    ) -> list[JsonDict]:
        """
        Fetch every episode for a show, automatically paginating through all pages.

        Parameters
        ----------
        show_uri:
            Spotify show URI.  Resolved automatically when not provided.
        page_size:
            Episodes per page used in each underlying request.
        station_id:
            Deprecated and ignored.  Kept as the first positional parameter so
            that legacy callers using ``get_all_episodes(STATION_ID, ...)`` keep
            working.  Use ``show_uri=`` (keyword-only) instead.

        Returns
        -------
        A flat list of episode dicts in the native API shape.
        """
        if station_id is not None:
            logger.warning(
                "get_all_episodes(station_id=...) is deprecated and ignored; "
                "the upstream API now keys episode lists by showUri. "
                "Pass show_uri= instead (or rely on auto-resolution)."
            )
        uri = show_uri or self._ensure_show_uri()
        episodes: list[JsonDict] = []
        page = 1

        while True:
            logger.debug("Fetching episode page {} …", page)
            data = self.get_episode_list(
                show_uri=uri,
                current_page=page,
                page_size=page_size,
            )

            # Native response shape (current):  data.showByShowUri.episodesV2.{items, pagination}
            # Older shapes (fallback):          data.show.episodesV2 / data.showByStationId.episodesV2
            show_node = data.get("showByShowUri")
            if not isinstance(show_node, dict):
                show_node = data.get("show")
            if not isinstance(show_node, dict):
                show_node = data.get("showByStationId")
            if not isinstance(show_node, dict):
                break

            episodes_v2 = show_node.get("episodesV2")
            if not isinstance(episodes_v2, dict):
                break

            items = episodes_v2.get("items", [])
            if not isinstance(items, list) or not items:
                break

            for item in items:
                if isinstance(item, dict):
                    episodes.append(item)  # type: ignore[arg-type]

            # Use pagination.totalItems / totalPages when available
            pagination = episodes_v2.get("pagination")
            if isinstance(pagination, dict):
                total_items = pagination.get("totalItems")
                if isinstance(total_items, int) and len(episodes) >= total_items:
                    break
                total_pages = pagination.get("totalPages")
                if isinstance(total_pages, int) and page >= total_pages:
                    break

            # Fallback if pagination metadata is missing or incomplete
            if len(items) < page_size:
                break

            page += 1

        logger.info("Fetched {} episodes total", len(episodes))
        return episodes

    # ------------------------------------------------------------------
    # Public API: show analytics
    # ------------------------------------------------------------------

    def get_show_spotify_stats(
        self,
        show_uri: str | None = None,
        date_range_window: str = "WINDOW_LAST_THIRTY_DAYS",
        include_audience_size: bool = False,
        start_date: Date | str | None = None,
        end_date: Date | str | None = None,
    ) -> JsonDict:
        """
        Fetch daily plays/streams time series for a show on Spotify.

        Replaces the anchor-connector ``plays()`` and ``total_plays()`` methods.

        Parameters
        ----------
        show_uri:
            Spotify show URI.  Resolved automatically when not provided.
        date_range_window:
            One of ``"WINDOW_LAST_SEVEN_DAYS"``, ``"WINDOW_LAST_THIRTY_DAYS"``,
            ``"WINDOW_LAST_NINETY_DAYS"``, ``"WINDOW_ALL_TIME"``.
            Ignored when *start_date* / *end_date* are provided.
        include_audience_size:
            Whether to include the audience size field in the response.
        start_date:
            Inclusive start of a custom date range (``datetime.date`` or
            ``"YYYY-MM-DD"`` string).  Forces ``dateRangeWindow`` to
            ``"WINDOW_CUSTOM"`` when set.
        end_date:
            Inclusive end of a custom date range.  Must be supplied together
            with *start_date*.

        Corresponds to the ``getShowOnSpotifyStats`` persisted query.
        """
        uri = show_uri or self._ensure_show_uri()
        return self._query(
            "getShowOnSpotifyStats",
            variables={
                "showUri": uri,
                **self._resolve_date_range(date_range_window, start_date, end_date),
                "includeAudienceSize": include_audience_size,
            },
            creator_client=CLIENT_ANALYTICS,
        )

    def get_show_spotify_stats_nrt(
        self,
        show_uri: str | None = None,
        date_range_window: str = "WINDOW_LAST_THIRTY_DAYS",
        include_audience_size: bool = False,
        start_date: Date | str | None = None,
        end_date: Date | str | None = None,
    ) -> JsonDict:
        """
        Fetch near-real-time daily plays/streams time series for a show on Spotify.

        Similar to ``get_show_spotify_stats`` but uses the NRT (near-real-time)
        variant which supports ``WINDOW_CUSTOM`` date ranges in addition to the
        standard named windows.

        Parameters
        ----------
        show_uri:
            Spotify show URI.  Resolved automatically when not provided.
        date_range_window:
            One of ``"WINDOW_LAST_SEVEN_DAYS"``, ``"WINDOW_LAST_THIRTY_DAYS"``,
            ``"WINDOW_LAST_NINETY_DAYS"``, ``"WINDOW_ALL_TIME"``,
            ``"WINDOW_CUSTOM"``.  Ignored when *start_date* / *end_date* are
            provided.
        include_audience_size:
            Whether to include the audience size field in the response.
        start_date:
            Inclusive start of a custom date range (``datetime.date`` or
            ``"YYYY-MM-DD"`` string).  Forces ``dateRangeWindow`` to
            ``"WINDOW_CUSTOM"`` when set.
        end_date:
            Inclusive end of a custom date range.  Must be supplied together
            with *start_date*.

        Corresponds to the ``getShowOnSpotifyStatsNRT`` persisted query.
        """
        uri = show_uri or self._ensure_show_uri()
        return self._query(
            "getShowOnSpotifyStatsNRT",
            variables={
                "showUri": uri,
                **self._resolve_date_range(date_range_window, start_date, end_date),
                "includeAudienceSize": include_audience_size,
            },
            creator_client=CLIENT_ANALYTICS,
        )

    def get_show_geo_stats(
        self,
        show_uri: str | None = None,
        date_range_window: str = "WINDOW_LAST_THIRTY_DAYS",
        result_geo: str = "GEO_COUNTRY",
        country: str | None = None,
        region: str | None = None,
        start_date: Date | str | None = None,
        end_date: Date | str | None = None,
    ) -> JsonDict:
        """
        Fetch geographic breakdown of streams across all platforms.

        The same endpoint supports three levels of geographic granularity,
        controlled by *result_geo* and the optional *country* / *region*
        drill-down filters:

        * **Country** (``result_geo="GEO_COUNTRY"``, default) — top-level
          breakdown by country.  *country* and *region* are ignored.
        * **Region** (``result_geo="GEO_REGION"``) — breakdown by
          administrative region (state / province) within a single country.
          Requires *country* (e.g. ``"Germany"``).
        * **City** (``result_geo="GEO_CITY"``) — breakdown by city within a
          single region.  Requires both *country* and *region*
          (e.g. ``country="Germany"``, ``region="Baden-Wurttemberg"``).

        Parameters
        ----------
        show_uri:
            Spotify show URI.  Resolved automatically when not provided.
        date_range_window:
            Time window for the data.  Ignored when *start_date* / *end_date*
            are provided.
        result_geo:
            Granularity level: ``"GEO_COUNTRY"``, ``"GEO_REGION"``, or
            ``"GEO_CITY"``.
        country:
            Country name as returned by the country-level response
            (e.g. ``"Germany"``).  Required for ``GEO_REGION`` and
            ``GEO_CITY``; ignored for ``GEO_COUNTRY``.
        region:
            Region / state name as returned by the region-level response
            (e.g. ``"Baden-Wurttemberg"``).  Required for ``GEO_CITY``;
            ignored otherwise.
        start_date:
            Inclusive start of a custom date range (``datetime.date`` or
            ``"YYYY-MM-DD"`` string).  Forces ``dateRangeWindow`` to
            ``"WINDOW_CUSTOM"`` when set.
        end_date:
            Inclusive end of a custom date range.  Must be supplied together
            with *start_date*.

        Corresponds to the ``getShowAudienceAllPlatformsGeoStats`` persisted query.

        Notes
        -----
        Region- and city-level data may not be available for all shows or date
        ranges.  When the Spotify API returns null for the geo field this
        method normalises it to an empty ``showStreamsAndDownloadsByGeo``
        object and logs a warning.
        """
        if result_geo == "GEO_REGION" and not country:
            raise ValueError("country is required when result_geo='GEO_REGION'")
        if result_geo == "GEO_CITY" and not (country and region):
            raise ValueError("Both country and region are required when result_geo='GEO_CITY'")

        geo_params: JsonDict = {"resultGeo": result_geo}
        if country:
            geo_params["country"] = country
        if region:
            geo_params["region"] = region

        uri = show_uri or self._ensure_show_uri()
        result = self._query(
            "getShowAudienceAllPlatformsGeoStats",
            variables={
                "showUri": uri,
                **self._resolve_date_range(date_range_window, start_date, end_date),
                "geoParams": geo_params,
            },
            creator_client=CLIENT_ANALYTICS,
        )
        # The Spotify API occasionally returns a DataFetchingException for
        # region- and city-level geo, leaving showStreamsAndDownloadsByGeo as
        # null.  Normalise that to an empty object so callers don't have to
        # guard against None.
        show_node = result.get("showByShowUri") if isinstance(result, dict) else None
        if isinstance(show_node, dict) and show_node.get("showStreamsAndDownloadsByGeo") is None:
            logger.warning(
                "getShowAudienceAllPlatformsGeoStats returned null for {} (geo={}, country={}, region={}). "
                "Data may not be available for this show or date range.",
                uri,
                result_geo,
                country,
                region,
            )
            show_node["showStreamsAndDownloadsByGeo"] = {}
        return result

    def get_show_demographics_stats(
        self,
        show_uri: str | None = None,
        date_range_window: str = "WINDOW_LAST_THIRTY_DAYS",
        start_date: Date | str | None = None,
        end_date: Date | str | None = None,
    ) -> JsonDict:
        """
        Fetch age and gender demographics for a show's audience.

        Replaces the anchor-connector ``plays_by_age_range()`` and
        ``plays_by_gender()`` methods.

        Parameters
        ----------
        show_uri:
            Spotify show URI.  Resolved automatically when not provided.
        date_range_window:
            Time window for the data.  Ignored when *start_date* / *end_date*
            are provided.
        start_date:
            Inclusive start of a custom date range (``datetime.date`` or
            ``"YYYY-MM-DD"`` string).  Forces ``dateRangeWindow`` to
            ``"WINDOW_CUSTOM"`` when set.
        end_date:
            Inclusive end of a custom date range.  Must be supplied together
            with *start_date*.

        Corresponds to the ``getShowAudienceDemographicsStats`` persisted query.
        """
        uri = show_uri or self._ensure_show_uri()
        return self._query(
            "getShowAudienceDemographicsStats",
            variables={
                "showUri": uri,
                **self._resolve_date_range(date_range_window, start_date, end_date),
            },
            creator_client=CLIENT_ANALYTICS,
        )

    def get_show_platform_stats(
        self,
        show_uri: str | None = None,
        date_range_window: str = "WINDOW_LAST_THIRTY_DAYS",
        start_date: Date | str | None = None,
        end_date: Date | str | None = None,
    ) -> JsonDict:
        """
        Fetch app and device breakdown of streams across all platforms.

        Replaces the anchor-connector ``plays_by_app()`` and
        ``plays_by_device()`` methods.  The response contains both
        ``showStreamsAndDownloadsByApp`` and ``showStreamsAndDownloadsByDevice``
        in a single call.

        Parameters
        ----------
        show_uri:
            Spotify show URI.  Resolved automatically when not provided.
        date_range_window:
            Time window for the data.  Ignored when *start_date* / *end_date*
            are provided.
        start_date:
            Inclusive start of a custom date range (``datetime.date`` or
            ``"YYYY-MM-DD"`` string).  Forces ``dateRangeWindow`` to
            ``"WINDOW_CUSTOM"`` when set.
        end_date:
            Inclusive end of a custom date range.  Must be supplied together
            with *start_date*.

        Corresponds to the ``getShowAudienceAllPlatformsStats`` persisted query.
        """
        uri = show_uri or self._ensure_show_uri()
        return self._query(
            "getShowAudienceAllPlatformsStats",
            variables={
                "showUri": uri,
                **self._resolve_date_range(date_range_window, start_date, end_date),
            },
            creator_client=CLIENT_ANALYTICS,
        )

    def get_show_impressions_trend(
        self,
        show_uri: str | None = None,
        date_range_window: str = "WINDOW_LAST_THIRTY_DAYS",
        start_date: Date | str | None = None,
        end_date: Date | str | None = None,
    ) -> JsonDict:
        """
        Fetch impressions total and daily time series for a show.

        Replaces the anchor-connector ``impressions()`` method at show level.
        Returns both ``impressionsTotal`` (single count) and ``impressionsDaily``
        (time series of daily impression counts).

        Parameters
        ----------
        show_uri:
            Spotify show URI.  Resolved automatically when not provided.
        date_range_window:
            Time window for the data.  Ignored when *start_date* / *end_date*
            are provided.
        start_date:
            Inclusive start of a custom date range (``datetime.date`` or
            ``"YYYY-MM-DD"`` string).  Forces ``dateRangeWindow`` to
            ``"WINDOW_CUSTOM"`` when set.
        end_date:
            Inclusive end of a custom date range.  Must be supplied together
            with *start_date*.

        Corresponds to the ``getShowImpressionsTrendStats`` persisted query.
        """
        uri = show_uri or self._ensure_show_uri()
        return self._query(
            "getShowImpressionsTrendStats",
            variables={
                "showUri": uri,
                **self._resolve_date_range(date_range_window, start_date, end_date),
            },
            creator_client=CLIENT_ANALYTICS,
        )

    def get_show_audience_discovery(
        self,
        show_uri: str | None = None,
        date_range_window: str = "WINDOW_LAST_THIRTY_DAYS",
        start_date: Date | str | None = None,
        end_date: Date | str | None = None,
    ) -> JsonDict:
        """
        Fetch the audience discovery funnel and key audience metrics for a show.

        Returns the impression → consideration → consumption funnel, total
        audience size, follow rate, and consumption hours per person.

        Replaces the anchor-connector ``audience_size()``,
        ``unique_listeners()``, and ``impressions()`` methods.

        Parameters
        ----------
        show_uri:
            Spotify show URI.  Resolved automatically when not provided.
        date_range_window:
            Time window for the data.  Ignored when *start_date* / *end_date*
            are provided.
        start_date:
            Inclusive start of a custom date range (``datetime.date`` or
            ``"YYYY-MM-DD"`` string).  Forces ``dateRangeWindow`` to
            ``"WINDOW_CUSTOM"`` when set.
        end_date:
            Inclusive end of a custom date range.  Must be supplied together
            with *start_date*.

        Corresponds to the ``getShowAudienceDiscoveryStats`` persisted query.

        Note
        ----
        The Spotify backend does **not** support ``WINDOW_CUSTOM`` for this
        operation — passing a custom date range causes a server-side
        ``DataFetchingException`` for ``audienceSize``, ``audienceFollowRate``,
        ``consumptionHoursPerPerson`` and ``impressionsFunnel``.  When custom
        *start_date* / *end_date* values are supplied we therefore map the
        requested range to the nearest supported predefined window
        (``WINDOW_LAST_SEVEN_DAYS``, ``WINDOW_LAST_THIRTY_DAYS`` or
        ``WINDOW_LAST_NINETY_DAYS``) instead.
        """
        uri = show_uri or self._ensure_show_uri()

        # The server only accepts a fixed set of named windows for this op.
        if start_date is not None and end_date is not None:
            sd = Date.fromisoformat(start_date) if isinstance(start_date, str) else start_date
            ed = Date.fromisoformat(end_date) if isinstance(end_date, str) else end_date
            span_days = max((ed - sd).days + 1, 1)
            if span_days <= 7:
                effective_window = "WINDOW_LAST_SEVEN_DAYS"
            elif span_days <= 30:
                effective_window = "WINDOW_LAST_THIRTY_DAYS"
            else:
                effective_window = "WINDOW_LAST_NINETY_DAYS"
            logger.debug(
                "getShowAudienceDiscoveryStats does not support WINDOW_CUSTOM; "
                "mapping {} → {} ({} days)",
                f"{sd.isoformat()}..{ed.isoformat()}",
                effective_window,
                span_days,
            )
            variables: dict[str, JsonValue] = {
                "showUri": uri,
                "dateRangeWindow": effective_window,
            }
        else:
            variables = {
                "showUri": uri,
                "dateRangeWindow": date_range_window,
            }

        return self._query(
            "getShowAudienceDiscoveryStats",
            variables=variables,
            creator_client=CLIENT_ANALYTICS,
        )

    def get_show_impressions_sources(
        self,
        show_uri: str | None = None,
        date_range_window: str = "WINDOW_LAST_THIRTY_DAYS",
        start_date: Date | str | None = None,
        end_date: Date | str | None = None,
    ) -> JsonDict:
        """
        Fetch impressions broken down by source (Search, Home, Library, Other).

        Parameters
        ----------
        show_uri:
            Spotify show URI.  Resolved automatically when not provided.
        date_range_window:
            Time window for the data.  Ignored when *start_date* / *end_date*
            are provided.
        start_date:
            Inclusive start of a custom date range (``datetime.date`` or
            ``"YYYY-MM-DD"`` string).  Forces ``dateRangeWindow`` to
            ``"WINDOW_CUSTOM"`` when set.
        end_date:
            Inclusive end of a custom date range.  Must be supplied together
            with *start_date*.

        Corresponds to the ``getShowImpressionsSourcesStats`` persisted query.
        """
        uri = show_uri or self._ensure_show_uri()
        return self._query(
            "getShowImpressionsSourcesStats",
            variables={
                "showUri": uri,
                **self._resolve_date_range(date_range_window, start_date, end_date),
            },
            creator_client=CLIENT_ANALYTICS,
        )

    def get_show_top_episodes(
        self,
        show_uri: str | None = None,
    ) -> JsonDict:
        """
        Fetch all-time play counts per episode, ranked by popularity.

        Replaces the anchor-connector ``total_plays_by_episode()`` method.
        Note: this endpoint has no time-range parameter - it always returns
        all-time data.  For per-episode plays within a specific window use
        ``get_episode_plays_daily()`` on each episode URI individually.

        Parameters
        ----------
        show_uri:
            Spotify show URI.  Resolved automatically when not provided.

        Corresponds to the ``getShowTopEpisodes`` persisted query.
        """
        uri = show_uri or self._ensure_show_uri()
        return self._query(
            "getShowTopEpisodes",
            variables={"showUri": uri},
            creator_client=CLIENT_ANALYTICS,
        )

    # ------------------------------------------------------------------
    # Public API: episode analytics
    # ------------------------------------------------------------------

    def get_episode_metadata_for_analytics(
        self,
        episode_uri: str,
    ) -> JsonDict:
        """
        Fetch episode metadata (title, cover art, publish date) for analytics views.

        Replaces the anchor-connector ``episode_metadata()`` method.

        Parameters
        ----------
        episode_uri:
            Spotify episode URI, e.g. ``spotify:episode:4fndadZdKayBwmsRQJ8rNR``.

        Corresponds to the ``getEpisodeMetadataForAnalytics`` persisted query.
        """
        return self._query(
            "getEpisodeMetadataForAnalytics",
            variables={"episodeUri": episode_uri},
            creator_client=CLIENT_PUBLIC,
        )

    def get_episode_performance_all_time(
        self,
        episode_uri: str,
    ) -> JsonDict:
        """
        Fetch the second-by-second retention performance curve for an episode.

        Replaces the anchor-connector ``episode_performance()`` and
        ``episode_aggregated_performance()`` methods.

        Parameters
        ----------
        episode_uri:
            Spotify episode URI.

        Corresponds to the ``getEpisodePerformanceAllTime`` persisted query.
        """
        return self._query(
            "getEpisodePerformanceAllTime",
            variables={"episodeUri": episode_uri},
            creator_client=CLIENT_PUBLIC,
        )

    def get_episode_streams_and_downloads(
        self,
        episode_uri: str,
        date_range_window: str = "WINDOW_LAST_THIRTY_DAYS",
        aggregation_type: str = "AGGREGATION_TYPE_DAILY",
        start_date: Date | str | None = None,
        end_date: Date | str | None = None,
    ) -> JsonDict:
        """
        Fetch streams and downloads time series for an episode.

        Replaces the anchor-connector ``episode_plays()`` method.

        Parameters
        ----------
        episode_uri:
            Spotify episode URI.
        date_range_window:
            Time window for the data.  Ignored when *start_date* / *end_date*
            are provided.
        aggregation_type:
            ``"AGGREGATION_TYPE_DAILY"`` or ``"AGGREGATION_TYPE_WEEKLY"``.
        start_date:
            Inclusive start of a custom date range (``datetime.date`` or
            ``"YYYY-MM-DD"`` string).  Forces ``dateRangeWindow`` to
            ``"WINDOW_CUSTOM"`` when set.
        end_date:
            Inclusive end of a custom date range.  Must be supplied together
            with *start_date*.

        Corresponds to the ``getEpisodeStreamsAndDownloads`` persisted query.
        """
        return self._query(
            "getEpisodeStreamsAndDownloads",
            variables={
                "episodeUri": episode_uri,
                "aggregationType": aggregation_type,
                **self._resolve_date_range(date_range_window, start_date, end_date),
            },
            creator_client=CLIENT_PUBLIC,
        )

    def get_episode_plays_total(
        self,
        episode_uri: str,
        date_range_window: str = "WINDOW_ALL_TIME",
        start_date: Date | str | None = None,
        end_date: Date | str | None = None,
    ) -> JsonDict:
        """
        Fetch total play counts for an episode.

        Parameters
        ----------
        episode_uri:
            Spotify episode URI.
        date_range_window:
            Time window for the data.  Ignored when *start_date* / *end_date*
            are provided.
        start_date:
            Inclusive start of a custom date range (``datetime.date`` or
            ``"YYYY-MM-DD"`` string).  Forces ``dateRangeWindow`` to
            ``"WINDOW_CUSTOM"`` when set.
        end_date:
            Inclusive end of a custom date range.  Must be supplied together
            with *start_date*.

        Corresponds to the ``getEpisodePlaysTotal`` persisted query.
        """
        return self._query(
            "getEpisodePlaysTotal",
            variables={
                "episodeUri": episode_uri,
                **self._resolve_date_range(date_range_window, start_date, end_date),
            },
            creator_client=CLIENT_PUBLIC,
        )

    def get_episode_plays_daily(
        self,
        episode_uri: str,
        date_range_window: str = "WINDOW_LAST_THIRTY_DAYS",
        start_date: Date | str | None = None,
        end_date: Date | str | None = None,
    ) -> JsonDict:
        """
        Fetch daily play counts for an episode.

        Parameters
        ----------
        episode_uri:
            Spotify episode URI.
        date_range_window:
            Time window for the data.  Ignored when *start_date* / *end_date*
            are provided.
        start_date:
            Inclusive start of a custom date range (``datetime.date`` or
            ``"YYYY-MM-DD"`` string).  Forces ``dateRangeWindow`` to
            ``"WINDOW_CUSTOM"`` when set.
        end_date:
            Inclusive end of a custom date range.  Must be supplied together
            with *start_date*.

        Corresponds to the ``getEpisodePlaysDaily`` persisted query.
        """
        return self._query(
            "getEpisodePlaysDaily",
            variables={
                "episodeUri": episode_uri,
                **self._resolve_date_range(date_range_window, start_date, end_date),
            },
            creator_client=CLIENT_PUBLIC,
        )

    def get_episode_impressions_faceted(
        self,
        episode_uri: str,
        date_range_window: str = "WINDOW_LAST_THIRTY_DAYS",
        start_date: Date | str | None = None,
        end_date: Date | str | None = None,
    ) -> JsonDict:
        """
        Fetch impression counts broken down by source (Search, Home, Library, …).

        Replaces the anchor-connector ``impressions()`` method at episode level.

        Parameters
        ----------
        episode_uri:
            Spotify episode URI.
        date_range_window:
            Time window for the data.  Ignored when *start_date* / *end_date*
            are provided.
        start_date:
            Inclusive start of a custom date range (``datetime.date`` or
            ``"YYYY-MM-DD"`` string).  Forces ``dateRangeWindow`` to
            ``"WINDOW_CUSTOM"`` when set.
        end_date:
            Inclusive end of a custom date range.  Must be supplied together
            with *start_date*.

        Corresponds to the ``getEpisodeImpressionsFaceted`` persisted query.
        """
        return self._query(
            "getEpisodeImpressionsFaceted",
            variables={
                "episodeUri": episode_uri,
                **self._resolve_date_range(date_range_window, start_date, end_date),
            },
            creator_client=CLIENT_PUBLIC,
        )

    def get_episode_consumption_all_time(
        self,
        episode_uri: str,
    ) -> JsonDict:
        """
        Fetch all-time consumption stats for an episode.

        Returns total/foreground ms played, consumption hours, and foreground %.

        Parameters
        ----------
        episode_uri:
            Spotify episode URI.

        Corresponds to the ``getEpisodeConsumptionAllTime`` persisted query.
        """
        return self._query(
            "getEpisodeConsumptionAllTime",
            variables={"episodeUri": episode_uri},
            creator_client=CLIENT_PUBLIC,
        )

    def get_episode_consumption(
        self,
        episode_uri: str,
        date_range_window: str = "WINDOW_LAST_THIRTY_DAYS",
        start_date: Date | str | None = None,
        end_date: Date | str | None = None,
    ) -> JsonDict:
        """
        Fetch consumption stats for an episode over a date range.

        Returns both the total (``episodeConsumptionTotal``) and the daily
        time series (``episodeConsumptionDaily``) of ms played, foreground
        ms played, foreground %, and consumption hours for the requested
        window.

        Unlike ``get_episode_consumption_all_time`` (which has no date
        parameters), this query honours ``dateRangeWindow`` / custom
        ``start_date``-``end_date`` ranges.

        Parameters
        ----------
        episode_uri:
            Spotify episode URI.
        date_range_window:
            Named window such as ``"WINDOW_LAST_THIRTY_DAYS"``.  Ignored
            when *start_date* / *end_date* are supplied.
        start_date:
            Inclusive start of a custom date range.  Forces
            ``dateRangeWindow`` to ``"WINDOW_CUSTOM"`` when set.
        end_date:
            Inclusive end of a custom date range.  Must be supplied together
            with *start_date*.

        Corresponds to the ``getEpisodeConsumption`` persisted query.
        """
        return self._query(
            "getEpisodeConsumption",
            variables={
                "episodeUri": episode_uri,
                **self._resolve_date_range(date_range_window, start_date, end_date),
            },
            creator_client=CLIENT_PUBLIC,
        )

    def get_episode_audience_size_all_time(
        self,
        episode_uri: str,
    ) -> JsonDict:
        """
        Fetch all-time unique listener (audience size) stats for an episode.

        Replaces the anchor-connector ``unique_listeners()`` and
        ``audience_size()`` methods at episode level.

        Parameters
        ----------
        episode_uri:
            Spotify episode URI.

        Corresponds to the ``getEpisodeAudienceSizeAllTime`` persisted query.
        """
        return self._query(
            "getEpisodeAudienceSizeAllTime",
            variables={"episodeUri": episode_uri},
            creator_client=CLIENT_PUBLIC,
        )

    # ------------------------------------------------------------------
    # Public API: legacy Anchor REST API
    # ------------------------------------------------------------------

    def get_episode_legacy_web_id(self, episode_id: int | str) -> JsonDict:
        """
        Fetch episode metadata including ``webEpisodeId`` from the legacy Anchor API.

        The Anchor REST API (``api-v5.anchor.fm``) is still accessible using the
        same Spotify OAuth bearer token as the Creators GraphQL API.  It is the
        **only remaining source of** ``webEpisodeId`` (e.g. ``"e3g7a9o"``) and
        ``webStationId`` (e.g. ``"579d39a4"``), which were removed from the
        Spotify Creators GraphQL API.

        Parameters
        ----------
        episode_id:
            The numeric Anchor episode ID (e.g. ``116680440``).  This is
            available as the ``id`` field on episode items returned by
            ``get_all_episodes()`` — verify the exact field name against a
            live API response if needed.

        Returns
        -------
        Full response ``JsonDict`` which includes at minimum:

        - ``webEpisodeId``  — legacy Anchor web episode slug (e.g. ``"e3g7a9o"``)
        - ``webStationId``  — legacy Anchor web station slug (e.g. ``"579d39a4"``)
        - ``spotifyUri``    — canonical Spotify episode URI

        Corresponds to
        ``GET https://api-v5.anchor.fm/v3/episodes/{episode_id}/overview``
        with ``?isMumsCompatible=true&returnWebIds=true``.
        """
        for attempt in range(1, MAX_REQUEST_ATTEMPTS + 1):
            self._ensure_auth()
            assert self._bearer is not None

            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:147.0) "
                    "Gecko/20100101 Firefox/147.0"
                ),
                "Accept": "*/*",
                "Accept-Language": "en",
                "Anchor-API-Version": ANCHOR_LEGACY_API_VERSION,
                "Anchor-Client-Type": "web",
                "Authorization": f"Bearer {self._bearer}",
                "Referer": CREATORS_REFERER,
            }
            url = f"{ANCHOR_LEGACY_API_URL}/v3/episodes/{episode_id}/overview"

            logger.debug(
                "Anchor legacy API episode {} (attempt {}/{})",
                episode_id,
                attempt,
                MAX_REQUEST_ATTEMPTS,
            )
            resp = requests.get(
                url,
                params={"isMumsCompatible": "true", "returnWebIds": "true"},
                headers=headers,
                timeout=60,
            )

            if resp.status_code == 200:
                result: JsonDict = resp.json()
                return result

            if resp.status_code == 401:
                logger.warning("401 Unauthorised (legacy Anchor API) - refreshing token …")
                with self._auth_lock:
                    self._bearer = None
                    self._bearer_expires_at = 0.0
                time.sleep(DELAY_BASE**attempt)
                continue

            if resp.status_code in (429, 502, 503, 504):
                delay = DELAY_BASE**attempt
                logger.warning(
                    "HTTP {} on legacy Anchor API episode {} - retrying in {:.1f}s …",
                    resp.status_code,
                    episode_id,
                    delay,
                )
                time.sleep(delay)
                continue

            resp.raise_for_status()

        raise MaxRetriesException(
            f"All {MAX_REQUEST_ATTEMPTS} attempts failed for legacy Anchor episode {episode_id}"
        )

    def get_external_partner_id(self, partner_name: str) -> JsonDict:
        """
        Fetch an external partner ID for the authenticated user.

        Parameters
        ----------
        partner_name:
            The partner slug, e.g. ``"s4p-mparticle-braze"``.

        Corresponds to the ``WebGetExternalPartnerId`` persisted query.
        """
        return self._query(
            "WebGetExternalPartnerId",
            variables={"partnerName": partner_name},
        )
