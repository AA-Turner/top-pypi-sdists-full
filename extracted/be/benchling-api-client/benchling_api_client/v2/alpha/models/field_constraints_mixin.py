from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.app_config_field_type import AppConfigFieldType
from ..types import UNSET, Unset

T = TypeVar("T", bound="FieldConstraintsMixin")


@attr.s(auto_attribs=True, repr=False)
class FieldConstraintsMixin:
    """  """

    _is_multi: Union[Unset, None, bool] = UNSET
    _is_required: Union[Unset, None, bool] = UNSET
    _type: Union[Unset, AppConfigFieldType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("is_multi={}".format(repr(self._is_multi)))
        fields.append("is_required={}".format(repr(self._is_required)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "FieldConstraintsMixin({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        is_multi = self._is_multi
        is_required = self._is_required
        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if is_multi is not UNSET:
            field_dict["isMulti"] = is_multi
        if is_required is not UNSET:
            field_dict["isRequired"] = is_required
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

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

        field_constraints_mixin = cls(
            is_multi=is_multi,
            is_required=is_required,
            type=type,
        )

        field_constraints_mixin.additional_properties = d
        return field_constraints_mixin

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

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
