import logging

from .spotify_client import SpotifyPlaylistClient
from . import config

import spotipy


logger = logging.getLogger(name='spotify_tracker')


class SpotifyFavoritesClient(SpotifyPlaylistClient):
    def __init__(self):
        super().__init__()
        self.playlist_id = config.get_config_value('favorites_playlist_id')
        self.playlist_name = config.get_config_value('favorites_playlist_name')

    def setup_playlist_id(self):
        print("You need to add a playlist_id to your config to save "
              "song history to.")
        sp_playlists = self.sp.user_playlists(self.username)
        playlists = {p['id']: p['name'] for p in sp_playlists['items']
                     if p['owner']['id'] == self.username}
        for playlist_id, playlist_name in playlists.items():
            print('{}: {}'.format(playlist_name, playlist_id))
        playlist_id = input("Please input the playlist_id of the Playlist "
                            "you'd like to save your favorites to: ")
        playlist_name = playlists[playlist_id]
        config.save_config_value('favorites_playlist_id', playlist_id)
        config.save_config_value('favorites_playlist_name', playlist_name)

    def main(self, allow_raw_input=True):
        try:
            self.add_current_song_to_playlist()
        except spotipy.client.SpotifyException as exc:
            if exc.code == -1:
                logger.debug('spotify token expired. refreshing')
                self.save_token(allow_raw_input=allow_raw_input)
                self.refresh_sp()
                logger.debug('reattempting add_to_favorites')
                self.add_current_song_to_playlist()
            else:
                logger.exception('Unknown exception.')

    def add_current_song_to_playlist(self):
        if not self.check_config():
            raise Exception("Please run setupfavorites command.")

        track_id = self.get_current_track_id()
        if not track_id:
            logger.warning('No song currently playing')
            return
        if not self.check_track_in_playlist(track_id):
            self.add_track_to_playlist(track_id)
            logger.info('Added {} to {}'.format(
                self.get_track_name_and_artist_string(track_id),
                self.playlist_name
            ))
        else:
            logger.info('{} is already in {}'.format(
                self.get_track_name_and_artist_string(track_id),
                self.playlist_name
            ))

    def alfred_main(self):
        self.main(allow_raw_input=False)
