import logging
from random import randint
from typing import TYPE_CHECKING

from aiopenapi3.errors import HTTPError
from celery import shared_task

from esi.decorators import rate_limit_retry_task

from allianceauth.eveonline.providers import open_api_provider
from allianceauth.services.tasks import QueueOnce

from .models import (
    EveAllianceInfo, EveCharacter, EveCorporationInfo, EveFactionInfo,
)

logger = logging.getLogger(__name__)

TASK_PRIORITY = 7
CHARACTER_AFFILIATION_CHUNK_SIZE = 500
EVEONLINE_TASK_JITTER = 600

if TYPE_CHECKING:
    from celery.result import AsyncResult

    # https://github.com/sbdchd/celery-types
    classes = [
        AsyncResult,
    ]

    for cls in classes:
        setattr(cls, "__class_getitem__", classmethod(lambda cls, *args, **kwargs: cls))


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


@shared_task(bind=True)
@rate_limit_retry_task
def update_corp(self, corp_id: int) -> None:
    """Update given corporation from ESI"""
    EveCorporationInfo.objects.update_corporation(corp_id)


@shared_task(bind=True)
@rate_limit_retry_task
def update_alliance(self, alliance_id: int) -> None:
    """Update given alliance from ESI"""
    EveAllianceInfo.objects.get(alliance_id=alliance_id).update_alliance()
    EveAllianceInfo.objects.get(alliance_id=alliance_id).populate_alliance()


@shared_task(bind=True)
@rate_limit_retry_task
def update_character(self, character_id: int) -> None:
    """Update given character from ESI."""
    # TODO: split these up as they operated on different Caches (1hr/1day)
    EveCharacter.objects.update_character(character_id)  # Primary Affilation Data
    EveCharacter.objects.update_character_other(character_id)  # the rest of the model fluff


@shared_task(bind=True)
@rate_limit_retry_task
def update_all_factions(self) -> None:
    """Update given character from ESI."""
    EveFactionInfo.objects.update_factions()


@shared_task(base=QueueOnce)
def run_model_update() -> None:
    """Update all alliances, corporations and characters from ESI"""

    # Queue update tasks for Known Corporation Models, excluding closed corps (ceo_id=1)
    for corp in EveCorporationInfo.objects.exclude_closed().values('corporation_id'):
        update_corp.apply_async(
            args=(corp['corporation_id'],),
            priority=TASK_PRIORITY,
            countdown=randint(1, EVEONLINE_TASK_JITTER))

    # Queue update tasks for Known Alliance Models
    for alliance in EveAllianceInfo.objects.all().values('alliance_id'):
        update_alliance.apply_async(
            args=(alliance['alliance_id'],),
            priority=TASK_PRIORITY,
            countdown=randint(1, EVEONLINE_TASK_JITTER))

    # Queue update tasks for Known Character Models, excluding characters in Doomheim (corporation_id=1000001)
    character_ids = EveCharacter.objects.exclude_biomassed().values_list('character_id', flat=True)
    for character_ids_chunk in chunks(character_ids, CHARACTER_AFFILIATION_CHUNK_SIZE):
        update_character_chunk.apply_async(
            args=(character_ids_chunk,),
            priority=TASK_PRIORITY,
            countdown=randint(1, EVEONLINE_TASK_JITTER))


@shared_task
def update_character_chunk(character_ids_chunk: list) -> None:
    """Update a list of character from ESI"""

    try:
        affiliations_raw, _ = open_api_provider.get_affiliations(character_ids_chunk)
        character_names = open_api_provider.post_names(character_ids_chunk)
    except HTTPError:
        logger.info("Failed to bulk update characters. Attempting single updates")
        for character_id in character_ids_chunk:
            update_character.apply_async(
                args=(character_id,),
                priority=TASK_PRIORITY,
                countdown=randint(1, EVEONLINE_TASK_JITTER))
        return

    affiliations = {affiliation.character_id: affiliation for affiliation in affiliations_raw}

    # add character names to affiliations
    for character in character_names:
        character_id = character.id
        if character_id in affiliations:
            affiliations[character_id].name = character.name

    # fetch current characters
    characters = EveCharacter.objects.filter(
        character_id__in=character_ids_chunk
    ).values('character_id', 'corporation_id', 'alliance_id', 'character_name')

    for character in characters:
        character_id = character.get('character_id')
        if character_id in affiliations:
            affiliation = affiliations[character_id]

            corp_changed = (
                character.get('corporation_id') != affiliation.corporation_id
            )

            alliance_id = character.get('alliance_id')
            if not alliance_id:
                alliance_id = None
            alliance_changed = alliance_id != affiliation.alliance_id

            name_changed = False
            fetched_name = affiliation.name
            if fetched_name:
                name_changed = character.get('character_name') != fetched_name

            if corp_changed or alliance_changed or name_changed:
                update_character.apply_async(
                    args=(character.get('character_id'),),
                    priority=TASK_PRIORITY)
