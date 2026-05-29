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
    # most operations used here have `use_cache = False` this is cause we don't
    # want to use the space in ram for mostly useless data. We are using etags tho.

    def __init__(self) -> None:
        super().__init__(
            __esi_compatibility_date__,
            __title_useragent__,
            __version__,
            __url__,
            operations=OPEN_API_OPERATIONS
        )

    def get_alliance_corps(self, alliance_id: int, force_refresh=False, use_etag: bool = True) -> "AlliancesAllianceIdCorporationsGet":
        """Fetch alliance from ESI."""
        return self.client.Alliance.GetAlliancesAllianceIdCorporations(
            alliance_id=alliance_id,
        ).result(
            force_refresh=force_refresh,
            use_cache=False,
            use_etag=use_etag
        )

    def get_alliance(self, alliance_id: "AllianceID", last_modified: datetime | None = None, force_refresh=False, use_etag: bool = True) -> tuple["AllianceDetail", Response]:
        """Fetch alliance from ESI."""
        return self.client.Alliance.GetAlliancesAllianceId(
            alliance_id=alliance_id,
        ).result(
            return_response=True,
            force_refresh=force_refresh,
            use_cache=False,
            use_etag=use_etag,
            last_modified=last_modified
        )

    def get_corporation(self, corporation_id: "CorporationID", last_modified: datetime | None = None, force_refresh=False, use_etag: bool = True) -> tuple["CorporationsDetail", Response]:
        """Fetch corporation from ESI."""
        return self.client.Corporation.GetCorporationsCorporationId(
            corporation_id=corporation_id,
        ).result(
            return_response=True,
            force_refresh=force_refresh,
            use_cache=False,
            use_etag=use_etag,
            last_modified=last_modified
        )

    def get_character(self, character_id: "CharacterID", last_modified: datetime | None = None, force_refresh=False, use_etag: bool = True) -> tuple["CharactersDetail", Response]:
        """Fetch character from ESI."""
        return self.client.Character.GetCharactersCharacterId(
            character_id=character_id,
        ).result(
            return_response=True,
            force_refresh=force_refresh,
            use_cache=False,
            use_etag=use_etag,
            last_modified=last_modified
        )

    def get_all_factions(self, last_modified: datetime | None = None, force_refresh: bool = False, use_cache: bool = True, use_etag: bool = False) -> tuple["UniverseFactionsGet", Response]:
        """Fetch all factions from ESI."""
        return self.client.Universe.GetUniverseFactions().result(
            return_response=True,
            force_refresh=force_refresh,
            use_cache=use_cache,
            use_etag=use_etag,
            last_modified=last_modified
        )

    def get_faction(self, faction_id: "FactionID", last_modified: datetime | None = None, force_refresh: bool = False, use_cache: bool = True, use_etag: bool = False) -> tuple["UniverseFactionsGetItem", Response]:
        """Fetch faction from ESI."""
        factions, response = self.get_all_factions(last_modified=last_modified, force_refresh=force_refresh, use_cache=use_cache, use_etag=use_etag)
        for f in factions:
            if f.faction_id == int(faction_id):
                return f, response
        return None, response

    def get_affiliations(self, character_ids: list[int], force_refresh=False, use_etag: bool = True) -> list[dict]:
        return self.client.Character.PostCharactersAffiliation(
            body=character_ids
        ).result(
            force_refresh=force_refresh,
            use_cache=False,
            use_etag=use_etag
        )

    def post_names(self, ids: list[int], force_refresh=False, use_etag: bool = True) -> list[dict]:
        return self.client.Universe.PostUniverseNames(
            body=ids
        ).result(
            force_refresh=force_refresh,
            use_cache=False,
            use_etag=use_etag
        )


open_api_provider = EveOpenAPIProvider()
