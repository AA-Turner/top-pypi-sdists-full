import pathlib
import os

from rapidfuzz import process
import rapidfuzz.fuzz as fuzz
from src.utils.playlist import Playlist, Song

# FUTURE ENHANCEMENT? Allow user to select music folder via GUI

def get_music_library() -> tuple[pathlib.Path, list[pathlib.Path]]:
    """Get the user's music library and return the library path object
    and a list of artist path objects.
    """

    # Either get the music library from an environment variable OR
    # allow user to set at runtime
    music_library = os.environ.get("SPOTIPYLIST_MUSIC_LIBRARY")
    
    # if the environment variable is not set, prompt the user
    if not music_library:
        print("Music library not set. Please set the SPOTIPYLIST_MUSIC_LIBRARY environment variable before running or input the absolute path of your music library now")
        music_library = input("Music library absolute path: ")
    
    music_library = pathlib.Path(music_library)
    
    # pathlib.iterder() will list all top-level directories in the music library
    # My library is set up with Artist/Album/Track.mp3, so this will
    # allow us to search based on artist and filter, before selecting
    # the actual tracks
    library_artists = [*music_library.iterdir()]

    return music_library, library_artists

def search_tracks(track: Song, library_artists: list[pathlib.Path], music_library: pathlib.Path):
    """Read in track info and list of library artists;
    search for matching tracks and return a best match    
    """
    mp3_list=[]
    track_artist = track.artists[0] # take first/primary artist
    if len(track.artists) > 1: # if there are featured artists
        # setting cutoff of 70, seems to match pretty well for now
        artist_matches = [dir for dir in library_artists if fuzz.partial_ratio(track_artist, dir.name) > 70]

    else:
        # index library_artists with index provided by tuple returned from process.extract
        # setting cutoff of artist matches to > 86. When it's a single artist, <85.5 seems to
        # generate more issues with close artists, who may have songs with >70 ratio of similarity to
        # the song title
        artist_matches = [library_artists[result[2]] for result in process.extract(track_artist, [dir.name for dir in library_artists], score_cutoff=86)]

    for artist_dir in artist_matches:
        for mp3_file in artist_dir.rglob("*.mp3"):
            mp3_list.append(mp3_file)

    # remove first 5 chars of filename to remove track numbering (number throws off the matching)
    best_match = process.extractOne(track.name, [mp3.stem[4:] for mp3 in mp3_list], score_cutoff=70)
    
    # If a best_match exists, return best_match's relative path to the music_library, taking the index of the best match
    # in the mp3_list to get the full PosixPath object, allowing use of the .relative_to() method
    if best_match:
        return mp3_list[best_match[2]].relative_to(music_library)
    else:
        return

def write_playlist(playlist: Playlist, music_library: pathlib.Path, library_artists: list[pathlib.Path]) -> None:
    """Open a new playlist, write M3U header, write all best matches from search_tracks();
    return non_matches
    """
    with open(f"{music_library}/{playlist.name}.m3u", 'w', encoding="UTF-8") as f:
        f.write("#EXTM3U\n")
        non_matches = []
        for track in playlist.tracks:
            best_match = search_tracks(track, library_artists, music_library)

            # if a best_match is returned, write it to the playlist file, otherwise
            # append any non-matched track to list for use below, writing to separate file

            if best_match:
                f.write(f"{str(best_match)}\n")
            else:
                non_matches.append(track)

    if non_matches: # if any non-matched tracks, write to missing_tracks.txt and notify user
        with open(f"{music_library}/missing_tracks.txt", 'w', encoding="UTF-8") as f:
            for non_match in non_matches:
                line = [non_match.name, non_match.artists[0]]
                f.write(f"{' by '.join(line)}\n")

        print("Some songs from this playlist were not found in your library. See missing_tracks.txt for details.")     

    return

# 3 Songs we know we have; 2 songs we know we don't for testing

track_info = {
    'items': [
        {
            'track': {
                'artists': [{'name': 'Phantom Planet'}],
                'name': 'California - Tchad Blake Mix'
            }
        },
        {
            'track': {
                'artists': [{'name': 'blink-182'}],
                'name': 'First Date'
            }
        },
        {
            'track': {
                'artists': [{'name': 'G-Eazy'}, {'name': 'Bebe Rexha'}],
                'name': 'Me, Myself & I'
            }
        },
        {
            'track': {
                'artists': [{'name': 'Home Grown'}],
                'name': 'Keep Your Distance'
            }
        },
        {
            'track': {
                'artists': [{'name': 'Test-Artist'}, {'name': 'Featured'}],
                'name': 'Test-Track'
            }
        }
    ]
}

if __name__ == "__main__":

    music_library, library_artists = get_music_library()
    playlist_name = input("Name for New Playlist: ")

    write_playlist(track_info['items'], playlist_name, music_library)