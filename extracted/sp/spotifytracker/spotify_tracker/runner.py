""" Spotify Tracker - Save every song you play from OS X to a playlist

Usage:
  spotifytracker setupwatcher
  spotifytracker setupfavorites
  spotifytracker watch [ [-V | --verbose] | [-Q | --quiet ]]
  spotifytracker addtofavorites [ [-V | --verbose] | [-Q | --quiet ] | [--alfred ]]
  spotifytracker debug-refresh-token
  spotifytracker remove-old-tracks-watcher <days> [-D | --dryrun ] [ [-V | --verbose] | [-Q | --quiet ]]

Options:
  -V --verbose
  -Q --quiet
  -D --dryrun
"""
import logging
import sys

from docopt import docopt

from .spotify_client import SpotifyPlaylistClient
from .watcher_client import SpotifyWatcherClient
from .favorites_client import SpotifyFavoritesClient


DEFAULT_LOG_LEVEL = logging.INFO


def main():
    arguments = docopt(__doc__)

    logging.basicConfig(
        format='%(asctime)s %(levelname)s: %(message)s')

    spotify_tracker_logger = logging.getLogger(name='spotify_tracker')
    base_logger = logging.getLogger()
    if arguments['--verbose']:
        base_logger.setLevel(level=logging.DEBUG)
    elif arguments['--quiet']:
        base_logger.setLevel(level=logging.WARNING)
    elif arguments['--alfred']:
        spotify_tracker_logger.setLevel(level=DEFAULT_LOG_LEVEL)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(DEFAULT_LOG_LEVEL)
        formatter = logging.Formatter('%(message)s')
        ch.setFormatter(formatter)
        spotify_tracker_logger.addHandler(ch)
    else:
        spotify_tracker_logger.setLevel(level=DEFAULT_LOG_LEVEL)

    if arguments['setupwatcher']:
        _spotify_client = SpotifyWatcherClient()
        _spotify_client.setup()
        return
    if arguments['setupfavorites']:
        _spotify_client = SpotifyFavoritesClient()
        _spotify_client.setup()
        return
    if arguments['watch']:
        _spotify_client = SpotifyWatcherClient()
        _spotify_client.watch()
        return
    if arguments['addtofavorites']:
        _spotify_client = SpotifyFavoritesClient()
        if arguments['--alfred']:
            _spotify_client.alfred_main()
        else:
            _spotify_client.safe_main()
        return
    if arguments['debug-refresh-token']:
        _spotify_client = SpotifyPlaylistClient()
        _spotify_client.save_token()
        return
    if arguments['remove-old-tracks-watcher']:
        _spotify_client = SpotifyWatcherClient()
        _spotify_client.remove_old_tracks_in_playlist(
            int(arguments['<days>']), arguments['--dryrun']
        )


if __name__ == "__main__":
    main()
