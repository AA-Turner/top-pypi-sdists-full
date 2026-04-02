"""Utilities for making it easier to write tests."""

# pylint: disable=unused-import

import datetime as dt
import json
import logging
import os
import re
import socket
from dataclasses import dataclass
from itertools import count
from typing import Any, Dict, Iterable, List, Optional, Tuple

from django.contrib.auth.models import Group, User
from django.db import models
from django.http import HttpResponse, JsonResponse
from django.test import TestCase
from esi.models import Scope, Token

from allianceauth.authentication.models import CharacterOwnership, State
from allianceauth.eveonline.models import (
    EveAllianceInfo,
    EveCharacter,
    EveCorporationInfo,
    EveFactionInfo,
)
from allianceauth.groupmanagement.models import AuthGroup
from allianceauth.tests.auth_utils import AuthUtils
from app_utils.datetime import dt_eveformat
from app_utils.esi_testing import (  # noqa: F401
    BravadoOperationStub,
    BravadoResponseStub,
)
from app_utils.helpers import random_string


def generate_invalid_pk(MyModel: Any) -> int:
    """return an invalid PK for the given Django model"""
    pk_max = MyModel.objects.aggregate(models.Max("pk"))["pk__max"]
    return pk_max + 1 if pk_max else 1


class SocketAccessError(Exception):
    """Error raised when a test script accesses the network"""


class NoSocketsTestCase(TestCase):
    """Variation of Django's TestCase class that prevents any network use.

    Example:

        .. code-block:: python

            class TestMyStuff(NoSocketsTestCase):
                def test_should_do_what_i_need(self):
                    ...

    """

    @classmethod
    def setUpClass(cls):
        cls.socket_original = socket.socket
        socket.socket = cls.guard
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        socket.socket = cls.socket_original
        return super().tearDownClass()

    @staticmethod
    def guard(*args, **kwargs):
        """:meta_private:"""
        raise SocketAccessError("Attempted to access network")


def set_test_logger(logger_name: str, name: str) -> object:
    """set logger for current test module

    Args:
        logger: current logger object
        name: name of current module, e.g. __file__

    Returns:
        amended logger
    """

    # reconfigure logger so we get logging from tested module
    f_format = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(module)s:%(funcName)s - %(message)s"
    )
    file_name = os.path.splitext(name)[0]
    f_handler = logging.FileHandler(f"{file_name}.log", "w+")
    f_handler.setFormatter(f_format)
    my_logger = logging.getLogger(logger_name)
    my_logger.level = logging.DEBUG
    my_logger.addHandler(f_handler)
    my_logger.propagate = False
    return my_logger


def queryset_pks(queryset) -> set:
    """shortcut that returns the pks of the given queryset as set.
    Useful for comparing test results.
    """
    return set(queryset.values_list("pk", flat=True))


def response_text(response: HttpResponse) -> str:
    """Return content of a HTTP response as string."""
    return response.content.decode("utf-8")


def json_response_to_python(response: JsonResponse) -> Any:
    """Convert JSON response into Python object."""
    return json.loads(response_text(response))


def json_response_to_dict(response: JsonResponse, key="id") -> dict:
    """Convert JSON response into dict by given key."""
    return {x[key]: x for x in json_response_to_python(response)}


def multi_assert_in(items: Iterable, container: Iterable) -> bool:
    """Return True if all items are in container."""
    for item in items:
        if item not in container:
            return False

    return True


def multi_assert_not_in(items: Iterable, container: Iterable) -> bool:
    """Return True if none of the item is in container."""
    for item in items:
        if item in container:
            return False

    return True


# factories


def add_new_token(
    user: User,
    character: EveCharacter,
    scopes: Optional[List[str]] = None,
    owner_hash: Optional[str] = None,
) -> Token:
    """Generate a new token for a user based on a character."""
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
    owner_hash: Optional[str] = None,
    access_token: str = "access_token",
    refresh_token: str = "refresh_token",
    scopes: Optional[list] = None,
    timestamp_dt: Optional[dt.datetime] = None,
    expires_in: int = 1200,
) -> dict:
    """Generates the input to create a new SSO test token"""
    if timestamp_dt is None:
        timestamp_dt = dt.datetime.utcnow()
    if scopes is None:
        scopes = [
            "esi-mail.read_mail.v1",
            "esi-wallet.read_character_wallet.v1",
            "esi-universe.read_structures.v1",
        ]
    if owner_hash is None:
        owner_hash = random_string(28)
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


def _store_as_Token(token: dict, user: object) -> Token:
    """Stores a generated token dict as Token object for given user

    returns Token object
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


def create_user_from_evecharacter(
    character_id: int,
    permissions: Optional[List[str]] = None,
    scopes: Optional[List[str]] = None,
) -> Tuple[User, CharacterOwnership]:
    """Create new allianceauth user from EveCharacter object.

    Args:
        character_id: ID of eve character
        permissions: list of permission names, e.g. `"my_app.my_permission"`
        scopes: list of scope names
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


