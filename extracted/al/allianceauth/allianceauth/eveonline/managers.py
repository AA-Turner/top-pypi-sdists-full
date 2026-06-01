from datetime import datetime, timezone
from typing import TYPE_CHECKING, cast

from httpx import Response

from django.apps import apps
from django.db import transaction
from django.db.models import Manager, QuerySet
from django.db.utils import IntegrityError

from esi.exceptions import HTTPNotModified

from allianceauth.eveonline.providers import open_api_provider

if TYPE_CHECKING:
    from esi.stubs import (
        AllianceDetail, AllianceID, CharacterID, CharactersDetail,
        CorporationID, CorporationsDetail, FactionID, UniverseFactionsGetItem,
    )

    from allianceauth.eveonline.models import (
        EveAllianceInfo, EveCharacter, EveCorporationInfo, EveFactionInfo,
    )


def _eve_alliance_model() -> "type[EveAllianceInfo]":
    return cast("type[EveAllianceInfo]", apps.get_model("eveonline", "EveAllianceInfo"))


def _eve_corporation_model() -> "type[EveCorporationInfo]":
    return cast("type[EveCorporationInfo]", apps.get_model("eveonline", "EveCorporationInfo"))


def _eve_faction_model() -> "type[EveFactionInfo]":
    return cast("type[EveFactionInfo]", apps.get_model("eveonline", "EveFactionInfo"))


_DOOMHEIM_CORPORATION_ID = 1000001


