"""
Command-line interface for the Spotify GraphQL Connector.

Runs every supported endpoint and logs the responses with loguru.

Usage
-----
    uv run spotifygraphqlconnector

    # or directly:
    python -m spotifygraphqlconnector

Environment variables
---------------------
SPOTIFY_SP_DC        (required)
    The ``sp_dc`` cookie value from an active Spotify session.
    Log in to https://creators.spotify.com, open DevTools → Application →
    Cookies → https://accounts.spotify.com and copy the ``sp_dc`` value.

SPOTIFY_SP_KEY       (required)
    The ``sp_key`` cookie value from the same Spotify session.
    Found alongside ``sp_dc`` under https://accounts.spotify.com cookies.

SPOTIFY_SHOW_URI     (optional)
    Spotify show URI, e.g. ``spotify:show:1HaFboRBVORs2VCpNACYLn``.
    When omitted the connector resolves the first show owned by the
    authenticated user automatically.

SPOTIFY_STATION_ID   (optional, DEPRECATED)
    Numeric Anchor/Spotify station ID.
    No longer used by the episode-list endpoint (Spotify migrated
    ``WebGetIndexedEpisodeList`` from ``stationId`` to ``showUri`` in
    April 2026).  Still accepted for backwards compatibility and exposed
    on the connector instance, but ignored by ``get_episode_list()`` and
    ``get_all_episodes()``.  Prefer ``SPOTIFY_SHOW_URI`` instead.

SPOTIFY_COUNTRY_CODE (optional, default: "US")
    ISO 3166-1 alpha-2 country code used for the registration endpoint.

SPOTIFY_GEO_COUNTRY  (optional)
    Country name (as returned by the country-level geo stats response,
    e.g. ``"Germany"``) used to drill down into region-level geo stats.
    When set, the connector also fetches ``GEO_REGION`` data for that country.
    Must be set together with SPOTIFY_GEO_REGION to also fetch city-level data.

SPOTIFY_GEO_REGION   (optional)
    Region / state name (as returned by the region-level geo stats response,
    e.g. ``"Baden-Wurttemberg"``) used to drill down into city-level geo stats.
    Requires SPOTIFY_GEO_COUNTRY to also be set.

SPOTIFY_START_DATE   (optional, format: YYYY-MM-DD)
    Start of a custom date range for all analytics calls.
    Must be set together with SPOTIFY_END_DATE.
    When set, overrides the default WINDOW_LAST_THIRTY_DAYS window.

SPOTIFY_END_DATE     (optional, format: YYYY-MM-DD)
    End of a custom date range (inclusive) for all analytics calls.
    Must be set together with SPOTIFY_START_DATE.

SPOTIFY_OUTPUT_DIR   (optional)
    Directory to write each query result as a separate JSON file.
    The directory is created if it does not exist.
    When omitted, results are only logged to stdout.
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import date as Date
from datetime import datetime
from pathlib import Path
from typing import Any

from loguru import logger

from .connector import CredentialsExpired, SpotifyGraphQLConnector

# Default date range window used for all analytics calls
DEFAULT_DATE_RANGE = "WINDOW_LAST_THIRTY_DAYS"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _parse_date(value: str | None, name: str) -> Date | None:
    """Parse an ISO-format date string from an environment variable."""
    if not value:
        return None
    try:
        return Date.fromisoformat(value)
    except ValueError:
        logger.error(
            "Environment variable {} has an invalid date value: {!r} (expected YYYY-MM-DD).",
            name,
            value,
        )
        sys.exit(1)


def _load_env(name: str, default: str | None = None) -> str:
    """Return the value of an environment variable, or raise if it is unset."""
    value = os.environ.get(name)
    if not value:
        if default is not None:
            logger.warning(
                "Environment variable {} is not set - using default: {}",
                name,
                default,
            )
            return default
        logger.error("Required environment variable {} is not set.", name)
        sys.exit(1)
    return value


def _label_to_filename(label: str) -> str:
    """Convert a query label into a safe snake_case filename (no extension)."""
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", label).strip("_").lower()
    return slug


def _log_result(
    label: str, data: object, output_dir: Path | None = None, suffix: str | None = None
) -> None:
    """Pretty-print a result dict via loguru and optionally write it to a file."""
    pretty = json.dumps(data, indent=2, default=str)
    logger.info("{} =\n{}", label, pretty)
    if output_dir is not None:
        stem = _label_to_filename(label)
        if suffix:
            stem = f"{stem}_{suffix}"
        dest = output_dir / (stem + ".json")
        dest.write_text(pretty, encoding="utf-8")
        logger.debug("Wrote {} to {}", label, dest)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    # ------------------------------------------------------------------
    # Configuration from environment
    # ------------------------------------------------------------------
    _raw_output_dir = os.environ.get("SPOTIFY_OUTPUT_DIR")
    output_dir: Path | None = None
    if _raw_output_dir:
        output_dir = Path(_raw_output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        logger.info("Output directory: {}", output_dir.resolve())

    # ------------------------------------------------------------------
    sp_dc = _load_env("SPOTIFY_SP_DC")
    sp_key = _load_env("SPOTIFY_SP_KEY")
    show_uri = os.environ.get("SPOTIFY_SHOW_URI") or None
    station_id = os.environ.get("SPOTIFY_STATION_ID") or None
    country_code = _load_env("SPOTIFY_COUNTRY_CODE", "US")
    geo_country = os.environ.get("SPOTIFY_GEO_COUNTRY") or None
    geo_region = os.environ.get("SPOTIFY_GEO_REGION") or None
    start_date = _parse_date(os.environ.get("SPOTIFY_START_DATE"), "SPOTIFY_START_DATE")
    end_date = _parse_date(os.environ.get("SPOTIFY_END_DATE"), "SPOTIFY_END_DATE")

    if (start_date is None) != (end_date is None):
        logger.error("SPOTIFY_START_DATE and SPOTIFY_END_DATE must be set together or not at all.")
        sys.exit(1)

    if start_date and end_date:
        date_range_window = "WINDOW_CUSTOM"
        logger.info(
            "Using custom date range: {} – {}", start_date.isoformat(), end_date.isoformat()
        )
    else:
        date_range_window = DEFAULT_DATE_RANGE
        logger.info("Using date range window: {}", date_range_window)

    connector = SpotifyGraphQLConnector(
        sp_dc=sp_dc,
        sp_key=sp_key,
        show_uri=show_uri,
        station_id=station_id,
    )

    logger.info(
        "Starting Spotify GraphQL Connector - {}",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    # Shared date-range kwargs passed to every analytics method that supports them.
    dr_kwargs: dict[str, Any] = (
        {"start_date": start_date, "end_date": end_date}
        if start_date
        else {"date_range_window": date_range_window}
    )

    try:
        # ------------------------------------------------------------------
        # User / account level
        # ------------------------------------------------------------------
        logger.info("--- User Metadata ---")
        _log_result("getUserMetadata", connector.get_user_metadata(), output_dir)

        logger.info("--- User Shows ---")
        _log_result("WebGetUserShows", connector.get_user_shows(), output_dir)

        logger.info("--- Shows For User (rich) ---")
        _log_result("getShowsForUser", connector.get_shows_for_user(), output_dir)

        logger.info("--- User And Shows ---")
        _log_result("WebGetUserAndShows", connector.get_user_and_shows(), output_dir)

        logger.info("--- User Registration ---")
        _log_result(
            "WebGetUserRegistration",
            connector.get_user_registration(country_code=country_code),
            output_dir,
        )

        # ------------------------------------------------------------------
        # Show level  (show_uri resolved automatically if not set)
        # ------------------------------------------------------------------
        logger.info("--- Show Type ---")
        _log_result("WebGetShowTypeByUri", connector.get_show_type(), output_dir)

        logger.info("--- Show Overview Stats (NRT) ---")
        _log_result("getShowOverviewStatsNRT", connector.get_show_overview_stats(), output_dir)

        logger.info("--- Show Clips ---")
        _log_result("getShowClips", connector.get_show_clips(), output_dir)

        logger.info("--- Monetisation Lifecycle State ---")
        _log_result(
            "WebGetMonetizationLifecycleState",
            connector.get_monetization_lifecycle_state(),
            output_dir,
        )

        # ------------------------------------------------------------------
        # Show analytics
        # ------------------------------------------------------------------
        logger.info("--- Show Spotify Stats (plays/streams daily) ---")
        _log_result(
            "getShowOnSpotifyStats",
            connector.get_show_spotify_stats(**dr_kwargs),
            output_dir,
        )

        # NRT (near-real-time) variant of the Spotify stats endpoint.
        # Key differences from getShowOnSpotifyStats:
        #   - Data is refreshed more frequently (near-real-time vs. daily batch).
        #   - Supports WINDOW_CUSTOM date ranges in addition to the standard named
        #     windows, making it the preferred choice when start_date/end_date are set.
        # For historical/trend analysis over a standard window the non-NRT variant
        # may return slightly more stable/deduplicated numbers.
        logger.info("--- Show Spotify Stats NRT (near-real-time plays/streams) ---")
        _log_result(
            "getShowOnSpotifyStatsNRT",
            connector.get_show_spotify_stats_nrt(**dr_kwargs),
            output_dir,
        )

        logger.info("--- Show Geo Stats (country) ---")
        _log_result(
            "getShowAudienceAllPlatformsGeoStats_country",
            connector.get_show_geo_stats(result_geo="GEO_COUNTRY", **dr_kwargs),
            output_dir,
        )

        if geo_country:
            logger.info("--- Show Geo Stats (region, country={}) ---", geo_country)
            _log_result(
                "getShowAudienceAllPlatformsGeoStats_region",
                connector.get_show_geo_stats(
                    result_geo="GEO_REGION",
                    country=geo_country,
                    **dr_kwargs,
                ),
                output_dir,
            )

            if geo_region:
                logger.info(
                    "--- Show Geo Stats (city, country={}, region={}) ---",
                    geo_country,
                    geo_region,
                )
                _log_result(
                    "getShowAudienceAllPlatformsGeoStats_city",
                    connector.get_show_geo_stats(
                        result_geo="GEO_CITY",
                        country=geo_country,
                        region=geo_region,
                        **dr_kwargs,
                    ),
                    output_dir,
                )
        else:
            logger.info(
                "SPOTIFY_GEO_COUNTRY not set — skipping region and city geo stats. "
                "Set SPOTIFY_GEO_COUNTRY (and optionally SPOTIFY_GEO_REGION) to enable."
            )

        logger.info("--- Show Demographics Stats (age + gender) ---")
        _log_result(
            "getShowAudienceDemographicsStats",
            connector.get_show_demographics_stats(**dr_kwargs),
            output_dir,
        )

        logger.info("--- Show Platform Stats (app + device) ---")
        _log_result(
            "getShowAudienceAllPlatformsStats",
            connector.get_show_platform_stats(**dr_kwargs),
            output_dir,
        )

        logger.info("--- Show Impressions Trend ---")
        _log_result(
            "getShowImpressionsTrendStats",
            connector.get_show_impressions_trend(**dr_kwargs),
            output_dir,
        )

        logger.info("--- Show Audience Discovery (funnel + audience size + follow rate) ---")
        _log_result(
            "getShowAudienceDiscoveryStats",
            connector.get_show_audience_discovery(**dr_kwargs),
            output_dir,
        )

        logger.info("--- Show Impressions Sources ---")
        _log_result(
            "getShowImpressionsSourcesStats",
            connector.get_show_impressions_sources(**dr_kwargs),
            output_dir,
        )

        logger.info("--- Show Top Episodes (all-time plays per episode) ---")
        _log_result(
            "getShowTopEpisodes",
            connector.get_show_top_episodes(),
            output_dir,
        )

        # ------------------------------------------------------------------
        # Episode list  (station_id resolved automatically if not set)
        # ------------------------------------------------------------------
        logger.info("--- Episode List (page 1) ---")
        _log_result(
            "WebGetIndexedEpisodeList",
            connector.get_episode_list(current_page=1, page_size=10),
            output_dir,
        )

        logger.info("--- All Episodes (auto-paginated) ---")
        all_episodes = connector.get_all_episodes()
        _log_result("all_episodes", all_episodes, output_dir)
        logger.success("Fetched {} episodes in total.", len(all_episodes))

        # ------------------------------------------------------------------
        # Episode analytics - use the first episode from the list
        # ------------------------------------------------------------------
        episode_uri: str | None = os.environ.get("SPOTIFY_EPISODE_URI") or None
        # The numeric Anchor episode ID — needed to call the legacy Anchor API.
        # It is available as the "id" field on items returned by get_all_episodes()
        # (WebGetIndexedEpisodeList).  Verify the exact field name against a live
        # API response; common alternatives are "stationEpisodeId" or "episodeId".
        first_episode_numeric_id: int | str | None = None
        if episode_uri is None and all_episodes:
            first = all_episodes[0]
            episode_uri = str(first.get("uri", "")) or None
            first_episode_numeric_id = first.get("id")  # type: ignore[assignment]
            if episode_uri:
                logger.info("Using first episode for analytics: {}", episode_uri)

        if episode_uri:
            # Use the last segment of the URI (the bare ID) as a filename suffix
            # e.g. "spotify:episode:ABC123" → "ABC123"
            episode_id = episode_uri.rsplit(":", 1)[-1]

            logger.info("--- Episode Metadata (for analytics) ---")
            _log_result(
                "getEpisodeMetadataForAnalytics",
                connector.get_episode_metadata_for_analytics(episode_uri),
                output_dir,
                suffix=episode_id,
            )

            logger.info("--- Episode Performance All Time ---")
            _log_result(
                "getEpisodePerformanceAllTime",
                connector.get_episode_performance_all_time(episode_uri),
                output_dir,
                suffix=episode_id,
            )

            logger.info("--- Episode Streams & Downloads ---")
            _log_result(
                "getEpisodeStreamsAndDownloads",
                connector.get_episode_streams_and_downloads(episode_uri, **dr_kwargs),
                output_dir,
                suffix=episode_id,
            )

            logger.info("--- Episode Plays Daily ---")
            _log_result(
                "getEpisodePlaysDaily",
                connector.get_episode_plays_daily(episode_uri, **dr_kwargs),
                output_dir,
                suffix=episode_id,
            )

            logger.info("--- Episode Impressions (faceted) ---")
            _log_result(
                "getEpisodeImpressionsFaceted",
                connector.get_episode_impressions_faceted(episode_uri, **dr_kwargs),
                output_dir,
                suffix=episode_id,
            )

            logger.info("--- Episode Consumption All Time ---")
            _log_result(
                "getEpisodeConsumptionAllTime",
                connector.get_episode_consumption_all_time(episode_uri),
                output_dir,
                suffix=episode_id,
            )

            logger.info("--- Episode Consumption (date range) ---")
            _log_result(
                "getEpisodeConsumption",
                connector.get_episode_consumption(episode_uri, **dr_kwargs),
                output_dir,
                suffix=episode_id,
            )

            logger.info("--- Episode Audience Size All Time ---")
            _log_result(
                "getEpisodeAudienceSizeAllTime",
                connector.get_episode_audience_size_all_time(episode_uri),
                output_dir,
                suffix=episode_id,
            )

            # ------------------------------------------------------------------
            # Legacy Anchor API — webEpisodeId / webStationId
            #
            # webEpisodeId (e.g. "e3g7a9o") was removed from the Spotify
            # Creators GraphQL API but is still required by the DB schema.
            # The legacy Anchor REST API is the only remaining source for it.
            # We pass the numeric Anchor episode ID obtained from the episode
            # list above; if the field name turns out to be different in a live
            # response, adjust first.get("id") in the block above accordingly.
            # ------------------------------------------------------------------
            if first_episode_numeric_id is not None:
                logger.info("--- Episode Legacy Web ID (Anchor API) ---")
                _log_result(
                    "getEpisodeLegacyWebId",
                    connector.get_episode_legacy_web_id(first_episode_numeric_id),
                    output_dir,
                    suffix=episode_id,
                )
            else:
                logger.warning(
                    "Numeric Anchor episode ID not found in episode data "
                    "(checked field 'id') — skipping legacy web ID lookup. "
                    "Inspect the all_episodes.json output to find the correct field name."
                )
        else:
            logger.warning("No episode URI available - skipping episode analytics.")

    except CredentialsExpired as exc:
        logger.error(
            "Authentication failed - sp_dc cookie has expired.\n{}\n"
            "Please update SPOTIFY_SP_DC with a fresh cookie value.",
            exc,
        )
        sys.exit(1)
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unexpected error: {}", exc)
        sys.exit(1)

    logger.success("Done.")


if __name__ == "__main__":
    main()
