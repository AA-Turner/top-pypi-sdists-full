import logging
import datetime
import os

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import arrow

from . import current_track
from . import config


logger = logging.getLogger(name='spotify_tracker')


class SpotifyPlaylistClient:
    def __init__(self):
        config.ensure_config_file_exists()
        self.username = config.get_config_value('username')
        self.client_id = config.get_config_value('client_id')
        self.client_secret = config.get_config_value('client_secret')
        self.callback_url = config.get_config_value('callback_url')
        self.token = config.get_config_value('token')

    @property
    def sp(self):
        if not hasattr(self, '_sp'):
            self.refresh_sp()
        return self._sp

    @property
    def cache_path(self):
        cache_name = '.cache-{}'.format(self.username)
        return os.path.join(config.CONFIG_DIR, cache_name)

    def refresh_sp(self):
        self._sp = spotipy.Spotify(auth=config.get_config_value('token'))
        self._sp.trace = False

    def build_playlist_tracks(self, playlist_tracks=None, tracks=None):
        if not tracks:
            pl = self.sp.user_playlist(
                self.username, self.playlist_id,
                fields=['tracks', 'next']
            )
            tracks = pl['tracks']
        else:
            tracks = self.sp.next(tracks)
        if not playlist_tracks:
            playlist_tracks = []

        playlist_tracks.extend(tracks['items'])
        if tracks['next']:
            return self.build_playlist_tracks(playlist_tracks, tracks)
        else:
            return playlist_tracks

    def check_track_in_playlist(self, track_id):
        playlist_track_ids = {track['track']['id'] for
                              track in self.build_playlist_tracks()}
        return track_id in playlist_track_ids

    def remove_old_tracks_in_playlist(self, _days, dryrun=True):
        # remove tracks older than <days> days in the playlist
        old_track_ids = [
            track['track']['id'] for
            track in self.build_playlist_tracks()
            if arrow.now() - arrow.get(track['added_at']) > datetime.timedelta(days=_days)
        ]
        for track_id in old_track_ids:
            logger.info('Removing: {}'.format(
                self.get_track_name_and_artist_string(track_id)))
        if not dryrun:
            self.sp.user_playlist_remove_all_occurrences_of_tracks(
                self.username, self.playlist_id, old_track_ids
            )

    def get_track_name_and_artist_string(self, track_id):
        track = self.sp.track(track_id)
        track_name = '{} - '.format(track.get('name', '<Track Name Missing>'))
        artists_names = [
            a.get('name', '<Artist Name Missing>') for a in track.get('artists', [{}])
        ]
        return track_name + ', '.join(artists_names)

    def add_track_to_playlist(self, track_id):
        if self.check_track_in_playlist(track_id):
            self.sp.user_playlist_remove_all_occurrences_of_tracks(
                self.username, self.playlist_id, [track_id]
            )
        self.sp.user_playlist_add_tracks(
            self.username, self.playlist_id, [track_id]
        )
        logger.debug('Added {}'.format(
            self.get_track_name_and_artist_string(track_id)
        ))

    def get_token(self, allow_raw_input=True):
        if allow_raw_input:
            token = util.prompt_for_user_token(
                self.username, config.SCOPE, self.client_id,
                self.client_secret, self.callback_url)
        else:
            sp_oauth = SpotifyOAuth(
                self.client_id, self.client_secret, self.callback_url,
                scope=config.SCOPE, cache_path=self.cache_path)
            token_info = sp_oauth.get_cached_token()
            if token_info:
                token = token_info['access_token']
            else:
                raise Exception('need to run debug-refresh-token in a terminal')
        return token

    def save_token(self, allow_raw_input=True):
        logger.debug('Updating token.')
        token = self.get_token(allow_raw_input)
        config.save_config_value('token', token)
        self.token = token
        self.refresh_sp()

    def main(self):
        raise NotImplementedError

    def safe_main(self):
        try:
            self.main()
        except spotipy.client.SpotifyException as exc:
            if exc.code == -1:
                logger.debug('SpotifyException.')
                self.save_token()
            else:
                logger.exception('Unknown exception.')
                raise

    def get_current_track_id(self):
        try:
            track_id = current_track.get_current_track_id()
        except:
            logger.exception('Unknown Exception reach getting current track_id.')
            return
        return track_id

    def setup_username(self):
        username = input("Please provide your Spotify username: ")
        config.save_config_value('username', username)

    def setup_client_id(self):
        print("You'll need to setup a Spotify Application at "
              "https://developer.spotify.com/my-applications/#!/applications/create")
        client_id = input("Please provide your Spotify application Client ID: ")
        config.save_config_value('client_id', client_id)

    def setup_client_secret(self):
        print("You should have a Spotify Application. "
              "See https://developer.spotify.com/my-applications/#!/applications")
        client_secret = input("Please provide your Spotify application Client Secret: ")
        config.save_config_value('client_secret', client_secret)

    def setup_callback_url(self):
        print("You should have a Spotify Application. "
              "See https://developer.spotify.com/my-applications/#!/applications")
        print("You need to specify a Callback URL. "
              "It can be anything, but must match what you've saved on Spotify.")
        callback_url = input("Please provide your Spotify application Callback URL: ")
        config.save_config_value('callback_url', callback_url)

    def setup_token(self):
        print("You need to authorize your application.")
        self.save_token()
        print('Your token is saved.')

    def setup_playlist_id(self):
        raise NotImplementedError

    def setup(self):
        if not self.username:
            self.setup_username()
        if not self.client_id:
            self.setup_client_id()
        if not self.client_secret:
            self.setup_client_secret()
        if not self.callback_url:
            self.setup_callback_url()
        if not self.token:
            self.setup_token()
        if not self.playlist_id:
            self.setup_playlist_id()

    def check_config(self):
        return (self.username and self.client_id and self.client_secret and
                self.callback_url and self.token and self.playlist_id)
