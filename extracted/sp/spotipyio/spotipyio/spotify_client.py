from __future__ import annotations

from typing import Optional

from spotipyio.logic.consts.spotify_consts import SPOTIFY_API_BASE_URL
from spotipyio.auth import SpotifySession
from spotipyio.logic.managers import (
    AlbumsManager,
    ArtistsManager,
    ChaptersManager,
    CurrentUserManager,
    EpisodesManager,
    PlaylistsManager,
    SearchManager,
    TracksManager,
    UsersManager,
)


class SpotifyClient:
    def __init__(
        self,
        session: Optional[SpotifySession] = None,
        albums: Optional[AlbumsManager] = None,
        artists: Optional[ArtistsManager] = None,
        chapters: Optional[ChaptersManager] = None,
        current_user: Optional[CurrentUserManager] = None,
        episodes: Optional[EpisodesManager] = None,
        playlists: Optional[PlaylistsManager] = None,
        search: Optional[SearchManager] = None,
        tracks: Optional[TracksManager] = None,
        users: Optional[UsersManager] = None,
        base_url: str = SPOTIFY_API_BASE_URL,
    ):
        self.session = session
        self.albums = albums
        self.artists = artists
        self.chapters = chapters
        self.current_user = current_user
        self.episodes = episodes
        self.playlists = playlists
        self.search = search
        self.tracks = tracks
        self.users = users
        self._base_url = base_url

    @classmethod
    def create(cls, session: SpotifySession, base_url: str = SPOTIFY_API_BASE_URL) -> SpotifyClient:
        return SpotifyClient(
            session=session,
            artists=ArtistsManager.create(base_url, session),
            chapters=ChaptersManager.create(base_url, session),
            current_user=CurrentUserManager.create(base_url, session),
            episodes=EpisodesManager.create(base_url, session),
            playlists=PlaylistsManager.create(base_url, session),
            users=UsersManager.create(base_url, session),
            albums=AlbumsManager.create(base_url, session),
            tracks=TracksManager.create(base_url, session),
            search=SearchManager.create(base_url, session),
        )

    async def start(self) -> SpotifyClient:
        if self.session is None:
            session = SpotifySession()
            await session.start()
        else:
            session = self.session

        return SpotifyClient(
            session=session,
            artists=ArtistsManager.create(self._base_url, session),
            chapters=ChaptersManager.create(self._base_url, session),
            current_user=CurrentUserManager.create(self._base_url, session),
            episodes=EpisodesManager.create(self._base_url, session),
            playlists=PlaylistsManager.create(self._base_url, session),
            users=UsersManager.create(self._base_url, session),
            albums=AlbumsManager.create(self._base_url, session),
            tracks=TracksManager.create(self._base_url, session),
            search=SearchManager.create(self._base_url, session),
        )

    async def stop(self) -> None:
        if self.session is not None:
            await self.session.stop()

    async def __aenter__(self) -> SpotifyClient:
        return await self.start()

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.stop()
