"""Base models for Eve Universe."""

import enum
from typing import Any, Dict, Iterable, List, NamedTuple, Optional, Set, Tuple

from django.apps import apps
from django.db import models

from eveuniverse.app_settings import (
    EVEUNIVERSE_LOAD_ASTEROID_BELTS,
    EVEUNIVERSE_LOAD_DOGMAS,
    EVEUNIVERSE_LOAD_GRAPHICS,
    EVEUNIVERSE_LOAD_INDUSTRY_ACTIVITIES,
    EVEUNIVERSE_LOAD_MARKET_GROUPS,
    EVEUNIVERSE_LOAD_MOONS,
    EVEUNIVERSE_LOAD_PLANETS,
    EVEUNIVERSE_LOAD_STARGATES,
    EVEUNIVERSE_LOAD_STARS,
    EVEUNIVERSE_LOAD_STATIONS,
    EVEUNIVERSE_LOAD_TYPE_MATERIALS,
)
from eveuniverse.managers.universe import EveUniverseEntityModelManager

_NAMES_MAX_LENGTH = 100


class _EsiFieldMapping(NamedTuple):
    """Mapping of a model field to parse related object data from an ESI endpoint."""

    esi_name: str  # Name of the field in ESI data
    is_optional: bool
    is_pk: bool
    is_fk: bool
    related_model: Optional[Any]
    is_parent_fk: bool
    is_charfield: bool
    create_related: bool


class _SectionBase(str, enum.Enum):
    """Base class for all Sections"""

    @classmethod
    def values(cls) -> list:
        """Return values for the sections."""
        return list(item.value for item in cls)

    def __str__(self) -> str:
        return self.value


