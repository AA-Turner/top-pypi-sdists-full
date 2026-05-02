from calendar import monthrange
from datetime import datetime
from random import randint, choice, random, uniform
from typing import Optional, List, Dict, Callable, Any, Type

from spotipyio.logic.consts.spotify_consts import (
    PLAYLISTS,
    USERS,
    LIMIT,
    HREF,
    NEXT,
    OFFSET,
    TOTAL,
    ITEMS,
    ARTISTS,
    TRACKS,
    ALBUMS,
    TRACK,
    AUDIO_FEATURES,
    CHAPTERS,
    EPISODES,
    SHOWS,
    AUDIOBOOKS,
    SNAPSHOT_ID,
)
from spotipyio.logic.consts.typing_consts import EnumType

from spotipyio.models import (
    SearchItem,
    SearchItemFilters,
    SearchItemMetadata,
    SpotifySearchType,
    ItemsType,
    MatchingEntity,
)
from spotipyio.testing.utils.search_response_builder import SearchResponseBuilder
from spotipyio.logic.utils import random_alphanumeric_string


class SpotifyMockFactory:
    @staticmethod
    def spotify_id() -> str:
        return random_alphanumeric_string(min_length=22, max_length=22)

    @staticmethod
    def some_spotify_ids(length: Optional[int] = None) -> List[str]:
        number_of_ids = length or randint(2, 10)
        return [SpotifyMockFactory.spotify_id() for _ in range(number_of_ids)]

    @staticmethod
    def paged_playlists(**kwargs) -> dict:
        entity_id = kwargs.get("id", SpotifyMockFactory.spotify_id())
        href = kwargs.get("href") or SpotifyMockFactory.href(
            entity_type=USERS, entity_id=entity_id, extra_routes=[PLAYLISTS]
        )
        return {
            HREF: href,
            LIMIT: kwargs.get(LIMIT, randint(1, 50)),
            NEXT: "",
            OFFSET: kwargs.get(OFFSET, randint(1, 200)),
            TOTAL: kwargs.get(TOTAL, randint(1, 1000)),
            ITEMS: kwargs.get(ITEMS, SpotifyMockFactory._some_playlists()),
        }

    @staticmethod
    def playlist(user_id: Optional[str] = None, **kwargs) -> dict:
        owner = kwargs.get("owner", SpotifyMockFactory.owner(user_id))
        entity_type = "playlist"
        entity_id = kwargs.get("id", SpotifyMockFactory.spotify_id())

        return {
            "collaborative": kwargs.get("collaborative", SpotifyMockFactory._random_boolean()),
            "description": kwargs.get("description", random_alphanumeric_string()),
            "external_urls": SpotifyMockFactory.external_urls(entity_type=entity_type, entity_id=entity_id),
            "followers": kwargs.get("followers", SpotifyMockFactory.followers()),
            "href": SpotifyMockFactory.href(entity_type=entity_type, entity_id=entity_id),
            "id": entity_id,
            "images": kwargs.get("images", SpotifyMockFactory.images()),
            "name": kwargs.get("name", SpotifyMockFactory.name()),
            "owner": owner,
            "public": kwargs.get("public", SpotifyMockFactory._random_boolean()),
            "snapshot_id": kwargs.get("snapshot_id", SpotifyMockFactory.snapshot_id()),
            "tracks": kwargs.get("tracks", SpotifyMockFactory.playlist_tracks(id=entity_id, owner=owner)),
            "type": entity_type,
            "uri": SpotifyMockFactory.uri(entity_type=entity_type, entity_id=entity_id),
            "primary_color": None,
        }

    @staticmethod
    def playlist_tracks(**kwargs) -> dict:
        entity_type = "playlist"
        entity_id = kwargs.get("id", SpotifyMockFactory.spotify_id())
        owner = kwargs.get("owner")
        total_tracks = kwargs.get("total", randint(1, 100))
        items = [SpotifyMockFactory.playlist_item(owner) for _ in range(total_tracks)]

        return {
            "href": SpotifyMockFactory.href(entity_type=entity_type, entity_id=entity_id, extra_routes=["tracks"]),
            "limit": 100,
            "next": kwargs.get("next"),
            "offset": 0,
            "previous": None,
            "total": total_tracks,
            "items": items,
        }

    @staticmethod
    def playlist_item(owner: Optional[str] = None) -> dict:
        added_at = SpotifyMockFactory._random_datetime()
        return {
            "added_at": added_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "added_by": owner or SpotifyMockFactory.owner(),
            "is_local": SpotifyMockFactory._random_boolean(),
            "track": SpotifyMockFactory.track(),
        }

    @staticmethod
    def snapshot_response(snapshot_id: Optional[str] = None) -> Dict[str, str]:
        return {SNAPSHOT_ID: snapshot_id or SpotifyMockFactory.snapshot_id()}

    @staticmethod
    def snapshot_id() -> str:
        return random_alphanumeric_string(min_length=32, max_length=32)

    @staticmethod
    def owner(entity_id: Optional[str] = None) -> dict:
        entity_type = "user"
        if entity_id is None:
            entity_id = random_alphanumeric_string()

        return {
            "external_urls": SpotifyMockFactory.external_urls(entity_type=entity_type, entity_id=entity_id),
            "href": SpotifyMockFactory.href(entity_type=entity_type, entity_id=entity_id),
            "id": entity_id,
            "type": entity_type,
            "uri": SpotifyMockFactory.uri(entity_type=entity_type, entity_id=entity_id),
            "display": random_alphanumeric_string(),
        }

    @staticmethod
    def several_artists(ids: Optional[List[str]] = None) -> Dict[str, List[dict]]:
        return SpotifyMockFactory._several_items(method=SpotifyMockFactory.artist, ids=ids, key=ARTISTS)

    @staticmethod
    def several_tracks(ids: Optional[List[str]] = None) -> Dict[str, List[dict]]:
        return SpotifyMockFactory._several_items(method=SpotifyMockFactory.track, ids=ids, key=TRACKS)

    @staticmethod
    def several_albums(ids: Optional[List[str]] = None) -> Dict[str, List[dict]]:
        return SpotifyMockFactory._several_items(method=SpotifyMockFactory.album, ids=ids, key=ALBUMS)

    @staticmethod
    def several_chapters(ids: Optional[List[str]] = None) -> Dict[str, List[dict]]:
        return SpotifyMockFactory._several_items(method=SpotifyMockFactory.chapter, ids=ids, key=CHAPTERS)

    @staticmethod
    def several_episodes(ids: Optional[List[str]] = None) -> Dict[str, List[dict]]:
        return SpotifyMockFactory._several_items(method=SpotifyMockFactory.episode, ids=ids, key=EPISODES)

    @staticmethod
    def several_audio_features(ids: Optional[List[str]] = None) -> Dict[str, List[dict]]:
        return SpotifyMockFactory._several_items(method=SpotifyMockFactory.audio_features, ids=ids, key=AUDIO_FEATURES)

    @staticmethod
    def several_shows(ids: Optional[List[str]] = None) -> Dict[str, List[dict]]:
        return SpotifyMockFactory._several_items(method=SpotifyMockFactory.show, ids=ids, key=SHOWS)

    @staticmethod
    def several_playlists(ids: Optional[List[str]] = None) -> Dict[str, List[dict]]:
        return SpotifyMockFactory._several_items(method=SpotifyMockFactory.playlist, ids=ids, key=PLAYLISTS)

    @staticmethod
    def several_audiobooks(ids: Optional[List[str]] = None) -> Dict[str, List[dict]]:
        return SpotifyMockFactory._several_items(method=SpotifyMockFactory.audiobook, ids=ids, key=AUDIOBOOKS)

    @staticmethod
    def artist(**kwargs) -> dict:
        entity_type = "artist"
        entity_id = kwargs.get("id") or SpotifyMockFactory.spotify_id()

        return {
            "external_urls": kwargs.get("external_urls") or SpotifyMockFactory.external_urls(entity_type, entity_id),
            "followers": kwargs.get("followers", SpotifyMockFactory.followers()),
            "genres": kwargs.get("genres", SpotifyMockFactory.genres()),
            "href": SpotifyMockFactory.href(entity_type, entity_id),
            "id": entity_id,
            "images": kwargs.get("images", SpotifyMockFactory.images()),
            "name": kwargs.get("name", SpotifyMockFactory.name()),
            "popularity": kwargs.get("popularity", SpotifyMockFactory.popularity()),
            "type": entity_type,
            "uri": SpotifyMockFactory.uri(entity_type=entity_type, entity_id=entity_id),
        }

    @staticmethod
    def track(**kwargs) -> dict:
        entity_id = kwargs.get("id", SpotifyMockFactory.spotify_id())
        entity_type = "track"
        artists = kwargs.get("artists", SpotifyMockFactory._some_artists())

        return {
            "album": kwargs.get("album", SpotifyMockFactory.album(artists=artists)),
            "artists": artists,
            "available_markets": kwargs.get("available_markets", SpotifyMockFactory.available_markets()),
            "disc_number": kwargs.get("disc_number", SpotifyMockFactory.disc_number()),
            "duration_ms": kwargs.get("duration_ms", SpotifyMockFactory.duration_ms()),
            "explicit": kwargs.get("explicit", SpotifyMockFactory._random_boolean()),
            "external_ids": kwargs.get("external_ids", SpotifyMockFactory.external_ids()),
            "external_urls": kwargs.get("external_urls") or SpotifyMockFactory.external_urls(entity_type, entity_id),
            "href": SpotifyMockFactory.href(entity_type=entity_type, entity_id=entity_id),
            "id": entity_id,
            "is_local": kwargs.get("is_local", SpotifyMockFactory._random_boolean()),
            "is_playable": kwargs.get("is_playable", SpotifyMockFactory._random_boolean()),
            "name": kwargs.get("name", SpotifyMockFactory.name()),
            "popularity": kwargs.get("popularity", SpotifyMockFactory.popularity()),
            "preview_url": kwargs.get("preview_url", SpotifyMockFactory.preview_url()),
            "track_number": kwargs.get("track_number", SpotifyMockFactory.track_number()),
            "type": entity_type,
            "uri": SpotifyMockFactory.uri(entity_type=entity_type, entity_id=entity_id),
        }

    @staticmethod
    def album(**kwargs) -> dict:
        entity_type = "album"
        entity_id = kwargs.get("id", SpotifyMockFactory.spotify_id())

        return {
            "artists": kwargs.get("artists", SpotifyMockFactory._some_artists()),
            "album_type": kwargs.get("album_type", SpotifyMockFactory.album_type()),
            "total_tracks": kwargs.get("total_tracks", SpotifyMockFactory.track_number()),
            "external_urls": SpotifyMockFactory.external_urls(entity_type=entity_type, entity_id=entity_id),
            "available_markets": kwargs.get("available_markets", SpotifyMockFactory.available_markets()),
            "href": SpotifyMockFactory.href(entity_type=entity_type, entity_id=entity_id),
            "id": entity_id,
            "images": kwargs.get("images", SpotifyMockFactory.images()),
            "name": kwargs.get("name", SpotifyMockFactory.name()),
            "release_date": kwargs.get("release_date", SpotifyMockFactory.release_date()),
            "release_date_precision": kwargs.get("release_date_precision", "day"),
            "type": entity_type,
            "uri": SpotifyMockFactory.uri(entity_type=entity_type, entity_id=entity_id),
            "is_playable": kwargs.get("is_playable", SpotifyMockFactory._random_boolean()),
        }

    @staticmethod
    def audio_features(**kwargs) -> dict:
        entity_id = kwargs.get("id", SpotifyMockFactory.spotify_id())
        entity_type = TRACK

        return {
            "acousticness": SpotifyMockFactory._random_confidence("acousticness", **kwargs),
            "analysis_url": f"https://api.spotify.com/v1/audio-analysis/{entity_id}",
            "danceability": SpotifyMockFactory._random_confidence("danceability", **kwargs),
            "duration_ms": kwargs.get("duration_ms", randint(90000, 360000)),
            "energy": SpotifyMockFactory._random_confidence("energy", **kwargs),
            "id": entity_id,
            "instrumentalness": SpotifyMockFactory._random_confidence("instrumentalness", **kwargs),
            "key": kwargs.get("key", randint(0, 11)),
            "liveness": SpotifyMockFactory._random_confidence("liveness", **kwargs),
            "loudness": kwargs.get("loudness", randint(-60, 3)),
            "mode": kwargs.get("mode", SpotifyMockFactory._random_boolean()),
            "speechiness": SpotifyMockFactory._random_confidence("speechiness", **kwargs),
            "tempo": kwargs.get("tempo", uniform(40, 200)),
            "time_signature": kwargs.get("time_signature", randint(0, 5)),
            "track_href": SpotifyMockFactory.href(entity_type=entity_type, entity_id=entity_id),
            "type": "audio_features",
            "uri": SpotifyMockFactory.uri(entity_type=entity_type, entity_id=entity_id),
            "valence": SpotifyMockFactory._random_confidence("valence", **kwargs),
        }

    @staticmethod
    def chapter(**kwargs) -> dict:
        entity_type = "episode"
        entity_id = kwargs.get("id", SpotifyMockFactory.spotify_id())
        description = kwargs.get("description", SpotifyMockFactory.description())

        return {
            "audio_preview_url": kwargs.get("audio_preview_url", SpotifyMockFactory.preview_url()),
            "available_markets": kwargs.get("available_markets", SpotifyMockFactory.available_markets()),
            "chapter_number": kwargs.get("chapter_number", randint(1, 20)),
            "description": description,
            "html_description": SpotifyMockFactory.html_description(description),
            "duration_ms": kwargs.get("duration_ms", SpotifyMockFactory.duration_ms()),
            "explicit": kwargs.get("explicit", SpotifyMockFactory._random_boolean()),
            "external_urls": SpotifyMockFactory.external_urls(entity_type, entity_id),
            "href": SpotifyMockFactory.href(entity_type, entity_id),
            "id": entity_id,
            "images": kwargs.get("images", SpotifyMockFactory.images()),
            "is_playable": kwargs.get("is_playable", SpotifyMockFactory._random_boolean()),
            "languages": kwargs.get("languages", SpotifyMockFactory._random_string_array()),
            "name": kwargs.get("name", SpotifyMockFactory.name()),
            "release_date": kwargs.get("release_date", SpotifyMockFactory.release_date()),
            "release_date_precision": "day",
            "resume_point": kwargs.get("resume_point", SpotifyMockFactory.resume_point()),
            "type": entity_type,
            "uri": SpotifyMockFactory.uri(entity_type, entity_id),
            "restrictions": kwargs.get("restrictions", SpotifyMockFactory.restrictions()),
            "audiobook": kwargs.get("audiobook", SpotifyMockFactory.audiobook()),
        }

    @staticmethod
    def episode(**kwargs) -> dict:
        entity_type = "show"
        entity_id = kwargs.get("id", SpotifyMockFactory.spotify_id())
        description = kwargs.get("description", SpotifyMockFactory.description())

        return {
            "audio_preview_url": kwargs.get("audio_preview_url", SpotifyMockFactory.preview_url()),
            "description": description,
            "html_description": SpotifyMockFactory.html_description(description),
            "duration_ms": kwargs.get("duration_ms", SpotifyMockFactory.duration_ms()),
            "explicit": kwargs.get("explicit", SpotifyMockFactory._random_boolean()),
            "external_urls": SpotifyMockFactory.external_urls(entity_type, entity_id),
            "href": SpotifyMockFactory.href(entity_type, entity_id),
            "id": entity_id,
            "images": kwargs.get("images", SpotifyMockFactory.images()),
            "is_externally_hosted": kwargs.get("is_externally_hosted", SpotifyMockFactory._random_boolean()),
            "is_playable": kwargs.get("is_playable", SpotifyMockFactory._random_boolean()),
            "language": kwargs.get("language", random_alphanumeric_string()),
            "languages": kwargs.get("languages", SpotifyMockFactory._random_string_array()),
            "name": kwargs.get("name", SpotifyMockFactory.name()),
            "release_date": kwargs.get("release_date", SpotifyMockFactory.release_date()),
            "release_date_precision": "day",
            "resume_point": kwargs.get("resume_point", SpotifyMockFactory.resume_point()),
            "type": entity_type,
            "uri": SpotifyMockFactory.uri(entity_type, entity_id),
            "restrictions": kwargs.get("restrictions", SpotifyMockFactory.restrictions()),
            "show": kwargs.get("show", SpotifyMockFactory.show()),
        }

    @staticmethod
    def description() -> str:
        return random_alphanumeric_string()

    @staticmethod
    def html_description(description: Optional[str] = None) -> str:
        description_text = description or random_alphanumeric_string()
        return f"<p>{description_text}</p>"

    @staticmethod
    def album_type() -> str:
        return choice(["album", "single", "compilation"])

    @staticmethod
    def available_markets() -> List[str]:
        return SpotifyMockFactory._random_string_array()

    @staticmethod
    def disc_number() -> int:
        return randint(1, 2)

    @staticmethod
    def duration_ms() -> int:
        return randint(90000, 360000)

    @staticmethod
    def external_urls(entity_type: str, entity_id: str) -> Dict[str, str]:
        return {"spotify": f"https://open.spotify.com/{entity_type}/{entity_id}"}

    @staticmethod
    def external_ids() -> Dict[str, str]:
        return {"isrc": random_alphanumeric_string()}

    @staticmethod
    def href(entity_type: str, entity_id: str, extra_routes: Optional[List[str]] = None) -> str:
        href = f"https://api.spotify.com/v1/{entity_type}/{entity_id}"

        if extra_routes:
            formatted_routes = [route.strip("/") for route in extra_routes]
            joined_route = "/".join(formatted_routes)
            href += f"/{joined_route}"

        return href

    @staticmethod
    def followers(number: Optional[int] = None) -> dict:
        followers_number = number or randint(500, 50000000)
        return {"href": None, "total": followers_number}

    @staticmethod
    def genres(length: Optional[int] = None) -> List[str]:
        genres_number = length or randint(0, 5)
        return SpotifyMockFactory._random_string_array(genres_number)

    @staticmethod
    def images() -> List[Dict[str, str]]:
        return [SpotifyMockFactory._random_image(size) for size in [640, 320, 160]]

    @staticmethod
    def name() -> str:
        return random_alphanumeric_string()

    @staticmethod
    def popularity() -> int:
        return randint(0, 100)

    @staticmethod
    def preview_url() -> str:
        preview_id = random_alphanumeric_string(min_length=40, max_length=40)
        return f"https://p.scdn.co/mp3-preview/{preview_id}"

    @staticmethod
    def release_date() -> str:
        raw_date = SpotifyMockFactory._random_datetime()
        return raw_date.strftime("%Y-%m-%d")

    @staticmethod
    def track_number() -> int:
        return randint(1, 20)

    @staticmethod
    def uri(entity_type: str, entity_id: str) -> str:
        return f"spotify:{entity_type}:{entity_id}"

    @staticmethod
    def some_uris(entity_type: str, length: Optional[int] = None) -> List[str]:
        number_of_uris = length or randint(2, 10)
        uris = []

        for _ in range(number_of_uris):
            uri = SpotifyMockFactory.uri(entity_type=entity_type, entity_id=SpotifyMockFactory.spotify_id())
            uris.append(uri)

        return uris

    @staticmethod
    def user_profile(entity_id: Optional[str] = None) -> dict:
        entity_type = "user"
        if entity_id is None:
            entity_id = SpotifyMockFactory.spotify_id()

        return {
            "country": random_alphanumeric_string(),
            "display_name": random_alphanumeric_string(),
            "email": random_alphanumeric_string(),
            "explicit_content": {
                "filter_enabled": SpotifyMockFactory._random_boolean(),
                "filter_locked": SpotifyMockFactory._random_boolean(),
            },
            "external_urls": SpotifyMockFactory.external_urls(entity_type=entity_type, entity_id=entity_id),
            "followers": SpotifyMockFactory.followers(),
            "href": SpotifyMockFactory.href(entity_type=entity_type, entity_id=entity_id),
            "id": entity_id,
            "images": SpotifyMockFactory.images(),
            "product": choice(["premium", "free"]),
            "type": entity_type,
            "uri": SpotifyMockFactory.uri(entity_type=entity_type, entity_id=entity_id),
        }

    @staticmethod
    def user_top_items(items_type: ItemsType) -> dict:
        total_tracks = randint(1, 10)
        href = SpotifyMockFactory.href(entity_type="me", entity_id="", extra_routes=["top", items_type.value])

        if items_type == ItemsType.ARTISTS:
            items = SpotifyMockFactory._some_artists()
        else:
            items = SpotifyMockFactory._some_tracks()

        return {
            "href": href,
            "limit": 50,
            "next": None,
            "offset": 0,
            "previous": None,
            "total": total_tracks,
            "items": items,
        }

    @staticmethod
    def search_item() -> SearchItem:
        search_types = SpotifyMockFactory._random_multi_enum_values(SpotifySearchType) or [SpotifySearchType.TRACK]
        return SearchItem(
            text=random_alphanumeric_string(),
            filters=SearchItemFilters(
                track=SpotifyMockFactory._optional_random_alphanumeric_string(),
                artist=SpotifyMockFactory._optional_random_alphanumeric_string(),
                album=SpotifyMockFactory._optional_random_alphanumeric_string(),
                year=SpotifyMockFactory._an_optional(lambda: SpotifyMockFactory._random_datetime().year),
            ),
            metadata=SearchItemMetadata(
                search_types=search_types,
                quote=SpotifyMockFactory._random_boolean(),
            ),
        )

    @staticmethod
    def search_response(search_item: SearchItem) -> Dict[str, dict]:
        search_types_method_mapping = {
            SpotifySearchType.ALBUM: SpotifyMockFactory.album,
            SpotifySearchType.ARTIST: SpotifyMockFactory.album,
            SpotifySearchType.AUDIOBOOK: SpotifyMockFactory.audiobook,
            SpotifySearchType.EPISODE: SpotifyMockFactory.episode,
            SpotifySearchType.PLAYLIST: SpotifyMockFactory.playlist,
            SpotifySearchType.SHOW: SpotifyMockFactory.show,
            SpotifySearchType.TRACK: SpotifyMockFactory.track,
        }
        builder = SearchResponseBuilder(search_item)

        for search_type in search_item.metadata.search_types:
            search_type_method = search_types_method_mapping[search_type]
            items = SpotifyMockFactory._some_items(search_type_method)
            builder.add(search_type, items)

        return builder.build()

    @staticmethod
    def _several_items(method: Callable[..., dict], ids: Optional[List[str]], key: str) -> Dict[str, List[dict]]:
        if ids:
            items = [method(id=item_id) for item_id in ids]
        else:
            items = SpotifyMockFactory._some_items(method)

        return {key: items}

    @staticmethod
    def _some_items(method: Callable[..., dict]) -> List[dict]:
        return [method() for _ in range(randint(1, 10))]

    @staticmethod
    def _random_image(size: int) -> dict:
        image_id = random_alphanumeric_string(min_length=40, max_length=40)
        return {"url": f"https://i.scdn.co/image/{image_id}", "height": size, "width": size}

    @staticmethod
    def _some_artists() -> List[dict]:
        return SpotifyMockFactory._some_items(SpotifyMockFactory.artist)

    @staticmethod
    def _some_tracks() -> List[dict]:
        return SpotifyMockFactory._some_items(SpotifyMockFactory.track)

    @staticmethod
    def _some_playlists() -> List[dict]:
        return SpotifyMockFactory._some_items(SpotifyMockFactory.playlist)

    @staticmethod
    def _random_string_array(length: Optional[int] = None) -> List[str]:
        n_elements = length or randint(0, 10)
        return [random_alphanumeric_string() for _ in range(n_elements)]

    @staticmethod
    def _random_boolean() -> bool:
        return choice([True, False])

    @staticmethod
    def _random_datetime() -> datetime:
        current_year = datetime.now().year
        year = randint(1950, current_year)
        month = randint(1, 12)
        _, last_month_day = monthrange(year, month)
        day = randint(1, last_month_day)

        return datetime(year, month, day)

    @staticmethod
    def _random_confidence(key: str, **kwargs) -> float:
        return kwargs.get(key, random())

    @staticmethod
    def resume_point(**kwargs) -> dict:
        return {
            "fully_played": kwargs.get("fully_played", SpotifyMockFactory._random_boolean()),
            "resume_position_ms": kwargs.get("resume_position_ms", SpotifyMockFactory.duration_ms()),
        }

    @staticmethod
    def restrictions(**kwargs) -> dict:
        return {"reason": kwargs.get("reason", random_alphanumeric_string())}

    @staticmethod
    def audiobook(**kwargs) -> dict:
        entity_type = "audiobook"
        entity_id = kwargs.get("id", SpotifyMockFactory.spotify_id())
        description = kwargs.get("description", SpotifyMockFactory.description())

        return {
            "authors": kwargs.get("authors", SpotifyMockFactory.some_authors()),
            "available_markets": kwargs.get("available_markets", SpotifyMockFactory.available_markets()),
            "copyrights": kwargs.get("copyrights", SpotifyMockFactory.some_copyrights()),
            "description": description,
            "html_description": SpotifyMockFactory.html_description(description),
            "edition": kwargs.get("edition", random_alphanumeric_string()),
            "explicit": kwargs.get("explicit", SpotifyMockFactory._random_boolean()),
            "external_urls": SpotifyMockFactory.external_urls(entity_type, entity_id),
            "href": SpotifyMockFactory.href(entity_type, entity_id),
            "id": entity_id,
            "images": kwargs.get("images", SpotifyMockFactory.images()),
            "languages": kwargs.get("languages", SpotifyMockFactory._random_string_array()),
            "media_type": kwargs.get("media_type", random_alphanumeric_string()),
            "name": kwargs.get("name", SpotifyMockFactory.name()),
            "narrators": kwargs.get("narrators", SpotifyMockFactory.some_narrators()),
            "publisher": kwargs.get("publisher", random_alphanumeric_string()),
            "type": entity_type,
            "uri": SpotifyMockFactory.uri(entity_type, entity_id),
            "total_chapters": kwargs.get("total_chapters", randint(1, 20)),
        }

    @staticmethod
    def show(**kwargs) -> dict:
        entity_type = "show"
        entity_id = kwargs.get("id", SpotifyMockFactory.spotify_id())
        description = kwargs.get("description", SpotifyMockFactory.description())

        return {
            "available_markets": kwargs.get("available_markets", SpotifyMockFactory.available_markets()),
            "copyrights": kwargs.get("copyrights", SpotifyMockFactory.some_copyrights()),
            "description": description,
            "html_description": SpotifyMockFactory.html_description(description),
            "explicit": kwargs.get("explicit", SpotifyMockFactory._random_boolean()),
            "external_urls": SpotifyMockFactory.external_urls(entity_type, entity_id),
            "href": SpotifyMockFactory.href(entity_type, entity_id),
            "id": entity_id,
            "images": kwargs.get("images", SpotifyMockFactory.images()),
            "is_externally_hosted": kwargs.get("is_externally_hosted", SpotifyMockFactory._random_boolean()),
            "languages": kwargs.get("languages", SpotifyMockFactory._random_string_array()),
            "media_type": kwargs.get("media_type", random_alphanumeric_string()),
            "name": kwargs.get("name", SpotifyMockFactory.name()),
            "publisher": kwargs.get("publisher", random_alphanumeric_string()),
            "type": entity_type,
            "uri": SpotifyMockFactory.uri(entity_type, entity_id),
            "total_episodes": kwargs.get("total_episodes", randint(1, 20)),
        }

    @staticmethod
    def some_authors(length: Optional[int] = None) -> List[dict]:
        number_of_authors = length or randint(2, 10)
        return [SpotifyMockFactory.author() for _ in range(number_of_authors)]

    @staticmethod
    def author(**kwargs) -> dict:
        return {"name": kwargs.get("name", SpotifyMockFactory.name())}

    @staticmethod
    def some_copyrights(length: Optional[int] = None) -> List[dict]:
        number_of_copyrights = length or randint(2, 10)
        return [SpotifyMockFactory.copyright() for _ in range(number_of_copyrights)]

    @staticmethod
    def copyright(**kwargs) -> dict:
        return {
            "text": kwargs.get("text", random_alphanumeric_string()),
            "type": kwargs.get("type", choice(["C", "P"])),
        }

    @staticmethod
    def some_narrators(length: Optional[int] = None) -> List[dict]:
        number_of_authors = length or randint(2, 10)
        return [SpotifyMockFactory.author() for _ in range(number_of_authors)]

    @staticmethod
    def narrator(**kwargs) -> dict:
        return {"name": kwargs.get("name", SpotifyMockFactory.name())}

    @staticmethod
    def matching_entity(**kwargs) -> MatchingEntity:
        return MatchingEntity(
            track=kwargs.get("track", random_alphanumeric_string()),
            artist=kwargs.get("artist", random_alphanumeric_string()),
        )

    @staticmethod
    def _optional_random_alphanumeric_string() -> Optional[str]:
        return SpotifyMockFactory._an_optional(random_alphanumeric_string)

    @staticmethod
    def _an_optional(value_generator: Callable[[], Any]) -> Optional[Any]:
        if SpotifyMockFactory._random_boolean():
            return value_generator()

    @staticmethod
    def _random_multi_enum_values(enum_: Type[EnumType]) -> List[EnumType]:
        return [v for v in enum_ if SpotifyMockFactory._random_boolean()]
