__lazy_modules__ = ["allianceauth.authentication.models", "django.contrib.auth.models", "esi.models"]

import logging
from typing import TYPE_CHECKING

from django.db import transaction
from django.db.models import Manager, Q, QuerySet

from allianceauth.eveonline.models import EveCharacter

if TYPE_CHECKING:
    from django.contrib.auth.models import User

    from esi.models import Token

    from allianceauth.authentication.models import CharacterOwnership, State

logger = logging.getLogger(__name__)


def available_states_query(character: EveCharacter) -> Q:
    query = Q(public=True)
    if character.character_id:
        query |= Q(member_characters__character_id=character.character_id)
    if character.corporation_id:
        query |= Q(member_corporations__corporation_id=character.corporation_id)
    if character.alliance_id:
        query |= Q(member_alliances__alliance_id=character.alliance_id)
    if character.faction_id:
        query |= Q(member_factions__faction_id=character.faction_id)
    return query


class CharacterOwnershipManager(Manager["CharacterOwnership"]):
    def create_by_token(self, token: "Token") -> "CharacterOwnership":
        character = EveCharacter.objects.get_or_create_esi(token.character_id)
        return self.create(character=character, user=token.user, owner_hash=token.character_owner_hash)


class StateQuerySet(QuerySet["State"]):
    def available_to_character(self, character: EveCharacter) -> "QuerySet[State]":
        return self.filter(available_states_query(character))

    def available_to_user(self, user: "User") -> "QuerySet[State]":
        if user.profile.main_character:
            return self.available_to_character(user.profile.main_character)
        else:
            return self.none()

    def get_for_user(self, user: "User") -> "State":
        states = self.available_to_user(user)
        if states.exists():
            return states[0]
        else:
            from allianceauth.authentication.models import get_guest_state
            return get_guest_state()

    def delete(self) -> None:
        with transaction.atomic():
            for state in self:
                for profile in state.userprofile_set.all():
                    profile.assign_state(state=self.model.objects.exclude(pk=state.pk).get_for_user(profile.user))
        super().delete()


class StateManager(Manager["State"]):
    def get_queryset(self) -> StateQuerySet:
        return StateQuerySet(self.model, using=self._db)

    def available_to_character(self, character: EveCharacter) -> StateQuerySet:
        return self.get_queryset().available_to_character(character)

    def available_to_user(self, user: "User") -> StateQuerySet:
        return self.get_queryset().available_to_user(user)

    def get_for_character(self, character: EveCharacter) -> "State":
        states = self.get_queryset().available_to_character(character)
        if states.exists():
            return states[0]
        else:
            from allianceauth.authentication.models import get_guest_state
            return get_guest_state()

    def get_for_user(self, user: "User") -> "State":
        return self.get_queryset().get_for_user(user)