class EveUniverseBaseModel(models.Model):
    """Base class for all Eve Universe Models.

    :meta private:
    """

    class Meta:
        abstract = True

    def __repr__(self) -> str:
        """General purpose __repr__ that works for all model classes"""
        fields = sorted(
            [
                f
                for f in self._meta.get_fields()
                if isinstance(f, models.Field) and f.name != "last_updated"
            ],
            key=lambda x: x.name,
        )
        fields_2 = []
        for field in fields:
            if field.many_to_one or field.one_to_one:
                name = f"{field.name}_id"
                value = getattr(self, name)
            elif field.many_to_many:
                name = field.name
                value = ", ".join(
                    sorted([str(x) for x in getattr(self, field.name).all()])
                )
            else:
                name = field.name
                value = getattr(self, field.name)

            if isinstance(value, str):
                if isinstance(field, models.TextField) and len(value) > 32:
                    value = f"{value[:32]}..."
                text = f"{name}='{value}'"
            else:
                text = f"{name}={value}"

            fields_2.append(text)

        return f"{self.__class__.__name__}({', '.join(fields_2)})"

    @classmethod
    def all_models(cls) -> List[Dict[Any, int]]:
        """Return a list of all Eve Universe model classes sorted by load order."""
        mappings = []
        for model_class in apps.get_models():
            if model_class._meta.app_label != "eveuniverse":
                continue

            if issubclass(
                model_class, (EveUniverseEntityModel, EveUniverseInlineModel)
            ) and model_class not in (
                cls,
                EveUniverseEntityModel,
                EveUniverseInlineModel,
            ):
                mappings.append(
                    {
                        "model": model_class,
                        "load_order": model_class._eve_universe_meta_attr_strict(
                            "load_order"
                        ),
                    }
                )

        return [
            mapping["model"]
            for mapping in sorted(mappings, key=lambda obj: obj["load_order"])
        ]

    @classmethod
    def get_model_class(cls, model_name: str):
        """Return the model class for the given name or raise error when not found."""
        model_class = apps.get_model("eveuniverse", model_name)
        if not issubclass(model_class, (EveUniverseBaseModel, EveUniverseInlineModel)):
            raise TypeError("Invalid model class")
        return model_class

    @classmethod
    def _esi_pk(cls) -> str:
        """Return the name of the pk column on ESI that must exist."""
        return cls._eve_universe_meta_attr_strict("esi_pk")

    @classmethod
    def _esi_field_mappings(
        cls, enabled_sections: Optional[Set[str]] = None
    ) -> Dict[str, _EsiFieldMapping]:
        """Return ESI field mappings for this model."""
        explicit_field_mappings = cls._eve_universe_meta_attr("field_mappings")
        functional_pk = cls._eve_universe_meta_attr("functional_pk")
        parent_fk = cls._eve_universe_meta_attr("parent_fk")
        dont_create_related = cls._eve_universe_meta_attr("dont_create_related")
        disabled_fields = cls._disabled_fields(enabled_sections)

        field_mappings: Dict[str, _EsiFieldMapping] = {}
        relevant_fields = [
            field
            for field in cls._meta.get_fields()
            if not field.auto_created
            and field.name not in {"last_updated", "enabled_sections"}
            and field.name not in disabled_fields
            and not field.many_to_many
        ]
        for field in relevant_fields:
            if explicit_field_mappings and field.name in explicit_field_mappings:
                esi_name = explicit_field_mappings[field.name]
            else:
                esi_name = field.name

            if getattr(field, "primary_key") is True:
                is_pk = True
                esi_name = cls._esi_pk()
            elif functional_pk and field.name in functional_pk:
                is_pk = True
            else:
                is_pk = False

            if isinstance(field, models.ForeignKey):
                is_fk = True
                related_model = field.related_model
            else:
                is_fk = False
                related_model = None

            try:
                is_optional = field.has_default()  # type: ignore
            except AttributeError:
                is_optional = False

            field_mappings[field.name] = _EsiFieldMapping(
                esi_name=esi_name,
                is_optional=is_optional,
                is_pk=is_pk,
                is_fk=is_fk,
                related_model=related_model,
                is_parent_fk=bool(parent_fk and is_pk and field.name in parent_fk),
                is_charfield=isinstance(field, (models.CharField, models.TextField)),
                create_related=not (
                    dont_create_related and field.name in dont_create_related
                ),
            )

        return field_mappings

    @classmethod
    def _disabled_fields(cls, _enabled_sections: Optional[Set[str]] = None) -> set:
        """Return name of fields that must not be loaded from ESI."""
        return set()

    @classmethod
    def _eve_universe_meta_attr(cls, attr_name: str) -> Optional[Any]:
        """Return value of an attribute from EveUniverseMeta or None"""
        return cls._eve_universe_meta_attr_flexible(attr_name, is_mandatory=False)

    @classmethod
    def _eve_universe_meta_attr_strict(cls, attr_name: str) -> Any:
        """Return value of an attribute from EveUniverseMeta or raise exception."""
        return cls._eve_universe_meta_attr_flexible(attr_name, is_mandatory=True)

    @classmethod
    def _eve_universe_meta_attr_flexible(
        cls, attr_name: str, is_mandatory: bool = False
    ) -> Optional[Any]:
        try:
            value = getattr(cls._EveUniverseMeta, attr_name)  # type: ignore
        except AttributeError:
            value = None
            if is_mandatory:
                raise ValueError(
                    f"Mandatory attribute EveUniverseMeta.{attr_name} not defined "
                    f"for class {cls.__name__}"
                ) from None

        return value

    @classmethod
    def _defaults_from_esi_obj(
        cls, eve_data_obj: dict, enabled_sections: Optional[Set[str]] = None
    ) -> Dict[str, Any]:
        """Return defaults from an esi data object
        for update/creating objects of this model.
        """
        defaults: Dict[str, Any] = {}
        for field_name, field_mapping in cls._esi_field_mappings(
            enabled_sections
        ).items():
            if field_mapping.is_pk:
                continue

            if not isinstance(field_mapping.esi_name, tuple):
                esi_value = cls._esi_value_from_tuple(eve_data_obj, field_mapping)
            else:
                esi_value = cls._esi_value_from_non_tuple(eve_data_obj, field_mapping)

            if esi_value is not None:
                if field_mapping.is_fk:
                    value = cls._gather_value_from_fk(field_mapping, esi_value)

                else:
                    if field_mapping.is_charfield and esi_value is None:
                        value = ""
                    else:
                        value = esi_value

                defaults[field_name] = value

        return defaults

    @staticmethod
    def _esi_value_from_tuple(
        eve_data_obj: dict, field_mapping: _EsiFieldMapping
    ) -> Optional[Any]:
        if field_mapping.esi_name in eve_data_obj:
            return eve_data_obj[field_mapping.esi_name]
        return None

    @staticmethod
    def _esi_value_from_non_tuple(
        eve_data_obj: dict, field_mapping: _EsiFieldMapping
    ) -> Optional[Any]:
        if (
            field_mapping.esi_name[0] in eve_data_obj
            and field_mapping.esi_name[1] in eve_data_obj[field_mapping.esi_name[0]]
        ):
            return eve_data_obj[field_mapping.esi_name[0]][field_mapping.esi_name[1]]

        return None

    @staticmethod
    def _gather_value_from_fk(field_mapping, esi_value):
        parent_class = field_mapping.related_model
        try:
            value = parent_class.objects.get(id=esi_value)
        except parent_class.DoesNotExist:
            value = None
            if field_mapping.create_related:
                try:
                    value = parent_class.objects.update_or_create_esi(
                        id=esi_value, include_children=False, wait_for_children=True
                    )[0]
                except AttributeError:
                    pass
        return value


