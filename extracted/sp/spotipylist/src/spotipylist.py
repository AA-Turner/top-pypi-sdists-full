# pylint: disable=not-callable
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from src.utils.playlist_generator import get_music_library, write_playlist
from src.utils.playlist import Playlist, Song

def spotipylist():
    # take input of playlist URL or playlist_id from user
    playlist_url = input("""
    Please input the desired playlist ID.\n
    The id will be the string of characters at the end of the URL as below\n
    https://open.spotify.com/playlist/5t9TUKubTd0bOriqsxq79h -> 5t9TUKubTd0bOriqsxq79h\n
    Playlist ID: """)

    # SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET need to be set via environment variables

    auth_manager = SpotifyClientCredentials()
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    # Get playlist_items, extend results if is a paginated result
    # exclude unnecessary fields

    results = spotify.playlist_items(
        playlist_url,
        market="US"
    )

    tracks = results['items']

    while results['next']:
        results = spotify.next(results)
        tracks.extend(results['items'])

    music_library, library_artists = get_music_library()

    playlist_name = input("Name for New Playlist \
    (This will overwrite any playlist with the same name): ")

    # take tracks and create a Playlist object with Song objects
    playlist_tracks = Playlist(playlist_name, [])

    for item in tracks:
        song = Song(item['track']['name'], [artist['name'] for artist in item['track']['artists']])
        playlist_tracks.tracks.append(song)

    write_playlist(tracks, playlist_name, music_library, library_artists)

if __name__ == "__main__":
    spotipylist()
