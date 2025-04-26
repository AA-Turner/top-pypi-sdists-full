from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.entity_schema_dependency_type import EntitySchemaDependencyType
from ..models.field_definitions_manifest import FieldDefinitionsManifest
from ..models.schema_dependency_subtypes import SchemaDependencySubtypes
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntitySchemaDependency")


@attr.s(auto_attribs=True, repr=False)
class EntitySchemaDependency:
    """  """

    _type: EntitySchemaDependencyType
    _name: str
    _subtype: Union[Unset, SchemaDependencySubtypes] = UNSET
    _field_definitions: Union[Unset, List[FieldDefinitionsManifest]] = UNSET
    _description: Union[Unset, None, str] = UNSET
    _required_config: Union[Unset, bool] = False

    def __repr__(self):
        fields = []
        fields.append("type={}".format(repr(self._type)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("subtype={}".format(repr(self._subtype)))
        fields.append("field_definitions={}".format(repr(self._field_definitions)))
        fields.append("description={}".format(repr(self._description)))
        fields.append("required_config={}".format(repr(self._required_config)))
        return "EntitySchemaDependency({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        type = self._type.value

        name = self._name
        subtype: Union[Unset, int] = UNSET
        if not isinstance(self._subtype, Unset):
            subtype = self._subtype.value

        field_definitions: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._field_definitions, Unset):
            field_definitions = []
            for field_definitions_item_data in self._field_definitions:
                field_definitions_item = field_definitions_item_data.to_dict()

                field_definitions.append(field_definitions_item)

        description = self._description
        required_config = self._required_config

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if type is not UNSET:
            field_dict["type"] = type
        if name is not UNSET:
            field_dict["name"] = name
        if subtype is not UNSET:
            field_dict["subtype"] = subtype
        if field_definitions is not UNSET:
            field_dict["fieldDefinitions"] = field_definitions
        if description is not UNSET:
            field_dict["description"] = description
        if required_config is not UNSET:
            field_dict["requiredConfig"] = required_config

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_type() -> EntitySchemaDependencyType:
            _type = d.pop("type")
            try:
                type = EntitySchemaDependencyType(_type)
            except ValueError:
                type = EntitySchemaDependencyType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(EntitySchemaDependencyType, UNSET)

        def get_name() -> str:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(str, UNSET)

        def get_subtype() -> Union[Unset, SchemaDependencySubtypes]:
            subtype = UNSET
            _subtype = d.pop("subtype")
            if _subtype is not None and _subtype is not UNSET:
                try:
                    subtype = SchemaDependencySubtypes(_subtype)
                except ValueError:
                    subtype = SchemaDependencySubtypes.of_unknown(_subtype)

            return subtype

        try:
            subtype = get_subtype()
        except KeyError:
            if strict:
                raise
            subtype = cast(Union[Unset, SchemaDependencySubtypes], UNSET)

        def get_field_definitions() -> Union[Unset, List[FieldDefinitionsManifest]]:
            field_definitions = []
            _field_definitions = d.pop("fieldDefinitions")
            for field_definitions_item_data in _field_definitions or []:
                field_definitions_item = FieldDefinitionsManifest.from_dict(
                    field_definitions_item_data, strict=False
                )

                field_definitions.append(field_definitions_item)

            return field_definitions

        try:
            field_definitions = get_field_definitions()
        except KeyError:
            if strict:
                raise
            field_definitions = cast(Union[Unset, List[FieldDefinitionsManifest]], UNSET)

        def get_description() -> Union[Unset, None, str]:
            description = d.pop("description")
            return description

        try:
            description = get_description()
        except KeyError:
            if strict:
                raise
            description = cast(Union[Unset, None, str], UNSET)

        def get_required_config() -> Union[Unset, bool]:
            required_config = d.pop("requiredConfig")
            return required_config

        try:
            required_config = get_required_config()
        except KeyError:
            if strict:
                raise
            required_config = cast(Union[Unset, bool], UNSET)

        entity_schema_dependency = cls(
            type=type,
            name=name,
            subtype=subtype,
            field_definitions=field_definitions,
            description=description,
            required_config=required_config,
        )

        return entity_schema_dependency

    @property
    def type(self) -> EntitySchemaDependencyType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: EntitySchemaDependencyType) -> None:
        self._type = value

    @property
    def name(self) -> str:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def subtype(self) -> SchemaDependencySubtypes:
        if isinstance(self._subtype, Unset):
            raise NotPresentError(self, "subtype")
        return self._subtype

    @subtype.setter
    def subtype(self, value: SchemaDependencySubtypes) -> None:
        self._subtype = value

    @subtype.deleter
    def subtype(self) -> None:
        self._subtype = UNSET

    @property
    def field_definitions(self) -> List[FieldDefinitionsManifest]:
        if isinstance(self._field_definitions, Unset):
            raise NotPresentError(self, "field_definitions")
        return self._field_definitions

    @field_definitions.setter
    def field_definitions(self, value: List[FieldDefinitionsManifest]) -> None:
        self._field_definitions = value

    @field_definitions.deleter
    def field_definitions(self) -> None:
        self._field_definitions = UNSET

    @property
    def description(self) -> Optional[str]:
        if isinstance(self._description, Unset):
            raise NotPresentError(self, "description")
        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:
        self._description = value

    @description.deleter
    def description(self) -> None:
        self._description = UNSET

    @property
    def required_config(self) -> bool:
        if isinstance(self._required_config, Unset):
            raise NotPresentError(self, "required_config")
        return self._required_config

    @required_config.setter
    def required_config(self, value: bool) -> None:
        self._required_config = value

    @required_config.deleter
    def required_config(self) -> None:
        self._required_config = UNSET