class EveUniverseEntityModel(EveUniverseBaseModel):
    """Base class for Eve Universe Entity models.

    Entity models are normal Eve entities that have a dedicated ESI endpoint.

    :meta private:
    """

    class Section(_SectionBase):
        """A section represents a related data topic to be loaded
        when fetching data from ESI, e.g. dogmas for types.
        """

    # sections
    LOAD_DOGMAS = "dogmas"
    # TODO: Implement other sections

    # icons
    _DEFAULT_ICON_SIZE = 64

    id = models.PositiveIntegerField(primary_key=True, help_text="Eve Online ID")
    name = models.CharField(
        max_length=_NAMES_MAX_LENGTH,
        default="",
        db_index=True,
        help_text="Eve Online name",
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        help_text="When this object was last updated from ESI",
        db_index=True,
    )

    objects = EveUniverseEntityModelManager()

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name

    # pylint: disable = no-member
    def set_updated_sections(self, enabled_sections: Optional[Set[str]]) -> bool:
        """Set updated sections for this object."""
        if not enabled_sections or not hasattr(self, "enabled_sections"):
            return False

        updated_sections = False
        old_value = self.enabled_sections.mask
        for section in enabled_sections:
            if str(section) in self.Section.values():
                setattr(self.enabled_sections, section, True)
                updated_sections = True

        has_changed = self.enabled_sections.mask != old_value
        if not updated_sections or not has_changed:
            return False

        self.save()
        return True

    @classmethod
    def _update_or_create_children(
        cls,
        *,
        parent_eve_data_obj: dict,
        include_children: bool,
        wait_for_children: bool,
        enabled_sections: Set[str],
        task_priority: Optional[int] = None,
    ) -> None:
        """Update or creates child objects as defined for this parent model (if any)."""
        from eveuniverse.tasks import (
            update_or_create_eve_object as task_update_or_create_eve_object,
        )

        if not parent_eve_data_obj:
            raise ValueError(
                f"{cls.__name__}: Tried to create children from empty parent object"
            )

        for key, child_class in cls._children(enabled_sections).items():
            if key in parent_eve_data_obj and parent_eve_data_obj[key]:
                for obj in parent_eve_data_obj[key]:
                    # TODO: Refactor this hack
                    id = obj["planet_id"] if key == "planets" else obj
                    if wait_for_children:
                        child_model_class = cls.get_model_class(child_class)
                        child_model_class.objects.update_or_create_esi(  # type: ignore
                            id=id,
                            include_children=include_children,
                            wait_for_children=wait_for_children,
                            enabled_sections=enabled_sections,
                            task_priority=task_priority,
                        )

                    else:
                        params: Dict[str, Any] = {
                            "kwargs": {
                                "model_name": child_class,
                                "id": id,
                                "include_children": include_children,
                                "wait_for_children": wait_for_children,
                                "enabled_sections": list(enabled_sections),
                                "task_priority": task_priority,
                            },
                        }
                        if task_priority:
                            params["priority"] = task_priority
                        task_update_or_create_eve_object.apply_async(**params)  # type: ignore

    @classmethod
    def _update_or_create_inline_objects(
        cls,
        *,
        parent_eve_data_obj: dict,
        parent_obj,
        wait_for_children: bool,
        enabled_sections: Set[str],
        task_priority: Optional[int] = None,
    ) -> None:
        """Updates or create eve objects that are returned "inline" from ESI
        for the parent eve objects as defined for this parent model (if any).
        """
        from eveuniverse.tasks import (
            update_or_create_inline_object as task_update_or_create_inline_object,
        )

        inline_objects = cls._inline_objects(enabled_sections)
        if not inline_objects:
            return

        if not parent_eve_data_obj or not parent_obj:
            raise ValueError(
                f"{cls.__name__}: Tried to create inline object "
                "from empty parent object"
            )

        for inline_field, inline_model_name in inline_objects.items():
            if (
                inline_field not in parent_eve_data_obj
                or not parent_eve_data_obj[inline_field]
            ):
                continue

            parent_fk, parent2_model_name, other_pk_info = cls._identify_parent(
                inline_model_name
            )

            for eve_data_obj in parent_eve_data_obj[inline_field]:
                if wait_for_children:
                    cls._update_or_create_inline_object(
                        parent_obj_id=parent_obj.id,
                        parent_fk=parent_fk,
                        eve_data_obj=eve_data_obj,
                        other_pk_info=other_pk_info,
                        parent2_model_name=parent2_model_name,
                        inline_model_name=inline_model_name,
                        enabled_sections=enabled_sections,
                    )
                else:
                    params: Dict[str, Any] = {
                        "kwargs": {
                            "parent_obj_id": parent_obj.id,
                            "parent_fk": parent_fk,
                            "eve_data_obj": eve_data_obj,
                            "other_pk_info": other_pk_info,
                            "parent2_model_name": parent2_model_name,
                            "inline_model_name": inline_model_name,
                            "parent_model_name": type(parent_obj).__name__,
                            "enabled_sections": list(enabled_sections),
                        }
                    }
                    if task_priority:
                        params["priority"] = task_priority
                    task_update_or_create_inline_object.apply_async(**params)  # type: ignore

    @classmethod
    def _identify_parent(cls, inline_model_name: str) -> tuple:
        inline_model_class = cls.get_model_class(inline_model_name)
        esi_mapping = inline_model_class._esi_field_mappings()
        parent_fk = None
        other_pk = None
        parent_class_2 = None
        for field_name, mapping in esi_mapping.items():
            if mapping.is_pk:
                if mapping.is_parent_fk:
                    parent_fk = field_name
                else:
                    other_pk = (field_name, mapping)
                    parent_class_2 = mapping.related_model

        if not parent_fk or not other_pk:
            raise ValueError(
                f"ESI Mapping for {inline_model_name} not valid: {parent_fk}, {other_pk}"
            )

        parent2_model_name = parent_class_2.__name__ if parent_class_2 else None
        other_pk_info = {
            "name": other_pk[0],
            "esi_name": other_pk[1].esi_name,
            "is_fk": other_pk[1].is_fk,
        }
        return parent_fk, parent2_model_name, other_pk_info

    @classmethod
    def _update_or_create_inline_object(
        cls,
        parent_obj_id: int,
        parent_fk: str,
        eve_data_obj: dict,
        other_pk_info: Dict[str, Any],
        parent2_model_name: str,
        inline_model_name: str,
        enabled_sections: Set[str],
    ):
        """Update or create a single inline object.

        Will automatically create additional parent objects as needed
        """
        inline_model_class = cls.get_model_class(inline_model_name)

        params: Dict[str, Any] = {f"{parent_fk}_id": parent_obj_id}
        esi_value = eve_data_obj.get(other_pk_info["esi_name"])
        if other_pk_info["is_fk"]:
            parent_class_2 = cls.get_model_class(parent2_model_name)
            try:
                value = parent_class_2.objects.get(id=esi_value)
            except parent_class_2.DoesNotExist:
                try:
                    value, _ = parent_class_2.objects.update_or_create_esi(  # type: ignore
                        id=esi_value, enabled_sections=enabled_sections
                    )
                except AttributeError:
                    value = None
        else:
            value = esi_value

        key = other_pk_info["name"]
        params[key] = value
        params["defaults"] = inline_model_class._defaults_from_esi_obj(
            eve_data_obj, enabled_sections=enabled_sections
        )
        inline_model_class.objects.update_or_create(**params)

    @classmethod
    def eve_entity_category(cls) -> str:
        """Return the EveEntity category of this model if one exists
        else an empty string.
        """
        return ""

    @classmethod
    def _has_esi_path_list(cls) -> bool:
        return bool(cls._eve_universe_meta_attr("esi_path_list"))

    @classmethod
    def _esi_path_list(cls) -> Tuple[str, str]:
        return cls._esi_path("list")

    @classmethod
    def _esi_path_object(cls) -> Tuple[str, str]:
        return cls._esi_path("object")

    @classmethod
    def _esi_path(cls, variant: str) -> Tuple[str, str]:
        attr_name = f"esi_path_{str(variant)}"
        path = cls._eve_universe_meta_attr_strict(attr_name)
        if len(path.split(".")) != 2:
            raise ValueError(f"{attr_name} not valid")
        return path.split(".")

    @classmethod
    def _children(cls, _enabled_sections: Optional[Iterable[str]] = None) -> dict:
        """returns the mapping of children for this class"""
        mappings = cls._eve_universe_meta_attr("children")
        return mappings if mappings else {}

    @classmethod
    def _sections_need_children(cls) -> Set[Section]:
        """Return sections of this model, which require loading of children."""
        return {section for section in cls.Section if cls._children({section})}

    @classmethod
    def _inline_objects(cls, _enabled_sections: Optional[Iterable[str]] = None) -> dict:
        """returns a dict of inline objects if any"""
        inline_objects = cls._eve_universe_meta_attr("inline_objects")
        return inline_objects if inline_objects else {}

    @classmethod
    def _is_list_only_endpoint(cls) -> bool:
        esi_path_list = cls._eve_universe_meta_attr("esi_path_list")
        esi_path_object = cls._eve_universe_meta_attr("esi_path_object")
        return (
            bool(esi_path_list)
            and bool(esi_path_object)
            and esi_path_list == esi_path_object
        )


