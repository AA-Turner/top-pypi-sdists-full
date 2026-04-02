"""Eve universe models Part 2/2, containing location related models."""

# pylint: disable = too-few-public-methods

import logging
import math
import re
from collections import namedtuple
from typing import Iterable, List, Optional, Set

from bitfield import BitField
from django.db import models
from django.utils.functional import cached_property

from eveuniverse.constants import EveGroupId, EveRegionId
from eveuniverse.core import dotlan, evesdeapi
from eveuniverse.managers import (
    EveAsteroidBeltManager,
    EveMoonManager,
    EvePlanetManager,
    EveStargateManager,
)
from eveuniverse.providers import esi

from .base import EveUniverseEntityModel, _SectionBase, determine_effective_sections
from .entities import EveEntity
from .universe_1 import EveType

logger = logging.getLogger(__name__)


class EveAsteroidBelt(EveUniverseEntityModel):
    """An asteroid belt in Eve Online"""

    eve_planet = models.ForeignKey(
        "EvePlanet", on_delete=models.CASCADE, related_name="eve_asteroid_belts"
    )
    position_x = models.FloatField(
        null=True, default=None, blank=True, help_text="x position in the solar system"
    )
    position_y = models.FloatField(
        null=True, default=None, blank=True, help_text="y position in the solar system"
    )
    position_z = models.FloatField(
        null=True, default=None, blank=True, help_text="z position in the solar system"
    )

    objects = EveAsteroidBeltManager()

    class _EveUniverseMeta:
        esi_pk = "asteroid_belt_id"
        esi_path_object = "Universe.get_universe_asteroid_belts_asteroid_belt_id"
        field_mappings = {
            "eve_planet": "planet_id",
            "position_x": ("position", "x"),
            "position_y": ("position", "y"),
            "position_z": ("position", "z"),
        }
        load_order = 200


class EveConstellation(EveUniverseEntityModel):
    """A star constellation in Eve Online"""

    eve_region = models.ForeignKey(
        "EveRegion", on_delete=models.CASCADE, related_name="eve_constellations"
    )
    position_x = models.FloatField(
        null=True, default=None, blank=True, help_text="x position in the solar system"
    )
    position_y = models.FloatField(
        null=True, default=None, blank=True, help_text="y position in the solar system"
    )
    position_z = models.FloatField(
        null=True, default=None, blank=True, help_text="z position in the solar system"
    )

    class _EveUniverseMeta:
        esi_pk = "constellation_id"
        esi_path_list = "Universe.get_universe_constellations"
        esi_path_object = "Universe.get_universe_constellations_constellation_id"
        field_mappings = {
            "eve_region": "region_id",
            "position_x": ("position", "x"),
            "position_y": ("position", "y"),
            "position_z": ("position", "z"),
        }
        children = {"systems": "EveSolarSystem"}
        load_order = 192

    @classmethod
    def eve_entity_category(cls) -> str:
        return EveEntity.CATEGORY_CONSTELLATION


class EveMoon(EveUniverseEntityModel):
    """A moon in Eve Online"""

    eve_planet = models.ForeignKey(
        "EvePlanet", on_delete=models.CASCADE, related_name="eve_moons"
    )
    position_x = models.FloatField(
        null=True, default=None, blank=True, help_text="x position in the solar system"
    )
    position_y = models.FloatField(
        null=True, default=None, blank=True, help_text="y position in the solar system"
    )
    position_z = models.FloatField(
        null=True, default=None, blank=True, help_text="z position in the solar system"
    )

    objects = EveMoonManager()

    class _EveUniverseMeta:
        esi_pk = "moon_id"
        esi_path_object = "Universe.get_universe_moons_moon_id"
        field_mappings = {
            "eve_planet": "planet_id",
            "position_x": ("position", "x"),
            "position_y": ("position", "y"),
            "position_z": ("position", "z"),
        }
        load_order = 220


