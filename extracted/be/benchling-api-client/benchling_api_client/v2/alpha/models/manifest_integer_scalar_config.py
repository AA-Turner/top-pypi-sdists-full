from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.manifest_integer_scalar_config_type import ManifestIntegerScalarConfigType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ManifestIntegerScalarConfig")


@attr.s(auto_attribs=True, repr=False)
class ManifestIntegerScalarConfig:
    """  """

    _type: ManifestIntegerScalarConfigType
    _name: str
    _enum: Union[Unset, List[int]] = UNSET
    _description: Union[Unset, None, str] = UNSET
    _required_config: Union[Unset, bool] = False

    def __repr__(self):
        fields = []
        fields.append("type={}".format(repr(self._type)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("enum={}".format(repr(self._enum)))
        fields.append("description={}".format(repr(self._description)))
        fields.append("required_config={}".format(repr(self._required_config)))
        return "ManifestIntegerScalarConfig({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        type = self._type.value

        name = self._name
        enum: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._enum, Unset):
            enum = self._enum

        description = self._description
        required_config = self._required_config

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if type is not UNSET:
            field_dict["type"] = type
        if name is not UNSET:
            field_dict["name"] = name
        if enum is not UNSET:
            field_dict["enum"] = enum
        if description is not UNSET:
            field_dict["description"] = description
        if required_config is not UNSET:
            field_dict["requiredConfig"] = required_config

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_type() -> ManifestIntegerScalarConfigType:
            _type = d.pop("type")
            try:
                type = ManifestIntegerScalarConfigType(_type)
            except ValueError:
                type = ManifestIntegerScalarConfigType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(ManifestIntegerScalarConfigType, UNSET)

        def get_name() -> str:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(str, UNSET)

        def get_enum() -> Union[Unset, List[int]]:
            enum = cast(List[int], d.pop("enum"))

            return enum

        try:
            enum = get_enum()
        except KeyError:
            if strict:
                raise
            enum = cast(Union[Unset, List[int]], UNSET)

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

        manifest_integer_scalar_config = cls(
            type=type,
            name=name,
            enum=enum,
            description=description,
            required_config=required_config,
        )

        return manifest_integer_scalar_config

    @property
    def type(self) -> ManifestIntegerScalarConfigType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: ManifestIntegerScalarConfigType) -> None:
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
    def enum(self) -> List[int]:
        if isinstance(self._enum, Unset):
            raise NotPresentError(self, "enum")
        return self._enum

    @enum.setter
    def enum(self, value: List[int]) -> None:
        self._enum = value

    @enum.deleter
    def enum(self) -> None:
        self._enum = UNSET

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
