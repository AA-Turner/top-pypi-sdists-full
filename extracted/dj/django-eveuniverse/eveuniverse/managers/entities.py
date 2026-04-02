"""Managers and Querysets for EveEntity models."""

import logging
import warnings
from collections import defaultdict
from typing import Any, Iterable, Optional, Set, Tuple

from bravado.exception import HTTPNotFound
from django.db import models
from django.db.utils import IntegrityError

from eveuniverse import __title__
from eveuniverse.app_settings import EVEUNIVERSE_BULK_METHODS_BATCH_SIZE
from eveuniverse.constants import POST_UNIVERSE_NAMES_MAX_ITEMS
from eveuniverse.helpers import EveEntityNameResolver
from eveuniverse.providers import esi
from eveuniverse.utils import LoggerAddTag, chunks

from .universe import EveUniverseEntityModelManager

logger = LoggerAddTag(logging.getLogger(__name__), __title__)

_ESI_INVALID_IDS = [1]  # Will never try to resolve these invalid IDs from ESI


class EveEntityQuerySet(models.QuerySet):
    """Custom queryset for EveEntity."""

    def update_from_esi(self) -> int:
        """Updates all Eve entity objects in this queryset from ESI.

        Return count of updated objs.
        """
        from eveuniverse.models import EveEntity

        return EveEntity.objects.update_from_esi_by_id(self.valid_ids())  # type: ignore

    def valid_ids(self) -> Set[int]:
        """Determine valid Ids in this Queryset."""
        return set(self.exclude(id__in=_ESI_INVALID_IDS).values_list("id", flat=True))