class EvePlanet(EveUniverseEntityModel):
    """A planet in Eve Online"""

    class Section(_SectionBase):
        """Sections that can be optionally loaded with each instance"""

        ASTEROID_BELTS = "asteroid_belts"  #:
        MOONS = "moons"  #:

    eve_solar_system = models.ForeignKey(
        "EveSolarSystem", on_delete=models.CASCADE, related_name="eve_planets"
    )
    eve_type = models.ForeignKey(
        "EveType", on_delete=models.CASCADE, related_name="eve_planets"
    )
    position_x = models.FloatField(
        null=True, default=None, blank=True, help_text="x position in the solar system"
    )
    position_y = models.FloatField(
        null=True, default=None, blank=True, help_text="y position in the solar system"
    )
    position_z = models.FloatField(
        null=True, default=None, blank=True, help_text="z position in the solar system"
    )
    enabled_sections = BitField(
        flags=tuple(Section.values()),
        help_text=(
            "Flags for loadable sections. True if instance was loaded with section."
        ),  # no index, because MySQL does not support it for bitwise operations
    )  # type: ignore

    objects = EvePlanetManager()

    class _EveUniverseMeta:
        esi_pk = "planet_id"
        esi_path_object = "Universe.get_universe_planets_planet_id"
        field_mappings = {
            "eve_solar_system": "system_id",
            "eve_type": "type_id",
            "position_x": ("position", "x"),
            "position_y": ("position", "y"),
            "position_z": ("position", "z"),
        }
        children = {"moons": "EveMoon", "asteroid_belts": "EveAsteroidBelt"}
        load_order = 205

    def type_name(self) -> str:
        """Return shortened name of planet type.

        Note: Accesses the eve_type object.
        """
        matches = re.findall(r"Planet \((\S*)\)", self.eve_type.name)
        return matches[0] if matches else ""

    @classmethod
    def _children(cls, enabled_sections: Optional[Set[str]] = None) -> dict:
        enabled_sections = determine_effective_sections(enabled_sections)
        children = {}
        if cls.Section.ASTEROID_BELTS in enabled_sections:
            children["asteroid_belts"] = "EveAsteroidBelt"
        if cls.Section.MOONS in enabled_sections:
            children["moons"] = "EveMoon"
        return children


class EveRegion(EveUniverseEntityModel):
    """A star region in Eve Online"""

    description = models.TextField(default="")

    class _EveUniverseMeta:
        esi_pk = "region_id"
        esi_path_list = "Universe.get_universe_regions"
        esi_path_object = "Universe.get_universe_regions_region_id"
        children = {"constellations": "EveConstellation"}
        load_order = 190

    @property
    def profile_url(self) -> str:
        """URL to default third party website with profile info about this entity."""
        return dotlan.region_url(self.name)

    @classmethod
    def eve_entity_category(cls) -> str:
        return EveEntity.CATEGORY_REGION


