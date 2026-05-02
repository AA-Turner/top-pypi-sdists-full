import time
import logging

from .spotify_client import SpotifyPlaylistClient
from . import config


logger = logging.getLogger(name='spotify_tracker')


class SpotifyWatcherClient(SpotifyPlaylistClient):
    def __init__(self):
        self.playlist_id = config.get_config_value('watcher_playlist_id')
        self.last_track_id = None
        return super().__init__()

    def setup_playlist_id(self):
        print("You need to add a playlist_id to your config to save "
              "song history to.")
        sp_playlists = self.sp.user_playlists(self.username)
        playlists = [p for p in sp_playlists['items']
                     if p['owner']['id'] == self.username]
        for playlist in playlists:
            print('{}: {}'.format(playlist['name'], playlist['id']))
        playlist_id = input("Please input the playlist_id of the Playlist "
                            "you'd like to save your history to: ")
        config.save_config_value('watcher_playlist_id', playlist_id)

    def main(self):
        track_id = self.get_current_track_id()
        if not track_id or track_id == self.last_track_id:
            return
        logger.info('Currently listening to {}'.format(
            self.get_track_name_and_artist_string(track_id)
        ))
        self.add_track_to_playlist(track_id)
        self.last_track_id = track_id

    def watch(self):
        if not self.check_config():
            raise Exception("Please run setupwatcher command.")

        logger.debug('Starting watch loop')
        while True:
            logger.debug('New watch lap completed.')
            self.safe_main()
            time.sleep(5)
