# flake8: noqa=E501
# cSpell: disable
# Auto Generated do not edit
from datetime import date, datetime
from enum import Enum
from httpx import Response
from typing import Annotated, Any, Literal, overload
from uuid import UUID

from pydantic import BaseModel, Field

from esi.models import Token
from esi.openapi_clients import EsiOperation


class GetCharactersAccessListsDetailOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersAccessListsDetail:
        """Get the details of an Access List."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersAccessListsDetail, Response]:
        """Get the details of an Access List."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersAccessListsDetail | tuple[CharactersAccessListsDetail, Response]:
        """Get the details of an Access List."""
        ...

class GetCharactersAccessListsListingOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersAccessListsListing:
        """Lists all Access Lists the character is Manager or Admin of."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersAccessListsListing, Response]:
        """Lists all Access Lists the character is Manager or Admin of."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersAccessListsListing | tuple[CharactersAccessListsListing, Response]:
        """Lists all Access Lists the character is Manager or Admin of."""
        ...

class GetCharactersMercenaryTacticalOperationsDetailOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersMercenaryTacticalOperationsDetail:
        """Get the details of a Mercenary Tactical Operation."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersMercenaryTacticalOperationsDetail, Response]:
        """Get the details of a Mercenary Tactical Operation."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersMercenaryTacticalOperationsDetail | tuple[CharactersMercenaryTacticalOperationsDetail, Response]:
        """Get the details of a Mercenary Tactical Operation."""
        ...

class GetCharactersMercenaryTacticalOperationsListingOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersMercenaryTacticalOperationsListing:
        """Listing of all Mercenary Tactical Operations for the character."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersMercenaryTacticalOperationsListing, Response]:
        """Listing of all Mercenary Tactical Operations for the character."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersMercenaryTacticalOperationsListing | tuple[CharactersMercenaryTacticalOperationsListing, Response]:
        """Listing of all Mercenary Tactical Operations for the character."""
        ...

class GetSkyhooksRaidableOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> SkyhooksRaidable:
        """Listing of all Skyhooks that currently or will shortly be raidable."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[SkyhooksRaidable, Response]:
        """Listing of all Skyhooks that currently or will shortly be raidable."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> SkyhooksRaidable | tuple[SkyhooksRaidable, Response]:
        """Listing of all Skyhooks that currently or will shortly be raidable."""
        ...

class GetAlliancesOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> AlliancesGet:
        """List all active player alliances"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[AlliancesGet, Response]:
        """List all active player alliances"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> AlliancesGet | tuple[AlliancesGet, Response]:
        """List all active player alliances"""
        ...

class GetAlliancesAllianceIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> AllianceDetail:
        """Public information about an alliance"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[AllianceDetail, Response]:
        """Public information about an alliance"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> AllianceDetail | tuple[AllianceDetail, Response]:
        """Public information about an alliance"""
        ...

class GetAlliancesAllianceIdCorporationsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> AlliancesAllianceIdCorporationsGet:
        """List all current member corporations of an alliance"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[AlliancesAllianceIdCorporationsGet, Response]:
        """List all current member corporations of an alliance"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> AlliancesAllianceIdCorporationsGet | tuple[AlliancesAllianceIdCorporationsGet, Response]:
        """List all current member corporations of an alliance"""
        ...

class GetAlliancesAllianceIdIconsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> AlliancesAllianceIdIconsGet:
        """Get the icon urls for a alliance  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[AlliancesAllianceIdIconsGet, Response]:
        """Get the icon urls for a alliance  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> AlliancesAllianceIdIconsGet | tuple[AlliancesAllianceIdIconsGet, Response]:
        """Get the icon urls for a alliance  This route expires daily at 11:05"""
        ...

class GetCharactersCharacterIdAssetsOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdAssetsGet:
        """Return a list of the characters assets"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdAssetsGet, Response]:
        """Return a list of the characters assets"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdAssetsGet | tuple[CharactersCharacterIdAssetsGet, Response]:
        """Return a list of the characters assets"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CharactersCharacterIdAssetsGetItem]:
        """Return a list of the characters assets"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CharactersCharacterIdAssetsGetItem], Response]:
        """Return a list of the characters assets"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CharactersCharacterIdAssetsGetItem] | tuple[list[CharactersCharacterIdAssetsGetItem], Response]:
        """Return a list of the characters assets"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CharactersCharacterIdAssetsGetItem]]:
        """Return a list of the characters assets"""
        ...


class GetCorporationsCorporationIdAssetsOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdAssetsGet:
        """Return a list of the corporation assets"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdAssetsGet, Response]:
        """Return a list of the corporation assets"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdAssetsGet | tuple[CorporationsCorporationIdAssetsGet, Response]:
        """Return a list of the corporation assets"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdAssetsGetItem]:
        """Return a list of the corporation assets"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationsCorporationIdAssetsGetItem], Response]:
        """Return a list of the corporation assets"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdAssetsGetItem] | tuple[list[CorporationsCorporationIdAssetsGetItem], Response]:
        """Return a list of the corporation assets"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationsCorporationIdAssetsGetItem]]:
        """Return a list of the corporation assets"""
        ...


class PostCharactersCharacterIdAssetsLocationsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any:
        """Return locations for a set of item ids, which you can get from character assets endpoint. Coordinates for items in hangars or stations are set to (0,0,0)"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[Any, Response]:
        """Return locations for a set of item ids, which you can get from character assets endpoint. Coordinates for items in hangars or stations are set to (0,0,0)"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any | tuple[Any, Response]:
        """Return locations for a set of item ids, which you can get from character assets endpoint. Coordinates for items in hangars or stations are set to (0,0,0)"""
        ...

class PostCharactersCharacterIdAssetsNamesOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any:
        """Return names for a set of item ids, which you can get from character assets endpoint. Typically used for items that can customize names, like containers or ships."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[Any, Response]:
        """Return names for a set of item ids, which you can get from character assets endpoint. Typically used for items that can customize names, like containers or ships."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any | tuple[Any, Response]:
        """Return names for a set of item ids, which you can get from character assets endpoint. Typically used for items that can customize names, like containers or ships."""
        ...

class PostCorporationsCorporationIdAssetsLocationsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any:
        """Return locations for a set of item ids, which you can get from corporation assets endpoint. Coordinates for items in hangars or stations are set to (0,0,0)"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[Any, Response]:
        """Return locations for a set of item ids, which you can get from corporation assets endpoint. Coordinates for items in hangars or stations are set to (0,0,0)"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any | tuple[Any, Response]:
        """Return locations for a set of item ids, which you can get from corporation assets endpoint. Coordinates for items in hangars or stations are set to (0,0,0)"""
        ...

class PostCorporationsCorporationIdAssetsNamesOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any:
        """Return names for a set of item ids, which you can get from corporation assets endpoint. Only valid for items that can customize names, like containers or ships"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[Any, Response]:
        """Return names for a set of item ids, which you can get from corporation assets endpoint. Only valid for items that can customize names, like containers or ships"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any | tuple[Any, Response]:
        """Return names for a set of item ids, which you can get from corporation assets endpoint. Only valid for items that can customize names, like containers or ships"""
        ...

class GetCharactersCharacterIdCalendarOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdCalendarGet:
        """Get 50 event summaries from the calendar. If no from_event ID is given, the resource will return the next 50 chronological event summaries from now. If a from_event ID is specified, it will return the next 50 chronological event summaries from after that event"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdCalendarGet, Response]:
        """Get 50 event summaries from the calendar. If no from_event ID is given, the resource will return the next 50 chronological event summaries from now. If a from_event ID is specified, it will return the next 50 chronological event summaries from after that event"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdCalendarGet | tuple[CharactersCharacterIdCalendarGet, Response]:
        """Get 50 event summaries from the calendar. If no from_event ID is given, the resource will return the next 50 chronological event summaries from now. If a from_event ID is specified, it will return the next 50 chronological event summaries from after that event"""
        ...

class GetCharactersCharacterIdCalendarEventIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdCalendarEventIdGet:
        """Get all the information for a specific event"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdCalendarEventIdGet, Response]:
        """Get all the information for a specific event"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdCalendarEventIdGet | tuple[CharactersCharacterIdCalendarEventIdGet, Response]:
        """Get all the information for a specific event"""
        ...

class GetCharactersCharacterIdCalendarEventIdAttendeesOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdCalendarEventIdAttendeesGet:
        """Get all invited attendees for a given event"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdCalendarEventIdAttendeesGet, Response]:
        """Get all invited attendees for a given event"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdCalendarEventIdAttendeesGet | tuple[CharactersCharacterIdCalendarEventIdAttendeesGet, Response]:
        """Get all invited attendees for a given event"""
        ...

class PutCharactersCharacterIdCalendarEventIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None:
        """Set your response status to an event"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[None, Response]:
        """Set your response status to an event"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None | tuple[None, Response]:
        """Set your response status to an event"""
        ...

class GetCharactersCharacterIdAgentsResearchOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdAgentsResearchGet:
        """Return a list of agents research information for a character. The formula for finding the current research points with an agent is: currentPoints = remainderPoints + pointsPerDay * days(currentTime - researchStartDate)"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdAgentsResearchGet, Response]:
        """Return a list of agents research information for a character. The formula for finding the current research points with an agent is: currentPoints = remainderPoints + pointsPerDay * days(currentTime - researchStartDate)"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdAgentsResearchGet | tuple[CharactersCharacterIdAgentsResearchGet, Response]:
        """Return a list of agents research information for a character. The formula for finding the current research points with an agent is: currentPoints = remainderPoints + pointsPerDay * days(currentTime - researchStartDate)"""
        ...

class GetCharactersCharacterIdBlueprintsOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdBlueprintsGet:
        """Return a list of blueprints the character owns"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdBlueprintsGet, Response]:
        """Return a list of blueprints the character owns"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdBlueprintsGet | tuple[CharactersCharacterIdBlueprintsGet, Response]:
        """Return a list of blueprints the character owns"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CharactersCharacterIdBlueprintsGetItem]:
        """Return a list of blueprints the character owns"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CharactersCharacterIdBlueprintsGetItem], Response]:
        """Return a list of blueprints the character owns"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CharactersCharacterIdBlueprintsGetItem] | tuple[list[CharactersCharacterIdBlueprintsGetItem], Response]:
        """Return a list of blueprints the character owns"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CharactersCharacterIdBlueprintsGetItem]]:
        """Return a list of blueprints the character owns"""
        ...


class GetCharactersCharacterIdCorporationhistoryOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdCorporationhistoryGet:
        """Get a list of all the corporations a character has been a member of"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdCorporationhistoryGet, Response]:
        """Get a list of all the corporations a character has been a member of"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdCorporationhistoryGet | tuple[CharactersCharacterIdCorporationhistoryGet, Response]:
        """Get a list of all the corporations a character has been a member of"""
        ...

class GetCharactersCharacterIdFatigueOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdFatigueGet:
        """Return a character's jump activation and fatigue information"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdFatigueGet, Response]:
        """Return a character's jump activation and fatigue information"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdFatigueGet | tuple[CharactersCharacterIdFatigueGet, Response]:
        """Return a character's jump activation and fatigue information"""
        ...

class GetCharactersCharacterIdMedalsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdMedalsGet:
        """Return a list of medals the character has"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdMedalsGet, Response]:
        """Return a list of medals the character has"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdMedalsGet | tuple[CharactersCharacterIdMedalsGet, Response]:
        """Return a list of medals the character has"""
        ...

class GetCharactersCharacterIdNotificationsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdNotificationsGet:
        """Return character notifications"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdNotificationsGet, Response]:
        """Return character notifications"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdNotificationsGet | tuple[CharactersCharacterIdNotificationsGet, Response]:
        """Return character notifications"""
        ...

class GetCharactersCharacterIdNotificationsContactsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdNotificationsContactsGet:
        """Return notifications about having been added to someone's contact list"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdNotificationsContactsGet, Response]:
        """Return notifications about having been added to someone's contact list"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdNotificationsContactsGet | tuple[CharactersCharacterIdNotificationsContactsGet, Response]:
        """Return notifications about having been added to someone's contact list"""
        ...

class GetCharactersCharacterIdPortraitOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdPortraitGet:
        """Get portrait urls for a character  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdPortraitGet, Response]:
        """Get portrait urls for a character  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdPortraitGet | tuple[CharactersCharacterIdPortraitGet, Response]:
        """Get portrait urls for a character  This route expires daily at 11:05"""
        ...

class GetCharactersCharacterIdRolesOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdRolesGet:
        """Returns a character's corporation roles"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdRolesGet, Response]:
        """Returns a character's corporation roles"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdRolesGet | tuple[CharactersCharacterIdRolesGet, Response]:
        """Returns a character's corporation roles"""
        ...

class GetCharactersCharacterIdStandingsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdStandingsGet:
        """Return character standings from agents, NPC corporations, and factions"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdStandingsGet, Response]:
        """Return character standings from agents, NPC corporations, and factions"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdStandingsGet | tuple[CharactersCharacterIdStandingsGet, Response]:
        """Return character standings from agents, NPC corporations, and factions"""
        ...

class GetCharactersCharacterIdTitlesOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdTitlesGet:
        """Returns a character's titles"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdTitlesGet, Response]:
        """Returns a character's titles"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdTitlesGet | tuple[CharactersCharacterIdTitlesGet, Response]:
        """Returns a character's titles"""
        ...

class GetCharactersDetailOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersDetail:
        """Public information about a character"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersDetail, Response]:
        """Public information about a character"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersDetail | tuple[CharactersDetail, Response]:
        """Public information about a character"""
        ...

class PostCharactersAffiliationOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any:
        """Bulk lookup of character IDs to corporation, alliance and faction"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[Any, Response]:
        """Bulk lookup of character IDs to corporation, alliance and faction"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any | tuple[Any, Response]:
        """Bulk lookup of character IDs to corporation, alliance and faction"""
        ...

class PostCharactersCharacterIdCspaOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdCspaPost:
        """Takes a source character ID in the url and a set of target character ID's in the body, returns a CSPA charge cost"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdCspaPost, Response]:
        """Takes a source character ID in the url and a set of target character ID's in the body, returns a CSPA charge cost"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdCspaPost | tuple[CharactersCharacterIdCspaPost, Response]:
        """Takes a source character ID in the url and a set of target character ID's in the body, returns a CSPA charge cost"""
        ...

class GetCharactersCharacterIdClonesOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdClonesGet:
        """A list of the character's clones"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdClonesGet, Response]:
        """A list of the character's clones"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdClonesGet | tuple[CharactersCharacterIdClonesGet, Response]:
        """A list of the character's clones"""
        ...

class GetCharactersCharacterIdImplantsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdImplantsGet:
        """Return implants on the active clone of a character"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdImplantsGet, Response]:
        """Return implants on the active clone of a character"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdImplantsGet | tuple[CharactersCharacterIdImplantsGet, Response]:
        """Return implants on the active clone of a character"""
        ...

class DeleteCharactersCharacterIdContactsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None:
        """Bulk delete contacts"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[None, Response]:
        """Bulk delete contacts"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None | tuple[None, Response]:
        """Bulk delete contacts"""
        ...

class GetAlliancesAllianceIdContactsOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> AlliancesAllianceIdContactsGet:
        """Return contacts of an alliance"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[AlliancesAllianceIdContactsGet, Response]:
        """Return contacts of an alliance"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> AlliancesAllianceIdContactsGet | tuple[AlliancesAllianceIdContactsGet, Response]:
        """Return contacts of an alliance"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[AlliancesAllianceIdContactsGetItem]:
        """Return contacts of an alliance"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[AlliancesAllianceIdContactsGetItem], Response]:
        """Return contacts of an alliance"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[AlliancesAllianceIdContactsGetItem] | tuple[list[AlliancesAllianceIdContactsGetItem], Response]:
        """Return contacts of an alliance"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[AlliancesAllianceIdContactsGetItem]]:
        """Return contacts of an alliance"""
        ...


class GetAlliancesAllianceIdContactsLabelsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> AlliancesAllianceIdContactsLabelsGet:
        """Return custom labels for an alliance's contacts"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[AlliancesAllianceIdContactsLabelsGet, Response]:
        """Return custom labels for an alliance's contacts"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> AlliancesAllianceIdContactsLabelsGet | tuple[AlliancesAllianceIdContactsLabelsGet, Response]:
        """Return custom labels for an alliance's contacts"""
        ...

class GetCharactersCharacterIdContactsOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdContactsGet:
        """Return contacts of a character"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdContactsGet, Response]:
        """Return contacts of a character"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdContactsGet | tuple[CharactersCharacterIdContactsGet, Response]:
        """Return contacts of a character"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CharactersCharacterIdContactsGetItem]:
        """Return contacts of a character"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CharactersCharacterIdContactsGetItem], Response]:
        """Return contacts of a character"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CharactersCharacterIdContactsGetItem] | tuple[list[CharactersCharacterIdContactsGetItem], Response]:
        """Return contacts of a character"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CharactersCharacterIdContactsGetItem]]:
        """Return contacts of a character"""
        ...


class GetCharactersCharacterIdContactsLabelsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdContactsLabelsGet:
        """Return custom labels for a character's contacts"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdContactsLabelsGet, Response]:
        """Return custom labels for a character's contacts"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdContactsLabelsGet | tuple[CharactersCharacterIdContactsLabelsGet, Response]:
        """Return custom labels for a character's contacts"""
        ...

class GetCorporationsCorporationIdContactsOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdContactsGet:
        """Return contacts of a corporation"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdContactsGet, Response]:
        """Return contacts of a corporation"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdContactsGet | tuple[CorporationsCorporationIdContactsGet, Response]:
        """Return contacts of a corporation"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdContactsGetItem]:
        """Return contacts of a corporation"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationsCorporationIdContactsGetItem], Response]:
        """Return contacts of a corporation"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdContactsGetItem] | tuple[list[CorporationsCorporationIdContactsGetItem], Response]:
        """Return contacts of a corporation"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationsCorporationIdContactsGetItem]]:
        """Return contacts of a corporation"""
        ...


class GetCorporationsCorporationIdContactsLabelsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdContactsLabelsGet:
        """Return custom labels for a corporation's contacts"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdContactsLabelsGet, Response]:
        """Return custom labels for a corporation's contacts"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdContactsLabelsGet | tuple[CorporationsCorporationIdContactsLabelsGet, Response]:
        """Return custom labels for a corporation's contacts"""
        ...

class PostCharactersCharacterIdContactsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdContactsPost:
        """Bulk add contacts with same settings"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdContactsPost, Response]:
        """Bulk add contacts with same settings"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdContactsPost | tuple[CharactersCharacterIdContactsPost, Response]:
        """Bulk add contacts with same settings"""
        ...

class PutCharactersCharacterIdContactsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None:
        """Bulk edit contacts with same settings"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[None, Response]:
        """Bulk edit contacts with same settings"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None | tuple[None, Response]:
        """Bulk edit contacts with same settings"""
        ...

class GetCharactersCharacterIdContractsOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdContractsGet:
        """Returns contracts available to a character, only if the character is issuer, acceptor or assignee. Only returns contracts no older than 30 days, or if the status is "in_progress"."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdContractsGet, Response]:
        """Returns contracts available to a character, only if the character is issuer, acceptor or assignee. Only returns contracts no older than 30 days, or if the status is "in_progress"."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdContractsGet | tuple[CharactersCharacterIdContractsGet, Response]:
        """Returns contracts available to a character, only if the character is issuer, acceptor or assignee. Only returns contracts no older than 30 days, or if the status is "in_progress"."""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CharactersCharacterIdContractsGetItem]:
        """Returns contracts available to a character, only if the character is issuer, acceptor or assignee. Only returns contracts no older than 30 days, or if the status is "in_progress"."""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CharactersCharacterIdContractsGetItem], Response]:
        """Returns contracts available to a character, only if the character is issuer, acceptor or assignee. Only returns contracts no older than 30 days, or if the status is "in_progress"."""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CharactersCharacterIdContractsGetItem] | tuple[list[CharactersCharacterIdContractsGetItem], Response]:
        """Returns contracts available to a character, only if the character is issuer, acceptor or assignee. Only returns contracts no older than 30 days, or if the status is "in_progress"."""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CharactersCharacterIdContractsGetItem]]:
        """Returns contracts available to a character, only if the character is issuer, acceptor or assignee. Only returns contracts no older than 30 days, or if the status is "in_progress"."""
        ...


class GetCharactersCharacterIdContractsContractIdBidsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdContractsContractIdBidsGet:
        """Lists bids on a particular auction contract"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdContractsContractIdBidsGet, Response]:
        """Lists bids on a particular auction contract"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdContractsContractIdBidsGet | tuple[CharactersCharacterIdContractsContractIdBidsGet, Response]:
        """Lists bids on a particular auction contract"""
        ...

class GetCharactersCharacterIdContractsContractIdItemsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdContractsContractIdItemsGet:
        """Lists items of a particular contract"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdContractsContractIdItemsGet, Response]:
        """Lists items of a particular contract"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdContractsContractIdItemsGet | tuple[CharactersCharacterIdContractsContractIdItemsGet, Response]:
        """Lists items of a particular contract"""
        ...

class GetContractsPublicBidsContractIdOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> ContractsPublicBidsContractIdGet:
        """Lists bids on a public auction contract"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[ContractsPublicBidsContractIdGet, Response]:
        """Lists bids on a public auction contract"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> ContractsPublicBidsContractIdGet | tuple[ContractsPublicBidsContractIdGet, Response]:
        """Lists bids on a public auction contract"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[ContractsPublicBidsContractIdGetItem]:
        """Lists bids on a public auction contract"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[ContractsPublicBidsContractIdGetItem], Response]:
        """Lists bids on a public auction contract"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[ContractsPublicBidsContractIdGetItem] | tuple[list[ContractsPublicBidsContractIdGetItem], Response]:
        """Lists bids on a public auction contract"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[ContractsPublicBidsContractIdGetItem]]:
        """Lists bids on a public auction contract"""
        ...


class GetContractsPublicItemsContractIdOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> ContractsPublicItemsContractIdGet:
        """Lists items of a public contract"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[ContractsPublicItemsContractIdGet, Response]:
        """Lists items of a public contract"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> ContractsPublicItemsContractIdGet | tuple[ContractsPublicItemsContractIdGet, Response]:
        """Lists items of a public contract"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[ContractsPublicItemsContractIdGetItem]:
        """Lists items of a public contract"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[ContractsPublicItemsContractIdGetItem], Response]:
        """Lists items of a public contract"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[ContractsPublicItemsContractIdGetItem] | tuple[list[ContractsPublicItemsContractIdGetItem], Response]:
        """Lists items of a public contract"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[ContractsPublicItemsContractIdGetItem]]:
        """Lists items of a public contract"""
        ...


class GetContractsPublicRegionIdOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> ContractsPublicRegionIdGet:
        """Returns a paginated list of all public contracts in the given region"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[ContractsPublicRegionIdGet, Response]:
        """Returns a paginated list of all public contracts in the given region"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> ContractsPublicRegionIdGet | tuple[ContractsPublicRegionIdGet, Response]:
        """Returns a paginated list of all public contracts in the given region"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[ContractsPublicRegionIdGetItem]:
        """Returns a paginated list of all public contracts in the given region"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[ContractsPublicRegionIdGetItem], Response]:
        """Returns a paginated list of all public contracts in the given region"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[ContractsPublicRegionIdGetItem] | tuple[list[ContractsPublicRegionIdGetItem], Response]:
        """Returns a paginated list of all public contracts in the given region"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[ContractsPublicRegionIdGetItem]]:
        """Returns a paginated list of all public contracts in the given region"""
        ...


class GetCorporationsCorporationIdContractsOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdContractsGet:
        """Returns contracts available to a corporation, only if the corporation is issuer, acceptor or assignee. Only returns contracts no older than 30 days, or if the status is "in_progress"."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdContractsGet, Response]:
        """Returns contracts available to a corporation, only if the corporation is issuer, acceptor or assignee. Only returns contracts no older than 30 days, or if the status is "in_progress"."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdContractsGet | tuple[CorporationsCorporationIdContractsGet, Response]:
        """Returns contracts available to a corporation, only if the corporation is issuer, acceptor or assignee. Only returns contracts no older than 30 days, or if the status is "in_progress"."""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdContractsGetItem]:
        """Returns contracts available to a corporation, only if the corporation is issuer, acceptor or assignee. Only returns contracts no older than 30 days, or if the status is "in_progress"."""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationsCorporationIdContractsGetItem], Response]:
        """Returns contracts available to a corporation, only if the corporation is issuer, acceptor or assignee. Only returns contracts no older than 30 days, or if the status is "in_progress"."""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdContractsGetItem] | tuple[list[CorporationsCorporationIdContractsGetItem], Response]:
        """Returns contracts available to a corporation, only if the corporation is issuer, acceptor or assignee. Only returns contracts no older than 30 days, or if the status is "in_progress"."""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationsCorporationIdContractsGetItem]]:
        """Returns contracts available to a corporation, only if the corporation is issuer, acceptor or assignee. Only returns contracts no older than 30 days, or if the status is "in_progress"."""
        ...


class GetCorporationsCorporationIdContractsContractIdBidsOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdContractsContractIdBidsGet:
        """Lists bids on a particular auction contract"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdContractsContractIdBidsGet, Response]:
        """Lists bids on a particular auction contract"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdContractsContractIdBidsGet | tuple[CorporationsCorporationIdContractsContractIdBidsGet, Response]:
        """Lists bids on a particular auction contract"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdContractsContractIdBidsGetItem]:
        """Lists bids on a particular auction contract"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationsCorporationIdContractsContractIdBidsGetItem], Response]:
        """Lists bids on a particular auction contract"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdContractsContractIdBidsGetItem] | tuple[list[CorporationsCorporationIdContractsContractIdBidsGetItem], Response]:
        """Lists bids on a particular auction contract"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationsCorporationIdContractsContractIdBidsGetItem]]:
        """Lists bids on a particular auction contract"""
        ...


class GetCorporationsCorporationIdContractsContractIdItemsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdContractsContractIdItemsGet:
        """Lists items of a particular contract"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdContractsContractIdItemsGet, Response]:
        """Lists items of a particular contract"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdContractsContractIdItemsGet | tuple[CorporationsCorporationIdContractsContractIdItemsGet, Response]:
        """Lists items of a particular contract"""
        ...

class GetCorporationsCorporationIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsDetail:
        """Public information about a corporation"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsDetail, Response]:
        """Public information about a corporation"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsDetail | tuple[CorporationsDetail, Response]:
        """Public information about a corporation"""
        ...

class GetCorporationsCorporationIdAlliancehistoryOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdAlliancehistoryGet:
        """Get a list of all the alliances a corporation has been a member of"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdAlliancehistoryGet, Response]:
        """Get a list of all the alliances a corporation has been a member of"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdAlliancehistoryGet | tuple[CorporationsCorporationIdAlliancehistoryGet, Response]:
        """Get a list of all the alliances a corporation has been a member of"""
        ...

class GetCorporationsCorporationIdBlueprintsOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdBlueprintsGet:
        """Returns a list of blueprints the corporation owns"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdBlueprintsGet, Response]:
        """Returns a list of blueprints the corporation owns"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdBlueprintsGet | tuple[CorporationsCorporationIdBlueprintsGet, Response]:
        """Returns a list of blueprints the corporation owns"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdBlueprintsGetItem]:
        """Returns a list of blueprints the corporation owns"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationsCorporationIdBlueprintsGetItem], Response]:
        """Returns a list of blueprints the corporation owns"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdBlueprintsGetItem] | tuple[list[CorporationsCorporationIdBlueprintsGetItem], Response]:
        """Returns a list of blueprints the corporation owns"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationsCorporationIdBlueprintsGetItem]]:
        """Returns a list of blueprints the corporation owns"""
        ...


class GetCorporationsCorporationIdContainersLogsOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdContainersLogsGet:
        """Returns logs recorded in the past seven days from all audit log secure containers (ALSC) owned by a given corporation"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdContainersLogsGet, Response]:
        """Returns logs recorded in the past seven days from all audit log secure containers (ALSC) owned by a given corporation"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdContainersLogsGet | tuple[CorporationsCorporationIdContainersLogsGet, Response]:
        """Returns logs recorded in the past seven days from all audit log secure containers (ALSC) owned by a given corporation"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdContainersLogsGetItem]:
        """Returns logs recorded in the past seven days from all audit log secure containers (ALSC) owned by a given corporation"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationsCorporationIdContainersLogsGetItem], Response]:
        """Returns logs recorded in the past seven days from all audit log secure containers (ALSC) owned by a given corporation"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdContainersLogsGetItem] | tuple[list[CorporationsCorporationIdContainersLogsGetItem], Response]:
        """Returns logs recorded in the past seven days from all audit log secure containers (ALSC) owned by a given corporation"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationsCorporationIdContainersLogsGetItem]]:
        """Returns logs recorded in the past seven days from all audit log secure containers (ALSC) owned by a given corporation"""
        ...


class GetCorporationsCorporationIdDivisionsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdDivisionsGet:
        """Return corporation hangar and wallet division names, only show if a division is not using the default name"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdDivisionsGet, Response]:
        """Return corporation hangar and wallet division names, only show if a division is not using the default name"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdDivisionsGet | tuple[CorporationsCorporationIdDivisionsGet, Response]:
        """Return corporation hangar and wallet division names, only show if a division is not using the default name"""
        ...

class GetCorporationsCorporationIdFacilitiesOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdFacilitiesGet:
        """Return a corporation's facilities"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdFacilitiesGet, Response]:
        """Return a corporation's facilities"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdFacilitiesGet | tuple[CorporationsCorporationIdFacilitiesGet, Response]:
        """Return a corporation's facilities"""
        ...

class GetCorporationsCorporationIdIconsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdIconsGet:
        """Get the icon urls for a corporation"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdIconsGet, Response]:
        """Get the icon urls for a corporation"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdIconsGet | tuple[CorporationsCorporationIdIconsGet, Response]:
        """Get the icon urls for a corporation"""
        ...

class GetCorporationsCorporationIdMedalsOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdMedalsGet:
        """Returns a corporation's medals"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdMedalsGet, Response]:
        """Returns a corporation's medals"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdMedalsGet | tuple[CorporationsCorporationIdMedalsGet, Response]:
        """Returns a corporation's medals"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdMedalsGetItem]:
        """Returns a corporation's medals"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationsCorporationIdMedalsGetItem], Response]:
        """Returns a corporation's medals"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdMedalsGetItem] | tuple[list[CorporationsCorporationIdMedalsGetItem], Response]:
        """Returns a corporation's medals"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationsCorporationIdMedalsGetItem]]:
        """Returns a corporation's medals"""
        ...


class GetCorporationsCorporationIdMedalsIssuedOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdMedalsIssuedGet:
        """Returns medals issued by a corporation"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdMedalsIssuedGet, Response]:
        """Returns medals issued by a corporation"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdMedalsIssuedGet | tuple[CorporationsCorporationIdMedalsIssuedGet, Response]:
        """Returns medals issued by a corporation"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdMedalsIssuedGetItem]:
        """Returns medals issued by a corporation"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationsCorporationIdMedalsIssuedGetItem], Response]:
        """Returns medals issued by a corporation"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdMedalsIssuedGetItem] | tuple[list[CorporationsCorporationIdMedalsIssuedGetItem], Response]:
        """Returns medals issued by a corporation"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationsCorporationIdMedalsIssuedGetItem]]:
        """Returns medals issued by a corporation"""
        ...


class GetCorporationsCorporationIdMembersOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdMembersGet:
        """Return the current member list of a corporation, the token's character need to be a member of the corporation."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdMembersGet, Response]:
        """Return the current member list of a corporation, the token's character need to be a member of the corporation."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdMembersGet | tuple[CorporationsCorporationIdMembersGet, Response]:
        """Return the current member list of a corporation, the token's character need to be a member of the corporation."""
        ...

class GetCorporationsCorporationIdMembersLimitOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdMembersLimitGet:
        """Return a corporation's member limit, not including CEO himself"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdMembersLimitGet, Response]:
        """Return a corporation's member limit, not including CEO himself"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdMembersLimitGet | tuple[CorporationsCorporationIdMembersLimitGet, Response]:
        """Return a corporation's member limit, not including CEO himself"""
        ...

class GetCorporationsCorporationIdMembersTitlesOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdMembersTitlesGet:
        """Returns a corporation's members' titles"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdMembersTitlesGet, Response]:
        """Returns a corporation's members' titles"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdMembersTitlesGet | tuple[CorporationsCorporationIdMembersTitlesGet, Response]:
        """Returns a corporation's members' titles"""
        ...

class GetCorporationsCorporationIdMembertrackingOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdMembertrackingGet:
        """Returns additional information about a corporation's members which helps tracking their activities"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdMembertrackingGet, Response]:
        """Returns additional information about a corporation's members which helps tracking their activities"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdMembertrackingGet | tuple[CorporationsCorporationIdMembertrackingGet, Response]:
        """Returns additional information about a corporation's members which helps tracking their activities"""
        ...

class GetCorporationsCorporationIdRolesOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdRolesGet:
        """Return the roles of all members if the character has the personnel manager role or any grantable role."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdRolesGet, Response]:
        """Return the roles of all members if the character has the personnel manager role or any grantable role."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdRolesGet | tuple[CorporationsCorporationIdRolesGet, Response]:
        """Return the roles of all members if the character has the personnel manager role or any grantable role."""
        ...

class GetCorporationsCorporationIdRolesHistoryOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdRolesHistoryGet:
        """Return how roles have changed for a coporation's members, up to a month"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdRolesHistoryGet, Response]:
        """Return how roles have changed for a coporation's members, up to a month"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdRolesHistoryGet | tuple[CorporationsCorporationIdRolesHistoryGet, Response]:
        """Return how roles have changed for a coporation's members, up to a month"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdRolesHistoryGetItem]:
        """Return how roles have changed for a coporation's members, up to a month"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationsCorporationIdRolesHistoryGetItem], Response]:
        """Return how roles have changed for a coporation's members, up to a month"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdRolesHistoryGetItem] | tuple[list[CorporationsCorporationIdRolesHistoryGetItem], Response]:
        """Return how roles have changed for a coporation's members, up to a month"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationsCorporationIdRolesHistoryGetItem]]:
        """Return how roles have changed for a coporation's members, up to a month"""
        ...


class GetCorporationsCorporationIdShareholdersOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdShareholdersGet:
        """Return the current shareholders of a corporation."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdShareholdersGet, Response]:
        """Return the current shareholders of a corporation."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdShareholdersGet | tuple[CorporationsCorporationIdShareholdersGet, Response]:
        """Return the current shareholders of a corporation."""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdShareholdersGetItem]:
        """Return the current shareholders of a corporation."""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationsCorporationIdShareholdersGetItem], Response]:
        """Return the current shareholders of a corporation."""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdShareholdersGetItem] | tuple[list[CorporationsCorporationIdShareholdersGetItem], Response]:
        """Return the current shareholders of a corporation."""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationsCorporationIdShareholdersGetItem]]:
        """Return the current shareholders of a corporation."""
        ...


class GetCorporationsCorporationIdStandingsOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdStandingsGet:
        """Return corporation standings from agents, NPC corporations, and factions"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdStandingsGet, Response]:
        """Return corporation standings from agents, NPC corporations, and factions"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdStandingsGet | tuple[CorporationsCorporationIdStandingsGet, Response]:
        """Return corporation standings from agents, NPC corporations, and factions"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdStandingsGetItem]:
        """Return corporation standings from agents, NPC corporations, and factions"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationsCorporationIdStandingsGetItem], Response]:
        """Return corporation standings from agents, NPC corporations, and factions"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdStandingsGetItem] | tuple[list[CorporationsCorporationIdStandingsGetItem], Response]:
        """Return corporation standings from agents, NPC corporations, and factions"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationsCorporationIdStandingsGetItem]]:
        """Return corporation standings from agents, NPC corporations, and factions"""
        ...


class GetCorporationsCorporationIdStarbasesOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdStarbasesGet:
        """Returns list of corporation starbases (POSes)"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdStarbasesGet, Response]:
        """Returns list of corporation starbases (POSes)"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdStarbasesGet | tuple[CorporationsCorporationIdStarbasesGet, Response]:
        """Returns list of corporation starbases (POSes)"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdStarbasesGetItem]:
        """Returns list of corporation starbases (POSes)"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationsCorporationIdStarbasesGetItem], Response]:
        """Returns list of corporation starbases (POSes)"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdStarbasesGetItem] | tuple[list[CorporationsCorporationIdStarbasesGetItem], Response]:
        """Returns list of corporation starbases (POSes)"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationsCorporationIdStarbasesGetItem]]:
        """Returns list of corporation starbases (POSes)"""
        ...


class GetCorporationsCorporationIdStarbasesStarbaseIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdStarbasesStarbaseIdGet:
        """Returns various settings and fuels of a starbase (POS)"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdStarbasesStarbaseIdGet, Response]:
        """Returns various settings and fuels of a starbase (POS)"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdStarbasesStarbaseIdGet | tuple[CorporationsCorporationIdStarbasesStarbaseIdGet, Response]:
        """Returns various settings and fuels of a starbase (POS)"""
        ...

class GetCorporationsCorporationIdStructuresOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdStructuresGet:
        """Get a list of corporation structures. This route's version includes the changes to structures detailed in this blog: https://www.eveonline.com/article/upwell-2.0-structures-changes-coming-on-february-13th"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdStructuresGet, Response]:
        """Get a list of corporation structures. This route's version includes the changes to structures detailed in this blog: https://www.eveonline.com/article/upwell-2.0-structures-changes-coming-on-february-13th"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdStructuresGet | tuple[CorporationsCorporationIdStructuresGet, Response]:
        """Get a list of corporation structures. This route's version includes the changes to structures detailed in this blog: https://www.eveonline.com/article/upwell-2.0-structures-changes-coming-on-february-13th"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdStructuresGetItem]:
        """Get a list of corporation structures. This route's version includes the changes to structures detailed in this blog: https://www.eveonline.com/article/upwell-2.0-structures-changes-coming-on-february-13th"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationsCorporationIdStructuresGetItem], Response]:
        """Get a list of corporation structures. This route's version includes the changes to structures detailed in this blog: https://www.eveonline.com/article/upwell-2.0-structures-changes-coming-on-february-13th"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdStructuresGetItem] | tuple[list[CorporationsCorporationIdStructuresGetItem], Response]:
        """Get a list of corporation structures. This route's version includes the changes to structures detailed in this blog: https://www.eveonline.com/article/upwell-2.0-structures-changes-coming-on-february-13th"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationsCorporationIdStructuresGetItem]]:
        """Get a list of corporation structures. This route's version includes the changes to structures detailed in this blog: https://www.eveonline.com/article/upwell-2.0-structures-changes-coming-on-february-13th"""
        ...


class GetCorporationsCorporationIdTitlesOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdTitlesGet:
        """Returns a corporation's titles"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdTitlesGet, Response]:
        """Returns a corporation's titles"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdTitlesGet | tuple[CorporationsCorporationIdTitlesGet, Response]:
        """Returns a corporation's titles"""
        ...

class GetCorporationsNpccorpsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsNpccorpsGet:
        """Get a list of npc corporations  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsNpccorpsGet, Response]:
        """Get a list of npc corporations  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsNpccorpsGet | tuple[CorporationsNpccorpsGet, Response]:
        """Get a list of npc corporations  This route expires daily at 11:05"""
        ...

class GetCorporationsProjectsContributionOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsProjectsContribution:
        """Show your contribution to a corporation project."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsProjectsContribution, Response]:
        """Show your contribution to a corporation project."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsProjectsContribution | tuple[CorporationsProjectsContribution, Response]:
        """Show your contribution to a corporation project."""
        ...

class GetCorporationsProjectsContributorsOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsProjectsContributors:
        """Listing of all contributors to a corporation project."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsProjectsContributors, Response]:
        """Listing of all contributors to a corporation project."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsProjectsContributors | tuple[CorporationsProjectsContributors, Response]:
        """Listing of all contributors to a corporation project."""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsProjectsContributors]:
        """Listing of all contributors to a corporation project."""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationsProjectsContributors], Response]:
        """Listing of all contributors to a corporation project."""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsProjectsContributors] | tuple[list[CorporationsProjectsContributors], Response]:
        """Listing of all contributors to a corporation project."""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationsProjectsContributors]]:
        """Listing of all contributors to a corporation project."""
        ...


class GetCorporationsProjectsDetailOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsProjectsDetail:
        """Get the details of a corporation project."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsProjectsDetail, Response]:
        """Get the details of a corporation project."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsProjectsDetail | tuple[CorporationsProjectsDetail, Response]:
        """Get the details of a corporation project."""
        ...

class GetCorporationsProjectsListingOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsProjectsListing:
        """Listing of all (active) corporation projects."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsProjectsListing, Response]:
        """Listing of all (active) corporation projects."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsProjectsListing | tuple[CorporationsProjectsListing, Response]:
        """Listing of all (active) corporation projects."""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsProjectsListing]:
        """Listing of all (active) corporation projects."""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationsProjectsListing], Response]:
        """Listing of all (active) corporation projects."""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsProjectsListing] | tuple[list[CorporationsProjectsListing], Response]:
        """Listing of all (active) corporation projects."""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationsProjectsListing]]:
        """Listing of all (active) corporation projects."""
        ...


class GetDogmaAttributesOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> DogmaAttributesGet:
        """Get a list of dogma attribute ids  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[DogmaAttributesGet, Response]:
        """Get a list of dogma attribute ids  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> DogmaAttributesGet | tuple[DogmaAttributesGet, Response]:
        """Get a list of dogma attribute ids  This route expires daily at 11:05"""
        ...

class GetDogmaAttributesAttributeIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> DogmaAttributesAttributeIdGet:
        """Get information on a dogma attribute  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[DogmaAttributesAttributeIdGet, Response]:
        """Get information on a dogma attribute  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> DogmaAttributesAttributeIdGet | tuple[DogmaAttributesAttributeIdGet, Response]:
        """Get information on a dogma attribute  This route expires daily at 11:05"""
        ...

class GetDogmaDynamicItemsTypeIdItemIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> DogmaDynamicItemsTypeIdItemIdGet:
        """Returns info about a dynamic item resulting from mutation with a mutaplasmid.  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[DogmaDynamicItemsTypeIdItemIdGet, Response]:
        """Returns info about a dynamic item resulting from mutation with a mutaplasmid.  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> DogmaDynamicItemsTypeIdItemIdGet | tuple[DogmaDynamicItemsTypeIdItemIdGet, Response]:
        """Returns info about a dynamic item resulting from mutation with a mutaplasmid.  This route expires daily at 11:05"""
        ...

class GetDogmaEffectsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> DogmaEffectsGet:
        """Get a list of dogma effect ids  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[DogmaEffectsGet, Response]:
        """Get a list of dogma effect ids  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> DogmaEffectsGet | tuple[DogmaEffectsGet, Response]:
        """Get a list of dogma effect ids  This route expires daily at 11:05"""
        ...

class GetDogmaEffectsEffectIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> DogmaEffectsEffectIdGet:
        """Get information on a dogma effect  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[DogmaEffectsEffectIdGet, Response]:
        """Get information on a dogma effect  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> DogmaEffectsEffectIdGet | tuple[DogmaEffectsEffectIdGet, Response]:
        """Get information on a dogma effect  This route expires daily at 11:05"""
        ...

class GetCharactersCharacterIdFwStatsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdFwStatsGet:
        """Statistical overview of a character involved in faction warfare  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdFwStatsGet, Response]:
        """Statistical overview of a character involved in faction warfare  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdFwStatsGet | tuple[CharactersCharacterIdFwStatsGet, Response]:
        """Statistical overview of a character involved in faction warfare  This route expires daily at 11:05"""
        ...

class GetCorporationsCorporationIdFwStatsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdFwStatsGet:
        """Statistics about a corporation involved in faction warfare  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdFwStatsGet, Response]:
        """Statistics about a corporation involved in faction warfare  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdFwStatsGet | tuple[CorporationsCorporationIdFwStatsGet, Response]:
        """Statistics about a corporation involved in faction warfare  This route expires daily at 11:05"""
        ...

class GetFwLeaderboardsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FwLeaderboardsGet:
        """Top 4 leaderboard of factions for kills and victory points separated by total, last week and yesterday  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[FwLeaderboardsGet, Response]:
        """Top 4 leaderboard of factions for kills and victory points separated by total, last week and yesterday  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FwLeaderboardsGet | tuple[FwLeaderboardsGet, Response]:
        """Top 4 leaderboard of factions for kills and victory points separated by total, last week and yesterday  This route expires daily at 11:05"""
        ...

class GetFwLeaderboardsCharactersOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FwLeaderboardsCharactersGet:
        """Top 100 leaderboard of pilots for kills and victory points separated by total, last week and yesterday  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[FwLeaderboardsCharactersGet, Response]:
        """Top 100 leaderboard of pilots for kills and victory points separated by total, last week and yesterday  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FwLeaderboardsCharactersGet | tuple[FwLeaderboardsCharactersGet, Response]:
        """Top 100 leaderboard of pilots for kills and victory points separated by total, last week and yesterday  This route expires daily at 11:05"""
        ...

class GetFwLeaderboardsCorporationsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FwLeaderboardsCorporationsGet:
        """Top 10 leaderboard of corporations for kills and victory points separated by total, last week and yesterday  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[FwLeaderboardsCorporationsGet, Response]:
        """Top 10 leaderboard of corporations for kills and victory points separated by total, last week and yesterday  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FwLeaderboardsCorporationsGet | tuple[FwLeaderboardsCorporationsGet, Response]:
        """Top 10 leaderboard of corporations for kills and victory points separated by total, last week and yesterday  This route expires daily at 11:05"""
        ...

class GetFwStatsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FwStatsGet:
        """Statistical overviews of factions involved in faction warfare  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[FwStatsGet, Response]:
        """Statistical overviews of factions involved in faction warfare  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FwStatsGet | tuple[FwStatsGet, Response]:
        """Statistical overviews of factions involved in faction warfare  This route expires daily at 11:05"""
        ...

class GetFwSystemsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FwSystemsGet:
        """An overview of the current ownership of faction warfare solar systems"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[FwSystemsGet, Response]:
        """An overview of the current ownership of faction warfare solar systems"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FwSystemsGet | tuple[FwSystemsGet, Response]:
        """An overview of the current ownership of faction warfare solar systems"""
        ...

class GetFwWarsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FwWarsGet:
        """Data about which NPC factions are at war  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[FwWarsGet, Response]:
        """Data about which NPC factions are at war  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FwWarsGet | tuple[FwWarsGet, Response]:
        """Data about which NPC factions are at war  This route expires daily at 11:05"""
        ...

class DeleteCharactersCharacterIdFittingsFittingIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None:
        """Delete a fitting from a character"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[None, Response]:
        """Delete a fitting from a character"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None | tuple[None, Response]:
        """Delete a fitting from a character"""
        ...

class GetCharactersCharacterIdFittingsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdFittingsGet:
        """Return fittings of a character"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdFittingsGet, Response]:
        """Return fittings of a character"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdFittingsGet | tuple[CharactersCharacterIdFittingsGet, Response]:
        """Return fittings of a character"""
        ...

class PostCharactersCharacterIdFittingsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdFittingsPost:
        """Save a new fitting for a character"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdFittingsPost, Response]:
        """Save a new fitting for a character"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdFittingsPost | tuple[CharactersCharacterIdFittingsPost, Response]:
        """Save a new fitting for a character"""
        ...

class DeleteFleetsFleetIdMembersMemberIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None:
        """Kick a fleet member"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[None, Response]:
        """Kick a fleet member"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None | tuple[None, Response]:
        """Kick a fleet member"""
        ...

class DeleteFleetsFleetIdSquadsSquadIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None:
        """Delete a fleet squad, only empty squads can be deleted"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[None, Response]:
        """Delete a fleet squad, only empty squads can be deleted"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None | tuple[None, Response]:
        """Delete a fleet squad, only empty squads can be deleted"""
        ...

class DeleteFleetsFleetIdWingsWingIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None:
        """Delete a fleet wing, only empty wings can be deleted. The wing may contain squads, but the squads must be empty"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[None, Response]:
        """Delete a fleet wing, only empty wings can be deleted. The wing may contain squads, but the squads must be empty"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None | tuple[None, Response]:
        """Delete a fleet wing, only empty wings can be deleted. The wing may contain squads, but the squads must be empty"""
        ...

class GetCharactersCharacterIdFleetOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdFleetGet:
        """Return the fleet ID the character is in, if any."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdFleetGet, Response]:
        """Return the fleet ID the character is in, if any."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdFleetGet | tuple[CharactersCharacterIdFleetGet, Response]:
        """Return the fleet ID the character is in, if any."""
        ...

class GetFleetsFleetIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FleetsFleetIdGet:
        """Return details about a fleet"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[FleetsFleetIdGet, Response]:
        """Return details about a fleet"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FleetsFleetIdGet | tuple[FleetsFleetIdGet, Response]:
        """Return details about a fleet"""
        ...

class GetFleetsFleetIdMembersOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FleetsFleetIdMembersGet:
        """Return information about fleet members"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[FleetsFleetIdMembersGet, Response]:
        """Return information about fleet members"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FleetsFleetIdMembersGet | tuple[FleetsFleetIdMembersGet, Response]:
        """Return information about fleet members"""
        ...

class GetFleetsFleetIdWingsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FleetsFleetIdWingsGet:
        """Return information about wings in a fleet"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[FleetsFleetIdWingsGet, Response]:
        """Return information about wings in a fleet"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FleetsFleetIdWingsGet | tuple[FleetsFleetIdWingsGet, Response]:
        """Return information about wings in a fleet"""
        ...

class PostFleetsFleetIdMembersOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any:
        """Invite a character into the fleet. If a character has a CSPA charge set it is not possible to invite them to the fleet using ESI"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[Any, Response]:
        """Invite a character into the fleet. If a character has a CSPA charge set it is not possible to invite them to the fleet using ESI"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any | tuple[Any, Response]:
        """Invite a character into the fleet. If a character has a CSPA charge set it is not possible to invite them to the fleet using ESI"""
        ...

class PostFleetsFleetIdWingsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FleetsFleetIdWingsPost:
        """Create a new wing in a fleet"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[FleetsFleetIdWingsPost, Response]:
        """Create a new wing in a fleet"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FleetsFleetIdWingsPost | tuple[FleetsFleetIdWingsPost, Response]:
        """Create a new wing in a fleet"""
        ...

class PostFleetsFleetIdWingsWingIdSquadsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FleetsFleetIdWingsWingIdSquadsPost:
        """Create a new squad in a fleet"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[FleetsFleetIdWingsWingIdSquadsPost, Response]:
        """Create a new squad in a fleet"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FleetsFleetIdWingsWingIdSquadsPost | tuple[FleetsFleetIdWingsWingIdSquadsPost, Response]:
        """Create a new squad in a fleet"""
        ...

class PutFleetsFleetIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None:
        """Update settings about a fleet"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[None, Response]:
        """Update settings about a fleet"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None | tuple[None, Response]:
        """Update settings about a fleet"""
        ...

class PutFleetsFleetIdMembersMemberIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None:
        """Move a fleet member around"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[None, Response]:
        """Move a fleet member around"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None | tuple[None, Response]:
        """Move a fleet member around"""
        ...

class PutFleetsFleetIdSquadsSquadIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None:
        """Rename a fleet squad"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[None, Response]:
        """Rename a fleet squad"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None | tuple[None, Response]:
        """Rename a fleet squad"""
        ...

class PutFleetsFleetIdWingsWingIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None:
        """Rename a fleet wing"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[None, Response]:
        """Rename a fleet wing"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None | tuple[None, Response]:
        """Rename a fleet wing"""
        ...

class GetCharactersFreelanceJobsListingOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersFreelanceJobsListing:
        """Listing of all freelance jobs you are actively participating in."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersFreelanceJobsListing, Response]:
        """Listing of all freelance jobs you are actively participating in."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersFreelanceJobsListing | tuple[CharactersFreelanceJobsListing, Response]:
        """Listing of all freelance jobs you are actively participating in."""
        ...

class GetCharactersFreelanceJobsParticipationOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersFreelanceJobsParticipation:
        """Show your participation in a freelance job."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersFreelanceJobsParticipation, Response]:
        """Show your participation in a freelance job."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersFreelanceJobsParticipation | tuple[CharactersFreelanceJobsParticipation, Response]:
        """Show your participation in a freelance job."""
        ...

class GetCorporationsFreelanceJobsListingOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsFreelanceJobsListing:
        """Listing of all freelance jobs for your corporation."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsFreelanceJobsListing, Response]:
        """Listing of all freelance jobs for your corporation."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsFreelanceJobsListing | tuple[CorporationsFreelanceJobsListing, Response]:
        """Listing of all freelance jobs for your corporation."""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsFreelanceJobsListing]:
        """Listing of all freelance jobs for your corporation."""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationsFreelanceJobsListing], Response]:
        """Listing of all freelance jobs for your corporation."""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsFreelanceJobsListing] | tuple[list[CorporationsFreelanceJobsListing], Response]:
        """Listing of all freelance jobs for your corporation."""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationsFreelanceJobsListing]]:
        """Listing of all freelance jobs for your corporation."""
        ...


class GetCorporationsFreelanceJobsParticipantsOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsFreelanceJobsParticipants:
        """Listing of all participants of a freelance job."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsFreelanceJobsParticipants, Response]:
        """Listing of all participants of a freelance job."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsFreelanceJobsParticipants | tuple[CorporationsFreelanceJobsParticipants, Response]:
        """Listing of all participants of a freelance job."""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsFreelanceJobsParticipants]:
        """Listing of all participants of a freelance job."""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationsFreelanceJobsParticipants], Response]:
        """Listing of all participants of a freelance job."""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsFreelanceJobsParticipants] | tuple[list[CorporationsFreelanceJobsParticipants], Response]:
        """Listing of all participants of a freelance job."""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationsFreelanceJobsParticipants]]:
        """Listing of all participants of a freelance job."""
        ...


class GetFreelanceJobsDetailOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FreelanceJobsDetail:
        """Get the details of a freelance job.  Jobs without an ACL (public jobs) does not require authentication.  Jobs with an ACL requires authentication, and requires that the character is: - An active participant of the job, or - A freelance job manager for the corporation that owns the job."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[FreelanceJobsDetail, Response]:
        """Get the details of a freelance job.  Jobs without an ACL (public jobs) does not require authentication.  Jobs with an ACL requires authentication, and requires that the character is: - An active participant of the job, or - A freelance job manager for the corporation that owns the job."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FreelanceJobsDetail | tuple[FreelanceJobsDetail, Response]:
        """Get the details of a freelance job.  Jobs without an ACL (public jobs) does not require authentication.  Jobs with an ACL requires authentication, and requires that the character is: - An active participant of the job, or - A freelance job manager for the corporation that owns the job."""
        ...

class GetFreelanceJobsListingOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FreelanceJobsListing:
        """Listing of all public freelance jobs."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[FreelanceJobsListing, Response]:
        """Listing of all public freelance jobs."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> FreelanceJobsListing | tuple[FreelanceJobsListing, Response]:
        """Listing of all public freelance jobs."""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[FreelanceJobsListing]:
        """Listing of all public freelance jobs."""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[FreelanceJobsListing], Response]:
        """Listing of all public freelance jobs."""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[FreelanceJobsListing] | tuple[list[FreelanceJobsListing], Response]:
        """Listing of all public freelance jobs."""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[FreelanceJobsListing]]:
        """Listing of all public freelance jobs."""
        ...


class GetIncursionsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> IncursionsGet:
        """Return a list of current incursions"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[IncursionsGet, Response]:
        """Return a list of current incursions"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> IncursionsGet | tuple[IncursionsGet, Response]:
        """Return a list of current incursions"""
        ...

class GetCharactersCharacterIdIndustryJobsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdIndustryJobsGet:
        """List industry jobs placed by a character"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdIndustryJobsGet, Response]:
        """List industry jobs placed by a character"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdIndustryJobsGet | tuple[CharactersCharacterIdIndustryJobsGet, Response]:
        """List industry jobs placed by a character"""
        ...

class GetCharactersCharacterIdMiningOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdMiningGet:
        """Paginated record of all mining done by a character for the past 30 days"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdMiningGet, Response]:
        """Paginated record of all mining done by a character for the past 30 days"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdMiningGet | tuple[CharactersCharacterIdMiningGet, Response]:
        """Paginated record of all mining done by a character for the past 30 days"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CharactersCharacterIdMiningGetItem]:
        """Paginated record of all mining done by a character for the past 30 days"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CharactersCharacterIdMiningGetItem], Response]:
        """Paginated record of all mining done by a character for the past 30 days"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CharactersCharacterIdMiningGetItem] | tuple[list[CharactersCharacterIdMiningGetItem], Response]:
        """Paginated record of all mining done by a character for the past 30 days"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CharactersCharacterIdMiningGetItem]]:
        """Paginated record of all mining done by a character for the past 30 days"""
        ...


class GetCorporationCorporationIdMiningExtractionsOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationCorporationIdMiningExtractionsGet:
        """Extraction timers for all moon chunks being extracted by refineries belonging to a corporation."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationCorporationIdMiningExtractionsGet, Response]:
        """Extraction timers for all moon chunks being extracted by refineries belonging to a corporation."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationCorporationIdMiningExtractionsGet | tuple[CorporationCorporationIdMiningExtractionsGet, Response]:
        """Extraction timers for all moon chunks being extracted by refineries belonging to a corporation."""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationCorporationIdMiningExtractionsGetItem]:
        """Extraction timers for all moon chunks being extracted by refineries belonging to a corporation."""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationCorporationIdMiningExtractionsGetItem], Response]:
        """Extraction timers for all moon chunks being extracted by refineries belonging to a corporation."""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationCorporationIdMiningExtractionsGetItem] | tuple[list[CorporationCorporationIdMiningExtractionsGetItem], Response]:
        """Extraction timers for all moon chunks being extracted by refineries belonging to a corporation."""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationCorporationIdMiningExtractionsGetItem]]:
        """Extraction timers for all moon chunks being extracted by refineries belonging to a corporation."""
        ...


class GetCorporationCorporationIdMiningObserversOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationCorporationIdMiningObserversGet:
        """Paginated list of all entities capable of observing and recording mining for a corporation"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationCorporationIdMiningObserversGet, Response]:
        """Paginated list of all entities capable of observing and recording mining for a corporation"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationCorporationIdMiningObserversGet | tuple[CorporationCorporationIdMiningObserversGet, Response]:
        """Paginated list of all entities capable of observing and recording mining for a corporation"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationCorporationIdMiningObserversGetItem]:
        """Paginated list of all entities capable of observing and recording mining for a corporation"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationCorporationIdMiningObserversGetItem], Response]:
        """Paginated list of all entities capable of observing and recording mining for a corporation"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationCorporationIdMiningObserversGetItem] | tuple[list[CorporationCorporationIdMiningObserversGetItem], Response]:
        """Paginated list of all entities capable of observing and recording mining for a corporation"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationCorporationIdMiningObserversGetItem]]:
        """Paginated list of all entities capable of observing and recording mining for a corporation"""
        ...


class GetCorporationCorporationIdMiningObserversObserverIdOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationCorporationIdMiningObserversObserverIdGet:
        """Paginated record of all mining seen by an observer"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationCorporationIdMiningObserversObserverIdGet, Response]:
        """Paginated record of all mining seen by an observer"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationCorporationIdMiningObserversObserverIdGet | tuple[CorporationCorporationIdMiningObserversObserverIdGet, Response]:
        """Paginated record of all mining seen by an observer"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationCorporationIdMiningObserversObserverIdGetItem]:
        """Paginated record of all mining seen by an observer"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationCorporationIdMiningObserversObserverIdGetItem], Response]:
        """Paginated record of all mining seen by an observer"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationCorporationIdMiningObserversObserverIdGetItem] | tuple[list[CorporationCorporationIdMiningObserversObserverIdGetItem], Response]:
        """Paginated record of all mining seen by an observer"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationCorporationIdMiningObserversObserverIdGetItem]]:
        """Paginated record of all mining seen by an observer"""
        ...


class GetCorporationsCorporationIdIndustryJobsOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdIndustryJobsGet:
        """List industry jobs run by a corporation"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdIndustryJobsGet, Response]:
        """List industry jobs run by a corporation"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdIndustryJobsGet | tuple[CorporationsCorporationIdIndustryJobsGet, Response]:
        """List industry jobs run by a corporation"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdIndustryJobsGetItem]:
        """List industry jobs run by a corporation"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationsCorporationIdIndustryJobsGetItem], Response]:
        """List industry jobs run by a corporation"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdIndustryJobsGetItem] | tuple[list[CorporationsCorporationIdIndustryJobsGetItem], Response]:
        """List industry jobs run by a corporation"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationsCorporationIdIndustryJobsGetItem]]:
        """List industry jobs run by a corporation"""
        ...


class GetIndustryFacilitiesOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> IndustryFacilitiesGet:
        """Return a list of industry facilities"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[IndustryFacilitiesGet, Response]:
        """Return a list of industry facilities"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> IndustryFacilitiesGet | tuple[IndustryFacilitiesGet, Response]:
        """Return a list of industry facilities"""
        ...

class GetIndustrySystemsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> IndustrySystemsGet:
        """Return cost indices for solar systems"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[IndustrySystemsGet, Response]:
        """Return cost indices for solar systems"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> IndustrySystemsGet | tuple[IndustrySystemsGet, Response]:
        """Return cost indices for solar systems"""
        ...

class GetInsurancePricesOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> InsurancePricesGet:
        """Return available insurance levels for all ship types"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[InsurancePricesGet, Response]:
        """Return available insurance levels for all ship types"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> InsurancePricesGet | tuple[InsurancePricesGet, Response]:
        """Return available insurance levels for all ship types"""
        ...

class GetCharactersCharacterIdKillmailsRecentOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdKillmailsRecentGet:
        """Return a list of a character's kills and losses going back 90 days"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdKillmailsRecentGet, Response]:
        """Return a list of a character's kills and losses going back 90 days"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdKillmailsRecentGet | tuple[CharactersCharacterIdKillmailsRecentGet, Response]:
        """Return a list of a character's kills and losses going back 90 days"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CharactersCharacterIdKillmailsRecentGetItem]:
        """Return a list of a character's kills and losses going back 90 days"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CharactersCharacterIdKillmailsRecentGetItem], Response]:
        """Return a list of a character's kills and losses going back 90 days"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CharactersCharacterIdKillmailsRecentGetItem] | tuple[list[CharactersCharacterIdKillmailsRecentGetItem], Response]:
        """Return a list of a character's kills and losses going back 90 days"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CharactersCharacterIdKillmailsRecentGetItem]]:
        """Return a list of a character's kills and losses going back 90 days"""
        ...


class GetCorporationsCorporationIdKillmailsRecentOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdKillmailsRecentGet:
        """Get a list of a corporation's kills and losses going back 90 days"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdKillmailsRecentGet, Response]:
        """Get a list of a corporation's kills and losses going back 90 days"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdKillmailsRecentGet | tuple[CorporationsCorporationIdKillmailsRecentGet, Response]:
        """Get a list of a corporation's kills and losses going back 90 days"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdKillmailsRecentGetItem]:
        """Get a list of a corporation's kills and losses going back 90 days"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationsCorporationIdKillmailsRecentGetItem], Response]:
        """Get a list of a corporation's kills and losses going back 90 days"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdKillmailsRecentGetItem] | tuple[list[CorporationsCorporationIdKillmailsRecentGetItem], Response]:
        """Get a list of a corporation's kills and losses going back 90 days"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationsCorporationIdKillmailsRecentGetItem]]:
        """Get a list of a corporation's kills and losses going back 90 days"""
        ...


class GetKillmailsKillmailIdKillmailHashOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> KillmailsKillmailIdKillmailHashGet:
        """Return a single killmail from its ID and hash"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[KillmailsKillmailIdKillmailHashGet, Response]:
        """Return a single killmail from its ID and hash"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> KillmailsKillmailIdKillmailHashGet | tuple[KillmailsKillmailIdKillmailHashGet, Response]:
        """Return a single killmail from its ID and hash"""
        ...

class GetCharactersCharacterIdLocationOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdLocationGet:
        """Information about the characters current location. Returns the current solar system id, and also the current station or structure ID if applicable"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdLocationGet, Response]:
        """Information about the characters current location. Returns the current solar system id, and also the current station or structure ID if applicable"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdLocationGet | tuple[CharactersCharacterIdLocationGet, Response]:
        """Information about the characters current location. Returns the current solar system id, and also the current station or structure ID if applicable"""
        ...

class GetCharactersCharacterIdOnlineOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdOnlineGet:
        """Checks if the character is currently online"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdOnlineGet, Response]:
        """Checks if the character is currently online"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdOnlineGet | tuple[CharactersCharacterIdOnlineGet, Response]:
        """Checks if the character is currently online"""
        ...

class GetCharactersCharacterIdShipOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdShipGet:
        """Get the current ship type, name and id"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdShipGet, Response]:
        """Get the current ship type, name and id"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdShipGet | tuple[CharactersCharacterIdShipGet, Response]:
        """Get the current ship type, name and id"""
        ...

class GetCharactersCharacterIdLoyaltyPointsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdLoyaltyPointsGet:
        """Return a list of loyalty points for all corporations the character has worked for"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdLoyaltyPointsGet, Response]:
        """Return a list of loyalty points for all corporations the character has worked for"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdLoyaltyPointsGet | tuple[CharactersCharacterIdLoyaltyPointsGet, Response]:
        """Return a list of loyalty points for all corporations the character has worked for"""
        ...

class GetLoyaltyStoresCorporationIdOffersOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> LoyaltyStoresCorporationIdOffersGet:
        """Return a list of offers from a specific corporation's loyalty store  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[LoyaltyStoresCorporationIdOffersGet, Response]:
        """Return a list of offers from a specific corporation's loyalty store  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> LoyaltyStoresCorporationIdOffersGet | tuple[LoyaltyStoresCorporationIdOffersGet, Response]:
        """Return a list of offers from a specific corporation's loyalty store  This route expires daily at 11:05"""
        ...

class DeleteCharactersCharacterIdMailLabelsLabelIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None:
        """Delete a mail label"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[None, Response]:
        """Delete a mail label"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None | tuple[None, Response]:
        """Delete a mail label"""
        ...

class DeleteCharactersCharacterIdMailMailIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None:
        """Delete a mail"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[None, Response]:
        """Delete a mail"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None | tuple[None, Response]:
        """Delete a mail"""
        ...

class GetCharactersCharacterIdMailOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdMailGet:
        """Return the 50 most recent mail headers belonging to the character that match the query criteria. Queries can be filtered by label, and last_mail_id can be used to paginate backwards"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdMailGet, Response]:
        """Return the 50 most recent mail headers belonging to the character that match the query criteria. Queries can be filtered by label, and last_mail_id can be used to paginate backwards"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdMailGet | tuple[CharactersCharacterIdMailGet, Response]:
        """Return the 50 most recent mail headers belonging to the character that match the query criteria. Queries can be filtered by label, and last_mail_id can be used to paginate backwards"""
        ...

class GetCharactersCharacterIdMailLabelsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdMailLabelsGet:
        """Return a list of the users mail labels, unread counts for each label and a total unread count."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdMailLabelsGet, Response]:
        """Return a list of the users mail labels, unread counts for each label and a total unread count."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdMailLabelsGet | tuple[CharactersCharacterIdMailLabelsGet, Response]:
        """Return a list of the users mail labels, unread counts for each label and a total unread count."""
        ...

class GetCharactersCharacterIdMailListsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdMailListsGet:
        """Return all mailing lists that the character is subscribed to"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdMailListsGet, Response]:
        """Return all mailing lists that the character is subscribed to"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdMailListsGet | tuple[CharactersCharacterIdMailListsGet, Response]:
        """Return all mailing lists that the character is subscribed to"""
        ...

class GetCharactersCharacterIdMailMailIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdMailMailIdGet:
        """Return the contents of an EVE mail"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdMailMailIdGet, Response]:
        """Return the contents of an EVE mail"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdMailMailIdGet | tuple[CharactersCharacterIdMailMailIdGet, Response]:
        """Return the contents of an EVE mail"""
        ...

class PostCharactersCharacterIdMailOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdMailPost:
        """Create and send a new mail"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdMailPost, Response]:
        """Create and send a new mail"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdMailPost | tuple[CharactersCharacterIdMailPost, Response]:
        """Create and send a new mail"""
        ...

class PostCharactersCharacterIdMailLabelsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdMailLabelsPost:
        """Create a mail label"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdMailLabelsPost, Response]:
        """Create a mail label"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdMailLabelsPost | tuple[CharactersCharacterIdMailLabelsPost, Response]:
        """Create a mail label"""
        ...

class PutCharactersCharacterIdMailMailIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None:
        """Update metadata about a mail"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[None, Response]:
        """Update metadata about a mail"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> None | tuple[None, Response]:
        """Update metadata about a mail"""
        ...

class GetCharactersCharacterIdOrdersOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdOrdersGet:
        """List open market orders placed by a character"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdOrdersGet, Response]:
        """List open market orders placed by a character"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdOrdersGet | tuple[CharactersCharacterIdOrdersGet, Response]:
        """List open market orders placed by a character"""
        ...

class GetCharactersCharacterIdOrdersHistoryOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdOrdersHistoryGet:
        """List cancelled and expired market orders placed by a character up to 90 days in the past."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdOrdersHistoryGet, Response]:
        """List cancelled and expired market orders placed by a character up to 90 days in the past."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdOrdersHistoryGet | tuple[CharactersCharacterIdOrdersHistoryGet, Response]:
        """List cancelled and expired market orders placed by a character up to 90 days in the past."""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CharactersCharacterIdOrdersHistoryGetItem]:
        """List cancelled and expired market orders placed by a character up to 90 days in the past."""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CharactersCharacterIdOrdersHistoryGetItem], Response]:
        """List cancelled and expired market orders placed by a character up to 90 days in the past."""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CharactersCharacterIdOrdersHistoryGetItem] | tuple[list[CharactersCharacterIdOrdersHistoryGetItem], Response]:
        """List cancelled and expired market orders placed by a character up to 90 days in the past."""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CharactersCharacterIdOrdersHistoryGetItem]]:
        """List cancelled and expired market orders placed by a character up to 90 days in the past."""
        ...


class GetCorporationsCorporationIdOrdersOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdOrdersGet:
        """List open market orders placed on behalf of a corporation"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdOrdersGet, Response]:
        """List open market orders placed on behalf of a corporation"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdOrdersGet | tuple[CorporationsCorporationIdOrdersGet, Response]:
        """List open market orders placed on behalf of a corporation"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdOrdersGetItem]:
        """List open market orders placed on behalf of a corporation"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationsCorporationIdOrdersGetItem], Response]:
        """List open market orders placed on behalf of a corporation"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdOrdersGetItem] | tuple[list[CorporationsCorporationIdOrdersGetItem], Response]:
        """List open market orders placed on behalf of a corporation"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationsCorporationIdOrdersGetItem]]:
        """List open market orders placed on behalf of a corporation"""
        ...


class GetCorporationsCorporationIdOrdersHistoryOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdOrdersHistoryGet:
        """List cancelled and expired market orders placed on behalf of a corporation up to 90 days in the past."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdOrdersHistoryGet, Response]:
        """List cancelled and expired market orders placed on behalf of a corporation up to 90 days in the past."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdOrdersHistoryGet | tuple[CorporationsCorporationIdOrdersHistoryGet, Response]:
        """List cancelled and expired market orders placed on behalf of a corporation up to 90 days in the past."""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdOrdersHistoryGetItem]:
        """List cancelled and expired market orders placed on behalf of a corporation up to 90 days in the past."""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationsCorporationIdOrdersHistoryGetItem], Response]:
        """List cancelled and expired market orders placed on behalf of a corporation up to 90 days in the past."""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdOrdersHistoryGetItem] | tuple[list[CorporationsCorporationIdOrdersHistoryGetItem], Response]:
        """List cancelled and expired market orders placed on behalf of a corporation up to 90 days in the past."""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationsCorporationIdOrdersHistoryGetItem]]:
        """List cancelled and expired market orders placed on behalf of a corporation up to 90 days in the past."""
        ...


class GetMarketsGroupsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MarketsGroupsGet:
        """Get a list of item groups  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[MarketsGroupsGet, Response]:
        """Get a list of item groups  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MarketsGroupsGet | tuple[MarketsGroupsGet, Response]:
        """Get a list of item groups  This route expires daily at 11:05"""
        ...

class GetMarketsGroupsMarketGroupIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MarketsGroupsMarketGroupIdGet:
        """Get information on an item group  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[MarketsGroupsMarketGroupIdGet, Response]:
        """Get information on an item group  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MarketsGroupsMarketGroupIdGet | tuple[MarketsGroupsMarketGroupIdGet, Response]:
        """Get information on an item group  This route expires daily at 11:05"""
        ...

class GetMarketsPricesOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MarketsPricesGet:
        """Return a list of prices"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[MarketsPricesGet, Response]:
        """Return a list of prices"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MarketsPricesGet | tuple[MarketsPricesGet, Response]:
        """Return a list of prices"""
        ...

class GetMarketsRegionIdHistoryOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MarketsRegionIdHistoryGet:
        """Return a list of historical market statistics for the specified type in a region  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[MarketsRegionIdHistoryGet, Response]:
        """Return a list of historical market statistics for the specified type in a region  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MarketsRegionIdHistoryGet | tuple[MarketsRegionIdHistoryGet, Response]:
        """Return a list of historical market statistics for the specified type in a region  This route expires daily at 11:05"""
        ...

class GetMarketsRegionIdOrdersOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MarketsRegionIdOrdersGet:
        """Return a list of orders in a region"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[MarketsRegionIdOrdersGet, Response]:
        """Return a list of orders in a region"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MarketsRegionIdOrdersGet | tuple[MarketsRegionIdOrdersGet, Response]:
        """Return a list of orders in a region"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[MarketsRegionIdOrdersGetItem]:
        """Return a list of orders in a region"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[MarketsRegionIdOrdersGetItem], Response]:
        """Return a list of orders in a region"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[MarketsRegionIdOrdersGetItem] | tuple[list[MarketsRegionIdOrdersGetItem], Response]:
        """Return a list of orders in a region"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[MarketsRegionIdOrdersGetItem]]:
        """Return a list of orders in a region"""
        ...


class GetMarketsRegionIdTypesOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MarketsRegionIdTypesGet:
        """Return a list of type IDs that have active orders in the region, for efficient market indexing."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[MarketsRegionIdTypesGet, Response]:
        """Return a list of type IDs that have active orders in the region, for efficient market indexing."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MarketsRegionIdTypesGet | tuple[MarketsRegionIdTypesGet, Response]:
        """Return a list of type IDs that have active orders in the region, for efficient market indexing."""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[int]:
        """Return a list of type IDs that have active orders in the region, for efficient market indexing."""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[int], Response]:
        """Return a list of type IDs that have active orders in the region, for efficient market indexing."""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[int] | tuple[list[int], Response]:
        """Return a list of type IDs that have active orders in the region, for efficient market indexing."""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[int]]:
        """Return a list of type IDs that have active orders in the region, for efficient market indexing."""
        ...


class GetMarketsStructuresStructureIdOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MarketsStructuresStructureIdGet:
        """Return all orders in a structure"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[MarketsStructuresStructureIdGet, Response]:
        """Return all orders in a structure"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MarketsStructuresStructureIdGet | tuple[MarketsStructuresStructureIdGet, Response]:
        """Return all orders in a structure"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[MarketsStructuresStructureIdGetItem]:
        """Return all orders in a structure"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[MarketsStructuresStructureIdGetItem], Response]:
        """Return all orders in a structure"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[MarketsStructuresStructureIdGetItem] | tuple[list[MarketsStructuresStructureIdGetItem], Response]:
        """Return all orders in a structure"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[MarketsStructuresStructureIdGetItem]]:
        """Return all orders in a structure"""
        ...


class GetMetaChangelogOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MetaChangelog:
        """Get the changelog of this API."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[MetaChangelog, Response]:
        """Get the changelog of this API."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MetaChangelog | tuple[MetaChangelog, Response]:
        """Get the changelog of this API."""
        ...

class GetMetaCompatibilityDatesOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MetaCompatibilityDates:
        """Get a list of compatibility dates."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[MetaCompatibilityDates, Response]:
        """Get a list of compatibility dates."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MetaCompatibilityDates | tuple[MetaCompatibilityDates, Response]:
        """Get a list of compatibility dates."""
        ...

class GetMetaNameOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MetaName:
        """Get the name ESI is currently going by, plus the full and glorious history of every name it has ever had. The three letters have never once meant the same thing twice."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[MetaName, Response]:
        """Get the name ESI is currently going by, plus the full and glorious history of every name it has ever had. The three letters have never once meant the same thing twice."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MetaName | tuple[MetaName, Response]:
        """Get the name ESI is currently going by, plus the full and glorious history of every name it has ever had. The three letters have never once meant the same thing twice."""
        ...

class GetMetaStatusOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MetaStatus:
        """Get the health status of each API route."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[MetaStatus, Response]:
        """Get the health status of each API route."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MetaStatus | tuple[MetaStatus, Response]:
        """Get the health status of each API route."""
        ...

class GetCharactersMilitaryCampaignsObjectivesListingOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersMilitaryCampaignsObjectivesListing:
        """Listing of the military campaign objectives the character has participated in."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersMilitaryCampaignsObjectivesListing, Response]:
        """Listing of the military campaign objectives the character has participated in."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersMilitaryCampaignsObjectivesListing | tuple[CharactersMilitaryCampaignsObjectivesListing, Response]:
        """Listing of the military campaign objectives the character has participated in."""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CharactersMilitaryCampaignsObjectivesListing]:
        """Listing of the military campaign objectives the character has participated in."""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CharactersMilitaryCampaignsObjectivesListing], Response]:
        """Listing of the military campaign objectives the character has participated in."""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CharactersMilitaryCampaignsObjectivesListing] | tuple[list[CharactersMilitaryCampaignsObjectivesListing], Response]:
        """Listing of the military campaign objectives the character has participated in."""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CharactersMilitaryCampaignsObjectivesListing]]:
        """Listing of the military campaign objectives the character has participated in."""
        ...


class GetCharactersMilitaryCampaignsObjectivesParticipationOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersMilitaryCampaignsObjectivesParticipation:
        """Show your participation in a military campaign objective."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersMilitaryCampaignsObjectivesParticipation, Response]:
        """Show your participation in a military campaign objective."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersMilitaryCampaignsObjectivesParticipation | tuple[CharactersMilitaryCampaignsObjectivesParticipation, Response]:
        """Show your participation in a military campaign objective."""
        ...

class GetMilitaryCampaignsDetailOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MilitaryCampaignsDetail:
        """Get the details of a military campaign."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[MilitaryCampaignsDetail, Response]:
        """Get the details of a military campaign."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MilitaryCampaignsDetail | tuple[MilitaryCampaignsDetail, Response]:
        """Get the details of a military campaign."""
        ...

class GetMilitaryCampaignsListingOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MilitaryCampaignsListing:
        """Listing of all active military campaigns."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[MilitaryCampaignsListing, Response]:
        """Listing of all active military campaigns."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MilitaryCampaignsListing | tuple[MilitaryCampaignsListing, Response]:
        """Listing of all active military campaigns."""
        ...

class GetMilitaryCampaignsObjectivesDetailOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MilitaryCampaignsObjectivesDetail:
        """Get the details of an objective of a military campaign."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[MilitaryCampaignsObjectivesDetail, Response]:
        """Get the details of an objective of a military campaign."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MilitaryCampaignsObjectivesDetail | tuple[MilitaryCampaignsObjectivesDetail, Response]:
        """Get the details of an objective of a military campaign."""
        ...

class GetMilitaryCampaignsObjectivesListingOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MilitaryCampaignsObjectivesListing:
        """Listing of all active, completed or expired objectives of a military campaign."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[MilitaryCampaignsObjectivesListing, Response]:
        """Listing of all active, completed or expired objectives of a military campaign."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> MilitaryCampaignsObjectivesListing | tuple[MilitaryCampaignsObjectivesListing, Response]:
        """Listing of all active, completed or expired objectives of a military campaign."""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[MilitaryCampaignsObjectivesListing]:
        """Listing of all active, completed or expired objectives of a military campaign."""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[MilitaryCampaignsObjectivesListing], Response]:
        """Listing of all active, completed or expired objectives of a military campaign."""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[MilitaryCampaignsObjectivesListing] | tuple[list[MilitaryCampaignsObjectivesListing], Response]:
        """Listing of all active, completed or expired objectives of a military campaign."""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[MilitaryCampaignsObjectivesListing]]:
        """Listing of all active, completed or expired objectives of a military campaign."""
        ...


class GetCharactersCharacterIdPlanetsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdPlanetsGet:
        """Returns a list of all planetary colonies owned by a character."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdPlanetsGet, Response]:
        """Returns a list of all planetary colonies owned by a character."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdPlanetsGet | tuple[CharactersCharacterIdPlanetsGet, Response]:
        """Returns a list of all planetary colonies owned by a character."""
        ...

class GetCharactersCharacterIdPlanetsPlanetIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdPlanetsPlanetIdGet:
        """Returns full details on the layout of a single planetary colony, including links, pins and routes. Note: Planetary information is only recalculated when the colony is viewed through the client. Information will not update until this criteria is met."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdPlanetsPlanetIdGet, Response]:
        """Returns full details on the layout of a single planetary colony, including links, pins and routes. Note: Planetary information is only recalculated when the colony is viewed through the client. Information will not update until this criteria is met."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdPlanetsPlanetIdGet | tuple[CharactersCharacterIdPlanetsPlanetIdGet, Response]:
        """Returns full details on the layout of a single planetary colony, including links, pins and routes. Note: Planetary information is only recalculated when the colony is viewed through the client. Information will not update until this criteria is met."""
        ...

class GetCorporationsCorporationIdCustomsOfficesOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdCustomsOfficesGet:
        """List customs offices owned by a corporation"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdCustomsOfficesGet, Response]:
        """List customs offices owned by a corporation"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdCustomsOfficesGet | tuple[CorporationsCorporationIdCustomsOfficesGet, Response]:
        """List customs offices owned by a corporation"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdCustomsOfficesGetItem]:
        """List customs offices owned by a corporation"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationsCorporationIdCustomsOfficesGetItem], Response]:
        """List customs offices owned by a corporation"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdCustomsOfficesGetItem] | tuple[list[CorporationsCorporationIdCustomsOfficesGetItem], Response]:
        """List customs offices owned by a corporation"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationsCorporationIdCustomsOfficesGetItem]]:
        """List customs offices owned by a corporation"""
        ...


class GetUniverseSchematicsSchematicIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseSchematicsSchematicIdGet:
        """Get information on a planetary factory schematic"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseSchematicsSchematicIdGet, Response]:
        """Get information on a planetary factory schematic"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseSchematicsSchematicIdGet | tuple[UniverseSchematicsSchematicIdGet, Response]:
        """Get information on a planetary factory schematic"""
        ...

class PostRouteOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any:
        """Calculate the systems between the given origin and destination."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[Any, Response]:
        """Calculate the systems between the given origin and destination."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any | tuple[Any, Response]:
        """Calculate the systems between the given origin and destination."""
        ...

class GetCharactersCharacterIdSearchOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdSearchGet:
        """Search for entities that match a given sub-string."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdSearchGet, Response]:
        """Search for entities that match a given sub-string."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdSearchGet | tuple[CharactersCharacterIdSearchGet, Response]:
        """Search for entities that match a given sub-string."""
        ...

class GetCharactersCharacterIdAttributesOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdAttributesGet:
        """Return attributes of a character"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdAttributesGet, Response]:
        """Return attributes of a character"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdAttributesGet | tuple[CharactersCharacterIdAttributesGet, Response]:
        """Return attributes of a character"""
        ...

class GetCharactersCharacterIdSkillqueueOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CharactersSkillqueueSkill]:
        """List the configured skill queue for the given character.  Entries that have their finish time in the past are completed, but aren't updated in the "/skills" route yet. This will happen the next time the character logs in."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CharactersSkillqueueSkill], Response]:
        """List the configured skill queue for the given character.  Entries that have their finish time in the past are completed, but aren't updated in the "/skills" route yet. This will happen the next time the character logs in."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CharactersSkillqueueSkill] | tuple[list[CharactersSkillqueueSkill], Response]:
        """List the configured skill queue for the given character.  Entries that have their finish time in the past are completed, but aren't updated in the "/skills" route yet. This will happen the next time the character logs in."""
        ...

class GetCharactersCharacterIdSkillsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersSkills:
        """List all trained skills for the given character.  Skills returned by this route can be out-of-date if the character hasn't logged in since one or more skills completed training. Use the /skillqueue route to check for skills that completed training. Entries that are in the past need to be applied on top of this list to get an accurate view of the character's current skills."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersSkills, Response]:
        """List all trained skills for the given character.  Skills returned by this route can be out-of-date if the character hasn't logged in since one or more skills completed training. Use the /skillqueue route to check for skills that completed training. Entries that are in the past need to be applied on top of this list to get an accurate view of the character's current skills."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersSkills | tuple[CharactersSkills, Response]:
        """List all trained skills for the given character.  Skills returned by this route can be out-of-date if the character hasn't logged in since one or more skills completed training. Use the /skillqueue route to check for skills that completed training. Entries that are in the past need to be applied on top of this list to get an accurate view of the character's current skills."""
        ...

class GetSovereigntyCampaignsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> SovereigntyCampaignsGet:
        """Shows sovereignty data for campaigns."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[SovereigntyCampaignsGet, Response]:
        """Shows sovereignty data for campaigns."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> SovereigntyCampaignsGet | tuple[SovereigntyCampaignsGet, Response]:
        """Shows sovereignty data for campaigns."""
        ...

class GetSovereigntySystemsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> SovereigntySystems:
        """Listing of sovereignty details for all K-space systems in New Eden."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[SovereigntySystems, Response]:
        """Listing of sovereignty details for all K-space systems in New Eden."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> SovereigntySystems | tuple[SovereigntySystems, Response]:
        """Listing of sovereignty details for all K-space systems in New Eden."""
        ...

class GetStatusOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> StatusGet:
        """EVE Server status"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[StatusGet, Response]:
        """EVE Server status"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> StatusGet | tuple[StatusGet, Response]:
        """EVE Server status"""
        ...

class GetCharactersStructuresMercenaryDensDetailOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersStructuresMercenaryDensDetail:
        """Get the details of a Mercenary Den."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersStructuresMercenaryDensDetail, Response]:
        """Get the details of a Mercenary Den."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersStructuresMercenaryDensDetail | tuple[CharactersStructuresMercenaryDensDetail, Response]:
        """Get the details of a Mercenary Den."""
        ...

class GetCharactersStructuresMercenaryDensListingOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersStructuresMercenaryDensListing:
        """Listing of all Mercenary Dens."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersStructuresMercenaryDensListing, Response]:
        """Listing of all Mercenary Dens."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersStructuresMercenaryDensListing | tuple[CharactersStructuresMercenaryDensListing, Response]:
        """Listing of all Mercenary Dens."""
        ...

class GetCorporationsStructuresSkyhooksDetailOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsStructuresSkyhooksDetail:
        """Get the details of a Skyhook."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsStructuresSkyhooksDetail, Response]:
        """Get the details of a Skyhook."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsStructuresSkyhooksDetail | tuple[CorporationsStructuresSkyhooksDetail, Response]:
        """Get the details of a Skyhook."""
        ...

class GetCorporationsStructuresSkyhooksListingOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsStructuresSkyhooksListing:
        """Listing of all Skyhooks."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsStructuresSkyhooksListing, Response]:
        """Listing of all Skyhooks."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsStructuresSkyhooksListing | tuple[CorporationsStructuresSkyhooksListing, Response]:
        """Listing of all Skyhooks."""
        ...

class GetCorporationsStructuresSovereigntyHubsDetailOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsStructuresSovereigntyHubsDetail:
        """Get the details of a Sovereignty Hub."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsStructuresSovereigntyHubsDetail, Response]:
        """Get the details of a Sovereignty Hub."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsStructuresSovereigntyHubsDetail | tuple[CorporationsStructuresSovereigntyHubsDetail, Response]:
        """Get the details of a Sovereignty Hub."""
        ...

class GetCorporationsStructuresSovereigntyHubsListingOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsStructuresSovereigntyHubsListing:
        """Listing of all Sovereignty Hubs."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsStructuresSovereigntyHubsListing, Response]:
        """Listing of all Sovereignty Hubs."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsStructuresSovereigntyHubsListing | tuple[CorporationsStructuresSovereigntyHubsListing, Response]:
        """Listing of all Sovereignty Hubs."""
        ...

class GetUniverseAncestriesOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseAncestriesGet:
        """Get all character ancestries  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseAncestriesGet, Response]:
        """Get all character ancestries  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseAncestriesGet | tuple[UniverseAncestriesGet, Response]:
        """Get all character ancestries  This route expires daily at 11:05"""
        ...

class GetUniverseAsteroidBeltsAsteroidBeltIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseAsteroidBeltsAsteroidBeltIdGet:
        """Get information on an asteroid belt  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseAsteroidBeltsAsteroidBeltIdGet, Response]:
        """Get information on an asteroid belt  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseAsteroidBeltsAsteroidBeltIdGet | tuple[UniverseAsteroidBeltsAsteroidBeltIdGet, Response]:
        """Get information on an asteroid belt  This route expires daily at 11:05"""
        ...

class GetUniverseBloodlinesOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseBloodlinesGet:
        """Get a list of bloodlines  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseBloodlinesGet, Response]:
        """Get a list of bloodlines  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseBloodlinesGet | tuple[UniverseBloodlinesGet, Response]:
        """Get a list of bloodlines  This route expires daily at 11:05"""
        ...

class GetUniverseCategoriesOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseCategoriesGet:
        """Get a list of item categories  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseCategoriesGet, Response]:
        """Get a list of item categories  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseCategoriesGet | tuple[UniverseCategoriesGet, Response]:
        """Get a list of item categories  This route expires daily at 11:05"""
        ...

class GetUniverseCategoriesCategoryIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseCategoriesCategoryIdGet:
        """Get information of an item category  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseCategoriesCategoryIdGet, Response]:
        """Get information of an item category  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseCategoriesCategoryIdGet | tuple[UniverseCategoriesCategoryIdGet, Response]:
        """Get information of an item category  This route expires daily at 11:05"""
        ...

class GetUniverseConstellationsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseConstellationsGet:
        """Get a list of constellations  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseConstellationsGet, Response]:
        """Get a list of constellations  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseConstellationsGet | tuple[UniverseConstellationsGet, Response]:
        """Get a list of constellations  This route expires daily at 11:05"""
        ...

class GetUniverseConstellationsConstellationIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseConstellationsConstellationIdGet:
        """Get information on a constellation  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseConstellationsConstellationIdGet, Response]:
        """Get information on a constellation  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseConstellationsConstellationIdGet | tuple[UniverseConstellationsConstellationIdGet, Response]:
        """Get information on a constellation  This route expires daily at 11:05"""
        ...

class GetUniverseFactionsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseFactionsGet:
        """Get a list of factions  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseFactionsGet, Response]:
        """Get a list of factions  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseFactionsGet | tuple[UniverseFactionsGet, Response]:
        """Get a list of factions  This route expires daily at 11:05"""
        ...

class GetUniverseGraphicsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseGraphicsGet:
        """Get a list of graphics  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseGraphicsGet, Response]:
        """Get a list of graphics  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseGraphicsGet | tuple[UniverseGraphicsGet, Response]:
        """Get a list of graphics  This route expires daily at 11:05"""
        ...

class GetUniverseGraphicsGraphicIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseGraphicsGraphicIdGet:
        """Get information on a graphic  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseGraphicsGraphicIdGet, Response]:
        """Get information on a graphic  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseGraphicsGraphicIdGet | tuple[UniverseGraphicsGraphicIdGet, Response]:
        """Get information on a graphic  This route expires daily at 11:05"""
        ...

class GetUniverseGroupsOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseGroupsGet:
        """Get a list of item groups  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseGroupsGet, Response]:
        """Get a list of item groups  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseGroupsGet | tuple[UniverseGroupsGet, Response]:
        """Get a list of item groups  This route expires daily at 11:05"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[int]:
        """Get a list of item groups  This route expires daily at 11:05"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[int], Response]:
        """Get a list of item groups  This route expires daily at 11:05"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[int] | tuple[list[int], Response]:
        """Get a list of item groups  This route expires daily at 11:05"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[int]]:
        """Get a list of item groups  This route expires daily at 11:05"""
        ...


class GetUniverseGroupsGroupIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseGroupsGroupIdGet:
        """Get information on an item group  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseGroupsGroupIdGet, Response]:
        """Get information on an item group  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseGroupsGroupIdGet | tuple[UniverseGroupsGroupIdGet, Response]:
        """Get information on an item group  This route expires daily at 11:05"""
        ...

class GetUniverseMoonsMoonIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseMoonsMoonIdGet:
        """Get information on a moon  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseMoonsMoonIdGet, Response]:
        """Get information on a moon  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseMoonsMoonIdGet | tuple[UniverseMoonsMoonIdGet, Response]:
        """Get information on a moon  This route expires daily at 11:05"""
        ...

class GetUniversePlanetsPlanetIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniversePlanetsPlanetIdGet:
        """Get information on a planet  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniversePlanetsPlanetIdGet, Response]:
        """Get information on a planet  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniversePlanetsPlanetIdGet | tuple[UniversePlanetsPlanetIdGet, Response]:
        """Get information on a planet  This route expires daily at 11:05"""
        ...

class GetUniverseRacesOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseRacesGet:
        """Get a list of character races  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseRacesGet, Response]:
        """Get a list of character races  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseRacesGet | tuple[UniverseRacesGet, Response]:
        """Get a list of character races  This route expires daily at 11:05"""
        ...

class GetUniverseRegionsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseRegionsGet:
        """Get a list of regions  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseRegionsGet, Response]:
        """Get a list of regions  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseRegionsGet | tuple[UniverseRegionsGet, Response]:
        """Get a list of regions  This route expires daily at 11:05"""
        ...

class GetUniverseRegionsRegionIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseRegionsRegionIdGet:
        """Get information on a region  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseRegionsRegionIdGet, Response]:
        """Get information on a region  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseRegionsRegionIdGet | tuple[UniverseRegionsRegionIdGet, Response]:
        """Get information on a region  This route expires daily at 11:05"""
        ...

class GetUniverseStargatesStargateIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseStargatesStargateIdGet:
        """Get information on a stargate  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseStargatesStargateIdGet, Response]:
        """Get information on a stargate  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseStargatesStargateIdGet | tuple[UniverseStargatesStargateIdGet, Response]:
        """Get information on a stargate  This route expires daily at 11:05"""
        ...

class GetUniverseStarsStarIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseStarsStarIdGet:
        """Get information on a star  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseStarsStarIdGet, Response]:
        """Get information on a star  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseStarsStarIdGet | tuple[UniverseStarsStarIdGet, Response]:
        """Get information on a star  This route expires daily at 11:05"""
        ...

class GetUniverseStationsStationIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseStationsStationIdGet:
        """Get information on a station  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseStationsStationIdGet, Response]:
        """Get information on a station  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseStationsStationIdGet | tuple[UniverseStationsStationIdGet, Response]:
        """Get information on a station  This route expires daily at 11:05"""
        ...

class GetUniverseStructuresOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseStructuresGet:
        """List all public structures"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseStructuresGet, Response]:
        """List all public structures"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseStructuresGet | tuple[UniverseStructuresGet, Response]:
        """List all public structures"""
        ...

class GetUniverseStructuresStructureIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseStructuresStructureIdGet:
        """Returns information on requested structure if you are on the ACL. Otherwise, returns "Forbidden" for all inputs."""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseStructuresStructureIdGet, Response]:
        """Returns information on requested structure if you are on the ACL. Otherwise, returns "Forbidden" for all inputs."""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseStructuresStructureIdGet | tuple[UniverseStructuresStructureIdGet, Response]:
        """Returns information on requested structure if you are on the ACL. Otherwise, returns "Forbidden" for all inputs."""
        ...

class GetUniverseSystemJumpsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseSystemJumpsGet:
        """Get the number of jumps in solar systems within the last hour ending at the timestamp of the Last-Modified header, excluding wormhole space. Only systems with jumps will be listed"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseSystemJumpsGet, Response]:
        """Get the number of jumps in solar systems within the last hour ending at the timestamp of the Last-Modified header, excluding wormhole space. Only systems with jumps will be listed"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseSystemJumpsGet | tuple[UniverseSystemJumpsGet, Response]:
        """Get the number of jumps in solar systems within the last hour ending at the timestamp of the Last-Modified header, excluding wormhole space. Only systems with jumps will be listed"""
        ...

class GetUniverseSystemKillsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseSystemKillsGet:
        """Get the number of ship, pod and NPC kills per solar system within the last hour ending at the timestamp of the Last-Modified header, excluding wormhole space. Only systems with kills will be listed"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseSystemKillsGet, Response]:
        """Get the number of ship, pod and NPC kills per solar system within the last hour ending at the timestamp of the Last-Modified header, excluding wormhole space. Only systems with kills will be listed"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseSystemKillsGet | tuple[UniverseSystemKillsGet, Response]:
        """Get the number of ship, pod and NPC kills per solar system within the last hour ending at the timestamp of the Last-Modified header, excluding wormhole space. Only systems with kills will be listed"""
        ...

class GetUniverseSystemsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseSystemsGet:
        """Get a list of solar systems  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseSystemsGet, Response]:
        """Get a list of solar systems  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseSystemsGet | tuple[UniverseSystemsGet, Response]:
        """Get a list of solar systems  This route expires daily at 11:05"""
        ...

class GetUniverseSystemsSystemIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseSystemsSystemIdGet:
        """Get information on a solar system.  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseSystemsSystemIdGet, Response]:
        """Get information on a solar system.  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseSystemsSystemIdGet | tuple[UniverseSystemsSystemIdGet, Response]:
        """Get information on a solar system.  This route expires daily at 11:05"""
        ...

class GetUniverseTypesOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseTypesGet:
        """Get a list of type ids  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseTypesGet, Response]:
        """Get a list of type ids  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseTypesGet | tuple[UniverseTypesGet, Response]:
        """Get a list of type ids  This route expires daily at 11:05"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[int]:
        """Get a list of type ids  This route expires daily at 11:05"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[int], Response]:
        """Get a list of type ids  This route expires daily at 11:05"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[int] | tuple[list[int], Response]:
        """Get a list of type ids  This route expires daily at 11:05"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[int]]:
        """Get a list of type ids  This route expires daily at 11:05"""
        ...


class GetUniverseTypesTypeIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseTypesTypeIdGet:
        """Get information on a type  This route expires daily at 11:05"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[UniverseTypesTypeIdGet, Response]:
        """Get information on a type  This route expires daily at 11:05"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> UniverseTypesTypeIdGet | tuple[UniverseTypesTypeIdGet, Response]:
        """Get information on a type  This route expires daily at 11:05"""
        ...

class PostUniverseIdsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any:
        """Resolve a set of names to IDs in the following categories: agents, alliances, characters, constellations, corporations factions, inventory_types, regions, stations, and systems. Only exact matches will be returned. All names searched for are cached for 12 hours"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[Any, Response]:
        """Resolve a set of names to IDs in the following categories: agents, alliances, characters, constellations, corporations factions, inventory_types, regions, stations, and systems. Only exact matches will be returned. All names searched for are cached for 12 hours"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any | tuple[Any, Response]:
        """Resolve a set of names to IDs in the following categories: agents, alliances, characters, constellations, corporations factions, inventory_types, regions, stations, and systems. Only exact matches will be returned. All names searched for are cached for 12 hours"""
        ...

class PostUniverseNamesOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any:
        """Resolve a set of IDs to names and categories. Supported ID's for resolving are: Characters, Corporations, Alliances, Stations, Solar Systems, Constellations, Regions, Types, Factions"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[Any, Response]:
        """Resolve a set of IDs to names and categories. Supported ID's for resolving are: Characters, Corporations, Alliances, Stations, Solar Systems, Constellations, Regions, Types, Factions"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any | tuple[Any, Response]:
        """Resolve a set of IDs to names and categories. Supported ID's for resolving are: Characters, Corporations, Alliances, Stations, Solar Systems, Constellations, Regions, Types, Factions"""
        ...

class PostUiAutopilotWaypointOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any:
        """Set a solar system as autopilot waypoint"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[Any, Response]:
        """Set a solar system as autopilot waypoint"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any | tuple[Any, Response]:
        """Set a solar system as autopilot waypoint"""
        ...

class PostUiOpenwindowContractOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any:
        """Open the contract window inside the client"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[Any, Response]:
        """Open the contract window inside the client"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any | tuple[Any, Response]:
        """Open the contract window inside the client"""
        ...

class PostUiOpenwindowInformationOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any:
        """Open the information window for a character, corporation or alliance inside the client"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[Any, Response]:
        """Open the information window for a character, corporation or alliance inside the client"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any | tuple[Any, Response]:
        """Open the information window for a character, corporation or alliance inside the client"""
        ...

class PostUiOpenwindowMarketdetailsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any:
        """Open the market details window for a specific typeID inside the client"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[Any, Response]:
        """Open the market details window for a specific typeID inside the client"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any | tuple[Any, Response]:
        """Open the market details window for a specific typeID inside the client"""
        ...

class PostUiOpenwindowNewmailOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any:
        """Open the New Mail window, according to settings from the request if applicable"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[Any, Response]:
        """Open the New Mail window, according to settings from the request if applicable"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> Any | tuple[Any, Response]:
        """Open the New Mail window, according to settings from the request if applicable"""
        ...

class GetCharactersCharacterIdWalletOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdWalletGet:
        """Returns a character's wallet balance"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdWalletGet, Response]:
        """Returns a character's wallet balance"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdWalletGet | tuple[CharactersCharacterIdWalletGet, Response]:
        """Returns a character's wallet balance"""
        ...

class GetCharactersCharacterIdWalletJournalOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdWalletJournalGet:
        """Retrieve the given character's wallet journal going 30 days back"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdWalletJournalGet, Response]:
        """Retrieve the given character's wallet journal going 30 days back"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdWalletJournalGet | tuple[CharactersCharacterIdWalletJournalGet, Response]:
        """Retrieve the given character's wallet journal going 30 days back"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CharactersCharacterIdWalletJournalGetItem]:
        """Retrieve the given character's wallet journal going 30 days back"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CharactersCharacterIdWalletJournalGetItem], Response]:
        """Retrieve the given character's wallet journal going 30 days back"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CharactersCharacterIdWalletJournalGetItem] | tuple[list[CharactersCharacterIdWalletJournalGetItem], Response]:
        """Retrieve the given character's wallet journal going 30 days back"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CharactersCharacterIdWalletJournalGetItem]]:
        """Retrieve the given character's wallet journal going 30 days back"""
        ...


class GetCharactersCharacterIdWalletTransactionsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdWalletTransactionsGet:
        """Get wallet transactions of a character"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CharactersCharacterIdWalletTransactionsGet, Response]:
        """Get wallet transactions of a character"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CharactersCharacterIdWalletTransactionsGet | tuple[CharactersCharacterIdWalletTransactionsGet, Response]:
        """Get wallet transactions of a character"""
        ...

class GetCorporationsCorporationIdWalletsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdWalletsGet:
        """Get a corporation's wallets"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdWalletsGet, Response]:
        """Get a corporation's wallets"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdWalletsGet | tuple[CorporationsCorporationIdWalletsGet, Response]:
        """Get a corporation's wallets"""
        ...

class GetCorporationsCorporationIdWalletsDivisionJournalOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdWalletsDivisionJournalGet:
        """Retrieve the given corporation's wallet journal for the given division going 30 days back"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdWalletsDivisionJournalGet, Response]:
        """Retrieve the given corporation's wallet journal for the given division going 30 days back"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdWalletsDivisionJournalGet | tuple[CorporationsCorporationIdWalletsDivisionJournalGet, Response]:
        """Retrieve the given corporation's wallet journal for the given division going 30 days back"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdWalletsDivisionJournalGetItem]:
        """Retrieve the given corporation's wallet journal for the given division going 30 days back"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[CorporationsCorporationIdWalletsDivisionJournalGetItem], Response]:
        """Retrieve the given corporation's wallet journal for the given division going 30 days back"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[CorporationsCorporationIdWalletsDivisionJournalGetItem] | tuple[list[CorporationsCorporationIdWalletsDivisionJournalGetItem], Response]:
        """Retrieve the given corporation's wallet journal for the given division going 30 days back"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[CorporationsCorporationIdWalletsDivisionJournalGetItem]]:
        """Retrieve the given corporation's wallet journal for the given division going 30 days back"""
        ...


class GetCorporationsCorporationIdWalletsDivisionTransactionsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdWalletsDivisionTransactionsGet:
        """Get wallet transactions of a corporation"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[CorporationsCorporationIdWalletsDivisionTransactionsGet, Response]:
        """Get wallet transactions of a corporation"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> CorporationsCorporationIdWalletsDivisionTransactionsGet | tuple[CorporationsCorporationIdWalletsDivisionTransactionsGet, Response]:
        """Get wallet transactions of a corporation"""
        ...

class GetWarsOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> WarsGet:
        """Return a list of wars"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[WarsGet, Response]:
        """Return a list of wars"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> WarsGet | tuple[WarsGet, Response]:
        """Return a list of wars"""
        ...

class GetWarsWarIdOperation(EsiOperation):
    """EsiOperation, use result()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> WarsWarIdGet:
        """Return details about a war"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[WarsWarIdGet, Response]:
        """Return details about a war"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> WarsWarIdGet | tuple[WarsWarIdGet, Response]:
        """Return details about a war"""
        ...

class GetWarsWarIdKillmailsOperation(EsiOperation):
    """EsiOperation, use result(), results() or results_localized()"""
    @overload
    def result(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> WarsWarIdKillmailsGet:
        """Return a list of kills related to a war"""
        ...

    @overload
    def result(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[WarsWarIdKillmailsGet, Response]:
        """Return a list of kills related to a war"""
        ...

    def result(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> WarsWarIdKillmailsGet | tuple[WarsWarIdKillmailsGet, Response]:
        """Return a list of kills related to a war"""
        ...

    @overload
    def results(self, use_etag: bool = True, return_response: Literal[False] = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[WarsWarIdKillmailsGetItem]:
        """Return a list of kills related to a war"""
        ...

    @overload
    def results(self, use_etag: bool = True, *, return_response: Literal[True], force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> tuple[list[WarsWarIdKillmailsGetItem], Response]:
        """Return a list of kills related to a war"""
        ...

    def results(self, use_etag: bool = True, return_response: bool = False, force_refresh: bool = False, use_cache: bool = True, store_cache: bool = True, last_modified: datetime | None = None, **extra) -> list[WarsWarIdKillmailsGetItem] | tuple[list[WarsWarIdKillmailsGetItem], Response]:
        """Return a list of kills related to a war"""
        ...

    def results_localized(self, languages: list[str] | str | None = None, **extra) -> dict[str, list[WarsWarIdKillmailsGetItem]]:
        """Return a list of kills related to a war"""
        ...


class ErrorDetail(BaseModel):
    location: str | None
    message: str | None
    value: Any | None


class Error(BaseModel):
    details: list[ErrorDetail] | None
    error: str
    status: int | None


PostCharactersCharacterIdAssetsLocationsOperationBody = list[int]


PostCharactersCharacterIdAssetsNamesOperationBody = list[int]


PostCorporationsCorporationIdAssetsLocationsOperationBody = list[int]


PostCorporationsCorporationIdAssetsNamesOperationBody = list[int]


class PutCharactersCharacterIdCalendarEventIdOperationBody(BaseModel):
    response: Literal['accepted', 'declined', 'tentative']


PostCharactersAffiliationOperationBody = list[int]


PostCharactersCharacterIdCspaOperationBody = list[int]


PostCharactersCharacterIdContactsOperationBody = list[int]


PutCharactersCharacterIdContactsOperationBody = list[int]


class PostCharactersCharacterIdFittingsOperationBody_ItemsItem(BaseModel):
    flag: Literal['Cargo', 'DroneBay', 'FighterBay', 'HiSlot0', 'HiSlot1', 'HiSlot2', 'HiSlot3', 'HiSlot4', 'HiSlot5', 'HiSlot6', 'HiSlot7', 'Invalid', 'LoSlot0', 'LoSlot1', 'LoSlot2', 'LoSlot3', 'LoSlot4', 'LoSlot5', 'LoSlot6', 'LoSlot7', 'MedSlot0', 'MedSlot1', 'MedSlot2', 'MedSlot3', 'MedSlot4', 'MedSlot5', 'MedSlot6', 'MedSlot7', 'RigSlot0', 'RigSlot1', 'RigSlot2', 'ServiceSlot0', 'ServiceSlot1', 'ServiceSlot2', 'ServiceSlot3', 'ServiceSlot4', 'ServiceSlot5', 'ServiceSlot6', 'ServiceSlot7', 'SubSystemSlot0', 'SubSystemSlot1', 'SubSystemSlot2', 'SubSystemSlot3']
    quantity: int
    type_id: int


class PostCharactersCharacterIdFittingsOperationBody(BaseModel):
    description: Annotated[str, Field(max_length=500)]
    items: list[PostCharactersCharacterIdFittingsOperationBody_ItemsItem]
    name: Annotated[str, Field(min_length=1, max_length=50)]
    ship_type_id: int


class PostFleetsFleetIdMembersOperationBody(BaseModel):
    character_id: int
    role: Literal['fleet_commander', 'wing_commander', 'squad_commander', 'squad_member']
    squad_id: int | None
    wing_id: int | None


class PutFleetsFleetIdOperationBody(BaseModel):
    is_free_move: bool | None
    motd: str | None


class PutFleetsFleetIdMembersMemberIdOperationBody(BaseModel):
    role: Literal['fleet_commander', 'wing_commander', 'squad_commander', 'squad_member']
    squad_id: int | None
    wing_id: int | None


class PutFleetsFleetIdSquadsSquadIdOperationBody(BaseModel):
    name: Annotated[str, Field(max_length=10)]


class PutFleetsFleetIdWingsWingIdOperationBody(BaseModel):
    name: Annotated[str, Field(max_length=10)]


class PostCharactersCharacterIdMailOperationBody_RecipientsItem(BaseModel):
    recipient_id: int
    recipient_type: Literal['alliance', 'character', 'corporation', 'mailing_list']


class PostCharactersCharacterIdMailOperationBody(BaseModel):
    approved_cost: int | None
    body: Annotated[str, Field(max_length=10000)]
    recipients: list[PostCharactersCharacterIdMailOperationBody_RecipientsItem]
    subject: Annotated[str, Field(max_length=1000)]


class PostCharactersCharacterIdMailLabelsOperationBody(BaseModel):
    color: Literal['#0000fe', '#006634', '#0099ff', '#00ff33', '#01ffff', '#349800', '#660066', '#666666', '#999999', '#99ffff', '#9a0000', '#ccff9a', '#e6e6e6', '#fe0000', '#ff6600', '#ffff01', '#ffffcd', '#ffffff'] | None
    name: Annotated[str, Field(min_length=1, max_length=40)]


class PutCharactersCharacterIdMailMailIdOperationBody(BaseModel):
    labels: list[int] | None
    read: bool | None


SolarSystemID = int


class RouteConnection(BaseModel):
    from_: Annotated[SolarSystemID, Field(alias='from')]
    to: SolarSystemID


class RouteRequestBody(BaseModel):
    avoid_systems: list[SolarSystemID] | None
    connections: list[RouteConnection] | None
    preference: Literal['Shorter', 'Safer', 'LessSecure'] | None
    security_penalty: int | None


PostRouteOperationBody = RouteRequestBody


PostUniverseIdsOperationBody = list[Annotated[str, Field(min_length=1, max_length=100)]]


PostUniverseNamesOperationBody = list[int]


class PostUiOpenwindowNewmailOperationBody(BaseModel):
    body: Annotated[str, Field(max_length=10000)]
    recipients: list[int]
    subject: Annotated[str, Field(max_length=1000)]
    to_corp_or_alliance_id: int | None
    to_mailing_list_id: int | None


AccessListID = int


AllianceID = int


class CharactersAccessListsDetailAllianceentry(BaseModel):
    access: Literal['Unspecified', 'Allowed', 'Blocked', 'Manager', 'Admin']
    alliance_id: AllianceID


CharacterID = int


class CharactersAccessListsDetailCharacterentry(BaseModel):
    access: Literal['Unspecified', 'Allowed', 'Blocked', 'Manager', 'Admin']
    character_id: CharacterID


CorporationID = int


class CharactersAccessListsDetailCorporationentry(BaseModel):
    access: Literal['Unspecified', 'Allowed', 'Blocked', 'Manager', 'Admin']
    corporation_id: CorporationID


class CharactersAccessListsDetailMembership(BaseModel):
    alliances: list[CharactersAccessListsDetailAllianceentry]
    allow_everyone: bool
    characters: list[CharactersAccessListsDetailCharacterentry]
    corporations: list[CharactersAccessListsDetailCorporationentry]


class CharactersAccessListsDetail(BaseModel):
    description: str
    id: AccessListID
    membership: CharactersAccessListsDetailMembership
    name: str


class CharactersAccessListsListingAccesslist(BaseModel):
    id: AccessListID


class CharactersAccessListsListing(BaseModel):
    access_lists: list[CharactersAccessListsListingAccesslist]


DungeonID = int


ItemID = int


class CharactersMercenaryTacticalOperationsDetail(BaseModel):
    dungeon_type_id: DungeonID
    expires: datetime
    id: UUID
    mercenary_den_id: ItemID
    state: Literal['Unspecified', 'Available', 'Started', 'Completed', 'Expired', 'Removed']


class CharactersMercenaryTacticalOperationsListingOperation(BaseModel):
    id: UUID
    mercenary_den_id: ItemID


class CharactersMercenaryTacticalOperationsListing(BaseModel):
    operations: list[CharactersMercenaryTacticalOperationsListingOperation]


PlanetID = int


class SkyhooksRaidableTheftvulnerability(BaseModel):
    end: datetime
    start: datetime


class SkyhooksRaidableVulnerableskyhook(BaseModel):
    planet_id: PlanetID
    solar_system_id: SolarSystemID
    theft_vulnerability: SkyhooksRaidableTheftvulnerability


class SkyhooksRaidable(BaseModel):
    skyhooks: list[SkyhooksRaidableVulnerableskyhook]


AlliancesGet = list[int]


FactionID = int


class AllianceDetail(BaseModel):
    creator_corporation_id: CorporationID
    creator_id: CharacterID
    date_founded: datetime
    executor_corporation_id: CorporationID | None
    faction_id: FactionID | None
    name: str
    ticker: str


AlliancesAllianceIdCorporationsGet = list[int]


class AlliancesAllianceIdIconsGet(BaseModel):
    px128x128: str | None
    px64x64: str | None


class CharactersCharacterIdAssetsGetItem(BaseModel):
    is_blueprint_copy: bool | None
    is_singleton: bool
    item_id: int
    location_flag: Literal['AssetSafety', 'AutoFit', 'BoosterBay', 'CapsuleerDeliveries', 'Cargo', 'CorporationGoalDeliveries', 'CorpseBay', 'Deliveries', 'DroneBay', 'ExpeditionHold', 'FighterBay', 'FighterTube0', 'FighterTube1', 'FighterTube2', 'FighterTube3', 'FighterTube4', 'FleetHangar', 'FrigateEscapeBay', 'Hangar', 'HangarAll', 'HiSlot0', 'HiSlot1', 'HiSlot2', 'HiSlot3', 'HiSlot4', 'HiSlot5', 'HiSlot6', 'HiSlot7', 'HiddenModifiers', 'Implant', 'InfrastructureHangar', 'LoSlot0', 'LoSlot1', 'LoSlot2', 'LoSlot3', 'LoSlot4', 'LoSlot5', 'LoSlot6', 'LoSlot7', 'Locked', 'MedSlot0', 'MedSlot1', 'MedSlot2', 'MedSlot3', 'MedSlot4', 'MedSlot5', 'MedSlot6', 'MedSlot7', 'MobileDepotHold', 'MoonMaterialBay', 'QuafeBay', 'RigSlot0', 'RigSlot1', 'RigSlot2', 'RigSlot3', 'RigSlot4', 'RigSlot5', 'RigSlot6', 'RigSlot7', 'ShipHangar', 'Skill', 'SpecializedAmmoHold', 'SpecializedAsteroidHold', 'SpecializedCommandCenterHold', 'SpecializedFuelBay', 'SpecializedGasHold', 'SpecializedIceHold', 'SpecializedIndustrialShipHold', 'SpecializedLargeShipHold', 'SpecializedMaterialBay', 'SpecializedMediumShipHold', 'SpecializedMineralHold', 'SpecializedOreHold', 'SpecializedPlanetaryCommoditiesHold', 'SpecializedSalvageHold', 'SpecializedShipHold', 'SpecializedSmallShipHold', 'StructureDeedBay', 'SubSystemBay', 'SubSystemSlot0', 'SubSystemSlot1', 'SubSystemSlot2', 'SubSystemSlot3', 'SubSystemSlot4', 'SubSystemSlot5', 'SubSystemSlot6', 'SubSystemSlot7', 'Unlocked', 'Wardrobe']
    location_id: int
    location_type: Literal['station', 'solar_system', 'item', 'other']
    quantity: int
    type_id: int


CharactersCharacterIdAssetsGet = list[CharactersCharacterIdAssetsGetItem]


class CorporationsCorporationIdAssetsGetItem(BaseModel):
    is_blueprint_copy: bool | None
    is_singleton: bool
    item_id: int
    location_flag: Literal['AssetSafety', 'AutoFit', 'Bonus', 'Booster', 'BoosterBay', 'Capsule', 'CapsuleerDeliveries', 'Cargo', 'CorpDeliveries', 'CorpSAG1', 'CorpSAG2', 'CorpSAG3', 'CorpSAG4', 'CorpSAG5', 'CorpSAG6', 'CorpSAG7', 'CorporationGoalDeliveries', 'CrateLoot', 'Deliveries', 'DroneBay', 'DustBattle', 'DustDatabank', 'ExpeditionHold', 'FighterBay', 'FighterTube0', 'FighterTube1', 'FighterTube2', 'FighterTube3', 'FighterTube4', 'FleetHangar', 'FrigateEscapeBay', 'Hangar', 'HangarAll', 'HiSlot0', 'HiSlot1', 'HiSlot2', 'HiSlot3', 'HiSlot4', 'HiSlot5', 'HiSlot6', 'HiSlot7', 'HiddenModifiers', 'Implant', 'Impounded', 'InfrastructureHangar', 'JunkyardReprocessed', 'JunkyardTrashed', 'LoSlot0', 'LoSlot1', 'LoSlot2', 'LoSlot3', 'LoSlot4', 'LoSlot5', 'LoSlot6', 'LoSlot7', 'Locked', 'MedSlot0', 'MedSlot1', 'MedSlot2', 'MedSlot3', 'MedSlot4', 'MedSlot5', 'MedSlot6', 'MedSlot7', 'MobileDepotHold', 'MoonMaterialBay', 'OfficeFolder', 'Pilot', 'PlanetSurface', 'QuafeBay', 'QuantumCoreRoom', 'Reward', 'RigSlot0', 'RigSlot1', 'RigSlot2', 'RigSlot3', 'RigSlot4', 'RigSlot5', 'RigSlot6', 'RigSlot7', 'SecondaryStorage', 'ServiceSlot0', 'ServiceSlot1', 'ServiceSlot2', 'ServiceSlot3', 'ServiceSlot4', 'ServiceSlot5', 'ServiceSlot6', 'ServiceSlot7', 'ShipHangar', 'ShipOffline', 'Skill', 'SkillInTraining', 'SpecializedAmmoHold', 'SpecializedAsteroidHold', 'SpecializedCommandCenterHold', 'SpecializedFuelBay', 'SpecializedGasHold', 'SpecializedIceHold', 'SpecializedIndustrialShipHold', 'SpecializedLargeShipHold', 'SpecializedMaterialBay', 'SpecializedMediumShipHold', 'SpecializedMineralHold', 'SpecializedOreHold', 'SpecializedPlanetaryCommoditiesHold', 'SpecializedSalvageHold', 'SpecializedShipHold', 'SpecializedSmallShipHold', 'StructureActive', 'StructureFuel', 'StructureInactive', 'StructureOffline', 'SubSystemBay', 'SubSystemSlot0', 'SubSystemSlot1', 'SubSystemSlot2', 'SubSystemSlot3', 'SubSystemSlot4', 'SubSystemSlot5', 'SubSystemSlot6', 'SubSystemSlot7', 'Unlocked', 'Wallet', 'Wardrobe']
    location_id: int
    location_type: Literal['station', 'solar_system', 'item', 'other']
    quantity: int
    type_id: int


CorporationsCorporationIdAssetsGet = list[CorporationsCorporationIdAssetsGetItem]


class CharactersCharacterIdCalendarGetItem(BaseModel):
    event_date: datetime | None
    event_id: int | None
    event_response: Literal['declined', 'not_responded', 'accepted', 'tentative'] | None
    importance: int | None
    title: str | None


CharactersCharacterIdCalendarGet = list[CharactersCharacterIdCalendarGetItem]


class CharactersCharacterIdCalendarEventIdGet(BaseModel):
    date: datetime
    duration: int
    event_id: int
    importance: int
    owner_id: int
    owner_name: str
    owner_type: Literal['eve_server', 'corporation', 'faction', 'character', 'alliance']
    response: str
    text: str
    title: str


class CharactersCharacterIdCalendarEventIdAttendeesGetItem(BaseModel):
    character_id: int | None
    event_response: Literal['declined', 'not_responded', 'accepted', 'tentative'] | None


CharactersCharacterIdCalendarEventIdAttendeesGet = list[CharactersCharacterIdCalendarEventIdAttendeesGetItem]


class CharactersCharacterIdAgentsResearchGetItem(BaseModel):
    agent_id: int
    points_per_day: float
    remainder_points: float
    skill_type_id: int
    started_at: datetime


CharactersCharacterIdAgentsResearchGet = list[CharactersCharacterIdAgentsResearchGetItem]


class CharactersCharacterIdBlueprintsGetItem(BaseModel):
    item_id: int
    location_flag: Literal['AutoFit', 'Cargo', 'CorpseBay', 'DroneBay', 'FleetHangar', 'Deliveries', 'HiddenModifiers', 'Hangar', 'HangarAll', 'LoSlot0', 'LoSlot1', 'LoSlot2', 'LoSlot3', 'LoSlot4', 'LoSlot5', 'LoSlot6', 'LoSlot7', 'MedSlot0', 'MedSlot1', 'MedSlot2', 'MedSlot3', 'MedSlot4', 'MedSlot5', 'MedSlot6', 'MedSlot7', 'HiSlot0', 'HiSlot1', 'HiSlot2', 'HiSlot3', 'HiSlot4', 'HiSlot5', 'HiSlot6', 'HiSlot7', 'AssetSafety', 'Locked', 'Unlocked', 'Implant', 'QuafeBay', 'RigSlot0', 'RigSlot1', 'RigSlot2', 'RigSlot3', 'RigSlot4', 'RigSlot5', 'RigSlot6', 'RigSlot7', 'ShipHangar', 'SpecializedFuelBay', 'SpecializedOreHold', 'SpecializedGasHold', 'SpecializedMineralHold', 'SpecializedSalvageHold', 'SpecializedShipHold', 'SpecializedSmallShipHold', 'SpecializedMediumShipHold', 'SpecializedLargeShipHold', 'SpecializedIndustrialShipHold', 'SpecializedAmmoHold', 'SpecializedCommandCenterHold', 'SpecializedPlanetaryCommoditiesHold', 'SpecializedMaterialBay', 'SubSystemSlot0', 'SubSystemSlot1', 'SubSystemSlot2', 'SubSystemSlot3', 'SubSystemSlot4', 'SubSystemSlot5', 'SubSystemSlot6', 'SubSystemSlot7', 'FighterBay', 'FighterTube0', 'FighterTube1', 'FighterTube2', 'FighterTube3', 'FighterTube4', 'Module']
    location_id: int
    material_efficiency: int
    quantity: int
    runs: int
    time_efficiency: int
    type_id: int


CharactersCharacterIdBlueprintsGet = list[CharactersCharacterIdBlueprintsGetItem]


class CharactersCharacterIdCorporationhistoryGetItem(BaseModel):
    corporation_id: int
    is_deleted: bool | None
    record_id: int
    start_date: datetime


CharactersCharacterIdCorporationhistoryGet = list[CharactersCharacterIdCorporationhistoryGetItem]


class CharactersCharacterIdFatigueGet(BaseModel):
    jump_fatigue_expire_date: datetime | None
    last_jump_date: datetime | None
    last_update_date: datetime | None


class CharactersCharacterIdMedalsGetItem_GraphicsItem(BaseModel):
    color: int | None
    graphic: str
    layer: int
    part: int


class CharactersCharacterIdMedalsGetItem(BaseModel):
    corporation_id: int
    date: datetime
    description: str
    graphics: list[CharactersCharacterIdMedalsGetItem_GraphicsItem]
    issuer_id: int
    medal_id: int
    reason: str
    status: Literal['public', 'private']
    title: str


CharactersCharacterIdMedalsGet = list[CharactersCharacterIdMedalsGetItem]


class CharactersCharacterIdNotificationsGetItem(BaseModel):
    is_read: bool | None
    notification_id: int
    sender_id: int
    sender_type: Literal['character', 'corporation', 'alliance', 'faction', 'other']
    text: str | None
    timestamp: datetime
    type: Literal['AcceptedAlly', 'AcceptedSurrender', 'AgentRetiredTrigravian', 'AllAnchoringMsg', 'AllMaintenanceBillMsg', 'AllStrucInvulnerableMsg', 'AllStructVulnerableMsg', 'AllWarCorpJoinedAllianceMsg', 'AllWarDeclaredMsg', 'AllWarInvalidatedMsg', 'AllWarRetractedMsg', 'AllWarSurrenderMsg', 'AllianceCapitalChanged', 'AllianceWarDeclaredV2', 'AllyContractCancelled', 'AllyJoinedWarAggressorMsg', 'AllyJoinedWarAllyMsg', 'AllyJoinedWarDefenderMsg', 'BattlePunishFriendlyFire', 'BillOutOfMoneyMsg', 'BillPaidCorpAllMsg', 'BountyClaimMsg', 'BountyESSShared', 'BountyESSTaken', 'BountyPlacedAlliance', 'BountyPlacedChar', 'BountyPlacedCorp', 'BountyYourBountyClaimed', 'BuddyConnectContactAdd', 'CharAppAcceptMsg', 'CharAppRejectMsg', 'CharAppWithdrawMsg', 'CharLeftCorpMsg', 'CharMedalMsg', 'CharTerminationMsg', 'CloneActivationMsg', 'CloneActivationMsg2', 'CloneMovedMsg', 'CloneRevokedMsg1', 'CloneRevokedMsg2', 'CombatOperationFinished', 'ContactAdd', 'ContactEdit', 'ContainerPasswordMsg', 'ContractRegionChangedToPochven', 'CorpAllBillMsg', 'CorpAppAcceptMsg', 'CorpAppInvitedMsg', 'CorpAppNewMsg', 'CorpAppRejectCustomMsg', 'CorpAppRejectMsg', 'CorpBecameWarEligible', 'CorpDividendMsg', 'CorpFriendlyFireDisableTimerCompleted', 'CorpFriendlyFireDisableTimerStarted', 'CorpFriendlyFireEnableTimerCompleted', 'CorpFriendlyFireEnableTimerStarted', 'CorpKicked', 'CorpLiquidationMsg', 'CorpNewCEOMsg', 'CorpNewsMsg', 'CorpNoLongerWarEligible', 'CorpOfficeExpirationMsg', 'CorpStructLostMsg', 'CorpTaxChangeMsg', 'CorpVoteCEORevokedMsg', 'CorpVoteMsg', 'CorpWarDeclaredMsg', 'CorpWarDeclaredV2', 'CorpWarFightingLegalMsg', 'CorpWarInvalidatedMsg', 'CorpWarRetractedMsg', 'CorpWarSurrenderMsg', 'CorporationGoalClosed', 'CorporationGoalCompleted', 'CorporationGoalCreated', 'CorporationGoalExpired', 'CorporationGoalLimitReached', 'CorporationGoalNameChange', 'CorporationLeft', 'CustomsMsg', 'DailyItemRewardAutoClaimed', 'DeclareWar', 'DistrictAttacked', 'DustAppAcceptedMsg', 'ESSMainBankLink', 'EntosisCaptureStarted', 'ExpertSystemExpired', 'ExpertSystemExpiryImminent', 'FWAllianceKickCeoIndividualStandingWarning', 'FWAllianceKickMsg', 'FWAllianceKickedCeoIndividualStanding', 'FWAllianceWarningMsg', 'FWCharKickMsg', 'FWCharRankGainMsg', 'FWCharRankLossMsg', 'FWCharWarningMsg', 'FWCharacterKickFromCorpIndividualStandingWarning', 'FWCharacterKickedFromCorpIndividualStanding', 'FWCorpJoinMsg', 'FWCorpKickMsg', 'FWCorpLeaveMsg', 'FWCorpWarningMsg', 'FWCorporationKickCeoIndividualStandingWarning', 'FWCorporationKickedCeoIndividualStanding', 'FacWarCorpJoinRequestMsg', 'FacWarCorpJoinWithdrawMsg', 'FacWarCorpLeaveRequestMsg', 'FacWarCorpLeaveWithdrawMsg', 'FacWarDirectEnlistmentRevoked', 'FacWarLPDisqualifiedEvent', 'FacWarLPDisqualifiedKill', 'FacWarLPPayoutEvent', 'FacWarLPPayoutKill', 'FreelanceProjectACLDeleted', 'FreelanceProjectClosed', 'FreelanceProjectCompleted', 'FreelanceProjectCreated', 'FreelanceProjectExpired', 'FreelanceProjectLimitReached', 'FreelanceProjectParticipantKicked', 'GameTimeAdded', 'GameTimeReceived', 'GameTimeSent', 'GiftReceived', 'IHubDestroyedByBillFailure', 'IncursionCompletedMsg', 'IndustryOperationFinished', 'IndustryTeamAuctionLost', 'IndustryTeamAuctionWon', 'InfrastructureHubBillAboutToExpire', 'InsuranceExpirationMsg', 'InsuranceFirstShipMsg', 'InsuranceInvalidatedMsg', 'InsuranceIssuedMsg', 'InsurancePayoutMsg', 'InvasionCompletedMsg', 'InvasionSystemLogin', 'InvasionSystemStart', 'JumpCloneDeletedMsg1', 'JumpCloneDeletedMsg2', 'KillReportFinalBlow', 'KillReportVictim', 'KillRightAvailable', 'KillRightAvailableOpen', 'KillRightEarned', 'KillRightUnavailable', 'KillRightUnavailableOpen', 'KillRightUsed', 'LPAutoRedeemed', 'LocateCharMsg', 'MadeWarMutual', 'MercOfferRetractedMsg', 'MercOfferedNegotiationMsg', 'MercenaryDenAttacked', 'MercenaryDenNewMTO', 'MercenaryDenReinforced', 'MissionCanceledTriglavian', 'MissionOfferExpirationMsg', 'MissionTimeoutMsg', 'MoonminingAutomaticFracture', 'MoonminingExtractionCancelled', 'MoonminingExtractionFinished', 'MoonminingExtractionStarted', 'MoonminingLaserFired', 'MutualWarExpired', 'MutualWarInviteAccepted', 'MutualWarInviteRejected', 'MutualWarInviteSent', 'NPCStandingsGained', 'NPCStandingsLost', 'OfferToAllyRetracted', 'OfferedSurrender', 'OfferedToAlly', 'OfficeLeaseCanceledInsufficientStandings', 'OldLscMessages', 'OperationFinished', 'OrbitalAttacked', 'OrbitalReinforced', 'OwnershipTransferred', 'RaffleCreated', 'RaffleExpired', 'RaffleFinished', 'ReimbursementMsg', 'ResearchMissionAvailableMsg', 'RetractsWar', 'SPAutoRedeemed', 'SeasonalChallengeCompleted', 'SkinSequencingCompleted', 'SkyhookDeployed', 'SkyhookDestroyed', 'SkyhookLostShields', 'SkyhookOnline', 'SkyhookUnderAttack', 'SovAllClaimAquiredMsg', 'SovAllClaimLostMsg', 'SovCommandNodeEventStarted', 'SovCorpBillLateMsg', 'SovCorpClaimFailMsg', 'SovDisruptorMsg', 'SovStationEnteredFreeport', 'SovStructureDestroyed', 'SovStructureReinforced', 'SovStructureSelfDestructCancel', 'SovStructureSelfDestructFinished', 'SovStructureSelfDestructRequested', 'SovereigntyIHDamageMsg', 'SovereigntySBUDamageMsg', 'SovereigntyTCUDamageMsg', 'StationAggressionMsg1', 'StationAggressionMsg2', 'StationConquerMsg', 'StationServiceDisabled', 'StationServiceEnabled', 'StationStateChangeMsg', 'StoryLineMissionAvailableMsg', 'StructureAnchoring', 'StructureCourierContractChanged', 'StructureDestroyed', 'StructureFuelAlert', 'StructureImpendingAbandonmentAssetsAtRisk', 'StructureItemsDelivered', 'StructureItemsMovedToSafety', 'StructureLostArmor', 'StructureLostShields', 'StructureLowReagentsAlert', 'StructureNoReagentsAlert', 'StructureOnline', 'StructurePaintPurchased', 'StructureServicesOffline', 'StructureUnanchoring', 'StructureUnderAttack', 'StructureWentHighPower', 'StructureWentLowPower', 'StructuresJobsCancelled', 'StructuresJobsPaused', 'StructuresReinforcementChanged', 'TowerAlertMsg', 'TowerResourceAlertMsg', 'TransactionReversalMsg', 'TutorialMsg', 'WarAdopted ', 'WarAllyInherited', 'WarAllyOfferDeclinedMsg', 'WarConcordInvalidates', 'WarDeclared', 'WarEndedHqSecurityDrop', 'WarHQRemovedFromSpace', 'WarInherited', 'WarInvalid', 'WarRetracted', 'WarRetractedByConcord', 'WarSurrenderDeclinedMsg', 'WarSurrenderOfferMsg']


CharactersCharacterIdNotificationsGet = list[CharactersCharacterIdNotificationsGetItem]


class CharactersCharacterIdNotificationsContactsGetItem(BaseModel):
    message: str
    notification_id: int
    send_date: datetime
    sender_character_id: int
    standing_level: float


CharactersCharacterIdNotificationsContactsGet = list[CharactersCharacterIdNotificationsContactsGetItem]


class CharactersCharacterIdPortraitGet(BaseModel):
    px128x128: str | None
    px256x256: str | None
    px512x512: str | None
    px64x64: str | None


class CharactersCharacterIdRolesGet(BaseModel):
    roles: list[Literal['Account_Take_1', 'Account_Take_2', 'Account_Take_3', 'Account_Take_4', 'Account_Take_5', 'Account_Take_6', 'Account_Take_7', 'Accountant', 'Auditor', 'Brand_Manager', 'Communications_Officer', 'Config_Equipment', 'Config_Starbase_Equipment', 'Container_Take_1', 'Container_Take_2', 'Container_Take_3', 'Container_Take_4', 'Container_Take_5', 'Container_Take_6', 'Container_Take_7', 'Contract_Manager', 'Deliveries_Container_Take', 'Deliveries_Query', 'Deliveries_Take', 'Diplomat', 'Director', 'Factory_Manager', 'Fitting_Manager', 'Hangar_Query_1', 'Hangar_Query_2', 'Hangar_Query_3', 'Hangar_Query_4', 'Hangar_Query_5', 'Hangar_Query_6', 'Hangar_Query_7', 'Hangar_Take_1', 'Hangar_Take_2', 'Hangar_Take_3', 'Hangar_Take_4', 'Hangar_Take_5', 'Hangar_Take_6', 'Hangar_Take_7', 'Junior_Accountant', 'Personnel_Manager', 'Project_Manager', 'Rent_Factory_Facility', 'Rent_Office', 'Rent_Research_Facility', 'Security_Officer', 'Skill_Plan_Manager', 'Starbase_Defense_Operator', 'Starbase_Fuel_Technician', 'Station_Manager', 'Trader']] | None
    roles_at_base: list[Literal['Account_Take_1', 'Account_Take_2', 'Account_Take_3', 'Account_Take_4', 'Account_Take_5', 'Account_Take_6', 'Account_Take_7', 'Accountant', 'Auditor', 'Brand_Manager', 'Communications_Officer', 'Config_Equipment', 'Config_Starbase_Equipment', 'Container_Take_1', 'Container_Take_2', 'Container_Take_3', 'Container_Take_4', 'Container_Take_5', 'Container_Take_6', 'Container_Take_7', 'Contract_Manager', 'Deliveries_Container_Take', 'Deliveries_Query', 'Deliveries_Take', 'Diplomat', 'Director', 'Factory_Manager', 'Fitting_Manager', 'Hangar_Query_1', 'Hangar_Query_2', 'Hangar_Query_3', 'Hangar_Query_4', 'Hangar_Query_5', 'Hangar_Query_6', 'Hangar_Query_7', 'Hangar_Take_1', 'Hangar_Take_2', 'Hangar_Take_3', 'Hangar_Take_4', 'Hangar_Take_5', 'Hangar_Take_6', 'Hangar_Take_7', 'Junior_Accountant', 'Personnel_Manager', 'Project_Manager', 'Rent_Factory_Facility', 'Rent_Office', 'Rent_Research_Facility', 'Security_Officer', 'Skill_Plan_Manager', 'Starbase_Defense_Operator', 'Starbase_Fuel_Technician', 'Station_Manager', 'Trader']] | None
    roles_at_hq: list[Literal['Account_Take_1', 'Account_Take_2', 'Account_Take_3', 'Account_Take_4', 'Account_Take_5', 'Account_Take_6', 'Account_Take_7', 'Accountant', 'Auditor', 'Brand_Manager', 'Communications_Officer', 'Config_Equipment', 'Config_Starbase_Equipment', 'Container_Take_1', 'Container_Take_2', 'Container_Take_3', 'Container_Take_4', 'Container_Take_5', 'Container_Take_6', 'Container_Take_7', 'Contract_Manager', 'Deliveries_Container_Take', 'Deliveries_Query', 'Deliveries_Take', 'Diplomat', 'Director', 'Factory_Manager', 'Fitting_Manager', 'Hangar_Query_1', 'Hangar_Query_2', 'Hangar_Query_3', 'Hangar_Query_4', 'Hangar_Query_5', 'Hangar_Query_6', 'Hangar_Query_7', 'Hangar_Take_1', 'Hangar_Take_2', 'Hangar_Take_3', 'Hangar_Take_4', 'Hangar_Take_5', 'Hangar_Take_6', 'Hangar_Take_7', 'Junior_Accountant', 'Personnel_Manager', 'Project_Manager', 'Rent_Factory_Facility', 'Rent_Office', 'Rent_Research_Facility', 'Security_Officer', 'Skill_Plan_Manager', 'Starbase_Defense_Operator', 'Starbase_Fuel_Technician', 'Station_Manager', 'Trader']] | None
    roles_at_other: list[Literal['Account_Take_1', 'Account_Take_2', 'Account_Take_3', 'Account_Take_4', 'Account_Take_5', 'Account_Take_6', 'Account_Take_7', 'Accountant', 'Auditor', 'Brand_Manager', 'Communications_Officer', 'Config_Equipment', 'Config_Starbase_Equipment', 'Container_Take_1', 'Container_Take_2', 'Container_Take_3', 'Container_Take_4', 'Container_Take_5', 'Container_Take_6', 'Container_Take_7', 'Contract_Manager', 'Deliveries_Container_Take', 'Deliveries_Query', 'Deliveries_Take', 'Diplomat', 'Director', 'Factory_Manager', 'Fitting_Manager', 'Hangar_Query_1', 'Hangar_Query_2', 'Hangar_Query_3', 'Hangar_Query_4', 'Hangar_Query_5', 'Hangar_Query_6', 'Hangar_Query_7', 'Hangar_Take_1', 'Hangar_Take_2', 'Hangar_Take_3', 'Hangar_Take_4', 'Hangar_Take_5', 'Hangar_Take_6', 'Hangar_Take_7', 'Junior_Accountant', 'Personnel_Manager', 'Project_Manager', 'Rent_Factory_Facility', 'Rent_Office', 'Rent_Research_Facility', 'Security_Officer', 'Skill_Plan_Manager', 'Starbase_Defense_Operator', 'Starbase_Fuel_Technician', 'Station_Manager', 'Trader']] | None


class CharactersCharacterIdStandingsGetItem(BaseModel):
    from_id: int
    from_type: Literal['agent', 'npc_corp', 'faction']
    standing: float


CharactersCharacterIdStandingsGet = list[CharactersCharacterIdStandingsGetItem]


class CharactersCharacterIdTitlesGetItem(BaseModel):
    name: str | None
    title_id: int | None


CharactersCharacterIdTitlesGet = list[CharactersCharacterIdTitlesGetItem]


BloodlineID = int


RaceID = int


class CharactersDetail(BaseModel):
    achievement_score: int
    alliance_id: AllianceID | None
    birthday: datetime
    bloodline_id: BloodlineID
    character_title_id: UUID | None
    corporation_id: CorporationID
    corporation_title: str | None
    description: str | None
    faction_id: FactionID | None
    gender: Literal['male', 'female']
    name: str
    race_id: RaceID
    security_status: float | None


CharactersCharacterIdCspaPost = float


class CharactersCharacterIdClonesGet_Home_location(BaseModel):
    location_id: int | None
    location_type: Literal['station', 'structure'] | None


class CharactersCharacterIdClonesGet_Jump_clonesItem(BaseModel):
    implants: list[int]
    jump_clone_id: int
    location_id: int
    location_type: Literal['station', 'structure']
    name: str | None


class CharactersCharacterIdClonesGet(BaseModel):
    home_location: CharactersCharacterIdClonesGet_Home_location | None
    jump_clones: list[CharactersCharacterIdClonesGet_Jump_clonesItem]
    last_clone_jump_date: datetime | None
    last_station_change_date: datetime | None


CharactersCharacterIdImplantsGet = list[int]


class AlliancesAllianceIdContactsGetItem(BaseModel):
    contact_id: int
    contact_type: Literal['character', 'corporation', 'alliance', 'faction']
    label_ids: list[int] | None
    standing: float


AlliancesAllianceIdContactsGet = list[AlliancesAllianceIdContactsGetItem]


class AlliancesAllianceIdContactsLabelsGetItem(BaseModel):
    label_id: int
    label_name: str


AlliancesAllianceIdContactsLabelsGet = list[AlliancesAllianceIdContactsLabelsGetItem]


class CharactersCharacterIdContactsGetItem(BaseModel):
    contact_id: int
    contact_type: Literal['character', 'corporation', 'alliance', 'faction']
    is_blocked: bool | None
    is_watched: bool | None
    label_ids: list[int] | None
    standing: float


CharactersCharacterIdContactsGet = list[CharactersCharacterIdContactsGetItem]


class CharactersCharacterIdContactsLabelsGetItem(BaseModel):
    label_id: int
    label_name: str


CharactersCharacterIdContactsLabelsGet = list[CharactersCharacterIdContactsLabelsGetItem]


class CorporationsCorporationIdContactsGetItem(BaseModel):
    contact_id: int
    contact_type: Literal['character', 'corporation', 'alliance', 'faction']
    is_watched: bool | None
    label_ids: list[int] | None
    standing: float


CorporationsCorporationIdContactsGet = list[CorporationsCorporationIdContactsGetItem]


class CorporationsCorporationIdContactsLabelsGetItem(BaseModel):
    label_id: int
    label_name: str


CorporationsCorporationIdContactsLabelsGet = list[CorporationsCorporationIdContactsLabelsGetItem]


CharactersCharacterIdContactsPost = list[int]


class CharactersCharacterIdContractsGetItem(BaseModel):
    acceptor_id: int
    assignee_id: int
    availability: Literal['public', 'personal', 'corporation', 'alliance']
    buyout: float | None
    collateral: float | None
    contract_id: int
    date_accepted: datetime | None
    date_completed: datetime | None
    date_expired: datetime
    date_issued: datetime
    days_to_complete: int | None
    end_location_id: int | None
    for_corporation: bool
    issuer_corporation_id: int
    issuer_id: int
    price: float | None
    reward: float | None
    start_location_id: int | None
    status: Literal['outstanding', 'in_progress', 'finished_issuer', 'finished_contractor', 'finished', 'cancelled', 'rejected', 'failed', 'deleted', 'reversed']
    title: str | None
    type: Literal['unknown', 'item_exchange', 'auction', 'courier', 'loan']
    volume: float | None


CharactersCharacterIdContractsGet = list[CharactersCharacterIdContractsGetItem]


class CharactersCharacterIdContractsContractIdBidsGetItem(BaseModel):
    amount: float
    bid_id: int
    bidder_id: int
    date_bid: datetime


CharactersCharacterIdContractsContractIdBidsGet = list[CharactersCharacterIdContractsContractIdBidsGetItem]


class CharactersCharacterIdContractsContractIdItemsGetItem(BaseModel):
    is_included: bool
    is_singleton: bool
    quantity: int
    raw_quantity: int | None
    record_id: int
    type_id: int


CharactersCharacterIdContractsContractIdItemsGet = list[CharactersCharacterIdContractsContractIdItemsGetItem]


class ContractsPublicBidsContractIdGetItem(BaseModel):
    amount: float
    bid_id: int
    date_bid: datetime


ContractsPublicBidsContractIdGet = list[ContractsPublicBidsContractIdGetItem]


class ContractsPublicItemsContractIdGetItem(BaseModel):
    is_blueprint_copy: bool | None
    is_included: bool
    item_id: int | None
    material_efficiency: int | None
    quantity: int
    record_id: int
    runs: int | None
    time_efficiency: int | None
    type_id: int


ContractsPublicItemsContractIdGet = list[ContractsPublicItemsContractIdGetItem]


class ContractsPublicRegionIdGetItem(BaseModel):
    buyout: float | None
    collateral: float | None
    contract_id: int
    date_expired: datetime
    date_issued: datetime
    days_to_complete: int | None
    end_location_id: int | None
    for_corporation: bool | None
    issuer_corporation_id: int
    issuer_id: int
    price: float | None
    reward: float | None
    start_location_id: int | None
    title: str | None
    type: Literal['unknown', 'item_exchange', 'auction', 'courier', 'loan']
    volume: float | None


ContractsPublicRegionIdGet = list[ContractsPublicRegionIdGetItem]


class CorporationsCorporationIdContractsGetItem(BaseModel):
    acceptor_id: int
    assignee_id: int
    availability: Literal['public', 'personal', 'corporation', 'alliance']
    buyout: float | None
    collateral: float | None
    contract_id: int
    date_accepted: datetime | None
    date_completed: datetime | None
    date_expired: datetime
    date_issued: datetime
    days_to_complete: int | None
    end_location_id: int | None
    for_corporation: bool
    issuer_corporation_id: int
    issuer_id: int
    price: float | None
    reward: float | None
    start_location_id: int | None
    status: Literal['outstanding', 'in_progress', 'finished_issuer', 'finished_contractor', 'finished', 'cancelled', 'rejected', 'failed', 'deleted', 'reversed']
    title: str | None
    type: Literal['unknown', 'item_exchange', 'auction', 'courier', 'loan']
    volume: float | None


CorporationsCorporationIdContractsGet = list[CorporationsCorporationIdContractsGetItem]


class CorporationsCorporationIdContractsContractIdBidsGetItem(BaseModel):
    amount: float
    bid_id: int
    bidder_id: int
    date_bid: datetime


CorporationsCorporationIdContractsContractIdBidsGet = list[CorporationsCorporationIdContractsContractIdBidsGetItem]


class CorporationsCorporationIdContractsContractIdItemsGetItem(BaseModel):
    is_included: bool
    is_singleton: bool
    quantity: int
    raw_quantity: int | None
    record_id: int
    type_id: int


CorporationsCorporationIdContractsContractIdItemsGet = list[CorporationsCorporationIdContractsContractIdItemsGetItem]


StationID = int


class CorporationsDetailPalette(BaseModel):
    main_color: str
    secondary_color: str | None
    tertiary_color: str | None


class CorporationsDetailTaxrates(BaseModel):
    isk: float
    loyalty_point: float


class CorporationsDetail(BaseModel):
    alliance_id: AllianceID | None
    ceo_id: CharacterID | None
    creator_id: CharacterID | None
    date_founded: datetime | None
    description: str
    enlisted_faction_id: FactionID | None
    friendly_fire: Literal['legal', 'illegal']
    home_station_id: StationID
    member_count: int
    name: str
    palette: CorporationsDetailPalette | None
    shares: int
    state: Literal['active', 'closed']
    tax_rates: CorporationsDetailTaxrates
    ticker: str
    type: Literal['player_owned', 'npc_owned']
    url: str | None
    war_eligible: bool


class CorporationsCorporationIdAlliancehistoryGetItem(BaseModel):
    alliance_id: int | None
    is_deleted: bool | None
    record_id: int
    start_date: datetime


CorporationsCorporationIdAlliancehistoryGet = list[CorporationsCorporationIdAlliancehistoryGetItem]


class CorporationsCorporationIdBlueprintsGetItem(BaseModel):
    item_id: int
    location_flag: Literal['AssetSafety', 'AutoFit', 'Bonus', 'Booster', 'BoosterBay', 'Capsule', 'CapsuleerDeliveries', 'Cargo', 'CorpDeliveries', 'CorpSAG1', 'CorpSAG2', 'CorpSAG3', 'CorpSAG4', 'CorpSAG5', 'CorpSAG6', 'CorpSAG7', 'CorporationGoalDeliveries', 'CrateLoot', 'Deliveries', 'DroneBay', 'DustBattle', 'DustDatabank', 'ExpeditionHold', 'FighterBay', 'FighterTube0', 'FighterTube1', 'FighterTube2', 'FighterTube3', 'FighterTube4', 'FleetHangar', 'FrigateEscapeBay', 'Hangar', 'HangarAll', 'HiSlot0', 'HiSlot1', 'HiSlot2', 'HiSlot3', 'HiSlot4', 'HiSlot5', 'HiSlot6', 'HiSlot7', 'HiddenModifiers', 'Implant', 'Impounded', 'InfrastructureHangar', 'JunkyardReprocessed', 'JunkyardTrashed', 'LoSlot0', 'LoSlot1', 'LoSlot2', 'LoSlot3', 'LoSlot4', 'LoSlot5', 'LoSlot6', 'LoSlot7', 'Locked', 'MedSlot0', 'MedSlot1', 'MedSlot2', 'MedSlot3', 'MedSlot4', 'MedSlot5', 'MedSlot6', 'MedSlot7', 'MobileDepotHold', 'MoonMaterialBay', 'OfficeFolder', 'Pilot', 'PlanetSurface', 'QuafeBay', 'QuantumCoreRoom', 'Reward', 'RigSlot0', 'RigSlot1', 'RigSlot2', 'RigSlot3', 'RigSlot4', 'RigSlot5', 'RigSlot6', 'RigSlot7', 'SecondaryStorage', 'ServiceSlot0', 'ServiceSlot1', 'ServiceSlot2', 'ServiceSlot3', 'ServiceSlot4', 'ServiceSlot5', 'ServiceSlot6', 'ServiceSlot7', 'ShipHangar', 'ShipOffline', 'Skill', 'SkillInTraining', 'SpecializedAmmoHold', 'SpecializedAsteroidHold', 'SpecializedCommandCenterHold', 'SpecializedFuelBay', 'SpecializedGasHold', 'SpecializedIceHold', 'SpecializedIndustrialShipHold', 'SpecializedLargeShipHold', 'SpecializedMaterialBay', 'SpecializedMediumShipHold', 'SpecializedMineralHold', 'SpecializedOreHold', 'SpecializedPlanetaryCommoditiesHold', 'SpecializedSalvageHold', 'SpecializedShipHold', 'SpecializedSmallShipHold', 'StructureActive', 'StructureFuel', 'StructureInactive', 'StructureOffline', 'SubSystemBay', 'SubSystemSlot0', 'SubSystemSlot1', 'SubSystemSlot2', 'SubSystemSlot3', 'SubSystemSlot4', 'SubSystemSlot5', 'SubSystemSlot6', 'SubSystemSlot7', 'Unlocked', 'Wallet', 'Wardrobe']
    location_id: int
    material_efficiency: int
    quantity: int
    runs: int
    time_efficiency: int
    type_id: int


CorporationsCorporationIdBlueprintsGet = list[CorporationsCorporationIdBlueprintsGetItem]


class CorporationsCorporationIdContainersLogsGetItem(BaseModel):
    action: Literal['add', 'assemble', 'configure', 'enter_password', 'lock', 'move', 'repackage', 'set_name', 'set_password', 'unlock']
    character_id: int
    container_id: int
    container_type_id: int
    location_flag: Literal['AssetSafety', 'AutoFit', 'Bonus', 'Booster', 'BoosterBay', 'Capsule', 'CapsuleerDeliveries', 'Cargo', 'CorpDeliveries', 'CorpSAG1', 'CorpSAG2', 'CorpSAG3', 'CorpSAG4', 'CorpSAG5', 'CorpSAG6', 'CorpSAG7', 'CorporationGoalDeliveries', 'CrateLoot', 'Deliveries', 'DroneBay', 'DustBattle', 'DustDatabank', 'ExpeditionHold', 'FighterBay', 'FighterTube0', 'FighterTube1', 'FighterTube2', 'FighterTube3', 'FighterTube4', 'FleetHangar', 'FrigateEscapeBay', 'Hangar', 'HangarAll', 'HiSlot0', 'HiSlot1', 'HiSlot2', 'HiSlot3', 'HiSlot4', 'HiSlot5', 'HiSlot6', 'HiSlot7', 'HiddenModifiers', 'Implant', 'Impounded', 'InfrastructureHangar', 'JunkyardReprocessed', 'JunkyardTrashed', 'LoSlot0', 'LoSlot1', 'LoSlot2', 'LoSlot3', 'LoSlot4', 'LoSlot5', 'LoSlot6', 'LoSlot7', 'Locked', 'MedSlot0', 'MedSlot1', 'MedSlot2', 'MedSlot3', 'MedSlot4', 'MedSlot5', 'MedSlot6', 'MedSlot7', 'MobileDepotHold', 'MoonMaterialBay', 'OfficeFolder', 'Pilot', 'PlanetSurface', 'QuafeBay', 'QuantumCoreRoom', 'Reward', 'RigSlot0', 'RigSlot1', 'RigSlot2', 'RigSlot3', 'RigSlot4', 'RigSlot5', 'RigSlot6', 'RigSlot7', 'SecondaryStorage', 'ServiceSlot0', 'ServiceSlot1', 'ServiceSlot2', 'ServiceSlot3', 'ServiceSlot4', 'ServiceSlot5', 'ServiceSlot6', 'ServiceSlot7', 'ShipHangar', 'ShipOffline', 'Skill', 'SkillInTraining', 'SpecializedAmmoHold', 'SpecializedAsteroidHold', 'SpecializedCommandCenterHold', 'SpecializedFuelBay', 'SpecializedGasHold', 'SpecializedIceHold', 'SpecializedIndustrialShipHold', 'SpecializedLargeShipHold', 'SpecializedMaterialBay', 'SpecializedMediumShipHold', 'SpecializedMineralHold', 'SpecializedOreHold', 'SpecializedPlanetaryCommoditiesHold', 'SpecializedSalvageHold', 'SpecializedShipHold', 'SpecializedSmallShipHold', 'StructureActive', 'StructureFuel', 'StructureInactive', 'StructureOffline', 'SubSystemBay', 'SubSystemSlot0', 'SubSystemSlot1', 'SubSystemSlot2', 'SubSystemSlot3', 'SubSystemSlot4', 'SubSystemSlot5', 'SubSystemSlot6', 'SubSystemSlot7', 'Unlocked', 'Wallet', 'Wardrobe']
    location_id: int
    logged_at: datetime
    new_config_bitmask: int | None
    old_config_bitmask: int | None
    password_type: Literal['config', 'general'] | None
    quantity: int | None
    type_id: int | None


CorporationsCorporationIdContainersLogsGet = list[CorporationsCorporationIdContainersLogsGetItem]


class CorporationsCorporationIdDivisionsGet_HangarItem(BaseModel):
    division: int | None
    name: str | None


class CorporationsCorporationIdDivisionsGet_WalletItem(BaseModel):
    division: int | None
    name: str | None


class CorporationsCorporationIdDivisionsGet(BaseModel):
    hangar: list[CorporationsCorporationIdDivisionsGet_HangarItem] | None
    wallet: list[CorporationsCorporationIdDivisionsGet_WalletItem] | None


class CorporationsCorporationIdFacilitiesGetItem(BaseModel):
    facility_id: int
    system_id: int
    type_id: int


CorporationsCorporationIdFacilitiesGet = list[CorporationsCorporationIdFacilitiesGetItem]


class CorporationsCorporationIdIconsGet(BaseModel):
    px128x128: str | None
    px256x256: str | None
    px64x64: str | None


class CorporationsCorporationIdMedalsGetItem(BaseModel):
    created_at: datetime
    creator_id: int
    description: str
    medal_id: int
    title: str


CorporationsCorporationIdMedalsGet = list[CorporationsCorporationIdMedalsGetItem]


class CorporationsCorporationIdMedalsIssuedGetItem(BaseModel):
    character_id: int
    issued_at: datetime
    issuer_id: int
    medal_id: int
    reason: str
    status: Literal['private', 'public']


CorporationsCorporationIdMedalsIssuedGet = list[CorporationsCorporationIdMedalsIssuedGetItem]


CorporationsCorporationIdMembersGet = list[int]


CorporationsCorporationIdMembersLimitGet = int


class CorporationsCorporationIdMembersTitlesGetItem(BaseModel):
    character_id: int
    titles: list[int]


CorporationsCorporationIdMembersTitlesGet = list[CorporationsCorporationIdMembersTitlesGetItem]


class CorporationsCorporationIdMembertrackingGetItem(BaseModel):
    base_id: int | None
    character_id: int
    location_id: int | None
    logoff_date: datetime | None
    logon_date: datetime | None
    ship_type_id: int | None
    start_date: datetime | None


CorporationsCorporationIdMembertrackingGet = list[CorporationsCorporationIdMembertrackingGetItem]


class CorporationsCorporationIdRolesGetItem(BaseModel):
    character_id: int
    grantable_roles: list[Literal['Account_Take_1', 'Account_Take_2', 'Account_Take_3', 'Account_Take_4', 'Account_Take_5', 'Account_Take_6', 'Account_Take_7', 'Accountant', 'Auditor', 'Brand_Manager', 'Communications_Officer', 'Config_Equipment', 'Config_Starbase_Equipment', 'Container_Take_1', 'Container_Take_2', 'Container_Take_3', 'Container_Take_4', 'Container_Take_5', 'Container_Take_6', 'Container_Take_7', 'Contract_Manager', 'Deliveries_Container_Take', 'Deliveries_Query', 'Deliveries_Take', 'Diplomat', 'Director', 'Factory_Manager', 'Fitting_Manager', 'Hangar_Query_1', 'Hangar_Query_2', 'Hangar_Query_3', 'Hangar_Query_4', 'Hangar_Query_5', 'Hangar_Query_6', 'Hangar_Query_7', 'Hangar_Take_1', 'Hangar_Take_2', 'Hangar_Take_3', 'Hangar_Take_4', 'Hangar_Take_5', 'Hangar_Take_6', 'Hangar_Take_7', 'Junior_Accountant', 'Personnel_Manager', 'Project_Manager', 'Rent_Factory_Facility', 'Rent_Office', 'Rent_Research_Facility', 'Security_Officer', 'Skill_Plan_Manager', 'Starbase_Defense_Operator', 'Starbase_Fuel_Technician', 'Station_Manager', 'Trader']] | None
    grantable_roles_at_base: list[Literal['Account_Take_1', 'Account_Take_2', 'Account_Take_3', 'Account_Take_4', 'Account_Take_5', 'Account_Take_6', 'Account_Take_7', 'Accountant', 'Auditor', 'Brand_Manager', 'Communications_Officer', 'Config_Equipment', 'Config_Starbase_Equipment', 'Container_Take_1', 'Container_Take_2', 'Container_Take_3', 'Container_Take_4', 'Container_Take_5', 'Container_Take_6', 'Container_Take_7', 'Contract_Manager', 'Deliveries_Container_Take', 'Deliveries_Query', 'Deliveries_Take', 'Diplomat', 'Director', 'Factory_Manager', 'Fitting_Manager', 'Hangar_Query_1', 'Hangar_Query_2', 'Hangar_Query_3', 'Hangar_Query_4', 'Hangar_Query_5', 'Hangar_Query_6', 'Hangar_Query_7', 'Hangar_Take_1', 'Hangar_Take_2', 'Hangar_Take_3', 'Hangar_Take_4', 'Hangar_Take_5', 'Hangar_Take_6', 'Hangar_Take_7', 'Junior_Accountant', 'Personnel_Manager', 'Project_Manager', 'Rent_Factory_Facility', 'Rent_Office', 'Rent_Research_Facility', 'Security_Officer', 'Skill_Plan_Manager', 'Starbase_Defense_Operator', 'Starbase_Fuel_Technician', 'Station_Manager', 'Trader']] | None
    grantable_roles_at_hq: list[Literal['Account_Take_1', 'Account_Take_2', 'Account_Take_3', 'Account_Take_4', 'Account_Take_5', 'Account_Take_6', 'Account_Take_7', 'Accountant', 'Auditor', 'Brand_Manager', 'Communications_Officer', 'Config_Equipment', 'Config_Starbase_Equipment', 'Container_Take_1', 'Container_Take_2', 'Container_Take_3', 'Container_Take_4', 'Container_Take_5', 'Container_Take_6', 'Container_Take_7', 'Contract_Manager', 'Deliveries_Container_Take', 'Deliveries_Query', 'Deliveries_Take', 'Diplomat', 'Director', 'Factory_Manager', 'Fitting_Manager', 'Hangar_Query_1', 'Hangar_Query_2', 'Hangar_Query_3', 'Hangar_Query_4', 'Hangar_Query_5', 'Hangar_Query_6', 'Hangar_Query_7', 'Hangar_Take_1', 'Hangar_Take_2', 'Hangar_Take_3', 'Hangar_Take_4', 'Hangar_Take_5', 'Hangar_Take_6', 'Hangar_Take_7', 'Junior_Accountant', 'Personnel_Manager', 'Project_Manager', 'Rent_Factory_Facility', 'Rent_Office', 'Rent_Research_Facility', 'Security_Officer', 'Skill_Plan_Manager', 'Starbase_Defense_Operator', 'Starbase_Fuel_Technician', 'Station_Manager', 'Trader']] | None
    grantable_roles_at_other: list[Literal['Account_Take_1', 'Account_Take_2', 'Account_Take_3', 'Account_Take_4', 'Account_Take_5', 'Account_Take_6', 'Account_Take_7', 'Accountant', 'Auditor', 'Brand_Manager', 'Communications_Officer', 'Config_Equipment', 'Config_Starbase_Equipment', 'Container_Take_1', 'Container_Take_2', 'Container_Take_3', 'Container_Take_4', 'Container_Take_5', 'Container_Take_6', 'Container_Take_7', 'Contract_Manager', 'Deliveries_Container_Take', 'Deliveries_Query', 'Deliveries_Take', 'Diplomat', 'Director', 'Factory_Manager', 'Fitting_Manager', 'Hangar_Query_1', 'Hangar_Query_2', 'Hangar_Query_3', 'Hangar_Query_4', 'Hangar_Query_5', 'Hangar_Query_6', 'Hangar_Query_7', 'Hangar_Take_1', 'Hangar_Take_2', 'Hangar_Take_3', 'Hangar_Take_4', 'Hangar_Take_5', 'Hangar_Take_6', 'Hangar_Take_7', 'Junior_Accountant', 'Personnel_Manager', 'Project_Manager', 'Rent_Factory_Facility', 'Rent_Office', 'Rent_Research_Facility', 'Security_Officer', 'Skill_Plan_Manager', 'Starbase_Defense_Operator', 'Starbase_Fuel_Technician', 'Station_Manager', 'Trader']] | None
    roles: list[Literal['Account_Take_1', 'Account_Take_2', 'Account_Take_3', 'Account_Take_4', 'Account_Take_5', 'Account_Take_6', 'Account_Take_7', 'Accountant', 'Auditor', 'Brand_Manager', 'Communications_Officer', 'Config_Equipment', 'Config_Starbase_Equipment', 'Container_Take_1', 'Container_Take_2', 'Container_Take_3', 'Container_Take_4', 'Container_Take_5', 'Container_Take_6', 'Container_Take_7', 'Contract_Manager', 'Deliveries_Container_Take', 'Deliveries_Query', 'Deliveries_Take', 'Diplomat', 'Director', 'Factory_Manager', 'Fitting_Manager', 'Hangar_Query_1', 'Hangar_Query_2', 'Hangar_Query_3', 'Hangar_Query_4', 'Hangar_Query_5', 'Hangar_Query_6', 'Hangar_Query_7', 'Hangar_Take_1', 'Hangar_Take_2', 'Hangar_Take_3', 'Hangar_Take_4', 'Hangar_Take_5', 'Hangar_Take_6', 'Hangar_Take_7', 'Junior_Accountant', 'Personnel_Manager', 'Project_Manager', 'Rent_Factory_Facility', 'Rent_Office', 'Rent_Research_Facility', 'Security_Officer', 'Skill_Plan_Manager', 'Starbase_Defense_Operator', 'Starbase_Fuel_Technician', 'Station_Manager', 'Trader']] | None
    roles_at_base: list[Literal['Account_Take_1', 'Account_Take_2', 'Account_Take_3', 'Account_Take_4', 'Account_Take_5', 'Account_Take_6', 'Account_Take_7', 'Accountant', 'Auditor', 'Brand_Manager', 'Communications_Officer', 'Config_Equipment', 'Config_Starbase_Equipment', 'Container_Take_1', 'Container_Take_2', 'Container_Take_3', 'Container_Take_4', 'Container_Take_5', 'Container_Take_6', 'Container_Take_7', 'Contract_Manager', 'Deliveries_Container_Take', 'Deliveries_Query', 'Deliveries_Take', 'Diplomat', 'Director', 'Factory_Manager', 'Fitting_Manager', 'Hangar_Query_1', 'Hangar_Query_2', 'Hangar_Query_3', 'Hangar_Query_4', 'Hangar_Query_5', 'Hangar_Query_6', 'Hangar_Query_7', 'Hangar_Take_1', 'Hangar_Take_2', 'Hangar_Take_3', 'Hangar_Take_4', 'Hangar_Take_5', 'Hangar_Take_6', 'Hangar_Take_7', 'Junior_Accountant', 'Personnel_Manager', 'Project_Manager', 'Rent_Factory_Facility', 'Rent_Office', 'Rent_Research_Facility', 'Security_Officer', 'Skill_Plan_Manager', 'Starbase_Defense_Operator', 'Starbase_Fuel_Technician', 'Station_Manager', 'Trader']] | None
    roles_at_hq: list[Literal['Account_Take_1', 'Account_Take_2', 'Account_Take_3', 'Account_Take_4', 'Account_Take_5', 'Account_Take_6', 'Account_Take_7', 'Accountant', 'Auditor', 'Brand_Manager', 'Communications_Officer', 'Config_Equipment', 'Config_Starbase_Equipment', 'Container_Take_1', 'Container_Take_2', 'Container_Take_3', 'Container_Take_4', 'Container_Take_5', 'Container_Take_6', 'Container_Take_7', 'Contract_Manager', 'Deliveries_Container_Take', 'Deliveries_Query', 'Deliveries_Take', 'Diplomat', 'Director', 'Factory_Manager', 'Fitting_Manager', 'Hangar_Query_1', 'Hangar_Query_2', 'Hangar_Query_3', 'Hangar_Query_4', 'Hangar_Query_5', 'Hangar_Query_6', 'Hangar_Query_7', 'Hangar_Take_1', 'Hangar_Take_2', 'Hangar_Take_3', 'Hangar_Take_4', 'Hangar_Take_5', 'Hangar_Take_6', 'Hangar_Take_7', 'Junior_Accountant', 'Personnel_Manager', 'Project_Manager', 'Rent_Factory_Facility', 'Rent_Office', 'Rent_Research_Facility', 'Security_Officer', 'Skill_Plan_Manager', 'Starbase_Defense_Operator', 'Starbase_Fuel_Technician', 'Station_Manager', 'Trader']] | None
    roles_at_other: list[Literal['Account_Take_1', 'Account_Take_2', 'Account_Take_3', 'Account_Take_4', 'Account_Take_5', 'Account_Take_6', 'Account_Take_7', 'Accountant', 'Auditor', 'Brand_Manager', 'Communications_Officer', 'Config_Equipment', 'Config_Starbase_Equipment', 'Container_Take_1', 'Container_Take_2', 'Container_Take_3', 'Container_Take_4', 'Container_Take_5', 'Container_Take_6', 'Container_Take_7', 'Contract_Manager', 'Deliveries_Container_Take', 'Deliveries_Query', 'Deliveries_Take', 'Diplomat', 'Director', 'Factory_Manager', 'Fitting_Manager', 'Hangar_Query_1', 'Hangar_Query_2', 'Hangar_Query_3', 'Hangar_Query_4', 'Hangar_Query_5', 'Hangar_Query_6', 'Hangar_Query_7', 'Hangar_Take_1', 'Hangar_Take_2', 'Hangar_Take_3', 'Hangar_Take_4', 'Hangar_Take_5', 'Hangar_Take_6', 'Hangar_Take_7', 'Junior_Accountant', 'Personnel_Manager', 'Project_Manager', 'Rent_Factory_Facility', 'Rent_Office', 'Rent_Research_Facility', 'Security_Officer', 'Skill_Plan_Manager', 'Starbase_Defense_Operator', 'Starbase_Fuel_Technician', 'Station_Manager', 'Trader']] | None


CorporationsCorporationIdRolesGet = list[CorporationsCorporationIdRolesGetItem]


class CorporationsCorporationIdRolesHistoryGetItem(BaseModel):
    changed_at: datetime
    character_id: int
    issuer_id: int
    new_roles: list[Literal['Account_Take_1', 'Account_Take_2', 'Account_Take_3', 'Account_Take_4', 'Account_Take_5', 'Account_Take_6', 'Account_Take_7', 'Accountant', 'Auditor', 'Brand_Manager', 'Communications_Officer', 'Config_Equipment', 'Config_Starbase_Equipment', 'Container_Take_1', 'Container_Take_2', 'Container_Take_3', 'Container_Take_4', 'Container_Take_5', 'Container_Take_6', 'Container_Take_7', 'Contract_Manager', 'Deliveries_Container_Take', 'Deliveries_Query', 'Deliveries_Take', 'Diplomat', 'Director', 'Factory_Manager', 'Fitting_Manager', 'Hangar_Query_1', 'Hangar_Query_2', 'Hangar_Query_3', 'Hangar_Query_4', 'Hangar_Query_5', 'Hangar_Query_6', 'Hangar_Query_7', 'Hangar_Take_1', 'Hangar_Take_2', 'Hangar_Take_3', 'Hangar_Take_4', 'Hangar_Take_5', 'Hangar_Take_6', 'Hangar_Take_7', 'Junior_Accountant', 'Personnel_Manager', 'Project_Manager', 'Rent_Factory_Facility', 'Rent_Office', 'Rent_Research_Facility', 'Security_Officer', 'Skill_Plan_Manager', 'Starbase_Defense_Operator', 'Starbase_Fuel_Technician', 'Station_Manager', 'Trader']]
    old_roles: list[Literal['Account_Take_1', 'Account_Take_2', 'Account_Take_3', 'Account_Take_4', 'Account_Take_5', 'Account_Take_6', 'Account_Take_7', 'Accountant', 'Auditor', 'Brand_Manager', 'Communications_Officer', 'Config_Equipment', 'Config_Starbase_Equipment', 'Container_Take_1', 'Container_Take_2', 'Container_Take_3', 'Container_Take_4', 'Container_Take_5', 'Container_Take_6', 'Container_Take_7', 'Contract_Manager', 'Deliveries_Container_Take', 'Deliveries_Query', 'Deliveries_Take', 'Diplomat', 'Director', 'Factory_Manager', 'Fitting_Manager', 'Hangar_Query_1', 'Hangar_Query_2', 'Hangar_Query_3', 'Hangar_Query_4', 'Hangar_Query_5', 'Hangar_Query_6', 'Hangar_Query_7', 'Hangar_Take_1', 'Hangar_Take_2', 'Hangar_Take_3', 'Hangar_Take_4', 'Hangar_Take_5', 'Hangar_Take_6', 'Hangar_Take_7', 'Junior_Accountant', 'Personnel_Manager', 'Project_Manager', 'Rent_Factory_Facility', 'Rent_Office', 'Rent_Research_Facility', 'Security_Officer', 'Skill_Plan_Manager', 'Starbase_Defense_Operator', 'Starbase_Fuel_Technician', 'Station_Manager', 'Trader']]
    role_type: Literal['grantable_roles', 'grantable_roles_at_base', 'grantable_roles_at_hq', 'grantable_roles_at_other', 'roles', 'roles_at_base', 'roles_at_hq', 'roles_at_other']


CorporationsCorporationIdRolesHistoryGet = list[CorporationsCorporationIdRolesHistoryGetItem]


class CorporationsCorporationIdShareholdersGetItem(BaseModel):
    share_count: int
    shareholder_id: int
    shareholder_type: Literal['character', 'corporation']


CorporationsCorporationIdShareholdersGet = list[CorporationsCorporationIdShareholdersGetItem]


class CorporationsCorporationIdStandingsGetItem(BaseModel):
    from_id: int
    from_type: Literal['agent', 'npc_corp', 'faction']
    standing: float


CorporationsCorporationIdStandingsGet = list[CorporationsCorporationIdStandingsGetItem]


class CorporationsCorporationIdStarbasesGetItem(BaseModel):
    moon_id: int | None
    onlined_since: datetime | None
    reinforced_until: datetime | None
    starbase_id: int
    state: Literal['offline', 'online', 'onlining', 'reinforced', 'unanchoring'] | None
    system_id: int
    type_id: int
    unanchor_at: datetime | None


CorporationsCorporationIdStarbasesGet = list[CorporationsCorporationIdStarbasesGetItem]


class CorporationsCorporationIdStarbasesStarbaseIdGet_FuelsItem(BaseModel):
    quantity: int
    type_id: int


class CorporationsCorporationIdStarbasesStarbaseIdGet(BaseModel):
    allow_alliance_members: bool
    allow_corporation_members: bool
    anchor: Literal['alliance_member', 'config_starbase_equipment_role', 'corporation_member', 'starbase_fuel_technician_role']
    attack_if_at_war: bool
    attack_if_other_security_status_dropping: bool
    attack_security_status_threshold: float | None
    attack_standing_threshold: float | None
    fuel_bay_take: Literal['alliance_member', 'config_starbase_equipment_role', 'corporation_member', 'starbase_fuel_technician_role']
    fuel_bay_view: Literal['alliance_member', 'config_starbase_equipment_role', 'corporation_member', 'starbase_fuel_technician_role']
    fuels: list[CorporationsCorporationIdStarbasesStarbaseIdGet_FuelsItem] | None
    offline: Literal['alliance_member', 'config_starbase_equipment_role', 'corporation_member', 'starbase_fuel_technician_role']
    online: Literal['alliance_member', 'config_starbase_equipment_role', 'corporation_member', 'starbase_fuel_technician_role']
    unanchor: Literal['alliance_member', 'config_starbase_equipment_role', 'corporation_member', 'starbase_fuel_technician_role']
    use_alliance_standings: bool


class CorporationsCorporationIdStructuresGetItem_ServicesItem(BaseModel):
    name: str
    state: Literal['online', 'offline', 'cleanup']


class CorporationsCorporationIdStructuresGetItem(BaseModel):
    corporation_id: int
    fuel_expires: datetime | None
    name: str | None
    next_reinforce_apply: datetime | None
    next_reinforce_hour: int | None
    profile_id: int
    reinforce_hour: int | None
    services: list[CorporationsCorporationIdStructuresGetItem_ServicesItem] | None
    state: Literal['anchor_vulnerable', 'anchoring', 'armor_reinforce', 'armor_vulnerable', 'deploy_vulnerable', 'fitting_invulnerable', 'hull_reinforce', 'hull_vulnerable', 'online_deprecated', 'onlining_vulnerable', 'shield_vulnerable', 'unanchored', 'unknown']
    state_timer_end: datetime | None
    state_timer_start: datetime | None
    structure_id: int
    system_id: int
    type_id: int
    unanchors_at: datetime | None


CorporationsCorporationIdStructuresGet = list[CorporationsCorporationIdStructuresGetItem]


class CorporationsCorporationIdTitlesGetItem(BaseModel):
    grantable_roles: list[Literal['Account_Take_1', 'Account_Take_2', 'Account_Take_3', 'Account_Take_4', 'Account_Take_5', 'Account_Take_6', 'Account_Take_7', 'Accountant', 'Auditor', 'Brand_Manager', 'Communications_Officer', 'Config_Equipment', 'Config_Starbase_Equipment', 'Container_Take_1', 'Container_Take_2', 'Container_Take_3', 'Container_Take_4', 'Container_Take_5', 'Container_Take_6', 'Container_Take_7', 'Contract_Manager', 'Deliveries_Container_Take', 'Deliveries_Query', 'Deliveries_Take', 'Diplomat', 'Director', 'Factory_Manager', 'Fitting_Manager', 'Hangar_Query_1', 'Hangar_Query_2', 'Hangar_Query_3', 'Hangar_Query_4', 'Hangar_Query_5', 'Hangar_Query_6', 'Hangar_Query_7', 'Hangar_Take_1', 'Hangar_Take_2', 'Hangar_Take_3', 'Hangar_Take_4', 'Hangar_Take_5', 'Hangar_Take_6', 'Hangar_Take_7', 'Junior_Accountant', 'Personnel_Manager', 'Project_Manager', 'Rent_Factory_Facility', 'Rent_Office', 'Rent_Research_Facility', 'Security_Officer', 'Skill_Plan_Manager', 'Starbase_Defense_Operator', 'Starbase_Fuel_Technician', 'Station_Manager', 'Trader']] | None
    grantable_roles_at_base: list[Literal['Account_Take_1', 'Account_Take_2', 'Account_Take_3', 'Account_Take_4', 'Account_Take_5', 'Account_Take_6', 'Account_Take_7', 'Accountant', 'Auditor', 'Brand_Manager', 'Communications_Officer', 'Config_Equipment', 'Config_Starbase_Equipment', 'Container_Take_1', 'Container_Take_2', 'Container_Take_3', 'Container_Take_4', 'Container_Take_5', 'Container_Take_6', 'Container_Take_7', 'Contract_Manager', 'Deliveries_Container_Take', 'Deliveries_Query', 'Deliveries_Take', 'Diplomat', 'Director', 'Factory_Manager', 'Fitting_Manager', 'Hangar_Query_1', 'Hangar_Query_2', 'Hangar_Query_3', 'Hangar_Query_4', 'Hangar_Query_5', 'Hangar_Query_6', 'Hangar_Query_7', 'Hangar_Take_1', 'Hangar_Take_2', 'Hangar_Take_3', 'Hangar_Take_4', 'Hangar_Take_5', 'Hangar_Take_6', 'Hangar_Take_7', 'Junior_Accountant', 'Personnel_Manager', 'Project_Manager', 'Rent_Factory_Facility', 'Rent_Office', 'Rent_Research_Facility', 'Security_Officer', 'Skill_Plan_Manager', 'Starbase_Defense_Operator', 'Starbase_Fuel_Technician', 'Station_Manager', 'Trader']] | None
    grantable_roles_at_hq: list[Literal['Account_Take_1', 'Account_Take_2', 'Account_Take_3', 'Account_Take_4', 'Account_Take_5', 'Account_Take_6', 'Account_Take_7', 'Accountant', 'Auditor', 'Brand_Manager', 'Communications_Officer', 'Config_Equipment', 'Config_Starbase_Equipment', 'Container_Take_1', 'Container_Take_2', 'Container_Take_3', 'Container_Take_4', 'Container_Take_5', 'Container_Take_6', 'Container_Take_7', 'Contract_Manager', 'Deliveries_Container_Take', 'Deliveries_Query', 'Deliveries_Take', 'Diplomat', 'Director', 'Factory_Manager', 'Fitting_Manager', 'Hangar_Query_1', 'Hangar_Query_2', 'Hangar_Query_3', 'Hangar_Query_4', 'Hangar_Query_5', 'Hangar_Query_6', 'Hangar_Query_7', 'Hangar_Take_1', 'Hangar_Take_2', 'Hangar_Take_3', 'Hangar_Take_4', 'Hangar_Take_5', 'Hangar_Take_6', 'Hangar_Take_7', 'Junior_Accountant', 'Personnel_Manager', 'Project_Manager', 'Rent_Factory_Facility', 'Rent_Office', 'Rent_Research_Facility', 'Security_Officer', 'Skill_Plan_Manager', 'Starbase_Defense_Operator', 'Starbase_Fuel_Technician', 'Station_Manager', 'Trader']] | None
    grantable_roles_at_other: list[Literal['Account_Take_1', 'Account_Take_2', 'Account_Take_3', 'Account_Take_4', 'Account_Take_5', 'Account_Take_6', 'Account_Take_7', 'Accountant', 'Auditor', 'Brand_Manager', 'Communications_Officer', 'Config_Equipment', 'Config_Starbase_Equipment', 'Container_Take_1', 'Container_Take_2', 'Container_Take_3', 'Container_Take_4', 'Container_Take_5', 'Container_Take_6', 'Container_Take_7', 'Contract_Manager', 'Deliveries_Container_Take', 'Deliveries_Query', 'Deliveries_Take', 'Diplomat', 'Director', 'Factory_Manager', 'Fitting_Manager', 'Hangar_Query_1', 'Hangar_Query_2', 'Hangar_Query_3', 'Hangar_Query_4', 'Hangar_Query_5', 'Hangar_Query_6', 'Hangar_Query_7', 'Hangar_Take_1', 'Hangar_Take_2', 'Hangar_Take_3', 'Hangar_Take_4', 'Hangar_Take_5', 'Hangar_Take_6', 'Hangar_Take_7', 'Junior_Accountant', 'Personnel_Manager', 'Project_Manager', 'Rent_Factory_Facility', 'Rent_Office', 'Rent_Research_Facility', 'Security_Officer', 'Skill_Plan_Manager', 'Starbase_Defense_Operator', 'Starbase_Fuel_Technician', 'Station_Manager', 'Trader']] | None
    name: str | None
    roles: list[Literal['Account_Take_1', 'Account_Take_2', 'Account_Take_3', 'Account_Take_4', 'Account_Take_5', 'Account_Take_6', 'Account_Take_7', 'Accountant', 'Auditor', 'Brand_Manager', 'Communications_Officer', 'Config_Equipment', 'Config_Starbase_Equipment', 'Container_Take_1', 'Container_Take_2', 'Container_Take_3', 'Container_Take_4', 'Container_Take_5', 'Container_Take_6', 'Container_Take_7', 'Contract_Manager', 'Deliveries_Container_Take', 'Deliveries_Query', 'Deliveries_Take', 'Diplomat', 'Director', 'Factory_Manager', 'Fitting_Manager', 'Hangar_Query_1', 'Hangar_Query_2', 'Hangar_Query_3', 'Hangar_Query_4', 'Hangar_Query_5', 'Hangar_Query_6', 'Hangar_Query_7', 'Hangar_Take_1', 'Hangar_Take_2', 'Hangar_Take_3', 'Hangar_Take_4', 'Hangar_Take_5', 'Hangar_Take_6', 'Hangar_Take_7', 'Junior_Accountant', 'Personnel_Manager', 'Project_Manager', 'Rent_Factory_Facility', 'Rent_Office', 'Rent_Research_Facility', 'Security_Officer', 'Skill_Plan_Manager', 'Starbase_Defense_Operator', 'Starbase_Fuel_Technician', 'Station_Manager', 'Trader']] | None
    roles_at_base: list[Literal['Account_Take_1', 'Account_Take_2', 'Account_Take_3', 'Account_Take_4', 'Account_Take_5', 'Account_Take_6', 'Account_Take_7', 'Accountant', 'Auditor', 'Brand_Manager', 'Communications_Officer', 'Config_Equipment', 'Config_Starbase_Equipment', 'Container_Take_1', 'Container_Take_2', 'Container_Take_3', 'Container_Take_4', 'Container_Take_5', 'Container_Take_6', 'Container_Take_7', 'Contract_Manager', 'Deliveries_Container_Take', 'Deliveries_Query', 'Deliveries_Take', 'Diplomat', 'Director', 'Factory_Manager', 'Fitting_Manager', 'Hangar_Query_1', 'Hangar_Query_2', 'Hangar_Query_3', 'Hangar_Query_4', 'Hangar_Query_5', 'Hangar_Query_6', 'Hangar_Query_7', 'Hangar_Take_1', 'Hangar_Take_2', 'Hangar_Take_3', 'Hangar_Take_4', 'Hangar_Take_5', 'Hangar_Take_6', 'Hangar_Take_7', 'Junior_Accountant', 'Personnel_Manager', 'Project_Manager', 'Rent_Factory_Facility', 'Rent_Office', 'Rent_Research_Facility', 'Security_Officer', 'Skill_Plan_Manager', 'Starbase_Defense_Operator', 'Starbase_Fuel_Technician', 'Station_Manager', 'Trader']] | None
    roles_at_hq: list[Literal['Account_Take_1', 'Account_Take_2', 'Account_Take_3', 'Account_Take_4', 'Account_Take_5', 'Account_Take_6', 'Account_Take_7', 'Accountant', 'Auditor', 'Brand_Manager', 'Communications_Officer', 'Config_Equipment', 'Config_Starbase_Equipment', 'Container_Take_1', 'Container_Take_2', 'Container_Take_3', 'Container_Take_4', 'Container_Take_5', 'Container_Take_6', 'Container_Take_7', 'Contract_Manager', 'Deliveries_Container_Take', 'Deliveries_Query', 'Deliveries_Take', 'Diplomat', 'Director', 'Factory_Manager', 'Fitting_Manager', 'Hangar_Query_1', 'Hangar_Query_2', 'Hangar_Query_3', 'Hangar_Query_4', 'Hangar_Query_5', 'Hangar_Query_6', 'Hangar_Query_7', 'Hangar_Take_1', 'Hangar_Take_2', 'Hangar_Take_3', 'Hangar_Take_4', 'Hangar_Take_5', 'Hangar_Take_6', 'Hangar_Take_7', 'Junior_Accountant', 'Personnel_Manager', 'Project_Manager', 'Rent_Factory_Facility', 'Rent_Office', 'Rent_Research_Facility', 'Security_Officer', 'Skill_Plan_Manager', 'Starbase_Defense_Operator', 'Starbase_Fuel_Technician', 'Station_Manager', 'Trader']] | None
    roles_at_other: list[Literal['Account_Take_1', 'Account_Take_2', 'Account_Take_3', 'Account_Take_4', 'Account_Take_5', 'Account_Take_6', 'Account_Take_7', 'Accountant', 'Auditor', 'Brand_Manager', 'Communications_Officer', 'Config_Equipment', 'Config_Starbase_Equipment', 'Container_Take_1', 'Container_Take_2', 'Container_Take_3', 'Container_Take_4', 'Container_Take_5', 'Container_Take_6', 'Container_Take_7', 'Contract_Manager', 'Deliveries_Container_Take', 'Deliveries_Query', 'Deliveries_Take', 'Diplomat', 'Director', 'Factory_Manager', 'Fitting_Manager', 'Hangar_Query_1', 'Hangar_Query_2', 'Hangar_Query_3', 'Hangar_Query_4', 'Hangar_Query_5', 'Hangar_Query_6', 'Hangar_Query_7', 'Hangar_Take_1', 'Hangar_Take_2', 'Hangar_Take_3', 'Hangar_Take_4', 'Hangar_Take_5', 'Hangar_Take_6', 'Hangar_Take_7', 'Junior_Accountant', 'Personnel_Manager', 'Project_Manager', 'Rent_Factory_Facility', 'Rent_Office', 'Rent_Research_Facility', 'Security_Officer', 'Skill_Plan_Manager', 'Starbase_Defense_Operator', 'Starbase_Fuel_Technician', 'Station_Manager', 'Trader']] | None
    title_id: int | None


CorporationsCorporationIdTitlesGet = list[CorporationsCorporationIdTitlesGetItem]


CorporationsNpccorpsGet = list[int]


class CorporationsProjectsContribution(BaseModel):
    contributed: int
    last_modified: datetime | None


class CorporationsProjectsContributorsContributor(BaseModel):
    contributed: int
    id: CharacterID
    name: str


class Cursor(BaseModel):
    after: str | None
    before: str | None


class CorporationsProjectsContributors(BaseModel):
    contributors: list[CorporationsProjectsContributorsContributor]
    cursor: Cursor | None


ArchetypeID = int


class CorporationsProjectsDetailConfigurationmatcherarchetype(BaseModel):
    archetype_id: ArchetypeID | None


class CorporationsProjectsDetailConfigurationmatcherfaction(BaseModel):
    faction_id: FactionID | None


class CorporationsProjectsDetailConfigurationcapturefwcomplex_LocationsItemAlt0(BaseModel):
    solar_system_id: SolarSystemID | None


ConstellationID = int


class CorporationsProjectsDetailConfigurationcapturefwcomplex_LocationsItemAlt1(BaseModel):
    constellation_id: ConstellationID | None


RegionID = int


class CorporationsProjectsDetailConfigurationcapturefwcomplex_LocationsItemAlt2(BaseModel):
    region_id: RegionID | None


class CorporationsProjectsDetailConfigurationcapturefwcomplex(BaseModel):
    archetypes: list[CorporationsProjectsDetailConfigurationmatcherarchetype] | None
    factions: list[CorporationsProjectsDetailConfigurationmatcherfaction] | None
    locations: list[CorporationsProjectsDetailConfigurationcapturefwcomplex_LocationsItemAlt0 | CorporationsProjectsDetailConfigurationcapturefwcomplex_LocationsItemAlt1 | CorporationsProjectsDetailConfigurationcapturefwcomplex_LocationsItemAlt2] | None


class CorporationsProjectsDetail_ConfigurationAlt0(BaseModel):
    capture_fw_complex: CorporationsProjectsDetailConfigurationcapturefwcomplex | None


class CorporationsProjectsDetailConfigurationdamageship_IdentitiesItemAlt0(BaseModel):
    character_id: CharacterID | None


class CorporationsProjectsDetailConfigurationdamageship_IdentitiesItemAlt1(BaseModel):
    corporation_id: CorporationID | None


class CorporationsProjectsDetailConfigurationdamageship_IdentitiesItemAlt2(BaseModel):
    alliance_id: AllianceID | None


class CorporationsProjectsDetailConfigurationdamageship_IdentitiesItemAlt3(BaseModel):
    faction_id: FactionID | None


class CorporationsProjectsDetailConfigurationdamageship_LocationsItemAlt0(BaseModel):
    solar_system_id: SolarSystemID | None


class CorporationsProjectsDetailConfigurationdamageship_LocationsItemAlt1(BaseModel):
    constellation_id: ConstellationID | None


class CorporationsProjectsDetailConfigurationdamageship_LocationsItemAlt2(BaseModel):
    region_id: RegionID | None


TypeID = int


class CorporationsProjectsDetailConfigurationdamageship_ShipsItemAlt0(BaseModel):
    type_id: TypeID | None


ShipTreeGroupID = int


class CorporationsProjectsDetailConfigurationdamageship_ShipsItemAlt1(BaseModel):
    group_id: ShipTreeGroupID | None


class CorporationsProjectsDetailConfigurationdamageship(BaseModel):
    identities: list[CorporationsProjectsDetailConfigurationdamageship_IdentitiesItemAlt0 | CorporationsProjectsDetailConfigurationdamageship_IdentitiesItemAlt1 | CorporationsProjectsDetailConfigurationdamageship_IdentitiesItemAlt2 | CorporationsProjectsDetailConfigurationdamageship_IdentitiesItemAlt3] | None
    locations: list[CorporationsProjectsDetailConfigurationdamageship_LocationsItemAlt0 | CorporationsProjectsDetailConfigurationdamageship_LocationsItemAlt1 | CorporationsProjectsDetailConfigurationdamageship_LocationsItemAlt2] | None
    ships: list[CorporationsProjectsDetailConfigurationdamageship_ShipsItemAlt0 | CorporationsProjectsDetailConfigurationdamageship_ShipsItemAlt1] | None


class CorporationsProjectsDetail_ConfigurationAlt1(BaseModel):
    damage_ship: CorporationsProjectsDetailConfigurationdamageship | None


class CorporationsProjectsDetailConfigurationdefendfwcomplex_LocationsItemAlt0(BaseModel):
    solar_system_id: SolarSystemID | None


class CorporationsProjectsDetailConfigurationdefendfwcomplex_LocationsItemAlt1(BaseModel):
    constellation_id: ConstellationID | None


class CorporationsProjectsDetailConfigurationdefendfwcomplex_LocationsItemAlt2(BaseModel):
    region_id: RegionID | None


class CorporationsProjectsDetailConfigurationdefendfwcomplex(BaseModel):
    archetypes: list[CorporationsProjectsDetailConfigurationmatcherarchetype] | None
    factions: list[CorporationsProjectsDetailConfigurationmatcherfaction] | None
    locations: list[CorporationsProjectsDetailConfigurationdefendfwcomplex_LocationsItemAlt0 | CorporationsProjectsDetailConfigurationdefendfwcomplex_LocationsItemAlt1 | CorporationsProjectsDetailConfigurationdefendfwcomplex_LocationsItemAlt2] | None


class CorporationsProjectsDetail_ConfigurationAlt2(BaseModel):
    defend_fw_complex: CorporationsProjectsDetailConfigurationdefendfwcomplex | None


class CorporationsProjectsDetailConfigurationdeliveritem_Docking_locationsItemAlt0(BaseModel):
    structure_id: ItemID | None


class CorporationsProjectsDetailConfigurationdeliveritem_Docking_locationsItemAlt1(BaseModel):
    station_id: StationID | None


class CorporationsProjectsDetailConfigurationdeliveritem_ItemsItemAlt0(BaseModel):
    type_id: TypeID | None


GroupID = int


class CorporationsProjectsDetailConfigurationdeliveritem_ItemsItemAlt1(BaseModel):
    group_id: GroupID | None


class CorporationsProjectsDetailConfigurationdeliveritem(BaseModel):
    docking_locations: list[CorporationsProjectsDetailConfigurationdeliveritem_Docking_locationsItemAlt0 | CorporationsProjectsDetailConfigurationdeliveritem_Docking_locationsItemAlt1] | None
    items: list[CorporationsProjectsDetailConfigurationdeliveritem_ItemsItemAlt0 | CorporationsProjectsDetailConfigurationdeliveritem_ItemsItemAlt1] | None
    office_id: ItemID | None


class CorporationsProjectsDetail_ConfigurationAlt3(BaseModel):
    deliver_item: CorporationsProjectsDetailConfigurationdeliveritem | None


class CorporationsProjectsDetailConfigurationdestroynpc_LocationsItemAlt0(BaseModel):
    solar_system_id: SolarSystemID | None


class CorporationsProjectsDetailConfigurationdestroynpc_LocationsItemAlt1(BaseModel):
    constellation_id: ConstellationID | None


class CorporationsProjectsDetailConfigurationdestroynpc_LocationsItemAlt2(BaseModel):
    region_id: RegionID | None


class CorporationsProjectsDetailConfigurationdestroynpc(BaseModel):
    locations: list[CorporationsProjectsDetailConfigurationdestroynpc_LocationsItemAlt0 | CorporationsProjectsDetailConfigurationdestroynpc_LocationsItemAlt1 | CorporationsProjectsDetailConfigurationdestroynpc_LocationsItemAlt2] | None


class CorporationsProjectsDetail_ConfigurationAlt4(BaseModel):
    destroy_npc: CorporationsProjectsDetailConfigurationdestroynpc | None


class CorporationsProjectsDetailConfigurationdestroyship_IdentitiesItemAlt0(BaseModel):
    character_id: CharacterID | None


class CorporationsProjectsDetailConfigurationdestroyship_IdentitiesItemAlt1(BaseModel):
    corporation_id: CorporationID | None


class CorporationsProjectsDetailConfigurationdestroyship_IdentitiesItemAlt2(BaseModel):
    alliance_id: AllianceID | None


class CorporationsProjectsDetailConfigurationdestroyship_IdentitiesItemAlt3(BaseModel):
    faction_id: FactionID | None


class CorporationsProjectsDetailConfigurationdestroyship_LocationsItemAlt0(BaseModel):
    solar_system_id: SolarSystemID | None


class CorporationsProjectsDetailConfigurationdestroyship_LocationsItemAlt1(BaseModel):
    constellation_id: ConstellationID | None


class CorporationsProjectsDetailConfigurationdestroyship_LocationsItemAlt2(BaseModel):
    region_id: RegionID | None


class CorporationsProjectsDetailConfigurationdestroyship_ShipsItemAlt0(BaseModel):
    type_id: TypeID | None


class CorporationsProjectsDetailConfigurationdestroyship_ShipsItemAlt1(BaseModel):
    group_id: ShipTreeGroupID | None


class CorporationsProjectsDetailConfigurationdestroyship(BaseModel):
    identities: list[CorporationsProjectsDetailConfigurationdestroyship_IdentitiesItemAlt0 | CorporationsProjectsDetailConfigurationdestroyship_IdentitiesItemAlt1 | CorporationsProjectsDetailConfigurationdestroyship_IdentitiesItemAlt2 | CorporationsProjectsDetailConfigurationdestroyship_IdentitiesItemAlt3] | None
    locations: list[CorporationsProjectsDetailConfigurationdestroyship_LocationsItemAlt0 | CorporationsProjectsDetailConfigurationdestroyship_LocationsItemAlt1 | CorporationsProjectsDetailConfigurationdestroyship_LocationsItemAlt2] | None
    ships: list[CorporationsProjectsDetailConfigurationdestroyship_ShipsItemAlt0 | CorporationsProjectsDetailConfigurationdestroyship_ShipsItemAlt1] | None


class CorporationsProjectsDetail_ConfigurationAlt5(BaseModel):
    destroy_ship: CorporationsProjectsDetailConfigurationdestroyship | None


class CorporationsProjectsDetailConfigurationmatchercorporation(BaseModel):
    corporation_id: CorporationID | None


class CorporationsProjectsDetailConfigurationearnloyaltypoints(BaseModel):
    corporations: list[CorporationsProjectsDetailConfigurationmatchercorporation] | None


class CorporationsProjectsDetail_ConfigurationAlt6(BaseModel):
    earn_loyalty_point: CorporationsProjectsDetailConfigurationearnloyaltypoints | None


class CorporationsProjectsDetailConfigurationlostship_IdentitiesItemAlt0(BaseModel):
    character_id: CharacterID | None


class CorporationsProjectsDetailConfigurationlostship_IdentitiesItemAlt1(BaseModel):
    corporation_id: CorporationID | None


class CorporationsProjectsDetailConfigurationlostship_IdentitiesItemAlt2(BaseModel):
    alliance_id: AllianceID | None


class CorporationsProjectsDetailConfigurationlostship_IdentitiesItemAlt3(BaseModel):
    faction_id: FactionID | None


class CorporationsProjectsDetailConfigurationlostship_LocationsItemAlt0(BaseModel):
    solar_system_id: SolarSystemID | None


class CorporationsProjectsDetailConfigurationlostship_LocationsItemAlt1(BaseModel):
    constellation_id: ConstellationID | None


class CorporationsProjectsDetailConfigurationlostship_LocationsItemAlt2(BaseModel):
    region_id: RegionID | None


class CorporationsProjectsDetailConfigurationlostship_ShipsItemAlt0(BaseModel):
    type_id: TypeID | None


class CorporationsProjectsDetailConfigurationlostship_ShipsItemAlt1(BaseModel):
    group_id: ShipTreeGroupID | None


class CorporationsProjectsDetailConfigurationlostship(BaseModel):
    identities: list[CorporationsProjectsDetailConfigurationlostship_IdentitiesItemAlt0 | CorporationsProjectsDetailConfigurationlostship_IdentitiesItemAlt1 | CorporationsProjectsDetailConfigurationlostship_IdentitiesItemAlt2 | CorporationsProjectsDetailConfigurationlostship_IdentitiesItemAlt3] | None
    locations: list[CorporationsProjectsDetailConfigurationlostship_LocationsItemAlt0 | CorporationsProjectsDetailConfigurationlostship_LocationsItemAlt1 | CorporationsProjectsDetailConfigurationlostship_LocationsItemAlt2] | None
    ships: list[CorporationsProjectsDetailConfigurationlostship_ShipsItemAlt0 | CorporationsProjectsDetailConfigurationlostship_ShipsItemAlt1] | None


class CorporationsProjectsDetail_ConfigurationAlt7(BaseModel):
    lost_ship: CorporationsProjectsDetailConfigurationlostship | None


CorporationsProjectsDetailConfigurationmanual = dict[str, Any]


class CorporationsProjectsDetail_ConfigurationAlt8(BaseModel):
    manual: CorporationsProjectsDetailConfigurationmanual | None


class CorporationsProjectsDetailConfigurationmanufactureitem_Docking_locationsItemAlt0(BaseModel):
    structure_id: ItemID | None


class CorporationsProjectsDetailConfigurationmanufactureitem_Docking_locationsItemAlt1(BaseModel):
    station_id: StationID | None


class CorporationsProjectsDetailConfigurationmanufactureitem_ItemsItemAlt0(BaseModel):
    type_id: TypeID | None


class CorporationsProjectsDetailConfigurationmanufactureitem_ItemsItemAlt1(BaseModel):
    group_id: GroupID | None


class CorporationsProjectsDetailConfigurationmanufactureitem(BaseModel):
    docking_locations: list[CorporationsProjectsDetailConfigurationmanufactureitem_Docking_locationsItemAlt0 | CorporationsProjectsDetailConfigurationmanufactureitem_Docking_locationsItemAlt1] | None
    items: list[CorporationsProjectsDetailConfigurationmanufactureitem_ItemsItemAlt0 | CorporationsProjectsDetailConfigurationmanufactureitem_ItemsItemAlt1] | None
    owner: Literal['Any', 'Corporation', 'Character']


class CorporationsProjectsDetail_ConfigurationAlt9(BaseModel):
    manufacture_item: CorporationsProjectsDetailConfigurationmanufactureitem | None


class CorporationsProjectsDetailConfigurationminematerial_LocationsItemAlt0(BaseModel):
    solar_system_id: SolarSystemID | None


class CorporationsProjectsDetailConfigurationminematerial_LocationsItemAlt1(BaseModel):
    constellation_id: ConstellationID | None


class CorporationsProjectsDetailConfigurationminematerial_LocationsItemAlt2(BaseModel):
    region_id: RegionID | None


class CorporationsProjectsDetailConfigurationminematerial_MaterialsItemAlt0(BaseModel):
    type_id: TypeID | None


class CorporationsProjectsDetailConfigurationminematerial_MaterialsItemAlt1(BaseModel):
    group_id: GroupID | None


class CorporationsProjectsDetailConfigurationminematerial(BaseModel):
    locations: list[CorporationsProjectsDetailConfigurationminematerial_LocationsItemAlt0 | CorporationsProjectsDetailConfigurationminematerial_LocationsItemAlt1 | CorporationsProjectsDetailConfigurationminematerial_LocationsItemAlt2] | None
    materials: list[CorporationsProjectsDetailConfigurationminematerial_MaterialsItemAlt0 | CorporationsProjectsDetailConfigurationminematerial_MaterialsItemAlt1] | None


class CorporationsProjectsDetail_ConfigurationAlt10(BaseModel):
    mine_material: CorporationsProjectsDetailConfigurationminematerial | None


class CorporationsProjectsDetailConfigurationremoteboostshield_IdentitiesItemAlt0(BaseModel):
    character_id: CharacterID | None


class CorporationsProjectsDetailConfigurationremoteboostshield_IdentitiesItemAlt1(BaseModel):
    corporation_id: CorporationID | None


class CorporationsProjectsDetailConfigurationremoteboostshield_IdentitiesItemAlt2(BaseModel):
    alliance_id: AllianceID | None


class CorporationsProjectsDetailConfigurationremoteboostshield_IdentitiesItemAlt3(BaseModel):
    faction_id: FactionID | None


class CorporationsProjectsDetailConfigurationremoteboostshield_LocationsItemAlt0(BaseModel):
    solar_system_id: SolarSystemID | None


class CorporationsProjectsDetailConfigurationremoteboostshield_LocationsItemAlt1(BaseModel):
    constellation_id: ConstellationID | None


class CorporationsProjectsDetailConfigurationremoteboostshield_LocationsItemAlt2(BaseModel):
    region_id: RegionID | None


class CorporationsProjectsDetailConfigurationremoteboostshield_ShipsItemAlt0(BaseModel):
    type_id: TypeID | None


class CorporationsProjectsDetailConfigurationremoteboostshield_ShipsItemAlt1(BaseModel):
    group_id: ShipTreeGroupID | None


class CorporationsProjectsDetailConfigurationremoteboostshield(BaseModel):
    identities: list[CorporationsProjectsDetailConfigurationremoteboostshield_IdentitiesItemAlt0 | CorporationsProjectsDetailConfigurationremoteboostshield_IdentitiesItemAlt1 | CorporationsProjectsDetailConfigurationremoteboostshield_IdentitiesItemAlt2 | CorporationsProjectsDetailConfigurationremoteboostshield_IdentitiesItemAlt3] | None
    locations: list[CorporationsProjectsDetailConfigurationremoteboostshield_LocationsItemAlt0 | CorporationsProjectsDetailConfigurationremoteboostshield_LocationsItemAlt1 | CorporationsProjectsDetailConfigurationremoteboostshield_LocationsItemAlt2] | None
    ships: list[CorporationsProjectsDetailConfigurationremoteboostshield_ShipsItemAlt0 | CorporationsProjectsDetailConfigurationremoteboostshield_ShipsItemAlt1] | None


class CorporationsProjectsDetail_ConfigurationAlt11(BaseModel):
    remote_boost_shield: CorporationsProjectsDetailConfigurationremoteboostshield | None


class CorporationsProjectsDetailConfigurationremoterepairarmor_IdentitiesItemAlt0(BaseModel):
    character_id: CharacterID | None


class CorporationsProjectsDetailConfigurationremoterepairarmor_IdentitiesItemAlt1(BaseModel):
    corporation_id: CorporationID | None


class CorporationsProjectsDetailConfigurationremoterepairarmor_IdentitiesItemAlt2(BaseModel):
    alliance_id: AllianceID | None


class CorporationsProjectsDetailConfigurationremoterepairarmor_IdentitiesItemAlt3(BaseModel):
    faction_id: FactionID | None


class CorporationsProjectsDetailConfigurationremoterepairarmor_LocationsItemAlt0(BaseModel):
    solar_system_id: SolarSystemID | None


class CorporationsProjectsDetailConfigurationremoterepairarmor_LocationsItemAlt1(BaseModel):
    constellation_id: ConstellationID | None


class CorporationsProjectsDetailConfigurationremoterepairarmor_LocationsItemAlt2(BaseModel):
    region_id: RegionID | None


class CorporationsProjectsDetailConfigurationremoterepairarmor_ShipsItemAlt0(BaseModel):
    type_id: TypeID | None


class CorporationsProjectsDetailConfigurationremoterepairarmor_ShipsItemAlt1(BaseModel):
    group_id: ShipTreeGroupID | None


class CorporationsProjectsDetailConfigurationremoterepairarmor(BaseModel):
    identities: list[CorporationsProjectsDetailConfigurationremoterepairarmor_IdentitiesItemAlt0 | CorporationsProjectsDetailConfigurationremoterepairarmor_IdentitiesItemAlt1 | CorporationsProjectsDetailConfigurationremoterepairarmor_IdentitiesItemAlt2 | CorporationsProjectsDetailConfigurationremoterepairarmor_IdentitiesItemAlt3] | None
    locations: list[CorporationsProjectsDetailConfigurationremoterepairarmor_LocationsItemAlt0 | CorporationsProjectsDetailConfigurationremoterepairarmor_LocationsItemAlt1 | CorporationsProjectsDetailConfigurationremoterepairarmor_LocationsItemAlt2] | None
    ships: list[CorporationsProjectsDetailConfigurationremoterepairarmor_ShipsItemAlt0 | CorporationsProjectsDetailConfigurationremoterepairarmor_ShipsItemAlt1] | None


class CorporationsProjectsDetail_ConfigurationAlt12(BaseModel):
    remote_repair_armor: CorporationsProjectsDetailConfigurationremoterepairarmor | None


class CorporationsProjectsDetailConfigurationsalvagewreck_LocationsItemAlt0(BaseModel):
    solar_system_id: SolarSystemID | None


class CorporationsProjectsDetailConfigurationsalvagewreck_LocationsItemAlt1(BaseModel):
    constellation_id: ConstellationID | None


class CorporationsProjectsDetailConfigurationsalvagewreck_LocationsItemAlt2(BaseModel):
    region_id: RegionID | None


class CorporationsProjectsDetailConfigurationsalvagewreck(BaseModel):
    locations: list[CorporationsProjectsDetailConfigurationsalvagewreck_LocationsItemAlt0 | CorporationsProjectsDetailConfigurationsalvagewreck_LocationsItemAlt1 | CorporationsProjectsDetailConfigurationsalvagewreck_LocationsItemAlt2] | None


class CorporationsProjectsDetail_ConfigurationAlt13(BaseModel):
    salvage_wreck: CorporationsProjectsDetailConfigurationsalvagewreck | None


class CorporationsProjectsDetailConfigurationscansignature_LocationsItemAlt0(BaseModel):
    solar_system_id: SolarSystemID | None


class CorporationsProjectsDetailConfigurationscansignature_LocationsItemAlt1(BaseModel):
    constellation_id: ConstellationID | None


class CorporationsProjectsDetailConfigurationscansignature_LocationsItemAlt2(BaseModel):
    region_id: RegionID | None


AttributeID = int


class CorporationsProjectsDetailConfigurationmatchersignature(BaseModel):
    signature_type_id: AttributeID | None


class CorporationsProjectsDetailConfigurationscansignature(BaseModel):
    locations: list[CorporationsProjectsDetailConfigurationscansignature_LocationsItemAlt0 | CorporationsProjectsDetailConfigurationscansignature_LocationsItemAlt1 | CorporationsProjectsDetailConfigurationscansignature_LocationsItemAlt2] | None
    signatures: list[CorporationsProjectsDetailConfigurationmatchersignature] | None


class CorporationsProjectsDetail_ConfigurationAlt14(BaseModel):
    scan_signature: CorporationsProjectsDetailConfigurationscansignature | None


class CorporationsProjectsDetailConfigurationshipinsurance_IdentitiesItemAlt0(BaseModel):
    character_id: CharacterID | None


class CorporationsProjectsDetailConfigurationshipinsurance_IdentitiesItemAlt1(BaseModel):
    corporation_id: CorporationID | None


class CorporationsProjectsDetailConfigurationshipinsurance_IdentitiesItemAlt2(BaseModel):
    alliance_id: AllianceID | None


class CorporationsProjectsDetailConfigurationshipinsurance_IdentitiesItemAlt3(BaseModel):
    faction_id: FactionID | None


class CorporationsProjectsDetailConfigurationshipinsurance_LocationsItemAlt0(BaseModel):
    solar_system_id: SolarSystemID | None


class CorporationsProjectsDetailConfigurationshipinsurance_LocationsItemAlt1(BaseModel):
    constellation_id: ConstellationID | None


class CorporationsProjectsDetailConfigurationshipinsurance_LocationsItemAlt2(BaseModel):
    region_id: RegionID | None


class CorporationsProjectsDetailConfigurationshipinsurance_ShipsItemAlt0(BaseModel):
    type_id: TypeID | None


class CorporationsProjectsDetailConfigurationshipinsurance_ShipsItemAlt1(BaseModel):
    group_id: ShipTreeGroupID | None


class CorporationsProjectsDetailConfigurationshipinsurance(BaseModel):
    conflict_type: Literal['Any', 'Pvp', 'Pve']
    identities: list[CorporationsProjectsDetailConfigurationshipinsurance_IdentitiesItemAlt0 | CorporationsProjectsDetailConfigurationshipinsurance_IdentitiesItemAlt1 | CorporationsProjectsDetailConfigurationshipinsurance_IdentitiesItemAlt2 | CorporationsProjectsDetailConfigurationshipinsurance_IdentitiesItemAlt3] | None
    locations: list[CorporationsProjectsDetailConfigurationshipinsurance_LocationsItemAlt0 | CorporationsProjectsDetailConfigurationshipinsurance_LocationsItemAlt1 | CorporationsProjectsDetailConfigurationshipinsurance_LocationsItemAlt2] | None
    reimburse_implants: bool
    ships: list[CorporationsProjectsDetailConfigurationshipinsurance_ShipsItemAlt0 | CorporationsProjectsDetailConfigurationshipinsurance_ShipsItemAlt1] | None


class CorporationsProjectsDetail_ConfigurationAlt15(BaseModel):
    ship_insurance: CorporationsProjectsDetailConfigurationshipinsurance | None


class CorporationsProjectsDetailConfigurationunknown(BaseModel):
    data: Any
    type: str


class CorporationsProjectsDetail_ConfigurationAlt16(BaseModel):
    unknown: CorporationsProjectsDetailConfigurationunknown | None


class CorporationsProjectsDetailContribution(BaseModel):
    participation_limit: int | None
    reward_per_contribution: float | None
    submission_limit: int | None
    submission_multiplier: float | None


class CorporationsProjectsDetailCreator(BaseModel):
    id: CharacterID
    name: str


class CorporationsProjectsDetailDetails(BaseModel):
    career: Literal['Unspecified', 'Explorer', 'Industrialist', 'Enforcer', 'Soldier of Fortune']
    created: datetime
    description: str
    expires: datetime | None
    finished: datetime | None


class CorporationsProjectsDetailProgress(BaseModel):
    current: int
    desired: int


class CorporationsProjectsDetailReward(BaseModel):
    initial: float
    remaining: float


class CorporationsProjectsDetail(BaseModel):
    configuration: CorporationsProjectsDetail_ConfigurationAlt0 | CorporationsProjectsDetail_ConfigurationAlt1 | CorporationsProjectsDetail_ConfigurationAlt2 | CorporationsProjectsDetail_ConfigurationAlt3 | CorporationsProjectsDetail_ConfigurationAlt4 | CorporationsProjectsDetail_ConfigurationAlt5 | CorporationsProjectsDetail_ConfigurationAlt6 | CorporationsProjectsDetail_ConfigurationAlt7 | CorporationsProjectsDetail_ConfigurationAlt8 | CorporationsProjectsDetail_ConfigurationAlt9 | CorporationsProjectsDetail_ConfigurationAlt10 | CorporationsProjectsDetail_ConfigurationAlt11 | CorporationsProjectsDetail_ConfigurationAlt12 | CorporationsProjectsDetail_ConfigurationAlt13 | CorporationsProjectsDetail_ConfigurationAlt14 | CorporationsProjectsDetail_ConfigurationAlt15 | CorporationsProjectsDetail_ConfigurationAlt16
    contribution: CorporationsProjectsDetailContribution | None
    creator: CorporationsProjectsDetailCreator
    details: CorporationsProjectsDetailDetails
    id: UUID
    last_modified: datetime
    name: str
    progress: CorporationsProjectsDetailProgress
    reward: CorporationsProjectsDetailReward | None
    state: Literal['Unspecified', 'Active', 'Closed', 'Completed', 'Expired', 'Deleted']


class CorporationsProjectsDetailProject(BaseModel):
    id: UUID
    last_modified: datetime
    name: str
    progress: CorporationsProjectsDetailProgress
    reward: CorporationsProjectsDetailReward | None
    state: Literal['Unspecified', 'Active', 'Closed', 'Completed', 'Expired', 'Deleted']


class CorporationsProjectsListing(BaseModel):
    cursor: Cursor | None
    projects: list[CorporationsProjectsDetailProject]


DogmaAttributesGet = list[int]


class DogmaAttributesAttributeIdGet(BaseModel):
    attribute_id: int
    default_value: float | None
    description: str | None
    display_name: str | None
    high_is_good: bool | None
    icon_id: int | None
    name: str | None
    published: bool | None
    stackable: bool | None
    unit_id: int | None


class DogmaDynamicItemsTypeIdItemIdGet_Dogma_attributesItem(BaseModel):
    attribute_id: int
    value: float


class DogmaDynamicItemsTypeIdItemIdGet_Dogma_effectsItem(BaseModel):
    effect_id: int
    is_default: bool


class DogmaDynamicItemsTypeIdItemIdGet(BaseModel):
    created_by: int
    dogma_attributes: list[DogmaDynamicItemsTypeIdItemIdGet_Dogma_attributesItem]
    dogma_effects: list[DogmaDynamicItemsTypeIdItemIdGet_Dogma_effectsItem]
    mutator_type_id: int
    source_type_id: int


DogmaEffectsGet = list[int]


class DogmaEffectsEffectIdGet_ModifiersItem(BaseModel):
    domain: str | None
    effect_id: int | None
    func: str
    modified_attribute_id: int | None
    modifying_attribute_id: int | None
    operator: int | None


class DogmaEffectsEffectIdGet(BaseModel):
    description: str | None
    disallow_auto_repeat: bool | None
    discharge_attribute_id: int | None
    display_name: str | None
    duration_attribute_id: int | None
    effect_category: int | None
    effect_id: int
    electronic_chance: bool | None
    falloff_attribute_id: int | None
    icon_id: int | None
    is_assistance: bool | None
    is_offensive: bool | None
    is_warp_safe: bool | None
    modifiers: list[DogmaEffectsEffectIdGet_ModifiersItem] | None
    name: str | None
    post_expression: int | None
    pre_expression: int | None
    published: bool | None
    range_attribute_id: int | None
    range_chance: bool | None
    tracking_speed_attribute_id: int | None


class CharactersCharacterIdFwStatsGet_Kills(BaseModel):
    last_week: int
    total: int
    yesterday: int


class CharactersCharacterIdFwStatsGet_Victory_points(BaseModel):
    last_week: int
    total: int
    yesterday: int


class CharactersCharacterIdFwStatsGet(BaseModel):
    current_rank: int | None
    enlisted_on: datetime | None
    faction_id: int | None
    highest_rank: int | None
    kills: CharactersCharacterIdFwStatsGet_Kills
    victory_points: CharactersCharacterIdFwStatsGet_Victory_points


class CorporationsCorporationIdFwStatsGet_Kills(BaseModel):
    last_week: int
    total: int
    yesterday: int


class CorporationsCorporationIdFwStatsGet_Victory_points(BaseModel):
    last_week: int
    total: int
    yesterday: int


class CorporationsCorporationIdFwStatsGet(BaseModel):
    enlisted_on: datetime | None
    faction_id: int | None
    kills: CorporationsCorporationIdFwStatsGet_Kills
    pilots: int | None
    victory_points: CorporationsCorporationIdFwStatsGet_Victory_points


class FwLeaderboardsGet_Kills_Active_totalItem(BaseModel):
    amount: int | None
    faction_id: int | None


class FwLeaderboardsGet_Kills_Last_weekItem(BaseModel):
    amount: int | None
    faction_id: int | None


class FwLeaderboardsGet_Kills_YesterdayItem(BaseModel):
    amount: int | None
    faction_id: int | None


class FwLeaderboardsGet_Kills(BaseModel):
    active_total: list[FwLeaderboardsGet_Kills_Active_totalItem]
    last_week: list[FwLeaderboardsGet_Kills_Last_weekItem]
    yesterday: list[FwLeaderboardsGet_Kills_YesterdayItem]


class FwLeaderboardsGet_Victory_points_Active_totalItem(BaseModel):
    amount: int | None
    faction_id: int | None


class FwLeaderboardsGet_Victory_points_Last_weekItem(BaseModel):
    amount: int | None
    faction_id: int | None


class FwLeaderboardsGet_Victory_points_YesterdayItem(BaseModel):
    amount: int | None
    faction_id: int | None


class FwLeaderboardsGet_Victory_points(BaseModel):
    active_total: list[FwLeaderboardsGet_Victory_points_Active_totalItem]
    last_week: list[FwLeaderboardsGet_Victory_points_Last_weekItem]
    yesterday: list[FwLeaderboardsGet_Victory_points_YesterdayItem]


class FwLeaderboardsGet(BaseModel):
    kills: FwLeaderboardsGet_Kills
    victory_points: FwLeaderboardsGet_Victory_points


class FwLeaderboardsCharactersGet_Kills_Active_totalItem(BaseModel):
    amount: int | None
    character_id: int | None


class FwLeaderboardsCharactersGet_Kills_Last_weekItem(BaseModel):
    amount: int | None
    character_id: int | None


class FwLeaderboardsCharactersGet_Kills_YesterdayItem(BaseModel):
    amount: int | None
    character_id: int | None


class FwLeaderboardsCharactersGet_Kills(BaseModel):
    active_total: list[FwLeaderboardsCharactersGet_Kills_Active_totalItem]
    last_week: list[FwLeaderboardsCharactersGet_Kills_Last_weekItem]
    yesterday: list[FwLeaderboardsCharactersGet_Kills_YesterdayItem]


class FwLeaderboardsCharactersGet_Victory_points_Active_totalItem(BaseModel):
    amount: int | None
    character_id: int | None


class FwLeaderboardsCharactersGet_Victory_points_Last_weekItem(BaseModel):
    amount: int | None
    character_id: int | None


class FwLeaderboardsCharactersGet_Victory_points_YesterdayItem(BaseModel):
    amount: int | None
    character_id: int | None


class FwLeaderboardsCharactersGet_Victory_points(BaseModel):
    active_total: list[FwLeaderboardsCharactersGet_Victory_points_Active_totalItem]
    last_week: list[FwLeaderboardsCharactersGet_Victory_points_Last_weekItem]
    yesterday: list[FwLeaderboardsCharactersGet_Victory_points_YesterdayItem]


class FwLeaderboardsCharactersGet(BaseModel):
    kills: FwLeaderboardsCharactersGet_Kills
    victory_points: FwLeaderboardsCharactersGet_Victory_points


class FwLeaderboardsCorporationsGet_Kills_Active_totalItem(BaseModel):
    amount: int | None
    corporation_id: int | None


class FwLeaderboardsCorporationsGet_Kills_Last_weekItem(BaseModel):
    amount: int | None
    corporation_id: int | None


class FwLeaderboardsCorporationsGet_Kills_YesterdayItem(BaseModel):
    amount: int | None
    corporation_id: int | None


class FwLeaderboardsCorporationsGet_Kills(BaseModel):
    active_total: list[FwLeaderboardsCorporationsGet_Kills_Active_totalItem]
    last_week: list[FwLeaderboardsCorporationsGet_Kills_Last_weekItem]
    yesterday: list[FwLeaderboardsCorporationsGet_Kills_YesterdayItem]


class FwLeaderboardsCorporationsGet_Victory_points_Active_totalItem(BaseModel):
    amount: int | None
    corporation_id: int | None


class FwLeaderboardsCorporationsGet_Victory_points_Last_weekItem(BaseModel):
    amount: int | None
    corporation_id: int | None


class FwLeaderboardsCorporationsGet_Victory_points_YesterdayItem(BaseModel):
    amount: int | None
    corporation_id: int | None


class FwLeaderboardsCorporationsGet_Victory_points(BaseModel):
    active_total: list[FwLeaderboardsCorporationsGet_Victory_points_Active_totalItem]
    last_week: list[FwLeaderboardsCorporationsGet_Victory_points_Last_weekItem]
    yesterday: list[FwLeaderboardsCorporationsGet_Victory_points_YesterdayItem]


class FwLeaderboardsCorporationsGet(BaseModel):
    kills: FwLeaderboardsCorporationsGet_Kills
    victory_points: FwLeaderboardsCorporationsGet_Victory_points


class FwStatsGetItem_Kills(BaseModel):
    last_week: int
    total: int
    yesterday: int


class FwStatsGetItem_Victory_points(BaseModel):
    last_week: int
    total: int
    yesterday: int


class FwStatsGetItem(BaseModel):
    faction_id: int
    kills: FwStatsGetItem_Kills
    pilots: int
    systems_controlled: int
    victory_points: FwStatsGetItem_Victory_points


FwStatsGet = list[FwStatsGetItem]


class FwSystemsGetItem(BaseModel):
    contested: Literal['captured', 'contested', 'uncontested', 'vulnerable']
    occupier_faction_id: int
    owner_faction_id: int
    solar_system_id: int
    victory_points: int
    victory_points_threshold: int


FwSystemsGet = list[FwSystemsGetItem]


class FwWarsGetItem(BaseModel):
    against_id: int
    faction_id: int


FwWarsGet = list[FwWarsGetItem]


class CharactersCharacterIdFittingsGetItem_ItemsItem(BaseModel):
    flag: Literal['Cargo', 'DroneBay', 'FighterBay', 'HiSlot0', 'HiSlot1', 'HiSlot2', 'HiSlot3', 'HiSlot4', 'HiSlot5', 'HiSlot6', 'HiSlot7', 'Invalid', 'LoSlot0', 'LoSlot1', 'LoSlot2', 'LoSlot3', 'LoSlot4', 'LoSlot5', 'LoSlot6', 'LoSlot7', 'MedSlot0', 'MedSlot1', 'MedSlot2', 'MedSlot3', 'MedSlot4', 'MedSlot5', 'MedSlot6', 'MedSlot7', 'RigSlot0', 'RigSlot1', 'RigSlot2', 'ServiceSlot0', 'ServiceSlot1', 'ServiceSlot2', 'ServiceSlot3', 'ServiceSlot4', 'ServiceSlot5', 'ServiceSlot6', 'ServiceSlot7', 'SubSystemSlot0', 'SubSystemSlot1', 'SubSystemSlot2', 'SubSystemSlot3']
    quantity: int
    type_id: int


class CharactersCharacterIdFittingsGetItem(BaseModel):
    description: str
    fitting_id: int
    items: list[CharactersCharacterIdFittingsGetItem_ItemsItem]
    name: str
    ship_type_id: int


CharactersCharacterIdFittingsGet = list[CharactersCharacterIdFittingsGetItem]


class CharactersCharacterIdFittingsPost(BaseModel):
    fitting_id: int


class CharactersCharacterIdFleetGet(BaseModel):
    fleet_boss_id: int
    fleet_id: int
    role: Literal['fleet_commander', 'squad_commander', 'squad_member', 'wing_commander']
    squad_id: int
    wing_id: int


class FleetsFleetIdGet(BaseModel):
    is_free_move: bool
    is_registered: bool
    is_voice_enabled: bool
    motd: str


class FleetsFleetIdMembersGetItem(BaseModel):
    character_id: int
    join_time: datetime
    role: Literal['fleet_commander', 'wing_commander', 'squad_commander', 'squad_member']
    role_name: str
    ship_type_id: int
    solar_system_id: int
    squad_id: int
    station_id: int | None
    takes_fleet_warp: bool
    wing_id: int


FleetsFleetIdMembersGet = list[FleetsFleetIdMembersGetItem]


class FleetsFleetIdWingsGetItem_SquadsItem(BaseModel):
    id: int
    name: str


class FleetsFleetIdWingsGetItem(BaseModel):
    id: int
    name: str
    squads: list[FleetsFleetIdWingsGetItem_SquadsItem]


FleetsFleetIdWingsGet = list[FleetsFleetIdWingsGetItem]


class FleetsFleetIdWingsPost(BaseModel):
    wing_id: int


class FleetsFleetIdWingsWingIdSquadsPost(BaseModel):
    squad_id: int


class FreelanceJobsDetailProgress(BaseModel):
    current: int
    desired: int


class FreelanceJobsDetailReward(BaseModel):
    initial: float
    remaining: float


class FreelanceJobsDetailFreelancejob(BaseModel):
    id: UUID
    last_modified: datetime
    name: str
    progress: FreelanceJobsDetailProgress
    reward: FreelanceJobsDetailReward | None
    state: Literal['Unspecified', 'Active', 'Closed', 'Completed', 'Expired', 'Deleted']


class CharactersFreelanceJobsListing(BaseModel):
    freelance_jobs: list[FreelanceJobsDetailFreelancejob]


class CharactersFreelanceJobsParticipation(BaseModel):
    contributed: int
    last_modified: datetime
    state: Literal['Unspecified', 'Committed', 'Kicked', 'Resigned']


class CorporationsFreelanceJobsListing(BaseModel):
    cursor: Cursor | None
    freelance_jobs: list[FreelanceJobsDetailFreelancejob]


class CorporationsFreelanceJobsParticipantsParticipant(BaseModel):
    contributed: int
    id: CharacterID
    name: str
    state: Literal['Unspecified', 'Committed', 'Kicked', 'Resigned']


class CorporationsFreelanceJobsParticipants(BaseModel):
    cursor: Cursor | None
    participants: list[CorporationsFreelanceJobsParticipantsParticipant]


class FreelanceJobsDetailBroadcastlocations(BaseModel):
    id: SolarSystemID
    name: str


class FreelanceJobsDetailRestrictions(BaseModel):
    maximum_age: int | None
    minimum_age: int | None


class FreelanceJobsDetailAccessandvisibility(BaseModel):
    acl_protected: bool
    broadcast_locations: list[FreelanceJobsDetailBroadcastlocations] | None
    restrictions: FreelanceJobsDetailRestrictions | None


class FreelanceJobsDetailParametermatchervalue(BaseModel):
    value_type: str
    values: list[str]


class FreelanceJobsDetailParametermatcher(BaseModel):
    values: list[FreelanceJobsDetailParametermatchervalue]


class FreelanceJobsDetailConfiguration_ParametersValueAlt0(BaseModel):
    matcher: FreelanceJobsDetailParametermatcher | None


class FreelanceJobsDetailParameteroptions(BaseModel):
    selected: list[str]


class FreelanceJobsDetailConfiguration_ParametersValueAlt1(BaseModel):
    options: FreelanceJobsDetailParameteroptions | None


class FreelanceJobsDetailParameterboolean(BaseModel):
    value: bool


class FreelanceJobsDetailConfiguration_ParametersValueAlt2(BaseModel):
    boolean: FreelanceJobsDetailParameterboolean | None


class FreelanceJobsDetailParametercorporationitemdelivery(BaseModel):
    corporation_office_location: FreelanceJobsDetailParametermatcher
    item_type: FreelanceJobsDetailParametermatcher


class FreelanceJobsDetailConfiguration_ParametersValueAlt3(BaseModel):
    corporation_item_delivery: FreelanceJobsDetailParametercorporationitemdelivery | None


class FreelanceJobsDetailConfiguration(BaseModel):
    method: str
    parameters: dict[str, FreelanceJobsDetailConfiguration_ParametersValueAlt0 | FreelanceJobsDetailConfiguration_ParametersValueAlt1 | FreelanceJobsDetailConfiguration_ParametersValueAlt2 | FreelanceJobsDetailConfiguration_ParametersValueAlt3]
    version: int


class FreelanceJobsDetailContribution(BaseModel):
    contribution_per_participant_limit: int | None
    max_committed_participants: int
    reward_per_contribution: float | None
    submission_limit: int | None
    submission_multiplier: float | None


class FreelanceJobsDetailCreatorcharacter(BaseModel):
    id: CharacterID
    name: str


class FreelanceJobsDetailCreatorcorporation(BaseModel):
    id: CorporationID
    name: str


class FreelanceJobsDetailCreator(BaseModel):
    character: FreelanceJobsDetailCreatorcharacter
    corporation: FreelanceJobsDetailCreatorcorporation


class FreelanceJobsDetailDetails(BaseModel):
    career: Literal['Unspecified', 'Explorer', 'Industrialist', 'Enforcer', 'Soldier of Fortune']
    created: datetime
    creator: FreelanceJobsDetailCreator
    description: str
    expires: datetime | None
    finished: datetime | None


class FreelanceJobsDetail(BaseModel):
    access_and_visibility: FreelanceJobsDetailAccessandvisibility
    configuration: FreelanceJobsDetailConfiguration
    contribution: FreelanceJobsDetailContribution | None
    details: FreelanceJobsDetailDetails
    id: UUID
    last_modified: datetime
    name: str
    progress: FreelanceJobsDetailProgress
    reward: FreelanceJobsDetailReward | None
    state: Literal['Unspecified', 'Active', 'Closed', 'Completed', 'Expired', 'Deleted']


class FreelanceJobsListing(BaseModel):
    cursor: Cursor | None
    freelance_jobs: list[FreelanceJobsDetailFreelancejob]


class IncursionsGetItem(BaseModel):
    constellation_id: int
    faction_id: int
    has_boss: bool
    infested_solar_systems: list[int]
    influence: float
    staging_solar_system_id: int
    state: Literal['withdrawing', 'mobilizing', 'established']
    type: str


IncursionsGet = list[IncursionsGetItem]


class CharactersCharacterIdIndustryJobsGetItem(BaseModel):
    activity_id: int
    blueprint_id: int
    blueprint_location_id: int
    blueprint_type_id: int
    completed_character_id: int | None
    completed_date: datetime | None
    cost: float | None
    duration: int
    end_date: datetime
    facility_id: int
    installer_id: int
    job_id: int
    licensed_runs: int | None
    output_location_id: int
    pause_date: datetime | None
    probability: float | None
    product_type_id: int | None
    runs: int
    start_date: datetime
    station_id: int
    status: Literal['active', 'cancelled', 'delivered', 'paused', 'ready', 'reverted']
    successful_runs: int | None


CharactersCharacterIdIndustryJobsGet = list[CharactersCharacterIdIndustryJobsGetItem]


class CharactersCharacterIdMiningGetItem(BaseModel):
    date: date
    quantity: int
    solar_system_id: int
    type_id: int


CharactersCharacterIdMiningGet = list[CharactersCharacterIdMiningGetItem]


class CorporationCorporationIdMiningExtractionsGetItem(BaseModel):
    chunk_arrival_time: datetime
    extraction_start_time: datetime
    moon_id: int
    natural_decay_time: datetime
    structure_id: int


CorporationCorporationIdMiningExtractionsGet = list[CorporationCorporationIdMiningExtractionsGetItem]


class CorporationCorporationIdMiningObserversGetItem(BaseModel):
    last_updated: date
    observer_id: int
    observer_type: Literal['structure']


CorporationCorporationIdMiningObserversGet = list[CorporationCorporationIdMiningObserversGetItem]


class CorporationCorporationIdMiningObserversObserverIdGetItem(BaseModel):
    character_id: int
    last_updated: date
    quantity: int
    recorded_corporation_id: int
    type_id: int


CorporationCorporationIdMiningObserversObserverIdGet = list[CorporationCorporationIdMiningObserversObserverIdGetItem]


class CorporationsCorporationIdIndustryJobsGetItem(BaseModel):
    activity_id: int
    blueprint_id: int
    blueprint_location_id: int
    blueprint_type_id: int
    completed_character_id: int | None
    completed_date: datetime | None
    cost: float | None
    duration: int
    end_date: datetime
    facility_id: int
    installer_id: int
    job_id: int
    licensed_runs: int | None
    location_id: int
    output_location_id: int
    pause_date: datetime | None
    probability: float | None
    product_type_id: int | None
    runs: int
    start_date: datetime
    status: Literal['active', 'cancelled', 'delivered', 'paused', 'ready', 'reverted']
    successful_runs: int | None


CorporationsCorporationIdIndustryJobsGet = list[CorporationsCorporationIdIndustryJobsGetItem]


class IndustryFacilitiesGetItem(BaseModel):
    facility_id: int
    owner_id: int
    region_id: int
    solar_system_id: int
    tax: float | None
    type_id: int


IndustryFacilitiesGet = list[IndustryFacilitiesGetItem]


class IndustrySystemsGetItem_Cost_indicesItem(BaseModel):
    activity: Literal['copying', 'duplicating', 'invention', 'manufacturing', 'none', 'reaction', 'researching_material_efficiency', 'researching_technology', 'researching_time_efficiency', 'reverse_engineering']
    cost_index: float


class IndustrySystemsGetItem(BaseModel):
    cost_indices: list[IndustrySystemsGetItem_Cost_indicesItem]
    solar_system_id: int


IndustrySystemsGet = list[IndustrySystemsGetItem]


class InsurancePricesGetItem_LevelsItem(BaseModel):
    cost: float
    name: str
    payout: float


class InsurancePricesGetItem(BaseModel):
    levels: list[InsurancePricesGetItem_LevelsItem]
    type_id: int


InsurancePricesGet = list[InsurancePricesGetItem]


class CharactersCharacterIdKillmailsRecentGetItem(BaseModel):
    killmail_hash: str
    killmail_id: int


CharactersCharacterIdKillmailsRecentGet = list[CharactersCharacterIdKillmailsRecentGetItem]


class CorporationsCorporationIdKillmailsRecentGetItem(BaseModel):
    killmail_hash: str
    killmail_id: int


CorporationsCorporationIdKillmailsRecentGet = list[CorporationsCorporationIdKillmailsRecentGetItem]


class KillmailsKillmailIdKillmailHashGet_AttackersItem(BaseModel):
    alliance_id: int | None
    character_id: int | None
    corporation_id: int | None
    damage_done: int
    faction_id: int | None
    final_blow: bool
    security_status: float
    ship_type_id: int | None
    weapon_type_id: int | None


class KillmailsKillmailIdKillmailHashGet_Victim_ItemsItem_ItemsItem(BaseModel):
    flag: int
    item_type_id: int
    quantity_destroyed: int | None
    quantity_dropped: int | None
    singleton: int


class KillmailsKillmailIdKillmailHashGet_Victim_ItemsItem(BaseModel):
    flag: int
    item_type_id: int
    items: list[KillmailsKillmailIdKillmailHashGet_Victim_ItemsItem_ItemsItem] | None
    quantity_destroyed: int | None
    quantity_dropped: int | None
    singleton: int


class KillmailsKillmailIdKillmailHashGet_Victim_Position(BaseModel):
    x: float
    y: float
    z: float


class KillmailsKillmailIdKillmailHashGet_Victim(BaseModel):
    alliance_id: int | None
    character_id: int | None
    corporation_id: int | None
    damage_taken: int
    faction_id: int | None
    items: list[KillmailsKillmailIdKillmailHashGet_Victim_ItemsItem] | None
    position: KillmailsKillmailIdKillmailHashGet_Victim_Position | None
    ship_type_id: int


class KillmailsKillmailIdKillmailHashGet(BaseModel):
    attackers: list[KillmailsKillmailIdKillmailHashGet_AttackersItem]
    killmail_id: int
    killmail_time: datetime
    moon_id: int | None
    solar_system_id: int
    victim: KillmailsKillmailIdKillmailHashGet_Victim
    war_id: int | None


class CharactersCharacterIdLocationGet(BaseModel):
    solar_system_id: int
    station_id: int | None
    structure_id: int | None


class CharactersCharacterIdOnlineGet(BaseModel):
    last_login: datetime | None
    last_logout: datetime | None
    logins: int | None
    online: bool


class CharactersCharacterIdShipGet(BaseModel):
    ship_item_id: int
    ship_name: str
    ship_type_id: int


class CharactersCharacterIdLoyaltyPointsGetItem(BaseModel):
    corporation_id: int
    loyalty_points: int


CharactersCharacterIdLoyaltyPointsGet = list[CharactersCharacterIdLoyaltyPointsGetItem]


class LoyaltyStoresCorporationIdOffersGetItem_Required_itemsItem(BaseModel):
    quantity: int
    type_id: int


class LoyaltyStoresCorporationIdOffersGetItem(BaseModel):
    ak_cost: int | None
    isk_cost: int
    lp_cost: int
    offer_id: int
    quantity: int
    required_items: list[LoyaltyStoresCorporationIdOffersGetItem_Required_itemsItem]
    type_id: int


LoyaltyStoresCorporationIdOffersGet = list[LoyaltyStoresCorporationIdOffersGetItem]


class CharactersCharacterIdMailGetItem_RecipientsItem(BaseModel):
    recipient_id: int
    recipient_type: Literal['alliance', 'character', 'corporation', 'mailing_list']


class CharactersCharacterIdMailGetItem(BaseModel):
    from_: Annotated[int | None, Field(alias='from')]
    is_read: bool | None
    labels: list[int] | None
    mail_id: int | None
    recipients: list[CharactersCharacterIdMailGetItem_RecipientsItem] | None
    subject: str | None
    timestamp: datetime | None


CharactersCharacterIdMailGet = list[CharactersCharacterIdMailGetItem]


class CharactersCharacterIdMailLabelsGet_LabelsItem(BaseModel):
    color: Literal['#0000fe', '#006634', '#0099ff', '#00ff33', '#01ffff', '#349800', '#660066', '#666666', '#999999', '#99ffff', '#9a0000', '#ccff9a', '#e6e6e6', '#fe0000', '#ff6600', '#ffff01', '#ffffcd', '#ffffff'] | None
    label_id: int | None
    name: str | None
    unread_count: int | None


class CharactersCharacterIdMailLabelsGet(BaseModel):
    labels: list[CharactersCharacterIdMailLabelsGet_LabelsItem] | None
    total_unread_count: int | None


class CharactersCharacterIdMailListsGetItem(BaseModel):
    mailing_list_id: int
    name: str


CharactersCharacterIdMailListsGet = list[CharactersCharacterIdMailListsGetItem]


class CharactersCharacterIdMailMailIdGet_RecipientsItem(BaseModel):
    recipient_id: int
    recipient_type: Literal['alliance', 'character', 'corporation', 'mailing_list']


class CharactersCharacterIdMailMailIdGet(BaseModel):
    body: str | None
    from_: Annotated[int | None, Field(alias='from')]
    labels: list[int] | None
    read: bool | None
    recipients: list[CharactersCharacterIdMailMailIdGet_RecipientsItem] | None
    subject: str | None
    timestamp: datetime | None


CharactersCharacterIdMailPost = int


CharactersCharacterIdMailLabelsPost = int


class CharactersCharacterIdOrdersGetItem(BaseModel):
    duration: int
    escrow: float | None
    is_buy_order: bool | None
    is_corporation: bool
    issued: datetime
    location_id: int
    min_volume: int | None
    order_id: int
    price: float
    range: Literal['1', '10', '2', '20', '3', '30', '4', '40', '5', 'region', 'solarsystem', 'station']
    region_id: int
    type_id: int
    volume_remain: int
    volume_total: int


CharactersCharacterIdOrdersGet = list[CharactersCharacterIdOrdersGetItem]


class CharactersCharacterIdOrdersHistoryGetItem(BaseModel):
    duration: int
    escrow: float | None
    is_buy_order: bool | None
    is_corporation: bool
    issued: datetime
    location_id: int
    min_volume: int | None
    order_id: int
    price: float
    range: Literal['1', '10', '2', '20', '3', '30', '4', '40', '5', 'region', 'solarsystem', 'station']
    region_id: int
    state: Literal['cancelled', 'expired']
    type_id: int
    volume_remain: int
    volume_total: int


CharactersCharacterIdOrdersHistoryGet = list[CharactersCharacterIdOrdersHistoryGetItem]


class CorporationsCorporationIdOrdersGetItem(BaseModel):
    duration: int
    escrow: float | None
    is_buy_order: bool | None
    issued: datetime
    issued_by: int
    location_id: int
    min_volume: int | None
    order_id: int
    price: float
    range: Literal['1', '10', '2', '20', '3', '30', '4', '40', '5', 'region', 'solarsystem', 'station']
    region_id: int
    type_id: int
    volume_remain: int
    volume_total: int
    wallet_division: int


CorporationsCorporationIdOrdersGet = list[CorporationsCorporationIdOrdersGetItem]


class CorporationsCorporationIdOrdersHistoryGetItem(BaseModel):
    duration: int
    escrow: float | None
    is_buy_order: bool | None
    issued: datetime
    issued_by: int | None
    location_id: int
    min_volume: int | None
    order_id: int
    price: float
    range: Literal['1', '10', '2', '20', '3', '30', '4', '40', '5', 'region', 'solarsystem', 'station']
    region_id: int
    state: Literal['cancelled', 'expired']
    type_id: int
    volume_remain: int
    volume_total: int
    wallet_division: int


CorporationsCorporationIdOrdersHistoryGet = list[CorporationsCorporationIdOrdersHistoryGetItem]


MarketsGroupsGet = list[int]


class MarketsGroupsMarketGroupIdGet(BaseModel):
    description: str
    market_group_id: int
    name: str
    parent_group_id: int | None
    types: list[int]


class MarketsPricesGetItem(BaseModel):
    adjusted_price: float | None
    average_price: float | None
    type_id: int


MarketsPricesGet = list[MarketsPricesGetItem]


class MarketsRegionIdHistoryGetItem(BaseModel):
    average: float
    date: date
    highest: float
    lowest: float
    order_count: int
    volume: int


MarketsRegionIdHistoryGet = list[MarketsRegionIdHistoryGetItem]


class MarketsRegionIdOrdersGetItem(BaseModel):
    duration: int
    is_buy_order: bool
    issued: datetime
    location_id: int
    min_volume: int
    order_id: int
    price: float
    range: Literal['station', 'region', 'solarsystem', '1', '2', '3', '4', '5', '10', '20', '30', '40']
    system_id: int
    type_id: int
    volume_remain: int
    volume_total: int


MarketsRegionIdOrdersGet = list[MarketsRegionIdOrdersGetItem]


MarketsRegionIdTypesGet = list[int]


class MarketsStructuresStructureIdGetItem(BaseModel):
    duration: int
    is_buy_order: bool
    issued: datetime
    location_id: int
    min_volume: int
    order_id: int
    price: float
    range: Literal['station', 'region', 'solarsystem', '1', '2', '3', '4', '5', '10', '20', '30', '40']
    type_id: int
    volume_remain: int
    volume_total: int


MarketsStructuresStructureIdGet = list[MarketsStructuresStructureIdGetItem]


CompatibilityDate = date


class MetaChangelogEntry(BaseModel):
    compatibility_date: CompatibilityDate
    description: str
    method: Literal['GET', 'POST', 'PUT', 'DELETE']
    path: str
    type: Literal['breaking', 'changed', 'new', 'removed']


class MetaChangelog(BaseModel):
    changelog: dict[str, list[MetaChangelogEntry]]


class MetaCompatibilityDates(BaseModel):
    compatibility_dates: list[CompatibilityDate]


class MetaNameEntry(BaseModel):
    date: str
    name: str


class MetaName(BaseModel):
    current: str
    history: list[MetaNameEntry]


class MetaStatusRoutestatus(BaseModel):
    method: Literal['GET', 'POST', 'PUT', 'DELETE']
    path: str
    status: Literal['Unknown', 'OK', 'Degraded', 'Down', 'Recovering']


class MetaStatus(BaseModel):
    routes: list[MetaStatusRoutestatus]


class CharactersMilitaryCampaignsObjectivesParticipationCharacterobjective(BaseModel):
    campaign_id: UUID
    contributed: int
    id: UUID
    is_committed: bool
    last_modified: datetime


class CharactersMilitaryCampaignsObjectivesListing(BaseModel):
    cursor: Cursor | None
    objectives: list[CharactersMilitaryCampaignsObjectivesParticipationCharacterobjective]


class CharactersMilitaryCampaignsObjectivesParticipation(BaseModel):
    campaign_id: UUID
    contributed: int
    id: UUID
    is_committed: bool
    last_modified: datetime


class MilitaryCampaignsDetail(BaseModel):
    finished: datetime | None
    id: UUID
    progress: int
    started: datetime | None
    state: Literal['Unspecified', 'Active', 'Completed', 'Expired']


class MilitaryCampaignsDetailCampaign(BaseModel):
    finished: datetime | None
    id: UUID
    progress: int
    started: datetime | None
    state: Literal['Unspecified', 'Active', 'Completed', 'Expired']


class MilitaryCampaignsListing(BaseModel):
    campaigns: list[MilitaryCampaignsDetailCampaign]


class MilitaryCampaignsObjectivesDetailParticipants(BaseModel):
    committed: int
    contributors: int
    total: int


class MilitaryCampaignsObjectivesDetail(BaseModel):
    finished: datetime | None
    id: UUID
    last_modified: datetime
    participants: MilitaryCampaignsObjectivesDetailParticipants
    progress: int
    started: datetime | None
    state: Literal['Unspecified', 'Active', 'Completed', 'Expired']


class MilitaryCampaignsObjectivesDetailObjective(BaseModel):
    finished: datetime | None
    id: UUID
    last_modified: datetime
    participants: MilitaryCampaignsObjectivesDetailParticipants
    progress: int
    started: datetime | None
    state: Literal['Unspecified', 'Active', 'Completed', 'Expired']


class MilitaryCampaignsObjectivesListing(BaseModel):
    cursor: Cursor | None
    objectives: list[MilitaryCampaignsObjectivesDetailObjective]


class CharactersCharacterIdPlanetsGetItem(BaseModel):
    last_update: datetime
    num_pins: int
    owner_id: int
    planet_id: int
    planet_type: Literal['temperate', 'barren', 'oceanic', 'ice', 'gas', 'lava', 'storm', 'plasma']
    solar_system_id: int
    upgrade_level: int


CharactersCharacterIdPlanetsGet = list[CharactersCharacterIdPlanetsGetItem]


class CharactersCharacterIdPlanetsPlanetIdGet_LinksItem(BaseModel):
    destination_pin_id: int
    link_level: int
    source_pin_id: int


class CharactersCharacterIdPlanetsPlanetIdGet_PinsItem_ContentsItem(BaseModel):
    amount: int
    type_id: int


class CharactersCharacterIdPlanetsPlanetIdGet_PinsItem_Extractor_details_HeadsItem(BaseModel):
    head_id: int
    latitude: float
    longitude: float


class CharactersCharacterIdPlanetsPlanetIdGet_PinsItem_Extractor_details(BaseModel):
    cycle_time: int | None
    head_radius: float | None
    heads: list[CharactersCharacterIdPlanetsPlanetIdGet_PinsItem_Extractor_details_HeadsItem]
    product_type_id: int | None
    qty_per_cycle: int | None


class CharactersCharacterIdPlanetsPlanetIdGet_PinsItem_Factory_details(BaseModel):
    schematic_id: int


class CharactersCharacterIdPlanetsPlanetIdGet_PinsItem(BaseModel):
    contents: list[CharactersCharacterIdPlanetsPlanetIdGet_PinsItem_ContentsItem] | None
    expiry_time: datetime | None
    extractor_details: CharactersCharacterIdPlanetsPlanetIdGet_PinsItem_Extractor_details | None
    factory_details: CharactersCharacterIdPlanetsPlanetIdGet_PinsItem_Factory_details | None
    install_time: datetime | None
    last_cycle_start: datetime | None
    latitude: float
    longitude: float
    pin_id: int
    schematic_id: int | None
    type_id: int


class CharactersCharacterIdPlanetsPlanetIdGet_RoutesItem(BaseModel):
    content_type_id: int
    destination_pin_id: int
    quantity: float
    route_id: int
    source_pin_id: int
    waypoints: list[int] | None


class CharactersCharacterIdPlanetsPlanetIdGet(BaseModel):
    links: list[CharactersCharacterIdPlanetsPlanetIdGet_LinksItem]
    pins: list[CharactersCharacterIdPlanetsPlanetIdGet_PinsItem]
    routes: list[CharactersCharacterIdPlanetsPlanetIdGet_RoutesItem]


class CorporationsCorporationIdCustomsOfficesGetItem(BaseModel):
    alliance_tax_rate: float | None
    allow_access_with_standings: bool
    allow_alliance_access: bool
    bad_standing_tax_rate: float | None
    corporation_tax_rate: float | None
    excellent_standing_tax_rate: float | None
    good_standing_tax_rate: float | None
    neutral_standing_tax_rate: float | None
    office_id: int
    reinforce_exit_end: int
    reinforce_exit_start: int
    standing_level: Literal['bad', 'excellent', 'good', 'neutral', 'terrible'] | None
    system_id: int
    terrible_standing_tax_rate: float | None
    type_id: int | None


CorporationsCorporationIdCustomsOfficesGet = list[CorporationsCorporationIdCustomsOfficesGetItem]


class UniverseSchematicsSchematicIdGet(BaseModel):
    cycle_time: int
    schematic_name: str


class CharactersCharacterIdSearchGet(BaseModel):
    agent: list[int] | None
    alliance: list[int] | None
    character: list[int] | None
    constellation: list[int] | None
    corporation: list[int] | None
    faction: list[int] | None
    inventory_type: list[int] | None
    region: list[int] | None
    solar_system: list[int] | None
    station: list[int] | None
    structure: list[int] | None


class CharactersCharacterIdAttributesGet(BaseModel):
    accrued_remap_cooldown_date: datetime | None
    bonus_remaps: int | None
    charisma: int
    intelligence: int
    last_remap_date: datetime | None
    memory: int
    perception: int
    willpower: int


class CharactersSkillqueueSkill(BaseModel):
    finish_date: datetime | None
    finished_level: int
    level_end_sp: int | None
    level_start_sp: int | None
    queue_position: int
    skill_id: TypeID
    start_date: datetime | None
    training_start_sp: int | None


class CharactersSkillsSkill(BaseModel):
    active_skill_level: int
    skill_id: int
    skillpoints_in_skill: int
    trained_skill_level: int


class CharactersSkills(BaseModel):
    skills: list[CharactersSkillsSkill]
    total_sp: int
    unallocated_sp: int | None


class SovereigntyCampaignsGetItem_ParticipantsItem(BaseModel):
    alliance_id: int
    score: float


class SovereigntyCampaignsGetItem(BaseModel):
    attackers_score: float | None
    campaign_id: int
    constellation_id: int
    defender_id: int | None
    defender_score: float | None
    event_type: Literal['tcu_defense', 'ihub_defense', 'station_defense', 'station_freeport']
    participants: list[SovereigntyCampaignsGetItem_ParticipantsItem] | None
    solar_system_id: int
    start_time: datetime
    structure_id: int


SovereigntyCampaignsGet = list[SovereigntyCampaignsGetItem]


class SovereigntySystemsFaction(BaseModel):
    faction_id: FactionID


class SovereigntySystemsSolarsystem_ClaimAlt0(BaseModel):
    faction: SovereigntySystemsFaction | None


class SovereigntySystemsDevelopment(BaseModel):
    activity_defense_multiplier: float
    industrial_level: int
    military_level: int
    strategic_level: int


class SovereigntySystemsVulnerabilitywindow(BaseModel):
    end: datetime
    start: datetime


class SovereigntySystemsSovereigntyhub(BaseModel):
    id: ItemID
    vulnerability_window: SovereigntySystemsVulnerabilitywindow | None


class SovereigntySystemsAlliance(BaseModel):
    alliance_id: AllianceID
    claimed_since: datetime
    corporation_id: CorporationID
    development: SovereigntySystemsDevelopment
    is_capital_system: bool
    sovereignty_hub: SovereigntySystemsSovereigntyhub


class SovereigntySystemsSolarsystem_ClaimAlt1(BaseModel):
    alliance: SovereigntySystemsAlliance | None


class SovereigntySystemsSolarsystem_ClaimAlt2(BaseModel):
    unclaimed: bool | None


class SovereigntySystemsSolarsystem(BaseModel):
    claim: SovereigntySystemsSolarsystem_ClaimAlt0 | SovereigntySystemsSolarsystem_ClaimAlt1 | SovereigntySystemsSolarsystem_ClaimAlt2
    solar_system_id: SolarSystemID


class SovereigntySystems(BaseModel):
    solar_systems: list[SovereigntySystemsSolarsystem]


class StatusGet(BaseModel):
    players: int
    server_version: str
    start_time: datetime
    vip: bool | None


class CharactersStructuresMercenaryDensDetailEvolutionanarchy(BaseModel):
    amount: int
    level: Literal['Unspecified', 'Level0', 'Level1', 'Level2', 'Level3', 'Level4']


class CharactersStructuresMercenaryDensDetailEvolutiondevelopment(BaseModel):
    amount: int
    level: Literal['Unspecified', 'Level0', 'Level1', 'Level2', 'Level3', 'Level4']


class CharactersStructuresMercenaryDensDetailEvolution(BaseModel):
    anarchy: CharactersStructuresMercenaryDensDetailEvolutionanarchy
    development: CharactersStructuresMercenaryDensDetailEvolutiondevelopment


class CharactersStructuresMercenaryDensDetailInfomorphs(BaseModel):
    amount: int


class CharactersStructuresMercenaryDensDetailReinforcementtimer(BaseModel):
    end: datetime


class CharactersStructuresMercenaryDensDetailSkyhook(BaseModel):
    corporation_id: CorporationID
    id: ItemID
    planet_id: PlanetID


class CharactersStructuresMercenaryDensDetail(BaseModel):
    evolution: CharactersStructuresMercenaryDensDetailEvolution
    id: ItemID
    infomorphs: CharactersStructuresMercenaryDensDetailInfomorphs
    reinforcement_timer: CharactersStructuresMercenaryDensDetailReinforcementtimer | None
    skyhook: CharactersStructuresMercenaryDensDetailSkyhook
    state: Literal['Unspecified', 'Running', 'Paused', 'Disabled']
    type_id: TypeID


class CharactersStructuresMercenaryDensListingMercenaryden(BaseModel):
    id: ItemID
    planet_id: PlanetID


class CharactersStructuresMercenaryDensListing(BaseModel):
    mercenary_dens: list[CharactersStructuresMercenaryDensListingMercenaryden]


class CorporationsStructuresSkyhooksDetailReagent(BaseModel):
    last_cycle: datetime
    secured_stock: int
    type_id: TypeID
    unsecured_stock: int


class CorporationsStructuresSkyhooksDetailReinforcementtimer(BaseModel):
    end: datetime


class CorporationsStructuresSkyhooksDetailTheftvulnerability(BaseModel):
    end: datetime
    start: datetime


class CorporationsStructuresSkyhooksDetail(BaseModel):
    effective_workforce: int | None
    id: ItemID
    is_active: bool
    planet_id: PlanetID
    reagents: list[CorporationsStructuresSkyhooksDetailReagent] | None
    reinforcement_timer: CorporationsStructuresSkyhooksDetailReinforcementtimer | None
    state: Literal['Unspecified', 'ShieldVulnerable', 'ArmorReinforced', 'ArmorVulnerable', 'HullReinforced', 'HullVulnerable']
    theft_vulnerability: CorporationsStructuresSkyhooksDetailTheftvulnerability | None


class CorporationsStructuresSkyhooksListingSkyhook(BaseModel):
    id: ItemID
    planet_id: PlanetID


class CorporationsStructuresSkyhooksListing(BaseModel):
    skyhooks: list[CorporationsStructuresSkyhooksListingSkyhook]


class CorporationsStructuresSovereigntyHubsDetailReagent(BaseModel):
    amount: int
    burning_per_hour: int
    type_id: TypeID


class CorporationsStructuresSovereigntyHubsDetailReagentbay(BaseModel):
    last_updated: datetime
    reagents: list[CorporationsStructuresSovereigntyHubsDetailReagent]


class CorporationsStructuresSovereigntyHubsDetailResourcepower(BaseModel):
    allocated: int
    available: int


class CorporationsStructuresSovereigntyHubsDetailResourceworkforce(BaseModel):
    allocated: int
    available: int


class CorporationsStructuresSovereigntyHubsDetailResources(BaseModel):
    power: CorporationsStructuresSovereigntyHubsDetailResourcepower
    workforce: CorporationsStructuresSovereigntyHubsDetailResourceworkforce


class CorporationsStructuresSovereigntyHubsDetailUpgrade(BaseModel):
    power_state: Literal['Unspecified', 'Online', 'Offline', 'Low', 'Pending']
    type_id: TypeID


class CorporationsStructuresSovereigntyHubsDetailVulnerabilitywindow(BaseModel):
    end: datetime
    start: datetime


class CorporationsStructuresSovereigntyHubsDetailTransportconfigurationsource(BaseModel):
    solar_system_id: SolarSystemID


class CorporationsStructuresSovereigntyHubsDetailTransportconfigurationimport(BaseModel):
    sources: list[CorporationsStructuresSovereigntyHubsDetailTransportconfigurationsource]


class CorporationsStructuresSovereigntyHubsDetailTransport_ConfigurationAlt0(BaseModel):
    import_: Annotated[CorporationsStructuresSovereigntyHubsDetailTransportconfigurationimport | None, Field(alias='import')]


class CorporationsStructuresSovereigntyHubsDetailTransportconfigurationexport(BaseModel):
    amount: int
    solar_system_id: SolarSystemID | None


class CorporationsStructuresSovereigntyHubsDetailTransport_ConfigurationAlt1(BaseModel):
    export: CorporationsStructuresSovereigntyHubsDetailTransportconfigurationexport | None


class CorporationsStructuresSovereigntyHubsDetailTransport_ConfigurationAlt2(BaseModel):
    transit: bool | None | None


class CorporationsStructuresSovereigntyHubsDetailTransportstateimportsource(BaseModel):
    amount: int
    solar_system_id: SolarSystemID


class CorporationsStructuresSovereigntyHubsDetailTransportstateimport(BaseModel):
    sources: list[CorporationsStructuresSovereigntyHubsDetailTransportstateimportsource]


class CorporationsStructuresSovereigntyHubsDetailTransport_StateAlt0(BaseModel):
    import_: Annotated[CorporationsStructuresSovereigntyHubsDetailTransportstateimport | None, Field(alias='import')]


class CorporationsStructuresSovereigntyHubsDetailTransportstateexport(BaseModel):
    amount: int | None
    solar_system_id: SolarSystemID | None


class CorporationsStructuresSovereigntyHubsDetailTransport_StateAlt1(BaseModel):
    export: CorporationsStructuresSovereigntyHubsDetailTransportstateexport | None


class CorporationsStructuresSovereigntyHubsDetailTransport_StateAlt2(BaseModel):
    transit: bool | None | None


class CorporationsStructuresSovereigntyHubsDetailTransport(BaseModel):
    configuration: CorporationsStructuresSovereigntyHubsDetailTransport_ConfigurationAlt0 | CorporationsStructuresSovereigntyHubsDetailTransport_ConfigurationAlt1 | CorporationsStructuresSovereigntyHubsDetailTransport_ConfigurationAlt2
    state: CorporationsStructuresSovereigntyHubsDetailTransport_StateAlt0 | CorporationsStructuresSovereigntyHubsDetailTransport_StateAlt1 | CorporationsStructuresSovereigntyHubsDetailTransport_StateAlt2


class CorporationsStructuresSovereigntyHubsDetail(BaseModel):
    fuel_access_list_id: AccessListID | None
    id: ItemID
    reagent_bay: CorporationsStructuresSovereigntyHubsDetailReagentbay
    resources: CorporationsStructuresSovereigntyHubsDetailResources
    solar_system_id: SolarSystemID
    upgrades: list[CorporationsStructuresSovereigntyHubsDetailUpgrade]
    vulnerability_window: CorporationsStructuresSovereigntyHubsDetailVulnerabilitywindow | None
    workforce_transport: CorporationsStructuresSovereigntyHubsDetailTransport


class CorporationsStructuresSovereigntyHubsListingSovereigntyhub(BaseModel):
    id: ItemID
    solar_system_id: SolarSystemID


class CorporationsStructuresSovereigntyHubsListing(BaseModel):
    sovereignty_hubs: list[CorporationsStructuresSovereigntyHubsListingSovereigntyhub]


class UniverseAncestriesGetItem(BaseModel):
    bloodline_id: int
    description: str
    icon_id: int | None
    id: int
    name: str
    short_description: str | None


UniverseAncestriesGet = list[UniverseAncestriesGetItem]


class UniverseAsteroidBeltsAsteroidBeltIdGet_Position(BaseModel):
    x: float
    y: float
    z: float


class UniverseAsteroidBeltsAsteroidBeltIdGet(BaseModel):
    name: str
    position: UniverseAsteroidBeltsAsteroidBeltIdGet_Position
    system_id: int


class UniverseBloodlinesGetItem(BaseModel):
    bloodline_id: int
    charisma: int
    corporation_id: int
    description: str
    intelligence: int
    memory: int
    name: str
    perception: int
    race_id: int
    ship_type_id: int | None
    willpower: int


UniverseBloodlinesGet = list[UniverseBloodlinesGetItem]


UniverseCategoriesGet = list[int]


class UniverseCategoriesCategoryIdGet(BaseModel):
    category_id: int
    groups: list[int]
    name: str
    published: bool


UniverseConstellationsGet = list[int]


class UniverseConstellationsConstellationIdGet_Position(BaseModel):
    x: float
    y: float
    z: float


class UniverseConstellationsConstellationIdGet(BaseModel):
    constellation_id: int
    name: str
    position: UniverseConstellationsConstellationIdGet_Position
    region_id: int
    systems: list[int]


class UniverseFactionsGetItem(BaseModel):
    corporation_id: int | None
    description: str
    faction_id: int
    is_unique: bool
    militia_corporation_id: int | None
    name: str
    size_factor: float
    solar_system_id: int | None
    station_count: int
    station_system_count: int


UniverseFactionsGet = list[UniverseFactionsGetItem]


UniverseGraphicsGet = list[int]


class UniverseGraphicsGraphicIdGet(BaseModel):
    collision_file: str | None
    graphic_file: str | None
    graphic_id: int
    icon_folder: str | None
    sof_dna: str | None
    sof_fation_name: str | None
    sof_hull_name: str | None
    sof_race_name: str | None


UniverseGroupsGet = list[int]


class UniverseGroupsGroupIdGet(BaseModel):
    category_id: int
    group_id: int
    name: str
    published: bool
    types: list[int]


class UniverseMoonsMoonIdGet_Position(BaseModel):
    x: float
    y: float
    z: float


class UniverseMoonsMoonIdGet(BaseModel):
    moon_id: int
    name: str
    position: UniverseMoonsMoonIdGet_Position
    system_id: int


class UniversePlanetsPlanetIdGet_Position(BaseModel):
    x: float
    y: float
    z: float


class UniversePlanetsPlanetIdGet(BaseModel):
    name: str
    planet_id: int
    position: UniversePlanetsPlanetIdGet_Position
    system_id: int
    type_id: int


class UniverseRacesGetItem(BaseModel):
    alliance_id: int
    description: str
    name: str
    race_id: int


UniverseRacesGet = list[UniverseRacesGetItem]


UniverseRegionsGet = list[int]


class UniverseRegionsRegionIdGet(BaseModel):
    constellations: list[int]
    description: str | None
    name: str
    region_id: int


class UniverseStargatesStargateIdGet_Destination(BaseModel):
    stargate_id: int
    system_id: int


class UniverseStargatesStargateIdGet_Position(BaseModel):
    x: float
    y: float
    z: float


class UniverseStargatesStargateIdGet(BaseModel):
    destination: UniverseStargatesStargateIdGet_Destination
    name: str
    position: UniverseStargatesStargateIdGet_Position
    stargate_id: int
    system_id: int
    type_id: int


class UniverseStarsStarIdGet(BaseModel):
    age: int
    luminosity: float
    name: str
    radius: int
    solar_system_id: int
    spectral_class: Literal['K2 V', 'K4 V', 'G2 V', 'G8 V', 'M7 V', 'K7 V', 'M2 V', 'K5 V', 'M3 V', 'G0 V', 'G7 V', 'G3 V', 'F9 V', 'G5 V', 'F6 V', 'K8 V', 'K9 V', 'K6 V', 'G9 V', 'G6 V', 'G4 VI', 'G4 V', 'F8 V', 'F2 V', 'F1 V', 'K3 V', 'F0 VI', 'G1 VI', 'G0 VI', 'K1 V', 'M4 V', 'M1 V', 'M6 V', 'M0 V', 'K2 IV', 'G2 VI', 'K0 V', 'K5 IV', 'F5 VI', 'G6 VI', 'F6 VI', 'F2 IV', 'G3 VI', 'M8 V', 'F1 VI', 'K1 IV', 'F7 V', 'G5 VI', 'M5 V', 'G7 VI', 'F5 V', 'F4 VI', 'F8 VI', 'K3 IV', 'F4 IV', 'F0 V', 'G7 IV', 'G8 VI', 'F2 VI', 'F4 V', 'F7 VI', 'F3 V', 'G1 V', 'G9 VI', 'F3 IV', 'F9 VI', 'M9 V', 'K0 IV', 'F1 IV', 'G4 IV', 'F3 VI', 'K4 IV', 'G5 IV', 'G3 IV', 'G1 IV', 'K7 IV', 'G0 IV', 'K6 IV', 'K9 IV', 'G2 IV', 'F9 IV', 'F0 IV', 'K8 IV', 'G8 IV', 'F6 IV', 'F5 IV', 'A0', 'A0IV', 'A0IV2']
    temperature: int
    type_id: int


class UniverseStationsStationIdGet_Position(BaseModel):
    x: float
    y: float
    z: float


class UniverseStationsStationIdGet(BaseModel):
    max_dockable_ship_volume: float
    name: str
    office_rental_cost: float
    owner: int | None
    position: UniverseStationsStationIdGet_Position
    race_id: int | None
    reprocessing_efficiency: float
    reprocessing_stations_take: float
    services: list[Literal['bounty-missions', 'assasination-missions', 'courier-missions', 'interbus', 'reprocessing-plant', 'refinery', 'market', 'black-market', 'stock-exchange', 'cloning', 'surgery', 'dna-therapy', 'repair-facilities', 'factory', 'labratory', 'gambling', 'fitting', 'paintshop', 'news', 'storage', 'insurance', 'docking', 'office-rental', 'jump-clone-facility', 'loyalty-point-store', 'navy-offices', 'security-offices']]
    station_id: int
    system_id: int
    type_id: int


UniverseStructuresGet = list[int]


class UniverseStructuresStructureIdGet_Position(BaseModel):
    x: float
    y: float
    z: float


class UniverseStructuresStructureIdGet(BaseModel):
    name: str
    owner_id: int
    position: UniverseStructuresStructureIdGet_Position | None
    solar_system_id: int
    type_id: int | None


class UniverseSystemJumpsGetItem(BaseModel):
    ship_jumps: int
    system_id: int


UniverseSystemJumpsGet = list[UniverseSystemJumpsGetItem]


class UniverseSystemKillsGetItem(BaseModel):
    npc_kills: int
    pod_kills: int
    ship_kills: int
    system_id: int


UniverseSystemKillsGet = list[UniverseSystemKillsGetItem]


UniverseSystemsGet = list[int]


class UniverseSystemsSystemIdGet_PlanetsItem(BaseModel):
    asteroid_belts: list[int] | None
    moons: list[int] | None
    planet_id: int


class UniverseSystemsSystemIdGet_Position(BaseModel):
    x: float
    y: float
    z: float


class UniverseSystemsSystemIdGet(BaseModel):
    constellation_id: int
    name: str
    planets: list[UniverseSystemsSystemIdGet_PlanetsItem] | None
    position: UniverseSystemsSystemIdGet_Position
    security_class: str | None
    security_status: float
    star_id: int | None
    stargates: list[int] | None
    stations: list[int] | None
    system_id: int


UniverseTypesGet = list[int]


class UniverseTypesTypeIdGet_Dogma_attributesItem(BaseModel):
    attribute_id: int
    value: float


class UniverseTypesTypeIdGet_Dogma_effectsItem(BaseModel):
    effect_id: int
    is_default: bool


class UniverseTypesTypeIdGet(BaseModel):
    capacity: float | None
    description: str
    dogma_attributes: list[UniverseTypesTypeIdGet_Dogma_attributesItem] | None
    dogma_effects: list[UniverseTypesTypeIdGet_Dogma_effectsItem] | None
    graphic_id: int | None
    group_id: int
    icon_id: int | None
    market_group_id: int | None
    mass: float | None
    name: str
    packaged_volume: float | None
    portion_size: int | None
    published: bool
    radius: float | None
    type_id: int
    volume: float | None


CharactersCharacterIdWalletGet = float


class CharactersCharacterIdWalletJournalGetItem(BaseModel):
    amount: float | None
    balance: float | None
    context_id: int | None
    context_id_type: Literal['structure_id', 'station_id', 'market_transaction_id', 'character_id', 'corporation_id', 'alliance_id', 'eve_system', 'industry_job_id', 'contract_id', 'planet_id', 'system_id', 'type_id'] | None
    date: datetime
    description: str
    first_party_id: int | None
    id: int
    reason: str | None
    ref_type: Literal['acceleration_gate_fee', 'achievement_category_milestone_reward', 'achievement_milestone_reward', 'advertisement_listing_fee', 'agent_donation', 'agent_location_services', 'agent_miscellaneous', 'agent_mission_collateral_paid', 'agent_mission_collateral_refunded', 'agent_mission_reward', 'agent_mission_reward_corporation_tax', 'agent_mission_security_tax', 'agent_mission_time_bonus_reward', 'agent_mission_time_bonus_reward_corporation_tax', 'agent_security_services', 'agent_services_rendered', 'agents_preward', 'air_career_program_reward', 'alliance_maintainance_fee', 'alliance_registration_fee', 'allignment_based_gate_toll', 'asset_safety_recovery_tax', 'bounty', 'bounty_prize', 'bounty_prize_corporation_tax', 'bounty_prizes', 'bounty_reimbursement', 'bounty_surcharge', 'brokers_fee', 'campaign_objective_isk_reward', 'clone_activation', 'clone_transfer', 'contraband_fine', 'contract_auction_bid', 'contract_auction_bid_corp', 'contract_auction_bid_refund', 'contract_auction_sold', 'contract_brokers_fee', 'contract_brokers_fee_corp', 'contract_collateral', 'contract_collateral_deposited_corp', 'contract_collateral_payout', 'contract_collateral_refund', 'contract_deposit', 'contract_deposit_corp', 'contract_deposit_refund', 'contract_deposit_sales_tax', 'contract_price', 'contract_price_payment_corp', 'contract_reversal', 'contract_reward', 'contract_reward_deposited', 'contract_reward_deposited_corp', 'contract_reward_refund', 'contract_sales_tax', 'copying', 'corporate_reward_payout', 'corporate_reward_tax', 'corporation_account_withdrawal', 'corporation_bulk_payment', 'corporation_dividend_payment', 'corporation_liquidation', 'corporation_logo_change_cost', 'corporation_payment', 'corporation_registration_fee', 'cosmetic_market_component_item_purchase', 'cosmetic_market_skin_purchase', 'cosmetic_market_skin_sale', 'cosmetic_market_skin_sale_broker_fee', 'cosmetic_market_skin_sale_tax', 'cosmetic_market_skin_transaction', 'courier_mission_escrow', 'cspa', 'cspaofflinerefund', 'daily_challenge_reward', 'daily_goal_payouts', 'daily_goal_payouts_tax', 'datacore_fee', 'dna_modification_fee', 'docking_fee', 'duel_wager_escrow', 'duel_wager_payment', 'duel_wager_refund', 'ess_escrow_transfer', 'external_trade_delivery', 'external_trade_freeze', 'external_trade_thaw', 'factory_slot_rental_fee', 'flux_payout', 'flux_tax', 'flux_ticket_repayment', 'flux_ticket_sale', 'freelance_jobs_broadcasting_fee', 'freelance_jobs_duration_fee', 'freelance_jobs_escrow_refund', 'freelance_jobs_reward', 'freelance_jobs_reward_corporation_tax', 'freelance_jobs_reward_escrow', 'gm_cash_transfer', 'gm_plex_fee_refund', 'industry_job_tax', 'industry_security_tax', 'infrastructure_hub_maintenance', 'inheritance', 'insurance', 'insurgency_corruption_contribution_reward', 'insurgency_suppression_contribution_reward', 'item_trader_payment', 'jump_clone_activation_fee', 'jump_clone_installation_fee', 'kill_right_fee', 'lp_store', 'manufacturing', 'market_escrow', 'market_fine_paid', 'market_provider_tax', 'market_security_tax', 'market_transaction', 'medal_creation', 'medal_issued', 'milestone_reward_payment', 'mission_completion', 'mission_cost', 'mission_expiration', 'mission_reward', 'npc_bounty_security_tax', 'office_rental_fee', 'operation_bonus', 'opportunity_reward', 'planetary_construction', 'planetary_export_tax', 'planetary_import_tax', 'player_donation', 'player_trading', 'project_discovery_reward', 'project_discovery_tax', 'project_payouts', 'reaction', 'redeemed_isk_token', 'release_of_impounded_property', 'repair_bill', 'reprocessing_tax', 'researching_material_productivity', 'researching_technology', 'researching_time_productivity', 'resource_wars_reward', 'reverse_engineering', 'season_challenge_reward', 'security_processing_fee', 'shares', 'skill_purchase', 'skyhook_claim_fee', 'sovereignity_bill', 'store_purchase', 'store_purchase_refund', 'structure_gate_jump', 'transaction_tax', 'under_construction', 'upkeep_adjustment_fee', 'war_ally_contract', 'war_fee', 'war_fee_surrender']
    second_party_id: int | None
    tax: float | None
    tax_receiver_id: int | None


CharactersCharacterIdWalletJournalGet = list[CharactersCharacterIdWalletJournalGetItem]


class CharactersCharacterIdWalletTransactionsGetItem(BaseModel):
    client_id: int
    date: datetime
    is_buy: bool
    is_personal: bool
    journal_ref_id: int
    location_id: int
    quantity: int
    transaction_id: int
    type_id: int
    unit_price: float


CharactersCharacterIdWalletTransactionsGet = list[CharactersCharacterIdWalletTransactionsGetItem]


class CorporationsCorporationIdWalletsGetItem(BaseModel):
    balance: float
    division: int


CorporationsCorporationIdWalletsGet = list[CorporationsCorporationIdWalletsGetItem]


class CorporationsCorporationIdWalletsDivisionJournalGetItem(BaseModel):
    amount: float | None
    balance: float | None
    context_id: int | None
    context_id_type: Literal['structure_id', 'station_id', 'market_transaction_id', 'character_id', 'corporation_id', 'alliance_id', 'eve_system', 'industry_job_id', 'contract_id', 'planet_id', 'system_id', 'type_id'] | None
    date: datetime
    description: str
    first_party_id: int | None
    id: int
    reason: str | None
    ref_type: Literal['acceleration_gate_fee', 'achievement_category_milestone_reward', 'achievement_milestone_reward', 'advertisement_listing_fee', 'agent_donation', 'agent_location_services', 'agent_miscellaneous', 'agent_mission_collateral_paid', 'agent_mission_collateral_refunded', 'agent_mission_reward', 'agent_mission_reward_corporation_tax', 'agent_mission_security_tax', 'agent_mission_time_bonus_reward', 'agent_mission_time_bonus_reward_corporation_tax', 'agent_security_services', 'agent_services_rendered', 'agents_preward', 'air_career_program_reward', 'alliance_maintainance_fee', 'alliance_registration_fee', 'allignment_based_gate_toll', 'asset_safety_recovery_tax', 'bounty', 'bounty_prize', 'bounty_prize_corporation_tax', 'bounty_prizes', 'bounty_reimbursement', 'bounty_surcharge', 'brokers_fee', 'campaign_objective_isk_reward', 'clone_activation', 'clone_transfer', 'contraband_fine', 'contract_auction_bid', 'contract_auction_bid_corp', 'contract_auction_bid_refund', 'contract_auction_sold', 'contract_brokers_fee', 'contract_brokers_fee_corp', 'contract_collateral', 'contract_collateral_deposited_corp', 'contract_collateral_payout', 'contract_collateral_refund', 'contract_deposit', 'contract_deposit_corp', 'contract_deposit_refund', 'contract_deposit_sales_tax', 'contract_price', 'contract_price_payment_corp', 'contract_reversal', 'contract_reward', 'contract_reward_deposited', 'contract_reward_deposited_corp', 'contract_reward_refund', 'contract_sales_tax', 'copying', 'corporate_reward_payout', 'corporate_reward_tax', 'corporation_account_withdrawal', 'corporation_bulk_payment', 'corporation_dividend_payment', 'corporation_liquidation', 'corporation_logo_change_cost', 'corporation_payment', 'corporation_registration_fee', 'cosmetic_market_component_item_purchase', 'cosmetic_market_skin_purchase', 'cosmetic_market_skin_sale', 'cosmetic_market_skin_sale_broker_fee', 'cosmetic_market_skin_sale_tax', 'cosmetic_market_skin_transaction', 'courier_mission_escrow', 'cspa', 'cspaofflinerefund', 'daily_challenge_reward', 'daily_goal_payouts', 'daily_goal_payouts_tax', 'datacore_fee', 'dna_modification_fee', 'docking_fee', 'duel_wager_escrow', 'duel_wager_payment', 'duel_wager_refund', 'ess_escrow_transfer', 'external_trade_delivery', 'external_trade_freeze', 'external_trade_thaw', 'factory_slot_rental_fee', 'flux_payout', 'flux_tax', 'flux_ticket_repayment', 'flux_ticket_sale', 'freelance_jobs_broadcasting_fee', 'freelance_jobs_duration_fee', 'freelance_jobs_escrow_refund', 'freelance_jobs_reward', 'freelance_jobs_reward_corporation_tax', 'freelance_jobs_reward_escrow', 'gm_cash_transfer', 'gm_plex_fee_refund', 'industry_job_tax', 'industry_security_tax', 'infrastructure_hub_maintenance', 'inheritance', 'insurance', 'insurgency_corruption_contribution_reward', 'insurgency_suppression_contribution_reward', 'item_trader_payment', 'jump_clone_activation_fee', 'jump_clone_installation_fee', 'kill_right_fee', 'lp_store', 'manufacturing', 'market_escrow', 'market_fine_paid', 'market_provider_tax', 'market_security_tax', 'market_transaction', 'medal_creation', 'medal_issued', 'milestone_reward_payment', 'mission_completion', 'mission_cost', 'mission_expiration', 'mission_reward', 'npc_bounty_security_tax', 'office_rental_fee', 'operation_bonus', 'opportunity_reward', 'planetary_construction', 'planetary_export_tax', 'planetary_import_tax', 'player_donation', 'player_trading', 'project_discovery_reward', 'project_discovery_tax', 'project_payouts', 'reaction', 'redeemed_isk_token', 'release_of_impounded_property', 'repair_bill', 'reprocessing_tax', 'researching_material_productivity', 'researching_technology', 'researching_time_productivity', 'resource_wars_reward', 'reverse_engineering', 'season_challenge_reward', 'security_processing_fee', 'shares', 'skill_purchase', 'skyhook_claim_fee', 'sovereignity_bill', 'store_purchase', 'store_purchase_refund', 'structure_gate_jump', 'transaction_tax', 'under_construction', 'upkeep_adjustment_fee', 'war_ally_contract', 'war_fee', 'war_fee_surrender']
    second_party_id: int | None
    tax: float | None
    tax_receiver_id: int | None


CorporationsCorporationIdWalletsDivisionJournalGet = list[CorporationsCorporationIdWalletsDivisionJournalGetItem]


class CorporationsCorporationIdWalletsDivisionTransactionsGetItem(BaseModel):
    client_id: int
    date: datetime
    is_buy: bool
    journal_ref_id: int
    location_id: int
    quantity: int
    transaction_id: int
    type_id: int
    unit_price: float


CorporationsCorporationIdWalletsDivisionTransactionsGet = list[CorporationsCorporationIdWalletsDivisionTransactionsGetItem]


WarsGet = list[int]


class WarsWarIdGet_Aggressor(BaseModel):
    alliance_id: int | None
    corporation_id: int | None
    isk_destroyed: float
    ships_killed: int


class WarsWarIdGet_AlliesItem(BaseModel):
    alliance_id: int | None
    corporation_id: int | None


class WarsWarIdGet_Defender(BaseModel):
    alliance_id: int | None
    corporation_id: int | None
    isk_destroyed: float
    ships_killed: int


class WarsWarIdGet(BaseModel):
    aggressor: WarsWarIdGet_Aggressor
    allies: list[WarsWarIdGet_AlliesItem] | None
    declared: datetime
    defender: WarsWarIdGet_Defender
    finished: datetime | None
    id: int
    mutual: bool
    open_for_allies: bool
    retracted: datetime | None
    started: datetime | None


class WarsWarIdKillmailsGetItem(BaseModel):
    killmail_hash: str
    killmail_id: int


WarsWarIdKillmailsGet = list[WarsWarIdKillmailsGetItem]


class ESIClientStub:
    class _Access_List:
        def GetCharactersAccessListsDetail(self, access_list_id: AccessListID, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersAccessListsDetailOperation:
            """Get the details of an Access List."""
            ...

        def GetCharactersAccessListsListing(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersAccessListsListingOperation:
            """Lists all Access Lists the character is Manager or Admin of."""
            ...


    Access_List: _Access_List = _Access_List()

    class _Activities:
        def GetCharactersMercenaryTacticalOperationsDetail(self, operation_id: UUID, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersMercenaryTacticalOperationsDetailOperation:
            """Get the details of a Mercenary Tactical Operation."""
            ...

        def GetCharactersMercenaryTacticalOperationsListing(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersMercenaryTacticalOperationsListingOperation:
            """Listing of all Mercenary Tactical Operations for the character."""
            ...

        def GetSkyhooksRaidable(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetSkyhooksRaidableOperation:
            """Listing of all Skyhooks that currently or will shortly be raidable."""
            ...


    Activities: _Activities = _Activities()

    class _Alliance:
        def GetAlliances(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetAlliancesOperation:
            """List all active player alliances"""
            ...

        def GetAlliancesAllianceId(self, alliance_id: AllianceID, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetAlliancesAllianceIdOperation:
            """Public information about an alliance"""
            ...

        def GetAlliancesAllianceIdCorporations(self, alliance_id: AllianceID, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetAlliancesAllianceIdCorporationsOperation:
            """List all current member corporations of an alliance"""
            ...

        def GetAlliancesAllianceIdIcons(self, alliance_id: AllianceID, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetAlliancesAllianceIdIconsOperation:
            """Get the icon urls for a alliance  This route expires daily at 11:05"""
            ...


    Alliance: _Alliance = _Alliance()

    class _Assets:
        def GetCharactersCharacterIdAssets(self, character_id: CharacterID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdAssetsOperation:
            """Return a list of the characters assets"""
            ...

        def GetCorporationsCorporationIdAssets(self, corporation_id: CorporationID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdAssetsOperation:
            """Return a list of the corporation assets"""
            ...

        def PostCharactersCharacterIdAssetsLocations(self, body: list[int], character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PostCharactersCharacterIdAssetsLocationsOperation:
            """Return locations for a set of item ids, which you can get from character assets endpoint. Coordinates for items in hangars or stations are set to (0,0,0)"""
            ...

        def PostCharactersCharacterIdAssetsNames(self, body: list[int], character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PostCharactersCharacterIdAssetsNamesOperation:
            """Return names for a set of item ids, which you can get from character assets endpoint. Typically used for items that can customize names, like containers or ships."""
            ...

        def PostCorporationsCorporationIdAssetsLocations(self, body: list[int], corporation_id: CorporationID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PostCorporationsCorporationIdAssetsLocationsOperation:
            """Return locations for a set of item ids, which you can get from corporation assets endpoint. Coordinates for items in hangars or stations are set to (0,0,0)"""
            ...

        def PostCorporationsCorporationIdAssetsNames(self, body: list[int], corporation_id: CorporationID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PostCorporationsCorporationIdAssetsNamesOperation:
            """Return names for a set of item ids, which you can get from corporation assets endpoint. Only valid for items that can customize names, like containers or ships"""
            ...


    Assets: _Assets = _Assets()

    class _Calendar:
        def GetCharactersCharacterIdCalendar(self, character_id: CharacterID, token: Token, from_event: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdCalendarOperation:
            """Get 50 event summaries from the calendar. If no from_event ID is given, the resource will return the next 50 chronological event summaries from now. If a from_event ID is specified, it will return the next 50 chronological event summaries from after that event"""
            ...

        def GetCharactersCharacterIdCalendarEventId(self, character_id: CharacterID, event_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdCalendarEventIdOperation:
            """Get all the information for a specific event"""
            ...

        def GetCharactersCharacterIdCalendarEventIdAttendees(self, character_id: CharacterID, event_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdCalendarEventIdAttendeesOperation:
            """Get all invited attendees for a given event"""
            ...

        def PutCharactersCharacterIdCalendarEventId(self, body: PutCharactersCharacterIdCalendarEventIdOperationBody, character_id: CharacterID, event_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PutCharactersCharacterIdCalendarEventIdOperation:
            """Set your response status to an event"""
            ...


    Calendar: _Calendar = _Calendar()

    class _Character:
        def GetCharactersCharacterIdAgentsResearch(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdAgentsResearchOperation:
            """Return a list of agents research information for a character. The formula for finding the current research points with an agent is: currentPoints = remainderPoints + pointsPerDay * days(currentTime - researchStartDate)"""
            ...

        def GetCharactersCharacterIdBlueprints(self, character_id: CharacterID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdBlueprintsOperation:
            """Return a list of blueprints the character owns"""
            ...

        def GetCharactersCharacterIdCorporationhistory(self, character_id: CharacterID, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdCorporationhistoryOperation:
            """Get a list of all the corporations a character has been a member of"""
            ...

        def GetCharactersCharacterIdFatigue(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdFatigueOperation:
            """Return a character's jump activation and fatigue information"""
            ...

        def GetCharactersCharacterIdMedals(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdMedalsOperation:
            """Return a list of medals the character has"""
            ...

        def GetCharactersCharacterIdNotifications(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdNotificationsOperation:
            """Return character notifications"""
            ...

        def GetCharactersCharacterIdNotificationsContacts(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdNotificationsContactsOperation:
            """Return notifications about having been added to someone's contact list"""
            ...

        def GetCharactersCharacterIdPortrait(self, character_id: CharacterID, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdPortraitOperation:
            """Get portrait urls for a character  This route expires daily at 11:05"""
            ...

        def GetCharactersCharacterIdRoles(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdRolesOperation:
            """Returns a character's corporation roles"""
            ...

        def GetCharactersCharacterIdStandings(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdStandingsOperation:
            """Return character standings from agents, NPC corporations, and factions"""
            ...

        def GetCharactersCharacterIdTitles(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdTitlesOperation:
            """Returns a character's titles"""
            ...

        def GetCharactersDetail(self, character_id: CharacterID, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersDetailOperation:
            """Public information about a character"""
            ...

        def PostCharactersAffiliation(self, body: list[int], Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PostCharactersAffiliationOperation:
            """Bulk lookup of character IDs to corporation, alliance and faction"""
            ...

        def PostCharactersCharacterIdCspa(self, body: list[int], character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PostCharactersCharacterIdCspaOperation:
            """Takes a source character ID in the url and a set of target character ID's in the body, returns a CSPA charge cost"""
            ...


    Character: _Character = _Character()

    class _Clones:
        def GetCharactersCharacterIdClones(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdClonesOperation:
            """A list of the character's clones"""
            ...

        def GetCharactersCharacterIdImplants(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdImplantsOperation:
            """Return implants on the active clone of a character"""
            ...


    Clones: _Clones = _Clones()

    class _Contacts:
        def DeleteCharactersCharacterIdContacts(self, character_id: CharacterID, contact_ids: list[int], token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> DeleteCharactersCharacterIdContactsOperation:
            """Bulk delete contacts"""
            ...

        def GetAlliancesAllianceIdContacts(self, alliance_id: AllianceID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetAlliancesAllianceIdContactsOperation:
            """Return contacts of an alliance"""
            ...

        def GetAlliancesAllianceIdContactsLabels(self, alliance_id: AllianceID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetAlliancesAllianceIdContactsLabelsOperation:
            """Return custom labels for an alliance's contacts"""
            ...

        def GetCharactersCharacterIdContacts(self, character_id: CharacterID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdContactsOperation:
            """Return contacts of a character"""
            ...

        def GetCharactersCharacterIdContactsLabels(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdContactsLabelsOperation:
            """Return custom labels for a character's contacts"""
            ...

        def GetCorporationsCorporationIdContacts(self, corporation_id: CorporationID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdContactsOperation:
            """Return contacts of a corporation"""
            ...

        def GetCorporationsCorporationIdContactsLabels(self, corporation_id: CorporationID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdContactsLabelsOperation:
            """Return custom labels for a corporation's contacts"""
            ...

        def PostCharactersCharacterIdContacts(self, body: list[int], character_id: CharacterID, standing: float, token: Token, label_ids: list[int] | None = ..., watched: bool | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PostCharactersCharacterIdContactsOperation:
            """Bulk add contacts with same settings"""
            ...

        def PutCharactersCharacterIdContacts(self, body: list[int], character_id: CharacterID, standing: float, token: Token, label_ids: list[int] | None = ..., watched: bool | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PutCharactersCharacterIdContactsOperation:
            """Bulk edit contacts with same settings"""
            ...


    Contacts: _Contacts = _Contacts()

    class _Contracts:
        def GetCharactersCharacterIdContracts(self, character_id: CharacterID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdContractsOperation:
            """Returns contracts available to a character, only if the character is issuer, acceptor or assignee. Only returns contracts no older than 30 days, or if the status is "in_progress"."""
            ...

        def GetCharactersCharacterIdContractsContractIdBids(self, character_id: CharacterID, contract_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdContractsContractIdBidsOperation:
            """Lists bids on a particular auction contract"""
            ...

        def GetCharactersCharacterIdContractsContractIdItems(self, character_id: CharacterID, contract_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdContractsContractIdItemsOperation:
            """Lists items of a particular contract"""
            ...

        def GetContractsPublicBidsContractId(self, contract_id: int, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetContractsPublicBidsContractIdOperation:
            """Lists bids on a public auction contract"""
            ...

        def GetContractsPublicItemsContractId(self, contract_id: int, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetContractsPublicItemsContractIdOperation:
            """Lists items of a public contract"""
            ...

        def GetContractsPublicRegionId(self, region_id: int, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetContractsPublicRegionIdOperation:
            """Returns a paginated list of all public contracts in the given region"""
            ...

        def GetCorporationsCorporationIdContracts(self, corporation_id: CorporationID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdContractsOperation:
            """Returns contracts available to a corporation, only if the corporation is issuer, acceptor or assignee. Only returns contracts no older than 30 days, or if the status is "in_progress"."""
            ...

        def GetCorporationsCorporationIdContractsContractIdBids(self, contract_id: int, corporation_id: CorporationID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdContractsContractIdBidsOperation:
            """Lists bids on a particular auction contract"""
            ...

        def GetCorporationsCorporationIdContractsContractIdItems(self, contract_id: int, corporation_id: CorporationID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdContractsContractIdItemsOperation:
            """Lists items of a particular contract"""
            ...


    Contracts: _Contracts = _Contracts()

    class _Corporation:
        def GetCorporationsCorporationId(self, corporation_id: CorporationID, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdOperation:
            """Public information about a corporation"""
            ...

        def GetCorporationsCorporationIdAlliancehistory(self, corporation_id: CorporationID, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdAlliancehistoryOperation:
            """Get a list of all the alliances a corporation has been a member of"""
            ...

        def GetCorporationsCorporationIdBlueprints(self, corporation_id: CorporationID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdBlueprintsOperation:
            """Returns a list of blueprints the corporation owns"""
            ...

        def GetCorporationsCorporationIdContainersLogs(self, corporation_id: CorporationID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdContainersLogsOperation:
            """Returns logs recorded in the past seven days from all audit log secure containers (ALSC) owned by a given corporation"""
            ...

        def GetCorporationsCorporationIdDivisions(self, corporation_id: CorporationID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdDivisionsOperation:
            """Return corporation hangar and wallet division names, only show if a division is not using the default name"""
            ...

        def GetCorporationsCorporationIdFacilities(self, corporation_id: CorporationID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdFacilitiesOperation:
            """Return a corporation's facilities"""
            ...

        def GetCorporationsCorporationIdIcons(self, corporation_id: CorporationID, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdIconsOperation:
            """Get the icon urls for a corporation"""
            ...

        def GetCorporationsCorporationIdMedals(self, corporation_id: CorporationID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdMedalsOperation:
            """Returns a corporation's medals"""
            ...

        def GetCorporationsCorporationIdMedalsIssued(self, corporation_id: CorporationID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdMedalsIssuedOperation:
            """Returns medals issued by a corporation"""
            ...

        def GetCorporationsCorporationIdMembers(self, corporation_id: CorporationID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdMembersOperation:
            """Return the current member list of a corporation, the token's character need to be a member of the corporation."""
            ...

        def GetCorporationsCorporationIdMembersLimit(self, corporation_id: CorporationID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdMembersLimitOperation:
            """Return a corporation's member limit, not including CEO himself"""
            ...

        def GetCorporationsCorporationIdMembersTitles(self, corporation_id: CorporationID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdMembersTitlesOperation:
            """Returns a corporation's members' titles"""
            ...

        def GetCorporationsCorporationIdMembertracking(self, corporation_id: CorporationID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdMembertrackingOperation:
            """Returns additional information about a corporation's members which helps tracking their activities"""
            ...

        def GetCorporationsCorporationIdRoles(self, corporation_id: CorporationID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdRolesOperation:
            """Return the roles of all members if the character has the personnel manager role or any grantable role."""
            ...

        def GetCorporationsCorporationIdRolesHistory(self, corporation_id: CorporationID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdRolesHistoryOperation:
            """Return how roles have changed for a coporation's members, up to a month"""
            ...

        def GetCorporationsCorporationIdShareholders(self, corporation_id: CorporationID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdShareholdersOperation:
            """Return the current shareholders of a corporation."""
            ...

        def GetCorporationsCorporationIdStandings(self, corporation_id: CorporationID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdStandingsOperation:
            """Return corporation standings from agents, NPC corporations, and factions"""
            ...

        def GetCorporationsCorporationIdStarbases(self, corporation_id: CorporationID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdStarbasesOperation:
            """Returns list of corporation starbases (POSes)"""
            ...

        def GetCorporationsCorporationIdStarbasesStarbaseId(self, corporation_id: CorporationID, starbase_id: int, system_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdStarbasesStarbaseIdOperation:
            """Returns various settings and fuels of a starbase (POS)"""
            ...

        def GetCorporationsCorporationIdStructures(self, corporation_id: CorporationID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdStructuresOperation:
            """Get a list of corporation structures. This route's version includes the changes to structures detailed in this blog: https://www.eveonline.com/article/upwell-2.0-structures-changes-coming-on-february-13th"""
            ...

        def GetCorporationsCorporationIdTitles(self, corporation_id: CorporationID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdTitlesOperation:
            """Returns a corporation's titles"""
            ...

        def GetCorporationsNpccorps(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsNpccorpsOperation:
            """Get a list of npc corporations  This route expires daily at 11:05"""
            ...


    Corporation: _Corporation = _Corporation()

    class _Corporation_Projects:
        def GetCorporationsProjectsContribution(self, corporation_id: CorporationID, project_id: UUID, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsProjectsContributionOperation:
            """Show your contribution to a corporation project."""
            ...

        def GetCorporationsProjectsContributors(self, corporation_id: CorporationID, project_id: UUID, token: Token, after: str | None = ..., before: str | None = ..., limit: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsProjectsContributorsOperation:
            """Listing of all contributors to a corporation project."""
            ...

        def GetCorporationsProjectsDetail(self, corporation_id: CorporationID, project_id: UUID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsProjectsDetailOperation:
            """Get the details of a corporation project."""
            ...

        def GetCorporationsProjectsListing(self, corporation_id: CorporationID, token: Token, after: str | None = ..., before: str | None = ..., limit: int | None = ..., state: Literal['All', 'Active'] | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsProjectsListingOperation:
            """Listing of all (active) corporation projects."""
            ...


    Corporation_Projects: _Corporation_Projects = _Corporation_Projects()

    class _Dogma:
        def GetDogmaAttributes(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetDogmaAttributesOperation:
            """Get a list of dogma attribute ids  This route expires daily at 11:05"""
            ...

        def GetDogmaAttributesAttributeId(self, attribute_id: int, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetDogmaAttributesAttributeIdOperation:
            """Get information on a dogma attribute  This route expires daily at 11:05"""
            ...

        def GetDogmaDynamicItemsTypeIdItemId(self, item_id: int, type_id: int, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetDogmaDynamicItemsTypeIdItemIdOperation:
            """Returns info about a dynamic item resulting from mutation with a mutaplasmid.  This route expires daily at 11:05"""
            ...

        def GetDogmaEffects(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetDogmaEffectsOperation:
            """Get a list of dogma effect ids  This route expires daily at 11:05"""
            ...

        def GetDogmaEffectsEffectId(self, effect_id: int, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetDogmaEffectsEffectIdOperation:
            """Get information on a dogma effect  This route expires daily at 11:05"""
            ...


    Dogma: _Dogma = _Dogma()

    class _Faction_Warfare:
        def GetCharactersCharacterIdFwStats(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdFwStatsOperation:
            """Statistical overview of a character involved in faction warfare  This route expires daily at 11:05"""
            ...

        def GetCorporationsCorporationIdFwStats(self, corporation_id: CorporationID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdFwStatsOperation:
            """Statistics about a corporation involved in faction warfare  This route expires daily at 11:05"""
            ...

        def GetFwLeaderboards(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetFwLeaderboardsOperation:
            """Top 4 leaderboard of factions for kills and victory points separated by total, last week and yesterday  This route expires daily at 11:05"""
            ...

        def GetFwLeaderboardsCharacters(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetFwLeaderboardsCharactersOperation:
            """Top 100 leaderboard of pilots for kills and victory points separated by total, last week and yesterday  This route expires daily at 11:05"""
            ...

        def GetFwLeaderboardsCorporations(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetFwLeaderboardsCorporationsOperation:
            """Top 10 leaderboard of corporations for kills and victory points separated by total, last week and yesterday  This route expires daily at 11:05"""
            ...

        def GetFwStats(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetFwStatsOperation:
            """Statistical overviews of factions involved in faction warfare  This route expires daily at 11:05"""
            ...

        def GetFwSystems(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetFwSystemsOperation:
            """An overview of the current ownership of faction warfare solar systems"""
            ...

        def GetFwWars(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetFwWarsOperation:
            """Data about which NPC factions are at war  This route expires daily at 11:05"""
            ...


    Faction_Warfare: _Faction_Warfare = _Faction_Warfare()

    class _Fittings:
        def DeleteCharactersCharacterIdFittingsFittingId(self, character_id: CharacterID, fitting_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> DeleteCharactersCharacterIdFittingsFittingIdOperation:
            """Delete a fitting from a character"""
            ...

        def GetCharactersCharacterIdFittings(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdFittingsOperation:
            """Return fittings of a character"""
            ...

        def PostCharactersCharacterIdFittings(self, body: PostCharactersCharacterIdFittingsOperationBody, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PostCharactersCharacterIdFittingsOperation:
            """Save a new fitting for a character"""
            ...


    Fittings: _Fittings = _Fittings()

    class _Fleets:
        def DeleteFleetsFleetIdMembersMemberId(self, fleet_id: int, member_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> DeleteFleetsFleetIdMembersMemberIdOperation:
            """Kick a fleet member"""
            ...

        def DeleteFleetsFleetIdSquadsSquadId(self, fleet_id: int, squad_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> DeleteFleetsFleetIdSquadsSquadIdOperation:
            """Delete a fleet squad, only empty squads can be deleted"""
            ...

        def DeleteFleetsFleetIdWingsWingId(self, fleet_id: int, wing_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> DeleteFleetsFleetIdWingsWingIdOperation:
            """Delete a fleet wing, only empty wings can be deleted. The wing may contain squads, but the squads must be empty"""
            ...

        def GetCharactersCharacterIdFleet(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdFleetOperation:
            """Return the fleet ID the character is in, if any."""
            ...

        def GetFleetsFleetId(self, fleet_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetFleetsFleetIdOperation:
            """Return details about a fleet"""
            ...

        def GetFleetsFleetIdMembers(self, fleet_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetFleetsFleetIdMembersOperation:
            """Return information about fleet members"""
            ...

        def GetFleetsFleetIdWings(self, fleet_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetFleetsFleetIdWingsOperation:
            """Return information about wings in a fleet"""
            ...

        def PostFleetsFleetIdMembers(self, body: PostFleetsFleetIdMembersOperationBody, fleet_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PostFleetsFleetIdMembersOperation:
            """Invite a character into the fleet. If a character has a CSPA charge set it is not possible to invite them to the fleet using ESI"""
            ...

        def PostFleetsFleetIdWings(self, fleet_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PostFleetsFleetIdWingsOperation:
            """Create a new wing in a fleet"""
            ...

        def PostFleetsFleetIdWingsWingIdSquads(self, fleet_id: int, wing_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PostFleetsFleetIdWingsWingIdSquadsOperation:
            """Create a new squad in a fleet"""
            ...

        def PutFleetsFleetId(self, body: PutFleetsFleetIdOperationBody, fleet_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PutFleetsFleetIdOperation:
            """Update settings about a fleet"""
            ...

        def PutFleetsFleetIdMembersMemberId(self, body: PutFleetsFleetIdMembersMemberIdOperationBody, fleet_id: int, member_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PutFleetsFleetIdMembersMemberIdOperation:
            """Move a fleet member around"""
            ...

        def PutFleetsFleetIdSquadsSquadId(self, body: PutFleetsFleetIdSquadsSquadIdOperationBody, fleet_id: int, squad_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PutFleetsFleetIdSquadsSquadIdOperation:
            """Rename a fleet squad"""
            ...

        def PutFleetsFleetIdWingsWingId(self, body: PutFleetsFleetIdWingsWingIdOperationBody, fleet_id: int, wing_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PutFleetsFleetIdWingsWingIdOperation:
            """Rename a fleet wing"""
            ...


    Fleets: _Fleets = _Fleets()

    class _Freelance_Jobs:
        def GetCharactersFreelanceJobsListing(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersFreelanceJobsListingOperation:
            """Listing of all freelance jobs you are actively participating in."""
            ...

        def GetCharactersFreelanceJobsParticipation(self, character_id: CharacterID, job_id: UUID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersFreelanceJobsParticipationOperation:
            """Show your participation in a freelance job."""
            ...

        def GetCorporationsFreelanceJobsListing(self, corporation_id: CorporationID, token: Token, after: str | None = ..., before: str | None = ..., limit: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsFreelanceJobsListingOperation:
            """Listing of all freelance jobs for your corporation."""
            ...

        def GetCorporationsFreelanceJobsParticipants(self, corporation_id: CorporationID, job_id: UUID, token: Token, after: str | None = ..., before: str | None = ..., limit: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsFreelanceJobsParticipantsOperation:
            """Listing of all participants of a freelance job."""
            ...

        def GetFreelanceJobsDetail(self, job_id: UUID, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetFreelanceJobsDetailOperation:
            """Get the details of a freelance job.  Jobs without an ACL (public jobs) does not require authentication.  Jobs with an ACL requires authentication, and requires that the character is: - An active participant of the job, or - A freelance job manager for the corporation that owns the job."""
            ...

        def GetFreelanceJobsListing(self, after: str | None = ..., before: str | None = ..., limit: int | None = ..., corporation_id: CorporationID | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetFreelanceJobsListingOperation:
            """Listing of all public freelance jobs."""
            ...


    Freelance_Jobs: _Freelance_Jobs = _Freelance_Jobs()

    class _Incursions:
        def GetIncursions(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetIncursionsOperation:
            """Return a list of current incursions"""
            ...


    Incursions: _Incursions = _Incursions()

    class _Industry:
        def GetCharactersCharacterIdIndustryJobs(self, character_id: CharacterID, token: Token, include_completed: bool | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdIndustryJobsOperation:
            """List industry jobs placed by a character"""
            ...

        def GetCharactersCharacterIdMining(self, character_id: CharacterID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdMiningOperation:
            """Paginated record of all mining done by a character for the past 30 days"""
            ...

        def GetCorporationCorporationIdMiningExtractions(self, corporation_id: CorporationID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationCorporationIdMiningExtractionsOperation:
            """Extraction timers for all moon chunks being extracted by refineries belonging to a corporation."""
            ...

        def GetCorporationCorporationIdMiningObservers(self, corporation_id: CorporationID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationCorporationIdMiningObserversOperation:
            """Paginated list of all entities capable of observing and recording mining for a corporation"""
            ...

        def GetCorporationCorporationIdMiningObserversObserverId(self, corporation_id: CorporationID, observer_id: int, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationCorporationIdMiningObserversObserverIdOperation:
            """Paginated record of all mining seen by an observer"""
            ...

        def GetCorporationsCorporationIdIndustryJobs(self, corporation_id: CorporationID, token: Token, include_completed: bool | None = ..., page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdIndustryJobsOperation:
            """List industry jobs run by a corporation"""
            ...

        def GetIndustryFacilities(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetIndustryFacilitiesOperation:
            """Return a list of industry facilities"""
            ...

        def GetIndustrySystems(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetIndustrySystemsOperation:
            """Return cost indices for solar systems"""
            ...


    Industry: _Industry = _Industry()

    class _Insurance:
        def GetInsurancePrices(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetInsurancePricesOperation:
            """Return available insurance levels for all ship types"""
            ...


    Insurance: _Insurance = _Insurance()

    class _Killmails:
        def GetCharactersCharacterIdKillmailsRecent(self, character_id: CharacterID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdKillmailsRecentOperation:
            """Return a list of a character's kills and losses going back 90 days"""
            ...

        def GetCorporationsCorporationIdKillmailsRecent(self, corporation_id: CorporationID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdKillmailsRecentOperation:
            """Get a list of a corporation's kills and losses going back 90 days"""
            ...

        def GetKillmailsKillmailIdKillmailHash(self, killmail_hash: str, killmail_id: int, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetKillmailsKillmailIdKillmailHashOperation:
            """Return a single killmail from its ID and hash"""
            ...


    Killmails: _Killmails = _Killmails()

    class _Location:
        def GetCharactersCharacterIdLocation(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdLocationOperation:
            """Information about the characters current location. Returns the current solar system id, and also the current station or structure ID if applicable"""
            ...

        def GetCharactersCharacterIdOnline(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdOnlineOperation:
            """Checks if the character is currently online"""
            ...

        def GetCharactersCharacterIdShip(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdShipOperation:
            """Get the current ship type, name and id"""
            ...


    Location: _Location = _Location()

    class _Loyalty:
        def GetCharactersCharacterIdLoyaltyPoints(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdLoyaltyPointsOperation:
            """Return a list of loyalty points for all corporations the character has worked for"""
            ...

        def GetLoyaltyStoresCorporationIdOffers(self, corporation_id: CorporationID, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetLoyaltyStoresCorporationIdOffersOperation:
            """Return a list of offers from a specific corporation's loyalty store  This route expires daily at 11:05"""
            ...


    Loyalty: _Loyalty = _Loyalty()

    class _Mail:
        def DeleteCharactersCharacterIdMailLabelsLabelId(self, character_id: CharacterID, label_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> DeleteCharactersCharacterIdMailLabelsLabelIdOperation:
            """Delete a mail label"""
            ...

        def DeleteCharactersCharacterIdMailMailId(self, character_id: CharacterID, mail_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> DeleteCharactersCharacterIdMailMailIdOperation:
            """Delete a mail"""
            ...

        def GetCharactersCharacterIdMail(self, character_id: CharacterID, token: Token, labels: list[int] | None = ..., last_mail_id: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdMailOperation:
            """Return the 50 most recent mail headers belonging to the character that match the query criteria. Queries can be filtered by label, and last_mail_id can be used to paginate backwards"""
            ...

        def GetCharactersCharacterIdMailLabels(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdMailLabelsOperation:
            """Return a list of the users mail labels, unread counts for each label and a total unread count."""
            ...

        def GetCharactersCharacterIdMailLists(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdMailListsOperation:
            """Return all mailing lists that the character is subscribed to"""
            ...

        def GetCharactersCharacterIdMailMailId(self, character_id: CharacterID, mail_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdMailMailIdOperation:
            """Return the contents of an EVE mail"""
            ...

        def PostCharactersCharacterIdMail(self, body: PostCharactersCharacterIdMailOperationBody, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PostCharactersCharacterIdMailOperation:
            """Create and send a new mail"""
            ...

        def PostCharactersCharacterIdMailLabels(self, body: PostCharactersCharacterIdMailLabelsOperationBody, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PostCharactersCharacterIdMailLabelsOperation:
            """Create a mail label"""
            ...

        def PutCharactersCharacterIdMailMailId(self, body: PutCharactersCharacterIdMailMailIdOperationBody, character_id: CharacterID, mail_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PutCharactersCharacterIdMailMailIdOperation:
            """Update metadata about a mail"""
            ...


    Mail: _Mail = _Mail()

    class _Market:
        def GetCharactersCharacterIdOrders(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdOrdersOperation:
            """List open market orders placed by a character"""
            ...

        def GetCharactersCharacterIdOrdersHistory(self, character_id: CharacterID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdOrdersHistoryOperation:
            """List cancelled and expired market orders placed by a character up to 90 days in the past."""
            ...

        def GetCorporationsCorporationIdOrders(self, corporation_id: CorporationID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdOrdersOperation:
            """List open market orders placed on behalf of a corporation"""
            ...

        def GetCorporationsCorporationIdOrdersHistory(self, corporation_id: CorporationID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdOrdersHistoryOperation:
            """List cancelled and expired market orders placed on behalf of a corporation up to 90 days in the past."""
            ...

        def GetMarketsGroups(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetMarketsGroupsOperation:
            """Get a list of item groups  This route expires daily at 11:05"""
            ...

        def GetMarketsGroupsMarketGroupId(self, market_group_id: int, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetMarketsGroupsMarketGroupIdOperation:
            """Get information on an item group  This route expires daily at 11:05"""
            ...

        def GetMarketsPrices(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetMarketsPricesOperation:
            """Return a list of prices"""
            ...

        def GetMarketsRegionIdHistory(self, region_id: int, type_id: int, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetMarketsRegionIdHistoryOperation:
            """Return a list of historical market statistics for the specified type in a region  This route expires daily at 11:05"""
            ...

        def GetMarketsRegionIdOrders(self, order_type: Literal['buy', 'sell', 'all'], region_id: int, page: int | None = ..., type_id: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetMarketsRegionIdOrdersOperation:
            """Return a list of orders in a region"""
            ...

        def GetMarketsRegionIdTypes(self, region_id: int, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetMarketsRegionIdTypesOperation:
            """Return a list of type IDs that have active orders in the region, for efficient market indexing."""
            ...

        def GetMarketsStructuresStructureId(self, structure_id: int, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetMarketsStructuresStructureIdOperation:
            """Return all orders in a structure"""
            ...


    Market: _Market = _Market()

    class _Meta:
        def GetMetaChangelog(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetMetaChangelogOperation:
            """Get the changelog of this API."""
            ...

        def GetMetaCompatibilityDates(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetMetaCompatibilityDatesOperation:
            """Get a list of compatibility dates."""
            ...

        def GetMetaName(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetMetaNameOperation:
            """Get the name ESI is currently going by, plus the full and glorious history of every name it has ever had. The three letters have never once meant the same thing twice."""
            ...

        def GetMetaStatus(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetMetaStatusOperation:
            """Get the health status of each API route."""
            ...


    Meta: _Meta = _Meta()

    class _Military_Campaigns:
        def GetCharactersMilitaryCampaignsObjectivesListing(self, character_id: CharacterID, token: Token, after: str | None = ..., before: str | None = ..., limit: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersMilitaryCampaignsObjectivesListingOperation:
            """Listing of the military campaign objectives the character has participated in."""
            ...

        def GetCharactersMilitaryCampaignsObjectivesParticipation(self, character_id: CharacterID, objective_id: UUID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersMilitaryCampaignsObjectivesParticipationOperation:
            """Show your participation in a military campaign objective."""
            ...

        def GetMilitaryCampaignsDetail(self, campaign_id: UUID, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetMilitaryCampaignsDetailOperation:
            """Get the details of a military campaign."""
            ...

        def GetMilitaryCampaignsListing(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetMilitaryCampaignsListingOperation:
            """Listing of all active military campaigns."""
            ...

        def GetMilitaryCampaignsObjectivesDetail(self, campaign_id: UUID, objective_id: UUID, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetMilitaryCampaignsObjectivesDetailOperation:
            """Get the details of an objective of a military campaign."""
            ...

        def GetMilitaryCampaignsObjectivesListing(self, campaign_id: UUID, after: str | None = ..., before: str | None = ..., limit: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetMilitaryCampaignsObjectivesListingOperation:
            """Listing of all active, completed or expired objectives of a military campaign."""
            ...


    Military_Campaigns: _Military_Campaigns = _Military_Campaigns()

    class _Planetary_Interaction:
        def GetCharactersCharacterIdPlanets(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdPlanetsOperation:
            """Returns a list of all planetary colonies owned by a character."""
            ...

        def GetCharactersCharacterIdPlanetsPlanetId(self, character_id: CharacterID, planet_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdPlanetsPlanetIdOperation:
            """Returns full details on the layout of a single planetary colony, including links, pins and routes. Note: Planetary information is only recalculated when the colony is viewed through the client. Information will not update until this criteria is met."""
            ...

        def GetCorporationsCorporationIdCustomsOffices(self, corporation_id: CorporationID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdCustomsOfficesOperation:
            """List customs offices owned by a corporation"""
            ...

        def GetUniverseSchematicsSchematicId(self, schematic_id: int, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseSchematicsSchematicIdOperation:
            """Get information on a planetary factory schematic"""
            ...


    Planetary_Interaction: _Planetary_Interaction = _Planetary_Interaction()

    class _Routes:
        def PostRoute(self, body: RouteRequestBody, origin_system_id: SolarSystemID, destination_system_id: SolarSystemID, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PostRouteOperation:
            """Calculate the systems between the given origin and destination."""
            ...


    Routes: _Routes = _Routes()

    class _Search:
        def GetCharactersCharacterIdSearch(self, categories: list[Literal['agent', 'alliance', 'character', 'constellation', 'corporation', 'faction', 'inventory_type', 'region', 'solar_system', 'station', 'structure']], character_id: CharacterID, search: Annotated[str, Field(min_length=3)], token: Token, strict: bool | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdSearchOperation:
            """Search for entities that match a given sub-string."""
            ...


    Search: _Search = _Search()

    class _Skills:
        def GetCharactersCharacterIdAttributes(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdAttributesOperation:
            """Return attributes of a character"""
            ...

        def GetCharactersCharacterIdSkillqueue(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdSkillqueueOperation:
            """List the configured skill queue for the given character.  Entries that have their finish time in the past are completed, but aren't updated in the "/skills" route yet. This will happen the next time the character logs in."""
            ...

        def GetCharactersCharacterIdSkills(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdSkillsOperation:
            """List all trained skills for the given character.  Skills returned by this route can be out-of-date if the character hasn't logged in since one or more skills completed training. Use the /skillqueue route to check for skills that completed training. Entries that are in the past need to be applied on top of this list to get an accurate view of the character's current skills."""
            ...


    Skills: _Skills = _Skills()

    class _Sovereignty:
        def GetSovereigntyCampaigns(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetSovereigntyCampaignsOperation:
            """Shows sovereignty data for campaigns."""
            ...

        def GetSovereigntySystems(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetSovereigntySystemsOperation:
            """Listing of sovereignty details for all K-space systems in New Eden."""
            ...


    Sovereignty: _Sovereignty = _Sovereignty()

    class _Status:
        def GetStatus(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetStatusOperation:
            """EVE Server status"""
            ...


    Status: _Status = _Status()

    class _Structures:
        def GetCharactersStructuresMercenaryDensDetail(self, mercenary_den_id: ItemID, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersStructuresMercenaryDensDetailOperation:
            """Get the details of a Mercenary Den."""
            ...

        def GetCharactersStructuresMercenaryDensListing(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersStructuresMercenaryDensListingOperation:
            """Listing of all Mercenary Dens."""
            ...

        def GetCorporationsStructuresSkyhooksDetail(self, skyhook_id: ItemID, corporation_id: CorporationID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsStructuresSkyhooksDetailOperation:
            """Get the details of a Skyhook."""
            ...

        def GetCorporationsStructuresSkyhooksListing(self, corporation_id: CorporationID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsStructuresSkyhooksListingOperation:
            """Listing of all Skyhooks."""
            ...

        def GetCorporationsStructuresSovereigntyHubsDetail(self, sovereignty_hub_id: ItemID, corporation_id: CorporationID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsStructuresSovereigntyHubsDetailOperation:
            """Get the details of a Sovereignty Hub."""
            ...

        def GetCorporationsStructuresSovereigntyHubsListing(self, corporation_id: CorporationID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsStructuresSovereigntyHubsListingOperation:
            """Listing of all Sovereignty Hubs."""
            ...


    Structures: _Structures = _Structures()

    class _Universe:
        def GetUniverseAncestries(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseAncestriesOperation:
            """Get all character ancestries  This route expires daily at 11:05"""
            ...

        def GetUniverseAsteroidBeltsAsteroidBeltId(self, asteroid_belt_id: int, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseAsteroidBeltsAsteroidBeltIdOperation:
            """Get information on an asteroid belt  This route expires daily at 11:05"""
            ...

        def GetUniverseBloodlines(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseBloodlinesOperation:
            """Get a list of bloodlines  This route expires daily at 11:05"""
            ...

        def GetUniverseCategories(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseCategoriesOperation:
            """Get a list of item categories  This route expires daily at 11:05"""
            ...

        def GetUniverseCategoriesCategoryId(self, category_id: int, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseCategoriesCategoryIdOperation:
            """Get information of an item category  This route expires daily at 11:05"""
            ...

        def GetUniverseConstellations(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseConstellationsOperation:
            """Get a list of constellations  This route expires daily at 11:05"""
            ...

        def GetUniverseConstellationsConstellationId(self, constellation_id: int, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseConstellationsConstellationIdOperation:
            """Get information on a constellation  This route expires daily at 11:05"""
            ...

        def GetUniverseFactions(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseFactionsOperation:
            """Get a list of factions  This route expires daily at 11:05"""
            ...

        def GetUniverseGraphics(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseGraphicsOperation:
            """Get a list of graphics  This route expires daily at 11:05"""
            ...

        def GetUniverseGraphicsGraphicId(self, graphic_id: int, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseGraphicsGraphicIdOperation:
            """Get information on a graphic  This route expires daily at 11:05"""
            ...

        def GetUniverseGroups(self, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseGroupsOperation:
            """Get a list of item groups  This route expires daily at 11:05"""
            ...

        def GetUniverseGroupsGroupId(self, group_id: int, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseGroupsGroupIdOperation:
            """Get information on an item group  This route expires daily at 11:05"""
            ...

        def GetUniverseMoonsMoonId(self, moon_id: int, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseMoonsMoonIdOperation:
            """Get information on a moon  This route expires daily at 11:05"""
            ...

        def GetUniversePlanetsPlanetId(self, planet_id: int, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniversePlanetsPlanetIdOperation:
            """Get information on a planet  This route expires daily at 11:05"""
            ...

        def GetUniverseRaces(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseRacesOperation:
            """Get a list of character races  This route expires daily at 11:05"""
            ...

        def GetUniverseRegions(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseRegionsOperation:
            """Get a list of regions  This route expires daily at 11:05"""
            ...

        def GetUniverseRegionsRegionId(self, region_id: int, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseRegionsRegionIdOperation:
            """Get information on a region  This route expires daily at 11:05"""
            ...

        def GetUniverseStargatesStargateId(self, stargate_id: int, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseStargatesStargateIdOperation:
            """Get information on a stargate  This route expires daily at 11:05"""
            ...

        def GetUniverseStarsStarId(self, star_id: int, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseStarsStarIdOperation:
            """Get information on a star  This route expires daily at 11:05"""
            ...

        def GetUniverseStationsStationId(self, station_id: int, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseStationsStationIdOperation:
            """Get information on a station  This route expires daily at 11:05"""
            ...

        def GetUniverseStructures(self, filter: Literal['market', 'manufacturing_basic'] | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseStructuresOperation:
            """List all public structures"""
            ...

        def GetUniverseStructuresStructureId(self, structure_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseStructuresStructureIdOperation:
            """Returns information on requested structure if you are on the ACL. Otherwise, returns "Forbidden" for all inputs."""
            ...

        def GetUniverseSystemJumps(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseSystemJumpsOperation:
            """Get the number of jumps in solar systems within the last hour ending at the timestamp of the Last-Modified header, excluding wormhole space. Only systems with jumps will be listed"""
            ...

        def GetUniverseSystemKills(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseSystemKillsOperation:
            """Get the number of ship, pod and NPC kills per solar system within the last hour ending at the timestamp of the Last-Modified header, excluding wormhole space. Only systems with kills will be listed"""
            ...

        def GetUniverseSystems(self, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseSystemsOperation:
            """Get a list of solar systems  This route expires daily at 11:05"""
            ...

        def GetUniverseSystemsSystemId(self, system_id: int, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseSystemsSystemIdOperation:
            """Get information on a solar system.  This route expires daily at 11:05"""
            ...

        def GetUniverseTypes(self, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseTypesOperation:
            """Get a list of type ids  This route expires daily at 11:05"""
            ...

        def GetUniverseTypesTypeId(self, type_id: int, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetUniverseTypesTypeIdOperation:
            """Get information on a type  This route expires daily at 11:05"""
            ...

        def PostUniverseIds(self, body: list[Annotated[str, Field(min_length=1, max_length=100)]], Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PostUniverseIdsOperation:
            """Resolve a set of names to IDs in the following categories: agents, alliances, characters, constellations, corporations factions, inventory_types, regions, stations, and systems. Only exact matches will be returned. All names searched for are cached for 12 hours"""
            ...

        def PostUniverseNames(self, body: list[int], Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PostUniverseNamesOperation:
            """Resolve a set of IDs to names and categories. Supported ID's for resolving are: Characters, Corporations, Alliances, Stations, Solar Systems, Constellations, Regions, Types, Factions"""
            ...


    Universe: _Universe = _Universe()

    class _User_Interface:
        def PostUiAutopilotWaypoint(self, add_to_beginning: bool, clear_other_waypoints: bool, destination_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PostUiAutopilotWaypointOperation:
            """Set a solar system as autopilot waypoint"""
            ...

        def PostUiOpenwindowContract(self, contract_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PostUiOpenwindowContractOperation:
            """Open the contract window inside the client"""
            ...

        def PostUiOpenwindowInformation(self, target_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PostUiOpenwindowInformationOperation:
            """Open the information window for a character, corporation or alliance inside the client"""
            ...

        def PostUiOpenwindowMarketdetails(self, type_id: int, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PostUiOpenwindowMarketdetailsOperation:
            """Open the market details window for a specific typeID inside the client"""
            ...

        def PostUiOpenwindowNewmail(self, body: PostUiOpenwindowNewmailOperationBody, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> PostUiOpenwindowNewmailOperation:
            """Open the New Mail window, according to settings from the request if applicable"""
            ...


    User_Interface: _User_Interface = _User_Interface()

    class _Wallet:
        def GetCharactersCharacterIdWallet(self, character_id: CharacterID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdWalletOperation:
            """Returns a character's wallet balance"""
            ...

        def GetCharactersCharacterIdWalletJournal(self, character_id: CharacterID, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdWalletJournalOperation:
            """Retrieve the given character's wallet journal going 30 days back"""
            ...

        def GetCharactersCharacterIdWalletTransactions(self, character_id: CharacterID, token: Token, from_id: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCharactersCharacterIdWalletTransactionsOperation:
            """Get wallet transactions of a character"""
            ...

        def GetCorporationsCorporationIdWallets(self, corporation_id: CorporationID, token: Token, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdWalletsOperation:
            """Get a corporation's wallets"""
            ...

        def GetCorporationsCorporationIdWalletsDivisionJournal(self, corporation_id: CorporationID, division: int, token: Token, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdWalletsDivisionJournalOperation:
            """Retrieve the given corporation's wallet journal for the given division going 30 days back"""
            ...

        def GetCorporationsCorporationIdWalletsDivisionTransactions(self, corporation_id: CorporationID, division: int, token: Token, from_id: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetCorporationsCorporationIdWalletsDivisionTransactionsOperation:
            """Get wallet transactions of a corporation"""
            ...


    Wallet: _Wallet = _Wallet()

    class _Wars:
        def GetWars(self, max_war_id: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetWarsOperation:
            """Return a list of wars"""
            ...

        def GetWarsWarId(self, war_id: int, Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetWarsWarIdOperation:
            """Return details about a war"""
            ...

        def GetWarsWarIdKillmails(self, war_id: int, page: int | None = ..., Accept_Language: Literal['en', 'de', 'fr', 'ja', 'ru', 'zh', 'ko', 'es'] | None = ..., If_None_Match: str | None = ..., X_Compatibility_Date: Literal['2026-08-04'] | None = ..., X_Tenant: str | None = ..., If_Modified_Since: str | None = ..., **kwargs: Any) -> GetWarsWarIdKillmailsOperation:
            """Return a list of kills related to a war"""
            ...


    Wars: _Wars = _Wars()
