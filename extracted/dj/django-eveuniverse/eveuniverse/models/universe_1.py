"""Eve universe models Part 1/2, containing non location related models."""

# pylint: disable = too-few-public-methods

import enum
from typing import Optional, Set

from bitfield import BitField
from django.contrib.staticfiles.storage import staticfiles_storage
from django.db import models

from eveuniverse.app_settings import EVEUNIVERSE_USE_EVESKINSERVER
from eveuniverse.constants import EveCategoryId
from eveuniverse.core import dotlan, eveimageserver, eveitems, eveskinserver
from eveuniverse.managers import EveMarketPriceManager, EveTypeManager

from .base import (
    _NAMES_MAX_LENGTH,
    EveUniverseEntityModel,
    EveUniverseInlineModel,
    _SectionBase,
    determine_effective_sections,
)
from .entities import EveEntity


class EveAncestry(EveUniverseEntityModel):
    """An ancestry in Eve Online"""

    eve_bloodline = models.ForeignKey(
        "EveBloodline", on_delete=models.CASCADE, related_name="eve_bloodlines"
    )
    description = models.TextField()
    icon_id = models.PositiveIntegerField(default=None, null=True, db_index=True)
    short_description = models.TextField(default="")

    class _EveUniverseMeta:
        esi_pk = "id"
        esi_path_list = "Universe.get_universe_ancestries"
        esi_path_object = "Universe.get_universe_ancestries"
        field_mappings = {"eve_bloodline": "bloodline_id"}
        load_order = 180


class EveBloodline(EveUniverseEntityModel):
    """A bloodline in Eve Online"""

    eve_race = models.ForeignKey(
        "EveRace",
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True,
        related_name="eve_bloodlines",
    )
    eve_ship_type = models.ForeignKey(
        "EveType", on_delete=models.CASCADE, related_name="eve_bloodlines"
    )
    charisma = models.PositiveIntegerField()
    corporation_id = models.PositiveIntegerField()
    description = models.TextField()
    intelligence = models.PositiveIntegerField()
    memory = models.PositiveIntegerField()
    perception = models.PositiveIntegerField()
    willpower = models.PositiveIntegerField()

    class _EveUniverseMeta:
        esi_pk = "bloodline_id"
        esi_path_list = "Universe.get_universe_bloodlines"
        esi_path_object = "Universe.get_universe_bloodlines"
        field_mappings = {"eve_race": "race_id", "eve_ship_type": "ship_type_id"}
        load_order = 170


class EveCategory(EveUniverseEntityModel):
    """An inventory category in Eve Online"""

    published = models.BooleanField()

    class _EveUniverseMeta:
        esi_pk = "category_id"
        esi_path_list = "Universe.get_universe_categories"
        esi_path_object = "Universe.get_universe_categories_category_id"
        children = {"groups": "EveGroup"}
        load_order = 130


class EveDogmaAttribute(EveUniverseEntityModel):
    """A dogma attribute in Eve Online"""

    eve_unit = models.ForeignKey(
        "EveUnit",
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True,
        related_name="eve_units",
    )
    default_value = models.FloatField(default=None, null=True)
    description = models.TextField(default="")
    display_name = models.CharField(max_length=_NAMES_MAX_LENGTH, default="")
    high_is_good = models.BooleanField(default=None, null=True)
    icon_id = models.PositiveIntegerField(default=None, null=True, db_index=True)
    published = models.BooleanField(default=None, null=True)
    stackable = models.BooleanField(default=None, null=True)

    class _EveUniverseMeta:
        esi_pk = "attribute_id"
        esi_path_list = "Dogma.get_dogma_attributes"
        esi_path_object = "Dogma.get_dogma_attributes_attribute_id"
        field_mappings = {"eve_unit": "unit_id"}
        load_order = 140


