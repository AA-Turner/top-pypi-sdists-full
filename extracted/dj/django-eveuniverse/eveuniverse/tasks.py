"""Tasks for Eve Universe."""

import datetime as dt
import logging
from typing import Iterable, List, Optional

from bravado.exception import HTTPError
from celery import chain, shared_task
from celery_once import QueueOnce as BaseQueueOnce
from django.db.utils import OperationalError
from django.utils.timezone import now

from . import __title__
from .app_settings import (
    EVEUNIVERSE_LOAD_TASKS_PRIORITY,
    EVEUNIVERSE_NAMES_EXPIRATION_TIME,
    EVEUNIVERSE_TASKS_TIME_LIMIT,
)
from .constants import POST_UNIVERSE_NAMES_MAX_ITEMS, EveCategoryId
from .core.esitools import is_esi_online
from .models import EveCategory, EveEntity, EveMarketPrice, EveRegion, EveType
from .models.base import EveUniverseEntityModel, determine_effective_sections
from .providers import esi
from .utils import LoggerAddTag, chunks

logger = LoggerAddTag(logging.getLogger(__name__), __title__)
# logging.getLogger("esi").setLevel(logging.INFO)


# pylint: disable = abstract-method
class QueueOnce(BaseQueueOnce):
    """Make sure all redundant tasks will abort gracefully."""

    once = BaseQueueOnce.once
    once["graceful"] = True


# params for all tasks
_TASK_DEFAULTS = {"time_limit": EVEUNIVERSE_TASKS_TIME_LIMIT}

# params for tasks that make ESI calls
_TASK_ESI_DEFAULTS = {
    **_TASK_DEFAULTS,
    **{
        "autoretry_for": [OperationalError],  # TODO: Double-check: Correct exception?
        "retry_kwargs": {"max_retries": 3},
        "retry_backoff": True,
    },
}
_TASK_ESI_DEFAULTS_ONCE = {**_TASK_ESI_DEFAULTS, **{"base": QueueOnce}}


# Eve Universe objects


@shared_task(**_TASK_ESI_DEFAULTS_ONCE)
def load_eve_object(
    model_name: str, id: int, include_children=False, wait_for_children=True
) -> None:
    """Task for loading an eve object.
    Will only be created from ESI if it does not exist
    """
    logger.info("Loading %s with ID %s", model_name, id)
    model_class = EveUniverseEntityModel.get_model_class(model_name)
    model_class.objects.get_or_create_esi(  # type: ignore
        id=id, include_children=include_children, wait_for_children=wait_for_children
    )


@shared_task(**_TASK_ESI_DEFAULTS_ONCE)
def update_or_create_eve_object(
    model_name: str,
    id: int,
    include_children=False,
    wait_for_children=True,
    enabled_sections: Optional[List[str]] = None,
    task_priority: Optional[int] = None,
) -> None:
    """Update or create an eve object from ESI.

    Args:
        model_name: Name of the respective Django model, e.g. ``"EveType"``
        id: Eve Online ID of object
        include_children: if child objects should be updated/created as well
        (only when a new object is created)
        wait_for_children: when true child objects will be updated/created blocking (if any),
        else async (only when a new object is created)
        enabled_sections: Sections to load regardless of current settings,
        e.g. `[EveType.Section.DOGMAS]` will always load dogmas for EveTypes
        task_priority: priority of started tasks
    """
    logger.info("Updating/Creating %s with ID %s", model_name, id)
    model_class = EveUniverseEntityModel.get_model_class(model_name)
    model_class.objects.update_or_create_esi(  # type: ignore
        id=id,
        include_children=include_children,
        wait_for_children=wait_for_children,
        enabled_sections=enabled_sections,
        task_priority=task_priority,
    )


@shared_task(**_TASK_ESI_DEFAULTS_ONCE)
def update_or_create_inline_object(
    parent_obj_id: int,
    parent_fk: str,
    eve_data_obj: dict,
    other_pk_info: dict,
    parent2_model_name: str,
    inline_model_name: str,
    parent_model_name: str,
    enabled_sections: Optional[List[str]] = None,
) -> None:
    """Task for updating or creating a single inline object from ESI"""
    logger.info(
        "Updating/Creating inline object %s for %s wit ID %s",
        inline_model_name,
        parent_model_name,
        parent_obj_id,
    )
    model_class = EveUniverseEntityModel.get_model_class(parent_model_name)
    model_class._update_or_create_inline_object(  # type: ignore
        parent_obj_id=parent_obj_id,
        parent_fk=parent_fk,
        eve_data_obj=eve_data_obj,
        other_pk_info=other_pk_info,
        parent2_model_name=parent2_model_name,
        inline_model_name=inline_model_name,
        enabled_sections=enabled_sections,
    )


