"""
Type definitions for the Spotify GraphQL Connector.

All types are modelled to closely mirror the native Spotify Creators GraphQL
API responses so that consumers can adapt to the raw shape of the data.
"""

from __future__ import annotations

from typing import TypeAlias

# ---------------------------------------------------------------------------
# Primitive recursive JSON type
# ---------------------------------------------------------------------------

JsonValue: TypeAlias = "str | int | float | bool | None | list[JsonValue] | dict[str, JsonValue]"
JsonDict: TypeAlias = "dict[str, JsonValue]"


# ---------------------------------------------------------------------------
# Persisted-query operation names and their sha256 hashes
# ---------------------------------------------------------------------------

OPERATION_HASHES: dict[str, str] = {
    # --- user / account ---
    "getUserMetadata": "f8e54c8841602e6a1712b02776a70c289bc3f1e8661b77c8ddea6e5912ee4287",
    "WebGetUserShows": "e5b72190d76dacc4d93ac4c01489f33116e7885890c95241f2f3ede11d9eca11",
    "WebGetUserAndShows": "cf421f56b9ab0910269f4029e7f7fbc5097fb73f7687b7927ffcd5064f2aaf21",
    "WebGetUserRegistration": "ce98ffc51a07f15df4dcce6c40ed0dc320471e0f29ef28f7fe651252e191aec2",
    "WebGetExternalPartnerId": "4f46a6d85e4ff29760dfe7b93050d2fd6dfccb7d5ea45bf718fd1d968dbeb826",
    # --- show discovery (analytics microfrontend) ---
    # Returns richer show data: authorName, category, description, hostingProvider
    "getShowsForUser": "95c6ed0306a2e7fe00f00563a5a3beb6a58797ddf74da833be0b77c29283be62",
    # --- show metadata ---
    "WebGetShowTypeByUri": "aecbba024ed4d62919387f7d45ae102537a0f8c58e9f6d48503cbfe4b1046247",
    "WebGetMonetizationLifecycleState": "707ff5526827a68b07435ea9c39039cf1b6eceb2ff24abc3da432df8cbf09672",
    "getShowClips": "e568e6b1bc1844bc27b5e0262947926ed4b2e7a29e6911604e47cf9b8a1e2dbd",
    # --- show analytics (microfrontend-analytics client) ---
    # Plays/streams time series + optional audience size
    "getShowOnSpotifyStats": "9910af3f474a8733f79e04f58ccb81a78c0065737bae17c3ce670f77e1216c37",
    # Near-real-time plays/streams time series + optional audience size (supports WINDOW_CUSTOM)
    "getShowOnSpotifyStatsNRT": "1b45317a124d159de6a8c030d87b2968ced224b301f025268a3783db7d844a18",
    # Geo breakdown of streams across all platforms
    "getShowAudienceAllPlatformsGeoStats": "88fcde1673093a27d5915209d861d2413902f322a0a672478ae823fc957319c7",
    # Age + gender demographics
    "getShowAudienceDemographicsStats": "f5d7195822edfd4796a97674cea46bc0015da7a795aba849eb410139d4b40573",
    # App + device breakdown across all platforms
    "getShowAudienceAllPlatformsStats": "ee86edbac9d7f0dbc587b10a778658e3097b30826705ba237f9755dfd2a47e3a",
    # Impressions daily time series + total count
    "getShowImpressionsTrendStats": "25ef2a881e05475ba547183a4b971d277f474be95861dc1c24fdc9a13ff6f530",
    # Audience discovery funnel: reached → interested → consumed + audience size + follow rate
    "getShowAudienceDiscoveryStats": "9bdb7a5a1fa5d456939344b349cdbeca2676321093a8e3059749e952461e1e74",
    # Impressions broken down by source (Search, Home, Library, Other)
    "getShowImpressionsSourcesStats": "e773c8e6a388a69f29b405d13642187c871127f61ca0520a69087775e2abff42",
    # All-time per-episode play counts ranked by popularity (no time range parameter)
    "getShowTopEpisodes": "7f0f4dc6869de6c2fa05e08850d87d12b3b3a0fb44792b852bfbc74bad4fcf0e",
    # Near-real-time overview (streams/downloads total)
    "getShowOverviewStatsNRT": "73886721739bbcad6b416a18cfa750250e5039077be0f383a77172f456d0ee39",
    # Show streams & downloads all time
    "getShowAllPlatformsStatsNRT": "a305842e6b2c6ad04a4e568e3bf45b3fcbfe2c85aa484f14a2df94446467492c",
    # --- episode list ---
    "WebGetIndexedEpisodeList": "3788960e6d466f984f2f8349eece3894d818eb2ade198ef5294b92a86fe963d2",
    # --- episode analytics (public-website client) ---
    # Episode performance curve (second-by-second retention) all time
    "getEpisodePerformanceAllTime": "55201900cdba8c65ac62dfeb48a3ad38a595206e9130e3b56e010ea5add906a0",
    # Episode metadata (title, cover art, publish date) for analytics views
    "getEpisodeMetadataForAnalytics": "9c887e38027a9b121ca64a4600f2ad1b82b74108a0d4cd61bc2372d300f5f800",
    # Episode streams & downloads time series (daily or other aggregation)
    "getEpisodeStreamsAndDownloads": "b798bdc1367bdbc805b520d0103db981ad9fe7c602eedb187e9434351c969737",
    # Episode plays total
    "getEpisodePlaysTotal": "c888657ba7e5e9169561123aa5b7b4001110049b17fd9204c11c52f8e28b7e96",
    # Episode plays daily time series
    "getEpisodePlaysDaily": "7e9550d103f2aa9ebfe564c3389324e991f752ec1ed498923113331ad401c52c",
    # Episode impressions broken down by source (search, home, library, …)
    "getEpisodeImpressionsFaceted": "9ca243fbcee851d936f8f7a7a87ed9480a0b600c9c22659fbbde1304fab67881",
    # Episode consumption all time (ms played, foreground %, hours)
    "getEpisodeConsumptionAllTime": "a57d14960f5c47de98bbbfb72ea30a0de131d3ed97c7464e3537da226ee94a1b",
    # Episode consumption for a date range (total + daily time series)
    "getEpisodeConsumption": "a0b691d7492605e327d707f18f214d8ea4ec5283a74454524c119763ace4e0c0",
    # Episode audience size all time (unique listeners, foreground %)
    "getEpisodeAudienceSizeAllTime": "e5bd6e45a6e52bc91dec6c5e46b4b89a21c0c5095fa14f1202e5a93b076b70ba",
}