class EveDogmaEffect(EveUniverseEntityModel):
    """A dogma effect in Eve Online"""

    # we need to redefine the name field, because effect names can be very long
    name = models.CharField(
        max_length=400,
        default="",
        db_index=True,
        help_text="Eve Online name",
    )

    description = models.TextField(default="")
    disallow_auto_repeat = models.BooleanField(default=None, null=True)
    discharge_attribute = models.ForeignKey(
        "EveDogmaAttribute",
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True,
        related_name="discharge_attribute_effects",
    )
    display_name = models.CharField(max_length=_NAMES_MAX_LENGTH, default="")
    duration_attribute = models.ForeignKey(
        "EveDogmaAttribute",
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True,
        related_name="duration_attribute_effects",
    )
    effect_category = models.PositiveIntegerField(default=None, null=True)
    electronic_chance = models.BooleanField(default=None, null=True)
    falloff_attribute = models.ForeignKey(
        "EveDogmaAttribute",
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True,
        related_name="falloff_attribute_effects",
    )
    icon_id = models.PositiveIntegerField(default=None, null=True, db_index=True)
    is_assistance = models.BooleanField(default=None, null=True)
    is_offensive = models.BooleanField(default=None, null=True)
    is_warp_safe = models.BooleanField(default=None, null=True)
    post_expression = models.PositiveIntegerField(default=None, null=True)
    pre_expression = models.PositiveIntegerField(default=None, null=True)
    published = models.BooleanField(default=None, null=True)
    range_attribute = models.ForeignKey(
        "EveDogmaAttribute",
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True,
        related_name="range_attribute_effects",
    )
    range_chance = models.BooleanField(default=None, null=True)
    tracking_speed_attribute = models.ForeignKey(
        "EveDogmaAttribute",
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True,
        related_name="tracking_speed_attribute_effects",
    )

    class _EveUniverseMeta:
        esi_pk = "effect_id"
        esi_path_list = "Dogma.get_dogma_effects"
        esi_path_object = "Dogma.get_dogma_effects_effect_id"
        field_mappings = {
            "discharge_attribute": "discharge_attribute_id",
            "duration_attribute": "duration_attribute_id",
            "falloff_attribute": "falloff_attribute_id",
            "range_attribute": "range_attribute_id",
            "tracking_speed_attribute": "tracking_speed_attribute_id",
        }
        inline_objects = {
            "modifiers": "EveDogmaEffectModifier",
        }
        load_order = 142


class EveDogmaEffectModifier(EveUniverseInlineModel):
    """A modifier for a dogma effect in Eve Online"""

    domain = models.CharField(max_length=_NAMES_MAX_LENGTH, default="")
    eve_dogma_effect = models.ForeignKey(
        "EveDogmaEffect", on_delete=models.CASCADE, related_name="modifiers"
    )
    func = models.CharField(max_length=_NAMES_MAX_LENGTH)
    modified_attribute = models.ForeignKey(
        "EveDogmaAttribute",
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True,
        related_name="modified_attribute_modifiers",
    )
    modifying_attribute = models.ForeignKey(
        "EveDogmaAttribute",
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True,
        related_name="modifying_attribute_modifiers",
    )
    modifying_effect = models.ForeignKey(
        "EveDogmaEffect",
        on_delete=models.SET_DEFAULT,
        null=True,
        default=None,
        blank=True,
        related_name="modifying_effect_modifiers",
    )
    operator = models.IntegerField(default=None, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["eve_dogma_effect", "func"],
                name="fpk_evedogmaeffectmodifier",
            )
        ]

    class _EveUniverseMeta:
        parent_fk = "eve_dogma_effect"
        functional_pk = [
            "eve_dogma_effect",
            "func",
        ]
        field_mappings = {
            "modified_attribute": "modified_attribute_id",
            "modifying_attribute": "modifying_attribute_id",
            "modifying_effect": "effect_id",
        }
        load_order = 144


