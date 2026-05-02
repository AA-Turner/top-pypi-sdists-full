from enum import Enum


class EntityType(Enum):
    ALBUM = "album"
    ARTIST = "artist"
    AUDIOBOOK = "audiobook"
    EPISODE = "episode"
    PLAYLIST = "playlist"
    SHOW = "show"
    TRACK = "track"
    USER = "user"