# The base URL for the Spotify Creators GraphQL persisted-query endpoint
GRAPHQL_URL = "https://creators-graph.spotify.com/v2/graph-pq"

# The OAuth token exchange URL
TOKEN_URL = "https://accounts.spotify.com/api/token"

# The OAuth authorise URL
AUTH_URL = "https://accounts.spotify.com/oauth2/v2/auth"

# Spotify Creators OAuth client ID (stable public value used by the web app)
SPOTIFY_CLIENT_ID = "05a1371ee5194c27860b3ff3ff3979d2"

# OAuth redirect URI - must match what the Spotify auth server expects
OAUTH_REDIRECT_URI = "https://podcasters.spotify.com"

# OAuth scopes required by the Spotify Creators web app
OAUTH_SCOPE = "streaming ugc-image-upload user-read-email user-read-private"

# Referer / Origin used by the Spotify Creators web app
CREATORS_ORIGIN = "https://creators.spotify.com"
CREATORS_REFERER = "https://creators.spotify.com/"

# x-creator-client header values observed in the wild
CLIENT_SHELL = "podcasters-shell-app"
CLIENT_PUBLIC = "public-website"
CLIENT_ANALYTICS = "microfrontend-analytics"

# Legacy Anchor REST API (api-v5.anchor.fm).
# Still accessible with the same Spotify OAuth bearer token and is the only
# remaining source of webEpisodeId / webStationId, which were removed from
# the Spotify Creators GraphQL API.
ANCHOR_LEGACY_API_URL = "https://api-v5.anchor.fm"
ANCHOR_LEGACY_API_VERSION = "3.8.3"
