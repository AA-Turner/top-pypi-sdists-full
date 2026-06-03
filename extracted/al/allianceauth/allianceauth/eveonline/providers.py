import logging
from datetime import datetime
from typing import TYPE_CHECKING

from httpx import Response

from esi.openapi_clients import ESIClientProvider

if TYPE_CHECKING:
    from esi.stubs import (
        AllianceDetail, AllianceID, AlliancesAllianceIdCorporationsGet,
        CharactersDetail, CorporationID, CorporationsDetail,
        UniverseFactionsGet, UniverseFactionsGetItem, CharacterID, FactionID
    )

from allianceauth import __title_useragent__, __url__, __version__
from allianceauth.eveonline import __esi_compatibility_date__

# for the love of Bob please add operations you use here. I'm tired of breaking undocumented things.
# Open API
OPEN_API_OPERATIONS = [
    "GetAlliancesAllianceId",
    "GetAlliancesAllianceIdCorporations",
    "GetCorporationsCorporationId",
    "GetCharactersCharacterId",
    "PostCharactersAffiliation",
    "GetUniverseFactions",
    "PostUniverseNames",

]

logger = logging.getLogger(__name__)


class EveOpenAPIProvider(ESIClientProvider):
    # Most operations here are called fairly infrequently, or intentionally slower than HTTP Cache
    # use_cache = True to check the cache, but store_cache = False
    # to not store the response in memory for mostly useless data.
    # We are are using ETags wherever possible and injecting Last-Modified from Models too.

    def __init__(self) -> None:
        super().__init__(
            __esi_compatibility_date__,
            __title_useragent__,
            __version__,
            __url__,
            operations=OPEN_API_OPERATIONS
        )

    def get_alliance_corps(
            self, alliance_id: int,
            use_etag: bool = True,
            force_refresh: bool = False,
            use_cache: bool = True,
            store_cache: bool = False,
            last_modified: datetime | None = None) -> "AlliancesAllianceIdCorporationsGet":
        """Fetch alliance from ESI."""
        return self.client.Alliance.GetAlliancesAllianceIdCorporations(
            alliance_id=alliance_id,
        ).result(
            force_refresh=force_refresh,
            use_cache=use_cache,
            store_cache=store_cache,
            use_etag=use_etag,
            last_modified=last_modified
        )

    def get_alliance(
            self, alliance_id: "AllianceID",
            use_etag: bool = True,
            force_refresh: bool = False,
            use_cache: bool = True,
            store_cache: bool = False,
            last_modified: datetime | None = None) -> tuple["AllianceDetail", Response]:
        """Fetch alliance from ESI."""
        return self.client.Alliance.GetAlliancesAllianceId(
            alliance_id=alliance_id,
        ).result(
            return_response=True,
            force_refresh=force_refresh,
            use_cache=use_cache,
            store_cache=store_cache,
            use_etag=use_etag,
            last_modified=last_modified
        )

    def get_corporation(
            self, corporation_id: "CorporationID",
            use_etag: bool = True,
            force_refresh: bool = False,
            use_cache: bool = True,
            store_cache: bool = False,
            last_modified: datetime | None = None) -> tuple["CorporationsDetail", Response]:
        """Fetch corporation from ESI."""
        return self.client.Corporation.GetCorporationsCorporationId(
            corporation_id=corporation_id,
        ).result(
            return_response=True,
            force_refresh=force_refresh,
            use_cache=use_cache,
            store_cache=store_cache,
            use_etag=use_etag,
            last_modified=last_modified
        )

    def get_character(
            self, character_id: "CharacterID",
            use_etag: bool = True,
            force_refresh: bool = False,
            use_cache: bool = True,
            store_cache: bool = False,
            last_modified: datetime | None = None) -> tuple["CharactersDetail", Response]:
        """Fetch character from ESI."""
        return self.client.Character.GetCharactersCharacterId(
            character_id=character_id,
        ).result(
            return_response=True,
            force_refresh=force_refresh,
            use_cache=use_cache,
            store_cache=store_cache,
            use_etag=use_etag,
            last_modified=last_modified
        )

    def get_all_factions(
            self,
            use_etag: bool = False,  # used by get_faction, trust cache, here be dragons, etags are safe outside this module if you account for it.
            force_refresh: bool = False,
            use_cache: bool = True,
            store_cache: bool = True,
            last_modified: datetime | None = None) -> tuple["UniverseFactionsGet", Response]:
        """Fetch all factions from ESI."""
        return self.client.Universe.GetUniverseFactions().result(
            return_response=True,
            force_refresh=force_refresh,
            use_cache=use_cache,
            store_cache=store_cache,
            use_etag=use_etag,
            last_modified=last_modified
        )

    def get_faction(
            self,faction_id: "FactionID",
            use_etag: bool = False,  # In most cases if we want a specific faction we need the response.
            force_refresh: bool = False,
            use_cache: bool = True,
            store_cache: bool = True,
            last_modified: datetime | None = None) -> tuple["UniverseFactionsGetItem", Response]:
        """Fetch faction from ESI."""
        factions, response = self.get_all_factions(
            last_modified=last_modified,
            force_refresh=force_refresh,
            use_cache=use_cache,
            store_cache=store_cache,
            use_etag=use_etag)

        for f in factions:
            if f.faction_id == int(faction_id):
                return f, response
        return None, response

    def get_affiliations(
            self, character_ids: list[int],
            use_etag: bool = True,
            force_refresh: bool = False,
            use_cache: bool = True,
            store_cache: bool = False,
            last_modified: datetime | None = None) -> tuple[list[dict[str, int]], Response]:
        return self.client.Character.PostCharactersAffiliation(
            body=character_ids
        ).result(
            return_response=True,
            force_refresh=force_refresh,
            use_cache=use_cache,
            store_cache=store_cache,
            use_etag=use_etag,
            last_modified=last_modified
        )

    def post_names(
            self, ids: list[int],
            use_etag: bool = False,
            force_refresh: bool = False,
            use_cache: bool = True,
            store_cache: bool = False,
            last_modified: datetime | None = None) -> list[dict]:
        return self.client.Universe.PostUniverseNames(
            body=ids
        ).result(
            force_refresh=force_refresh,
            use_cache=use_cache,
            store_cache=store_cache,
            use_etag=use_etag,
            last_modified=last_modified
        )


open_api_provider = EveOpenAPIProvider()
