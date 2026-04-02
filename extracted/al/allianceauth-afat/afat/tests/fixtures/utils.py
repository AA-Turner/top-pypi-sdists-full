"""
Test utilities
"""

# Standard Library
import datetime as dt
import re

# Django
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.crypto import get_random_string

# Alliance Auth
from allianceauth.authentication.models import CharacterOwnership
from allianceauth.eveonline.models import EveCharacter
from allianceauth.tests.auth_utils import AuthUtils
from esi.models import Scope, Token


class RequestStub:
    """
    Request Stub
    """

    def __init__(self, user) -> None:
        """
        Initializes the RequestStub.

        :param user:
        :type user:
        """

        self.user = user


def _store_as_Token(token: dict, user: object) -> Token:
    """
    Stores the given token dict as a Token object for the given user.

    :param token:
    :type token:
    :param user:
    :type user:
    :return:
    :rtype:
    """

    character_tokens = user.token_set.filter(character_id=token["CharacterID"])

    if character_tokens.exists():
        token["CharacterOwnerHash"] = character_tokens.first().character_owner_hash

    obj = Token.objects.create(
        access_token=token["access_token"],
        refresh_token=token["refresh_token"],
        user=user,
        character_id=token["CharacterID"],
        character_name=token["CharacterName"],
        token_type=token["TokenType"],
        character_owner_hash=token["CharacterOwnerHash"],
    )

    for scope_name in token["Scopes"].split(" "):
        scope, _ = Scope.objects.get_or_create(name=scope_name)
        obj.scopes.add(scope)

    return obj


def dt_eveformat(my_dt: dt.datetime) -> str:
    """
    converts a datetime to a string in eve format

    :param my_dt:
    :type my_dt:
    :return:
    :rtype:
    """

    my_dt_2 = dt.datetime(
        my_dt.year, my_dt.month, my_dt.day, my_dt.hour, my_dt.minute, my_dt.second
    )

    return my_dt_2.isoformat()


def add_new_token(
    user: User,
    character: EveCharacter,
    scopes: list[str] | None = None,
    owner_hash: str | None = None,
) -> Token:
    """
    Generates and stores a new SSO test token for the given user and character.

    :param user:
    :type user:
    :param character:
    :type character:
    :param scopes:
    :type scopes:
    :param owner_hash:
    :type owner_hash:
    :return:
    :rtype:
    """

    return _store_as_Token(
        _generate_token(
            character_id=character.character_id,
            character_name=character.character_name,
            owner_hash=owner_hash,
            scopes=scopes,
        ),
        user,
    )


def _generate_token(
    character_id: int,
    character_name: str,
    owner_hash: str | None = None,
    access_token: str = "access_token",
    refresh_token: str = "refresh_token",
    scopes: list | None = None,
    timestamp_dt: dt.datetime | None = None,
    expires_in: int = 1200,
) -> dict:
    """
    Generates a SSO test token dict.

    :param character_id:
    :type character_id:
    :param character_name:
    :type character_name:
    :param owner_hash:
    :type owner_hash:
    :param access_token:
    :type access_token:
    :param refresh_token:
    :type refresh_token:
    :param scopes:
    :type scopes:
    :param timestamp_dt:
    :type timestamp_dt:
    :param expires_in:
    :type expires_in:
    :return:
    :rtype:
    """

    if timestamp_dt is None:
        timestamp_dt = timezone.now()

    if scopes is None:
        scopes = [
            "esi-mail.read_mail.v1",
            "esi-wallet.read_character_wallet.v1",
            "esi-universe.read_structures.v1",
        ]

    if owner_hash is None:
        owner_hash = get_random_string(length=28)

    token = {
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": expires_in,
        "refresh_token": refresh_token,
        "timestamp": int(timestamp_dt.timestamp()),
        "CharacterID": character_id,
        "CharacterName": character_name,
        "ExpiresOn": dt_eveformat(timestamp_dt + dt.timedelta(seconds=expires_in)),
        "Scopes": " ".join(list(scopes)),
        "TokenType": "Character",
        "CharacterOwnerHash": owner_hash,
        "IntellectualProperty": "EVE",
    }

    return token


def add_character_to_user(
    user: User,
    character: EveCharacter,
    is_main: bool = False,
    scopes: list[str] | None = None,
    disconnect_signals: bool = False,
) -> CharacterOwnership:
    """
    Adds the given character to the given user.

    :param user:
    :type user:
    :param character:
    :type character:
    :param is_main:
    :type is_main:
    :param scopes:
    :type scopes:
    :param disconnect_signals:
    :type disconnect_signals:
    :return:
    :rtype:
    """

    if not scopes:
        scopes = ["publicData"]

    if disconnect_signals:
        AuthUtils.disconnect_signals()

    add_new_token(user, character, scopes)

    if is_main:
        user.profile.main_character = character
        user.profile.save()
        user.save()

    if disconnect_signals:
        AuthUtils.connect_signals()

    return CharacterOwnership.objects.get(user=user, character=character)


def create_user_from_evecharacter(
    character_id: int,
    permissions: list[str] | None = None,
    scopes: list[str] | None = None,
) -> tuple[User, CharacterOwnership]:
    """
    Creates a user from the given EveCharacter ID, assigns the given permissions and scopes.

    :param character_id:
    :type character_id:
    :param permissions:
    :type permissions:
    :param scopes:
    :type scopes:
    :return:
    :rtype:
    """

    auth_character = EveCharacter.objects.get(character_id=character_id)
    user = AuthUtils.create_user(auth_character.character_name.replace(" ", "_"))
    character_ownership = add_character_to_user(
        user, auth_character, is_main=True, scopes=scopes
    )

    if permissions:
        for permission_name in permissions:
            user = AuthUtils.add_permission_to_user_by_name(permission_name, user)

    return user, character_ownership


def create_fake_user(
    character_id: int,
    character_name: str,
    corporation_id: int = None,
    corporation_name: str = None,
    corporation_ticker: str = None,
    permissions: list[str] = None,
    **kwargs,
) -> User:
    """
    Create a fake user with a given character name and id.

    :param character_id:
    :type character_id:
    :param character_name:
    :type character_name:
    :param corporation_id:
    :type corporation_id:
    :param corporation_name:
    :type corporation_name:
    :param corporation_ticker:
    :type corporation_ticker:
    :param permissions:
    :type permissions:
    :param kwargs:
    :type kwargs:
    :return:
    :rtype:
    """

    username = re.sub(pattern=r"[^\w\d@\.\+-]", repl="_", string=character_name)
    user = AuthUtils.create_user(username=username)

    if not corporation_id:
        corporation_id = 2001
        corporation_name = "Wayne Technologies Inc."
        corporation_ticker = "WTE"

    alliance_id = kwargs.get("alliance_id", 3001)
    alliance_name = (
        kwargs.get("alliance_name", "Wayne Enterprises")
        if alliance_id is not None
        else ""
    )

    AuthUtils.add_main_character_2(
        user=user,
        name=character_name,
        character_id=character_id,
        corp_id=corporation_id,
        corp_name=corporation_name,
        corp_ticker=corporation_ticker,
        alliance_id=alliance_id,
        alliance_name=alliance_name,
    )

    if permissions:
        perm_objs = [AuthUtils.get_permission_by_name(perm) for perm in permissions]
        user = AuthUtils.add_permissions_to_user(perms=perm_objs, user=user)

    return user
