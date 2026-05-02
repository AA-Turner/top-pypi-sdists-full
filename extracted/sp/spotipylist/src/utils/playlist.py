# define classes for Playlist and Track/Song

class Song:
    """Class for holding song information."""
    def __init__(self, name: str, artists: list[str]) -> None:
        self.name = name
        self.artists = artists

class Playlist:
    """Class for holding playlist information, which is made up of multiple Songs"""
    def __init__(self, name: str, tracks: list[Song]) -> None:
        self.name = name
        self.tracks = tracks