class EveEntityManagerBase(EveUniverseEntityModelManager):
    """Custom manager for EveEntity"""

    _MAX_DEPTH = 5  # max recursion depth when resolving IDs

    def bulk_create_esi(self, ids: Iterable[int]) -> int:
        """Resolve given IDs from ESI and update or create corresponding objects.

        `DEPRECATED` - please use ``bulk_resolve_ids()`` instead

        Args:
            ids: List of valid EveEntity IDs

        Returns:
            Count of updated entities
        """
        warnings.warn("Please use bulk_resolve_ids() instead.", DeprecationWarning)
        return self.bulk_resolve_ids(ids)

    def bulk_resolve_ids(self, ids: Iterable[int]) -> int:
        """Resolve given IDs from ESI and update or create corresponding objects.

        Args:
            ids: IDs to be resolved

        Returns:
            Count of updated entities
        """
        ids = set(map(int, ids))
        self._create_missing_objs(ids)

        to_update_qs: EveEntityQuerySet = self.filter(id__in=ids, name="")
        return to_update_qs.update_from_esi()

    def _create_missing_objs(self, ids: Set[int]) -> Set[int]:
        """Create missing objs and return their IDs."""
        existing_ids = set(self.filter(id__in=ids).values_list("id", flat=True))
        new_ids = ids.difference(existing_ids)

        if new_ids:
            objects = [self.model(id=id) for id in new_ids]
            self.bulk_create(
                objects,
                batch_size=EVEUNIVERSE_BULK_METHODS_BATCH_SIZE,
                ignore_conflicts=True,
            )  # type: ignore

        return new_ids

    def bulk_resolve_names(self, ids: Iterable[int]) -> EveEntityNameResolver:
        """Resolve given IDs to names and return them.

        Args:
            ids: List of valid EveEntity IDs

        Returns:
            EveEntityNameResolver object helpful for quick resolving a large amount
            of IDs
        """
        ids = set(map(int, ids))
        self.bulk_resolve_ids(ids)
        return EveEntityNameResolver(
            {
                row[0]: row[1]
                for row in self.filter(id__in=ids).values_list("id", "name")
            }
        )

    def bulk_update_all_esi(self):
        """Update all EveEntity objects in the database from ESI.

        Returns:
            Count of updated entities.
        """
        return self.all().update_from_esi()  # type: ignore

    def bulk_update_new_esi(self) -> int:
        """Update all unresolved EveEntity objects in the database from ESI.

        Returns:
            Count of updated entities.
        """
        return self.filter(name="").update_from_esi()  # type: ignore

    def fetch_by_names_esi(
        self, names: Iterable[str], update: bool = False
    ) -> models.QuerySet:
        """Fetch entities matching given names.
        Will fetch missing entities from ESI if needed or requested.

        Note that names that are not found by ESI are ignored.

        Args:
            names: Names of entities to fetch
            update: When True will always update from ESI

        Returns:
            query with matching entities.
        """
        names = set(names)
        if update:
            names_to_fetch = names
        else:
            existing_names = set(
                self.filter(name__in=names).values_list("name", flat=True)
            )
            names_to_fetch = names - existing_names
        if names_to_fetch:
            esi_result = self._fetch_names_from_esi(names_to_fetch)
            if esi_result:
                self._update_or_create_entities(esi_result)
        return self.filter(name__in=names)

    def _fetch_names_from_esi(self, names: Iterable[str]) -> dict:
        logger.info("Trying to fetch EveEntities from ESI by name")
        result = defaultdict(list)
        for chunk_names in chunks(list(names), 500):
            result_chunk = esi.client.Universe.post_universe_ids(
                names=chunk_names
            ).results()
            for category, entities in result_chunk.items():
                if entities:
                    result[category] += entities
        result_compressed = {
            category: entities for category, entities in result.items() if entities
        }
        return result_compressed

    def _update_or_create_entities(self, esi_result):
        for category_key, entities in esi_result.items():
            try:
                category = self._map_category_key_to_category(category_key)
            except ValueError:
                logger.warning(
                    "Ignoring entities with unknown category %s: %s",
                    category_key,
                    entities,
                )
                continue

            for entity in entities:
                self.update_or_create(
                    id=entity["id"],
                    defaults={"name": entity["name"], "category": category},
                )

    def _map_category_key_to_category(self, category_key: str) -> str:
        """Map category keys from ESI result to categories."""
        my_map = {
            "alliances": self.model.CATEGORY_ALLIANCE,
            "characters": self.model.CATEGORY_CHARACTER,
            "constellations": self.model.CATEGORY_CONSTELLATION,
            "corporations": self.model.CATEGORY_CORPORATION,
            "factions": self.model.CATEGORY_FACTION,
            "inventory_types": self.model.CATEGORY_INVENTORY_TYPE,
            "regions": self.model.CATEGORY_REGION,
            "systems": self.model.CATEGORY_SOLAR_SYSTEM,
            "stations": self.model.CATEGORY_STATION,
        }
        try:
            return my_map[category_key]
        except KeyError:
            raise ValueError(f"Invalid category: {category_key}") from None

    def get_queryset(self) -> models.QuerySet:
        """:meta private:"""
        return EveEntityQuerySet(self.model, using=self._db)

    def get_or_create_esi(
        self,
        *,
        id: int,
        include_children: bool = False,
        wait_for_children: bool = True,
        enabled_sections: Optional[Iterable[str]] = None,
        task_priority: Optional[int] = None,
    ) -> Tuple[Any, bool]:
        """gets or creates an EvEntity object.

        The object is automatically fetched from ESI if it does not exist (blocking)
        or if it has not yet been resolved.

        Args:
            id: Eve Online ID of object

        Returns:
            A tuple consisting of the requested EveEntity object and a created flag
            Returns a None objects if the ID is invalid
        """
        id = int(id)
        try:
            obj = self.exclude(name="").get(id=id)
            created = False
        except self.model.DoesNotExist:
            obj, created = self.update_or_create_esi(
                id=id,
                include_children=include_children,
                wait_for_children=wait_for_children,
            )

        return obj, created

    def resolve_name(self, id: int) -> str:
        """Return the name for the given Eve entity ID
        or an empty string if ID is not valid.
        """
        if id is not None:
            obj, _ = self.get_or_create_esi(id=int(id))
            if obj:
                return obj.name
        return ""

    def update_or_create_esi(
        self,
        *,
        id: int,
        include_children: bool = False,
        wait_for_children: bool = True,
        enabled_sections: Optional[Iterable[str]] = None,
        task_priority: Optional[int] = None,
    ) -> Tuple[Any, bool]:
        """Update or create an EveEntity object by fetching it from ESI (blocking).

        Args:
            id: Eve Online ID of object
            include_children: (no effect)
            wait_for_children: (no effect)

        Returns:
            A tuple consisting of the requested object and a created flag
            When the ID is invalid the returned object will be None

        Exceptions:
            Raises all HTTP codes of ESI endpoint /universe/names except 404
        """
        id = int(id)
        logger.info("%s: Trying to resolve ID to EveEntity with ESI", id)
        if id in _ESI_INVALID_IDS:
            logger.info("%s: ID is not valid", id)
            return None, False
        try:
            result = esi.client.Universe.post_universe_names(ids=[id]).results()
        except HTTPNotFound:
            logger.info("%s: ID is not valid", id)
            return None, False
        item = result[0]
        return self.update_or_create(
            id=item.get("id"),
            defaults={"name": item.get("name"), "category": item.get("category")},
        )

    def update_or_create_all_esi(
        self,
        *,
        include_children: bool = False,
        wait_for_children: bool = True,
        enabled_sections: Optional[Iterable[str]] = None,
        task_priority: Optional[int] = None,
    ) -> None:
        """not implemented - do not use"""
        raise NotImplementedError()

    def update_from_esi_by_id(self, ids: Iterable[int]) -> int:
        """Updates all Eve entity objects by id from ESI."""
        if not ids:
            return 0
        ids = list(set((int(id) for id in ids if id not in _ESI_INVALID_IDS)))
        logger.info("Updating %d entities from ESI", len(ids))
        resolved_counter = 0
        for chunk_ids in chunks(ids, POST_UNIVERSE_NAMES_MAX_ITEMS):
            logger.debug("Trying to resolve the following IDs from ESI:\n%s", chunk_ids)
            resolved_counter = self._resolve_entities_from_esi(chunk_ids)
        return resolved_counter

    def _resolve_entities_from_esi(self, ids: list, depth: int = 1):
        resolved_counter = 0
        try:
            items = esi.client.Universe.post_universe_names(ids=ids).results()
        except HTTPNotFound:
            # if API fails to resolve all IDs, we divide and conquer,
            # trying to resolve each half of the ids separately
            if len(ids) > 1 and depth < self._MAX_DEPTH:
                resolved_counter += self._resolve_entities_from_esi(ids[::2], depth + 1)
                resolved_counter += self._resolve_entities_from_esi(
                    ids[1::2], depth + 1
                )
            else:
                logger.warning("Failed to resolve invalid IDs: %s", ids)
        else:
            resolved_counter += len(items)
            for item in items:
                try:
                    self.update_or_create(
                        id=item["id"],
                        defaults={"name": item["name"], "category": item["category"]},
                    )
                except IntegrityError:
                    pass
        return resolved_counter


EveEntityManager = EveEntityManagerBase.from_queryset(EveEntityQuerySet)