class EveUnit(EveUniverseEntityModel):
    """A unit in Eve Online"""

    display_name = models.CharField(max_length=50, default="")
    description = models.TextField(default="")

    objects = models.Manager()

    class _EveUniverseMeta:
        esi_pk = "unit_id"
        esi_path_object = None
        field_mappings = {
            "unit_id": "id",
            "unit_name": "name",
        }
        load_order = 100


class EveFaction(EveUniverseEntityModel):
    """A faction in Eve Online"""

    corporation_id = models.PositiveIntegerField(default=None, null=True, db_index=True)
    description = models.TextField()
    eve_solar_system = models.ForeignKey(
        "EveSolarSystem",
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True,
        related_name="eve_factions",
    )
    is_unique = models.BooleanField()
    militia_corporation_id = models.PositiveIntegerField(
        default=None, null=True, db_index=True
    )
    size_factor = models.FloatField()
    station_count = models.PositiveIntegerField()
    station_system_count = models.PositiveIntegerField()

    class _EveUniverseMeta:
        esi_pk = "faction_id"
        esi_path_list = "Universe.get_universe_factions"
        esi_path_object = "Universe.get_universe_factions"
        field_mappings = {"eve_solar_system": "solar_system_id"}
        load_order = 210

    @property
    def profile_url(self) -> str:
        """URL to default third party website with profile info about this entity."""
        return dotlan.faction_url(self.name)

    def logo_url(self, size=EveUniverseEntityModel._DEFAULT_ICON_SIZE) -> str:
        """returns an image URL for this faction

        Args:
            size: optional size of the image
        """
        return eveimageserver.faction_logo_url(self.id, size=size)

    @classmethod
    def eve_entity_category(cls) -> str:
        return EveEntity.CATEGORY_FACTION


class EveGraphic(EveUniverseEntityModel):
    """A graphic in Eve Online"""

    FILENAME_MAX_CHARS = 255

    collision_file = models.CharField(max_length=FILENAME_MAX_CHARS, default="")
    graphic_file = models.CharField(max_length=FILENAME_MAX_CHARS, default="")
    icon_folder = models.CharField(max_length=FILENAME_MAX_CHARS, default="")
    sof_dna = models.CharField(max_length=FILENAME_MAX_CHARS, default="")
    sof_fation_name = models.CharField(max_length=FILENAME_MAX_CHARS, default="")
    sof_hull_name = models.CharField(max_length=FILENAME_MAX_CHARS, default="")
    sof_race_name = models.CharField(max_length=FILENAME_MAX_CHARS, default="")

    class _EveUniverseMeta:
        esi_pk = "graphic_id"
        esi_path_list = "Universe.get_universe_graphics"
        esi_path_object = "Universe.get_universe_graphics_graphic_id"
        load_order = 120


class EveGroup(EveUniverseEntityModel):
    """An inventory group in Eve Online"""

    eve_category = models.ForeignKey(
        "EveCategory", on_delete=models.CASCADE, related_name="eve_groups"
    )
    published = models.BooleanField()

    class _EveUniverseMeta:
        esi_pk = "group_id"
        esi_path_list = "Universe.get_universe_groups"
        esi_path_object = "Universe.get_universe_groups_group_id"
        field_mappings = {"eve_category": "category_id"}
        children = {"types": "EveType"}
        load_order = 132


class EveMarketGroup(EveUniverseEntityModel):
    """A market group in Eve Online"""

    description = models.TextField()
    parent_market_group = models.ForeignKey(
        "self",
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True,
        related_name="market_group_children",
    )

    class _EveUniverseMeta:
        esi_pk = "market_group_id"
        esi_path_list = "Market.get_markets_groups"
        esi_path_object = "Market.get_markets_groups_market_group_id"
        field_mappings = {"parent_market_group": "parent_group_id"}
        children = {"types": "EveType"}
        load_order = 230


