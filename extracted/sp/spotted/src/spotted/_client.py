# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
    not_given,
)
from ._utils import (
    is_given,
    is_mapping_t,
    get_async_library,
)
from ._compat import cached_property
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import SpottedError, APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

if TYPE_CHECKING:
    from .resources import (
        me,
        shows,
        users,
        albums,
        browse,
        search,
        tracks,
        artists,
        markets,
        chapters,
        episodes,
        playlists,
        audiobooks,
        audio_analysis,
        audio_features,
        recommendations,
    )
    from .resources.me.me import MeResource, AsyncMeResource
    from .resources.shows import ShowsResource, AsyncShowsResource
    from .resources.albums import AlbumsResource, AsyncAlbumsResource
    from .resources.search import SearchResource, AsyncSearchResource
    from .resources.tracks import TracksResource, AsyncTracksResource
    from .resources.artists import ArtistsResource, AsyncArtistsResource
    from .resources.markets import MarketsResource, AsyncMarketsResource
    from .resources.chapters import ChaptersResource, AsyncChaptersResource
    from .resources.episodes import EpisodesResource, AsyncEpisodesResource
    from .resources.audiobooks import AudiobooksResource, AsyncAudiobooksResource
    from .resources.users.users import UsersResource, AsyncUsersResource
    from .resources.browse.browse import BrowseResource, AsyncBrowseResource
    from .resources.audio_analysis import AudioAnalysisResource, AsyncAudioAnalysisResource
    from .resources.audio_features import AudioFeaturesResource, AsyncAudioFeaturesResource
    from .resources.recommendations import RecommendationsResource, AsyncRecommendationsResource
    from .resources.playlists.playlists import PlaylistsResource, AsyncPlaylistsResource

__all__ = ["Timeout", "Transport", "ProxiesTypes", "RequestOptions", "Spotted", "AsyncSpotted", "Client", "AsyncClient"]