def add_character_to_user(
    user: User,
    character: EveCharacter,
    is_main: bool = False,
    scopes: Optional[List[str]] = None,
    disconnect_signals: bool = False,
) -> CharacterOwnership:
    """Generates a token for the given Eve character and makes the given user it's owner

    Args:
        user: New character owner
        character: Character to add
        is_main: Will set character as the users's main when True
        scopes: List of scopes for the token
        disconnect_signals: Will disconnect signals temporarily when True
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


def add_character_to_user_2(
    user: User,
    character_id,
    character_name,
    corporation_id,
    corporation_name,
    alliance_id=None,
    alliance_name=None,
    disconnect_signals=False,
) -> EveCharacter:
    """Creates a new EVE character and makes the given user the owner"""
    defaults = {
        "character_name": str(character_name),
        "corporation_id": int(corporation_id),
        "corporation_name": str(corporation_name),
    }
    if alliance_id:
        defaults["alliance_id"] = int(alliance_id)
        defaults["alliance_name"] = str(alliance_name)

    if disconnect_signals:
        AuthUtils.disconnect_signals()
    character, _ = EveCharacter.objects.update_or_create(
        character_id=character_id, defaults=defaults
    )
    CharacterOwnership.objects.create(
        character=character, owner_hash=f"{character_id}_{character_name}", user=user
    )
    if disconnect_signals:
        AuthUtils.connect_signals()

    return character


def create_fake_user(
    character_id: int,
    character_name: str,
    corporation_id: Optional[int] = None,
    corporation_name: Optional[str] = None,
    corporation_ticker: Optional[str] = None,
    alliance_id: Optional[int] = None,
    alliance_name: Optional[str] = None,
    permissions: Optional[List[str]] = None,
) -> User:
    """Create a fake user incl. main character and (optional) permissions.

    Will use default corporation and alliance if not set.
    """
    username = re.sub(r"[^\w\d@\.\+-]", "_", character_name)
    user = AuthUtils.create_user(username)
    if not corporation_id:
        corporation_id = 2001
        corporation_name = "Wayne Technologies Inc."
        corporation_ticker = "WTE"
    if corporation_id == 2001:
        alliance_id = 3001
        alliance_name = "Wayne Enterprises"
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


def create_authgroup(states: Optional[Iterable[State]] = None, **kwargs) -> Group:
    """Create Group object with additional Auth related properties for tests."""
    if "name" not in kwargs:
        kwargs["name"] = f"Test Group #{next_number('authgroup')}"
    name = kwargs.pop("name")
    group = Group.objects.create(name=name)
    if states:
        group.authgroup.states.add(*states)
    if kwargs:
        AuthGroup.objects.filter(group=group).update(**kwargs)
        group.authgroup.refresh_from_db()
    return group


def create_state(
    priority: int,
    permissions: Optional[Iterable[str]] = None,
    member_characters: Optional[Iterable[EveCharacter]] = None,
    member_corporations: Optional[Iterable[EveCorporationInfo]] = None,
    member_alliances: Optional[Iterable[EveAllianceInfo]] = None,
    member_factions: Optional[Iterable[EveFactionInfo]] = None,
    **kwargs,
) -> State:
    """Create a State object for tests."""
    params = {"priority": priority, "name": f"Test State #{next_number('state_name')}"}
    params.update(kwargs)
    obj = State.objects.create(**params)
    if permissions:
        perm_objs = [AuthUtils.get_permission_by_name(perm) for perm in permissions]
        obj.permissions.add(*perm_objs)
    if member_characters:
        obj.member_characters.add(*member_characters)
    if member_corporations:
        obj.member_corporations.add(*member_corporations)
    if member_alliances:
        obj.member_alliances.add(*member_alliances)
    if member_factions:
        obj.member_factions.add(*member_factions)
    return obj


def create_eve_character(
    character_id: int, character_name: str, **kwargs
) -> EveCharacter:
    """Create an EveCharacter object for tests."""
    params = {
        "character_id": character_id,
        "character_name": character_name,
        "corporation_id": 2001,
        "corporation_name": "Wayne Technologies",
        "corporation_ticker": "WYT",
        "alliance_id": 3001,
        "alliance_name": "Wayne Enterprises",
        "alliance_ticker": "WYE",
    }
    params.update(kwargs)
    return EveCharacter.objects.create(**params)


def next_number(key=None) -> int:
    """Generate consecutive numbers. Optionally numbers are generates for given key."""
    if key is None:
        key = "_general"
    try:
        return next(next_number._counter[key])
    except AttributeError:
        next_number._counter = {}
    except KeyError:
        pass
    next_number._counter[key] = count(start=1)
    return next(next_number._counter[key])


def reset_celery_once_locks(app_label: str) -> int:
    """Reset celery once locks on all tasks of an app.

    Args:
        app_label: label of the app

    Returns:
        number of deleted locks
    """
    from app_utils.allianceauth import get_redis_client

    if not app_label:
        raise ValueError("Must specify an app label")
    r = get_redis_client()
    keys = r.keys(f":?:qo_{app_label}.*")
    if not keys:
        return 0
    deleted = r.delete(*keys)
    return deleted


class CacheFake:
    """A fake for replacing Django's cache in tests.

    Example:

    .. code-block:: python

        from app_utils.testing import CacheFake

        @patch("my_module.cache", new_callable=CacheFake)
        def test_my_function(self):
            ...

    """

    DEFAULT_TIMEOUT = 3600

    @dataclass
    class Entry:
        value: Any
        timeout: float

    def __init__(self):
        self._cache: Dict[str, CacheFake.Entry] = {}

    def clear(self) -> None:
        self._cache.clear()

    def delete(self, key: str, version: int = None) -> None:
        try:
            del self._cache[key]
        except KeyError:
            pass

    def get(self, key: str, default: Any = None, version: int = None) -> Any:
        try:
            x = self._cache[key]
        except KeyError:
            return default
        return x.value

    def set(
        self, key: str, value: Any, timeout: int = None, version: int = None
    ) -> None:
        if not timeout:
            timeout = CacheFake.DEFAULT_TIMEOUT
        self._cache[key] = CacheFake.Entry(value=value, timeout=timeout)

    def ttl(self, key: str) -> Optional[float]:
        try:
            x = self._cache[key]
        except KeyError:
            return None
        return x.timeout