# EveEntity objects


@shared_task(**_TASK_ESI_DEFAULTS)
def create_eve_entities(ids: Iterable[int]) -> None:
    """Task for bulk creating and resolving multiple entities from ESI."""
    EveEntity.objects.bulk_resolve_ids(ids)  # type: ignore


@shared_task(**_TASK_ESI_DEFAULTS_ONCE)
def update_unresolved_eve_entities() -> None:
    """Update all unresolved EveEntity objects from ESI.

    Will resolve entities in parallel to speed up resolving large sets.
    """
    ids = list(EveEntity.objects.filter(name="").valid_ids())  # type: ignore
    logger.info("Updating %d unresolved entities from ESI", len(ids))
    for chunk_ids in chunks(ids, POST_UNIVERSE_NAMES_MAX_ITEMS):
        _update_unresolved_eve_entities_for_page.delay(chunk_ids)  # type: ignore


@shared_task(**_TASK_ESI_DEFAULTS)
def _update_unresolved_eve_entities_for_page(ids: Iterable[int]) -> None:
    """Update unresolved EveEntity objects for given ids from ESI."""
    EveEntity.objects.update_from_esi_by_id(ids)  # type: ignore


# Object loaders


@shared_task(**_TASK_ESI_DEFAULTS_ONCE)
def load_map(enabled_sections: Optional[List[str]] = None) -> None:
    """Load the complete Eve map with all regions, constellation and solar systems
    and additional related entities if they are enabled.

    Args:
        enabled_sections: Sections to load regardless of current settings
    """
    logger.info(
        "Loading complete map with all regions, constellations, solar systems "
        "and the following additional entities if related to the map: %s",
        ", ".join(determine_effective_sections(enabled_sections)),
    )
    category, method = EveRegion._esi_path_list()
    all_ids = getattr(getattr(esi.client, category), method)().results()
    for id in all_ids:
        update_or_create_eve_object.delay(
            model_name="EveRegion",
            id=id,
            include_children=True,
            wait_for_children=False,
            enabled_sections=enabled_sections,
            task_priority=EVEUNIVERSE_LOAD_TASKS_PRIORITY,
        )  # type: ignore


@shared_task(**_TASK_ESI_DEFAULTS_ONCE)
def load_all_types(enabled_sections: Optional[List[str]] = None) -> None:
    """Load all eve types.

    Args:
        enabled_sections: Sections to load regardless of current settings
    """
    logger.info(
        "Loading all eve types from ESI including these sections: %s",
        ", ".join(determine_effective_sections(enabled_sections)),
    )
    category, method = EveCategory._esi_path_list()
    result = getattr(getattr(esi.client, category), method)().results()
    if not result:
        raise ValueError("Did not receive category IDs from ESI.")
    category_ids = sorted(result)
    logger.debug("Fetching categories for IDs: %s", category_ids)
    for category_id in category_ids:
        _load_category_with_children(
            category_id=category_id, enabled_sections=enabled_sections
        )


def _load_category_with_children(
    category_id: int,
    force_loading_dogma: bool = False,
    enabled_sections: Optional[List[str]] = None,
) -> None:
    """Start loading a category async incl. all it's children from ESI."""
    enabled_sections = enabled_sections or []
    if force_loading_dogma:
        enabled_sections.append(EveType.Section.DOGMAS.value)
    update_or_create_eve_object.delay(
        model_name="EveCategory",
        id=category_id,
        include_children=True,
        wait_for_children=False,
        enabled_sections=enabled_sections,
        task_priority=EVEUNIVERSE_LOAD_TASKS_PRIORITY,
    )  # type: ignore


def _load_group_with_children(group_id: int, force_loading_dogma: bool = False) -> None:
    """Starts a task for loading a group incl. all it's children from ESI"""
    enabled_sections = [EveType.Section.DOGMAS.value] if force_loading_dogma else None
    update_or_create_eve_object.delay(
        model_name="EveGroup",
        id=group_id,
        include_children=True,
        wait_for_children=False,
        enabled_sections=enabled_sections,
        task_priority=EVEUNIVERSE_LOAD_TASKS_PRIORITY,
    )  # type: ignore


def _load_type_with_children(type_id: int, force_loading_dogma: bool = False) -> None:
    """Starts a task for loading a type incl. all it's children from ESI"""
    enabled_sections = [EveType.Section.DOGMAS.value] if force_loading_dogma else None
    update_or_create_eve_object.delay(
        model_name="EveType",
        id=type_id,
        include_children=False,
        wait_for_children=False,
        enabled_sections=enabled_sections,
        task_priority=EVEUNIVERSE_LOAD_TASKS_PRIORITY,
    )  # type: ignore


