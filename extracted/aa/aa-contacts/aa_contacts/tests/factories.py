from __future__ import annotations

from itertools import count
from typing import TYPE_CHECKING

from allianceauth.authentication.models import CharacterOwnership
from allianceauth.eveonline.models import (
    EveAllianceInfo,
    EveCharacter,
    EveCorporationInfo,
)
from allianceauth.tests.auth_utils import AuthUtils
from esi.models import Scope, Token

if TYPE_CHECKING:
    from django.contrib.auth.models import User

DEFAULT_SCOPES = ["publicData"]

# High ID ranges, so generated objects never collide with the IDs
# hardcoded elsewhere in the test suite.
_ALLIANCE_ID_BASE = 99_000_000
_CORPORATION_ID_BASE = 98_000_000
_CHARACTER_ID_BASE = 90_000_000

_alliance_ids = count(_ALLIANCE_ID_BASE + 1)
_corporation_ids = count(_CORPORATION_ID_BASE + 1)
_character_ids = count(_CHARACTER_ID_BASE + 1)
_owner_hashes = count(1)


def create_eve_alliance(**kwargs) -> EveAllianceInfo:
    num = next(_alliance_ids)
    params = {
        "alliance_id": num,
        "alliance_name": f"Alliance {num}",
        "alliance_ticker": f"A{num - _ALLIANCE_ID_BASE}",
        "executor_corp_id": 0,
    }
    params.update(kwargs)
    return EveAllianceInfo.objects.create(**params)


def create_eve_corporation(
    alliance: EveAllianceInfo | None = None,
    *,
    create_alliance: bool = True,
    **kwargs,
) -> EveCorporationInfo:
    """Create a corporation, with its own alliance unless told otherwise."""
    num = next(_corporation_ids)
    params = {
        "corporation_id": num,
        "corporation_name": f"Corporation {num}",
        "corporation_ticker": f"C{num - _CORPORATION_ID_BASE}",
        "member_count": 100,
    }
    params.update(kwargs)
    if alliance is None and create_alliance:
        alliance = create_eve_alliance(executor_corp_id=params["corporation_id"])
    params["alliance"] = alliance
    return EveCorporationInfo.objects.create(**params)


def create_eve_character(
    corporation: EveCorporationInfo | None = None, **kwargs
) -> EveCharacter:
    """Create a character, copying its corporation and alliance details onto it."""
    num = next(_character_ids)
    if corporation is None:
        corporation = create_eve_corporation()
    alliance = corporation.alliance
    params = {
        "character_id": num,
        "character_name": f"Character {num}",
        "corporation_id": corporation.corporation_id,
        "corporation_name": corporation.corporation_name,
        "corporation_ticker": corporation.corporation_ticker,
        "alliance_id": alliance.alliance_id if alliance else None,
        "alliance_name": alliance.alliance_name if alliance else "",
        "alliance_ticker": alliance.alliance_ticker if alliance else "",
    }
    params.update(kwargs)
    return EveCharacter.objects.create(**params)


def add_new_token(
    user: User, character: EveCharacter, scopes: list[str] | None = None
) -> Token:
    """Generate a new ESI token for the given character, owned by the given user."""
    if not scopes:
        scopes = DEFAULT_SCOPES

    existing = user.token_set.filter(character_id=character.character_id).first()
    owner_hash = (
        existing.character_owner_hash
        if existing
        else f"owner-hash-{next(_owner_hashes)}"
    )

    token = Token.objects.create(
        access_token="access_token",  # noqa: S106
        refresh_token="refresh_token",  # noqa: S106
        user=user,
        character_id=character.character_id,
        character_name=character.character_name,
        character_owner_hash=owner_hash,
    )
    for scope_name in scopes:
        scope, _ = Scope.objects.get_or_create(name=scope_name)
        token.scopes.add(scope)

    return token


def add_character_to_user(
    user: User,
    character: EveCharacter,
    *,
    is_main: bool = False,
    scopes: list[str] | None = None,
) -> CharacterOwnership:
    """Make the given user the owner of the given (already existing) character."""
    add_new_token(user, character, scopes)

    if is_main:
        user.profile.main_character = character
        user.profile.save()
        user.save()

    return CharacterOwnership.objects.get(user=user, character=character)


def create_user_main(
    permissions: list[str] | None = None,
    character: EveCharacter | None = None,
    scopes: list[str] | None = None,
    **kwargs,
) -> User:
    """Create a user with a main character and (optional) permissions."""
    if character is None:
        character = create_eve_character()

    user = AuthUtils.create_user(character.character_name.replace(" ", "_"))
    if kwargs:
        for field, value in kwargs.items():
            setattr(user, field, value)
        user.save()

    add_character_to_user(user, character, is_main=True, scopes=scopes)

    if permissions:
        user = AuthUtils.add_permissions_to_user_by_name(permissions, user)

    return user
