from typing import Any, cast, Dict, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.app_config_field_type import AppConfigFieldType
from ..types import UNSET, Unset

T = TypeVar("T", bound="FieldDefinitionsManifest")


@attr.s(auto_attribs=True, repr=False)
class FieldDefinitionsManifest:
    """  """

    _name: str
    _is_multi: Union[Unset, None, bool] = UNSET
    _is_required: Union[Unset, None, bool] = UNSET
    _type: Union[Unset, AppConfigFieldType] = UNSET
    _description: Union[Unset, None, str] = UNSET
    _required_config: Union[Unset, bool] = False

    def __repr__(self):
        fields = []
        fields.append("name={}".format(repr(self._name)))
        fields.append("is_multi={}".format(repr(self._is_multi)))
        fields.append("is_required={}".format(repr(self._is_required)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("description={}".format(repr(self._description)))
        fields.append("required_config={}".format(repr(self._required_config)))
        return "FieldDefinitionsManifest({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        name = self._name
        is_multi = self._is_multi
        is_required = self._is_required
        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        description = self._description
        required_config = self._required_config

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if name is not UNSET:
            field_dict["name"] = name
        if is_multi is not UNSET:
            field_dict["isMulti"] = is_multi
        if is_required is not UNSET:
            field_dict["isRequired"] = is_required
        if type is not UNSET:
            field_dict["type"] = type
        if description is not UNSET:
            field_dict["description"] = description
        if required_config is not UNSET:
            field_dict["requiredConfig"] = required_config

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_name() -> str:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(str, UNSET)

        def get_is_multi() -> Union[Unset, None, bool]:
            is_multi = d.pop("isMulti")
            return is_multi

        try:
            is_multi = get_is_multi()
        except KeyError:
            if strict:
                raise
            is_multi = cast(Union[Unset, None, bool], UNSET)

        def get_is_required() -> Union[Unset, None, bool]:
            is_required = d.pop("isRequired")
            return is_required

        try:
            is_required = get_is_required()
        except KeyError:
            if strict:
                raise
            is_required = cast(Union[Unset, None, bool], UNSET)

        def get_type() -> Union[Unset, AppConfigFieldType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = AppConfigFieldType(_type)
                except ValueError:
                    type = AppConfigFieldType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, AppConfigFieldType], UNSET)

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

        field_definitions_manifest = cls(
            name=name,
            is_multi=is_multi,
            is_required=is_required,
            type=type,
            description=description,
            required_config=required_config,
        )

        return field_definitions_manifest

    @property
    def name(self) -> str:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def is_multi(self) -> Optional[bool]:
        """ Schema field's isMulti property, or null for either. """
        if isinstance(self._is_multi, Unset):
            raise NotPresentError(self, "is_multi")
        return self._is_multi

    @is_multi.setter
    def is_multi(self, value: Optional[bool]) -> None:
        self._is_multi = value

    @is_multi.deleter
    def is_multi(self) -> None:
        self._is_multi = UNSET

    @property
    def is_required(self) -> Optional[bool]:
        """ Schema field's isRequired property, or null for either. """
        if isinstance(self._is_required, Unset):
            raise NotPresentError(self, "is_required")
        return self._is_required

    @is_required.setter
    def is_required(self, value: Optional[bool]) -> None:
        self._is_required = value

    @is_required.deleter
    def is_required(self) -> None:
        self._is_required = UNSET

    @property
    def type(self) -> AppConfigFieldType:
        """ Schema field's type, or null for Any. """
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: AppConfigFieldType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET

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