@shared_task(**_TASK_ESI_DEFAULTS_ONCE)
def load_ship_types(enabled_sections: Optional[List[str]] = None) -> None:
    """Load all ship types.

    Args:
        enabled_sections: Sections to load regardless of current settings
    """
    logger.info("Started loading all ship types into eveuniverse")
    _load_category_with_children(
        category_id=EveCategoryId.SHIP.value, enabled_sections=enabled_sections
    )


@shared_task(**_TASK_ESI_DEFAULTS_ONCE)
def load_structure_types(enabled_sections: Optional[List[str]] = None) -> None:
    """Load all structure types.

    Args:
        enabled_sections: Sections to load regardless of current settings
    """
    logger.info("Started loading all structure types into eveuniverse")
    _load_category_with_children(
        category_id=EveCategoryId.STRUCTURE.value, enabled_sections=enabled_sections
    )


@shared_task(**_TASK_ESI_DEFAULTS_ONCE)
def load_eve_types(
    category_ids: Optional[List[int]] = None,
    group_ids: Optional[List[int]] = None,
    type_ids: Optional[List[int]] = None,
    force_loading_dogma: bool = False,
) -> None:
    """Load specified eve types from ESI. Will always load all children except for EveType

    Args:
    - category_ids: EveCategory IDs
    - group_ids: EveGroup IDs
    - type_ids: EveType IDs
    - load_dogma: When True will load dogma for all types
    """
    logger.info("Started loading several eve types into eveuniverse")
    if category_ids:
        for category_id in category_ids:
            _load_category_with_children(category_id, force_loading_dogma)

    if group_ids:
        for group_id in group_ids:
            _load_group_with_children(group_id, force_loading_dogma)

    if type_ids:
        for type_id in type_ids:
            _load_type_with_children(type_id, force_loading_dogma)


@shared_task(**_TASK_ESI_DEFAULTS_ONCE)
def update_market_prices(minutes_until_stale: Optional[int] = None):
    """Updates market prices from ESI."""
    chain(
        _fetch_market_prices_esi.s().set(priority=EVEUNIVERSE_LOAD_TASKS_PRIORITY),
        _update_market_prices_from_data.s(minutes_until_stale).set(
            priority=EVEUNIVERSE_LOAD_TASKS_PRIORITY
        ),
    ).delay()


@shared_task(**_TASK_ESI_DEFAULTS_ONCE)
def _fetch_market_prices_esi():
    """Fetch market prices from ESI."""
    prices = EveMarketPrice.objects.fetch_data_from_esi()  # type: ignore
    return prices


@shared_task(**_TASK_DEFAULTS)
def _update_market_prices_from_data(
    prices: dict, minutes_until_stale: Optional[int] = None
):
    """Updates market prices from provided data."""
    if not prices:
        return

    EveMarketPrice.objects.update_objs_from_esi_data(prices, minutes_until_stale)  # type: ignore


@shared_task
def update_stale_entities(
    chunk_size: int = 950, expiration_time=EVEUNIVERSE_NAMES_EXPIRATION_TIME
) -> int:
    """Update stale EveEntity objects (alliances, characters and corporations only)
    and return the total number of stale objects.

    This task can be run on a regular basis (e.g. as periodic task)
    to ensure EveEntity names stay updated.

    Args:
        chunk_size: Maximum number of entity objects to be updated per task run
        expiration_time: Time in seconds after which an entity object becomes stale
    """
    if not is_esi_online():
        raise RuntimeError("ESI is not online. Aborted")

    oldest = now() - dt.timedelta(seconds=expiration_time)
    categories = [
        EveEntity.CATEGORY_ALLIANCE,
        EveEntity.CATEGORY_CHARACTER,
        EveEntity.CATEGORY_CORPORATION,
    ]
    ids_all = EveEntity.objects.filter(
        last_updated__lt=oldest, category__in=categories
    ).valid_ids()
    ids = [id for id in ids_all if not EveEntity.is_npc_id(id)]
    if not ids:
        logger.info("Found no entities with stale names")
        return 0

    logger.info("Starting to update %d entities with stale names", len(ids))
    for ids_chunk in chunks(ids, chunk_size):
        update_or_create_entities_from_esi.apply_async(
            kwargs={"ids": ids_chunk},
            priority=EVEUNIVERSE_LOAD_TASKS_PRIORITY,
        )

    return len(ids)


@shared_task(
    autoretry_for=(HTTPError,),
    retry_kwargs={"max_retries": 3},
    retry_backoff=True,
)
def update_or_create_entities_from_esi(ids: List[int]) -> int:
    """Updates or creates EveEntity objects from ESI.
    Returns how many objects where changed.
    """
    updated = EveEntity.objects.update_from_esi_by_id(ids)
    logger.info("Updated %d entities from ESI", updated)
    return updated