class EveSolarSystem(EveUniverseEntityModel):
    """A solar system in Eve Online"""

    class Section(_SectionBase):
        """Sections that can be optionally loaded with each instance"""

        PLANETS = "planets"  #:
        STARGATES = "stargates"  #:
        STARS = "stars"  #:
        STATIONS = "stations"  #:

    eve_constellation = models.ForeignKey(
        "EveConstellation", on_delete=models.CASCADE, related_name="eve_solarsystems"
    )
    eve_star = models.OneToOneField(
        "EveStar",
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True,
        related_name="eve_solarsystem",
    )
    position_x = models.FloatField(
        null=True, default=None, blank=True, help_text="x position in the solar system"
    )
    position_y = models.FloatField(
        null=True, default=None, blank=True, help_text="y position in the solar system"
    )
    position_z = models.FloatField(
        null=True, default=None, blank=True, help_text="z position in the solar system"
    )
    security_status = models.FloatField()
    enabled_sections = BitField(
        flags=tuple(Section.values()),
        help_text=(
            "Flags for loadable sections. True if instance was loaded with section."
        ),  # no index, because MySQL does not support it for bitwise operations
    )  # type: ignore

    class _EveUniverseMeta:
        esi_pk = "system_id"
        esi_path_list = "Universe.get_universe_systems"
        esi_path_object = "Universe.get_universe_systems_system_id"
        field_mappings = {
            "eve_constellation": "constellation_id",
            "eve_star": "star_id",
            "position_x": ("position", "x"),
            "position_y": ("position", "y"),
            "position_z": ("position", "z"),
        }
        children = {}
        load_order = 194

    NearestCelestial = namedtuple(
        "NearestCelestial", ["eve_type", "eve_object", "distance"]
    )
    NearestCelestial.__doc__ = "Container for a nearest celestial"

    @property
    def profile_url(self) -> str:
        """Return URL to default third party website
        with profile info about this solar system.
        """
        return dotlan.solar_system_url(self.name)

    @property
    def is_high_sec(self) -> bool:
        """Return True when this solar system is in high sec, else False."""
        return self.security_status >= 0.45

    @property
    def is_low_sec(self) -> bool:
        """Return True when this solar system is in low sec, else False."""
        return 0.0 < self.security_status < 0.45

    @property
    def is_null_sec(self) -> bool:
        """Return True when this solar system is in null sec, else False."""
        return (
            not self.is_w_space
            and not self.is_trig_space
            and not self.is_abyssal_deadspace
            and self.security_status <= 0.0
            and not self.is_w_space
        )

    @property
    def is_w_space(self) -> bool:
        """Return True when this solar system is in wormhole space, else False."""
        return 31_000_000 <= self.id < 32_000_000

    @cached_property
    def is_trig_space(self) -> bool:
        """Return True when this solar system is in Triglavian space, else False."""
        return self.eve_constellation.eve_region_id == EveRegionId.POCHVEN

    @property
    def is_abyssal_deadspace(self) -> bool:
        """Return True when this solar system is in abyssal deadspace, else False."""
        return 32_000_000 <= self.id < 33_000_000

    @classmethod
    def eve_entity_category(cls) -> str:
        """Return related EveEntity category."""
        return EveEntity.CATEGORY_SOLAR_SYSTEM

    def distance_to(self, destination: "EveSolarSystem") -> Optional[float]:
        """Calculates the distance in meters between the current and the given solar system

        Args:
            destination: Other solar system to use in calculation

        Returns:
            Distance in meters or None if one of the systems is in WH space
        """
        if not self.position_x or not self.position_y or not self.position_z:
            return None
        if (
            not destination
            or not destination.position_x
            or not destination.position_y
            or not destination.position_z
        ):
            return None

        if (
            self.is_w_space
            or destination.is_w_space
            or self.is_trig_space
            or destination.is_trig_space
        ):
            return None

        return math.sqrt(
            (destination.position_x - self.position_x) ** 2
            + (destination.position_y - self.position_y) ** 2
            + (destination.position_z - self.position_z) ** 2
        )

    def route_to(
        self, destination: "EveSolarSystem"
    ) -> Optional[List["EveSolarSystem"]]:
        """Calculates the shortest route between the current and the given solar system

        Args:
            destination: Other solar system to use in calculation

        Returns:
            List of solar system objects incl. origin and destination
            or None if no route can be found (e.g. if one system is in WH space)
        """
        if (
            self.is_w_space
            or destination.is_w_space
            or self.is_trig_space
            or destination.is_trig_space
        ):
            return None

        path_ids = self._calc_route_esi(self.id, destination.id)
        if path_ids is None:
            return None

        return [
            EveSolarSystem.objects.get_or_create_esi(id=solar_system_id)  # type: ignore
            for solar_system_id in path_ids
        ]

    def jumps_to(self, destination: "EveSolarSystem") -> Optional[int]:
        """Calculates the shortest route between the current and the given solar system

        Args:
            destination: Other solar system to use in calculation

        Returns:
            Number of total jumps
            or None if no route can be found (e.g. if one system is in WH space)
        """
        if (
            self.is_w_space
            or destination.is_w_space
            or self.is_trig_space
            or destination.is_trig_space
        ):
            return None

        path_ids = self._calc_route_esi(self.id, destination.id)
        return len(path_ids) - 1 if path_ids is not None else None

    @staticmethod
    def _calc_route_esi(origin_id: int, destination_id: int) -> Optional[List[int]]:
        """returns the shortest route between two given solar systems.

        Route is calculated by ESI

        Args:
            destination_id: ID of the other solar system to use in calculation

        Returns:
            List of solar system IDs incl. origin and destination
            or None if no route can be found (e.g. if one system is in WH space)
        """

        try:
            return esi.client.Routes.get_route_origin_destination(
                origin=origin_id, destination=destination_id
            ).results()
        except OSError:  # FIXME: ESI is supposed to return 404,
            # but django-esi is actually returning an OSError
            return None

    def nearest_celestial(
        self, x: int, y: int, z: int, group_id: Optional[int] = None
    ) -> Optional[NearestCelestial]:
        """Determine nearest celestial to given coordinates as eveuniverse object.

        Args:
            x, y, z: Start point in space to look from
            group_id: Eve ID of group to filter results by

        Raises:
            HTTPError: If an HTTP error is encountered
            ValueError: If there is an semantic issue

        Returns:
            Eve item or None if none is found
        """
        item = evesdeapi.nearest_celestial(
            solar_system_id=self.id, x=x, y=y, z=z, group_id=group_id
        )
        if not item:
            return None
        eve_type, _ = EveType.objects.get_or_create_esi(id=item.type_id)  # type: ignore
        class_mapping = {
            EveGroupId.ASTEROID_BELT: EveAsteroidBelt,
            EveGroupId.MOON: EveMoon,
            EveGroupId.PLANET: EvePlanet,
            EveGroupId.STAR: EveStar,
            EveGroupId.STARGATE: EveStargate,
            EveGroupId.STATION: EveStation,
        }
        try:
            my_class = class_mapping[eve_type.eve_group_id]
        except KeyError:
            logger.debug(
                "Nearest celestial returned from API has unexpected type ID: %d",
                eve_type.id,
            )
            return None
        obj, _ = my_class.objects.get_or_create_esi(id=item.id)
        result = self.NearestCelestial(
            eve_type=eve_type, eve_object=obj, distance=item.distance
        )
        return result

    @classmethod
    def _children(cls, enabled_sections: Optional[Set[str]] = None) -> dict:
        enabled_sections = determine_effective_sections(enabled_sections)
        children = {}
        if cls.Section.PLANETS in enabled_sections:
            children["planets"] = "EvePlanet"
        if cls.Section.STARGATES in enabled_sections:
            children["stargates"] = "EveStargate"
        if cls.Section.STATIONS in enabled_sections:
            children["stations"] = "EveStation"
        return children

    @classmethod
    def _disabled_fields(cls, enabled_sections: Optional[Set[str]] = None) -> set:
        enabled_sections = determine_effective_sections(enabled_sections)
        if cls.Section.STARS not in enabled_sections:
            return {"eve_star"}
        return set()

    @classmethod
    def _inline_objects(cls, enabled_sections: Optional[Set[str]] = None) -> dict:
        if not enabled_sections or cls.Section.PLANETS not in enabled_sections:
            return {}
        return super()._inline_objects()