class Spotted(SyncAPIClient):
    # client options
    access_token: str

    def __init__(
        self,
        *,
        access_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous Spotted client instance.

        This automatically infers the `access_token` argument from the `SPOTIFY_ACCESS_TOKEN` environment variable if it is not provided.
        """
        if access_token is None:
            access_token = os.environ.get("SPOTIFY_ACCESS_TOKEN")
        if access_token is None:
            raise SpottedError(
                "The access_token client option must be set either by passing access_token to the client or by setting the SPOTIFY_ACCESS_TOKEN environment variable"
            )
        self.access_token = access_token

        if base_url is None:
            base_url = os.environ.get("SPOTTED_BASE_URL")
        if base_url is None:
            base_url = f"https://api.spotify.com/v1"

        custom_headers_env = os.environ.get("SPOTTED_CUSTOM_HEADERS")
        if custom_headers_env is not None:
            parsed: dict[str, str] = {}
            for line in custom_headers_env.split("\n"):
                colon = line.find(":")
                if colon >= 0:
                    parsed[line[:colon].strip()] = line[colon + 1 :].strip()
            default_headers = {**parsed, **(default_headers if is_mapping_t(default_headers) else {})}

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

    @cached_property
    def albums(self) -> AlbumsResource:
        from .resources.albums import AlbumsResource

        return AlbumsResource(self)

    @cached_property
    def artists(self) -> ArtistsResource:
        from .resources.artists import ArtistsResource

        return ArtistsResource(self)

    @cached_property
    def shows(self) -> ShowsResource:
        from .resources.shows import ShowsResource

        return ShowsResource(self)

    @cached_property
    def episodes(self) -> EpisodesResource:
        from .resources.episodes import EpisodesResource

        return EpisodesResource(self)

    @cached_property
    def audiobooks(self) -> AudiobooksResource:
        from .resources.audiobooks import AudiobooksResource

        return AudiobooksResource(self)

    @cached_property
    def me(self) -> MeResource:
        from .resources.me import MeResource

        return MeResource(self)

    @cached_property
    def chapters(self) -> ChaptersResource:
        from .resources.chapters import ChaptersResource

        return ChaptersResource(self)

    @cached_property
    def tracks(self) -> TracksResource:
        from .resources.tracks import TracksResource

        return TracksResource(self)

    @cached_property
    def search(self) -> SearchResource:
        from .resources.search import SearchResource

        return SearchResource(self)

    @cached_property
    def playlists(self) -> PlaylistsResource:
        from .resources.playlists import PlaylistsResource

        return PlaylistsResource(self)

    @cached_property
    def users(self) -> UsersResource:
        from .resources.users import UsersResource

        return UsersResource(self)

    @cached_property
    def browse(self) -> BrowseResource:
        from .resources.browse import BrowseResource

        return BrowseResource(self)

    @cached_property
    def audio_features(self) -> AudioFeaturesResource:
        from .resources.audio_features import AudioFeaturesResource

        return AudioFeaturesResource(self)

    @cached_property
    def audio_analysis(self) -> AudioAnalysisResource:
        from .resources.audio_analysis import AudioAnalysisResource

        return AudioAnalysisResource(self)

    @cached_property
    def recommendations(self) -> RecommendationsResource:
        from .resources.recommendations import RecommendationsResource

        return RecommendationsResource(self)

    @cached_property
    def markets(self) -> MarketsResource:
        from .resources.markets import MarketsResource

        return MarketsResource(self)

    @cached_property
    def with_raw_response(self) -> SpottedWithRawResponse:
        return SpottedWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SpottedWithStreamedResponse:
        return SpottedWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        access_token = self.access_token
        return {"Authorization": f"Bearer {access_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        access_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            access_token=access_token or self.access_token,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncSpotted(AsyncAPIClient):
    # client options
    access_token: str

    def __init__(
        self,
        *,
        access_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncSpotted client instance.

        This automatically infers the `access_token` argument from the `SPOTIFY_ACCESS_TOKEN` environment variable if it is not provided.
        """
        if access_token is None:
            access_token = os.environ.get("SPOTIFY_ACCESS_TOKEN")
        if access_token is None:
            raise SpottedError(
                "The access_token client option must be set either by passing access_token to the client or by setting the SPOTIFY_ACCESS_TOKEN environment variable"
            )
        self.access_token = access_token

        if base_url is None:
            base_url = os.environ.get("SPOTTED_BASE_URL")
        if base_url is None:
            base_url = f"https://api.spotify.com/v1"

        custom_headers_env = os.environ.get("SPOTTED_CUSTOM_HEADERS")
        if custom_headers_env is not None:
            parsed: dict[str, str] = {}
            for line in custom_headers_env.split("\n"):
                colon = line.find(":")
                if colon >= 0:
                    parsed[line[:colon].strip()] = line[colon + 1 :].strip()
            default_headers = {**parsed, **(default_headers if is_mapping_t(default_headers) else {})}

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

    @cached_property
    def albums(self) -> AsyncAlbumsResource:
        from .resources.albums import AsyncAlbumsResource

        return AsyncAlbumsResource(self)

    @cached_property
    def artists(self) -> AsyncArtistsResource:
        from .resources.artists import AsyncArtistsResource

        return AsyncArtistsResource(self)

    @cached_property
    def shows(self) -> AsyncShowsResource:
        from .resources.shows import AsyncShowsResource

        return AsyncShowsResource(self)

    @cached_property
    def episodes(self) -> AsyncEpisodesResource:
        from .resources.episodes import AsyncEpisodesResource

        return AsyncEpisodesResource(self)

    @cached_property
    def audiobooks(self) -> AsyncAudiobooksResource:
        from .resources.audiobooks import AsyncAudiobooksResource

        return AsyncAudiobooksResource(self)

    @cached_property
    def me(self) -> AsyncMeResource:
        from .resources.me import AsyncMeResource

        return AsyncMeResource(self)

    @cached_property
    def chapters(self) -> AsyncChaptersResource:
        from .resources.chapters import AsyncChaptersResource

        return AsyncChaptersResource(self)

    @cached_property
    def tracks(self) -> AsyncTracksResource:
        from .resources.tracks import AsyncTracksResource

        return AsyncTracksResource(self)

    @cached_property
    def search(self) -> AsyncSearchResource:
        from .resources.search import AsyncSearchResource

        return AsyncSearchResource(self)

    @cached_property
    def playlists(self) -> AsyncPlaylistsResource:
        from .resources.playlists import AsyncPlaylistsResource

        return AsyncPlaylistsResource(self)

    @cached_property
    def users(self) -> AsyncUsersResource:
        from .resources.users import AsyncUsersResource

        return AsyncUsersResource(self)

    @cached_property
    def browse(self) -> AsyncBrowseResource:
        from .resources.browse import AsyncBrowseResource

        return AsyncBrowseResource(self)

    @cached_property
    def audio_features(self) -> AsyncAudioFeaturesResource:
        from .resources.audio_features import AsyncAudioFeaturesResource

        return AsyncAudioFeaturesResource(self)

    @cached_property
    def audio_analysis(self) -> AsyncAudioAnalysisResource:
        from .resources.audio_analysis import AsyncAudioAnalysisResource

        return AsyncAudioAnalysisResource(self)

    @cached_property
    def recommendations(self) -> AsyncRecommendationsResource:
        from .resources.recommendations import AsyncRecommendationsResource

        return AsyncRecommendationsResource(self)

    @cached_property
    def markets(self) -> AsyncMarketsResource:
        from .resources.markets import AsyncMarketsResource

        return AsyncMarketsResource(self)

    @cached_property
    def with_raw_response(self) -> AsyncSpottedWithRawResponse:
        return AsyncSpottedWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSpottedWithStreamedResponse:
        return AsyncSpottedWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        access_token = self.access_token
        return {"Authorization": f"Bearer {access_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        access_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            access_token=access_token or self.access_token,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class SpottedWithRawResponse:
    _client: Spotted

    def __init__(self, client: Spotted) -> None:
        self._client = client

    @cached_property
    def albums(self) -> albums.AlbumsResourceWithRawResponse:
        from .resources.albums import AlbumsResourceWithRawResponse

        return AlbumsResourceWithRawResponse(self._client.albums)

    @cached_property
    def artists(self) -> artists.ArtistsResourceWithRawResponse:
        from .resources.artists import ArtistsResourceWithRawResponse

        return ArtistsResourceWithRawResponse(self._client.artists)

    @cached_property
    def shows(self) -> shows.ShowsResourceWithRawResponse:
        from .resources.shows import ShowsResourceWithRawResponse

        return ShowsResourceWithRawResponse(self._client.shows)

    @cached_property
    def episodes(self) -> episodes.EpisodesResourceWithRawResponse:
        from .resources.episodes import EpisodesResourceWithRawResponse

        return EpisodesResourceWithRawResponse(self._client.episodes)

    @cached_property
    def audiobooks(self) -> audiobooks.AudiobooksResourceWithRawResponse:
        from .resources.audiobooks import AudiobooksResourceWithRawResponse

        return AudiobooksResourceWithRawResponse(self._client.audiobooks)

    @cached_property
    def me(self) -> me.MeResourceWithRawResponse:
        from .resources.me import MeResourceWithRawResponse

        return MeResourceWithRawResponse(self._client.me)

    @cached_property
    def chapters(self) -> chapters.ChaptersResourceWithRawResponse:
        from .resources.chapters import ChaptersResourceWithRawResponse

        return ChaptersResourceWithRawResponse(self._client.chapters)

    @cached_property
    def tracks(self) -> tracks.TracksResourceWithRawResponse:
        from .resources.tracks import TracksResourceWithRawResponse

        return TracksResourceWithRawResponse(self._client.tracks)

    @cached_property
    def search(self) -> search.SearchResourceWithRawResponse:
        from .resources.search import SearchResourceWithRawResponse

        return SearchResourceWithRawResponse(self._client.search)

    @cached_property
    def playlists(self) -> playlists.PlaylistsResourceWithRawResponse:
        from .resources.playlists import PlaylistsResourceWithRawResponse

        return PlaylistsResourceWithRawResponse(self._client.playlists)

    @cached_property
    def users(self) -> users.UsersResourceWithRawResponse:
        from .resources.users import UsersResourceWithRawResponse

        return UsersResourceWithRawResponse(self._client.users)

    @cached_property
    def browse(self) -> browse.BrowseResourceWithRawResponse:
        from .resources.browse import BrowseResourceWithRawResponse

        return BrowseResourceWithRawResponse(self._client.browse)

    @cached_property
    def audio_features(self) -> audio_features.AudioFeaturesResourceWithRawResponse:
        from .resources.audio_features import AudioFeaturesResourceWithRawResponse

        return AudioFeaturesResourceWithRawResponse(self._client.audio_features)

    @cached_property
    def audio_analysis(self) -> audio_analysis.AudioAnalysisResourceWithRawResponse:
        from .resources.audio_analysis import AudioAnalysisResourceWithRawResponse

        return AudioAnalysisResourceWithRawResponse(self._client.audio_analysis)

    @cached_property
    def recommendations(self) -> recommendations.RecommendationsResourceWithRawResponse:
        from .resources.recommendations import RecommendationsResourceWithRawResponse

        return RecommendationsResourceWithRawResponse(self._client.recommendations)

    @cached_property
    def markets(self) -> markets.MarketsResourceWithRawResponse:
        from .resources.markets import MarketsResourceWithRawResponse

        return MarketsResourceWithRawResponse(self._client.markets)


class AsyncSpottedWithRawResponse:
    _client: AsyncSpotted

    def __init__(self, client: AsyncSpotted) -> None:
        self._client = client

    @cached_property
    def albums(self) -> albums.AsyncAlbumsResourceWithRawResponse:
        from .resources.albums import AsyncAlbumsResourceWithRawResponse

        return AsyncAlbumsResourceWithRawResponse(self._client.albums)

    @cached_property
    def artists(self) -> artists.AsyncArtistsResourceWithRawResponse:
        from .resources.artists import AsyncArtistsResourceWithRawResponse

        return AsyncArtistsResourceWithRawResponse(self._client.artists)

    @cached_property
    def shows(self) -> shows.AsyncShowsResourceWithRawResponse:
        from .resources.shows import AsyncShowsResourceWithRawResponse

        return AsyncShowsResourceWithRawResponse(self._client.shows)

    @cached_property
    def episodes(self) -> episodes.AsyncEpisodesResourceWithRawResponse:
        from .resources.episodes import AsyncEpisodesResourceWithRawResponse

        return AsyncEpisodesResourceWithRawResponse(self._client.episodes)

    @cached_property
    def audiobooks(self) -> audiobooks.AsyncAudiobooksResourceWithRawResponse:
        from .resources.audiobooks import AsyncAudiobooksResourceWithRawResponse

        return AsyncAudiobooksResourceWithRawResponse(self._client.audiobooks)

    @cached_property
    def me(self) -> me.AsyncMeResourceWithRawResponse:
        from .resources.me import AsyncMeResourceWithRawResponse

        return AsyncMeResourceWithRawResponse(self._client.me)

    @cached_property
    def chapters(self) -> chapters.AsyncChaptersResourceWithRawResponse:
        from .resources.chapters import AsyncChaptersResourceWithRawResponse

        return AsyncChaptersResourceWithRawResponse(self._client.chapters)

    @cached_property
    def tracks(self) -> tracks.AsyncTracksResourceWithRawResponse:
        from .resources.tracks import AsyncTracksResourceWithRawResponse

        return AsyncTracksResourceWithRawResponse(self._client.tracks)

    @cached_property
    def search(self) -> search.AsyncSearchResourceWithRawResponse:
        from .resources.search import AsyncSearchResourceWithRawResponse

        return AsyncSearchResourceWithRawResponse(self._client.search)

    @cached_property
    def playlists(self) -> playlists.AsyncPlaylistsResourceWithRawResponse:
        from .resources.playlists import AsyncPlaylistsResourceWithRawResponse

        return AsyncPlaylistsResourceWithRawResponse(self._client.playlists)

    @cached_property
    def users(self) -> users.AsyncUsersResourceWithRawResponse:
        from .resources.users import AsyncUsersResourceWithRawResponse

        return AsyncUsersResourceWithRawResponse(self._client.users)

    @cached_property
    def browse(self) -> browse.AsyncBrowseResourceWithRawResponse:
        from .resources.browse import AsyncBrowseResourceWithRawResponse

        return AsyncBrowseResourceWithRawResponse(self._client.browse)

    @cached_property
    def audio_features(self) -> audio_features.AsyncAudioFeaturesResourceWithRawResponse:
        from .resources.audio_features import AsyncAudioFeaturesResourceWithRawResponse

        return AsyncAudioFeaturesResourceWithRawResponse(self._client.audio_features)

    @cached_property
    def audio_analysis(self) -> audio_analysis.AsyncAudioAnalysisResourceWithRawResponse:
        from .resources.audio_analysis import AsyncAudioAnalysisResourceWithRawResponse

        return AsyncAudioAnalysisResourceWithRawResponse(self._client.audio_analysis)

    @cached_property
    def recommendations(self) -> recommendations.AsyncRecommendationsResourceWithRawResponse:
        from .resources.recommendations import AsyncRecommendationsResourceWithRawResponse

        return AsyncRecommendationsResourceWithRawResponse(self._client.recommendations)

    @cached_property
    def markets(self) -> markets.AsyncMarketsResourceWithRawResponse:
        from .resources.markets import AsyncMarketsResourceWithRawResponse

        return AsyncMarketsResourceWithRawResponse(self._client.markets)


class SpottedWithStreamedResponse:
    _client: Spotted

    def __init__(self, client: Spotted) -> None:
        self._client = client

    @cached_property
    def albums(self) -> albums.AlbumsResourceWithStreamingResponse:
        from .resources.albums import AlbumsResourceWithStreamingResponse

        return AlbumsResourceWithStreamingResponse(self._client.albums)

    @cached_property
    def artists(self) -> artists.ArtistsResourceWithStreamingResponse:
        from .resources.artists import ArtistsResourceWithStreamingResponse

        return ArtistsResourceWithStreamingResponse(self._client.artists)

    @cached_property
    def shows(self) -> shows.ShowsResourceWithStreamingResponse:
        from .resources.shows import ShowsResourceWithStreamingResponse

        return ShowsResourceWithStreamingResponse(self._client.shows)

    @cached_property
    def episodes(self) -> episodes.EpisodesResourceWithStreamingResponse:
        from .resources.episodes import EpisodesResourceWithStreamingResponse

        return EpisodesResourceWithStreamingResponse(self._client.episodes)

    @cached_property
    def audiobooks(self) -> audiobooks.AudiobooksResourceWithStreamingResponse:
        from .resources.audiobooks import AudiobooksResourceWithStreamingResponse

        return AudiobooksResourceWithStreamingResponse(self._client.audiobooks)

    @cached_property
    def me(self) -> me.MeResourceWithStreamingResponse:
        from .resources.me import MeResourceWithStreamingResponse

        return MeResourceWithStreamingResponse(self._client.me)

    @cached_property
    def chapters(self) -> chapters.ChaptersResourceWithStreamingResponse:
        from .resources.chapters import ChaptersResourceWithStreamingResponse

        return ChaptersResourceWithStreamingResponse(self._client.chapters)

    @cached_property
    def tracks(self) -> tracks.TracksResourceWithStreamingResponse:
        from .resources.tracks import TracksResourceWithStreamingResponse

        return TracksResourceWithStreamingResponse(self._client.tracks)

    @cached_property
    def search(self) -> search.SearchResourceWithStreamingResponse:
        from .resources.search import SearchResourceWithStreamingResponse

        return SearchResourceWithStreamingResponse(self._client.search)

    @cached_property
    def playlists(self) -> playlists.PlaylistsResourceWithStreamingResponse:
        from .resources.playlists import PlaylistsResourceWithStreamingResponse

        return PlaylistsResourceWithStreamingResponse(self._client.playlists)

    @cached_property
    def users(self) -> users.UsersResourceWithStreamingResponse:
        from .resources.users import UsersResourceWithStreamingResponse

        return UsersResourceWithStreamingResponse(self._client.users)

    @cached_property
    def browse(self) -> browse.BrowseResourceWithStreamingResponse:
        from .resources.browse import BrowseResourceWithStreamingResponse

        return BrowseResourceWithStreamingResponse(self._client.browse)

    @cached_property
    def audio_features(self) -> audio_features.AudioFeaturesResourceWithStreamingResponse:
        from .resources.audio_features import AudioFeaturesResourceWithStreamingResponse

        return AudioFeaturesResourceWithStreamingResponse(self._client.audio_features)

    @cached_property
    def audio_analysis(self) -> audio_analysis.AudioAnalysisResourceWithStreamingResponse:
        from .resources.audio_analysis import AudioAnalysisResourceWithStreamingResponse

        return AudioAnalysisResourceWithStreamingResponse(self._client.audio_analysis)

    @cached_property
    def recommendations(self) -> recommendations.RecommendationsResourceWithStreamingResponse:
        from .resources.recommendations import RecommendationsResourceWithStreamingResponse

        return RecommendationsResourceWithStreamingResponse(self._client.recommendations)

    @cached_property
    def markets(self) -> markets.MarketsResourceWithStreamingResponse:
        from .resources.markets import MarketsResourceWithStreamingResponse

        return MarketsResourceWithStreamingResponse(self._client.markets)


class AsyncSpottedWithStreamedResponse:
    _client: AsyncSpotted

    def __init__(self, client: AsyncSpotted) -> None:
        self._client = client

    @cached_property
    def albums(self) -> albums.AsyncAlbumsResourceWithStreamingResponse:
        from .resources.albums import AsyncAlbumsResourceWithStreamingResponse

        return AsyncAlbumsResourceWithStreamingResponse(self._client.albums)

    @cached_property
    def artists(self) -> artists.AsyncArtistsResourceWithStreamingResponse:
        from .resources.artists import AsyncArtistsResourceWithStreamingResponse

        return AsyncArtistsResourceWithStreamingResponse(self._client.artists)

    @cached_property
    def shows(self) -> shows.AsyncShowsResourceWithStreamingResponse:
        from .resources.shows import AsyncShowsResourceWithStreamingResponse

        return AsyncShowsResourceWithStreamingResponse(self._client.shows)

    @cached_property
    def episodes(self) -> episodes.AsyncEpisodesResourceWithStreamingResponse:
        from .resources.episodes import AsyncEpisodesResourceWithStreamingResponse

        return AsyncEpisodesResourceWithStreamingResponse(self._client.episodes)

    @cached_property
    def audiobooks(self) -> audiobooks.AsyncAudiobooksResourceWithStreamingResponse:
        from .resources.audiobooks import AsyncAudiobooksResourceWithStreamingResponse

        return AsyncAudiobooksResourceWithStreamingResponse(self._client.audiobooks)

    @cached_property
    def me(self) -> me.AsyncMeResourceWithStreamingResponse:
        from .resources.me import AsyncMeResourceWithStreamingResponse

        return AsyncMeResourceWithStreamingResponse(self._client.me)

    @cached_property
    def chapters(self) -> chapters.AsyncChaptersResourceWithStreamingResponse:
        from .resources.chapters import AsyncChaptersResourceWithStreamingResponse

        return AsyncChaptersResourceWithStreamingResponse(self._client.chapters)

    @cached_property
    def tracks(self) -> tracks.AsyncTracksResourceWithStreamingResponse:
        from .resources.tracks import AsyncTracksResourceWithStreamingResponse

        return AsyncTracksResourceWithStreamingResponse(self._client.tracks)

    @cached_property
    def search(self) -> search.AsyncSearchResourceWithStreamingResponse:
        from .resources.search import AsyncSearchResourceWithStreamingResponse

        return AsyncSearchResourceWithStreamingResponse(self._client.search)

    @cached_property
    def playlists(self) -> playlists.AsyncPlaylistsResourceWithStreamingResponse:
        from .resources.playlists import AsyncPlaylistsResourceWithStreamingResponse

        return AsyncPlaylistsResourceWithStreamingResponse(self._client.playlists)

    @cached_property
    def users(self) -> users.AsyncUsersResourceWithStreamingResponse:
        from .resources.users import AsyncUsersResourceWithStreamingResponse

        return AsyncUsersResourceWithStreamingResponse(self._client.users)

    @cached_property
    def browse(self) -> browse.AsyncBrowseResourceWithStreamingResponse:
        from .resources.browse import AsyncBrowseResourceWithStreamingResponse

        return AsyncBrowseResourceWithStreamingResponse(self._client.browse)

    @cached_property
    def audio_features(self) -> audio_features.AsyncAudioFeaturesResourceWithStreamingResponse:
        from .resources.audio_features import AsyncAudioFeaturesResourceWithStreamingResponse

        return AsyncAudioFeaturesResourceWithStreamingResponse(self._client.audio_features)

    @cached_property
    def audio_analysis(self) -> audio_analysis.AsyncAudioAnalysisResourceWithStreamingResponse:
        from .resources.audio_analysis import AsyncAudioAnalysisResourceWithStreamingResponse

        return AsyncAudioAnalysisResourceWithStreamingResponse(self._client.audio_analysis)

    @cached_property
    def recommendations(self) -> recommendations.AsyncRecommendationsResourceWithStreamingResponse:
        from .resources.recommendations import AsyncRecommendationsResourceWithStreamingResponse

        return AsyncRecommendationsResourceWithStreamingResponse(self._client.recommendations)

    @cached_property
    def markets(self) -> markets.AsyncMarketsResourceWithStreamingResponse:
        from .resources.markets import AsyncMarketsResourceWithStreamingResponse

        return AsyncMarketsResourceWithStreamingResponse(self._client.markets)


Client = Spotted

AsyncClient = AsyncSpotted