class EveUniverseInlineModel(EveUniverseBaseModel):
    """Base class for Eve Universe Inline models.

    Inline models are objects which do not have a dedicated ESI endpoint and are
    provided through the endpoint of another entity

    This class is also used for static Eve data.

    :meta private:
    """

    class Meta:
        abstract = True


def determine_effective_sections(
    enabled_sections: Optional[Iterable[str]] = None,
) -> Set[str]:
    """Determine currently effective sections.

    :meta private:
    """
    from .universe_1 import EveType
    from .universe_2 import EvePlanet, EveSolarSystem

    enabled_sections = set(enabled_sections) if enabled_sections else set()
    if EVEUNIVERSE_LOAD_ASTEROID_BELTS:
        enabled_sections.add(EvePlanet.Section.ASTEROID_BELTS.value)
    if EVEUNIVERSE_LOAD_DOGMAS:
        enabled_sections.add(EveType.Section.DOGMAS.value)
    if EVEUNIVERSE_LOAD_GRAPHICS:
        enabled_sections.add(EveType.Section.GRAPHICS.value)
    if EVEUNIVERSE_LOAD_MARKET_GROUPS:
        enabled_sections.add(EveType.Section.MARKET_GROUPS.value)
    if EVEUNIVERSE_LOAD_MOONS:
        enabled_sections.add(EvePlanet.Section.MOONS.value)
    if EVEUNIVERSE_LOAD_PLANETS:
        enabled_sections.add(EveSolarSystem.Section.PLANETS.value)
    if EVEUNIVERSE_LOAD_STARGATES:
        enabled_sections.add(EveSolarSystem.Section.STARGATES.value)
    if EVEUNIVERSE_LOAD_STARS:
        enabled_sections.add(EveSolarSystem.Section.STARS.value)
    if EVEUNIVERSE_LOAD_STATIONS:
        enabled_sections.add(EveSolarSystem.Section.STATIONS.value)
    if EVEUNIVERSE_LOAD_TYPE_MATERIALS:
        enabled_sections.add(EveType.Section.TYPE_MATERIALS.value)
    if EVEUNIVERSE_LOAD_INDUSTRY_ACTIVITIES:
        enabled_sections.add(EveType.Section.INDUSTRY_ACTIVITIES.value)
    return enabled_sections