class EveCharacterManager(Manager["EveCharacter"]):

    def exclude_biomassed(self) -> QuerySet["EveCharacter"]:
        """
        Get a queryset of EveCharacter objects, excluding the "Doomheim" corporation (1000001).

        :return:
        :rtype:
        """

        return self.exclude(corporation_id=_DOOMHEIM_CORPORATION_ID)

    def create_character(self, character_id) -> "EveCharacter":
        character, response = open_api_provider.get_character(character_id=character_id, use_etag=False)  # ETAG False, We need response data to create a character object.
        return self.create_character_obj(character_id, character, response)  # ETAG False, We need response data to create a character object.

    def create_character_obj(self, character_id: "CharacterID", character: "CharactersDetail", response: Response) -> "EveCharacter":
        corporation_model = _eve_corporation_model()
        alliance_model = _eve_alliance_model()
        faction_model = _eve_faction_model()

        corporation_id = character.corporation_id
        try:
            corporation_obj = corporation_model.objects.get(corporation_id=corporation_id)
        except corporation_model.DoesNotExist:
            corporation_obj = corporation_model.objects.create_corporation(corporation_id=corporation_id)

        if character.alliance_id:
            try:
                alliance_obj = alliance_model.objects.get(alliance_id=character.alliance_id)
            except alliance_model.DoesNotExist:
                alliance_obj = alliance_model.objects.create_alliance(alliance_id=character.alliance_id)
        else:
            alliance_obj = None

        if character.faction_id:
            try:
                faction_obj = faction_model.objects.get(faction_id=character.faction_id)
            except faction_model.DoesNotExist:
                faction_obj = faction_model.objects.create_faction(faction_id=character.faction_id)
        else:
            faction_obj = None

        return self.create(
            character_id=character_id,
            alliance_id=character.alliance_id if character.alliance_id else None,
            birthday=character.birthday,
            bloodline_id=character.bloodline_id,
            corporation_id=corporation_id,
            description=character.description if character.description else "",
            faction_id=character.faction_id if character.faction_id else None,
            gender=character.gender,
            character_name=character.name,
            race_id=character.race_id,
            security_status=character.security_status if character.security_status else 0.0,
            title=character.title if character.title else "",
            corporation_name=corporation_obj.corporation_name,
            corporation_ticker=corporation_obj.corporation_ticker,
            alliance_name=alliance_obj.alliance_name if alliance_obj else "",
            alliance_ticker=alliance_obj.alliance_ticker if alliance_obj else "",
            faction_name=faction_obj.faction_name if faction_obj else "",
            last_updated=datetime.strptime(response.headers.get("Last-Modified"), "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone.utc)
        )

    def update_character(self, character_id) -> "EveCharacter":
        return self.get(character_id=character_id).update_character()

    def get_character_by_id(self, character_id: "CharacterID") -> "EveCharacter | None":
        """Return character by character ID or None if not found."""
        try:
            return self.get(character_id=character_id)
        except self.model.DoesNotExist:
            return None


class EveAllianceManager(Manager["EveAllianceInfo"]):

    def create_alliance(self, alliance_id: "AllianceID") -> "EveAllianceInfo":
        alliance, response = open_api_provider.get_alliance(alliance_id=alliance_id, use_etag=False)  # ETAG False, We need response data to create an alliance object.
        return self.create_alliance_obj(alliance_id, alliance, response)
        # do not populate corporations here, let a scheduled task handle that.

    def create_alliance_obj(self, alliance_id: "AllianceID", alliance: "AllianceDetail", response: Response) -> "EveAllianceInfo":
        faction_model = _eve_faction_model()

        if alliance.faction_id:
            try:
                faction_obj = faction_model.objects.get(faction_id=alliance.faction_id)
            except faction_model.DoesNotExist:
                faction_obj = faction_model.objects.create_faction(faction_id=alliance.faction_id)
        else:
            faction_obj = None

        return self.create(
            alliance_id=alliance_id,
            creator_corporation_id=alliance.creator_corporation_id,
            creator_id=alliance.creator_id,
            date_founded=alliance.date_founded,
            executor_corp_id=alliance.executor_corporation_id,
            faction=faction_obj,
            alliance_name=alliance.name,
            alliance_ticker=alliance.ticker,
            last_updated=datetime.strptime(response.headers.get("Last-Modified"), "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone.utc)
        )

    def get_or_create_esi(self, alliance_id: "AllianceID") -> "EveAllianceInfo":
        try:
            return self.get(alliance_id=alliance_id)
        except self.model.DoesNotExist:
            try:
                with transaction.atomic():
                    return self.create_alliance(alliance_id=alliance_id)
            except IntegrityError:
                return self.get(alliance_id=alliance_id)

    def update_alliance(self, alliance_id) -> "EveAllianceInfo":
        return self.get(alliance_id=alliance_id).update_alliance()


class EveCorporationManager(Manager["EveCorporationInfo"]):
    def exclude_closed(self) -> QuerySet["EveCorporationInfo"]:
        """
        Get a queryset of EveCorporationInfo objects, excluding those with a CEO ID of 1.

        :return:
        :rtype:
        """

        return self.exclude(ceo_id=1)

    def create_corporation(self, corporation_id: "CorporationID",) -> "EveCorporationInfo":
        corporation, response = open_api_provider.get_corporation(corporation_id=corporation_id, use_etag=False)  # ETAG False, We need response data to create a corporation object.
        return self.create_corporation_obj(corporation_id=corporation_id, corporation=corporation, response=response,)

    def create_corporation_obj(self, corporation_id: "CorporationID", corporation: "CorporationsDetail", response: Response,) -> "EveCorporationInfo":
        alliance_model = _eve_alliance_model()
        faction_model = _eve_faction_model()

        if corporation.alliance_id:
            try:
                alliance_obj = alliance_model.objects.get(alliance_id=corporation.alliance_id)
            except alliance_model.DoesNotExist:
                alliance_obj = alliance_model.objects.create_alliance(alliance_id=corporation.alliance_id)
        else:
            alliance_obj = None

        if corporation.faction_id:
            try:
                faction_obj = faction_model.objects.get(faction_id=corporation.faction_id)
            except faction_model.DoesNotExist:
                faction_obj = faction_model.objects.create_faction(faction_id=corporation.faction_id)
        else:
            faction_obj = None

        return self.create(
            corporation_id=corporation_id,
            alliance=alliance_obj,
            ceo_id=corporation.ceo_id,
            creator_id=corporation.creator_id,
            date_founded=corporation.date_founded if corporation.date_founded else None,
            description=corporation.description if corporation.description else "",
            faction=faction_obj,
            home_station_id=corporation.home_station_id if corporation.home_station_id else None,
            member_count=corporation.member_count,
            corporation_name=corporation.name,
            shares=corporation.shares if corporation.shares else None,
            tax_rate=corporation.tax_rate,
            corporation_ticker=corporation.ticker,
            url=corporation.url if corporation.url and len(corporation.url) <= 2048 else "",
            war_eligible=corporation.war_eligible if corporation.war_eligible else False,
            last_updated=datetime.strptime(response.headers.get("Last-Modified"), "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone.utc)
        )

    def get_or_create_esi(self, corporation_id: "CorporationID") -> "EveCorporationInfo":
        try:
            return self.get(corporation_id=corporation_id)
        except self.model.DoesNotExist:
            try:
                with transaction.atomic():
                    return self.create_corporation(corporation_id=corporation_id)
            except IntegrityError:
                return self.get(corporation_id=corporation_id)

    def update_corporation(self, corp_id: int) -> "EveCorporationInfo":
        return self.get(corporation_id=corp_id).update_corporation()


class EveFactionManager(Manager["EveFactionInfo"]):

    def create_faction(self, faction_id: "FactionID") -> "EveFactionInfo":
        faction, response = open_api_provider.get_faction(faction_id=faction_id, use_etag=False)  # ETAG False, We need response data to create a faction object.
        return self.create_faction_obj(faction=faction, response=response)

    def create_faction_obj(self, faction: "UniverseFactionsGetItem", response: Response) -> "EveFactionInfo":

        return self.create(
            faction_id=faction.faction_id,
            corporation_id=faction.corporation_id if faction.corporation_id else None,
            description=faction.description,
            # is_unique boolean required # skipped
            militia_corporation_id=faction.militia_corporation_id if faction.militia_corporation_id else None,
            faction_name=faction.name,
            size_factor=faction.size_factor,
            solar_system_id=faction.solar_system_id,
            station_count=faction.station_count,
            station_system_count=faction.station_system_count,
            last_updated=datetime.strptime(response.headers.get("Last-Modified"), "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone.utc)
        )

    def get_or_create_esi(self, faction_id: "FactionID") -> "EveFactionInfo":
        try:
            return self.get(faction_id=faction_id)
        except self.model.DoesNotExist:
            try:
                with transaction.atomic():
                    return self.create_faction(faction_id=faction_id)
            except IntegrityError:
                return self.get(faction_id=faction_id)

    def update_factions(self) :
        try:
            factions, response = open_api_provider.get_all_factions(use_etag=True)
        except HTTPNotModified:
            # nothing to update
            return self

        for faction in factions:
            obj, created = self.get_or_create(faction_id=faction.faction_id)
            obj.corporation_id = faction.corporation_id if faction.corporation_id else None
            obj.description = faction.description if faction.description else ""
            # obj.is_unique = faction.is_unique
            obj.militia_corporation_id = faction.militia_corporation_id if faction.militia_corporation_id else None
            obj.faction_name = faction.name
            obj.size_factor = faction.size_factor if faction.size_factor else None
            obj.solar_system_id = faction.solar_system_id if faction.solar_system_id else None
            obj.station_count = faction.station_count if faction.station_count else None
            obj.station_system_count = faction.station_system_count if faction.station_system_count else None
            obj.last_updated = datetime.strptime(response.headers.get("Last-Modified"), "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone.utc)
            obj.save()