class EveMarketPrice(models.Model):
    """A market price of an Eve Online type"""

    DEFAULT_MINUTES_UNTIL_STALE = 60

    eve_type = models.OneToOneField(
        "EveType",
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="market_price",
    )
    adjusted_price = models.FloatField(default=None, null=True)
    average_price = models.FloatField(default=None, null=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    objects = EveMarketPriceManager()

    def __str__(self) -> str:
        return f"{self.eve_type}: {self.average_price}"

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(eve_type='{self.eve_type}', "
            f"adjusted_price={self.adjusted_price}, average_price={self.average_price}, "
            f"updated_at={self.updated_at})"
        )


class EveRace(EveUniverseEntityModel):
    """A race in Eve Online"""

    alliance_id = models.PositiveIntegerField(db_index=True)
    description = models.TextField()

    class _EveUniverseMeta:
        esi_pk = "race_id"
        esi_path_list = "Universe.get_universe_races"
        esi_path_object = "Universe.get_universe_races"
        load_order = 150


class EveType(EveUniverseEntityModel):
    """An inventory type in Eve Online"""

    class Section(_SectionBase):
        """Sections that can be optionally loaded with each instance"""

        DOGMAS = "dogmas"  #:
        GRAPHICS = "graphics"  #:
        MARKET_GROUPS = "market_groups"  #:
        TYPE_MATERIALS = "type_materials"  #:
        INDUSTRY_ACTIVITIES = "industry_activities"  #:

    capacity = models.FloatField(default=None, null=True)
    description = models.TextField(default="")
    eve_group = models.ForeignKey(
        "EveGroup",
        on_delete=models.CASCADE,
        related_name="eve_types",
    )
    eve_graphic = models.ForeignKey(
        "EveGraphic",
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True,
        related_name="eve_types",
    )
    icon_id = models.PositiveIntegerField(default=None, null=True, db_index=True)
    eve_market_group = models.ForeignKey(
        "EveMarketGroup",
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True,
        related_name="eve_types",
    )
    mass = models.FloatField(default=None, null=True)
    packaged_volume = models.FloatField(default=None, null=True)
    portion_size = models.PositiveIntegerField(default=None, null=True)
    radius = models.FloatField(default=None, null=True)
    published = models.BooleanField()
    volume = models.FloatField(default=None, null=True)
    enabled_sections = BitField(
        flags=tuple(Section.values()),
        help_text=(
            "Flags for loadable sections. True if instance was loaded with section."
        ),  # no index, because MySQL does not support it for bitwise operations
    )  # type: ignore

    objects = EveTypeManager()

    class _EveUniverseMeta:
        esi_pk = "type_id"
        esi_path_list = "Universe.get_universe_types"
        esi_path_object = "Universe.get_universe_types_type_id"
        field_mappings = {
            "eve_graphic": "graphic_id",
            "eve_group": "group_id",
            "eve_market_group": "market_group_id",
        }
        inline_objects = {
            "dogma_attributes": "EveTypeDogmaAttribute",
            "dogma_effects": "EveTypeDogmaEffect",
        }
        load_order = 134

    @property
    def profile_url(self) -> str:
        """URL to display this type on the default third party webpage."""
        return eveitems.type_url(self.id)

    class IconVariant(enum.Enum):
        """Variant of icon to produce with `icon_url()`"""

        REGULAR = enum.auto()
        """anything, except blueprint or skin"""

        BPO = enum.auto()
        """blueprint original"""

        BPC = enum.auto()
        """blueprint copy"""

        SKIN = enum.auto()
        """SKIN"""

    def icon_url(
        self,
        size: int = EveUniverseEntityModel._DEFAULT_ICON_SIZE,
        variant: Optional[IconVariant] = None,
        category_id: Optional[int] = None,
        is_blueprint: Optional[bool] = None,
    ) -> str:
        """returns an image URL to this type as icon. Also works for blueprints and SKINs.

        Will try to auto-detect the variant based on the types's category,
        unless `variant` or `category_id` is specified.

        Args:
            variant: icon variant to use
            category_id: category ID of this type
            is_blueprint: DEPRECATED - type is assumed to be a blueprint
        """
        # if is_blueprint is not None:
        #    warnings.warn("is_blueprint in EveType.icon_url() is deprecated")

        if is_blueprint:
            variant = self.IconVariant.BPO

        if not variant:
            if not category_id:
                category_id = self.eve_group.eve_category_id

            if category_id == EveCategoryId.BLUEPRINT:
                variant = self.IconVariant.BPO

            elif category_id == EveCategoryId.SKIN:
                variant = self.IconVariant.SKIN

        if variant is self.IconVariant.BPO:
            return eveimageserver.type_bp_url(self.id, size=size)

        if variant is self.IconVariant.BPC:
            return eveimageserver.type_bpc_url(self.id, size=size)

        if variant is self.IconVariant.SKIN:
            size = EveUniverseEntityModel._DEFAULT_ICON_SIZE if not size else size
            if EVEUNIVERSE_USE_EVESKINSERVER:
                return eveskinserver.type_icon_url(self.id, size=size)

            if size < 32 or size > 128 or (size & (size - 1) != 0):
                raise ValueError(f"Invalid size: {size}")

            filename = f"eveuniverse/skin_generic_{size}.png"
            return staticfiles_storage.url(filename)

        return eveimageserver.type_icon_url(self.id, size=size)

    def render_url(self, size=EveUniverseEntityModel._DEFAULT_ICON_SIZE) -> str:
        """return an image URL to this type as render"""
        return eveimageserver.type_render_url(self.id, size=size)

    @classmethod
    def _disabled_fields(cls, enabled_sections: Optional[Set[str]] = None) -> set:
        enabled_sections = determine_effective_sections(enabled_sections)
        disabled_fields = set()
        if cls.Section.GRAPHICS not in enabled_sections:
            disabled_fields.add("eve_graphic")
        if cls.Section.MARKET_GROUPS not in enabled_sections:
            disabled_fields.add("eve_market_group")
        return disabled_fields

    @classmethod
    def _inline_objects(cls, enabled_sections: Optional[Set[str]] = None) -> dict:
        if not enabled_sections or cls.Section.DOGMAS not in enabled_sections:
            return {}
        return super()._inline_objects()

    @classmethod
    def eve_entity_category(cls) -> str:
        return EveEntity.CATEGORY_INVENTORY_TYPE


class EveTypeDogmaAttribute(EveUniverseInlineModel):
    """A dogma attribute of on inventory type in Eve Online"""

    eve_dogma_attribute = models.ForeignKey(
        "EveDogmaAttribute",
        on_delete=models.CASCADE,
        related_name="eve_type_dogma_attributes",
    )
    eve_type = models.ForeignKey(
        "EveType", on_delete=models.CASCADE, related_name="dogma_attributes"
    )
    value = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["eve_type", "eve_dogma_attribute"],
                name="fpk_evetypedogmaattribute",
            )
        ]

    class _EveUniverseMeta:
        parent_fk = "eve_type"
        functional_pk = [
            "eve_type",
            "eve_dogma_attribute",
        ]
        field_mappings = {"eve_dogma_attribute": "attribute_id"}
        load_order = 148


class EveTypeDogmaEffect(EveUniverseInlineModel):
    """A dogma effect of on inventory type in Eve Online"""

    eve_dogma_effect = models.ForeignKey(
        "EveDogmaEffect",
        on_delete=models.CASCADE,
        related_name="eve_type_dogma_effects",
    )
    eve_type = models.ForeignKey(
        "EveType", on_delete=models.CASCADE, related_name="dogma_effects"
    )
    is_default = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["eve_type", "eve_dogma_effect"],
                name="fpk_evetypedogmaeffect",
            )
        ]

    class _EveUniverseMeta:
        parent_fk = "eve_type"
        functional_pk = [
            "eve_type",
            "eve_dogma_effect",
        ]
        field_mappings = {"eve_dogma_effect": "effect_id"}
        load_order = 146
