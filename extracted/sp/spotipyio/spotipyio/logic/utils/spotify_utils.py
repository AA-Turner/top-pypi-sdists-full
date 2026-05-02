from base64 import b64encode
from random import randint
from typing import List

from spotipyio.auth import ClientCredentials, SpotifyGrantType
from spotipyio.logic.consts.spotify_consts import ARTISTS, NAME
from spotipyio.logic.utils.general_utils import random_enum_value
from spotipyio.logic.utils.string_utils import random_alphanumeric_string
from spotipyio.models import EntityType


def to_uri(entity_id: str, entity_type: EntityType) -> str:
    return f"spotify:{entity_type.value}:{entity_id}"


def encode_bearer_token(client_id: str, client_secret: str) -> str:
    bytes_auth = bytes(f"{client_id}:{client_secret}", "ISO-8859-1")
    b64_auth = b64encode(bytes_auth)

    return b64_auth.decode("ascii")


def random_client_credentials() -> ClientCredentials:
    redirect_uri_port = randint(1000, 9999)
    return ClientCredentials(
        client_id=random_alphanumeric_string(),
        client_secret=random_alphanumeric_string(),
        redirect_uri=f"http://localhost:{redirect_uri_port}",
        grant_type=random_enum_value(SpotifyGrantType),
        access_code=random_alphanumeric_string(),
    )


def extract_artists_names(entity: dict) -> List[str]:
    artists_names = []
    artists = entity.get(ARTISTS, [])

    for artist in artists:
        artist_name = artist.get(NAME)

        if isinstance(artist_name, str):
            artists_names.append(artist_name)

    return artists_names