class EveStar(EveUniverseEntityModel):
    """A star in Eve Online"""

    age = models.BigIntegerField()
    eve_type = models.ForeignKey(
        "EveType", on_delete=models.CASCADE, related_name="eve_stars"
    )
    luminosity = models.FloatField()
    radius = models.PositiveIntegerField()
    spectral_class = models.CharField(max_length=16)
    temperature = models.PositiveIntegerField()

    class _EveUniverseMeta:
        esi_pk = "star_id"
        esi_path_object = "Universe.get_universe_stars_star_id"
        field_mappings = {"eve_type": "type_id"}
        load_order = 222


class EveStargate(EveUniverseEntityModel):
    """A stargate in Eve Online"""

    destination_eve_stargate = models.OneToOneField(
        "EveStargate", on_delete=models.SET_DEFAULT, null=True, default=None, blank=True
    )
    destination_eve_solar_system = models.ForeignKey(
        "EveSolarSystem",
        on_delete=models.SET_DEFAULT,
        null=True,
        default=None,
        blank=True,
        related_name="destination_eve_stargates",
    )
    eve_solar_system = models.ForeignKey(
        "EveSolarSystem", on_delete=models.CASCADE, related_name="eve_stargates"
    )
    eve_type = models.ForeignKey(
        "EveType", on_delete=models.CASCADE, related_name="eve_stargates"
    )
    position_x = models.FloatField(
        null=True, default=None, blank=True, help_text="x position in the solar system"
    )
    position_y = models.FloatField(
        null=True, default=None, blank=True, help_text="y position in the solar system"
    )
    position_z = models.FloatField(
        null=True, default=None, blank=True, help_text="z position in the solar system"
    )

    objects = EveStargateManager()

    class _EveUniverseMeta:
        esi_pk = "stargate_id"
        esi_path_object = "Universe.get_universe_stargates_stargate_id"
        field_mappings = {
            "destination_eve_stargate": ("destination", "stargate_id"),
            "destination_eve_solar_system": ("destination", "system_id"),
            "eve_solar_system": "system_id",
            "eve_type": "type_id",
            "position_x": ("position", "x"),
            "position_y": ("position", "y"),
            "position_z": ("position", "z"),
        }
        dont_create_related = {
            "destination_eve_stargate",
            "destination_eve_solar_system",
        }
        load_order = 224


class EveStation(EveUniverseEntityModel):
    """A space station in Eve Online"""

    eve_race = models.ForeignKey(
        "EveRace",
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True,
        related_name="eve_stations",
    )
    eve_solar_system = models.ForeignKey(
        "EveSolarSystem",
        on_delete=models.CASCADE,
        related_name="eve_stations",
    )
    eve_type = models.ForeignKey(
        "EveType",
        on_delete=models.CASCADE,
        related_name="eve_stations",
    )
    max_dockable_ship_volume = models.FloatField()
    office_rental_cost = models.FloatField()
    owner_id = models.PositiveIntegerField(default=None, null=True, db_index=True)
    position_x = models.FloatField(
        null=True, default=None, blank=True, help_text="x position in the solar system"
    )
    position_y = models.FloatField(
        null=True, default=None, blank=True, help_text="y position in the solar system"
    )
    position_z = models.FloatField(
        null=True, default=None, blank=True, help_text="z position in the solar system"
    )
    reprocessing_efficiency = models.FloatField()
    reprocessing_stations_take = models.FloatField()
    services = models.ManyToManyField("EveStationService")

    class _EveUniverseMeta:
        esi_pk = "station_id"
        esi_path_object = "Universe.get_universe_stations_station_id"
        field_mappings = {
            "eve_race": "race_id",
            "eve_solar_system": "system_id",
            "eve_type": "type_id",
            "owner_id": "owner",
            "position_x": ("position", "x"),
            "position_y": ("position", "y"),
            "position_z": ("position", "z"),
        }
        inline_objects = {"services": "EveStationService"}
        load_order = 207

    @classmethod
    def eve_entity_category(cls) -> str:
        return EveEntity.CATEGORY_STATION

    @classmethod
    def _update_or_create_inline_objects(
        cls,
        *,
        parent_eve_data_obj: dict,
        parent_obj,
        wait_for_children: bool,
        enabled_sections: Iterable[str],
        task_priority: Optional[int] = None,
    ) -> None:
        """updates_or_creates station service objects for EveStations"""

        if "services" in parent_eve_data_obj:
            services = []
            for service_name in parent_eve_data_obj["services"]:
                service, _ = EveStationService.objects.get_or_create(name=service_name)
                services.append(service)

            if services:
                parent_obj.services.add(*services)


class EveStationService(models.Model):
    """A service in a space station"""

    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name
